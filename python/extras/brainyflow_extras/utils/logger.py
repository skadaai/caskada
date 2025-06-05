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

# --- Setup Function (ensure it can update new smart_print_options) ---
def setup(
    *,
    output_handler: Optional[Any] = None,
    highlighter: Optional[ReprHighlighter] = None,
    install_rich_traceback: Optional[bool] = None,
    show_locals_in_traceback: Optional[bool] = None,
    smart_print_options_update: Optional[Dict[str, Any]] = None, # Accepts new options
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
            # This should ideally not happen if setup logic is correct
            print("ERROR: Rich mode configured but output_handler is not a Rich Console. Traceback functionality may be impaired.", file=sys.stderr)
            # Fallback to a default console for traceback if possible, or log error
        
        if show_locals_in_traceback is not None:
            _config.show_locals_in_traceback = show_locals_in_traceback

        should_install_traceback = False
        if install_rich_traceback is True:
            should_install_traceback = True
        elif install_rich_traceback is None: # Default behavior: install if not installed or if settings change
            if new_output_handler_is_rich_console or \
               (show_locals_in_traceback is not None and _config.rich_traceback_installed) or \
               not _config.rich_traceback_installed:
                should_install_traceback = True
        
        if should_install_traceback and isinstance(_config.output_handler, Console):
            if not _config.rich_traceback_installed and _config.original_sys_excepthook is None:
                _config.original_sys_excepthook = sys.excepthook # Store only if we are installing for the first time
            
            rich_traceback.install(
                console=_config.output_handler,
                show_locals=_config.show_locals_in_traceback
            )
            _config.rich_traceback_installed = True
        elif install_rich_traceback is False and _config.rich_traceback_installed: # Explicitly uninstall
            if _config.original_sys_excepthook is not None:
                sys.excepthook = _config.original_sys_excepthook
            else: # pragma: no cover
                # This case implies it was installed externally or original_sys_excepthook wasn't captured.
                # Reverting to Python's default might be the safest.
                sys.excepthook = sys.__excepthook__
            _config.rich_traceback_installed = False
            _config.original_sys_excepthook = None # Clear stored hook as it's restored
    else: # Not in "rich" output mode
        # If rich traceback was installed by us, uninstall it
        if _config.rich_traceback_installed: 
            if _config.original_sys_excepthook is not None:
                sys.excepthook = _config.original_sys_excepthook
            else: # pragma: no cover
                sys.excepthook = sys.__excepthook__
            _config.rich_traceback_installed = False
            _config.original_sys_excepthook = None

    if smart_print_options_update is not None:
        _config.smart_print_options.update(smart_print_options_update)
        # Validate new options if necessary, e.g., ensure types are correct

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
             # If installation fails, print exception using the handler if it's a Console,
             # otherwise, just use a standard print to stderr.
            if isinstance(_config.output_handler, Console):
                _config.output_handler.print_exception(show_locals=_config.show_locals_in_traceback)
            else:
                import traceback
                traceback.print_exc()

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

    # 2. Handle basic types and strings directly
    if isinstance(obj, (int, float, bool)) or obj is None:
        return Text(str(obj))
    if isinstance(obj, str):
        # For strings that are items within a summary (depth > 0), apply summary_item_max_len.
        # Top-level strings (depth 0) are handled by overall max_length later.
        s_text = Text.from_markup(obj) # Try to preserve user's markup
        if current_depth > 0 and len(s_text.plain) > options['summary_item_max_len']:
            s_text.truncate(options['summary_item_max_len'], overflow="ellipsis")
            s_text.plain = s_text.plain + options['truncate_suffix']
        return s_text
    
    # 3. Determine if this object (collection or complex) should be summarized
    is_collection_type = isinstance(obj, (list, tuple, dict)) or \
                         ('numpy' in sys.modules and isinstance(obj, sys.modules['numpy'].ndarray))

    # Summarize if:
    #   a) 'single_line' is true for the whole smart_print call, AND it's a collection.
    #   b) OR it's a collection and we are already nested (current_depth > 0).
    should_summarize_this_obj = (options['single_line'] and is_collection_type) or \
                                (current_depth > 0 and is_collection_type)
    

    if should_summarize_this_obj:
        summary_text = Text()
        num_items_to_show = options['summary_max_items']
        item_max_len = options['summary_item_max_len'] # For items *within* this summary

        if isinstance(obj, (list, tuple)):
            summary_text.append(f"{type(obj).__name__} ({len(obj)} items): [")
            for i, item in enumerate(obj):
                if i >= num_items_to_show:
                    summary_text.append(options['truncate_suffix'])
                    break
                item_text = _format_obj_to_rich_text(item, options, current_depth + 1, highlighter)
                # item_text is already truncated if it was a string and current_depth+1 > 0
                summary_text.append(item_text)
                if i < min(len(obj), num_items_to_show) - 1 and i < len(obj)-1 : # Check against actual length too
                    summary_text.append(", ")
            summary_text.append("]")
        
        elif isinstance(obj, dict):
            summary_text.append(f"dict ({len(obj)} items): {{")
            count = 0
            for k_idx, (k, v) in enumerate(obj.items()):
                if count >= num_items_to_show:
                    summary_text.append(options['truncate_suffix'])
                    break
                k_text = _format_obj_to_rich_text(k, options, current_depth + 1, highlighter)
                v_text = _format_obj_to_rich_text(v, options, current_depth + 1, highlighter)
                
                summary_text.append(k_text)
                summary_text.append(": ")
                summary_text.append(v_text)
                count += 1
                # Add comma if not the last item to be shown AND not the actual last item in dict
                if count < min(len(obj), num_items_to_show) and k_idx < len(obj) -1:
                     summary_text.append(", ")
            summary_text.append("}")

        elif 'numpy' in sys.modules and isinstance(obj, sys.modules['numpy'].ndarray):
            summary_text = Text(f"np.ndarray (shape={obj.shape}, dtype={obj.dtype})")
        
        else: # Should not be reached due to should_summarize_this_obj conditions
            return highlighter(repr(obj)) # Fallback to full repr if logic error

        return summary_text

    # 4. If not summarizing, render the object "fully" using Rich capabilities
    if isinstance(obj, Text): # Already Rich Text
        return obj.copy()
    # For strings, handled above (as Text.from_markup)
    if hasattr(obj, "__rich__"):
        try:
            rich_repr = obj.__rich__()
            return rich_repr if isinstance(rich_repr, Text) else Text(str(rich_repr))
        except Exception: # pragma: no cover
            return highlighter(repr(obj)) 
    
    # Default for other types (including collections not summarized): use highlighter on repr
    # Rich Console's print will do the "pretty" printing for collections based on this.
    return highlighter(repr(obj))


# --- Smart Print Function ---
def smart_print(*objects: Any, **override_options) -> None:
    _ensure_rich_traceback_installed()

    options = {**_config.smart_print_options, **override_options}
    
    is_rich_mode = _config.output_mode == "rich"
    # Ensure highlighter for rich mode, even if _config.highlighter is None (though setup should init)
    highlighter = _config.highlighter if is_rich_mode and _config.highlighter else ReprHighlighter()

    processed_texts: List[Text] = []

    for i, obj in enumerate(objects):
        text_part = _format_obj_to_rich_text(obj, options, 0, highlighter)
        
        # Handle 'single_line' post-formatting for this part's plain representation
        # This affects the visual output but might alter Rich styling if not careful.
        # The summarization logic should primarily achieve the single-line effect for collections.
        if options['single_line'] and '\n' in text_part.plain:
            # Forcibly make it single line by replacing newlines in its plain form.
            # This is a visual override; original Rich structure might be multi-line.
            escaped_plain = text_part.plain.replace("\n", "\\n").replace("\r", "\\r")
            # Re-create Text. This might lose complex internal styling of the original text_part.
            # If text_part was simple (e.g., from a basic type or simple string), style might be preserved.
            simple_style = text_part.style if text_part.style and not text_part.spans else ""
            text_part = Text(escaped_plain, style=simple_style)

        processed_texts.append(text_part)

    # Join the processed Text objects
    final_text = Text(options['sep']).join(processed_texts)


    # Apply overall max_length truncation to the final joined Text
    max_len = options['max_length']
    if max_len is not None and len(final_text.plain) > max_len:
        # The real problem and fix, as suffix is not a parameter to Text.truncate
        truncated_len = max_len - len(options['truncate_suffix'])
        if truncated_len < 0:
            truncated_len = 0  # Avoid negative slice
        truncated_text = final_text.plain[:truncated_len]
        truncated_text += options['truncate_suffix']
        final_text = Text(truncated_text)
    
    # Print using the configured handler
    if _config.output_mode == "rich":
        if isinstance(_config.output_handler, Console):
            _config.output_handler.print(final_text)
        else: # pragma: no cover
            # Fallback if handler is misconfigured
            print(f"Rich Mode Error (handler not Console): {final_text.plain}")
    elif _config.output_mode == "logger":
        if isinstance(_config.output_handler, logging.Logger):
            _config.output_handler.log(_config.logger_level, final_text.plain)
        else: # pragma: no cover
            print(f"Logger Error (misconfigured handler: {type(_config.output_handler)}): {final_text.plain}")
    elif _config.output_mode == "callable":
        try:
            _config.output_handler(final_text.plain)
        except Exception as e: # pragma: no cover
            print(f"Error in custom output_handler callable: {e}", file=sys.stderr)
            print(f"Original message: {final_text.plain}", file=sys.stderr)
