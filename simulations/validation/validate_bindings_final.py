#!/usr/bin/env python3
"""
PM Binding Validation Script
Validates data-pm-value, data-category+data-param, and data-formula-id attributes
in HTML files against theory_output.json and CoreFormulas.
"""

import os
import re
import json
from pathlib import Path
from collections import defaultdict

def extract_pm_value_bindings(content, filename):
    """Extract all data-pm-value attributes from HTML content."""
    bindings = []
    pattern = r'data-pm-value="([^"]+)"'

    for line_num, line in enumerate(content.split('\n'), 1):
        for match in re.finditer(pattern, line):
            bindings.append({
                'type': 'data-pm-value',
                'file': filename,
                'line': line_num,
                'value': match.group(1),
                'context': line.strip()[:100]
            })
    return bindings

def extract_category_param_bindings(content, filename):
    """Extract all data-category + data-param combinations."""
    bindings = []
    # Match both orderings: category before param, or param before category
    pattern1 = r'data-category="([^"]+)"[^>]*?data-param="([^"]+)"'
    pattern2 = r'data-param="([^"]+)"[^>]*?data-category="([^"]+)"'

    for line_num, line in enumerate(content.split('\n'), 1):
        # Try pattern 1: category before param
        for match in re.finditer(pattern1, line):
            bindings.append({
                'type': 'data-category+data-param',
                'file': filename,
                'line': line_num,
                'category': match.group(1),
                'param': match.group(2),
                'value': f"{match.group(1)}.{match.group(2)}",
                'context': line.strip()[:100]
            })

        # Try pattern 2: param before category (avoid duplicates)
        for match in re.finditer(pattern2, line):
            # Only add if we didn't already catch it with pattern1
            value = f"{match.group(2)}.{match.group(1)}"
            if not any(b['value'] == value and b['line'] == line_num for b in bindings):
                bindings.append({
                    'type': 'data-category+data-param',
                    'file': filename,
                    'line': line_num,
                    'category': match.group(2),
                    'param': match.group(1),
                    'value': value,
                    'context': line.strip()[:100]
                })

    return bindings

def extract_formula_id_bindings(content, filename):
    """Extract all data-formula-id attributes."""
    bindings = []
    pattern = r'data-formula-id="([^"]+)"'

    for line_num, line in enumerate(content.split('\n'), 1):
        for match in re.finditer(pattern, line):
            bindings.append({
                'type': 'data-formula-id',
                'file': filename,
                'line': line_num,
                'value': match.group(1),
                'context': line.strip()[:100]
            })
    return bindings

def validate_pm_value(path, valid_paths):
    """Check if a pm-value path exists."""
    return path in valid_paths

def validate_category_param(category, param, theory_data):
    """Check if category.param exists in theory_output.json."""
    if category not in theory_data:
        return False, f'Category "{category}" not found'
    if param not in theory_data[category]:
        return False, f'Parameter "{param}" not found in category "{category}"'
    return True, None

def validate_formula_id(formula_id, valid_formula_ids):
    """Check if formula ID exists in CoreFormulas."""
    return formula_id in valid_formula_ids

