import pytest
import asyncio
import time
from unittest.mock import Mock, AsyncMock
from brainyflow import Memory, Node, Flow, ParallelFlow, DEFAULT_ACTION

# Helper sleep function for async tests
async def async_sleep(seconds: float):
    await asyncio.sleep(seconds)

# --- Helper Node Implementations ---
class DelayedNode(Node):
    """Node with configurable execution delays for testing parallel execution."""
    
    def __init__(self, id_str):
        super().__init__()
        self.id = id_str
        self.prep_mock = AsyncMock()
        self.exec_mock = AsyncMock()
        self.next_node_delay = None
    
    async def prep(self, memory):
        # Read delay from local memory (passed via forkingData)
        delay = getattr(memory, 'delay', 0)
        memory[f"prep_start_{self.id}_{getattr(memory, 'id', 'main')}"] = time.time()
        await self.prep_mock(memory)
        return {"delay": delay}
    
    async def exec(self, prep_res):
        delay = prep_res["delay"]
        await async_sleep(delay)
        await self.exec_mock(prep_res)
        return f"exec_{self.id}_slept_{delay}"
    
    async def post(self, memory, prep_res, exec_res):
        memory[f"post_{self.id}_{getattr(memory, 'id', 'main')}"] = exec_res
        memory[f"prep_end_{self.id}_{getattr(memory, 'id', 'main')}"] = time.time()
        
        # Trigger default successor, passing the intended delay for the *next* node if set
        if self.next_node_delay is not None:
            self.trigger(DEFAULT_ACTION, {"delay": self.next_node_delay, "id": getattr(memory, 'id', None)})
        else:
            self.trigger(DEFAULT_ACTION, {"id": getattr(memory, 'id', None)})

class MultiTriggerNode(Node):
    """Node that triggers multiple branches with configurable actions and fork data."""
    
    def __init__(self):
        super().__init__()
        self.triggers_to_fire = []
    
    def add_trigger(self, action, fork_data):
        self.triggers_to_fire.append({"action": action, "fork_data": fork_data})
    
    async def post(self, memory, prep_res, exec_res):
        memory.trigger_node_post_time = time.time()
        for t in self.triggers_to_fire:
            self.trigger(t["action"], t["fork_data"])

