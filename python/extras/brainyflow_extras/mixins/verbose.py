from __future__ import annotations
from types import SimpleNamespace
from typing import Any, TYPE_CHECKING
from contextvars import ContextVar

if TYPE_CHECKING:
    import brainyflow as bf
else:
    from ..brainyflow_original import bf

from ..utils.logger import smart_print, _config

# Context variable to track nesting depth for verbose output
verbose_depth_var: ContextVar[int] = ContextVar("verbose_depth", default=0)

class VerboseMemoryMixin:
    """A mixin for BaseMemory derivatives to print execution logs."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    @property
    def _refer(self):
        return SimpleNamespace(
            me=f"[white]{self.__class__.__name__}[/white]",
            attr=lambda key: f"{self._refer.me}.[bold]{key}[/bold]",
        )
    
    def _set_value(self, key: str, value: Any) -> None:
        super()._set_value(key, value)
        
        if not _config.verbose_mixin_logging:
            return
        if key.startswith("__") and key.endswith("__"):
            return
        
        depth = verbose_depth_var.get()
        # Memory logs appear inside the node's execution box
        prefix = "│  " * depth + "├─"
        smart_print(prefix, self._refer.attr(key), "=", value, single_line=True)

class VerboseNodeMixin:
    """A mixin that provides nested, box-drawing output."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    @property
    def _refer(self):
        return SimpleNamespace(
            me=f"[bold yellow]{self.__class__.__name__}[/bold yellow][white]#{getattr(self, '_node_order', 'Unknown')}[/white]",
        )
    
    async def exec_runner(self, *args, **kwargs) -> Any:
        if not _config.verbose_mixin_logging:
            return await super().exec_runner(*args, **kwargs)

        prefix = "│  " * (verbose_depth_var.get()) + "├─"
        if self.prep.__func__ != bf.BaseNode.prep:
            smart_print(f"{prefix} prep() →", args[1] if len(args) > 1 else "No prep result")

        exec_res = await super().exec_runner(*args, **kwargs)
        if self.prep.__func__ != bf.BaseNode.prep:
            smart_print(f"{prefix} exec() →", exec_res)
        
        return exec_res
        
    async def run(self, *args, **kwargs):
        if not _config.verbose_mixin_logging:
            return await super().run(*args, **kwargs)

        depth = verbose_depth_var.get()
        is_flow = issubclass(self.__class__, getattr(bf, 'Flow', type(None)))
        
        # All nodes and flows get a "Running" banner
        smart_print("│  " * depth + f"┌── Running {self._refer.me}")

        token = verbose_depth_var.set(depth + 1)
        try:
            result = await super().run(*args, **kwargs)
        finally:
            verbose_depth_var.reset(token)
        
        # The ExecutionTreePrinter handles the final output for Flows
        propagate: bool = kwargs.get('propagate', args[1] if len(args) > 1 and isinstance(args[1], bool) else False)
        if not propagate:
             smart_print("│  " * depth + f"└── Finished {self._refer.me}")
             return result
             
        smart_print("│  " * depth + f"└─ {self._refer.me} next:")
        if hasattr(self, '_triggers') and hasattr(self, 'get_next_nodes'):
            if (len(result) == 1 and result[0][0] == 'default' and len(getattr(self, '_triggers', [])) == 0):
                smart_print("│  " * depth + f"\t[dim italic]> Leaf Node[/dim italic]")
            else:
                for key,_ in result:
                    try:
                        next_nodes = self.get_next_nodes(key)
                        successors = ", ".join(f"[green]{c.__class__.__name__}[/green]#{getattr(c, '_node_order', 'Unknown')}" for c in next_nodes) or f"[dim red]Terminal Action[/dim red]"
                        smart_print("│  " * depth + f"\t- [blue]{key}[/blue]\t >> {successors}")
                    except Exception as e:
                        smart_print("│  " * depth + f"\t- [blue]{key}[/blue]\t >> [red]Error: {e}[/red]")

        return result


    # def trigger(self, action: str, forking_data: Optional[Dict[str, Any]] = None)-> None:
    #     result = super().trigger(action, forking_data)

    #     if not _config.verbose_mixin_logging:
    #     	return result
        	
    #     depth = verbose_depth_var.get()
    #     prefix = "│  " * (depth) + "└─>\t"
        
    #     successors_str = ""
    #     if hasattr(self, 'get_next_nodes'):
    #         try:
    #             next_nodes = self.get_next_nodes(action)
    #             if next_nodes:
    #                 successors_str = " >> " + ", ".join(f"[green]{n.__class__.__name__}[/green]#{getattr(n, '_node_order', '?')}" for n in next_nodes)
    #             else:
    #                 successors_str = f" >> [red]Terminal Action[/red]"
    #         except Exception:
    #             pass
    #     smart_print(f"{prefix} [blue]{action}[/blue]{successors_str}")

    #     return result
