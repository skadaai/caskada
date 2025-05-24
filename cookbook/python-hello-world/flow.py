from brainyflow import Node, Flow
from utils.call_llm import call_llm

# An example node and flow
# Please replace this with your own node and flow
class AnswerNode(Node):
    async def prep(self, shared):
        # Read question from shared
        return shared["question"]
    
    async def exec(self, question):
        return call_llm(question)
    
    async def post(self, shared, prep_res, exec_res):
        # Store the answer in shared
        shared["answer"] = exec_res

answer_node = AnswerNode()
qa_flow = Flow(start=answer_node)