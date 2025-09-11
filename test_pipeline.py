"""
Test script for the RAG pipeline deployment.
Run this after deploying to Railway to verify everything works.
"""

import asyncio
import httpx
import json
import os
from datetime import datetime

# Configuration
CHAT_API_URL = os.getenv('RAG_CHAT_API_URL', 'http://localhost:8000')
VECTORIZATION_API_URL = os.getenv('RAG_VECTORIZATION_API_URL', 'http://localhost:8001')

async def test_health_checks():
    """Test health endpoints for both services."""
    
    print("🔍 Testing Health Checks...")
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        # Test chat API
        try:
            response = await client.get(f"{CHAT_API_URL}/health")
            if response.status_code == 200:
                print("✅ Chat API is healthy")
                print(f"   Response: {response.json()}")
            else:
                print(f"❌ Chat API unhealthy: {response.status_code}")
        except Exception as e:
            print(f"❌ Chat API error: {e}")
        
        # Test vectorization API
        try:
            response = await client.get(f"{VECTORIZATION_API_URL}/health")
            if response.status_code == 200:
                print("✅ Vectorization API is healthy")
                print(f"   Response: {response.json()}")
            else:
                print(f"❌ Vectorization API unhealthy: {response.status_code}")
        except Exception as e:
            print(f"❌ Vectorization API error: {e}")

async def test_chat():
    """Test the chat functionality."""
    
    print("\n💬 Testing Chat Functionality...")
    
    test_query = "What are the key project insights from recent meetings?"
    
    async with httpx.AsyncClient(timeout=60.0) as client:
        try:
            response = await client.post(
                f"{CHAT_API_URL}/chat",
                json={
                    "message": test_query,
                    "conversation_history": [],
                    "session_id": "test-session"
                }
            )
            
            if response.status_code == 200:
                result = response.json()
                print("✅ Chat API working")
                print(f"   Query: {test_query}")
                print(f"   Response: {result.get('response', 'No response')[:200]}...")
                if result.get('tool_calls'):
                    print(f"   Tool calls: {len(result['tool_calls'])}")
            else:
                print(f"❌ Chat failed: {response.status_code}")
                print(f"   Error: {response.text}")
                
        except Exception as e:
            print(f"❌ Chat error: {e}")

async def test_vectorization():
    """Test document vectorization."""
    
    print("\n⚡ Testing Vectorization...")
    
    # First, check for pending documents
    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            response = await client.get(f"{VECTORIZATION_API_URL}/api/documents/pending")
            
            if response.status_code == 200:
                result = response.json()
                pending_count = result.get('count', 0)
                print(f"📄 Found {pending_count} pending documents")
                
                if pending_count > 0:
                    # Test vectorizing the first pending document
                    first_doc = result['documents'][0]
                    doc_id = first_doc['id']
                    
                    print(f"   Testing vectorization of document: {first_doc['title']}")
                    
                    vectorize_response = await client.post(
                        f"{VECTORIZATION_API_URL}/api/vectorize",
                        json={
                            "document_id": doc_id,
                            "force_revectorize": True,
                            "use_intelligent_chunking": True
                        }
                    )
                    
                    if vectorize_response.status_code == 200:
                        vectorize_result = vectorize_response.json()
                        print("✅ Vectorization successful")
                        print(f"   Chunks created: {vectorize_result.get('chunks_created', 0)}")
                        print(f"   Processing time: {vectorize_result.get('processing_time_ms', 0)}ms")
                    else:
                        print(f"❌ Vectorization failed: {vectorize_response.status_code}")
                        print(f"   Error: {vectorize_response.text}")
                else:
                    print("   No pending documents to test")
                    
            else:
                print(f"❌ Failed to get pending documents: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Vectorization test error: {e}")

async def test_search():
    """Test document search functionality."""
    
    print("\n🔍 Testing Document Search...")
    
    test_query = "project timeline"
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            response = await client.post(
                f"{VECTORIZATION_API_URL}/api/documents/search",
                json={
                    "query": test_query,
                    "limit": 5,
                    "use_semantic": True
                }
            )
            
            if response.status_code == 200:
                result = response.json()
                results_count = len(result.get('results', []))
                print(f"✅ Search working - found {results_count} results")
                
                if results_count > 0:
                    print(f"   Sample result: {result['results'][0].get('title', 'No title')}")
            else:
                print(f"❌ Search failed: {response.status_code}")
                print(f"   Error: {response.text}")
                
        except Exception as e:
            print(f"❌ Search error: {e}")

async def run_tests():
    """Run all tests."""
    
    print("🧪 RAG Pipeline Test Suite")
    print("=" * 50)
    print(f"Chat API URL: {CHAT_API_URL}")
    print(f"Vectorization API URL: {VECTORIZATION_API_URL}")
    print(f"Test started at: {datetime.now()}")
    print()
    
    await test_health_checks()
    await test_vectorization() 
    await test_search()
    await test_chat()
    
    print("\n" + "=" * 50)
    print("✅ Test suite completed!")
    print("\n💡 Next steps:")
    print("1. If tests pass, your RAG pipeline is working")
    print("2. Add documents to your Supabase documents table")
    print("3. They should auto-vectorize and generate insights")
    print("4. Test the chat API from your Next.js app")

if __name__ == "__main__":
    asyncio.run(run_tests())
