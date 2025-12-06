#!/usr/bin/env python3
"""
V12.0 Consistency Validation Script
====================================

Checks all files for outdated version references and ensures v12.0 consistency.

Copyright (c) 2025 Andrew Keith Watts. All rights reserved.
"""

import re
from pathlib import Path
from typing import Dict, List, Tuple

def check_file_for_old_versions(filepath: Path) -> List[Tuple[int, str]]:
    """Check a file for references to old versions (v8.4, v9, v10, v11)"""
    issues = []

    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            for i, line in enumerate(f, 1):
                # Skip version history and documentation files
                if 'VERSION' in str(filepath) or 'CHANGELOG' in str(filepath):
                    continue
                if 'v8.4 to 12.0' in str(filepath) or 'changes.txt' in str(filepath):
                    continue

                # Check for outdated version references
                if re.search(r'v8\.4(?!\s*→|\s*to)', line, re.IGNORECASE):
                    issues.append((i, f"Reference to v8.4: {line.strip()[:100]}"))
                if re.search(r'v9\.0(?!\s*→|\s*to)', line, re.IGNORECASE):
                    issues.append((i, f"Reference to v9.0: {line.strip()[:100]}"))
                if re.search(r'v10\.0(?!\s*→|\s*to)', line, re.IGNORECASE):
                    issues.append((i, f"Reference to v10.0: {line.strip()[:100]}"))
                if re.search(r'v11\.0(?!\s*→|\s*to)', line, re.IGNORECASE):
                    issues.append((i, f"Reference to v11.0: {line.strip()[:100]}"))

                # Check for "current version" statements that might be outdated
                if re.search(r'current.*version.*(?:8|9|10|11)', line, re.IGNORECASE):
                    if '12' not in line:
                        issues.append((i, f"Outdated 'current version': {line.strip()[:100]}"))

    except Exception as e:
        print(f"Error reading {filepath}: {e}")

    return issues

def validate_simulation_runner(filepath: Path) -> List[str]:
    """Validate run_all_simulations.py is correctly structured for v12.0"""
    issues = []

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # Check version declaration
        if 'VERSION = "12.0"' not in content and "version': '12.0'" not in content:
            issues.append("Missing VERSION = '12.0' declaration")

        # Check all v9-v12 functions are present
        required_functions = [
            'run_v9_transparency',
            'run_v9_brst_proof',
            'run_v10_geometric_derivations',
            'run_v10_1_neutrino_masses',
            'run_v10_2_all_fermions',
            'run_v11_final_observables',
            'run_v12_final_values'
        ]

        for func in required_functions:
            if f'def {func}' not in content:
                issues.append(f"Missing function: {func}")

        # Check all are called in main
        if 'run_all_simulations' in content:
            for func in required_functions:
                if f'{func}(' not in content:
                    issues.append(f"Function {func} not called in main")

    except Exception as e:
        issues.append(f"Error validating: {e}")

    return issues

def scan_directory() -> Dict[str, List]:
    """Scan all relevant files for v12.0 consistency"""

    base_path = Path(__file__).parent

    # Files to check
    html_files = list(base_path.glob('*.html'))
    html_files.extend(base_path.glob('sections/*.html'))
    html_files.extend(base_path.glob('foundations/*.html'))

    py_files = [
        base_path / 'config.py',
        base_path / 'run_all_simulations.py',
        base_path / 'generate_enhanced_constants.py',
        base_path / 'sections_content.py'
    ]

    md_files = list(base_path.glob('*.md'))

    results = {}

    print("="*80)
    print("V12.0 CONSISTENCY VALIDATION")
    print("="*80)
    print()

    # Check HTML files
    print("Checking HTML files...")
    for filepath in html_files:
        issues = check_file_for_old_versions(filepath)
        if issues:
            results[str(filepath)] = issues

    # Check Python files
    print("Checking Python files...")
    for filepath in py_files:
        if filepath.exists():
            issues = check_file_for_old_versions(filepath)
            if issues:
                results[str(filepath)] = issues

    # Special check for run_all_simulations.py
    print("Validating run_all_simulations.py structure...")
    runner_issues = validate_simulation_runner(base_path / 'run_all_simulations.py')
    if runner_issues:
        results['run_all_simulations.py [STRUCTURE]'] = [(0, issue) for issue in runner_issues]

    # Check markdown files (exclude changelogs)
    print("Checking documentation files...")
    for filepath in md_files:
        if 'CHANGELOG' not in filepath.name and 'VERSION' not in filepath.name:
            if 'V12' not in filepath.name and 'v12' not in filepath.name:
                issues = check_file_for_old_versions(filepath)
                if issues:
                    results[str(filepath)] = issues

    return results

def generate_report(results: Dict[str, List]) -> None:
    """Generate validation report"""

    print()
    print("="*80)
    print("VALIDATION RESULTS")
    print("="*80)
    print()

    if not results:
        print("[OK] NO ISSUES FOUND - All files consistent with v12.0")
        print()
        return

    print(f"[WARNING] FOUND {len(results)} FILES WITH POTENTIAL ISSUES")
    print()

    for filepath, issues in results.items():
        print(f"\n{filepath}:")
        print("-" * 80)
        for line_num, issue in issues[:10]:  # Limit to first 10 issues per file
            if line_num > 0:
                print(f"  Line {line_num}: {issue}")
            else:
                print(f"  {issue}")
        if len(issues) > 10:
            print(f"  ... and {len(issues) - 10} more issues")

    print()
    print("="*80)
    print(f"SUMMARY: {sum(len(v) for v in results.values())} total issues across {len(results)} files")
    print("="*80)

    # Write detailed report
    report_path = Path(__file__).parent / 'V12_VALIDATION_REPORT.txt'
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("V12.0 CONSISTENCY VALIDATION REPORT\n")
        f.write("="*80 + "\n\n")

        for filepath, issues in results.items():
            f.write(f"\n{filepath}:\n")
            f.write("-" * 80 + "\n")
            for line_num, issue in issues:
                if line_num > 0:
                    f.write(f"Line {line_num}: {issue}\n")
                else:
                    f.write(f"{issue}\n")

        f.write(f"\n\nSUMMARY: {sum(len(v) for v in results.values())} total issues\n")

    print(f"\nDetailed report written to: {report_path}")

if __name__ == '__main__':
    results = scan_directory()
    generate_report(results)
