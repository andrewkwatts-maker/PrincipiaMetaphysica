#!/usr/bin/env python3
"""
Magic Number Detector for Principia Metaphysica Website
=======================================================

Searches all HTML files for hard-coded numeric constants that should be
replaced with values from theory-constants.js (PM object).

Copyright (c) 2025 Andrew Keith Watts. All rights reserved.
"""

import re
import json
from pathlib import Path
from collections import defaultdict
import sys

# Load the theory constants to compare against
with open('theory_output.json', 'r') as f:
    theory_data = json.load(f)

# Define the constants we're looking for with their canonical values and JS paths
CONSTANTS_TO_FIND = {
    # Dimensions
    '26': {'category': 'dimensions', 'name': 'D_bulk', 'js_path': 'PM.dimensions.D_bulk', 'value': theory_data['dimensions']['D_bulk']},
    '13': {'category': 'dimensions', 'name': 'D_after_sp2r', 'js_path': 'PM.dimensions.D_after_sp2r', 'value': theory_data['dimensions']['D_after_sp2r']},
    '6': {'category': 'dimensions', 'name': 'D_effective/D_observable_brane', 'js_path': 'PM.dimensions.D_observable_brane', 'value': theory_data['dimensions']['D_observable_brane']},
    '4': {'category': 'dimensions', 'name': 'D_common/D_shadow_brane', 'js_path': 'PM.dimensions.D_common', 'value': theory_data['dimensions']['D_common']},

    # Topology
    '144': {'category': 'topology', 'name': 'chi_eff', 'js_path': 'PM.topology.chi_eff', 'value': theory_data['topology']['chi_eff']},
    '24': {'category': 'topology', 'name': 'b3/nu', 'js_path': 'PM.topology.b3', 'value': theory_data['topology']['b3']},
    '3': {'category': 'topology', 'name': 'n_gen', 'js_path': 'PM.topology.n_gen', 'value': theory_data['topology']['n_gen']},

    # Proton Decay
    '2.118e16': {'category': 'proton_decay', 'name': 'M_GUT', 'js_path': 'PM.proton_decay.M_GUT', 'value': theory_data['proton_decay']['M_GUT'], 'tolerance': 0.01},
    '2.118e+16': {'category': 'proton_decay', 'name': 'M_GUT', 'js_path': 'PM.proton_decay.M_GUT', 'value': theory_data['proton_decay']['M_GUT'], 'tolerance': 0.01},
    '1.8e16': {'category': 'proton_decay', 'name': 'M_GUT_OLD', 'js_path': 'PM.proton_decay.M_GUT', 'value': theory_data['proton_decay']['M_GUT'], 'outdated': True},
    '3.70e34': {'category': 'proton_decay', 'name': 'tau_p', 'js_path': 'PM.proton_decay.tau_p_median', 'value': theory_data['proton_decay']['tau_p_median'], 'tolerance': 0.05},
    '3.84e34': {'category': 'proton_decay', 'name': 'tau_p', 'js_path': 'PM.proton_decay.tau_p_median', 'value': theory_data['proton_decay']['tau_p_median'], 'tolerance': 0.05},
    '23.54': {'category': 'proton_decay', 'name': 'alpha_GUT_inv', 'js_path': 'PM.proton_decay.alpha_GUT_inv', 'value': theory_data['proton_decay']['alpha_GUT_inv'], 'tolerance': 0.01},

    # PMNS Matrix
    '47.20': {'category': 'pmns', 'name': 'theta_23', 'js_path': 'PM.pmns_matrix.theta_23', 'value': theory_data['pmns_matrix']['theta_23'], 'tolerance': 0.1},
    '47.2': {'category': 'pmns', 'name': 'theta_23', 'js_path': 'PM.pmns_matrix.theta_23', 'value': theory_data['pmns_matrix']['theta_23'], 'tolerance': 0.1},
    '33.59': {'category': 'pmns', 'name': 'theta_12', 'js_path': 'PM.pmns_matrix.theta_12', 'value': theory_data['pmns_matrix']['theta_12'], 'tolerance': 0.1},
    '8.57': {'category': 'pmns', 'name': 'theta_13', 'js_path': 'PM.pmns_matrix.theta_13', 'value': theory_data['pmns_matrix']['theta_13'], 'tolerance': 0.1},
    '235': {'category': 'pmns', 'name': 'delta_cp', 'js_path': 'PM.pmns_matrix.delta_cp', 'value': theory_data['pmns_matrix']['delta_cp'], 'tolerance': 1.0},

    # Dark Energy
    '-0.8528': {'category': 'dark_energy', 'name': 'w0', 'js_path': 'PM.dark_energy.w0_PM', 'value': theory_data['dark_energy']['w0_PM'], 'tolerance': 0.001},
    '-0.853': {'category': 'dark_energy', 'name': 'w0', 'js_path': 'PM.dark_energy.w0_PM', 'value': theory_data['dark_energy']['w0_PM'], 'tolerance': 0.001},
    '-0.95': {'category': 'dark_energy', 'name': 'wa_eff', 'js_path': 'PM.dark_energy.wa_PM_effective', 'value': theory_data['dark_energy']['wa_PM_effective'], 'tolerance': 0.01},

    # Shared Dimensions
    '0.9557': {'category': 'shared_dims', 'name': 'alpha_4', 'js_path': 'PM.shared_dimensions.alpha_4', 'value': theory_data['shared_dimensions']['alpha_4'], 'tolerance': 0.001},
    '0.2224': {'category': 'shared_dims', 'name': 'alpha_5', 'js_path': 'PM.shared_dimensions.alpha_5', 'value': theory_data['shared_dimensions']['alpha_5'], 'tolerance': 0.001},
}

