from __future__ import annotations
import json
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    import brainyflow as bf
else:
    from ..brainyflow_original import bf

from ..utils.logger import smart_print


class FileLoggerNodeMixin:
    """
    Simple file logger for BrainyFlow nodes.
    Logs only essential lifecycle data: prep input/output, exec input/output, post input/triggers.
    """
    
    def __init__(self, *args, log_folder: str = "brainyflow_logs", **kwargs):
        super().__init__(*args, **kwargs)
        self._log_folder = Path(log_folder)
        self._session_id = datetime.now().strftime('%Y%m%d_%H%M%S')
        
    def _ensure_log_folder(self):
        """Ensure log folder exists"""
        self._log_folder.mkdir(exist_ok=True)
        
    def _safe_serialize(self, value: Any) -> Any:
        """Safely serialize values for JSON"""
        if value is None or isinstance(value, (str, int, float, bool)):
            return value
        elif isinstance(value, (list, tuple)):
            return [self._safe_serialize(item) for item in value[:5]]  # Limit to 5 items
        elif isinstance(value, dict):
            return {str(k): self._safe_serialize(v) for k, v in list(value.items())[:10]}  # Limit to 10 items
        else:
            return f"<{type(value).__name__}: {str(value)[:100]}>"
    
    def _log_event(self, event: str, data: Dict[str, Any]):
        """Log a single event to file"""
        self._ensure_log_folder()
        
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "session": self._session_id,
            "node": f"{self.__class__.__name__}#{getattr(self, '_node_order', '?')}",
            "event": event,
            "data": self._safe_serialize(data)
        }
        
        # Write to session file
        log_file = self._log_folder / f"{self._session_id}.jsonl"
        try:
            with open(log_file, 'a', encoding='utf-8') as f:
                f.write(json.dumps(log_entry) + '\n')
        except Exception as e:
            smart_print(f"[red]Failed to write log: {e}[/red]")

    async def prep(self, memory):
        """Log prep phase"""
        self._log_event("prep_start", {"memory": memory})
        
        try:
            result = await super().prep(memory)
            self._log_event("prep_complete", {"result": result})
            return result
        except Exception as error:
            self._log_event("prep_error", {"error": str(error)})
            raise

    async def exec(self, prep_res):
        """Log exec phase"""
        self._log_event("exec_start", {"prep_result": prep_res})
        
        try:
            result = await super().exec(prep_res)
            self._log_event("exec_complete", {"result": result})
            return result
        except Exception as error:
            self._log_event("exec_error", {"error": str(error), "retry": getattr(self, 'cur_retry', 0)})
            raise

    async def post(self, memory, prep_res, exec_res):
        """Log post phase"""
        self._log_event("post_start", {
            "memory": memory,
            "prep_result": prep_res, 
            "exec_result": exec_res
        })
        
        try:
            result = await super().post(memory, prep_res, exec_res)
            self._log_event("post_complete", {"memory_after": memory})
            return result
        except Exception as error:
            self._log_event("post_error", {"error": str(error)})
            raise

    def trigger(self, action: str, forking_data=None):
        """Log trigger calls"""
        self._log_event("trigger", {
            "action": action,
            "forking_data": forking_data
        })
        return super().trigger(action, forking_data)


class FileLoggerFlowMixin(FileLoggerNodeMixin):
    """
    Simple file logger for BrainyFlow flows.
    Logs flow start/end and execution tree.
    """
    
    async def run(self, *args, **kwargs):
        """Log flow execution"""
        memory = args[0] if args else {}
        start_node = getattr(self, 'start', None)
        start_node_name = start_node.__class__.__name__ if start_node else 'Unknown'
        
        self._log_event("flow_start", {
            "start_node": start_node_name,
            "initial_memory": memory
        })
        
        try:
            result = await super().run(*args, **kwargs)
            self._log_event("flow_complete", {
                "execution_tree": result,
                "final_memory": memory
            })
            return result
        except Exception as error:
            self._log_event("flow_error", {"error": str(error)})
            raise
