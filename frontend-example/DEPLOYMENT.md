# Local & Production Deployment Guide

## Environment Configuration

### For Your Next.js App

Create two environment files in your Next.js project:

#### `.env.local` (for local development)
```bash
# Local development
NEXT_PUBLIC_RAG_API_URL=http://localhost:8000
```

#### `.env.production` (for production)
```bash
# Production - Update this with your deployed RAG API URL
NEXT_PUBLIC_RAG_API_URL=https://your-rag-api.onrender.com
# Or if using Railway:
# NEXT_PUBLIC_RAG_API_URL=https://your-app.railway.app
# Or if using Vercel Functions:
# NEXT_PUBLIC_RAG_API_URL=https://alleato-ai-dashboard.vercel.app/api/rag
```

## Setup Instructions

### 1. Copy the Required Files to Your Next.js App

```bash
# Copy the RAG client library
cp frontend-example/lib/rag-client.ts your-nextjs-app/lib/rag-client.ts

# Copy the chat component
cp frontend-example/chat-component-v2.tsx your-nextjs-app/components/Chat.tsx
```

### 2. Install in Your Next.js App

The RAG client automatically detects the environment:
- **Local**: Uses `http://localhost:8000`
- **Production** (alleato-ai-dashboard.vercel.app): Uses your production API URL

### 3. Use in Your Next.js Pages

```tsx
// app/chat/page.tsx
import Chat from '@/components/Chat';

export default function ChatPage() {
  return (
    <div className="min-h-screen">
      <Chat />
    </div>
  );
}
```

## Deploying the RAG API

### Option 1: Deploy to Render (Recommended)

1. Create a `render.yaml` in the RAG project (already exists)
2. Connect your GitHub repo to Render
3. Set environment variables in Render dashboard:
   - `DATABASE_URL`
   - `LLM_API_KEY`
   - `LLM_PROVIDER`
   - `LLM_MODEL`

### Option 2: Deploy to Railway

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login and initialize
railway login
railway init

# Deploy
railway up
```

### Option 3: Deploy to Vercel (as API Route)

Create `api/rag/route.ts` in your Next.js app:

```typescript
import { NextRequest, NextResponse } from 'next/server';

const PYTHON_API_URL = process.env.PYTHON_API_URL || 'http://localhost:8000';

export async function POST(request: NextRequest) {
  const body = await request.json();
  
  // Forward to Python backend
  const response = await fetch(`${PYTHON_API_URL}/chat`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  });

  return NextResponse.json(await response.json());
}
```

## CORS Configuration

The FastAPI server already includes CORS support for:
- `http://localhost:3000-3006` (development)
- `https://alleato-ai-dashboard.vercel.app` (production)
- `https://*.vercel.app` (all Vercel deployments)

To add additional domains, update `app.py`:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://alleato-ai-dashboard.vercel.app",
        "https://your-custom-domain.com",  # Add your domain
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## Testing the Setup

### Local Testing
1. Start the RAG API:
   ```bash
   python app.py
   ```

2. Start your Next.js app:
   ```bash
   npm run dev
   ```

3. Visit `http://localhost:3000/chat`

### Production Testing
1. Deploy the RAG API to your chosen platform
2. Update `NEXT_PUBLIC_RAG_API_URL` in Vercel dashboard
3. Deploy your Next.js app to Vercel
4. Visit `https://alleato-ai-dashboard.vercel.app/chat`

## Environment Variable Summary

### RAG API Server (.env)
```bash
DATABASE_URL=postgresql://...
LLM_API_KEY=sk-...
LLM_PROVIDER=openai
LLM_MODEL=gpt-4
```

### Next.js App (.env.local / Vercel Dashboard)
```bash
NEXT_PUBLIC_RAG_API_URL=https://your-rag-api.onrender.com
```

## Troubleshooting

### CORS Issues
- Check browser console for CORS errors
- Verify the origin is in the allowed list in `app.py`
- Ensure credentials are included if using cookies/auth

### Connection Issues
- Check the RAG API health: `curl https://your-api/health`
- Verify environment variables are set correctly
- Check network/firewall settings

### Streaming Issues
- Ensure your hosting platform supports SSE (Server-Sent Events)
- Render, Railway, and Vercel all support SSE
- Some proxies/CDNs may buffer responses - check settings

## Security Considerations

1. **API Keys**: Never expose API keys in client-side code
2. **Rate Limiting**: Implement rate limiting on the RAG API
3. **Authentication**: Add authentication if needed:
   ```typescript
   // In rag-client.ts
   headers: {
     'Authorization': `Bearer ${token}`,
     'Content-Type': 'application/json',
   }
   ```
4. **HTTPS**: Always use HTTPS in production