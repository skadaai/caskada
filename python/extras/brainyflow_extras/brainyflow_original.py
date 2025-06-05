import sys
import os
import importlib.util
import importlib.metadata
from pathlib import Path

_bf_base_for_extras = None
_initial_sys_modules_brainyflow = sys.modules.get('brainyflow')

def _find_installed_brainyflow_location():
    """Find the actual installed location of the brainyflow package."""
    try:
        # Method 1: Try importlib.metadata (Python 3.8+)
        try:
            distribution = importlib.metadata.distribution('brainyflow')
            # Get the installation location
            if distribution.files:
                # Find the brainyflow.py file in the distribution
                for file_path in distribution.files:
                    if file_path.name == 'brainyflow.py':
                        # Reconstruct the full path
                        install_location = file_path.locate()
                        if install_location.exists():
                            return str(install_location)
        except (importlib.metadata.PackageNotFoundError, AttributeError):
            pass

        # Method 2: Try pkg_resources (fallback for older Python)
        try:
            import pkg_resources
            distribution = pkg_resources.get_distribution('brainyflow')
            # Look for brainyflow.py in the egg-info or installed files
            try:
                installed_files = distribution.get_metadata('RECORD').splitlines()
                for line in installed_files:
                    if 'brainyflow.py' in line:
                        file_path = line.split(',')[0]  # RECORD format: path,hash,size
                        full_path = os.path.join(distribution.location, file_path)
                        if os.path.exists(full_path):
                            return full_path
            except Exception:
                # If RECORD doesn't exist, try looking directly in the distribution location
                brainyflow_path = os.path.join(distribution.location, 'brainyflow.py')
                if os.path.exists(brainyflow_path):
                    return brainyflow_path
        except (ImportError, Exception):  # Fixed the pkg_resources error handling
            pass

        # Method 3: Search in likely locations
        # Check site-packages and other common locations
        for path in sys.path:
            if path and ('site-packages' in path or 'dist-packages' in path):
                brainyflow_path = os.path.join(path, 'brainyflow.py')
                if os.path.exists(brainyflow_path):
                    return brainyflow_path

        # Method 4: If installed in editable mode, try to find it in development directories
        # Look for paths that contain 'brainyFlow' (the project name) but not 'brainyAbba' (user's app)
        for path in sys.path:
            if path and 'brainyFlow' in path and 'brainyAbba' not in path:
                potential_paths = [
                    os.path.join(path, 'brainyflow.py'),
                    os.path.join(path, 'python', 'brainyflow.py'),  # if path is project root
                ]
                for potential_path in potential_paths:
                    if os.path.exists(potential_path):
                        return potential_path

        # Method 5: Try relative path from extras location (development setup)
        # Since we know the structure: brainyFlow/python/brainyflow.py and brainyFlow/python/extras/brainyflow_extras/
        current_file = os.path.abspath(__file__)
        # Go up from brainyflow_extras/ -> extras/ -> python/
        python_dir = os.path.dirname(os.path.dirname(os.path.dirname(current_file)))
        potential_brainyflow = os.path.join(python_dir, 'brainyflow.py')
        if os.path.exists(potential_brainyflow):
            return potential_brainyflow

    except Exception as e:
        # If all methods fail, we'll try the import bypass method as fallback
        print(f"Warning: Could not determine brainyflow installation location: {e}")
    
    return None

# Try to find the installed brainyflow location
base_brainyflow_path = _find_installed_brainyflow_location()

if base_brainyflow_path:
    # Method A: Direct file loading (most reliable)
    try:
        spec = importlib.util.spec_from_file_location("brainyflow_base_internal", base_brainyflow_path)
        if spec and spec.loader:
            _bf_base_for_extras = importlib.util.module_from_spec(spec)
            # Important: Add to sys.modules under a unique name to handle any internal imports
            sys.modules["brainyflow_base_internal"] = _bf_base_for_extras
            spec.loader.exec_module(_bf_base_for_extras)
            print(f"brainyflow_extras: Successfully loaded base from {base_brainyflow_path}")
        else:
            raise ImportError(f"Could not create module spec from {base_brainyflow_path}")
    except Exception as e:
        print(f"Warning: Direct loading failed: {e}")
        _bf_base_for_extras = None

if _bf_base_for_extras is None:
    # Method B: More aggressive sys.path manipulation
    print("brainyflow_extras: Falling back to aggressive sys.path manipulation method...")
    
    _original_sys_path = list(sys.path)
    
    # More aggressive path cleaning - remove any path that could contain the shadowing file
    if _initial_sys_modules_brainyflow and hasattr(_initial_sys_modules_brainyflow, '__file__'):
        shadow_file_path = os.path.abspath(_initial_sys_modules_brainyflow.__file__)
        shadow_dir = os.path.dirname(shadow_file_path)
        
        # Get current working directory
        try:
            current_dir = os.getcwd()
        except OSError:
            current_dir = None
        
        # Remove paths that could lead to the shadow
        cleaned_path = []
        for path in sys.path:
            abs_path = os.path.abspath(path) if path else current_dir
            should_remove = (
                abs_path == shadow_dir or 
                abs_path == current_dir or
                path == '' or 
                path == '.' or
                (shadow_dir and abs_path and abs_path == shadow_dir)
            )
            if not should_remove:
                cleaned_path.append(path)
        
        sys.path = cleaned_path

    # Clear the module cache
    if 'brainyflow' in sys.modules:
        del sys.modules['brainyflow']

    try:
        import brainyflow as _imported_base_brainyflow
        _bf_base_for_extras = _imported_base_brainyflow
        
        # Sanity check: ensure we didn't get the shadow again
        if (hasattr(_bf_base_for_extras, '__file__') and 
            _initial_sys_modules_brainyflow and
            hasattr(_initial_sys_modules_brainyflow, '__file__')):
            
            base_path = os.path.abspath(_bf_base_for_extras.__file__)
            shadow_path = os.path.abspath(_initial_sys_modules_brainyflow.__file__)
            
            if base_path == shadow_path:
                raise ImportError("Aggressive sys.path manipulation still failed to bypass shadow")
        
        print(f"brainyflow_extras: Loaded base via aggressive import from {getattr(_bf_base_for_extras, '__file__', 'unknown')}")
        
    except ImportError as e:
        # Restore sys.path before re-raising
        sys.path = _original_sys_path
        if _initial_sys_modules_brainyflow:
            sys.modules['brainyflow'] = _initial_sys_modules_brainyflow
        
        raise ImportError(
            "brainyflow-extras requires the base 'brainyflow' library to be installed. "
            f"Could not load it using any method. Original error: {e}"
        ) from e
    finally:
        # Always restore sys.path
        sys.path = _original_sys_path

# Restore the user's shadowing module if it existed
if _initial_sys_modules_brainyflow:
    sys.modules['brainyflow'] = _initial_sys_modules_brainyflow
elif 'brainyflow' not in sys.modules and _bf_base_for_extras:
    # If no shadow existed, make the base available
    sys.modules['brainyflow'] = _bf_base_for_extras

bf = _bf_base_for_extras

if bf is None:
    raise ImportError("brainyflow-extras: Failed to load base 'brainyflow' module.")

# Debug output
print(f"brainyflow_extras: Final bf alias points to {bf} from {getattr(bf, '__file__', 'unknown location')}")
