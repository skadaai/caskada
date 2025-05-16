import pytest
from brainyflow import Memory

class TestMemory:
    """Tests for the Memory class."""
    class TestInitialization:
        """Tests for Memory initialization."""

        def test_initialize_with_global_store_only(self):
            """Should initialize with global store only."""
            global_store = {"g1": "global1"}
            memory = Memory.create(global_store)
            assert memory.g1 == "global1", "Should access global property"
            assert memory.local == memory._local == {}, "Local store should be empty"

        def test_initialize_with_global_and_local_stores(self):
            """Should initialize with global and local stores."""
            global_store = {"g1": "global1", "common": "global_common"}
            local_store = {"l1": "local1", "common": "local_common"}
            memory = Memory.create(global_store, local_store)
            assert memory.g1 == "global1", "Should access global property"
            assert memory.l1 == "local1", "Should access local property"
            assert memory.common == "local_common", "Local should shadow global"
            assert memory.local == memory._local == {"l1": "local1", "common": "local_common"}, "Local store should contain initial local data"

    class TestProxyBehaviorReading:
        """Tests for Memory proxy reading behavior."""

        @pytest.fixture
        def memory(self):
            """Create a memory instance with both global and local stores."""
            global_store = {"g1": "global1", "common": "global_common"}
            local_store = {"l1": "local1", "common": "local_common"}
            return Memory.create(global_store, local_store)

        def test_read_from_local_store_first(self, memory):
            """Should read from local store first."""
            assert memory.l1 == "local1"
            assert memory.common == "local_common"

        def test_fall_back_to_global_store_if_not_in_local(self, memory):
            """Should fall back to global store if property not in local."""
            assert memory.g1 == "global1"

        def test_return_none_if_property_exists_in_neither_store(self, memory):
            """Should raise AttributeError if property exists in neither store."""
            with pytest.raises(AttributeError, match="'Memory' object has no attribute 'non_existent'"):
                _ = memory.non_existent

        def test_correctly_access_the_local_property(self, memory):
            """Should correctly access the local property."""
            assert memory.local == memory._local  == {"l1": "local1", "common": "local_common"}

    class TestProxyBehaviorWriting:
        """Tests for Memory proxy writing behavior."""

        @pytest.fixture
        def memory(self):
            """Create a memory instance with both global and local stores."""
            self.global_store = {"g1": "global1", "common": "global_common"}
            self.local_store = {"l1": "local1", "common": "local_common"}
            return Memory.create(self.global_store, self.local_store)

        def test_write_property_to_global_store_by_default(self, memory):
            """Should write property to global store by default."""
            memory.new_prop = "new_value"
            assert memory.new_prop == "new_value", "Should read the new property"
            assert self.global_store["new_prop"] == "new_value", "Global store should be updated"
            assert "new_prop" not in self.local_store, "Local store should not be updated"

        def test_overwrite_existing_global_property(self, memory):
            """Should overwrite existing global property."""
            memory.g1 = "updated_global1"
            assert memory.g1 == "updated_global1", "Should read the updated property"
            assert self.global_store["g1"] == "updated_global1", "Global store should be updated"

        def test_remove_property_from_local_store_when_writing_globally(self, memory):
            """Should remove property from local store if it exists when writing globally."""
            assert memory.common == "local_common", "Should initially read from local"
            memory.common = "updated_common_globally"
            assert memory.common == "updated_common_globally", "Should read the new global value"
            assert self.global_store["common"] == "updated_common_globally", "Global store should be updated"
            assert "common" not in self.local_store, "Property should be removed from local store"
            assert "common" not in memory.local, "Accessing via memory.local should also show removal"
            assert "common" not in memory._local, "Accessing via memory._local should also show removal"

        def test_throw_error_when_attempting_to_set_reserved_properties(self, memory):
            """Should throw error when attempting to set reserved properties."""
            with pytest.raises(Exception, match="Reserved property 'global' cannot be set"):
                # Use the exact reserved name 'global'
                setattr(memory, 'global', {})
            with pytest.raises(Exception, match="Reserved property 'local' cannot be set"):
                # Use the exact reserved name 'local'
                setattr(memory, 'local', {})
            with pytest.raises(Exception, match="Reserved property '_global' cannot be set"):
                memory._global = {}
            with pytest.raises(Exception, match="Reserved property '_local' cannot be set"):
                memory._local = {}

    class TestCloning:
        """Tests for Memory clone method."""

        @pytest.fixture
        def memory_setup(self):
            """Create a memory instance and data for cloning tests."""
            self.global_store = {
                "g1": "global1",
                "common": "global_common",
                "nested_g": {"val": 1}
            }
            self.local_store = {
                "l1": "local1",
                "common": "local_common",
                "nested_l": {"val": 2}
            }
            self.memory = Memory.create(self.global_store, self.local_store)
            return self.memory

        def test_create_new_memory_instance_with_shared_global_store(self, memory_setup):
            """Should create a new Memory instance with shared global store reference."""
            cloned_memory = memory_setup.clone()
            assert cloned_memory is not memory_setup, "Cloned memory should be a new instance"
            
            # Verify global store reference is shared by modifying through one and checking the other
            # Modify global via original, check clone
            memory_setup.g1 = "modified_global"
            assert cloned_memory.g1 == "modified_global", "Clone should see global changes"
            
            # Modify global via clone, check original
            cloned_memory.g2 = "added_via_clone"
            assert memory_setup.g2 == "added_via_clone", "Original should see global changes from clone"

        def test_create_deep_clone_of_local_store(self, memory_setup):
            """Should create a deep clone of the local store."""
            cloned_memory = memory_setup.clone()
            
            # Verify local store is not shared by reference
            assert (cloned_memory.local is not memory_setup.local) and (cloned_memory._local is not memory_setup._local), "Local store reference should NOT be shared"
            assert cloned_memory.local == cloned_memory._local == self.local_store, "Cloned local store should have same values initially"
            
            # Modify local via original, check clone
            memory_setup.local["l1"] = "modified_local_original"  # Modify original's internal local store
            
            # Read from the clone. Since its local store is independent, it should still find 'l1' locally.
            assert cloned_memory.l1 == "local1", "Clone local property should be unaffected by original local changes"
            assert cloned_memory.local["l1"] == cloned_memory._local["l1"] == "local1", "Clone local store internal value should be unchanged"
            
            # Modify local via clone, check original
            cloned_memory.local["l2"] = "added_via_clone_local"
            # Accessing l2 on the original should raise AttributeError as it wasn't set globally or locally there
            with pytest.raises(AttributeError, match="'Memory' object has no attribute 'l2'"):
                _ = memory_setup.l2
            assert "l2" not in memory_setup.local, "Original local store internal value should be unchanged"
            
            # Test nested objects
            assert cloned_memory.nested_l == {"val": 2}
            memory_setup.local["nested_l"]["val"] = 99
            assert cloned_memory.nested_l == {"val": 2}, "Nested local object in clone should be unaffected"

        def test_correctly_merge_forking_data_into_new_local_store(self, memory_setup):
            """Should correctly merge forkingData into the new local store."""
            forking_data = {"f1": "forked1", "common": "forked_common", "nested_f": {"val": 3}}
            cloned_memory = memory_setup.clone(forking_data)
            
            assert cloned_memory.f1 == "forked1", "Should access forked property"
            assert cloned_memory.common == "forked_common", "Forked data should shadow original local and global"
            assert cloned_memory.l1 == "local1", "Should still access original local property"
            assert cloned_memory.g1 == "global1", "Should still access global property"
            assert cloned_memory.nested_f == {"val": 3}
            
            # Check internal local store state
            assert cloned_memory.local == {
                "l1": "local1",
                "common": "forked_common",  # Overwritten
                "nested_l": {"val": 2},
                "f1": "forked1",  # Added
                "nested_f": {"val": 3},  # Added
            }
            
            # Ensure forkingData was deep cloned
            forking_data["nested_f"]["val"] = 99
            assert cloned_memory.nested_f == {"val": 3}, "Nested object in forked data should have been deep cloned"

        def test_handle_empty_forking_data(self, memory_setup):
            """Should handle empty forkingData."""
            cloned_memory = memory_setup.clone({})
            assert cloned_memory.local == cloned_memory._local == self.local_store

        def test_handle_cloning_without_forking_data(self, memory_setup):
            """Should handle cloning without forkingData."""
            cloned_memory = memory_setup.clone()
            assert cloned_memory.local == cloned_memory._local == self.local_store
