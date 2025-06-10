"""
Universal enhancement system for BrainyFlow classes.
Provides intuitive, discoverable API for applying mixins without knowing their names.
"""
from __future__ import annotations
from typing import TYPE_CHECKING, Union, Dict, Any, Type, Optional, overload, TypeVar
from dataclasses import dataclass
import uuid
import types

if TYPE_CHECKING:
    import brainyflow as bf
else:
    from .brainyflow_original import bf

from .mixins import (
    VerboseMemoryMixin,
    VerboseNodeMixin,
    ExecutionTreePrinterMixin,
    FileLoggerNodeMixin,
    FileLoggerFlowMixin,
    SingleThreadedMixin,
    PerformanceMonitorMixin,
)

# Type variables for proper generic typing
T = TypeVar('T')

# Type definitions for options
VerboseOptions = Union[bool, Dict[str, Any]]
FileLoggingOptions = Union[bool, Dict[str, Any]]
PerformanceOptions = Union[bool, Dict[str, Any]]
SingleThreadedOptions = Union[bool, Dict[str, Any]]
ExecutionTreeOptions = Union[bool, Dict[str, Any]]


@dataclass
class EnhancementConfig:
    """Configuration for enhancements"""
    verbose: Optional[VerboseOptions] = None
    file_logging: Optional[FileLoggingOptions] = None
    performance: Optional[PerformanceOptions] = None
    single_threaded: Optional[SingleThreadedOptions] = None
    execution_tree: Optional[ExecutionTreeOptions] = None


def _create_configured_mixin(mixin_class: Type, options: Union[bool, Dict[str, Any]], suffix: str = "") -> Optional[Type]:
    """Create a mixin class that passes options to the underlying mixin"""
    if options is False:
        return None
    
    if options is True:
        return mixin_class
    
    # If options is a dict, create a configured mixin with unique name to avoid MRO conflicts
    class_name = f"Configured{mixin_class.__name__}{suffix}"
    
    def __init__(self, *args, **kwargs):
        final_kwargs = {**options, **kwargs} if isinstance(options, dict) else kwargs
        mixin_class.__init__(self, *args, **final_kwargs)
    
    return type(class_name, (mixin_class,), {'__init__': __init__, '__module__': mixin_class.__module__})

@overload
def enhance(
    base_class: Type[T],
    *,
    verbose: VerboseOptions = None,
    file_logging: FileLoggingOptions = None,
    performance: PerformanceOptions = None,
    single_threaded: SingleThreadedOptions = None,
    execution_tree: ExecutionTreeOptions = None,
) -> Type[T]:
    ...


@overload
def enhance(
    base_class: None = None,
    *,
    verbose: VerboseOptions = None,
    file_logging: FileLoggingOptions = None,
    performance: PerformanceOptions = None,
    single_threaded: SingleThreadedOptions = None,
    execution_tree: ExecutionTreeOptions = None,
) -> 'EnhancementBuilder':
    ...


def enhance(
    base_class: Optional[Type[T]] = None,
    *,
    verbose: VerboseOptions = None,
    file_logging: FileLoggingOptions = None,
    performance: PerformanceOptions = None,
    single_threaded: SingleThreadedOptions = None,
    execution_tree: ExecutionTreeOptions = None,
) -> Union[Type[T], 'EnhancementBuilder']:
    """
    Universal enhancement function for BrainyFlow classes.
    
    Usage Pattern 1 - Direct enhancement:
        NodeEnhanced = enhance(Node, verbose=True, file_logging={'log_folder': 'custom_logs'})
        node = NodeEnhanced()
    
    Usage Pattern 2 - Builder pattern:
        builder = enhance(verbose=True, file_logging=True)
        NodeEnhanced = builder.Node
        FlowEnhanced = builder.Flow
    
    Args:
        base_class: The base class to enhance (Node, Flow, etc.). If None, returns builder.
        verbose: Enable verbose output. True/False or dict with options.
        file_logging: Enable file file_logging. True/False or dict with options.
        performance: Enable performance monitoring. True/False or dict with options.
        single_threaded: Enable single-threaded execution. True/False or dict with options.
        execution_tree: Enable execution tree printing. True/False or dict with options.
    
    Returns:
        Enhanced class if base_class provided, otherwise EnhancementBuilder
    """
    config = EnhancementConfig(
        verbose=verbose,
        file_logging=file_logging,
        performance=performance,
        single_threaded=single_threaded,
        execution_tree=execution_tree,
    )
    
    if base_class is None:
        # Return builder for pattern 2
        return EnhancementBuilder(config)
    
    # Pattern 1 - direct enhancement
    return _create_enhanced_class(base_class, config)


def _is_memory_like(cls: Type) -> bool:
    """Check if class is Memory-like"""
    # Check for a unique attribute of Memory, like _global, and check inheritance.
    return issubclass(cls, getattr(bf, 'Memory', type(None)))


