#!/usr/bin/env python3
"""
validate_equation_numbering.py - Validate equation numbering across PM website

This script:
1. Loads the centralized equation-registry.json
2. Scans all HTML files for equation references
3. Validates old numbering is replaced with new
4. Checks PM constant references are used
5. Generates a validation report

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.
"""

import json
import re
import sys
from pathlib import Path
from typing import Dict, List, Tuple
from dataclasses import dataclass, field
from collections import defaultdict


@dataclass
class EquationMatch:
    """A found equation reference in an HTML file."""
    file_path: str
    line_number: int
    equation_id: str
    found_number: str
    expected_number: str
    context: str
    is_valid: bool
    issue: str = ""


@dataclass
class ValidationReport:
    """Complete validation report."""
    total_equations: int = 0
    total_files_scanned: int = 0
    valid_references: int = 0
    invalid_references: int = 0
    missing_numbers: List[str] = field(default_factory=list)
    orphaned_numbers: List[str] = field(default_factory=list)
    issues: List[EquationMatch] = field(default_factory=list)
    file_coverage: Dict[str, List[str]] = field(default_factory=dict)


# Patterns to detect equation numbers in HTML
EQUATION_PATTERNS = [
    # Standard (X.Y) format
    r'\((\d+\.\d+[a-z]?)\)',
    # Eq. X.Y format
    r'[Ee]q\.?\s*(\d+\.\d+[a-z]?)',
    # Equation (X.Y) format
    r'[Ee]quation\s*\((\d+\.\d+[a-z]?)\)',
    # Label field in formula-registry.js: "(X.Y) Title"
    r'label:\s*["\']?\((\d+\.\d+[a-z]?)\)',
]

# Patterns for PM constant references (good - centralized)
PM_CONSTANT_PATTERNS = [
    r'PM\.\w+\.\w+',
    r'data-category=["\'](\w+)["\'].*?data-param=["\'](\w+)["\']',
    r'pm-value.*?data-param',
]


