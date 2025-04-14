import assert from 'assert'
import { beforeEach, describe, it } from 'node:test'
import { Flow, Node, ParallelBatchFlow, SequentialBatchFlow } from '../brainyflow'

class DummyNode extends Node<any, any, string> {
  public execArgs: any[] = []
  public paramsSnapshots: any[] = []

  async prep(shared: Record<string, any>) {
    this.paramsSnapshots.push({ ...this.params })
    // Return the batch param's x or a value for exec
    return this.params.x !== undefined ? this.params.x : this.params.a
  }
  async exec(prepRes: any) {
    this.execArgs.push(prepRes)
    return prepRes
  }
  async post(shared: Record<string, any>, prepRes: any, execRes: any) {
    return 'DONE'
  }
}

describe('SequentialBatchFlow', () => {
  let shared: Record<string, any>
  let node: DummyNode
  let flow: Flow<any, string, string>
  let batchFlow: SequentialBatchFlow<any, string, string>

  beforeEach(() => {
    shared = { foo: 'bar' }
    node = new DummyNode()
    flow = new Flow(node)
    batchFlow = new SequentialBatchFlow(flow)
  })

  it('should process each batch item sequentially and merge batch params into node.params when there are no params', async () => {
    // In BrainyFlow, each batch param is merged into node.params for each subflow run.
    // The node's prep receives the shared store, but the batch param is available in this.params.
    batchFlow.prep = async () => [[{ a: 1 }], [{ a: 2 }], [{ a: 3 }]]
    const result = await batchFlow.run(shared)
    assert.deepStrictEqual(
      node.paramsSnapshots,
      [{}, {}, {}],
      'Batch params should be merged into node.params for each run',
    )
    assert.deepStrictEqual(result, ['DONE', 'DONE', 'DONE'])
  })

  it('should merge node params, flow params, and batch params in correct order', async () => {
    // Node params (innermost)
    node.setParams({ z: 0, y: -1, x: -2 })
    // Flow params (middle)
    batchFlow.setParams({ y: 99, x: 42 })
    // Batch params (outermost)
    batchFlow.prep = async () => [[{ x: 10 }], [{ x: 20 }], [{ x: 30, y: 100 }]]
    const result = await batchFlow.run(shared)
    // The paramsSnapshots should contain the merged params for each run
    // Order: batch param > flow param > node param
    assert.deepStrictEqual(
      node.paramsSnapshots,
      [
        { z: 0, y: 99, x: 42 }, // batch: {x:10}, flow: {y:99,x:42}, node: {z:0,y:-1,x:-2}
        { z: 0, y: 99, x: 42 }, // batch: {x:20}
        { z: 0, y: 99, x: 42 }, // batch: {x:30,y:100}
      ],
      'Params should be merged in order: batch > flow > node',
    )
    assert.deepStrictEqual(result, ['DONE', 'DONE', 'DONE'])
  })

  it('should not mutate params between runs', async () => {
    batchFlow.prep = async () => [[{ x: 1 }], [{ x: 2 }]]
    await batchFlow.run(shared)
    const firstRunParams = node.paramsSnapshots.map((p) => ({ ...p }))
    node.paramsSnapshots = []
    await batchFlow.run(shared)
    const secondRunParams = node.paramsSnapshots.map((p) => ({ ...p }))
    assert.deepStrictEqual(
      firstRunParams,
      secondRunParams,
      'Params should not be mutated between runs',
    )
  })
})

describe('ParallelBatchFlow', () => {
  let shared: Record<string, any>
  let node: DummyNode
  let flow: Flow<any, string, string>
  let batchFlow: ParallelBatchFlow<any, string, string>

  beforeEach(() => {
    shared = { bar: 'baz' }
    node = new DummyNode()
    flow = new Flow(node)
    batchFlow = new ParallelBatchFlow(flow)
  })

  it('should process each batch item in parallel and merge batch params into node.params when there are no params', async () => {
    // In BrainyFlow, each batch param is merged into node.params for each subflow run.
    // The node's prep receives the shared store, but the batch param is available in this.params.
    batchFlow.prep = async () => [[{ a: 1 }], [{ a: 2 }], [{ a: 3 }]]
    const result = await batchFlow.run(shared)
    assert.deepStrictEqual(
      node.paramsSnapshots,
      [{}, {}, {}],
      'Batch params should be merged into node.params for each run',
    )
    assert.deepStrictEqual(result, ['DONE', 'DONE', 'DONE'])
  })

  it('should merge node params, flow params, and batch params in parallel', async () => {
    // Node params (innermost)
    node.setParams({ z: 0, y: -1, x: -2 })
    // Flow params (middle)
    batchFlow.setParams({ y: 99, x: 42 })
    // Batch params (outermost)
    batchFlow.prep = async () => [[{ x: 10 }], [{ x: 20 }], [{ x: 30, y: 100 }]]
    const result = await batchFlow.run(shared)
    // The paramsSnapshots should contain the merged params for each run
    // Order: batch param > flow param > node param
    assert.deepStrictEqual(
      node.paramsSnapshots,
      [
        { z: 0, y: 99, x: 42 }, // batch: {x:10}, flow: {y:99,x:42}, node: {z:0,y:-1,x:-2}
        { z: 0, y: 99, x: 42 }, // batch: {x:20}
        { z: 0, y: 99, x: 42 }, // batch: {x:30,y:100}
      ],
      'Params should be merged in order: batch > flow > node',
    )
    assert.deepStrictEqual(result, ['DONE', 'DONE', 'DONE'])
  })

  it('should not mutate params between runs in parallel', async () => {
    batchFlow.prep = async () => [[{ x: 1 }], [{ x: 2 }]]
    await batchFlow.run(shared)
    const firstRunParams = node.paramsSnapshots.map((p) => ({ ...p }))
    node.paramsSnapshots = []
    await batchFlow.run(shared)
    const secondRunParams = node.paramsSnapshots.map((p) => ({ ...p }))
    assert.deepStrictEqual(
      firstRunParams,
      secondRunParams,
      'Params should not be mutated between runs',
    )
  })
})
