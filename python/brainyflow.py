# python/brainyflow.py

import asyncio
import copy
import warnings
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Tuple, TypeVar, Generic, Callable, Union, Type, cast

DEFAULT_ACTION = 'default'

class Memory:
    """
    Memory class for managing global and local state.
    
    Memory provides a dual-scope approach to state management:
    - Global store: Shared across the entire flow
    - Local store: Specific to a particular execution path
    """
    
    def __init__(self, _global, _local=None):
        """Initialize a Memory instance with global and optional local stores."""
        # Directly set attributes in __dict__ to avoid __setattr__
        object.__setattr__(self, '_global', _global)
        object.__setattr__(self, '_local', _local or {})
    
    def __getattr__(self, name):
        """Access properties, checking local store first, then global."""
        if name in self._local:
            return self._local[name]
        return self._global.get(name)
    
    def __setattr__(self, name, value):
        """Write properties, handling reserved names and local/global interaction."""
        # Reserved property handling
        if name in ['global', 'local', '_global', '_local']:
            raise ValueError(f"Reserved property '{name}' cannot be set")
            
        # Remove from local if exists, then set in global
        if hasattr(self, '_local') and name in self._local:
            del self._local[name]
            
        # Set in global store
        self._global[name] = value
    
    def __getitem__(self, key):
        """Support dictionary-style access (memory['key'])."""
        if key in self._local:
            return self._local[key]
        return self._global.get(key)
    
    def __setitem__(self, key, value):
        """Support dictionary-style assignment (memory['key'] = value)."""
        # Remove from local if exists, then set in global
        if key in self._local:
            del self._local[key]
        
        # Set in global store
        self._global[key] = value
    
    def __contains__(self, key):
        """Support 'in' operator (key in memory)."""
        return key in self._local or key in self._global
    
    @property
    def local(self):
        """Access the local store directly."""
        return self._local
    
    def clone(self, forking_data=None):
        """Create a new Memory with shared global store but deep-copied local store."""
        forking_data = forking_data or {}
        new_local = copy.deepcopy(self._local)
        new_local.update(copy.deepcopy(forking_data))
        return Memory.create(self._global, new_local)
    
    @staticmethod
    def create(global_store, local_store=None):
        """Factory method to create a Memory instance."""
        return Memory(global_store, local_store)


class NodeError(Exception):
    """Error raised during node execution with retry count information."""
    pass


class BaseNode(ABC):
    """
    Base class for all computational nodes in a flow.
    
    Implements the core lifecycle (prep, exec, post) and graph connection logic.
    """
    
    _next_id = 0
    
    def __init__(self):
        """Initialize a BaseNode instance."""
        self.successors = {}  # dict of action -> list of nodes
        self._triggers = []   # list of dicts with action and forking_data
        self._locked = True   # Prevent trigger calls outside post()
        self._node_order = BaseNode._next_id  # Changed from __node_order to _node_order
        BaseNode._next_id += 1
    
    def clone(self, seen=None):
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
    
    def on(self, action, node):
        """Add a successor node for a specific action."""
        if action not in self.successors:
            self.successors[action] = []
        self.successors[action].append(node)
        return node
    
    def next(self, node, action=DEFAULT_ACTION):
        """Convenience method equivalent to on()."""
        return self.on(action, node)
    
    def get_next_nodes(self, action=DEFAULT_ACTION):
        """Get successor nodes for a specific action."""
        next_nodes = self.successors.get(action, [])
        if not next_nodes and action != DEFAULT_ACTION and self.successors:
            warnings.warn(f"Flow ends: '{action}' not found in {list(self.successors.keys())}")
        return next_nodes
    
    async def prep(self, memory):
        """Prepare phase - override in subclasses."""
        pass
    
    async def exec(self, prep_res):
        """Execute phase - override in subclasses."""
        pass
    
    async def post(self, memory, prep_res, exec_res):
        """Post-processing phase - override in subclasses."""
        pass
    
    def trigger(self, action, forking_data=None):
        """Trigger a successor action with optional forking data."""
        if self._locked:
            raise RuntimeError("An action can only be triggered inside post()")
            
        self._triggers.append({
            "action": action,
            "forking_data": forking_data or {}
        })
    
    def list_triggers(self, memory):
        """Process triggers or return default."""
        if not self._triggers:
            return [(DEFAULT_ACTION, memory.clone())]
            
        return [(t["action"], memory.clone(t["forking_data"])) for t in self._triggers]
    
    @abstractmethod
    async def exec_runner(self, memory, prep_res):
        """Core execution logic - must be implemented by subclasses."""
        pass
    
    async def run(self, memory, propagate=False):
        """Run the node's full lifecycle."""
        if self.successors:
            warnings.warn("Node won't run successors. Use Flow!")
            
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


