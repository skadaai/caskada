from brainyflow import Node, Memory
from utils.vector_index import create_index, add_vector, search_vectors
from utils.call_llm import call_llm
from utils.get_embedding import get_embedding

class GetUserQuestionNode(Node):
    async def prep(self, memory: Memory):
        """Initialize messages if first run"""
        if not hasattr(memory, "messages"):
            memory.messages = []
            print("Welcome to the interactive chat! Type 'exit' to end the conversation.")

        return None

    async def exec(self, _):
        """Get user input interactively"""
        # Get interactive input from user
        user_input = input("\nYou: ")

        # Check if user wants to exit
        if user_input.lower() == 'exit':
            return None

        return user_input

    async def post(self, memory: Memory, prep_res, exec_res):
        # If exec_res is None, the user wants to exit
        if exec_res is None:
            print("\nGoodbye!")
            self.trigger(None)  # End the conversation
            return

        # Add user message to current messages
        memory.messages.append({"role": "user", "content": exec_res})

        self.trigger("retrieve")

class AnswerNode(Node):
    async def prep(self, memory: Memory):
        """Prepare context for the LLM"""
        if not hasattr(memory, "messages") or not memory.messages:
            return None

        # 1. Get the last 3 conversation pairs (or fewer if not available)
        recent_messages = memory.messages[-6:] if len(memory.messages) > 6 else memory.messages

        # 2. Add the retrieved relevant conversation if available
        context = []
        if hasattr(memory, "retrieved_conversation") and memory.retrieved_conversation:
            # Add a system message to indicate this is a relevant past conversation
            context.append({
                "role": "system",
                "content": "The following is a relevant past conversation that may help with the current query:"
            })
            context.extend(memory.retrieved_conversation)
            context.append({
                "role": "system",
                "content": "Now continue the current conversation:"
            })

        # 3. Add the recent messages
        context.extend(recent_messages)

        return context

    async def exec(self, messages):
        """Generate a response using the LLM"""
        if messages is None:
            return None

        # Call LLM with the context
        response = call_llm(messages)
        return response

    async def post(self, memory: Memory, prep_res, exec_res):
        """Process the LLM response"""
        if prep_res is None or exec_res is None:
            self.trigger(None)  # End the conversation
            return

        # Print the assistant's response
        print(f"\nAssistant: {exec_res}")

        # Add assistant message to history
        memory.messages.append({"role": "assistant", "content": exec_res})

        # If we have more than 6 messages (3 conversation pairs), archive the oldest pair
        if len(memory.messages) > 6:
            self.trigger("embed")
        else:
            # We only end if the user explicitly typed 'exit'
            # Even if last_question is set, we continue in interactive mode
            self.trigger("question")

class EmbedNode(Node):
    async def prep(self, memory: Memory):
        """Extract the oldest conversation pair for embedding"""
        if not hasattr(memory, "messages") or len(memory.messages) <= 6:
            return None

        # Extract the oldest user-assistant pair
        oldest_pair = memory.messages[:2]
        # Remove them from current messages
        memory.messages = memory.messages[2:]

        return oldest_pair

    async def exec(self, conversation):
        """Embed a conversation"""
        if not conversation:
            return None

        # Combine user and assistant messages into a single text for embedding
        user_msg = next((msg for msg in conversation if msg["role"] == "user"), {"content": ""})
        assistant_msg = next((msg for msg in conversation if msg["role"] == "assistant"), {"content": ""})
        combined = f"User: {user_msg['content']} Assistant: {assistant_msg['content']}"

        # Generate embedding
        embedding = get_embedding(combined)

        return {
            "conversation": conversation,
            "embedding": embedding
        }

    async def post(self, memory: Memory, prep_res, exec_res):
        """Store the embedding and add to index"""
        if not exec_res:
            # If there's nothing to embed, just continue with the next question
            self.trigger("question")
            return

        # Initialize vector index if not exist
        if not hasattr(memory, "vector_index"):
            memory.vector_index = create_index()
            memory.vector_items = []  # Track items separately

        # Add the embedding to the index and store the conversation
        position = add_vector(memory.vector_index, exec_res["embedding"])
        memory.vector_items.append(exec_res["conversation"])

        print(f"✅ Added conversation to index at position {position}")
        print(f"✅ Index now contains {len(memory.vector_items)} conversations")

        # Continue with the next question
        self.trigger("question")

class RetrieveNode(Node):
    async def prep(self, memory: Memory):
        """Get the current query for retrieval"""
        if not hasattr(memory, "messages") or not memory.messages:
            return None

        # Get the latest user message for searching
        latest_user_msg = next((msg for msg in reversed(memory.messages)
                                if msg["role"] == "user"), {"content": ""})

        # Check if we have a vector index with items
        if (not hasattr(memory, "vector_index") or
            not hasattr(memory, "vector_items") or
            len(memory.vector_items) == 0):
            return None

        return {
            "query": latest_user_msg["content"],
            "vector_index": memory.vector_index,
            "vector_items": memory.vector_items
        }

    async def exec(self, inputs):
        """Find the most relevant past conversation"""
        if not inputs:
            return None

        query = inputs["query"]
        vector_index = inputs["vector_index"]
        vector_items = inputs["vector_items"]

        print(f"🔍 Finding relevant conversation for: {query[:30]}...")

        # Create embedding for the query
        query_embedding = get_embedding(query)

        # Search for the most similar conversation
        indices, distances = search_vectors(vector_index, query_embedding, k=1)

        if not indices:
            return None

        # Get the corresponding conversation
        conversation = vector_items[indices[0]]

        return {
            "conversation": conversation,
            "distance": distances[0]
        }

    async def post(self, memory: Memory, prep_res, exec_res):
        """Store the retrieved conversation"""
        if exec_res is not None:
            memory.retrieved_conversation = exec_res["conversation"]
            print(f"📄 Retrieved conversation (distance: {exec_res['distance']:.4f})")
        else:
            memory.retrieved_conversation = None

        self.trigger("answer")
