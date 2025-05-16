import pytest
from unittest.mock import Mock, AsyncMock
from brainyflow import Memory, Node, Flow, DEFAULT_ACTION, BaseNode

# --- Helper Node Implementations ---
class BaseTestNode(Node):
    """Basic test node with mocked lifecycle methods."""
    
    def __init__(self, id_str):
        super().__init__()
        self.id = id_str
        self.prep_mock = AsyncMock(return_value=f"prep_{self.id}")
        self.exec_mock = AsyncMock(return_value=f"exec_{self.id}")
        self.post_mock = AsyncMock()
    
    async def prep(self, memory):
        memory[f"prep_{self.id}"] = True
        await self.prep_mock(memory)
        return f"prep_{self.id}"
    
    async def exec(self, prep_res):
        assert prep_res == f"prep_{self.id}"
        return await self.exec_mock(prep_res)
    
    async def post(self, memory, prep_res, exec_res):
        assert prep_res == f"prep_{self.id}"
        assert exec_res == f"exec_{self.id}"
        memory[f"post_{self.id}"] = True
        await self.post_mock(memory, prep_res, exec_res)
        # Default trigger is implicit


class BranchingNode(BaseTestNode):
    """Node that triggers a specific action with optional forking data."""
    
    def __init__(self, id_str):
        super().__init__(id_str)
        self.action = DEFAULT_ACTION
        self.fork_data = None
    
    def set_trigger(self, action, fork_data=None):
        """Configure which action this node will trigger."""
        self.action = action
        self.fork_data = fork_data
    
    async def post(self, memory, prep_res, exec_res):
        await super().post(memory, prep_res, exec_res)  # Call base post
        if self.fork_data is not None:
            self.trigger(self.action, self.fork_data)
        else:
            self.trigger(self.action)


