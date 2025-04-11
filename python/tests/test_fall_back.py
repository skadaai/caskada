import unittest
import asyncio
from brainyflow import Node, Flow, ParallelBatchNode

class FallbackNode(Node):
    def __init__(self, should_fail=True, max_retries=1, custom_fallback=None):
        super().__init__(max_retries=max_retries)
        self.should_fail = should_fail
        self.custom_fallback = custom_fallback
        self.last_error = None
    
    async def prep(self, shared_storage):
        if 'results' not in shared_storage:
            shared_storage['results'] = []
        return None
    
    async def exec(self, prep_result):
        if self.should_fail:
            raise ValueError("Intentional failure")
        return "success"
    
    async def exec_fallback(self, prep_result, exc):
        self.last_error = exc
        await asyncio.sleep(0.01)  # Simulate async work
        return self.custom_fallback if self.custom_fallback else "fallback"
    
    async def post(self, shared_storage, prep_result, exec_result):
        shared_storage['results'].append({
            'attempts': self.cur_retry + 1,
            'result': exec_result,
            'error': str(self.last_error) if self.last_error else None
        })

class ContextNode(Node):
    async def exec(self, item):
        err = ValueError("Failed with context")
        err.context = {'item_id': 123}
        raise err
    
    async def exec_fallback(self, item, exc):
        return {
            'error': str(exc),
            'context': getattr(exc, 'context', None)
        }

class ConditionalFallbackNode(Node):
    async def exec(self, item):
        if item.get('type') == 'invalid':
            raise ValueError("Invalid item")
        return {**item, 'processed': True}
    
    async def exec_fallback(self, item, exc):
        if item.get('type') == 'invalid-but-recoverable':
            return {**item, 'processed': False, 'error': str(exc)}
        raise exc

