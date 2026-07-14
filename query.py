import os
from llama_index.core import StorageContext, load_index_from_storage
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.openai import OpenAI
from dotenv import load_dotenv

def query_index(query_str: str, storage_dir: str = "storage"):
    # Load environment variables (API Key)
    load_dotenv()
    
    # Check if storage exists
    if not os.path.exists(storage_dir):
        print(f"Error: Storage directory '{storage_dir}' does not exist. Please run ingest.py first.")
        return

    # Load embedding model
    embed_model = HuggingFaceEmbedding(model_name="sentence-transformers/all-MiniLM-L6-v2")
    
    # Load LLM
    llm = OpenAI(model="gpt-3.5-turbo")
    
    # Load index
    storage_context = StorageContext.from_defaults(persist_dir=storage_dir)
    index = load_index_from_storage(storage_context, embed_model=embed_model)
    
    # Build query engine
    query_engine = index.as_query_engine(similarity_top_k=4, response_mode="compact", llm=llm)
    
    # Query
    print(f"Querying: {query_str}")
    response = query_engine.query(query_str)
    
    print("\n================ Answer ================\n")
    print(response.response)
    print("\n================ Sources ================\n")
    for node in response.source_nodes:
        file_name = node.node.metadata.get("file_name", "Unknown")
        page_label = node.node.metadata.get("page_label", "Unknown")
        score = node.score
        text = node.node.text[:120].replace('\n', ' ')
        print(f"File: {file_name}, Page: {page_label}, Score: {score:.3f}")
        print(f"Text: {text}...\n")
    
if __name__ == "__main__":
    import sys
    query = "Can you summarize the research papers?"
    if len(sys.argv) > 1:
        query = " ".join(sys.argv[1:])
    query_index(query)
