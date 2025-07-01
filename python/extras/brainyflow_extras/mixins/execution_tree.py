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

        class_name = getattr(self, 'id', None) or self.__class__.__name__
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
        
        return result

    def _recursive_print_execution_log(self, current_log_node: ExecutionTree, prefix: str, is_last_sibling: bool, skip_node_print: bool = False):
        """
        Recursively prints the execution log in a tree structure.
        Highlights structural path endings based on the ExecutionTree content.
        """
        orchestrated_body = current_log_node.get('orchestrated')
        triggered_map = current_log_node.get('triggered')
        
        # Check if this is a leaf node (no orchestrated body and no triggered actions)
        is_leaf_node = not orchestrated_body and not triggered_map
        
        if not skip_node_print:
            connector = "└── " if is_last_sibling else "├── "
            node_type = current_log_node.get('type', 'UnknownType')
            node_order = current_log_node.get('order', 'UnknownID')
            
            # If it's a leaf node, append "Leaf Node" to the same line
            leaf_suffix = " [dim italic]Leaf Node[/dim italic]" if is_leaf_node else ""
            smart_print(f"{prefix}{connector}[green bold]{node_type}[/green bold]#[green]{node_order}[/green]{leaf_suffix}")

        children_prefix = prefix + ("    " if is_last_sibling else "│   ")

        # 1. If the node orchestrated a sub-graph, print that first.
        if orchestrated_body:
            is_last_item = not triggered_map
            body_connector = "└── " if is_last_item else "├── "
            # Print "orchestrates" and the orchestrated node on the same line
            orchestrated_node_type = orchestrated_body.get('type', 'UnknownType')
            orchestrated_node_order = orchestrated_body.get('order', 'UnknownID')
            smart_print(f"{children_prefix}{body_connector}[dim italic]orchestrates[/dim italic] [green bold]{orchestrated_node_type}[/green bold]#[green]{orchestrated_node_order}[/green]")
            
            # Continue with the orchestrated node's children, skipping the node print since we already printed it
            body_prefix = children_prefix + ("    " if is_last_item else "│   ")
            self._recursive_print_execution_log(orchestrated_body, body_prefix, is_last_sibling=True, skip_node_print=True)

        # 2. Then, print any externally triggered actions.
        if triggered_map:
            actions = list(triggered_map.keys())
            for i, action_key in enumerate(actions):
                is_last_action = (i == len(actions) - 1)
                action_conn = "└── " if is_last_action else "├── "
                
                sub_trees = triggered_map.get(action_key)
                sub_prefix = children_prefix + ("    " if is_last_action else "│   ")

                if sub_trees is None or not sub_trees:
                    smart_print(f"{children_prefix}{action_conn}[blue bold]{str(action_key)}[/blue bold]")
                    smart_print(f"{sub_prefix}└── [red][End][/red]")
                elif len(sub_trees) == 1:
                    # If action leads to a single node, print them on the same line
                    single_sub_tree = sub_trees[0]
                    node_type = single_sub_tree.get('type', 'UnknownType')
                    node_order = single_sub_tree.get('order', 'UnknownID')
                    
                    # Check if the single node is a leaf node
                    single_orchestrated_body = single_sub_tree.get('orchestrated')
                    single_triggered_map = single_sub_tree.get('triggered')
                    single_is_leaf_node = not single_orchestrated_body and not single_triggered_map
                    
                    # If it's a leaf node, append "Leaf Node" to the same line
                    leaf_suffix = " [dim italic]Leaf Node[/dim italic]" if single_is_leaf_node else ""
                    smart_print(f"{children_prefix}{action_conn}[blue bold]{str(action_key)}[/blue bold] >> [green bold]{node_type}[/green bold]#[green]{node_order}[/green]{leaf_suffix}")
                    
                    # Continue with the single node's children only if it's not a leaf node
                    if not single_is_leaf_node:
                        self._recursive_print_execution_log(single_sub_tree, sub_prefix, is_last_sibling=True, skip_node_print=True)
                else:
                    # Multiple nodes - use the original format
                    smart_print(f"{children_prefix}{action_conn}[blue bold]{str(action_key)}[/blue bold]")
                    for j, sub_tree in enumerate(sub_trees):
                        self._recursive_print_execution_log(sub_tree, sub_prefix, (j == len(sub_trees) - 1))
        
        # Note: Leaf node indication is now handled inline when printing the node itself
             