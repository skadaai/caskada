import pytest
import asyncio
import time
from unittest.mock import AsyncMock
# Assuming brainyflow classes are in a module named 'brainyflow'
from brainyflow import Memory, Node, Flow, ParallelFlow, DEFAULT_ACTION, BaseNode

# --- Helper Node Implementations ---

class DelayedNode(Node):
    """
    Node with configurable delays.
    FIXED: Writes results to the shared GLOBAL memory for post-run inspection.
    """
    def __init__(self, id_str: str):
        super().__init__()
        self.id = id_str
        self.exec_mock = AsyncMock()
        self.next_forking_data = {}

    async def prep(self, memory: Memory) -> dict:
        """Gets branch_id and delay, saving the start time to GLOBAL memory."""
        branch_id = getattr(memory.local, 'id', 'main')
        delay = getattr(memory.local, 'delay', 0)
        # FIX: Write to the global store for post-run analysis
        memory[f"start_time_{self.id}_{branch_id}"] = time.time()
        return {"delay": delay}

    async def exec(self, prep_res: dict):
        """Sleeps for the delay amount received from the prep phase."""
        delay = prep_res.get("delay", 0)
        await asyncio.sleep(delay)
        await self.exec_mock()
        return f"exec_{self.id}_slept_{delay}"

    async def post(self, memory: Memory, prep_res, exec_res):
        """Records end time and results to GLOBAL memory and triggers next node."""
        branch_id = getattr(memory.local, 'id', 'main')
        # FIX: Write to the global store for post-run analysis
        memory[f"end_time_{self.id}_{branch_id}"] = time.time()
        memory[f"result_{self.id}_{branch_id}"] = exec_res
        
        forking_data = self.next_forking_data.copy()
        forking_data["id"] = branch_id
        self.trigger(DEFAULT_ACTION, forking_data)

class MultiTriggerNode(Node):
    """Node that triggers multiple branches."""
    def __init__(self):
        super().__init__()
        self.triggers_to_fire = []

    def add_trigger(self, action, fork_data):
        self.triggers_to_fire.append({"action": action, "fork_data": fork_data})

    async def post(self, memory, prep_res, exec_res):
        for t in self.triggers_to_fire:
            self.trigger(t["action"], t["fork_data"])

class FailingNode(Node):
    """A node designed to fail during execution."""
    def __init__(self, message="Execution failed"):
        super().__init__()
        self.error_message = message

    async def exec(self, prep_res):
        await asyncio.sleep(0.01)
        raise ValueError(self.error_message)

# --- Test Suite ---

