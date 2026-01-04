#!/usr/bin/env python3
"""Fix remaining mojibake in references.html"""

import sys

def main():
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

    refs_path = 'references.html'

    with open(refs_path, 'rb') as f:
        content = f.read()

    original = content
    fixes = 0

    # Fix patterns found in raw bytes
    patterns = [
        # Triple-encoded superscript -1: c3 a2 c2 81 c2 bb c2 b9 -> ⁻¹
        (b'\xc3\xa2\xc2\x81\xc2\xbb\xc2\xb9', '⁻¹'.encode('utf-8')),
        # Corrupted sqrt: c3 a2 cb 86 c5 a1 -> √
        (b'\xc3\xa2\xcb\x86\xc5\xa1', '√'.encode('utf-8')),
    ]

    for corrupted, correct in patterns:
        count = content.count(corrupted)
        if count > 0:
            content = content.replace(corrupted, correct)
            fixes += count
            print(f"Fixed {count}x: {corrupted.hex()} -> {correct.decode('utf-8')}")

    if content != original:
        with open(refs_path, 'wb') as f:
            f.write(content)
        print(f"Total fixes: {fixes}")
    else:
        print("No changes needed")

if __name__ == '__main__':
    main()
