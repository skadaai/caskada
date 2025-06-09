from __future__ import annotations
from types import SimpleNamespace
from typing import List, Tuple, Optional, cast, Any, Dict, Callable

import logging
import sys

from rich.text import Text
from rich.console import Console
from rich.highlighter import ReprHighlighter
from rich import traceback as rich_traceback
from rich.markup import escape as escape_markup # Import escape
from rich.errors import MarkupError # Import MarkupError

# --- Configuration Store ---
DEFAULT_SMART_PRINT_OPTIONS = {
    "max_length": None,  # Overall max length for the entire output line
    "single_line": False, # Attempt to render the entire output on a single line
    "truncate_suffix": "...",
    "sep": " ",
    "summary_max_items": 3,       # Max items to show in a summarized collection
    "summary_item_max_len": 30,   # Max char length for an item within a summary
    "summary_max_depth": 2,       # Max recursion depth for summarizing nested collections
}

class ExtrasConfig(SimpleNamespace):
    output_handler: Any
    output_mode: str
    highlighter: Optional[ReprHighlighter]
    smart_print_options: Dict[str, Any]
    verbose_mixin_logging: bool
    rich_traceback_installed: bool
    show_locals_in_traceback: bool
    logger_level: int
    original_sys_excepthook: Optional[Callable] = None

_config = ExtrasConfig(
    output_handler=Console(),
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
    smart_print_options: Optional[Dict[str, Any]] = None,
    verbose_mixin_logging: Optional[bool] = None,
    logger_level_name: Optional[str] = None,
) -> None:
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
            # Fallback to print for warning if handler is unusual
            warning_printer = print 
            if isinstance(_config.output_handler, Console):
                 warning_printer = _config.output_handler.print
            
            warning_message = f"Warning: Invalid 'output_handler' type: {type(output_handler)}. Keeping previous handler."
            if isinstance(_config.output_handler, Console): # Try to use rich style for warning
                _config.output_handler.print(f"[bold red]Warning:[/bold red] Invalid 'output_handler' type: {type(output_handler)}. Keeping previous handler.", style="red")
            else:
                print(warning_message, file=sys.stderr)


    if highlighter is not None:
        if _config.output_mode == "rich":
            _config.highlighter = highlighter
        else:
            warning_printer = print
            if isinstance(_config.output_handler, Console): # Try to use rich style for warning
                 warning_printer = lambda msg: _config.output_handler.print(f"[yellow]{msg}[/yellow]") # type: ignore
            warning_message = "Warning: Highlighter provided but not in 'rich' output mode. It will be ignored."
            warning_printer(warning_message)


    if logger_level_name is not None and _config.output_mode == "logger":
        level = getattr(logging, logger_level_name.upper(), None)
        if isinstance(level, int):
            _config.logger_level = level
        else:
            log_msg = f"Warning: Invalid 'logger_level_name': {logger_level_name}. Using current level."
            warning_printer = print
            if isinstance(_config.output_handler, Console):  # Try to use rich style for warning
                warning_printer = lambda msg: _config.output_handler.print(f"[yellow]{msg}[/yellow]") # type: ignore
            warning_printer(log_msg)

    # Handle Rich traceback installation/uninstallation when output mode changes
    if previous_output_mode == "rich" and _config.output_mode != "rich": # Switched away from Rich
        if _config.rich_traceback_installed:
            sys.excepthook = _config.original_sys_excepthook if _config.original_sys_excepthook else sys.__excepthook__
            _config.rich_traceback_installed = False
            _config.original_sys_excepthook = None 

    if _config.output_mode == "rich":
        if not isinstance(_config.output_handler, Console): # Should be caught by output_handler logic
            print("ERROR: Rich mode set but output_handler is not a Rich Console.", file=sys.stderr)
        
        if show_locals_in_traceback is not None:
            _config.show_locals_in_traceback = show_locals_in_traceback

        should_install_traceback = False
        if install_rich_traceback is True:
            should_install_traceback = True
        elif install_rich_traceback is None: # Default: install if needed or settings change
            if new_output_handler_is_rich_console or \
               (show_locals_in_traceback is not None and _config.rich_traceback_installed) or \
               not _config.rich_traceback_installed:
                should_install_traceback = True
        
        if should_install_traceback and isinstance(_config.output_handler, Console):
            if not _config.rich_traceback_installed and _config.original_sys_excepthook is None:
                _config.original_sys_excepthook = sys.excepthook
            
            rich_traceback.install(console=_config.output_handler, show_locals=_config.show_locals_in_traceback)
            _config.rich_traceback_installed = True
        elif install_rich_traceback is False and _config.rich_traceback_installed: # Explicit uninstall
            sys.excepthook = _config.original_sys_excepthook if _config.original_sys_excepthook else sys.__excepthook__
            _config.rich_traceback_installed = False
            _config.original_sys_excepthook = None
    else: # Not in "rich" mode
        if _config.rich_traceback_installed: # If we installed it, uninstall it
            sys.excepthook = _config.original_sys_excepthook if _config.original_sys_excepthook else sys.__excepthook__
            _config.rich_traceback_installed = False
            _config.original_sys_excepthook = None

    if smart_print_options is not None:
        _config.smart_print_options.update(smart_print_options)

    if verbose_mixin_logging is not None:
        _config.verbose_mixin_logging = verbose_mixin_logging