class TestParallelFlow:
    """Tests for the ParallelFlow class, focusing on concurrency."""

    @pytest.fixture
    def setup(self):
        """Create test nodes and a new memory instance for each test."""
        BaseNode._next_id = 0
        memory_instance = Memory({"initial": "global"})
        return {
            "memory": memory_instance,
            "trigger_node": MultiTriggerNode(),
            "node_b": DelayedNode("B"),
            "node_c": DelayedNode("C"),
            "node_d": DelayedNode("D"),
        }

    @pytest.mark.asyncio
    async def test_branches_execute_concurrently_with_overlap(self, setup):
        """Verifies concurrent execution via overlapping time windows."""
        delay_b, delay_c = 0.05, 0.06
        trigger_node, node_b, node_c, memory = setup["trigger_node"], setup["node_b"], setup["node_c"], setup["memory"]

        trigger_node.add_trigger("process_b", {"id": "branch_b", "delay": delay_b})
        trigger_node.add_trigger("process_c", {"id": "branch_c", "delay": delay_c})
        trigger_node.on("process_b", node_b)
        trigger_node.on("process_c", node_c)

        parallel_flow = ParallelFlow(trigger_node)
        await parallel_flow.run(memory)

        # FIX: Read from the main memory object, which accesses the global store.
        start_b = memory["start_time_B_branch_b"]
        end_b = memory["end_time_B_branch_b"]
        start_c = memory["start_time_C_branch_c"]
        end_c = memory["end_time_C_branch_c"]
        
        assert start_c < end_b and start_b < end_c, "Execution windows should overlap"
        assert memory["result_B_branch_b"] == f"exec_B_slept_{delay_b}"

    @pytest.mark.asyncio
    async def test_mixed_parallel_and_sequential_execution(self, setup):
        """Verifies a fan-out, fan-in pattern."""
        delay_b, delay_c, delay_d = 0.05, 0.06, 0.03
        trigger_node, node_b, node_c, node_d, memory = setup["trigger_node"], setup["node_b"], setup["node_c"], setup["node_d"], setup["memory"]

        trigger_node.add_trigger("path_b", {"id": "branch_b", "delay": delay_b})
        trigger_node.add_trigger("path_c", {"id": "branch_c", "delay": delay_c})
        trigger_node.on("path_b", node_b)
        trigger_node.on("path_c", node_c)
        
        node_b.next(node_d)
        node_c.next(node_d)
        
        node_b.next_forking_data = {"delay": delay_d}
        node_c.next_forking_data = {"delay": delay_d}
        
        parallel_flow = ParallelFlow(trigger_node)
        await parallel_flow.run(memory)

        assert node_d.exec_mock.call_count == 2
        
        # FIX: Read from the main memory object.
        start_d_from_b = memory["start_time_D_branch_b"]
        end_d_from_b = memory["end_time_D_branch_b"]
        start_d_from_c = memory["start_time_D_branch_c"]
        end_d_from_c = memory["end_time_D_branch_c"]

        assert start_d_from_b < end_d_from_c and start_d_from_c < end_d_from_b

    @pytest.mark.asyncio
    async def test_mixed_parallel_and_sequential_execution2(self, setup):
        """
        Verifies a fan-out, fan-in pattern with asymmetric delays
        to prove non-blocking behavior.
        """
        # B is very fast, C is slow. D is fast.
        delay_b, delay_c, delay_d = 0.01, 0.2, 0.03
        # ... (rest of the setup is identical) ...
        trigger_node, node_b, node_c, node_d, memory = setup["trigger_node"], setup["node_b"], setup["node_c"], setup["node_d"], setup["memory"]

        trigger_node.add_trigger("path_b", {"id": "branch_b", "delay": delay_b})
        trigger_node.add_trigger("path_c", {"id": "branch_c", "delay": delay_c})
        trigger_node.on("path_b", node_b)
        trigger_node.on("path_c", node_c)
        
        node_b.next(node_d)
        node_c.next(node_d)
        
        node_b.next_forking_data = {"delay": delay_d}
        node_c.next_forking_data = {"delay": delay_d}
        
        await ParallelFlow(trigger_node).run(memory)

        # Timestamps from global memory
        end_time_c = memory["end_time_C_branch_c"]
        start_time_d_from_b = memory["start_time_D_branch_b"]

        # *** THE KEY ASSERTION ***
        # This proves that Node D on the fast path started BEFORE the slow
        # parallel branch (Node C) was finished. This is definitive proof
        # that the slow branch did not block the fast one.
        assert start_time_d_from_b < end_time_c

    @pytest.mark.asyncio
    async def test_exception_in_one_branch_propagates(self, setup):
        """Verifies that an exception in one branch is properly raised."""
        trigger_node, node_b, memory = setup["trigger_node"], setup["node_b"], setup["memory"]
        failing_node = FailingNode("Branch C failed!")
        
        trigger_node.add_trigger("good_path", {"id": "branch_b", "delay": 0.02})
        trigger_node.add_trigger("bad_path", {"id": "branch_c"})
        trigger_node.on("good_path", node_b)
        trigger_node.on("bad_path", failing_node)
        
        parallel_flow = ParallelFlow(trigger_node)
        
        with pytest.raises(ValueError, match="Branch C failed!"):
            await parallel_flow.run(memory)

        # Allow time for other tasks to potentially complete before checking mocks
        await asyncio.sleep(0.03) 
        assert node_b.exec_mock.call_count == 1

# (Add this new test method to the TestParallelFlow class in your test file)

    @pytest.mark.asyncio
    async def test_flow_vs_parallel_flow_timing(self, setup):
        """
        Directly compares the execution time of a sequential Flow vs. a ParallelFlow
        for the same graph, proving the concurrency benefit.
        """
        delay_b, delay_c = 0.05, 0.06
        trigger_node = setup["trigger_node"]
        node_b = DelayedNode("B-comp") # Use different ID to not collide
        node_c = DelayedNode("C-comp")
        memory = setup["memory"]

        # 1. Define the graph
        trigger_node.add_trigger("process_b", {"id": "b", "delay": delay_b})
        trigger_node.add_trigger("process_c", {"id": "c", "delay": delay_c})
        (trigger_node
            .on("process_b", node_b))
        (trigger_node
            .on("process_c", node_c))

        # 2. Run sequentially with Flow
        sequential_flow = Flow(trigger_node.clone()) # Use a clone to keep it clean
        start_seq = time.time()
        await sequential_flow.run(memory)
        duration_seq = time.time() - start_seq

        # 3. Run concurrently with ParallelFlow
        parallel_flow = ParallelFlow(trigger_node.clone())
        start_par = time.time()
        await parallel_flow.run(memory)
        duration_par = time.time() - start_par

        # 4. Assert the timing difference
        # The sequential flow should take the sum of delays
        assert duration_seq == pytest.approx(delay_b + delay_c, abs=0.05)
        # The parallel flow should take the time of the longest delay
        assert duration_par == pytest.approx(max(delay_b, delay_c), abs=0.05)
        # The parallel flow must be faster than the sequential one
        assert duration_par < duration_seq