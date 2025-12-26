#!/usr/bin/env python3
"""
Check the structure of validation_summary
"""

import json
from pathlib import Path

def check_structure():
    """Check validation_summary structure."""

    theory_file = Path(r'h:\Github\PrincipiaMetaphysica\theory_output.json')
    with open(theory_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    validation_summary = data.get('validation_summary', [])

    print(f"Type of validation_summary: {type(validation_summary)}")
    print(f"Length: {len(validation_summary)}")

    if validation_summary:
        print(f"\nFirst entry type: {type(validation_summary[0])}")
        print(f"First entry preview:")
        print(json.dumps(validation_summary[0], indent=2)[:500])

        if isinstance(validation_summary[0], list):
            print(f"\nNested list detected. First element of first list:")
            if validation_summary[0]:
                print(json.dumps(validation_summary[0][0], indent=2)[:500])

if __name__ == '__main__':
    check_structure()
