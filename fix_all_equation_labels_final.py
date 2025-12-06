#!/usr/bin/env python3
"""
Systematically fix all 39 equation labels using PM values.
Final version with proper duplicate handling
"""

import re
from pathlib import Path

def fix_equation_labels(file_path):
    """Fix all equation labels in the HTML file"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    changes_made = []

    # Define all replacements in the order they appear in the file
    # Format: (pattern, replacement, description, new_label)
    replacements = [
        # Section 2 - Planck derivation (10 equations: lines 3490-4344)
        (r'<span class="equation-label">\s*\(\s*<span class="pm-value"[^>]*data-param="ratio_to_bound"[^>]*>\s*</span>\s*\)\s*</span>',
         '<span class="equation-label">(2.10)</span>', 'ratio_to_bound', '(2.10)'),

        (r'<span class="equation-label">\s*\(\s*<span class="pm-value"[^>]*data-param="ratio_to_bound"[^>]*>\s*</span>\s*a\)\s*</span>',
         '<span class="equation-label">(2.11)</span>', 'ratio_to_bound a', '(2.11)'),

        (r'<span class="equation-label">\s*\(\s*<span class="pm-value"[^>]*data-param="ratio_to_bound"[^>]*>\s*</span>\s*b\)\s*</span>',
         '<span class="equation-label">(2.12)</span>', 'ratio_to_bound b', '(2.12)'),

        (r'<span class="equation-label">\s*\(\s*<span class="pm-value"[^>]*data-param="ratio_to_bound"[^>]*>\s*</span>\s*c\)\s*</span>',
         '<span class="equation-label">(2.13)</span>', 'ratio_to_bound c', '(2.13)'),

        (r'<span class="equation-label">\s*\(\s*<span class="pm-value"[^>]*data-param="ratio_to_bound"[^>]*>\s*</span>\s*\.1\)\s*</span>',
         '<span class="equation-label">(2.14)</span>', 'ratio_to_bound.1', '(2.14)'),

        (r'<span class="equation-label">\s*\(\s*<span class="pm-value"[^>]*data-param="ratio_to_bound"[^>]*>\s*</span>\s*\.2\)\s*</span>',
         '<span class="equation-label">(2.15)</span>', 'ratio_to_bound.2', '(2.15)'),

        (r'<span class="equation-label">\s*\(\s*<span class="pm-value"[^>]*data-param="ratio_to_bound"[^>]*>\s*</span>\s*\.3\)\s*</span>',
         '<span class="equation-label">(2.16)</span>', 'ratio_to_bound.3', '(2.16)'),

        (r'<span class="equation-label">\s*\(\s*<span class="pm-value"[^>]*data-param="ratio_to_bound"[^>]*>\s*</span>\s*\.3a\)\s*</span>',
         '<span class="equation-label">(2.17)</span>', 'ratio_to_bound.3a', '(2.17)'),

        (r'<span class="equation-label">\s*\(\s*<span class="pm-value"[^>]*data-param="ratio_to_bound"[^>]*>\s*</span>\s*\.4\)\s*</span>',
         '<span class="equation-label">(2.18)</span>', 'ratio_to_bound.4', '(2.18)'),

        (r'<span class="equation-label">\s*\(\s*<span class="pm-value"[^>]*data-param="ratio_to_bound"[^>]*>\s*</span>\s*\.4a\)\s*</span>',
         '<span class="equation-label">(2.19)</span>', 'ratio_to_bound.4a', '(2.19)'),

        # Section 3 - Geometry (6 equations: lines 4681-5062)
        (r'<span class="equation-label">\s*\(\s*<span class="pm-value"[^>]*data-param="functional_test_chi2_log"[^>]*>\s*</span>\s*a\)\s*</span>',
         '<span class="equation-label">(3.1)</span>', 'functional_test_chi2_log a', '(3.1)'),

        (r'<span class="equation-label">\s*\(\s*<span class="pm-value"[^>]*data-param="functional_test_chi2_log"[^>]*>\s*</span>\s*b\)\s*</span>',
         '<span class="equation-label">(3.2)</span>', 'functional_test_chi2_log b', '(3.2)'),

        # Two without suffix - apply in order
        (r'<span class="equation-label">\s*\(\s*<span class="pm-value"[^>]*data-param="functional_test_chi2_log"[^>]*>\s*</span>\s*\)\s*</span>',
         '<span class="equation-label">(3.3)</span>', 'functional_test_chi2_log [1st]', '(3.3)'),

        (r'<span class="equation-label">\s*\(\s*<span class="pm-value"[^>]*data-param="functional_test_chi2_log"[^>]*>\s*</span>\s*\)\s*</span>',
         '<span class="equation-label">(3.4)</span>', 'functional_test_chi2_log [2nd]', '(3.4)'),

        (r'<span class="equation-label">\s*\(\s*<span class="pm-value"[^>]*data-param="functional_test_chi2_log"[^>]*>\s*</span>\s*a\)\s*</span>',
         '<span class="equation-label">(3.5)</span>', 'functional_test_chi2_log a [2nd]', '(3.5)'),

        (r'<span class="equation-label">\s*\(\s*<span class="pm-value"[^>]*data-param="functional_test_chi2_log"[^>]*>\s*</span>\s*b\)\s*</span>',
         '<span class="equation-label">(3.6)</span>', 'functional_test_chi2_log b [2nd]', '(3.6)'),

        # Section 4 - Gauge (1 equation: line 5468)
        (r'<span class="equation-label">\s*\(\s*<span class="pm-value"[^>]*data-param="D_common"[^>]*>\s*</span>\s*\)\s*</span>',
         '<span class="equation-label">(4.1)</span>', 'D_common', '(4.1)'),

        # Section 5 - Thermal (11 equations: lines 5509-6200)
        (r'<span class="equation-label">\s*\(\s*<span class="pm-value"[^>]*data-param="significance"[^>]*>\s*</span>\s*\)\s*</span>',
         '<span class="equation-label">(5.1)</span>', 'significance [1st]', '(5.1)'),

        (r'<span class="equation-label">\s*\(\s*<span class="pm-value"[^>]*data-param="significance"[^>]*>\s*</span>\s*\)\s*</span>',
         '<span class="equation-label">(5.2)</span>', 'significance [2nd]', '(5.2)'),

        (r'<span class="equation-label">\s*\(\s*<span class="pm-value"[^>]*data-param="significance"[^>]*>\s*</span>\s*a\)\s*</span>',
         '<span class="equation-label">(5.3)</span>', 'significance a [1st]', '(5.3)'),

        (r'<span class="equation-label">\s*\(\s*<span class="pm-value"[^>]*data-param="significance"[^>]*>\s*</span>\s*b\)\s*</span>',
         '<span class="equation-label">(5.4)</span>', 'significance b [1st]', '(5.4)'),

        (r'<span class="equation-label">\s*\(\s*<span class="pm-value"[^>]*data-param="significance"[^>]*>\s*</span>\s*c\)\s*</span>',
         '<span class="equation-label">(5.5)</span>', 'significance c [1st]', '(5.5)'),

        (r'<span class="equation-label">\s*\(\s*<span class="pm-value"[^>]*data-param="significance"[^>]*>\s*</span>\s*a\)\s*</span>',
         '<span class="equation-label">(5.6)</span>', 'significance a [2nd]', '(5.6)'),

        (r'<span class="equation-label">\s*\(\s*<span class="pm-value"[^>]*data-param="significance"[^>]*>\s*</span>\s*b\)\s*</span>',
         '<span class="equation-label">(5.7)</span>', 'significance b [2nd]', '(5.7)'),

        (r'<span class="equation-label">\s*\(\s*<span class="pm-value"[^>]*data-param="significance"[^>]*>\s*</span>\s*c\)\s*</span>',
         '<span class="equation-label">(5.8)</span>', 'significance c [2nd]', '(5.8)'),

        (r'<span class="equation-label">\s*\(\s*<span class="pm-value"[^>]*data-param="significance"[^>]*>\s*</span>\s*d\)\s*</span>',
         '<span class="equation-label">(5.9)</span>', 'significance d', '(5.9)'),

        (r'<span class="equation-label">\s*\(\s*<span class="pm-value"[^>]*data-param="significance"[^>]*>\s*</span>\s*e\)\s*</span>',
         '<span class="equation-label">(5.10)</span>', 'significance e', '(5.10)'),

        (r'<span class="equation-label">\s*\(\s*<span class="pm-value"[^>]*data-param="significance"[^>]*>\s*</span>\s*f\)\s*</span>',
         '<span class="equation-label">(5.11)</span>', 'significance f', '(5.11)'),

        # Section 6 - Cosmology - D_effective (7 equations: lines 7516-8041)
        (r'<span class="equation-label">\s*\(\s*<span class="pm-value"[^>]*data-param="D_effective"[^>]*>\s*</span>\s*\)\s*</span>',
         '<span class="equation-label">(6.1)</span>', 'D_effective', '(6.1)'),

        (r'<span class="equation-label">\s*\(\s*<span class="pm-value"[^>]*data-param="D_effective"[^>]*>\s*</span>\s*a-new\)\s*</span>',
         '<span class="equation-label">(6.2)</span>', 'D_effective a-new', '(6.2)'),

        (r'<span class="equation-label">\s*\(\s*<span class="pm-value"[^>]*data-param="D_effective"[^>]*>\s*</span>\s*a\)\s*</span>',
         '<span class="equation-label">(6.3)</span>', 'D_effective a', '(6.3)'),

        (r'<span class="equation-label">\s*\(\s*<span class="pm-value"[^>]*data-param="D_effective"[^>]*>\s*</span>\s*b\)\s*</span>',
         '<span class="equation-label">(6.4)</span>', 'D_effective b', '(6.4)'),

        (r'<span class="equation-label">\s*\(\s*<span class="pm-value"[^>]*data-param="D_effective"[^>]*>\s*</span>\s*c\)\s*</span>',
         '<span class="equation-label">(6.5)</span>', 'D_effective c', '(6.5)'),

        (r'<span class="equation-label">\s*\(\s*<span class="pm-value"[^>]*data-param="D_effective"[^>]*>\s*</span>\s*d\)\s*</span>',
         '<span class="equation-label">(6.6)</span>', 'D_effective d', '(6.6)'),

        (r'<span class="equation-label">\s*\(\s*<span class="pm-value"[^>]*data-param="D_effective"[^>]*>\s*</span>\s*e\)\s*</span>',
         '<span class="equation-label">(6.7)</span>', 'D_effective e', '(6.7)'),

        # Section 6 - Cosmology - D_internal (4 equations: lines 8399-8758)
        (r'<span class="equation-label">\s*\(\s*<span class="pm-value"[^>]*data-param="D_internal"[^>]*>\s*</span>\s*\)\s*</span>',
         '<span class="equation-label">(6.8)</span>', 'D_internal', '(6.8)'),

        (r'<span class="equation-label">\s*\(\s*<span class="pm-value"[^>]*data-param="D_internal"[^>]*>\s*</span>\s*a\)\s*</span>',
         '<span class="equation-label">(6.9)</span>', 'D_internal a', '(6.9)'),

        (r'<span class="equation-label">\s*\(\s*<span class="pm-value"[^>]*data-param="D_internal"[^>]*>\s*</span>\s*b\)\s*</span>',
         '<span class="equation-label">(6.10)</span>', 'D_internal b', '(6.10)'),

        (r'<span class="equation-label">\s*\(\s*<span class="pm-value"[^>]*data-param="D_internal"[^>]*>\s*</span>\s*c\)\s*</span>',
         '<span class="equation-label">(6.11)</span>', 'D_internal c', '(6.11)'),
    ]

    # Apply replacements in order (one at a time to handle duplicates)
    for pattern, replacement, description, new_label in replacements:
        # Apply only the first match
        new_content = re.sub(pattern, replacement, content, count=1)

        if new_content != content:
            changes_made.append({
                'description': description,
                'new_label': new_label
            })
            print(f"[OK] {description} -> {new_label}")
            content = new_content
        else:
            print(f"[NOT FOUND] {description}")

    return content, changes_made

def main():
    file_path = Path('H:/Github/PrincipiaMetaphysica/principia-metaphysica-paper.html')

    print("=" * 80)
    print("EQUATION LABEL FIXING SCRIPT - FINAL VERSION")
    print("=" * 80)
    print(f"Processing: {file_path}")
    print(f"Target: Fix all 39 equation labels using PM values")
    print("=" * 80)
    print()

    new_content, changes = fix_equation_labels(file_path)

    print()
    print("=" * 80)
    print(f"SUMMARY: {len(changes)} / 39 equation labels fixed")
    print("=" * 80)

    if len(changes) == 39:
        print("\n*** ALL 39 EQUATION LABELS SUCCESSFULLY FIXED! ***")
    else:
        print(f"\nWARNING: Expected 39 fixes, got {len(changes)}")

    # Write changes
    print(f"\n[OK] Writing changes to {file_path}")
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)

    print("\nDone!")
    return len(changes) == 39

if __name__ == '__main__':
    success = main()
    exit(0 if success else 1)
