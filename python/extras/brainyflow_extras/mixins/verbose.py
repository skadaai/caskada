from __future__ import annotations
import copy
import asyncio
from types import SimpleNamespace
from typing import Any, TYPE_CHECKING, List, Tuple, Dict, Optional, Callable, Awaitable
from contextvars import ContextVar

if TYPE_CHECKING:
    import brainyflow as bf
else:
    from ..brainyflow_original import bf

try:
    from PIL import Image
except ImportError:
    Image = None

from ..utils.logger import smart_print, _config

_log_lock = asyncio.Lock()
log_buffer_var: ContextVar[Optional[List[Tuple[Tuple, Dict]]]] = ContextVar("log_buffer", default=None)
verbose_depth_var: ContextVar[int] = ContextVar("verbose_depth", default=0)


def _log(*args: Any, **kwargs: Any):
    """
    A helper function that either prints directly or appends to a context-specific buffer
    to ensure atomic output from parallel tasks.
    """
    buffer = log_buffer_var.get()
    if buffer is not None:
        # Deepcopy the arguments to capture their state at this moment in time.
        # This prevents issues with stale object references when printing later.
        try:
            copied_args = copy.deepcopy(args)
            copied_kwargs = copy.deepcopy(kwargs)
            buffer.append((copied_args, copied_kwargs))
        except Exception:
            # Fallback for uncopyable objects (like some locks or system resources)
            buffer.append((args, kwargs))
    else:
        # Otherwise, print directly to the console (for non-buffered runs).
        smart_print(*args, **kwargs)


class VerboseLocalProxy(bf.LocalProxy):
    """A proxy for the local memory store that logs set and delete operations."""
    def __init__(self, store: bf.SharedStore, parent_refer: SimpleNamespace):
        super().__init__(store)
        # Store a reference to the parent's logger for consistent naming
        object.__setattr__(self, '_parent_refer', parent_refer)

    def __setattr__(self, key: str, value: Any) -> None:
        super().__setattr__(key, value)
        if not _config.verbose_mixin_logging:
            return
        
        depth = verbose_depth_var.get()
        prefix = "│  " * depth + "├─"
        # Construct a log name like "Memory_abc.local.my_key"
        log_key = f"{self._parent_refer.me}.[dim italic green]local[/dim italic green].[bold]{key}[/bold]"
        _log(prefix, "📦", log_key, "=", value, single_line=True)

    def __setitem__(self, key: str, value: Any) -> None:
        self.__setattr__(key, value)

    def __delattr__(self, key: str) -> None:
        super().__delattr__(key)
        if not (_config.verbose_mixin_logging and not key.startswith("__")):
            return
        
        depth = verbose_depth_var.get()
        prefix = "│  " * depth + "├─"
        log_key = f"{self._parent_refer.me}.[dim italic green]local[/dim italic green].[bold]{key}[/bold]"
        _log(prefix, "🚫", log_key, single_line=True)

    def __delitem__(self, key: str) -> None:
        self.__delattr__(key)


