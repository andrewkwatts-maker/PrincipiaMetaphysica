#!/usr/bin/env python3
"""
Script to identify and catalog remaining equation label issues
in principia-metaphysica-paper.html
"""

import re
from pathlib import Path

def find_equation_labels_with_pm_values(file_path):
    """Find all equation labels that still use PM values"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find equation labels with PM values (multiline pattern)
    pattern = r'<span class="equation-label">\s*\(\s*<span class="pm-value"[^>]*data-param="([^"]+)"[^>]*>\s*</span>\s*([^)]*)\)\s*</span>'

    matches = []
    for match in re.finditer(pattern, content, re.DOTALL):
        param = match.group(1)
        suffix = match.group(2).strip()
        start_pos = match.start()

        # Get line number
        line_num = content[:start_pos].count('\n') + 1

        # Get surrounding context
        context_start = max(0, start_pos - 200)
        context_end = min(len(content), start_pos + 200)
        context = content[context_start:context_end]

        matches.append({
            'line': line_num,
            'param': param,
            'suffix': suffix,
            'position': start_pos,
            'context': context
        })

    return matches

def main():
    file_path = Path(r'H:\Github\PrincipiaMetaphysica\principia-metaphysica-paper.html')

    matches = find_equation_labels_with_pm_values(file_path)

    print(f"Found {len(matches)} equation labels with PM values:\n")

    for i, match in enumerate(matches, 1):
        print(f"{i}. Line {match['line']}: ({match['param']}{match['suffix']})")
        print(f"   Param: {match['param']}")
        print()

    # Group by parameter
    by_param = {}
    for match in matches:
        param = match['param']
        if param not in by_param:
            by_param[param] = []
        by_param[param].append(match)

    print("\nGrouped by parameter:")
    for param, items in sorted(by_param.items()):
        print(f"\n{param}: {len(items)} instances")
        for item in items:
            print(f"  - Line {item['line']}: ({item['suffix']})")

if __name__ == '__main__':
    main()
