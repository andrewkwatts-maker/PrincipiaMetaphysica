#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Iterative Paper Encoding and LaTeX Fix Script

This script identifies and fixes:
1. Broken Unicode characters (corrupted UTF-8 sequences)
2. Raw LaTeX that should be MathJax
3. Corrupted subscripts/superscripts
4. Broken HTML entities

Run iteratively until no more fixes are found.

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.
"""

import re
import os
import sys
from pathlib import Path

# Unicode replacement map for corrupted characters
# These are UTF-8 bytes interpreted as Latin-1, creating mojibake
# Format: corrupted_sequence -> correct_unicode
UNICODE_FIXES = {
    # Greek letters - UTF-8 bytes read as Latin-1
    # Pattern: 0xCE 0xXX or 0xCF 0xXX for Greek
    b'\xc3\x8e\xc2\xb1'.decode('latin-1'): '\u03b1',  # alpha
    b'\xc3\x8e\xc2\xb2'.decode('latin-1'): '\u03b2',  # beta
    b'\xc3\x8e\xc2\xb3'.decode('latin-1'): '\u03b3',  # gamma
    b'\xc3\x8e\xc2\xb4'.decode('latin-1'): '\u03b4',  # delta
    b'\xc3\x8e\xc2\xb5'.decode('latin-1'): '\u03b5',  # epsilon
    b'\xc3\x8e\xc2\xb8'.decode('latin-1'): '\u03b8',  # theta
    b'\xc3\x8e\xc2\xba'.decode('latin-1'): '\u03ba',  # kappa
    b'\xc3\x8e\xc2\xbb'.decode('latin-1'): '\u03bb',  # lambda
    b'\xc3\x8e\xc2\xbc'.decode('latin-1'): '\u03bc',  # mu
    b'\xc3\x8f\xc2\x80'.decode('latin-1'): '\u03c0',  # pi
    b'\xc3\x8f\xc2\x83'.decode('latin-1'): '\u03c3',  # sigma
    b'\xc3\x8f\xc2\x84'.decode('latin-1'): '\u03c4',  # tau
    b'\xc3\x8f\xc2\x86'.decode('latin-1'): '\u03c6',  # phi
    b'\xc3\x8f\xc2\x87'.decode('latin-1'): '\u03c7',  # chi
    b'\xc3\x8f\xc2\x88'.decode('latin-1'): '\u03c8',  # psi
    b'\xc3\x8f\xc2\x89'.decode('latin-1'): '\u03c9',  # omega

    # Common corrupted patterns (direct string matches)
    # These are what actually appear in the corrupted HTML
    'Î±': '\u03b1',  # alpha
    'Î²': '\u03b2',  # beta
    'Î³': '\u03b3',  # gamma
    'Î´': '\u03b4',  # delta
    'Îµ': '\u03b5',  # epsilon
    'Î¸': '\u03b8',  # theta
    'Îº': '\u03ba',  # kappa
    'Î»': '\u03bb',  # lambda
    'Î¼': '\u03bc',  # mu
    'Ï€': '\u03c0',  # pi
    'Ïƒ': '\u03c3',  # sigma
    'Ï„': '\u03c4',  # tau
    'Ï†': '\u03c6',  # phi
    'Ï‡': '\u03c7',  # chi
    'Ïˆ': '\u03c8',  # psi
    'Ï‰': '\u03c9',  # omega

    # Angle brackets - very common corruption
    'âŸ¨': '\u27e8',  # left angle bracket ⟨
    'âŸ©': '\u27e9',  # right angle bracket ⟩

    # Mathematical symbols
    'â‰¤': '\u2264',  # less than or equal ≤
    'â‰¥': '\u2265',  # greater than or equal ≥
    'â‰ ': '\u2260',  # not equal ≠
    'â‰ˆ': '\u2248',  # approximately ≈
    'Â±': '\u00b1',   # plus-minus ±
    'Ã—': '\u00d7',   # multiplication ×
    'âˆš': '\u221a',  # square root √
    'âˆž': '\u221e',  # infinity ∞
    'âˆ‚': '\u2202',  # partial derivative ∂
    'âˆ‡': '\u2207',  # nabla ∇
    'âˆˆ': '\u2208',  # element of ∈
    'âˆ'': '\u2211',  # summation Σ
    'âˆ«': '\u222b',  # integral ∫

    # Arrows
    'â†'': '\u2192',  # right arrow →
    'â†'': '\u2191',  # up arrow ↑
    'â†"': '\u2193',  # down arrow ↓
    'â‡'': '\u21d2',  # double right arrow ⇒

    # Subscripts
    'â‚€': '\u2080',  # subscript 0
    'â‚': '\u2081',   # subscript 1 (partial match)
    'â‚‚': '\u2082',  # subscript 2
    'â‚ƒ': '\u2083',  # subscript 3
    'â‚„': '\u2084',  # subscript 4

    # Superscripts
    'Â²': '\u00b2',   # superscript 2
    'Â³': '\u00b3',   # superscript 3
    'Â¹': '\u00b9',   # superscript 1

    # Degree and other symbols
    'Â°': '\u00b0',   # degree °

    # Quotes and dashes
    'â€"': '\u2014',  # em dash —
    'â€˜': '\u2018',  # left single quote '
    'â€™': '\u2019',  # right single quote '
    'â€œ': '\u201c',  # left double quote "
    'â€': '\u201d',   # right double quote "

    # G2 specific
    'Gâ‚‚': 'G\u2082',  # G₂
}

# LaTeX patterns that indicate raw LaTeX not inside MathJax delimiters
LATEX_ISSUE_PATTERNS = [
    # These patterns indicate LaTeX that should be wrapped in \(...\) or $$...$$
    (r'(?<!\$|\\\(|\\\[)\\theta_\{([^}]+)\}(?!\$|\\\)|\\\])', r'\u03b8_{\1}'),
    (r'(?<!\$|\\\(|\\\[)\\alpha_(\d)(?!\$|\\\)|\\\])', r'\u03b1\1'),
    (r'(?<!\$|\\\(|\\\[)\\chi_\{eff\}(?!\$|\\\)|\\\])', '\u03c7_eff'),
    (r'(?<!\$|\\\(|\\\[)\\delta_\{CP\}(?!\$|\\\)|\\\])', '\u03b4_CP'),
    (r'(?<!\$|\\\(|\\\[)\\leq(?![a-z])(?!\$|\\\)|\\\])', '\u2264'),
    (r'(?<!\$|\\\(|\\\[)\\geq(?![a-z])(?!\$|\\\)|\\\])', '\u2265'),
    (r'(?<!\$|\\\(|\\\[)\\times(?![a-z])(?!\$|\\\)|\\\])', '\u00d7'),
    (r'(?<!\$|\\\(|\\\[)\\pm(?![a-z])(?!\$|\\\)|\\\])', '\u00b1'),
]


def find_unicode_issues(content):
    """Find all Unicode encoding issues."""
    issues = []
    lines = content.split('\n')

    for i, line in enumerate(lines, 1):
        for corrupted in UNICODE_FIXES.keys():
            if corrupted in line:
                issues.append({
                    'line': i,
                    'corrupted': repr(corrupted),
                    'correct': repr(UNICODE_FIXES[corrupted]),
                    'context': line[:100] if len(line) > 100 else line
                })

    return issues


def find_latex_issues(content):
    """Find raw LaTeX that should be converted to Unicode or MathJax."""
    issues = []
    lines = content.split('\n')

    # Simple patterns to detect raw LaTeX outside MathJax
    raw_latex_patterns = [
        r'\\leq\s',
        r'\\geq\s',
        r'\\times\s',
        r'\\pm\s',
        r'\\theta_\{',
        r'\\alpha_\d',
    ]

    for i, line in enumerate(lines, 1):
        # Skip lines that are inside MathJax blocks
        if '\\(' in line or '\\[' in line or '$$' in line:
            continue

        for pattern in raw_latex_patterns:
            if re.search(pattern, line):
                issues.append({
                    'line': i,
                    'pattern': pattern,
                    'context': line[:100] if len(line) > 100 else line
                })

    return issues


def fix_unicode(content):
    """Fix Unicode corruptions. Returns (fixed_content, fix_count)."""
    fix_count = 0

    for corrupted, correct in UNICODE_FIXES.items():
        count = content.count(corrupted)
        if count > 0:
            content = content.replace(corrupted, correct)
            fix_count += count
            print(f"  Fixed {count}x: {repr(corrupted)} -> {repr(correct)}")

    return content, fix_count


def fix_latex_outside_mathjax(content):
    """
    Fix LaTeX symbols that appear outside of MathJax delimiters.
    Convert them to Unicode equivalents.
    """
    fix_count = 0

    # Simple replacements for common LaTeX outside MathJax
    # Only replace if NOT preceded by \( or $
    simple_fixes = [
        # Pattern: (regex, replacement)
        (r'(?<![\$\\])\\leq(?=\s|[^a-z])', '\u2264'),
        (r'(?<![\$\\])\\geq(?=\s|[^a-z])', '\u2265'),
        (r'(?<![\$\\])\\times(?=\s|[^a-z])', '\u00d7'),
        (r'(?<![\$\\])\\pm(?=\s|[^a-z])', '\u00b1'),
        (r'(?<![\$\\])\\infty(?=\s|[^a-z])', '\u221e'),
        (r'(?<![\$\\])\\sqrt(?=\s|[^a-z])', '\u221a'),
    ]

    for pattern, replacement in simple_fixes:
        matches = re.findall(pattern, content)
        if matches:
            content = re.sub(pattern, replacement, content)
            fix_count += len(matches)
            print(f"  Fixed {len(matches)}x LaTeX: {pattern} -> {repr(replacement)}")

    return content, fix_count


def generate_report(unicode_issues, latex_issues, iteration):
    """Generate a report of issues found."""
    report = []
    report.append(f"\n{'='*70}")
    report.append(f"ITERATION {iteration} - ISSUES FOUND")
    report.append(f"{'='*70}")

    report.append(f"\nUnicode Corruptions: {len(unicode_issues)}")
    if unicode_issues:
        for item in unicode_issues[:10]:
            report.append(f"  Line {item['line']}: {item['corrupted']}")
        if len(unicode_issues) > 10:
            report.append(f"  ... and {len(unicode_issues) - 10} more")

    report.append(f"\nRaw LaTeX Issues: {len(latex_issues)}")
    if latex_issues:
        for item in latex_issues[:10]:
            report.append(f"  Line {item['line']}: {item['pattern']}")
        if len(latex_issues) > 10:
            report.append(f"  ... and {len(latex_issues) - 10} more")

    return '\n'.join(report)


def fix_paper(file_path, max_iterations=10):
    """
    Iteratively fix the paper until no more issues are found.
    """
    print(f"\nOpening: {file_path}")
    print(f"File size: {os.path.getsize(file_path):,} bytes")

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
        unicode_issues = find_unicode_issues(content)
        latex_issues = find_latex_issues(content)

        report = generate_report(unicode_issues, latex_issues, iteration)
        print(report)

        # Count total issues
        total_issues = len(unicode_issues) + len(latex_issues)

        if total_issues == 0:
            print(f"\nSUCCESS: No more issues found after {iteration} iterations!")
            break

        # Apply fixes
        fixes_this_iteration = 0

        print(f"\nApplying Unicode fixes...")
        content, unicode_fixes = fix_unicode(content)
        fixes_this_iteration += unicode_fixes

        print(f"\nApplying LaTeX fixes...")
        content, latex_fixes = fix_latex_outside_mathjax(content)
        fixes_this_iteration += latex_fixes

        total_fixes += fixes_this_iteration

        print(f"\n>>> Applied {fixes_this_iteration} fixes this iteration")
        print(f">>> Total fixes so far: {total_fixes}")

        if fixes_this_iteration == 0 and total_issues > 0:
            print("\nWARNING: Issues detected but no fixes could be applied.")
            print("These may require manual intervention or updated fix patterns.")
            # Show remaining issues for debugging
            print("\nRemaining Unicode issues (first 5):")
            for item in unicode_issues[:5]:
                print(f"  Line {item['line']}: {item['corrupted']}")
            break

    # Save if changes were made
    if content != original_content:
        # Create backup
        backup_path = file_path + '.backup'
        with open(backup_path, 'w', encoding='utf-8') as f:
            f.write(original_content)
        print(f"\nBackup saved to: {backup_path}")

        # Save fixed content
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Fixed content saved to: {file_path}")
        print(f"Total fixes applied: {total_fixes}")
    else:
        print("\nNo changes needed - file is clean!")

    return {
        'iterations': iteration,
        'total_fixes': total_fixes,
        'file_path': file_path,
        'unicode_issues_remaining': len(find_unicode_issues(content)),
        'latex_issues_remaining': len(find_latex_issues(content))
    }


def main():
    """Main entry point."""
    script_dir = Path(__file__).parent.parent
    paper_path = script_dir / 'principia-metaphysica-paper.html'

    if len(sys.argv) > 1:
        paper_path = Path(sys.argv[1])

    if not paper_path.exists():
        print(f"Error: File not found: {paper_path}")
        sys.exit(1)

    print("="*70)
    print("PRINCIPIA METAPHYSICA - PAPER ENCODING FIX SCRIPT")
    print("="*70)
    print(f"\nTarget file: {paper_path}")

    result = fix_paper(str(paper_path))

    print(f"\n{'='*70}")
    print("SUMMARY")
    print(f"{'='*70}")
    print(f"File: {result['file_path']}")
    print(f"Iterations: {result['iterations']}")
    print(f"Total fixes applied: {result['total_fixes']}")
    print(f"Unicode issues remaining: {result['unicode_issues_remaining']}")
    print(f"LaTeX issues remaining: {result['latex_issues_remaining']}")

    if result['unicode_issues_remaining'] > 0 or result['latex_issues_remaining'] > 0:
        print("\n*** Some issues remain - may need manual review ***")
        sys.exit(1)
    else:
        print("\n*** All issues resolved! ***")
        sys.exit(0)


if __name__ == '__main__':
    main()
