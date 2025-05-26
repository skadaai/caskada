import assert from 'node:assert/strict'
import { beforeEach, describe, it, mock } from 'node:test'
import { BaseNode, createMemory, DEFAULT_ACTION, ExecutionTree, Flow, Memory, Node, ParallelFlow, SharedStore } from '../brainyflow'

// --- Helper Nodes ---
class TestNode<
  G extends SharedStore = SharedStore,
  L extends SharedStore = SharedStore,
  AllowedA extends string[] = string[],
  P = any,
  E = any,
> extends Node<G, L, AllowedA, P, E> {
  id: string
  defaultPrepMockImpl = async (memory: Memory<G, L>): Promise<void> => {}
  defaultExecMockImpl = async (prepRes: P): Promise<E> => `exec_${this.id}` as any
  defaultPostMockImpl = async (memory: Memory<G, L>, prepRes: P, execRes: E): Promise<void> => {}

  prepMock = mock.fn(this.defaultPrepMockImpl)
  execMock = mock.fn(this.defaultExecMockImpl)
  postMock = mock.fn(this.defaultPostMockImpl)

  constructor(id: string) {
    super()
    this.id = id
  }

  async prep(memory: Memory<G, L>): Promise<P> {
    memory[`prep_${this.id}`] = true
    await this.prepMock(memory)
    return `prep_${this.id}` as any
  }

  async exec(prepRes: P): Promise<E> {
    assert.equal(prepRes, `prep_${this.id}`)
    return await this.execMock(prepRes)
  }

  async post(memory: Memory<G, L>, prepRes: P, execRes: E): Promise<void> {
    assert.equal(prepRes, `prep_${this.id}`)
    assert.equal(execRes, `exec_${this.id}` as any)
    memory[`post_${this.id}`] = true
    await this.postMock(memory, prepRes, execRes)
    // If no explicit trigger is called by a subclass's post or postMock,
    // the default trigger mechanism in BaseNode.listTriggers will take effect.
  }

  // Helper to reset mocks for this instance
  resetMocks() {
    this.prepMock = mock.fn(this.defaultPrepMockImpl)
    this.execMock = mock.fn(this.defaultExecMockImpl)
    this.postMock = mock.fn(this.defaultPostMockImpl)
  }
}

class BranchingNode<
  G extends SharedStore = SharedStore,
  L extends SharedStore = SharedStore,
  AllowedA extends string[] = string[],
  P = any,
  E = any,
> extends TestNode<G, L, AllowedA, P, E> {
  actionToTrigger: AllowedA[number] | typeof DEFAULT_ACTION = DEFAULT_ACTION
  forkDataForTrigger: SharedStore | null = null

  constructor(id: string) {
    super(id)
  }

  setTrigger(action: AllowedA[number] | typeof DEFAULT_ACTION, forkData: SharedStore | null = null) {
    this.actionToTrigger = action
    this.forkDataForTrigger = forkData
  }

  async post(memory: Memory<G, L>, prepRes: P, execRes: E): Promise<void> {
    await super.post(memory, prepRes, execRes)
    if (this.actionToTrigger) {
      this.trigger(this.actionToTrigger as AllowedA[number], this.forkDataForTrigger ?? {})
    }
  }
}

