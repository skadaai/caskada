import assert from 'node:assert/strict'
import { beforeEach, describe, it, mock } from 'node:test'
import { BaseNode, createMemory, DEFAULT_ACTION, ExecutionTree, Flow, Memory, Node, ParallelFlow, SharedStore } from '../brainyflow'

// --- Helper Nodes ---
class TestNode<
  G extends SharedStore = SharedStore,
  AllowedA extends string[] = string[], // Mapped to Action[] in BaseNode
  P = any,
  E = any,
> extends Node<G, P, E, AllowedA> {
  // Adjusted generic parameters to match Node
  id: string
  defaultPrepMockImpl = async (memory: Memory<G>): Promise<void> => {} // Memory uses GS, LS (InferLocal<GS>)
  defaultExecMockImpl = async (prepRes: P): Promise<E> => `exec_${this.id}` as any
  defaultPostMockImpl = async (memory: Memory<G>, prepRes: P, execRes: E): Promise<void> => {}

  prepMock = mock.fn(this.defaultPrepMockImpl)
  execMock = mock.fn(this.defaultExecMockImpl)
  postMock = mock.fn(this.defaultPostMockImpl)

  constructor(id: string) {
    super()
    this.id = id
  }

  async prep(memory: Memory<G>): Promise<P> {
    memory[`prep_${this.id}`] = true
    await this.prepMock(memory)
    return `prep_${this.id}` as any
  }

  async exec(prepRes: P): Promise<E> {
    assert.equal(prepRes, `prep_${this.id}`)
    return await this.execMock(prepRes)
  }

  async post(memory: Memory<G>, prepRes: P, execRes: E): Promise<void> {
    assert.equal(prepRes, `prep_${this.id}`)
    // Ensure execRes can be undefined if exec returns void
    if (execRes !== undefined || `exec_${this.id}` !== undefined) {
      assert.equal(execRes, `exec_${this.id}` as any)
    }
    memory[`post_${this.id}`] = true
    await this.postMock(memory, prepRes, execRes)
  }

  resetMocks() {
    this.prepMock = mock.fn(this.defaultPrepMockImpl)
    this.execMock = mock.fn(this.defaultExecMockImpl)
    this.postMock = mock.fn(this.defaultPostMockImpl)
  }
}

class BranchingNode<G extends SharedStore = SharedStore, AllowedA extends string[] = string[], P = any, E = any> extends TestNode<
  G,
  AllowedA,
  P,
  E
> {
  actionToTrigger: AllowedA[number] | typeof DEFAULT_ACTION = DEFAULT_ACTION
  forkDataForTrigger: SharedStore | null = null
  private clearTriggersFirstInPost = false

  constructor(id: string) {
    super(id)
  }

  setTrigger(action: AllowedA[number] | typeof DEFAULT_ACTION, forkData: SharedStore | null = null, clearPrevious: boolean = false) {
    this.actionToTrigger = action
    this.forkDataForTrigger = forkData
    this.clearTriggersFirstInPost = clearPrevious
  }

  async post(memory: Memory<G>, prepRes: P, execRes: E): Promise<void> {
    await super.post(memory, prepRes, execRes) // Calls TestNode.post, which calls this.postMock
    if (this.clearTriggersFirstInPost) {
      this.triggers = [] // Clear any triggers set by super.post or its mock
    }
    if (this.actionToTrigger) {
      // Cast is necessary because AllowedA[number] might not be assignable to Action if AllowedA is too narrow
      this.trigger(this.actionToTrigger as any, this.forkDataForTrigger ?? {})
    }
  }
}