class TestFlow:
    """Tests for the Flow class."""
    
    @pytest.fixture
    def memory(self):
        """Create a test memory instance."""
        global_store = {"initial": "global"}
        return Memory.create(global_store)
    
    @pytest.fixture
    def nodes(self):
        """Create test nodes."""
        return {
            "A": BaseTestNode("A"),
            "B": BaseTestNode("B"),
            "C": BaseTestNode("C"),
            "D": BaseTestNode("D")
        }
    
    class TestInitialization:
        """Tests for Flow initialization."""
        
        def test_store_start_node_and_default_options(self, nodes):
            """Should store the start node and default options."""
            flow = Flow(nodes["A"])
            assert flow.start == nodes["A"]
            assert getattr(flow, "options", {}).get("max_visits") == 5
        
        def test_accept_custom_options(self, nodes):
            """Should accept custom options."""
            flow = Flow(nodes["A"], {"max_visits": 10})
            assert flow.start == nodes["A"]
            assert getattr(flow, "options", {}).get("max_visits") == 10
    
    class TestSequentialExecution:
        """Tests for sequential execution of nodes."""
        
        async def test_execute_nodes_sequentially_following_default_actions(self, nodes, memory):
            """Should execute nodes sequentially following default actions."""
            nodes["A"].next(nodes["B"])
            nodes["B"].next(nodes["C"])  # A -> B -> C
            
            flow = Flow(nodes["A"])
            await flow.run(memory)
            
            # Verify execution order via mocks
            assert nodes["A"].prep_mock.call_count == 1
            assert nodes["A"].exec_mock.call_count == 1
            assert nodes["A"].post_mock.call_count == 1
            assert nodes["B"].prep_mock.call_count == 1
            assert nodes["B"].exec_mock.call_count == 1
            assert nodes["B"].post_mock.call_count == 1
            assert nodes["C"].prep_mock.call_count == 1
            assert nodes["C"].exec_mock.call_count == 1
            assert nodes["C"].post_mock.call_count == 1
            
            # Verify memory changes
            assert memory.prep_A is True
            assert memory.post_A is True
            assert memory.prep_B is True
            assert memory.post_B is True
            assert memory.prep_C is True
            assert memory.post_C is True
        
        async def test_stop_execution_if_node_has_no_successor(self, nodes, memory):
            """Should stop execution if a node has no successor for the triggered action."""
            nodes["A"].next(nodes["B"])  # A -> B (B has no successor)
            
            flow = Flow(nodes["A"])
            await flow.run(memory)
            
            assert nodes["A"].post_mock.call_count == 1
            assert nodes["B"].post_mock.call_count == 1
            assert nodes["C"].prep_mock.call_count == 0  # C should not run
    
    class TestConditionalBranching:
        """Tests for conditional branching."""
        
        async def test_follow_correct_path_based_on_triggered_action(self, nodes, memory):
            """Should follow the correct path based on triggered action."""
            branching_node = BranchingNode("Branch")
            branching_node.on("path_B", nodes["B"])
            branching_node.on("path_C", nodes["C"])
            
            # Test path B
            branching_node.set_trigger("path_B")
            flow_b = Flow(branching_node)
            memory_b = Memory.create({})
            await flow_b.run(memory_b)
            
            assert memory_b.post_Branch is True
            assert memory_b.post_B is True
            assert getattr(memory_b, "post_C", None) is None
            
            # Test path C
            branching_node.set_trigger("path_C")  # Reset trigger
            flow_c = Flow(branching_node)  # New flow to reset visit counts
            memory_c = Memory.create({})
            await flow_c.run(memory_c)
            
            assert memory_c.post_Branch is True
            assert getattr(memory_c, "post_B", None) is None
            assert memory_c.post_C is True
    
    class TestMemoryHandling:
        """Tests for memory handling."""
        
        async def test_propagate_global_memory_changes(self, nodes, memory):
            """Should propagate global memory changes."""
            # Setup mock to modify memory
            # Accept extra args passed by post_mock
            async def modify_memory(mem, prep_res, exec_res):  
                mem.global_A = "set_by_A"
            
            nodes["A"].post_mock.side_effect = modify_memory
            
            # Setup mock to verify memory
            async def verify_memory(mem):
                assert mem.global_A == "set_by_A"
            
            nodes["B"].prep_mock.side_effect = verify_memory
            
            nodes["A"].next(nodes["B"])
            flow = Flow(nodes["A"])
            await flow.run(memory)
            
            assert memory.global_A == "set_by_A"
            assert nodes["B"].prep_mock.call_count == 1  # Ensure B ran
        
        async def test_isolate_local_memory_using_forking_data(self, nodes, memory):
            """Should isolate local memory using forkingData."""
            branching_node = BranchingNode("Branch")
            branching_node.on("path_B", nodes["B"])
            branching_node.on("path_C", nodes["C"])
            
            # Setup mocks to check local memory
            async def check_b_memory(mem):
                assert mem.local_data == "for_B"
                assert mem.common_local == "common"
                assert mem.local["local_data"] == "for_B"
            
            async def check_c_memory(mem):
                assert mem.local_data == "for_C"
                assert mem.common_local == "common"
                assert mem.local["local_data"] == "for_C"
            
            nodes["B"].prep_mock.side_effect = check_b_memory
            nodes["C"].prep_mock.side_effect = check_c_memory
            
            # Trigger B with specific local data
            branching_node.set_trigger("path_B", {"local_data": "for_B", "common_local": "common"})
            flow_b = Flow(branching_node)
            memory_b = Memory.create({"global_val": 1})
            await flow_b.run(memory_b)
            
            assert nodes["B"].prep_mock.call_count == 1
            assert nodes["C"].prep_mock.call_count == 0
            assert getattr(memory_b, "local_data", None) is None  # Forked data shouldn't leak to global
            assert getattr(memory_b, "common_local", None) is None
            
            # Trigger C with different local data
            branching_node.set_trigger("path_C", {"local_data": "for_C", "common_local": "common"})
            flow_c = Flow(branching_node)  # New flow to reset visits
            memory_c = Memory.create({"global_val": 1})
            await flow_c.run(memory_c)
            
            assert nodes["B"].prep_mock.call_count == 1  # Still called once from previous run
            assert nodes["C"].prep_mock.call_count == 1
            assert getattr(memory_c, "local_data", None) is None
            assert getattr(memory_c, "common_local", None) is None
    
    class TestCycleDetection:
        """Tests for cycle detection."""
        
        async def test_execute_loop_maxvisits_times_before_error(self, nodes):
            """Should execute a loop exactly maxVisits times before error."""
            loop_count = [0]  # Using a list for mutable closure
            
            # Setup mock to increment count
            async def increment_count(mem):
                loop_count[0] += 1
                mem.count = loop_count[0]
            
            nodes["A"].prep_mock.side_effect = increment_count
            nodes["A"].next(nodes["A"])  # A -> A loop
            
            max_visits = 3
            flow = Flow(nodes["A"], {"max_visits": max_visits})
            
            # Use a fresh memory for this test
            loop_memory = Memory.create({})
            
            # Should raise exception when max_visits is exceeded
            # Updated regex to match the actual error message format and changed Exception to AssertionError
            with pytest.raises(AssertionError, match=f".*Maximum cycle count \\({max_visits}\\) reached"):
                await flow.run(loop_memory)
            
            # Verify counts
            assert loop_count[0] == max_visits
            assert loop_memory.count == max_visits
        
        async def test_error_immediately_if_loop_exceeds_maxvisits(self, nodes):
            """Should throw error immediately if loop exceeds max_visits (e.g. max_visits=2)."""
            nodes["A"].next(nodes["A"])  # A -> A loop
            
            max_visits = 2
            flow = Flow(nodes["A"], {"max_visits": max_visits})
            
            loop_memory = Memory.create({})
            
            # Updated regex to match the actual error message format and changed Exception to AssertionError
            with pytest.raises(AssertionError, match=f".*Maximum cycle count \\({max_visits}\\) reached"):
                await flow.run(loop_memory)
    
    class TestFlowAsNode:
        """Tests for using a Flow as a Node (nesting)."""
        
        async def test_execute_nested_flow_as_single_node_step(self, nodes, memory):
            """Should execute a nested flow as a single node step."""
            # Sub-flow: B -> C
            nodes["B"].next(nodes["C"])
            sub_flow = Flow(nodes["B"])
            
            # Main flow: A -> subFlow -> D
            nodes["A"].next(sub_flow)
            sub_flow.next(nodes["D"])  # Connect subFlow's exit to D
            
            main_flow = Flow(nodes["A"])
            await main_flow.run(memory)
            
            # Check execution order
            assert nodes["A"].post_mock.call_count == 1
            assert nodes["B"].post_mock.call_count == 1  # B ran inside subFlow
            assert nodes["C"].post_mock.call_count == 1  # C ran inside subFlow
            assert nodes["D"].post_mock.call_count == 1  # D ran after subFlow
            
            # Check memory state
            assert memory.post_A is True
            assert memory.post_B is True
            assert memory.post_C is True
            assert memory.post_D is True
        
        async def test_nested_flow_prep_post_wrap_subflow_execution(self, nodes, memory):
            """Should run nested flow's prep/post methods around sub-flow execution."""
            nodes["B"].next(nodes["C"])
            sub_flow = Flow(nodes["B"])
            
            # Add prep/post to the subFlow 
            sub_flow.prep = AsyncMock()
            sub_flow.post = AsyncMock()
            
            # Setup mock side effects to modify memory
            async def subflow_prep(mem):
                mem.subflow_prep = True
                return None
            
            async def subflow_post(mem, prep_res, exec_res):
                mem.subflow_post = True
                return None
            
            sub_flow.prep.side_effect = subflow_prep
            sub_flow.post.side_effect = subflow_post
            
            nodes["A"].next(sub_flow).next(nodes["D"])
            main_flow = Flow(nodes["A"])
            
            await main_flow.run(memory)
            
            assert memory.subflow_prep is True
            assert memory.post_B is True  # Inner nodes ran
            assert memory.post_C is True
            assert memory.subflow_post is True
            assert memory.post_D is True  # D ran after subflow post
            
            assert sub_flow.prep.call_count == 1
            assert sub_flow.post.call_count == 1
    
    class TestResultAggregation:
        """Tests for result aggregation."""
        
        async def test_return_correct_nested_actions_structure_for_simple_flow(self, nodes, memory):
            """Should return correct structure for a simple flow."""
            nodes["A"].next(nodes["B"])  # A -> B
            
            flow = Flow(nodes["A"])
            result = await flow.run(memory)
            
            expected = {
                # Results from node A triggering default
                DEFAULT_ACTION: [
                    {  # Results from node B triggering default
                        DEFAULT_ACTION: []  # Terminal node
                    }
                ]
            }
            
            assert result == expected
        
        async def test_return_correct_structure_for_branching_flow(self, nodes):
            """Should return correct structure for branching flow."""
            branching_node = BranchingNode("Branch")
            branching_node.on("path_B", nodes["B"])  # Branch -> B on path_B
            branching_node.on("path_C", nodes["C"])  # Branch -> C on path_C
            nodes["B"].next(nodes["D"])  # B -> D
            
            # Trigger path B
            branching_node.set_trigger("path_B")
            flow_b = Flow(branching_node)
            result_b = await flow_b.run(Memory.create({}))
            
            expected_b = {
                "path_B": [
                    {  # Results from Branch triggering path_B
                        DEFAULT_ACTION: [
                            {  # Results from B triggering default
                                DEFAULT_ACTION: []  # Terminal node D
                            }
                        ]
                    }
                ]
            }
            
            assert result_b == expected_b
            
            # Trigger path C
            branching_node.set_trigger("path_C")
            flow_c = Flow(branching_node)  # Reset flow visits
            result_c = await flow_c.run(Memory.create({}))
            
            expected_c = {
                "path_C": [
                    {  # Results from Branch triggering path_C
                        DEFAULT_ACTION: []  # Terminal node C
                    }
                ]
            }
            
            assert result_c == expected_c
        
        async def test_return_correct_structure_for_multi_trigger(self, nodes, memory):
            """Should return correct structure for multi-trigger (fan-out)."""
            class MultiTrigger(BaseTestNode):
                async def post(self, memory, prep_res, exec_res):
                    await super().post(memory, prep_res, exec_res)
                    self.trigger("out1")
                    self.trigger("out2")
            
            multi_node = MultiTrigger("Multi")
            multi_node.on("out1", nodes["B"])  # Multi -> B on out1
            multi_node.on("out2", nodes["C"])  # Multi -> C on out2
            
            flow = Flow(multi_node)
            result = await flow.run(memory)
            
            expected = {
                "out1": [
                    {  # Results from Multi triggering out1
                        DEFAULT_ACTION: []  # Terminal node B
                    }
                ],
                "out2": [
                    {  # Results from Multi triggering out2
                        DEFAULT_ACTION: []  # Terminal node C
                    }
                ]
            }
            
            # Verify structure without being sensitive to key order
            assert set(result.keys()) == {"out1", "out2"}
            assert result["out1"] == expected["out1"]
            assert result["out2"] == expected["out2"]
