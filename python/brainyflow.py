import asyncio
import copy
import warnings
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Tuple, TypeVar, Generic, Callable, Union, cast, TypedDict, Literal, overload, Awaitable, Sequence

DEFAULT_ACTION = 'default'

Action = str
SharedStore = Dict[str, Any]

G = TypeVar('G', bound=SharedStore)
L = TypeVar('L', bound=SharedStore)
T = TypeVar('T')
PrepResultT = TypeVar('PrepResultT')
ExecResultT = TypeVar('ExecResultT')
ActionT = TypeVar('ActionT', bound=str)

class Trigger(TypedDict):
    """Represents a triggered action with forking data."""
    action: Action
    forking_data: SharedStore

class Memory(Generic[G, L]):
    """
    Memory class for managing global and local state.
    Memory provides a dual-scope approach to state management:
    - Global store: Shared across the entire flow
    - Local store: Specific to a particular execution path
    """
    
    def __init__(self, _global: G, _local: Optional[L] = None):
        """Initialize a Memory instance with global and optional local stores."""
        # Directly set attributes in __dict__ to avoid __setattr__
        object.__setattr__(self, '_global', _global)
        object.__setattr__(self, '_local', _local if _local is not None else cast(L, {}))
    
    def __getattr__(self, name: str) -> Any:
        """Access properties, checking local store first, then global."""
        if name in self._local:
            return self._local[name]
        if name in self._global:
            return self._global[name]
        raise AttributeError(f"'Memory' object has no attribute {name!r}")
    
    def __setattr__(self, name: str, value: Any) -> None:
        """Write properties, handling reserved names and local/global interaction."""
        # Reserved property handling
        if name in ['global', 'local', '_global', '_local', 'clone', 'create']:
            raise ValueError(f"Reserved property '{name}' cannot be set")
        
        # Remove from local if exists, then set in global
        if name in self._local:
            del self._local[name]
        
        # Set in global store
        self._global[name] = value
    
    def __getitem__(self, key: str) -> Any:
        """Support dictionary-style access (memory['key'])."""
        if key in self._local:
            return self._local[key]
        return self._global.get(key)
    
    def __setitem__(self, key: str, value: Any) -> None:
        """Support dictionary-style assignment (memory['key'] = value)."""
        # Remove from local if exists, then set in global
        if key in self._local:
            del self._local[key]
        self._global[key] = value
    
    def __contains__(self, key: str) -> bool:
        """Support 'in' operator (key in memory)."""
        return key in self._local or key in self._global
    
    @property
    def local(self) -> L:
        """Access the local store directly."""
        return self._local
    
    def clone(self, forking_data: Optional[SharedStore] = None) -> 'Memory[G, L]':
        """Create a new Memory with shared global store but deep-copied local store."""
        forking_data = forking_data or {}
        new_local_store = copy.deepcopy(self._local)
        new_local_store.update(copy.deepcopy(forking_data))
        return Memory.create(self._global, cast(L, new_local_store))
    
    @staticmethod
    def create(global_store: G, local_store: Optional[L] = None) -> 'Memory[G, L]':
        """Factory method to create a Memory instance."""
        return Memory(global_store, local_store if local_store is not None else cast(L, {}))

class NodeError(Exception):
    """Error raised during node execution with retry count information."""
    retry_count: int = 0

