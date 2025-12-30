#!/usr/bin/env python3
"""
Delete the migrated HTML files after confirming migration is complete.
"""

import os
from pathlib import Path

def main():
    base_path = Path(__file__).parent
    foundations_dir = base_path / 'foundations'

    files_to_delete = [
        'einstein-field-equations.html',
        'einstein-hilbert-action.html',
        'ricci-tensor.html',
        'metric-tensor.html'
    ]

    print("=" * 80)
    print("DELETING MIGRATED HTML FILES")
    print("=" * 80)
    print()

    deleted = []
    not_found = []

    for filename in files_to_delete:
        filepath = foundations_dir / filename
        if filepath.exists():
            try:
                os.remove(filepath)
                deleted.append(filename)
                print(f"[DELETED] {filename}")
            except Exception as e:
                print(f"[ERROR] Could not delete {filename}: {e}")
        else:
            not_found.append(filename)
            print(f"[NOT FOUND] {filename}")

    print()
    print("=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"Files deleted: {len(deleted)}")
    print(f"Files not found: {len(not_found)}")
    print()

    if deleted:
        print("Successfully deleted:")
        for f in deleted:
            print(f"  - {f}")

    print()
    print("[COMPLETE] Migration cleanup finished!")

if __name__ == '__main__':
    main()
