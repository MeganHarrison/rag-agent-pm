#!/usr/bin/env python3
"""
Automated AI Insights Generation System

This script provides multiple methods for automatically generating insights:
1. Real-time: Process new documents as they're added
2. Scheduled: Run periodically to process unprocessed documents
3. On-demand: Trigger via API endpoint or webhook
"""

import asyncio
import asyncpg
import os
import sys
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List
from dotenv import load_dotenv
from openai import OpenAI
import argparse

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('insights_generation.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Configure OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class AutomatedInsightsGenerator:
    """Automated system for generating AI insights."""
    
    def __init__(self, pool: asyncpg.Pool):
        self.pool = pool
        
    async def process_unprocessed_documents(self) -> Dict[str, Any]:
        """
        Find and process all documents that don't have insights yet.
        This is the main method for scheduled/batch processing.
        """
        results = {
            'documents_processed': 0,
            'insights_generated': 0,
            'projects_affected': set(),
            'errors': []
        }
        
        try:
            # Find documents without insights
            unprocessed = await self.pool.fetch("""
                SELECT DISTINCT 
                    d.id as doc_id,
                    d.project_id,
                    d.title,
                    d.content,
                    p.name as project_name
                FROM documents d
                JOIN projects p ON p.id = d.project_id
                LEFT JOIN ai_insights ai ON ai.document_id = d.id::text
                WHERE d.content IS NOT NULL
                    AND LENGTH(d.content) > 100
                    AND ai.id IS NULL
                ORDER BY d.created_at DESC
                LIMIT 50  -- Process in batches to avoid timeouts
            """)
            
            logger.info(f"Found {len(unprocessed)} unprocessed documents")
            
            for doc in unprocessed:
                try:
                    logger.info(f"Processing: {doc['title']} (Project: {doc['project_name']})")
                    
                    # Get existing insights for duplicate prevention
                    existing = await self.pool.fetch("""
                        SELECT LOWER(title) || ':' || insight_type as unique_key
                        FROM ai_insights 
                        WHERE project_id = $1
                    """, doc['project_id'])
                    
                    existing_keys = {row['unique_key'] for row in existing}
                    
                    # Extract insights using AI
                    insights = await self._extract_insights_with_ai(
                        doc_id=str(doc['doc_id']),
                        title=doc['title'],
                        content=doc['content'],
                        project_name=doc['project_name']
                    )
                    
                    # Store insights
                    stored = await self._store_insights(
                        insights=insights,
                        project_id=doc['project_id'],
                        document_id=str(doc['doc_id']),
                        existing_keys=existing_keys
                    )
                    
                    results['documents_processed'] += 1
                    results['insights_generated'] += stored
                    results['projects_affected'].add(doc['project_id'])
                    
                    logger.info(f"  Generated {stored} insights")
                    
                except Exception as e:
                    error_msg = f"Error processing {doc['title']}: {str(e)}"
                    logger.error(error_msg)
                    results['errors'].append(error_msg)
            
        except Exception as e:
            logger.error(f"Fatal error in batch processing: {str(e)}")
            results['errors'].append(f"Fatal error: {str(e)}")
        
        return results
    
    async def process_new_document(self, document_id: int) -> Dict[str, Any]:
        """
        Process a single new document immediately.
        This is for real-time processing when documents are added.
        """
        results = {
            'document_id': document_id,
            'insights_generated': 0,
            'errors': []
        }
        
        try:
            # Get document details
            doc = await self.pool.fetchrow("""
                SELECT 
                    d.id,
                    d.project_id,
                    d.title,
                    d.content,
                    p.name as project_name
                FROM documents d
                JOIN projects p ON p.id = d.project_id
                WHERE d.id = $1
                    AND d.content IS NOT NULL
                    AND LENGTH(d.content) > 100
            """, document_id)
            
            if not doc:
                results['errors'].append(f"Document {document_id} not found or has no content")
                return results
            
            logger.info(f"Processing new document: {doc['title']}")
            
            # Get existing insights for duplicate prevention
            existing = await self.pool.fetch("""
                SELECT LOWER(title) || ':' || insight_type as unique_key
                FROM ai_insights 
                WHERE project_id = $1
            """, doc['project_id'])
            
            existing_keys = {row['unique_key'] for row in existing}
            
            # Extract insights
            insights = await self._extract_insights_with_ai(
                doc_id=str(doc['id']),
                title=doc['title'],
                content=doc['content'],
                project_name=doc['project_name']
            )
            
            # Store insights
            stored = await self._store_insights(
                insights=insights,
                project_id=doc['project_id'],
                document_id=str(doc['id']),
                existing_keys=existing_keys
            )
            
            results['insights_generated'] = stored
            logger.info(f"Generated {stored} insights for document {document_id}")
            
        except Exception as e:
            error_msg = f"Error processing document {document_id}: {str(e)}"
            logger.error(error_msg)
            results['errors'].append(error_msg)
        
        return results
    
    async def process_project_incrementally(self, project_id: int) -> Dict[str, Any]:
        """
        Process only new documents for a specific project.
        Useful for periodic updates of active projects.
        """
        results = {
            'project_id': project_id,
            'documents_processed': 0,
            'insights_generated': 0,
            'errors': []
        }
        
        try:
            # Find documents added in last 7 days without insights
            recent_docs = await self.pool.fetch("""
                SELECT DISTINCT 
                    d.id as doc_id,
                    d.title,
                    d.content,
                    p.name as project_name
                FROM documents d
                JOIN projects p ON p.id = d.project_id
                LEFT JOIN ai_insights ai ON ai.document_id = d.id::text
                WHERE d.project_id = $1
                    AND d.content IS NOT NULL
                    AND LENGTH(d.content) > 100
                    AND d.created_at > NOW() - INTERVAL '7 days'
                    AND ai.id IS NULL
                ORDER BY d.created_at DESC
            """, project_id)
            
            logger.info(f"Found {len(recent_docs)} recent unprocessed documents for project {project_id}")
            
            # Get existing insights for duplicate prevention
            existing = await self.pool.fetch("""
                SELECT LOWER(title) || ':' || insight_type as unique_key
                FROM ai_insights 
                WHERE project_id = $1
            """, project_id)
            
            existing_keys = {row['unique_key'] for row in existing}
            
            for doc in recent_docs:
                try:
                    insights = await self._extract_insights_with_ai(
                        doc_id=str(doc['doc_id']),
                        title=doc['title'],
                        content=doc['content'],
                        project_name=doc['project_name']
                    )
                    
                    stored = await self._store_insights(
                        insights=insights,
                        project_id=project_id,
                        document_id=str(doc['doc_id']),
                        existing_keys=existing_keys
                    )
                    
                    results['documents_processed'] += 1
                    results['insights_generated'] += stored
                    
                except Exception as e:
                    results['errors'].append(f"Error with {doc['title']}: {str(e)}")
            
        except Exception as e:
            results['errors'].append(f"Fatal error: {str(e)}")
        
        return results
    
    async def _extract_insights_with_ai(
        self,
        doc_id: str,
        title: str,
        content: str,
        project_name: str
    ) -> List[Dict[str, Any]]:
        """Extract high-quality insights using OpenAI."""
        
        # Truncate content if too long
        max_content_length = 8000
        if len(content) > max_content_length:
            content = content[:max_content_length] + "..."
        
        prompt = f"""You are an expert project manager analyzing documents for the "{project_name}" project.
        
Extract SPECIFIC, ACTIONABLE insights from this document. DO NOT generate generic observations.
Each insight must include concrete details like names, dates, amounts, and specific actions.

Document: {title}
Content: {content}

Extract insights in these categories:

1. ACTION ITEMS (things that need to be done):
- Include WHO needs to do it (specific name or role)
- WHAT exactly needs to be done (specific task)
- WHEN it needs to be done (date or timeframe)
- WHY it's important (impact if not done)

2. DECISIONS (choices that were made):
- What was decided
- Who made the decision
- Financial or timeline impact
- Rationale for the decision

3. RISKS (potential problems):
- Specific risk description
- Severity (critical/high/medium/low)
- Impact if it occurs
- Mitigation strategy mentioned

4. KEY FACTS (important information):
- Budget amounts mentioned
- Timeline milestones
- Technical specifications
- Stakeholder commitments

Return ONLY a JSON array with this structure:
[
  {{
    "type": "action_item|decision|risk|fact",
    "title": "Brief descriptive title (max 100 chars)",
    "description": "Detailed description with all context, names, dates, amounts",
    "severity": "critical|high|medium|low",
    "assignee": "Person's name if mentioned",
    "due_date": "YYYY-MM-DD if mentioned",
    "financial_impact": "Dollar amount if mentioned",
    "confidence": 0.9
  }}
]

Guidelines:
- Be SPECIFIC - use actual names, dates, amounts from the document
- NO generic insights like "Review budget" without context
- Include enough detail that someone can take action
- If no meaningful insights exist, return empty array []
"""

        try:
            response = await asyncio.to_thread(
                client.chat.completions.create,
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a project management expert extracting actionable insights."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.1,
                max_tokens=2000
            )
            
            insights_json = response.choices[0].message.content
            
            # Clean up the response
            insights_json = insights_json.strip()
            if insights_json.startswith("```json"):
                insights_json = insights_json[7:]
            if insights_json.endswith("```"):
                insights_json = insights_json[:-3]
            
            insights = json.loads(insights_json)
            
            # Validate and clean insights
            valid_insights = []
            for insight in insights:
                if len(insight.get('description', '')) < 50:
                    continue
                if 'type' in insight and 'title' in insight and 'description' in insight:
                    valid_insights.append(insight)
            
            return valid_insights
            
        except Exception as e:
            logger.error(f"AI extraction failed: {e}")
            return []
    
    async def _store_insights(
        self,
        insights: List[Dict[str, Any]],
        project_id: int,
        document_id: str,
        existing_keys: set
    ) -> int:
        """Store insights with duplicate prevention."""
        
        stored_count = 0
        
        for insight in insights:
            try:
                # Generate unique key
                unique_key = f"{insight.get('title', '').lower()}:{insight.get('type', 'fact')}"
                
                # Skip if duplicate
                if unique_key in existing_keys:
                    continue
                
                # Map insight types
                insight_type = insight.get('type', 'fact')
                type_mapping = {
                    'action_item': 'action_item',
                    'decision': 'decision', 
                    'risk': 'risk',
                    'fact': 'fact',
                }
                insight_type = type_mapping.get(insight_type, 'fact')
                
                # Map severity
                severity = insight.get('severity', 'medium')
                if severity not in ['critical', 'high', 'medium', 'low']:
                    severity = 'medium'
                
                # Parse due date
                due_date = None
                if insight.get('due_date'):
                    try:
                        due_date = datetime.strptime(insight['due_date'], '%Y-%m-%d').date()
                    except:
                        pass
                
                # Store insight
                await self.pool.execute("""
                    INSERT INTO ai_insights (
                        project_id,
                        insight_type,
                        title,
                        description,
                        severity,
                        status,
                        confidence_score,
                        assignee,
                        due_date,
                        document_id,
                        financial_impact,
                        created_at
                    ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12)
                    ON CONFLICT DO NOTHING
                """,
                    project_id,
                    insight_type,
                    insight.get('title', 'Untitled')[:200],
                    insight.get('description', ''),
                    severity,
                    'open',
                    insight.get('confidence', 0.8),
                    insight.get('assignee'),
                    due_date,
                    document_id,
                    insight.get('financial_impact'),
                    datetime.now().isoformat()
                )
                
                stored_count += 1
                existing_keys.add(unique_key)
                
            except Exception as e:
                logger.error(f"Failed to store insight: {str(e)}")
                continue
        
        return stored_count


async def run_scheduled_batch():
    """Run scheduled batch processing of unprocessed documents."""
    
    DATABASE_URL = os.getenv("DATABASE_URL")
    
    if not os.getenv("OPENAI_API_KEY"):
        logger.error("OPENAI_API_KEY not found in environment variables")
        return
    
    try:
        pool = await asyncpg.create_pool(DATABASE_URL, min_size=1, max_size=10)
        logger.info("Starting scheduled batch processing...")
        
        generator = AutomatedInsightsGenerator(pool)
        results = await generator.process_unprocessed_documents()
        
        logger.info(f"Batch processing complete:")
        logger.info(f"  Documents processed: {results['documents_processed']}")
        logger.info(f"  Insights generated: {results['insights_generated']}")
        logger.info(f"  Projects affected: {len(results['projects_affected'])}")
        
        if results['errors']:
            logger.warning(f"  Errors encountered: {len(results['errors'])}")
        
        await pool.close()
        
    except Exception as e:
        logger.error(f"Fatal error in scheduled batch: {str(e)}")


async def process_single_document(document_id: int):
    """Process a single document immediately."""
    
    DATABASE_URL = os.getenv("DATABASE_URL")
    
    if not os.getenv("OPENAI_API_KEY"):
        logger.error("OPENAI_API_KEY not found")
        return
    
    try:
        pool = await asyncpg.create_pool(DATABASE_URL, min_size=1, max_size=10)
        
        generator = AutomatedInsightsGenerator(pool)
        results = await generator.process_new_document(document_id)
        
        logger.info(f"Document processing complete:")
        logger.info(f"  Document ID: {results['document_id']}")
        logger.info(f"  Insights generated: {results['insights_generated']}")
        
        await pool.close()
        
    except Exception as e:
        logger.error(f"Fatal error: {str(e)}")


async def main():
    """Main entry point with command line arguments."""
    
    parser = argparse.ArgumentParser(description='Automated AI Insights Generation')
    parser.add_argument('--mode', choices=['batch', 'document', 'project'], 
                       default='batch',
                       help='Processing mode')
    parser.add_argument('--document-id', type=int,
                       help='Document ID for single document processing')
    parser.add_argument('--project-id', type=int,
                       help='Project ID for incremental project processing')
    
    args = parser.parse_args()
    
    if args.mode == 'batch':
        await run_scheduled_batch()
    elif args.mode == 'document':
        if not args.document_id:
            logger.error("Document ID required for document mode")
            sys.exit(1)
        await process_single_document(args.document_id)
    elif args.mode == 'project':
        if not args.project_id:
            logger.error("Project ID required for project mode")
            sys.exit(1)
        
        DATABASE_URL = os.getenv("DATABASE_URL")
        pool = await asyncpg.create_pool(DATABASE_URL, min_size=1, max_size=10)
        generator = AutomatedInsightsGenerator(pool)
        results = await generator.process_project_incrementally(args.project_id)
        
        logger.info(f"Project processing complete:")
        logger.info(f"  Documents processed: {results['documents_processed']}")
        logger.info(f"  Insights generated: {results['insights_generated']}")
        
        await pool.close()


if __name__ == "__main__":
    asyncio.run(main())