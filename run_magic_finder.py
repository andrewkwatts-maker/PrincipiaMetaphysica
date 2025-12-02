#!/usr/bin/env python3
"""
Wrapper to run magic number finder without Unicode console issues
"""

import sys
import os

# Set encoding
os.environ['PYTHONIOENCODING'] = 'utf-8'

# Import modules
import re
import json
from pathlib import Path
from collections import defaultdict

# Load theory data
with open('theory_output.json', 'r') as f:
    theory_data = json.load(f)

# Constants from theory data
CONSTANTS_TO_FIND = {
    # Dimensions
    '26': {'category': 'dimensions', 'name': 'D_bulk', 'js_path': 'PM.dimensions.D_bulk', 'value': theory_data['dimensions']['D_bulk']},
    '13': {'category': 'dimensions', 'name': 'D_after_sp2r', 'js_path': 'PM.dimensions.D_after_sp2r', 'value': theory_data['dimensions']['D_after_sp2r']},
    '6': {'category': 'dimensions', 'name': 'D_effective/D_observable_brane', 'js_path': 'PM.dimensions.D_observable_brane', 'value': theory_data['dimensions']['D_observable_brane']},
    '4': {'category': 'dimensions', 'name': 'D_common/D_shadow_brane', 'js_path': 'PM.dimensions.D_common', 'value': theory_data['dimensions']['D_common']},
    '144': {'category': 'topology', 'name': 'chi_eff', 'js_path': 'PM.topology.chi_eff', 'value': theory_data['topology']['chi_eff']},
    '24': {'category': 'topology', 'name': 'b3/nu', 'js_path': 'PM.topology.b3', 'value': theory_data['topology']['b3']},
    '3': {'category': 'topology', 'name': 'n_gen', 'js_path': 'PM.topology.n_gen', 'value': theory_data['topology']['n_gen']},
    '2.118e16': {'category': 'proton_decay', 'name': 'M_GUT', 'js_path': 'PM.proton_decay.M_GUT', 'value': theory_data['proton_decay']['M_GUT'], 'tolerance': 0.01},
    '2.118e+16': {'category': 'proton_decay', 'name': 'M_GUT', 'js_path': 'PM.proton_decay.M_GUT', 'value': theory_data['proton_decay']['M_GUT'], 'tolerance': 0.01},
    '1.8e16': {'category': 'proton_decay', 'name': 'M_GUT_OLD', 'js_path': 'PM.proton_decay.M_GUT', 'value': theory_data['proton_decay']['M_GUT'], 'outdated': True},
    '3.70e34': {'category': 'proton_decay', 'name': 'tau_p', 'js_path': 'PM.proton_decay.tau_p_median', 'value': theory_data['proton_decay']['tau_p_median'], 'tolerance': 0.05},
    '3.84e34': {'category': 'proton_decay', 'name': 'tau_p', 'js_path': 'PM.proton_decay.tau_p_median', 'value': theory_data['proton_decay']['tau_p_median'], 'tolerance': 0.05},
    '23.54': {'category': 'proton_decay', 'name': 'alpha_GUT_inv', 'js_path': 'PM.proton_decay.alpha_GUT_inv', 'value': theory_data['proton_decay']['alpha_GUT_inv'], 'tolerance': 0.01},
    '47.20': {'category': 'pmns', 'name': 'theta_23', 'js_path': 'PM.pmns_matrix.theta_23', 'value': theory_data['pmns_matrix']['theta_23'], 'tolerance': 0.1},
    '47.2': {'category': 'pmns', 'name': 'theta_23', 'js_path': 'PM.pmns_matrix.theta_23', 'value': theory_data['pmns_matrix']['theta_23'], 'tolerance': 0.1},
    '33.59': {'category': 'pmns', 'name': 'theta_12', 'js_path': 'PM.pmns_matrix.theta_12', 'value': theory_data['pmns_matrix']['theta_12'], 'tolerance': 0.1},
    '8.57': {'category': 'pmns', 'name': 'theta_13', 'js_path': 'PM.pmns_matrix.theta_13', 'value': theory_data['pmns_matrix']['theta_13'], 'tolerance': 0.1},
    '235': {'category': 'pmns', 'name': 'delta_cp', 'js_path': 'PM.pmns_matrix.delta_cp', 'value': theory_data['pmns_matrix']['delta_cp'], 'tolerance': 1.0},
    '-0.8528': {'category': 'dark_energy', 'name': 'w0', 'js_path': 'PM.dark_energy.w0_PM', 'value': theory_data['dark_energy']['w0_PM'], 'tolerance': 0.001},
    '-0.853': {'category': 'dark_energy', 'name': 'w0', 'js_path': 'PM.dark_energy.w0_PM', 'value': theory_data['dark_energy']['w0_PM'], 'tolerance': 0.001},
    '-0.95': {'category': 'dark_energy', 'name': 'wa_eff', 'js_path': 'PM.dark_energy.wa_PM_effective', 'value': theory_data['dark_energy']['wa_PM_effective'], 'tolerance': 0.01},
    '0.9557': {'category': 'shared_dims', 'name': 'alpha_4', 'js_path': 'PM.shared_dimensions.alpha_4', 'value': theory_data['shared_dimensions']['alpha_4'], 'tolerance': 0.001},
    '0.2224': {'category': 'shared_dims', 'name': 'alpha_5', 'js_path': 'PM.shared_dimensions.alpha_5', 'value': theory_data['shared_dimensions']['alpha_5'], 'tolerance': 0.001},
}

def find_magic_numbers_in_file(filepath):
    """Find all magic numbers in a single HTML file"""
    findings = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.read().split('\n')
    except:
        return findings

    for search_str, const_info in CONSTANTS_TO_FIND.items():
        pattern = re.escape(search_str).replace(r'\+', r'\+?')
        regex = re.compile(rf'\b{pattern}\b', re.IGNORECASE)
        for line_num, line in enumerate(lines, 1):
            if 'theory-constants.js' in line or 'PM.' in line:
                continue
            for match in regex.finditer(line):
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
    return findings

def scan_all_files():
    """Scan all HTML files"""
    html_files = list(Path('.').rglob('*.html'))
    excluded_dirs = {'node_modules', '.git', 'venv', '__pycache__'}
    html_files = [f for f in html_files if not any(ex in str(f) for ex in excluded_dirs)]

    all_findings = []
    file_counts = defaultdict(int)
    category_counts = defaultdict(int)

    for filepath in html_files:
        findings = find_magic_numbers_in_file(filepath)
        if findings:
            all_findings.extend(findings)
            file_counts[str(filepath)] = len(findings)
            for finding in findings:
                category_counts[finding['category']] += 1

    return all_findings, file_counts, category_counts

# Run scan
print("Scanning HTML files...")
all_findings, file_counts, category_counts = scan_all_files()

# Generate fix instructions JSON
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

# Save JSON
with open('magic_number_fix_instructions.json', 'w', encoding='utf-8') as f:
    json.dump(fix_instructions, f, indent=2)

# Print summary (ASCII only)
print(f"\nFound {len(all_findings)} magic numbers in {len(file_counts)} files")
print("\nTop files by magic number count:")
for filepath, count in sorted(file_counts.items(), key=lambda x: -x[1])[:10]:
    print(f"  {count:3d} - {Path(filepath).name}")

print(f"\nCategories:")
for category, count in sorted(category_counts.items(), key=lambda x: -x[1]):
    print(f"  {category:20s}: {count:4d}")

print(f"\nSaved: magic_number_fix_instructions.json")
print(f"Total files to fix: {len(by_file)}")
