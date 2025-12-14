#!/usr/bin/env python3
"""
Pass 5: Fix remaining subscript letter patterns

These are subscript letters that got mangled:
- c₁'₁˜₁˜₁'₁™ should be cₒₘₘₒₙ (common)
- g₁'₁™ should be gₒₙ or similar
- V₁‰ should be V₉ (subscript 9)
- ₁… needs context to fix
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
    print("ENCODING FIX PASS 5 - SUBSCRIPT LETTERS")
    print("=" * 70)

    with open(paper_path, 'r', encoding='utf-8') as f:
        content = f.read()

    original_len = len(content)
    total_fixes = 0

    # Fix the broken subscript letter patterns
    # These need to be carefully mapped based on context

    fixes = [
        # c₁'₁˜₁˜₁'₁™ -> cₒₘₘₒₙ (common)
        ("c₁'₁˜₁˜₁'₁™", "cₒₘₘₒₙ"),

        # g₁'₁™ -> gₒₙ (as in 'polygon' context maybe)
        # But need to check context - might be different
        # Let's leave this for now and check context

        # V₁‰ -> V₉ (subscript 9 for 9D volume)
        ("V₁‰", "V₉"),

        # ₁… -> ₅ (subscript 5 in D₅ context, already fixed above)
        # But there might be other contexts
    ]

    for old, new in fixes:
        count = content.count(old)
        if count > 0:
            content = content.replace(old, new)
            total_fixes += count
            print(f"  Fixed {count}x: '{old}' -> '{new}'")

    # Check what g₁'₁™ should be
    if "g₁'₁™" in content:
        # Find context
        idx = content.find("g₁'₁™")
        context = content[max(0, idx-50):idx+60]
        print(f"\n  Context for g₁'₁™: ...{context}...")

    # Save
    print("\n  Saving...")
    with open(paper_path, 'w', encoding='utf-8') as f:
        f.write(content)

    new_len = len(content)

    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"  Total fixes: {total_fixes}")
    print(f"  Size change: {new_len - original_len:+,} chars")

    # Check for remaining issues
    remaining = []
    check_patterns = ["₁'", "₁˜", "₁‰"]
    for p in check_patterns:
        count = content.count(p)
        if count > 0:
            remaining.append(f"  '{p}': {count}")

    if remaining:
        print("\n  Remaining patterns to check:")
        for r in remaining:
            print(r)

    return 0

if __name__ == '__main__':
    sys.exit(main())
