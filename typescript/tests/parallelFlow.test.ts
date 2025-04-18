import assert from 'node:assert/strict'
import { beforeEach, describe, it, mock } from 'node:test'
import { DEFAULT_ACTION, Memory, Node, ParallelFlow } from '../brainyflow'

// Helper sleep function
const sleep = (ms: number) => new Promise((resolve) => setTimeout(resolve, ms))

// --- Helper Nodes ---
class DelayedNode extends Node<any, { delay?: number; id: string }> {
  id: string
  prepMock = mock.fn(async (memory: Memory<any, any>) => {}) // Add prepMock
  execMock = mock.fn(async (prepRes: any) => {})

  constructor(id: string) {
    super()
    this.id = id
  }

  async prep(memory: Memory<any, { delay?: number; id: string }>): Promise<{ delay: number }> {
    // Read delay from local memory (passed via forkingData)
    const delay = memory.delay ?? 0
    memory[`prep_start_${this.id}_${memory.id ?? 'main'}`] = Date.now()
    return { delay }
  }

  async exec(prepRes: { delay: number }): Promise<string> {
    await sleep(prepRes.delay)
    await this.execMock(prepRes)
    return `exec_${this.id}_slept_${prepRes.delay}`
  }

  async post(memory: Memory<any, any>, prepRes: any, execRes: any): Promise<void> {
    memory[`post_${this.id}_${memory.id ?? 'main'}`] = execRes
    memory[`prep_end_${this.id}_${memory.id ?? 'main'}`] = Date.now()
  }
}

class MultiTriggerNode extends Node {
  triggersToFire: { action: string; forkData: Record<string, any> }[] = []

  addTrigger(action: string, forkData: Record<string, any>) {
    this.triggersToFire.push({ action, forkData })
  }

  async post(memory: Memory<any, any>): Promise<void> {
    memory.trigger_node_post_time = Date.now()
    for (const t of this.triggersToFire) {
      this.trigger(t.action, t.forkData)
    }
  }
}

describe('ParallelFlow Class', () => {
  let memory: Memory<any, any>
  let globalStore: Record<string, any>
  let triggerNode: MultiTriggerNode
  let nodeB: DelayedNode
  let nodeC: DelayedNode
  let nodeD: DelayedNode // Another node for sequential part

  beforeEach(() => {
    globalStore = { initial: 'global' }
    memory = Memory.create(globalStore)
    triggerNode = new MultiTriggerNode()
    nodeB = new DelayedNode('B')
    nodeC = new DelayedNode('C')
    nodeD = new DelayedNode('D') // For testing sequential after parallel
    mock.reset() // Reset all mocks
  })

  it('should execute triggered branches concurrently using runTasks override', async () => {
    const delayB = 50
    const delayC = 60

    // Setup: TriggerNode fans out to B and C with different delays
    triggerNode.addTrigger('process', { id: 'B', delay: delayB })
    triggerNode.addTrigger('process', { id: 'C', delay: delayC })
    triggerNode.on('process', nodeB) // Both triggers use the same action name
    triggerNode.on('process', nodeC) // But different nodes handle them here for clarity
    // Note: In a real scenario, you might have one ProcessorNode type
    // and differentiate behavior based on forkingData.
    // Here we use separate nodes B and C for easier tracking.

    const parallelFlow = new ParallelFlow(triggerNode)

    const startTime = Date.now()
    const result = await parallelFlow.run(memory)
    const endTime = Date.now()
    const duration = endTime - startTime

    // --- Assertions ---

    // 1. Check total duration: Should be closer to max(delayB, delayC) than sum(delayB, delayC)
    const maxDelay = Math.max(delayB, delayC)
    const sumDelay = delayB + delayC
    console.log(
      `Execution Time: ${duration}ms (Max Delay: ${maxDelay}ms, Sum Delay: ${sumDelay}ms)`,
    )
    assert.ok(
      duration < sumDelay - 10,
      `Duration (${duration}ms) should be significantly less than sum (${sumDelay}ms)`,
    )
    assert.ok(
      duration >= maxDelay - 5 && duration < maxDelay + 50, // Allow buffer for overhead
      `Duration (${duration}ms) should be close to max delay (${maxDelay}ms)`,
    )

    // 2. Check if both nodes executed (via post-execution memory state)
    assert.equal(memory.post_B_B, `exec_B_slept_${delayB}`)
    assert.equal(memory.post_C_C, `exec_C_slept_${delayC}`)

    // 3. Check the aggregated result structure (order might vary)
    assert.ok(result && typeof result === 'object', 'Result should be an object')
    assert.ok('process' in result, "Result should contain 'process' key")
    const processResults = result.process
    assert.ok(
      Array.isArray(processResults) && processResults.length === 2,
      "'process' should be an array with 2 results",
    )

    // Check that both branches completed (results are empty objects as DelayedNode has no successors)
    assert.deepStrictEqual(processResults[0], { [DEFAULT_ACTION]: [] })
    assert.deepStrictEqual(processResults[1], { [DEFAULT_ACTION]: [] })

    // 4. Check mock calls (optional, less reliable for timing)
    assert.equal(nodeB.execMock.mock.calls.length, 1)
    assert.equal(nodeC.execMock.mock.calls.length, 1)
  })

  it('should handle mix of parallel and sequential execution', async () => {
    // A (MultiTrigger) -> [B (delay 50), C (delay 60)] -> D (delay 30)
    const delayB = 50
    const delayC = 60
    const delayD = 30

    triggerNode.addTrigger('parallel_step', { id: 'B', delay: delayB })
    triggerNode.addTrigger('parallel_step', { id: 'C', delay: delayC })

    // Both parallel branches lead to D
    triggerNode.on('parallel_step', nodeB)
    triggerNode.on('parallel_step', nodeC)
    nodeB.next(nodeD, 'default') // B -> D
    nodeC.next(nodeD, 'default') // C -> D

    // Add delay to D
    nodeD.prepMock.mock.mockImplementation(async (mem: Memory<any, any>) => {
      // Type mem
      mem.delay = delayD // Set delay for D dynamically if needed, or pass via forkData
    })

    const parallelFlow = new ParallelFlow(triggerNode)
    const startTime = Date.now()
    await parallelFlow.run(memory)
    const endTime = Date.now()
    const duration = endTime - startTime

    const expectedMinDuration = Math.max(delayB, delayC) + delayD
    console.log(`Mixed Execution Time: ${duration}ms (Expected Min: ~${expectedMinDuration}ms)`)

    // Check completion
    assert.equal(memory.post_B_B, `exec_B_slept_${delayB}`)
    assert.equal(memory.post_C_C, `exec_C_slept_${delayC}`)
    assert.equal(memory.post_D_B, `exec_D_slept_${delayD}`) // D executed after B
    assert.equal(memory.post_D_C, `exec_D_slept_${delayD}`) // D executed after C

    // Check timing: D should start only after its respective predecessor (B or C) finishes.
    // The whole flow should take roughly max(delayB, delayC) + delayD
    assert.ok(
      duration >= expectedMinDuration - 10,
      `Duration (${duration}ms) should be >= expected min (${expectedMinDuration}ms)`,
    )
    assert.ok(
      duration < expectedMinDuration + 100, // Allow generous buffer for overhead
      `Duration (${duration}ms) should be reasonably close to expected min (${expectedMinDuration}ms)`,
    )

    // Check D was executed twice (once for each incoming path)
    assert.equal(nodeD.execMock.mock.calls.length, 2)
  })
})
