from __future__ import annotations
from abc import ABC
import json
import hashlib
import pickle
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Generic, Optional, TYPE_CHECKING, Callable, Tuple
from contextvars import ContextVar

try:
    import numpy as np
except ImportError:
    np = None

if TYPE_CHECKING:
    import brainyflow as bf
else:
    # A trick to allow type-checking without circular dependencies
    from ..brainyflow_original import bf

# --- Context and Artifact Management ---

class LogContext:
    """A central object to manage paths and state for a single logging session."""
    def __init__(self, log_folder: Path, session_id: str):
        self.log_folder = log_folder
        self.session_id = session_id
        self.session_dir = log_folder / "sessions" / session_id
        self.snapshot_dir = log_folder / "memory_snapshots"
        self.artifact_dir = log_folder / "artifacts"
        # Ensure directories exist
        self.session_dir.mkdir(parents=True, exist_ok=True)
        self.snapshot_dir.mkdir(parents=True, exist_ok=True)
        self.artifact_dir.mkdir(parents=True, exist_ok=True)

# ContextVar to hold the current LogContext for the running async task.
log_context_var: ContextVar[Optional[LogContext]] = ContextVar("log_context", default=None)

class ArtifactSerializer:
    """Handles serialization of complex, non-JSON objects to binary files."""
    def __init__(self):
        self.handlers: Dict[type, Tuple[str, Callable, str]] = {}
        if np:
            self.register(np.ndarray, 'numpy', self.save_numpy, '.npy')

    def register(self, type_to_handle: type, handler_name: str, save_func: Callable, extension: str):
        self.handlers[type_to_handle] = (handler_name, save_func, extension)

    def save_numpy(self, obj: np.ndarray, path: Path):
        np.save(path, obj)

    def save_pickle(self, obj: Any, path: Path):
        with open(path, 'wb') as f:
            pickle.dump(obj, f, protocol=pickle.HIGHEST_PROTOCOL)

    def handle(self, obj: Any, context: LogContext) -> Optional[Dict[str, Any]]:
        obj_type = type(obj)
        handler_name, save_func, extension = self.handlers.get(obj_type, ('pickle', self.save_pickle, '.pkl'))
        try:
            data_bytes = pickle.dumps(obj)
            data_hash = hashlib.sha256(data_bytes).hexdigest()
            filename = f"{data_hash}{extension}"
            filepath = context.artifact_dir / filename
            if not filepath.exists():
                save_func(obj, filepath)
            return {"__type__": "Artifact", "handler": handler_name, "ref": filename}
        except Exception:
            return None

# --- Serialization Engine ---

def _serialize_for_log(data: Any, context: LogContext, serializer: ArtifactSerializer, seen: set) -> Any:
    """Recursively serializes data for logging, handling Memory, artifacts, and recursion."""
    obj_id = id(data)
    if obj_id in seen:
        return f"<CircularReference to {type(data).__name__}>"
    
    # Use duck-typing for Memory-like objects
    if hasattr(data, '_global') and hasattr(data, '_local'):
        seen.add(obj_id)
        # Serialize the *contents* of the memory, not the object itself, to prevent recursion on the container.
        snapshot_content = {
            "global": _serialize_for_log(data._global, context, serializer, seen),
            "local": _serialize_for_log(data._local, context, serializer, seen),
        }
        seen.remove(obj_id)
        try:
            state_str = json.dumps(snapshot_content, sort_keys=True)
            state_hash = hashlib.sha256(state_str.encode('utf-8')).hexdigest()
            filepath = context.snapshot_dir / f"{state_hash}.json"
            if not filepath.exists():
                with open(filepath, 'w', encoding='utf-8') as f:
                    json.dump(snapshot_content, f, indent=2)
            return {"__type__": "MemorySnapshot", "ref": state_hash}
        except Exception:
            return "<Unserializable Memory State>"

    if data is None or isinstance(data, (str, int, float, bool)):
        return data

    seen.add(obj_id)
    if isinstance(data, (list, tuple, set)):
        res = [_serialize_for_log(item, context, serializer, seen) for item in list(data)]
    elif isinstance(data, dict):
        res = {str(k): _serialize_for_log(v, context, serializer, seen) for k, v in data.items()}
    else:
        # Fallback to artifact serialization for any other complex type
        res = serializer.handle(data, context) or f"<{type(data).__name__}>"
    seen.remove(obj_id)
    return res

# --- The Mixin Implementation ---

class FileLoggerNodeMixin:
    def __init__(self, *args, log_folder: str = "brainyflow_logs", **kwargs):
        super().__init__(*args, **kwargs)
        self.log_folder = Path(log_folder)
        self.artifact_serializer = ArtifactSerializer()

    def _log_event(self, event_name: str, data: Dict[str, Any]):
        context = log_context_var.get()
        if not context: return # Do not log if not in a logging context

        mro_list = [cls.__name__ for cls in self.__class__.__mro__ if cls not in (object, ABC, Generic)]
        if 'BaseNode' not in mro_list: mro_list.append('BaseNode')
        mro_list = mro_list[:mro_list.index('BaseNode')+1]
        
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "node": f"{self.__class__.__name__}#{getattr(self, '_node_order', '?')}",
            "mro": mro_list,
            "event": event_name,
            "data": _serialize_for_log(data, context, self.artifact_serializer, set())
        }
        log_file = context.session_dir / "events.jsonl"
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(log_entry) + '\n')

    async def prep(self, memory: "bf.Memory", **kwargs):
        self._log_event("prep.enter", {"memory_in": memory})
        try:
            result = await super().prep(memory, **kwargs)
            self._log_event("prep.exit", {"result": result})
            return result
        except Exception as error:
            self._log_event("prep.error", {"error": str(error)})
            raise

    async def exec(self, prep_res: Any, **kwargs):
        self._log_event("exec.enter", {"prep_result": prep_res})
        try:
            result = await super().exec(prep_res, **kwargs)
            self._log_event("exec.exit", {"result": result})
            return result
        except Exception as error:
            self._log_event("exec.error", {"error": str(error), "retry": getattr(self, 'cur_retry', 0)})
            raise

    async def post(self, memory: "bf.Memory", prep_res: Any, exec_res: Any, **kwargs):
        self._log_event("post.enter", {"memory_in": memory, "prep_result": prep_res, "exec_result": exec_res})
        try:
            await super().post(memory, prep_res, exec_res, **kwargs)
            self._log_event("post.exit", {"memory_out": memory})
        except Exception as error:
            self._log_event("post.error", {"error": str(error)})
            raise

    def trigger(self, action: str, forking_data: Optional[Dict[str, Any]] = None, **kwargs):
        self._log_event("trigger", {"action": action, "forking_data": forking_data})
        return super().trigger(action, forking_data, **kwargs)

class FileLoggerFlowMixin(FileLoggerNodeMixin):
    async def run(self, *args, **kwargs):
        ctx = log_context_var.get()
        is_root_call = ctx is None

        if is_root_call:
            session_id = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
            ctx = LogContext(self.log_folder, session_id)
            log_context_var.set(ctx)

        self._log_event("flow.enter", {"flow_type": self.__class__.__name__,"initial_memory": args[0] if args else {}})
        try:
            result = await super().run(*args, **kwargs)
            self._log_event("flow.exit", {"result": result, "final_memory": args[0] if args else {}})
            return result
        except Exception as error:
            self._log_event("flow.error", {"error": str(error), "final_memory": args[0] if args else {}})
            raise
        finally:
            if is_root_call:
                log_context_var.set(None)