#!/usr/bin/env python3
"""Check for remaining encoding issues in the paper."""

import sys

def main():
    sys.stdout.reconfigure(encoding='utf-8')

    with open('principia-metaphysica-paper.html', 'r', encoding='utf-8') as f:
        content = f.read()

    issues = []

    # Check for BOM
    if content.startswith(chr(0xfeff)):
        issues.append(('BOM at start', 0, content[:20]))

    # Common mojibake patterns to check
    mojibake_checks = [
        (chr(0xe2) + chr(0x80) + chr(0x94), 'em dash mojibake'),
        (chr(0xe2) + chr(0x80) + chr(0x93), 'en dash mojibake'),
        (chr(0xc3) + chr(0xa2), 'double-encoded a-circumflex'),
        (chr(0xc2) + chr(0xa0), 'nbsp as two chars'),
    ]

    for pattern, name in mojibake_checks:
        count = content.count(pattern)
        if count > 0:
            idx = content.find(pattern)
            context = content[max(0, idx-15):idx+25]
            issues.append((name, count, context))

    # Check for proper characters that should be present
    proper_chars = [
        (chr(0x2014), 'em dash'),  # —
        (chr(0x2013), 'en dash'),  # –
        (chr(0x221a), 'sqrt'),      # √
        (chr(0x2264), 'leq'),       # ≤
        (chr(0x2265), 'geq'),       # ≥
    ]

    print("PROPER UNICODE CHARACTERS:")
    for char, name in proper_chars:
        count = content.count(char)
        print(f"  {name} ({repr(char)}): {count}")

    print("\nISSUES FOUND:")
    if issues:
        for name, count_or_idx, context in issues:
            if isinstance(count_or_idx, int) and count_or_idx > 1:
                print(f"  {name}: {count_or_idx} instances")
            else:
                print(f"  {name}")
            context_safe = context.encode('unicode_escape').decode('ascii')
            print(f"    Context: {context_safe}")
    else:
        print("  None!")


if __name__ == '__main__':
    main()
