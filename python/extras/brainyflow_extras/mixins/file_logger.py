from __future__ import annotations
from abc import ABC
import json
import cbor2
import hashlib
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Generic, Optional, TYPE_CHECKING
from contextvars import ContextVar
import sys

# Optional imports for handling specific complex types
try:
    import numpy as np
except ImportError:
    np = None

try:
    import faiss
except ImportError:
    faiss = None

if TYPE_CHECKING:
    import brainyflow as bf

# --- Context and Artifact Management ---

class LogContext:
    """A central object to manage paths and state for a single logging session."""
    def __init__(self, log_folder: Path, session_id: str):
        self.log_folder = log_folder
        self.session_id = session_id
        self.session_log_path = self.log_folder / f"{self.session_id}.jsonl"
        self.snapshot_dir = self.log_folder / "memory_snapshots"
        self.artifact_dir = self.log_folder / "artifacts"
        self.log_folder.mkdir(parents=True, exist_ok=True)
        self.snapshot_dir.mkdir(parents=True, exist_ok=True)
        self.artifact_dir.mkdir(parents=True, exist_ok=True)

log_context_var: ContextVar[Optional[LogContext]] = ContextVar("log_context", default=None)

# --- Serialization Engine using Hybrid JSON + CBOR ---

class ArtifactSerializer:
    """Handles secure serialization of complex 'artifact' objects to binary CBOR files."""

    def _cbor_encoder_hook(self, encoder, value: Any) -> Any:
        """
        A hook for cbor2.dumps to handle types that aren't natively supported.
        This is the core of handling complex, non-standard objects.
        """
        # Handle NumPy types if numpy is installed
        if np:
            if isinstance(value, np.ndarray):
                encoder.encode(value.tolist())
                return
            if isinstance(value, (np.int64, np.int32, np.int16, np.int8)):
                encoder.encode(int(value))
                return
            if isinstance(value, (np.float64, np.float32, np.float16)):
                encoder.encode(float(value))
                return

        # Handle FAISS index if faiss is installed
        if faiss and isinstance(value, faiss.Index):
            try:
                binary_index = faiss.serialize_index(value)
                encoder.encode(cbor2.CBORTag(4001, binary_index))
            except Exception as e:
                 # FIX: Catch any exception from FAISS and provide a more informative message
                print(f"├─ Error: FAISS serialization failed for index of type {type(value)}: {e}")
                encoder.encode(f"<Unserializable FAISS Index: {type(value).__name__}>")
            return
            
        # Handle Python's Path objects
        if isinstance(value, Path):
            encoder.encode(str(value))
            return
            
        # Handle typing objects (like list[str]) by converting them to strings
        if 'typing' in sys.modules and isinstance(value, sys.modules['typing']._GenericAlias):
            encoder.encode(str(value))
            return

        # For any other object, represent it as a generic map.
        if hasattr(value, '__dict__'):
            # The payload is a map with class info and the object's dictionary
            payload = {
                "__type__": "GenericObject",
                "module": value.__class__.__module__,
                "class": value.__class__.__name__,
                "data": vars(value)
            }
            encoder.encode(payload)
            return
            
        # If all else fails, use the default encoder which will raise an error
        # for unhandled types. We can catch this and provide a fallback.
        try:
            # Let the default encoder handle it if possible (e.g., dicts, lists inside objects)
            return encoder.encode(value)
        except cbor2.CBOREncodeError:
            # Fallback for objects that are truly not serializable
            encoder.encode(f"<Unserializable CBOR Leaf: {type(value).__name__}>")

    def handle_as_cbor_artifact(self, obj: Any, context: LogContext) -> Optional[Dict[str, Any]]:
        """
        Securely serializes a single Python object to a standalone CBOR artifact file.
        """
        try:
            # Pass our custom encoder hook to cbor2.dumps
            data_bytes = cbor2.dumps(obj, default=self._cbor_encoder_hook)
            data_hash = hashlib.sha256(data_bytes).hexdigest()
            filename = f"{data_hash}.cbor"
            filepath = context.artifact_dir / filename

            if not filepath.exists():
                with open(filepath, 'wb') as f:
                    f.write(data_bytes)
            
            # Return a JSON-serializable dictionary that references the binary artifact
            return {"__type__": "Artifact", "handler": "cbor2", "ref": filename}
        except (cbor2.CBOREncodeError, TypeError) as e:
            print(f"├─ ArtifactSerializerError: Could not serialize object to CBOR. Type: {type(obj)}. Error: {e}")
            return None
            
