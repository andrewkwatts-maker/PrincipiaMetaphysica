#!/usr/bin/env python3
"""
Replace magic numbers in principia-metaphysica-paper.html with PM.* references.
"""

import re
import sys

# Define replacements - CRITICAL: Order matters for some patterns
REPLACEMENTS = [
    # Proton decay values
    (r'3\.84\s*×\s*10<sup>34</sup>', '<span class="pm-value" data-category="proton_decay" data-param="tau_p_median" data-format="display"></span>'),
    (r'3\.84×10<sup>34</sup>', '<span class="pm-value" data-category="proton_decay" data-param="tau_p_median" data-format="display"></span>'),
    (r'3\.764e34', '<span class="pm-value" data-category="proton_decay" data-param="tau_p_median" data-format="display"></span>'),

    # Proton decay confidence intervals - need to keep as text for now
    (r'\[2\.48,\s*5\.51\]', '[2.48, 5.51]'),  # normalize spacing

    # Proton decay uncertainty
    (r'0\.177(?!\d)', '<span class="pm-value" data-category="proton_decay" data-param="uncertainty_oom" data-format="fixed:3"></span>'),

    # M_GUT
    (r'2\.118\s*×\s*10<sup>16</sup>', '<span class="pm-value" data-category="proton_decay" data-param="M_GUT" data-format="display"></span>'),
    (r'2\.118×10<sup>16</sup>', '<span class="pm-value" data-category="proton_decay" data-param="M_GUT" data-format="display"></span>'),

    # Dark energy w0
    (r'-0\.8528(?!\d)', '<span class="pm-value" data-category="dark_energy" data-param="w0_PM" data-format="fixed:4"></span>'),
    (r'-0\.846(?!\d)', '<span class="pm-value" data-category="dark_energy" data-param="w0_PM" data-format="fixed:3"></span>'),

    # DESI w0
    (r'-0\.83(?=\s*±)', '<span class="pm-value" data-category="dark_energy" data-param="w0_DESI_central" data-format="fixed:2"></span>'),
    (r'0\.06(?=\s+at\s+)', '<span class="pm-value" data-category="dark_energy" data-param="w0_DESI_error" data-format="fixed:2"></span>'),

    # Dark energy agreement
    (r'0\.38σ', '<span class="pm-value" data-category="dark_energy" data-param="w0_sigma" data-format="fixed:2"></span>σ'),

    # PMNS angles - be careful with context
    (r'θ<sub>23</sub>\s*=\s*47\.20°', 'θ<sub>23</sub> = <span class="pm-value" data-category="pmns_matrix" data-param="theta_23" data-format="fixed:2"></span>°'),
    (r'47\.20°(?!\s*±)', '<span class="pm-value" data-category="pmns_matrix" data-param="theta_23" data-format="fixed:2"></span>°'),
    (r'47\.20(?=\s*<)', '<span class="pm-value" data-category="pmns_matrix" data-param="theta_23" data-format="fixed:2"></span>'),

    (r'θ<sub>12</sub>\s*=\s*33\.59°', 'θ<sub>12</sub> = <span class="pm-value" data-category="pmns_matrix" data-param="theta_12" data-format="fixed:2"></span>°'),
    (r'33\.59°', '<span class="pm-value" data-category="pmns_matrix" data-param="theta_12" data-format="fixed:2"></span>°'),

    (r'θ<sub>13</sub>\s*=\s*8\.57°', 'θ<sub>13</sub> = <span class="pm-value" data-category="pmns_matrix" data-param="theta_13" data-format="fixed:2"></span>°'),
    (r'8\.57°', '<span class="pm-value" data-category="pmns_matrix" data-param="theta_13" data-format="fixed:2"></span>°'),

    (r'δ<sub>CP</sub>\s*=\s*235\.0°', 'δ<sub>CP</sub> = <span class="pm-value" data-category="pmns_matrix" data-param="delta_CP" data-format="fixed:1"></span>°'),
    (r'235\.0°', '<span class="pm-value" data-category="pmns_matrix" data-param="delta_CP" data-format="fixed:1"></span>°'),

    # PMNS average sigma
    (r'0\.09σ', '<span class="pm-value" data-category="pmns_matrix" data-param="avg_sigma" data-format="fixed:2"></span>σ'),

    # Alpha GUT inverse
    (r'23\.54(?!\d)', '<span class="pm-value" data-category="gauge_unification" data-param="alpha_GUT_inv" data-format="fixed:2"></span>'),

    # Topology
    (r'χ<sub>eff</sub>\s*=\s*144', 'χ<sub>eff</sub> = <span class="pm-value" data-category="topology" data-param="chi_eff" data-format="display"></span>'),
    (r'(?<![\d\.])144(?!\d)(?=\s*[/→])', '<span class="pm-value" data-category="topology" data-param="chi_eff" data-format="display"></span>'),

    # Generations
    (r'(?<![>\d])3(?!\d)(?=\s+(?:fermion\s+)?generations)', '<span class="pm-value" data-category="topology" data-param="n_gen" data-format="display"></span>'),
]

def replace_magic_numbers(filepath):
    """Replace magic numbers in HTML file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original_content = content
    replacements_made = []

    for pattern, replacement in REPLACEMENTS:
        matches = list(re.finditer(pattern, content))
        if matches:
            print(f"Found {len(matches)} matches for: {pattern}")
            replacements_made.append((pattern, len(matches)))
            content = re.sub(pattern, replacement, content)

    # Write back
    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"\n[OK] Replaced {len(replacements_made)} patterns in {filepath}")
        print(f"Total replacements: {sum(count for _, count in replacements_made)}")
        return True
    else:
        print(f"No changes made to {filepath}")
        return False

if __name__ == '__main__':
    filepath = r'H:\Github\PrincipiaMetaphysica\principia-metaphysica-paper.html'
    replace_magic_numbers(filepath)
