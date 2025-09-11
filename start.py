#!/usr/bin/env python3
"""
Railway startup script with PORT fix and better error handling
"""

import sys
import os
import asyncio
import traceback
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Ensure PORT is set correctly
if not os.getenv("PORT"):
    os.environ["PORT"] = "8000"
    print("⚙️ PORT not set, defaulting to 8000")

print(f"🌐 PORT configured as: {os.getenv('PORT')}")

async def diagnostic_check():
    """Run diagnostic checks before starting the API."""
    print("🔍 Running Railway deployment diagnostics...")
    
    # Check port configuration
    port = os.getenv("PORT", "8000")
    try:
        port_int = int(port)
        print(f"✅ PORT: {port_int}")
    except ValueError:
        print(f"❌ Invalid PORT value: {port}")
        return False
    
    # Check environment variables
    required_env_vars = [
        "DATABASE_URL",
        "OPENAI_API_KEY"
    ]
    
    missing_vars = []
    for var in required_env_vars:
        value = os.getenv(var)
        if not value:
            missing_vars.append(var)
        else:
            # Show only last 4 characters for security
            print(f"✅ {var}: {'*' * max(0, len(value) - 4)}{value[-4:] if len(value) >= 4 else '*' * len(value)}")
    
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
        print(f"✅ Settings loaded: model={getattr(settings, 'llm_model', 'unknown')}")
    except Exception as e:
        print(f"❌ Settings error: {e}")
        traceback.print_exc()
        return False
    
    # Test dependencies initialization (basic test)
    try:
        print("🔗 Testing dependencies...")
        deps = AgentDependencies()
        print("✅ Dependencies created")
        # Note: Skip full initialization in diagnostic to avoid blocking
    except Exception as e:
        print(f"⚠️ Dependencies warning: {e}")
        # Continue anyway - some dependency issues can be resolved at runtime
    
    return True

def start_api():
    """Start the FastAPI application."""
    print("🚀 Starting FastAPI application...")
    
    try:
        import uvicorn
        from api.app import app
        
        # Get port with proper error handling
        port_str = os.getenv("PORT", "8000")
        try:
            port = int(port_str)
        except ValueError:
            print(f"❌ Invalid PORT value '{port_str}', using 8000")
            port = 8000
        
        print(f"🌐 Starting server on 0.0.0.0:{port}")
        
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
    print("🤖 PM RAG Agent - Railway Startup v2")
    print("="*60)
    
    # Print environment info for debugging
    print(f"🐍 Python version: {sys.version}")
    print(f"📁 Working directory: {os.getcwd()}")
    print(f"🌐 PORT environment: {os.getenv('PORT', 'NOT_SET')}")
    
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
            print("❌ Diagnostics failed - attempting to start anyway...")
            print("="*60)
            start_api()  # Try to start anyway - some issues may resolve at runtime
            
    except Exception as e:
        print(f"❌ Startup error: {e}")
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
