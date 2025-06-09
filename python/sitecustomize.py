import functools
import inspect
import os
from openai import OpenAI

from extras.brainyflow_extras import enhance, setup

setup(
    show_locals_in_traceback=False,
    smart_print_options={
        "single_line": True,
    }
)

enhanced_components = enhance(
    verbose=True,
    file_logging={'log_folder': '.logs'},
    performance=True,
    execution_tree=True,
)

@functools.wraps(OpenAI)
def custom_OpenAI(*args, **kwargs):
    kwargs["base_url"] = "https://openrouter.ai/api/v1"
    kwargs["api_key"] = os.environ.get("OPENROUTER_API_KEY")

    return OpenAI(
        *args,
        **kwargs,
    )


def call_llm(input: str | list):    
    r = custom_OpenAI().chat.completions.create(
        model="deepseek/deepseek-chat-v3-0324:free",
        # model="meta-llama/llama-4-maverick:free",
        messages=[{"role": "user", "content": input}] if isinstance(input, str) else input
    )
    return r.choices[0].message.content

async def async_call_llm(*args, **kwargs):
    return call_llm(*args, **kwargs)

def get_embedding(text):
    from light_embed import TextEmbedding

    model = TextEmbedding(model_name_or_path='sentence-transformers/all-MiniLM-L6-v2')
    embeddings = model.encode([text])
    return embeddings[0]


# -------------------------------------------------------------------------------------------------------------

import os
import sys

# Original import hook
original_import = __import__


# Custom import function
def custom_import(name, globals=None, locals=None, fromlist=(), level=0):
    # First, use the original import
    module = original_import(name, globals, locals, fromlist, level)

    if 'ipykernel' in sys.modules or 'IPython' in sys.modules:
        # skip patching in Jupyter environments
        return module
    
    if "OPENROUTER_API_KEY" in os.environ:
        # If it's the utils module, patch it
        if name in ['utils', 'utils.call_llm'] and hasattr(module, 'call_llm'):
            # Save original if needed
            if not hasattr(module.call_llm, '_original'):
                module.call_llm._original = module.call_llm
            
            # Replace it
            if inspect.iscoroutinefunction(module.call_llm):
                module.call_llm = async_call_llm
            else:
                module.call_llm = call_llm

        if name in ['utils', 'utils.get_embedding', 'tools', 'tools.embeddings'] and hasattr(module, 'get_embedding'):
            if not hasattr(module.get_embedding, '_original'):
                module.get_embedding._original = module.get_embedding
            
            module.get_embedding = get_embedding
                

        if name == "openai" and hasattr(module, 'OpenAI'):
            if not hasattr(module.OpenAI, '_original'):
                module.OpenAI._original = module.OpenAI
            
            module.OpenAI = custom_OpenAI


    if name == 'brainyflow':
        if not hasattr(module.Memory, '_original'):
            module.Memory._original = module.Memory
        
        module.Memory = enhanced_components.Memory

    if name == 'brainyflow' and hasattr(module, 'Node'):
        if not hasattr(module.Node, '_original'):
            module.Node._original = module.Node
        
        module.Node = enhanced_components.Node


    if name == 'brainyflow' and hasattr(module, 'Flow'):
        if not hasattr(module.Flow, '_original'):
            module.Flow._original = module.Flow
        
        module.Flow = enhanced_components.Flow

    return module

# Replace the built-in import function
__builtins__['__import__'] = custom_import

print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> brainyflow, utils, and tools have been patched globally <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")