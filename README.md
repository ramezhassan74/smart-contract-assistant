# 🔗 Smart Contract Assistant

AI-powered **RAG-based Q&A** system for **Solidity** and **Smart Contract** development.

Built with **LangChain**, **Google Gemini**, **FAISS**, and **Gradio**.

---

## ✨ Features

- 💬 **Ask Questions** — Get AI-powered answers about smart contracts
- 📄 **Document Ingestion** — Upload PDF, TXT, MD, or Solidity files
- 🔍 **RAG Pipeline** — Retrieval-Augmented Generation for accurate answers
- 🌐 **Dual Interface** — Gradio UI or FastAPI REST API

## 📁 Project Structure

```
smart contract assistant/
├── main.py                  # Entry point
├── requirements.txt         # Dependencies
├── app/
│   ├── config.py            # Configuration
│   ├── embeddings.py        # Embedding model
│   ├── vector_store.py      # FAISS vector store
│   ├── ingestion.py         # Document ingestion pipeline
│   ├── retriever.py         # Document retriever
│   └── qa_chain.py          # QA chain (Gemini + RAG)
├── server/
│   └── api.py               # FastAPI server
├── ui/
│   └── gradio_app.py        # Gradio interface
└── data/
    └── docs/                # Place your documents here
```

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set API Key

Create a `.env` file in the project root:

```env
GOOGLE_API_KEY=your_google_api_key_here
```

### 3. Add Documents

Place your `.pdf`, `.txt`, `.md`, or `.sol` files in `data/docs/`.

### 4. Run

```bash
# Gradio UI (default)
python main.py

# FastAPI server
python main.py --mode api

# Custom host/port
python main.py --host 0.0.0.0 --port 8080
```

## 🔌 API Endpoints

| Method | Endpoint   | Description              |
|--------|------------|--------------------------|
| GET    | `/health`  | Health check             |
| POST   | `/ask`     | Ask a question           |
| POST   | `/ingest`  | Run ingestion pipeline   |
| POST   | `/upload`  | Upload a document        |

## 📜 License

MIT
