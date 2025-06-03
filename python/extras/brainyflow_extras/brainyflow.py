import sys
import os
# import importlib # Not strictly needed for this approach but useful for other import manipulations

_bf_base_for_extras = None
_shadowing_brainyflow_module_obj_at_start = sys.modules.get('brainyflow')
_shadowing_brainyflow_dir_path = None
_original_sys_path = list(sys.path) # Make a copy to restore later
_shadowing_path_was_in_sys_path = False

if _shadowing_brainyflow_module_obj_at_start and hasattr(_shadowing_brainyflow_module_obj_at_start, '__file__') and _shadowing_brainyflow_module_obj_at_start.__file__:
    _shadowing_brainyflow_filepath = os.path.abspath(_shadowing_brainyflow_module_obj_at_start.__file__)
    _shadowing_brainyflow_dir_path = os.path.dirname(_shadowing_brainyflow_filepath)

    # Temporarily remove the shadowing path from sys.path if it's present
    if _shadowing_brainyflow_dir_path in sys.path:
        sys.path = [p for p in sys.path if p != _shadowing_brainyflow_dir_path]
        _shadowing_path_was_in_sys_path = True # Mark that we modified sys.path

# Temporarily remove the potentially shadowing 'brainyflow' module from Python's import cache.
# This is important so that the subsequent import statement re-evaluates finders.
if 'brainyflow' in sys.modules:
    del sys.modules['brainyflow']

try:
    # 3. Attempt to import the base 'brainyflow' library.
    #    With the shadowing directory path temporarily removed from sys.path,
    #    this should find the version installed in site-packages or otherwise
    #    next in the modified sys.path, bypassing the user's local "switch" file.
    import brainyflow as _imported_base_brainyflow # This should be the "real" base library
    _bf_base_for_extras = _imported_base_brainyflow
except ImportError as e:
    # If the import fails, it means the base 'brainyflow' is not installed or not findable.
    # Restore sys.path first.
    if _shadowing_path_was_in_sys_path and _shadowing_brainyflow_dir_path:
        # Only add it back if it was there and we have a valid path.
        # Check if it's already back (e.g., due to nested imports that restored it).
        if _shadowing_brainyflow_dir_path not in sys.path:
            # A common place to add it back is at the beginning, where Python usually puts script dirs.
            sys.path.insert(0, _shadowing_brainyflow_dir_path)
    else: # If we didn't modify sys.path, ensure it's fully restored from original copy
        sys.path = _original_sys_path

    # Then restore the user's shadowing module if it was present.
    if _shadowing_brainyflow_module_obj_at_start:
        sys.modules['brainyflow'] = _shadowing_brainyflow_module_obj_at_start
    
    raise ImportError(
        "brainyflow-extras requires the base 'brainyflow' library to be installed and importable. "
        f"Could not load it. Original error: {e}"
    ) from e
finally:
    # 4. CRITICAL: Restore sys.path to its original state to avoid side effects for other imports.
    #    If we removed the shadowing path, add it back to where it likely was (often the start).
    #    A simple restoration to the original list is safest.
    sys.path = _original_sys_path

    # CRITICAL: Restore the original (potentially shadowing) 'brainyflow' module
    #    into sys.modules. This ensures that when the user's application code
    #    (outside of brainyflow-extras) performs 'import brainyflow', it gets the
    #    module that it expects (i.e., their shadowing "switch" file, if it existed).
    if _shadowing_brainyflow_module_obj_at_start:
        sys.modules['brainyflow'] = _shadowing_brainyflow_module_obj_at_start
    elif 'brainyflow' not in sys.modules and _bf_base_for_extras:
        # This case handles if 'brainyflow' wasn't initially in sys.modules (e.g., extras imported first directly)
        # or if it was the base that was initially there.
        # We ensure the base we loaded is available as 'brainyflow' if no shadow needs restoring.
        sys.modules['brainyflow'] = _bf_base_for_extras

# 5. Alias the successfully imported base brainyflow for use within this module.
bf = _bf_base_for_extras

if bf is None:
    # This should ideally be caught by the ImportError in the try block, but as a safeguard:
    raise ImportError("Failed to load base 'brainyflow' for brainyflow-extras due to an unexpected issue.")

# The rest of your brainyflow_extras.py code (not shown here) that uses 'bf'
# can now proceed, assuming 'bf' refers to the "raw" brainyflow library's components.
