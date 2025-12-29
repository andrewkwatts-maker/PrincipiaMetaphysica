#!/usr/bin/env python3
"""
Quick script to add MIT license reference to files with copyright.

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.
Licensed under the MIT License. See LICENSE file for details.
"""

import os
import sys
from pathlib import Path

def add_license_to_file(filepath):
    """Add MIT license reference after copyright line in a file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Check if already has license
    content = ''.join(lines)
    if 'Licensed under the MIT License' in content or 'MIT License' in content:
        return False, "Already has license"

    if 'Copyright (c) 2025' not in content or 'Andrew Keith Watts' not in content:
        return False, "No copyright found"

    # Find copyright line and add license after it
    new_lines = []
    added = False

    for i, line in enumerate(lines):
        new_lines.append(line)
        if not added and 'Copyright (c) 2025' in line and 'Andrew Keith Watts' in line:
            # Add license line on next line
            new_lines.append("Licensed under the MIT License. See LICENSE file for details.\n")
            added = True

    if added:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.writelines(new_lines)
        return True, "License added"

    return False, "Could not find copyright line"

def main():
    repo_root = Path(r"h:\Github\PrincipiaMetaphysica")

    # Patterns to process
    patterns = [
        "simulations/base/*.py",
        "simulations/v16/*/*.py",
        "simulations/v16/*/*/*.py",
    ]

    updated = []
    skipped = []
    errors = []

    for pattern in patterns:
        for filepath in repo_root.glob(pattern):
            if filepath.is_file() and filepath.suffix == '.py':
                try:
                    success, msg = add_license_to_file(filepath)
                    rel_path = filepath.relative_to(repo_root)

                    if success:
                        updated.append(str(rel_path))
                        print(f"✓ {rel_path}")
                    else:
                        skipped.append(f"{rel_path}: {msg}")
                except Exception as e:
                    errors.append(f"{filepath}: {str(e)}")
                    print(f"✗ {filepath}: {e}")

    print(f"\n{'='*70}")
    print(f"Updated: {len(updated)} files")
    print(f"Skipped: {len(skipped)} files")
    print(f"Errors: {len(errors)} files")

    if errors:
        print("\nErrors:")
        for error in errors:
            print(f"  {error}")

if __name__ == "__main__":
    main()
