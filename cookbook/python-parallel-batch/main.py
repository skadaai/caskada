import asyncio
import time
import os
from brainyflow import ParallelFlow, Node
from utils import call_llm

# --- Node Definitions ---

class TriggerTranslationsNode(Node):
    """Triggers translation of README files into multiple languages in parallel."""
    async def prep(self, shared):
        """Reads text and target languages from shared store."""
        text = getattr(shared, "text", "(No text provided)")
        languages = getattr(shared, "languages", [])
        return [(text, lang) for lang in languages]

    async def post(self, memory, prep_res, exec_res):
        for index, input in enumerate(prep_res):
            self.trigger("default", {"index": index, "data": input})


class TranslateTextNodeParallel(Node):
    """Translates text into multiple languages in parallel and saves files."""
    async def prep(self, memory):
        return memory.index, memory.data            


    async def exec(self, data_tuple):
        """Calls the async LLM utility for each target language."""
        index, (text, language) = data_tuple
        
        prompt = f"""
Please translate the following markdown file into {language}. 
But keep the original markdown format, links and code blocks.
Directly return the translated text, without any other text or comments.

Original: 
{text}

Translated:"""
        
        result = await call_llm(prompt)
        print(f"Translated {language} text")
        return {"language": language, "translation": result}

    async def post(self, shared, prep_res, result):
        """Stores the dictionary of {language: translation} pairs and writes to files."""
        if not isinstance(result, dict):
            print(f"Warning: Invalid result received: {result}")
            return
        
        output_dir = getattr(shared, "output_dir", "translations")
        os.makedirs(output_dir, exist_ok=True)
        
        language, translation = result["language"], result["translation"]
        
        filename = os.path.join(output_dir, f"README_{language.upper()}.md")
        try:
            import aiofiles
            async with aiofiles.open(filename, "w", encoding="utf-8") as f:
                await f.write(translation)
            print(f"Saved translation to {filename}")
        except ImportError:
            with open(filename, "w", encoding="utf-8") as f:
                f.write(translation)
            print(f"Saved translation to {filename} (sync fallback)")
        except Exception as e:
            print(f"Error writing file {filename}: {e}")

# --- Flow Creation ---

def create_parallel_translation_flow():
    """Creates and returns the parallel translation flow."""
    trigger_node = TriggerTranslationsNode()
    translate_node = TranslateTextNodeParallel(max_retries=3)
    trigger_node >> translate_node
    return ParallelFlow(start=trigger_node)

# --- Main Execution ---

async def main():
    source_readme_path = "../../README.md"
    try:
        with open(source_readme_path, "r", encoding='utf-8') as f:
            text = f.read()
    except FileNotFoundError:
        print(f"Error: Could not find the source README file at {source_readme_path}")
        exit(1)
    except Exception as e:
        print(f"Error reading file {source_readme_path}: {e}")
        exit(1)

    shared = {
        "text": text,
        "languages": ["Chinese", "Spanish", "Japanese", "German", "Russian", "Portuguese", "French", "Korean"],
        "output_dir": "translations"
    }

    translation_flow = create_parallel_translation_flow()

    print(f"Starting parallel translation into {len(shared['languages'])} languages...")
    start_time = time.perf_counter()

    await translation_flow.run(shared)

    end_time = time.perf_counter()
    duration = end_time - start_time
    print(f"\nTotal parallel translation time: {duration:.4f} seconds")
    print("\n=== Translation Complete ===")
    print(f"Translations saved to: {shared['output_dir']}")
    print("============================")

if __name__ == "__main__":
    asyncio.run(main()) 