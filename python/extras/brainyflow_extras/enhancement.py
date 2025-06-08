"""
Universal enhancement system for BrainyFlow classes.
Provides intuitive, discoverable API for applying mixins without knowing their names.
"""
from __future__ import annotations
from typing import TYPE_CHECKING, Union, Dict, Any, Type, Optional, overload, TypeVar
from dataclasses import dataclass

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
LoggingOptions = Union[bool, Dict[str, Any]]
PerformanceOptions = Union[bool, Dict[str, Any]]
SingleThreadedOptions = Union[bool, Dict[str, Any]]
ExecutionTreeOptions = Union[bool, Dict[str, Any]]


@dataclass
class EnhancementConfig:
    """Configuration for enhancements"""
    verbose: Optional[VerboseOptions] = None
    logging: Optional[LoggingOptions] = None
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
        # Merge provided options with kwargs
        if isinstance(options, dict):
            kwargs.update(options)
        mixin_class.__init__(self, *args, **kwargs)
    
    # Create a new class that inherits from the mixin
    configured_mixin = type(class_name, (mixin_class,), {
        '__init__': __init__,
        '__module__': mixin_class.__module__,
    })
    
    return configured_mixin


# Overloads for proper typing
@overload
def enhance(
    base_class: Type[T],
    *,
    verbose: VerboseOptions = None,
    logging: LoggingOptions = None,
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
    logging: LoggingOptions = None,
    performance: PerformanceOptions = None,
    single_threaded: SingleThreadedOptions = None,
    execution_tree: ExecutionTreeOptions = None,
) -> 'EnhancementBuilder':
    ...


