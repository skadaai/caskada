"""
Example of how easy it is to add new mixins to the system
"""
from __future__ import annotations
import time

from ..utils.logger import smart_print


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
            smart_print(f"├─ ⏱️  {self._refer.me or self.__class__.__name__}.run() executed in {execution_time:.3f}s")
            return result
        except Exception as e:
            execution_time = time.perf_counter() - start_time
            self._perf_metrics['last_run_time'] = execution_time
            smart_print(f"├─ ⚠️  {self._refer.me or self.__class__.__name__}.run() failed after {execution_time:.3f}s")
            raise
    
    def get_performance_metrics(self) -> dict:
        """Get performance metrics for this node"""
        return self._perf_metrics.copy()