def load_equation_registry(registry_path: Path) -> Dict:
    """Load the centralized equation registry."""
    with open(registry_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def scan_html_file(file_path: Path, registry: Dict) -> List[EquationMatch]:
    """Scan an HTML file for equation references."""
    matches = []

    try:
        content = file_path.read_text(encoding='utf-8')
    except Exception as e:
        print(f"  Warning: Could not read {file_path}: {e}")
        return matches

    lines = content.split('\n')

    # Build lookup from equation number to ID
    number_to_id = {}
    for eq_id, eq_data in registry.get('equations', {}).items():
        num = eq_data.get('equationNumber', '')
        number_to_id[num] = eq_id

    for line_num, line in enumerate(lines, 1):
        for pattern in EQUATION_PATTERNS:
            for match in re.finditer(pattern, line, re.IGNORECASE):
                found_number = match.group(1)

                # Check if this number is in our registry
                if found_number in number_to_id:
                    eq_id = number_to_id[found_number]
                    expected = registry['equations'][eq_id].get('equationNumber', '')

                    matches.append(EquationMatch(
                        file_path=str(file_path),
                        line_number=line_num,
                        equation_id=eq_id,
                        found_number=found_number,
                        expected_number=expected,
                        context=line.strip()[:100],
                        is_valid=True
                    ))
                else:
                    # Found an equation number not in registry
                    matches.append(EquationMatch(
                        file_path=str(file_path),
                        line_number=line_num,
                        equation_id="UNKNOWN",
                        found_number=found_number,
                        expected_number="N/A",
                        context=line.strip()[:100],
                        is_valid=False,
                        issue=f"Equation number ({found_number}) not in registry"
                    ))

    return matches


def check_pm_constants(file_path: Path) -> int:
    """Count PM constant references in a file (good practice)."""
    try:
        content = file_path.read_text(encoding='utf-8')
    except:
        return 0

    count = 0
    for pattern in PM_CONSTANT_PATTERNS:
        count += len(re.findall(pattern, content))

    return count


def validate_all_files(project_root: Path, registry: Dict) -> ValidationReport:
    """Validate equation numbering across all HTML files."""
    report = ValidationReport()
    report.total_equations = len(registry.get('equations', {}))

    # Files to scan
    html_patterns = [
        'index.html',
        'principia-metaphysica-paper.html',
        'references.html',
        'beginners-guide.html',
        'philosophical-implications.html',
        'visualization-index.html',
        'sections/*.html',
        'foundations/*.html',
        'diagrams/*.html',
    ]

    all_files = []
    for pattern in html_patterns:
        if '*' in pattern:
            all_files.extend(project_root.glob(pattern))
        else:
            f = project_root / pattern
            if f.exists():
                all_files.append(f)

    report.total_files_scanned = len(all_files)
    found_equations = set()

    print(f"\nScanning {len(all_files)} HTML files...")

    for file_path in all_files:
        matches = scan_html_file(file_path, registry)
        pm_count = check_pm_constants(file_path)

        report.file_coverage[str(file_path.relative_to(project_root))] = []

        for match in matches:
            if match.is_valid:
                report.valid_references += 1
                found_equations.add(match.equation_id)
                report.file_coverage[str(file_path.relative_to(project_root))].append(
                    match.equation_id
                )
            else:
                report.invalid_references += 1
                report.issues.append(match)

        # Progress indicator
        if matches:
            print(f"  {file_path.name}: {len(matches)} equation refs, {pm_count} PM constants")

    # Check for missing equations (in registry but not found)
    all_equation_ids = set(registry.get('equations', {}).keys())
    report.missing_numbers = list(all_equation_ids - found_equations)

    return report


def generate_report(report: ValidationReport, output_path: Path):
    """Generate validation report."""
    lines = [
        "# Equation Numbering Validation Report",
        "",
        f"Generated: {__import__('datetime').datetime.now().isoformat()}",
        "",
        "## Summary",
        "",
        f"- **Total Equations in Registry:** {report.total_equations}",
        f"- **Files Scanned:** {report.total_files_scanned}",
        f"- **Valid References Found:** {report.valid_references}",
        f"- **Invalid References Found:** {report.invalid_references}",
        f"- **Equations Not Found in Files:** {len(report.missing_numbers)}",
        "",
    ]

    if report.invalid_references > 0:
        lines.extend([
            "## Issues Found",
            "",
            "| File | Line | Found | Issue |",
            "|------|------|-------|-------|",
        ])
        for issue in report.issues:
            lines.append(
                f"| {Path(issue.file_path).name} | {issue.line_number} | "
                f"({issue.found_number}) | {issue.issue} |"
            )
        lines.append("")

    if report.missing_numbers:
        lines.extend([
            "## Equations Not Found in HTML Files",
            "",
            "These equations are in the registry but weren't found in scanned files:",
            "",
        ])
        for eq_id in sorted(report.missing_numbers):
            lines.append(f"- `{eq_id}`")
        lines.append("")

    lines.extend([
        "## File Coverage",
        "",
        "| File | Equations Found |",
        "|------|-----------------|",
    ])
    for file_path, equations in sorted(report.file_coverage.items()):
        if equations:
            lines.append(f"| {file_path} | {', '.join(equations[:5])}{'...' if len(equations) > 5 else ''} |")

    lines.extend([
        "",
        "## Validation Status",
        "",
    ])

    if report.invalid_references == 0 and len(report.missing_numbers) == 0:
        lines.append("**PASS** - All equation numbers validated successfully!")
    elif report.invalid_references == 0:
        lines.append(f"**PARTIAL PASS** - No invalid references, but {len(report.missing_numbers)} equations not found in files.")
    else:
        lines.append(f"**FAIL** - Found {report.invalid_references} invalid references.")

    lines.extend([
        "",
        "---",
        "",
        "Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.",
    ])

    output_path.write_text('\n'.join(lines), encoding='utf-8')
    return '\n'.join(lines)


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(description='Validate equation numbering')
    parser.add_argument('--project-root', default='.', help='Project root directory')
    parser.add_argument('--registry', default='content-templates/equation-registry.json',
                        help='Path to equation registry JSON')
    parser.add_argument('--output', default='reports/equation-numbering-validation.md',
                        help='Output report path')
    parser.add_argument('--json-output', help='Optional JSON output path')

    args = parser.parse_args()

    project_root = Path(args.project_root).resolve()
    registry_path = project_root / args.registry
    output_path = project_root / args.output

    print("=" * 60)
    print("Equation Numbering Validation")
    print("=" * 60)

    if not registry_path.exists():
        print(f"Error: Registry not found: {registry_path}")
        sys.exit(1)

    print(f"\nLoading registry from: {registry_path}")
    registry = load_equation_registry(registry_path)
    print(f"Found {len(registry.get('equations', {}))} equations in registry")

    report = validate_all_files(project_root, registry)

    # Generate report
    output_path.parent.mkdir(parents=True, exist_ok=True)
    report_text = generate_report(report, output_path)
    print(f"\nReport written to: {output_path}")

    # Optional JSON output
    if args.json_output:
        json_path = project_root / args.json_output
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump({
                'total_equations': report.total_equations,
                'total_files_scanned': report.total_files_scanned,
                'valid_references': report.valid_references,
                'invalid_references': report.invalid_references,
                'missing_numbers': report.missing_numbers,
                'issues': [
                    {
                        'file': i.file_path,
                        'line': i.line_number,
                        'found': i.found_number,
                        'issue': i.issue
                    }
                    for i in report.issues
                ],
                'file_coverage': report.file_coverage
            }, f, indent=2)
        print(f"JSON report written to: {json_path}")

    print("\n" + "=" * 60)
    if report.invalid_references == 0:
        print("VALIDATION PASSED")
    else:
        print(f"VALIDATION FOUND {report.invalid_references} ISSUES")
    print("=" * 60)

    sys.exit(0 if report.invalid_references == 0 else 1)


if __name__ == '__main__':
    main()
