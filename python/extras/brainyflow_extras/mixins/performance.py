"""
Example of how easy it is to add new mixins to the system
"""
from __future__ import annotations
import time
from contextvars import ContextVar

from ..utils.logger import smart_print, _config

try:
    from .verbose import verbose_depth_var, _log
except ImportError:
    # Fallback if verbose mixin isn't used: _log is a simple alias for smart_print.
    verbose_depth_var = ContextVar("verbose_depth", default=0)
    _log = smart_print

class PerformanceMonitorMixin:
    """
    A mixin that monitors and reports performance metrics for node execution.
    """
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._perf_metrics = {}
    
    async def run(self, *args, **kwargs):
        start_time = time.perf_counter()
        try:
            result = await super().run(*args, **kwargs)
            execution_time = time.perf_counter() - start_time
            self._perf_metrics['last_run_time'] = execution_time
            
            # Use depth for nested output if verbose logging is on
            if _config.verbose_mixin_logging:
                depth = verbose_depth_var.get()
                # The depth is already incremented by the VerboseNodeMixin.run before this is called
                prefix = "│  " * (depth - 1) + "├─" if depth > 0 else "├─"
                refer_name = getattr(getattr(self, '_refer', None), 'me', self.__class__.__name__)
                _log(f"{prefix} ⏱️  {refer_name if not depth else 'it'} ran in {execution_time:.3f}s")

            return result
        except Exception as e:
            execution_time = time.perf_counter() - start_time
            self._perf_metrics['last_run_time'] = execution_time
            
            if _config.verbose_mixin_logging:
                depth = verbose_depth_var.get()
                prefix = "│  " * (depth - 1) + "├─" if depth > 0 else "├─"
                refer_name = getattr(getattr(self, '_refer', None), 'me', self.__class__.__name__)
                _log(f"{prefix} ⛔️  {refer_name} failed after {execution_time:.3f}s")
            
            raise
    
    def get_performance_metrics(self) -> dict:
        """Get performance metrics for this node"""
        return self._perf_metrics.copy()