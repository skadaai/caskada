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
    ParallelContextMixin,
    VerboseMemoryMixin,
    VerboseNodeMixin,
    VerboseParallelFlowMixin,
    ExecutionTreePrinterMixin,
    FileLoggerNodeMixin,
    FileLoggerFlowMixin,
    SingleThreadedMixin,
    PerformanceMonitorMixin,
)

T = TypeVar('T')
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
        NodeEnhanced = enhance(Node, verbose=True, file_logging={'log_folder': 'custom_logs', 'clear_logs': True})
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
    return issubclass(cls, getattr(bf, 'Memory', type(None)))
    
def _is_node_like(cls: Type) -> bool:
    return issubclass(cls, getattr(bf, 'BaseNode', type(None)))
    
def _is_flow_like(cls: Type) -> bool:
    return hasattr(cls, 'run_node')
    
def _is_parallel_flow_like(cls: Type) -> bool:
    return issubclass(cls, getattr(bf, 'ParallelFlow', type(None)))
    

def _create_enhanced_class(base_class: Type[T], config: EnhancementConfig) -> Type[T]:
    """Create an enhanced class with the specified configuration"""
    
    # Special handling for Memory class to preserve generic behavior
    if _is_memory_like(base_class):
        return _create_enhanced_memory_class(base_class, config)
    
    mixins = []

    if _is_parallel_flow_like(base_class) and (config.file_logging or config.verbose):
        mixins.append(ParallelContextMixin)
        
    if config.file_logging and _is_node_like(base_class):
        file_logging_mixin = FileLoggerFlowMixin if _is_flow_like(base_class) else FileLoggerNodeMixin
        mixin = _create_configured_mixin(file_logging_mixin, config.file_logging, f"_{len(mixins)}")
        if mixin:
            mixins.append(mixin)

    if config.single_threaded:
        mixin = _create_configured_mixin(SingleThreadedMixin, config.single_threaded, f"_{len(mixins)}")
        if mixin:
            mixins.append(mixin)
            
    if config.execution_tree and _is_flow_like(base_class):
        mixin = _create_configured_mixin(ExecutionTreePrinterMixin, config.execution_tree, f"_{len(mixins)}")
        if mixin:
            mixins.append(mixin)

    if config.verbose:
        if _is_parallel_flow_like(base_class):
            # Apply the specialized mixin for ParallelFlow. It includes VerboseNodeMixin behavior.
            mixin = _create_configured_mixin(VerboseParallelFlowMixin, config.verbose, f"_{len(mixins)}")
            if mixin:
                mixins.append(mixin)
        elif _is_node_like(base_class):
            # Apply the standard mixin for all other nodes and flows.
            mixin = _create_configured_mixin(VerboseNodeMixin, config.verbose, f"_{len(mixins)}")
            if mixin:
                mixins.append(mixin)

    if config.performance and _is_node_like(base_class):
        mixin = _create_configured_mixin(PerformanceMonitorMixin, config.performance, f"_{len(mixins)}")
        if mixin:
            mixins.append(mixin)
    
    if not mixins:
        return base_class

    class_name = f"{base_class.__name__}_{str(uuid.uuid4())[:4]}"
    enhanced_class = types.new_class(class_name, tuple(mixins) + (base_class,), {})
    setattr(enhanced_class, '__module__', base_class.__module__)
    return enhanced_class

def _create_enhanced_memory_class(base_class: Type[T], config: EnhancementConfig) -> Type[T]:
    """Create an enhanced Memory class that preserves generic behavior."""
    
    mixins = []
    
    if config.verbose:
        mixin = _create_configured_mixin(VerboseMemoryMixin, config.verbose, f"_{len(mixins)}")
        if mixin:
            mixins.append(mixin)
    
    if not mixins:
        return base_class

    unique_id = str(uuid.uuid4())[:4]
    class_name = f"Memory_{unique_id}"
    enhanced_class = types.new_class(class_name, tuple(mixins) + (base_class,))

    # To make the enhanced class generic (support `EnhancedMemory[T]`), we must
    # provide a `__class_getitem__` method.
    _mixins = tuple(mixins)

    @classmethod
    def __class_getitem__(cls, item):
        # When EnhancedMemory[T] is called, this creates a new, specialized class.
        specialized_base = base_class[item]
        specialized_name = f"{cls.__name__}[{getattr(item, '__name__', str(item))}]"
        specialized_bases = _mixins + (specialized_base,)
        return types.new_class(specialized_name, specialized_bases)

    enhanced_class.__class_getitem__ = __class_getitem__
    setattr(enhanced_class, '__module__', base_class.__module__)

    return enhanced_class

class EnhancementBuilder:
    """
    Builder class for creating multiple enhanced classes with the same configuration.
    
    Usage:
        builder = enhance(verbose=True, file_logging={'log_folder': 'my_logs', 'clear_logs': True})
        MyNode = builder.Node
        MyFlow = builder.Flow
        MyMemory = builder.Memory
    """
    
    def __init__(self, config: EnhancementConfig):
        self.config = config
        self._cache = {}
    
    def __dir__(self):
        return dir(bf) + list(self._cache.keys())

    def __getattr__(self, name: str) -> Any:
        """Dynamically enhance any attribute from the base brainyflow module."""
        if name in self._cache:
            return self._cache[name]

        if hasattr(bf, name):
            base_class = getattr(bf, name)
            if isinstance(base_class, type):
                self._cache[name] = _create_enhanced_class(base_class, self.config)
                return self._cache[name]
            return base_class
        
        raise AttributeError(f"'{type(self).__name__}' has no attribute '{name}' and it was not found in the base brainyflow module.")

    def custom(self, base_class: Type[T]) -> Type[T]:
        """Enhance a custom base class with the builder's configuration"""
        return _create_enhanced_class(base_class, self.config)
        