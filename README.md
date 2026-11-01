# ExpertMind — AI-Powered RAG Document Mentor

ExpertMind is an AI-powered document assistant that helps users learn from their own documents. It uses Retrieval-Augmented Generation (RAG) to retrieve relevant information, generate context-grounded answers, and provide source references.

It also identifies unanswered questions, extracts knowledge gaps, and generates personalized learning recommendations.

## Key Features

- **Document Upload:** Upload PDF and TXT documents.
- **Text Processing:** Extract text and split documents into manageable chunks.
- **Semantic Search:** Generate embeddings and retrieve relevant document chunks.
- **RAG-Based Question Answering:** Generate answers using retrieved document context.
- **Source Citations:** Display the document and chunk references used to generate answers.
- **Answerability Detection:** Identify questions that cannot be answered using the available documents.
- **Conversation Memory:** Maintain conversation context during a session.
- **Knowledge Gap Analysis:** Track unanswered questions and identify important topics.
- **Personalized Learning Recommendations:** Suggest topics and activities based on identified knowledge gaps.
- **Performance Dashboard:** Display document counts, chunks, knowledge gaps, and learning topics.

## Technology Stack

| Component | Technology |
|---|---|
| Programming Language | Python |
| Backend | FastAPI |
| Frontend | Streamlit |
| LLM | Ollama — Qwen 2.5 (3B) |
| LLM Integration | LangChain |
| Embedding Model | Sentence Transformers — all-MiniLM-L6-v2 |
| Vector Database | ChromaDB |
| Document Processing | PyPDF |
| API Server | Uvicorn |
| Testing | Pytest, HTTPX |

## System Architecture

                 USER
                   |
                   v
          Streamlit Frontend
                   |
                   v
             FastAPI Backend
                   |
          +--------+--------+
          |                 |
          v                 v
    Document Upload     User Question
          |                 |
          v                 v
    Text Extraction    Query Embedding
          |                 |
          v                 v
     Text Chunking     ChromaDB Search
          |                 |
          v                 v
    Text Embeddings    Relevant Chunks
          |                 |
          v                 v
       ChromaDB <------ Retrieval
                            |
                            v
                     Context + Query
                            |
                            v
                      Ollama LLM
                            |
                            v
                    Generated Answer
                            |
                            v
                    Source References

          Knowledge Gap Analysis
                   |
                   v
            Topic Extraction
                   |
                   v
         Learning Recommendations
                   |
                   v
             Dashboard

## Project Structure

```text
ExpertMind/
│
├── backend/
│   └── app/
│       ├── config.py
│       ├── main.py
│       ├── schemas.py
│       │
│       └── services/
│           ├── answerability_checker.py
│           ├── conversation_memory.py
│           ├── dashboard_service.py
│           ├── document_loader.py
│           ├── document_manager.py
│           ├── document_service.py
│           ├── embedding_service.py
│           ├── knowledge_gap_analyzer.py
│           ├── knowledge_gap_tracker.py
│           ├── learning_recommender.py
│           ├── llm_service.py
│           ├── rag_pipeline.py
│           ├── retriever.py
│           ├── text_chunker.py
│           ├── topic_extractor.py
│           └── vector_store.py
│
├── frontend/
│   └── app.py
│
├── data/
├── models/
├── notebooks/
├── outputs/
├── reports/
├── tests/
├── vector_store/
│
└── requirements.txt
```

## Installation and Setup

### 1. Clone the repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd ExpertMind
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Install and configure Ollama

Install Ollama from:

https://ollama.com/

Download the required model:

```bash
ollama pull qwen2.5:3b
```

Ensure Ollama is running before starting the application.

### 5. Start the FastAPI backend

```bash
python -m uvicorn backend.app.main:app --reload --port 8000
```

Backend:

http://127.0.0.1:8000

API documentation:

http://127.0.0.1:8000/docs

### 6. Start the Streamlit frontend

Open another terminal:

```bash
python -m streamlit run frontend/app.py --server.port 8502
```

Frontend:

http://localhost:8502

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Root endpoint |
| GET | `/health` | Application health check |
| POST | `/api/v1/chat` | Ask questions using RAG |
| POST | `/api/v1/documents/upload` | Upload documents |
| GET | `/api/v1/documents` | List uploaded documents |
| DELETE | `/api/v1/documents/{document_id}` | Delete a document |
| GET | `/api/v1/knowledge-gaps` | Retrieve knowledge gaps |
| DELETE | `/api/v1/knowledge-gaps` | Clear knowledge gaps |
| GET | `/api/v1/knowledge-gaps/analyze` | Analyze unanswered questions |
| GET | `/api/v1/learning-recommendations` | Generate learning recommendations |
| GET | `/api/v1/dashboard` | Retrieve dashboard metrics |

## Testing

Run automated tests:

```bash
python -m pytest -q
```

Latest verified result:

```text
14 passed in 8.56s
```

## Current Project Validation

The application has been tested with:

- 4 uploaded documents
- 51 indexed chunks
- 10 recorded knowledge gaps
- 6 identified learning topics
- Successful document retrieval with source references
- Successful unanswered-question detection
- Personalized learning recommendations
- 14 passing automated tests

These figures represent the latest local test environment and may change as documents and questions are added.

## Future Enhancements

- User authentication and multi-user support
- Persistent conversation history
- Advanced document summarization
- Improved recommendation ranking
- Cloud deployment
- Monitoring and performance analytics

## Project Objective

ExpertMind demonstrates how Large Language Models, semantic search, vector databases, and Retrieval-Augmented Generation can be combined to build a practical AI-powered knowledge assistant.

The project focuses on reducing unsupported AI responses by grounding generated answers in retrieved document content while helping users identify and improve their knowledge gaps.