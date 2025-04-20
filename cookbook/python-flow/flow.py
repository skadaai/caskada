from brainyflow import Node, Flow, Memory # Import Memory

class TextInput(Node):
    async def prep(self, memory: Memory): # Use memory and add type hint
        """Get text input from user."""
        if not hasattr(memory, 'text'): # Use property access
            text = input("\nEnter text to convert: ")
            memory.text = text # Use property access
        return memory.text # Use property access

    async def post(self, memory: Memory, prep_res, exec_res): # Use memory and add type hint
        print("\nChoose transformation:")
        print("1. Convert to UPPERCASE")
        print("2. Convert to lowercase")
        print("3. Reverse text")
        print("4. Remove extra spaces")
        print("5. Exit")

        choice = input("\nYour choice (1-5): ")

        if choice == "5":
            self.trigger("exit") # Use trigger
            return

        memory.choice = choice # Use property access
        self.trigger("transform") # Use trigger

class TextTransform(Node):
    async def prep(self, memory: Memory): # Use memory and add type hint
        return memory.text if hasattr(memory, 'text') else "", memory.choice if hasattr(memory, 'choice') else "" # Use property access

    async def exec(self, inputs):
        text, choice = inputs

        if choice == "1":
            return text.upper()
        elif choice == "2":
            return text.lower()
        elif choice == "3":
            return text[::-1]
        elif choice == "4":
            return " ".join(text.split())
        else:
            return "Invalid option!"

    async def post(self, memory: Memory, prep_res, exec_res): # Use memory and add type hint
        print("\nResult:", exec_res)

        if input("\nConvert another text? (y/n): ").lower() == 'y':
            if hasattr(memory, 'text'): # Check if text exists before popping
                del memory.text # Use property access to delete
            self.trigger("input") # Use trigger
            return
        self.trigger("exit") # Use trigger

class EndNode(Node):
    pass

# Create nodes
text_input = TextInput()
text_transform = TextTransform()
end_node = EndNode()

# Connect nodes
text_input - "transform" >> text_transform
text_transform - "input" >> text_input
text_transform - "exit" >> end_node

# Create flow
flow = Flow(start=text_input)
