from brainyflow import Node, Flow, Memory
from utils.call_llm import call_llm

# An example node and flow
# Please replace this with your own node and flow
class AnswerNode(Node):
    async def prep(self, memory: Memory): # Use memory and add type hint
        # Read question from memory
        return memory.question if hasattr(memory, 'question') else "" # Use property access

    async def exec(self, question):
        return call_llm(question)

    async def post(self, memory: Memory, prep_res, exec_res):
        # Store the answer in memory
        memory.answer = exec_res # Use property access

answer_node = AnswerNode()
qa_flow = Flow(start=answer_node)