def _create_snapshot(store: Dict, context: LogContext, serializer: ArtifactSerializer, seen: set) -> Dict:
    """Creates a standardized snapshot file for a dictionary-like store (e.g., global memory)."""
    # We must pass a new `seen` set here to avoid circular reference issues with the main log serialization
    snapshot_content = _serialize_for_log(store, context, serializer, set(seen))
    try:
        state_str = json.dumps(snapshot_content, sort_keys=True)
        state_hash = hashlib.sha256(state_str.encode('utf-8')).hexdigest()
        filepath = context.snapshot_dir / f"{state_hash}.json"
        if not filepath.exists():
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(snapshot_content, f, indent=2)
        return {"__type__": "MemorySnapshot", "ref": state_hash}
    except Exception as e:
        print('├─ MemorySnapshotError:', e)
        return {"__type__": "MemorySnapshot", "ref": "<error>"}

def _is_memory_obj(data: Any) -> bool:
    """More specific duck-typing to identify a Memory object."""
    return hasattr(data, '_global') and hasattr(data, '_local') and callable(getattr(data, 'clone', None))

def _is_execution_tree(data: Any) -> bool:
    """Duck-typing to identify an ExecutionTree dictionary."""
    return isinstance(data, dict) and all(k in data for k in ['order', 'type', 'triggered'])

def _serialize_for_log(data: Any, context: LogContext, serializer: ArtifactSerializer, seen: set) -> Any:
    """
    Recursively traverses data to make it JSON-serializable.
    Complex objects are offloaded to binary CBOR artifacts.
    """
    # 1. Handle primitive types that are already JSON-serializable
    if data is None or isinstance(data, (str, int, float, bool)):
        return data

    # 2. Handle circular references
    obj_id = id(data)
    if obj_id in seen:
        return f"<CircularReference to {type(data).__name__} id:{obj_id}>"

    # Handle simple typing representations directly, preventing them from becoming artifacts.
    if 'typing' in sys.modules and isinstance(data, sys.modules['typing']._GenericAlias):
        return str(data)

    # 3. Add object to the 'seen' set for the duration of its processing
    seen.add(obj_id)
    result = None
    try:
        # Prioritize handling of Memory objects to ensure they are never treated as generic artifacts.
        if _is_memory_obj(data):
            # A memory object's state is defined by its global and local stores. We serialize them separately.
            global_ref = _create_snapshot(data._global, context, serializer, seen)
            local_content = _serialize_for_log(data._local, context, serializer, seen)
            result = {"__type__": "MemoryObject", "global": global_ref, "local": local_content}
        # 4. Handle specific known container types
        elif isinstance(data, (list, tuple)):
            result = [_serialize_for_log(item, context, serializer, seen) for item in data]
        elif isinstance(data, dict):
            result = {str(k): _serialize_for_log(v, context, serializer, seen) for k, v in data.items()}
        # 5. Convert Python-specific types to a JSON-compatible representation
        elif isinstance(data, set):
            result = {"__type__": "set", "data": [_serialize_for_log(item, context, serializer, seen) for item in data]}
        elif isinstance(data, datetime):
            result = {'__type__': 'datetime', 'iso': data.isoformat()}
        elif isinstance(data, Path):
            result = {'__type__': 'path', 'path': str(data)}
        else:
            # 7. For any other complex object, offload it to a CBOR artifact.
            result = serializer.handle_as_cbor_artifact(data, context)
            if result is None:
                result = f"<Unserializable Object: {type(data).__name__}>"
    finally:
        # 8. IMPORTANT: We are done processing this object, so remove it from the 'seen' set
        seen.remove(obj_id)
    return result

# --- The Mixin Implementation ---

