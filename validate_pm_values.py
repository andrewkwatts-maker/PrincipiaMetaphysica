#!/usr/bin/env python3
"""
Validate that all PM.* value references in HTML files exist in theory-constants-enhanced.js
Copyright (c) 2025 Andrew Keith Watts. All rights reserved.
"""

import json
import re
import os
from pathlib import Path

def load_enhanced_constants():
    """Load the enhanced constants JavaScript file and extract PM object."""
    js_path = Path('theory-constants-enhanced.js')
    if not js_path.exists():
        print(f"ERROR: {js_path} not found!")
        return {}

    # Read JS file and extract JSON portion
    with open(js_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find the const PM = {...} section
    match = re.search(r'const PM = ({.*?});', content, re.DOTALL)
    if not match:
        print("ERROR: Could not parse PM object from JS file")
        return {}

    # Parse JSON
    pm_json = match.group(1)
    try:
        pm_data = json.loads(pm_json)
        return pm_data
    except json.JSONDecodeError as e:
        print(f"ERROR: Failed to parse PM JSON: {e}")
        return {}

def find_pm_references(html_file):
    """Find all PM.* references in an HTML file."""
    refs = []

    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find all data-category and data-param pairs
    pattern = r'data-category="([^"]*)" data-param="([^"]*)"'
    matches = re.findall(pattern, content)

    for category, param in matches:
        refs.append((category, param))

    return refs

def validate_references():
    """Validate all PM references across HTML files."""
    print("="*70)
    print("PM Value Reference Validation")
    print("="*70)

    # Load PM constants
    pm_data = load_enhanced_constants()
    if not pm_data:
        print("FAILED: Could not load PM constants")
        return False

    print(f"\n[OK] Loaded PM constants with {len(pm_data)} categories")

    # Print available categories
    print(f"\nAvailable categories:")
    for cat in sorted(pm_data.keys()):
        if isinstance(pm_data[cat], dict):
            params = list(pm_data[cat].keys())
            print(f"  {cat}: {len(params)} parameters")

    # Find all HTML files
    html_files = list(Path('.').glob('*.html')) + list(Path('sections').glob('*.html'))

    print(f"\n[OK] Found {len(html_files)} HTML files to check")

    # Validate each file
    all_valid = True
    missing_refs = []

    for html_file in sorted(html_files):
        refs = find_pm_references(html_file)
        if not refs:
            continue

        print(f"\n{html_file}:")
        print(f"  Found {len(refs)} PM references")

        file_valid = True
        for category, param in refs:
            # Check if category exists
            if category not in pm_data:
                print(f"    [MISSING] PM.{category}.{param} - category not found")
                missing_refs.append((str(html_file), category, param))
                file_valid = False
                all_valid = False
                continue

            # Check if parameter exists
            if not isinstance(pm_data[category], dict):
                print(f"    [ERROR] PM.{category} is not an object")
                missing_refs.append((str(html_file), category, param))
                file_valid = False
                all_valid = False
                continue

            if param not in pm_data[category]:
                print(f"    [MISSING] PM.{category}.{param} - parameter not found")
                missing_refs.append((str(html_file), category, param))
                file_valid = False
                all_valid = False
                continue

            # Get value for validation
            obj = pm_data[category][param]
            if isinstance(obj, dict) and 'value' in obj:
                value = obj['value']
                # Don't print display to avoid Unicode issues
                print(f"    [OK] PM.{category}.{param}")
            else:
                print(f"    [WARNING] PM.{category}.{param} exists but has unexpected structure")

        if file_valid:
            print(f"  [OK] All references valid")

    # Summary
    print("\n" + "="*70)
    if all_valid:
        print("[SUCCESS] All PM references are valid!")
        print(f"Validated {len(html_files)} files with PM.* references")
    else:
        print(f"[FAILED] Found {len(missing_refs)} missing references:")
        for html_file, category, param in missing_refs:
            print(f"  - {html_file}: PM.{category}.{param}")
        print("\nTo fix: Add missing parameters to generate_enhanced_constants.py")

    print("="*70)
    return all_valid

if __name__ == '__main__':
    success = validate_references()
    exit(0 if success else 1)
