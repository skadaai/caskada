from __future__ import annotations
from types import SimpleNamespace
from typing import List, Tuple, cast, Any, Dict, TYPE_CHECKING

import sys
import logging

from . import Memory, Node, Flow
from .utils.logger import Text, Console, ReprHighlighter
from .utils.logger import smart_print, setup, _config, _ensure_rich_traceback_installed, Console


# 1. Default Rich Console behavior
print("\n--- 1. Default Rich Console Logging ---")
smart_print("Hello", Text("Rich World", style="bold magenta"), {"data": [1,2,3]}, max_length=30)

class MyMemory(Memory): pass
mem = MyMemory({})
mem.default_rich_key= "This uses default Rich console."

# 2. Configure for standard Python logger
print("\n--- 2. Standard Python Logger (output to console via handler) ---")
std_logger = logging.getLogger("MyExtrasLogger")
std_logger.setLevel(logging.DEBUG) 
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
if not std_logger.hasHandlers(): 
    std_logger.addHandler(handler)

setup(
    output_handler=std_logger,
    logger_level_name="DEBUG", 
    smart_print_options_update={"max_length": 70, "truncate_suffix": "[...]"}
)
smart_print("Logging to std_logger:", Text("This Rich Text is now plain.", style="blue"), {"value": 42})
mem.std_log_key= "This goes to standard logger."

# 3. Configure for a custom callable (simple print)
print("\n--- 3. Custom Callable (simple print) ---")
def my_custom_print(s: str):
    print(f"CUSTOM PRINT: {s}")

setup(output_handler=my_custom_print, smart_print_options_update={"single_line": True})
smart_print("Using custom print:", Text("Multi\nLine\nText", style="green"), "becomes single line.")
mem.custom_print_key= "This uses the custom print function."

# 4. Back to Rich Console, but a new one, and test traceback
print("\n--- 4. New Rich Console & Traceback Test ---")
new_rich_console = Console(width=60, style="on blue")
setup(
    output_handler=new_rich_console,
    highlighter=ReprHighlighter(), 
    install_rich_traceback=True, 
    show_locals_in_traceback=True,
    verbose_mixin_logging=True 
)
smart_print("Switched to a new Rich Console with blue background!")
mem.new_rich_key= "Should appear on blue background console."

smart_print("Testing smart_print options directly:", "loooong string" * 10, max_length=50)

print("Testing Rich Traceback (expect an error message below):")
try:
    a = 1
    b = 0
    # c = a / b # Uncomment to see Rich traceback
    smart_print("If you uncommented the division by zero, a Rich traceback should have appeared.")
    if 'c' not in locals(): 
            smart_print("Division by zero was commented out, so no traceback this time.")
except ZeroDivisionError:
    smart_print("ZeroDivisionError caught (Rich traceback should have handled this).")

# 5. Disable verbose mixin logging
print("\n--- 5. Disabling Verbose Mixin Logging ---")
setup(verbose_mixin_logging=False, output_handler=Console()) 
smart_print("Verbose mixin logging is now OFF.")
mem.silent_key= "This _set_value call from mixin should NOT print."
smart_print("But smart_print itself still works.")
