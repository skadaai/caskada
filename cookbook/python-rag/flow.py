from caskada import Flow
from nodes import ProcessChunkDocumentsNode, EmbedDocumentsNode, CreateIndexNode, EmbedQueryNode, ReduceChunksAndEmbeddingsNode, RetrieveDocumentNode, GenerateAnswerNode
from mapreduce import mapreduce

def get_document_flow():
    # Create offline flow for document indexing
    process_chunk_docs_node = ProcessChunkDocumentsNode()
    embed_docs_node = EmbedDocumentsNode()
    
    process_chunk_docs_node >> embed_docs_node
    
    return Flow(start=process_chunk_docs_node)

def get_offline_flow():
    # Create offline flow for document indexing
    doc_flow = get_document_flow()
    reduce_chunks_and_embeddings_node = ReduceChunksAndEmbeddingsNode()
    create_index_node = CreateIndexNode()

    mapreduce_flow = mapreduce(doc_flow, {"input_key": "texts"})
    mapreduce_flow >> reduce_chunks_and_embeddings_node >> create_index_node
    
    offline_flow = Flow(start=mapreduce_flow)
    return offline_flow

def get_online_flow():
    # Create online flow for document retrieval and answer generation
    embed_query_node = EmbedQueryNode()
    retrieve_doc_node = RetrieveDocumentNode()
    generate_answer_node = GenerateAnswerNode()
    
    # Connect the nodes
    embed_query_node >> retrieve_doc_node >> generate_answer_node
    
    online_flow = Flow(start=embed_query_node)
    return online_flow

# Initialize flows
offline_flow = get_offline_flow()
online_flow = get_online_flow()