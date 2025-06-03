
import logging
import sys

from typing import Optional, Any, Dict, Callable
from types import SimpleNamespace


from rich.text import Text
from rich.console import Console
from rich.highlighter import ReprHighlighter
from rich import traceback as rich_traceback

# --- Configuration Store ---

# Default smart_print options
DEFAULT_SMART_PRINT_OPTIONS = {
    "max_length": None,
    "single_line": False,
    "truncate_suffix": "...", # This will be used for manual truncation in non-Rich modes
    "sep": " ",
}

class ExtrasConfig(SimpleNamespace):
    """Holds the configuration for the extras library."""
    output_handler: Any  # rich.Console, logging.Logger, or a Callable[[str], None]
    output_mode: str     # "rich", "logger", "callable"
    highlighter: Optional[ReprHighlighter] # Only used effectively in "rich" mode
    smart_print_options: Dict[str, Any]
    verbose_mixin_logging: bool
    rich_traceback_installed: bool
    show_locals_in_traceback: bool # Only used if rich_traceback_installed
    logger_level: int # e.g. logging.INFO, logging.DEBUG (for "logger" mode)
    # Stores the sys.excepthook that was active *before* this library first installed Rich.
    # This is used to restore the original behavior upon uninstallation by this library.
    original_sys_excepthook: Optional[Callable] = None


# Initialize with default values
_config = ExtrasConfig(
    output_handler=Console(), # Default to Rich Console
    output_mode="rich",
    highlighter=ReprHighlighter(),
    smart_print_options=DEFAULT_SMART_PRINT_OPTIONS.copy(),
    verbose_mixin_logging=True,
    rich_traceback_installed=False,
    show_locals_in_traceback=True,
    logger_level=logging.INFO,
    original_sys_excepthook=None
)

# --- Setup Function ---

def setup(
    *,
    output_handler: Optional[Any] = None,
    highlighter: Optional[ReprHighlighter] = None,
    install_rich_traceback: Optional[bool] = None,
    show_locals_in_traceback: Optional[bool] = None,
    smart_print_options_update: Optional[Dict[str, Any]] = None,
    verbose_mixin_logging: Optional[bool] = None,
    logger_level_name: Optional[str] = None,
) -> None:
    """
    Configures the behavior of the extras library.
    (Full docstring omitted for brevity in this update, see previous versions)
    """
    global _config

    previous_output_mode = _config.output_mode
    new_output_handler_is_rich_console = False

    if output_handler is not None:
        if isinstance(output_handler, Console):
            _config.output_handler = output_handler
            _config.output_mode = "rich"
            new_output_handler_is_rich_console = True
            if _config.highlighter is None:
                 _config.highlighter = ReprHighlighter()
        elif isinstance(output_handler, logging.Logger):
            _config.output_handler = output_handler
            _config.output_mode = "logger"
            _config.highlighter = None
        elif callable(output_handler):
            _config.output_handler = output_handler
            _config.output_mode = "callable"
            _config.highlighter = None
        else:
            current_console = _config.output_handler if isinstance(_config.output_handler, Console) else Console()
            current_console.print(f"[bold red]Warning:[/bold red] Invalid 'output_handler' type: {type(output_handler)}. Keeping previous handler.", style="red")

    if highlighter is not None:
        if _config.output_mode == "rich":
            _config.highlighter = highlighter
        else:
            if isinstance(_config.output_handler, Console):
                 _config.output_handler.print("[yellow]Warning:[/yellow] Highlighter provided but not in 'rich' output mode. It will be ignored.")
            else:
                 print("Warning: Highlighter provided but not in 'rich' output mode. It will be ignored.")

    if logger_level_name is not None and _config.output_mode == "logger":
        level = getattr(logging, logger_level_name.upper(), None)
        if isinstance(level, int):
            _config.logger_level = level
        else:
            log_msg = f"[yellow]Warning:[/yellow] Invalid 'logger_level_name': {logger_level_name}. Using current level."
            if _config.output_mode == "rich" and isinstance(_config.output_handler, Console): _config.output_handler.print(log_msg)
            else: print(log_msg)

    # --- Rich Traceback Management ---
    if previous_output_mode == "rich" and _config.output_mode != "rich":
        if _config.rich_traceback_installed:
            if _config.original_sys_excepthook is not None:
                sys.excepthook = _config.original_sys_excepthook
            else:
                sys.excepthook = sys.__excepthook__ # Fallback to system default
            _config.rich_traceback_installed = False
            _config.original_sys_excepthook = None # Reset for a clean future install

    if _config.output_mode == "rich":
        if not isinstance(_config.output_handler, Console):
            print("Error: Rich mode configured but output_handler is not a Rich Console. Traceback may fail.")

        if show_locals_in_traceback is not None:
            _config.show_locals_in_traceback = show_locals_in_traceback

        should_install = False
        if install_rich_traceback is True:
            should_install = True
        elif install_rich_traceback is None:
            if new_output_handler_is_rich_console or \
               (show_locals_in_traceback is not None and _config.rich_traceback_installed) or \
               not _config.rich_traceback_installed:
                should_install = True
        
        if should_install and isinstance(_config.output_handler, Console):
            if not _config.rich_traceback_installed:
                # Capture the current hook only if Rich isn't already installed by us
                _config.original_sys_excepthook = sys.excepthook
            
            rich_traceback.install(
                console=_config.output_handler,
                show_locals=_config.show_locals_in_traceback
            )
            _config.rich_traceback_installed = True
        elif install_rich_traceback is False and _config.rich_traceback_installed:
            if _config.original_sys_excepthook is not None:
                sys.excepthook = _config.original_sys_excepthook
            else:
                sys.excepthook = sys.__excepthook__
            _config.rich_traceback_installed = False
            _config.original_sys_excepthook = None
    else: 
        if _config.rich_traceback_installed: # If mode changed away from rich, uninstall
            if _config.original_sys_excepthook is not None:
                sys.excepthook = _config.original_sys_excepthook
            else:
                sys.excepthook = sys.__excepthook__
            _config.rich_traceback_installed = False
            _config.original_sys_excepthook = None

    if smart_print_options_update is not None:
        _config.smart_print_options.update(smart_print_options_update)

    if verbose_mixin_logging is not None:
        _config.verbose_mixin_logging = verbose_mixin_logging


