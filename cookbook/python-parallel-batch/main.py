import asyncio
import time

from brainyflow import Node, Flow, ParallelFlow, Memory

####################################
# Dummy async function (1s delay)
####################################
async def dummy_llm_summarize(text):
    """Simulates an async LLM call that takes 1 second."""
    await asyncio.sleep(1)
    return f"Summarized({len(text)} chars)"

###############################################
# Batch Processing Nodes
###############################################

class TriggerSummariesNode(Node):
    """
    Triggers processing for each item in the batch.
    """
    async def prep(self, memory: Memory):
        # Return a list of items to process.
        # Each item is (filename, content).
        return list(memory.data.items())

    async def post(self, memory: Memory, files_to_process: list, exec_res):
        print(f"Trigger: Triggering summary for {len(files_to_process)} files.")
        # Initialize results list in global memory
        memory.sequential_summaries = [None] * len(files_to_process)
        memory.parallel_summaries = [None] * len(files_to_process)

        # Trigger a 'process_item' action for each file
        for index, (filename, content) in enumerate(files_to_process):
            self.trigger('process_item', { "filename": filename, "content": content, "index": index })

class SummarizeFileNode(Node):
    """
    Processes a single item (summarizes a file).
    """
    async def prep(self, memory: Memory):
        # Read specific file data from local memory (passed via forkingData)
        return memory.filename, memory.content, memory.index

    async def exec(self, prep_res):
        filename, content, index = prep_res
        print(f"Processor: Summarizing {filename} (Index {index})...")
        summary = await dummy_llm_summarize(content)
        return {"filename": filename, "summary": summary, "index": index}

    async def post(self, memory: Memory, prep_res, exec_res):
        # Store individual summary in global memory at the correct index
        # This node will be used by both sequential and parallel flows,
        # so we need to handle both result lists.
        index = exec_res["index"]
        if hasattr(memory, 'sequential_summaries'):
             memory.sequential_summaries[index] = (exec_res["filename"], exec_res["summary"])
        if hasattr(memory, 'parallel_summaries'):
             memory.parallel_summaries[index] = (exec_res["filename"], exec_res["summary"])

        # No trigger needed if this is the end of the processing for this item

###############################################
# Demo comparing the two approaches
###############################################

async def main():
    # We'll use the same data for both flows
    memory = Memory({
        "data": {
            "file1.txt": "Hello world 1",
            "file2.txt": "Hello world 2",
            "file3.txt": "Hello world 3",
        }
    })

    # 1) Run the sequential version
    trigger_seq = TriggerSummariesNode()
    processor_seq = SummarizeFileNode()
    trigger_seq - 'process_item' >> processor_seq
    seq_flow = Flow(start=trigger_seq)

    print("\n=== Running Sequential ===")
    t0 = time.time()
    await seq_flow.run(memory)
    t1 = time.time()

    # Convert list of tuples to dictionary for consistent output
    memory.sequential_summaries = dict(memory.sequential_summaries)

    # Reset memory for the parallel run (except initial data)
    memory.parallel_summaries = [None] * len(memory.data)


    # 2) Run the parallel version
    trigger_par = TriggerSummariesNode()
    processor_par = SummarizeFileNode()
    trigger_par - 'process_item' >> processor_par
    par_flow = ParallelFlow(start=trigger_par)

    print("\n=== Running Parallel ===")
    t2 = time.time()
    await par_flow.run(memory)
    t3 = time.time()

    # Convert list of tuples to dictionary for consistent output
    memory.parallel_summaries = dict(memory.parallel_summaries)

    # Show times
    print("\n--- Results ---")
    print(f"Sequential Summaries: {memory.sequential_summaries}")
    print(f"Parallel Summaries:   {memory.parallel_summaries}")

    print(f"Sequential took: {t1 - t0:.2f} seconds")
    print(f"Parallel took:   {t3 - t2:.2f} seconds")

if __name__ == "__main__":
    asyncio.run(main())
