# AI Research Paper Summarizer – Implementation Plan

## Goal Description
Create a Python project that ingests a collection of research‑paper PDFs, builds a vector‑store index using LlamaIndex with HuggingFace embeddings, and provides a Streamlit chat interface for querying the papers. The system must always cite source papers in its answers.

## User Review Required
> [!IMPORTANT]
> No breaking changes are expected, but please confirm that the chosen example papers (medical AI / brain MRI arXiv PDFs) are acceptable for testing. If you have specific PDFs you want included, place them in `papers/` before running the ingest step.

## Open Questions
_None at this time._

## Proposed Changes
---
### Project Structure
Create the following directories and files under `research-paper-rag/`:
- `papers/` (empty – user adds PDFs)
- `storage/` (will hold persisted index)
- `ingest.py`
- `query.py`
- `app.py`
- `requirements.txt`
- `README.md`

---
### ingest.py
[NEW] [ingest.py](file:///C:/Users/yeshv/.gemini/antigravity-ide/brain/40ae6e9e-5fa3-4a91-ad7d-bc100c839994/research-paper-rag/ingest.py)

### query.py
[NEW] [query.py](file:///C:/Users/yeshv/.gemini/antigravity-ide/brain/40ae6e9e-5fa3-4a91-ad7d-bc100c839994/research-paper-rag/query.py)

---
### app.py
[NEW] [app.py](file:///C:/Users/yeshv/.gemini/antigravity-ide/brain/40ae6e9e-5fa3-4a91-ad7d-bc100c839994/research-paper-rag/app.py)

---
### requirements.txt
[NEW] [requirements.txt](file:///C:/Users/yeshv/.gemini/antigravity-ide/brain/40ae6e9e-5fa3-4a91-ad7d-bc100c839994/research-paper-rag/requirements.txt)

---
### README.md
[NEW] [README.md](file:///C:/Users/yeshv/.gemini/antigravity-ide/brain/40ae6e9e-5fa3-4a91-ad7d-bc100c839994/research-paper-rag/README.md)

---
## Verification Plan
### Automated Tests
- Run `python ingest.py` and verify that `storage/index.json` (or similar) is created.
- Run `python query.py "test query"` and check that output prints answer and source details.
- Launch `streamlit run app.py` manually and perform a few queries, confirming citation cards appear.

### Manual Verification
- User populates `papers/` with a few PDF files and executes the ingest script.
- User runs the Streamlit app and checks UI elements (sidebar file list, example questions, spinner, answer formatting, source expander).

---
