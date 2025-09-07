---
machine-display: false
---

# Text Chunking

{% hint style="warning" %}

**Caskada does NOT provide built-in utilities**

Instead, we offer examples that you can implement yourself. This approach gives you [more flexibility and control](./index.md#why-not-built-in) over your project's dependencies and functionality.

{% endhint %}

We recommend some implementations of commonly used text chunking approaches.

{% hint style="success" %}
Text Chunking is more a micro optimization, compared to the Flow Design.

It's recommended to start with the Naive Chunking and optimize later.
{% endhint %}

---

## Example Python Code Samples

### 1. Naive (Fixed-Size) Chunking

Splits text by a fixed number of characters (not words, as the Python example implies), ignoring sentence or semantic boundaries.

{% tabs %}
{% tab title="Python" %}

```python
def fixed_size_chunk(text: str, chunk_size: int = 100) -> list[str]:
    """Splits text into fixed-size chunks based on character count."""
    chunks = []
    for i in range(0, len(text), chunk_size):
        chunks.append(text[i : i + chunk_size])
    return chunks

# Example:
# text = "This is a sample text to demonstrate fixed-size chunking."
# chunks = fixed_size_chunk(text, 20)
# print(chunks)
# Output: ['This is a sample tex', 't to demonstrate fix', 'ed-size chunking.']
```

{% endtab %}

{% tab title="TypeScript" %}

```typescript
function fixedSizeChunk(text: string, chunkSize: number = 100): string[] {
  /** Splits text into fixed-size chunks based on character count. */
  const chunks: string[] = []
  for (let i = 0; i < text.length; i += chunkSize) {
    chunks.push(text.slice(i, i + chunkSize))
  }
  return chunks
}

// Example:
// const text = "This is a sample text to demonstrate fixed-size chunking.";
// const chunks = fixedSizeChunk(text, 20);
// console.log(chunks);
// Output: [ 'This is a sample tex', 't to demonstrate fix', 'ed-size chunking.' ]
```

{% endtab %}
{% endtabs %}

However, sentences are often cut awkwardly, losing coherence.

### 2. Sentence-Based Chunking

Groups a fixed number of sentences together. Requires a sentence tokenizer library.

{% tabs %}
{% tab title="Python" %}

```python
import nltk # Requires: pip install nltk

# Ensure NLTK data is downloaded (run once)
# try:
#     nltk.data.find('tokenizers/punkt')
# except nltk.downloader.DownloadError:
#     nltk.download('punkt')

def sentence_based_chunk(text: str, max_sentences: int = 2) -> list[str]:
    """Chunks text by grouping a maximum number of sentences."""
    try:
        sentences = nltk.sent_tokenize(text)
    except LookupError:
        print("NLTK 'punkt' tokenizer not found. Please run nltk.download('punkt')")
        return [] # Or handle error appropriately

    chunks = []
    for i in range(0, len(sentences), max_sentences):
        chunks.append(" ".join(sentences[i : i + max_sentences]))
    return chunks

# Example:
# text = "Mr. Smith went to Washington. He visited the White House. Then he went home."
# chunks = sentence_based_chunk(text, 2)
# print(chunks)
# Output: ['Mr. Smith went to Washington. He visited the White House.', 'Then he went home.']
```

{% endtab %}

{% tab title="TypeScript" %}

```typescript
// Requires a sentence tokenizer library, e.g., 'sentence-tokenizer'
// npm install sentence-tokenizer
import { Tokenizer } from 'sentence-tokenizer'

function sentenceBasedChunk(text: string, maxSentences: number = 2): string[] {
  /** Chunks text by grouping a maximum number of sentences. */
  const tokenizer = new Tokenizer('Chuck') // Identifier doesn't matter much here
  tokenizer.setEntry(text)
  const sentences = tokenizer.getSentences()

  const chunks: string[] = []
  for (let i = 0; i < sentences.length; i += maxSentences) {
    chunks.push(sentences.slice(i, i + maxSentences).join(' '))
  }
  return chunks
}

// Example:
// const text = "Mr. Smith went to Washington. He visited the White House. Then he went home.";
// const chunks = sentenceBasedChunk(text, 2);
// console.log(chunks);
// Output: [ 'Mr. Smith went to Washington. He visited the White House.', 'Then he went home.' ]
```

{% endtab %}
{% endtabs %}

However, might not handle very long sentences or paragraphs well.

### 3. Other Chunking

- **Paragraph-Based**: Split text by paragraphs (e.g., newlines). Large paragraphs can create big chunks.
- **Semantic**: Use embeddings or topic modeling to chunk by semantic boundaries.
- **Agentic**: Use an LLM to decide chunk boundaries based on context or meaning.
