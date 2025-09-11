#!/usr/bin/env python3
"""
Simple test to check if insights are being stored in the database
"""

import asyncio
import asyncpg
import os
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

async def test_insights_in_db():
    """Check what insights exist in the database."""
    
    # Database connection
    DATABASE_URL = os.getenv(
        "DATABASE_URL",
        "postgresql://postgres.fpbibuobrqkcqftcweqk:2025Reach_for_the_Stars@aws-0-us-west-1.pooler.supabase.com:6543/postgres"
    )
    
    try:
        # Create connection
        conn = await asyncpg.connect(DATABASE_URL)
        print("✅ Connected to database")
        
        # Check if ai_insights table exists
        table_exists = await conn.fetchval("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_schema = 'public' 
                AND table_name = 'ai_insights'
            );
        """)
        
        if table_exists:
            print("✅ ai_insights table exists")
            
            # Count total insights
            total_count = await conn.fetchval("SELECT COUNT(*) FROM ai_insights")
            print(f"📊 Total insights in database: {total_count}")
            
            # First, check the column structure
            columns = await conn.fetch("""
                SELECT column_name, data_type 
                FROM information_schema.columns 
                WHERE table_name = 'ai_insights'
                ORDER BY ordinal_position
            """)
            
            print("\n📋 ai_insights table columns:")
            for col in columns:
                print(f"  - {col['column_name']}: {col['data_type']}")
            
            # Get insights for project 59 with actual columns
            project_insights = await conn.fetch("""
                SELECT *
                FROM ai_insights
                WHERE project_id = 59
                ORDER BY created_at DESC
                LIMIT 5
            """)
            
            if project_insights:
                print(f"\n📈 Found {len(project_insights)} recent insights for Project 59:")
                for insight in project_insights:
                    print(f"\n  Insight ID: {insight['id']}")
                    print(f"  Keys available: {list(insight.keys())}")
                    # Print the first few key-value pairs
                    for key in list(insight.keys())[:5]:
                        value = insight[key]
                        if isinstance(value, str) and len(value) > 100:
                            print(f"  {key}: {value[:100]}...")
                        else:
                            print(f"  {key}: {value}")
            else:
                print("\n⚠️ No insights found for Project 59")
                
                # Check if project exists
                project_exists = await conn.fetchval("""
                    SELECT EXISTS (
                        SELECT 1 FROM projects WHERE id = 59
                    )
                """)
                
                if project_exists:
                    print("✅ Project 59 exists in database")
                    
                    # Get project name
                    project_name = await conn.fetchval("""
                        SELECT name FROM projects WHERE id = 59
                    """)
                    print(f"   Project name: {project_name}")
                else:
                    print("❌ Project 59 does not exist in database")
        else:
            print("❌ ai_insights table does not exist")
            
            # Check what tables do exist
            tables = await conn.fetch("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
                ORDER BY table_name
            """)
            
            print("\n📋 Available tables:")
            for table in tables[:20]:  # Show first 20 tables
                print(f"  - {table['table_name']}")
        
        # Close connection
        await conn.close()
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    # Run the test
    asyncio.run(test_insights_in_db())