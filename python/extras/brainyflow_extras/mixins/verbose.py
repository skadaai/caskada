from __future__ import annotations
from types import SimpleNamespace
from typing import Any, TYPE_CHECKING

from ..utils.logger import smart_print

class VerboseMemoryMixin:
    """
    A mixin for BaseMemory derivatives to print execution logs
    in a user-friendly way.
    """
    
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
        if key.startswith("__") and key.endswith("__"):
            return        
        smart_print(self._refer.attr(key), "=", value, single_line=True)


class VerboseNodeMixin:
    """
    A mixin for BaseNode derivatives to print execution logs
    in a user-friendly way.
    """
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    @property
    def _refer(self):
        return SimpleNamespace(
            me=f"[bold yellow]{self.__class__.__name__}[/bold yellow][white]#{getattr(self, '_node_order', 'Unknown')}[/white]",
        )

    async def exec_runner(self, *args, **kwargs) -> Any:
        smart_print(f"{self._refer.me}.prep() →", args[1] if len(args) > 1 else "No prep result", single_line=True)
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
        if hasattr(self, '_triggers') and hasattr(self, 'get_next_nodes'):
            if (len(result) == 1 and result[0][0] == 'default' and len(getattr(self, '_triggers', [])) == 0):
                smart_print(f"\t[dim italic]> Leaf Node[/dim italic]")
            else:
                for key, value in result:
                    try:
                        next_nodes = self.get_next_nodes(key)
                        successors = ", ".join(f"[green]{c.__class__.__name__}[/green]#{getattr(c, '_node_order', 'Unknown')}" for c in next_nodes) or f"[dim red]Terminal Action[/dim red]"
                        smart_print(f"\t- [blue]{key}[/blue]\t >> {successors}")
                    except Exception as e:
                        smart_print(f"\t- [blue]{key}[/blue]\t >> [red]Error: {e}[/red]")

        return result