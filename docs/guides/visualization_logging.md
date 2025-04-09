---
machine-display: false
---

# Visualization and Logging

{% hint style="warning" %}

**BrainyFlow does NOT provide built-in utilities**

Instead, we offer examples that you can implement yourself. This approach gives you [more flexibility and control](./index#why-not-built-in) over your project's dependencies and functionality.

{% endhint %}

Similar to LLM wrappers, we **don't** provide built-in visualization and debugging. Here, we recommend some _minimal_ (and incomplete) implementations. These examples can serve as a starting point for your own tooling.

## 1. Visualization with Mermaid

This code recursively traverses the nested graph, assigns unique IDs to each node, and treats Flow nodes as subgraphs to generate Mermaid syntax for a hierarchical visualization.

{% tabs %}
{% tab title="Python" %}

```python
def build_mermaid(start):
    ids, visited, lines = {}, set(), ["graph LR"]
    ctr = 1
    def get_id(n):
        nonlocal ctr
        return ids[n] if n in ids else (ids.setdefault(n, f"N{ctr}"), (ctr := ctr + 1))[0]
    def link(a, b):
        lines.append(f"    {a} --> {b}")
    def walk(node, parent=None):
        if node in visited:
            return parent and link(parent, get_id(node))
        visited.add(node)
        if isinstance(node, Flow):
            node.start and parent and link(parent, get_id(node.start))
            lines.append(f"\n    subgraph sub_flow_{get_id(node)}[{type(node).__name__}]")
            node.start and walk(node.start)
            for nxt in node.successors.values():
                node.start and walk(nxt, get_id(node.start)) or (parent and link(parent, get_id(nxt))) or walk(nxt)
            lines.append("    end\n")
        else:
            lines.append(f"    {(nid := get_id(node))}['{type(node).__name__}']")
            parent and link(parent, nid)
            [walk(nxt, nid) for nxt in node.successors.values()]
    walk(start)
    return "\n".join(lines)
```

{% endtab %}

{% tab title="TypeScript" %}

```typescript
function buildMermaid(start: any): string {
  const ids: Record = {}
  const visited = new Set()
  const lines: string[] = ['graph LR']
  let ctr = 1

  function getId(n: any): string {
    const key = n.toString()
    if (key in ids) return ids[key]
    ids[key] = `N${ctr++}`
    return ids[key]
  }

  function link(a: string, b: string): void {
    lines.push(`    ${a} --> ${b}`)
  }

  function walk(node: any, parent: string | null = null): void {
    const nodeKey = node.toString()
    if (visited.has(nodeKey)) {
      if (parent) link(parent, getId(node))
      return
    }

    visited.add(nodeKey)

    if (node instanceof Flow) {
      if (node.start && parent) {
        link(parent, getId(node.start))
      }

      lines.push(`\n    subgraph sub_flow_${getId(node)}[${node.constructor.name}]`)

      if (node.start) {
        walk(node.start)
      }

      for (const nxt of Object.values(node.successors)) {
        if (node.start) {
          walk(nxt, getId(node.start))
        } else if (parent) {
          link(parent, getId(nxt))
        } else {
          walk(nxt)
        }
      }

      lines.push('    end\n')
    } else {
      const nid = getId(node)
      lines.push(`    ${nid}['${node.constructor.name}']`)

      if (parent) {
        link(parent, nid)
      }

      for (const nxt of Object.values(node.successors)) {
        walk(nxt, nid)
      }
    }
  }

  walk(start)
  return lines.join('\n')
}
```

{% endtab %}
{% endtabs %}

For example, suppose we have a complex Flow for data science:

{% tabs %}
{% tab title="Python" %}

```python
class DataPrepBatchNode(BatchNode):
    def prep(self,shared): return []
class ValidateDataNode(Node): pass
class FeatureExtractionNode(Node): pass
class TrainModelNode(Node): pass
class EvaluateModelNode(Node): pass
class ModelFlow(Flow): pass
class DataScienceFlow(Flow):pass

feature_node = FeatureExtractionNode()
train_node = TrainModelNode()
evaluate_node = EvaluateModelNode()
feature_node >> train_node >> evaluate_node
model_flow = ModelFlow(start=feature_node)
data_prep_node = DataPrepBatchNode()
validate_node = ValidateDataNode()
data_prep_node >> validate_node >> model_flow
data_science_flow = DataScienceFlow(start=data_prep_node)
result = build_mermaid(start=data_science_flow)
```

{% endtab %}

{% tab title="TypeScript" %}

```typescript
class DataPrepBatchNode extends BatchNode {
  prep(shared: any): any[] {
    return []
  }
}
class ValidateDataNode extends Node {}
class FeatureExtractionNode extends Node {}
class TrainModelNode extends Node {}
class EvaluateModelNode extends Node {}
class ModelFlow extends Flow {}
class DataScienceFlow extends Flow {}

const featureNode = new FeatureExtractionNode()
const trainNode = new TrainModelNode()
const evaluateNode = new EvaluateModelNode()
featureNode.next(trainNode).next(evaluateNode)
const modelFlow = new ModelFlow(featureNode)
const dataPrepNode = new DataPrepBatchNode()
const validateNode = new ValidateDataNode()
dataPrepNode.next(validateNode).next(modelFlow)
const dataScienceFlow = new DataScienceFlow(dataPrepNode)
const result = buildMermaid(dataScienceFlow)
```

{% endtab %}
{% endtabs %}

The code generates a Mermaid diagram:

```mermaid
graph LR
    subgraph sub_flow_N1[DataScienceFlow]
    N2['DataPrepBatchNode']
    N3['ValidateDataNode']
    N2 --> N3
    N3 --> N4

    subgraph sub_flow_N5[ModelFlow]
    N4['FeatureExtractionNode']
    N6['TrainModelNode']
    N4 --> N6
    N7['EvaluateModelNode']
    N6 --> N7
    end

    end
```

## 2. Call Stack Debugging

For debugging purposes, it's useful to inspect the runtime call stack to understand the execution path through your nodes. This implementation extracts the Node call stack by examining the current execution frames:

{% tabs %}
{% tab title="Python" %}

```python
import inspect

def get_node_call_stack():
    stack = inspect.stack()
    node_names = []
    seen_ids = set()
    for frame_info in stack[1:]:
        local_vars = frame_info.frame.f_locals
        if 'self' in local_vars:
            caller_self = local_vars['self']
            if isinstance(caller_self, BaseNode) and id(caller_self) not in seen_ids:
                seen_ids.add(id(caller_self))
                node_names.append(type(caller_self).__name__)
    return node_names
```

{% endtab %}

{% tab title="TypeScript" %}

```typescript
function getNodeCallStack(): string[] {
  // Create a new Error to capture the stack trace
  const stackTrace = new Error().stack || ''
  const nodeNames: string[] = []
  const seenIds = new Set()

  // Parse the stack trace to extract node information
  // This is a simplified implementation - in practice you would need
  // a more robust approach to track Node instances

  const stackFrames = stackTrace.split('\n').slice(1) // Skip Error constructor

  for (const frame of stackFrames) {
    // Look for Node class method calls in the stack trace
    // Format typically: "at NodeClassName.methodName"
    const match = frame.match(/at\s+(\w+)\.(prep|exec|post)/)

    if (match) {
      const className = match[1]
      // Check if this is likely a Node class (ends with "Node" or is a Flow)
      if ((className.endsWith('Node') || className.endsWith('Flow')) && !seenIds.has(className)) {
        seenIds.add(className)
        nodeNames.push(className)
      }
    }
  }

  return nodeNames
}
```

{% endtab %}
{% endtabs %}

For example, suppose we have a complex Flow for data science:

{% tabs %}
{% tab title="Python" %}

```python
class DataPrepBatchNode(BatchNode):
    def prep(self, shared): return []
class ValidateDataNode(Node): pass
class FeatureExtractionNode(Node): pass
class TrainModelNode(Node): pass
class EvaluateModelNode(Node):
    def prep(self, shared):
        stack = get_node_call_stack()
        print("Call stack:", stack)
class ModelFlow(Flow): pass
class DataScienceFlow(Flow):pass

feature_node = FeatureExtractionNode()
train_node = TrainModelNode()
evaluate_node = EvaluateModelNode()
feature_node >> train_node >> evaluate_node
model_flow = ModelFlow(start=feature_node)
data_prep_node = DataPrepBatchNode()
validate_node = ValidateDataNode()
data_prep_node >> validate_node >> model_flow
data_science_flow = DataScienceFlow(start=data_prep_node)
data_science_flow.run({})
```

{% endtab %}

{% tab title="TypeScript" %}

```typescript
class DataPrepBatchNode extends BatchNode {
  prep(shared: any): any[] {
    return []
  }
}
class ValidateDataNode extends Node {}
class FeatureExtractionNode extends Node {}
class TrainModelNode extends Node {}
class EvaluateModelNode extends Node {
  prep(shared: any): void {
    const stack = getNodeCallStack()
    console.log('Call stack:', stack)
  }
}
class ModelFlow extends Flow {}
class DataScienceFlow extends Flow {}

const featureNode = new FeatureExtractionNode()
const trainNode = new TrainModelNode()
const evaluateNode = new EvaluateModelNode()
featureNode.next(trainNode).next(evaluateNode)
const modelFlow = new ModelFlow(featureNode)
const dataPrepNode = new DataPrepBatchNode()
const validateNode = new ValidateDataNode()
dataPrepNode.next(validateNode).next(modelFlow)
const dataScienceFlow = new DataScienceFlow(dataPrepNode)
dataScienceFlow.run({})
```

{% endtab %}
{% endtabs %}

The output would be: `Call stack: ['EvaluateModelNode', 'ModelFlow', 'DataScienceFlow']`

This shows the nested execution path, with the current node (`EvaluateModelNode`) at the top, followed by its parent flows.

## 3. Logging and Tracing

A simple logging utility can help track the flow of execution through your nodes:

{% tabs %}
{% tab title="Python" %}

```python
import logging
import time
from functools import wraps

# Configure logging
logging.basicConfig(level=logging.INFO,
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('brainyflow')

def trace_node(cls):
    """Class decorator to trace node execution"""
    original_prep = cls.prep
    original_exec = cls.exec
    original_post = cls.post

    @wraps(original_prep)
    async def traced_prep(self, shared):
        logger.info(f"ENTER prep: {type(self).__name__}")
        start_time = time.time()
        result = await original_prep(self, shared)
        elapsed = time.time() - start_time
        logger.info(f"EXIT prep: {type(self).__name__} ({elapsed:.3f}s)")
        return result

    @wraps(original_exec)
    async def traced_exec(self, prep_res):
        logger.info(f"ENTER exec: {type(self).__name__}")
        start_time = time.time()
        result = await original_exec(self, prep_res)
        elapsed = time.time() - start_time
        logger.info(f"EXIT exec: {type(self).__name__} ({elapsed:.3f}s)")
        return result

    @wraps(original_post)
    async def traced_post(self, shared, prep_res, exec_res):
        logger.info(f"ENTER post: {type(self).__name__}")
        start_time = time.time()
        result = await original_post(self, shared, prep_res, exec_res)
        elapsed = time.time() - start_time
        logger.info(f"EXIT post: {type(self).__name__} ({elapsed:.3f}s) -> {result}")
        return result

    cls.prep = traced_prep
    cls.exec = traced_exec
    cls.post = traced_post
    return cls

# Usage:
@trace_node
class MyNode(Node):
    async def prep(self, shared):
        return "data"

    async def exec(self, prep_res):
        return prep_res.upper()

    async def post(self, shared, prep_res, exec_res):
        shared["result"] = exec_res
        return "default"
```

{% endtab %}

{% tab title="TypeScript" %}

```typescript
import { createLogger, format, transports } from 'winston'

// Configure logging
const logger = createLogger({
  level: 'info',
  format: format.combine(
    format.timestamp(),
    format.printf(({ timestamp, level, message }) => {
      return `${timestamp} - ${level}: ${message}`
    }),
  ),
  transports: [new transports.Console()],
})

// Node tracing decorator function
function traceNode(BaseClass: T): T {
  return class extends BaseClass {
    async prep(shared: any): Promise {
      logger.info(`ENTER prep: ${this.constructor.name}`)
      const startTime = Date.now()
      const result = await super.prep(shared)
      const elapsed = (Date.now() - startTime) / 1000
      logger.info(`EXIT prep: ${this.constructor.name} (${elapsed.toFixed(3)}s)`)
      return result
    }

    async exec(prepRes: any): Promise {
      logger.info(`ENTER exec: ${this.constructor.name}`)
      const startTime = Date.now()
      const result = await super.exec(prepRes)
      const elapsed = (Date.now() - startTime) / 1000
      logger.info(`EXIT exec: ${this.constructor.name} (${elapsed.toFixed(3)}s)`)
      return result
    }

    async post(shared: any, prepRes: any, execRes: any): Promise {
      logger.info(`ENTER post: ${this.constructor.name}`)
      const startTime = Date.now()
      const result = await super.post(shared, prepRes, execRes)
      const elapsed = (Date.now() - startTime) / 1000
      logger.info(`EXIT post: ${this.constructor.name} (${elapsed.toFixed(3)}s) -> ${result}`)
      return result
    }
  } as T
}

// Usage:
class MyNode extends traceNode(Node) {
  async prep(shared: any): Promise {
    return 'data'
  }

  async exec(prepRes: string): Promise {
    return prepRes.toUpperCase()
  }

  async post(shared: any, prepRes: string, execRes: string): Promise {
    shared.result = execRes
    return 'default'
  }
}
```

{% endtab %}
{% endtabs %}

This tracing utility provides detailed logs of node execution, including timing information, which can be invaluable for debugging and performance optimization.
