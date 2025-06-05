import sys
import os
import importlib.util
import importlib.metadata
from .utils.debug import debug_print

_bf_base_for_extras = None
_initial_sys_modules_brainyflow = sys.modules.get('brainyflow')

def _find_installed_brainyflow_location():
    """Find the actual installed location of the brainyflow package."""
    try:
        # Method 1: Relative path from extras location (works for development setup)
        current_file = os.path.abspath(__file__)
        # Go up from brainyflow_extras/ -> extras/ -> python/
        python_dir = os.path.dirname(os.path.dirname(os.path.dirname(current_file)))
        potential_brainyflow = os.path.join(python_dir, 'brainyflow.py')
        if os.path.exists(potential_brainyflow):
            debug_print(f"Found via relative path: {potential_brainyflow}")
            return potential_brainyflow

        # Method 2: Use importlib.metadata for installed packages
        distribution = importlib.metadata.distribution('brainyflow')
        if distribution.files:
            for file_path in distribution.files:
                if file_path.name == 'brainyflow.py':
                    install_location = file_path.locate()
                    if install_location.exists():
                        debug_print(f"Found via importlib.metadata: {install_location}")
                        return str(install_location)

        # Method 3: Search in site-packages
        for path in sys.path:
            if path and 'site-packages' in path:
                brainyflow_path = os.path.join(path, 'brainyflow.py')
                if os.path.exists(brainyflow_path):
                    debug_print(f"Found in site-packages: {brainyflow_path}")
                    return brainyflow_path

    except Exception as e:
        debug_print(f"Error finding brainyflow location: {e}")
    
    return None

# Try to find and load the base brainyflow
base_brainyflow_path = _find_installed_brainyflow_location()

if base_brainyflow_path:
    # Direct file loading (most reliable)
    try:
        spec = importlib.util.spec_from_file_location("brainyflow_base_internal", base_brainyflow_path)
        if spec and spec.loader:
            _bf_base_for_extras = importlib.util.module_from_spec(spec)
            sys.modules["brainyflow_base_internal"] = _bf_base_for_extras
            spec.loader.exec_module(_bf_base_for_extras)
            debug_print(f"Successfully loaded base from {base_brainyflow_path}")
        else:
            raise ImportError(f"Could not create module spec from {base_brainyflow_path}")
    except Exception as e:
        debug_print(f"Direct loading failed: {e}")
        _bf_base_for_extras = None

if _bf_base_for_extras is None:
    # Fallback: try sys.path manipulation (simplified)
    debug_print("Falling back to sys.path manipulation...")
    
    _original_sys_path = list(sys.path)
    
    # Remove potential shadowing paths
    if _initial_sys_modules_brainyflow and hasattr(_initial_sys_modules_brainyflow, '__file__'):
        shadow_file_path = os.path.abspath(_initial_sys_modules_brainyflow.__file__)
        shadow_dir = os.path.dirname(shadow_file_path)
        
        # Remove shadow directory and current working directory
        try:
            current_dir = os.getcwd()
            sys.path = [p for p in sys.path if os.path.abspath(p or current_dir) not in [shadow_dir, current_dir]]
        except OSError:
            pass

    # Clear module cache and try import
    if 'brainyflow' in sys.modules:
        del sys.modules['brainyflow']

    try:
        import brainyflow as _imported_base_brainyflow
        _bf_base_for_extras = _imported_base_brainyflow
        debug_print(f"Loaded base via sys.path manipulation from {getattr(_bf_base_for_extras, '__file__', 'unknown')}")
    except ImportError as e:
        sys.path = _original_sys_path
        if _initial_sys_modules_brainyflow:
            sys.modules['brainyflow'] = _initial_sys_modules_brainyflow
        
        raise ImportError(
            "brainyflow-extras requires the base 'brainyflow' library to be installed. "
            f"Could not load it using any method. Original error: {e}"
        ) from e
    finally:
        sys.path = _original_sys_path

# Restore the user's shadowing module if it existed
if _initial_sys_modules_brainyflow:
    sys.modules['brainyflow'] = _initial_sys_modules_brainyflow
elif 'brainyflow' not in sys.modules and _bf_base_for_extras:
    sys.modules['brainyflow'] = _bf_base_for_extras

bf = _bf_base_for_extras

if bf is None:
    raise ImportError("brainyflow-extras: Failed to load base 'brainyflow' module.")

# Debug output
debug_print(f"Final bf alias points to {bf} from {getattr(bf, '__file__', 'unknown location')}")
