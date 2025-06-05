from __future__ import annotations
from types import SimpleNamespace
from typing import List, Tuple, cast, Any, Dict, TYPE_CHECKING

import threading
from .utils.logger import smart_print, setup, _config, _ensure_rich_traceback_installed, Console
from .utils.debug import debug_print

if TYPE_CHECKING:
    import brainyflow as bf
else:
    from .brainyflow_original import bf

debug_print(f"Internal 'bf' alias for base is {bf}, from file: {getattr(bf, '__file__', 'Unknown location')}")

#############################################################################################################
# Pure Exports
#############################################################################################################

DEFAULT_ACTION = bf.DEFAULT_ACTION
Action = bf.Action
SharedStore = bf.SharedStore
M = bf.M
T = bf.T
PrepResultT = bf.PrepResultT
ExecResultT = bf.ExecResultT
ActionT = bf.ActionT
AnyNode = bf.AnyNode
ExecutionTree = bf.ExecutionTree
Trigger = bf.Trigger
_get_from_stores = bf._get_from_stores
_delete_from_stores = bf._delete_from_stores
LocalProxy = bf.LocalProxy
NodeError = bf.NodeError

#############################################################################################################
# Memory
#############################################################################################################

class VerboseMemoryRunnerMixin:
    """
    A mixin for BaseMemory derivatives (especially Flow) to print execution logs
    in a user-friendly way.
    """
    
    @property
    def _refer(self):
        return SimpleNamespace(
            me=f"[white]{self.__class__.__name__}[/white]",
            attr=lambda key: f"{self._refer.me}.[bold]{key}[/bold]",
        )
    
    def _set_value(self, key: str, value: Any) -> None:
        super()._set_value(key, value)
        if key.startswith("__") and key.endswith("__"):
            return        
        smart_print(self._refer.attr(key), "=", value, single_line=True)

class Memory(VerboseMemoryRunnerMixin, bf.Memory[bf.M]):
    pass

#############################################################################################################
# Node
#############################################################################################################

class VerboseNodeRunnerMixin:
    """
    A mixin for BaseNode derivatives (especially Flow) to print execution logs
    in a user-friendly way.
    """
    
    @property
    def _refer(self):
        return SimpleNamespace(
            me=f"[bold yellow]{self.__class__.__name__}[/bold yellow][white]#{self._node_order}[/white]",
        )

    async def exec_runner(self, *args, **kwargs) -> Any:
        smart_print(f"{self._refer.me}.prep() →", args[1], single_line=True)
        exec_res = await super().exec_runner(*args, **kwargs)
        smart_print(f"{self._refer.me}.exec() →", exec_res, single_line=True)
        return exec_res

    async def run(self, *args, **kwargs):
        result = await super().run(*args, **kwargs)
        propagate: bool = kwargs.get('propagate', args[1] if len(args) > 1 and isinstance(args[1], bool) else False)
        if not propagate:
            smart_print(f"{self._refer.me}.run() → {result}", single_line=True)
            return result
    
        smart_print(f"{self._refer.me}.post():")
        if (len(result) == 1 and result[0][0] == 'default' and len(self._triggers) == 0):
            smart_print(f"\t[dim italic]> Leaf Node[/dim italic]")
        else:
            for key, value in result:
                smart_print(f"\t- [blue]{key}[/blue]\t >> ", ", ".join(f"[green]{c.__class__.__name__}[/green]#{c._node_order}" for c in self.get_next_nodes(key)) or f"[dim red]Terminal Action[/dim red]")

        return result

class SingleThreadedMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._lock = threading.Lock()

    async def run(self, **kwargs):
        smart_print(f"Acquiring lock for single-threaded execution in {self.__class__.__name__}...")
        self._lock.acquire()
        try:
            return await super().run(**kwargs)
        finally:
            smart_print(f"Releasing lock for {self.__class__.__name__}.")
            self._lock.release()

class Node(VerboseNodeRunnerMixin, bf.Node[bf.M, bf.PrepResultT, bf.ExecResultT, bf.ActionT]):
    pass

###################################################################################################################
# Flow
###################################################################################################################
ExecutionTree = Dict[str, Any] 
Action = str 

