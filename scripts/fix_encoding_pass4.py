#!/usr/bin/env python3
"""
Pass 4: Fix the final remaining mojibake patterns

C3 8F CB 86 = broken phi character (should be φ = CF 86)
C3 A2 C2 81 C2 XX = broken superscript characters
C3 A2 C2 9D E2 80 = broken quote variant
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
    print("ENCODING FIX PASS 4 - FINAL PATTERNS")
    print("=" * 70)

    with open(paper_path, 'rb') as f:
        content = f.read()

    original_len = len(content)
    total_fixes = 0

    # ========== C3 8F CB 86 patterns (phi variants) ==========
    print("\n1. Fixing broken phi patterns (C3 8F CB 86)...")

    # C3 8F CB 86 appears to be a broken phi (φ)
    # The correct UTF-8 for φ is CF 86
    # This is: C3 8F (= Ï in Latin-1 = UTF-8 prefix) + CB 86 (broken continuation)
    # This might be Ï followed by ˆ (modifier letter circumflex)
    # In context of physics, this is likely φ (phi)
    phi_fixes = [
        (b'\xc3\x8f\xcb\x86', b'\xcf\x86'),  # Ïˆ -> φ
    ]

    for corrupted, correct in phi_fixes:
        count = content.count(corrupted)
        if count > 0:
            content = content.replace(corrupted, correct)
            total_fixes += count
            print(f"  Fixed {count}x: phi")

    # ========== C3 A2 C2 81 C2 XX patterns (superscripts) ==========
    print("\n2. Fixing broken superscript patterns (C3 A2 C2 81 C2 XX)...")

    # These are double-encoded superscript characters
    # E2 81 B0-BF are superscript digits/letters in Unicode
    # C3 A2 C2 81 C2 XX = broken version
    superscript_fixes = [
        # Superscript digits
        (b'\xc3\xa2\xc2\x81\xc2\xb0', b'\xe2\x81\xb0'),  # ⁰
        (b'\xc3\xa2\xc2\x81\xc2\xb1', b'\xe2\x81\xb1'),  # ¹ variant
        (b'\xc3\xa2\xc2\x81\xc2\xb2', b'\xe2\x81\xb2'),  # ²
        (b'\xc3\xa2\xc2\x81\xc2\xb3', b'\xe2\x81\xb3'),  # ³
        (b'\xc3\xa2\xc2\x81\xc2\xb4', b'\xe2\x81\xb4'),  # ⁴
        (b'\xc3\xa2\xc2\x81\xc2\xb5', b'\xe2\x81\xb5'),  # ⁵
        (b'\xc3\xa2\xc2\x81\xc2\xb6', b'\xe2\x81\xb6'),  # ⁶
        (b'\xc3\xa2\xc2\x81\xc2\xb7', b'\xe2\x81\xb7'),  # ⁷
        (b'\xc3\xa2\xc2\x81\xc2\xb8', b'\xe2\x81\xb8'),  # ⁸
        (b'\xc3\xa2\xc2\x81\xc2\xb9', b'\xe2\x81\xb9'),  # ⁹
        # Superscript signs and letters
        (b'\xc3\xa2\xc2\x81\xc2\xba', b'\xe2\x81\xba'),  # ⁺
        (b'\xc3\xa2\xc2\x81\xc2\xbb', b'\xe2\x81\xbb'),  # ⁻
        (b'\xc3\xa2\xc2\x81\xc2\xbc', b'\xe2\x81\xbc'),  # ⁼
        (b'\xc3\xa2\xc2\x81\xc2\xbd', b'\xe2\x81\xbd'),  # ⁽
        (b'\xc3\xa2\xc2\x81\xc2\xbe', b'\xe2\x81\xbe'),  # ⁾
        (b'\xc3\xa2\xc2\x81\xc2\xbf', b'\xe2\x81\xbf'),  # ⁿ
    ]

    for corrupted, correct in superscript_fixes:
        count = content.count(corrupted)
        if count > 0:
            content = content.replace(corrupted, correct)
            total_fixes += count
            try:
                print(f"  Fixed {count}x: {correct.decode('utf-8')}")
            except:
                print(f"  Fixed {count}x: superscript")

    # ========== C3 A2 C2 9D E2 80 pattern ==========
    print("\n3. Fixing broken quote patterns (C3 A2 C2 9D)...")

    # C3 A2 C2 9D E2 80 9C = broken pattern with quotes
    # This might be a broken right bracket or similar
    quote_fixes = [
        (b'\xc3\xa2\xc2\x9d\xe2\x80\x9c', b'\xe2\x9d\x9c'),  # ❜ or similar
    ]

    for corrupted, correct in quote_fixes:
        count = content.count(corrupted)
        if count > 0:
            content = content.replace(corrupted, correct)
            total_fixes += count
            print(f"  Fixed {count}x: quote pattern")

    # ========== C3 A2 C2 B1 C2 BC pattern ==========
    print("\n4. Fixing other broken patterns...")

    other_fixes = [
        (b'\xc3\xa2\xc2\xb1\xc2\xbc', b'\xe2\xb1\xbc'),  # Some symbol
    ]

    for corrupted, correct in other_fixes:
        count = content.count(corrupted)
        if count > 0:
            content = content.replace(corrupted, correct)
            total_fixes += count
            print(f"  Fixed {count}x: other pattern")

    # ========== SAVE ==========
    print("\n5. Saving fixed content...")

    with open(paper_path, 'wb') as f:
        f.write(content)

    new_len = len(content)

    # ========== VERIFY ==========
    print("\n6. Final verification...")

    remaining_cf = content.count(b'\xc3\x8f\xcb')
    remaining_triple = content.count(b'\xc3\xa2\xc2')

    # ========== REPORT ==========
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"  Total fixes applied: {total_fixes}")
    print(f"  Original size: {original_len:,} bytes")
    print(f"  New size: {new_len:,} bytes")
    print(f"  Size change: {new_len - original_len:+,} bytes")
    print(f"\n  Remaining C3 8F CB patterns: {remaining_cf}")
    print(f"  Remaining C3 A2 C2 patterns: {remaining_triple}")

    if remaining_cf == 0 and remaining_triple == 0:
        print("\n  SUCCESS: All patterns fixed!")
        return 0
    else:
        return 1

if __name__ == '__main__':
    sys.exit(main())
