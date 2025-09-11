#!/usr/bin/env python3
"""
Generate insights for a specific project by processing its documents
"""

import asyncio
import asyncpg
import os
from datetime import datetime
from dotenv import load_dotenv
from services.project_insights_service import ProjectInsightsService

# Load environment variables
load_dotenv()

async def generate_insights_for_project(project_id: int = 59):
    """Generate insights for the Tampa Event/Party project."""
    
    # Database connection
    DATABASE_URL = os.getenv(
        "DATABASE_URL",
        "postgresql://postgres.fpbibuobrqkcqftcweqk:2025Reach_for_the_Stars@aws-0-us-west-1.pooler.supabase.com:6543/postgres"
    )
    
    try:
        # Create connection pool
        pool = await asyncpg.create_pool(DATABASE_URL, min_size=1, max_size=10)
        print("✅ Connected to database")
        
        # Initialize the insights service
        insights_service = ProjectInsightsService(pool)
        print("✅ Initialized insights service")
        
        print(f"\n🔍 Processing documents for Project ID: {project_id}")
        print("-" * 50)
        
        # First, get all documents for this project
        documents = await pool.fetch("""
            SELECT 
                d.id,
                d.title,
                d.content,
                d.created_at,
                d.project_id,
                p.name as project_name
            FROM documents d
            JOIN projects p ON p.id = d.project_id
            WHERE d.project_id = $1
            ORDER BY d.created_at DESC
        """, project_id)
        
        if documents:
            print(f"📄 Found {len(documents)} documents for project")
            
            # Process each document to extract insights
            for doc in documents:
                print(f"\n📋 Processing: {doc['title']}")
                
                # Store the document content in a temporary meeting record for processing
                # First create or update a meeting record
                meeting_id = await pool.fetchval("""
                    INSERT INTO meetings (id, name, transcript_text, project_id, created_at)
                    VALUES (gen_random_uuid(), $1, $2, $3, NOW())
                    ON CONFLICT DO NOTHING
                    RETURNING id
                """, doc['title'], doc['content'], project_id)
                
                if meeting_id:
                    # Process the meeting transcript using the correct function
                    from services.project_insights_service import process_meeting_with_insights
                    
                    result = await process_meeting_with_insights(
                        pool=pool,
                        meeting_id=str(meeting_id),
                        transcript=doc['content'],
                        meeting_name=doc['title']
                    )
                    
                    insights = result.get('insights') if result else None
                
                if insights:
                    print(f"  ✅ Extracted insights:")
                    if insights.get('action_items'):
                        print(f"    - {len(insights['action_items'])} action items")
                    if insights.get('decisions'):
                        print(f"    - {len(insights['decisions'])} decisions")
                    if insights.get('risks'):
                        print(f"    - {len(insights['risks'])} risks")
                    if insights.get('timeline_updates'):
                        print(f"    - {len(insights['timeline_updates'])} timeline updates")
                    if insights.get('stakeholder_feedback'):
                        print(f"    - {len(insights['stakeholder_feedback'])} stakeholder feedback items")
                else:
                    print(f"  ⚠️ No insights extracted")
            
            # Now aggregate all insights for the project
            print("\n📊 Aggregating project insights...")
            summary = await insights_service.aggregate_project_insights(project_id)
            
            if summary:
                print("\n✅ Project insights generated successfully!")
                
                # Get the newly created insights from database
                new_insights = await pool.fetch("""
                    SELECT 
                        id,
                        insight_type,
                        severity,
                        title,
                        description,
                        created_at
                    FROM ai_insights
                    WHERE project_id = $1
                    ORDER BY created_at DESC
                    LIMIT 10
                """, project_id)
                
                if new_insights:
                    print(f"\n📈 Generated {len(new_insights)} new insights:")
                    for insight in new_insights:
                        print(f"\n  Type: {insight['insight_type']}")
                        print(f"  Severity: {insight['severity']}")
                        print(f"  Title: {insight['title']}")
                        if insight['description']:
                            print(f"  Description: {insight['description'][:150]}...")
            else:
                print("⚠️ No summary generated")
                
        else:
            print(f"⚠️ No documents found for project {project_id}")
            
            # Check if there are any meetings that could be processed
            meetings = await pool.fetch("""
                SELECT 
                    m.id,
                    m.name,
                    m.transcript_text,
                    m.created_at
                FROM meetings m
                WHERE m.project_id = $1
                    AND m.transcript_text IS NOT NULL
                ORDER BY m.created_at DESC
            """, project_id)
            
            if meetings:
                print(f"\n📝 Found {len(meetings)} meetings with transcripts")
                
                for meeting in meetings:
                    print(f"\n📋 Processing meeting: {meeting['name']}")
                    
                    # Process the meeting transcript
                    from services.project_insights_service import process_meeting_with_insights
                    
                    result = await process_meeting_with_insights(
                        pool=pool,
                        meeting_id=str(meeting['id']),
                        transcript=meeting['transcript_text'],
                        meeting_name=meeting['name']
                    )
                    
                    if result and result.get('insights'):
                        insights = result['insights']
                        print(f"  ✅ Extracted insights from meeting:")
                        if insights.get('action_items'):
                            print(f"    - {len(insights['action_items'])} action items")
                        if insights.get('decisions'):
                            print(f"    - {len(insights['decisions'])} decisions")
                        if insights.get('risks'):
                            print(f"    - {len(insights['risks'])} risks")
            else:
                print("⚠️ No meetings found with transcripts")
        
        # Final count of insights
        total_insights = await pool.fetchval("""
            SELECT COUNT(*) 
            FROM ai_insights 
            WHERE project_id = $1
        """, project_id)
        
        print(f"\n📊 Total insights for project: {total_insights}")
        
        # Close the pool
        await pool.close()
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    # Run the insights generation
    asyncio.run(generate_insights_for_project(59))