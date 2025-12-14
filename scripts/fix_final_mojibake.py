#!/usr/bin/env python3
"""Fix remaining mojibake patterns in the paper."""

import sys
import os

def main():
    paper_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'principia-metaphysica-paper.html')

    with open(paper_path, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content
    fixes_applied = 0

    # Fix patterns - build them from bytes to avoid encoding issues in source
    patterns = [
        # Double-encoded nbsp (C2 A0 when read as Latin-1 gives these chars)
        (b'\xc2\xa0'.decode('latin-1'), ' '),  # nbsp -> regular space
        # Middle dot
        (b'\xc2\xb7'.decode('latin-1'), '\u00b7'),  # middle dot
        # Minus sign / summation (triple encoded)
        (b'\xe2\x88\x92'.decode('latin-1'), '\u2212'),  # minus sign
        (b'\xe2\x87\x92'.decode('latin-1'), '\u21d2'),  # double right arrow
        # Fix any remaining em dash mojibake
        (b'\xe2\x80\x94'.decode('latin-1'), '\u2014'),  # em dash
        (b'\xe2\x80\x93'.decode('latin-1'), '\u2013'),  # en dash
    ]

    for corrupted, correct in patterns:
        count = content.count(corrupted)
        if count > 0:
            content = content.replace(corrupted, correct)
            fixes_applied += count
            print(f"Fixed {count}x: {corrupted.encode('unicode_escape').decode('ascii')} -> {correct.encode('unicode_escape').decode('ascii')}")

    if content != original:
        # Save backup
        backup_path = paper_path + '.bak2'
        with open(backup_path, 'w', encoding='utf-8') as f:
            f.write(original)
        print(f"Backup saved to: {backup_path}")

        with open(paper_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Fixed {fixes_applied} issues")
    else:
        print("No changes needed")

    # Verify
    with open(paper_path, 'r', encoding='utf-8') as f:
        content = f.read()

    remaining = 0
    for corrupted, _ in patterns:
        count = content.count(corrupted)
        remaining += count

    print(f"Remaining issues: {remaining}")
    return remaining

if __name__ == '__main__':
    sys.exit(main())
