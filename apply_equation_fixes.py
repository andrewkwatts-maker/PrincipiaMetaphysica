#!/usr/bin/env python3
"""
Script to fix all equation labels in principia-metaphysica-paper.html
Replaces PM values with correct static equation numbers
"""

import re
from pathlib import Path

def fix_equation_labels(content):
    """Fix all equation labels by replacing PM values with static numbers"""

    # Define the mapping of what each equation should be numbered
    # Based on section analysis
    fixes = [
        # Section 2.2 remaining equations
        (3490, "(2.2j)"),   # ratio_to_bound
        (3613, "(2.2k)"),   # ratio_to_bounda
        (3689, "(2.2l)"),   # ratio_to_boundb
        (3749, "(2.2m)"),   # ratio_to_boundc

        # Section 2.3 equations
        (3878, "(2.3.1)"),  # ratio_to_bound.1
        (4056, "(2.3.2)"),  # ratio_to_bound.2
        (4147, "(2.3.3)"),  # ratio_to_bound.3
        (4180, "(2.3.3a)"), # ratio_to_bound.3a
        (4326, "(2.3.4)"),  # ratio_to_bound.4
        (4347, "(2.3.4a)"), # ratio_to_bound.4a

        # Section 3 equations (Geometric Structure)
        (4684, "(3.1a)"),   # functional_test_chi2_loga
        (4707, "(3.1b)"),   # functional_test_chi2_logb
        (4766, "(3.2)"),    # functional_test_chi2_log
        (4841, "(3.3)"),    # functional_test_chi2_log
        (5038, "(3.3a)"),   # functional_test_chi2_loga
        (5065, "(3.3b)"),   # functional_test_chi2_logb
        (5471, "(4.1)"),    # D_common

        # Section 4/5 equations (significance)
        (5512, "(4.2)"),    # significance
        (5606, "(4.3)"),    # significance
        (5792, "(4.3a)"),   # significancea
        (5825, "(4.3b)"),   # significanceb
        (5857, "(4.3c)"),   # significancec
        (6045, "(5.1a)"),   # significancea
        (6070, "(5.1b)"),   # significanceb
        (6114, "(5.1c)"),   # significancec
        (6137, "(5.1d)"),   # significanced
        (6178, "(5.1e)"),   # significancee
        (6203, "(5.1f)"),   # significancef

        # Section 5/6 equations (D_effective)
        (7519, "(5.2)"),    # D_effective
        (7552, "(5.2a)"),   # D_effectivea-new
        (7736, "(5.3a)"),   # D_effectivea
        (7763, "(5.3b)"),   # D_effectiveb
        (7798, "(5.3c)"),   # D_effectivec
        (7968, "(5.3d)"),   # D_effectived
        (8044, "(5.3e)"),   # D_effectivee

        # Section 6+ equations (D_internal)
        (8402, "(6.1)"),    # D_internal
        (8667, "(6.1a)"),   # D_internala
        (8733, "(6.1b)"),   # D_internalb
        (8761, "(6.1c)"),   # D_internalc
    ]

    lines = content.split('\n')

    # Pattern to match PM value equation labels
    pm_pattern = re.compile(
        r'<span class="equation-label">\s*\(\s*<span class="pm-value"[^>]*>\s*</span>\s*([^)]*)\)\s*</span>',
        re.DOTALL
    )

    # Apply fixes by line number
    for line_num, replacement in fixes:
        idx = line_num - 1  # Convert to 0-indexed
        if idx < len(lines):
            # Find and replace the PM value pattern on this line or nearby lines
            # Check a window around the line number
            for offset in range(-5, 6):
                check_idx = idx + offset
                if 0 <= check_idx < len(lines):
                    if pm_pattern.search(lines[check_idx]):
                        lines[check_idx] = pm_pattern.sub(
                            f'<span class="equation-label">\n     {replacement}\n    </span>',
                            lines[check_idx]
                        )
                        break

    return '\n'.join(lines)

def main():
    file_path = Path(r'H:\Github\PrincipiaMetaphysica\principia-metaphysica-paper.html')

    print("Reading file...")
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    print("Applying fixes...")
    fixed_content = fix_equation_labels(content)

    print("Writing fixed content...")
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(fixed_content)

    print("Done! Fixed all equation labels.")

if __name__ == '__main__':
    main()
