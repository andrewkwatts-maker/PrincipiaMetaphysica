#!/usr/bin/env python3
"""
Pass 3: Fix remaining complex mojibake patterns

These are triple-encoded patterns with embedded quote characters.
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
    print("ENCODING FIX PASS 3 - COMPLEX PATTERNS")
    print("=" * 70)

    with open(paper_path, 'rb') as f:
        content = f.read()

    original_len = len(content)
    total_fixes = 0

    # These are the actual byte patterns found in the file
    # Pattern: C3 8E E2 80 9C = I-circumflex + left double quote (broken Delta)
    # Pattern: C3 8E E2 80 9D = I-circumflex + right double quote (broken Delta)
    # Pattern: C3 8E E2 80 BA = I-circumflex + single right angle quote

    print("\n1. Fixing complex triple-encoded Greek patterns...")

    # Based on analysis, these Î" and Î" patterns are broken Greek capital letters
    # The context shows these are Delta (Δ) in physics formulas like ΔV, Δm, etc.
    complex_fixes = [
        # Î" (C3 8E E2 80 9C) -> Δ (CE 94) - used for Delta
        (b'\xc3\x8e\xe2\x80\x9c', b'\xce\x94'),
        # Î" (C3 8E E2 80 9D) -> Δ (CE 94) - alternate encoding of Delta
        (b'\xc3\x8e\xe2\x80\x9d', b'\xce\x94'),
        # Î› (C3 8E E2 80 BA) -> CDM context suggests this might be Λ for Lambda
        (b'\xc3\x8e\xe2\x80\xba', b'\xce\x9b'),
    ]

    for corrupted, correct in complex_fixes:
        count = content.count(corrupted)
        if count > 0:
            content = content.replace(corrupted, correct)
            total_fixes += count
            try:
                correct_char = correct.decode('utf-8')
                print(f"  Fixed {count}x: {corrupted.hex()} -> {correct_char}")
            except:
                print(f"  Fixed {count}x: {corrupted.hex()} -> {correct.hex()}")

    # Now check for remaining C3 8E patterns and their actual byte sequences
    print("\n2. Scanning for remaining C3 8E patterns...")

    idx = 0
    remaining_patterns = {}
    while True:
        idx = content.find(b'\xc3\x8e', idx)
        if idx == -1:
            break
        # Get next few bytes
        next_bytes = content[idx:idx+6]
        pattern_hex = next_bytes.hex()
        if pattern_hex not in remaining_patterns:
            remaining_patterns[pattern_hex] = 0
        remaining_patterns[pattern_hex] += 1
        idx += 1

    if remaining_patterns:
        print("  Unique remaining patterns:")
        for pattern, count in sorted(remaining_patterns.items(), key=lambda x: -x[1])[:15]:
            print(f"    {pattern}: {count}x")

    # ========== SAVE ==========
    print("\n3. Saving fixed content...")

    with open(paper_path, 'wb') as f:
        f.write(content)

    new_len = len(content)

    # ========== VERIFY ==========
    print("\n4. Verifying...")

    remaining_ce = content.count(b'\xc3\x8e')
    remaining_cf = content.count(b'\xc3\x8f')
    remaining_triple = content.count(b'\xc3\xa2\xc2')

    # ========== REPORT ==========
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"  Total fixes applied: {total_fixes}")
    print(f"  Original size: {original_len:,} bytes")
    print(f"  New size: {new_len:,} bytes")
    print(f"  Size change: {new_len - original_len:+,} bytes")
    print(f"\n  Remaining C3 8E patterns: {remaining_ce}")
    print(f"  Remaining C3 8F patterns: {remaining_cf}")
    print(f"  Remaining triple-encoded: {remaining_triple}")

    if remaining_ce > 0 or remaining_cf > 0 or remaining_triple > 0:
        return 1
    else:
        print("\n  SUCCESS: All patterns fixed!")
        return 0

if __name__ == '__main__':
    sys.exit(main())
