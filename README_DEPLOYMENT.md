# RAG Pipeline Deployment Configuration

## ✅ **COMPLETED** - Railway Multi-Service Setup

Your RAG pipeline is now configured for Railway deployment with **2 separate services**:

### 🏗️ Architecture

```
Next.js App → RAG Chat API → Supabase Database ← Vectorization API
                     ↓              ↑
              Document Search    Auto-processing
                     ↓              ↑
               Vector Embeddings   New Documents
                     ↓              ↑
                AI Insights ← Database Triggers
```

### 🚀 Services to Deploy

#### 1. **rag-agent-api** (Port 8000)
- **Purpose**: Chat interface with RAG functionality
- **Dockerfile**: `Dockerfile` (main)
- **Entry point**: `python api/app.py`
- **Health check**: `/health`

#### 2. **rag-vectorization-api** (Port 8001)  
- **Purpose**: Background document processing & insights generation
- **Dockerfile**: `Dockerfile.vectorization`
- **Entry point**: `python vectorization_api.py`
- **Health check**: `/health`

#### 3. **rag-database**
- **Purpose**: PostgreSQL database with vector extensions
- **Schema**: `sql/unified_schema.sql`
- **Triggers**: Automatic document queuing for processing

### 🔧 Environment Variables

Set these for **both services**:

```bash
# Database
DATABASE_URL=postgresql://user:pass@host:port/db

# LLM Configuration  
LLM_API_KEY=your_openai_or_anthropic_key
LLM_PROVIDER=openai  # or anthropic
LLM_MODEL=gpt-4     # or claude-3-sonnet

# Service URLs (for internal communication)
VECTORIZATION_API_URL=https://your-vectorization-api.railway.app
```

### 📋 Railway Deployment Steps

1. **Create Railway Project**
   ```bash
   railway login
   railway new rag-pipeline
   ```

2. **Deploy Database Service**
   - Add PostgreSQL database
   - Run `sql/unified_schema.sql` to initialize

3. **Deploy Chat API Service**
   - Connect GitHub repo
   - Use `Dockerfile` (main)
   - Set environment variables
   - Deploy to port 8000

4. **Deploy Vectorization Service**
   - Same repo, different service
   - Use `Dockerfile.vectorization` 
   - Set environment variables
   - Deploy to port 8001

### 🔄 How It Works

1. **Document Ingestion**:
   - New rows added to `documents` table in Supabase
   - Database trigger queues document for processing

2. **Automatic Processing**:
   - Vectorization API processes queued documents
   - Creates embeddings and stores in `chunks` table
   - Generates AI insights and stores in `ai_insights` table

3. **RAG Chat**:
   - Chat API receives user queries
   - Searches vector embeddings for relevant context
   - Generates AI responses with retrieved context

4. **Next.js Integration**:
   - Frontend calls Chat API for conversations
   - Displays insights from `ai_insights` table
   - Shows real-time processing status

### 🧪 Testing

Run the test suite after deployment:

```bash
python test_pipeline.py
```

Or test manually:
```bash
# Health checks
curl https://your-chat-api.railway.app/health
curl https://your-vectorization-api.railway.app/health

# Test chat
curl -X POST https://your-chat-api.railway.app/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What are the key project insights?"}'

# Test vectorization
curl https://your-vectorization-api.railway.app/api/documents/pending
```

### 📊 Monitoring

Track these metrics:
- **Queue status**: `insights_generation_queue` table
- **Processing logs**: Railway service logs
- **Insights generated**: `ai_insights` table count
- **API health**: `/health` endpoints

### 🔗 Next.js Configuration

In your Next.js app environment:

```env
RAG_CHAT_API_URL=https://your-rag-agent-api.railway.app
RAG_VECTORIZATION_API_URL=https://your-rag-vectorization-api.railway.app
```

### 🛠️ Files Created/Updated

- ✅ `railway.json` - Railway deployment config
- ✅ `Dockerfile.vectorization` - Vectorization service Docker config
- ✅ `document_processor.py` - Background processing worker
- ✅ `test_pipeline.py` - Pipeline testing script
- ✅ `RAILWAY_DEPLOYMENT.md` - Deployment guide
- ✅ Updated `Dockerfile` - Main chat API config
- ✅ Updated `vectorization_api.py` - Port configuration

### 🎯 Benefits of This Setup

1. **Scalable**: Each service can scale independently
2. **Reliable**: Database triggers ensure no documents are missed
3. **Fast**: Chat API optimized for real-time responses
4. **Automated**: Background processing handles vectorization
5. **Monitored**: Health checks and queue monitoring built-in

Your RAG pipeline is now ready for Railway deployment! 🚀
