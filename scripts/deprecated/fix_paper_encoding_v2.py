#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Iterative Paper Encoding and LaTeX Fix Script v2

This script identifies and fixes:
1. Broken Unicode characters (corrupted UTF-8 sequences)
2. Raw LaTeX that should be MathJax
3. Corrupted subscripts/superscripts

Run iteratively until no more fixes are found.

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.
"""

import re
import os
import sys
from pathlib import Path


def get_unicode_fixes():
    """
    Build the Unicode fix dictionary dynamically.
    This avoids encoding issues in the source file itself.
    """
    fixes = {}

    # Greek letters - double-encoded UTF-8 patterns
    # When UTF-8 is read as Latin-1 and then encoded again
    greek_map = [
        # (corrupted_hex, correct_char, name)
        ('c38ec2b1', '\u03b1', 'alpha'),
        ('c38ec2b2', '\u03b2', 'beta'),
        ('c38ec2b3', '\u03b3', 'gamma'),
        ('c38ec2b4', '\u03b4', 'delta'),
        ('c38ec2b5', '\u03b5', 'epsilon'),
        ('c38ec2b6', '\u03b6', 'zeta'),
        ('c38ec2b7', '\u03b7', 'eta'),
        ('c38ec2b8', '\u03b8', 'theta'),
        ('c38ec2b9', '\u03b9', 'iota'),
        ('c38ec2ba', '\u03ba', 'kappa'),
        ('c38ec2bb', '\u03bb', 'lambda'),
        ('c38ec2bc', '\u03bc', 'mu'),
        ('c38ec2bd', '\u03bd', 'nu'),
        ('c38ec2be', '\u03be', 'xi'),
        ('c38fc280', '\u03c0', 'pi'),
        ('c38fc281', '\u03c1', 'rho'),
        ('c38fc283', '\u03c3', 'sigma'),
        ('c38fc284', '\u03c4', 'tau'),
        ('c38fc285', '\u03c5', 'upsilon'),
        ('c38fc286', '\u03c6', 'phi'),
        ('c38fc287', '\u03c7', 'chi'),
        ('c38fc288', '\u03c8', 'psi'),
        ('c38fc289', '\u03c9', 'omega'),
    ]

    for hex_str, correct, name in greek_map:
        try:
            corrupted = bytes.fromhex(hex_str).decode('utf-8', errors='replace')
            fixes[corrupted] = correct
        except:
            pass

    # Common single-level mojibake patterns (UTF-8 read as Latin-1)
    # Format: bytes -> correct unicode
    mojibake_patterns = [
        # Greek lowercase
        (b'\xce\xb1', '\u03b1'),  # alpha
        (b'\xce\xb2', '\u03b2'),  # beta
        (b'\xce\xb3', '\u03b3'),  # gamma
        (b'\xce\xb4', '\u03b4'),  # delta
        (b'\xce\xb5', '\u03b5'),  # epsilon
        (b'\xce\xb8', '\u03b8'),  # theta
        (b'\xce\xba', '\u03ba'),  # kappa
        (b'\xce\xbb', '\u03bb'),  # lambda
        (b'\xce\xbc', '\u03bc'),  # mu
        (b'\xcf\x80', '\u03c0'),  # pi
        (b'\xcf\x83', '\u03c3'),  # sigma
        (b'\xcf\x84', '\u03c4'),  # tau
        (b'\xcf\x86', '\u03c6'),  # phi
        (b'\xcf\x87', '\u03c7'),  # chi
        (b'\xcf\x88', '\u03c8'),  # psi
        (b'\xcf\x89', '\u03c9'),  # omega

        # Mathematical symbols
        (b'\xe2\x89\xa4', '\u2264'),  # less or equal
        (b'\xe2\x89\xa5', '\u2265'),  # greater or equal
        (b'\xe2\x89\xa0', '\u2260'),  # not equal
        (b'\xe2\x89\x88', '\u2248'),  # approximately
        (b'\xc2\xb1', '\u00b1'),      # plus-minus
        (b'\xc3\x97', '\u00d7'),      # multiplication
        (b'\xe2\x88\x9a', '\u221a'),  # sqrt
        (b'\xe2\x88\x9e', '\u221e'),  # infinity
        (b'\xe2\x88\x82', '\u2202'),  # partial
        (b'\xe2\x88\x87', '\u2207'),  # nabla
        (b'\xe2\x88\x88', '\u2208'),  # element of
        (b'\xe2\x88\x91', '\u2211'),  # summation
        (b'\xe2\x88\xab', '\u222b'),  # integral

        # Angle brackets
        (b'\xe2\x9f\xa8', '\u27e8'),  # left angle
        (b'\xe2\x9f\xa9', '\u27e9'),  # right angle

        # Arrows
        (b'\xe2\x86\x90', '\u2190'),  # left arrow
        (b'\xe2\x86\x92', '\u2192'),  # right arrow
        (b'\xe2\x87\x90', '\u21d0'),  # double left arrow
        (b'\xe2\x87\x92', '\u21d2'),  # double right arrow

        # Subscripts
        (b'\xe2\x82\x80', '\u2080'),  # subscript 0
        (b'\xe2\x82\x81', '\u2081'),  # subscript 1
        (b'\xe2\x82\x82', '\u2082'),  # subscript 2
        (b'\xe2\x82\x83', '\u2083'),  # subscript 3
        (b'\xe2\x82\x84', '\u2084'),  # subscript 4

        # Superscripts
        (b'\xc2\xb2', '\u00b2'),      # superscript 2
        (b'\xc2\xb3', '\u00b3'),      # superscript 3
        (b'\xc2\xb9', '\u00b9'),      # superscript 1
        (b'\xc2\xb0', '\u00b0'),      # degree

        # Dashes and quotes
        (b'\xe2\x80\x94', '\u2014'),  # em dash
        (b'\xe2\x80\x93', '\u2013'),  # en dash
        (b'\xe2\x80\x98', '\u2018'),  # left single quote
        (b'\xe2\x80\x99', '\u2019'),  # right single quote
        (b'\xe2\x80\x9c', '\u201c'),  # left double quote
        (b'\xe2\x80\x9d', '\u201d'),  # right double quote
    ]

    # Add patterns where UTF-8 was read as Latin-1
    for utf8_bytes, correct in mojibake_patterns:
        try:
            # This is what happens when UTF-8 is read as Latin-1
            corrupted = utf8_bytes.decode('latin-1')
            fixes[corrupted] = correct
        except:
            pass

    return fixes


def find_and_report_issues(content, fixes):
    """Find all encoding issues and report them."""
    issues = []
    lines = content.split('\n')

    for i, line in enumerate(lines, 1):
        for corrupted in fixes.keys():
            if corrupted in line:
                issues.append({
                    'line': i,
                    'corrupted': repr(corrupted),
                    'correct': repr(fixes[corrupted]),
                })

    return issues


def fix_unicode(content, fixes):
    """Fix Unicode corruptions. Returns (fixed_content, fix_count)."""
    fix_count = 0

    for corrupted, correct in fixes.items():
        count = content.count(corrupted)
        if count > 0:
            content = content.replace(corrupted, correct)
            fix_count += count
            # Use ASCII-safe representation for Windows console
            corrupted_safe = corrupted.encode('unicode_escape').decode('ascii')[:30]
            correct_safe = correct.encode('unicode_escape').decode('ascii')
            print(f"  Fixed {count}x: {corrupted_safe} -> {correct_safe}")

    return content, fix_count


def fix_raw_latex(content):
    """
    Fix raw LaTeX that appears outside MathJax delimiters.
    Convert to Unicode equivalents.
    """
    fix_count = 0

    # Only fix LaTeX that is clearly outside MathJax context
    # These patterns look for LaTeX commands followed by whitespace or punctuation
    latex_fixes = [
        (r'\\leq\s', '\u2264 '),
        (r'\\geq\s', '\u2265 '),
        (r'\\times\s', '\u00d7 '),
        (r'\\pm\s', '\u00b1 '),
        (r'\\neq\s', '\u2260 '),
        (r'\\approx\s', '\u2248 '),
        (r'\\infty(?=[\s,.\)])', '\u221e'),
    ]

    for pattern, replacement in latex_fixes:
        matches = re.findall(pattern, content)
        if matches:
            content = re.sub(pattern, replacement, content)
            fix_count += len(matches)
            print(f"  Fixed {len(matches)}x LaTeX pattern: {pattern}")

    return content, fix_count


def fix_paper(file_path, max_iterations=10):
    """Iteratively fix the paper until no more issues are found."""

    print(f"\nOpening: {file_path}")
    print(f"File size: {os.path.getsize(file_path):,} bytes")

    # Build fix dictionary
    fixes = get_unicode_fixes()
    print(f"Loaded {len(fixes)} Unicode fix patterns")

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    original_content = content
    total_fixes = 0
    iteration = 0

    while iteration < max_iterations:
        iteration += 1
        print(f"\n{'='*70}")
        print(f"ITERATION {iteration}")
        print(f"{'='*70}")

        # Find issues
        issues = find_and_report_issues(content, fixes)
        print(f"\nFound {len(issues)} Unicode issues")

        if issues:
            for item in issues[:5]:
                print(f"  Line {item['line']}: {item['corrupted'][:40]}")
            if len(issues) > 5:
                print(f"  ... and {len(issues) - 5} more")

        if len(issues) == 0:
            print(f"\nSUCCESS: No more issues found!")
            break

        # Apply Unicode fixes
        print(f"\nApplying Unicode fixes...")
        content, unicode_fixes = fix_unicode(content, fixes)

        # Apply LaTeX fixes
        print(f"\nApplying LaTeX fixes...")
        content, latex_fixes = fix_raw_latex(content)

        fixes_this_iteration = unicode_fixes + latex_fixes
        total_fixes += fixes_this_iteration

        print(f"\n>>> Applied {fixes_this_iteration} fixes this iteration")

        if fixes_this_iteration == 0:
            print("\nWARNING: No fixes could be applied despite issues found.")
            print("May need to add new patterns to fix dictionary.")
            break

    # Save if changes made
    if content != original_content:
        backup_path = file_path + '.bak'
        with open(backup_path, 'w', encoding='utf-8') as f:
            f.write(original_content)
        print(f"\nBackup saved: {backup_path}")

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Fixed content saved: {file_path}")
    else:
        print("\nNo changes needed.")

    # Final check
    remaining = find_and_report_issues(content, fixes)

    return {
        'iterations': iteration,
        'total_fixes': total_fixes,
        'issues_remaining': len(remaining)
    }


def main():
    script_dir = Path(__file__).parent.parent
    paper_path = script_dir / 'principia-metaphysica-paper.html'

    if len(sys.argv) > 1:
        paper_path = Path(sys.argv[1])

    if not paper_path.exists():
        print(f"Error: File not found: {paper_path}")
        sys.exit(1)

    print("="*70)
    print("PRINCIPIA METAPHYSICA - PAPER ENCODING FIX SCRIPT v2")
    print("="*70)

    result = fix_paper(str(paper_path))

    print(f"\n{'='*70}")
    print("SUMMARY")
    print(f"{'='*70}")
    print(f"Iterations: {result['iterations']}")
    print(f"Total fixes: {result['total_fixes']}")
    print(f"Issues remaining: {result['issues_remaining']}")

    if result['issues_remaining'] > 0:
        print("\n*** Some issues remain ***")
        sys.exit(1)
    else:
        print("\n*** All issues resolved! ***")
        sys.exit(0)


if __name__ == '__main__':
    main()
