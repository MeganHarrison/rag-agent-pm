#!/usr/bin/env python3
"""
Test script for insights generation
"""

import asyncio
import asyncpg
import os
from datetime import datetime
from dotenv import load_dotenv
from services.project_insights_service import ProjectInsightsService

# Load environment variables
load_dotenv()

async def test_insights_generation():
    """Test the insights generation for a specific project."""
    
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
        
        # Test project ID (Paradise Isle project)
        project_id = 59
        
        print(f"\n🔍 Generating insights for Project ID: {project_id}")
        print("-" * 50)
        
        # Aggregate project insights
        insights = await insights_service.aggregate_project_insights(project_id)
        
        if insights:
            print("\n📊 Generated Insights:")
            print(f"  - Project: {insights.get('project_name', 'Unknown')}")
            print(f"  - Status: {insights.get('status', 'Unknown')}")
            print(f"  - Risk Level: {insights.get('risk_level', 'Unknown')}")
            print(f"  - Next Actions: {len(insights.get('next_actions', []))}")
            
            # Print key metrics
            if 'key_metrics' in insights:
                print("\n📈 Key Metrics:")
                for metric, value in insights['key_metrics'].items():
                    print(f"  - {metric}: {value}")
            
            # Print recent activities
            if 'recent_activities' in insights:
                print("\n📅 Recent Activities:")
                for activity in insights['recent_activities'][:5]:  # Show first 5
                    print(f"  - {activity}")
            
            # Print risks
            if 'risks' in insights:
                print("\n⚠️ Identified Risks:")
                for risk in insights['risks'][:3]:  # Show first 3
                    print(f"  - {risk}")
            
            print("\n✅ Insights generation successful!")
            
        else:
            print("❌ No insights generated")
        
        # Close the pool
        await pool.close()
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    # Run the test
    asyncio.run(test_insights_generation())