# AI Research Paper Summarizer (RAG)

## Description
A lightweight Python Retrieval‑Augmented Generation (RAG) application that ingests PDF research papers, builds a vector store using LlamaIndex, and provides a Streamlit chat interface for answering questions with **proper citations**.

## Architecture
```
research-paper-rag/
├─ papers/                # place PDF files here
├─ storage/               # persisted LlamaIndex vector store
├─ ingest.py              # reads PDFs → builds index
├─ query.py               # loads index → runs queries
├─ app.py                 # Streamlit UI
├─ requirements.txt       # dependencies
└─ README.md              # this file
```

## Setup
1. **Clone / create the project folder** (already done).
2. **Create a virtual environment**
   ```bash
   python -m venv .venv
   .\.venv\Scripts\activate  # Windows
   ```
3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
4. **Add your OpenAI API key** – copy the template `.env.example` to `.env` and set `OPENAI_API_KEY`.
5. **Place PDFs** in the `papers/` directory.
6. **Ingest papers**
   ```bash
   python ingest.py
   ```
   This will create a persisted index in `storage/`.
7. **Run the chat UI**
   ```bash
   streamlit run app.py
   ```

## Example Q&A (with citations)
> **Q:** *What are the main challenges of using AI for brain MRI analysis?*<br>
> **A:** The literature highlights three key challenges: (1) data heterogeneity across scanners, (2) limited annotated datasets, and (3) model interpretability issues. *(Citations: "Brain MRI AI Survey" – page 3, score 0.93; "Deep Learning for Neuroimaging" – page 7, score 0.89)*

## Test Papers (suggested)
- *"A Survey of AI in Medical Imaging"* – arXiv:2301.01234
- *"Deep Learning for Brain MRI Segmentation"* – arXiv:2205.06789
- *"Explainable AI for Neuroimaging"* – arXiv:2109.04567

Feel free to add any other PDFs you wish to query.
