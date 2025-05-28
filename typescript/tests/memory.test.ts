import assert from 'node:assert/strict'
import { beforeEach, describe, it } from 'node:test'

import { createMemory, Memory, SharedStore } from '../brainyflow'

describe('Memory Factory Function (`createMemory`)', () => {
  describe('Initialization', () => {
    it('should initialize with global store only', () => {
      const global = { g1: 'global1' }
      const memory = createMemory(global)

      assert.strictEqual(memory.g1, 'global1', 'Should access global property')
      // Accessing memory.local should return the local store proxy
      assert.deepStrictEqual(memory.local, {}, 'Local store should be an empty object via proxy')
      // To check the internal structure if possible (though it's an implementation detail)
      // This might not be directly testable if local is fully encapsulated by the proxy.
      // The key is that operations on memory.local affect only the local scope.
    })

    it('should initialize with global and local stores', () => {
      const global = { g1: 'global1', common: 'global_common' }
      const local = { l1: 'local1', common: 'local_common' }
      const memory = createMemory(global, local)

      assert.strictEqual(memory.g1, 'global1', 'Should access global property')
      assert.strictEqual(memory.l1, 'local1', 'Should access local property')
      assert.strictEqual(memory.common, 'local_common', 'Local should shadow global')

      // Test memory.local proxy
      assert.strictEqual(memory.local.l1, 'local1', 'memory.local.l1 should access local property')
      assert.strictEqual(memory.local.common, 'local_common', 'memory.local.common should access local property')
      assert.strictEqual(memory.local.g1, undefined, 'memory.local.g1 should be undefined')

      // Check the content of the local store via the .local accessor
      const expectedLocalStore = { l1: 'local1', common: 'local_common' }
      // We can iterate over keys if direct deepStrictEqual on proxy is tricky
      for (const key in expectedLocalStore) {
        assert.strictEqual(memory.local[key], expectedLocalStore[key], `Local store key ${key} mismatch`)
      }
      for (const key in memory.local) {
        assert.ok(key in expectedLocalStore, `Unexpected key ${key} in local store`)
      }
    })
  })

  describe('Proxy Behavior (Reading)', () => {
    const global = { g1: 'global1', common: 'global_common' }
    const local = { l1: 'local1', common: 'local_common' }
    let memory: Memory<typeof global, typeof local>

    beforeEach(() => {
      // Re-create memory before each test in this block to ensure isolation
      memory = createMemory(global, local)
    })

    it('should read from local store first', () => {
      assert.strictEqual(memory.l1, 'local1')
      assert.strictEqual(memory.common, 'local_common')
    })

    it('should fall back to global store if not in local', () => {
      assert.strictEqual(memory.g1, 'global1')
    })

    it('should return undefined if property exists in neither store', () => {
      assert.strictEqual((memory as any).nonExistent, undefined)
    })

    it('should correctly access the local property via memory.local', () => {
      const expectedLocal = {
        l1: 'local1',
        common: 'local_common',
      }
      assert.strictEqual(memory.local.l1, expectedLocal.l1)
      assert.strictEqual(memory.local.common, expectedLocal.common)
      // Ensure no global properties leak into memory.local
      assert.strictEqual(memory.local.g1, undefined)

      // Check all keys for memory.local
      const localKeys = Object.keys(memory.local)
      const expectedLocalKeys = Object.keys(expectedLocal)
      assert.deepStrictEqual(localKeys.sort(), expectedLocalKeys.sort(), "Keys of memory.local do not match")
      expectedLocalKeys.forEach(key => {
        assert.strictEqual(memory.local[key], expectedLocal[key], `Value of memory.local.${key} incorrect`)
      })
    })
  })

  describe('Proxy Behavior (Writing)', () => {
    let global: SharedStore
    let local: SharedStore
    let memory: Memory<SharedStore, SharedStore>

    beforeEach(() => {
      global = { g1: 'global1', common: 'global_common' }
      local = { l1: 'local1', common: 'local_common' }
      memory = createMemory(global, local)
    })

    it('should write property to global store by default, removing from local if present', () => {
      memory.newProp = 'newValue'
      assert.strictEqual(memory.newProp, 'newValue', 'Should read the new property')
      assert.strictEqual(global.newProp, 'newValue', 'Global store should be updated')
      assert.strictEqual(local.newProp, undefined, 'Local store should not be updated')
    })

    it('should overwrite existing global property', () => {
      memory.g1 = 'updated_global1'
      assert.strictEqual(memory.g1, 'updated_global1', 'Should read the updated property')
      assert.strictEqual(global.g1, 'updated_global1', 'Global store should be updated')
    })

    it('should remove property from local store if it exists when writing globally', () => {
      assert.strictEqual(memory.common, 'local_common', 'Should initially read from local')
      memory.common = 'updated_common_globally'
      assert.strictEqual(memory.common, 'updated_common_globally', 'Should read the new global value')
      assert.strictEqual(global.common, 'updated_common_globally', 'Global store should be updated')
      assert.strictEqual(local.common, undefined, 'Property should be removed from local store')
      assert.strictEqual(memory.local.common, undefined, 'Accessing via memory.local should also show removal')
    })

    it('should throw error when attempting to set reserved properties on the main memory proxy', () => {
      // These properties exist on the target object of the main proxy
      assert.throws(() => ((memory as any)._isMemoryObject = {}), /Reserved property '_isMemoryObject' cannot be set/)
      assert.throws(() => ((memory as any).local = {}), /Reserved property 'local' cannot be set/)
      assert.throws(() => ((memory as any).clone = () => ({} as Memory<any, any>)), /Reserved property 'clone' cannot be set/)
    })

    it('should write to local store directly using memory.local', () => {
      memory.local.newLocalProp = 'newLocalValue'
      assert.strictEqual(memory.local.newLocalProp, 'newLocalValue', 'Should read new prop from memory.local')
      assert.strictEqual(local.newLocalProp, 'newLocalValue', 'Internal local store should be updated')
      assert.strictEqual(global.newLocalProp, undefined, 'Global store should not be affected')

      // Verify main memory object reads from local first
      assert.strictEqual(memory.newLocalProp, 'newLocalValue', 'Main memory should read new prop from local')

      // Overwriting existing local property via memory.local
      memory.local.l1 = 'updated_local1'
      assert.strictEqual(memory.local.l1, 'updated_local1')
      assert.strictEqual(local.l1, 'updated_local1')
      assert.strictEqual(memory.l1, 'updated_local1')
    })
  })

  describe('Proxy Behavior (Deleting)', () => {
    let global: SharedStore
    let local: SharedStore
    let memory: Memory<SharedStore, SharedStore>

    beforeEach(() => {
      global = { g1: 'global1', common: 'global_common', only_global: 'val' }
      local = { l1: 'local1', common: 'local_common', only_local: 'val' }
      memory = createMemory(global, local)
    })

    it('should delete from local and global stores via main memory proxy', () => {
      delete memory.common // Exists in both
      assert.strictEqual(memory.common, undefined, 'memory.common should be undefined after delete')
      assert.strictEqual(local.common, undefined, 'local.common should be undefined')
      assert.strictEqual(global.common, undefined, 'global.common should be undefined')

      delete memory.l1 // Exists in local only
      assert.strictEqual(memory.l1, undefined)
      assert.strictEqual(local.l1, undefined)

      delete memory.g1 // Exists in global only
      assert.strictEqual(memory.g1, undefined)
      assert.strictEqual(global.g1, undefined)
    })

    it('should delete from local store only via memory.local proxy', () => {
      delete memory.local.common // Exists in local, shadowed by global
      assert.strictEqual(memory.local.common, undefined, 'memory.local.common should be undefined')
      assert.strictEqual(local.common, undefined, 'local.common should be undefined')
      // Main memory should now read from global
      assert.strictEqual(memory.common, 'global_common', 'memory.common should now fallback to global')

      delete memory.local.only_local
      assert.strictEqual(memory.local.only_local, undefined)
      assert.strictEqual(local.only_local, undefined)
      assert.strictEqual(memory.only_local, undefined)
    })
  })

  describe('Proxy Behavior (Existence Check - `in` operator)', () => {
    let global: SharedStore
    let local: SharedStore
    let memory: Memory<SharedStore, SharedStore>

    beforeEach(() => {
      global = { g1: 'global1', common_g: 'global_common' }
      local = { l1: 'local1', common_l: 'local_common' }
      memory = createMemory(global, local)
    })

    it('should correctly check existence via main memory proxy', () => {
      assert.ok('l1' in memory, 'l1 should be in memory (from local)')
      assert.ok('common_l' in memory, 'common_l should be in memory (from local)')
      assert.ok('g1' in memory, 'g1 should be in memory (from global)')
      assert.ok('common_g' in memory, 'common_g should be in memory (from global)')
      assert.ok(!('non_existent' in memory), 'non_existent should not be in memory')
    })

    it('should correctly check existence via memory.local proxy', () => {
      assert.ok('l1' in memory.local, 'l1 should be in memory.local')
      assert.ok('common_l' in memory.local, 'common_l should be in memory.local')
      assert.ok(!('g1' in memory.local), 'g1 should not be in memory.local')
      assert.ok(!('common_g' in memory.local), 'common_g should not be in memory.local')
      assert.ok(!('non_existent' in memory.local), 'non_existent should not be in memory.local')
    })
  })


  describe('Cloning (`clone()`)', () => {
    let global: SharedStore
    let local: SharedStore
    let memory: Memory<SharedStore, SharedStore>

    beforeEach(() => {
      global = { g1: 'global1', common: 'global_common_original', nestedG: { val: 1 } }
      local = { l1: 'local1', common: 'local_common_original', nestedL: { val: 2 } }
      memory = createMemory(global, local)
    })

    it('should create a new Memory instance with shared global store reference', () => {
      const clonedMemory = memory.clone()
      assert.notStrictEqual(clonedMemory, memory, 'Cloned memory should be a new proxy instance')
      assert.ok((clonedMemory as any)._isMemoryObject, 'Cloned memory should have _isMemoryObject flag')

      // Verify global store reference is shared
      clonedMemory.g1 = 'modified_global_via_clone'
      assert.strictEqual(memory.g1, 'modified_global_via_clone', 'Original should see global changes from clone')
      assert.strictEqual(global.g1, 'modified_global_via_clone', 'Original global object should be changed')

      memory.newGlobal = 'added_to_global_via_original'
      assert.strictEqual(clonedMemory.newGlobal, 'added_to_global_via_original', 'Clone should see new global prop from original')
    })

    it('should create a deep clone of the local store', () => {
      const clonedMemory = memory.clone()

      assert.notStrictEqual(clonedMemory.local, memory.local, 'Local store proxy reference should NOT be shared')
      // The internal local stores should also not be the same reference after structuredClone
      // Modify local via original's local proxy, check clone
      memory.local.l1 = 'modified_local_original'
      assert.strictEqual(clonedMemory.local.l1, 'local1', "Clone's local.l1 property should be unaffected by original local changes")
      assert.strictEqual(clonedMemory.l1, 'local1', "Clone's l1 property (via main proxy) should be unaffected")


      // Modify local via clone's local proxy, check original
      clonedMemory.local.l2 = 'added_via_clone_local'
      assert.strictEqual(memory.local.l2, undefined, 'Original local.l2 should not see local changes from clone')
      assert.strictEqual((memory as any).l2, undefined, 'Original l2 (via main proxy) should not see local changes from clone')


      // Test nested objects in local store
      assert.deepStrictEqual(clonedMemory.local.nestedL, { val: 2 })
      memory.local.nestedL.val = 99
      assert.deepStrictEqual(clonedMemory.local.nestedL, { val: 2 }, 'Nested local object in clone should be unaffected due to deep clone')
      assert.deepStrictEqual(clonedMemory.nestedL, { val: 2 }) // Check via main proxy
    })

    it('should correctly merge forkingData into the new local store (forkingData shadows original local)', () => {
      const forkingData = {
        f1: 'forked1',
        common: 'forked_common', // This should overwrite 'local_common_original'
        nestedF: { val: 3 },
      }
      const clonedMemory = memory.clone(forkingData)

      // Check direct access via main proxy (local first)
      assert.strictEqual(clonedMemory.f1, 'forked1', 'Should access forked property f1')
      assert.strictEqual(clonedMemory.common, 'forked_common', 'Forked data common should shadow original local and global')
      assert.strictEqual(clonedMemory.l1, 'local1', 'Should still access original local property l1')
      assert.strictEqual(clonedMemory.g1, 'global1', 'Should still access global property g1')
      assert.deepStrictEqual(clonedMemory.nestedF, { val: 3 })
      assert.deepStrictEqual(clonedMemory.nestedL, { val: 2 }) // Original local nested

      // Check internal local store state via memory.local proxy
      const expectedLocal = {
        l1: 'local1',             // from original local
        common: 'forked_common',  // from forkingData, overwriting original local's common
        nestedL: { val: 2 },      // from original local
        f1: 'forked1',            // from forkingData
        nestedF: { val: 3 },      // from forkingData
      }
      assert.strictEqual(clonedMemory.local.l1, expectedLocal.l1)
      assert.strictEqual(clonedMemory.local.common, expectedLocal.common)
      assert.deepStrictEqual(clonedMemory.local.nestedL, expectedLocal.nestedL)
      assert.strictEqual(clonedMemory.local.f1, expectedLocal.f1)
      assert.deepStrictEqual(clonedMemory.local.nestedF, expectedLocal.nestedF)

      // Ensure forkingData itself was deep cloned into the new local store
      forkingData.nestedF.val = 99 // Modify original forkingData
      // Check the cloned memory's version (should be unaffected)
      assert.deepStrictEqual(clonedMemory.nestedF, { val: 3 }, 'Nested object in forked data should have been deep cloned (main proxy)')
      assert.deepStrictEqual(clonedMemory.local.nestedF, { val: 3 }, 'Nested object in forked data should have been deep cloned (local proxy)')
    })

    it('should handle empty forkingData object', () => {
      const clonedMemory = memory.clone({}) // Pass an empty object
      assert.deepStrictEqual(clonedMemory.local, local, "Cloned local store should be identical to original when forkingData is empty object")
    })

    it('should handle cloning without forkingData (undefined)', () => {
      const clonedMemory = memory.clone() // No argument
      assert.deepStrictEqual(clonedMemory.local, local, "Cloned local store should be identical to original when no forkingData")
    })
  })
})
