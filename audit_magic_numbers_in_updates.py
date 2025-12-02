#!/usr/bin/env python3
"""
Audit Magic Numbers in Recently Updated HTML Files
==================================================

Scans the HTML files we just updated to find hard-coded values that should
be replaced with PM.* references from theory-constants.js.

Copyright (c) 2025 Andrew Keith Watts. All rights reserved.
"""

import re
from pathlib import Path
import json

# Load the theory constants to know what's available
with open('theory_output.json', 'r') as f:
    theory = json.load(f)

# Define patterns for numbers we should be using from PM
MAGIC_NUMBERS = {
    # Proton decay
    '2.118e16': 'PM.proton_decay.M_GUT',
    '2.118e+16': 'PM.proton_decay.M_GUT',
    '2.118×10¹⁶': 'PM.format.scientific(PM.proton_decay.M_GUT, 3)',
    '3.84e34': 'PM.proton_decay.tau_p_median',
    '3.84×10³⁴': 'PM.format.scientific(PM.proton_decay.tau_p_median, 2)',
    '3.764': 'PM.proton_decay.tau_p_median',
    '2.41e34': 'PM.proton_decay.tau_p_lower_68',
    '5.61e34': 'PM.proton_decay.tau_p_upper_68',
    '0.177': 'PM.proton_decay.tau_p_uncertainty_oom',
    '23.54': 'PM.proton_decay.alpha_GUT_inv',
    '0.09e16': 'PM.proton_decay.M_GUT_error',
    '0.0425': 'PM.proton_decay.alpha_GUT',

    # PMNS angles
    '47.20': 'PM.pmns_matrix.theta_23',
    '47.2': 'PM.pmns_matrix.theta_23',
    '33.59': 'PM.pmns_matrix.theta_12',
    '8.57': 'PM.pmns_matrix.theta_13',
    '235.0': 'PM.pmns_matrix.delta_cp',
    '235': 'PM.pmns_matrix.delta_cp',
    '0.09σ': 'PM.format.sigma(PM.pmns_matrix.average_sigma)',
    '0.00σ': 'PM.format.sigma(PM.pmns_matrix.theta_23_sigma)',
    '0.01σ': 'PM.format.sigma(PM.pmns_matrix.theta_13_sigma)',
    '0.24σ': 'PM.format.sigma(PM.pmns_matrix.theta_12_sigma)',
    '0.10σ': 'PM.format.sigma(PM.pmns_matrix.delta_cp_sigma)',

    # Dark energy
    '-0.8528': 'PM.dark_energy.w0_PM',
    '-0.853': 'PM.dark_energy.w0_PM',
    '-0.95': 'PM.dark_energy.wa_PM_effective',
    '0.38σ': 'PM.format.sigma(PM.dark_energy.w0_deviation_sigma)',
    '0.66σ': 'PM.format.sigma(PM.dark_energy.wa_deviation_sigma)',

    # DESI DR2
    '-0.83': 'PM.desi_dr2_data.w0',
    '0.06': 'PM.desi_dr2_data.w0_error',
    '-0.75': 'PM.desi_dr2_data.wa',
    '0.30': 'PM.desi_dr2_data.wa_error',
    '4.2σ': 'PM.desi_dr2_data.significance',

    # Shared dimensions
    '0.956': 'PM.shared_dimensions.alpha_4',
    '0.222': 'PM.shared_dimensions.alpha_5',
    '12.589': 'PM.shared_dimensions.d_eff',

    # KK spectrum (if we add it to config)
    '5.0±1.5': 'PM.v61_predictions.m_KK (need to add)',
    '6.2σ': 'PM.kk_spectrum.hl_lhc_significance (need to add)',
    '0.10±0.03': 'PM.kk_spectrum.sigma_diphoton (need to add)',

    # Tensions/deviations
    '6.0σ': 'Planck tension initial',
    '1.3σ': 'Planck tension residual',
}

FILES_TO_AUDIT = [
    'principia-metaphysica-paper.html',
    'sections/cosmology.html',
    'sections/gauge-unification.html',
    'sections/fermion-sector.html',
    'sections/predictions.html',
]

def find_magic_numbers_in_file(filepath):
    """Find magic numbers in a file"""
    findings = []

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except:
        return findings

    for line_num, line in enumerate(lines, 1):
        # Skip lines that already use PM.
        if 'PM.' in line or 'theory-constants.js' in line:
            continue

        # Check for each magic number
        for magic_num, replacement in MAGIC_NUMBERS.items():
            # Escape special characters for regex
            pattern = re.escape(magic_num)
            if re.search(pattern, line):
                context = line.strip()[:100]
                findings.append({
                    'file': filepath,
                    'line': line_num,
                    'magic_number': magic_num,
                    'replacement': replacement,
                    'context': context
                })

    return findings

def main():
    print("=" * 80)
    print("AUDITING MAGIC NUMBERS IN UPDATED HTML FILES")
    print("=" * 80)
    print()

    all_findings = []

    for filepath in FILES_TO_AUDIT:
        print(f"Scanning {filepath}...")
        findings = find_magic_numbers_in_file(filepath)
        if findings:
            all_findings.extend(findings)
            print(f"  Found {len(findings)} magic numbers")
        else:
            print(f"  Clean (no magic numbers found)")

    print()
    print("=" * 80)
    print(f"TOTAL MAGIC NUMBERS FOUND: {len(all_findings)}")
    print("=" * 80)
    print()

    # Group by file
    by_file = {}
    for finding in all_findings:
        filepath = finding['file']
        if filepath not in by_file:
            by_file[filepath] = []
        by_file[filepath].append(finding)

    # Print detailed report
    for filepath, findings in sorted(by_file.items()):
        print(f"\n{filepath}: {len(findings)} magic numbers")
        print("-" * 80)

        # Group by magic number
        by_magic = {}
        for f in findings:
            num = f['magic_number']
            if num not in by_magic:
                by_magic[num] = []
            by_magic[num].append(f['line'])

        for magic_num, lines in sorted(by_magic.items()):
            replacement = next(f['replacement'] for f in findings if f['magic_number'] == magic_num)
            print(f"  {magic_num}")
            print(f"    Lines: {', '.join(map(str, sorted(lines)))}")
            print(f"    Replace with: {replacement}")

    # Save detailed report
    with open('MAGIC_NUMBER_AUDIT_REPORT.txt', 'w', encoding='utf-8') as f:
        f.write("MAGIC NUMBER AUDIT REPORT\n")
        f.write("=" * 80 + "\n\n")
        f.write(f"Total magic numbers found: {len(all_findings)}\n")
        f.write(f"Files affected: {len(by_file)}\n\n")

        for filepath, findings in sorted(by_file.items()):
            f.write(f"\n{filepath}\n")
            f.write("-" * 80 + "\n")
            for finding in findings:
                f.write(f"Line {finding['line']}: {finding['magic_number']}\n")
                f.write(f"  Replace with: {finding['replacement']}\n")
                f.write(f"  Context: {finding['context']}\n\n")

    print()
    print("=" * 80)
    print("Report saved to: MAGIC_NUMBER_AUDIT_REPORT.txt")
    print("=" * 80)

    return len(all_findings)

if __name__ == '__main__':
    count = main()
    exit(0 if count == 0 else 1)
