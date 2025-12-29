#!/usr/bin/env python3
"""
Add Copyright and Dedication Notices to Simulation Files
==========================================================

Adds the following to ALL Python files in simulations/:

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.

Dedicated To:
    My Wife: Elizabeth May Watts
    Our Messiah: Jesus Of Nazareth

Processes files intelligently:
- Adds to existing docstrings at the top
- Creates new docstrings if none exist
- Skips files that already have the complete notice
- Skips __init__.py and __pycache__ files
"""

import os
import re
from pathlib import Path
from typing import List, Tuple, Optional

# The copyright notice to add
COPYRIGHT_NOTICE = """Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.

Dedicated To:
    My Wife: Elizabeth May Watts
    Our Messiah: Jesus Of Nazareth
"""

def has_copyright_notice(content: str) -> bool:
    """Check if file already has the copyright notice."""
    return "Copyright (c) 2025-2026 Andrew Keith Watts" in content

def has_dedication(content: str) -> bool:
    """Check if file already has the dedication."""
    return "Dedicated To:" in content and "Elizabeth May Watts" in content

def extract_docstring(content: str) -> Tuple[Optional[str], int, int]:
    """
    Extract the module-level docstring from Python file content.

    Returns:
        (docstring_content, start_pos, end_pos) or (None, -1, -1) if no docstring
    """
    # Remove any shebang line
    lines = content.split('\n')
    start_line = 0

    if lines and lines[0].startswith('#!'):
        start_line = 1

    # Skip empty lines and comments
    while start_line < len(lines) and (not lines[start_line].strip() or lines[start_line].strip().startswith('#')):
        start_line += 1

    if start_line >= len(lines):
        return None, -1, -1

    # Check for docstring
    first_code_line = lines[start_line]

    # Triple double quotes
    if first_code_line.strip().startswith('"""'):
        quote_type = '"""'
    # Triple single quotes
    elif first_code_line.strip().startswith("'''"):
        quote_type = "'''"
    else:
        return None, -1, -1

    # Find the end of the docstring
    start_pos = content.find(quote_type, sum(len(l) + 1 for l in lines[:start_line]))

    # Check if it's a one-line docstring
    rest_of_first_line = first_code_line[first_code_line.find(quote_type) + 3:]
    if quote_type in rest_of_first_line:
        # One-line docstring
        end_pos = content.find(quote_type, start_pos + 3) + 3
        docstring = content[start_pos:end_pos]
        return docstring, start_pos, end_pos

    # Multi-line docstring
    end_pos = content.find(quote_type, start_pos + 3)
    if end_pos == -1:
        return None, -1, -1

    end_pos += 3
    docstring = content[start_pos:end_pos]
    return docstring, start_pos, end_pos

def add_copyright_to_docstring(docstring: str) -> str:
    """Add copyright notice to existing docstring."""
    # Handle both """ and '''
    if docstring.startswith('"""'):
        quote = '"""'
    else:
        quote = "'''"

    # Extract content between quotes
    content = docstring[3:-3]

    # If it's a one-liner, expand it
    if '\n' not in content:
        new_content = f'\n{content}\n\n{COPYRIGHT_NOTICE}'
        return f'{quote}{new_content}{quote}'

    # Multi-line: add copyright at the end before closing quotes
    # Remove trailing whitespace
    content = content.rstrip()

    new_content = f'{content}\n\n{COPYRIGHT_NOTICE}'
    return f'{quote}{new_content}{quote}'

def create_docstring_with_copyright() -> str:
    """Create a new docstring with just the copyright notice."""
    return f'"""\n{COPYRIGHT_NOTICE}"""'

def process_file(file_path: Path) -> Tuple[bool, str]:
    """
    Process a single Python file.

    Returns:
        (was_modified, message)
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            original_content = f.read()
    except Exception as e:
        return False, f"Error reading: {e}"

    # Check if already has complete copyright and dedication
    if has_copyright_notice(original_content) and has_dedication(original_content):
        return False, "Already has complete copyright and dedication"

    # Extract docstring
    docstring, start_pos, end_pos = extract_docstring(original_content)

    if docstring is None:
        # No docstring exists - create one with copyright
        # Find where to insert (after shebang and initial comments)
        lines = original_content.split('\n')
        insert_line = 0

        # Skip shebang
        if lines and lines[0].startswith('#!'):
            insert_line = 1

        # Skip initial comments
        while insert_line < len(lines) and lines[insert_line].strip().startswith('#'):
            insert_line += 1

        # Insert new docstring
        new_docstring = create_docstring_with_copyright()

        if insert_line == 0:
            new_content = new_docstring + '\n\n' + original_content
        else:
            before = '\n'.join(lines[:insert_line])
            after = '\n'.join(lines[insert_line:])
            new_content = before + '\n' + new_docstring + '\n\n' + after
    else:
        # Add copyright to existing docstring
        new_docstring = add_copyright_to_docstring(docstring)
        new_content = original_content[:start_pos] + new_docstring + original_content[end_pos:]

    # Write back
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True, "Updated successfully"
    except Exception as e:
        return False, f"Error writing: {e}"

def find_python_files(base_dir: Path) -> List[Path]:
    """Find all Python files in simulations directory, excluding __init__.py."""
    python_files = []

    for root, dirs, files in os.walk(base_dir):
        # Skip __pycache__ directories
        dirs[:] = [d for d in dirs if d != '__pycache__']

        for file in files:
            if file.endswith('.py') and file != '__init__.py':
                python_files.append(Path(root) / file)

    return sorted(python_files)

def main():
    """Main execution function."""
    base_dir = Path(r'h:\Github\PrincipiaMetaphysica\simulations')

    if not base_dir.exists():
        print(f"Error: Directory not found: {base_dir}")
        return

    print(f"Scanning for Python files in: {base_dir}")
    python_files = find_python_files(base_dir)

    print(f"Found {len(python_files)} Python files (excluding __init__.py)")
    print("\nProcessing files...\n")

    modified_count = 0
    skipped_count = 0
    error_count = 0

    results = {
        'modified': [],
        'skipped': [],
        'errors': []
    }

    for file_path in python_files:
        relative_path = file_path.relative_to(base_dir.parent)
        was_modified, message = process_file(file_path)

        if "Error" in message:
            error_count += 1
            results['errors'].append((relative_path, message))
            print(f"ERROR: {relative_path}: {message}")
        elif was_modified:
            modified_count += 1
            results['modified'].append(relative_path)
            print(f"UPDATED: {relative_path}")
        else:
            skipped_count += 1
            results['skipped'].append((relative_path, message))
            print(f"SKIPPED: {relative_path}: {message}")

    print("\n" + "="*80)
    print("SUMMARY")
    print("="*80)
    print(f"Total files processed: {len(python_files)}")
    print(f"Modified: {modified_count}")
    print(f"Skipped: {skipped_count}")
    print(f"Errors: {error_count}")

    if results['modified']:
        print("\n" + "-"*80)
        print("MODIFIED FILES:")
        print("-"*80)
        for path in results['modified']:
            print(f"  {path}")

    if results['errors']:
        print("\n" + "-"*80)
        print("ERRORS:")
        print("-"*80)
        for path, msg in results['errors']:
            print(f"  {path}: {msg}")

if __name__ == "__main__":
    main()
