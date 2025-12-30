#!/usr/bin/env python3
"""Fix remaining mojibake patterns in the paper."""

import sys

def get_mojibake_fixes():
    """Get dictionary of mojibake patterns to fix."""
    fixes = []

    # Left/right angle brackets
    fixes.append((chr(0xe2) + chr(0x9f) + chr(0xa8), chr(0x27e8)))
    fixes.append((chr(0xe2) + chr(0x9f) + chr(0xa9), chr(0x27e9)))

    # Arrows
    fixes.append((chr(0xe2) + chr(0x86) + chr(0x90), chr(0x2190)))
    fixes.append((chr(0xe2) + chr(0x86) + chr(0x92), chr(0x2192)))

    # Em/en dash
    fixes.append((chr(0xe2) + chr(0x80) + chr(0x94), chr(0x2014)))
    fixes.append((chr(0xe2) + chr(0x80) + chr(0x93), chr(0x2013)))

    # Comparison operators
    fixes.append((chr(0xe2) + chr(0x89) + chr(0xa4), chr(0x2264)))
    fixes.append((chr(0xe2) + chr(0x89) + chr(0xa5), chr(0x2265)))
    fixes.append((chr(0xe2) + chr(0x89) + chr(0xa0), chr(0x2260)))
    fixes.append((chr(0xe2) + chr(0x89) + chr(0x88), chr(0x2248)))

    # Math symbols
    fixes.append((chr(0xe2) + chr(0x88) + chr(0x9e), chr(0x221e)))
    fixes.append((chr(0xe2) + chr(0x88) + chr(0x82), chr(0x2202)))
    fixes.append((chr(0xe2) + chr(0x88) + chr(0x87), chr(0x2207)))
    fixes.append((chr(0xe2) + chr(0x88) + chr(0x91), chr(0x2211)))
    fixes.append((chr(0xe2) + chr(0x88) + chr(0xab), chr(0x222b)))
    fixes.append((chr(0xe2) + chr(0x88) + chr(0x88), chr(0x2208)))

    # Double arrow
    fixes.append((chr(0xe2) + chr(0x87) + chr(0x92), chr(0x21d2)))

    return fixes


def main():
    sys.stdout.reconfigure(encoding='utf-8')

    filepath = 'principia-metaphysica-paper.html'

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    fixes = get_mojibake_fixes()
    total_fixed = 0

    for bad, good in fixes:
        count = content.count(bad)
        if count > 0:
            bad_repr = bad.encode('unicode_escape').decode('ascii')
            good_repr = good.encode('unicode_escape').decode('ascii')
            print(f'Fixing {count} instances: {bad_repr} -> {good_repr}')
            content = content.replace(bad, good)
            total_fixed += count

    if total_fixed > 0:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f'\nTotal fixes: {total_fixed}')
        print('File saved.')
    else:
        print('No mojibake patterns found.')


if __name__ == '__main__':
    main()
