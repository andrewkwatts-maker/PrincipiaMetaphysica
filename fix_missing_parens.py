#!/usr/bin/env python3
"""
Fix missing closing parentheses in Parameter definitions.
"""

import re
from pathlib import Path

def fix_missing_parens(content: str) -> str:
    """
    Fix Parameter definitions missing closing parenthesis.

    Pattern:
        bound_source="..."[,]
        <blank line or whitespace>
        Parameter(

    Should be:
        bound_source="..."
        ),
        Parameter(
    """
    # Remove trailing comma after bound_source if followed by Parameter
    pattern = r'(bound_source="[^"]+"),?\s*\n\s*\n\s*Parameter\('

    def fix(match):
        # Extract just the bound_source part
        full_match = match.group(0)
        bound_source_line = match.group(1)

        # Return fixed version
        return bound_source_line + '\n            ),\n            Parameter('

    content = re.sub(pattern, fix, content)

    return content

def process_file(file_path: Path):
    """Fix Parameter syntax in a file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        original = content
        content = fix_missing_parens(content)

        if content != original:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"[OK] Fixed: {file_path.name}")

            # Test compilation
            try:
                import py_compile
                py_compile.compile(str(file_path), doraise=True)
                print(f"  ✓ Compiles successfully")
                return True
            except SyntaxError as e:
                print(f"  ✗ Still has syntax error at line {e.lineno}: {e.msg}")
                return False
        else:
            print(f"  No changes: {file_path.name}")
            return False

    except Exception as e:
        print(f"[ERROR] {file_path.name}: {e}")
        return False

def main():
    """Process all v16 simulation files with known syntax errors."""
    v16_dir = Path("h:/Github/PrincipiaMetaphysica/simulations/v16")

    # List of files with known syntax errors (from earlier compile test)
    problem_files = [
        "cosmology/dark_energy_v16_0.py",
        "cosmology/s8_bulk_viscosity_solver.py",
        "fermion/ckm_matrix_v16_0.py",
        "fermion/fermion_generations_v16_0.py",
        "quantum_bio/orch_or_geometry_v16_1.py",
    ]

    modified = 0
    for file_rel in problem_files:
        file_path = v16_dir / file_rel
        if file_path.exists():
            if process_file(file_path):
                modified += 1
        else:
            print(f"[SKIP] Not found: {file_rel}")

    print(f"\nFixed {modified}/{len(problem_files)} files")

if __name__ == "__main__":
    main()
