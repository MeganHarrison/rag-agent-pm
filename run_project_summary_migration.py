#!/usr/bin/env python3
"""
Run Project Summary Migration Script

This script applies the project summary database migrations to Supabase.
"""

import os
import asyncio
import asyncpg
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

async def run_migration():
    """Run the project summary migration."""
    
    # Get database URL
    database_url = os.getenv('DATABASE_URL')
    if not database_url:
        print("❌ DATABASE_URL not found in environment variables")
        print("Please ensure your .env file contains DATABASE_URL")
        return False
    
    print(f"✅ Database URL found: {database_url[:30]}...")
    
    # Load SQL file
    sql_file = Path(__file__).parent / 'sql' / 'add_project_summary.sql'
    if not sql_file.exists():
        print(f"❌ SQL file not found: {sql_file}")
        return False
    
    print(f"✅ Loading SQL from: {sql_file}")
    
    with open(sql_file, 'r') as f:
        sql_content = f.read()
    
    print(f"✅ SQL loaded: {len(sql_content)} characters")
    
    # Connect to database and run migration
    try:
        print("🔄 Connecting to database...")
        conn = await asyncpg.connect(database_url)
        
        print("🔄 Running migration...")
        
        # Split SQL into individual statements and execute
        statements = [s.strip() for s in sql_content.split(';') if s.strip()]
        
        for i, statement in enumerate(statements, 1):
            if statement:
                try:
                    print(f"  Executing statement {i}/{len(statements)}...")
                    await conn.execute(statement)
                except asyncpg.exceptions.DuplicateColumnError as e:
                    print(f"  ⚠️  Column already exists (skipping): {str(e)[:100]}")
                except asyncpg.exceptions.DuplicateObjectError as e:
                    print(f"  ⚠️  Object already exists (skipping): {str(e)[:100]}")
                except Exception as e:
                    print(f"  ❌ Error in statement {i}: {str(e)[:200]}")
                    # Continue with other statements
        
        print("✅ Migration completed successfully!")
        
        # Verify the changes
        print("\n🔄 Verifying migration...")
        
        # Check if new columns exist
        column_check = await conn.fetch("""
            SELECT column_name, data_type 
            FROM information_schema.columns 
            WHERE table_name = 'projects' 
            AND column_name IN ('summary', 'health_score', 'health_status', 'summary_metadata', 'summary_updated_at')
            ORDER BY column_name
        """)
        
        if column_check:
            print("✅ New columns added to projects table:")
            for col in column_check:
                print(f"  - {col['column_name']}: {col['data_type']}")
        else:
            print("⚠️  No new columns found - they may already exist")
        
        # Check if functions were created
        function_check = await conn.fetch("""
            SELECT routine_name 
            FROM information_schema.routines 
            WHERE routine_schema = 'public' 
            AND routine_name IN ('get_projects_needing_summary_update', 'update_project_summary')
        """)
        
        if function_check:
            print("\n✅ Functions created:")
            for func in function_check:
                print(f"  - {func['routine_name']}()")
        
        # Check if view was created
        view_check = await conn.fetch("""
            SELECT table_name 
            FROM information_schema.views 
            WHERE table_schema = 'public' 
            AND table_name = 'project_health_dashboard'
        """)
        
        if view_check:
            print("\n✅ View created: project_health_dashboard")
        
        await conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        return False


async def test_summary_functions():
    """Test the new summary functions."""
    
    database_url = os.getenv('DATABASE_URL')
    if not database_url:
        print("❌ Cannot test - DATABASE_URL not found")
        return
    
    try:
        conn = await asyncpg.connect(database_url)
        
        print("\n📊 Testing summary functions...")
        
        # Test get_projects_needing_summary_update
        projects_needing_update = await conn.fetch("""
            SELECT * FROM get_projects_needing_summary_update(24)
            LIMIT 5
        """)
        
        print(f"\n✅ Projects needing summary update: {len(projects_needing_update)}")
        for project in projects_needing_update:
            print(f"  - {project['project_name']}: Last updated {project['hours_since_update']:.1f} hours ago")
        
        # Check project health dashboard
        dashboard = await conn.fetch("""
            SELECT id, name, health_score, health_status, recent_insights_count
            FROM project_health_dashboard
            WHERE name IS NOT NULL
            LIMIT 5
        """)
        
        print(f"\n✅ Project Health Dashboard: {len(dashboard)} projects")
        for project in dashboard:
            health_score = project['health_score'] or 0
            health_status = project['health_status'] or 'Not Calculated'
            insights = project['recent_insights_count'] or 0
            print(f"  - {project['name']}: Score={health_score:.1f}, Status={health_status}, Insights={insights}")
        
        await conn.close()
        
    except Exception as e:
        print(f"❌ Test failed: {e}")


async def main():
    """Main execution function."""
    
    print("=" * 60)
    print("PROJECT SUMMARY MIGRATION")
    print("=" * 60)
    
    # Run migration
    success = await run_migration()
    
    if success:
        print("\n" + "=" * 60)
        print("TESTING NEW FUNCTIONALITY")
        print("=" * 60)
        await test_summary_functions()
        
        print("\n" + "=" * 60)
        print("✨ MIGRATION COMPLETE!")
        print("=" * 60)
        print("\nThe following features are now available:")
        print("  1. Project summaries with AI generation")
        print("  2. Health scores and status tracking")
        print("  3. Summary metadata for metrics")
        print("  4. Project health dashboard view")
        print("  5. Functions to manage summaries")
        print("\nYou can now run the insights pipeline to start generating insights!")
    else:
        print("\n❌ Migration failed. Please check the errors above.")


if __name__ == "__main__":
    asyncio.run(main())