"""
Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.

Dedicated To:
    My Wife: Elizabeth May Watts
    Our Messiah: Jesus Of Nazareth
"""

import os
import re
import json
from pathlib import Path

# Read valid paths
with open('H:/Github/PrincipiaMetaphysica/temp_valid_paths.txt', 'r', encoding='utf-8') as f:
    valid_paths = set(line.strip() for line in f)

# Read valid formula IDs
valid_formula_ids = {
    'attractor-potential', 'bekenstein-hawking', 'bottom-quark-mass', 'ckm-elements',
    'cp-phase-geometric', 'dark-energy-w0', 'dark-energy-wa', 'de-sitter-attractor',
    'dirac-pneuma', 'division-algebra', 'doublet-triplet', 'effective-dimension',
    'effective-euler', 'effective-torsion', 'effective-torsion-spinor', 'flux-quantization',
    'friedmann-constraint', 'generation-number', 'ghost-coefficient', 'gut-coupling',
    'gut-scale', 'gw-dispersion', 'gw-dispersion-alt', 'gw-dispersion-coeff',
    'hidden-variables', 'hierarchy-ratio', 'higgs-mass', 'higgs-potential',
    'higgs-quartic', 'higgs-vev', 'kappa-gut-coefficient', 'kk-graviton-mass',
    'kms-condition', 'master-action-26d', 'mirror-dm-ratio', 'mirror-temp-ratio',
    'neutrino-mass-21', 'neutrino-mass-31', 'pati-salam-chain', 'planck-mass-derivation',
    'pneuma-stress-energy', 'pneuma-vev', 'primordial-spinor-13d', 'proton-branching',
    'proton-lifetime', 'racetrack-superpotential', 'reduction-cascade', 'rg-running-couplings',
    'scalar-potential', 'seesaw-mechanism', 'so10-breaking', 'sp2r-constraints',
    'strong-coupling', 'tau-lepton-mass', 'tcs-topology', 'thermal-time',
    'theta23-maximal', 'tomita-takesaki', 'top-quark-mass', 'vacuum-minimization',
    'virasoro-anomaly', 'weak-mixing-angle', 'yukawa-instanton'
}

# Load theory_output.json to verify category+param combinations
with open('H:/Github/PrincipiaMetaphysica/theory_output.json', 'r', encoding='utf-8') as f:
    theory_data = json.load(f)

sections_dir = Path('H:/Github/PrincipiaMetaphysica/sections')
html_files = list(sections_dir.glob('*.html'))

total_bindings = 0
valid_bindings = 0
invalid_bindings = []

# Patterns to search for
pm_value_pattern = r'data-pm-value="([^"]+)"'
category_param_pattern = r'data-category="([^"]+)"[^>]*data-param="([^"]+)"'
formula_id_pattern = r'data-formula-id="([^"]+)"'

for html_file in sorted(html_files):
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
        lines = content.split('\n')

    # Check data-pm-value attributes
    for line_num, line in enumerate(lines, 1):
        # Check data-pm-value
        for match in re.finditer(pm_value_pattern, line):
            total_bindings += 1
            path = match.group(1)
            if path in valid_paths:
                valid_bindings += 1
            else:
                invalid_bindings.append({
                    'type': 'data-pm-value',
                    'file': html_file.name,
                    'line': line_num,
                    'value': path,
                    'reason': 'Path not found in theory_output.json'
                })

        # Check data-category + data-param combinations
        for match in re.finditer(category_param_pattern, line):
            total_bindings += 1
            category = match.group(1)
            param = match.group(2)

            # Check if category exists in theory_output.json
            if category in theory_data:
                # Check if param exists in that category
                if param in theory_data[category]:
                    valid_bindings += 1
                else:
                    invalid_bindings.append({
                        'type': 'data-category+data-param',
                        'file': html_file.name,
                        'line': line_num,
                        'value': f'{category}.{param}',
                        'reason': f'Parameter "{param}" not found in category "{category}"'
                    })
            else:
                invalid_bindings.append({
                    'type': 'data-category+data-param',
                    'file': html_file.name,
                    'line': line_num,
                    'value': f'{category}.{param}',
                    'reason': f'Category "{category}" not found in theory_output.json'
                })

        # Check data-formula-id attributes
        for match in re.finditer(formula_id_pattern, line):
            total_bindings += 1
            formula_id = match.group(1)
            if formula_id in valid_formula_ids:
                valid_bindings += 1
            else:
                invalid_bindings.append({
                    'type': 'data-formula-id',
                    'file': html_file.name,
                    'line': line_num,
                    'value': formula_id,
                    'reason': 'Formula ID not found in CoreFormulas'
                })

# Generate report
report = f"""# PM Binding Validation Report

Generated: 2025-12-25

## Summary

- **Total PM bindings found:** {total_bindings}
- **Valid bindings:** {valid_bindings}
- **Invalid/broken bindings:** {len(invalid_bindings)}
- **Success rate:** {(valid_bindings/total_bindings*100) if total_bindings > 0 else 0:.1f}%

## Files Scanned

"""

for html_file in sorted(html_files):
    report += f"- {html_file.name}\n"

report += f"\n## Binding Types Checked\n\n"
report += f"1. **data-pm-value** - Direct paths to theory_output.json values\n"
report += f"2. **data-category + data-param** - Category/parameter combinations\n"
report += f"3. **data-formula-id** - Formula IDs from CoreFormulas\n"

if invalid_bindings:
    report += f"\n## Invalid/Broken Bindings ({len(invalid_bindings)})\n\n"

    # Group by type
    by_type = {}
    for binding in invalid_bindings:
        btype = binding['type']
        if btype not in by_type:
            by_type[btype] = []
        by_type[btype].append(binding)

    for btype, bindings in sorted(by_type.items()):
        report += f"\n### {btype} ({len(bindings)} issues)\n\n"
        for binding in bindings:
            report += f"- **{binding['file']}:{binding['line']}**\n"
            report += f"  - Value: `{binding['value']}`\n"
            report += f"  - Reason: {binding['reason']}\n\n"
else:
    report += f"\n## Validation Results\n\n"
    report += f"✅ All PM bindings are valid!\n\n"

report += f"\n## Valid Path Examples\n\n"
report += f"Sample of valid paths from theory_output.json:\n\n"
sample_paths = sorted(list(valid_paths))[:20]
for path in sample_paths:
    report += f"- `{path}`\n"

report += f"\n## Valid Formula IDs\n\n"
report += f"All {len(valid_formula_ids)} formula IDs from CoreFormulas:\n\n"
for fid in sorted(valid_formula_ids):
    report += f"- `{fid}`\n"

# Write report
os.makedirs('H:/Github/PrincipiaMetaphysica/reports', exist_ok=True)
with open('H:/Github/PrincipiaMetaphysica/reports/PM_BINDING_VALIDATION.md', 'w', encoding='utf-8') as f:
    f.write(report)

print(f"Report generated successfully!")
print(f"Total bindings: {total_bindings}")
print(f"Valid: {valid_bindings}")
print(f"Invalid: {len(invalid_bindings)}")
