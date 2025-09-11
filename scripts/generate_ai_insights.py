#!/usr/bin/env python3
"""
AI-Powered Insights Generation Script

This script uses OpenAI to extract high-quality, actionable insights from project documents.
It generates specific, detailed insights similar to the Paradise Project example.
"""

import asyncio
import asyncpg
import os
import sys
import json
from datetime import datetime, date, timedelta
from typing import Dict, Any, Optional, List
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

# Configure OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class AIInsightsGenerator:
    """Generate high-quality insights using AI."""
    
    def __init__(self, pool: asyncpg.Pool):
        self.pool = pool
        
    async def generate_insights_for_project(self, project_id: int) -> Dict[str, Any]:
        """
        Generate AI-powered insights for a specific project.
        
        Args:
            project_id: The project ID to generate insights for
            
        Returns:
            Dictionary with generation results and statistics
        """
        
        results = {
            'project_id': project_id,
            'project_name': None,
            'documents_processed': 0,
            'insights_generated': 0,
            'duplicates_prevented': 0,
            'errors': []
        }
        
        try:
            # Get project details
            project = await self.pool.fetchrow("""
                SELECT id, name, description, client_id, state
                FROM projects
                WHERE id = $1
            """, project_id)
            
            if not project:
                results['errors'].append(f"Project {project_id} not found")
                return results
                
            results['project_name'] = project['name']
            print(f"\n🔍 Processing Project: {project['name']} (ID: {project_id})")
            print("=" * 60)
            
            # Clear existing insights for fresh generation (optional)
            # await self.pool.execute("DELETE FROM ai_insights WHERE project_id = $1", project_id)
            
            # Get existing insights to prevent duplicates (using title + type as unique identifier)
            existing_insights = await self.pool.fetch("""
                SELECT LOWER(title) || ':' || insight_type as unique_key
                FROM ai_insights 
                WHERE project_id = $1
            """, project_id)
            
            existing_keys = {row['unique_key'] for row in existing_insights}
            
            # Process documents
            documents = await self.pool.fetch("""
                SELECT 
                    id,
                    title,
                    content,
                    created_at,
                    metadata
                FROM documents
                WHERE project_id = $1
                    AND content IS NOT NULL
                    AND LENGTH(content) > 100
                ORDER BY created_at DESC
            """, project_id)
            
            print(f"\n📄 Found {len(documents)} documents with content")
            
            for doc in documents:
                try:
                    print(f"\n📝 Processing: {doc['title']}")
                    
                    # Extract insights using AI
                    insights = await self._extract_insights_with_ai(
                        doc_id=str(doc['id']),
                        title=doc['title'],
                        content=doc['content'],
                        project_name=project['name']
                    )
                    
                    # Store insights with duplicate prevention
                    stored, duplicates = await self._store_insights(
                        insights=insights,
                        project_id=project_id,
                        document_id=doc['id'],
                        existing_keys=existing_keys
                    )
                    
                    results['documents_processed'] += 1
                    results['insights_generated'] += stored
                    results['duplicates_prevented'] += duplicates
                    
                    print(f"  ✅ Generated {stored} new insights ({duplicates} duplicates prevented)")
                    
                except Exception as e:
                    error_msg = f"Error processing {doc['title']}: {str(e)}"
                    print(f"  ❌ {error_msg}")
                    results['errors'].append(error_msg)
            
            # Print final statistics
            print(f"\n📊 Summary for {project['name']}:")
            print(f"  Documents processed: {results['documents_processed']}")
            print(f"  New insights generated: {results['insights_generated']}")
            print(f"  Duplicates prevented: {results['duplicates_prevented']}")
            
            if results['errors']:
                print(f"  ⚠️ Errors encountered: {len(results['errors'])}")
                
        except Exception as e:
            results['errors'].append(f"Fatal error: {str(e)}")
            print(f"❌ Fatal error: {str(e)}")
            
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
            # Call OpenAI API (using new v1.0+ format)
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
            
            # Parse the response
            insights_json = response.choices[0].message.content
            
            # Clean up the response if needed
            insights_json = insights_json.strip()
            if insights_json.startswith("```json"):
                insights_json = insights_json[7:]
            if insights_json.endswith("```"):
                insights_json = insights_json[:-3]
            
            insights = json.loads(insights_json)
            
            # Validate and clean insights
            valid_insights = []
            for insight in insights:
                # Skip generic insights
                if len(insight.get('description', '')) < 50:
                    continue
                    
                # Ensure required fields
                if 'type' in insight and 'title' in insight and 'description' in insight:
                    valid_insights.append(insight)
            
            return valid_insights
            
        except json.JSONDecodeError as e:
            print(f"    ⚠️ Failed to parse AI response: {e}")
            return []
        except Exception as e:
            print(f"    ⚠️ AI extraction failed: {e}")
            return []
    
    async def _store_insights(
        self,
        insights: List[Dict[str, Any]],
        project_id: int,
        document_id: str,
        existing_keys: set
    ) -> tuple[int, int]:
        """Store insights with duplicate prevention."""
        
        stored_count = 0
        duplicate_count = 0
        
        for insight in insights:
            try:
                # Generate unique key for duplicate detection
                unique_key = f"{insight.get('title', '').lower()}:{insight.get('type', 'fact')}"
                
                # Skip if duplicate
                if unique_key in existing_keys:
                    duplicate_count += 1
                    continue
                
                # Map insight types to valid DB values
                insight_type = insight.get('type', 'fact')
                type_mapping = {
                    'action_item': 'action_item',
                    'decision': 'decision', 
                    'risk': 'risk',
                    'fact': 'fact',
                    'key_fact': 'fact',
                    'timeline': 'timeline_change',
                    'stakeholder': 'stakeholder_feedback'
                }
                insight_type = type_mapping.get(insight_type, 'fact')
                
                # Map severity
                severity = insight.get('severity', 'medium')
                if severity not in ['critical', 'high', 'medium', 'low']:
                    severity = 'medium'
                
                # Parse due date if present
                due_date = None
                if insight.get('due_date'):
                    try:
                        due_date = datetime.strptime(insight['due_date'], '%Y-%m-%d').date()
                    except:
                        pass
                
                # Prepare the insert
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
                existing_keys.add(unique_key)  # Add to set for this session
                
            except Exception as e:
                print(f"      ⚠️ Failed to store insight: {str(e)}")
                continue
        
        return stored_count, duplicate_count


