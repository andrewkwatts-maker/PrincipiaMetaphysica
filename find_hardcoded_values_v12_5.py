"""
Find Hardcoded Values That Should Use PM Constants (v12.5)

This script scans HTML files for hardcoded numerical values that should be
using PM constants from theory-constants-enhanced.js instead.

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.
"""

import re
import json
from pathlib import Path

# Load theory_output.json to get expected values
with open('theory_output.json', 'r', encoding='utf-8') as f:
    theory_data = json.load(f)

# Key v12.5 values that should NEVER be hardcoded
CRITICAL_VALUES = {
    # Re(T) - The v12.5 breakthrough value
    '7.086': 'Re(T) modulus (PM.higgs_mass.Re_T_modulus)',
    '1.833': 'OLD Re(T) value (WRONG - should be 7.086)',

    # Lambda values
    '0.0945': 'lambda_0 geometric (PM.higgs_mass.lambda_0)',
    '0.129': 'OLD lambda_0 phenomenological (WRONG - should be 0.0945)',

    # Higgs mass
    '125.10': 'Higgs mass GeV (PM.higgs_mass.m_h)',
    '414': 'OLD Higgs mass from wrong Re(T) (WRONG)',

    # Swampland
    '1.958': 'Swampland delta_phi (PM.v12_5_rigor_resolution.swampland.delta_phi)',
    '0.605': 'OLD swampland VIOLATION (WRONG - should be 1.958)',
    '0.816': 'Swampland bound (constant, OK to hardcode)',

    # PMNS angles (NuFIT 6.0)
    '45.0': 'theta_23 maximal mixing (PM.pmns_matrix.theta_23)',
    '47.2': 'OLD theta_23 NuFIT 5.2 (WRONG in theory - should be 45.0)',
    '33.6': 'theta_12 (PM.pmns_matrix.theta_12)',
    '8.57': 'theta_13 (PM.pmns_matrix.theta_13)',

    # Alpha parameters
    '0.576152': 'alpha_4 = alpha_5 perfect alignment (PM.v12_3_updates.alpha_4)',
    '0.0': 'alpha_4 - alpha_5 difference (should be calculated)',
    '0.7333': 'OLD alpha difference (WRONG - should be 0.0)',

    # Dark energy
    '-0.8528': 'w0 dark energy (PM.dark_energy.w0_PM)',
    '-0.853': 'w0 rounded (PM.dark_energy.w0_PM)',
    '0.38': 'DESI w0 sigma deviation (PM.dark_energy.w0_deviation_sigma)',

    # Topology
    '144': 'chi_eff (PM.topology.chi_eff)',
    '24': 'b3 associative cycles (PM.topology.b3)',
    '3': 'n_gen generations (PM.topology.n_gen)',

    # M_GUT
    '2.118e16': 'M_GUT (PM.proton_decay.M_GUT)',
    '2.118×10¹⁶': 'M_GUT formatted (PM.proton_decay.M_GUT)',
}

# Patterns to find numbers in HTML
NUMBER_PATTERNS = [
    r'\b(\d+\.?\d*)\s*(?:GeV|TeV|eV)\b',  # Numbers with energy units
    r'\b(\d+\.?\d*)\s*×\s*10[⁰¹²³⁴⁵⁶⁷⁸⁹]+',  # Scientific notation
    r'(?:Re\(T\)|lambda_0|λ₀|θ₂₃|α₄|α₅|w₀|χ_eff|M_GUT)\s*=\s*([0-9.]+)',  # Formula assignments
    r'>([0-9.]+)<',  # Numbers in tags
]

def scan_html_file(filepath):
    """Scan HTML file for hardcoded values"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        lines = content.split('\n')

    findings = []

    for line_num, line in enumerate(lines, 1):
        # Skip lines with PM constants or data- attributes (these are OK)
        if 'PM.' in line or 'data-category' in line or 'data-param' in line:
            continue

        # Skip comments and script tags
        if '<!--' in line or '<script' in line:
            continue

        # Check for critical hardcoded values
        for value, description in CRITICAL_VALUES.items():
            if value in line:
                # Check if it's in a problematic context (not in a comment or PM reference)
                context = line[max(0, line.find(value)-50):min(len(line), line.find(value)+50)]

                # Skip if it's already using PM constants
                if 'PM.' in context or 'data-param' in context:
                    continue

                findings.append({
                    'file': filepath.name,
                    'line': line_num,
                    'value': value,
                    'description': description,
                    'context': context.strip(),
                    'severity': 'CRITICAL' if 'WRONG' in description else 'WARNING'
                })

    return findings

def main():
    """Main function"""
    print("="*80)
    print("HARDCODED VALUE DETECTOR (v12.5)")
    print("="*80)
    print()
    print("Scanning HTML files for hardcoded values that should use PM constants...")
    print()

    # Scan all HTML files
    html_files = [
        Path('index.html'),
        Path('beginners-guide.html'),
        Path('principia-metaphysica-paper.html'),
        Path('philosophical-implications.html'),
        Path('references.html'),
    ]

    # Add section pages
    sections_dir = Path('sections')
    if sections_dir.exists():
        html_files.extend(sections_dir.glob('*.html'))

    # Add foundation pages
    foundations_dir = Path('foundations')
    if foundations_dir.exists():
        html_files.extend(foundations_dir.glob('*.html'))

    all_findings = []

    for filepath in sorted(html_files):
        if not filepath.exists():
            continue

        findings = scan_html_file(filepath)
        if findings:
            all_findings.extend(findings)

    # Report findings
    if not all_findings:
        print("✓ No hardcoded critical values found! All values appear to use PM constants.")
        return

    # Group by severity
    critical = [f for f in all_findings if f['severity'] == 'CRITICAL']
    warnings = [f for f in all_findings if f['severity'] == 'WARNING']

    if critical:
        print(f"CRITICAL ISSUES ({len(critical)} found):")
        print("These are WRONG values from v11.0-v12.4 that MUST be fixed:")
        print()
        for f in critical:
            print(f"  {f['file']}:{f['line']}")
            print(f"    Value: {f['value']}")
            print(f"    Issue: {f['description']}")
            print(f"    Context: ...{f['context']}...")
            print()

    if warnings:
        print(f"WARNINGS ({len(warnings)} found):")
        print("These values should probably use PM constants:")
        print()
        for f in warnings:
            print(f"  {f['file']}:{f['line']}")
            print(f"    Value: {f['value']}")
            print(f"    Description: {f['description']}")
            print()

    # Summary
    print("="*80)
    print(f"SUMMARY: {len(critical)} critical issues, {len(warnings)} warnings")
    print("="*80)

    # Save detailed report
    report_file = 'hardcoded_values_v12_5_report.json'
    with open(report_file, 'w', encoding='utf-8') as f:
        json.dump({
            'critical': critical,
            'warnings': warnings,
            'total': len(all_findings)
        }, f, indent=2)

    print(f"\nDetailed report saved to: {report_file}")

if __name__ == '__main__':
    main()
