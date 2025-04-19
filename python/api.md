# BrainyFlow Python API Reference

This document lists the classes and methods available in the `brainyflow.py` module.

## Classes

### `Memory`

Manages global and local state for flow execution.

- `__init__(self, _global, _local=None)`: Initializes memory with global and optional local stores.
- `__getattr__(self, name)`: Accesses properties, checking local then global store.
- `__setattr__(self, name, value)`: Sets properties, writing to the global store.
- `__getitem__(self, key)`: Dictionary-style access (read).
- `__setitem__(self, key, value)`: Dictionary-style assignment (write to global).
- `__contains__(self, key)`: Checks if a key exists in local or global store.
- `local` (property): Provides direct access to the local store.
- `clone(self, forking_data=None)`: Creates a new Memory instance with a shared global store and a deep-copied local store, optionally updated with `forking_data`.
- `create(global_store, local_store=None)` (staticmethod): Factory method to create a Memory instance.

### `NodeError(Exception)`

Custom exception raised during node execution, potentially carrying retry information.

### `BaseNode(ABC)`

Abstract base class for all computational nodes.

- `__init__(self)`: Initializes the node, setting up successors and a unique ID.
- `clone(self, seen=None)`: Creates a deep copy of the node and its successors, handling cycles.
- `on(self, action, node)`: Adds a successor node for a specific action. Returns the added node.
- `next(self, node, action=DEFAULT_ACTION)`: Convenience method for `on` with the default action. Returns the added node.
- `__rshift__(self, other)`: Syntax sugar (`>>`) for `next(other)`.
- `__sub__(self, action)`: Syntax sugar (`-`) to initiate action-specific linking. Returns an `ActionLinker`.
- `ActionLinker` (inner class): Helper for action-specific linking.
  - `__init__(self, node, action)`
  - `__rshift__(self, other)`: Syntax sugar (`- "action" >> other`) for `node.on(action, other)`.
- `get_next_nodes(self, action=DEFAULT_ACTION)`: Retrieves the list of successor nodes for a given action.
- `async prep(self, memory)`: Asynchronous preparation phase. Override in subclasses.
- `async exec(self, prep_res)`: Asynchronous execution phase (core logic). Override in subclasses.
- `async post(self, memory, prep_res, exec_res)`: Asynchronous post-processing phase. Override in subclasses.
- `trigger(self, action, forking_data=None)`: Triggers a subsequent action during the `post` phase, optionally passing data to the local scope of the next branch.
- `list_triggers(self, memory)`: Returns a list of `(action, memory_clone)` tuples based on `trigger` calls.
- `async exec_runner(self, memory, prep_res)` (abstract): Core execution logic runner (implemented by subclasses like `Node`).
- `async run(self, memory, propagate=False)`: Runs the node's full lifecycle (`prep` -> `exec_runner` -> `post`). Returns `exec_runner` result or triggers if `propagate=True`.

### `Node(BaseNode)`

Standard node implementation with retry capabilities.

- `__init__(self, max_retries=1, wait=0)`: Initializes the node with retry configuration.
- `async exec_fallback(self, prep_res, error)`: Called if all retry attempts in `exec` fail. Default raises the error.
- `async exec_runner(self, memory, prep_res)`: Runs the `exec` method with retry logic based on `max_retries` and `wait`.

### `Flow(BaseNode)`

Orchestrates sequential execution of a node graph.

- `__init__(self, start, options=None)`: Initializes the flow with a starting node and options (e.g., `max_visits`).
- `async exec(self, prep_res)`: Raises `RuntimeError` (Flows orchestrate, not execute directly).
- `async exec_runner(self, memory, prep_res)`: Starts the flow execution from the `start` node.
- `async run_tasks(self, tasks)`: Executes a list of async task functions sequentially.
- `async run_nodes(self, nodes, memory)`: Runs a list of nodes sequentially using `run_tasks`.
- `async run_node(self, node, memory)`: Runs a single node within the flow, handling cloning, execution, triggers, recursion, and cycle detection.
- `async _process_trigger(self, action, next_nodes, node_memory)`: Processes a single trigger, running subsequent nodes.

### `ParallelFlow(Flow)`

Orchestrates parallel execution of node graph branches.

- `async run_tasks(self, tasks)`: Overrides `Flow.run_tasks` to execute tasks concurrently using `asyncio.gather`.