async def main():
    """Main entry point."""
    
    if len(sys.argv) < 2:
        print("Usage: python generate_ai_insights.py <project_id>")
        print("\nExamples:")
        print("  python generate_ai_insights.py 43   # Westfield Collective")
        print("  python generate_ai_insights.py 59   # Tampa Event/Party")
        sys.exit(1)
    
    project_id = int(sys.argv[1])
    
    # Database connection
    DATABASE_URL = os.getenv(
        "DATABASE_URL",
        "postgresql://postgres.fpbibuobrqkcqftcweqk:2025Reach_for_the_Stars@aws-0-us-west-1.pooler.supabase.com:6543/postgres"
    )
    
    # Check for OpenAI API key
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ Error: OPENAI_API_KEY not found in environment variables")
        sys.exit(1)
    
    try:
        # Create connection pool
        pool = await asyncpg.create_pool(DATABASE_URL, min_size=1, max_size=10)
        print("✅ Connected to database")
        
        # Initialize generator
        generator = AIInsightsGenerator(pool)
        
        print(f"🚀 Starting AI-powered insights generation...")
        
        results = await generator.generate_insights_for_project(project_id)
        
        # Print final results
        print("\n" + "=" * 60)
        print("✨ AI INSIGHTS GENERATION COMPLETE")
        print("=" * 60)
        
        if results['errors']:
            print(f"\n⚠️ {len(results['errors'])} errors occurred:")
            for error in results['errors'][:5]:
                print(f"  - {error}")
        
        # Close pool
        await pool.close()
        
    except Exception as e:
        print(f"❌ Fatal error: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())