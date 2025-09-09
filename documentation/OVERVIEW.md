# RAG Agent PM – Semantic Search Agent

## Overview

rag-agent-pm is a Retrieval-Augmented Generation (RAG) agent optimized for semantic search across Alleato’s project management documents and meetings. It enables fast, intelligent retrieval of both conceptual queries and specific facts, with support for multiple LLM providers and flexible deployment options.

⸻

## 🔑 Key Features
	•	Dual Search Strategies
	•	Semantic search for conceptual queries
	•	Hybrid search for fact-based queries (vector + text search)
	•	Vector Similarity: PostgreSQL + PGVector
	•	Multi-Provider LLM Support: OpenAI, Anthropic, Groq, Ollama, and other OpenAI-compatible APIs
	•	Streaming Responses: Real-time token streaming in CLI and API
	•	Conversation Memory: Context persistence with message scoring and compression
	•	FastAPI Backend: RESTful API with CORS support for browser apps

⸻

## 🏗️ Architecture
	1.	Agent Core (agent.py) – Pydantic-based agent with semantic + hybrid search tools
	2.	CLI Interface (cli.py) – Rich terminal UI with streaming responses
	3.	FastAPI Server (app.py) – Production-ready API with streaming endpoints
	4.	Search Tools – Automatic selection between semantic vs. hybrid
	5.	Document Processing – Intelligent chunking + embeddings stored in PostgreSQL

⸻

## ⚙️ Setup

Prerequisites
	•	Python 3.10+
	•	PostgreSQL with PGVector extension
	•	At least one LLM API key (OpenAI, Anthropic, etc.)

Installation

1. Install dependencies
pip install -r requirements.txt

2. Initialize database schema
psql -d your_database -f sql/schema.sql

3. Configure environment
export DATABASE_URL=postgresql://user:password@host:5432/database
export LLM_API_KEY=your-api-key
export LLM_PROVIDER=openai
export LLM_MODEL=gpt-4-1106-preview
export EMBEDDING_MODEL=text-embedding-3-small

4. Ingest documents
python -m ingestion.ingest --documents documents/


⸻

## 🚀 Usage

CLI Mode

python -m cli

	•	Interactive terminal with live streaming
	•	Shows tool execution + retrieved context

API Server

uvicorn app:app --reload

Endpoints:
	•	POST /chat → non-streaming chat
	•	POST /chat/stream → streaming (SSE) chat
	•	GET /health → health check

⸻

## 📂 Document Context

The /documents/ directory stores Alleato’s operational knowledge base:
	•	Weekly ops meetings
	•	Client calls (Uniqlo, Goodwill, etc.)
	•	Project reviews and design sessions
	•	Business development activities
	•	Employee onboarding/interviews

All documents are automatically chunked, embedded, and stored for retrieval.

⸻

⚡ Triggers
	1.	CLI – python -m cli
	•	Streaming Q&A with history persistence
	2.	API – uvicorn app:app
	•	POST /chat, POST /chat/stream, GET /health
	3.	Document Ingestion –

python -m ingestion.ingest --documents documents/ --clean

	•	Parses Markdown → splits into chunks → generates embeddings → stores in PostgreSQL

⸻

## 🗄️ Database Schema (Supabase/Postgres)

Document Storage

documents
	•	id UUID PK
	•	title TEXT
	•	source TEXT
	•	content TEXT
	•	metadata JSONB
	•	created_at/updated_at TIMESTAMPTZ

chunks
	•	id UUID PK
	•	document_id UUID FK
	•	content TEXT
	•	embedding VECTOR(1536)
	•	chunk_index INT
	•	metadata JSONB
	•	token_count INT
	•	created_at TIMESTAMPTZ

Conversation Memory

conversations – session-level context
conversation_messages – per-message memory + embeddings
conversation_facts – extracted entities, goals, constraints
conversation_retrievals – search results + relevance scores

⸻

## 🎯 RAG Strategy

1. Semantic Search
	•	Use case: conceptual queries
	•	Method: pure vector similarity (cosine distance)
	•	Example: “ideas about client meetings”

2. Hybrid Search
	•	Use case: exact facts / names / dates
	•	Method: vector + PostgreSQL full-text search
	•	Scoring: (vector_sim × (1-text_weight)) + (text_sim × text_weight)
	•	Example: “Uniqlo meeting on March 15th”

⸻

🧠 Advanced Features
	•	Memory Management
	•	Importance scoring
	•	Automatic compression of old messages
	•	Query Enhancement
	•	HyDE (Hypothetical Document Embeddings)
	•	Sub-query generation for complex questions
	•	Result Reranking
	•	Cross-encoder reranking
	•	MMR for diversity
	•	Recency boost

⸻

## 🔄 Data Flow

User Query → Agent → Strategy Selection
           → Database Query → Embedding Generation
           → Search Execution → Result Retrieval
           → LLM Processing → Streaming Response


⸻

📝 Document Ingestion Flow

Markdown Files → Content Extraction
               → Intelligent Chunking
               → Embedding Generation
               → PostgreSQL Storage (PGVector)
               → Vector Index Creation


⸻

✅ Key Config

DATABASE_URL=postgresql://user:password@host:5432/database
LLM_API_KEY=your-openai-key
LLM_PROVIDER=openai
LLM_MODEL=gpt-4-1106-preview
EMBEDDING_MODEL=text-embedding-3-small


⸻

This RAG agent is tailored for Alleato’s project management workflows, enabling teams to quickly search meeting history and documents with semantic + hybrid retrieval strategies.