import pytest
from caskada import Node

class TestNodeCloneDeepCopying:
    """Tests that verify mutable attributes are properly deep-copied during node cloning."""
    
    def test_mutable_list_independence(self):
        """Test that mutable list attributes are independent after cloning."""
        # Create a node with a mutable list attribute
        original_node = Node()
        original_node.mutable_list = [1, 2, 3]
        
        # Clone the node
        cloned_node = original_node.clone()
        
        # Verify initial state is identical
        assert cloned_node.mutable_list == [1, 2, 3]
        
        # Modify the list in the original node
        original_node.mutable_list.append(4)
        
        # Verify that the change does NOT affect the cloned node
        assert cloned_node.mutable_list == [1, 2, 3]
        assert id(original_node.mutable_list) != id(cloned_node.mutable_list)
        
        # Modify the list in the cloned node
        cloned_node.mutable_list.append(5)
        
        # Verify that the change does NOT affect the original node
        assert original_node.mutable_list == [1, 2, 3, 4]
        assert cloned_node.mutable_list == [1, 2, 3, 5]
    
    def test_mutable_dict_independence(self):
        """Test that mutable dictionary attributes are independent after cloning."""
        # Create a node with a mutable dictionary attribute
        original_node = Node()
        original_node.mutable_dict = {"a": 1, "b": 2}
        
        # Clone the node
        cloned_node = original_node.clone()
        
        # Verify initial state is identical
        assert cloned_node.mutable_dict == {"a": 1, "b": 2}
        
        # Modify the dict in the original node
        original_node.mutable_dict["c"] = 3
        
        # Verify that the change does NOT affect the cloned node
        assert cloned_node.mutable_dict == {"a": 1, "b": 2}
        assert id(original_node.mutable_dict) != id(cloned_node.mutable_dict)
        
        # Modify the dict in the cloned node
        cloned_node.mutable_dict["d"] = 4
        
        # Verify that the change does NOT affect the original node
        assert original_node.mutable_dict == {"a": 1, "b": 2, "c": 3}
        assert cloned_node.mutable_dict == {"a": 1, "b": 2, "d": 4}
    
    def test_nested_mutable_objects_independence(self):
        """Test that nested mutable objects are independent after cloning."""
        # Create a node with nested mutable structures
        original_node = Node()
        original_node.nested = {
            "list": [1, 2],
            "dict": {"x": 1},
            "complex": [{"a": 1}, {"b": 2}]
        }
        
        # Clone the node
        cloned_node = original_node.clone()
        
        # Modify nested structures in original
        original_node.nested["list"].append(3)
        original_node.nested["dict"]["y"] = 2
        original_node.nested["complex"][0]["a"] = 100
        
        # Verify changes do NOT affect clone
        assert 3 not in cloned_node.nested["list"]
        assert "y" not in cloned_node.nested["dict"]
        assert cloned_node.nested["complex"][0]["a"] == 1

        # Modify nested structures in clone
        cloned_node.nested["list"].append(4)
        cloned_node.nested["dict"]["z"] = 3
        cloned_node.nested["complex"][1]["b"] = 200

        # Verify changes do NOT affect original
        assert 4 not in original_node.nested["list"]
        assert "z" not in original_node.nested["dict"]
        assert original_node.nested["complex"][1]["b"] == 2

    def test_internal_triggers_list_independence(self):
        """Test that internal _triggers list is independent after cloning."""
        # Create custom node that will use _triggers
        class TriggerTestNode(Node):
            def trigger_action(self, action="test", data=None):
                # Unlock to allow triggering
                self._locked = False
                self.trigger(action, data)
                self._locked = True
        
        # Create and clone node
        original_node = TriggerTestNode()
        cloned_node = original_node.clone()
        
        # Verify both start with empty triggers list
        assert original_node._triggers == []
        assert cloned_node._triggers == []
        assert id(original_node._triggers) != id(cloned_node._triggers)
        
        # Trigger action on original
        original_node.trigger_action()
        
        # Verify _triggers is NOT updated in cloned node
        assert len(original_node._triggers) == 1
        assert len(cloned_node._triggers) == 0
    
    @pytest.mark.asyncio
    async def test_concurrent_flow_independence(self):
        """Test confirming independence in concurrent flows."""
        # Create a flow with a state-tracking node
        class StateNode(Node):
            def __init__(self):
                super().__init__()
                self.state_list = []
            
            async def exec(self, prep_res):
                # Simulate processing that modifies internal state
                self.state_list.append(f"processing-{len(self.state_list)}")
                return f"result-{len(self.state_list)}"
        
        # Setup test
        node = StateNode()
        node_clone = node.clone()
        
        # Verify initial state
        assert node.state_list == []
        assert node_clone.state_list == []
        assert id(node.state_list) != id(node_clone.state_list)
        
        # Simulate first "flow" modifying the state
        node.state_list.append("flow-1-item")
        
        # Verify second "flow" does NOT see the modification
        assert node_clone.state_list == []
        
        # Simulate second "flow" modifying the state
        node_clone.state_list.append("flow-2-item")
        
        # Verify first "flow" does NOT see the modifications from the second flow
        assert node.state_list == ["flow-1-item"]
        assert node_clone.state_list == ["flow-2-item"]
