#!/usr/bin/env python3
"""
Remove the 'uncertainty=' field from Parameter() calls since it's not a valid field.
The uncertainty should only be in the validation dict.
"""

import re
from pathlib import Path

def process_file(file_path: Path):
    """Remove uncertainty field from Parameter definitions."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        original = content

        # Pattern: Remove 'uncertainty=..., ' from Parameter definitions
        # This handles both 'uncertainty=None,' and 'uncertainty=0.75,'
        pattern = r',\s*\n\s*uncertainty=[^,]+,'

        content = re.sub(pattern, ',', content)

        if content != original:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        return False

    except Exception as e:
        print(f"Error processing {file_path.name}: {e}")
        return False

def main():
    """Process all v16 simulation files."""
    v16_dir = Path("h:/Github/PrincipiaMetaphysica/simulations/v16")

    py_files = [
        f for f in v16_dir.rglob("*.py")
        if f.name != "__init__.py" and "test_" not in f.name
    ]

    modified = 0
    for py_file in sorted(py_files):
        if process_file(py_file):
            print(f"[OK] Cleaned: {py_file.name}")
            modified += 1

    print(f"\nCleaned {modified}/{len(py_files)} files")

if __name__ == "__main__":
    main()
