#!/usr/bin/env python3
"""
Ingest FM Global Insights Document into RAG System
"""

import os
import sys
import asyncio
import asyncpg
import json
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv
import hashlib
from openai import OpenAI

# Load environment variables
load_dotenv()
load_dotenv('ingestion/.env')

# Add ingestion module to path
sys.path.append(str(Path(__file__).parent))

from ingestion.chunker import ChunkingConfig, create_chunker
from ingestion.embedder import create_embedder

async def ingest_fm_insights():
    """Ingest the FM Global insights document into the database."""
    
    # Configuration
    insights_file = Path("insights/westfield_collective_project_insights.md")
    
    if not insights_file.exists():
        print(f"❌ File not found: {insights_file}")
        return
    
    # Read the document
    with open(insights_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print(f"📄 Processing: {insights_file.name}")
    print(f"📏 Document size: {len(content):,} characters")
    
    # Initialize database connection
    database_url = os.getenv('DATABASE_URL')
    if not database_url:
        print("❌ DATABASE_URL not found in environment")
        return
    
    conn = await asyncpg.connect(database_url)
    
    try:
        # Configure chunking
        chunking_config = ChunkingConfig(
            chunk_size=1500,
            chunk_overlap=200,
            min_chunk_size=100,
            use_semantic_splitting=True
        )
        
        # Create chunker
        chunker = create_chunker(chunking_config)
        
        # Generate chunks
        print("🔄 Creating semantic chunks...")
        chunks = await chunker.chunk_document(
            content=content,
            title="FM Global ASRS Project Insights",
            source=insights_file.name,
            metadata={
                "type": "project_insights",
                "project": "FM Global ASRS",
                "created_at": datetime.now().isoformat()
            }
        )
        
        print(f"✅ Created {len(chunks)} chunks")
        
        # Create embedder
        embedder = create_embedder(
            model="text-embedding-3-small",
            use_cache=True
        )
        
        # Generate embeddings
        print("🔄 Generating embeddings...")
        embedded_chunks = await embedder.embed_chunks(chunks)
        
        print(f"✅ Generated {len(embedded_chunks)} embeddings")
        
        # Store in database
        print("💾 Storing in database...")
        
        # Create documents table if it doesn't exist
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS documents (
                id SERIAL PRIMARY KEY,
                content TEXT NOT NULL,
                metadata JSONB,
                embedding vector(1536),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Clear existing FM insights entries
        await conn.execute("""
            DELETE FROM documents 
            WHERE metadata->>'source' = $1
        """, insights_file.name)
        
        # Insert new chunks with embeddings
        inserted = 0
        for chunk in embedded_chunks:
            if chunk.embedding:
                # Convert embedding to PostgreSQL vector format
                embedding_str = f"[{','.join(map(str, chunk.embedding))}]"
                
                await conn.execute("""
                    INSERT INTO documents (content, metadata, embedding)
                    VALUES ($1, $2, $3::vector)
                """, chunk.content, json.dumps(chunk.metadata), embedding_str)
                
                inserted += 1
        
        print(f"✅ Stored {inserted} chunks in database")
        
        # Verify storage
        count = await conn.fetchval("""
            SELECT COUNT(*) FROM documents 
            WHERE metadata->>'source' = $1
        """, insights_file.name)
        
        print(f"📊 Verified: {count} chunks in database")
        
        # Test a sample query
        print("\n🔍 Testing search functionality...")
        
        # Create a test query
        test_query = "What are the main challenges with the FM Global project?"
        
        # Generate embedding for query
        client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        response = client.embeddings.create(
            model="text-embedding-3-small",
            input=test_query
        )
        query_embedding = response.data[0].embedding
        query_embedding_str = f"[{','.join(map(str, query_embedding))}]"
        
        # Search for similar chunks
        results = await conn.fetch("""
            SELECT 
                content,
                metadata,
                1 - (embedding <=> $1::vector) as similarity
            FROM documents
            WHERE metadata->>'source' = $2
            ORDER BY embedding <=> $1::vector
            LIMIT 3
        """, query_embedding_str, insights_file.name)
        
        print(f"\n📋 Top 3 results for: '{test_query}'")
        print("-" * 60)
        for i, result in enumerate(results, 1):
            print(f"\n{i}. Similarity: {result['similarity']:.3f}")
            print(f"   Content: {result['content'][:200]}...")
        
        print("\n✅ FM Global insights document successfully ingested!")
        
    except Exception as e:
        print(f"❌ Error during ingestion: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        await conn.close()


if __name__ == "__main__":
    asyncio.run(ingest_fm_insights())