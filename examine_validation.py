#!/usr/bin/env python3
"""
Examine all validation_summary entries
"""

import json
from pathlib import Path

def examine_entries():
    """Examine all validation entries."""

    theory_file = Path(r'h:\Github\PrincipiaMetaphysica\theory_output.json')
    with open(theory_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    validation_summary = data.get('validation_summary', [])

    print(f"Total entries: {len(validation_summary)}\n")
    print("All entries:\n")

    for i, entry in enumerate(validation_summary):
        print(f"[{i}] Type: {type(entry)}, Length: {len(entry) if isinstance(entry, (list, dict)) else 'N/A'}")
        if isinstance(entry, list):
            print(f"     Content: {entry}")
        elif isinstance(entry, dict):
            print(f"     Keys: {list(entry.keys())}")
            print(f"     Content: {entry}")
        else:
            print(f"     Content: {entry}")
        print()

if __name__ == '__main__':
    examine_entries()
