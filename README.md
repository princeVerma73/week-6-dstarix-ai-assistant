# DStarix AI Assistant

A production-ready AI assistant built using Generative AI, Retrieval-Augmented Generation (RAG), conversation memory, and tool calling.

## Features

- Gemini-powered AI assistant
- Retrieval-Augmented Generation (RAG)
- PDF document ingestion
- Text chunking
- Gemini embeddings
- FAISS vector database
- Query transformation
- Document retrieval
- LLM-based document reranking
- Conversation memory
- Tool calling
- FastAPI REST API
- API key authentication
- Streaming responses
- Evaluation framework
- Swagger API documentation

## Architecture

```text
User
  |
  v
FastAPI API
  |
  v
API Key Authentication
  |
  v
AI Assistant
  |
  +----------------------+----------------------+
  |                                             |
  v                                             v
Tool Calling                                RAG Pipeline
  |                                             |
  |                                             v
  |                                      Query Transformation
  |                                             |
  |                                             v
  |                                      FAISS Retrieval
  |                                             |
  |                                             v
  |                                       Reranking
  |                                             |
  |                                             v
  |                                          Context
  |                                             |
  +----------------------+----------------------+
                         |
                         v
                       Gemini
                         |
                         v
                   Final Answer
                         |
                         v
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
|
+-- api/
|   +-- __init__.py
|   +-- routes.py
|   +-- schemas.py
|
+-- documents/
|
+-- evaluation/
|   +-- __init__.py
|   +-- test_cases.py
|   +-- run_evaluation.py
|
+-- memory/
|   +-- __init__.py
|   +-- conversation.py
|
+-- rag/
|   +-- __init__.py
|   +-- ingestion.py
|   +-- retrieval.py
|   +-- query_transform.py
|   +-- reranker.py
|   +-- prompts.py
|
+-- screenshots/
|
+-- tools/
|   +-- __init__.py
|   +-- tools.py
|
+-- .env
+-- .gitignore
+-- config.py
+-- exceptions.py
+-- llm.py
+-- main.py
+-- requirements.txt
+-- README.md
```

## Setup

### 1. Clone the repository

```bash
git clone <your-github-repository-url>
cd week-6-dstarix-ai-assistant
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows:

```powershell
.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root:

```env
GOOGLE_API_KEY=your-gemini-api-key
API_KEY=your-secret-api-key
```

Do not commit `.env` to GitHub.

## Document Ingestion

Place the required PDF document inside the `documents/` directory.

Run the ingestion pipeline:

```bash
python rag/ingestion.py
```

The ingestion pipeline:

1. Loads the PDF
2. Splits the document into chunks
3. Generates Gemini embeddings
4. Stores the embeddings in FAISS

## Run the Application

Start the FastAPI server:

```bash
uvicorn main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

Swagger documentation:

```text
http://127.0.0.1:8000/docs
```

## API Endpoints

### Chat

```text
POST /chat
```

The endpoint accepts a question and returns an AI-generated answer.

Example request:

```json
{
  "question": "What happens in the second phase?"
}
```

Example response:

```json
{
  "answer": "The second phase focuses on applying your knowledge by contributing to practical projects under mentor guidance."
}
```

### Streaming Chat

```text
POST /chat/stream
```

Example request:

```json
{
  "question": "Explain Generative AI in simple words"
}
```

The response is streamed as the model generates the answer.

## API Authentication

The API uses an API key for authentication.

The key must be sent through the following header:

```text
x-api-key
```

Example:

```text
x-api-key: your-secret-api-key
```

Requests with an invalid API key return:

```text
401 Unauthorized
```

## RAG Pipeline

The Retrieval-Augmented Generation pipeline follows these steps:

1. Load PDF documents
2. Split documents into chunks
3. Generate embeddings
4. Store embeddings in FAISS
5. Transform the user's query
6. Retrieve relevant documents
7. Rerank the retrieved documents
8. Build the context
9. Generate the final answer using Gemini

This allows the assistant to answer questions using information from the provided documents.

## Query Transformation

The user's original question is transformed into a concise search query before retrieval.

Example:

```text
Original query:
What happens in the second phase?

Transformed query:
second phase description
```

This improves document retrieval by focusing the search on the important concepts.

## Document Reranking

The system initially retrieves multiple documents from FAISS.

The retrieved documents are then evaluated for relevance and reranked.

Example:

```text
Retrieved documents: 5
Reranked documents: 3
```

The most relevant documents are then passed to the final RAG prompt.

## Conversation Memory

The assistant maintains conversation history using the conversation memory module.

Stored messages contain:

- `role`
- `content`

Example:

```python
[
    {
        "role": "user",
        "content": "What happens in the second phase?"
    },
    {
        "role": "assistant",
        "content": "The second phase focuses on practical projects."
    }
]
```

Conversation history is included when generating responses where appropriate.

## Tool Calling

The assistant can use tools when a question can be answered using structured project information.

Available tools:

- `get_project_info`
- `get_internship_phase`

Example tool result:

```python
{
    "phase_1": "Learning Phase",
    "phase_2": "Project Phase"
}
```

The model can decide when a tool is useful and request the appropriate tool.

## Evaluation

The project contains an evaluation framework inside:

```text
evaluation/
```

Evaluation test cases are defined in:

```text
evaluation/test_cases.py
```

Run the evaluation:

```bash
python evaluation/run_evaluation.py
```

The evaluation checks generated answers against expected answers using keyword coverage.

Example result:

```text
Test 1
Question: What happens in the second phase?

Score: 0.90
PASS

Evaluation Summary
Passed: 1/1
Accuracy: 100.00%
```

## Error Handling

The application includes error handling for:

- Invalid API keys
- Invalid request data
- Empty questions
- Unexpected assistant errors
- Service failures

Invalid requests are handled using appropriate HTTP responses instead of exposing internal Python errors.

## Swagger Documentation

FastAPI automatically provides interactive API documentation.

Open:

```text
http://127.0.0.1:8000/docs
```

From Swagger, you can test:

- `POST /chat`
- `POST /chat/stream`

including API-key authentication.

## Screenshots

Screenshots demonstrating the project are available in:

```text
screenshots/
```

The screenshots include:

- Swagger API
- Chat endpoint
- API authentication
- Streaming endpoint
- RAG responses
- Evaluation results

## Example Workflow

A typical question goes through the following workflow:

```text
User Question
      |
      v
API Authentication
      |
      v
Question Processing
      |
      +------------------+
      |                  |
      v                  v
Tool Calling            RAG
                           |
                           v
                    Query Transformation
                           |
                           v
                    FAISS Retrieval
                           |
                           v
                      Reranking
                           |
                           v
                        Context
                           |
                           v
                         Gemini
                           |
                           v
                     Final Answer
                           |
                           v
                  Conversation Memory
```

## Current Capabilities

The assistant currently supports:

- Document-based question answering
- Semantic document retrieval
- Query transformation
- Document reranking
- Gemini-powered generation
- Conversation memory
- Tool calling
- REST API access
- API authentication
- Streaming responses
- Basic automated evaluation

## Future Improvements

- Persistent database-backed conversation memory
- Improved semantic evaluation
- Additional tools
- Better observability and logging
- Production database integration
- Frontend interface
- Cloud deployment
- Improved authentication and authorization
- More advanced RAG evaluation
- Multi-document knowledge bases

## Security

The following files should never be committed:

```text
.env
.venv/
```

The Gemini API key and application API key must be stored in environment variables.

## License

This project was developed as part of the DStarix Generative AI Internship.
