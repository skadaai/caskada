from __future__ import annotations
from types import SimpleNamespace
from typing import List, Tuple, Optional, cast, Any

import threading
import brainyflow as bf
from rich.text import Text
from rich.console import Console
from rich.highlighter import ReprHighlighter
from rich import traceback as rich_traceback

# Configure rich traceback
rich_traceback.install()

console = Console()
highlighter = ReprHighlighter()

# @functools.wraps(func) TODO

def smart_print(
    *objects: Any,
    max_length: Optional[int] = None,
    single_line: bool = False,
    truncate_suffix: str = "...",
    sep: str = " ",
) -> None:
    """
    Print one or more objects with customizable truncation and formatting.
    
    Args:
        *objects: One or more objects to display
        max_length: Maximum length of the displayed string representation (None for no limit)
        single_line: If True, display content in a single line
        truncate_suffix: String to append when truncation occurs
        sep: Separator between multiple objects (default space)
    """
    if not objects:
        return
    
    # Convert objects to Rich Text objects
    text_objects = []
    
    for obj in objects:
        if isinstance(obj, Text):
            # Already a Text object
            text_obj = obj
        elif isinstance(obj, str):
            # Convert string to Text object
            text_obj = Text.from_markup(obj)
        elif hasattr(obj, "__rich__"):
            # Rich-compatible object, get its representation
            text_obj = obj.__rich__()
        else:
            # Regular object, convert to string and highlight
            obj_str = str(obj)
            text_obj = highlighter(obj_str)
        
        # Handle single line conversion if needed
        if single_line and isinstance(text_obj, Text):
            plain_text = text_obj.plain
            if "\n" in plain_text or "\r" in plain_text:
                new_text = plain_text.replace("\n", "\\n").replace("\r", "\\r")
                text_obj = Text(new_text, style=text_obj.style)
        
        text_objects.append(text_obj)
    
    # Join text objects with separator
    if len(text_objects) > 1:
        result = text_objects[0]
        for text_obj in text_objects[1:]:
            result = Text.assemble(result, sep, text_obj)
    else:
        result = text_objects[0]
    
    # Handle truncation
    if max_length is not None:
        plain_text = result.plain
        if len(plain_text) > max_length:
            # Create a new text object with the truncated content
            truncated = result.copy()
            truncated.plain = plain_text[:max_length] + truncate_suffix
            result = truncated
    
    # Print the result
    console.print(result)


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
        smart_print(self._refer.attr(key), "=", value)

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

    # async def exec_runner(self, *args, **kwargs) -> Any:
    #     smart_print(f"{self._refer.me}.prep() →", args[1])
    #     exec_res = await super().exec_runner(*args, **kwargs)
    #     smart_print(f"{self._refer.me}.exec() →", exec_res)
    #     return exec_res

    async def run(self, *args, **kwargs):
        result = await super().run(*args, **kwargs)
        propagate = getattr(kwargs, "propagate", args[1] if len(args) > 1 else False)
        if not propagate:
            smart_print(f"{self._refer.me}.run() → {result}")
            return result
    
        # smart_print(f"{self._refer.me}.post():")
        # for key, value in result:
        #     smart_print(f"\t- [blue]{key}[/blue]\t >> ", ", ".join(f"[green]{c.__class__.__name__}[/green]#{c._node_order}" for c in self.get_next_nodes(key)) or f"[red]Missing successor![/red]")

        return result

class SingleThreadedMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._lock = threading.Lock()

    async def run(self, **kwargs):
        print("Acquiring lock for single-threaded execution...")
        self._lock.acquire()
        try:
            return await super().run(**kwargs)
        finally:
            print("Releasing lock.")
            self._lock.release()

            

class Node(VerboseNodeRunnerMixin, bf.Node[bf.M, bf.PrepResultT, bf.ExecResultT, bf.ActionT]):
    pass



###################################################################################################################
# Flow
###################################################################################################################