def main():
    print("PM Binding Validation Script")
    print("=" * 60)

    # Load valid paths from theory_output.json
    print("\n1. Loading valid paths from theory_output.json...")
    with open('H:/Github/PrincipiaMetaphysica/theory_output.json', 'r', encoding='utf-8') as f:
        theory_data = json.load(f)

    # Extract all valid paths recursively
    def get_all_paths(d, prefix=''):
        paths = set()
        if isinstance(d, dict):
            for k, v in d.items():
                new_prefix = f'{prefix}.{k}' if prefix else k
                if isinstance(v, dict):
                    paths.update(get_all_paths(v, new_prefix))
                else:
                    paths.add(new_prefix)
        return paths

    valid_paths = get_all_paths(theory_data)
    print(f"   Found {len(valid_paths)} valid paths")

    # Valid formula IDs from CoreFormulas
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
    print(f"   Found {len(valid_formula_ids)} valid formula IDs")

    # Scan HTML files
    print("\n2. Scanning HTML files in sections/...")
    sections_dir = Path('H:/Github/PrincipiaMetaphysica/sections')
    html_files = sorted(sections_dir.glob('*.html'))
    print(f"   Found {len(html_files)} HTML files")

    all_bindings = []
    valid_bindings = []
    invalid_bindings = []

    for html_file in html_files:
        print(f"   Scanning {html_file.name}...")
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Extract bindings
        pm_values = extract_pm_value_bindings(content, html_file.name)
        cat_params = extract_category_param_bindings(content, html_file.name)
        formula_ids = extract_formula_id_bindings(content, html_file.name)

        # Validate data-pm-value
        for binding in pm_values:
            all_bindings.append(binding)
            if validate_pm_value(binding['value'], valid_paths):
                valid_bindings.append(binding)
            else:
                binding['reason'] = 'Path not found in theory_output.json'
                invalid_bindings.append(binding)

        # Validate data-category + data-param
        for binding in cat_params:
            all_bindings.append(binding)
            is_valid, reason = validate_category_param(binding['category'], binding['param'], theory_data)
            if is_valid:
                valid_bindings.append(binding)
            else:
                binding['reason'] = reason
                invalid_bindings.append(binding)

        # Validate data-formula-id
        for binding in formula_ids:
            all_bindings.append(binding)
            if validate_formula_id(binding['value'], valid_formula_ids):
                valid_bindings.append(binding)
            else:
                binding['reason'] = 'Formula ID not found in CoreFormulas'
                invalid_bindings.append(binding)

    # Generate report
    print("\n3. Generating validation report...")

    total_count = len(all_bindings)
    valid_count = len(valid_bindings)
    invalid_count = len(invalid_bindings)
    success_rate = (valid_count / total_count * 100) if total_count > 0 else 0

    report = f"""# PM Binding Validation Report

Generated: 2025-12-25

## Summary

- **Total PM bindings found:** {total_count}
- **Valid bindings:** {valid_count}
- **Invalid/broken bindings:** {invalid_count}
- **Success rate:** {success_rate:.1f}%

## Binding Types

1. **data-pm-value** - Direct paths to theory_output.json values
2. **data-category + data-param** - Category/parameter combinations
3. **data-formula-id** - Formula IDs from CoreFormulas (not found in this scan)

## Files Scanned ({len(html_files)} files)

"""

    for html_file in html_files:
        report += f"- {html_file.name}\n"

    # Binding statistics by type
    type_stats = defaultdict(lambda: {'total': 0, 'valid': 0, 'invalid': 0})
    for binding in all_bindings:
        type_stats[binding['type']]['total'] += 1
    for binding in valid_bindings:
        type_stats[binding['type']]['valid'] += 1
    for binding in invalid_bindings:
        type_stats[binding['type']]['invalid'] += 1

    report += "\n## Statistics by Binding Type\n\n"
    for btype, stats in sorted(type_stats.items()):
        rate = (stats['valid'] / stats['total'] * 100) if stats['total'] > 0 else 0
        report += f"### {btype}\n\n"
        report += f"- Total: {stats['total']}\n"
        report += f"- Valid: {stats['valid']}\n"
        report += f"- Invalid: {stats['invalid']}\n"
        report += f"- Success rate: {rate:.1f}%\n\n"

    if invalid_bindings:
        report += f"\n## Invalid/Broken Bindings ({invalid_count} issues)\n\n"

        # Group by type
        by_type = defaultdict(list)
        for binding in invalid_bindings:
            by_type[binding['type']].append(binding)

        for btype, bindings in sorted(by_type.items()):
            report += f"\n### {btype} ({len(bindings)} issues)\n\n"
            for binding in sorted(bindings, key=lambda x: (x['file'], x['line'])):
                report += f"#### {binding['file']}:{binding['line']}\n\n"
                report += f"- **Value:** `{binding['value']}`\n"
                report += f"- **Reason:** {binding['reason']}\n"
                report += f"- **Context:** `{binding['context']}`\n\n"
    else:
        report += f"\n## Validation Results\n\n"
        report += f"✅ **All PM bindings are valid!**\n\n"

    # Sample of valid paths
    report += f"\n## Reference: Valid Paths (sample)\n\n"
    report += f"Sample of {min(30, len(valid_paths))} valid paths from theory_output.json:\n\n"
    for path in sorted(list(valid_paths))[:30]:
        report += f"- `{path}`\n"

    # All formula IDs
    report += f"\n## Reference: All Valid Formula IDs\n\n"
    report += f"Complete list of {len(valid_formula_ids)} formula IDs from CoreFormulas:\n\n"
    for fid in sorted(valid_formula_ids):
        report += f"- `{fid}`\n"

    # Write report
    os.makedirs('H:/Github/PrincipiaMetaphysica/reports', exist_ok=True)
    report_path = 'H:/Github/PrincipiaMetaphysica/reports/PM_BINDING_VALIDATION.md'
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report)

    print(f"\n✓ Report saved to: {report_path}")
    print(f"\nResults:")
    print(f"  Total bindings: {total_count}")
    print(f"  Valid: {valid_count}")
    print(f"  Invalid: {invalid_count}")
    print(f"  Success rate: {success_rate:.1f}%")

    if invalid_count > 0:
        print(f"\n⚠ Found {invalid_count} invalid bindings - see report for details")
    else:
        print(f"\n✓ All bindings are valid!")

if __name__ == '__main__':
    main()