class TestParallelFlow:
    """Tests for the ParallelFlow class."""
    
    @pytest.fixture
    def setup(self):
        """Create test nodes and memory."""
        global_store = {"initial": "global"}
        memory = Memory.create(global_store)
        trigger_node = MultiTriggerNode()
        node_b = DelayedNode("B")
        node_c = DelayedNode("C")
        node_d = DelayedNode("D")  # For testing sequential after parallel
        
        return {
            "memory": memory, 
            "global_store": global_store,
            "trigger_node": trigger_node,
            "node_b": node_b,
            "node_c": node_c,
            "node_d": node_d
        }
    
    @pytest.mark.asyncio
    async def test_execute_triggered_branches_concurrently(self, setup):
        """Should execute triggered branches concurrently using run_tasks override."""
        delay_b = 0.05  # 50ms
        delay_c = 0.06  # 60ms
        
        # Setup: TriggerNode fans out to B and C with different delays using distinct actions
        setup["trigger_node"].add_trigger("process_b", {"id": "B", "delay": delay_b})
        setup["trigger_node"].add_trigger("process_c", {"id": "C", "delay": delay_c})
        setup["trigger_node"].on("process_b", setup["node_b"])
        setup["trigger_node"].on("process_c", setup["node_c"])
        
        parallel_flow = ParallelFlow(setup["trigger_node"])
        
        start_time = time.time()
        result = await parallel_flow.run(setup["memory"])
        end_time = time.time()
        duration = end_time - start_time
        
        # --- Assertions ---
        
        # 1. Check total duration: Should be closer to max(delay_b, delay_c) than sum(delay_b, delay_c)
        max_delay = max(delay_b, delay_c)
        sum_delay = delay_b + delay_c
        
        print(f"Execution Time: {duration}s (Max Delay: {max_delay}s, Sum Delay: {sum_delay}s)")
        
        # Duration should be significantly less than sum of delays
        assert duration < sum_delay - 0.01, f"Duration ({duration}s) should be significantly less than sum ({sum_delay}s)"
        
        # Duration should be close to the max delay (with some overhead)
        assert max_delay - 0.01 <= duration < max_delay + 0.05, f"Duration ({duration}s) should be close to max delay ({max_delay}s)"
        
        # 2. Check if both nodes executed (via post-execution memory state)
        assert setup["memory"][f"post_B_B"] == f"exec_B_slept_{delay_b}"
        assert setup["memory"][f"post_C_C"] == f"exec_C_slept_{delay_c}"
        
        # 3. Check the aggregated result structure
        assert result and isinstance(result, dict), "Result should be a dictionary"
        assert "process_b" in result, "Result should contain 'process_b' key"
        assert "process_c" in result, "Result should contain 'process_c' key"
        
        process_b_results = result["process_b"]
        process_c_results = result["process_c"]
        
        assert isinstance(process_b_results, list) and len(process_b_results) == 1, "'process_b' should be a list with 1 result"
        assert isinstance(process_c_results, list) and len(process_c_results) == 1, "'process_c' should be a list with 1 result"
        
        # Check that both branches completed
        assert process_b_results[0] == {DEFAULT_ACTION: []}
        assert process_c_results[0] == {DEFAULT_ACTION: []}
        
        # 4. Check total mock calls
        assert setup["node_b"].exec_mock.call_count + setup["node_c"].exec_mock.call_count == 2, "Total exec calls across parallel nodes should be 2"
    
    @pytest.mark.asyncio
    async def test_handle_mix_of_parallel_and_sequential_execution(self, setup):
        """Should handle mix of parallel and sequential execution."""
        # A (MultiTrigger) -> [B (delay 50ms), C (delay 60ms)] -> D (delay 30ms)
        delay_b = 0.05  # 50ms
        delay_c = 0.06  # 60ms
        delay_d = 0.03  # 30ms
        
        # Use distinct actions for parallel steps
        setup["trigger_node"].add_trigger("parallel_b", {"id": "B", "delay": delay_b})
        setup["trigger_node"].add_trigger("parallel_c", {"id": "C", "delay": delay_c})
        
        # Both parallel branches lead to D
        setup["trigger_node"].on("parallel_b", setup["node_b"])
        setup["trigger_node"].on("parallel_c", setup["node_c"])
        
        setup["node_b"].next(setup["node_d"])  # B -> D
        setup["node_c"].next(setup["node_d"])  # C -> D
        
        # Set the delay that nodes B and C should pass to node D
        setup["node_b"].next_node_delay = delay_d
        setup["node_c"].next_node_delay = delay_d
        
        parallel_flow = ParallelFlow(setup["trigger_node"])
        
        start_time = time.time()
        await parallel_flow.run(setup["memory"])
        end_time = time.time()
        duration = end_time - start_time
        
        expected_min_duration = max(delay_b, delay_c) + delay_d
        
        print(f"Mixed Execution Time: {duration}s (Expected Min: ~{expected_min_duration}s)")
        
        # Check completion
        assert setup["memory"][f"post_B_B"] == f"exec_B_slept_{delay_b}"
        assert setup["memory"][f"post_C_C"] == f"exec_C_slept_{delay_c}"
        assert setup["memory"][f"post_D_B"] == f"exec_D_slept_{delay_d}"  # D executed after B
        assert setup["memory"][f"post_D_C"] == f"exec_D_slept_{delay_d}"  # D executed after C
        
        # Check timing: D should start only after its respective predecessor (B or C) finishes.
        # The whole flow should take roughly max(delay_b, delay_c) + delay_d
        assert duration >= expected_min_duration - 0.01, f"Duration ({duration}s) should be >= expected min ({expected_min_duration}s)"
        assert duration < expected_min_duration + 0.1, f"Duration ({duration}s) should be reasonably close to expected min ({expected_min_duration}s)"
        
        # Check D was executed twice (once for each incoming path)
        assert setup["node_d"].exec_mock.call_count == 2
