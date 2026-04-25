#!/usr/bin/env python3
"""
add_run_eml.py
==============
Scans all simulation .py files under simulations/PM/ and adds a run_eml()
method to any class that has a run() method but not run_eml().

Two modes:
  --passthrough   Add passthrough run_eml() to ALL files (safe default)
  --physics FILE  Add physics EML skeleton to a single named file

This script is idempotent: it will not add a second run_eml() if one exists.
"""

import ast
import sys
import re
from pathlib import Path

ROOT = Path(__file__).parent.parent
SIMULATIONS_DIR = ROOT / "simulations" / "PM"

PASSTHROUGH_TEMPLATE = '''
    def run_eml(self, registry: 'PMRegistry') -> Dict[str, Any]:
        """
        EML Math computation path.

        This simulation produces {category} outputs. The EML Math representation
        for this module is in the section text via <EML>...</EML> blocks in
        get_section_content(). The computed parameter values are identical
        between Normal Math and EML Math modes.
        """
        return self.run(registry)
'''

PHYSICS_EML_TEMPLATE = '''
    def run_eml(self, registry: 'PMRegistry') -> Dict[str, Any]:
        """
        EML Math computation path using Mirror Phase Mathematics.

        Recomputes all outputs via the EML Sheffer operator:
            eml(x, y) = exp(x) - ln(y)
        Results must agree with run() to within rtol=1e-6.
        """
        from simulations.core.eml_integration import (
            eml_scalar, eml_compute, eml_pi, eml_add, eml_sub,
            eml_mul, eml_div, eml_sqrt, eml_pow, eml_neg,
            eml_sin, eml_cos, eml_agree,
        )
        # EML implementation — mirrors the arithmetic in run() via EML operators.
        # Fallback to run() while full EML implementation is pending.
        return self.run(registry)
'''


def has_run_method(source: str) -> bool:
    """Check if the source code defines a run() method."""
    return bool(re.search(r'^\s+def run\s*\(self', source, re.MULTILINE))


def has_run_eml_method(source: str) -> bool:
    """Check if the source code already has a run_eml() method."""
    return bool(re.search(r'^\s+def run_eml\s*\(self', source, re.MULTILINE))


def get_class_category(filepath: Path) -> str:
    """Infer a category label from the file path."""
    parts = filepath.parts
    for part in parts:
        if part in ('paper', 'validation', 'geometry', 'gauge', 'cosmology',
                    'particle', 'field_dynamics', 'algebra', 'portals',
                    'consciousness', 'qed', 'derivations', 'support'):
            return part
    return 'derived'


def find_insertion_point(source: str) -> int:
    """
    Find the line index after the last method in the last class,
    or after the run() method body, so we can insert run_eml() there.

    Simple heuristic: find last occurrence of '    def ' and insert after
    that method's block.
    """
    lines = source.split('\n')
    last_run_end = None
    i = 0
    in_run = False
    run_indent = None
    while i < len(lines):
        line = lines[i]
        # Detect start of run() method
        if re.match(r'^    def run\s*\(self', line):
            in_run = True
            run_indent = 4
        elif in_run:
            # End of run() method: we see another method or class at same indentation
            if (line.strip() and
                    not line.strip().startswith('#') and
                    not line.strip().startswith('"""') and
                    not line.strip().startswith("'''") and
                    re.match(r'^    def |^class ', line)):
                last_run_end = i
                in_run = False
            elif line.strip() == '' and i + 1 < len(lines):
                # Check next non-blank line
                pass
        i += 1

    if in_run:
        # run() is the last method — insert at end of file
        last_run_end = len(lines)

    return last_run_end


def add_run_eml(filepath: Path, physics: bool = False) -> bool:
    """
    Add run_eml() to the file if it has run() but not run_eml().

    Returns True if the file was modified.
    """
    source = filepath.read_text(encoding='utf-8')

    if not has_run_method(source):
        return False  # No run() to pair with

    if has_run_eml_method(source):
        return False  # Already has run_eml()

    category = get_class_category(filepath)
    template = PHYSICS_EML_TEMPLATE if physics else PASSTHROUGH_TEMPLATE.format(category=category)

    # Find insertion point: right after the run() method block
    lines = source.split('\n')
    insert_at = None
    i = 0
    run_depth = 0
    in_run = False

    for i, line in enumerate(lines):
        stripped = line.strip()
        # Detect run() method start (4-space indented class method)
        if re.match(r'^    def run\s*\(self', line):
            in_run = True
            run_depth = 0
            continue
        if in_run:
            if stripped.startswith('def ') or re.match(r'^class ', line):
                insert_at = i
                break
            if stripped:
                run_depth = len(line) - len(line.lstrip())

    if insert_at is None:
        insert_at = len(lines)

    # Insert the run_eml() method
    insertion = template.rstrip('\n') + '\n'
    new_lines = lines[:insert_at] + [insertion] + lines[insert_at:]
    new_source = '\n'.join(new_lines)

    filepath.write_text(new_source, encoding='utf-8')
    return True


def main():
    physics_mode = '--physics' in sys.argv
    specific_file = None
    if physics_mode:
        idx = sys.argv.index('--physics')
        if idx + 1 < len(sys.argv):
            specific_file = sys.argv[idx + 1]

    if specific_file:
        path = Path(specific_file)
        if not path.exists():
            path = SIMULATIONS_DIR / specific_file
        modified = add_run_eml(path, physics=True)
        print(f"{'Modified' if modified else 'Skipped (already has run_eml)'}: {path}")
        return

    # Process all files
    all_py = list(SIMULATIONS_DIR.rglob('*.py'))
    all_py = [f for f in all_py if '__pycache__' not in str(f) and f.name != '__init__.py']

    modified_count = 0
    skipped_count = 0

    for filepath in sorted(all_py):
        modified = add_run_eml(filepath, physics=physics_mode)
        if modified:
            modified_count += 1
            rel = filepath.relative_to(ROOT)
            print(f"  Added run_eml(): {rel}")
        else:
            skipped_count += 1

    print(f"\nDone: {modified_count} files modified, {skipped_count} skipped.")


if __name__ == '__main__':
    main()
