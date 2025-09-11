#!/usr/bin/env python3
"""
Debug test to isolate the NoneType error
"""

import asyncio
import traceback
from dependencies import AgentDependencies
from settings import load_settings
from agent import search_agent

async def debug_test():
    """Debug the NoneType error step by step."""
    try:
        print("1. Loading settings...")
        settings = load_settings()
        print(f"   ✓ Settings loaded, default_match_count: {settings.default_match_count}")
        
        print("2. Creating dependencies...")
        deps = AgentDependencies()
        print(f"   ✓ Dependencies created, settings: {deps.settings}")
        
        print("3. Initializing dependencies...")
        await deps.initialize()
        print(f"   ✓ Dependencies initialized, settings: {deps.settings is not None}")
        
        if deps.settings:
            print(f"   ✓ default_match_count: {deps.settings.default_match_count}")
        else:
            print("   ✗ deps.settings is still None!")
            return
            
        print("4. Testing agent run...")
        result = await search_agent.run("What was discussed in the last meeting?", deps=deps)
        print(f"   ✓ Agent run successful: {type(result)}")
        
        # Extract response safely
        if hasattr(result, 'data'):
            response = result.data
        elif hasattr(result, 'response'):
            response = str(result.response)
        elif hasattr(result, 'output'):
            response = str(result.output)
        else:
            response = str(result)
            
        print(f"5. Response extracted: {len(response)} characters")
        print(f"Response: {response[:200]}...")
        
        await deps.cleanup()
        print("6. Cleanup complete")
        
    except Exception as e:
        print(f"❌ Error at step: {e}")
        traceback.print_exc()
        
if __name__ == "__main__":
    asyncio.run(debug_test())