import pytest
from unittest.mock import AsyncMock, ANY
from caskada import Memory, Node, Flow, ParallelFlow, DEFAULT_ACTION, BaseNode

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
    
    def set_trigger(self, action, fork_data=None, clear_existing_in_post=False): # Added clear_existing
        """Configure which action this node will trigger."""
        self.action = action
        self.fork_data = fork_data
        self._clear_triggers_in_post = clear_existing_in_post
    
    async def post(self, memory, prep_res, exec_res):
        await super().post(memory, prep_res, exec_res)  # Call base post
        if self._clear_triggers_in_post:
            self._triggers = [] # Explicitly clear if flag is set

        if self.fork_data is not None:
            self.trigger(self.action, self.fork_data)
        else:
            self.trigger(self.action)


class TestFlow:
    """Tests for the Flow class."""
    
    @pytest.fixture(autouse=True)
    def reset_node_ids(self):
        """Reset BaseNode._next_id before each test in this class.
                IMPORTANT: Reset BaseNode._next_id to ensure predictable orders for tests.
        This should ideally be handled by a session-scoped or test-scoped fixture
        if node creation order varies significantly across test files or setup.
        For now, we assume it's reset or nodes are created fresh with predictable IDs.
        """
        BaseNode._next_id = 0
        yield # Allow the test to run
        BaseNode._next_id = 0 # Optionally reset after, though pre-test reset is key

    @pytest.fixture
    def memory(self):
        """Create a test memory instance."""
        global_store = {"initial": "global"}
        return Memory(global_store)
    
    @pytest.fixture
    def nodes(self):
        """Create test nodes."""
        # BaseNode._next_id is reset by reset_node_ids fixture
        return {
            "A": BaseTestNode("A"), # Order 0
            "B": BaseTestNode("B"), # Order 1
            "C": BaseTestNode("C"), # Order 2
            "D": BaseTestNode("D")  # Order 3
        }
    
    @pytest.fixture
    def branching_node_fixture(self):
        # BaseNode._next_id is reset by reset_node_ids fixture
        return BranchingNode("Branch") # Order 0 if created first in a test


    class TestInitialization:
        """Tests for Flow initialization."""
        
        def test_store_start_node_and_default_options(self, nodes):
            """Should store the start node and default options."""
            flow = Flow(nodes["A"])
            assert flow.start == nodes["A"]
            assert getattr(flow, "options", {}).get("max_visits") == 15
        
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
            nodes["A"].prep_mock.assert_called_once()
            nodes["B"].prep_mock.assert_called_once()
            nodes["C"].prep_mock.assert_called_once()

            nodes["A"].exec_mock.assert_called_once()
            nodes["B"].exec_mock.assert_called_once()
            nodes["C"].exec_mock.assert_called_once()

            nodes["A"].post_mock.assert_called_once()
            nodes["B"].post_mock.assert_called_once()
            nodes["C"].post_mock.assert_called_once()
            
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
            
            nodes["A"].post_mock.assert_called_once()
            nodes["B"].post_mock.assert_called_once()
            nodes["C"].prep_mock.assert_not_called()
    
    class TestConditionalBranching:
        """Tests for conditional branching."""
        
        async def test_follow_correct_path_based_on_triggered_action(self, nodes, memory):
            """Should follow the correct path based on triggered action."""
            # Reset BaseNode ID for predictable IDs in this test
            BaseNode._next_id = 0
            branching_node = BranchingNode("Branch") # id_Branch = 0
            # nodes A, B, C, D are created by fixture, their IDs will be 0,1,2,3 if nodes fixture is used first
            # If branching_node is created first, its ID will be 0.
            # Let's use fresh nodes for clarity here if IDs matter deeply for the test logic.
            # For this test, memory state check is primary.
            
            node_b_local = BaseTestNode("B_local") # id_B_local = 1
            node_c_local = BaseTestNode("C_local") # id_C_local = 2

            branching_node.on("path_B", node_b_local)
            branching_node.on("path_C", node_c_local)
            
            # Test path B
            branching_node.set_trigger("path_B")
            flow_b = Flow(branching_node)
            memory_b = Memory({})
            await flow_b.run(memory_b)
            
            assert memory_b.post_Branch is True
            assert memory_b.post_B_local is True
            assert getattr(memory_b, "post_C_local", None) is None
            
            # Test path C
            # Re-create branching_node or use a new Flow instance to reset visit counts
            # and ensure post_mock counts are fresh for this path.
            BaseNode._next_id = 0 # Reset again if we want same ID for branching_node
            branching_node_for_c = BranchingNode("Branch") # id = 0
            node_b_for_c = BaseTestNode("B_for_C") # id = 1
            node_c_for_c = BaseTestNode("C_for_C") # id = 2
            branching_node_for_c.on("path_B", node_b_for_c)
            branching_node_for_c.on("path_C", node_c_for_c)

            branching_node_for_c.set_trigger("path_C")
            flow_c = Flow(branching_node_for_c) 
            memory_c = Memory({})
            await flow_c.run(memory_c)
            
            assert memory_c.post_Branch is True
            assert getattr(memory_c, "post_B_for_C", None) is None
            assert memory_c.post_C_for_C is True
    
    class TestMemoryHandling:
        """Tests for memory handling."""
        
        async def test_propagate_global_memory_changes(self, nodes, memory):
            """Should propagate global memory changes."""
            async def modify_memory(mem, prep_res, exec_res):  
                mem.global_A = "set_by_A"
            
            nodes["A"].post_mock.side_effect = modify_memory
            
            async def verify_memory(mem):
                assert mem.global_A == "set_by_A"
            
            nodes["B"].prep_mock.side_effect = verify_memory
            
            nodes["A"].next(nodes["B"])
            flow = Flow(nodes["A"])
            await flow.run(memory)
            
            assert memory.global_A == "set_by_A"
            assert nodes["B"].prep_mock.call_count == 1
        
        async def test_isolate_local_memory_using_forking_data(self, nodes, memory):
            """Should isolate local memory using forkingData."""
            BaseNode._next_id = 0
            branching_node = BranchingNode("Branch") # id 0
            node_b_local = BaseTestNode("B_local")   # id 1
            node_c_local = BaseTestNode("C_local")   # id 2

            branching_node.on("path_B", node_b_local)
            branching_node.on("path_C", node_c_local)
            
            async def check_b_memory(mem):
                assert mem.local_data == "for_B"
                assert mem.common_local == "common"
                assert mem.local["local_data"] == "for_B"
            
            async def check_c_memory(mem):
                assert mem.local_data == "for_C"
                assert mem.common_local == "common"
                assert mem.local["local_data"] == "for_C"
            
            node_b_local.prep_mock.side_effect = check_b_memory
            node_c_local.prep_mock.side_effect = check_c_memory
            
            branching_node.set_trigger("path_B", {"local_data": "for_B", "common_local": "common"})
            flow_b = Flow(branching_node)
            memory_b = Memory({"global_val": 1})
            await flow_b.run(memory_b)
            
            assert node_b_local.prep_mock.call_count == 1
            assert node_c_local.prep_mock.call_count == 0
            assert getattr(memory_b, "local_data", None) is None
            assert getattr(memory_b, "common_local", None) is None
            
            # For path C, use a new branching_node instance or reset mocks for clarity
            BaseNode._next_id = 0
            branching_node_for_c = BranchingNode("BranchC") # id 0
            # node_b_local and node_c_local are not reused here to avoid mock call count confusion
            node_b_for_c_path = BaseTestNode("B_for_C_Path") # id 1
            node_c_for_c_path = BaseTestNode("C_for_C_Path") # id 2
            node_c_for_c_path.prep_mock.side_effect = check_c_memory


            branching_node_for_c.on("path_B", node_b_for_c_path)
            branching_node_for_c.on("path_C", node_c_for_c_path)
            branching_node_for_c.set_trigger("path_C", {"local_data": "for_C", "common_local": "common"})
            
            flow_c = Flow(branching_node_for_c)
            memory_c = Memory({"global_val": 1})
            await flow_c.run(memory_c)
            
            assert node_c_for_c_path.prep_mock.call_count == 1
            assert getattr(memory_c, "local_data", None) is None
            assert getattr(memory_c, "common_local", None) is None
    
    class TestCycleDetection:
        """Tests for cycle detection."""
        
        async def test_execute_loop_maxvisits_times_before_error(self, nodes):
            """Should execute a loop exactly maxVisits times before error."""
            loop_count = [0] 
            
            async def increment_count(mem):
                loop_count[0] += 1
                mem.count = loop_count[0]
            
            nodes["A"].prep_mock.side_effect = increment_count
            nodes["A"].next(nodes["A"]) 
            
            max_visits = 3
            flow = Flow(nodes["A"], {"max_visits": max_visits})
            loop_memory = Memory({})
            
            with pytest.raises(AssertionError, match=f"Maximum cycle count \\({max_visits}\\) reached for {nodes['A'].__class__.__name__}#{nodes['A']._node_order}"):
                await flow.run(loop_memory)
            
            assert loop_count[0] == max_visits
            assert loop_memory.count == max_visits
        
        async def test_error_immediately_if_loop_exceeds_maxvisits(self, nodes):
            """Should throw error immediately if loop exceeds max_visits (e.g. max_visits=2)."""
            nodes["A"].next(nodes["A"]) 
            
            max_visits = 2
            flow = Flow(nodes["A"], {"max_visits": max_visits})
            loop_memory = Memory({})
            
            with pytest.raises(AssertionError, match=f"Maximum cycle count \\({max_visits}\\) reached for {nodes['A'].__class__.__name__}#{nodes['A']._node_order}"):
                await flow.run(loop_memory)
    
    class TestFlowAsNode:
        """Tests for using a Flow as a Node (nesting)."""
        
        async def test_execute_nested_flow_as_single_node_step(self, nodes, memory):
            """Should execute a nested flow as a single node step."""
            nodes["B"].next(nodes["C"])
            sub_flow = Flow(nodes["B"])
            
            nodes["A"].next(sub_flow)
            sub_flow.next(nodes["D"]) 
            
            main_flow = Flow(nodes["A"])
            await main_flow.run(memory)
            
            nodes["A"].post_mock.assert_called_once()
            nodes["B"].post_mock.assert_called_once() 
            nodes["C"].post_mock.assert_called_once() 
            nodes["D"].post_mock.assert_called_once() 
            
            assert memory["post_A"] is True
            assert memory["post_B"] is True
            assert memory["post_C"] is True
            assert memory["post_D"] is True
        
        async def test_nested_flow_prep_post_wrap_subflow_execution(self, nodes, memory):
            """Should run nested flow's prep/post methods around sub-flow execution."""
            nodes["B"].next(nodes["C"])
            sub_flow = Flow(nodes["B"])
            
            sub_flow.prep = AsyncMock()
            sub_flow.post = AsyncMock()
            
            async def subflow_prep(mem):
                mem.subflow_prep = True
                return None # PrepResultT for Flow is not used by its exec_runner
            
            async def subflow_post(mem, prep_res, exec_res):
                mem.subflow_post = True
                # exec_res here is the ExecutionTree from the sub_flow's execution
                return None 
            
            sub_flow.prep.side_effect = subflow_prep
            sub_flow.post.side_effect = subflow_post
            
            nodes["A"].next(sub_flow).next(nodes["D"])
            main_flow = Flow(nodes["A"])
            
            await main_flow.run(memory)
            
            assert memory.subflow_prep is True
            assert memory.post_B is True
            assert memory.post_C is True
            assert memory.subflow_post is True
            assert memory.post_D is True
            
            assert sub_flow.prep.call_count == 1
            sub_flow.post.assert_called_once() # Check it was called
            # To check args: sub_flow.post.assert_called_with(memory, None, ANY) # prep_res is None, exec_res is the log

        async def test_nested_flow_propagates_terminal_action_to_parent_flow(self, memory):
            """Should propagate a terminal action from a sub-flow to the parent flow."""
            BaseNode._next_id = 0
            main_start_node = BaseTestNode("MainStart") # id 0
            sub_node_a = BaseTestNode("SubA")           # id 1
            
            sub_node_b = BranchingNode("SubB")          # id 2
            sub_node_b.set_trigger("sub_flow_completed")
            
            main_end_node = BaseTestNode("MainEnd")     # id 3

            sub_node_a.next(sub_node_b)
            sub_flow = Flow(start=sub_node_a)           # id 4 (Flow itself is a BaseNode)

            main_start_node.next(sub_flow)
            sub_flow.on("sub_flow_completed", main_end_node)

            main_flow = Flow(start=main_start_node)     # id 5
            await main_flow.run(memory)

            assert memory["post_MainStart"] is True
            assert memory["post_SubA"] is True
            assert memory["post_SubB"] is True
            assert memory["post_MainEnd"] is True

            main_start_node.post_mock.assert_called_once()
            sub_node_a.post_mock.assert_called_once()
            sub_node_b.post_mock.assert_called_once() 
            main_end_node.post_mock.assert_called_once()
    
    class TestResultAggregation:
        """Tests for result aggregation using ExecutionTree."""
        
        async def test_return_correct_nested_actions_structure_for_simple_flow(self, nodes, memory):
            """Should return correct structure for a simple flow A -> B."""
            node_a = nodes["A"]
            node_b = nodes["B"]
            node_a.next(node_b)
            
            flow = Flow(node_a)
            result = await flow.run(memory)
            
            expected = {
                'order': node_a._node_order,
                'type': node_a.__class__.__name__,
                'triggered': {
                    DEFAULT_ACTION: [
                        {
                            'order': node_b._node_order,
                            'type': node_b.__class__.__name__,
                            'triggered': None # Node B is terminal
                        }
                    ]
                }
            }
            assert result == expected
        
        async def test_return_correct_structure_for_branching_flow(self, nodes):
            """Should return correct structure for branching flow."""
            # Reset BaseNode ID for predictable IDs
            BaseNode._next_id = 0
            branching_node = BranchingNode("Branch") # id 0
            node_b = BaseTestNode("B_local_branch")      # id 1
            node_c = BaseTestNode("C_local_branch")      # id 2
            node_d = BaseTestNode("D_local_branch")      # id 3

            branching_node.on("path_B", node_b)
            branching_node.on("path_C", node_c)
            node_b.next(node_d) 
            
            # Test path B: Branch -> B -> D
            branching_node.set_trigger("path_B")
            flow_b = Flow(branching_node)
            result_b = await flow_b.run(Memory({}))
            
            expected_b = {
                'order': branching_node._node_order,
                'type': branching_node.__class__.__name__,
                'triggered': {
                    "path_B": [
                        {
                            'order': node_b._node_order,
                            'type': node_b.__class__.__name__,
                            'triggered': {
                                DEFAULT_ACTION: [
                                    {
                                        'order': node_d._node_order,
                                        'type': node_d.__class__.__name__,
                                        'triggered': None # Node D is terminal
                                    }
                                ]
                            }
                        }
                    ]
                }
            }
            assert result_b == expected_b
            
            # Test path C: Branch -> C
            # Need to use a new branching_node or flow to reset visit counts
            BaseNode._next_id = 0
            branching_node_c_path = BranchingNode("BranchCPath") # id 0
            node_b_c_path = BaseTestNode("B_CPath")              # id 1 (unused for path C trigger)
            node_c_c_path = BaseTestNode("C_CPath")              # id 2
            node_d_c_path = BaseTestNode("D_CPath")              # id 3 (unused for path C trigger)

            branching_node_c_path.on("path_B", node_b_c_path)
            branching_node_c_path.on("path_C", node_c_c_path)
            # node_b_c_path.next(node_d_c_path) # Not relevant for path C test

            branching_node_c_path.set_trigger("path_C")
            flow_c = Flow(branching_node_c_path)
            result_c = await flow_c.run(Memory({}))
            
            expected_c = {
                'order': branching_node_c_path._node_order,
                'type': branching_node_c_path.__class__.__name__,
                'triggered': {
                    "path_C": [
                        {
                            'order': node_c_c_path._node_order,
                            'type': node_c_c_path.__class__.__name__,
                            'triggered': None # Node C is terminal
                        }
                    ]
                }
            }
            assert result_c == expected_c
        
        async def test_return_correct_structure_for_multi_trigger(self, nodes, memory):
            """Should return correct structure for multi-trigger (fan-out)."""
            BaseNode._next_id = 0
            class MultiTrigger(BaseTestNode): # Inherits BaseTestNode, so uses its _node_order
                async def post(self, memory, prep_res, exec_res):
                    await super().post(memory, prep_res, exec_res)
                    self.trigger("out1")
                    self.trigger("out2")
            
            multi_node = MultiTrigger("Multi") # id 0
            node_b = BaseTestNode("B_multi")       # id 1
            node_c = BaseTestNode("C_multi")       # id 2
            
            multi_node.on("out1", node_b)
            multi_node.on("out2", node_c)
            
            flow = Flow(multi_node)
            result = await flow.run(memory)
            
            expected_triggered = {
                "out1": [
                    {
                        'order': node_b._node_order,
                        'type': node_b.__class__.__name__,
                        'triggered': None # Node B is terminal
                    }
                ],
                "out2": [
                    {
                        'order': node_c._node_order,
                        'type': node_c.__class__.__name__,
                        'triggered': None # Node C is terminal
                    }
                ]
            }
            
            assert result['order'] == multi_node._node_order
            assert result['type'] == multi_node.__class__.__name__
            assert result['triggered'] is not None
            assert set(result['triggered'].keys()) == {"out1", "out2"}
            assert result['triggered']["out1"] == expected_triggered["out1"]
            assert result['triggered']["out2"] == expected_triggered["out2"]

    class TestTerminalTriggerPropagation:
        """Tests for verifying terminal trigger propagation behavior in Flow and ParallelFlow."""

        async def test_flow_terminal_trigger_propagation_from_nested_flow(self, memory):
            """
            Tests terminal trigger propagation: ParentFlow -> SubFlow (Flow) -> TriggeringNode.
            The TriggeringNode issues a terminal trigger ("TERMINAL_ACTION") with forking_data.
            This trigger is not handled by an edge in SubFlow, so it propagates to SubFlow._triggers.
            This trigger is then not handled by an edge from SubFlow in ParentFlow, so it propagates to ParentFlow._triggers.
            The ExecutionTree for SubFlow within ParentFlow should show triggered["TERMINAL_ACTION"] = [].
            """
            tnode = BranchingNode("TNode")  
            tnode_forking_data = {"tnode_local_key": "tnode_local_val"}
            tnode.set_trigger("TERMINAL_ACTION", tnode_forking_data)

            sflow = Flow(start=tnode)  
            pflow = Flow(start=sflow)  

            parent_execution_tree_for_sflow = await pflow.run(memory, propagate=False)

            assert len(pflow._triggers) == 1
            parent_trigger_info = pflow._triggers[0]
            assert parent_trigger_info["action"] == "TERMINAL_ACTION"
            assert parent_trigger_info["forking_data"] == tnode_forking_data

            assert parent_execution_tree_for_sflow['order'] == sflow._node_order 
            assert parent_execution_tree_for_sflow['type'] == "Flow" 
            assert "TERMINAL_ACTION" in parent_execution_tree_for_sflow['triggered']
            assert parent_execution_tree_for_sflow['triggered']["TERMINAL_ACTION"] == []
            
        async def test_parallelflow_terminal_trigger_propagation_from_nested_parallelflow(self, memory):
            """
            Tests terminal trigger propagation with ParallelFlow: ParentFlow (Parallel) -> SubFlow (Parallel) -> TriggeringNode.
            Similar logic to the Flow test, but using ParallelFlow for parent and sub-flow.
            """
            tnode = BranchingNode("TNode") 
            tnode_forking_data = {"tnode_local_key": "tnode_local_val"}
            tnode.set_trigger("TERMINAL_ACTION", tnode_forking_data)

            sflow = ParallelFlow(start=tnode)  
            pflow = ParallelFlow(start=sflow)  

            parent_execution_tree_for_sflow = await pflow.run(memory, propagate=False)

            assert len(pflow._triggers) == 1
            parent_trigger_info = pflow._triggers[0]
            assert parent_trigger_info["action"] == "TERMINAL_ACTION"
            assert parent_trigger_info["forking_data"] == tnode_forking_data

            assert parent_execution_tree_for_sflow['order'] == sflow._node_order
            assert parent_execution_tree_for_sflow['type'] == "ParallelFlow" 
            assert "TERMINAL_ACTION" in parent_execution_tree_for_sflow['triggered']
            assert parent_execution_tree_for_sflow['triggered']["TERMINAL_ACTION"] == []


