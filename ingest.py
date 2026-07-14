'''"""Ingest research papers into a LlamaIndex vector store.

This script scans the ``papers/`` directory for PDF files, creates embeddings using a
HuggingFace sentence‑transformer model, builds a :class:`~llama_index.VectorStoreIndex`
and persists the index to ``storage/``.

The script can be executed directly::

    python ingest.py

It will raise informative errors if the input directory is missing or contains no
PDFs.
"""'''

import os
from pathlib import Path
from typing import List

from tqdm import tqdm

from llama_index.core import SimpleDirectoryReader, VectorStoreIndex, StorageContext
from llama_index.embeddings.huggingface import HuggingFaceEmbedding


def ingest_papers(papers_dir: str = "papers", storage_dir: str = "storage") -> None:
    """Read all PDFs from *papers_dir*, embed them, and persist a vector index.

    Parameters
    ----------
    papers_dir: str
        Directory containing PDF files to ingest.
    storage_dir: str
        Destination directory where the persisted index will be stored.
    """
    # ---------------------------------------------------------------------
    # Validate input directory
    # ---------------------------------------------------------------------
    if not os.path.isdir(papers_dir):
        raise FileNotFoundError(f"Papers directory '{papers_dir}' does not exist.")

    pdf_files = [f for f in os.listdir(papers_dir) if f.lower().endswith('.pdf')]
    if not pdf_files:
        raise ValueError(f"No PDF files found in '{papers_dir}'.")

    # ---------------------------------------------------------------------
    # Load documents with SimpleDirectoryReader (filename_as_id=True tracks source)
    # ---------------------------------------------------------------------
    reader = SimpleDirectoryReader(input_dir=papers_dir, filename_as_id=True)
    # Using tqdm to give the user visual progress while loading
    documents = []
    for _ in tqdm(reader.iter_data(), desc="Loading PDFs"):
        # SimpleDirectoryReader yields documents lazily; we collect them all
        documents.extend(_)

    # ---------------------------------------------------------------------
    # Create embedding model from HuggingFace sentence‑transformers
    # ---------------------------------------------------------------------
    embed_model = HuggingFaceEmbedding(model_name="sentence-transformers/all-MiniLM-L6-v2")

    # ---------------------------------------------------------------------
    # Build the VectorStoreIndex – the heavy lifting is done internally.
    # ---------------------------------------------------------------------
    index = VectorStoreIndex.from_documents(documents, embed_model=embed_model)

    # ---------------------------------------------------------------------
    # Persist the index to the storage directory
    # ---------------------------------------------------------------------
    storage_path = Path(storage_dir)
    storage_path.mkdir(parents=True, exist_ok=True)

    # The StorageContext knows where to write the index files.
    storage_context = StorageContext.from_defaults(persist_dir=storage_path)
    index.storage_context.persist(persist_dir=storage_path)

    print(f"✅ Index persisted to '{storage_path}'.")


if __name__ == "__main__":
    ingest_papers()
