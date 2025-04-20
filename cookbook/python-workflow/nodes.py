from brainyflow import Node, Memory # Import Memory
from utils import call_llm
import yaml

class GenerateOutline(Node):
    async def prep(self, memory: Memory): # Use memory and add type hint
        return memory.topic if hasattr(memory, 'topic') else "" # Use property access

    async def exec(self, topic):
        prompt = f"""
Create a simple outline for an article about {topic}.
Include at most 3 main sections (no subsections).

Output the sections in YAML format as shown below:

```yaml
sections:
    - First section
    - Second section
    - Third section
```"""
        response = call_llm(prompt)
        yaml_str = response.split("```yaml")[1].split("```")[0].strip()
        structured_result = yaml.safe_load(yaml_str)
        return structured_result
    
    async def post(self, memory: Memory, prep_res, exec_res): # Use memory and add type hint
        # Store the structured data
        memory.outline_yaml = exec_res # Use property access

        # Extract sections
        sections = exec_res.get("sections", []) # Use .get for safety
        memory.sections = sections # Use property access

        # Format for display
        formatted_outline = "\n".join([f"{i+1}. {section}" for i, section in enumerate(sections)])
        memory.outline = formatted_outline # Use property access

        # Display the results
        print("\n===== OUTLINE (YAML) =====\n")
        print(yaml.dump(exec_res, default_flow_style=False))
        print("\n===== PARSED OUTLINE =====\n")
        print(formatted_outline)
        print("\n=========================\n")

        self.trigger("default") # Use trigger

class WriteSimpleContent(Node):
    async def prep(self, memory: Memory): # Use memory and add type hint
        # Get the list of sections to process
        return memory.sections if hasattr(memory, 'sections') else [] # Use property access

    async def exec(self, sections):
        all_sections_content = []
        section_contents = {}

        for section in sections:
            prompt = f"""
Write a short paragraph (MAXIMUM 100 WORDS) about this section:

{section}

Requirements:
- Explain the idea in simple, easy-to-understand terms
- Use everyday language, avoiding jargon
- Keep it very concise (no more than 100 words)
- Include one brief example or analogy
"""
            content = call_llm(prompt)
            section_contents[section] = content
            all_sections_content.append(f"## {section}\n\n{content}\n")

        return sections, section_contents, "\n".join(all_sections_content)

    async def post(self, memory: Memory, prep_res, exec_res): # Use memory and add type hint
        sections, section_contents, draft = exec_res

        # Store the section contents and draft
        memory.section_contents = section_contents # Use property access
        memory.draft = draft # Use property access

        print("\n===== SECTION CONTENTS =====\n")
        for section, content in section_contents.items():
            print(f"--- {section} ---")
            print(content)
            print()
        print("===========================\n")

        self.trigger("default") # Use trigger

class ApplyStyle(Node):
    """Node to apply a specific style to the article draft.""" # Add docstring
    async def prep(self, memory: Memory): # Use memory and add type hint
        """
        Get the draft from memory
        """
        return memory.draft if hasattr(memory, 'draft') else "" # Use property access

    async def exec(self, draft):
        """
        Apply a specific style to the article
        """
        prompt = f"""
        Rewrite the following draft in a conversational, engaging style:

        {draft}

        Make it:
        - Conversational and warm in tone
        - Include rhetorical questions that engage the reader
        - Add analogies and metaphors where appropriate
        - Include a strong opening and conclusion
        """
        return call_llm(prompt)

    async def post(self, memory: Memory, prep_res, exec_res):
        """
        Store the final article in memory
        """
        memory.final_article = exec_res
        print("\n===== FINAL ARTICLE =====\n")
        print(exec_res)
        print("\n========================\n")
        self.trigger("default") # Use trigger
