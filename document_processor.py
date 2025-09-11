"""
Background worker for processing document vectorization and insight generation.
This service polls the database for new documents and processes them automatically.
"""

import asyncio
import logging
import json
import os
from datetime import datetime, timedelta
from typing import Optional, Dict, Any

import asyncpg
import httpx
from dotenv import load_dotenv

from lib.utils.db_utils import create_db_pool
from services.project_insights_service import ProjectInsightsService
from ingestion.intelligent_chunker import IntelligentChunker
from ingestion.embedder import create_embedder

load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DocumentProcessor:
    """Service for processing documents in the background."""
    
    def __init__(self):
        self.db_pool = None
        self.insights_service = None
        self.chunker = None
        self.embedder = None
        self.vectorization_api_url = os.getenv('VECTORIZATION_API_URL', 'http://localhost:8001')
        self.processing = False
        
    async def initialize(self):
        """Initialize the processor."""
        self.db_pool = await create_db_pool()
        
        self.insights_service = ProjectInsightsService()
        await self.insights_service.initialize()
        
        self.chunker = IntelligentChunker(
            base_chunk_size=1000,
            chunk_overlap=200,
            enable_hierarchical=True,
            enable_semantic=True
        )
        
        self.embedder = create_embedder()
        
        logger.info("Document processor initialized")
    
    async def get_next_queued_document(self) -> Optional[Dict[str, Any]]:
        """Get the next document from the processing queue."""
        try:
            async with self.db_pool.acquire() as conn:
                row = await conn.fetchrow(
                    "SELECT * FROM get_next_queued_document()"
                )
                
                if row:
                    return {
                        'queue_id': str(row['queue_id']),
                        'document_id': str(row['document_id']),
                        'project_id': row['project_id']
                    }
                
                return None
                
        except Exception as e:
            logger.error(f"Failed to get queued document: {e}")
            return None
    
    async def process_document(self, queue_item: Dict[str, Any]) -> bool:
        """Process a single document: vectorize and generate insights."""
        
        document_id = queue_item['document_id']
        project_id = queue_item['project_id']
        queue_id = queue_item['queue_id']
        
        logger.info(f"Processing document {document_id}")
        
        try:
            # Step 1: Vectorize the document
            await self.vectorize_document(document_id)
            
            # Step 2: Generate insights
            await self.generate_insights(document_id, project_id)
            
            # Step 3: Mark as completed
            await self.mark_completed(queue_id, success=True)
            
            logger.info(f"Successfully processed document {document_id}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to process document {document_id}: {e}")
            await self.mark_completed(queue_id, success=False, error=str(e))
            return False
    
    async def vectorize_document(self, document_id: str):
        """Vectorize a document using the vectorization API."""
        
        # Call the vectorization API
        async with httpx.AsyncClient(timeout=300.0) as client:
            response = await client.post(
                f"{self.vectorization_api_url}/api/vectorize",
                json={
                    "document_id": document_id,
                    "force_revectorize": False,
                    "use_intelligent_chunking": True
                }
            )
            
            if response.status_code != 200:
                raise Exception(f"Vectorization API failed: {response.text}")
            
            result = response.json()
            
            if not result.get('success'):
                raise Exception(f"Vectorization failed: {result.get('error', 'Unknown error')}")
            
            logger.info(f"Vectorized document {document_id}: {result.get('chunks_created', 0)} chunks created")
    
    async def generate_insights(self, document_id: str, project_id: int):
        """Generate AI insights for a document."""
        
        try:
            # Get document content
            async with self.db_pool.acquire() as conn:
                document = await conn.fetchrow(
                    """
                    SELECT id, title, content, document_type, metadata
                    FROM documents
                    WHERE id = $1::uuid
                    """,
                    document_id
                )
                
                if not document:
                    raise Exception(f"Document {document_id} not found")
            
            # Generate insights using the insights service
            await self.insights_service.generate_document_insights(
                document_id=document_id,
                content=document['content'],
                title=document['title'],
                document_type=document['document_type'],
                project_id=project_id,
                metadata=json.loads(document['metadata']) if document['metadata'] else {}
            )
            
            logger.info(f"Generated insights for document {document_id}")
            
        except Exception as e:
            logger.error(f"Failed to generate insights for document {document_id}: {e}")
            raise
    
    async def mark_completed(self, queue_id: str, success: bool = True, error: Optional[str] = None):
        """Mark a queue item as completed or failed."""
        
        try:
            async with self.db_pool.acquire() as conn:
                await conn.execute(
                    "SELECT complete_queued_document($1::uuid, $2, $3)",
                    queue_id,
                    success,
                    error
                )
                
        except Exception as e:
            logger.error(f"Failed to mark queue item {queue_id} as completed: {e}")
    
    async def process_queue(self):
        """Main processing loop."""
        
        if self.processing:
            return
            
        self.processing = True
        
        try:
            while True:
                # Get next document to process
                queue_item = await self.get_next_queued_document()
                
                if queue_item:
                    await self.process_document(queue_item)
                else:
                    # No documents to process, wait before checking again
                    await asyncio.sleep(10)
                    
        except Exception as e:
            logger.error(f"Processing loop error: {e}")
        finally:
            self.processing = False
    
    async def health_check(self) -> Dict[str, Any]:
        """Check the health of the processor."""
        
        try:
            async with self.db_pool.acquire() as conn:
                # Check queue status
                queue_stats = await conn.fetchrow("""
                    SELECT 
                        COUNT(*) as total,
                        COUNT(*) FILTER (WHERE status = 'pending') as pending,
                        COUNT(*) FILTER (WHERE status = 'processing') as processing,
                        COUNT(*) FILTER (WHERE status = 'failed') as failed
                    FROM insights_generation_queue
                    WHERE created_at > NOW() - INTERVAL '24 hours'
                """)
                
                return {
                    'status': 'healthy',
                    'processing': self.processing,
                    'queue_stats': dict(queue_stats) if queue_stats else {},
                    'timestamp': datetime.now().isoformat()
                }
                
        except Exception as e:
            return {
                'status': 'unhealthy',
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    async def cleanup_old_queue_items(self):
        """Clean up old completed queue items."""
        
        try:
            async with self.db_pool.acquire() as conn:
                # Delete completed items older than 7 days
                deleted = await conn.execute("""
                    DELETE FROM insights_generation_queue
                    WHERE status = 'completed'
                      AND processed_at < NOW() - INTERVAL '7 days'
                """)
                
                logger.info(f"Cleaned up {deleted} old queue items")
                
        except Exception as e:
            logger.error(f"Failed to cleanup queue: {e}")


async def run_processor():
    """Main function to run the document processor."""
    
    processor = DocumentProcessor()
    await processor.initialize()
    
    logger.info("Starting document processor")
    
    # Start background tasks
    tasks = [
        asyncio.create_task(processor.process_queue()),
        # Cleanup task runs every hour
        asyncio.create_task(periodic_cleanup(processor))
    ]
    
    try:
        await asyncio.gather(*tasks)
    except KeyboardInterrupt:
        logger.info("Shutting down processor")
        for task in tasks:
            task.cancel()
        
        await processor.db_pool.close()


async def periodic_cleanup(processor: DocumentProcessor):
    """Periodic cleanup task."""
    
    while True:
        try:
            await asyncio.sleep(3600)  # Run every hour
            await processor.cleanup_old_queue_items()
        except asyncio.CancelledError:
            break
        except Exception as e:
            logger.error(f"Cleanup task error: {e}")


if __name__ == "__main__":
    asyncio.run(run_processor())