class TestExecFallback(unittest.IsolatedAsyncioTestCase):
    async def test_successful_execution(self):
        """Test that exec_fallback is called after all retries are exhausted"""
        shared_storage = {}
        node = FallbackNode(should_fail=False)
        await node.run(shared_storage)
        
        self.assertEqual(len(shared_storage['results']), 1)
        self.assertEqual(shared_storage['results'][0]['attempts'], 1)
        self.assertEqual(shared_storage['results'][0]['result'], "success")
        self.assertIsNone(shared_storage['results'][0]['error'])

    async def test_fallback_after_failure(self):
        """Test that exec_fallback is called after all retries are exhausted"""
        shared_storage = {}
        node = FallbackNode(should_fail=True, max_retries=2)
        await node.run(shared_storage)
        
        self.assertEqual(len(shared_storage['results']), 1)
        self.assertEqual(shared_storage['results'][0]['attempts'], 2)
        self.assertEqual(shared_storage['results'][0]['result'], "fallback")
        self.assertIn("Intentional failure", shared_storage['results'][0]['error'])

    async def test_custom_fallback_result(self):
        shared_storage = {}
        node = FallbackNode(should_fail=True, custom_fallback="custom")
        await node.run(shared_storage)
        
        self.assertEqual(shared_storage['results'][0]['result'], "custom")

    async def test_error_context_preservation(self):
        node = ContextNode()
        try:
            await node.run({})
        except ValueError as e:
            self.assertEqual(e.context['item_id'], 123)
            self.assertEqual(str(e), "Failed with context")

    async def test_conditional_fallback(self):
        node = ConditionalFallbackNode()
        
        # Should process normally
        valid_result = await node.exec({'type': 'valid'})
        self.assertTrue(valid_result['processed'])
        
        # Should recover with fallback
        recoverable_result = await node.exec_fallback(
            {'type': 'invalid-but-recoverable'}, 
            ValueError("Test error")
        )
        self.assertFalse(recoverable_result['processed'])
        self.assertIn("Test error", recoverable_result['error'])
        
        # Should re-raise for unrecoverable items
        with self.assertRaises(ValueError):
            await node.exec_fallback({'type': 'invalid'}, ValueError("Test error"))

    async def test_fallback_in_flow(self):
        """Test that fallback works within a Flow"""
        class ResultNode(Node):
            async def prep(self, shared_storage):
                return shared_storage.get('results', [])
                
            async def exec(self, prep_result):
                return prep_result
                
            async def post(self, shared_storage, prep_result, exec_result):
                shared_storage['final_result'] = exec_result
                return None
        
        shared_storage = {}
        fallback_node = FallbackNode(should_fail=True)
        result_node = ResultNode()
        fallback_node >> result_node
        
        flow = Flow(start=fallback_node)
        await flow.run(shared_storage)
        
        self.assertEqual(len(shared_storage['results']), 1)
        self.assertEqual(shared_storage['results'][0]['result'], "fallback")
        self.assertEqual(shared_storage['final_result'], [{
            'attempts': 1, 
            'result': 'fallback',
            'error': 'Intentional failure'
        }])

    async def test_retry_count_accuracy(self):
        shared_storage = {}
        node = FallbackNode(should_fail=True, max_retries=3)
        await node.run(shared_storage)

        self.assertEqual(shared_storage['results'][0]['attempts'], 3)

    async def test_throttled_fallback(self):
        shared_storage = {}
        node = FallbackNode(should_fail=True, max_retries=3)
        node.wait = 0.1  # Set wait after initialization
        start_time = asyncio.get_event_loop().time()
        await node.run(shared_storage)
        duration = asyncio.get_event_loop().time() - start_time

        self.assertEqual(shared_storage['results'][0]['attempts'], 3)
        self.assertGreaterEqual(duration, 0.2)  # At least 2 retries * 0.1s wait

    async def test_parallel_batch_fallback(self):
        """Test that fallback works with a node inheriting from ParallelBatchNode"""
        class ParallelItemProcessor(ParallelBatchNode):
            def __init__(self):
                # Initialize ParallelBatchNode which inherits from Node
                super().__init__(max_retries=1) 

            async def exec(self, item):
                # This method processes a SINGLE item. 
                # ParallelBatchNode._exec handles running this in parallel.
                if item.get('should_fail'):
                    raise ValueError("Intentional failure")
                return {**item, 'processed': True}

            async def exec_fallback(self, item, exc):
                 # This method handles fallback for a SINGLE item.
                return {**item, 'fallback': True, 'error': str(exc)}

        # Create test items
        test_items = [
            {'id': 1},
            {'id': 2, 'should_fail': True},
            {'id': 3}
        ]

        # Instantiate the node that inherits from ParallelBatchNode
        processor_node = ParallelItemProcessor()
        
        # Call _exec directly to test the parallel execution and fallback logic
        # Note: _exec takes the list of items directly
        results = await processor_node._exec(test_items)

        # Verify results - asyncio.gather preserves order
        self.assertEqual(len(results), 3)
        
        # Check item 1 (success) - results[0] corresponds to test_items[0]
        self.assertEqual(results[0]['id'], 1)
        self.assertTrue(results[0].get('processed'))
        self.assertIsNone(results[0].get('fallback'))
        self.assertIsNone(results[0].get('error'))

        # Check item 2 (fallback) - results[1] corresponds to test_items[1]
        self.assertEqual(results[1]['id'], 2)
        self.assertIsNone(results[1].get('processed'))
        self.assertTrue(results[1].get('fallback'))
        self.assertIn("Intentional failure", results[1].get('error', ''))

        # Check item 3 (success) - results[2] corresponds to test_items[2]
        self.assertEqual(results[2]['id'], 3)
        self.assertTrue(results[2].get('processed'))
        self.assertIsNone(results[2].get('fallback'))
        self.assertIsNone(results[2].get('error'))
        
    async def test_fallback_with_async_side_effects(self):
        cleanup_called = False
        
        class CleanupNode(Node):
            async def exec(self, _):
                raise ValueError("Always fails")
                
            async def exec_fallback(self, _, exc):
                nonlocal cleanup_called
                await asyncio.sleep(0.01)
                cleanup_called = True
                return "cleanup_complete"
                
        node = CleanupNode()
        await node.run({})
        self.assertTrue(cleanup_called)
        
    async def test_state_between_retries(self):
        attempt_count = 0
        
        class RetryTrackingNode(Node):
            def __init__(self):
                super().__init__(max_retries=3)
                
            async def exec(self, _):
                nonlocal attempt_count
                attempt_count += 1
                raise ValueError(f"Attempt {attempt_count}")
                
            async def exec_fallback(self, _, exc):
                return str(exc)
                
        node = RetryTrackingNode()
        await node.run({})
        self.assertEqual(attempt_count, 3)

if __name__ == '__main__':
    unittest.main()
