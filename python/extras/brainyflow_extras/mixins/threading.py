from __future__ import annotations
import threading
from ..utils.logger import smart_print


class SingleThreadedMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._lock = threading.Lock()

    async def run(self, **kwargs):
        display_name = getattr(self, 'id', None) or self.__class__.__name__
        smart_print(f"├─ Acquiring lock for single-threaded execution in {display_name}...")
        self._lock.acquire()
        try:
            return await super().run(**kwargs)
        finally:
            display_name = getattr(self, 'id', None) or self.__class__.__name__
            smart_print(f"├─ Releasing lock for {display_name}.")
            self._lock.release()