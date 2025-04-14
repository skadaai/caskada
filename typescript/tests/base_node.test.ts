import assert from 'assert'
import { beforeEach, describe, it } from 'node:test'
import { BaseNode } from '../brainyflow'

// DummyNode for testing BaseNode (implements abstract execRunner)
class DummyNode extends BaseNode<any, any, string> {
  public prepCalled = false
  public execRunnerCalled = false
  public postCalled = false
  public execRunnerResult: any = 'execResult'
  public postResult: any = undefined

  async prep(shared: Record<string, any>) {
    this.prepCalled = true
    return shared.input || 'prepResult'
  }
  protected async execRunner(shared: Record<string, any>, prepRes: any) {
    this.execRunnerCalled = true
    return this.execRunnerResult
  }
  async post(shared: Record<string, any>, prepRes: any, execRes: any) {
    this.postCalled = true
    return this.postResult
  }
}

describe('BaseNode', () => {
  let node: DummyNode
  let shared: Record<string, any>

  beforeEach(() => {
    node = new DummyNode()
    shared = { input: 'testInput' }
  })

  it('should set params and return itself', () => {
    const result = node.setParams({ foo: 1, bar: 2 })
    assert.strictEqual(result, node)
    assert.deepStrictEqual((node as any).params, { foo: 1, bar: 2 })
  })

  it('should support on() and next() for transitions', () => {
    const nextNode = new DummyNode()
    node.on('custom', nextNode)
    assert.strictEqual((node as any).successors.get('custom'), nextNode)

    const nextNode2 = new DummyNode()
    node.next(nextNode2)
    assert.strictEqual((node as any).successors.get('default'), nextNode2)
  })

  it('should getNextNode for defined and undefined actions', () => {
    const n1 = new DummyNode()
    const n2 = new DummyNode()
    node.on('foo', n1)
    node.on('bar', n2)
    assert.strictEqual(node.getNextNode('foo'), n1)
    assert.strictEqual(node.getNextNode('bar'), n2)
    assert.strictEqual(node.getNextNode('baz'), null)
  })

  it('should clone itself and its successors', () => {
    const n1 = new DummyNode()
    const n2 = new DummyNode()
    node.on('a', n1)
    node.on('b', n2)
    const clone = node.clone()
    assert.notStrictEqual(clone, node)
    assert(clone instanceof DummyNode)
    assert.strictEqual(clone.getNextNode('a')?.constructor, DummyNode)
    assert.strictEqual(clone.getNextNode('b')?.constructor, DummyNode)
    // Changing clone's successors does not affect original
    const n3 = new DummyNode()
    clone.on('c', n3)
    assert.strictEqual(node.getNextNode('c'), null)
  })

  it('should run the full lifecycle: prep → execRunner → post', async () => {
    node.execRunnerResult = 'execResult'
    node.postResult = 'customAction'
    const action = await node.run(shared)
    assert(node.prepCalled)
    assert(node.execRunnerCalled)
    assert(node.postCalled)
    assert.strictEqual(action, 'customAction')
  })

  it('should default to "default" action if post returns undefined', async () => {
    node.postResult = undefined
    const action = await node.run(shared)
    assert.strictEqual(action, 'default')
  })

  it('should warn if successors exist when run() is called', async () => {
    // Patch console.warn to capture output
    let warned = false
    const origWarn = console.warn
    console.warn = () => {
      warned = true
    }
    node.on('foo', new DummyNode())
    await node.run(shared)
    console.warn = origWarn
    assert(warned)
  })

  it('should handle cloning cycles', () => {
    // Create a cycle: node1 -> node2 -> node1
    const node1 = new DummyNode()
    const node2 = new DummyNode()
    node1.on('loop', node2)
    node2.on('back', node1)
    const clone = node1.clone()
    // The clone's successors should also form a cycle
    const clone2 = clone.getNextNode('loop')
    assert(clone2)
    assert.strictEqual(clone2?.getNextNode('back'), clone)
  })
})
