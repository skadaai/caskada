# BrainyFlow Python Implementation Design

This document outlines the design for the Python port of the BrainyFlow library, ensuring functional parity with the TypeScript version while embracing Pythonic idioms.

## 1. Overview

The BrainyFlow Python library implements the same core abstractions as the TypeScript version:

- **Memory:** State management with global and local stores
- **BaseNode:** Abstract foundation with lifecycle methods and graph connections
- **Node:** Concrete implementation with retry capabilities
- **Flow:** Sequential orchestration of nodes
- **ParallelFlow:** Parallel execution of branches

While maintaining functional parity, the implementation adapts to Python's language features and conventions.

## 2. Core Components

### 2.1. Memory Class

The `Memory` class manages state with global and local stores, providing a dual-scope system:

```python
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
        return self._local

    def clone(self, forking_data=None):
        # Create new Memory with same global reference but deep-copied local
        forking_data = forking_data or {}
        new_local = copy.deepcopy(self._local)
        new_local.update(copy.deepcopy(forking_data))
        return Memory.create(self._global, new_local)

    @staticmethod
    def create(global_store, local_store=None):
        return Memory(global_store, local_store)
```

### 2.2. BaseNode Abstract Class

The `BaseNode` class provides the foundation for all nodes with lifecycle methods and connections:

```python
class BaseNode:
    _next_id = 0

    def __init__(self):
        self.successors = {}  # dict of action -> list of nodes
        self._triggers = []   # list of dicts with action and forking_data
        self._locked = True   # Prevent trigger calls outside post()
        self._node_order = BaseNode._next_id  # Changed from __node_order to _node_order
        BaseNode._next_id += 1

    def clone(self, seen=None):
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
        # Add node as successor for the given action
        if action not in self.successors:
            self.successors[action] = []
        self.successors[action].append(node)
        return node

    def next(self, node, action=DEFAULT_ACTION):
        # Convenience method equivalent to on()
        return self.on(action, node)

    # Python-specific syntax sugar
    def __rshift__(self, other):
        """Implement node_a >> node_b syntax for default action"""
        return self.next(other)

    def __sub__(self, action):
        """Implement node_a - "action" syntax for action selection"""
        return self.ActionLinker(self, action)

    class ActionLinker:
        """Helper class for action-specific transitions"""
        def __init__(self, node, action):
            self.node = node
            self.action = action

        def __rshift__(self, other):
            """Implement - "action" >> node_b syntax"""
            return self.node.on(self.action, other)

    def get_next_nodes(self, action=DEFAULT_ACTION):
        # Get nodes for the given action or empty list
        next_nodes = self.successors.get(action, [])
        if not next_nodes and action != DEFAULT_ACTION and self.successors:
            warnings.warn(f"Flow ends: '{action}' not found in {list(self.successors.keys())}")
        return next_nodes

    async def prep(self, memory):
        # Prepare phase - override in subclasses
        pass

    async def exec(self, prep_res):
        # Execute phase - override in subclasses
        pass

    async def post(self, memory, prep_res, exec_res):
        # Post-processing phase - override in subclasses
        pass

    def trigger(self, action, forking_data=None):
        # Trigger a successor action
        if self._locked:
            raise RuntimeError("An action can only be triggered inside post()")

        self._triggers.append({
            "action": action,
            "forking_data": forking_data or {}
        })

    def list_triggers(self, memory):
        # Process triggers or return default
        if not self._triggers:
            return [(DEFAULT_ACTION, memory.clone())]

        return [(t["action"], memory.clone(t["forking_data"])) for t in self._triggers]

    async def exec_runner(self, memory, prep_res):
        # Abstract method to be implemented by subclasses
        raise NotImplementedError("exec_runner must be implemented by subclasses")

    async def run(self, memory, propagate=False):
        # Run the node lifecycle
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
```

### 2.3. Node Class (with Retry Logic)

The `Node` class extends `BaseNode` with retry capabilities:

