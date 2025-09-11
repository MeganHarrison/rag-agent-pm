#!/usr/bin/env python3
"""
Direct test of search tools to isolate the NoneType error
"""

import asyncio
from dependencies import AgentDependencies
from tools.search_tools import semantic_search
from pydantic_ai import RunContext

class MockRunContext:
    """Mock RunContext for testing."""
    def __init__(self, deps):
        self.deps = deps

async def test_search_tools():
    """Test search tools directly."""
    try:
        print("Creating and initializing dependencies...")
        deps = AgentDependencies()
        await deps.initialize()
        
        print(f"Dependencies settings: {deps.settings is not None}")
        if deps.settings:
            print(f"default_match_count: {deps.settings.default_match_count}")
        
        # Create mock context
        ctx = MockRunContext(deps)
        
        print("Testing semantic_search directly...")
        results = await semantic_search(ctx, "What was discussed in the last meeting?")
        print(f"Search results: {len(results)} items")
        
        await deps.cleanup()
        print("Test completed successfully!")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_search_tools())