# Additional patterns to detect (formula-based)
FORMULA_PATTERNS = [
    (r'M_\{GUT\}\s*[=~]\s*([0-9.]+)\s*×?\s*10\^?\{?16\}?', 'M_GUT'),
    (r'τ_p\s*[=~]\s*([0-9.]+)\s*×?\s*10\^?\{?34\}?', 'tau_p'),
    (r'\\tau_p\s*[=~]\s*([0-9.]+)\s*×?\s*10\^?\{?34\}?', 'tau_p'),
    (r'θ_\{23\}\s*[=~]\s*([0-9.]+)', 'theta_23'),
    (r'\\theta_\{23\}\s*[=~]\s*([0-9.]+)', 'theta_23'),
    (r'w_0\s*[=~]\s*([-.0-9]+)', 'w0'),
    (r'χ_\{eff\}\s*[=~]\s*([0-9]+)', 'chi_eff'),
    (r'\\chi_\{eff\}\s*[=~]\s*([0-9]+)', 'chi_eff'),
]

def normalize_number(num_str):
    """Convert various number formats to canonical form"""
    num_str = num_str.strip()

    # Handle scientific notation
    if 'e' in num_str.lower():
        try:
            val = float(num_str)
            # Normalize scientific notation
            if abs(val) >= 1e10:
                return f"{val:.3e}"
            return num_str
        except:
            pass

    # Handle regular numbers
    try:
        val = float(num_str)
        if abs(val) < 0.001 or abs(val) >= 1000:
            return f"{val:.4e}"
        return num_str
    except:
        return num_str

def find_magic_numbers_in_file(filepath):
    """Find all magic numbers in a single HTML file"""
    findings = []

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            lines = content.split('\n')
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        return findings

    # Search for known constants
    for search_str, const_info in CONSTANTS_TO_FIND.items():
        # Create regex pattern that matches the number in various contexts
        # Match as standalone number or in scientific notation
        pattern = re.escape(search_str).replace(r'\+', r'\+?')
        regex = re.compile(rf'\b{pattern}\b', re.IGNORECASE)

        for line_num, line in enumerate(lines, 1):
            # Skip if line contains 'theory-constants.js' or 'PM.' (already using JS constants)
            if 'theory-constants.js' in line or 'PM.' in line:
                continue

            matches = regex.finditer(line)
            for match in matches:
                # Get context (30 chars before and after)
                start = max(0, match.start() - 30)
                end = min(len(line), match.end() + 30)
                context = line[start:end].strip()

                findings.append({
                    'file': str(filepath),
                    'line': line_num,
                    'value': search_str,
                    'context': context,
                    'constant': const_info['name'],
                    'category': const_info['category'],
                    'js_path': const_info['js_path'],
                    'canonical_value': const_info['value'],
                    'outdated': const_info.get('outdated', False)
                })

    # Search for formula patterns
    for pattern, const_name in FORMULA_PATTERNS:
        regex = re.compile(pattern, re.IGNORECASE)
        for line_num, line in enumerate(lines, 1):
            if 'theory-constants.js' in line or 'PM.' in line:
                continue

            matches = regex.finditer(line)
            for match in matches:
                start = max(0, match.start() - 30)
                end = min(len(line), match.end() + 30)
                context = line[start:end].strip()

                findings.append({
                    'file': str(filepath),
                    'line': line_num,
                    'value': match.group(1) if match.groups() else match.group(0),
                    'context': context,
                    'constant': const_name,
                    'category': 'formula',
                    'js_path': f'(formula containing {const_name})',
                    'canonical_value': None,
                    'outdated': False
                })

    return findings

def scan_all_files():
    """Scan all HTML files in the project"""
    html_files = list(Path('.').rglob('*.html'))

    # Exclude certain directories
    excluded_dirs = {'node_modules', '.git', 'venv', '__pycache__'}
    html_files = [f for f in html_files if not any(ex in str(f) for ex in excluded_dirs)]

    all_findings = []
    file_counts = defaultdict(int)
    category_counts = defaultdict(int)

    print(f"Scanning {len(html_files)} HTML files for magic numbers...")
    print("=" * 80)

    for filepath in sorted(html_files):
        findings = find_magic_numbers_in_file(filepath)
        if findings:
            all_findings.extend(findings)
            file_counts[str(filepath)] = len(findings)
            for finding in findings:
                category_counts[finding['category']] += 1

    return all_findings, file_counts, category_counts

