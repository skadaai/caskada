import assert from 'assert'
import { beforeEach, describe, it } from 'node:test'
import { ParallelBatchNode, SequentialBatchNode } from '../brainyflow'

class SeqBatchTestNode extends SequentialBatchNode<number, string, string> {
  public prepItems: number[][] = [[1], [2], [3]]
  public postResult: string | undefined = undefined
  public postShared: any = null
  public processedItems: number[][] = []

  async prep(shared: Record<string, any>) {
    return this.prepItems
  }
  protected async processBatch(items: (() => Promise<string>)[]): Promise<string[]> {
    const results: string[] = []
    for (let i = 0; i < items.length; i++) {
      this.processedItems.push(this.prepItems[i])
      results.push(`item${this.prepItems[i][0]}`)
    }
    return results
  }
  async post(shared: Record<string, any>, prepRes: number[][], execRes: string[]) {
    this.postShared = { ...shared }
    return this.postResult
  }
}

class ParBatchTestNode extends ParallelBatchNode<number, string, string> {
  public prepItems: number[][] = [[4], [5], [6]]
  public postResult: string | undefined = undefined
  public postShared: any = null
  public processedItems: number[][] = []

  async prep(shared: Record<string, any>) {
    return this.prepItems
  }
  protected async processBatch(items: (() => Promise<string>)[]): Promise<string[]> {
    // Simulate parallel processing, but just record all items
    for (let i = 0; i < items.length; i++) {
      this.processedItems.push(this.prepItems[i])
    }
    return this.prepItems.map((item) => `item${item[0]}`)
  }
  async post(shared: Record<string, any>, prepRes: number[][], execRes: string[]) {
    this.postShared = { ...shared }
    return this.postResult
  }
}

describe('SequentialBatchNode', () => {
  let node: SeqBatchTestNode
  let shared: Record<string, any>

  beforeEach(() => {
    node = new SeqBatchTestNode()
    shared = { foo: 'bar' }
  })

  it('should process items sequentially and call exec for each', async () => {
    await node.run(shared)
    assert.deepStrictEqual(node.processedItems, [[1], [2], [3]])
  })

  it('should call post with correct shared, prepRes, execRes', async () => {
    await node.run(shared)
    assert.deepStrictEqual(node.postShared, shared)
  })

  it('should return custom action from post', async () => {
    node.postResult = 'done'
    const action = await node.run(shared)
    assert.strictEqual(action, 'done')
  })
})

describe('ParallelBatchNode', () => {
  let node: ParBatchTestNode
  let shared: Record<string, any>

  beforeEach(() => {
    node = new ParBatchTestNode()
    shared = { bar: 'baz' }
  })

  it('should process items in parallel and call exec for each', async () => {
    await node.run(shared)
    const sorted = (arr: number[][]) => arr.map((x) => x[0]).sort()
    assert.deepStrictEqual(sorted(node.processedItems), [4, 5, 6])
  })

  it('should call post with correct shared, prepRes, execRes', async () => {
    await node.run(shared)
    assert.deepStrictEqual(node.postShared, shared)
  })

  it('should return custom action from post', async () => {
    node.postResult = 'done'
    const action = await node.run(shared)
    assert.strictEqual(action, 'done')
  })
})