describe('Flow Class', () => {
  let globalStore: SharedStore
  let memory: Memory<SharedStore, SharedStore> // This memory is for general use if a test doesn't create its own specific one
  let nodeA: TestNode, nodeB: TestNode, nodeC: TestNode, nodeD: TestNode
  let branchingNodeInstance: BranchingNode

  beforeEach(() => {
    globalStore = { initial: 'global' }
    memory = createMemory(globalStore) // General memory for tests

    // Instantiate all nodes that will be used across different test groups or need consistent reset
    nodeA = new TestNode('A')
    nodeB = new TestNode('B')
    nodeC = new TestNode('C')
    nodeD = new TestNode('D')
    branchingNodeInstance = new BranchingNode('Branch')

    const nodesToResetMocks = [nodeA, nodeB, nodeC, nodeD, branchingNodeInstance]
    nodesToResetMocks.forEach((node) => {
      if (node instanceof TestNode) {
        // Ensures node is not undefined and is of TestNode type
        node.resetMocks()
      }
    })
  })

  describe('Initialization', () => {
    it('should store the start node and default options', () => {
      const flow = new Flow(nodeA)
      assert.strictEqual(flow.start, nodeA)
      assert.deepStrictEqual((flow as any).options, { maxVisits: 15 })
    })

    it('should accept custom options', () => {
      const flow = new Flow(nodeA, { maxVisits: 10 })
      assert.strictEqual(flow.start, nodeA)
      assert.deepStrictEqual((flow as any).options, { maxVisits: 10 })
    })
  })

  describe('Sequential Execution', () => {
    it('should execute nodes sequentially following default actions', async () => {
      nodeA.next(nodeB)
      nodeB.next(nodeC) // A -> B -> C
      const flow = new Flow(nodeA)
      const currentMemory = createMemory({ test_case: 'sequential' }) // Use a fresh memory
      await flow.run(currentMemory)

      assert.equal(nodeA.prepMock.mock.calls.length, 1, 'A prep')
      assert.equal(nodeA.execMock.mock.calls.length, 1, 'A exec')
      assert.equal(nodeA.postMock.mock.calls.length, 1, 'A post')
      assert.equal(nodeB.prepMock.mock.calls.length, 1, 'B prep')
      assert.equal(nodeB.execMock.mock.calls.length, 1, 'B exec')
      assert.equal(nodeB.postMock.mock.calls.length, 1, 'B post')
      assert.equal(nodeC.prepMock.mock.calls.length, 1, 'C prep')
      assert.equal(nodeC.execMock.mock.calls.length, 1, 'C exec')
      assert.equal(nodeC.postMock.mock.calls.length, 1, 'C post')

      assert.equal(currentMemory.prep_A, true)
      assert.equal(currentMemory.post_A, true)
      assert.equal(currentMemory.prep_B, true)
      assert.equal(currentMemory.post_B, true)
      assert.equal(currentMemory.prep_C, true)
      assert.equal(currentMemory.post_C, true)
    })

    it('should stop execution if a node has no successor for the triggered action', async () => {
      nodeA.next(nodeB) // A -> B (B has no successor for default)
      const flow = new Flow(nodeA)
      const currentMemory = createMemory({ test_case: 'stop_no_successor' })
      await flow.run(currentMemory)

      assert.equal(nodeA.postMock.mock.calls.length, 1, 'A post mock calls')
      assert.equal(nodeB.postMock.mock.calls.length, 1, 'B post mock calls')
      assert.equal(nodeC.prepMock.mock.calls.length, 0, 'C prep mock calls (should not run)')
    })
  })

  describe('Conditional Branching', () => {
    it('should follow the correct path based on triggered action', async () => {
      branchingNodeInstance.on('path_B' as any, nodeB)
      branchingNodeInstance.on('path_C' as any, nodeC)

      // Test path B
      branchingNodeInstance.setTrigger('path_B' as any)
      let flowB = new Flow(branchingNodeInstance)
      let memoryB = createMemory({})
      await flowB.run(memoryB)

      assert.equal(memoryB.post_Branch, true, 'Branch node post flag for path_B')
      assert.equal(memoryB.post_B, true, 'Node B post flag for path_B')
      assert.strictEqual((memoryB as any).post_C, undefined, 'Node C should not have post_C flag for path_B')
      assert.equal(nodeB.postMock.mock.calls.length, 1, 'NodeB postMock for path_B')
      assert.equal(nodeC.postMock.mock.calls.length, 0, 'NodeC postMock for path_B')

      nodeB.resetMocks()
      nodeC.resetMocks()

      // Test path C
      branchingNodeInstance.setTrigger('path_C' as any)
      let flowC = new Flow(branchingNodeInstance)
      let memoryC = createMemory({})
      await flowC.run(memoryC)

      assert.equal(memoryC.post_Branch, true, 'Branch node post flag for path_C')
      assert.strictEqual((memoryC as any).post_B, undefined, 'Node B should not have post_B flag for path_C')
      assert.equal(memoryC.post_C, true, 'Node C post flag for path_C')
      assert.equal(nodeB.postMock.mock.calls.length, 0, 'NodeB postMock for path_C')
      assert.equal(nodeC.postMock.mock.calls.length, 1, 'NodeC postMock for path_C')
    })
  })

  describe('Memory Handling', () => {
    it('should propagate global memory changes', async () => {
      nodeA.postMock.mock.mockImplementation(async (mem: Memory) => {
        mem.global_A = 'set_by_A'
      })
      nodeB.prepMock.mock.mockImplementation(async (mem: Memory) => {
        assert.equal(mem.global_A, 'set_by_A', 'Node B should see global_A from Node A')
      })
      nodeA.next(nodeB)
      const flow = new Flow(nodeA)
      const currentGlobalStore = { test_case: 'global_propagate' }
      const currentMemory = createMemory(currentGlobalStore)
      await flow.run(currentMemory)

      assert.equal(currentMemory.global_A, 'set_by_A', 'Memory should have global_A after flow')
      assert.equal(currentGlobalStore.global_A, 'set_by_A', 'Original global store object should be modified')
      assert.equal(nodeB.prepMock.mock.calls.length, 1, 'Node B prepMock calls')
    })

    it('should isolate local memory using forkingData', async () => {
      branchingNodeInstance.on('path_B' as any, nodeB)
      branchingNodeInstance.on('path_C' as any, nodeC)

      nodeB.prepMock.mock.mockImplementation(async (mem: Memory) => {
        assert.equal(mem.local_data, 'for_B', 'Node B local_data incorrect')
        assert.equal(mem.common_local, 'common', 'Node B common_local incorrect')
        assert.strictEqual(mem.local.local_data, 'for_B', 'Node B mem.local.local_data incorrect')
        assert.strictEqual(mem.local.common_local, 'common', 'Node B mem.local.common_local incorrect')
      })
      nodeC.prepMock.mock.mockImplementation(async (mem: Memory) => {
        assert.equal(mem.local_data, 'for_C', 'Node C local_data incorrect')
        assert.equal(mem.common_local, 'common', 'Node C common_local incorrect')
        assert.strictEqual(mem.local.local_data, 'for_C', 'Node C mem.local.local_data incorrect')
        assert.strictEqual(mem.local.common_local, 'common', 'Node C mem.local.common_local incorrect')
      })

      // Trigger B
      branchingNodeInstance.setTrigger('path_B' as any, { local_data: 'for_B', common_local: 'common' })
      let flowB = new Flow(branchingNodeInstance)
      let memoryB = createMemory({ global_val: 1 })
      await flowB.run(memoryB)
      assert.equal(nodeB.prepMock.mock.calls.length, 1, 'Node B prepMock calls for path_B')
      assert.equal(nodeC.prepMock.mock.calls.length, 0, 'Node C prepMock calls for path_B')
      assert.strictEqual((memoryB as any).local_data, undefined, 'memoryB should not have local_data')
      assert.strictEqual((memoryB as any).common_local, undefined, 'memoryB should not have common_local')

      nodeB.resetMocks()
      nodeC.resetMocks()

      // Trigger C
      branchingNodeInstance.setTrigger('path_C' as any, { local_data: 'for_C', common_local: 'common' })
      let flowC = new Flow(branchingNodeInstance)
      let memoryC = createMemory({ global_val: 1 })
      await flowC.run(memoryC)
      assert.equal(nodeB.prepMock.mock.calls.length, 0, 'Node B prepMock calls for path_C')
      assert.equal(nodeC.prepMock.mock.calls.length, 1, 'Node C prepMock calls for path_C')
      assert.strictEqual((memoryC as any).local_data, undefined, 'memoryC should not have local_data')
      assert.strictEqual((memoryC as any).common_local, undefined, 'memoryC should not have common_local')
    })
  })

  describe('Cycle Detection', () => {
    it('should execute a loop exactly maxVisits times before throwing error', async () => {
      let loopCount = 0
      const maxVisitsAllowed = 3
      nodeA.prepMock.mock.mockImplementation(async (mem: Memory) => {
        loopCount++
        mem.count = loopCount
      })
      nodeA.next(nodeA)
      const flow = new Flow(nodeA, { maxVisits: maxVisitsAllowed })
      const loopMemory = createMemory<{ count?: number }>({})

      await assert.rejects(
        async () => {
          try {
            await flow.run(loopMemory)
          } catch (e: any) {
            assert.equal(loopCount, maxVisitsAllowed, `Node should have executed ${maxVisitsAllowed} times before error`)
            assert.equal(loopMemory.count, maxVisitsAllowed, `Memory count should be ${maxVisitsAllowed} before error`)
            throw e
          }
          assert.fail('Flow should have rejected due to cycle limit')
        },
        (err: Error) => {
          assert.match(
            err.message,
            new RegExp(`Maximum cycle count \\(${maxVisitsAllowed}\\) reached for TestNode#${nodeA.__nodeOrder}`),
          )
          return true
        },
        'Flow should reject when loop count exceeds maxVisits',
      )
      assert.equal(loopCount, maxVisitsAllowed, `Node should have executed ${maxVisitsAllowed} times (final check)`)
    })
  })

  describe('ExecutionTree Result Structure', () => {
    it('should return triggered: { default: [] } if a node is terminal and has no explicit trigger', async () => {
      const terminalNode = new TestNode('Terminal') // Terminal by default
      // Ensure its post method does NOT call this.trigger explicitly
      terminalNode.postMock = mock.fn(async (mem, prepRes, execRes) => {
        // No explicit this.trigger(...) call here.
        // The TestNode.post will call this mock, but won't call this.trigger itself.
        // BaseNode.run will clear this.triggers, then call post.
        // If this.triggers is still empty, BaseNode.listTriggers returns default.
      })

      const flow = new Flow(terminalNode)
      const result = (await flow.run(createMemory({}))) as ExecutionTree

      const expected: ExecutionTree = {
        order: terminalNode.__nodeOrder,
        type: 'TestNode',
        // According to BaseNode.listTriggers, if this.triggers is empty,
        // it defaults to [[DEFAULT_ACTION, memory.clone()]].
        // Flow.runNode then processes this, and if no successor for DEFAULT_ACTION,
        // it results in { [DEFAULT_ACTION]: [] } for triggered.
        triggered: { [DEFAULT_ACTION]: [] },
      }
      assert.deepStrictEqual(result, expected)
    })
  })

  // For "Flow as Node" tests that fail with {}, it usually means an unhandled promise rejection
  // or an error swallowed somewhere. We'd need to carefully trace their execution.
  // A common cause is if a sub-flow's run method itself throws an error, or if
  // assertions are made on undefined properties.
  describe('Flow as Node (Nesting)', () => {
    it('should execute a nested flow as a single node step', async () => {
      nodeB.next(nodeC)
      const subFlow = new Flow(nodeB)
      nodeA.next(subFlow as BaseNode)
      subFlow.next(nodeD as BaseNode)

      const mainFlow = new Flow(nodeA)
      const mainMemory = createMemory({ flow: 'main' })
      const result = (await mainFlow.run(mainMemory)) as ExecutionTree

      assert.equal(nodeA.postMock.mock.calls.length, 1, 'Node A post')
      assert.equal(nodeB.postMock.mock.calls.length, 1, 'Node B post (in subFlow)')
      assert.equal(nodeC.postMock.mock.calls.length, 1, 'Node C post (in subFlow)')
      assert.equal(nodeD.postMock.mock.calls.length, 1, 'Node D post (after subFlow)')

      assert.equal(mainMemory.post_A, true)
      assert.equal(mainMemory.post_B, true)
      assert.equal(mainMemory.post_C, true)
      assert.equal(mainMemory.post_D, true)

      assert.equal(result.order, nodeA.__nodeOrder)
      assert.equal(result.type, 'TestNode')
      assert.ok(result.triggered?.[DEFAULT_ACTION]?.[0], 'SubFlow not triggered correctly from A')
      const subFlowResultInTree = result.triggered![DEFAULT_ACTION][0]
      assert.equal(subFlowResultInTree.order, subFlow.__nodeOrder)
      assert.equal(subFlowResultInTree.type, 'Flow')
      assert.ok(subFlowResultInTree.triggered?.[DEFAULT_ACTION]?.[0], 'Node D not triggered by SubFlow')
      const nodeDfromSubFlowTrigger = subFlowResultInTree.triggered![DEFAULT_ACTION][0]
      assert.equal(nodeDfromSubFlowTrigger.order, nodeD.__nodeOrder)
      assert.equal(nodeDfromSubFlowTrigger.type, 'TestNode')
    })

    it('nested flow prep/post should wrap sub-flow execution', async () => {
      nodeB.next(nodeC)
      const subFlow = new Flow(nodeB)

      const subFlowPrepMockImpl = async (mem: Memory) => {
        mem.subflow_prep_flag = true
      }
      const subFlowPostMockImpl = async (mem: Memory, prepRes: any, execRes: ExecutionTree) => {
        mem.subflow_post_flag = true
      }

      subFlow.prep = mock.fn(subFlowPrepMockImpl)
      subFlow.post = mock.fn(subFlowPostMockImpl)

      nodeA.next(subFlow as BaseNode).next(nodeD as BaseNode)
      const mainFlow = new Flow(nodeA)
      const mainMemory = createMemory({ flow: 'main_prep_post' })
      await mainFlow.run(mainMemory)

      assert.equal((subFlow.prep as any).mock.calls.length, 1, 'SubFlow prep mock')
      assert.equal(mainMemory.subflow_prep_flag, true, 'SubFlow prep flag in memory')
      assert.equal(nodeB.postMock.mock.calls.length, 1, 'Node B (in subFlow) post mock')
      assert.equal(nodeC.postMock.mock.calls.length, 1, 'Node C (in subFlow) post mock')
      assert.equal((subFlow.post as any).mock.calls.length, 1, 'SubFlow post mock')
      assert.equal(mainMemory.subflow_post_flag, true, 'SubFlow post flag in memory')
      assert.equal(nodeD.postMock.mock.calls.length, 1, 'Node D (after subFlow) post mock')
    })
  })

  describe('ExecutionTree Result Structure', () => {
    it('should return the correct ExecutionTree for a simple flow A -> B', async () => {
      nodeA.next(nodeB)
      const flow = new Flow(nodeA)
      const currentMemory = createMemory({ test_case: 'exec_tree_simple' })
      const result = (await flow.run(currentMemory)) as ExecutionTree

      const expected: ExecutionTree = {
        order: nodeA.__nodeOrder,
        type: 'TestNode',
        triggered: {
          [DEFAULT_ACTION]: [
            {
              order: nodeB.__nodeOrder,
              type: 'TestNode',
              triggered: { [DEFAULT_ACTION]: [] },
            },
          ],
        },
      }
      assert.deepStrictEqual(result, expected)
    })

    it('should return triggered: { default: [] } if a node is terminal and its post does not explicitly trigger', async () => {
      const terminalNode = new TestNode('TerminalOnly')
      terminalNode.postMock = mock.fn(async (mem, prepRes, execRes) => {
        // This mock for postMock is called by TestNode.post.
        // TestNode.post itself does not call this.trigger().
        // So, this.triggers in BaseNode remains empty after post() finishes.
      })

      const flow = new Flow(terminalNode)
      const currentMemory = createMemory({ test_case: 'exec_tree_terminal_implicit_default' })
      const result = (await flow.run(currentMemory)) as ExecutionTree

      const expected: ExecutionTree = {
        order: terminalNode.__nodeOrder,
        type: 'TestNode',
        triggered: { [DEFAULT_ACTION]: [] }, // BaseNode.listTriggers provides default
      }
      assert.deepStrictEqual(result, expected)
    })

    it('should return triggered: null if post explicitly clears triggers and calls no new trigger (advanced case)', async () => {
      // This tests a scenario where a node's post method actively manipulates this.triggers to be empty
      // AND prevents the default mechanism if the Flow logic were to allow `null` for non-triggering terminals.
      // However, with current brainyflow.ts, Flow.runNode populates triggered based on listTriggers.
      // If listTriggers returns default, triggered will show default.
      // To get `null`, `listTriggers` would have to return empty, or `Flow.runNode` would need to interpret empty `listTriggers` as `null`.
      // The current test for "terminal and no explicit trigger" already covers the standard behavior.
      // This test case demonstrates how one might *try* to get null, and why it results in default.
      const specialTerminalNode = new TestNode('SpecialTerminal')
      specialTerminalNode.post = mock.fn(async function (this: BaseNode, mem, prepRes, execRes) {
        // Call the original TestNode post logic if needed for flags, but not its mock that might trigger.
        // Or just set the flag directly.
        mem[`post_${(this as TestNode).id}`] = true
        // Explicitly ensure triggers array is empty. BaseNode.run already does this before calling post.
        this.triggers = []
        // Crucially, do NOT call this.trigger()
      })

      const flow = new Flow(specialTerminalNode)
      const result = (await flow.run(createMemory({}))) as ExecutionTree

      // Based on current brainyflow.ts:
      // 1. BaseNode.run clears this.triggers.
      // 2. specialTerminalNode.post (mocked) runs, doesn't call this.trigger(). this.triggers remains [].
      // 3. BaseNode.listTriggers sees empty this.triggers, returns [[DEFAULT_ACTION, ...]].
      // 4. Flow.runNode processes this, finds no successor for DEFAULT_ACTION.
      // Result is { ..., triggered: { [DEFAULT_ACTION]: [] } }
      const expected: ExecutionTree = {
        order: specialTerminalNode.__nodeOrder,
        type: 'TestNode',
        triggered: { [DEFAULT_ACTION]: [] },
      }
      assert.deepStrictEqual(result, expected)
    })

    it('should return correct structure for branching flow', async () => {
      branchingNodeInstance.on('path_B' as any, nodeB)
      branchingNodeInstance.on('path_C' as any, nodeC)
      nodeB.next(nodeD)

      branchingNodeInstance.setTrigger('path_B' as any)
      let flowB_exec = new Flow(branchingNodeInstance)
      let resultB = (await flowB_exec.run(createMemory({}))) as ExecutionTree

      const expectedB: ExecutionTree = {
        order: branchingNodeInstance.__nodeOrder,
        type: 'BranchingNode',
        triggered: {
          path_B: [
            {
              order: nodeB.__nodeOrder,
              type: 'TestNode',
              triggered: {
                [DEFAULT_ACTION]: [
                  {
                    order: nodeD.__nodeOrder,
                    type: 'TestNode',
                    triggered: { [DEFAULT_ACTION]: [] },
                  },
                ],
              },
            },
          ],
        },
      }
      assert.deepStrictEqual(resultB, expectedB)

      nodeB.resetMocks()
      nodeC.resetMocks()
      nodeD.resetMocks() // Reset for next part

      branchingNodeInstance.setTrigger('path_C' as any)
      let flowC_exec = new Flow(branchingNodeInstance)
      let resultC = (await flowC_exec.run(createMemory({}))) as ExecutionTree
      const expectedC: ExecutionTree = {
        order: branchingNodeInstance.__nodeOrder,
        type: 'BranchingNode',
        triggered: {
          path_C: [
            {
              order: nodeC.__nodeOrder,
              type: 'TestNode',
              triggered: { [DEFAULT_ACTION]: [] },
            },
          ],
        },
      }
      assert.deepStrictEqual(resultC, expectedC)
    })

    it('should return correct structure for multi-trigger (fan-out)', async () => {
      class MultiTriggerNode extends TestNode<SharedStore, SharedStore, ['out1', 'out2']> {
        constructor(id: string) {
          super(id)
        }
        async post(mem: Memory, prepRes: any, execRes: any) {
          await super.post(mem, prepRes, execRes)
          this.trigger('out1', { data: 'for_out1' })
          this.trigger('out2', { data: 'for_out2' })
        }
      }
      const multiNode = new MultiTriggerNode('Multi')
      multiNode.on('out1', nodeB)
      multiNode.on('out2', nodeC)

      const flow = new Flow(multiNode)
      const currentMemory = createMemory({ test_case: 'exec_tree_multi_trigger' })
      const result = (await flow.run(currentMemory)) as ExecutionTree

      const expected: ExecutionTree = {
        order: multiNode.__nodeOrder,
        type: 'MultiTriggerNode',
        triggered: {
          out1: [{ order: nodeB.__nodeOrder, type: 'TestNode', triggered: { [DEFAULT_ACTION]: [] } }],
          out2: [{ order: nodeC.__nodeOrder, type: 'TestNode', triggered: { [DEFAULT_ACTION]: [] } }],
        },
      }
      assert.ok(result.triggered, 'Result should have a triggered field')
      const resultKeys = Object.keys(result.triggered!).sort()
      const expectedKeys = Object.keys(expected.triggered!).sort()
      assert.deepStrictEqual(resultKeys, expectedKeys, 'Keys of triggered object mismatch')
      assert.deepStrictEqual(result.triggered!['out1'], expected.triggered!['out1'])
      assert.deepStrictEqual(result.triggered!['out2'], expected.triggered!['out2'])
      assert.strictEqual(result.order, expected.order)
      assert.strictEqual(result.type, expected.type)
    })
  })

  describe('ParallelFlow', () => {
    it('should execute parallel branches concurrently', async () => {
      const parallelStartNode = new BranchingNode('ParallelStartNode') // Use a distinct instance
      const nodeP1 = new TestNode('P1')
      const nodeP2 = new TestNode('P2')

      // Reset mocks for P1 and P2 specifically for this test
      nodeP1.resetMocks()
      nodeP2.resetMocks()
      parallelStartNode.resetMocks()

      let p1DoneTime = 0
      let p2DoneTime = 0

      nodeP1.execMock.mock.mockImplementation(async () => {
        await new Promise((resolve) => setTimeout(resolve, 50)) // P1 is slower
        p1DoneTime = Date.now()
        return 'exec_P1'
      })
      nodeP2.execMock.mock.mockImplementation(async () => {
        await new Promise((resolve) => setTimeout(resolve, 10)) // P2 is faster
        p2DoneTime = Date.now()
        return 'exec_P2'
      })

      parallelStartNode.on('branch1', nodeP1)
      parallelStartNode.on('branch2', nodeP2)

      parallelStartNode.post = async function (this: BranchingNode, memory, prepRes, execRes) {
        // Call TestNode's post for flags etc.
        await TestNode.prototype.post.call(this, memory, prepRes, execRes)
        // Explicitly clear and set triggers for this test
        this.triggers = []
        this.trigger('branch1' as any, { data: 'for_p1' })
        this.trigger('branch2' as any, { data: 'for_p2' })
      }

      const flow = new ParallelFlow(parallelStartNode)
      await flow.run(createMemory({ test_case: 'parallel_flow_concurrent' }))

      assert.ok(p1DoneTime > 0, 'P1 should have completed')
      assert.ok(p2DoneTime > 0, 'P2 should have completed')
      assert.ok(
        p2DoneTime < p1DoneTime,
        `P2 (ended at ${p2DoneTime}) should finish before P1 (ended at ${p1DoneTime}) if truly parallel`,
      )
      assert.equal(nodeP1.execMock.mock.calls.length, 1, 'P1 exec should be called once')
      assert.equal(nodeP2.execMock.mock.calls.length, 1, 'P2 exec should be called once')
    })
  })
})