class Node(BaseNode):
    """
    Standard node implementation with retry capabilities.
    
    Attributes:
        max_retries: Maximum number of execution attempts
        wait: Seconds to wait between retry attempts
        cur_retry: Current retry attempt (0-indexed)
    """
    
    def __init__(self, max_retries=1, wait=0):
        """Initialize a Node with retry configuration."""
        super().__init__()
        self.max_retries = max_retries
        self.wait = wait
        self.cur_retry = 0
    
    async def exec_fallback(self, prep_res, error):
        """Called when all retry attempts fail."""
        raise error
    
    async def exec_runner(self, memory, prep_res):
        """Run exec with retry logic."""
        for self.cur_retry in range(self.max_retries):
            try:
                return await self.exec(prep_res)
            except Exception as error:
                if self.cur_retry < self.max_retries - 1:
                    if self.wait > 0:
                        await asyncio.sleep(self.wait)
                    continue
                    
                # Last attempt failed, add retry info and use fallback
                error.retry_count = self.cur_retry
                return await self.exec_fallback(prep_res, error)


class Flow(BaseNode):
    """
    Orchestrates the execution of a graph of nodes sequentially.
    
    Attributes:
        start: The entry point node of the flow
        options: Configuration options like max_visits
        visit_counts: Tracks node visits for cycle detection
    """
    
    def __init__(self, start, options=None):
        """Initialize a Flow with a start node and options."""
        super().__init__()
        self.start = start
        self.options = options or {"max_visits": 5}
        self.visit_counts = {}
    
    async def exec(self, prep_res):
        """This method should never be called in a Flow."""
        raise RuntimeError("This method should never be called in a Flow")
    
    async def exec_runner(self, memory, prep_res):
        """Run the flow starting from the start node."""
        self.visit_counts = {}  # Reset visit counts
        return await self.run_node(self.start, memory)
    
    async def run_tasks(self, tasks):
        """Run tasks sequentially."""
        results = []
        for task in tasks:
            results.append(await task())
        return results
    
    async def run_nodes(self, nodes, memory):
        """Run a list of nodes with the given memory."""
        tasks = [lambda n=node, m=memory: self.run_node(n, m) for node in nodes]
        return await self.run_tasks(tasks)
    
    async def run_node(self, node, memory):
        """Run a node with cycle detection."""
        # Changed from __node_order to _node_order
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
        tasks = []
        for action, node_memory in triggers:
            next_nodes = cloned_node.get_next_nodes(action)
            tasks.append(
                lambda a=action, nn=next_nodes, nm=node_memory: 
                self._process_trigger(a, nn, nm)
            )
            
        # Run all trigger tasks and build result tree
        tree = await self.run_tasks(tasks)
        return {action: results for action, results in tree}
    
    async def _process_trigger(self, action, next_nodes, node_memory):
        """Process a single trigger."""
        if not next_nodes:
            return [action, []]
            
        results = await self.run_nodes(next_nodes, node_memory)
        return [action, results]


class ParallelFlow(Flow):
    """
    Orchestrates execution of a graph of nodes with parallel branching.
    
    Overrides run_tasks to execute tasks concurrently using asyncio.gather.
    """
    
    async def run_tasks(self, tasks):
        """Run tasks concurrently using asyncio.gather."""
        if not tasks:
            return []
        return await asyncio.gather(*(task() for task in tasks))
