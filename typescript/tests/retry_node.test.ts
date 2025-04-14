import assert from 'assert'
import { beforeEach, describe, it } from 'node:test'
import { Node } from '../brainyflow'

class FailingNode extends Node<any, any, string> {
  public execCalls: number[] = []
  public fallbackCalled = false
  public fallbackError: any = null
  public fallbackRetryCount: number | null = null
  public failTimes = 1
  public succeedResult: any = 'success'
  public fallbackResult: any = 'fallback'
  public waitSeconds = 0

  constructor(options: { maxRetries?: number; wait?: number } = {}) {
    super(options)
    if (options.wait !== undefined) this.waitSeconds = options.wait
  }

  async prep(shared: Record<string, any>) {
    return shared.input || 'prep'
  }

  async exec(prepRes: any) {
    this.execCalls.push(Date.now())
    if (this.execCalls.length <= this.failTimes) {
      throw new Error('fail')
    }
    return this.succeedResult
  }

  async execFallback(prepRes: any, error: any) {
    this.fallbackCalled = true
    this.fallbackError = error
    this.fallbackRetryCount = error.retryCount
    return this.fallbackResult
  }

  async post(shared: Record<string, any>, prepRes: any, execRes: any) {
    shared.result = execRes
    return 'done'
  }
}

describe('RetryNode', () => {
  let node: FailingNode
  let shared: Record<string, any>

  beforeEach(() => {
    node = new FailingNode({ maxRetries: 3 })
    shared = { input: 'test' }
  })

  it('should retry exec up to maxRetries and then call fallback', async () => {
    node.failTimes = 3 // fail all attempts
    const action = await node.run(shared)
    assert.strictEqual(node.execCalls.length, 3)
    assert(node.fallbackCalled)
    assert.strictEqual(node.fallbackRetryCount, 2)
    assert.strictEqual(shared.result, 'fallback')
    assert.strictEqual(action, 'done')
  })

  it('should succeed if exec eventually succeeds before maxRetries', async () => {
    node.failTimes = 2 // fail twice, succeed on third
    node.succeedResult = 'ok'
    const action = await node.run(shared)
    assert.strictEqual(node.execCalls.length, 3)
    assert(!node.fallbackCalled)
    assert.strictEqual(shared.result, 'ok')
    assert.strictEqual(action, 'done')
  })

  it('should not retry if maxRetries is 1', async () => {
    node = new FailingNode({ maxRetries: 1 })
    node.failTimes = 1
    const action = await node.run(shared)
    assert.strictEqual(node.execCalls.length, 1)
    assert(node.fallbackCalled)
    assert.strictEqual(node.fallbackRetryCount, 0)
    assert.strictEqual(shared.result, 'fallback')
    assert.strictEqual(action, 'done')
  })

  it('should wait between retries if wait is set', async () => {
    // Patch setTimeout to count calls and simulate delay
    let waits = 0
    const origSetTimeout = global.setTimeout
    global.setTimeout = (fn: (...args: any[]) => void, ms?: number) => {
      waits++
      fn()
      return {} as any
    }
    node = new FailingNode({ maxRetries: 3, wait: 1 })
    node.failTimes = 3
    await node.run(shared)
    global.setTimeout = origSetTimeout
    assert.strictEqual(waits, 2)
  })

  it('should pass correct retryCount to fallback error', async () => {
    node.failTimes = 3
    await node.run(shared)
    assert(node.fallbackError)
    assert.strictEqual(node.fallbackError.retryCount, 2)
  })
})
