#!/usr/bin/env python3
"""
Final encoding fix pass - fix remaining broken subscript patterns
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
    print("FINAL ENCODING FIX")
    print("=" * 70)

    with open(paper_path, 'rb') as f:
        content = f.read()

    original_len = len(content)
    total_fixes = 0

    # Fix the broken subscript letter patterns using exact byte sequences
    fixes = [
        # c₁'₁˜₁˜₁'₁™ -> cₒₘₘₒₙ (common)
        (b'\x63\xe2\x82\x81\xe2\x80\x99\xe2\x82\x81\xcb\x9c\xe2\x82\x81\xcb\x9c\xe2\x82\x81\xe2\x80\x99\xe2\x82\x81\xe2\x84\xa2',
         b'\x63\xe2\x82\x92\xe2\x82\x98\xe2\x82\x98\xe2\x82\x92\xe2\x82\x99'),

        # V₁‰ -> V₉ (subscript 9)
        # ₁‰ = U+2081 + U+2030 = subscript 1 + per mille
        # Should be ₉ = U+2089 = subscript 9
        (b'\xe2\x82\x81\xe2\x80\xb0', b'\xe2\x82\x89'),

        # g₁'₁™ -> gₑₙ (assuming gen context)
        # Let me check - in context "n_gen" so this is likely gₑₙ
        # ₑ = U+2091, ₙ = U+2099
        # But the pattern is: g + ₁ + ' + ₁ + ™
        # That's: 67 e28281 e28099 e28281 e284a2
        # Should be: gₑₙ = 67 e28291 e28299
        (b'\x67\xe2\x82\x81\xe2\x80\x99\xe2\x82\x81\xe2\x84\xa2',
         b'\x67\xe2\x82\x91\xe2\x82\x99'),  # gₑₙ

        # Standalone ₁… patterns
        # These are likely ₅ (subscript 5) based on D₅ context
        # But need to be careful - context matters
    ]

    for corrupted, correct in fixes:
        count = content.count(corrupted)
        if count > 0:
            content = content.replace(corrupted, correct)
            total_fixes += count
            try:
                correct_str = correct.decode('utf-8')
                print(f"  Fixed {count}x -> '{correct_str}'")
            except:
                print(f"  Fixed {count}x: {correct.hex()}")

    # Now look for remaining ₁ patterns that need fixing
    print("\n  Scanning for remaining broken subscript patterns...")

    # Patterns with ₁ followed by unusual characters
    remaining_patterns = []
    idx = 0
    while True:
        idx = content.find(b'\xe2\x82\x81', idx)  # subscript 1
        if idx == -1:
            break
        # Get context
        context = content[max(0, idx-10):idx+15]
        # Check if next byte is also a subscript (normal) or something broken
        next_bytes = content[idx+3:idx+6] if idx+6 < len(content) else b''
        if next_bytes and next_bytes != b'\xe2\x82':  # not another subscript
            # This might be broken
            remaining_patterns.append((idx, context.hex()))
        idx += 1
        if len(remaining_patterns) > 20:
            break

    if remaining_patterns:
        print(f"  Found {len(remaining_patterns)} potentially broken patterns")
        for pos, ctx in remaining_patterns[:5]:
            print(f"    Position {pos}: {ctx}")

    # Save
    print("\n  Saving...")
    with open(paper_path, 'wb') as f:
        f.write(content)

    new_len = len(content)

    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"  Total fixes: {total_fixes}")
    print(f"  Original size: {original_len:,} bytes")
    print(f"  New size: {new_len:,} bytes")
    print(f"  Size change: {new_len - original_len:+,} bytes")

    return 0

if __name__ == '__main__':
    sys.exit(main())
