import asyncio
import os
import time
from brainyflow import Node, Flow
from utils import call_llm

class TriggerTranslationsNode(Node):
    async def prep(self, shared):
        text = getattr(shared, "text", "(No text provided)")
        languages = getattr(shared, "languages", ["Chinese", "Spanish", "Japanese", "German", 
                              "Russian", "Portuguese", "French", "Korean"])
        
        return [(text, lang) for lang in languages]
    
    async def post(self, memory, prep_res, exec_res):
        for index, input in enumerate(prep_res):
            self.trigger("default", {"index": index, "data": input})
            

class TranslateTextNode(Node):
    async def prep(self, memory):
        return memory.index, memory.data            

    async def exec(self, data_tuple):
        index, (text, language) = data_tuple

        prompt = f"""
Please translate the following markdown file into {language}. 
But keep the original markdown format, links and code blocks.
Directly return the translated text, without any other text or comments.

Original: 
{text}

Translated:"""
        
        result = call_llm(prompt)
        print(f"Translated {language} text")
        return {"language": language, "translation": result}

    async def post(self, shared, prep_res, result):
        if not isinstance(result, dict):
            print(f"Warning: Invalid result received: {result}")
            return

        # Create output directory if it doesn't exist
        output_dir = getattr(shared, "output_dir", "translations")
        os.makedirs(output_dir, exist_ok=True)
        
        # Write each translation to a file
        language, translation = result["language"], result["translation"]
        
        # Write to file
        filename = os.path.join(output_dir, f"README_{language.upper()}.md")
        with open(filename, "w", encoding="utf-8") as f:
            f.write(translation)
        
        print(f"Saved translation to {filename}")

async def main():
    # read the text from ../../README.md
    with open("../../README.md", "r") as f:
        text = f.read()
    
    # Default settings
    shared = {
        "text": text,
        "languages": ["Chinese", "Spanish", "Japanese", "German", "Russian", "Portuguese", "French", "Korean"],
        "output_dir": "translations"
    }

    # --- Time Measurement Start ---
    print(f"Starting sequential translation into {len(shared['languages'])} languages...")
    start_time = time.perf_counter()

    # Run the translation flow
    trigger_node = TriggerTranslationsNode(max_retries=3)
    translate_node = TranslateTextNode(max_retries=3)
    trigger_node >> translate_node
    flow = Flow(start=trigger_node)
    await flow.run(shared)

    # --- Time Measurement End ---
    end_time = time.perf_counter()
    duration = end_time - start_time

    print(f"\nTotal sequential translation time: {duration:.4f} seconds") # Print duration
    print("\n=== Translation Complete ===")
    print(f"Translations saved to: {shared['output_dir']}")
    print("============================")

if __name__ == "__main__":
    asyncio.run(main())