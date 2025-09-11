"""
FastAPI server for Insights Service
Provides health check and status endpoints while running the insights pipeline
"""

import asyncio
import logging
from datetime import datetime
from typing import Dict, Any

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from .main import InsightsPipeline, initialize_pipeline

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="RAG Agent PM Insights Service",
    description="AI insights generation and monitoring pipeline",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global pipeline instance
pipeline = None

@app.on_event("startup")
async def startup_event():
    """Initialize and start the insights pipeline."""
    global pipeline
    try:
        logger.info("Initializing Insights Pipeline...")
        pipeline = await initialize_pipeline()
        logger.info("Insights Pipeline started successfully")
    except Exception as e:
        logger.error(f"Failed to start Insights Pipeline: {e}")
        raise

@app.on_event("shutdown")
async def shutdown_event():
    """Stop the insights pipeline."""
    global pipeline
    if pipeline:
        logger.info("Stopping Insights Pipeline...")
        await pipeline.stop()
        logger.info("Insights Pipeline stopped")

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    global pipeline
    
    is_healthy = pipeline is not None and pipeline.is_running
    
    return {
        "status": "healthy" if is_healthy else "unhealthy",
        "service": "rag-agent-pm-insights",
        "timestamp": datetime.now().isoformat(),
        "pipeline_running": is_healthy
    }

@app.get("/")
async def root():
    """Root endpoint."""
    return {"message": "RAG Agent PM Insights Service", "status": "running"}

@app.get("/status")
async def get_status():
    """Get detailed service status."""
    global pipeline
    
    if not pipeline:
        raise HTTPException(status_code=503, detail="Pipeline not initialized")
    
    status = {
        "service": "insights",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat(),
        "pipeline_running": pipeline.is_running,
        "scheduler_running": pipeline.scheduler.running if hasattr(pipeline.scheduler, 'running') else False
    }
    
    return status