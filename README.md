# 🧠 Internal Knowledge AI Assistant (Company Brain)

Enterprise “Private ChatGPT” for companies — answer questions from internal company documents.

This system ingests PDFs, DOCX, PPTX, TXT, CSV, Images etc and turns them into a secure private knowledge base with RAG + vector search + hybrid search.

### Features
- Upload company documents (PDF, PPTX, DOCX, TXT, CSV, Images)
- Automatic text extraction + chunking
- Vector Embeddings + pgvector
- Hybrid similarity + BM25 search
- RAG answer generation using OpenAI model
- Citations (shows which document / snippet answer came from)
- Object Storage (MinIO S3)
- Worker Queue (Redis)
- Dockerized full stack (API + Worker + DB + Web UI)

---

## Architecture

| Component | Tech |
|----------|------|
| API | FastAPI |
| DB | Postgres + pgvector |
| Object Storage | MinIO (S3 compatible) |
| Queue | Redis |
| LLM / Embeddings | OpenAI |
| Web UI | HTML/JS |

---

## Run locally

### 1) Add your OpenAI Key
Create file `.env` in project root:

OPENAI_API_KEY=sk-xxxxxxx


### 2) Run via Docker

```bash
docker compose up --build

3) Open browser
http://localhost:5173
Upload documents → Ask questions.


Roadmap

✅ Basic RAG done

🔜 OCR for images (Tesseract)

🔜 Add ReRanker (BGE)

🔜 Google Drive / SharePoint / Confluence connectors

🔜 SAML / OAuth SSO

🔜 Audit logs + Usage dashboard


Why this project matters

Every company has tons of documents:

HR policies

Sales playbooks

SOPs

Client docs

Training manuals

Nobody reads them.
This project converts company knowledge → AI searchable brain.

This is the #1 most demanded AI product for enterprises right now.


Credits

Built by Shankar Kumar.