class ExecutionLogTreePrinterMixin:
    """
    A mixin for BaseNode derivatives (especially Flow) to print execution logs
    in a user-friendly way.
    - If run with propagate=False on a Flow producing an ExecutionTree, prints a tree.
    - If run with propagate=True on any BaseNode, prints triggered actions and successors.
    """
    async def run(self, *args: Any, **kwargs: Any) -> Any:
        result = await super().run(*args, **kwargs) # type: ignore
        _ensure_rich_traceback_installed()
        effective_propagate: bool = kwargs.get('propagate', args[1] if len(args) > 1 and isinstance(args[1], bool) else False)

        # `self` must be a BaseNode derivative to have _node_order and get_next_nodes.
        # These checks ensure we don't try to access attributes that might not exist.
        if not hasattr(self, '_node_order') or not isinstance(getattr(self, '_node_order', None), int):
            return result

        class_name = self.__class__.__name__
        node_order_val = getattr(self, '_node_order', 'UnknownID')

        if not effective_propagate:
            # This branch handles propagate=False. For Flows, this typically returns ExecutionTree.
            if (isinstance(result, dict) and all(k in result for k in ['order', 'type', 'triggered'])):
                log_tree_data = cast(ExecutionTree, result)
                title = f"Execution Path for {class_name}#{node_order_val}"
                if _config.output_mode == "rich" and isinstance(_config.output_handler, Console):
                    _config.output_handler.rule(f"[bold cyan]{title}", style="cyan", characters="═")
                    self._recursive_print_execution_log(log_tree_data, prefix="", is_last_sibling=True)
                    _config.output_handler.rule(style="cyan", characters="═")
                else: 
                    rule_line = "═" * (len(title) + 4) if len(title) < 76 else "═" * 80 # Adjusted for typical console
                    smart_print(rule_line)
                    smart_print(f"  {title}  ")
                    self._recursive_print_execution_log(log_tree_data, prefix="", is_last_sibling=True)
                    smart_print(rule_line)
            else:
                # Fallback: If not propagate and result isn't an ExecutionTree, print basic result.
                # This matches the old VerboseNodeRunnerMixin's behavior for this case.
                smart_print(f">>>>>>> Result for {class_name}[#{node_order_val}]: {result}")
        
        else: # effective_propagate is True
            # This branch handles propagate=True, expects List[Tuple[Action, Memory]] from BaseNode.run.
            if isinstance(result, list) and all(isinstance(item, tuple) and len(item) == 2 for item in result):
                triggers_list = cast(List[Tuple[Action, Any]], result)
                smart_print(f"Triggered in [bold yellow]{class_name}[/bold yellow]#{node_order_val}:")
                if hasattr(self, 'get_next_nodes') and callable(self.get_next_nodes):
                    for action_name_triggered, _ in triggers_list:
                        try:
                            next_nodes = self.get_next_nodes(action_name_triggered) # type: ignore
                            successors = ", ".join(
                                f"[green]{n.__class__.__name__}[/green]#{getattr(n, '_node_order', 'ID?')}" for n in next_nodes
                            ) or f"[red]Terminal Action[/red]"
                            smart_print(f"\t- [blue]{action_name_triggered}[/blue]\t >> ", successors)
                        except Exception as e:
                            # Gracefully handle errors during successor fetching for logging
                            smart_print(f"\t- [blue]{action_name_triggered}[/blue]\t >> [bold red]Error getting successors: {e}[/bold red]")
                else:
                    # Fallback if get_next_nodes is somehow not available
                    for action_name_triggered, _ in triggers_list:
                        smart_print(f"\t- [blue]{action_name_triggered}[/blue]\t >> [dim](Successor info unavailable)[/dim]")
            else:
                # If propagate=True but result is not the expected list of triggers.
                smart_print(f"Triggers from [bold yellow]{class_name}[/bold yellow]#{node_order_val} (propagate=True): {result} ([italic]unexpected format[/italic])")

        return result

    def _recursive_print_execution_log(self, current_log_node: ExecutionTree, prefix: str, is_last_sibling: bool):
        """
        Recursively prints the execution log in a tree structure.
        Highlights structural path endings based on the ExecutionTree content.
        """
        connector = "└── " if is_last_sibling else "├── "
        node_type = current_log_node.get('type', 'UnknownType')
        node_order = current_log_node.get('order', 'UnknownID')
        smart_print(f"{prefix}{connector}[green bold]{node_type}[/green bold]#[green]{node_order}[/green]")

        children_prefix = prefix + ("    " if is_last_sibling else "│   ")
        triggered_map = current_log_node.get('triggered')

        if triggered_map is not None:
            actions = list(triggered_map.keys())
            if not actions:
                smart_print(f"{children_prefix}└── [dim italic][No further actions/paths logged][/dim italic]")
                return
            for i, action_key in enumerate(actions):
                is_last_action = (i == len(actions) - 1)
                action_conn = "└── " if is_last_action else "├── "
                smart_print(f"{children_prefix}{action_conn}[blue bold]{str(action_key)}[/blue bold]")
                sub_trees = triggered_map.get(action_key, [])
                sub_prefix = children_prefix + ("    " if is_last_action else "│   ")
                if not sub_trees:
                    smart_print(f"{sub_prefix}└── [red][Path End/Exit Trigger][/red]")
                else:
                    for j, sub_tree in enumerate(sub_trees):
                        self._recursive_print_execution_log(sub_tree, sub_prefix, (j == len(sub_trees) - 1))
        else:
            smart_print(f"{children_prefix}└── [dim italic]Leaf Node[/dim italic]")

class Flow(ExecutionLogTreePrinterMixin, bf.Flow[bf.M, bf.PrepResultT, bf.ActionT]): # type: ignore
    pass
class ParallelFlow(ExecutionLogTreePrinterMixin, bf.ParallelFlow[bf.M, bf.PrepResultT, bf.ActionT]): # type: ignore
    pass

