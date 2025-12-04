#!/usr/bin/env python3
"""
Magic Number Validator
======================

Scans HTML files for hardcoded numerical values that should come from
simulation output instead. Helps maintain single source of truth.

Detects:
- Scientific notation (1.23e16, 10^16)
- Decimal numbers in specific contexts
- Order of magnitude values (OOM)
- Tension/sigma values
- Percentages

Copyright (c) 2025 Andrew Keith Watts. All rights reserved.
"""

import re
import json
from pathlib import Path
from typing import Dict, List, Tuple

# Load simulation output for comparison
def load_simulation_values():
    """Load all values from theory_output.json and theory-constants-enhanced.js"""
    values = {}

    # Load from theory_output.json
    try:
        with open('theory_output.json', 'r') as f:
            sim_data = json.load(f)

        # Flatten nested structure
        def flatten(d, prefix=''):
            for key, val in d.items():
                if isinstance(val, dict):
                    flatten(val, f"{prefix}{key}.")
                elif isinstance(val, (int, float)):
                    values[f"{prefix}{key}"] = val

        flatten(sim_data)
    except FileNotFoundError:
        print("Warning: theory_output.json not found")

    return values


# Pattern definitions for magic numbers
MAGIC_NUMBER_PATTERNS = [
    # Scientific notation in text (not in PM references)
    (r'(?<!data-param=")(?<!value">)(\d+\.?\d*)\s*×\s*10[¹²³⁴⁵⁶⁷⁸⁹⁰\^-]*(\d+)',
     'scientific_notation',
     'Scientific notation should use PM reference'),

    # Decimal values for specific parameters
    (r'(?<!data-param=")(?<!value">)(?:w₀|w0|w_0)\s*=\s*[−-]?(0\.\d+)',
     'w0_value',
     'w₀ value should use PM.dark_energy.w0_PM'),

    (r'(?<!data-param=")(?<!value">)(?:χ|chi)_?(?:eff)?\s*=\s*(\d+)',
     'chi_value',
     'χ_eff should use PM.topology.chi_eff'),

    (r'(?<!data-param=")(?<!value">)n_?gen\s*=\s*(\d+)',
     'ngen_value',
     'n_gen should use PM.topology.n_gen'),

    # Tension/sigma values
    (r'(?<!data-param=")(\d+\.?\d*)\s*σ',
     'sigma_value',
     'Tension values should use PM references'),

    (r'(?<!data-param=")(\d+\.?\d*)&sigma;',
     'sigma_html',
     'Tension values should use PM references'),

    # OOM values
    (r'(?<!data-param=")(?<!value">)(\d+\.?\d+)\s*OOM',
     'oom_value',
     'OOM uncertainty should use PM.proton_decay.uncertainty_oom'),

    # M_GUT values
    (r'(?<!data-param=")(?<!value">)M_?GUT.*?(\d+\.?\d+)\s*×\s*10\^?16',
     'mgut_value',
     'M_GUT should use PM.proton_decay.M_GUT or PM.xy_bosons.M_X'),

    # Percentages that might be predictions
    (r'(?<!data-param=")(?<!value">)(\d+\.?\d+)%',
     'percentage',
     'Check if percentage should use PM reference'),
]


def scan_file(filepath: Path, simulation_values: Dict) -> List[Tuple]:
    """
    Scan a single HTML file for magic numbers.
    Returns list of (line_num, pattern_type, matched_value, suggestion)
    """
    findings = []

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        return findings

    for line_num, line in enumerate(lines, 1):
        # Skip lines that are already using PM system
        if 'class="pm-value"' in line or 'data-category=' in line:
            continue

        # Skip comments
        if line.strip().startswith('<!--') or line.strip().startswith('//'):
            continue

        for pattern, pattern_type, suggestion in MAGIC_NUMBER_PATTERNS:
            matches = re.finditer(pattern, line)
            for match in matches:
                value = match.group(1) if match.groups() else match.group(0)
                findings.append((
                    line_num,
                    pattern_type,
                    value,
                    suggestion,
                    line.strip()[:100]  # First 100 chars of line
                ))

    return findings


