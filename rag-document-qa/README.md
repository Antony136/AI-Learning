# RAG Document Q&A

A document question-answering application built to learn and demonstrate Retrieval-Augmented Generation (RAG).

The application allows users to upload PDF documents and ask questions about their contents. It retrieves relevant document chunks, reranks them, and uses a local Qwen 2.5 7B model through Ollama to generate grounded answers.

## Architecture

```text
PDF
 ↓
Text Extraction
 ↓
Sentence-based Chunking
 ↓
Embeddings
 ↓
PostgreSQL + pgvector
 ↓
User Question
 ↓
Query Normalization
 ↓
Conversation-aware Query Rewrite
 ↓
Query Correction
 ↓
Multi-query Generation
 ↓
Vector Search
 ↓
Reciprocal Rank Fusion
 ↓
Cross-encoder Reranking
 ↓
Rerank Threshold
 ↓
Context Construction
 ↓
Qwen 2.5 7B
 ↓
Answer + Sources
```

## Features

* PDF document upload
* PDF text extraction
* Sentence-based text chunking
* Overlapping chunks
* Local text embeddings using `nomic-embed-text`
* PostgreSQL storage
* pgvector similarity search
* Document-specific retrieval
* Query normalization
* Conversation-aware query rewriting
* Query spelling correction
* Multi-query retrieval
* Reciprocal Rank Fusion (RRF)
* Cross-encoder reranking
* Reranking threshold for low-confidence retrieval
* Grounded answer generation
* Source and page information
* Follow-up questions using conversation history
* React frontend
* FastAPI backend
* Local LLM inference using Ollama

## Tech Stack

### Backend

* Python
* FastAPI
* PostgreSQL
* pgvector
* psycopg
* pypdf
* Sentence Transformers
* Ollama

### LLM

* Qwen 2.5 Coder 7B

### Embedding Model

* `nomic-embed-text`

### Reranker

* `cross-encoder/ms-marco-MiniLM-L-6-v2`

### Frontend

* React
* Vite

## Project Structure

```text
rag-document-qa/
│
├── app/
│   ├── core/
│   │   ├── config.py
│   │   ├── database.py
│   │   └── test_database.py
│   │
│   ├── ingestion/
│   │   ├── extract.py
│   │   ├── chunker.py
│   │   ├── embeddings.py
│   │   └── pipeline.py
│   │
│   ├── retrieval/
│   │   ├── vector_store.py
│   │   ├── similarity.py
│   │   ├── search.py
│   │   ├── reranker.py
│   │   ├── query_transform.py
│   │   ├── multi_query.py
│   │   ├── fusion.py
│   │   ├── query_correction.py
│   │   ├── vocabulary.py
│   │   ├── query_rewrite.py
│   │   ├── query_normalization.py
│   │   └── query_rewriter.py
│   │
│   ├── generation/
│   │   ├── llm.py
│   │   ├── prompts.py
│   │   └── sources.py
│   │
│   ├── storage/
│   │   ├── chunks.py
│   │   └── documents.py
│   │
│   ├── evaluation/
│   │   └── grounding.py
│   │
│   ├── api/
│   │   └── documents.py
│   │
│   ├── rag.py
│   └── main.py
│
├── frontend/
├── documents/
├── experiments/
├── tests/
│
├── .env
├── .gitignore
├── pytest.ini
├── requirements.txt
└── README.md
```

## Setup

### 1. Clone the repository

```bash
git clone <your-repository-url>
cd rag-document-qa
```

### 2. Create a virtual environment

```powershell
python -m venv .venv
```

Activate it:

```powershell
.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```powershell
pip install -r requirements.txt
```

### 4. Install and start Ollama

Make sure Ollama is installed and running.

Pull the required models:

```powershell
ollama pull qwen2.5-coder:7b
ollama pull nomic-embed-text
```

### 5. Configure PostgreSQL

Create a PostgreSQL database with pgvector enabled.

Example:

```sql
CREATE DATABASE rag_document_qa;
```

Connect to the database and enable pgvector:

```sql
CREATE EXTENSION vector;
```

Create the required tables according to the database schema used by the application.

### 6. Configure environment variables

Create a `.env` file:

```env
DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@localhost:5432/rag_document_qa
DATABASE_URL_TEST=postgresql://postgres:YOUR_PASSWORD@localhost:5432/rag_document_qa_test
```

Do not commit `.env` to GitHub.

## Running the Backend

From the project root:

```powershell
uvicorn app.main:app --reload
```

The backend normally runs at:

```text
http://127.0.0.1:8000
```

## Running the Frontend

Open another terminal:

```powershell
cd frontend
npm install
npm run dev
```

Then open the Vite development URL shown in the terminal.

## Testing

Run the complete test suite:

```powershell
pytest
```

The project currently has:

* 69 passing tests
* 2 dependency deprecation warnings

The warnings do not currently cause test failures.

## RAG Evaluation

The project also contains retrieval and answer evaluation experiments.

The retrieval evaluation measures:

* Recall@1
* Recall@3
* Recall@5
* Mean Reciprocal Rank (MRR)

The answer evaluation checks whether generated claims are supported by the retrieved context.

The latest grounding evaluation tested:

* 5 questions
* 13 expected claims
* 12 supported claims
* 1 unsupported claim
* 92.31% grounding score

These evaluations are based on a small development dataset and are intended for learning and experimentation rather than production benchmarking.

## Generation Verification

The project includes:

```text
experiments/generation_test.py
```

This verifies two important behaviors:

1. The model can answer when the information exists in the supplied context.
2. The model refuses to answer when the requested information is not present in the context.

Example behavior:

```text
Context contains the answer
        ↓
Grounded answer
```

and:

```text
Context does not contain the answer
        ↓
"I could not find the answer in the document."
```

## Learning Goals

This project was built as a practical learning project covering:

* Retrieval-Augmented Generation
* Embeddings
* Vector databases
* Semantic search
* Query transformation
* Multi-query retrieval
* Reciprocal Rank Fusion
* Cross-encoder reranking
* Grounded generation
* Local LLM inference
* FastAPI
* React
* PostgreSQL
* Automated testing
* RAG evaluation

## Project Status

Project 2 is functionally complete.

The complete flow has been manually verified from:

```text
PDF upload
 → ingestion
 → embedding
 → vector storage
 → retrieval
 → reranking
 → context construction
 → LLM generation
 → grounded answer
 → source display
```

## Next Project

This project is part of a progressive AI engineering learning path:

```text
Project 1 → LLM Playground
Project 2 → RAG Document Q&A
Project 3 → Agents and Tool Calling
Project 4 → AI Full-Stack Application
Project 5 → Advanced AI System
```