class TestFlowActionPropagation:
    """
    Tests how a Flow propagates actions when it's run as a node itself
    (i.e., using flow.run(memory, propagate=True)).
    Focuses on the *observable output* of flow.run(propagate=True).
    """

    @pytest.fixture(autouse=True)
    def reset_ids_fixture(self):
        """Ensures predictable node ordering for each test."""
        BaseNode._next_id = 0
        yield
        BaseNode._next_id = 0 # Optional: reset after, pre-test is key

    @pytest.fixture
    def mem(self):
        """Provides a fresh Memory instance for each test."""
        return Memory({})

    async def test_flow_with_silently_terminating_sub_node_propagates_implicit_default(self, mem):
        """
        Scenario: Flow contains one sub-node that finishes without any explicit trigger.
        Expected: The Flow itself, when run with propagate=True, should yield its own
                  implicit DEFAULT_ACTION (because its internal _triggers list will be empty).
        """
        silent_sub_node = BaseTestNode("SilentSub") # Order 0
        # silent_sub_node.post_mock is not configured to call self.trigger()

        flow = Flow(silent_sub_node) # Order 1
        propagated_triggers = await flow.run(mem, propagate=True)

        assert len(propagated_triggers) == 1, "Flow should propagate one action"
        action, p_mem = propagated_triggers[0]
        assert action == DEFAULT_ACTION, "Flow should propagate DEFAULT_ACTION"
        assert isinstance(p_mem, Memory), "Propagated action should include a Memory object"
        # No direct check on flow._triggers - its state is implied by propagated_triggers

    async def test_flow_with_sub_node_explicitly_triggering_default_propagates_default(self, mem):
        """
        Scenario: Flow's sub-node explicitly triggers DEFAULT_ACTION, which is terminal within the Flow.
        Expected: The Flow should add this explicit DEFAULT_ACTION to its own _triggers list
                  and subsequently propagate it.
        """
        explicit_default_sub_node = BranchingNode("ExplicitDefaultSub") # Order 0
        explicit_default_sub_node.set_trigger(DEFAULT_ACTION, clear_existing_in_post=True)

        flow = Flow(explicit_default_sub_node) # Order 1
        propagated_triggers = await flow.run(mem, propagate=True)
        
        assert len(propagated_triggers) == 1, "Flow should propagate one action"
        action, p_mem = propagated_triggers[0]
        assert action == DEFAULT_ACTION, "Flow should propagate the explicit DEFAULT_ACTION"
        assert isinstance(p_mem, Memory)

    async def test_flow_with_sub_node_explicitly_triggering_custom_action_propagates_custom(self, mem):
        """
        Scenario: Flow's sub-node explicitly triggers a CUSTOM_ACTION, terminal within the Flow.
        Expected: The Flow should add this CUSTOM_ACTION to its _triggers and propagate it.
        """
        explicit_custom_sub_node = BranchingNode("ExplicitCustomSub") # Order 0
        fork_data = {"key": "value"}
        explicit_custom_sub_node.set_trigger("MY_CUSTOM", fork_data=fork_data, clear_existing_in_post=True)

        flow = Flow(explicit_custom_sub_node) # Order 1
        propagated_triggers = await flow.run(mem, propagate=True)

        assert len(propagated_triggers) == 1, "Flow should propagate one action"
        action, p_mem = propagated_triggers[0]
        assert action == "MY_CUSTOM", "Flow should propagate the CUSTOM_ACTION"
        assert isinstance(p_mem, Memory)
        assert p_mem.local["key"] == "value", "Forking data should be in the propagated memory's local store"
        
    async def test_nested_flow_outer_propagates_implicit_default_if_sub_flow_silent(self, mem):
        """
        Scenario: OuterFlow -> SubFlow -> SilentTerminalNode.
                  SubFlow will propagate its own implicit DEFAULT_ACTION (its _triggers will be empty).
        Expected: OuterFlow should NOT add SubFlow's implicit DEFAULT_ACTION to its own _triggers.
                  Thus, OuterFlow will propagate its own implicit DEFAULT_ACTION.
        """
        silent_in_nested = BaseTestNode("SilentInNested") # Order 0
        sub_flow = Flow(silent_in_nested) # Order 1
        
        outer_a = BaseTestNode("OuterA") # Order 2
        outer_a.next(sub_flow) # OuterA -> SubFlow (default action)
        
        outer_flow = Flow(outer_a) # Order 3
        propagated_triggers = await outer_flow.run(mem, propagate=True)

        assert len(propagated_triggers) == 1, "OuterFlow should propagate one action"
        action, _ = propagated_triggers[0]
        assert action == DEFAULT_ACTION, "OuterFlow should propagate its own implicit DEFAULT_ACTION"

    async def test_nested_flow_outer_propagates_explicit_default_from_sub_flow(self, mem):
        """
        Scenario: OuterFlow -> SubFlow -> NodeExplicitlyTriggeringDEFAULT.
                  SubFlow will explicitly collect and propagate DEFAULT_ACTION (its _triggers will contain it).
        Expected: OuterFlow SHOULD add SubFlow's explicit DEFAULT_ACTION to its own _triggers
                  and then propagate it.
        """
        explicit_default_in_nested = BranchingNode("ExplicitDefaultInNested") # Order 0
        explicit_default_in_nested.set_trigger(DEFAULT_ACTION, clear_existing_in_post=True)
        sub_flow = Flow(explicit_default_in_nested) # Order 1
        
        outer_a = BaseTestNode("OuterA") # Order 2
        outer_a.next(sub_flow)
        
        outer_flow = Flow(outer_a) # Order 3
        propagated_triggers = await outer_flow.run(mem, propagate=True)

        assert len(propagated_triggers) == 1, "OuterFlow should propagate one action"
        action, _ = propagated_triggers[0]
        assert action == DEFAULT_ACTION, "OuterFlow should propagate the explicit DEFAULT_ACTION from SubFlow"

    async def test_nested_flow_outer_propagates_explicit_custom_action_from_sub_flow(self, mem):
        """
        Scenario: OuterFlow -> SubFlow -> NodeExplicitlyTriggeringCUSTOM.
                  SubFlow will explicitly collect and propagate CUSTOM_ACTION.
        Expected: OuterFlow SHOULD add SubFlow's CUSTOM_ACTION to its _triggers and propagate it.
        """
        explicit_custom_in_nested = BranchingNode("ExplicitCustomInNested") # Order 0
        custom_fork_data = {"sub_val": "sub_data_value"}
        explicit_custom_in_nested.set_trigger("NESTED_CUSTOM", fork_data=custom_fork_data, clear_existing_in_post=True)
        sub_flow = Flow(explicit_custom_in_nested) # Order 1
        
        outer_a = BaseTestNode("OuterA") # Order 2
        outer_a.next(sub_flow)
        
        outer_flow = Flow(outer_a) # Order 3
        propagated_triggers = await outer_flow.run(mem, propagate=True)

        assert len(propagated_triggers) == 1, "OuterFlow should propagate one action"
        action, p_mem = propagated_triggers[0]
        assert action == "NESTED_CUSTOM", "OuterFlow should propagate the CUSTOM_ACTION from SubFlow"
        assert isinstance(p_mem, Memory)
        assert p_mem.local["sub_val"] == "sub_data_value", "Forking data should be present"