def _ensure_rich_traceback_installed():
    """Ensures Rich traceback is installed if in rich mode and not already installed by this lib."""
    if _config.output_mode == "rich" and \
       isinstance(_config.output_handler, Console) and \
       not _config.rich_traceback_installed:
        try:
            # Capture the original hook if this is the first install by this library
            if _config.original_sys_excepthook is None:
                 _config.original_sys_excepthook = sys.excepthook

            rich_traceback.install(
                console=_config.output_handler,
                show_locals=_config.show_locals_in_traceback
            )
            _config.rich_traceback_installed = True
        except Exception:
            if isinstance(_config.output_handler, Console):
                _config.output_handler.print_exception(show_locals=_config.show_locals_in_traceback)


# --- Smart Print Function ---
def smart_print(*objects: Any, **override_options) -> None:
    """
    Prints one or more objects using the configured output_handler and options.
    (Full docstring omitted for brevity, see previous versions)
    """
    _ensure_rich_traceback_installed()

    options = _config.smart_print_options.copy()
    options.update(override_options)

    actual_max_length = options['max_length']
    actual_single_line = options['single_line']
    actual_truncate_suffix = options['truncate_suffix']
    actual_sep = options['sep']

    if not objects:
        return

    if _config.output_mode == "rich":
        if not isinstance(_config.output_handler, Console):
            print("Error: Rich mode configured, but output_handler is not a Console. Cannot smart_print with Rich.", actual_sep.join(map(str, objects)))
            return

        text_objects = []
        current_highlighter = _config.highlighter if _config.highlighter else ReprHighlighter()

        for obj in objects:
            text_obj: Text
            if isinstance(obj, Text):
                text_obj = obj
            elif isinstance(obj, str):
                text_obj = Text.from_markup(obj)
            elif hasattr(obj, "__rich__"):
                try:
                    rich_repr = obj.__rich__()
                    if not isinstance(rich_repr, Text):
                        text_obj = current_highlighter(str(rich_repr))
                    else:
                        text_obj = rich_repr
                except Exception:
                    text_obj = current_highlighter(str(obj))
            else:
                text_obj = current_highlighter(str(obj))
            
            if actual_single_line:
                plain_text_for_single_line = text_obj.plain.replace("\n", "\\n").replace("\r", "\\r")
                text_obj = Text(plain_text_for_single_line, style=text_obj.style if text_obj.style else "")
            text_objects.append(text_obj)

        result_text: Text
        if not text_objects: result_text = Text("")
        elif len(text_objects) == 1: result_text = text_objects[0]
        else: result_text = Text(actual_sep).join(text_objects)

        if actual_max_length is not None and len(result_text.plain) > actual_max_length:
            result_text.truncate(max_width=actual_max_length, overflow="ellipsis")
        
        _config.output_handler.print(result_text)

    else:  # "logger" or "callable" mode (plain text)
        plain_strings = []
        for obj in objects:
            s: str
            if isinstance(obj, Text): s = obj.plain
            elif isinstance(obj, str): s = obj
            else: s = str(obj)

            if actual_single_line:
                s = s.replace("\n", "\\n").replace("\r", "\\r")
            plain_strings.append(s)

        output_string = actual_sep.join(plain_strings)

        if actual_max_length is not None and len(output_string) > actual_max_length:
            if actual_max_length > len(actual_truncate_suffix):
                 output_string = output_string[:actual_max_length - len(actual_truncate_suffix)] + actual_truncate_suffix
            else:
                 output_string = output_string[:actual_max_length]

        if _config.output_mode == "logger":
            if isinstance(_config.output_handler, logging.Logger):
                _config.output_handler.log(_config.logger_level, output_string)
            else:
                print(f"Logger Error (misconfigured handler): {output_string}")
        elif _config.output_mode == "callable":
            try:
                _config.output_handler(output_string)
            except Exception as e:
                print(f"Error in custom output_handler callable: {e}", file=sys.stderr)
                print(f"Original message: {output_string}", file=sys.stderr)