class FileLoggerNodeMixin:
    """A mixin that provides deep, secure logging by hooking into orchestrator methods."""
    def __init__(self, *args, log_folder: str = "brainyflow_logs", **kwargs):
        super().__init__(*args, **kwargs)
        self.log_folder = Path(log_folder)
        self.artifact_serializer = ArtifactSerializer()

    def _log_event(self, event_name: str, data: Dict[str, Any]):
        context = log_context_var.get()
        if not context: raise Exception(f"Log context not found when trying to log event '{event_name}' for node '{getattr(self, '_refer', self).__class__.__name__}'")

        mro_list = [cls.__name__ for cls in self.__class__.__mro__ if cls not in (object, ABC, Generic)]
        if 'BaseNode' not in mro_list: mro_list.append('BaseNode')
        mro_list = mro_list[:mro_list.index('BaseNode')+1]
        
        # This is now a JSON-serializable dictionary because _serialize_for_log offloads
        # complex objects to CBOR files and returns a JSON-friendly reference dict.
        log_entry = {
            "when": datetime.now().isoformat(),
            "node": f"{self.__class__.__name__}#{getattr(self, '_node_order', '?')}",
            "event": event_name,
            "data": _serialize_for_log(data, context, self.artifact_serializer, set()),
            # "mro": mro_list,
        }
        
        with open(context.session_log_path, 'a', encoding='utf-8') as f:
            f.write(json.dumps(log_entry) + '\n')
    
    # Hook into `exec_runner` to gain visibility into the results of `prep` and `exec`
    async def exec_runner(self, memory: "bf.Memory", prep_res: Any, **kwargs) -> Any:
        self._log_event("prep.exit", {"result": prep_res})
        # self._log_event("exec.enter", {"prep_result": prep_res})
        try:
            exec_res = await super().exec_runner(memory, prep_res, **kwargs)
            self._log_event("exec.exit", {"result": exec_res})
            return exec_res
        except Exception as error:
            self._log_event("exec.error", {"error": str(error), "retry": getattr(self, 'cur_retry', 0)})
            raise

    def trigger(self, action: str, forking_data: Optional[Dict[str, Any]] = None)-> None:
        self._log_event("trigger", {"action": action, "forking_data": forking_data})
        return super().trigger(action, forking_data)

    # Hook into the main `run` method to log the state before and after the node's execution.
    async def run(self, *args, **kwargs):
        context = log_context_var.get()
        is_flow = hasattr(self, 'start') # Duck-typing to check if it's a Flow

        # We only log node.enter for non-flow nodes, as the Flow mixin handles its own entry log.
        if context and not is_flow:
            memory_in = args[0] if args else {}
            self._log_event("node.enter", {"memory": memory_in})
        
        try:
            result = await super().run(*args, **kwargs)
            
            if context and not is_flow:
                memory_out = result[0][1] if isinstance(result, list) and result and isinstance(result[0], (list, tuple)) and len(result[0]) > 1 else args[0]
                self._log_event("node.exit", {"result": result, "memory": memory_out})

            return result
        except Exception as error:
            if context and not is_flow:
                 self._log_event("node.error", {"error": str(error)})
            raise

class FileLoggerFlowMixin(FileLoggerNodeMixin):
    """A mixin that establishes the logging context and logs flow-specific events."""
    async def run(self, *args, **kwargs):
        # This is the root of the logging context.
        ctx = log_context_var.get()
        is_root_call = ctx is None
        token = None

        if is_root_call:
            session_id = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
            ctx = LogContext(self.log_folder, session_id)
            token = log_context_var.set(ctx)

        try:
            # We log the flow's entry before calling super().run().
            # At this point, the context is guaranteed to be set for this task.
            initial_memory = args[0] if args else {}
            self._log_event("flow.enter", {"flow_type": self.__class__.__name__, "initial_memory": initial_memory})
            
            # This call will propagate down to FileLoggerNodeMixin.run
            result = await super().run(*args, **kwargs)
            
            final_memory = args[0] if args else {}
            self._log_event("flow.exit", {"execution_tree": result, "final_memory": final_memory})
            
            return result
        except Exception as error:
            final_memory = args[0] if args else {}
            self._log_event("flow.error", {"error": str(error), "final_memory": final_memory})
            raise
        finally:
            # The context is reset only at the very end of the root call.
            if is_root_call and token:
                log_context_var.reset(token)

