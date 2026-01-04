#!/usr/bin/env python3
"""
Comprehensive encoding fix for principia-metaphysica-paper.html

This script fixes ALL mojibake and encoding issues identified by the polish agents.
It processes the file in a single pass to avoid concurrent modification issues.

Usage: python scripts/fix_paper_encoding_comprehensive.py

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.
"""

import sys
import re
from pathlib import Path

def main():
    # Configure stdout for UTF-8
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

    paper_path = Path('principia-metaphysica-paper.html')

    if not paper_path.exists():
        print(f"Error: {paper_path} not found")
        return 1

    print("=" * 70)
    print("COMPREHENSIVE PAPER ENCODING FIX")
    print("=" * 70)

    # Read file as binary first to detect encoding issues
    with open(paper_path, 'rb') as f:
        raw_content = f.read()

    original_len = len(raw_content)
    fixes = 0

    # ===== BINARY MOJIBAKE FIXES =====
    print("\n1. Fixing binary mojibake patterns...")

    # All fixes use hex bytes and Unicode escapes to avoid encoding issues in script
    binary_fixes = [
        # Greek lowercase - corrupted patterns
        (b'\xc3\x8e\xc2\xb1', b'\xce\xb1'),  # alpha
        (b'\xc3\x8e\xc2\xb2', b'\xce\xb2'),  # beta
        (b'\xc3\x8e\xc2\xb3', b'\xce\xb3'),  # gamma
        (b'\xc3\x8e\xc2\xb4', b'\xce\xb4'),  # delta
        (b'\xc3\x8e\xc2\xb5', b'\xce\xb5'),  # epsilon
        (b'\xc3\x8e\xc2\xb6', b'\xce\xb6'),  # zeta
        (b'\xc3\x8e\xc2\xb7', b'\xce\xb7'),  # eta
        (b'\xc3\x8e\xc2\xb8', b'\xce\xb8'),  # theta
        (b'\xc3\x8e\xc2\xba', b'\xce\xba'),  # kappa
        (b'\xc3\x8e\xc2\xbb', b'\xce\xbb'),  # lambda
        (b'\xc3\x8e\xc2\xbc', b'\xce\xbc'),  # mu
        (b'\xc3\x8e\xc2\xbd', b'\xce\xbd'),  # nu
        (b'\xc3\x8e\xc2\xbe', b'\xce\xbe'),  # xi
        (b'\xc3\x8f\xc2\x80', b'\xcf\x80'),  # pi
        (b'\xc3\x8f\xc2\x81', b'\xcf\x81'),  # rho
        (b'\xc3\x8f\xc2\x83', b'\xcf\x83'),  # sigma
        (b'\xc3\x8f\xc2\x84', b'\xcf\x84'),  # tau
        (b'\xc3\x8f\xc2\x86', b'\xcf\x86'),  # phi
        (b'\xc3\x8f\xc2\x87', b'\xcf\x87'),  # chi
        (b'\xc3\x8f\xc2\x88', b'\xcf\x88'),  # psi
        (b'\xc3\x8f\xc2\x89', b'\xcf\x89'),  # omega

        # Greek uppercase
        (b'\xc3\x8e\xc2\x93', b'\xce\x93'),  # Gamma
        (b'\xc3\x8e\xc2\x94', b'\xce\x94'),  # Delta
        (b'\xc3\x8e\xc2\xa3', b'\xce\xa3'),  # Sigma
        (b'\xc3\x8e\xc2\xa8', b'\xce\xa8'),  # Psi
        (b'\xc3\x8e\xc2\xa9', b'\xce\xa9'),  # Omega

        # Arrows - triple encoded
        (b'\xc3\xa2\xc2\x86\xc2\x92', b'\xe2\x86\x92'),  # right arrow
        (b'\xc3\xa2\xc2\x87\xc2\x92', b'\xe2\x87\x92'),  # double right arrow
        (b'\xc3\xa2\xc2\x86\xc2\x90', b'\xe2\x86\x90'),  # left arrow
        (b'\xc3\xa2\xc2\x86\xc2\x94', b'\xe2\x86\x94'),  # left-right arrow

        # Subscripts - triple encoded
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

        # Superscripts - double encoded
        (b'\xc3\x82\xc2\xb2', b'\xc2\xb2'),  # superscript 2
        (b'\xc3\x82\xc2\xb3', b'\xc2\xb3'),  # superscript 3
        (b'\xc3\x82\xc2\xb9', b'\xc2\xb9'),  # superscript 1
        (b'\xc3\x82\xc2\xb1', b'\xc2\xb1'),  # plus-minus

        # Math operators - triple encoded
        (b'\xc3\xa2\xc2\x88\xc2\x92', b'\xe2\x88\x92'),  # minus
        (b'\xc3\xa2\xc2\x88\xc2\x9a', b'\xe2\x88\x9a'),  # sqrt
        (b'\xc3\xa2\xc2\x88\xc2\x9e', b'\xe2\x88\x9e'),  # infinity
        (b'\xc3\xa2\xc2\x88\xc2\x82', b'\xe2\x88\x82'),  # partial
        (b'\xc3\xa2\xc2\x88\xc2\xab', b'\xe2\x88\xab'),  # integral
        (b'\xc3\xa2\xc2\x88\xc2\x91', b'\xe2\x88\x91'),  # sum
        (b'\xc3\xa2\xc2\x88\xc2\x8f', b'\xe2\x88\x8f'),  # product
        (b'\xc3\xa2\xc2\x88\xc2\x88', b'\xe2\x88\x88'),  # element of
        (b'\xc3\xa2\xc2\x89\xc2\x88', b'\xe2\x89\x88'),  # approx
        (b'\xc3\xa2\xc2\x89\xc2\xa1', b'\xe2\x89\xa1'),  # equiv
        (b'\xc3\xa2\xc2\x89\xc2\xa4', b'\xe2\x89\xa4'),  # leq
        (b'\xc3\xa2\xc2\x89\xc2\xa5', b'\xe2\x89\xa5'),  # geq
        (b'\xc3\xa2\xc2\x89\xc2\xa0', b'\xe2\x89\xa0'),  # neq

        # Brackets - triple encoded
        (b'\xc3\xa2\xc2\x8c\xc2\x8a', b'\xe2\x8c\x8a'),  # left floor
        (b'\xc3\xa2\xc2\x8c\xc2\x8b', b'\xe2\x8c\x8b'),  # right floor
        (b'\xc3\xa2\xc2\x8c\xc2\x88', b'\xe2\x8c\x88'),  # left ceiling
        (b'\xc3\xa2\xc2\x8c\xc2\x89', b'\xe2\x8c\x89'),  # right ceiling
        (b'\xc3\xa2\xc2\x9f\xc2\xa8', b'\xe2\x9f\xa8'),  # left angle
        (b'\xc3\xa2\xc2\x9f\xc2\xa9', b'\xe2\x9f\xa9'),  # right angle

        # Set operators - triple encoded
        (b'\xc3\xa2\xc2\x8a\xc2\x97', b'\xe2\x8a\x97'),  # tensor
        (b'\xc3\xa2\xc2\x8a\xc2\x95', b'\xe2\x8a\x95'),  # direct sum
        (b'\xc3\xa2\xc2\x8a\xc2\x82', b'\xe2\x8a\x82'),  # subset
        (b'\xc3\xa2\xc2\x8a\xc2\x83', b'\xe2\x8a\x83'),  # superset

        # Dashes and quotes - triple encoded
        (b'\xc3\xa2\xc2\x80\xc2\x94', b'\xe2\x80\x94'),  # em dash
        (b'\xc3\xa2\xc2\x80\xc2\x93', b'\xe2\x80\x93'),  # en dash
        (b'\xc3\xa2\xc2\x80\xc2\x99', b'\xe2\x80\x99'),  # right quote
        (b'\xc3\xa2\xc2\x80\xc2\x9c', b'\xe2\x80\x9c'),  # left dquote
        (b'\xc3\xa2\xc2\x80\xc2\x9d', b'\xe2\x80\x9d'),  # right dquote

        # Multiplication and umlaut - double encoded
        (b'\xc3\x83\xc2\x97', b'\xc3\x97'),  # times
        (b'\xc3\x83\xc2\xa4', b'\xc3\xa4'),  # a-umlaut (Kahler)
    ]

    for corrupted, correct in binary_fixes:
        count = raw_content.count(corrupted)
        if count > 0:
            raw_content = raw_content.replace(corrupted, correct)
            fixes += count
            print(f"  Fixed {count}x: {corrupted.hex()[:16]}... -> {correct.hex()}")

    # ===== STRING-BASED FIXES =====
    print("\n2. Fixing remaining string patterns...")

    # Decode to string for remaining fixes
    content = raw_content.decode('utf-8', errors='replace')

    # These are the remaining mojibake patterns that appear as literal strings
    string_fixes = {
        # Common double-encoded patterns that survived binary fixes
        '\xc3\xa2\xe2\x82\xac\xe2\x80\x99': "'",  # right quote variant
        '\xc3\xa2\xe2\x82\xac\xe2\x80\x9c': '"',  # left dquote variant
        '\xc3\xa2\xe2\x82\xac\xe2\x80\x9d': '"',  # right dquote variant
    }

    for corrupted, correct in string_fixes.items():
        count = content.count(corrupted)
        if count > 0:
            content = content.replace(corrupted, correct)
            fixes += count
            print(f"  Fixed {count}x: [string pattern] -> {repr(correct)}")

    # ===== WHITESPACE FIXES =====
    print("\n3. Fixing whitespace issues...")

    # Fix extra spaces before subscript tags using regex
    whitespace_patterns = [
        (r'(\w)\s+<sub>', r'\1<sub>'),  # any letter + spaces + <sub>
    ]

    for pattern, replacement in whitespace_patterns:
        matches = re.findall(pattern, content)
        if matches:
            before = len(content)
            content = re.sub(pattern, replacement, content)
            count = len(matches)
            fixes += count
            print(f"  Fixed {count}x whitespace before <sub> tags")

    # ===== SAVE FIXED CONTENT =====
    print("\n4. Saving fixed content...")

    with open(paper_path, 'w', encoding='utf-8', newline='\n') as f:
        f.write(content)

    new_len = len(content.encode('utf-8'))

    # ===== VERIFICATION =====
    print("\n5. Verifying fixes...")

    # Re-read and check for remaining issues
    with open(paper_path, 'rb') as f:
        verify_content = f.read()

    # Check for remaining mojibake patterns (byte sequences that shouldn't appear)
    remaining_issues = []
    check_patterns = [
        (b'\xc3\x8e', 'double-encoded Greek'),
        (b'\xc3\x8f', 'double-encoded Greek'),
        (b'\xc3\xa2\xc2', 'triple-encoded symbols'),
        (b'\xc3\x82\xc2', 'double-encoded superscripts'),
        (b'\xc3\x83\xc2', 'double-encoded misc'),
    ]

    for pattern, desc in check_patterns:
        count = verify_content.count(pattern)
        if count > 0:
            remaining_issues.append(f"{desc}: {count} occurrences")

    # ===== REPORT =====
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"  Total fixes applied: {fixes}")
    print(f"  Original file size: {original_len:,} bytes")
    print(f"  New file size: {new_len:,} bytes")
    print(f"  Size change: {new_len - original_len:+,} bytes")

    if remaining_issues:
        print(f"\n  REMAINING ISSUES ({len(remaining_issues)}):")
        for issue in remaining_issues[:10]:
            print(f"    - {issue}")
        return 1
    else:
        print("\n  SUCCESS: No mojibake patterns detected!")
        return 0

if __name__ == '__main__':
    sys.exit(main())
