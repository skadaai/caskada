from brainyflow import Node
from utils.process_task import process_task

class ProcessNode(Node):
    async def prep(self, shared):
        task_input = getattr(shared, "task_input", "No input")
        print("ProcessNode Prep")
        return task_input

    async def exec(self, prep_res):
        return process_task(prep_res)

    async def post(self, shared, prep_res, exec_res):
        shared["processed_output"] = exec_res
        print("ProcessNode Post: Output stored.")
        self.trigger("default") # Go to ReviewNode

class ReviewNode(Node):
    async def prep(self, shared):
        review_event = getattr(shared, "review_event")
        queue = getattr(shared, "sse_queue") # Expect queue in shared
        processed_output = getattr(shared, "processed_output", "N/A")

        if not review_event or not queue:
            print("ERROR: ReviewNode Prep - Missing review_event or sse_queue in shared store!")
            return None # Signal failure

        # Push status update to SSE queue
        status_update = {
            "status": "waiting_for_review",
            "output_to_review": processed_output
        }
        await queue.put(status_update)
        print("ReviewNode Prep: Put 'waiting_for_review' on SSE queue.")

        return review_event # Return event for exec

    async def exec(self, prep_res):
        review_event = prep_res
        if not review_event:
            print("ReviewNode Exec: Skipping wait (no event from prep).")
            return
        print("ReviewNode Exec: Waiting on review_event...")
        await review_event.wait()
        print("ReviewNode Exec: review_event set.")

    async def post(self, shared, prep_res, exec_res):
        feedback = getattr(shared, "feedback")
        print(f"ReviewNode Post: Processing feedback '{feedback}'")

        # Clear the event for potential loops
        review_event = getattr(shared, "review_event")
        if review_event:
            review_event.clear()
        shared["feedback"] = None # Reset feedback

        if feedback == "approved":
            shared["final_result"] = getattr(shared, "processed_output")
            print("ReviewNode Post: Action=approved")
            self.trigger("approved")
            return
        
        print("ReviewNode Post: Action=rejected")
        self.trigger("rejected")

class ResultNode(Node):
     async def prep(self, shared):
         print("ResultNode Prep")
         return getattr(shared, "final_result", "No final result.")

     async def exec(self, prep_res):
         print(f"--- FINAL RESULT ---")
         print(prep_res)
         print(f"--------------------")
         return prep_res

     async def post(self, shared, prep_res, exec_res):
         print("ResultNode Post: Flow finished.")
         self.trigger(None) # End flow