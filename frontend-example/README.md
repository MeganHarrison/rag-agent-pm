# Next.js Integration Guide for RAG Agent

This guide shows how to integrate the RAG Agent API with your Next.js application.

## Available Endpoints

The FastAPI server provides two main endpoints:

1. **POST `/chat`** - Non-streaming chat endpoint
2. **POST `/chat/stream`** - Streaming chat endpoint (Server-Sent Events)

## Setup

### 1. Environment Variables

Add to your `.env.local`:

```bash
RAG_API_URL=http://localhost:8000  # Or your deployed URL
```

### 2. API Route (Optional)

If you want to proxy through Next.js API routes, use the provided `nextjs-api-route.ts` file:

```bash
# Copy to your Next.js app
cp nextjs-api-route.ts your-app/app/api/chat/route.ts
```

### 3. Chat Component

Use the provided `chat-component.tsx` as a starting point:

```bash
# Copy to your Next.js app
cp chat-component.tsx your-app/app/components/Chat.tsx
```

## Direct API Usage

You can also call the FastAPI endpoints directly from your Next.js app:

### Non-Streaming Example

```typescript
const response = await fetch('http://localhost:8000/chat', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    message: 'What are the ASRS requirements?',
    conversation_history: [],
    session_id: 'unique-session-id'
  }),
});

const data = await response.json();
console.log(data.response);
```

### Streaming Example

```typescript
const response = await fetch('http://localhost:8000/chat/stream', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    message: 'Explain the sprinkler system requirements',
    conversation_history: [],
    session_id: 'unique-session-id'
  }),
});

const reader = response.body.getReader();
const decoder = new TextDecoder();

while (true) {
  const { done, value } = await reader.read();
  if (done) break;
  
  const chunk = decoder.decode(value);
  const lines = chunk.split('\n');
  
  for (const line of lines) {
    if (line.startsWith('data: ')) {
      const data = JSON.parse(line.slice(6));
      
      if (data.type === 'text') {
        // Handle text chunks
        console.log(data.data);
      }
    }
  }
}
```

## CORS Configuration

The FastAPI server is configured to accept requests from:
- `http://localhost:3000-3006` (development)
- `https://alleato-ai-dashboard.vercel.app`
- `https://rag-agent-chat.vercel.app`
- Any `*.vercel.app` domain

To add your domain, update the CORS settings in `app.py`.

## Request/Response Format

### Request
```typescript
interface ChatRequest {
  message: string;
  conversation_history?: Array<{
    role: 'user' | 'assistant';
    content: string;
  }>;
  session_id?: string;
}
```

### Response
```typescript
interface ChatResponse {
  response: string;
  session_id: string;
  tool_calls?: Array<{
    tool: string;
    args: any;
  }>;
}
```

### Streaming Events
```typescript
// Text chunk
{ type: 'text', data: 'chunk of text' }

// Tool call
{ type: 'tool_call', data: { tool: 'semantic_search', args: {...} } }

// Tool result
{ type: 'tool_result', data: { result: '...' } }

// Complete
{ type: 'complete', data: { response: 'full response', tool_calls: [...] } }

// Error
{ type: 'error', data: 'error message' }
```

## Testing

1. Start the FastAPI server:
```bash
python app.py
```

2. Test the endpoints:
```bash
# Health check
curl http://localhost:8000/health

# Chat endpoint
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello", "conversation_history": []}'

# Streaming endpoint
curl -X POST http://localhost:8000/chat/stream \
  -H "Content-Type: application/json" \
  -d '{"message": "Tell me about ASRS", "conversation_history": []}'
```

## Deployment

For production, deploy the FastAPI server to a service like:
- Render
- Railway
- AWS Lambda
- Google Cloud Run
- Vercel (using Python runtime)

Update your `RAG_API_URL` environment variable to point to the deployed URL.