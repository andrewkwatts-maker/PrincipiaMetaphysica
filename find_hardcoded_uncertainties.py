#!/usr/bin/env python3
"""
Find all hardcoded ± uncertainty values in HTML files and verify they exist in theory_output.json
"""

import re
import json
import os
from pathlib import Path

def load_theory_output():
    """Load theory_output.json"""
    with open('theory_output.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def find_hardcoded_uncertainties(html_file):
    """Find all ± patterns in HTML file"""
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Pattern: number ± number (various formats)
    patterns = [
        r'(\d+\.?\d*)\s*±\s*(\d+\.?\d*)',  # 5.0 ± 1.5
        r'(\d+\.?\d*)\s*&plusmn;\s*(\d+\.?\d*)',  # 5.0 &plusmn; 1.5
        r'(\d+\.?\d*)\s*\+/-\s*(\d+\.?\d*)',  # 5.0 +/- 1.5
    ]

    results = []
    for pattern in patterns:
        matches = re.finditer(pattern, content)
        for match in matches:
            central = match.group(1)
            error = match.group(2)
            # Get context (50 chars before and after)
            start = max(0, match.start() - 50)
            end = min(len(content), match.end() + 50)
            context = content[start:end].replace('\n', ' ')

            results.append({
                'file': html_file,
                'central': central,
                'error': error,
                'full_match': match.group(0),
                'context': context,
                'line': content[:match.start()].count('\n') + 1
            })

    return results

def check_if_in_pm_constants(uncertainty_data, theory_data):
    """Check if uncertainty value exists in theory_output.json"""
    central = float(uncertainty_data['central'])
    error = float(uncertainty_data['error'])

    # Search through theory_data for matching values
    def search_dict(d, path=""):
        matches = []
        for key, value in d.items():
            current_path = f"{path}.{key}" if path else key

            if isinstance(value, dict):
                matches.extend(search_dict(value, current_path))
            elif isinstance(value, (int, float)):
                # Check if this matches the central value (within 1%)
                if abs(value - central) / max(abs(central), 0.001) < 0.01:
                    # Look for associated error/std/uncertainty
                    error_keys = [
                        f"{key}_error", f"{key}_std", f"{key}_uncertainty",
                        f"{key}_sigma", "error", "std", "uncertainty", "sigma"
                    ]
                    for err_key in error_keys:
                        if err_key in d:
                            err_val = d[err_key]
                            if isinstance(err_val, (int, float)) and abs(err_val - error) / max(abs(error), 0.001) < 0.1:
                                matches.append({
                                    'path': current_path,
                                    'error_path': f"{path}.{err_key}" if path else err_key,
                                    'central_value': value,
                                    'error_value': err_val
                                })
        return matches

    return search_dict(theory_data)

def main():
    print("="*70)
    print("HARDCODED UNCERTAINTY VALUE SCAN")
    print("="*70)
    print()

    # Load theory output
    theory_data = load_theory_output()
    print(f"[OK] Loaded theory_output.json")
    print()

    # Find all HTML files
    html_files = []
    for ext in ['*.html']:
        html_files.extend(Path('.').rglob(ext))

    # Exclude certain directories
    html_files = [f for f in html_files if 'node_modules' not in str(f) and '.git' not in str(f)]

    print(f"[OK] Found {len(html_files)} HTML files to scan")
    print()

    all_uncertainties = []
    for html_file in html_files:
        uncertainties = find_hardcoded_uncertainties(str(html_file))
        if uncertainties:
            all_uncertainties.extend(uncertainties)

    print(f"[INFO] Found {len(all_uncertainties)} hardcoded uncertainty values")
    print()

    # Group by file
    by_file = {}
    for unc in all_uncertainties:
        file = unc['file']
        if file not in by_file:
            by_file[file] = []
        by_file[file].append(unc)

    # Analyze each uncertainty
    print("="*70)
    print("ANALYSIS RESULTS")
    print("="*70)
    print()

    missing_in_pm = []
    found_in_pm = []

    for file, uncs in sorted(by_file.items()):
        print(f"\n{file}:")
        print(f"  Found {len(uncs)} hardcoded uncertainties")

        for unc in uncs:
            matches = check_if_in_pm_constants(unc, theory_data)

            if matches:
                print(f"    [OK] {unc['central']} +/- {unc['error']} (line {unc['line']})")
                print(f"      -> Found: PM.{matches[0]['path']} +/- PM.{matches[0]['error_path']}")
                found_in_pm.append(unc)
            else:
                print(f"    [MISSING] {unc['central']} +/- {unc['error']} (line {unc['line']})")
                print(f"      -> NOT FOUND in theory_output.json")
                print(f"      -> Context: ...{unc['context']}...")
                missing_in_pm.append(unc)

    # Summary
    print()
    print("="*70)
    print("SUMMARY")
    print("="*70)
    print()
    print(f"Total hardcoded uncertainties: {len(all_uncertainties)}")
    print(f"  [OK] Found in PM constants: {len(found_in_pm)}")
    print(f"  [MISSING] Missing from PM constants: {len(missing_in_pm)}")
    print()

    if missing_in_pm:
        print("ACTION REQUIRED:")
        print("The following hardcoded values should be replaced with PM constant references:")
        print()
        for unc in missing_in_pm:
            print(f"  File: {unc['file']}:{unc['line']}")
            print(f"  Value: {unc['full_match']}")
            print(f"  Context: {unc['context'][:80]}...")
            print()

    # Save results
    with open('hardcoded_uncertainties_report.json', 'w') as f:
        json.dump({
            'total': len(all_uncertainties),
            'found_in_pm': len(found_in_pm),
            'missing_from_pm': len(missing_in_pm),
            'missing_details': missing_in_pm
        }, f, indent=2)

    print(f"[OK] Saved detailed report to hardcoded_uncertainties_report.json")

    return len(missing_in_pm)

if __name__ == '__main__':
    missing_count = main()
    if missing_count > 0:
        exit(1)  # Exit with error if missing values found
    else:
        exit(0)  # Success
