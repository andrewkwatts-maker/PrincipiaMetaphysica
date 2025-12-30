#!/usr/bin/env python3
"""
sync_equation_numbering.py - Synchronize equation numbering from JSON to JS

This script:
1. Reads equation-registry.json (SINGLE SOURCE OF TRUTH)
2. Updates formula-registry.js labels to match
3. Generates a diff report for validation
4. Optionally applies changes

Usage:
    python scripts/sync_equation_numbering.py --diff     # Show diff only
    python scripts/sync_equation_numbering.py --apply    # Apply changes
    python scripts/sync_equation_numbering.py --validate # Validate current state

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.
"""

import json
import re
import sys
from pathlib import Path
from typing import Dict, List, Tuple
from dataclasses import dataclass


@dataclass
class EquationMapping:
    """Maps equation ID to numbering info."""
    registry_id: str
    equation_number: str
    label: str
    category: str
    section: int


@dataclass
class DiscrepancyReport:
    """Report of discrepancies found."""
    formula_id: str
    js_label: str
    json_number: str
    expected_label: str
    status: str  # 'MISMATCH', 'MISSING_IN_JS', 'EXTRA_IN_JS'


def load_equation_registry(registry_path: Path) -> Dict[str, EquationMapping]:
    """Load equation registry JSON as source of truth."""
    with open(registry_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    mappings = {}
    for eq_id, eq_data in data.get('equations', {}).items():
        mappings[eq_id] = EquationMapping(
            registry_id=eq_data.get('registryId', eq_id),
            equation_number=eq_data.get('equationNumber', ''),
            label=eq_data.get('label', ''),
            category=eq_data.get('category', ''),
            section=eq_data.get('section', 0)
        )

    return mappings


def parse_formula_registry_js(js_path: Path) -> Dict[str, Dict]:
    """Parse formula-registry.js to extract current labels."""
    content = js_path.read_text(encoding='utf-8')

    formulas = {}

    # Pattern to find formula definitions with labels
    # The label can be anywhere in the object, so we need to be more flexible
    # First, find all formula IDs that have a label property

    # Split by formula objects - look for "formula-id": {
    formula_block_pattern = re.compile(
        r'"([a-z0-9-]+)":\s*\{',
        re.IGNORECASE
    )

    # Find all potential formula IDs
    for match in formula_block_pattern.finditer(content):
        formula_id = match.group(1)
        start_pos = match.end()

        # Find the corresponding closing brace (accounting for nested braces)
        brace_count = 1
        pos = start_pos
        while pos < len(content) and brace_count > 0:
            if content[pos] == '{':
                brace_count += 1
            elif content[pos] == '}':
                brace_count -= 1
            pos += 1

        block = content[start_pos:pos]

        # Look for label in this block
        label_match = re.search(r'label:\s*"([^"]+)"', block)
        if label_match:
            label = label_match.group(1)
            formulas[formula_id] = {
                'id': formula_id,
                'current_label': label,
                'match_start': match.start(),
                'match_end': pos
            }

    return formulas


def extract_equation_number_from_label(label: str) -> Tuple[str, str]:
    """Extract equation number from label like '(2.6) Three Generations'."""
    match = re.match(r'\((\d+\.\d+[a-z]?)\)\s*(.+)', label)
    if match:
        return match.group(1), match.group(2)
    return '', label


def compare_registries(
    json_mappings: Dict[str, EquationMapping],
    js_formulas: Dict[str, Dict]
) -> List[DiscrepancyReport]:
    """Compare JSON registry with JS formula labels."""
    discrepancies = []

    # Check each JSON equation against JS
    for eq_id, mapping in json_mappings.items():
        expected_label = f"({mapping.equation_number}) {mapping.label}"

        if eq_id in js_formulas:
            js_label = js_formulas[eq_id]['current_label']
            js_num, js_text = extract_equation_number_from_label(js_label)

            # Check if equation number matches
            if js_num != mapping.equation_number:
                discrepancies.append(DiscrepancyReport(
                    formula_id=eq_id,
                    js_label=js_label,
                    json_number=mapping.equation_number,
                    expected_label=expected_label,
                    status='NUMBER_MISMATCH'
                ))
            elif js_text.strip() != mapping.label.strip():
                discrepancies.append(DiscrepancyReport(
                    formula_id=eq_id,
                    js_label=js_label,
                    json_number=mapping.equation_number,
                    expected_label=expected_label,
                    status='LABEL_MISMATCH'
                ))
        else:
            discrepancies.append(DiscrepancyReport(
                formula_id=eq_id,
                js_label='',
                json_number=mapping.equation_number,
                expected_label=expected_label,
                status='MISSING_IN_JS'
            ))

    # Check for formulas in JS that aren't in JSON
    for formula_id in js_formulas:
        if formula_id not in json_mappings:
            js_label = js_formulas[formula_id]['current_label']
            eq_num, _ = extract_equation_number_from_label(js_label)
            if eq_num:  # Only report if it has an equation number
                discrepancies.append(DiscrepancyReport(
                    formula_id=formula_id,
                    js_label=js_label,
                    json_number='',
                    expected_label='',
                    status='EXTRA_IN_JS'
                ))

    return discrepancies


def generate_js_update(
    js_path: Path,
    json_mappings: Dict[str, EquationMapping]
) -> str:
    """Generate updated formula-registry.js content with correct labels."""
    content = js_path.read_text(encoding='utf-8')

    for eq_id, mapping in json_mappings.items():
        expected_label = f"({mapping.equation_number}) {mapping.label}"

        # Pattern to find and replace the label for this formula
        # Match: "formula-id": { ... label: "whatever" ...
        pattern = rf'("{eq_id}":\s*\{{[^}}]*?label:\s*)"([^"]+)"'

        def replace_label(match):
            return f'{match.group(1)}"{expected_label}"'

        content = re.sub(pattern, replace_label, content, flags=re.DOTALL)

    return content


def sanitize_for_console(text: str) -> str:
    """Replace unicode with ASCII equivalents for Windows console."""
    replacements = {
        '\u2080': '_0', '\u2081': '_1', '\u2082': '_2', '\u2083': '_3',
        '\u2084': '_4', '\u2085': '_5', '\u2086': '_6', '\u2087': '_7',
        '\u2088': '_8', '\u2089': '_9',
        '\u2070': '^0', '\u00b9': '^1', '\u00b2': '^2', '\u00b3': '^3',
        '\u2074': '^4', '\u2075': '^5', '\u2076': '^6', '\u2077': '^7',
        '\u2078': '^8', '\u2079': '^9',
        '\u03b1': 'alpha', '\u03b2': 'beta', '\u03c7': 'chi',
        '\u03c3': 'sigma', '\u03c4': 'tau', '\u03b8': 'theta',
        '\u03bd': 'nu', '\u03c0': 'pi', '\u03b7': 'eta',
        '\u221a': 'sqrt', '\u00d7': 'x', '\u2248': '~',
        '\u2192': '->', '\u2026': '...', '\u0393': 'Gamma',
        '\u2212': '-', '\u222b': 'int',
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text


def print_diff_report(discrepancies: List[DiscrepancyReport]):
    """Print human-readable diff report."""
    print("=" * 70)
    print("EQUATION NUMBERING SYNC REPORT")
    print("=" * 70)

    if not discrepancies:
        print("\nNO DISCREPANCIES FOUND - All equation numbers are in sync!")
        return

    # Group by status
    by_status = {}
    for d in discrepancies:
        by_status.setdefault(d.status, []).append(d)

    print(f"\nTotal discrepancies: {len(discrepancies)}\n")

    for status, items in by_status.items():
        print(f"\n{status} ({len(items)} items):")
        print("-" * 50)

        for item in items:
            if status == 'NUMBER_MISMATCH':
                print(f"  {item.formula_id}:")
                print(f"    JS:       {sanitize_for_console(item.js_label)}")
                print(f"    Expected: {sanitize_for_console(item.expected_label)}")
            elif status == 'LABEL_MISMATCH':
                print(f"  {item.formula_id}:")
                print(f"    JS:       {sanitize_for_console(item.js_label)}")
                print(f"    Expected: {sanitize_for_console(item.expected_label)}")
            elif status == 'MISSING_IN_JS':
                print(f"  {item.formula_id}: NOT IN formula-registry.js")
                print(f"    Should be: {sanitize_for_console(item.expected_label)}")
            elif status == 'EXTRA_IN_JS':
                print(f"  {item.formula_id}: In JS but not in JSON registry")
                print(f"    JS label: {sanitize_for_console(item.js_label)}")

    print("\n" + "=" * 70)


def main():
    import argparse

    parser = argparse.ArgumentParser(description='Sync equation numbering')
    parser.add_argument('--diff', action='store_true', help='Show diff only')
    parser.add_argument('--apply', action='store_true', help='Apply changes')
    parser.add_argument('--validate', action='store_true', help='Validate current state')
    parser.add_argument('--project-root', default='.', help='Project root directory')

    args = parser.parse_args()

    # Default to diff if no action specified
    if not args.diff and not args.apply and not args.validate:
        args.diff = True

    project_root = Path(args.project_root).resolve()
    registry_path = project_root / 'content-templates' / 'equation-registry.json'
    js_path = project_root / 'js' / 'formula-registry.js'

    if not registry_path.exists():
        print(f"Error: Registry not found: {registry_path}")
        sys.exit(1)

    if not js_path.exists():
        print(f"Error: formula-registry.js not found: {js_path}")
        sys.exit(1)

    print(f"Loading equation registry from: {registry_path}")
    json_mappings = load_equation_registry(registry_path)
    print(f"Found {len(json_mappings)} equations in registry")

    print(f"\nParsing formula-registry.js: {js_path}")
    js_formulas = parse_formula_registry_js(js_path)
    print(f"Found {len(js_formulas)} formulas in JS file")

    # Compare
    discrepancies = compare_registries(json_mappings, js_formulas)

    if args.diff or args.validate:
        print_diff_report(discrepancies)

        if args.validate:
            if discrepancies:
                print("\nVALIDATION FAILED: Discrepancies found")
                sys.exit(1)
            else:
                print("\nVALIDATION PASSED: All in sync")
                sys.exit(0)

    if args.apply:
        if not discrepancies:
            print("\nNo changes needed - already in sync")
            sys.exit(0)

        print("\nApplying changes to formula-registry.js...")
        updated_content = generate_js_update(js_path, json_mappings)

        # Backup original
        backup_path = js_path.with_suffix('.js.bak')
        js_path.rename(backup_path)
        print(f"Backed up original to: {backup_path}")

        # Write updated
        js_path.write_text(updated_content, encoding='utf-8')
        print(f"Updated: {js_path}")

        # Verify
        new_js_formulas = parse_formula_registry_js(js_path)
        new_discrepancies = compare_registries(json_mappings, new_js_formulas)

        if new_discrepancies:
            print(f"\nWarning: {len(new_discrepancies)} discrepancies remain after update")
            print("Some formulas may need manual review")
        else:
            print("\nAll equation numbers now in sync!")

        # Clean up backup
        backup_path.unlink()
        print(f"Removed backup: {backup_path}")


if __name__ == '__main__':
    main()
