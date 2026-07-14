import streamlit as st
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# Fix sqlite3 issue in Streamlit cloud / old systems for Chroma/LlamaIndex if needed
try:
    __import__('pysqlite3')
    import sys
    sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
except ImportError:
    pass

st.set_page_config(page_title="AI Research Paper Summarizer", layout="centered")

# Hide Deploy Button
st.markdown("""
    <style>
    .stAppDeployButton {display:none;}
    </style>
""", unsafe_allow_html=True)

st.title("AI Research Paper Summarizer")

st.header("Document Ingestion")
uploaded_files = st.file_uploader("Upload PDF Papers", type="pdf", accept_multiple_files=True)

if st.button("Ingest Uploaded Papers"):
    if uploaded_files:
        os.makedirs("papers", exist_ok=True)
        for f in uploaded_files:
            file_path = os.path.join("papers", f.name)
            with open(file_path, "wb") as out_file:
                out_file.write(f.read())
        st.success(f"Saved {len(uploaded_files)} files!")
        
        with st.spinner("Ingesting papers into vector database..."):
            from ingest import ingest_papers
            try:
                ingest_papers("papers", "storage")
                st.success("Ingestion complete!")
            except Exception as e:
                st.error(f"Error during ingestion: {e}")
    else:
        st.warning("Please upload some PDFs first.")

st.header("Query the Knowledge Base")
query_str = st.text_input("Ask a question about your papers:", value="Can you summarize the research papers?")

if st.button("Query"):
    if os.path.exists("storage"):
        with st.spinner("Retrieving answer..."):
            from llama_index.core import StorageContext, load_index_from_storage
            from llama_index.embeddings.huggingface import HuggingFaceEmbedding
            from llama_index.llms.openai import OpenAI
            
            try:
                embed_model = HuggingFaceEmbedding(model_name="sentence-transformers/all-MiniLM-L6-v2")
                llm = OpenAI(model="gpt-3.5-turbo")
                
                storage_context = StorageContext.from_defaults(persist_dir="storage")
                index = load_index_from_storage(storage_context, embed_model=embed_model)
                
                query_engine = index.as_query_engine(similarity_top_k=4, response_mode="compact", llm=llm)
                response = query_engine.query(query_str)
                
                st.markdown("### Answer")
                st.write(response.response)
                
                st.markdown("### Sources")
                for node in response.source_nodes:
                    file_name = node.node.metadata.get("file_name", "Unknown")
                    page_label = node.node.metadata.get("page_label", "Unknown")
                    st.markdown(f"- **{file_name}** (Page {page_label}) - Relevance Score: `{node.score:.3f}`")
            except Exception as e:
                st.error(f"Error during querying: {e}")
    else:
        st.error("Vector index not found. Please ingest some papers first by uploading them above.")