def scan_all_files() -> Dict[str, List]:
    """Scan all HTML files in the project"""
    results = {}
    simulation_values = load_simulation_values()

    # Files to scan
    files_to_scan = [
        Path('index.html'),
        Path('principia-metaphysica-paper.html'),
        Path('beginners-guide.html'),
    ]

    # Add all section pages
    sections_dir = Path('sections')
    if sections_dir.exists():
        files_to_scan.extend(sections_dir.glob('*.html'))

    for filepath in files_to_scan:
        if not filepath.exists():
            continue

        findings = scan_file(filepath, simulation_values)
        if findings:
            results[str(filepath)] = findings

    return results


def print_report(results: Dict[str, List]):
    """Print formatted report of findings"""
    print("=" * 80)
    print("MAGIC NUMBER VALIDATION REPORT")
    print("=" * 80)
    print()

    total_issues = sum(len(findings) for findings in results.values())
    print(f"Total files scanned: {len(results)}")
    print(f"Total potential issues: {total_issues}")
    print()

    if not results:
        print("✅ No magic numbers found! All values use PM references.")
        return

    for filepath, findings in sorted(results.items()):
        print(f"\n{'='*80}")
        print(f"FILE: {filepath}")
        print(f"{'='*80}")
        print(f"Issues found: {len(findings)}")
        print()

        # Group by pattern type
        by_type = {}
        for finding in findings:
            pattern_type = finding[1]
            if pattern_type not in by_type:
                by_type[pattern_type] = []
            by_type[pattern_type].append(finding)

        for pattern_type, type_findings in sorted(by_type.items()):
            print(f"\n  [{pattern_type.upper()}] - {len(type_findings)} instances")
            for line_num, _, value, suggestion, line_preview in type_findings[:5]:  # Show first 5
                print(f"    Line {line_num}: {value}")
                print(f"      -> {suggestion}")
                print(f"      Context: {line_preview}")

            if len(type_findings) > 5:
                print(f"    ... and {len(type_findings) - 5} more")


def generate_fix_suggestions(results: Dict[str, List]) -> Dict:
    """Generate specific PM reference suggestions for each finding"""
    suggestions = {}

    # Mapping of value types to PM paths
    value_mappings = {
        'w0_value': 'PM.dark_energy.w0_PM',
        'chi_value': 'PM.topology.chi_eff',
        'ngen_value': 'PM.topology.n_gen',
        'oom_value': 'PM.proton_decay.uncertainty_oom',
        'mgut_value': 'PM.proton_decay.M_GUT',
        'sigma_value': 'PM.dark_energy.w0_sigma or PM.pmns_matrix.avg_sigma',
    }

    for filepath, findings in results.items():
        file_suggestions = []
        for line_num, pattern_type, value, suggestion, line_preview in findings:
            pm_path = value_mappings.get(pattern_type, 'PM.[category].[parameter]')
            file_suggestions.append({
                'line': line_num,
                'value': value,
                'pm_reference': pm_path,
                'html_replacement': f'<span class="pm-value" data-category="..." data-param="..." data-format="..."></span>'
            })

        if file_suggestions:
            suggestions[filepath] = file_suggestions

    return suggestions


if __name__ == "__main__":
    import sys
    import io
    # Force UTF-8 encoding for stdout
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

    print("Scanning for magic numbers...\n")
    results = scan_all_files()
    print_report(results)

    # Save detailed report to file
    with open('MAGIC_NUMBERS_REPORT.json', 'w', encoding='utf-8') as f:
        suggestions = generate_fix_suggestions(results)
        json.dump(suggestions, f, indent=2)

    print("\n" + "=" * 80)
    print(f"Detailed report saved to: MAGIC_NUMBERS_REPORT.json")
    print("=" * 80)
