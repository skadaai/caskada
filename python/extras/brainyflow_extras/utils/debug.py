import os

DEBUG_IMPORT = os.environ.get('BRAINYFLOW_DEBUG_IMPORT', '').lower() in ('1', 'true', 'on')

def debug_print(msg: str) -> None:
    """Print debug messages only when BRAINYFLOW_DEBUG_IMPORT is set."""
    if DEBUG_IMPORT:
        print(f"brainyflow_extras: {msg}")