def enhance(
    base_class: Optional[Type[T]] = None,
    *,
    verbose: VerboseOptions = None,
    logging: LoggingOptions = None,
    performance: PerformanceOptions = None,
    single_threaded: SingleThreadedOptions = None,
    execution_tree: ExecutionTreeOptions = None,
) -> Union[Type[T], 'EnhancementBuilder']:
    """
    Universal enhancement function for BrainyFlow classes.
    
    Usage Pattern 1 - Direct enhancement:
        NodeEnhanced = enhance(Node, verbose=True, logging={'log_folder': 'custom_logs'})
        node = NodeEnhanced()
    
    Usage Pattern 2 - Builder pattern:
        builder = enhance(verbose=True, logging=True)
        NodeEnhanced = builder.Node
        FlowEnhanced = builder.Flow
    
    Args:
        base_class: The base class to enhance (Node, Flow, etc.). If None, returns builder.
        verbose: Enable verbose output. True/False or dict with options.
        logging: Enable file logging. True/False or dict with options.
        performance: Enable performance monitoring. True/False or dict with options.
        single_threaded: Enable single-threaded execution. True/False or dict with options.
        execution_tree: Enable execution tree printing. True/False or dict with options.
    
    Returns:
        Enhanced class if base_class provided, otherwise EnhancementBuilder
    """
    config = EnhancementConfig(
        verbose=verbose,
        logging=logging,
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
    return hasattr(cls, '_set_value') or 'Memory' in getattr(cls, '__name__', '')


def _is_node_like(cls: Type) -> bool:
    """Check if class is Node-like"""
    return hasattr(cls, 'prep') and hasattr(cls, 'exec') and hasattr(cls, 'post')


def _is_flow_like(cls: Type) -> bool:
    """Check if class is Flow-like"""
    return hasattr(cls, 'start') or 'Flow' in getattr(cls, '__name__', '')


def _create_enhanced_class(base_class: Type[T], config: EnhancementConfig) -> Type[T]:
    """Create an enhanced class with the specified configuration"""
    
    # Special handling for Memory class to preserve generic behavior
    if _is_memory_like(base_class):
        return _create_enhanced_memory_class(base_class, config)
    
    mixins = []
    mixin_counter = 0
    
    # Determine which mixins to apply based on base class and config
    if config.verbose and _is_node_like(base_class):
        mixin = _create_configured_mixin(VerboseNodeMixin, config.verbose, f"_{mixin_counter}")
        if mixin:
            mixins.append(mixin)
            mixin_counter += 1
    
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
    
    if config.logging:
        # Choose appropriate logging mixin based on class type
        if _is_flow_like(base_class):
            logging_mixin = FileLoggerFlowMixin
        else:
            logging_mixin = FileLoggerNodeMixin
            
        mixin = _create_configured_mixin(logging_mixin, config.logging, f"_{mixin_counter}")
        if mixin:
            mixins.append(mixin)
            mixin_counter += 1
    
    if config.performance:
        mixin = _create_configured_mixin(PerformanceMonitorMixin, config.performance, f"_{mixin_counter}")
        if mixin:
            mixins.append(mixin)
            mixin_counter += 1
    
    # Create the enhanced class
    if not mixins:
        return base_class
    
    # Create unique class name to avoid conflicts
    import uuid
    unique_id = str(uuid.uuid4())[:8]
    class_name = f"Enhanced{base_class.__name__}_{unique_id}"
    
    try:
        enhanced_class = type(class_name, tuple(mixins) + (base_class,), {
            '__doc__': f"{base_class.__name__} enhanced with: {', '.join(type(m).__name__ for m in mixins)}",
            '__module__': base_class.__module__,
        })
        
        return enhanced_class  # type: ignore
        
    except TypeError as e:
        if "consistent method resolution order" in str(e):
            # Fallback: create a simpler enhanced class by combining mixins differently
            return _create_enhanced_class_fallback(base_class, config, mixins)
        else:
            raise


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
    
    # Create a wrapper class that preserves the original Memory's generic behavior
    import uuid
    unique_id = str(uuid.uuid4())[:8]
    
    class EnhancedMemoryWrapper:
        """Wrapper that preserves Memory's generic behavior while adding mixins"""
        
        def __new__(cls, *args, **kwargs):
            # Create the actual enhanced class dynamically when instantiated
            class_name = f"EnhancedMemory_{unique_id}"
            
            try:
                enhanced_class = type(class_name, tuple(mixins) + (base_class,), {
                    '__module__': base_class.__module__,
                })
                return enhanced_class(*args, **kwargs)
            except TypeError:
                # Fallback to just the base class if mixins cause issues
                return base_class(*args, **kwargs)
        
        @classmethod
        def __class_getitem__(cls, item):
            # Preserve generic subscripting behavior
            # When someone does EnhancedMemory[SomeType], we want to return
            # a class that can be instantiated with that type
            
            class TypedEnhancedMemory:
                def __new__(cls, *args, **kwargs):
                    # Get the typed base class
                    typed_base = base_class[item]
                    
                    # Create enhanced version of the typed class
                    class_name = f"EnhancedMemory_{unique_id}_{getattr(item, '__name__', str(item))}"
                    
                    try:
                        enhanced_class = type(class_name, tuple(mixins) + (typed_base,), {
                            '__module__': base_class.__module__,
                        })
                        return enhanced_class(*args, **kwargs)
                    except TypeError:
                        # Fallback to just the typed base class
                        return typed_base(*args, **kwargs)
            
            return TypedEnhancedMemory
    
    return EnhancedMemoryWrapper  # type: ignore


def _create_enhanced_class_fallback(base_class: Type[T], config: EnhancementConfig, failed_mixins: list) -> Type[T]:
    """
    Fallback method to create enhanced class when MRO conflicts occur.
    Creates a single combined mixin to avoid conflicts.
    """
    import uuid
    unique_id = str(uuid.uuid4())[:8]
    
    # Create a single combined mixin class
    class CombinedMixin:
        """Combined mixin to avoid MRO conflicts"""
        
        def __init__(self, *args, **kwargs):
            # Initialize all mixin functionality
            for mixin_class in failed_mixins:
                if hasattr(mixin_class, '__init__'):
                    try:
                        mixin_class.__init__(self, *args, **kwargs)
                    except TypeError:
                        # Skip if mixin doesn't accept the arguments
                        pass
            super().__init__(*args, **kwargs)
    
    # Add methods from all mixins to the combined mixin
    for mixin_class in failed_mixins:
        for attr_name in dir(mixin_class):
            if not attr_name.startswith('_') or attr_name in ['__init__']:
                attr = getattr(mixin_class, attr_name)
                if callable(attr) and not hasattr(CombinedMixin, attr_name):
                    setattr(CombinedMixin, attr_name, attr)
    
    class_name = f"Enhanced{base_class.__name__}_Fallback_{unique_id}"
    enhanced_class = type(class_name, (CombinedMixin, base_class), {
        '__doc__': f"{base_class.__name__} enhanced (fallback mode)",
        '__module__': base_class.__module__,
    })
    
    return enhanced_class  # type: ignore


class EnhancementBuilder:
    """
    Builder class for creating multiple enhanced classes with the same configuration.
    
    Usage:
        builder = enhance(verbose=True, logging={'log_folder': 'my_logs'})
        MyNode = builder.Node
        MyFlow = builder.Flow
        MyMemory = builder.Memory
    """
    
    def __init__(self, config: EnhancementConfig):
        self.config = config
        # Cache enhanced classes to avoid recreating them
        self._cache = {}
    
    @property
    def Node(self) -> Type['bf.Node']:
        """Get enhanced Node class"""
        if 'Node' not in self._cache:
            self._cache['Node'] = _create_enhanced_class(bf.Node, self.config)
        return self._cache['Node']
    
    @property
    def Flow(self) -> Type['bf.Flow']:
        """Get enhanced Flow class"""
        if 'Flow' not in self._cache:
            self._cache['Flow'] = _create_enhanced_class(bf.Flow, self.config)
        return self._cache['Flow']
    
    @property
    def ParallelFlow(self) -> Type['bf.ParallelFlow']:
        """Get enhanced ParallelFlow class"""
        return _create_enhanced_class(bf.ParallelFlow, self.config)
    
    @property
    def Memory(self) -> Type['bf.Memory']:
        """Get enhanced Memory class"""
        return _create_enhanced_class(bf.Memory, self.config)
    
    def custom(self, base_class: Type[T]) -> Type[T]:
        """Enhance a custom base class with the builder's configuration"""
        return _create_enhanced_class(base_class, self.config)
