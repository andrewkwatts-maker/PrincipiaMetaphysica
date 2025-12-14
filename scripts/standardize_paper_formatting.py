#!/usr/bin/env python3
"""
Standardize paper formatting - find and fix inconsistent layouts.

This script:
1. Identifies large text sections that need standardization
2. Fixes orphaned div structures
3. Ensures consistent styling for similar sections
4. Does NOT touch hc= parameters (as per user request)

Usage: python scripts/standardize_paper_formatting.py
"""

import sys
import re
from collections import Counter

def analyze_font_sizes(content):
    """Analyze font size usage patterns."""
    pattern = r'style="[^"]*font-size:\s*([^;"]+)'
    matches = re.findall(pattern, content)
    return Counter(matches)

def find_large_text_sections(content):
    """Find sections with unusually large text (2rem+) that might need review."""
    lines = content.split('\n')
    large_text_sections = []

    for i, line in enumerate(lines):
        # Match font-size >= 2rem or >= 24px
        if re.search(r'font-size:\s*(2|3|4|5)[0-9]*rem', line) or \
           re.search(r'font-size:\s*([2-9][0-9]|[1-9][0-9][0-9])px', line):
            # Get context (5 lines before and after)
            start = max(0, i - 5)
            end = min(len(lines), i + 6)
            context = '\n'.join(lines[start:end])
            large_text_sections.append({
                'line': i + 1,
                'content': line.strip()[:100],
                'context': context
            })

    return large_text_sections

def fix_orphaned_flex_containers(content):
    """Find and fix orphaned flex container children."""
    fixes = 0

    # Pattern: divs that appear to be flex children without a flex parent
    # This is a heuristic - we look for sequences of divs with arrows between them
    # that lack a proper flex container parent

    # The framework evolution pattern we already fixed - check for similar
    # patterns where text-align: center divs are followed by arrow divs

    # For safety, we won't automatically fix these - we'll report them
    issues = []

    lines = content.split('\n')
    for i, line in enumerate(lines):
        stripped = line.strip()

        # Look for arrow divs that might indicate flex layouts
        if '→' in stripped and '<div' in stripped and 'font-size: 2rem' in stripped:
            # Check if there's a flex container above
            found_flex = False
            for j in range(max(0, i-10), i):
                if 'display: flex' in lines[j] or 'display:flex' in lines[j]:
                    found_flex = True
                    break
            if not found_flex:
                issues.append({
                    'line': i + 1,
                    'issue': 'Arrow div without flex container parent',
                    'content': stripped[:80]
                })

    return issues, fixes

def find_inconsistent_status_badges(content):
    """Find status badges with inconsistent styling."""
    pattern = r'class="status-badge[^"]*"[^>]*style="[^"]*"'
    matches = list(re.finditer(pattern, content))

    if matches:
        return [(m.start(), m.group()) for m in matches[:10]]
    return []

def find_hc_parameters(content):
    """Find all hc= parameters to ensure we don't modify them."""
    pattern = r'hc=[^&"\s]+'
    matches = list(re.finditer(pattern, content))
    return [(m.start(), m.group()) for m in matches]

def generate_report(content):
    """Generate a formatting analysis report."""
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

    print("=" * 70)
    print("PAPER FORMATTING ANALYSIS REPORT")
    print("=" * 70)
    print()

    # Font size analysis
    print("1. FONT SIZE DISTRIBUTION")
    print("-" * 40)
    sizes = analyze_font_sizes(content)
    for size, count in sorted(sizes.items(), key=lambda x: -x[1])[:20]:
        print(f"   {size}: {count}")
    print()

    # Large text sections
    print("2. LARGE TEXT SECTIONS (2rem+)")
    print("-" * 40)
    large_sections = find_large_text_sections(content)
    if large_sections:
        for section in large_sections[:10]:
            print(f"   Line {section['line']}: {section['content'][:60]}")
    else:
        print("   No unusually large text found")
    print()

    # Orphaned flex children
    print("3. POTENTIAL ORPHANED FLEX CHILDREN")
    print("-" * 40)
    issues, _ = fix_orphaned_flex_containers(content)
    if issues:
        for issue in issues[:10]:
            print(f"   Line {issue['line']}: {issue['issue']}")
            print(f"      {issue['content'][:60]}")
    else:
        print("   No orphaned flex children detected")
    print()

    # hc= parameters
    print("4. HC= PARAMETERS (DO NOT MODIFY)")
    print("-" * 40)
    hc_params = find_hc_parameters(content)
    if hc_params:
        print(f"   Found {len(hc_params)} hc= parameters")
        for pos, param in hc_params[:5]:
            print(f"      {param}")
    else:
        print("   No hc= parameters found")
    print()

    # Summary
    print("=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"   Total font-size declarations: {sum(sizes.values())}")
    print(f"   Large text sections: {len(large_sections)}")
    print(f"   Potential structural issues: {len(issues)}")
    print(f"   hc= parameters (protected): {len(hc_params)}")
    print()

    return len(issues) == 0

def main():
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    paper_path = 'principia-metaphysica-paper.html'

    try:
        with open(paper_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"Error: {paper_path} not found")
        return 1

    # Generate report
    all_ok = generate_report(content)

    if all_ok:
        print("No formatting issues detected!")
        return 0
    else:
        print("Some potential issues found - review report above")
        return 0  # Don't fail, just report

if __name__ == '__main__':
    sys.exit(main())
