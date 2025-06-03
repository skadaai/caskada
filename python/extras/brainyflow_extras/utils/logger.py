from __future__ import annotations
from types import SimpleNamespace
from typing import List, Tuple, Optional, cast, Any, Dict, Callable

import logging 
import sys 

from rich.text import Text
from rich.console import Console
from rich.highlighter import ReprHighlighter
from rich import traceback as rich_traceback

# --- Configuration Store ---

DEFAULT_SMART_PRINT_OPTIONS = {
    "max_length": None,
    "single_line": False,
    "truncate_suffix": "...",
    "sep": " ",
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
    smart_print_options_update: Optional[Dict[str, Any]] = None,
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
            warning_printer = _config.output_handler if isinstance(_config.output_handler, Console) else print
            warning_message = f"Warning: Invalid 'output_handler' type: {type(output_handler)}. Keeping previous handler."
            if isinstance(_config.output_handler, Console):
                _config.output_handler.print(f"[bold red]Warning:[/bold red] Invalid 'output_handler' type: {type(output_handler)}. Keeping previous handler.", style="red")
            else:
                print(warning_message)

    if highlighter is not None:
        if _config.output_mode == "rich":
            _config.highlighter = highlighter
        else:
            warning_printer = _config.output_handler if isinstance(_config.output_handler, Console) else print
            warning_message = "Warning: Highlighter provided but not in 'rich' output mode. It will be ignored."
            if isinstance(warning_printer, Console):
                 warning_printer.print(f"[yellow]{warning_message}[/yellow]")
            else:
                 print(warning_message)

    if logger_level_name is not None and _config.output_mode == "logger":
        level = getattr(logging, logger_level_name.upper(), None)
        if isinstance(level, int):
            _config.logger_level = level
        else:
            log_msg = f"Warning: Invalid 'logger_level_name': {logger_level_name}. Using current level."
            warning_printer = _config.output_handler if isinstance(_config.output_handler, Console) else print
            if isinstance(warning_printer, Console): warning_printer.print(f"[yellow]{log_msg}[/yellow]")
            else: print(log_msg)

    if previous_output_mode == "rich" and _config.output_mode != "rich":
        if _config.rich_traceback_installed:
            if _config.original_sys_excepthook is not None:
                sys.excepthook = _config.original_sys_excepthook
            else: # pragma: no cover
                sys.excepthook = sys.__excepthook__ 
            _config.rich_traceback_installed = False
            _config.original_sys_excepthook = None 

    if _config.output_mode == "rich":
        if not isinstance(_config.output_handler, Console): # pragma: no cover
            print("ERROR: Rich mode configured but output_handler is not a Rich Console. Traceback functionality may be impaired.")

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
            if not _config.rich_traceback_installed and _config.original_sys_excepthook is None:
                _config.original_sys_excepthook = sys.excepthook
            
            rich_traceback.install(
                console=_config.output_handler,
                show_locals=_config.show_locals_in_traceback
            )
            _config.rich_traceback_installed = True
        elif install_rich_traceback is False and _config.rich_traceback_installed:
            if _config.original_sys_excepthook is not None:
                sys.excepthook = _config.original_sys_excepthook
            else: # pragma: no cover
                sys.excepthook = sys.__excepthook__
            _config.rich_traceback_installed = False
            _config.original_sys_excepthook = None 
    else: 
        if _config.rich_traceback_installed: 
            if _config.original_sys_excepthook is not None:
                sys.excepthook = _config.original_sys_excepthook
            else: # pragma: no cover
                sys.excepthook = sys.__excepthook__
            _config.rich_traceback_installed = False
            _config.original_sys_excepthook = None

    if smart_print_options_update is not None:
        _config.smart_print_options.update(smart_print_options_update)

    if verbose_mixin_logging is not None:
        _config.verbose_mixin_logging = verbose_mixin_logging

def _ensure_rich_traceback_installed():
    if _config.output_mode == "rich" and \
       isinstance(_config.output_handler, Console) and \
       not _config.rich_traceback_installed:
        try:
            if _config.original_sys_excepthook is None: 
                 _config.original_sys_excepthook = sys.excepthook
            rich_traceback.install(
                console=_config.output_handler,
                show_locals=_config.show_locals_in_traceback
            )
            _config.rich_traceback_installed = True
        except Exception: # pragma: no cover
            if isinstance(_config.output_handler, Console):
                _config.output_handler.print_exception(show_locals=_config.show_locals_in_traceback)

def _convert_to_rich_text_for_item_summary(obj: Any, highlighter: ReprHighlighter, max_len: int = 20) -> Text:
    """Helper to convert an item to a Rich Text object for summaries, truncating it."""
    item_text: Text
    if isinstance(obj, Text):
        item_text = obj.copy() # Work on a copy to truncate
    elif isinstance(obj, str):
        item_text = Text.from_markup(obj)
    elif hasattr(obj, "__rich__"):
        try:
            rich_repr = obj.__rich__()
            item_text = rich_repr if isinstance(rich_repr, Text) else Text(str(rich_repr))
        except Exception: # pragma: no cover
            item_text = highlighter(str(obj))
    else:
        item_text = highlighter(str(obj))
    
    # Truncate the plain representation if it's too long
    if len(item_text.plain) > max_len:
        item_text.truncate(max_len, overflow="ellipsis")
    # Escape newlines in the plain representation to ensure it's visually one line
    item_text.plain = item_text.plain.replace("\n", "\\n").replace("\r", "\\r")
    return item_text

# --- Smart Print Function ---
def smart_print(*objects: Any, **override_options) -> None:
    _ensure_rich_traceback_installed()

    options = {**_config.smart_print_options, **override_options}
    actual_max_length = options['max_length']
    actual_single_line = options['single_line']
    actual_truncate_suffix = options['truncate_suffix']
    actual_sep = options['sep']

    if not objects:
        return

    processed_parts_for_joining = []

    for obj in objects:
        current_renderable_part: Any # Text for Rich, str for plain

        # Determine if a summary should be generated for this specific object
        should_generate_summary = (actual_single_line or (actual_max_length is not None)) and \
                                   (isinstance(obj, (list, tuple, dict)) or \
                                    ('numpy' in sys.modules and isinstance(obj, sys.modules['numpy'].ndarray)))

        if _config.output_mode == "rich":
            current_highlighter = _config.highlighter if _config.highlighter else ReprHighlighter()
            rich_part: Text

            if should_generate_summary:
                MAX_SUMMARY_ITEMS = 2
                MAX_ITEM_LEN_IN_SUMMARY = 20 # Max length for each item shown in summary
                
                if isinstance(obj, (list, tuple)):
                    type_name = type(obj).__name__
                    rich_part = Text(f"{type_name} ({len(obj)} items): [")
                    for item_idx, item in enumerate(obj[:MAX_SUMMARY_ITEMS]):
                        item_text = _convert_to_rich_text_for_item_summary(item, current_highlighter, max_len=MAX_ITEM_LEN_IN_SUMMARY)
                        rich_part.append(item_text)
                        if item_idx < len(obj) - 1 and item_idx < MAX_SUMMARY_ITEMS - 1:
                            rich_part.append(", ")
                    if len(obj) > MAX_SUMMARY_ITEMS:
                        rich_part.append(", ...")
                    rich_part.append("]")
                elif isinstance(obj, dict):
                    rich_part = Text(f"dict ({len(obj)} keys): {{")
                    items_shown_count = 0
                    for k_idx, (k, v) in enumerate(obj.items()):
                        if items_shown_count >= MAX_SUMMARY_ITEMS: break
                        k_text = _convert_to_rich_text_for_item_summary(k, current_highlighter, max_len=MAX_ITEM_LEN_IN_SUMMARY -5) # Shorter for key
                        v_text = _convert_to_rich_text_for_item_summary(v, current_highlighter, max_len=MAX_ITEM_LEN_IN_SUMMARY)
                        rich_part.append(k_text)
                        rich_part.append(": ")
                        rich_part.append(v_text)
                        items_shown_count += 1
                        if items_shown_count < MAX_SUMMARY_ITEMS and k_idx < len(obj) - 1 :
                            rich_part.append(", ")
                    if len(obj) > items_shown_count:
                        rich_part.append(", ...")
                    rich_part.append("}")
                elif 'numpy' in sys.modules and isinstance(obj, sys.modules['numpy'].ndarray):
                    rich_part = Text(f"np.ndarray (shape={obj.shape}, dtype={obj.dtype})")
                else: # Should not be reached if should_generate_summary is true only for collections
                    rich_part = _convert_to_rich_text_for_item_summary(obj, current_highlighter, max_len=100) # Fallback
            else: # Not a collection summary, full Rich processing for the object
                if isinstance(obj, Text): rich_part = obj.copy()
                elif isinstance(obj, str): rich_part = Text.from_markup(obj)
                elif hasattr(obj, "__rich__"):
                    try:
                        rich_repr = obj.__rich__()
                        rich_part = rich_repr if isinstance(rich_repr, Text) else Text(str(rich_repr))
                    except Exception: # pragma: no cover
                        rich_part = current_highlighter(str(obj))
                else:
                    rich_part = current_highlighter(str(obj))
                
                # If actual_single_line is true, escape newlines in the plain text part of the Rich object
                # This is a compromise to make it visually one line while trying to keep styles.
                if actual_single_line and '\n' in rich_part.plain:
                    escaped_plain = rich_part.plain.replace("\n", "\\n").replace("\r", "\\r")
                    # Create new Text with original style if possible, or plain
                    # This might simplify internal styling but preserves overall style.
                    style_to_apply = rich_part.style if rich_part.style else ""
                    rich_part = Text(escaped_plain, style=style_to_apply)
            current_renderable_part = rich_part

        else: # logger or callable mode (plain text)
            plain_str: str
            if should_generate_summary:
                MAX_SUMMARY_ITEMS = 2
                MAX_ITEM_LEN_IN_SUMMARY = 20
                if isinstance(obj, (list, tuple)):
                    type_name = type(obj).__name__
                    elements_str = []
                    for item in obj[:MAX_SUMMARY_ITEMS]:
                        item_s = Text.from_markup(str(item)).plain # Get plain, markup-stripped
                        if len(item_s) > MAX_ITEM_LEN_IN_SUMMARY: item_s = item_s[:MAX_ITEM_LEN_IN_SUMMARY-3] + "..."
                        elements_str.append(item_s)
                    suffix = ", ..." if len(obj) > MAX_SUMMARY_ITEMS else ""
                    plain_str = f"{type_name} ({len(obj)} items): [{', '.join(elements_str)}{suffix}]"
                elif isinstance(obj, dict):
                    items_str = []
                    items_shown_count = 0
                    for k, v in obj.items():
                        if items_shown_count >= MAX_SUMMARY_ITEMS: break
                        k_s = Text.from_markup(str(k)).plain
                        v_s = Text.from_markup(str(v)).plain
                        if len(k_s) > MAX_ITEM_LEN_IN_SUMMARY -7 : k_s = k_s[:MAX_ITEM_LEN_IN_SUMMARY-10] + "..."
                        if len(v_s) > MAX_ITEM_LEN_IN_SUMMARY : v_s = v_s[:MAX_ITEM_LEN_IN_SUMMARY-3] + "..."
                        items_str.append(f"{k_s}: {v_s}")
                        items_shown_count +=1
                    suffix = ", ..." if len(obj) > items_shown_count else ""
                    plain_str = f"dict ({len(obj)} keys): {{{', '.join(items_str)}{suffix}}}"
                elif 'numpy' in sys.modules and isinstance(obj, sys.modules['numpy'].ndarray):
                    plain_str = f"np.ndarray (shape={obj.shape}, dtype={obj.dtype})"
                else: # Should not be reached
                    plain_str = str(obj)
            else: # Not a collection summary, get plain string representation
                if isinstance(obj, Text): plain_str = obj.plain
                elif isinstance(obj, str): plain_str = Text.from_markup(obj).plain # Strip markup
                else: plain_str = str(obj)
            
            if actual_single_line: # Ensure newline escaping for the final plain string part
                plain_str = plain_str.replace("\n", "\\n").replace("\r", "\\r")
            current_renderable_part = plain_str
            
        processed_parts_for_joining.append(current_renderable_part)

    # --- Final Joining, Truncation, and Printing ---
    if _config.output_mode == "rich":
        final_output_rich: Text
        if not processed_parts_for_joining: final_output_rich = Text("")
        elif len(processed_parts_for_joining) == 1: final_output_rich = cast(Text, processed_parts_for_joining[0])
        else: final_output_rich = Text(actual_sep).join(cast(List[Text], processed_parts_for_joining))

        if actual_max_length is not None and len(final_output_rich.plain) > actual_max_length:
            final_output_rich.truncate(max_width=actual_max_length, overflow="ellipsis")
        
        if isinstance(_config.output_handler, Console):
            _config.output_handler.print(final_output_rich)
        else: # pragma: no cover
            print(f"ERROR: Rich mode with non-Console handler: {final_output_rich.plain}")

    else: # logger or callable mode
        final_output_plain = actual_sep.join(cast(List[str], processed_parts_for_joining)) # All parts are strings
        if actual_max_length is not None and len(final_output_plain) > actual_max_length:
            if actual_max_length > len(actual_truncate_suffix):
                 final_output_plain = final_output_plain[:actual_max_length - len(actual_truncate_suffix)] + actual_truncate_suffix
            else: # pragma: no cover
                 final_output_plain = final_output_plain[:actual_max_length]

        if _config.output_mode == "logger":
            if isinstance(_config.output_handler, logging.Logger):
                _config.output_handler.log(_config.logger_level, final_output_plain)
            else: # pragma: no cover
                print(f"Logger Error (misconfigured handler type: {type(_config.output_handler)}): {final_output_plain}")
        elif _config.output_mode == "callable":
            try:
                _config.output_handler(final_output_plain)
            except Exception as e: # pragma: no cover
                print(f"Error in custom output_handler callable: {e}", file=sys.stderr)
                print(f"Original message: {final_output_plain}", file=sys.stderr)

