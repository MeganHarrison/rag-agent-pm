#!/usr/bin/env python3
"""
Railway startup script with better error handling and diagnostics
"""

import sys
import os
import asyncio
import traceback
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

async def diagnostic_check():
    """Run diagnostic checks before starting the API."""
    print("🔍 Running Railway deployment diagnostics...")
    
    # Check environment variables
    required_env_vars = [
        "DATABASE_URL",
        "LLM_API_KEY", 
        "OPENAI_API_KEY"
    ]
    
    missing_vars = []
    for var in required_env_vars:
        if not os.getenv(var):
            missing_vars.append(var)
        else:
            print(f"✅ {var}: {'*' * 8}{os.getenv(var)[-4:]}")
    
    if missing_vars:
        print(f"❌ Missing environment variables: {missing_vars}")
        return False
    
    # Test imports
    try:
        print("📦 Testing imports...")
        from settings import load_settings
        from dependencies import AgentDependencies
        from agent import search_agent
        print("✅ All imports successful")
    except Exception as e:
        print(f"❌ Import error: {e}")
        traceback.print_exc()
        return False
    
    # Test settings loading
    try:
        print("⚙️ Testing settings...")
        settings = load_settings()
        print(f"✅ Settings loaded: model={settings.llm_model}")
    except Exception as e:
        print(f"❌ Settings error: {e}")
        traceback.print_exc()
        return False
    
    # Test dependencies initialization
    try:
        print("🔗 Testing dependencies...")
        deps = AgentDependencies()
        await deps.initialize()
        print("✅ Dependencies initialized")
        await deps.cleanup()
        print("✅ Dependencies cleaned up")
    except Exception as e:
        print(f"❌ Dependencies error: {e}")
        traceback.print_exc()
        return False
    
    return True

def start_api():
    """Start the FastAPI application."""
    print("🚀 Starting FastAPI application...")
    
    try:
        import uvicorn
        from api.app import app
        
        port = int(os.getenv("PORT", 8000))
        print(f"🌐 Starting server on port {port}")
        
        uvicorn.run(
            app,
            host="0.0.0.0",
            port=port,
            log_level="info",
            access_log=True,
            timeout_keep_alive=30,
            timeout_graceful_shutdown=5
        )
    except Exception as e:
        print(f"❌ Failed to start API: {e}")
        traceback.print_exc()
        sys.exit(1)

def main():
    """Main startup routine."""
    print("="*60)
    print("🤖 PM RAG Agent - Railway Startup")
    print("="*60)
    
    # Run diagnostics in a new event loop
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        diagnostics_passed = loop.run_until_complete(diagnostic_check())
        loop.close()
        
        if diagnostics_passed:
            print("✅ All diagnostics passed!")
            print("="*60)
            start_api()
        else:
            print("❌ Diagnostics failed - cannot start service")
            sys.exit(1)
            
    except Exception as e:
        print(f"❌ Startup error: {e}")
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()