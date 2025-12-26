#!/usr/bin/env python3
"""
Restore the parameters section from the last git commit,
then we can re-run the fix script correctly.
"""

import json
import subprocess
from pathlib import Path

def main():
    filepath = Path(__file__).parent / 'theory_output.json'

    # Get the original parameters section from git
    print("Fetching original parameters from git...")
    result = subprocess.run(
        ['git', 'show', 'HEAD:theory_output.json'],
        capture_output=True,
        text=True,
        cwd=filepath.parent
    )

    if result.returncode != 0:
        print(f"Error: {result.stderr}")
        return

    original_data = json.loads(result.stdout)
    original_params = original_data.get('parameters', {})

    # Load current file
    with open(filepath, 'r', encoding='utf-8') as f:
        current_data = json.load(f)

    # Replace parameters section with original
    current_data['parameters'] = original_params

    # Save
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(current_data, f, indent=2, ensure_ascii=False)

    print(f"Restored parameters section from git HEAD")
    print(f"Original structure:")
    print(f"  dimensions.D_BULK: {original_params['dimensions']['D_BULK']}")
    print(f"  topology.CHI_EFF: {original_params['topology']['CHI_EFF']}")
    print(f"\nNow run fix_parameters_metadata.py to apply fixes correctly.")

if __name__ == '__main__':
    main()