class BaseNode(Generic[G, L, ActionT, PrepResultT, ExecResultT], ABC):
    """
    Base class for all computational nodes in a flow.
    Implements the core lifecycle (prep, exec, post) and graph connection logic.
    
    Type Parameters:
    - G: Global memory store type
    - L: Local memory store type
    - ActionT: Type of actions this node can trigger
    - PrepResultT: Return type of prep method
    - ExecResultT: Return type of exec method
    """
    
    _next_id = 0
    
    def __init__(self) -> None:
        """Initialize a BaseNode instance."""
        self.successors: Dict[Action, List['BaseNode']] = {}  # dict of action -> list of nodes
        self._triggers: List[Trigger] = []  # list of dicts with action and forking_data
        self._locked: bool = True  # Prevent trigger calls outside post()
        self._node_order: int = BaseNode._next_id
        BaseNode._next_id += 1
    
    def clone(self, seen: Optional[Dict['BaseNode', 'BaseNode']] = None) -> 'BaseNode[G, L, ActionT, PrepResultT, ExecResultT]':
        """Create a deep copy of the node including its successors."""
        # Create a deep copy with cycle detection
        seen = seen or {}
        if self in seen:
            return seen[self]
        
        # Create new instance maintaining class hierarchy
        cloned = type(self).__new__(type(self))
        seen[self] = cloned
        
        # Copy attributes except successors
        for key, value in self.__dict__.items():
            if key != 'successors':
                setattr(cloned, key, value)
        
        # Clone successors with cycle detection
        cloned.successors = {}
        for action, nodes in self.successors.items():
            cloned.successors[action] = [
                node.clone(seen) if node else node for node in nodes
            ]
        
        return cloned
    
    def on(self, action: Action, node: 'BaseNode') -> 'BaseNode':
        """Add a successor node for a specific action."""
        if action not in self.successors:
            self.successors[action] = []
        self.successors[action].append(node)
        return node
    
    def next(self, node: 'BaseNode', action: Action = DEFAULT_ACTION) -> 'BaseNode':
        """Convenience method equivalent to on()."""
        return self.on(action, node)
    
    # Python-specific syntax sugar
    def __rshift__(self, other: 'BaseNode') -> 'BaseNode':
        """Implement node_a >> node_b syntax for default action"""
        return self.next(other)
    
    def __sub__(self, action: Action) -> 'ActionLinker':
        """Implement node_a - "action" syntax for action selection"""
        return self.ActionLinker(self, action)
    
    class ActionLinker:
        """Helper class for action-specific transitions"""
        def __init__(self, node: 'BaseNode', action: Action):
            self.node = node
            self.action = action
        
        def __rshift__(self, other: 'BaseNode') -> 'BaseNode':
            """Implement - "action" >> node_b syntax"""
            return self.node.on(self.action, other)
    
    def get_next_nodes(self, action: Action = DEFAULT_ACTION) -> List['BaseNode']:
        """Get successor nodes for a specific action."""
        next_nodes = self.successors.get(action, [])
        if not next_nodes and action != DEFAULT_ACTION and self.successors:
            warnings.warn(f"Flow ends: '{action}' not found in {list(self.successors.keys())}", stacklevel=2)
        return next_nodes
    
    async def prep(self, memory: Memory[G, L]) -> PrepResultT:
        """Prepare phase - override in subclasses."""
        return cast(PrepResultT, None)
    
    async def exec(self, prep_res: PrepResultT) -> ExecResultT:
        """Execute phase - override in subclasses."""
        return cast(ExecResultT, None)
    
    async def post(self, memory: Memory[G, L], prep_res: PrepResultT, exec_res: ExecResultT) -> None:
        """Post-processing phase - override in subclasses."""
        pass
    
    def trigger(self, action: ActionT, forking_data: Optional[SharedStore] = None) -> None:
        """Trigger a successor action with optional forking data."""
        if self._locked:
            raise RuntimeError("An action can only be triggered inside post()")
        
        self._triggers.append({
            "action": action,
            "forking_data": forking_data or {}
        })
    
    def list_triggers(self, memory: Memory[G, L]) -> List[Tuple[Action, Memory[G, L]]]:
        """Process triggers or return default."""
        if not self._triggers:
            return [(DEFAULT_ACTION, memory.clone())]
        
        return [(t["action"], memory.clone(t["forking_data"])) for t in self._triggers]
    
    @abstractmethod
    async def exec_runner(self, memory: Memory[G, L], prep_res: PrepResultT) -> ExecResultT:
        """Core execution logic - must be implemented by subclasses."""
        pass
    
    @overload
    async def run(self, memory: Union[Memory[G, L], G], propagate: Literal[True]) -> List[Tuple[Action, Memory[G, L]]]: ...
    
    @overload
    async def run(self, memory: Union[Memory[G, L], G], propagate: Literal[False] = False) -> ExecResultT: ...
    
    async def run(self, memory: Union[Memory[G, L], G], propagate: bool = False) -> Union[List[Tuple[Action, Memory[G, L]]], ExecResultT]:
        """Run the node's full lifecycle."""
        if self.successors:
            warnings.warn("Node won't run successors. Use Flow!", stacklevel=2)
        
        if not isinstance(memory, Memory):
            memory = Memory.create(memory)
        
        self._triggers = []
        prep_res = await self.prep(memory)
        exec_res = await self.exec_runner(memory, prep_res)
        
        self._locked = False
        await self.post(memory, prep_res, exec_res)
        self._locked = True
        
        if propagate:
            return self.list_triggers(memory)
        return exec_res

