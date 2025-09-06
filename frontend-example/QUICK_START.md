# Quick Start Guide - RAG Integration for Alleato AI Dashboard

## Your URLs
- **Local API**: http://localhost:8000
- **Production API**: https://rag-agent-pm.onrender.com
- **Production App**: https://alleato-ai-dashboard.vercel.app

## Step 1: Copy These Files to Your Next.js App

```bash
# From this directory (rag-agent-pm/frontend-example), copy:
cp lib/rag-client.ts ~/path-to-your-nextjs-app/lib/
cp chat-component-v2.tsx ~/path-to-your-nextjs-app/components/Chat.tsx
```

## Step 2: Environment Variables

### For Local Development (.env.local)
```bash
NEXT_PUBLIC_RAG_API_URL=http://localhost:8000
```

### For Production (Vercel Dashboard)
Go to your Vercel project settings and add:
```bash
NEXT_PUBLIC_RAG_API_URL=https://rag-agent-pm.onrender.com
```

## Step 3: Use in Your Next.js App

### Create a Chat Page (app/chat/page.tsx)
```tsx
import Chat from '@/components/Chat';

export default function ChatPage() {
  return (
    <main className="min-h-screen bg-gray-50">
      <Chat />
    </main>
  );
}
```

### Or Add to Existing Page
```tsx
import Chat from '@/components/Chat';

export default function YourPage() {
  return (
    <div>
      {/* Your existing content */}
      <Chat />
    </div>
  );
}
```

## Step 4: Test It

### Local Testing
1. Start the RAG API locally:
   ```bash
   cd rag-agent-pm
   python app.py
   ```

2. Start your Next.js app:
   ```bash
   npm run dev
   ```

3. Go to `http://localhost:3000/chat`

### Production Testing
Your production API is already deployed at https://rag-agent-pm.onrender.com

Just deploy your Next.js app to Vercel and it will automatically use the production API.

## How It Works

The `rag-client.ts` automatically detects your environment:

- When running on `localhost` → uses `http://localhost:8000`
- When running on `alleato-ai-dashboard.vercel.app` → uses `https://rag-agent-pm.onrender.com`
- You can override with `NEXT_PUBLIC_RAG_API_URL` environment variable

## Available Features

- ✅ Streaming chat responses
- ✅ Non-streaming chat responses  
- ✅ Session management
- ✅ Conversation history
- ✅ Tool call visibility
- ✅ Error handling
- ✅ Auto-environment detection

## API Endpoints

Your RAG API provides:
- `POST /chat` - Regular chat
- `POST /chat/stream` - Streaming chat
- `GET /health` - Health check

## Troubleshooting

### CORS Issues
CORS is already configured for:
- `http://localhost:3000-3006`
- `https://alleato-ai-dashboard.vercel.app`
- All `*.vercel.app` domains

### Connection Issues
Test the API:
```bash
# Local
curl http://localhost:8000/health

# Production
curl https://rag-agent-pm.onrender.com/health
```

### Need Help?
The API is currently running locally at http://localhost:8000
The production API is deployed at https://rag-agent-pm.onrender.com