def generate_report(all_findings, file_counts, category_counts):
    """Generate a detailed report of all findings"""
    report = []

    report.append("=" * 80)
    report.append("MAGIC NUMBER DETECTION REPORT")
    report.append("=" * 80)
    report.append("")
    report.append(f"Total magic numbers found: {len(all_findings)}")
    report.append(f"Files affected: {len(file_counts)}")
    report.append("")

    # Summary by category
    report.append("FINDINGS BY CATEGORY:")
    report.append("-" * 80)
    for category, count in sorted(category_counts.items(), key=lambda x: -x[1]):
        report.append(f"  {category:20s}: {count:4d} occurrences")
    report.append("")

    # Summary by file
    report.append("FILES WITH MOST MAGIC NUMBERS:")
    report.append("-" * 80)
    for filepath, count in sorted(file_counts.items(), key=lambda x: -x[1])[:20]:
        report.append(f"  {count:4d} - {filepath}")
    report.append("")

    # Detailed findings by file
    report.append("DETAILED FINDINGS BY FILE:")
    report.append("=" * 80)

    # Group by file
    by_file = defaultdict(list)
    for finding in all_findings:
        by_file[finding['file']].append(finding)

    for filepath in sorted(by_file.keys()):
        findings = by_file[filepath]
        report.append("")
        report.append(f"File: {filepath}")
        report.append(f"Found {len(findings)} magic number(s)")
        report.append("-" * 80)

        for i, finding in enumerate(findings, 1):
            report.append(f"\n  [{i}] Line {finding['line']}: {finding['value']}")
            report.append(f"      Constant: {finding['constant']} ({finding['category']})")
            report.append(f"      Replace with: {finding['js_path']}")
            if finding['canonical_value'] is not None:
                report.append(f"      Canonical value: {finding['canonical_value']}")
            if finding['outdated']:
                report.append(f"      WARNING: OUTDATED VALUE - UPDATE REQUIRED")
            report.append(f"      Context: ...{finding['context']}...")

    report.append("")
    report.append("=" * 80)
    report.append("RECOMMENDATIONS:")
    report.append("=" * 80)
    report.append("")
    report.append("1. Add <script src='theory-constants.js'></script> to each HTML file header")
    report.append("2. Replace magic numbers with PM.category.constant references")
    report.append("3. For formulas, use PM.format.scientific() for display formatting")
    report.append("4. Prioritize fixing OUTDATED values first")
    report.append("5. Use agents/AI to automate the replacement process")
    report.append("")
    report.append("Example replacements:")
    report.append("  - '2.118e16' → PM.proton_decay.M_GUT")
    report.append("  - '47.2' → PM.pmns_matrix.theta_23")
    report.append("  - '-0.853' → PM.dark_energy.w0_PM")
    report.append("  - '144' → PM.topology.chi_eff")
    report.append("")

    return "\n".join(report)

def generate_fix_instructions():
    """Generate JSON file with fix instructions for agents"""

    all_findings, file_counts, _ = scan_all_files()

    # Group by file
    by_file = defaultdict(list)
    for finding in all_findings:
        by_file[finding['file']].append(finding)

    fix_instructions = {
        'meta': {
            'total_files': len(by_file),
            'total_findings': len(all_findings),
            'instructions': 'Replace magic numbers with theory-constants.js references'
        },
        'files': {}
    }

    for filepath, findings in by_file.items():
        fix_instructions['files'][filepath] = {
            'path': filepath,
            'count': len(findings),
            'findings': [
                {
                    'line': f['line'],
                    'old_value': f['value'],
                    'js_replacement': f['js_path'],
                    'canonical_value': f['canonical_value'],
                    'context': f['context'],
                    'category': f['category'],
                    'priority': 'HIGH' if f.get('outdated') else 'NORMAL'
                }
                for f in findings
            ]
        }

    return fix_instructions

if __name__ == '__main__':
    print("Principia Metaphysica - Magic Number Detector")
    print("=" * 80)
    print()

    # Scan all files
    all_findings, file_counts, category_counts = scan_all_files()

    # Generate and save report
    report = generate_report(all_findings, file_counts, category_counts)

    with open('MAGIC_NUMBERS_REPORT.txt', 'w', encoding='utf-8') as f:
        f.write(report)

    # Print report (handle Unicode for Windows console)
    try:
        print(report)
    except UnicodeEncodeError:
        # Strip Unicode characters for console output
        report_ascii = report.replace('⚠️', 'WARNING:').replace('→', '->').replace('χ', 'chi').replace('θ', 'theta').replace('τ', 'tau')
        print(report_ascii)

    # Generate fix instructions for agents
    fix_instructions = generate_fix_instructions()

    with open('magic_number_fix_instructions.json', 'w', encoding='utf-8') as f:
        json.dump(fix_instructions, f, indent=2)

    print("\n" + "=" * 80)
    print(f"Reports saved:")
    print(f"  - MAGIC_NUMBERS_REPORT.txt (human-readable)")
    print(f"  - magic_number_fix_instructions.json (for agents/automation)")
    print("=" * 80)

    sys.exit(0 if len(all_findings) == 0 else 1)