```python
class Node(BaseNode):
    def __init__(self, max_retries=1, wait=0):
        super().__init__()
        self.max_retries = max_retries
        self.wait = wait
        self.cur_retry = 0

    async def exec_fallback(self, prep_res, error):
        # Default implementation raises the error
        raise error

    async def exec_runner(self, memory, prep_res):
        # Run exec with retry logic
        for self.cur_retry in range(self.max_retries):
            try:
                return await self.exec(prep_res)
            except Exception as error:
                if self.cur_retry  0:
                        await asyncio.sleep(self.wait)
                    continue

                # Last attempt failed, add retry info and use fallback
                error.retry_count = self.cur_retry
                return await self.exec_fallback(prep_res, error)
```

### 2.4. Flow Class

The `Flow` class orchestrates node execution:

```python
class Flow(BaseNode):
    def __init__(self, start, options=None):
        super().__init__()
        self.start = start
        self.options = options or {"max_visits": 5}
        self.visit_counts = {}

    async def exec(self, prep_res):
        # This method should never be called in a Flow
        raise RuntimeError("This method should never be called in a Flow")

    async def exec_runner(self, memory, prep_res):
        # Run the flow starting from the start node
        self.visit_counts = {}  # Reset visit counts
        return await self.run_node(self.start, memory)

    async def run_tasks(self, tasks):
        # Run tasks sequentially
        results = []
        for task in tasks:
            results.append(await task())
        return results

    async def run_nodes(self, nodes, memory):
        # Run a list of nodes with the given memory
        tasks = [lambda n=node, m=memory: self.run_node(n, m) for node in nodes]
        return await self.run_tasks(tasks)

    async def run_node(self, node, memory):
        # Run a node with cycle detection
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
        # Process a single trigger
        if not next_nodes:
            return [action, []]

        results = await self.run_nodes(next_nodes, node_memory)
        return [action, results]
```

### 2.5. ParallelFlow Class

The `ParallelFlow` class extends `Flow` to run tasks concurrently:

```python
class ParallelFlow(Flow):
    async def run_tasks(self, tasks):
        # Run tasks concurrently using asyncio.gather
        if not tasks:
            return []
        return await asyncio.gather(*(task() for task in tasks))
```

## 3. Language-Specific Adaptations

### 3.1. Key Differences

| TypeScript Feature         | Python Equivalent                                        |
| -------------------------- | -------------------------------------------------------- |
| JavaScript Proxy           | `__getattr__`, `__setattr__`, `__getattribute__`         |
| structuredClone            | copy.deepcopy                                            |
| Promise.all                | asyncio.gather                                           |
| camelCase methods          | snake_case methods (e.g., getNextNodes → get_next_nodes) |
| undefined                  | None                                                     |
| class field initialization | Initialize in `__init__`                                 |
| Error.retryCount           | Add retry_count attribute to Exception object            |
|                            | Pythonic syntax sugar (`>>`, `- "action" >>`)            |
|                            | Type Hinting (`typing` module)                           |

### 3.2. Memory Access

- TypeScript uses JavaScript's Proxy API
- Python uses dunder methods (`__getattr__`, `__setattr__`, `__getitem__`, `__setitem__`, `__contains__`)
- Both implementations check local store first, then global

### 3.3. Asynchronous Execution

- TypeScript uses Promise-based asynchrony
- Python uses asyncio with async/await syntax
- Both models support sequential and parallel execution patterns

### 3.4. Error Handling

- Both implementations support the retry pattern
- Python adds attributes to Exception objects for retry tracking and defines a `NodeError` class (though not currently used in the core logic).
- Both provide fallback mechanisms for failed operations

## 4. Implementation Plan

1. Implement `Memory` class first as foundation for state management
2. Implement `BaseNode` abstract class with core lifecycle methods
3. Add `Node` implementation with retry logic
4. Implement `Flow` with sequential execution capabilities
5. Implement `ParallelFlow` for concurrent execution
6. Run test suite to verify parity with TypeScript

## 5. Success Criteria

The Python implementation will be considered successful when:

1. All tests pass with the same behavior as the TypeScript version
2. The API is consistent with the TypeScript version but follows Python conventions
3. The implementation maintains the same performance characteristics
4. All edge cases and error handling match the TypeScript implementation

This design provides a solid foundation for implementing BrainyFlow in Python while ensuring compatibility with the TypeScript version.
