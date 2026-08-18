# DStarix AI Assistant

A production-ready AI assistant built with **Gemini, RAG, FAISS, conversation memory, tool calling, and FastAPI**.

## Features

- Gemini-powered AI assistant
- PDF-based RAG
- Gemini embeddings + FAISS
- Query transformation
- Document retrieval and reranking
- Conversation memory
- Tool calling
- FastAPI REST API
- API-key authentication
- Streaming responses
- Evaluation framework
- Swagger documentation

## Architecture

```text
User
  ↓
FastAPI
  ↓
API Authentication
  ↓
AI Assistant
  ├── Tool Calling
  └── RAG Pipeline
        ↓
   Query Transformation
        ↓
   FAISS Retrieval
        ↓
     Reranking
        ↓
      Context
        ↓
      Gemini
        ↓
   Final Answer
        ↓
 Conversation Memory
```

## Tech Stack

- Python
- FastAPI
- Gemini API
- LangChain
- FAISS
- Pydantic
- Uvicorn
- python-dotenv

## Project Structure

```text
week-6-dstarix-ai-assistant/
├── api/
├── documents/
├── evaluation/
├── memory/
├── rag/
├── screenshots/
├── tools/
├── .env.example
├── .gitignore
├── config.py
├── exceptions.py
├── llm.py
├── main.py
├── requirements.txt
└── README.md
```

## Setup

```bash
git clone <your-github-repository-url>
cd week-6-dstarix-ai-assistant
python -m venv .venv
```

Windows:

```powershell
.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create `.env`:

```env
GOOGLE_API_KEY=your-gemini-api-key
API_KEY=your-secret-api-key
```

**Do not commit `.env` to GitHub.**

## Document Ingestion

Place the PDF inside `documents/` and run:

```bash
python rag/ingestion.py
```

This loads the PDF, chunks the text, generates embeddings, and stores them in FAISS.

## Run

```bash
uvicorn main:app --reload
```

API:

```text
http://127.0.0.1:8000
```

Swagger:

```text
http://127.0.0.1:8000/docs
```

## API

### `POST /chat`

Request:

```json
{
  "question": "What happens in the second phase?"
}
```

Response:

```json
{
  "answer": "The second phase focuses on practical projects under mentor guidance.",
  "sources": [
    {
      "source": "sample.pdf",
      "page": 2
    }
  ]
}
```

### `POST /chat/stream`

Streams the model response as plain text.

## Authentication

Send the application API key using:

```text
x-api-key: your-secret-api-key
```

Invalid keys return `401 Unauthorized`.

## RAG Pipeline

```text
PDF
 ↓
Chunking
 ↓
Gemini Embeddings
 ↓
FAISS
 ↓
Query Transformation
 ↓
Retrieval
 ↓
Reranking
 ↓
Context
 ↓
Gemini
 ↓
Answer + Sources
```

The assistant returns relevant document sources and page numbers where available.

## Tool Calling

Available tools:

- `get_project_info`
- `get_internship_phase`

Tools provide structured project and internship information.

## Conversation Memory

The assistant maintains recent conversation history using the memory module.

## Evaluation

Run:

```bash
python evaluation/run_evaluation.py
```

The evaluation framework compares generated answers with expected answers using keyword coverage.

## Screenshots

Project screenshots are available in:

```text
screenshots/
```

They demonstrate Swagger API usage, authentication, RAG responses, sources, and evaluation.

## Security

Never commit:

```text
.env
.venv/
```

Store API keys in environment variables.

## License

Developed as part of the **DStarix Generative AI Internship – Week 6**.
