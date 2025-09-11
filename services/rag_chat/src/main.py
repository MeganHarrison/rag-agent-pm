"""FastAPI server for RAG Agent - deployable on Render."""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import List, Optional, AsyncGenerator
import asyncio
import json
import uuid

from services.rag_chat.src.rag_agent import search_agent
from shared.utils.db_utils import initialize_database
from shared.utils.config import load_settings
from pydantic_ai import Agent

app = FastAPI(title="RAG Agent API", version="1.0.0")

# Configure CORS for Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:3001", 
        "http://localhost:3002",
        "http://localhost:3003",
        "http://localhost:3004",
        "http://localhost:3005",
        "http://localhost:3006",
        "https://alleato-ai-dashboard.vercel.app",
        "https://rag-agent-chat.vercel.app",
        "https://*.vercel.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load settings
settings = load_settings()

# Request/Response models
class ChatMessage(BaseModel):
    role: str  # "user" or "assistant"
    content: str

class ChatRequest(BaseModel):
    message: str
    conversation_history: Optional[List[ChatMessage]] = []
    session_id: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    session_id: str
    tool_calls: Optional[List[dict]] = None


async def stream_response(
    message: str, 
    conversation_history: List[ChatMessage],
    session_id: str
) -> AsyncGenerator[str, None]:
    """Stream agent responses as Server-Sent Events."""
    
    # Create and initialize dependencies
    deps = AgentDependencies(session_id=session_id)
    await deps.initialize()
    
    # Build context from conversation history
    context = "\n".join([
        f"{msg.role}: {msg.content}" 
        for msg in conversation_history[-6:]
    ]) if conversation_history else ""
    
    prompt = f"""Previous conversation:
{context}

User: {message}

Search the knowledge base to answer the user's question. Choose the appropriate search strategy (semantic_search or hybrid_search) based on the query type. Provide a comprehensive summary of your findings."""

    try:
        # Stream the agent execution
        async with search_agent.iter(prompt, deps=deps) as run:
            
            tool_calls = []
            response_text = ""
            
            async for node in run:
                
                # Handle tool call nodes
                if Agent.is_tool_call_node(node):
                    for tool_call in node:
                        tool_info = {
                            "tool": tool_call.name,
                            "args": tool_call.args
                        }
                        tool_calls.append(tool_info)
                        
                        # Send tool call event
                        yield f"data: {json.dumps({'type': 'tool_call', 'data': tool_info})}\n\n"
                
                # Handle tool response nodes
                elif Agent.is_tool_return_node(node):
                    for tool_return in node:
                        # Send tool result event
                        yield f"data: {json.dumps({'type': 'tool_result', 'data': {'result': str(tool_return.response)[:200]}})}\n\n"
                
                # Handle model text response
                elif Agent.is_text_chunk_node(node):
                    chunk = node.delta
                    response_text += chunk
                    # Send text chunk event
                    yield f"data: {json.dumps({'type': 'text', 'data': chunk})}\n\n"
            
            # Send final complete event
            yield f"data: {json.dumps({'type': 'complete', 'data': {'response': response_text, 'tool_calls': tool_calls}})}\n\n"
            
    except Exception as e:
        yield f"data: {json.dumps({'type': 'error', 'data': str(e)})}\n\n"
    finally:
        # Clean up resources
        try:
            await deps.cleanup()
        except:
            pass


@app.get("/")
async def root():
    """Health check endpoint."""
    return {"status": "healthy", "service": "RAG Agent API"}


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Non-streaming chat endpoint."""
    
    # Generate session ID if not provided
    session_id = request.session_id or str(uuid.uuid4())
    
    # Create and initialize dependencies
    deps = AgentDependencies(session_id=session_id)
    await deps.initialize()
    
    # Build context
    context = "\n".join([
        f"{msg.role}: {msg.content}" 
        for msg in request.conversation_history[-6:]
    ]) if request.conversation_history else ""
    
    prompt = f"""Previous conversation:
{context}

User: {request.message}

Search the knowledge base to answer the user's question. Choose the appropriate search strategy (semantic_search or hybrid_search) based on the query type. Provide a comprehensive summary of your findings."""
    
    try:
        # Run agent
        result = await search_agent.run(prompt, deps=deps)
        
        # Extract tool calls from result if available
        tool_calls = []
        if hasattr(result, '_tool_calls'):
            for tc in result._tool_calls:
                tool_calls.append({
                    "tool": tc.name,
                    "args": tc.args
                })
        
        return ChatResponse(
            response=str(result.response) if hasattr(result, 'response') else str(result),
            session_id=session_id,
            tool_calls=tool_calls if tool_calls else None
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        # Clean up resources
        try:
            await deps.cleanup()
        except:
            pass


@app.post("/chat/stream")
async def chat_stream(request: ChatRequest):
    """Streaming chat endpoint using Server-Sent Events."""
    
    # Generate session ID if not provided
    session_id = request.session_id or str(uuid.uuid4())
    
    return StreamingResponse(
        stream_response(
            request.message, 
            request.conversation_history,
            session_id
        ),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",  # Disable Nginx buffering
        }
    )


@app.get("/health")
async def health_check():
    """Detailed health check with dependency status."""
    
    health_status = {
        "status": "healthy",
        "checks": {
            "api": True,
            "llm_configured": bool(settings.llm_api_key),
            "model": settings.llm_model,
        }
    }
    
    # Test vector store connection if needed
    try:
        # Add your vector store health check here
        health_status["checks"]["vector_store"] = True
    except Exception:
        health_status["checks"]["vector_store"] = False
        health_status["status"] = "degraded"
    
    return health_status


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)