def _ensure_rich_traceback_installed(): # pragma: no cover (covered by setup)
    if _config.output_mode == "rich" and isinstance(_config.output_handler, Console) and not _config.rich_traceback_installed:
        try:
            if _config.original_sys_excepthook is None: 
                 _config.original_sys_excepthook = sys.excepthook
            rich_traceback.install(console=_config.output_handler, show_locals=_config.show_locals_in_traceback)
            _config.rich_traceback_installed = True
        except Exception:
            if isinstance(_config.output_handler, Console):
                _config.output_handler.print_exception(show_locals=_config.show_locals_in_traceback)
            else:
                import traceback
                traceback.print_exc(file=sys.stderr)


# --- Centralized Recursive Formatting Helper ---
def _format_obj_to_rich_text(
    obj: Any,
    options: Dict[str, Any],
    current_depth: int,
    highlighter: ReprHighlighter
) -> Text:

    # 1. Handle recursion depth limit
    if current_depth > options['summary_max_depth']:
        return Text(f"...(depth>{options['summary_max_depth']})...", style="dim")

    # 2. Handle basic types directly
    if isinstance(obj, (int, float, bool)) or obj is None:
        return Text(str(obj))
    
    # 3. Handle strings separately with care for markup and truncation
    if isinstance(obj, str):
        s_text: Text
        try:
            s_text = Text.from_markup(obj) # Try to parse as Rich markup
        except MarkupError:
            # If it's not valid markup, treat it like other objects: highlight its repr().
            s_text = highlighter(repr(obj)) # Fallback: highlight its repr()

        # Truncate string if it's an item within a summary (nested)
        if current_depth > 0 and options.get('summary_item_max_len') is not None:
            max_item_len = options['summary_item_max_len']
            if len(s_text.plain) > max_item_len:
                suffix = options['truncate_suffix']
                trunc_len = max_item_len - len(suffix)
                if trunc_len < 0: trunc_len = 0
                
                # Preserve style of the original s_text if it was simple (no complex spans)
                original_style = s_text.style if not s_text.spans else ""
                s_text = Text(s_text.plain[:trunc_len] + suffix, style=original_style)
        return s_text

    # 4. Determine if this object (collection or custom) should be summarized
    is_standard_collection = isinstance(obj, (list, tuple, dict)) or \
                             ('numpy' in sys.modules and isinstance(obj, sys.modules['numpy'].ndarray))
    
    # Custom objects are anything not basic, not string, not standard collection
    is_custom_object = not (is_standard_collection or isinstance(obj, (str, int, float, bool, type(None))))

    should_summarize = False
    if options['single_line']: # If overall print is single_line, summarize all non-basic/non-string objects
        if is_standard_collection or is_custom_object:
            should_summarize = True
    elif current_depth > 0: # If nested, summarize collections and custom objects
        if is_standard_collection or is_custom_object:
            should_summarize = True
    

    if should_summarize:
        summary_text = Text()
        num_items_to_show = options['summary_max_items']
        item_max_len_for_str_repr = options['summary_item_max_len'] # For str(custom_obj)

        if is_standard_collection:
            if isinstance(obj, (list, tuple)):
                summary_text.append(f"{type(obj).__name__} ({len(obj)} items): [")
                items_shown_count = 0
                for i, item in enumerate(obj):
                    if items_shown_count >= num_items_to_show:
                        summary_text.append(options['truncate_suffix'])
                        break
                    item_text = _format_obj_to_rich_text(item, options, current_depth + 1, highlighter)
                    summary_text.append(item_text)
                    items_shown_count +=1
                    if items_shown_count < num_items_to_show and i < len(obj) - 1:
                        summary_text.append(", ")
                summary_text.append("]")
            
            elif isinstance(obj, dict):
                summary_text.append(f"dict ({len(obj)} items): {{")
                items_shown_count = 0
                for i, (k, v) in enumerate(obj.items()):
                    if items_shown_count >= num_items_to_show:
                        summary_text.append(options['truncate_suffix'])
                        break
                    k_text = _format_obj_to_rich_text(k, options, current_depth + 1, highlighter)
                    v_text = _format_obj_to_rich_text(v, options, current_depth + 1, highlighter)
                    summary_text.append(k_text).append(": ").append(v_text)
                    items_shown_count += 1
                    if items_shown_count < num_items_to_show and i < len(obj) - 1:
                         summary_text.append(", ")
                summary_text.append("}")

            elif 'numpy' in sys.modules and isinstance(obj, sys.modules['numpy'].ndarray): # pragma: no cover
                summary_text = Text(f"np.ndarray (shape={obj.shape}, dtype={obj.dtype})")
        
        elif is_custom_object: # Summarize custom objects
            try:
                obj_str = str(obj)
            except Exception: # pragma: no cover
                obj_str = f"<{type(obj).__name__} (str error)>"
            
            suffix = options['truncate_suffix']
            if len(obj_str) > item_max_len_for_str_repr:
                trunc_len = item_max_len_for_str_repr - len(suffix)
                if trunc_len < 0: trunc_len = 0
                obj_str = obj_str[:trunc_len] + suffix
            
            summary_text = Text(f"<{type(obj).__name__}: '{obj_str}'>")
            # You could also try to get a "name" or "id" attribute for a more descriptive summary
            # e.g., if hasattr(obj, 'id'): summary_text = Text(f"{type(obj).__name__}(id='{obj.id}', ...)")

        else: # Should not be reached due to prior checks
            return highlighter(repr(obj))

        return summary_text

    # 5. If not summarizing, render the object "fully" using Rich capabilities
    if isinstance(obj, Text):
        return obj.copy()
    if hasattr(obj, "__rich_console__") and callable(obj.__rich_console__):
        try:
            # Rich Console Protocol: yields renderables
            temp_console = Console(width=120, highlighter=highlighter) # Temp console for rendering
            with temp_console.capture() as capture:
                for renderable in obj.__rich_console__(_config.output_handler if isinstance(_config.output_handler, Console) else temp_console, temp_console.options):
                    temp_console.print(renderable)
            rich_repr_str = capture.get()
            return Text(rich_repr_str.rstrip('\n'))
        except Exception as e_rich_console: # pragma: no cover
            # Fall through to __rich__ or repr
            pass

    if hasattr(obj, "__rich__") and callable(obj.__rich__):
        try:
            rich_repr = obj.__rich__()
            return rich_repr if isinstance(rich_repr, Text) else Text(str(rich_repr))
        except Exception as e_rich: # pragma: no cover
            pass
    
    return highlighter(repr(obj))


