#!/usr/bin/env python3
"""Test database connection and verify tables exist."""

import os
import asyncio
import asyncpg
from dotenv import load_dotenv
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()

async def test_connection():
    """Test database connection and list tables."""
    
    # Load environment variables
    load_dotenv()
    database_url = os.getenv("DATABASE_URL")
    
    if not database_url:
        console.print("[red]❌ DATABASE_URL not found in environment variables[/red]")
        console.print("[yellow]Please create a .env file with your database connection string[/yellow]")
        return False
    
    console.print(f"[cyan]🔗 Connecting to database...[/cyan]")
    
    try:
        # Connect to database
        conn = await asyncpg.connect(database_url)
        console.print("[green]✅ Successfully connected to database![/green]\n")
        
        # Get database version
        version = await conn.fetchval("SELECT version()")
        console.print(Panel(f"[blue]PostgreSQL Version:[/blue]\n{version.split(',')[0]}", title="Database Info"))
        
        # Check for required extensions
        console.print("\n[cyan]📦 Checking required extensions...[/cyan]")
        extensions = await conn.fetch("""
            SELECT extname, extversion 
            FROM pg_extension 
            WHERE extname IN ('vector', 'uuid-ossp', 'pg_trgm')
            ORDER BY extname
        """)
        
        ext_table = Table(title="Installed Extensions")
        ext_table.add_column("Extension", style="cyan")
        ext_table.add_column("Version", style="green")
        
        for ext in extensions:
            ext_table.add_row(ext['extname'], ext['extversion'])
        
        if extensions:
            console.print(ext_table)
        else:
            console.print("[yellow]⚠️  No required extensions found. They may need to be installed.[/yellow]")
        
        # List all tables
        console.print("\n[cyan]📊 Checking tables in database...[/cyan]")
        tables = await conn.fetch("""
            SELECT 
                tablename,
                pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) as size,
                (SELECT COUNT(*) FROM information_schema.columns 
                 WHERE table_name = tablename) as column_count
            FROM pg_tables 
            WHERE schemaname = 'public'
            ORDER BY tablename
        """)
        
        if tables:
            table_list = Table(title="Database Tables")
            table_list.add_column("Table Name", style="cyan", no_wrap=True)
            table_list.add_column("Size", style="yellow")
            table_list.add_column("Columns", style="green")
            
            for table in tables:
                table_list.add_row(
                    table['tablename'],
                    table['size'],
                    str(table['column_count'])
                )
            
            console.print(table_list)
            
            # Count records in main tables
            console.print("\n[cyan]📈 Record counts in main tables:[/cyan]")
            
            main_tables = [
                'projects', 'documents', 'chunks', 'ai_insights',
                'conversations', 'conversation_messages', 'conversation_facts'
            ]
            
            count_table = Table(title="Record Counts")
            count_table.add_column("Table", style="cyan")
            count_table.add_column("Records", style="green")
            
            for table_name in main_tables:
                # Check if table exists
                exists = await conn.fetchval(
                    "SELECT EXISTS (SELECT 1 FROM pg_tables WHERE tablename = $1)",
                    table_name
                )
                
                if exists:
                    count = await conn.fetchval(f"SELECT COUNT(*) FROM {table_name}")
                    count_table.add_row(table_name, f"{count:,}")
                else:
                    count_table.add_row(table_name, "[red]Table not found[/red]")
            
            console.print(count_table)
            
            # Test vector search capability
            console.print("\n[cyan]🔍 Testing vector search capability...[/cyan]")
            
            # Check if chunks table has embeddings
            has_embeddings = await conn.fetchval("""
                SELECT COUNT(*) 
                FROM chunks 
                WHERE embedding IS NOT NULL
            """)
            
            if has_embeddings > 0:
                console.print(f"[green]✅ Found {has_embeddings:,} chunks with embeddings ready for vector search[/green]")
            else:
                console.print("[yellow]⚠️  No embeddings found in chunks table. Documents need to be processed first.[/yellow]")
            
        else:
            console.print("[yellow]⚠️  No tables found in public schema[/yellow]")
            console.print("[yellow]You may need to run the SQL migration scripts first.[/yellow]")
        
        await conn.close()
        console.print("\n[green]✅ Database connection test completed successfully![/green]")
        return True
        
    except asyncpg.PostgresError as e:
        console.print(f"[red]❌ Database error: {e}[/red]")
        return False
    except Exception as e:
        console.print(f"[red]❌ Unexpected error: {e}[/red]")
        return False

if __name__ == "__main__":
    asyncio.run(test_connection())