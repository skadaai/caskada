from caskada import Node, Flow
from utils import call_llm, get_tools, call_tool
import yaml
import sys

class GetToolsNode(Node):
    async def prep(self, shared):
        """Initialize and get tools"""
        # The question is now passed from main via shared
        print("🔍 Getting available tools...")
        return "simple_server.py"

    async def exec(self, server_path):
        """Retrieve tools from the MCP server"""
        tools = get_tools(server_path)
        return tools

    async def post(self, shared, prep_res, exec_res):
        """Store tools and process to decision node"""
        tools = exec_res
        shared["tools"] = tools
        
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
        
        shared["tool_info"] = "\n".join(tool_info)
        self.trigger("decide")

class DecideToolNode(Node):
    async def prep(self, shared):
        """Prepare the prompt for LLM to process the question"""
        tool_info = shared["tool_info"]
        question = shared["question"]
        
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

IMPORTANT: Make sure to:
1. Use proper indentation (4 spaces) for all multi-line fields
2. Use the | character for multi-line text fields
3. Keep single-line fields without the | character
4. Your answer must be wrapped in yaml code block or it will result in an error. Do not forget to include the ```yaml sequence at the beginning and end it with ```.
"""
        return prompt

    async def exec(self, prompt):
        """Call LLM to process the question and decide which tool to use"""
        print("🤔 Analyzing question and deciding which tool to use...")
        response = call_llm(prompt)
        assert "```yaml" in response, "Response must contain yaml block"
        return response

    async def post(self, shared, prep_res, exec_res):
        """Extract decision from YAML and save to shared context"""
        try:
            yaml_str = exec_res.split("```yaml")[1].split("```")[0].strip()
            decision = yaml.safe_load(yaml_str)
            
            shared["tool_name"] = decision["tool"]
            shared["parameters"] = decision["parameters"]
            shared["thinking"] = decision.get("thinking", "")
            
            print(f"💡 Selected tool: {decision['tool']}")
            print(f"🔢 Extracted parameters: {decision['parameters']}")
            
            self.trigger("execute")
        except Exception as e:
            print(f"❌ Error parsing LLM response: {e}")
            print("Raw response:", exec_res)
            self.trigger(None)

class ExecuteToolNode(Node):
    async def prep(self, shared):
        """Prepare tool execution parameters"""
        return shared["tool_name"], shared["parameters"]

    async def exec(self, inputs):
        """Execute the chosen tool"""
        tool_name, parameters = inputs
        print(f"🔧 Executing tool '{tool_name}' with parameters: {parameters}")
        result = call_tool("simple_server.py", tool_name, parameters)
        return result

    async def post(self, shared, prep_res, exec_res):
        print(f"\n✅ Final Answer: {exec_res}")
        self.trigger("done")


async def main():
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
    
    # Connect nodes
    get_tools_node - "decide" >> decide_node
    decide_node - "execute" >> execute_node
    
    # Create and run flow
    flow = Flow(start=get_tools_node)
    shared = {"question": question}
    await flow.run(shared)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())