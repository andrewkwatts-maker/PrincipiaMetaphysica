#!/usr/bin/env python3
"""
Comprehensive fix for all Parameter syntax errors.
"""

import re
from pathlib import Path

def fix_parameter_closing_parens(content: str) -> str:
    """
    Fix all patterns where Parameter definitions are missing closing parenthesis.

    Patterns to fix:
    1. bound_source="...",\n            Parameter(
    2. bound_source="...",\n\n            Parameter(
    3. bound_source="...")\n            Parameter(  <- this one is correct, leave it
    """
    # Pattern 1: bound_source with comma, immediate Parameter
    pattern1 = r'(bound_source="[^"]+"),(\s*\n\s*)Parameter\('

    def fix1(match):
        bound_source = match.group(1)
        whitespace = match.group(2)
        return bound_source + '\n            ),\n            Parameter('

    content = re.sub(pattern1, fix1, content)

    # Pattern 2: bound_source without comma, immediate Parameter (but not if already has closing paren)
    pattern2 = r'(bound_source="[^"]+")(\s*\n\s*)(?!\))(\s*)Parameter\('

    def fix2(match):
        bound_source = match.group(1)
        whitespace = match.group(2)
        return bound_source + '\n            ),\n            Parameter('

    content = re.sub(pattern2, fix2, content)

    return content

def process_file(file_path: Path):
    """Fix Parameter syntax in a file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        original = content
        content = fix_parameter_closing_parens(content)

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
                print(f"  ✗ Still has error at line {e.lineno}")
                return False
        else:
            return False

    except Exception as e:
        print(f"[ERROR] {file_path.name}: {e}")
        return False

def main():
    """Process all v16 Python files."""
    v16_dir = Path("h:/Github/PrincipiaMetaphysica/simulations/v16")

    py_files = [
        f for f in v16_dir.rglob("*.py")
        if f.name != "__init__.py" and "test_" not in f.name
    ]

    modified = 0
    errors = 0

    for py_file in sorted(py_files):
        result = process_file(py_file)
        if result is True:
            modified += 1
        elif result is False and "error" in str(py_file).lower():
            errors += 1

    print(f"\nFixed {modified} files")

if __name__ == "__main__":
    main()