describe('Flow Class', () => {
  let globalStore: SharedStore
  let memory: Memory<SharedStore>
  let nodeA: TestNode, nodeB: TestNode, nodeC: TestNode, nodeD: TestNode
  let branchingNodeInstance: BranchingNode

  beforeEach(() => {
    ;(BaseNode as any).__nextId = 0 // Reset node order for deterministic tests
    globalStore = { initial: 'global' }
    memory = createMemory(globalStore)

    nodeA = new TestNode('A')
    nodeB = new TestNode('B')
    nodeC = new TestNode('C')
    nodeD = new TestNode('D')
    branchingNodeInstance = new BranchingNode('Branch')

    const nodesToResetMocks = [nodeA, nodeB, nodeC, nodeD, branchingNodeInstance]
    nodesToResetMocks.forEach((node) => {
      if (node instanceof TestNode) {
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
      // A=0, B=1, C=2
      nodeA.next(nodeB)
      nodeB.next(nodeC) // A -> B -> C
      const flow = new Flow(nodeA) // flow=3
      const currentMemory = createMemory({ test_case: 'sequential' })
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
      // A=0, B=1, C=2 (unused)
      nodeA.next(nodeB) // A -> B (B has no successor for default)
      const flow = new Flow(nodeA) // flow=3
      const currentMemory = createMemory({ test_case: 'stop_no_successor' })
      await flow.run(currentMemory)

      assert.equal(nodeA.postMock.mock.calls.length, 1, 'A post mock calls')
      assert.equal(nodeB.postMock.mock.calls.length, 1, 'B post mock calls')
      assert.equal(nodeC.prepMock.mock.calls.length, 0, 'C prep mock calls (should not run)')
    })
  })

  describe('Conditional Branching', () => {
    it('should follow the correct path based on triggered action', async () => {
      // Branch=0, B=1, C=2
      branchingNodeInstance.on('path_B' as any, nodeB)
      branchingNodeInstance.on('path_C' as any, nodeC)

      // Test path B
      branchingNodeInstance.setTrigger('path_B' as any)
      let flowB = new Flow(branchingNodeInstance) // flowB=3
      let memoryB = createMemory({})
      await flowB.run(memoryB)

      assert.equal(memoryB.post_Branch, true, 'Branch node post flag for path_B')
      assert.equal(memoryB.post_B, true, 'Node B post flag for path_B')
      assert.strictEqual((memoryB as any).post_C, undefined, 'Node C should not have post_C flag for path_B')
      assert.equal(nodeB.postMock.mock.calls.length, 1, 'NodeB postMock for path_B')
      assert.equal(nodeC.postMock.mock.calls.length, 0, 'NodeC postMock for path_B')

      // Reset for next part of the test: Branch=0, B=1, C=2. Node orders are global to the test suite due to beforeEach reset.
      // We need new instances or careful mock resets if __nodeOrder matters deeply for sub-assertions.
      // For this test, we reset mocks.
      nodeB.resetMocks()
      nodeC.resetMocks()

      const localBranchingNode = new BranchingNode('BranchLocal1') //0
      const localNodeB = new TestNode('BLocal1') //1
      const localNodeC = new TestNode('CLocal1') //2
      localBranchingNode.on('path_B' as any, localNodeB)
      localBranchingNode.on('path_C' as any, localNodeC)

      // Test path C
      localBranchingNode.setTrigger('path_C' as any)
      let flowC = new Flow(localBranchingNode) // flowC=3
      let memoryC = createMemory({})
      await flowC.run(memoryC)

      assert.equal(memoryC.post_BranchLocal1, true, 'Branch node post flag for path_C')
      assert.strictEqual((memoryC as any).post_BLocal1, undefined, 'Node B should not have post_B flag for path_C')
      assert.equal(memoryC.post_CLocal1, true, 'Node C post flag for path_C')
      assert.equal(localNodeB.postMock.mock.calls.length, 0, 'NodeB postMock for path_C')
      assert.equal(localNodeC.postMock.mock.calls.length, 1, 'NodeC postMock for path_C')
    })
  })

  describe('Memory Handling', () => {
    it('should propagate global memory changes', async () => {
      // A=0, B=1
      nodeA.postMock.mock.mockImplementation(async (mem: Memory) => {
        mem.global_A = 'set_by_A'
      })
      nodeB.prepMock.mock.mockImplementation(async (mem: Memory) => {
        assert.equal(mem.global_A, 'set_by_A', 'Node B should see global_A from Node A')
      })
      nodeA.next(nodeB)
      const flow = new Flow(nodeA) // flow=2
      const currentGlobalStore = { test_case: 'global_propagate' }
      const currentMemory = createMemory(currentGlobalStore)
      await flow.run(currentMemory)

      assert.equal(currentMemory.global_A, 'set_by_A', 'Memory should have global_A after flow')
      assert.equal(currentGlobalStore.global_A, 'set_by_A', 'Original global store object should be modified')
      assert.equal(nodeB.prepMock.mock.calls.length, 1, 'Node B prepMock calls')
    })

    it('should isolate local memory using forkingData', async () => {
      // Branch=0, B=1, C=2
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
      let flowB_mem = new Flow(branchingNodeInstance) // flowB_mem=3
      let memoryB_mem = createMemory({ global_val: 1 })
      await flowB_mem.run(memoryB_mem)
      assert.equal(nodeB.prepMock.mock.calls.length, 1, 'Node B prepMock calls for path_B')
      assert.equal(nodeC.prepMock.mock.calls.length, 0, 'Node C prepMock calls for path_B')
      assert.strictEqual((memoryB_mem as any).local_data, undefined, 'memoryB_mem should not have local_data')
      assert.strictEqual((memoryB_mem as any).common_local, undefined, 'memoryC_mem should not have common_local')

      nodeB.resetMocks()
      nodeC.resetMocks()

      // Trigger C
      branchingNodeInstance.setTrigger('path_C' as any, { local_data: 'for_C', common_local: 'common' })
      let flowC_mem = new Flow(branchingNodeInstance) // flowC_mem gets new order if __nextId not reset before its creation
      let memoryC_mem = createMemory({ global_val: 1 })
      await flowC_mem.run(memoryC_mem)
      assert.equal(nodeB.prepMock.mock.calls.length, 0, 'Node B prepMock calls for path_C')
      assert.equal(nodeC.prepMock.mock.calls.length, 1, 'Node C prepMock calls for path_C')
      assert.strictEqual((memoryC_mem as any).local_data, undefined, 'memoryC_mem should not have local_data')
      assert.strictEqual((memoryC_mem as any).common_local, undefined, 'memoryC_mem should not have common_local')
    })
  })

  describe('Cycle Detection', () => {
    it('should execute a loop exactly maxVisits times before throwing error', async () => {
      let loopCount = 0
      const maxVisitsAllowed = 3
      const loopingNode = new TestNode('LoopNode') // 0
      loopingNode.prepMock.mock.mockImplementation(async (mem: Memory) => {
        loopCount++
        mem.count = loopCount
      })
      loopingNode.next(loopingNode) // Points to itself
      const flow = new Flow(loopingNode, { maxVisits: maxVisitsAllowed }) // flow=1
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
            new RegExp(`Maximum cycle count \\(${maxVisitsAllowed}\\) reached for TestNode#${loopingNode.__nodeOrder}`),
          )
          return true
        },
        'Flow should reject when loop count exceeds maxVisits',
      )
      assert.equal(loopCount, maxVisitsAllowed, `Node should have executed ${maxVisitsAllowed} times (final check)`)
    })
  })

  describe('Flow as Node (Nesting)', () => {
    it('should execute a nested flow as a single node step', async () => {
      // OuterA=0, (SubFlow's B=1, C=2), OuterD=3
      nodeB.next(nodeC)
      const subFlow = new Flow(nodeB)
      const outerA = new TestNode('OuterA') // 0
      const subNodeB = new TestNode('SubNodeB') // 1
      const subNodeC = new TestNode('SubNodeC') // 2
      const outerD = new TestNode('OuterD') // 3

      subNodeB.next(subNodeC)
      const nestedFlow = new Flow(subNodeB) // nestedFlow=4
      outerA.next(nestedFlow as BaseNode)
      nestedFlow.next(outerD as BaseNode)

      const mainFlow = new Flow(outerA) // mainFlow=5
      const mainMemory = createMemory({ flow: 'main' })
      const result = (await mainFlow.run(mainMemory)) as ExecutionTree

      assert.equal(outerA.postMock.mock.calls.length, 1, 'OuterA post')
      assert.equal(subNodeB.postMock.mock.calls.length, 1, 'SubNodeB post (in nestedFlow)')
      assert.equal(subNodeC.postMock.mock.calls.length, 1, 'SubNodeC post (in nestedFlow)')
      assert.equal(outerD.postMock.mock.calls.length, 1, 'OuterD post (after nestedFlow)')

      assert.equal(mainMemory.post_OuterA, true)
      assert.equal(mainMemory.post_SubNodeB, true)
      assert.equal(mainMemory.post_SubNodeC, true)
      assert.equal(mainMemory.post_OuterD, true)

      assert.equal(result.order, outerA.__nodeOrder) // 0
      assert.equal(result.type, 'TestNode')
      assert.ok(result.triggered?.[DEFAULT_ACTION]?.[0], 'NestedFlow not triggered correctly from OuterA')
      const subFlowResultInTree = result.triggered![DEFAULT_ACTION][0]
      assert.equal(subFlowResultInTree.order, nestedFlow.__nodeOrder) // 4
      assert.equal(subFlowResultInTree.type, 'Flow')
      assert.ok(subFlowResultInTree.triggered?.[DEFAULT_ACTION]?.[0], 'OuterD not triggered by NestedFlow')
      const nodeDfromSubFlowTrigger = subFlowResultInTree.triggered![DEFAULT_ACTION][0]
      assert.equal(nodeDfromSubFlowTrigger.order, outerD.__nodeOrder) // 3
      assert.equal(nodeDfromSubFlowTrigger.type, 'TestNode')
    })

    it('nested flow prep/post should wrap sub-flow execution', async () => {
      ;(BaseNode as any).__nextId = 0
      const outerA = new TestNode('OuterA') // 0
      const subNodeB = new TestNode('SubNodeB') // 1
      const subNodeC = new TestNode('SubNodeC') // 2
      const outerD = new TestNode('OuterD') // 3

      subNodeB.next(subNodeC)
      const nestedFlow = new Flow(subNodeB) // nestedFlow=4

      const subFlowPrepMockImpl = async (mem: Memory) => {
        mem.subflow_prep_flag = true
      }
      const subFlowPostMockImpl = async (mem: Memory, prepRes: any, execRes: ExecutionTree) => {
        mem.subflow_post_flag = true
      }

      nestedFlow.prep = mock.fn(subFlowPrepMockImpl)
      nestedFlow.post = mock.fn(subFlowPostMockImpl) // This is Flow's own post

      outerA.next(nestedFlow as BaseNode).next(outerD as BaseNode) // Link OuterA -> nestedFlow -> OuterD
      const mainFlow = new Flow(outerA) // mainFlow=5
      const mainMemory = createMemory({ flow: 'main_prep_post' })
      await mainFlow.run(mainMemory)

      assert.equal((nestedFlow.prep as any).mock.calls.length, 1, 'NestedFlow prep mock')
      assert.equal(mainMemory.subflow_prep_flag, true, 'NestedFlow prep flag in memory')
      assert.equal(subNodeB.postMock.mock.calls.length, 1, 'SubNodeB (in nestedFlow) post mock')
      assert.equal(subNodeC.postMock.mock.calls.length, 1, 'SubNodeC (in nestedFlow) post mock')
      assert.equal((nestedFlow.post as any).mock.calls.length, 1, 'NestedFlow post mock')
      assert.equal(mainMemory.subflow_post_flag, true, 'NestedFlow post flag in memory')
      assert.equal(outerD.postMock.mock.calls.length, 1, 'OuterD (after nestedFlow) post mock')
    })
  })

  describe('ExecutionTree Result Structure', () => {
    it('should return the correct ExecutionTree for a simple flow A -> B', async () => {
      ;(BaseNode as any).__nextId = 0
      const nodeA_tree = new TestNode('A_tree') // 0
      const nodeB_tree = new TestNode('B_tree') // 1
      nodeA_tree.next(nodeB_tree)
      const flow = new Flow(nodeA_tree) // 2
      const currentMemory = createMemory({ test_case: 'exec_tree_simple' })
      const result = (await flow.run(currentMemory)) as ExecutionTree

      const expected: ExecutionTree = {
        order: nodeA_tree.__nodeOrder, // 0
        type: 'TestNode',
        triggered: {
          [DEFAULT_ACTION]: [
            {
              order: nodeB_tree.__nodeOrder, // 1
              type: 'TestNode',
              triggered: null, // B is terminal, its own default action leads to nothing
            },
          ],
        },
      }
      assert.deepStrictEqual(result, expected)
    })

    it('ExecutionTree: terminal node (no explicit trigger) shows its own implicit DEFAULT_ACTION', async () => {
      ;(BaseNode as any).__nextId = 0
      const terminalNode = new TestNode('TerminalOnly') // 0
      // TestNode's default postMock does not call this.trigger()
      terminalNode.postMock = mock.fn(async () => {})

      const flow = new Flow(terminalNode) // 1
      const result = (await flow.run(createMemory({}))) as ExecutionTree
      // The result here is the ExecutionTree of the *Flow's start node* (terminalNode)
      // This describes what terminalNode did *inside* the flow.

      const expected: ExecutionTree = {
        order: terminalNode.__nodeOrder, // 0
        type: 'TestNode',
        triggered: null, // terminalNode itself triggers default, leads to no successors for it
      }
      assert.deepStrictEqual(result, expected)
    })

    it('should return correct structure for branching flow', async () => {
      // This test uses branchingNodeInstance (order 4), nodeB (order 1),
      // nodeC (order 2), and nodeD (order 3) from the main beforeEach.
      // We are NOT resetting (BaseNode as any).__nextId here, to align with the
      // node orders (like order: 4) observed in your error message for branchingNodeInstance.

      // 1. Setup successors for the 'branchingNodeInstance' FOR THIS TEST
      branchingNodeInstance.on('path_B' as any, nodeB)
      branchingNodeInstance.on('path_C' as any, nodeC)
      nodeB.next(nodeD) // nodeB (successor of path_B) itself has a successor

      // Test path B
      branchingNodeInstance.setTrigger('path_B' as any, null, true) // clearPrevious = true for safety
      let flowB_exec = new Flow(branchingNodeInstance)
      let resultB = (await flowB_exec.run(createMemory({}))) as ExecutionTree

      const expectedB: ExecutionTree = {
        order: branchingNodeInstance.__nodeOrder, // Should be 4
        type: 'BranchingNode',
        triggered: {
          path_B: [
            {
              order: nodeB.__nodeOrder, // Should be 1
              type: 'TestNode',
              triggered: {
                [DEFAULT_ACTION]: [
                  {
                    order: nodeD.__nodeOrder, // Should be 3
                    type: 'TestNode',
                    triggered: null, // nodeD is terminal
                  },
                ],
              },
            },
          ],
        },
      }
      assert.deepStrictEqual(resultB, expectedB)

      // Reset mocks for the global nodes before testing the next path
      nodeB.resetMocks()
      nodeC.resetMocks()
      nodeD.resetMocks()
      branchingNodeInstance.resetMocks() // Also reset the branching node's mocks

      // Test path C using the SAME branchingNodeInstance (order 4)
      // Its successors were set at the beginning of this 'it' block and are still valid.
      branchingNodeInstance.setTrigger('path_C' as any, null, true) // clearPrevious = true

      let flowC_exec = new Flow(branchingNodeInstance)
      let resultC = (await flowC_exec.run(createMemory({}))) as ExecutionTree

      // 2. Corrected expectation for the terminal nodeC
      const expectedC_corrected: ExecutionTree = {
        order: branchingNodeInstance.__nodeOrder, // Should be 4
        type: 'BranchingNode',
        triggered: {
          path_C: [
            // Expecting array because 'path_C' leads to nodeC
            {
              order: nodeC.__nodeOrder, // Should be 2
              type: 'TestNode',
              triggered: null, // nodeC is terminal
            },
          ],
        },
      }
      assert.deepStrictEqual(resultC, expectedC_corrected)
    })

    it('should return correct structure for multi-trigger (fan-out)', async () => {
      ;(BaseNode as any).__nextId = 0
      class MultiTriggerNode extends TestNode<SharedStore, ['out1', 'out2']> {
        constructor(id: string) {
          super(id)
        }
        async post(mem: Memory, prepRes: any, execRes: any) {
          await super.post(mem, prepRes, execRes)
          this.trigger('out1', { data: 'for_out1' })
          this.trigger('out2', { data: 'for_out2' })
        }
      }
      const multiNode = new MultiTriggerNode('Multi') //0
      const mt_nodeB = new TestNode('mtB') //1
      const mt_nodeC = new TestNode('mtC') //2

      multiNode.on('out1', mt_nodeB)
      multiNode.on('out2', mt_nodeC)

      const flow = new Flow(multiNode) //3
      const result = (await flow.run(createMemory({}))) as ExecutionTree

      const expected: ExecutionTree = {
        order: multiNode.__nodeOrder, //0
        type: 'MultiTriggerNode',
        triggered: {
          out1: [{ order: mt_nodeB.__nodeOrder, type: 'TestNode', triggered: null }], //1
          out2: [{ order: mt_nodeC.__nodeOrder, type: 'TestNode', triggered: null }], //2
        },
      }
      assert.deepStrictEqual(result, expected)
    })
  })

  describe('ParallelFlow', () => {
    it('should execute parallel branches concurrently', async () => {
      ;(BaseNode as any).__nextId = 0
      const parallelStartNode = new BranchingNode('PStart') //0
      const nodeP1 = new TestNode('P1') //1
      const nodeP2 = new TestNode('P2') //2

      let p1DoneTime = 0,
        p2DoneTime = 0

      nodeP1.execMock.mock.mockImplementation(async () => {
        await new Promise((resolve) => setTimeout(resolve, 50))
        p1DoneTime = Date.now()
        return 'exec_P1'
      })
      nodeP2.execMock.mock.mockImplementation(async () => {
        await new Promise((resolve) => setTimeout(resolve, 10))
        p2DoneTime = Date.now()
        return 'exec_P2'
      })

      parallelStartNode.on('branch1', nodeP1)
      parallelStartNode.on('branch2', nodeP2)
      // BranchingNode's post needs to trigger both.
      // We use setTrigger with clearPrevious=true to ensure only these two are set.
      parallelStartNode.post = async function (this: BranchingNode, memory, prepRes, execRes) {
        await TestNode.prototype.post.call(this, memory, prepRes, execRes) // Call original TestNode post for flags
        this.triggers = [] // Clear any default triggers from super.post
        this.trigger('branch1' as any, { data: 'for_p1' })
        this.trigger('branch2' as any, { data: 'for_p2' })
      }

      const flow = new ParallelFlow(parallelStartNode) //3
      await flow.run(createMemory({}))

      assert.ok(p1DoneTime > 0, 'P1 should have completed')
      assert.ok(p2DoneTime > 0, 'P2 should have completed')
      assert.ok(
        p2DoneTime < p1DoneTime,
        `P2 (ended at ${p2DoneTime}) should finish before P1 (ended at ${p1DoneTime}) if truly parallel. Diff: ${p1DoneTime - p2DoneTime}`,
      )
      assert.equal(nodeP1.execMock.mock.calls.length, 1, 'P1 exec')
      assert.equal(nodeP2.execMock.mock.calls.length, 1, 'P2 exec')
    })
  })

  describe('Action Propagation from Flow (when Flow.run called with propagate=true)', () => {
    let currentMemory: Memory

    beforeEach(() => {
      currentMemory = createMemory({ test_case_prop: 'action_prop' })
    })

    it('Flow with silently terminating sub-node: propagates its own implicit DEFAULT_ACTION', async () => {
      ;(BaseNode as any).__nextId = 0
      const silentSubNode = new TestNode('SilentSub') // 0
      // silentSubNode.postMock does nothing, so it won't call this.trigger()

      const flow = new Flow(silentSubNode) // 1
      const propagatedTriggers = await flow.run(currentMemory, true)

      assert.strictEqual(propagatedTriggers.length, 1, 'Flow should propagate one action')
      assert.strictEqual(propagatedTriggers[0][0], DEFAULT_ACTION, 'Flow should propagate DEFAULT_ACTION')
      assert.ok(propagatedTriggers[0][1]._isMemoryObject, 'Propagated action should include memory')
      // Check that flow.triggers (internal list) was NOT populated by the sub-node's implicit default
      assert.strictEqual(flow.triggers.length, 0, "Flow's internal triggers should be empty")
    })

    it('Flow with sub-node explicitly triggering DEFAULT_ACTION (terminal in flow): propagates DEFAULT_ACTION', async () => {
      ;(BaseNode as any).__nextId = 0
      const explicitDefaultSubNode = new BranchingNode('ExplicitDefaultSub') // 0
      explicitDefaultSubNode.setTrigger(DEFAULT_ACTION, null, true) // clearPrevious=true

      const flow = new Flow(explicitDefaultSubNode) // 1
      const propagatedTriggers = await flow.run(currentMemory, true)

      assert.strictEqual(propagatedTriggers.length, 1)
      assert.strictEqual(propagatedTriggers[0][0], DEFAULT_ACTION)
      // Check that flow.triggers (internal list) WAS populated
      assert.strictEqual(flow.triggers.length, 1, "Flow's internal triggers should contain the explicit default")
      assert.strictEqual(flow.triggers[0].action, DEFAULT_ACTION)
    })

    it('Flow with sub-node explicitly triggering CUSTOM_ACTION (terminal in flow): propagates CUSTOM_ACTION', async () => {
      ;(BaseNode as any).__nextId = 0
      const explicitCustomSubNode = new BranchingNode('ExplicitCustomSub') // 0
      explicitCustomSubNode.setTrigger('MY_CUSTOM' as any, { customData: true }, true)

      const flow = new Flow(explicitCustomSubNode) // 1
      const propagatedTriggers = await flow.run(currentMemory, true)

      assert.strictEqual(propagatedTriggers.length, 1)
      assert.strictEqual(propagatedTriggers[0][0], 'MY_CUSTOM')
      assert.deepStrictEqual(propagatedTriggers[0][1].local.customData, true)
      assert.strictEqual(flow.triggers.length, 1)
      assert.strictEqual(flow.triggers[0].action, 'MY_CUSTOM')
    })

    it('Nested Flow: Outer propagates its own implicit DEFAULT if sub-flow terminates silently', async () => {
      ;(BaseNode as any).__nextId = 0
      const silentInNested = new TestNode('SilentInNested') // 0
      const subFlow = new Flow(silentInNested) // 1 (subFlow itself)
      // subFlow.post is default, so it will trigger its own DEFAULT_ACTION if its internal .triggers is empty

      const outerA = new TestNode('OuterA') // 2
      outerA.next(subFlow as BaseNode) // OuterA -> subFlow (subFlow is terminal for OuterA's path)

      const outerFlow = new Flow(outerA) // 3
      const propagatedTriggers = await outerFlow.run(currentMemory, true)

      // outerA runs, triggers DEFAULT_ACTION, leading to subFlow.
      // subFlow runs. Its internal node silentInNested is silent.
      // So, subFlow.runNode for silentInNested does NOT push to subFlow.triggers.
      // subFlow.triggers remains empty.
      // When subFlow.run(..., true) is called by outerFlow, subFlow.listTriggers() returns [[DEFAULT_ACTION, ...]] (subFlow's own implicit default).
      //
      // Now, outerFlow.runNode for subFlow:
      //   `action` is DEFAULT_ACTION (from subFlow's propagation).
      //   `clonedNode` is subFlow. `clonedNode.triggers` (subFlow's own explicit triggers) is empty.
      //   So, `isImplicitDefaultAction` is true.
      //   `outerFlow.triggers.push` is SKIPPED.
      //
      // outerFlow.triggers remains empty.
      // outerFlow.listTriggers() (called by outerFlow.run(..., true)) returns [[DEFAULT_ACTION, ...]] (outerFlow's own implicit default).
      assert.strictEqual(propagatedTriggers.length, 1, 'OuterFlow should propagate one action')
      assert.strictEqual(propagatedTriggers[0][0], DEFAULT_ACTION, 'OuterFlow should propagate DEFAULT_ACTION')
      assert.strictEqual(outerFlow.triggers.length, 0, "OuterFlow's internal triggers should be empty")
    })

    it('Nested Flow: Outer propagates explicit DEFAULT_ACTION from sub-flow', async () => {
      ;(BaseNode as any).__nextId = 0
      const explicitDefaultInNested = new BranchingNode('ExplicitDefaultInNested') // 0
      explicitDefaultInNested.setTrigger(DEFAULT_ACTION, null, true)
      const subFlow = new Flow(explicitDefaultInNested) // 1
      // subFlow.post is default. explicitDefaultInNested makes subFlow.triggers contain DEFAULT_ACTION.
      // So subFlow.listTriggers() will return [[DEFAULT_ACTION, ...]] based on its content.

      const outerA = new TestNode('OuterA') // 2
      outerA.next(subFlow as BaseNode)
      const outerFlow = new Flow(outerA) // 3
      const propagatedTriggers = await outerFlow.run(currentMemory, true)

      // outerFlow.runNode for subFlow:
      //   `action` is DEFAULT_ACTION (from subFlow's propagation).
      //   `clonedNode` is subFlow. `clonedNode.triggers` (subFlow's own explicit triggers) is NOT empty.
      //   So, `isImplicitDefaultAction` is false.
      //   `outerFlow.triggers.push({ action: DEFAULT_ACTION, ... })` IS called.
      //
      // outerFlow.triggers contains DEFAULT_ACTION.
      // outerFlow.listTriggers() returns [[DEFAULT_ACTION, ...]].
      assert.strictEqual(propagatedTriggers.length, 1)
      assert.strictEqual(propagatedTriggers[0][0], DEFAULT_ACTION)
      assert.strictEqual(outerFlow.triggers.length, 1, "OuterFlow's internal triggers should contain DEFAULT_ACTION")
      assert.strictEqual(outerFlow.triggers[0].action, DEFAULT_ACTION)
    })

    it('Nested Flow: Outer propagates explicit CUSTOM_ACTION from sub-flow', async () => {
      ;(BaseNode as any).__nextId = 0
      const explicitCustomInNested = new BranchingNode('ExplicitCustomInNested') // 0
      explicitCustomInNested.setTrigger('NESTED_CUSTOM' as any, { val: 123 }, true)
      const subFlow = new Flow(explicitCustomInNested) // 1

      const outerA = new TestNode('OuterA') // 2
      outerA.next(subFlow as BaseNode)
      const outerFlow = new Flow(outerA) // 3
      const propagatedTriggers = await outerFlow.run(currentMemory, true)

      assert.strictEqual(propagatedTriggers.length, 1)
      assert.strictEqual(propagatedTriggers[0][0], 'NESTED_CUSTOM')
      assert.deepStrictEqual(propagatedTriggers[0][1].local.val, 123)
      assert.strictEqual(outerFlow.triggers.length, 1)
      assert.strictEqual(outerFlow.triggers[0].action, 'NESTED_CUSTOM')
    })
  })
})
