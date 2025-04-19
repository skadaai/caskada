---
machine-display: false
---

# Embedding

{% hint style="warning" %}

**BrainyFlow does NOT provide built-in utilities**

Instead, we offer examples that you can implement yourself. This approach gives you [more flexibility and control](./index.md#why-not-built-in) over your project's dependencies and functionality.

{% endhint %}

Below you will find an overview table of various text embedding APIs, along with example Python code.

{% hint style="success" %}
Embedding is more a micro optimization, compared to the Flow Design.

It's recommended to start with the most convenient one and optimize later.
{% endhint %}

| **API**              | **Free Tier**                           | **Pricing Model**                   | **Docs**                                                                                                                  |
| -------------------- | --------------------------------------- | ----------------------------------- | ------------------------------------------------------------------------------------------------------------------------- |
| **OpenAI**           | ~$5 credit                              | ~$0.0001/1K tokens                  | [OpenAI Embeddings](https://platform.openai.com/docs/api-reference/embeddings)                                            |
| **Azure OpenAI**     | $200 credit                             | Same as OpenAI (~$0.0001/1K tokens) | [Azure OpenAI Embeddings](https://learn.microsoft.com/azure/cognitive-services/openai/how-to/create-resource?tabs=portal) |
| **Google Vertex AI** | $300 credit                             | ~$0.025 / million chars             | [Vertex AI Embeddings](https://cloud.google.com/vertex-ai/docs/generative-ai/embeddings/get-text-embeddings)              |
| **AWS Bedrock**      | No free tier, but AWS credits may apply | ~$0.00002/1K tokens (Titan V2)      | [Amazon Bedrock](https://docs.aws.amazon.com/bedrock/)                                                                    |
| **Cohere**           | Limited free tier                       | ~$0.0001/1K tokens                  | [Cohere Embeddings](https://docs.cohere.com/docs/cohere-embed)                                                            |
| **Hugging Face**     | ~$0.10 free compute monthly             | Pay per second of compute           | [HF Inference API](https://huggingface.co/docs/api-inference)                                                             |
| **Jina**             | 1M tokens free                          | Pay per token after                 | [Jina Embeddings](https://jina.ai/embeddings/)                                                                            |

## Example Code

### 1. OpenAI

{% tabs %}
{% tab title="Python" %}

```python
# Requires: pip install openai numpy
import os
import numpy as np
from openai import OpenAI

def get_openai_embedding(text: str, model: str = "text-embedding-3-small") -> np.ndarray | None:
    """Gets embedding from OpenAI API."""
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        print("Error: OPENAI_API_KEY not set.")
        return None
    try:
        client = OpenAI(api_key=api_key)
        response = client.embeddings.create(
            model=model,
            input=text
        )
        embedding = response.data[0].embedding
        return np.array(embedding, dtype=np.float32)
    except Exception as e:
        print(f"Error calling OpenAI embedding API: {e}")
        return None

# Example:
# text_to_embed = "Hello world"
# embedding_vector = get_openai_embedding(text_to_embed)
# if embedding_vector is not None:
#     print(embedding_vector)
#     print(f"Dimension: {len(embedding_vector)}")

```

{% endtab %}

{% tab title="TypeScript" %}

```typescript
// Requires: npm install openai
import OpenAI from 'openai'

async function getOpenaiEmbedding(
  text: string,
  model: string = 'text-embedding-3-small',
): Promise<number[] | null> {
  /** Gets embedding from OpenAI API. */
  const apiKey = process.env.OPENAI_API_KEY
  if (!apiKey) {
    console.error('Error: OPENAI_API_KEY not set.')
    return null
  }
  try {
    const openai = new OpenAI({ apiKey })
    const response = await openai.embeddings.create({
      model,
      input: text,
    })
    return response.data[0]?.embedding ?? null
  } catch (error) {
    console.error('Error calling OpenAI embedding API:', error)
    return null
  }
}

// Example:
// const textToEmbed = "Hello world";
// getOpenaiEmbedding(textToEmbed).then(embedding => {
//   if (embedding) {
//     console.log(embedding);
//     console.log(`Dimension: ${embedding.length}`);
//   }
// });
```

{% endtab %}
{% endtabs %}

### 2. Azure OpenAI

{% tabs %}
{% tab title="Python" %}

```python
# Requires: pip install openai numpy
import os
import numpy as np
from openai import AzureOpenAI

def get_azure_openai_embedding(text: str, deployment_name: str = "your-embedding-deployment") -> np.ndarray | None:
    """Gets embedding from Azure OpenAI API."""
    api_key = os.environ.get("AZURE_OPENAI_API_KEY")
    azure_endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT")
    api_version = "2023-05-15" # Example version, adjust as needed

    if not api_key or not azure_endpoint:
        print("Error: AZURE_OPENAI_API_KEY or AZURE_OPENAI_ENDPOINT not set.")
        return None
    try:
        client = AzureOpenAI(
            api_key=api_key,
            azure_endpoint=azure_endpoint,
            api_version=api_version
        )
        response = client.embeddings.create(
            model=deployment_name, # Use your deployment name
            input=text
        )
        embedding = response.data[0].embedding
        return np.array(embedding, dtype=np.float32)
    except Exception as e:
        print(f"Error calling Azure OpenAI embedding API: {e}")
        return None

# Example:
# text_to_embed = "Hello world"
# embedding_vector = get_azure_openai_embedding(text_to_embed, deployment_name="my-text-embedding-ada-002")
# if embedding_vector is not None:
#     print(embedding_vector)

```

{% endtab %}

{% tab title="TypeScript" %}

```typescript
// Requires: npm install @azure/openai
import { AzureKeyCredential, OpenAIClient } from '@azure/openai'

async function getAzureOpenaiEmbedding(
  text: string,
  deploymentName: string = 'your-embedding-deployment',
): Promise<number[] | null> {
  /** Gets embedding from Azure OpenAI API. */
  const apiKey = process.env.AZURE_OPENAI_API_KEY
  const endpoint = process.env.AZURE_OPENAI_ENDPOINT

  if (!apiKey || !endpoint) {
    console.error('Error: AZURE_OPENAI_API_KEY or AZURE_OPENAI_ENDPOINT not set.')
    return null
  }

  try {
    const client = new OpenAIClient(endpoint, new AzureKeyCredential(apiKey))
    const result = await client.getEmbeddings(deploymentName, [text]) // Input must be an array
    return result.data[0]?.embedding ?? null
  } catch (error) {
    console.error('Error calling Azure OpenAI embedding API:', error)
    return null
  }
}

// Example:
// const textToEmbed = "Hello world";
// getAzureOpenaiEmbedding(textToEmbed, "my-text-embedding-ada-002").then(embedding => {
//   if (embedding) {
//     console.log(embedding);
//   }
// });
```

{% endtab %}
{% endtabs %}

### 3. Google Vertex AI

{% tabs %}
{% tab title="Python" %}

```python
# Requires: pip install google-cloud-aiplatform numpy
import os
import numpy as np
from google.cloud import aiplatform
from google.cloud.aiplatform.gapic.schema import predict

def get_vertex_embedding(text: str, project_id: str | None = None, location: str = "us-central1", model_name: str = "textembedding-gecko@001") -> np.ndarray | None:
    """Gets embedding from Google Vertex AI."""
    project_id = project_id or os.environ.get("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        print("Error: GOOGLE_CLOUD_PROJECT not set and project_id not provided.")
        return None

    try:
        aiplatform.init(project=project_id, location=location)
        endpoint = aiplatform.Endpoint(f"projects/{project_id}/locations/{location}/publishers/google/models/{model_name}")

        instance = predict.instance.TextEmbeddingInstance(content=text).to_value()
        instances = [instance]
        response = endpoint.predict(instances=instances)

        embedding = response.predictions[0]['embeddings']['values']
        return np.array(embedding, dtype=np.float32)
    except Exception as e:
        print(f"Error calling Vertex AI embedding API: {e}")
        return None

# Example:
# text_to_embed = "Hello world"
# embedding_vector = get_vertex_embedding(text_to_embed)
# if embedding_vector is not None:
#     print(embedding_vector)

```

{% endtab %}

{% tab title="TypeScript" %}

```typescript
// Requires: npm install @google-cloud/aiplatform
const { PredictionServiceClient } = require('@google-cloud/aiplatform').v1
const { helpers } = require('@google-cloud/aiplatform') // Or use import

async function getVertexEmbedding(
  text: string,
  projectId: string | undefined = process.env.GOOGLE_CLOUD_PROJECT,
  location: string = 'us-central1',
  modelName: string = 'textembedding-gecko@001',
): Promise<number[] | null> {
  /** Gets embedding from Google Vertex AI. */
  if (!projectId) {
    console.error('Error: GOOGLE_CLOUD_PROJECT not set and projectId not provided.')
    return null
  }

  const clientOptions = { apiEndpoint: `${location}-aiplatform.googleapis.com` }
  const client = new PredictionServiceClient(clientOptions)

  const endpoint = `projects/${projectId}/locations/${location}/publishers/google/models/${modelName}`
  const instance = helpers.toValue({ content: text }) // Convert JSON object to Value proto
  const instances = [instance]
  const parameters = helpers.toValue({}) // No parameters needed for this model

  const request = { endpoint, instances, parameters }

  try {
    const [response] = await client.predict(request)
    const embeddings =
      response.predictions?.[0]?.structValue?.fields?.embeddings?.structValue?.fields?.values
        ?.listValue?.values
    if (!embeddings) {
      console.error('Invalid response structure from Vertex AI.')
      return null
    }
    // Convert Value protos back to numbers
    return embeddings.map((val: any) => val.numberValue)
  } catch (error) {
    console.error('Error calling Vertex AI embedding API:', error)
    return null
  }
}

// Example:
// const textToEmbed = "Hello world";
// getVertexEmbedding(textToEmbed).then(embedding => {
//   if (embedding) {
//     console.log(embedding);
//   }
// });
```

{% endtab %}
{% endtabs %}

### 4. AWS Bedrock

{% tabs %}
{% tab title="Python" %}

```python
# Requires: pip install boto3 numpy
import boto3
import json
import numpy as np
import os

def get_bedrock_embedding(text: str, region_name: str | None = None, model_id: str = "amazon.titan-embed-text-v2:0") -> np.ndarray | None:
    """Gets embedding from AWS Bedrock."""
    region = region_name or os.environ.get("AWS_REGION", "us-east-1")
    try:
        # Ensure AWS credentials are configured (e.g., via env vars, ~/.aws/credentials)
        client = boto3.client("bedrock-runtime", region_name=region)
        body = json.dumps({"inputText": text})
        response = client.invoke_model(
            modelId=model_id,
            contentType="application/json",
            accept="application/json",
            body=body
        )
        response_body = json.loads(response['body'].read())
        embedding = response_body.get('embedding')
        if embedding:
            return np.array(embedding, dtype=np.float32)
        else:
            print("Error: Embedding not found in Bedrock response.")
            return None
    except Exception as e:
        print(f"Error calling AWS Bedrock embedding API: {e}")
        return None

# Example:
# text_to_embed = "Hello world"
# embedding_vector = get_bedrock_embedding(text_to_embed)
# if embedding_vector is not None:
#     print(embedding_vector)

```

{% endtab %}

{% tab title="TypeScript" %}

```typescript
// Requires: npm install @aws-sdk/client-bedrock-runtime
import { BedrockRuntimeClient, InvokeModelCommand } from '@aws-sdk/client-bedrock-runtime'

async function getBedrockEmbedding(
  text: string,
  region: string = process.env.AWS_REGION ?? 'us-east-1',
  modelId: string = 'amazon.titan-embed-text-v2:0',
): Promise<number[] | null> {
  /** Gets embedding from AWS Bedrock. */
  // Ensure AWS credentials are configured (e.g., via env vars, instance profile)
  const client = new BedrockRuntimeClient({ region })
  const body = JSON.stringify({ inputText: text })

  const command = new InvokeModelCommand({
    modelId,
    contentType: 'application/json',
    accept: 'application/json',
    body,
  })

  try {
    const response = await client.send(command)
    // Decode the Uint8Array response body
    const responseBodyString = new TextDecoder().decode(response.body)
    const responseBody = JSON.parse(responseBodyString)
    return responseBody.embedding ?? null
  } catch (error) {
    console.error('Error calling AWS Bedrock embedding API:', error)
    return null
  }
}

// Example:
// const textToEmbed = "Hello world";
// getBedrockEmbedding(textToEmbed).then(embedding => {
//   if (embedding) {
//     console.log(embedding);
//   }
// });
```

{% endtab %}
{% endtabs %}

### 5. Cohere

{% tabs %}
{% tab title="Python" %}

```python
# Requires: pip install cohere numpy
import cohere
import os
import numpy as np

def get_cohere_embedding(text: str, model: str = "embed-english-v3.0") -> np.ndarray | None:
    """Gets embedding from Cohere API."""
    api_key = os.environ.get("COHERE_API_KEY")
    if not api_key:
        print("Error: COHERE_API_KEY not set.")
        return None
    try:
        co = cohere.Client(api_key)
        # Cohere API expects a list of texts
        response = co.embed(texts=[text], model=model, input_type="search_document") # Adjust input_type as needed
        embedding = response.embeddings[0]
        return np.array(embedding, dtype=np.float32)
    except Exception as e:
        print(f"Error calling Cohere embedding API: {e}")
        return None

# Example:
# text_to_embed = "Hello world"
# embedding_vector = get_cohere_embedding(text_to_embed)
# if embedding_vector is not None:
#     print(embedding_vector)

```

{% endtab %}

{% tab title="TypeScript" %}

```typescript
// Requires: npm install cohere-ai
import { CohereClient } from 'cohere-ai'

async function getCohereEmbedding(
  text: string,
  model: string = 'embed-english-v3.0',
): Promise<number[] | null> {
  /** Gets embedding from Cohere API. */
  const apiKey = process.env.COHERE_API_KEY
  if (!apiKey) {
    console.error('Error: COHERE_API_KEY not set.')
    return null
  }
  try {
    const cohere = new CohereClient({ token: apiKey })
    const response = await cohere.embed({
      texts: [text],
      model: model,
      inputType: 'search_document', // Adjust as needed
    })
    // Cohere TS SDK might return Float64Array, ensure conversion if needed elsewhere
    return response.embeddings?.[0] ? Array.from(response.embeddings[0]) : null
  } catch (error) {
    console.error('Error calling Cohere embedding API:', error)
    return null
  }
}

// Example:
// const textToEmbed = "Hello world";
// getCohereEmbedding(textToEmbed).then(embedding => {
//   if (embedding) {
//     console.log(embedding);
//   }
// });
```

{% endtab %}
{% endtabs %}

### 6. Hugging Face Inference API

{% tabs %}
{% tab title="Python" %}

```python
# Requires: pip install requests numpy
import requests
import os
import numpy as np

def get_hf_embedding(text: str, model_url: str = "https://api-inference.huggingface.co/models/sentence-transformers/all-MiniLM-L6-v2") -> np.ndarray | None:
    """Gets embedding from Hugging Face Inference API."""
    hf_token = os.environ.get("HUGGINGFACE_TOKEN")
    if not hf_token:
        print("Warning: HUGGINGFACE_TOKEN not set. Public models might work without it.")
        # Allow proceeding without token for public models, but auth is recommended

    headers = {"Authorization": f"Bearer {hf_token}"} if hf_token else {}
    payload = {"inputs": text}

    try:
        response = requests.post(model_url, headers=headers, json=payload)
        response.raise_for_status()
        # The response structure might vary; often it's a list of embeddings
        # For sentence-transformers, it's usually [[embedding]]
        embedding_list = response.json()
        if isinstance(embedding_list, list) and len(embedding_list) > 0 and isinstance(embedding_list[0], list):
             return np.array(embedding_list[0], dtype=np.float32)
        elif isinstance(embedding_list, list) and len(embedding_list) > 0 and isinstance(embedding_list[0], float):
             # Some models might return a flat list for single input
             return np.array(embedding_list, dtype=np.float32)
        else:
             print(f"Unexpected response structure from HF API: {embedding_list}")
             return None
    except requests.exceptions.RequestException as e:
        print(f"Error calling Hugging Face Inference API: {e}")
        return None
    except Exception as e:
        print(f"Error processing Hugging Face response: {e}")
        return None


# Example:
# text_to_embed = "Hello world"
# embedding_vector = get_hf_embedding(text_to_embed)
# if embedding_vector is not None:
#     print(embedding_vector)

```

{% endtab %}

{% tab title="TypeScript" %}

```typescript
async function getHfEmbedding(
  text: string,
  modelUrl: string = 'https://api-inference.huggingface.co/models/sentence-transformers/all-MiniLM-L6-v2',
): Promise<number[] | null> {
  /** Gets embedding from Hugging Face Inference API. */
  const hfToken = process.env.HUGGINGFACE_TOKEN
  const headers: HeadersInit = { 'Content-Type': 'application/json' }
  if (hfToken) {
    headers['Authorization'] = `Bearer ${hfToken}`
  } else {
    console.warn('Warning: HUGGINGFACE_TOKEN not set. Public models might work without it.')
  }

  const payload = JSON.stringify({ inputs: text })

  try {
    const response = await fetch(modelUrl, {
      method: 'POST',
      headers: headers,
      body: payload,
    })

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}, message: ${await response.text()}`)
    }

    const result = await response.json()
    // Handle potential variations in response structure
    if (Array.isArray(result) && result.length > 0 && Array.isArray(result[0])) {
      return result[0] // Common case for sentence-transformers
    } else if (Array.isArray(result) && result.length > 0 && typeof result[0] === 'number') {
      return result // Flat list for single input
    } else {
      console.error('Unexpected response structure from HF API:', result)
      return null
    }
  } catch (error) {
    console.error('Error calling Hugging Face Inference API:', error)
    return null
  }
}

// Example:
// const textToEmbed = "Hello world";
// getHfEmbedding(textToEmbed).then(embedding => {
//   if (embedding) {
//     console.log(embedding);
//   }
// });
```

{% endtab %}
{% endtabs %}

### 7. Jina AI

{% tabs %}
{% tab title="Python" %}

```python
# Requires: pip install requests numpy
import requests
import os
import numpy as np

def get_jina_embedding(text: str, model: str = "jina-embeddings-v2-base-en") -> np.ndarray | None:
    """Gets embedding from Jina AI API."""
    jina_token = os.environ.get("JINA_API_KEY") # Or JINA_TOKEN depending on convention
    if not jina_token:
        print("Error: JINA_API_KEY not set.")
        return None

    url = "https://api.jina.ai/v1/embeddings" # Use v1 endpoint
    headers = {
        "Authorization": f"Bearer {jina_token}",
        "Accept-Encoding": "identity", # Recommended by Jina docs
        "Content-Type": "application/json"
    }
    payload = {
        "input": [text], # API expects a list
        "model": model
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        result = response.json()
        embedding = result["data"][0]["embedding"]
        return np.array(embedding, dtype=np.float32)
    except requests.exceptions.RequestException as e:
        print(f"Error calling Jina AI embedding API: {e}")
        return None
    except (KeyError, IndexError) as e:
        print(f"Error parsing Jina AI response: {e}, Response: {response.text}")
        return None

# Example:
# text_to_embed = "Hello world"
# embedding_vector = get_jina_embedding(text_to_embed)
# if embedding_vector is not None:
#     print(embedding_vector)

```

{% endtab %}

{% tab title="TypeScript" %}

```typescript
async function getJinaEmbedding(
  text: string,
  model: string = 'jina-embeddings-v2-base-en',
): Promise<number[] | null> {
  /** Gets embedding from Jina AI API. */
  const jinaToken = process.env.JINA_API_KEY // Or JINA_TOKEN
  if (!jinaToken) {
    console.error('Error: JINA_API_KEY not set.')
    return null
  }

  const url = 'https://api.jina.ai/v1/embeddings' // Use v1 endpoint
  const headers: HeadersInit = {
    Authorization: `Bearer ${jinaToken}`,
    'Accept-Encoding': 'identity',
    'Content-Type': 'application/json',
  }
  const payload = JSON.stringify({
    input: [text], // API expects a list
    model: model,
  })

  try {
    const response = await fetch(url, {
      method: 'POST',
      headers: headers,
      body: payload,
    })

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}, message: ${await response.text()}`)
    }

    const result = await response.json()
    const embedding = result?.data?.[0]?.embedding

    if (!embedding || !Array.isArray(embedding)) {
      console.error('Error parsing Jina AI response:', result)
      return null
    }
    return embedding
  } catch (error) {
    console.error('Error calling Jina AI embedding API:', error)
    return null
  }
}

// Example:
// const textToEmbed = "Hello world";
// getJinaEmbedding(textToEmbed).then(embedding => {
//   if (embedding) {
//     console.log(embedding);
//   }
// });
```

{% endtab %}
{% endtabs %}
