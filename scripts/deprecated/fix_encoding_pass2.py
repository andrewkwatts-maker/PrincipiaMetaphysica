#!/usr/bin/env python3
"""
Pass 2: Fix remaining mojibake patterns in principia-metaphysica-paper.html

This script fixes the remaining encoding issues after the comprehensive pass.
It focuses on the specific patterns identified by the polish agents.

Usage: python scripts/fix_encoding_pass2.py
"""

import sys
from pathlib import Path

def main():
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

    paper_path = Path('principia-metaphysica-paper.html')

    if not paper_path.exists():
        print(f"Error: {paper_path} not found")
        return 1

    print("=" * 70)
    print("ENCODING FIX PASS 2 - REMAINING PATTERNS")
    print("=" * 70)

    with open(paper_path, 'rb') as f:
        content = f.read()

    original_len = len(content)
    total_fixes = 0

    # ========== CATEGORY 1: Double-encoded Greek (CE XX pattern) ==========
    print("\n1. Fixing double-encoded Greek letters (CE XX patterns)...")

    greek_ce_fixes = [
        # Lowercase Greek (CE B0-BF range)
        (b'\xc3\x8e\xc2\xb1', b'\xce\xb1'),  # alpha
        (b'\xc3\x8e\xc2\xb2', b'\xce\xb2'),  # beta
        (b'\xc3\x8e\xc2\xb3', b'\xce\xb3'),  # gamma
        (b'\xc3\x8e\xc2\xb4', b'\xce\xb4'),  # delta
        (b'\xc3\x8e\xc2\xb5', b'\xce\xb5'),  # epsilon
        (b'\xc3\x8e\xc2\xb6', b'\xce\xb6'),  # zeta
        (b'\xc3\x8e\xc2\xb7', b'\xce\xb7'),  # eta
        (b'\xc3\x8e\xc2\xb8', b'\xce\xb8'),  # theta
        (b'\xc3\x8e\xc2\xb9', b'\xce\xb9'),  # iota
        (b'\xc3\x8e\xc2\xba', b'\xce\xba'),  # kappa
        (b'\xc3\x8e\xc2\xbb', b'\xce\xbb'),  # lambda
        (b'\xc3\x8e\xc2\xbc', b'\xce\xbc'),  # mu
        (b'\xc3\x8e\xc2\xbd', b'\xce\xbd'),  # nu
        (b'\xc3\x8e\xc2\xbe', b'\xce\xbe'),  # xi
        (b'\xc3\x8e\xc2\xbf', b'\xce\xbf'),  # omicron

        # Uppercase Greek (CE 90-AF range)
        (b'\xc3\x8e\xc2\x91', b'\xce\x91'),  # Alpha
        (b'\xc3\x8e\xc2\x92', b'\xce\x92'),  # Beta
        (b'\xc3\x8e\xc2\x93', b'\xce\x93'),  # Gamma
        (b'\xc3\x8e\xc2\x94', b'\xce\x94'),  # Delta
        (b'\xc3\x8e\xc2\x95', b'\xce\x95'),  # Epsilon
        (b'\xc3\x8e\xc2\x96', b'\xce\x96'),  # Zeta
        (b'\xc3\x8e\xc2\x97', b'\xce\x97'),  # Eta
        (b'\xc3\x8e\xc2\x98', b'\xce\x98'),  # Theta
        (b'\xc3\x8e\xc2\x99', b'\xce\x99'),  # Iota
        (b'\xc3\x8e\xc2\x9a', b'\xce\x9a'),  # Kappa
        (b'\xc3\x8e\xc2\x9b', b'\xce\x9b'),  # Lambda
        (b'\xc3\x8e\xc2\x9c', b'\xce\x9c'),  # Mu
        (b'\xc3\x8e\xc2\x9d', b'\xce\x9d'),  # Nu
        (b'\xc3\x8e\xc2\x9e', b'\xce\x9e'),  # Xi
        (b'\xc3\x8e\xc2\x9f', b'\xce\x9f'),  # Omicron
        (b'\xc3\x8e\xc2\xa0', b'\xce\xa0'),  # Pi
        (b'\xc3\x8e\xc2\xa1', b'\xce\xa1'),  # Rho
        (b'\xc3\x8e\xc2\xa3', b'\xce\xa3'),  # Sigma
        (b'\xc3\x8e\xc2\xa4', b'\xce\xa4'),  # Tau
        (b'\xc3\x8e\xc2\xa5', b'\xce\xa5'),  # Upsilon
        (b'\xc3\x8e\xc2\xa6', b'\xce\xa6'),  # Phi
        (b'\xc3\x8e\xc2\xa7', b'\xce\xa7'),  # Chi
        (b'\xc3\x8e\xc2\xa8', b'\xce\xa8'),  # Psi
        (b'\xc3\x8e\xc2\xa9', b'\xce\xa9'),  # Omega
    ]

    for corrupted, correct in greek_ce_fixes:
        count = content.count(corrupted)
        if count > 0:
            content = content.replace(corrupted, correct)
            total_fixes += count
            print(f"  Fixed {count}x: {corrupted.hex()[:12]}... -> {correct.decode('utf-8')}")

    # ========== CATEGORY 2: Double-encoded Greek (CF XX pattern) ==========
    print("\n2. Fixing double-encoded Greek letters (CF XX patterns)...")

    greek_cf_fixes = [
        # Lowercase Greek continued (CF 80-8F range)
        (b'\xc3\x8f\xc2\x80', b'\xcf\x80'),  # pi
        (b'\xc3\x8f\xc2\x81', b'\xcf\x81'),  # rho
        (b'\xc3\x8f\xc2\x82', b'\xcf\x82'),  # final sigma
        (b'\xc3\x8f\xc2\x83', b'\xcf\x83'),  # sigma
        (b'\xc3\x8f\xc2\x84', b'\xcf\x84'),  # tau
        (b'\xc3\x8f\xc2\x85', b'\xcf\x85'),  # upsilon
        (b'\xc3\x8f\xc2\x86', b'\xcf\x86'),  # phi
        (b'\xc3\x8f\xc2\x87', b'\xcf\x87'),  # chi
        (b'\xc3\x8f\xc2\x88', b'\xcf\x88'),  # psi
        (b'\xc3\x8f\xc2\x89', b'\xcf\x89'),  # omega
    ]

    for corrupted, correct in greek_cf_fixes:
        count = content.count(corrupted)
        if count > 0:
            content = content.replace(corrupted, correct)
            total_fixes += count
            print(f"  Fixed {count}x: {corrupted.hex()[:12]}... -> {correct.decode('utf-8')}")

    # ========== CATEGORY 3: Triple-encoded subscripts ==========
    print("\n3. Fixing triple-encoded subscripts...")

    subscript_fixes = [
        (b'\xc3\xa2\xc2\x82\xc2\x80', b'\xe2\x82\x80'),  # subscript 0
        (b'\xc3\xa2\xc2\x82\xc2\x81', b'\xe2\x82\x81'),  # subscript 1
        (b'\xc3\xa2\xc2\x82\xc2\x82', b'\xe2\x82\x82'),  # subscript 2
        (b'\xc3\xa2\xc2\x82\xc2\x83', b'\xe2\x82\x83'),  # subscript 3
        (b'\xc3\xa2\xc2\x82\xc2\x84', b'\xe2\x82\x84'),  # subscript 4
        (b'\xc3\xa2\xc2\x82\xc2\x85', b'\xe2\x82\x85'),  # subscript 5
        (b'\xc3\xa2\xc2\x82\xc2\x86', b'\xe2\x82\x86'),  # subscript 6
        (b'\xc3\xa2\xc2\x82\xc2\x87', b'\xe2\x82\x87'),  # subscript 7
        (b'\xc3\xa2\xc2\x82\xc2\x88', b'\xe2\x82\x88'),  # subscript 8
        (b'\xc3\xa2\xc2\x82\xc2\x89', b'\xe2\x82\x89'),  # subscript 9
        (b'\xc3\xa2\xc2\x82\xc2\x99', b'\xe2\x82\x99'),  # subscript n
        (b'\xc3\xa2\xc2\x82\xc2\x98', b'\xe2\x82\x98'),  # subscript m
        (b'\xc3\xa2\xc2\x82\xc2\x9a', b'\xe2\x82\x9a'),  # subscript p
        (b'\xc3\xa2\xc2\x82\xc2\x91', b'\xe2\x82\x91'),  # subscript e
        (b'\xc3\xa2\xc2\x82\xc2\x9b', b'\xe2\x82\x9b'),  # subscript s
        (b'\xc3\xa2\xc2\x82\xc2\x95', b'\xe2\x82\x95'),  # subscript h
    ]

    for corrupted, correct in subscript_fixes:
        count = content.count(corrupted)
        if count > 0:
            content = content.replace(corrupted, correct)
            total_fixes += count
            print(f"  Fixed {count}x: subscript")

    # ========== CATEGORY 4: Triple-encoded math symbols ==========
    print("\n4. Fixing triple-encoded math symbols...")

    math_fixes = [
        # Arrows
        (b'\xc3\xa2\xc2\x86\xc2\x92', b'\xe2\x86\x92'),  # right arrow
        (b'\xc3\xa2\xc2\x86\xc2\x90', b'\xe2\x86\x90'),  # left arrow
        (b'\xc3\xa2\xc2\x86\xc2\x91', b'\xe2\x86\x91'),  # up arrow
        (b'\xc3\xa2\xc2\x86\xc2\x93', b'\xe2\x86\x93'),  # down arrow
        (b'\xc3\xa2\xc2\x86\xc2\x94', b'\xe2\x86\x94'),  # left-right arrow
        (b'\xc3\xa2\xc2\x87\xc2\x92', b'\xe2\x87\x92'),  # double right arrow
        (b'\xc3\xa2\xc2\x87\xc2\x90', b'\xe2\x87\x90'),  # double left arrow
        (b'\xc3\xa2\xc2\x87\xc2\x94', b'\xe2\x87\x94'),  # double left-right arrow

        # Angle brackets
        (b'\xc3\xa2\xc2\x9f\xc2\xa8', b'\xe2\x9f\xa8'),  # left angle bracket
        (b'\xc3\xa2\xc2\x9f\xc2\xa9', b'\xe2\x9f\xa9'),  # right angle bracket

        # Comparison
        (b'\xc3\xa2\xc2\x89\xc2\xa4', b'\xe2\x89\xa4'),  # less than or equal
        (b'\xc3\xa2\xc2\x89\xc2\xa5', b'\xe2\x89\xa5'),  # greater than or equal
        (b'\xc3\xa2\xc2\x89\xc2\xa0', b'\xe2\x89\xa0'),  # not equal
        (b'\xc3\xa2\xc2\x89\xc2\xa1', b'\xe2\x89\xa1'),  # equivalent
        (b'\xc3\xa2\xc2\x89\xc2\x88', b'\xe2\x89\x88'),  # approximately

        # Calculus/Analysis
        (b'\xc3\xa2\xc2\x88\xc2\x9a', b'\xe2\x88\x9a'),  # square root
        (b'\xc3\xa2\xc2\x88\xc2\x9e', b'\xe2\x88\x9e'),  # infinity
        (b'\xc3\xa2\xc2\x88\xc2\x82', b'\xe2\x88\x82'),  # partial derivative
        (b'\xc3\xa2\xc2\x88\xc2\x87', b'\xe2\x88\x87'),  # nabla
        (b'\xc3\xa2\xc2\x88\xc2\xab', b'\xe2\x88\xab'),  # integral
        (b'\xc3\xa2\xc2\x88\xc2\x91', b'\xe2\x88\x91'),  # summation
        (b'\xc3\xa2\xc2\x88\xc2\x8f', b'\xe2\x88\x8f'),  # product

        # Set theory
        (b'\xc3\xa2\xc2\x88\xc2\x88', b'\xe2\x88\x88'),  # element of
        (b'\xc3\xa2\xc2\x88\xc2\x89', b'\xe2\x88\x89'),  # not element of
        (b'\xc3\xa2\xc2\x8a\xc2\x82', b'\xe2\x8a\x82'),  # subset
        (b'\xc3\xa2\xc2\x8a\xc2\x83', b'\xe2\x8a\x83'),  # superset
        (b'\xc3\xa2\xc2\x8a\xc2\x95', b'\xe2\x8a\x95'),  # direct sum
        (b'\xc3\xa2\xc2\x8a\xc2\x97', b'\xe2\x8a\x97'),  # tensor product

        # Floor/Ceiling
        (b'\xc3\xa2\xc2\x8c\xc2\x8a', b'\xe2\x8c\x8a'),  # left floor
        (b'\xc3\xa2\xc2\x8c\xc2\x8b', b'\xe2\x8c\x8b'),  # right floor
        (b'\xc3\xa2\xc2\x8c\xc2\x88', b'\xe2\x8c\x88'),  # left ceiling
        (b'\xc3\xa2\xc2\x8c\xc2\x89', b'\xe2\x8c\x89'),  # right ceiling
    ]

    for corrupted, correct in math_fixes:
        count = content.count(corrupted)
        if count > 0:
            content = content.replace(corrupted, correct)
            total_fixes += count
            print(f"  Fixed {count}x: math symbol")

    # ========== CATEGORY 5: Double-encoded superscripts/misc ==========
    print("\n5. Fixing double-encoded superscripts and misc...")

    super_misc_fixes = [
        (b'\xc3\x82\xc2\xb2', b'\xc2\xb2'),  # superscript 2
        (b'\xc3\x82\xc2\xb3', b'\xc2\xb3'),  # superscript 3
        (b'\xc3\x82\xc2\xb9', b'\xc2\xb9'),  # superscript 1
        (b'\xc3\x82\xc2\xb0', b'\xc2\xb0'),  # degree
        (b'\xc3\x82\xc2\xb1', b'\xc2\xb1'),  # plus-minus
        (b'\xc3\x82\xc2\xbd', b'\xc2\xbd'),  # one-half
        (b'\xc3\x82\xc2\xbc', b'\xc2\xbc'),  # one-quarter
        (b'\xc3\x82\xc2\xa7', b'\xc2\xa7'),  # section sign
        (b'\xc3\x83\xc2\x97', b'\xc3\x97'),  # multiplication
        (b'\xc3\x83\xc2\xa4', b'\xc3\xa4'),  # a-umlaut (Kahler)
        (b'\xc3\x83\xc2\xb6', b'\xc3\xb6'),  # o-umlaut
        (b'\xc3\x83\xc2\xbc', b'\xc3\xbc'),  # u-umlaut
    ]

    for corrupted, correct in super_misc_fixes:
        count = content.count(corrupted)
        if count > 0:
            content = content.replace(corrupted, correct)
            total_fixes += count
            print(f"  Fixed {count}x: superscript/misc")

    # ========== CATEGORY 6: Dashes and quotes ==========
    print("\n6. Fixing dashes and quotes...")

    dash_quote_fixes = [
        (b'\xc3\xa2\xc2\x80\xc2\x94', b'\xe2\x80\x94'),  # em dash
        (b'\xc3\xa2\xc2\x80\xc2\x93', b'\xe2\x80\x93'),  # en dash
        (b'\xc3\xa2\xc2\x80\xc2\x98', b'\xe2\x80\x98'),  # left single quote
        (b'\xc3\xa2\xc2\x80\xc2\x99', b'\xe2\x80\x99'),  # right single quote
        (b'\xc3\xa2\xc2\x80\xc2\x9c', b'\xe2\x80\x9c'),  # left double quote
        (b'\xc3\xa2\xc2\x80\xc2\x9d', b'\xe2\x80\x9d'),  # right double quote
        (b'\xc3\xa2\xc2\x80\xc2\xa2', b'\xe2\x80\xa2'),  # bullet
        (b'\xc3\xa2\xc2\x80\xc2\xa6', b'\xe2\x80\xa6'),  # ellipsis
    ]

    for corrupted, correct in dash_quote_fixes:
        count = content.count(corrupted)
        if count > 0:
            content = content.replace(corrupted, correct)
            total_fixes += count
            print(f"  Fixed {count}x: dash/quote")

    # ========== CATEGORY 7: Emoji (4-byte sequences) ==========
    print("\n7. Fixing emoji patterns...")

    emoji_fixes = [
        # These are quadruple-encoded emoji
        (b'\xc3\xb0\xc2\x9f\xc2\x93\xc2\x84', b'\xf0\x9f\x93\x84'),  # document
        (b'\xc3\xb0\xc2\x9f\xc2\x95', b'\xf0\x9f\x95\x90'),  # clock (partial)
        (b'\xc3\xb0\xc2\x9f\xc2\x8e\xc2\x93', b'\xf0\x9f\x8e\x93'),  # graduation cap
    ]

    for corrupted, correct in emoji_fixes:
        count = content.count(corrupted)
        if count > 0:
            content = content.replace(corrupted, correct)
            total_fixes += count
            print(f"  Fixed {count}x: emoji")

    # ========== SAVE ==========
    print("\n8. Saving fixed content...")

    with open(paper_path, 'wb') as f:
        f.write(content)

    new_len = len(content)

    # ========== VERIFY ==========
    print("\n9. Verifying remaining issues...")

    remaining = []
    checks = [
        (b'\xc3\x8e', 'double-encoded Greek (CE)'),
        (b'\xc3\x8f', 'double-encoded Greek (CF)'),
        (b'\xc3\xa2\xc2', 'triple-encoded symbols'),
        (b'\xc3\x82\xc2', 'double-encoded superscripts'),
        (b'\xc3\x83\xc2', 'double-encoded misc'),
    ]

    for pattern, desc in checks:
        count = content.count(pattern)
        if count > 0:
            remaining.append(f"  {desc}: {count} remaining")

    # ========== REPORT ==========
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"  Total fixes applied: {total_fixes}")
    print(f"  Original size: {original_len:,} bytes")
    print(f"  New size: {new_len:,} bytes")
    print(f"  Size change: {new_len - original_len:+,} bytes")

    if remaining:
        print(f"\n  REMAINING ISSUES ({len(remaining)}):")
        for issue in remaining:
            print(issue)
        return 1
    else:
        print("\n  SUCCESS: No mojibake patterns detected!")
        return 0

if __name__ == '__main__':
    sys.exit(main())
