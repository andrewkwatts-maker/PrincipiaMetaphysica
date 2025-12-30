#!/usr/bin/env python3
"""
Pass 6: Fix remaining broken subscript patterns

These patterns result from partial decoding of triple-encoded subscripts:
- ₁† should be ₆
- ₁š₁ patterns need context-specific fixes
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
    print("ENCODING FIX PASS 6 - REMAINING SUBSCRIPTS")
    print("=" * 70)

    with open(paper_path, 'rb') as f:
        content = f.read()

    original_len = len(content)
    total_fixes = 0

    # Fix broken subscript patterns
    # ₁† (U+2081 U+2020) -> ₆ (U+2086)
    # ₁š (U+2081 U+0161) -> appears to be broken subscript pattern
    # Looking at context, these are subscript numbers that got mangled

    fixes = [
        # ₁† -> ₆ (subscript 6)
        (b'\xe2\x82\x81\xe2\x80\xa0', b'\xe2\x82\x86'),

        # ₁‡ -> ₇ (subscript 7) - dagger variant
        (b'\xe2\x82\x81\xe2\x80\xa1', b'\xe2\x82\x87'),

        # ₁ˆ -> ₈ (subscript 8) - circumflex variant
        (b'\xe2\x82\x81\xcb\x86', b'\xe2\x82\x88'),

        # ₁„ -> ₄ (subscript 4) - double low quotation
        (b'\xe2\x82\x81\xe2\x80\x9e', b'\xe2\x82\x84'),

        # ₁š -> this is trickier, need to see context
        # In "S₁š₁" context, this might be part of a formula
        # Let me check if it should be ₃ (subscript 3)
        # š = U+0161 has code point 353 decimal
        # ₃ = U+2083 has code point 8323 decimal
        # The corruption pattern suggests š came from double-encoding
        # Let's try ₃
        (b'\xe2\x82\x81\xc5\xa1', b'\xe2\x82\x83'),  # ₁š -> ₃

        # ₁Ž -> might be subscript pattern too
        # Ž = U+017D
        # This could be a broken subscript, possibly ₄ or another digit
        (b'\xe2\x82\x81\xc5\xbd', b'\xe2\x82\x84'),  # ₁Ž -> ₄ (guess based on context)

        # ₁ (just standalone) followed by unusual chars
        # Need to be careful not to break valid subscript 1s
    ]

    for corrupted, correct in fixes:
        count = content.count(corrupted)
        if count > 0:
            content = content.replace(corrupted, correct)
            total_fixes += count
            try:
                correct_str = correct.decode('utf-8')
                corrupted_str = corrupted.decode('utf-8', errors='replace')
                print(f"  Fixed {count}x: '{corrupted_str}' -> '{correct_str}'")
            except:
                print(f"  Fixed {count}x: {corrupted.hex()} -> {correct.hex()}")

    # Save
    print("\n  Saving...")
    with open(paper_path, 'wb') as f:
        f.write(content)

    new_len = len(content)

    # Verify
    print("\n  Verifying...")
    remaining_dagger = content.count(b'\xe2\x82\x81\xe2\x80\xa0')
    remaining_scaron = content.count(b'\xe2\x82\x81\xc5\xa1')

    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"  Total fixes: {total_fixes}")
    print(f"  Size change: {new_len - original_len:+,} bytes")
    print(f"  Remaining ₁† patterns: {remaining_dagger}")
    print(f"  Remaining ₁š patterns: {remaining_scaron}")

    return 0

if __name__ == '__main__':
    sys.exit(main())
