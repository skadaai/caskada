---
machine-display: false
---

# Vector Databases

{% hint style="warning" %}

**Caskada does NOT provide built-in utilities**

Instead, we offer examples that you can implement yourself. This approach gives you [more flexibility and control](./index.md#why-not-built-in) over your project's dependencies and functionality.

{% endhint %}

Below is a table of the popular vector search solutions:

| **Tool**     | **Free Tier**  | **Pricing Model**        | **Docs**                               |
| ------------ | -------------- | ------------------------ | -------------------------------------- |
| **FAISS**    | N/A, self-host | Open-source              | [Faiss.ai](https://faiss.ai)           |
| **Pinecone** | 2GB free       | From $25/mo              | [pinecone.io](https://pinecone.io)     |
| **Qdrant**   | 1GB free cloud | Pay-as-you-go            | [qdrant.tech](https://qdrant.tech)     |
| **Weaviate** | 14-day sandbox | From $25/mo              | [weaviate.io](https://weaviate.io)     |
| **Milvus**   | 5GB free cloud | PAYG or $99/mo dedicated | [milvus.io](https://milvus.io)         |
| **Chroma**   | N/A, self-host | Free (Apache 2.0)        | [trychroma.com](https://trychroma.com) |
| **Redis**    | 30MB free      | From $5/mo               | [redis.io](https://redis.io)           |

---

## Example Code

Below are basic usage snippets for each tool.

### 1. FAISS (Facebook AI Similarity Search)

FAISS is primarily a C++ library with Python bindings, optimized for performance. It's typically used for in-memory indexing or self-hosted scenarios. Direct usage from Node.js/TypeScript is less common without a dedicated server or WASM compilation.

{% tabs %}
{% tab title="Python" %}

```python
# Requires: pip install faiss-cpu # or faiss-gpu
import faiss
import numpy as np
from typing import List, Tuple, Any # Added for type hints

def create_faiss_index(dimension: int) -> faiss.Index:
    """Creates a simple FAISS index."""
    # Example: Flat L2 index
    index = faiss.IndexFlatL2(dimension)
    return index

def add_to_faiss_index(index: faiss.Index, vectors: np.ndarray):
    """Adds vectors to the FAISS index."""
    # Ensure vectors are float32
    if vectors.dtype != 'float32':
        vectors = vectors.astype('float32')
    index.add(vectors)

def search_faiss_index(index: faiss.Index, query_vector: np.ndarray, top_k: int = 5) -> Tuple[np.ndarray, np.ndarray]:
    """Searches the FAISS index."""
    if query_vector.dtype != 'float32':
        query_vector = query_vector.astype('float32')
    # Ensure query is 2D array
    if query_vector.ndim == 1:
        query_vector = np.array([query_vector])
    distances, indices = index.search(query_vector, top_k)
    return distances, indices

# Example Usage:
# d = 128 # Dimensionality of embeddings
# index = create_faiss_index(d)
# print(f"Index created. Is trained: {index.is_trained}, Total vectors: {index.ntotal}")

# data_vectors = np.random.random((1000, d)).astype('float32')
# add_to_faiss_index(index, data_vectors)
# print(f"Added {data_vectors.shape[0]} vectors. Total vectors: {index.ntotal}")

# query = np.random.random((1, d)).astype('float32')
# D, I = search_faiss_index(index, query, k=5)

# print("Distances:", D)
# print("Neighbors:", I)

# In production, you would also add functions to:
# - save_index(index, filename) -> faiss.write_index(index, filename)
# - load_index(filename) -> faiss.read_index(filename)
```

{% endtab %}

{% tab title="TypeScript" %}

```typescript
// FAISS is primarily a C++/Python library.
// Direct usage in TypeScript often involves:
// 1. Calling a Python backend service that uses FAISS.
// 2. Using community-maintained WASM ports (may have limitations).
// 3. Using alternative JS-native vector search libraries like hnswlib-node.

// Example using hnswlib-node (conceptual - requires installation)
// npm install hnswlib-node
/*
import { HierarchicalNSW } from 'hnswlib-node';

async function exampleHNSW() {
  const dim = 128;
  const maxElements = 1000;

  // Initialize index
  const index = new HierarchicalNSW('l2', dim); // 'l2' for Euclidean distance
  index.initIndex(maxElements);

  // Add vectors (example data)
  for (let i = 0; i < maxElements; i++) {
    const vector = Array.from({ length: dim }, () => Math.random());
    index.addPoint(vector, i); // Add vector with its ID (index i)
  }

  // Query
  const queryVector = Array.from({ length: dim }, () => Math.random());
  const numNeighbors = 5;
  const result = index.searchKnn(queryVector, numNeighbors);

  console.log("HNSW Neighbors:", result.neighbors); // Indices
  console.log("HNSW Distances:", result.distances);
}

// exampleHNSW();
*/

console.log('FAISS is typically used via Python or a dedicated service.')
console.log(
  'Consider using a JS-native library like hnswlib-node or a managed vector DB for TypeScript projects.',
)
```

{% endtab %}
{% endtabs %}

### 2. Pinecone

{% tabs %}
{% tab title="Python" %}

```python
# Requires: pip install pinecone-client
import os
from pinecone import Pinecone, PodSpec

def init_pinecone() -> Pinecone | None:
    """Initializes Pinecone client."""
    api_key = os.environ.get("PINECONE_API_KEY")
    # environment = os.environ.get("PINECONE_ENVIRONMENT") # Legacy, use API key only
    if not api_key:
        print("Error: PINECONE_API_KEY not set.")
        return None
    try:
        # pc = Pinecone(api_key=api_key, environment=environment) # Legacy init
        pc = Pinecone(api_key=api_key)
        print("Pinecone initialized.")
        return pc
    except Exception as e:
        print(f"Error initializing Pinecone: {e}")
        return None

def create_pinecone_index_if_not_exists(pc: Pinecone, index_name: str, dimension: int, metric: str = 'cosine', environment: str = 'gcp-starter'):
    """Creates a Pinecone index if it doesn't exist."""
    if index_name not in pc.list_indexes().names:
        print(f"Creating index '{index_name}'...")
        try:
            pc.create_index(
                name=index_name,
                dimension=dimension,
                metric=metric,
                spec=PodSpec(environment=environment) # Specify environment here
            )
            print(f"Index '{index_name}' created.")
        except Exception as e:
            print(f"Error creating Pinecone index: {e}")
    else:
        print(f"Index '{index_name}' already exists.")

# Example Usage:
# pc = init_pinecone()
# if pc:
#     index_name = "my-brainyflow-index"
#     dimension = 128
#     create_pinecone_index_if_not_exists(pc, index_name, dimension)

#     # Connect to the index
#     try:
#         index = pc.Index(index_name)

#         # Upsert vectors
#         vectors_to_upsert = [
#             ("vec_id1", [0.1] * dimension, {"genre": "fiction"}), # With metadata
#             ("vec_id2", [0.2] * dimension, {"year": 2023})
#         ]
#         print(f"Upserting {len(vectors_to_upsert)} vectors...")
#         index.upsert(vectors=vectors_to_upsert)
#         print("Upsert complete.")

#         # Query
#         query_vector = [0.15] * dimension
#         print("Querying index...")
#         response = index.query(vector=query_vector, top_k=3, include_metadata=True)
#         print("Query response:", response)

#     except Exception as e:
#         print(f"Error interacting with Pinecone index: {e}")

```

{% endtab %}

{% tab title="TypeScript" %}

```typescript
// Requires: npm install @pinecone-database/pinecone
import { Pinecone, PodSpec } from '@pinecone-database/pinecone'

async function initPinecone(): Promise<Pinecone | null> {
  /** Initializes Pinecone client. */
  const apiKey = process.env.PINECONE_API_KEY
  if (!apiKey) {
    console.error('Error: PINECONE_API_KEY not set.')
    return null
  }
  try {
    const pc = new Pinecone({ apiKey }) // Use new init style
    console.log('Pinecone initialized.')
    return pc
  } catch (error) {
    console.error('Error initializing Pinecone:', error)
    return null
  }
}

async function createPineconeIndexIfNotExists(
  pc: Pinecone,
  indexName: string,
  dimension: number,
  metric: 'cosine' | 'euclidean' | 'dotproduct' = 'cosine',
  environment: string = 'gcp-starter', // Or your specific environment
): Promise<void> {
  /** Creates a Pinecone index if it doesn't exist. */
  try {
    const indexes = await pc.listIndexes()
    if (!indexes.names?.includes(indexName)) {
      console.log(`Creating index '${indexName}'...`)
      await pc.createIndex({
        name: indexName,
        dimension: dimension,
        metric: metric,
        spec: {
          pod: {
            // Use PodSpec structure
            environment: environment,
            podType: 'p1.x1', // Example pod type, adjust as needed
          },
        },
      })
      console.log(`Index '${indexName}' created.`)
      // Add a small delay for index readiness (optional but sometimes helpful)
      await new Promise((resolve) => setTimeout(resolve, 5000))
    } else {
      console.log(`Index '${indexName}' already exists.`)
    }
  } catch (error) {
    console.error(`Error creating or checking Pinecone index:`, error)
  }
}

// Example Usage:
/*
async function pineconeExample() {
    const pc = await initPinecone();
    if (!pc) return;

    const indexName = "my-brainyflow-index-ts";
    const dimension = 128;
    await createPineconeIndexIfNotExists(pc, indexName, dimension);

    try {
        const index = pc.index(indexName);

        // Upsert vectors
        const vectorsToUpsert = [
            { id: "ts_vec_id1", values: Array(dimension).fill(0.1), metadata: { genre: "fiction" } },
            { id: "ts_vec_id2", values: Array(dimension).fill(0.2), metadata: { year: 2023 } }
        ];
        console.log(`Upserting ${vectorsToUpsert.length} vectors...`);
        await index.upsert(vectorsToUpsert);
        console.log("Upsert complete.");

        // Query
        const queryVector = Array(dimension).fill(0.15);
        console.log("Querying index...");
        const response = await index.query({ vector: queryVector, topK: 3, includeMetadata: true });
        console.log("Query response:", response);

    } catch (error) {
        console.error("Error interacting with Pinecone index:", error);
    }
}

pineconeExample();
*/
```

{% endtab %}
{% endtabs %}

### 3. Qdrant

{% tabs %}
{% tab title="Python" %}

```python
# Requires: pip install qdrant-client
import os
import qdrant_client
from qdrant_client.http.models import Distance, VectorParams, PointStruct, CollectionStatus

def init_qdrant_client() -> qdrant_client.QdrantClient | None:
    """Initializes Qdrant client."""
    qdrant_url = os.environ.get("QDRANT_URL") # e.g., "http://localhost:6333" or cloud URL
    api_key = os.environ.get("QDRANT_API_KEY") # Optional, for cloud
    if not qdrant_url:
        print("Error: QDRANT_URL not set.")
        return None
    try:
        client = qdrant_client.QdrantClient(url=qdrant_url, api_key=api_key)
        print("Qdrant client initialized.")
        return client
    except Exception as e:
        print(f"Error initializing Qdrant client: {e}")
        return None

def create_qdrant_collection_if_not_exists(client: qdrant_client.QdrantClient, collection_name: str, dimension: int, distance_metric: Distance = Distance.COSINE):
    """Creates a Qdrant collection if it doesn't exist."""
    try:
        collections = client.get_collections().collections
        if not any(c.name == collection_name for c in collections):
            print(f"Creating collection '{collection_name}'...")
            client.recreate_collection( # Use recreate_collection for simplicity, or check/create
                collection_name=collection_name,
                vectors_config=VectorParams(size=dimension, distance=distance_metric)
            )
            print(f"Collection '{collection_name}' created.")
        else:
            print(f"Collection '{collection_name}' already exists.")
    except Exception as e:
        print(f"Error creating or checking Qdrant collection: {e}")


# Example Usage:
# client = init_qdrant_client()
# if client:
#     collection_name = "brainyflow_qdrant_demo"
#     dimension = 128
#     create_qdrant_collection_if_not_exists(client, collection_name, dimension)

#     try:
#         # Upsert points
#         points_to_upsert = [
#             # Use UUIDs or sequential integers for IDs
#             PointStruct(id=1, vector=[0.1] * dimension, payload={"type": "doc1", "source": "fileA.txt"}),
#             PointStruct(id=2, vector=[0.2] * dimension, payload={"type": "doc2", "source": "fileB.txt"}),
#         ]
#         print(f"Upserting {len(points_to_upsert)} points...")
#         # Use wait=True for confirmation, especially in scripts
#         client.upsert(collection_name=collection_name, points=points_to_upsert, wait=True)
#         print("Upsert complete.")

#         # Search
#         query_vector = [0.15] * dimension
#         print("Searching collection...")
#         search_result = client.search(
#             collection_name=collection_name,
#             query_vector=query_vector,
#             limit=2 # Number of results to return
#         )
#         print("Search results:", search_result)

#     except Exception as e:
#         print(f"Error interacting with Qdrant collection: {e}")

```

{% endtab %}

{% tab title="TypeScript" %}

```typescript
// Requires: npm install @qdrant/js-client-rest
import { QdrantClient } from '@qdrant/js-client-rest'
import { Distance } from '@qdrant/js-client-rest/dist/types/types/Points' // Adjust import path if needed

function initQdrantClient(): QdrantClient | null {
  /** Initializes Qdrant client. */
  const qdrantUrl = process.env.QDRANT_URL // e.g., "http://localhost:6333" or cloud URL
  const apiKey = process.env.QDRANT_API_KEY // Optional, for cloud
  if (!qdrantUrl) {
    console.error('Error: QDRANT_URL not set.')
    return null
  }
  try {
    const client = new QdrantClient({ url: qdrantUrl, apiKey: apiKey })
    console.log('Qdrant client initialized.')
    return client
  } catch (error) {
    console.error('Error initializing Qdrant client:', error)
    return null
  }
}

async function createQdrantCollectionIfNotExists(
  client: QdrantClient,
  collectionName: string,
  dimension: number,
  distanceMetric: Distance = Distance.Cosine,
): Promise<void> {
  /** Creates a Qdrant collection if it doesn't exist. */
  try {
    const collectionsResponse = await client.getCollections()
    const collectionExists = collectionsResponse.collections.some((c) => c.name === collectionName)

    if (!collectionExists) {
      console.log(`Creating collection '${collectionName}'...`)
      await client.recreateCollection(collectionName, {
        // Use recreateCollection or check/create
        vectors: { size: dimension, distance: distanceMetric },
      })
      console.log(`Collection '${collectionName}' created.`)
    } else {
      console.log(`Collection '${collectionName}' already exists.`)
    }
  } catch (error) {
    console.error('Error creating or checking Qdrant collection:', error)
  }
}

// Example Usage:
/*
async function qdrantExample() {
    const client = initQdrantClient();
    if (!client) return;

    const collectionName = "brainyflow_qdrant_demo_ts";
    const dimension = 128;
    await createQdrantCollectionIfNotExists(client, collectionName, dimension);

    try {
        // Upsert points
        const pointsToUpsert = [
            // Use UUIDs or sequential integers for IDs
            { id: "a1b2c3d4-0001", vector: Array(dimension).fill(0.1), payload: { type: "doc1", source: "fileA.txt" } },
            { id: "a1b2c3d4-0002", vector: Array(dimension).fill(0.2), payload: { type: "doc2", source: "fileB.txt" } },
        ];
        console.log(`Upserting ${pointsToUpsert.length} points...`);
        await client.upsert(collectionName, { points: pointsToUpsert, wait: true });
        console.log("Upsert complete.");

        // Search
        const queryVector = Array(dimension).fill(0.15);
        console.log("Searching collection...");
        const searchResult = await client.search(collectionName, {
            vector: queryVector,
            limit: 2 // Number of results to return
        });
        console.log("Search results:", searchResult);

    } catch (error) {
        console.error("Error interacting with Qdrant collection:", error);
    }
}

qdrantExample();
*/
```

{% endtab %}
{% endtabs %}

### 4. Weaviate

{% tabs %}
{% tab title="Python" %}

```python
# Requires: pip install weaviate-client
import os
import weaviate
import weaviate.classes as wvc # New import style

def init_weaviate_client() -> weaviate.Client | None:
    """Initializes Weaviate client."""
    weaviate_url = os.environ.get("WEAVIATE_URL") # e.g., "http://localhost:8080" or cloud URL
    api_key = os.environ.get("WEAVIATE_API_KEY") # Optional, for cloud/auth
    if not weaviate_url:
        print("Error: WEAVIATE_URL not set.")
        return None
    try:
        auth_config = weaviate.AuthApiKey(api_key=api_key) if api_key else None
        client = weaviate.connect_to_custom( # Use new connection methods
            http_host=weaviate_url.replace("http://", "").split(":")[0],
            http_port=int(weaviate_url.split(":")[-1]),
            http_secure=weaviate_url.startswith("https"),
            # grpc_host=... # Optional gRPC connection details
            # grpc_port=...
            # grpc_secure=...
            auth_credentials=auth_config
        )
        # client = weaviate.Client(url=weaviate_url, auth_client_secret=auth_config) # Old init
        client.is_ready() # Check connection
        print("Weaviate client initialized and ready.")
        return client
    except Exception as e:
        print(f"Error initializing Weaviate client: {e}")
        return None

def create_weaviate_collection_if_not_exists(client: weaviate.Client, class_name: str, dimension: int):
    """Creates a Weaviate collection (class) if it doesn't exist."""
    try:
        if not client.collections.exists(class_name):
            print(f"Creating collection '{class_name}'...")
            client.collections.create(
                name=class_name,
                vectorizer_config=wvc.config.Configure.Vectorizer.none(), # Explicitly disable vectorizer
                # Define properties if needed
                properties=[
                    wvc.config.Property(name="title", data_type=wvc.config.DataType.TEXT),
                    wvc.config.Property(name="content", data_type=wvc.config.DataType.TEXT),
                ]
            )
            print(f"Collection '{class_name}' created.")
        else:
             print(f"Collection '{class_name}' already exists.")
    except Exception as e:
        print(f"Error creating or checking Weaviate collection: {e}")

# Example Usage:
# client = init_weaviate_client()
# if client:
#     collection_name = "CaskadaArticle" # Class names must be capitalized
#     dimension = 128
#     create_weaviate_collection_if_not_exists(client, collection_name, dimension)

#     try:
#         articles = client.collections.get(collection_name)

#         # Insert data object with vector
#         properties = {
#             "title": "Hello Weaviate",
#             "content": "This is an example document."
#         }
#         vector = [0.1] * dimension
#         print("Inserting object...")
#         uuid = articles.data.insert(properties=properties, vector=vector)
#         print(f"Object inserted with UUID: {uuid}")

#         # Query using nearVector
#         query_vector = [0.15] * dimension
#         print("Querying collection...")
#         response = articles.query.near_vector(
#             near_vector=query_vector,
#             limit=3,
#             return_properties=["title", "content"], # Specify properties to return
#             return_metadata=wvc.query.MetadataQuery(distance=True) # Include distance
#         )

#         print("Query results:")
#         for o in response.objects:
#             print(f" - Title: {o.properties['title']}, Distance: {o.metadata.distance}")

#     except Exception as e:
#         print(f"Error interacting with Weaviate collection: {e}")
#     finally:
#         client.close() # Close the connection
#         print("Weaviate client closed.")

```

{% endtab %}

{% tab title="TypeScript" %}

```typescript
// Requires: npm install weaviate-ts-client
import weaviate, {
  ApiKey,
  ObjectsBatcher,
  WeaviateClient,
  WeaviateObject,
} from 'weaviate-ts-client'

function initWeaviateClient(): WeaviateClient | null {
  /** Initializes Weaviate client. */
  const scheme = process.env.WEAVIATE_SCHEME || 'http'
  const host = process.env.WEAVIATE_HOST // e.g., "localhost:8080" or cloud host
  const apiKey = process.env.WEAVIATE_API_KEY // Optional

  if (!host) {
    console.error('Error: WEAVIATE_HOST not set.')
    return null
  }

  try {
    const clientConfig: any = { scheme, host }
    if (apiKey) {
      clientConfig.apiKey = new ApiKey(apiKey)
    }
    const client: WeaviateClient = weaviate.client(clientConfig)
    console.log('Weaviate client initialized.')
    // You might want to add a readiness check here in a real app
    // client.misc.readyChecker().do().then(...).catch(...);
    return client
  } catch (error) {
    console.error('Error initializing Weaviate client:', error)
    return null
  }
}

async function createWeaviateCollectionIfNotExists(
  client: WeaviateClient,
  className: string,
  dimension: number,
): Promise<void> {
  /** Creates a Weaviate collection (class) if it doesn't exist. */
  try {
    const schema = await client.schema.getter().do()
    const exists = schema.classes?.some((c) => c.class === className)

    if (!exists) {
      console.log(`Creating collection '${className}'...`)
      await client.schema
        .classCreator()
        .withClass({
          class: className,
          vectorizer: 'none', // Explicitly disable vectorizer
          properties: [
            { name: 'title', dataType: ['text'] },
            { name: 'content', dataType: ['text'] },
          ],
          // Vector index config can be added here if needed
        })
        .do()
      console.log(`Collection '${className}' created.`)
    } else {
      console.log(`Collection '${className}' already exists.`)
    }
  } catch (error) {
    console.error('Error creating or checking Weaviate collection:', error)
  }
}

// Example Usage:
/*
async function weaviateExample() {
    const client = initWeaviateClient();
    if (!client) return;

    const collectionName = "CaskadaArticleTs"; // Class names must be capitalized
    const dimension = 128;
    await createWeaviateCollectionIfNotExists(client, collectionName, dimension);

    try {
        // Insert data object with vector
        const properties = {
            title: "Hello Weaviate TS",
            content: "This is a TypeScript example document."
        };
        const vector = Array(dimension).fill(0.1);
        console.log("Inserting object...");
        const result = await client.data.creator()
            .withClassName(collectionName)
            .withProperties(properties)
            .withVector(vector)
            .do();
        console.log("Object inserted:", result); // Contains the object with its ID

        // Query using nearVector
        const queryVector = Array(dimension).fill(0.15);
        console.log("Querying collection...");
        const response = await client.graphql.get()
            .withClassName(collectionName)
            .withFields('title content _additional { distance id }') // Specify fields and metadata
            .withNearVector({ vector: queryVector })
            .withLimit(3)
            .do();

        console.log("Query results:", JSON.stringify(response, null, 2));

    } catch (error) {
        console.error("Error interacting with Weaviate collection:", error);
    }
    // Note: weaviate-ts-client v2 doesn't require explicit close()
}

weaviateExample();
*/
```

{% endtab %}
{% endtabs %}

### 5. Milvus

{% tabs %}
{% tab title="Python" %}

```python
# Requires: pip install pymilvus numpy
import os
from pymilvus import connections, utility, FieldSchema, CollectionSchema, DataType, Collection
import numpy as np

def connect_milvus():
    """Connects to Milvus."""
    milvus_uri = os.environ.get("MILVUS_URI", "http://localhost:19530") # Or Zilliz Cloud URI
    token = os.environ.get("MILVUS_TOKEN") # For Zilliz Cloud or authenticated Milvus
    alias = "default"
    try:
        print(f"Connecting to Milvus at {milvus_uri}...")
        connections.connect(alias=alias, uri=milvus_uri, token=token)
        print("Milvus connected.")
    except Exception as e:
        print(f"Error connecting to Milvus: {e}")

def create_milvus_collection_if_not_exists(collection_name: str, dimension: int):
    """Creates a Milvus collection if it doesn't exist."""
    alias = "default"
    if not utility.has_collection(collection_name, using=alias):
        print(f"Creating collection '{collection_name}'...")
        # Define fields: Primary key and embedding vector
        fields = [
            FieldSchema(name="pk", dtype=DataType.INT64, is_primary=True, auto_id=True), # Auto-incrementing ID
            FieldSchema(name="embeddings", dtype=DataType.FLOAT_VECTOR, dim=dimension)
        ]
        schema = CollectionSchema(fields, description="Caskada Milvus Demo")
        collection = Collection(name=collection_name, schema=schema, using=alias)
        print(f"Collection '{collection_name}' created.")
        # Create an index for the embedding field for efficient search
        index_params = {
            "metric_type": "L2", # Or "IP" for inner product
            "index_type": "IVF_FLAT", # Example index type
            "params": {"nlist": 1024} # Example parameter
        }
        collection.create_index(field_name="embeddings", index_params=index_params)
        print(f"Index created on 'embeddings' field.")
    else:
        print(f"Collection '{collection_name}' already exists.")
    # Load collection into memory for searching
    collection = Collection(collection_name) # Get collection object
    if collection.is_empty:
         print(f"Collection '{collection_name}' is empty, loading skipped.")
    elif utility.load_state(collection_name) != "Loaded":
         print(f"Loading collection '{collection_name}'...")
         collection.load()
         print("Collection loaded.")
    else:
         print(f"Collection '{collection_name}' already loaded.")


# Example Usage:
# connect_milvus()
# collection_name = "brainyflow_milvus_demo"
# dimension = 128
# create_milvus_collection_if_not_exists(collection_name, dimension)

# try:
#     collection = Collection(collection_name) # Get collection handle

#     # Insert data
#     num_vectors = 100
#     vectors_to_insert = np.random.rand(num_vectors, dimension).astype('float32').tolist()
#     # Data format for pymilvus is a list of lists/tuples matching field order (excluding auto-id pk)
#     data = [vectors_to_insert]
#     print(f"Inserting {num_vectors} vectors...")
#     mr = collection.insert(data)
#     print(f"Insert result: {mr}")
#     collection.flush() # Ensure data is written
#     print(f"Data flushed. Entity count: {collection.num_entities}")


#     # Search
#     query_vector = np.random.rand(1, dimension).astype('float32').tolist()
#     search_params = {
#         "metric_type": "L2",
#         "params": {"nprobe": 10} # Search parameter for IVF_FLAT
#     }
#     print("Searching collection...")
#     results = collection.search(
#         data=query_vector,
#         anns_field="embeddings",
#         param=search_params,
#         limit=3 # Number of results
#     )
#     print("Search results:")
#     for hit in results[0]: # Results is a list of lists (one per query vector)
#         print(f" - ID: {hit.id}, Distance: {hit.distance}")

# except Exception as e:
#     print(f"Error interacting with Milvus collection: {e}")
# finally:
#     # Disconnect (optional, depends on application lifecycle)
#     # connections.disconnect("default")
#     # print("Milvus disconnected.")
#     pass

```

{% endtab %}

{% tab title="TypeScript" %}

```typescript
// Requires: npm install @zilliz/milvus2-sdk-node
import { DataType, IndexType, MetricType, MilvusClient } from '@zilliz/milvus2-sdk-node'

function initMilvusClient(): MilvusClient | null {
  /** Initializes Milvus client. */
  const address = process.env.MILVUS_ADDRESS || 'localhost:19530' // Host:Port or Zilliz Cloud endpoint
  const token = process.env.MILVUS_TOKEN // For Zilliz Cloud or authenticated Milvus
  // SSL setup might be needed for cloud endpoints
  const ssl = address.includes('cloud') || address.includes('https') // Basic check

  try {
    console.log(`Connecting to Milvus at ${address}...`)
    const client = new MilvusClient({ address, ssl, token })
    console.log('Milvus client instance created.')
    // Note: SDK v2 doesn't have an explicit connect method, operations will connect.
    // Add a health check or simple operation to confirm connectivity if needed.
    // client.checkHealth().then(...).catch(...);
    return client
  } catch (error) {
    console.error('Error initializing Milvus client:', error)
    return null
  }
}

async function createMilvusCollectionIfNotExists(
  client: MilvusClient,
  collectionName: string,
  dimension: number,
): Promise<void> {
  /** Creates a Milvus collection if it doesn't exist. */
  try {
    const hasCollection = await client.hasCollection({ collection_name: collectionName })
    if (!hasCollection.value) {
      console.log(`Creating collection '${collectionName}'...`)
      await client.createCollection({
        collection_name: collectionName,
        fields: [
          { name: 'pk', dtype: DataType.Int64, is_primary_key: true, autoID: true },
          { name: 'embeddings', dtype: DataType.FloatVector, dim: dimension },
        ],
      })
      console.log(`Collection '${collectionName}' created.`)

      // Create index
      console.log("Creating index on 'embeddings' field...")
      await client.createIndex({
        collection_name: collectionName,
        field_name: 'embeddings',
        index_type: IndexType.IVF_FLAT, // Example index
        metric_type: MetricType.L2, // Or IP
        params: { nlist: 1024 }, // Example param
      })
      console.log('Index created.')
    } else {
      console.log(`Collection '${collectionName}' already exists.`)
    }

    // Load collection
    const loadStatus = await client.getLoadState({ collection_name: collectionName })
    if (loadStatus.state !== 'Loaded') {
      console.log(`Loading collection '${collectionName}'...`)
      await client.loadCollectionSync({ collection_name: collectionName }) // Use Sync for simplicity here
      console.log('Collection loaded.')
    } else {
      console.log(`Collection '${collectionName}' already loaded.`)
    }
  } catch (error) {
    console.error('Error creating or loading Milvus collection:', error)
  }
}

// Example Usage:
/*
async function milvusExample() {
    const client = initMilvusClient();
    if (!client) return;

    const collectionName = "brainyflow_milvus_demo_ts";
    const dimension = 128;
    await createMilvusCollectionIfNotExists(client, collectionName, dimension);

    try {
        // Insert data
        const numVectors = 100;
        // Data format for Node SDK: array of objects, keys match field names
        const dataToInsert = Array.from({ length: numVectors }, () => ({
            embeddings: Array.from({ length: dimension }, () => Math.random())
        }));
        console.log(`Inserting ${numVectors} vectors...`);
        const insertResult = await client.insert({
            collection_name: collectionName,
            data: dataToInsert
        });
        console.log("Insert result:", insertResult); // Contains IDs if autoID=true
        await client.flushSync({ collection_names: [collectionName] }); // Ensure data is written
        const stats = await client.getCollectionStatistics({ collection_name: collectionName });
        console.log(`Data flushed. Entity count: ${stats.data.row_count}`);


        // Search
        const queryVector = [Array.from({ length: dimension }, () => Math.random())]; // Search expects array of vectors
        const searchParams = {
            anns_field: "embeddings",
            topk: 3,
            metric_type: MetricType.L2,
            params: { nprobe: 10 } // Search param for IVF_FLAT
        };
        console.log("Searching collection...");
        const searchResult = await client.search({
            collection_name: collectionName,
            data: queryVector, // Pass query vectors in 'data' field
            ...searchParams
        });
        console.log("Search results:", searchResult);
        // Access results like: searchResult.results[0].ids, searchResult.results[0].scores

    } catch (error) {
        console.error("Error interacting with Milvus collection:", error);
    } finally {
        // Optional: Close connection if needed for app lifecycle
        // await client.close();
        // console.log("Milvus client closed.");
    }
}

milvusExample();
*/
```

{% endtab %}
{% endtabs %}

### 6. Chroma

{% tabs %}
{% tab title="Python" %}

```python
# Requires: pip install chromadb duckdb>=0.8.1 # Or other impl. deps
import os
import chromadb
# from chromadb.config import Settings # Settings is deprecated, use client args

def init_chroma_client(persist_directory: str = "./chroma_data_py") -> chromadb.Client | None:
    """Initializes a persistent Chroma client."""
    try:
        # Persistent client stores data on disk
        client = chromadb.PersistentClient(path=persist_directory)
        # Or use in-memory client: client = chromadb.Client()
        print(f"Chroma client initialized (persistent path: {persist_directory}).")
        return client
    except Exception as e:
        print(f"Error initializing Chroma client: {e}")
        return None

def get_or_create_chroma_collection(client: chromadb.Client, collection_name: str) -> chromadb.Collection | None:
    """Gets or creates a Chroma collection."""
    try:
        collection = client.get_or_create_collection(collection_name)
        print(f"Using Chroma collection '{collection_name}'.")
        return collection
    except Exception as e:
        print(f"Error getting/creating Chroma collection: {e}")
        return None

# Example Usage:
# client = init_chroma_client()
# if client:
#     collection_name = "brainyflow_chroma_demo"
#     collection = get_or_create_chroma_collection(client, collection_name)

#     if collection:
#         try:
#             # Add data (embeddings, optional documents, optional metadata, required IDs)
#             dimension = 128
#             ids_to_add = ["item1", "item2", "item3"]
#             embeddings_to_add = [
#                 [0.1] * dimension,
#                 [0.2] * dimension,
#                 [0.9] * dimension # Different vector
#             ]
#             metadatas_to_add = [
#                 {"source": "docA", "page": 1},
#                 {"source": "docB", "page": 5},
#                 {"source": "docA", "page": 2},
#             ]
#             documents_to_add = [ # Optional, can store original text
#                 "This is the first document.",
#                 "This is the second text.",
#                 "A third piece of information."
#             ]

#             print(f"Adding/updating {len(ids_to_add)} items...")
#             collection.add( # Use add or upsert
#                 ids=ids_to_add,
#                 embeddings=embeddings_to_add,
#                 metadatas=metadatas_to_add,
#                 documents=documents_to_add
#             )
#             print("Add/update complete.")
#             print(f"Collection count: {collection.count()}")

#             # Query
#             query_embedding = [[0.15] * dimension] # Query expects list of embeddings
#             num_results = 2
#             print("Querying collection...")
#             results = collection.query(
#                 query_embeddings=query_embedding,
#                 n_results=num_results,
#                 include=['metadatas', 'documents', 'distances'] # Specify what to include
#             )
#             print("Query results:", results)

#         except Exception as e:
#             print(f"Error interacting with Chroma collection: {e}")

```

{% endtab %}

{% tab title="TypeScript" %}

```typescript
// Requires: npm install chromadb
import { ChromaClient, OpenAIEmbeddingFunction } from 'chromadb' // Or use your own embedding function

function initChromaClient(persistDirectory: string = './chroma_data_ts'): ChromaClient | null {
  /** Initializes a persistent Chroma client. */
  try {
    // Persistent client stores data on disk
    const client = new ChromaClient({ path: persistDirectory })
    // Or use in-memory client: const client = new ChromaClient();
    console.log(`Chroma client initialized (persistent path: ${persistDirectory}).`)
    return client
  } catch (error) {
    console.error('Error initializing Chroma client:', error)
    return null
  }
}

async function getOrCreateChromaCollection(client: ChromaClient, collectionName: string) {
  /** Gets or creates a Chroma collection. */
  try {
    // Optional: Define embedding function if using Chroma's auto-embedding
    // const embedder = new OpenAIEmbeddingFunction({ openai_api_key: process.env.OPENAI_API_KEY! });
    // const collection = await client.getOrCreateCollection({ name: collectionName, embeddingFunction: embedder });
    const collection = await client.getOrCreateCollection({ name: collectionName }) // Manual embeddings
    console.log(`Using Chroma collection '${collectionName}'.`)
    return collection
  } catch (error) {
    console.error('Error getting/creating Chroma collection:', error)
    return null
  }
}

// Example Usage:
/*
async function chromaExample() {
    const client = initChromaClient();
    if (!client) return;

    const collectionName = "brainyflow_chroma_demo_ts";
    const collection = await getOrCreateChromaCollection(client, collectionName);

    if (collection) {
        try {
            // Add data (embeddings, optional documents, optional metadata, required IDs)
            const dimension = 128; // Assuming embeddings are pre-computed
            const idsToAdd = ["ts_item1", "ts_item2", "ts_item3"];
            const embeddingsToAdd = [
                Array(dimension).fill(0.1),
                Array(dimension).fill(0.2),
                Array(dimension).fill(0.9) // Different vector
            ];
            const metadatasToAdd = [
                { source: "docA", page: 1 },
                { source: "docB", page: 5 },
                { source: "docA", page: 2 },
            ];
            const documentsToAdd = [ // Optional
                "This is the first TS document.",
                "This is the second TS text.",
                "A third TS piece of information."
            ];

            console.log(`Adding/updating ${idsToAdd.length} items...`);
            await collection.add({ // Use add or upsert
                ids: idsToAdd,
                embeddings: embeddingsToAdd,
                metadatas: metadatasToAdd,
                documents: documentsToAdd
            });
            console.log("Add/update complete.");
            const count = await collection.count();
            console.log(`Collection count: ${count}`);

            // Query
            const queryEmbedding = [Array(dimension).fill(0.15)]; // Query expects array of embeddings
            const numResults = 2;
            console.log("Querying collection...");
            const results = await collection.query({
                queryEmbeddings: queryEmbedding,
                nResults: numResults,
                include: ['metadatas', 'documents', 'distances'] // Specify what to include
            });
            console.log("Query results:", JSON.stringify(results, null, 2));

        } catch (error) {
            console.error("Error interacting with Chroma collection:", error);
        }
    }
}

chromaExample();
*/
```

{% endtab %}
{% endtabs %}

### 7. Redis Stack (with Vector Search)

{% tabs %}
{% tab title="Python" %}

```python
# Requires: pip install redis numpy
import os
import redis
import numpy as np
from redis.commands.search.field import VectorField, TagField
from redis.commands.search.indexDefinition import IndexDefinition, IndexType
from redis.commands.search.query import Query

def init_redis_client() -> redis.Redis | None:
    """Initializes Redis client."""
    redis_host = os.environ.get("REDIS_HOST", "localhost")
    redis_port = int(os.environ.get("REDIS_PORT", 6379))
    redis_password = os.environ.get("REDIS_PASSWORD") # Optional
    try:
        # Ensure decoding responses for easier handling
        client = redis.Redis(host=redis_host, port=redis_port, password=redis_password, decode_responses=True)
        client.ping() # Verify connection
        print(f"Redis client connected to {redis_host}:{redis_port}.")
        return client
    except Exception as e:
        print(f"Error connecting to Redis: {e}")
        return None

def create_redis_index_if_not_exists(client: redis.Redis, index_name: str, prefix: str, dimension: int):
    """Creates a Redis Search index for vectors if it doesn't exist."""
    schema = (
        # Example: Add other fields like text or tags if needed
        # TagField("$.tag", as_name="tag"),
        VectorField("$.embedding", "FLAT", { # Or HNSW
            "TYPE": "FLOAT32",
            "DIM": dimension,
            "DISTANCE_METRIC": "L2", # Or COSINE, IP
            # "INITIAL_CAP": 1000, # Optional params for HNSW etc.
        }, as_name="vector")
    )
    definition = IndexDefinition(prefix=[prefix], index_type=IndexType.JSON) # Index JSON documents

    try:
        # Check if index exists
        client.ft(index_name).info()
        print(f"Redis index '{index_name}' already exists.")
    except:
        # Index doesn't exist, create it
        print(f"Creating Redis index '{index_name}' for prefix '{prefix}'...")
        client.ft(index_name).create_index(fields=schema, definition=definition)
        print(f"Redis index '{index_name}' created.")

# Example Usage:
# client = init_redis_client()
# if client:
#     index_name = "brainyflow-redis-idx"
#     doc_prefix = "bfdoc:" # Prefix for keys to be indexed
#     dimension = 128
#     create_redis_index_if_not_exists(client, index_name, doc_prefix, dimension)

#     try:
#         # Insert data using JSON.SET (requires RedisJSON module)
#         doc_id1 = f"{doc_prefix}item1"
#         doc_id2 = f"{doc_prefix}item2"
#         vector1 = np.array([0.1] * dimension, dtype=np.float32).tobytes()
#         vector2 = np.array([0.2] * dimension, dtype=np.float32).tobytes()

#         # Store vector as bytes in a JSON object
#         # Note: Storing raw bytes in JSON isn't standard.
#         # Often, vectors are stored as lists and indexed, or using HSET with raw bytes.
#         # Let's use HSET for simpler vector storage with raw bytes.

#         # Revisit index creation for HASH
#         client.ft(index_name).dropindex() # Drop JSON index if exists
#         schema_hash = (
#              VectorField("embedding", "FLAT", { # Indexing a field named 'embedding' in the HASH
#                 "TYPE": "FLOAT32", "DIM": dimension, "DISTANCE_METRIC": "L2"
#              }, as_name="vector"),
#              # TagField("tag", as_name="tag") # Example other field
#         )
#         definition_hash = IndexDefinition(prefix=[doc_prefix], index_type=IndexType.HASH)
#         try:
#              client.ft(index_name).info()
#         except:
#              print("Recreating index for HASH...")
#              client.ft(index_name).create_index(fields=schema_hash, definition=definition_hash)


#         print("Inserting data using HSET...")
#         client.hset(doc_id1, mapping={"embedding": vector1, "tag": "A"})
#         client.hset(doc_id2, mapping={"embedding": vector2, "tag": "B"})
#         print("Data inserted.")

#         # KNN Query
#         k = 3
#         query_vector = np.array([0.15] * dimension, dtype=np.float32).tobytes()
#         # Query syntax: "*=>[KNN $K @vector $vec AS vector_score]"
#         # $vec needs to be passed as query parameter
#         q = Query(f"*=>[KNN {k} @vector $vec AS vector_score]")\
#             .sort_by("vector_score")\
#             .return_fields("id", "vector_score", "tag")\
#             .dialect(2) # Use DIALECT 2 for parameter support

#         params = {"vec": query_vector}
#         print("Querying Redis index...")
#         results = client.ft(index_name).search(q, query_params=params)

#         print("Query results:")
#         for doc in results.docs:
#             print(f" - ID: {doc.id}, Score: {doc.vector_score}, Tag: {doc.tag}")

#     except Exception as e:
#         print(f"Error interacting with Redis Search: {e}")

```

{% endtab %}

{% tab title="TypeScript" %}

```typescript
// Requires: npm install redis ioredis @node-redis/search @node-redis/json # Using node-redis client
import numpy from 'numpy' // Or use Buffer directly
import {
  AggregateGroupByReducers,
  AggregateSteps,
  createClient,
  SchemaFieldTypes,
  VectorAlgorithms,
} from 'redis'

async function initRedisClient(): Promise<ReturnType<typeof createClient> | null> {
  /** Initializes Redis client. */
  const redisUrl = process.env.REDIS_URL // e.g., "redis://localhost:6379" or "redis://:password@host:port"
  if (!redisUrl) {
    console.error('Error: REDIS_URL not set.')
    return null
  }
  try {
    const client = createClient({ url: redisUrl })
    await client.connect()
    console.log(`Redis client connected to ${redisUrl}.`)
    return client
  } catch (error) {
    console.error('Error connecting to Redis:', error)
    return null
  }
}

async function createRedisIndexIfNotExists(
  client: ReturnType<typeof createClient>,
  indexName: string,
  prefix: string,
  dimension: number,
): Promise<void> {
  /** Creates a Redis Search index for vectors if it doesn't exist. */
  const schema = {
    // Indexing JSON: $.vector for vector field
    // '$.vector': { // Requires RedisJSON
    //     type: SchemaFieldTypes.VECTOR,
    //     ALGORITHM: VectorAlgorithms.FLAT, // Or HNSW
    //     TYPE: 'FLOAT32',
    //     DIM: dimension,
    //     DISTANCE_METRIC: 'L2' // Or COSINE, IP
    // },
    // '$.tag': { // Example other field
    //     type: SchemaFieldTypes.TAG,
    //     AS: 'tag'
    // }

    // Indexing HASH: field name directly
    embedding: {
      type: SchemaFieldTypes.VECTOR,
      ALGORITHM: VectorAlgorithms.FLAT,
      TYPE: 'FLOAT32',
      DIM: dimension,
      DISTANCE_METRIC: 'L2', // Or COSINE, IP
      AS: 'vector', // Alias for the vector field in queries
    },
    tag: {
      // Example other field
      type: SchemaFieldTypes.TAG,
      AS: 'tag',
    },
  }

  try {
    // Check if index exists
    await client.ft.info(indexName)
    console.log(`Redis index '${indexName}' already exists.`)
  } catch (e: any) {
    if (e.message.includes('Unknown Index name')) {
      // Index doesn't exist, create it
      console.log(`Creating Redis index '${indexName}' for prefix '${prefix}'...`)
      await client.ft.create(
        indexName,
        schema, // Pass schema directly
        {
          ON: 'HASH', // Index HASH data type
          PREFIX: prefix,
        },
      )
      console.log(`Redis index '${indexName}' created.`)
    } else {
      // Other error
      console.error('Error checking/creating Redis index:', e)
    }
  }
}

// Helper to convert number array to Float32 Buffer
function vectorToBuffer(vector: number[]): Buffer {
  const float32Array = new Float32Array(vector)
  return Buffer.from(float32Array.buffer)
}

// Example Usage:
/*
async function redisExample() {
    const client = await initRedisClient();
    if (!client) return;

    const indexName = "brainyflow-redis-idx-ts";
    const docPrefix = "bfdoc-ts:"; // Prefix for keys
    const dimension = 128;
    await createRedisIndexIfNotExists(client, indexName, docPrefix, dimension);

    try {
        // Insert data using HSET
        const docId1 = `${docPrefix}item1`;
        const docId2 = `${docPrefix}item2`;
        const vector1 = vectorToBuffer(Array(dimension).fill(0.1));
        const vector2 = vectorToBuffer(Array(dimension).fill(0.2));

        console.log("Inserting data using HSET...");
        // node-redis client expects key-value pairs for HSET
        await client.hSet(docId1, { embedding: vector1, tag: "A" });
        await client.hSet(docId2, { embedding: vector2, tag: "B" });
        console.log("Data inserted.");

        // KNN Query
        const k = 3;
        const queryVector = vectorToBuffer(Array(dimension).fill(0.15));

        // Query syntax: "*=>[KNN $K @vector $vec AS vector_score]"
        const queryString = `*=>[KNN ${k} @vector $vec AS vector_score]`;

        console.log("Querying Redis index...");
        const results = await client.ft.search(
            indexName,
            queryString,
            {
                PARAMS: { // Pass parameters in PARAMS object
                    vec: queryVector
                },
                RETURN: ['id', 'vector_score', 'tag'], // Specify fields to return
                SORTBY: { // Sort by score
                    BY: 'vector_score',
                    DIRECTION: 'ASC' // Lower score (distance) is better
                },
                DIALECT: 2 // Use DIALECT 2 for KNN parameters
            }
        );

        console.log("Query results:", results);
        // Access results: results.documents.forEach(doc => console.log(doc.id, doc.value.vector_score, doc.value.tag));

    } catch (error) {
        console.error("Error interacting with Redis Search:", error);
    } finally {
        await client.quit();
        console.log("Redis client disconnected.");
    }
}

redisExample();
*/
```

{% endtab %}
{% endtabs %}
