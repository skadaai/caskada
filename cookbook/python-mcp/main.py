import asyncio # Import asyncio
from brainyflow import Node, Flow, Memory
from utils import call_llm, get_tools, call_tool
import yaml
import sys

class GetToolsNode(Node):
    async def prep(self, memory: Memory):
        """Initialize and get tools"""
        # The question is now passed from main via memory
        print("🔍 Getting available tools...")
        return "simple_server.py"

    async def exec(self, server_path):
        """Retrieve tools from the MCP server"""
        tools = get_tools(server_path)
        return tools

    async def post(self, memory: Memory, prep_res, exec_res): # Use memory and add type hint
        """Store tools and process to decision node"""
        tools = exec_res
        memory.tools = tools # Use property access

        # Format tool information for later use
        tool_info = []
        for i, tool in enumerate(tools, 1):
            properties = tool.inputSchema.get('properties', {})
            required = tool.inputSchema.get('required', [])

            params = []
            for param_name, param_info in properties.items():
                param_type = param_info.get('type', 'unknown')
                req_status = "(Required)" if param_name in required else "(Optional)"
                params.append(f"    - {param_name} ({param_type}): {req_status}")

            tool_info.append(f"[{i}] {tool.name}\n  Description: {tool.description}\n  Parameters:\n" + "\n".join(params))

        memory.tool_info = "\n".join(tool_info) # Use property access
        self.trigger("decide") # Use trigger

class DecideToolNode(Node):
    async def prep(self, memory: Memory): # Use memory and add type hint
        """Prepare the prompt for LLM to process the question"""
        tool_info = memory.tool_info if hasattr(memory, 'tool_info') else "" # Use property access
        question = memory.question if hasattr(memory, 'question') else "" # Use property access

        prompt = f"""
### CONTEXT
You are an assistant that can use tools via Model Context Protocol (MCP).

### ACTION SPACE
{tool_info}

### TASK
Answer this question: "{question}"

## NEXT ACTION
Analyze the question, extract any numbers or parameters, and decide which tool to use.
Return your response in this format:

```yaml
thinking: |
    <your step-by-step reasoning about what the question is asking and what numbers to extract>
tool: <name of the tool to use>
reason: <why you chose this tool>
parameters:
    <parameter_name>: <parameter_value>
    <parameter_name>: <parameter_value>
```
IMPORTANT:
1. Extract numbers from the question properly
2. Use proper indentation (4 spaces) for multi-line fields
3. Use the | character for multi-line text fields
"""
        return prompt

    async def exec(self, prompt):
        """Call LLM to process the question and decide which tool to use"""
        print("🤔 Analyzing question and deciding which tool to use...")
        response = call_llm(prompt)
        return response

    async def post(self, memory: Memory, prep_res, exec_res):
        """Extract decision from YAML and save to memory"""
        try:
            yaml_str = exec_res.split("```yaml")[1].split("```")[0].strip()
            decision = yaml.safe_load(yaml_str)

            memory.tool_name = decision["tool"] # Use property access
            memory.parameters = decision["parameters"] # Use property access
            memory.thinking = decision.get("thinking", "") # Use property access and .get for safety

            print(f"💡 Selected tool: {memory.tool_name}") # Use property access
            print(f"🔢 Extracted parameters: {memory.parameters}") # Use property access

            self.trigger("execute") # Use trigger
        except Exception as e:
            print(f"❌ Error parsing LLM response: {e}")
            print("Raw response:", exec_res)
            self.trigger("error") # Trigger an error action
            return

class ExecuteToolNode(Node):
    async def prep(self, memory: Memory):
        """Prepare tool execution parameters"""
        return memory.tool_name if hasattr(memory, 'tool_name') else None, memory.parameters if hasattr(memory, 'parameters') else {}

    async def exec(self, inputs):
        """Execute the chosen tool"""
        tool_name, parameters = inputs
        print(f"🔧 Executing tool '{tool_name}' with parameters: {parameters}")
        result = call_tool("simple_server.py", tool_name, parameters)
        return result

    async def post(self, memory: Memory, prep_res, exec_res):
        print(f"\n✅ Final Answer: {exec_res}")
        memory.final_answer = exec_res # Store final answer in memory
        self.trigger("done")


if __name__ == "__main__":
    # Default question
    default_question = "What is 982713504867129384651 plus 73916582047365810293746529?"

    # Get question from command line if provided with --
    question = default_question
    for arg in sys.argv[1:]:
        if arg.startswith("--"):
            question = arg[2:]
            break

    print(f"🤔 Processing question: {question}")

    # Create nodes
    get_tools_node = GetToolsNode()
    decide_node = DecideToolNode()
    execute_node = ExecuteToolNode()

    # Connect nodes using sugar syntax
    get_tools_node - "decide" >> decide_node
    decide_node - "execute" >> execute_node

    # Create and run flow
    flow = Flow(start=get_tools_node)
    memory = {"question": question}
    asyncio.run(flow.run(memory))