class ExecutionLogTreePrinterMixin:
    """
    A mixin for BaseNode derivatives (especially Flow) to print execution logs
    in a user-friendly way.
    - If run with propagate=False on a Flow producing an ExecutionTree, prints a tree.
    - If run with propagate=True on any BaseNode, prints triggered actions and successors.
    """

    async def run(
        self, 
        # Using *args and **kwargs to be a transparent wrapper for super().run()
        *args: Any, 
        **kwargs: Any
    ) -> Any: # Return type is Any as super().run() can vary
        
        # Determine the effective 'propagate' argument value that super().run() will use.
        # BaseNode.run signature is: run(self, memory: Union[Memory, Dict], propagate: bool = False)
        # args[0] would be 'memory', args[1] could be 'propagate' if passed positionally.
        effective_propagate: bool
        if 'propagate' in kwargs:
            effective_propagate = bool(kwargs['propagate'])
        elif len(args) > 1 and isinstance(args[1], bool): # Check second positional arg
            effective_propagate = args[1]
        else:
            effective_propagate = False # Default for BaseNode.run

        # Call the superclass's run method first, passing all arguments through
        result = await super().run(*args, **kwargs) # type: ignore

        # `self` must be a BaseNode derivative to have _node_order and get_next_nodes.
        # These checks ensure we don't try to access attributes that might not exist.
        if not hasattr(self, '_node_order') or not isinstance(getattr(self, '_node_order', None), int):
            # Not a BaseNode derivative, or _node_order is missing/wrong type.
            # Cannot proceed with BrainyFlow-specific logging.
            return result

        # Safely get class name and node order for logging
        class_name = self.__class__.__name__
        node_order_val = getattr(self, '_node_order', 'UnknownID')

        if not effective_propagate:
            # This branch handles propagate=False. For Flows, this typically returns ExecutionTree.
            # Check if the result matches the structure of ExecutionTree.
            if (isinstance(result, dict) and 
                'order' in result and 'type' in result and 'triggered' in result): # Check for ExecutionTree structure
                
                log_tree_data = cast(bf.ExecutionTree, result) 
                
                console.rule(f"[bold cyan]Execution Path for {class_name}#{node_order_val}", style="cyan")
                self._recursive_print_execution_log(log_tree_data, prefix="", is_last_sibling=True)
                console.rule(style="cyan")
            else:
                # Fallback: If not propagate and result isn't an ExecutionTree, print basic result.
                # This matches the old VerboseNodeRunnerMixin's behavior for this case.
                smart_print(f">>>>>>> Result for {class_name}[#{node_order_val}]: {result}")
        
        else: # effective_propagate is True
            # This branch handles propagate=True, expects List[Tuple[Action, Memory]] from BaseNode.run.
            if isinstance(result, list) and all(isinstance(item, tuple) and len(item) == 2 for item in result):
                # This type assertion helps type checkers understand 'result' here.
                triggers_list = cast(List[Tuple["Action", "Memory"]], result)
                
                smart_print(f"Triggered in [bold yellow]{class_name}[/bold yellow]#{node_order_val}:")
                
                # Check if get_next_nodes method exists (it should for BaseNode derivatives)
                if hasattr(self, 'get_next_nodes') and callable(self.get_next_nodes):
                    for action_name_triggered, _node_memory_instance in triggers_list:
                        try:
                            # self.get_next_nodes is from BaseNode
                            next_nodes_for_action = self.get_next_nodes(action_name_triggered) # type: ignore 
                            
                            successors_str_parts = []
                            for c_node in next_nodes_for_action:
                                c_class_name = c_node.__class__.__name__
                                c_node_order_s = getattr(c_node, '_node_order', 'UnknownID')
                                successors_str_parts.append(f"[green]{c_class_name}[/green]#{c_node_order_s}")
                            
                            successors_str = ", ".join(successors_str_parts) or f"[red]Missing successor![/red]"
                            smart_print(f"\t- [blue]{action_name_triggered}[/blue]\t >> ", successors_str)
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

    def _recursive_print_execution_log(
        self, 
        current_log_node: ExecutionTree, 
        prefix: str, 
        is_last_sibling: bool
    ):
        """
        Recursively prints the execution log in a tree structure.
        Highlights structural path endings based on the ExecutionTree content.
        """
        connector = "└── " if is_last_sibling else "├── "
        node_text = Text()
        node_text.append(prefix + connector, style="dim") # Tree structure lines
        
        node_type_str = current_log_node.get('type', 'UnknownType')
        node_order_str = current_log_node.get('order', 'UnknownID')
        
        # Basic styling: assumes success if logged.
        # "Broken" node highlighting based on structure (e.g. early termination)
        # rather than explicit error fields, as ExecutionTree doesn't have them.
        node_text.append(f"{node_type_str}", style="green bold")
        node_text.append(f"#{node_order_str}", style="green")

        smart_print(node_text)

        children_prefix = prefix + ("    " if is_last_sibling else "│   ")
        triggered_actions_map = current_log_node.get('triggered') # This is Optional[Dict[Action, List[ExecutionTree]]]

        if triggered_actions_map is not None: 
            # Node has a 'triggered' dictionary (even if empty).
            actions_list = list(triggered_actions_map.keys())
            num_actions = len(actions_list)

            if num_actions == 0: 
                 # 'triggered' is an empty dictionary {}
                 # This implies the node ran but its triggers didn't lead to further logged sub-nodes in this context.
                 smart_print(Text(f"{children_prefix}└── ", style="dim") + Text("[No further actions/paths logged from this node]", style="dim italic"))

            for i, action_key in enumerate(actions_list):
                is_last_action_group = (i == num_actions - 1)
                
                action_connector = "└── " if is_last_action_group else "├── "
                action_text_print = Text()
                action_text_print.append(children_prefix + action_connector, style="dim")
                action_text_print.append(f"'{action_key}'", style="blue bold")
                smart_print(action_text_print)

                # Get the list of sub-ExecutionTree logs for this action
                sub_execution_trees = triggered_actions_map.get(action_key, []) 
                
                action_children_prefix = children_prefix + ("    " if is_last_action_group else "│   ")
                
                if not sub_execution_trees: 
                    # Action maps to an empty list [], indicating an "exit trigger" or path end for this flow context.
                    smart_print(Text(f"{action_children_prefix}└── ", style="dim") + Text("[Path End/Exit Trigger for this action]", style="red"))
                else:
                    num_sub_trees = len(sub_execution_trees)
                    for j, sub_tree_entry in enumerate(sub_execution_trees):
                        is_last_sub_tree_in_group = (j == num_sub_trees - 1)
                        self._recursive_print_execution_log(sub_tree_entry, prefix=action_children_prefix, is_last_sibling=is_last_sub_tree_in_group)
        
        elif triggered_actions_map is None: 
            # 'triggered' key is None (or missing).
            # This signifies a leaf in the execution tree as recorded by the Flow.
            # It could be a normal end of a branch or a point where logging stopped.
            smart_print(Text(f"{children_prefix}└── ", style="dim") + Text("[Leaf Node/No triggered paths logged]", style="dim italic"))



class Flow(ExecutionLogTreePrinterMixin, bf.Flow[bf.M, bf.PrepResultT, bf.ActionT]):
    pass