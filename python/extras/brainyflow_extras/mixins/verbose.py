from __future__ import annotations
import copy
import asyncio
from types import SimpleNamespace
from typing import Any, TYPE_CHECKING, List, Tuple, Dict, Optional, Callable, Awaitable
from contextvars import ContextVar

try:
    from PIL import Image
except ImportError:
    Image = None
if TYPE_CHECKING:
    import brainyflow as bf
else:
    from ..brainyflow_original import bf

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
            buffer.append((args, kwargs))
    else:
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
    """Provides detailed, race-condition-safe console logging for any node or flow."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    @property
    def _refer(self):
        return SimpleNamespace(
            me=f"{self.__class__.__name__}[dim]#{getattr(self, '_node_order', 'Unknown')}[/dim]",
            highlight=SimpleNamespace(
                me=f"[bold yellow]{self.__class__.__name__}[/bold yellow][dim]#{getattr(self, '_node_order', 'Unknown')}[/dim]",
            )
        )
    
    def _get_stable_repr(self, obj: Any) -> Any:
        """Creates a stable representation of complex objects for deferred logging."""
        if Image and isinstance(obj, Image.Image):
            return f"<Image mode={obj.mode} size={obj.size}>"
        if isinstance(obj, tuple):
            return tuple(self._get_stable_repr(item) for item in obj)
        return obj

    async def exec_runner(self, memory: bf.Memory, prep_res: Any, **kwargs) -> Any:
        """Hooks into the execution process to log prep and exec results."""
        if not _config.verbose_mixin_logging:
            return await super().exec_runner(memory, prep_res, **kwargs)

        prefix = "│  " * (verbose_depth_var.get())
        if self.prep.__func__ != bf.BaseNode.prep:
            _log(f"{prefix}┌─ [dim italic]prep()[/dim italic] →", self._get_stable_repr(prep_res))

        exec_res = await super().exec_runner(memory, prep_res, **kwargs)
        if self.exec.__func__ != bf.BaseNode.exec and self.exec.__func__ != bf.Flow.exec:
            _log(f"{prefix}├─ [dim italic]exec()[/dim italic] →", self._get_stable_repr(exec_res))
        
        return exec_res

    async def run(self, *args: Any, **kwargs: Any):
        """Wraps the node's run to provide entry/exit logging and successor visualization."""
        if not _config.verbose_mixin_logging:
            return await super().run(*args, **kwargs)

        active_buffer = log_buffer_var.get()
        is_top_level_log_manager = active_buffer is None
        if is_top_level_log_manager:
            active_buffer = []
            log_buffer_token = log_buffer_var.set(active_buffer)

        depth = verbose_depth_var.get()
        _log("│  " * depth + f"┌── Running {self._refer.highlight.me}")
        depth_token = verbose_depth_var.set(depth + 1)
        
        try:
            result = await super().run(*args, **kwargs)
			
            is_flow = hasattr(self, 'run_node')
            trigger_prefix = "│  " * (depth + (0 if is_flow else 1))
            
            # Log the triggers that were fired (no default added)
            _log(f"{trigger_prefix}{'├' if is_flow else '└'}─ [dim italic]trigger()[/dim italic] →", ", ".join([f"[blue]{str(t['action'])}[/blue]" for t in self._triggers]) or "[dim]none[/dim]")
            
            triggers = self._triggers or [{ "action": bf.DEFAULT_ACTION, "forking_data": {} }]
            verbose_depth_var.reset(depth_token)
            prefix = "│  " * depth

            ignored_actions = self.successors.keys() - [t["action"] for t in triggers]
            if len(ignored_actions) > 0:
                _log(f"{prefix}├─ ignored actions: {str(", ".join(f"[dim]{a}[/dim]" for a in ignored_actions))}")
                
            _log(f"{prefix}└─ successors:")

            for trigger in triggers:
                action = trigger.get('action')
                next_nodes = self.get_next_nodes(action)
                successors = ", ".join(f"[green]{c.__class__.__name__}[/green][dim]#{getattr(c, '_node_order', '?')}[/dim]" for c in next_nodes) or "[red]Terminal Action[/red]"
                action_repr = f"[blue]{str(action)}[/blue]" if len(self._triggers) else "[dim]default [italic](implicit)[/italic][/dim]"
                _log(f"{prefix}\t- {action_repr}\t >> {successors}" + ("" if not trigger.get('forking_data') else f" 📦"), ("" if not trigger.get('forking_data') else trigger.get('forking_data')))
            
            _log("│  " * depth) # Spacer
        
        except Exception as e:
            verbose_depth_var.reset(depth_token)
            _log("│  " * depth + f"└── [bold red]Error[/bold red] in {self._refer.me}", e)
            raise
        finally:
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
            _log("│  " * depth + f"╠══▷ Task {i+1}/{len(tasks)}:")
            
            for log_args, log_kwargs in buffer:
                if not log_args: continue
                
                modified_first_arg = log_args[0].replace("│  " * depth, "│  " * depth + "║ ", 1)
                new_args = (modified_first_arg,) + log_args[1:]
                _log(*new_args, **log_kwargs)
        
        _log("│  " * depth + f"╚══ Finished [bold cyan]Parallel Tasks[/bold cyan] ({len(tasks)} tasks)")
        return results