#!/usr/bin/env python3
"""
Simple CLI test interface for PM RAG Agent
Usage: python test_cli.py
"""

import asyncio
import sys
from typing import Optional

from agent import search_agent
from dependencies import AgentDependencies
from settings import load_settings

def print_banner():
    """Print welcome banner."""
    print("\n" + "="*60)
    print("🤖 PM RAG Agent - Interactive Test CLI")
    print("="*60)
    print("Type your questions about projects, meetings, or business strategy.")
    print("Commands: 'exit' or 'quit' to stop, 'clear' to clear screen")
    print("-"*60 + "\n")

async def test_agent_query(query: str) -> Optional[str]:
    """Test a single query against the agent."""
    try:
        # Load settings
        settings = load_settings()
        
        # Create and initialize dependencies
        deps = AgentDependencies()
        await deps.initialize()
        
        print(f"🔍 Processing: {query}")
        print("⏳ Thinking...")
        
        # Run the agent
        result = await search_agent.run(query, deps=deps)
        
        # Extract response safely
        if hasattr(result, 'data'):
            response = result.data
        elif hasattr(result, 'response'):
            response = str(result.response)
        elif hasattr(result, 'output'):
            response = str(result.output)
        else:
            response = str(result)
            
        # Clean up resources
        await deps.cleanup()
        return response
        
    except Exception as e:
        print(f"❌ Error: {e}")
        # Clean up resources on error
        try:
            await deps.cleanup()
        except:
            pass
        return None

async def main():
    """Main interactive loop."""
    print_banner()
    
    try:
        while True:
            try:
                # Get user input
                query = input("💬 You: ").strip()
                
                # Handle commands
                if query.lower() in ['exit', 'quit', 'q']:
                    print("\n👋 Goodbye!")
                    break
                elif query.lower() == 'clear':
                    print("\033[2J\033[H")  # Clear screen
                    print_banner()
                    continue
                elif not query:
                    continue
                
                # Process query
                print("\n🤖 Agent:")
                response = await test_agent_query(query)
                
                if response:
                    print(f"{response}")
                else:
                    print("Sorry, I couldn't process that query.")
                    
                print("\n" + "-"*60)
                
            except KeyboardInterrupt:
                print("\n\n👋 Interrupted. Goodbye!")
                break
            except EOFError:
                print("\n\n👋 Goodbye!")
                break
                
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())