import time
import threading
import asyncio
from brainyflow import Node, Flow, Memory # Import Memory
from utils import fake_stream_llm, stream_llm

class StreamNode(Node):
    async def prep(self, memory: Memory):
        # Create interrupt event
        interrupt_event = threading.Event()

        # Start a thread to listen for user interrupt
        def wait_for_interrupt():
            input("Press ENTER at any time to interrupt streaming...\n")
            interrupt_event.set()
        listener_thread = threading.Thread(target=wait_for_interrupt)
        listener_thread.start()

        # Get prompt from memory
        prompt = memory.prompt if hasattr(memory, 'prompt') else ""
        # Get chunks from LLM function
        chunks = fake_stream_llm(prompt)
        return chunks, interrupt_event, listener_thread

    async def exec(self, prep_res):
        chunks, interrupt_event, listener_thread = prep_res
        for chunk in chunks:
            if interrupt_event.is_set():
                print("User interrupted streaming.")
                break

            if hasattr(chunk.choices[0].delta, 'content') and chunk.choices[0].delta.content is not None:
                chunk_content = chunk.choices[0].delta.content
                print(chunk_content, end="", flush=True)
                await asyncio.sleep(0.1)  # simulate latency
        return interrupt_event, listener_thread

    async def post(self, memory: Memory, prep_res, exec_res):
        interrupt_event, listener_thread = exec_res
        # Join the interrupt listener so it doesn't linger
        interrupt_event.set()
        listener_thread.join()
        self.trigger("default")

async def main():
    # Usage:
    node = StreamNode()
    flow = Flow(start=node)

    memory = {"prompt": "What's the meaning of life?"}
    await flow.run(memory)

if __name__ == "__main__":
    asyncio.run(main())
