import os
import asyncio
from brainyflow import Node, Flow, Memory
from utils import call_llm

# 1. Trigger Node (Fans out work)
class TriggerTranslationsNode(Node):
    async def prep(self, memory: Memory):
        text = memory.text if hasattr(memory, 'text') else "(No text provided)"
        languages = memory.languages if hasattr(memory, 'languages') else ["Chinese", "Spanish", "Japanese", "German", 
                              "Russian", "Portuguese", "French", "Korean"]
        return [(text, lang) for lang in languages]

    async def post(self, memory: Memory, prep_res: list, exec_res):
        items = prep_res
        memory.translations = [] # Initialize results list
        for index, (text, lang) in enumerate(items):
            self.trigger("process_one", {"text": text, "language": lang, "index": index})
        self.trigger("write_results") # Trigger the next step after fanning out

# 2. Processor Node (Handles one language)
class TranslateOneLanguageNode(Node):
    async def prep(self, memory: Memory):
        # Read data passed via forkingData from local memory
        return {
            "text": memory.text,
            "language": memory.language,
            "index": memory.index
        }

    async def exec(self, item):
        text, language, index = item["text"], item["language"], item["index"]
        
        prompt = f"""
Please translate the following markdown file into {language}. 
But keep the original markdown format, links and code blocks.
Directly return the translated text, without any other text or comments.

Original: 
{text}

Translated:"""
        
        result = call_llm(prompt)
        
        print(f"Translated {language} text")

        return {"language": language, "translation": result, "index": index}

    async def post(self, memory: Memory, prep_res, exec_res):
        # Store individual summary in global memory
        memory.translations.append(exec_res)
        self.trigger("default") # Trigger next node in the sequential flow

# 3. Write Results Node (Aggregates and writes)
class WriteTranslationsNode(Node):
    async def prep(self, memory: Memory):
        return {
            "translations": memory.translations if hasattr(memory, 'translations') else [],
            "output_dir": memory.output_dir if hasattr(memory, 'output_dir') else "translations"
        }

    async def exec(self, prep_res):
        translations = prep_res["translations"]
        output_dir = prep_res["output_dir"]

        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        # Write each translation to a file
        for result in translations:
            language, translation = result["language"], result["translation"]
            
            # Write to file
            filename = os.path.join(output_dir, f"README_{language.upper()}.md")
            with open(filename, "w", encoding="utf-8") as f:
                f.write(translation)
            
            print(f"Saved translation to {filename}")
        
        return output_dir

    async def post(self, memory: Memory, prep_res, exec_res):
        output_dir = exec_res
        print("\n=== Translation Complete ===")
        print(f"Translations saved to: {output_dir}")
        print("============================")
        self.trigger("default") # End of the flow

async def main():
    # read the text from ../../README.md
    with open("../../README.md", "r") as f:
        text = f.read()
    
    # Default settings
    memory = Memory({
        "text": text,
        "languages": ["Chinese", "Spanish", "Japanese", "German", "Russian", "Portuguese", "French", "Korean"],
        "output_dir": "translations"
    })

    # Run the translation flow
    trigger_node = TriggerTranslationsNode()
    processor_node = TranslateOneLanguageNode()
    write_node = WriteTranslationsNode()

    trigger_node - "process_one" >> processor_node
    trigger_node - "write_results" >> write_node # Trigger write node after fanning out
    processor_node >> write_node # This transition is not strictly needed in a sequential flow where trigger_node handles the next step, but kept for clarity.

    flow = Flow(start=trigger_node)
    await flow.run(memory)

if __name__ == "__main__":
    asyncio.run(main())
