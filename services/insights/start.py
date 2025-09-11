#!/usr/bin/env python3
"""
Startup script for Insights Service
Handles Railway PORT environment variable properly
"""

import os
import sys

def main():
    # Get port from environment variable, with fallback
    port = int(os.getenv("PORT", 8002))
    
    # Import uvicorn here to ensure dependencies are loaded
    import uvicorn
    
    print(f"Starting Insights Service on port {port}")
    
    # Start uvicorn server with FastAPI app that includes pipeline
    uvicorn.run(
        "src.api:app",
        host="0.0.0.0",
        port=port,
        log_level="info"
    )

if __name__ == "__main__":
    main()