# --- Smart Print Function
def smart_print(*objects: Any, **override_options) -> None:
    _ensure_rich_traceback_installed()

    options = {**_config.smart_print_options, **override_options}
    
    is_rich_mode = _config.output_mode == "rich"
    current_highlighter = _config.highlighter if is_rich_mode and _config.highlighter is not None else ReprHighlighter()

    processed_texts: List[Text] = []

    for i, obj_to_print in enumerate(objects):
        text_part = _format_obj_to_rich_text(obj_to_print, options, 0, current_highlighter)
        
        # This 'single_line' post-processing for the plain representation might still be desired
        # for the very final output, but the summarization should do most of the work.
        if options['single_line'] and '\n' in text_part.plain:
            escaped_plain = text_part.plain.replace("\n", "\\n").replace("\r", "\\r")
            simple_style = text_part.style if text_part.style and not text_part.spans else ""
            text_part = Text(escaped_plain, style=simple_style) # This might lose complex styling from original text_part

        processed_texts.append(text_part)

    final_text = Text(options['sep']).join(processed_texts)

    # Apply overall max_length truncation
    max_len = options['max_length']
    if max_len is not None and len(final_text.plain) > max_len:
        suffix = options['truncate_suffix']
        truncated_len = max_len - len(suffix)
        if truncated_len < 0: truncated_len = 0
        final_text = Text(final_text.plain[:truncated_len] + suffix) # New Text from truncated plain
    
    # Output
    if _config.output_mode == "rich":
        if isinstance(_config.output_handler, Console):
            _config.output_handler.print(final_text)
        else: # pragma: no cover
            print(f"Rich Mode Error (handler not Console): {final_text.plain}", file=sys.stderr)
    elif _config.output_mode == "logger":
        if isinstance(_config.output_handler, logging.Logger):
            _config.output_handler.log(_config.logger_level, final_text.plain)
        else: # pragma: no cover
            print(f"Logger Error (misconfigured handler: {type(_config.output_handler)}): {final_text.plain}", file=sys.stderr)
    elif _config.output_mode == "callable":
        try:
            _config.output_handler(final_text.plain)
        except Exception as e: # pragma: no cover
            print(f"Error in custom output_handler callable: {e}", file=sys.stderr)
            print(f"Original message: {final_text.plain}", file=sys.stderr)

