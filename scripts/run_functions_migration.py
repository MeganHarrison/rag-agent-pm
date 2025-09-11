#!/usr/bin/env python3
"""
Run Project Functions Migration Script
"""

import os
import asyncio
import asyncpg
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

async def run_functions():
    """Run the functions migration."""
    
    database_url = os.getenv('DATABASE_URL')
    if not database_url:
        print("❌ DATABASE_URL not found")
        return False
    
    sql_file = Path(__file__).parent / 'sql' / 'add_project_functions.sql'
    
    with open(sql_file, 'r') as f:
        sql_content = f.read()
    
    try:
        print("🔄 Connecting to database...")
        conn = await asyncpg.connect(database_url)
        
        print("🔄 Creating functions and view...")
        
        # Execute the entire SQL content as one block
        await conn.execute(sql_content)
        
        print("✅ Functions and view created successfully!")
        
        # Test the functions
        print("\n📊 Testing functions...")
        
        # Test get_projects_needing_summary_update
        projects = await conn.fetch("SELECT * FROM get_projects_needing_summary_update(24) LIMIT 5")
        print(f"✅ Projects needing update: {len(projects)}")
        
        # Test the view
        dashboard = await conn.fetch("""
            SELECT name, health_score, health_status, recent_insights_count 
            FROM project_health_dashboard 
            WHERE name IS NOT NULL 
            LIMIT 5
        """)
        print(f"✅ Dashboard view working: {len(dashboard)} projects visible")
        
        for project in dashboard:
            print(f"  - {project['name']}: Insights={project['recent_insights_count']}")
        
        await conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    asyncio.run(run_functions())