class Node(BaseNode[G, L, ActionT, PrepResultT, ExecResultT]):
    """
    Standard node implementation with retry capabilities.
    
    Attributes:
        max_retries: Maximum number of execution attempts
        wait: Seconds to wait between retry attempts
        cur_retry: Current retry attempt (0-indexed)
    """
    
    def __init__(self, max_retries: int = 1, wait: float = 0) -> None:
        """Initialize a Node with retry configuration."""
        super().__init__()
        self.max_retries = max_retries
        self.wait = wait
        self.cur_retry = 0
    
    async def exec_fallback(self, prep_res: PrepResultT, error: NodeError) -> ExecResultT:
        """Called when all retry attempts fail."""
        raise error
    
    async def exec_runner(self, memory: Memory[G, L], prep_res: PrepResultT) -> ExecResultT:
        """Run exec with retry logic."""
        for attempt in range(self.max_retries):
            self.cur_retry = attempt
            try:
                return await self.exec(prep_res)
            except Exception as error:
                if attempt < self.max_retries - 1:
                    if self.wait > 0:
                        await asyncio.sleep(self.wait)
                    continue
                
                # Last attempt failed, add retry info and use fallback
                wrapped = NodeError(str(error))
                wrapped.retry_count = attempt + 1
                return await self.exec_fallback(prep_res, wrapped)
        raise RuntimeError("Unreachable: exec_runner should have returned or raised in the loop")

class Flow(BaseNode[G, L, ActionT, PrepResultT, Dict[str, Any]]):
    """
    Orchestrates the execution of a graph of nodes sequentially.
    
    Attributes:
        start: The entry point node of the flow
        options: Configuration options like max_visits
        visit_counts: Tracks node visits for cycle detection
    """
    
    def __init__(self, start: BaseNode, options: Optional[Dict[str, Any]] = None) -> None:
        """Initialize a Flow with a start node and options."""
        super().__init__()
        self.start = start
        self.options = options or {"max_visits": 5}
        self.visit_counts: Dict[str, int] = {}
    
    async def exec(self, prep_res: PrepResultT) -> Dict[str, Any]:
        raise RuntimeError("This method should never be called in a Flow")
    
    async def exec_runner(self, memory: Memory[G, L], prep_res: PrepResultT) -> Dict[str, Any]:
        """Run the flow starting from the start node."""
        self.visit_counts = {}  # Reset visit counts
        return await self.run_node(self.start, memory)
    
    async def run_tasks(self, tasks: Sequence[Callable[[], Awaitable[T]]]) -> List[T]:
        """Run tasks sequentially."""
        results: List[T] = []
        for task in tasks:
            results.append(await task())
        return results
    
    async def run_nodes(self, nodes: List[BaseNode], memory: Memory[G, L]) -> List[Any]:
        """Run a list of nodes with the given memory."""
        tasks: List[Callable[[], Awaitable[Any]]] = [
            lambda n=node, m=memory: self.run_node(n, m) for node in nodes
        ]
        return await self.run_tasks(tasks)
    
    async def run_node(self, node: BaseNode, memory: Memory[G, L]) -> Dict[str, Any]:
        """Run a node with cycle detection."""
        node_id = str(node._node_order)
        
        # Check for cycles
        current_visit_count = self.visit_counts.get(node_id, 0) + 1
        if current_visit_count > self.options["max_visits"]:
            raise RuntimeError(
                f"Maximum cycle count reached ({self.options['max_visits']}) for "
                f"{node_id}.{node.__class__.__name__}"
            )
        
        self.visit_counts[node_id] = current_visit_count
        
        # Clone node and run with propagate=True
        cloned_node = node.clone()
        triggers = await cloned_node.run(memory.clone(), True)
        
        # Process each trigger and collect results
        tasks: List[Callable[[], Awaitable[Tuple[Action, List[Any]]]]] = []
        for action, node_memory in triggers:
            next_nodes = cloned_node.get_next_nodes(action)
            tasks.append(
                lambda a=action, nn=next_nodes, nm=node_memory: self._process_trigger(a, nn, nm)
            )
        
        # Run all trigger tasks and build result tree
        tree = await self.run_tasks(tasks)
        return {action: results for action, results in tree}
    
    async def _process_trigger(self, action: Action, next_nodes: List[BaseNode], node_memory: Memory[G, L]) -> Tuple[Action, List[Any]]:
        """Process a single trigger."""
        if not next_nodes:
            return (action, [])
        
        results = await self.run_nodes(next_nodes, node_memory)
        return (action, results)

class ParallelFlow(Flow[G, L, ActionT, PrepResultT]):
    """
    Orchestrates execution of a graph of nodes with parallel branching.
    Overrides run_tasks to execute tasks concurrently using asyncio.gather.
    """
    
    async def run_tasks(self, tasks: Sequence[Callable[[], Awaitable[T]]]) -> List[T]:
        """Run tasks concurrently using asyncio.gather."""
        if not tasks:
            return []
        return await asyncio.gather(*(task() for task in tasks))
