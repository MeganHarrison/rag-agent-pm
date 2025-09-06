#!/usr/bin/env python3
"""Find unused Python files in the project."""

import os
import re
from pathlib import Path
from rich.console import Console
from rich.table import Table

console = Console()

def find_all_py_files():
    """Find all Python files in the project."""
    py_files = []
    for root, dirs, files in os.walk('.'):
        # Skip directories
        if '__pycache__' in root or '.git' in root or 'venv' in root:
            continue
        for file in files:
            if file.endswith('.py'):
                py_files.append(os.path.join(root, file)[2:])  # Remove './'
    return sorted(py_files)

def find_imported_modules():
    """Find all imported modules."""
    imported = set()
    import_patterns = [
        r'^from\s+([.\w]+)\s+import',
        r'^import\s+([.\w]+)'
    ]
    
    for py_file in find_all_py_files():
        with open(py_file, 'r') as f:
            content = f.read()
            for line in content.split('\n'):
                line = line.strip()
                for pattern in import_patterns:
                    match = re.match(pattern, line)
                    if match:
                        module = match.group(1)
                        # Convert module path to file path
                        if module.startswith('.'):
                            # Relative import
                            base_dir = os.path.dirname(py_file)
                            if module == '.':
                                imported.add(base_dir)
                            else:
                                rel_path = module.replace('.', '/')
                                if rel_path.startswith('/'):
                                    rel_path = rel_path[1:]
                                imported.add(os.path.join(base_dir, rel_path))
                        else:
                            # Absolute import within project
                            imported.add(module.replace('.', '/'))
    
    return imported

def main():
    """Main function to find unused files."""
    console.print("[cyan]🔍 Analyzing Python files usage...[/cyan]\n")
    
    all_files = find_all_py_files()
    imported_modules = find_imported_modules()
    
    # Convert module names to potential file paths
    imported_files = set()
    for module in imported_modules:
        # Add both module.py and module/__init__.py possibilities
        imported_files.add(f"{module}.py")
        imported_files.add(f"{module}/__init__.py")
        # Also check if it's a direct file reference
        if '/' in module:
            parts = module.split('/')
            for i in range(len(parts)):
                partial = '/'.join(parts[:i+1])
                imported_files.add(f"{partial}.py")
                imported_files.add(f"{partial}/__init__.py")
    
    # Files that are entry points or tests (always considered "used")
    entry_points = {
        'app.py',  # Main FastAPI app
        'cli.py',  # CLI interface
        'vectorization_api.py',  # Vectorization API
        'test_db_connection.py',  # Utility script
        'find_unused_files.py',  # This script
    }
    
    # Categorize files
    used_files = []
    unused_files = []
    test_files = []
    utility_files = []
    
    for file in all_files:
        if 'test' in file or file.startswith('tests/'):
            test_files.append(file)
        elif file in entry_points:
            utility_files.append(file)
        elif file in imported_files or any(file.endswith(f"/{imp}") for imp in imported_files):
            used_files.append(file)
        elif file == '__init__.py' or '/__init__.py' in file:
            # __init__.py files are always considered used
            used_files.append(file)
        else:
            # Check if this file is imported directly
            file_stem = file.replace('.py', '').replace('/', '.')
            if file_stem in imported_modules or file.replace('.py', '') in imported_modules:
                used_files.append(file)
            else:
                unused_files.append(file)
    
    # Display results
    table = Table(title="Python Files Usage Analysis")
    table.add_column("Category", style="cyan", no_wrap=True)
    table.add_column("Files", style="yellow")
    table.add_column("List", style="white")
    
    table.add_row(
        "✅ Used (imported)",
        str(len(used_files)),
        "\n".join(used_files[:10]) + ("\n..." if len(used_files) > 10 else "")
    )
    
    table.add_row(
        "🚀 Entry Points",
        str(len(utility_files)),
        "\n".join(utility_files)
    )
    
    table.add_row(
        "🧪 Test Files",
        str(len(test_files)),
        "\n".join(test_files)
    )
    
    table.add_row(
        "⚠️  Potentially Unused",
        str(len(unused_files)),
        "\n".join(unused_files) if unused_files else "None"
    )
    
    console.print(table)
    
    if unused_files:
        console.print("\n[yellow]⚠️  Potentially unused files:[/yellow]")
        for file in unused_files:
            console.print(f"  • {file}")
            # Try to understand what the file does
            with open(file, 'r') as f:
                lines = f.readlines()[:5]
                for line in lines:
                    if '"""' in line or "'''" in line or line.strip().startswith('#'):
                        doc = line.strip().replace('"""', '').replace("'''", '').replace('#', '')
                        if doc:
                            console.print(f"    → {doc}", style="dim")
                            break

if __name__ == "__main__":
    main()