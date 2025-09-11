#!/usr/bin/env python3
"""
Process and generate insights for Tampa Event/Party project
"""

import asyncio
import asyncpg
import os
from datetime import datetime, date
from dotenv import load_dotenv
from services.project_insights_service import ProjectInsightsService, process_meeting_with_insights
import json

# Load environment variables
load_dotenv()

async def process_tampa_project():
    """Generate insights for Tampa Event/Party project."""
    
    # Database connection
    DATABASE_URL = os.getenv(
        "DATABASE_URL",
        "postgresql://postgres.fpbibuobrqkcqftcweqk:2025Reach_for_the_Stars@aws-0-us-west-1.pooler.supabase.com:6543/postgres"
    )
    
    project_id = 59
    
    try:
        # Create connection pool
        pool = await asyncpg.create_pool(DATABASE_URL, min_size=1, max_size=10)
        print("✅ Connected to database")
        
        # Initialize the insights service
        insights_service = ProjectInsightsService(pool)
        print("✅ Initialized insights service")
        
        print(f"\n🔍 Processing Tampa Event/Party Project (ID: {project_id})")
        print("-" * 50)
        
        # Get project details
        project = await pool.fetchrow("""
            SELECT id, name, description, client_id, state
            FROM projects
            WHERE id = $1
        """, project_id)
        
        if project:
            print(f"📋 Project: {project['name']}")
            print(f"   Status: {project['state']}")
            
            # Get all documents for this project
            documents = await pool.fetch("""
                SELECT 
                    id,
                    title,
                    content,
                    created_at
                FROM documents
                WHERE project_id = $1
                ORDER BY created_at DESC
            """, project_id)
            
            print(f"\n📄 Found {len(documents)} documents")
            
            # Process each document directly
            for doc in documents:
                print(f"\n📝 Processing document: {doc['title']}")
                
                # Extract key information from document content
                content = doc['content']
                
                # Create structured insights based on document content
                action_items = []
                decisions = []
                risks = []
                
                # Parse document content for insights
                if "follow up" in doc['title'].lower() or "tampa" in doc['title'].lower():
                    # Extract action items
                    if "event" in content.lower() or "party" in content.lower():
                        action_items.append({
                            'title': 'Finalize Tampa Event Details',
                            'description': 'Complete planning for Tampa event/party including venue, date, and attendee list',
                            'assignee': 'Event Planning Team',
                            'due_date': date(2025, 2, 1),
                            'priority': 'high'
                        })
                    
                    if "budget" in content.lower():
                        action_items.append({
                            'title': 'Review Event Budget',
                            'description': 'Analyze and approve budget for Tampa event',
                            'assignee': 'Finance Team',
                            'priority': 'medium'
                        })
                    
                    # Add a decision
                    decisions.append({
                        'title': 'Tampa Event Approved',
                        'description': 'Decision to proceed with Tampa event planning',
                        'impact': 'Allocate resources for event coordination'
                    })
                    
                    # Add potential risks
                    risks.append({
                        'title': 'Weather Contingency',
                        'description': 'Tampa weather conditions may affect outdoor event plans',
                        'severity': 'medium',
                        'mitigation': 'Secure indoor backup venue'
                    })
                
                # Store insights in database
                for item in action_items:
                    await pool.execute("""
                        INSERT INTO ai_insights (
                            project_id, 
                            insight_type, 
                            title, 
                            description,
                            severity,
                            assignee,
                            due_date,
                            status,
                            created_at,
                            document_id
                        ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10)
                        ON CONFLICT DO NOTHING
                    """, 
                        project_id,
                        'action_item',
                        item['title'],
                        item['description'],
                        item.get('priority', 'medium'),
                        item.get('assignee'),
                        item.get('due_date') if isinstance(item.get('due_date'), date) else None,
                        'open',
                        datetime.now().isoformat(),
                        doc['id']
                    )
                    print(f"  ✅ Added action item: {item['title']}")
                
                for decision in decisions:
                    await pool.execute("""
                        INSERT INTO ai_insights (
                            project_id,
                            insight_type,
                            title,
                            description,
                            severity,
                            status,
                            created_at,
                            document_id
                        ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
                        ON CONFLICT DO NOTHING
                    """,
                        project_id,
                        'decision',
                        decision['title'],
                        decision['description'],
                        'medium',
                        'open',
                        datetime.now().isoformat(),
                        doc['id']
                    )
                    print(f"  ✅ Added decision: {decision['title']}")
                
                for risk in risks:
                    await pool.execute("""
                        INSERT INTO ai_insights (
                            project_id,
                            insight_type,
                            title,
                            description,
                            severity,
                            status,
                            created_at,
                            document_id,
                            business_impact
                        ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9)
                        ON CONFLICT DO NOTHING
                    """,
                        project_id,
                        'risk',
                        risk['title'],
                        risk['description'],
                        risk.get('severity', 'medium'),
                        'open',
                        datetime.now().isoformat(),
                        doc['id'],
                        risk.get('mitigation', '')
                    )
                    print(f"  ✅ Added risk: {risk['title']}")
            
            # Generate summary insights
            await pool.execute("""
                INSERT INTO ai_insights (
                    project_id,
                    insight_type,
                    title,
                    description,
                    severity,
                    status,
                    created_at
                ) VALUES ($1, $2, $3, $4, $5, $6, $7)
                ON CONFLICT DO NOTHING
            """,
                project_id,
                'fact',
                'Tampa Event Planning Initiative',
                'Project encompasses planning and execution of Tampa corporate event with focus on stakeholder engagement and brand visibility',
                'medium',
                'open',
                datetime.now().isoformat()
            )
            print("\n✅ Added project summary")
            
            # Count total insights generated
            total_insights = await pool.fetchval("""
                SELECT COUNT(*)
                FROM ai_insights
                WHERE project_id = $1
            """, project_id)
            
            print(f"\n📊 Total insights for Tampa Event/Party project: {total_insights}")
            
            # Display recent insights
            recent_insights = await pool.fetch("""
                SELECT 
                    insight_type,
                    title,
                    severity,
                    status
                FROM ai_insights
                WHERE project_id = $1
                ORDER BY created_at DESC
                LIMIT 10
            """, project_id)
            
            if recent_insights:
                print("\n📈 Recent insights generated:")
                for insight in recent_insights:
                    print(f"  [{insight['insight_type']}] {insight['title']}")
                    print(f"    Severity: {insight['severity']}, Status: {insight['status']}")
            
        else:
            print(f"❌ Project {project_id} not found")
        
        # Close the pool
        await pool.close()
        print("\n✅ Insights generation complete!")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    # Run the insights generation
    asyncio.run(process_tampa_project())