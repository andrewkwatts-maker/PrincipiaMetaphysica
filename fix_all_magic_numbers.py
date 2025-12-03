#!/usr/bin/env python3
"""
Systematically replace ALL magic numbers across all HTML files with PM.* references.
Copyright (c) 2025 Andrew Keith Watts. All rights reserved.
"""

import re
import os

# Mapping of files and their script tag paths
FILES = {
    'principia-metaphysica-paper.html': {
        'css_path': 'css/pm-tooltip.css',
        'js_constants': 'theory-constants-enhanced.js',
        'js_tooltip': 'js/pm-tooltip-system.js',
    },
    'sections/cosmology.html': {
        'css_path': '../css/pm-tooltip.css',
        'js_constants': '../theory-constants-enhanced.js',
        'js_tooltip': '../js/pm-tooltip-system.js',
    },
    'sections/gauge-unification.html': {
        'css_path': '../css/pm-tooltip.css',
        'js_constants': '../theory-constants-enhanced.js',
        'js_tooltip': '../js/pm-tooltip-system.js',
    },
    'sections/fermion-sector.html': {
        'css_path': '../css/pm-tooltip.css',
        'js_constants': '../theory-constants-enhanced.js',
        'js_tooltip': '../js/pm-tooltip-system.js',
    },
    'sections/predictions.html': {
        'css_path': '../css/pm-tooltip.css',
        'js_constants': '../theory-constants-enhanced.js',
        'js_tooltip': '../js/pm-tooltip-system.js',
    },
}

def pm_span(category, param, format_type='display'):
    """Generate PM value span."""
    return f'<span class="pm-value" data-category="{category}" data-param="{param}" data-format="{format_type}"></span>'

# Common replacements for ALL files
COMMON_REPLACEMENTS = [
    # Proton decay - exact formatted values
    (r'3\.84\s*[×xX]\s*10<sup>34</sup>', pm_span('proton_decay', 'tau_p_median')),
    (r'3\.764\s*[×xX]\s*10<sup>34</sup>', pm_span('proton_decay', 'tau_p_median')),
    (r'2\.118\s*[×xX]\s*10<sup>16</sup>', pm_span('proton_decay', 'M_GUT')),

    # Uncertainty
    (r'0\.177(?!\d)', pm_span('proton_decay', 'uncertainty_oom', 'fixed:3')),

    # Alpha GUT
    (r'(?<=\s)23\.54(?!\d)', pm_span('gauge_unification', 'alpha_GUT_inv', 'fixed:2')),

    # Dark energy
    (r'-0\.8528(?!\d)', pm_span('dark_energy', 'w0_PM', 'fixed:4')),
    (r'-0\.846(?!\d)', pm_span('dark_energy', 'w0_PM', 'fixed:3')),

    # DESI w0 (with lookahead for context)
    (r'-0\.83(?=\s*[±])', pm_span('dark_energy', 'w0_DESI_central', 'fixed:2')),
    (r'0\.06(?=\s+at)', pm_span('dark_energy', 'w0_DESI_error', 'fixed:2')),

    # Dark energy sigma
    (r'0\.38\s*[σ]', pm_span('dark_energy', 'w0_sigma', 'fixed:2') + 'σ'),

    # PMNS angles
    (r'47\.20\s*°', pm_span('pmns_matrix', 'theta_23', 'fixed:2') + '°'),
    (r'33\.59\s*°', pm_span('pmns_matrix', 'theta_12', 'fixed:2') + '°'),
    (r'8\.57\s*°', pm_span('pmns_matrix', 'theta_13', 'fixed:2') + '°'),
    (r'235\.0\s*°', pm_span('pmns_matrix', 'delta_CP', 'fixed:1') + '°'),

    # PMNS sigma
    (r'0\.09\s*[σ]', pm_span('pmns_matrix', 'avg_sigma', 'fixed:2') + 'σ'),

    # Topology
    (r'(?<=\s)144(?=\s*[/])', pm_span('topology', 'chi_eff')),
    (r'χ<sub>eff</sub>\s*=\s*144', 'χ<sub>eff</sub> = ' + pm_span('topology', 'chi_eff')),
]

def add_script_tags(content, file_config):
    """Add script tags before </head> if not present."""
    css_tag = f'<link rel="stylesheet" href="{file_config["css_path"]}">'
    js_constants_tag = f'<script src="{file_config["js_constants"]}"></script>'
    js_tooltip_tag = f'<script src="{file_config["js_tooltip"]}"></script>'

    # Check if already present
    if 'pm-tooltip.css' in content and 'theory-constants-enhanced.js' in content:
        return content  # Already has new scripts

    # Remove old script if present
    content = re.sub(r'<script src="theory-constants\.js"></script>\s*', '', content)
    content = re.sub(r'<script src="\.\./theory-constants\.js"></script>\s*', '', content)

    # Add new scripts before </head>
    insertion = f'    {css_tag}\n    {js_constants_tag}\n    {js_tooltip_tag}\n'
    content = re.sub(r'(\s*)</head>', f'\n{insertion}\\1</head>', content)

    return content

def process_file(filepath, file_config):
    """Process a single HTML file."""
    print(f"\nProcessing: {filepath}")

    if not os.path.exists(filepath):
        print(f"  SKIP: File not found")
        return 0

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content

    # Add script tags
    content = add_script_tags(content, file_config)
    if content != original:
        print(f"  Added/updated script tags")

    # Apply replacements
    total_replacements = 0
    for pattern, replacement in COMMON_REPLACEMENTS:
        matches = len(re.findall(pattern, content))
        if matches > 0:
            content = re.sub(pattern, replacement, content)
            total_replacements += matches
            # Print without special chars to avoid Unicode errors
            print(f"  Replaced {matches} instances")

    # Write if changed
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  [OK] Total {total_replacements} replacements made")
        return total_replacements
    else:
        print(f"  No changes needed")
        return 0

def main():
    """Process all files."""
    base_dir = r'H:\Github\PrincipiaMetaphysica'

    grand_total = 0
    for filename, config in FILES.items():
        filepath = os.path.join(base_dir, filename)
        count = process_file(filepath, config)
        grand_total += count

    print(f"\n{'='*60}")
    print(f"GRAND TOTAL: {grand_total} magic numbers replaced")
    print(f"{'='*60}")

if __name__ == '__main__':
    main()
