#!/usr/bin/env python3
"""
Update source version references in v16 simulations.
"""

from pathlib import Path

# Replacement mappings
REPLACEMENTS = [
    ("NuFIT 5.2 (2022)", "NuFIT 6.0 (2024)"),
    ("NuFIT 5.2", "NuFIT 6.0"),
    ("PDG 2022", "PDG 2024"),
    ("PDG 2023", "PDG 2024"),
    ("DESI 2024 VI", "DESI 2024"),
]

def update_file(file_path: Path):
    """Update source version references in a file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        original = content

        for old, new in REPLACEMENTS:
            content = content.replace(old, new)

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
        if update_file(py_file):
            print(f"[OK] Updated: {py_file.name}")
            modified += 1

    print(f"\nUpdated {modified}/{len(py_files)} files")

if __name__ == "__main__":
    main()
