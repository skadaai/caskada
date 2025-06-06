from __future__ import annotations
import json
import time
from datetime import datetime
from pathlib import Path

from ..utils.logger import smart_print


class FileLoggerMixin:
    """
    A mixin for BaseNode derivatives to log execution progression as files.
    Creates one file per node execution in a local folder, sorted by execution order.
    
    Options:
        log_folder: Path to log folder (default: "brainyflow_logs")
        log_format: Format for log files (default: "json")
        include_memory: Whether to include memory snapshots (default: True)
        max_result_length: Max length for result summaries (default: 200)
    """
    
    def __init__(self, *args, log_folder: str = "brainyflow_logs", 
                 log_format: str = "json", include_memory: bool = True,
                 max_result_length: int = 200, **kwargs):
        super().__init__(*args, **kwargs)
        self._log_folder = Path(log_folder)
        self._log_format = log_format
        self._include_memory = include_memory
        self._max_result_length = max_result_length
        self._execution_start_time = None
        self._node_execution_counter = 0
        
    def _ensure_log_folder(self):
        """Ensure the log folder exists"""
        self._log_folder.mkdir(exist_ok=True)
        
    def _get_execution_timestamp(self):
        """Get a consistent timestamp for this execution session"""
        if self._execution_start_time is None:
            self._execution_start_time = datetime.now().strftime("%Y%m%d_%H%M%S")
        return self._execution_start_time
        
    def _increment_execution_counter(self):
        """Increment and return the execution counter for ordering"""
        self._node_execution_counter += 1
        return self._node_execution_counter
        
    def _create_log_entry(self, phase: str, data: dict = None, error: Exception = None):
        """Create a log entry for a specific execution phase"""
        timestamp = datetime.now().isoformat()
        node_order = getattr(self, '_node_order', 'unknown')
        class_name = self.__class__.__name__
        
        log_entry = {
            "timestamp": timestamp,
            "execution_order": self._increment_execution_counter(),
            "node_class": class_name,
            "node_order": node_order,
            "phase": phase,
            "data": data or {},
            "error": str(error) if error else None
        }
        
        return log_entry
        
    def _write_log_file(self, log_entry: dict):
        """Write log entry to a file"""
        self._ensure_log_folder()
        
        # Create filename with execution order for sorting
        execution_order = log_entry["execution_order"]
        node_class = log_entry["node_class"]
        node_order = log_entry["node_order"]
        phase = log_entry["phase"]
        session_timestamp = self._get_execution_timestamp()
        
        filename = f"{execution_order:04d}_{session_timestamp}_{node_class}#{node_order}_{phase}.json"
        filepath = self._log_folder / filename
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(log_entry, f, indent=2, ensure_ascii=False)
        except Exception as e:
            # Fallback: print to console if file writing fails
            smart_print(f"[red]Failed to write log file {filepath}: {e}[/red]")
            
    async def run(self, *args, **kwargs):
        """Override run to log the overall execution"""
        start_time = time.time()
        memory_snapshot = None
        
        # Try to capture memory state if available
        if args and hasattr(args[0], '__dict__'):
            try:
                # Create a safe snapshot of memory (avoid circular references)
                memory_snapshot = {
                    k: str(v) if not isinstance(v, (str, int, float, bool, type(None))) else v
                    for k, v in args[0].__dict__.items()
                    if not k.startswith('_')
                }
            except:
                memory_snapshot = {"note": "Memory snapshot unavailable"}
        
        # Log run start
        log_entry = self._create_log_entry(
            "run_start",
            {
                "args_count": len(args),
                "kwargs": {k: str(v) for k, v in kwargs.items()},
                "memory_snapshot": memory_snapshot
            }
        )
        self._write_log_file(log_entry)
        
        try:
            result = await super().run(*args, **kwargs)
            
            # Log run success
            end_time = time.time()
            log_entry = self._create_log_entry(
                "run_success",
                {
                    "execution_time_seconds": round(end_time - start_time, 3),
                    "result_type": type(result).__name__,
                    "result_summary": str(result)[:200] + "..." if len(str(result)) > 200 else str(result)
                }
            )
            self._write_log_file(log_entry)
            
            return result
            
        except Exception as error:
            # Log run error
            end_time = time.time()
            log_entry = self._create_log_entry(
                "run_error",
                {
                    "execution_time_seconds": round(end_time - start_time, 3),
                    "error_type": type(error).__name__
                },
                error
            )
            self._write_log_file(log_entry)
            raise
            
    async def exec_runner(self, *args, **kwargs):
        """Override exec_runner to log execution phases"""
        start_time = time.time()
        
        # Log prep phase start
        log_entry = self._create_log_entry("prep_start")
        self._write_log_file(log_entry)
        
        try:
            # Call the parent's exec_runner which handles prep, exec, and post
            result = await super().exec_runner(*args, **kwargs)
            
            # Log exec completion
            end_time = time.time()
            log_entry = self._create_log_entry(
                "exec_complete",
                {
                    "execution_time_seconds": round(end_time - start_time, 3),
                    "result_type": type(result).__name__
                }
            )
            self._write_log_file(log_entry)
            
            return result
            
        except Exception as error:
            # Log exec error
            end_time = time.time()
            log_entry = self._create_log_entry(
                "exec_error",
                {
                    "execution_time_seconds": round(end_time - start_time, 3),
                    "error_type": type(error).__name__
                },
                error
            )
            self._write_log_file(log_entry)
            raise