"""A mixin to provide asyncio context propagation for ParallelFlow."""
from __future__ import annotations
import asyncio
import contextvars
from typing import List, Callable, Awaitable, Any, Sequence, TYPE_CHECKING

if TYPE_CHECKING:
    import brainyflow as bf

class ParallelContextMixin:
    """
    Overrides run_tasks to ensure asyncio context variables are
    propagated to tasks running in parallel via asyncio.gather.
    """
    async def run_tasks(self, tasks: Sequence[Callable[[], Awaitable[Any]]]) -> List[Any]:
        parent_context = contextvars.copy_context()

        # FIX: We must return a new list of CALLABLES, not coroutines.
        # Each new callable will run the original callable within the copied context.
        def create_contextualized_callable(original_callable):
            def contextualized_runner():
                # When this runner is called, it executes the original
                # callable inside the context, returning the coroutine.
                return parent_context.run(original_callable)
            return contextualized_runner

        # This creates a new list of callables, preserving the expected type.
        contextualized_tasks = [create_contextualized_callable(t) for t in tasks]

        # Pass the new list of context-aware callables down the chain.
        return await super().run_tasks(contextualized_tasks)