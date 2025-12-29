#!/usr/bin/env python3
"""
Fix Duplicate Copyright Notices in Simulation Files
====================================================

Removes duplicate copyright notices that were accidentally added.
Ensures each file has exactly one copyright notice with dedication.
"""

import os
import re
from pathlib import Path
from typing import List

def fix_duplicates(content: str) -> str:
    """Remove duplicate copyright notices, keeping the complete one with dedication."""

    # Pattern to match the full copyright block
    copyright_pattern = r'Copyright \(c\) 2025-2026 Andrew Keith Watts\. All rights reserved\.'

    # Count occurrences
    occurrences = list(re.finditer(copyright_pattern, content))

    if len(occurrences) <= 1:
        return content  # No duplicates

    # Check if we have the dedication
    has_dedication = "Dedicated To:" in content and "Elizabeth May Watts" in content

    if not has_dedication:
        # Shouldn't happen, but if it does, keep first occurrence
        return content

    # Find the copyright notice that's followed by the dedication
    dedication_pattern = r'Dedicated To:\s+My Wife: Elizabeth May Watts\s+Our Messiah: Jesus Of Nazareth'

    # Find which copyright is associated with the dedication
    dedication_match = re.search(dedication_pattern, content)
    if not dedication_match:
        return content

    # Find the copyright that comes right before the dedication
    for i, match in enumerate(occurrences):
        # Check if this copyright is followed by dedication (with possible whitespace)
        text_after = content[match.end():dedication_match.start()]
        if text_after.strip() == "":
            # This is the good one, keep it
            keep_index = i
            break
    else:
        # Couldn't find the right one, return unchanged
        return content

    # Remove all copyright notices except the one we want to keep
    result = content
    for i in reversed(range(len(occurrences))):
        if i != keep_index:
            match = occurrences[i]
            # Remove this copyright notice
            # Find the line it's on and remove it
            start = match.start()
            end = match.end()

            # Extend to include the newline after
            if end < len(result) and result[end] == '\n':
                end += 1

            # Also remove any blank lines immediately after
            while end < len(result) and result[end] == '\n':
                end += 1

            result = result[:start] + result[end:]

    return result

def process_file(file_path: Path) -> bool:
    """Process a single file to fix duplicates. Returns True if modified."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            original_content = f.read()
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return False

    fixed_content = fix_duplicates(original_content)

    if fixed_content == original_content:
        return False

    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(fixed_content)
        return True
    except Exception as e:
        print(f"Error writing {file_path}: {e}")
        return False

def find_python_files(base_dir: Path) -> List[Path]:
    """Find all Python files in simulations directory."""
    python_files = []

    for root, dirs, files in os.walk(base_dir):
        # Skip __pycache__ directories
        dirs[:] = [d for d in dirs if d != '__pycache__']

        for file in files:
            if file.endswith('.py'):
                python_files.append(Path(root) / file)

    return sorted(python_files)

def main():
    """Main execution function."""
    base_dir = Path(r'h:\Github\PrincipiaMetaphysica\simulations')

    if not base_dir.exists():
        print(f"Error: Directory not found: {base_dir}")
        return

    print(f"Scanning for Python files with duplicates in: {base_dir}")
    python_files = find_python_files(base_dir)

    modified_count = 0
    for file_path in python_files:
        if process_file(file_path):
            modified_count += 1
            relative_path = file_path.relative_to(base_dir.parent)
            print(f"FIXED: {relative_path}")

    print(f"\nFixed {modified_count} files with duplicate copyright notices")

if __name__ == "__main__":
    main()
