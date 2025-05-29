---
'brainyflow': minor
---

## Automatic Triggers Propagation

Since v2.0, Brainyflow propagates triggers from **terminal nodes** (i.e. _nodes missing successors_) to subsequent flows. This let you permeate an action from a node directly to outside of the parent flow, skipping the need to explicitly re-trigger the actions at the end of every flow execution.

This allows for more fluid and permeable flows, and effectively stops the parent flow from being a rigid barrier in the graph execution.
Think about it as "_handing over unfinished tasks in a flow to the first node in the next flow_".

It also means that you can **preserve the concurrency of that execution path as you navigate into the next flow**: the execution doesn’t end at the leaf node, it continues into the next flow.

### Ignoring Implicit Triggers Propagation

In v2.1 we are stopping the propagation of **Implicit Triggers** - _the default action that is automatically triggered when no `.trigger()` was explicitly called_ - to give users more control over trigger's propagation and avoid unexpected behavior.

Thus, this is the behaviour you can expect:

1. If a terminal node **does NOT** explicitly call `.trigger()`, **no action is propagated** from that terminal node.
2. If a terminal node **calls** `.trigger()`, then the parent flow **propagates** that action to its own sucessors - and any forking data passed is preserved.
