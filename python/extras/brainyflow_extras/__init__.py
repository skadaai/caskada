from __future__ import annotations
from typing import TYPE_CHECKING, Type, Union, Dict, Any

from .utils.logger import smart_print, setup, _config, _ensure_rich_traceback_installed, Console
from .utils.debug import debug_print

if TYPE_CHECKING:
    import brainyflow as bf
else:
    from .brainyflow_original import bf


#############################################################################################################
# Pure Exports from brainyflow
#############################################################################################################

for _name in dir(bf):
    if not _name.startswith('__'):
        globals()[_name] = getattr(bf, _name)

#############################################################################################################
# Universal Enhancement System
#############################################################################################################

from .enhancement import enhance, EnhancementBuilder

# Type checker knows this returns Type[Node]

#############################################################################################################
# Mixins (for advanced users who want direct access)
#############################################################################################################

from .mixins import *
