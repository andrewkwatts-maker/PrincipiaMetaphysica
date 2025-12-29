#!/usr/bin/env python3
"""
Fix syntax errors in Parameter definitions caused by removing uncertainty field.
The issue is that when we removed 'uncertainty=..., ' some Parameter() calls lost their closing parenthesis.
"""

import re
from pathlib import Path

def fix_parameter_syntax(content: str) -> str:
    """
    Fix Parameter definitions that are missing closing parenthesis.

    Pattern to fix:
        bound_source="...",
        <missing )>,
        Parameter(

    Should be:
        bound_source="..."
        ),
        Parameter(
    """
    # Find patterns where bound_source is followed directly by Parameter(
    # This indicates a missing ),
    pattern = r'(bound_source="[^"]+")(\s*\n\s*)Parameter\('

    def add_paren(match):
        bound_source = match.group(1)
        whitespace = match.group(2)
        return bound_source + '\n            ),\n            Parameter('

    content = re.sub(pattern, add_paren, content)

    # Also handle case where bound_source is the last field before validation
    pattern2 = r'(bound_source="[^"]+")(\s*\n\s*)validation='

    def add_paren2(match):
        bound_source = match.group(1)
        whitespace = match.group(2)
        return bound_source + ',\n                validation='

    content = re.sub(pattern2, add_paren2, content)

    return content

def process_file(file_path: Path):
    """Fix Parameter syntax in a file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        original = content
        content = fix_parameter_syntax(content)

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

    # List of files with known syntax errors
    problem_files = [
        "cosmology/dark_energy_v16_0.py",
        "cosmology/s8_bulk_viscosity_solver.py",
        "fermion/chirality_v16_0.py",
        "fermion/ckm_matrix_v16_0.py",
        "fermion/fermion_generations_v16_0.py",
        "quantum_bio/orch_or_geometry_v16_1.py",
    ]

    modified = 0
    for file_rel in problem_files:
        file_path = v16_dir / file_rel
        if file_path.exists():
            if process_file(file_path):
                print(f"[OK] Fixed: {file_path.name}")
                modified += 1
                # Test compilation
                try:
                    import py_compile
                    py_compile.compile(str(file_path), doraise=True)
                    print(f"  ✓ Compiles successfully")
                except SyntaxError as e:
                    print(f"  ✗ Still has syntax error: {e}")
        else:
            print(f"[SKIP] Not found: {file_rel}")

    print(f"\nFixed {modified}/{len(problem_files)} files")

if __name__ == "__main__":
    main()
