from __future__ import annotations
import json
from typing import cast, Any, Dict

from ..utils.logger import smart_print, _config, _ensure_rich_traceback_installed, Console

ExecutionTree = Dict[str, Any] 
# Action = str 

class ExecutionTreePrinterMixin:
    """
    A mixin for BaseNode derivatives (especially Flow) to print execution logs
    in a user-friendly way.
    - If run on a Flow producing an ExecutionTree, prints a tree.
    - If run with on a Node, prints its execution result.
    """
    async def run(self, *args: Any, **kwargs: Any) -> Any:
        result = await super().run(*args, **kwargs) # type: ignore
        _ensure_rich_traceback_installed()

        # `self` must be a BaseNode derivative to have _node_order and get_next_nodes.
        # These checks ensure we don't try to access attributes that might not exist.
        if not hasattr(self, '_node_order') or not isinstance(getattr(self, '_node_order', None), int):
            return result

        class_name = self.__class__.__name__
        node_order_val = getattr(self, '_node_order', 'UnknownID')

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
        
        # else: # effective_propagate is True
        #     # This branch handles propagate=True, expects List[Tuple[Action, Memory]] from BaseNode.run.
        #     if isinstance(result, list) and all(isinstance(item, tuple) and len(item) == 2 for item in result):
        #         triggers_list = cast(List[Tuple[Action, Any]], result)
        #         smart_print(f"Triggered in [bold yellow]{class_name}[/bold yellow]#{node_order_val}:")
        #         if hasattr(self, 'get_next_nodes') and callable(self.get_next_nodes):
        #             for action_name_triggered, _ in triggers_list:
        #                 try:
        #                     next_nodes = self.get_next_nodes(action_name_triggered) # type: ignore
        #                     successors = ", ".join(
        #                         f"[green]{n.__class__.__name__}[/green]#{getattr(n, '_node_order', 'ID?')}" for n in next_nodes
        #                     ) or f"[red]Terminal Action[/red]"
        #                     smart_print(f"\t- [blue]{action_name_triggered}[/blue]\t >> ", successors)
        #                 except Exception as e:
        #                     # Gracefully handle errors during successor fetching for logging
        #                     smart_print(f"\t- [blue]{action_name_triggered}[/blue]\t >> [bold red]Error getting successors: {e}[/bold red]")
        #         else:
        #             # Fallback if get_next_nodes is somehow not available
        #             for action_name_triggered, _ in triggers_list:
        #                 smart_print(f"\t- [blue]{action_name_triggered}[/blue]\t >> [dim](Successor info unavailable)[/dim]")
        #     else:
        #         # If propagate=True but result is not the expected list of triggers.
        #         smart_print(f"Triggers from [bold yellow]{class_name}[/bold yellow]#{node_order_val} (propagate=True): {result} ([italic]unexpected format[/italic])")

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
        orchestrated_body = current_log_node.get('orchestrated')
        triggered_map = current_log_node.get('triggered')

        # 1. If the node orchestrated a sub-graph, print that first.
        if orchestrated_body:
            is_last_item = not triggered_map
            body_connector = "└── " if is_last_item else "├── "
            smart_print(f"{children_prefix}{body_connector}[dim italic]orchestrates[/dim italic]")
            body_prefix = children_prefix + ("    " if is_last_item else "│   ")
            self._recursive_print_execution_log(orchestrated_body, body_prefix, is_last_sibling=True)

        # 2. Then, print any externally triggered actions.
        if triggered_map:
            actions = list(triggered_map.keys())
            for i, action_key in enumerate(actions):
                is_last_action = (i == len(actions) - 1)
                action_conn = "└── " if is_last_action else "├── "
                smart_print(f"{children_prefix}{action_conn}[blue bold]{str(action_key)}[/blue bold]")
                
                sub_trees = triggered_map.get(action_key)
                sub_prefix = children_prefix + ("    " if is_last_action else "│   ")

                if sub_trees is None or not sub_trees:
                    smart_print(f"{sub_prefix}└── [red][End][/red]")
                else:
                    for j, sub_tree in enumerate(sub_trees):
                        self._recursive_print_execution_log(sub_tree, sub_prefix, (j == len(sub_trees) - 1))
        
        # 3. If it's a true leaf node (no body and no triggers), indicate that.
        elif not orchestrated_body:
             smart_print(f"{children_prefix}└── [dim italic]Leaf Node[/dim italic]")
             