class VerboseMemoryMixin:
    """A mixin for Memory derivatives to provide detailed execution logs."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    @property
    def _refer(self) -> SimpleNamespace:
        return SimpleNamespace(
            me=f"[dim italic]memory[/dim italic]",
            attr=lambda key: f"{self._refer.me}.[bold]{key}[/bold]",
        )
    
    def _set_value(self, key: str, value: Any) -> None:
        super()._set_value(key, value)
        if not _config.verbose_mixin_logging:
            return
            
        depth = verbose_depth_var.get()
        prefix = "│  " * depth + "├─"
        _log(prefix, "📦", self._refer.attr(key), "=", value)

    def __delattr__(self, key: str) -> None:
        super().__delattr__(key)
        if not _config.verbose_mixin_logging:
            return
        
        depth = verbose_depth_var.get()
        prefix = "│  " * depth + "├─"
        _log(prefix, "🚫", self._refer.attr(key))

    def __delitem__(self, key: str) -> None:
        self.__delattr__(key)

    @property
    def local(self) -> VerboseLocalProxy:
        return VerboseLocalProxy(self._local, self._refer)


class VerboseNodeMixin:
    """A mixin that provides nested, race-condition-safe, box-drawing output."""
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
            _log(f"{prefix} prep() →", args[1] if len(args) > 1 else "No prep result")

        exec_res = await super().exec_runner(*args, **kwargs)
        if self.prep.__func__ != bf.BaseNode.prep:
            _log(f"{prefix} exec() →", exec_res)
        
        return exec_res
        
    async def run(self, *args, **kwargs):
        if not _config.verbose_mixin_logging:
            return await super().run(*args, **kwargs)

        active_buffer = log_buffer_var.get()
        is_top_level_log_manager = active_buffer is None

        # If this is the top-level call in a potentially parallel branch,
        # it becomes the manager for the buffer and the final, locked print-out.
        if is_top_level_log_manager:
            active_buffer = []
            log_buffer_token = log_buffer_var.set(active_buffer)

        result = None
        depth = verbose_depth_var.get()
        _log("│  " * depth + f"┌── Running {self._refer.me}")
        depth_token = verbose_depth_var.set(depth + 1)
        
        try:
            # The actual execution ALWAYS happens here.
            result = await super().run(*args, **kwargs)
            
            verbose_depth_var.reset(depth_token)
            propagate: bool = kwargs.get('propagate', args[1] if len(args) > 1 and isinstance(args[1], bool) else False)
            if not propagate:
                _log("│  " * depth + f"└── Finished {self._refer.me}")
                return result
                
            _log("│  " * depth + f"└─ {self._refer.me} next:")
            if hasattr(self, '_triggers') and hasattr(self, 'get_next_nodes') and isinstance(result, list):
                if (len(result) == 1 and result[0][0] == 'default' and len(getattr(self, '_triggers', [])) == 0):
                    _log("│  " * depth + f"\t[dim italic]> Leaf Node[/dim italic]")
                else:
                    for key, data in result:
                        try:
                            next_nodes = self.get_next_nodes(key)
                            successors = ", ".join(f"[green]{c.__class__.__name__}[/green]#{getattr(c, '_node_order', 'Unknown')}" for c in next_nodes) or f"[dim red]Terminal Action[/dim red]"
                            _log("│  " * depth + f"\t- [blue]{key}[/blue]\t >> {successors}" + ("" if not data else f" 📦"), data._local)
                        except Exception as e:
                            _log("│  " * depth + f"\t- [blue]{key}[/blue]\t >> [red]Error: {e}[/red]")
        except Exception as e:
            verbose_depth_var.reset(depth_token)
            _log("│  " * depth + f"└── [bold red]Error[/bold red] in {self._refer.me}", e)
            raise
        finally:
            # If this was the top-level manager, it now flushes the entire buffer atomically.
            if is_top_level_log_manager and active_buffer is not None:
                log_buffer_var.reset(log_buffer_token)
                async with _log_lock:
                    for log_args, log_kwargs in active_buffer:
                        smart_print(*log_args, **log_kwargs)

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


class VerboseParallelFlowMixin(VerboseNodeMixin):
    """
    A specialization of VerboseNodeMixin that overrides run_tasks to visualize concurrency.
    """
    async def run_tasks(self, tasks: List[Callable[[], Awaitable[Any]]]) -> List[Any]:
        if not _config.verbose_mixin_logging or len(tasks) <= 1:
            return await super().run_tasks(tasks)

        depth = verbose_depth_var.get()
        _log("│  " * depth + f"╔══ Running [bold cyan]Parallel Tasks[/bold cyan] ({len(tasks)} tasks)")
        
        task_buffers: List[List[Tuple[Tuple, Dict]]] = [[] for _ in tasks]
        
        async def create_logged_task(task: Callable[[], Awaitable[Any]], buffer: list) -> Callable[[], Awaitable[Any]]:
            async def logged_task_runner():
                token = log_buffer_var.set(buffer)
                try: return await task()
                finally: log_buffer_var.reset(token)
            return logged_task_runner

        logged_tasks = [await create_logged_task(t, b) for t, b in zip(tasks, task_buffers)]
        results = await super(VerboseNodeMixin, self).run_tasks(logged_tasks)

        for i, buffer in enumerate(task_buffers):
            is_last_task = i == len(tasks) - 1
            _log("│  " * depth + f"{"╠" if not is_last_task else "╚"}══▷ Task {i+1}/{len(tasks)}:")
            
            for log_args, log_kwargs in buffer:
                if not log_args: continue
                
                modified_first_arg = log_args[0].replace("│  " * depth, "│  " * depth + ("║ " if not is_last_task else "  "))
                new_args = (modified_first_arg,) + log_args[1:]
                _log(*new_args, **log_kwargs)
        
        return results