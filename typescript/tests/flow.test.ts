import assert from 'assert'
import { beforeEach, describe, it } from 'node:test'
import { Flow, Node } from '../brainyflow'

class ActionNode extends Node<any, any, string> {
  public postCalledWith: any[] = []

  async prep(shared: Record<string, any>) {
    return this.params?.prepValue ?? 'prep'
  }
  protected async execRunner(shared: Record<string, any>, prepRes: any) {
    return this.params?.execValue ?? 'exec'
  }
  async post(shared: Record<string, any>, prepRes: any, execRes: any) {
    this.postCalledWith.push([shared, prepRes, execRes])
    return execRes
  }
}

describe('Flow', () => {
  let shared: Record<string, any>

  beforeEach(() => {
    shared = { log: [] }
  })

  it('should run a linear flow of nodes with default actions', async () => {
    const n1 = new ActionNode()
    const n2 = new ActionNode()
    const n3 = new ActionNode()
    n1.next(n2)
    n2.next(n3)
    const flow = new Flow(n1)
    flow.setParams({ execValue: 'default' })
    const result = await flow.run(shared)
    assert.strictEqual(result, 'default')
  })

  it('should follow custom action transitions', async () => {
    let call = 0
    class CustomActionNode extends ActionNode {
      protected async execRunner(shared: Record<string, any>, prepRes: any) {
        return this.params?.execValue?.[call++] ?? 'exec'
      }
    }
    const n1 = new CustomActionNode()
    const n2 = new CustomActionNode()
    const n3 = new CustomActionNode()
    n1.on('foo', n2)
    n2.on('bar', n3)
    const flow = new Flow(n1)
    flow.setParams({ execValue: ['foo', 'bar', 'shouldNotRun'] })
    const result = await flow.run(shared)
    assert.strictEqual(result, 'shouldNotRun')
  })

  it('should stop when no transition exists for returned action', async () => {
    let call = 0
    class CustomActionNode extends ActionNode {
      protected async execRunner(shared: Record<string, any>, prepRes: any) {
        return this.params?.execValue?.[call++] ?? 'exec'
      }
    }
    const n1 = new CustomActionNode()
    const n2 = new CustomActionNode()
    n1.on('go', n2)
    const flow = new Flow(n1)
    flow.setParams({ execValue: ['go', 'stop'] })
    const result = await flow.run(shared)
    assert.strictEqual(result, 'stop')
  })

  it('should propagate params to nodes', async () => {
    const n1 = new ActionNode()
    const flow = new Flow(n1)
    flow.setParams({ foo: 42 })
    n1.prep = async function (shared) {
      // Make the function async
      // @ts-ignore
      assert.strictEqual(this.params.foo, 42)
      return 'prep'
    }
    await flow.run(shared)
  })

  it('should throw if exec is called directly', () => {
    const n1 = new ActionNode()
    const flow = new Flow(n1)
    assert.throws(() => flow.exec('foo'), /should never be called/)
  })

  it('should handle errors in nodes gracefully', async () => {
    class ErrorNode extends ActionNode {
      protected async execRunner(shared: Record<string, any>, prepRes: any) {
        throw new Error('fail')
      }
    }
    const n1 = new ErrorNode()
    const flow = new Flow(n1)
    await assert.rejects(() => flow.run(shared), /fail/)
  })
})