def _is_node_like(cls: Type) -> bool:
    """Check if class is Node-like"""
    return issubclass(cls, getattr(bf, 'BaseNode', type(None)))


def _is_flow_like(cls: Type) -> bool:
    """Check if class is Flow-like"""
    return issubclass(cls, getattr(bf, 'Flow', type(None)))


def _create_enhanced_class(base_class: Type[T], config: EnhancementConfig) -> Type[T]:
    """Create an enhanced class with the specified configuration"""
    
    # Special handling for Memory class to preserve generic behavior
    if _is_memory_like(base_class):
        return _create_enhanced_memory_class(base_class, config)
    
    mixins = []
    mixin_counter = 0

    if config.single_threaded:
        mixin = _create_configured_mixin(SingleThreadedMixin, config.single_threaded, f"_{mixin_counter}")
        if mixin:
            mixins.append(mixin)
            mixin_counter += 1
    
    if config.execution_tree and _is_flow_like(base_class):
        mixin = _create_configured_mixin(ExecutionTreePrinterMixin, config.execution_tree, f"_{mixin_counter}")
        if mixin:
            mixins.append(mixin)
            mixin_counter += 1
            
    # Verbose must come before performance for correct nesting display
    if config.verbose and _is_node_like(base_class):
        mixin = _create_configured_mixin(VerboseNodeMixin, config.verbose, f"_{mixin_counter}")
        if mixin:
            mixins.append(mixin)
            mixin_counter += 1

    if config.file_logging and _is_node_like(base_class):
        file_logging_mixin = FileLoggerFlowMixin if _is_flow_like(base_class) else FileLoggerNodeMixin
        mixin = _create_configured_mixin(file_logging_mixin, config.file_logging, f"_{mixin_counter}")
        if mixin:
            mixins.append(mixin)
            mixin_counter += 1
    
    if config.performance and _is_node_like(base_class):
        mixin = _create_configured_mixin(PerformanceMonitorMixin, config.performance, f"_{mixin_counter}")
        if mixin:
            mixins.append(mixin)
            mixin_counter += 1
    
    if not mixins:
        return base_class

    class_name = f"{base_class.__name__}_{str(uuid.uuid4())[:4]}"
    return types.new_class(class_name, tuple(mixins) + (base_class,))

def _create_enhanced_memory_class(base_class: Type[T], config: EnhancementConfig) -> Type[T]:
    """Create an enhanced Memory class that preserves generic behavior"""
    
    # Collect mixins for Memory
    mixins = []
    mixin_counter = 0
    
    if config.verbose:
        mixin = _create_configured_mixin(VerboseMemoryMixin, config.verbose, f"_{mixin_counter}")
        if mixin:
            mixins.append(mixin)
            mixin_counter += 1
    
    # If no mixins, return original class
    if not mixins:
        return base_class

    unique_id = str(uuid.uuid4())[:4]
    
    class EnhancedMemoryWrapper:
        """Wrapper that preserves Memory's generic behavior while adding mixins"""
        
        def __new__(cls, *args, **kwargs):
            # Create the actual enhanced class dynamically when instantiated
            class_name = f"Memory_{unique_id}"
            enhanced_class = types.new_class(class_name, tuple(mixins) + (base_class,), {})
            return enhanced_class(*args, **kwargs)
        
        @classmethod
        def __class_getitem__(cls, item):
            class TypedEnhancedMemory:
                def __new__(cls, *args, **kwargs):
                    typed_base = base_class[item]
                    class_name = f"Memory_{unique_id}_{getattr(item, '__name__', str(item))}"
                    enhanced_class = types.new_class(class_name, tuple(mixins) + (typed_base,), {})
                    return enhanced_class(*args, **kwargs)
            return TypedEnhancedMemory
    
    return EnhancedMemoryWrapper  # type: ignore

class EnhancementBuilder:
    """
    Builder class for creating multiple enhanced classes with the same configuration.
    
    Usage:
        builder = enhance(verbose=True, file_logging={'log_folder': 'my_logs'})
        MyNode = builder.Node
        MyFlow = builder.Flow
        MyMemory = builder.Memory
    """
    
    def __init__(self, config: EnhancementConfig):
        self.config = config
        self._cache = {}
    
    def __getattr__(self, name: str) -> Any:
        """Dynamically enhance any attribute from the base brainyflow module."""
        if name in self._cache:
            return self._cache[name]

        if hasattr(bf, name):
            base_class = getattr(bf, name)
            if isinstance(base_class, type):
                self._cache[name] = _create_enhanced_class(base_class, self.config)
                return self._cache[name]
        raise AttributeError(f"'{type(self).__name__}' has no attribute '{name}' and it was not found in the base brainyflow module.")

    def custom(self, base_class: Type[T]) -> Type[T]:
        """Enhance a custom base class with the builder's configuration"""
        return _create_enhanced_class(base_class, self.config)
        