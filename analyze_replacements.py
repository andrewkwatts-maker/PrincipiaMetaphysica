#!/usr/bin/env python3
"""
Analyze PM constant replacements vs hardcoded values
"""

import re
from pathlib import Path
from collections import defaultdict

def count_pm_references(content):
    """Count PM constant references (data-category attributes)"""
    return len(re.findall(r'data-category="[^"]+"\s+data-param="[^"]+"', content))

def count_hardcoded_uncertainties(content):
    """Count hardcoded ± values that are NOT PM references"""
    lines = content.split('\n')
    hardcoded = 0

    for line in lines:
        # Skip lines with PM references
        if 'data-category=' in line:
            continue
        # Count ± symbols
        if '±' in line or '&plusmn;' in line:
            hardcoded += 1

    return hardcoded

def main():
    html_files = []
    for f in Path('.').rglob('*.html'):
        if 'node_modules' not in str(f) and '.git' not in str(f):
            html_files.append(f)

    print("="*80)
    print("PM CONSTANT REPLACEMENT ANALYSIS")
    print("="*80)
    print()

    file_stats = []
    total_pm = 0
    total_hardcoded = 0

    for html_file in sorted(html_files):
        try:
            content = html_file.read_text(encoding='utf-8')
            pm_count = count_pm_references(content)
            hard_count = count_hardcoded_uncertainties(content)

            if pm_count > 0 or hard_count > 0:
                file_stats.append({
                    'file': str(html_file),
                    'pm': pm_count,
                    'hardcoded': hard_count,
                    'total': pm_count + hard_count
                })
                total_pm += pm_count
                total_hardcoded += hard_count
        except Exception as e:
            print(f"Error processing {html_file}: {e}")

    # Sort by total replacements
    file_stats.sort(key=lambda x: x['total'], reverse=True)

    print(f"{'File':<50} {'PM Refs':<10} {'Hardcoded':<10} {'Total':<10}")
    print("-"*80)

    for stat in file_stats:
        fname = stat['file']
        if len(fname) > 47:
            fname = "..." + fname[-44:]
        print(f"{fname:<50} {stat['pm']:<10} {stat['hardcoded']:<10} {stat['total']:<10}")

    print("-"*80)
    print(f"{'TOTAL':<50} {total_pm:<10} {total_hardcoded:<10} {total_pm + total_hardcoded:<10}")
    print()

    # Calculate reduction
    original_estimate = 128  # From task description
    reduction_pct = ((original_estimate - total_hardcoded) / original_estimate) * 100

    print("="*80)
    print("SUMMARY")
    print("="*80)
    print(f"Original hardcoded values (estimated): {original_estimate}")
    print(f"Remaining hardcoded values:            {total_hardcoded}")
    print(f"PM constant references created:        {total_pm}")
    print(f"Reduction achieved:                    {reduction_pct:.1f}%")
    print()

    if reduction_pct >= 90:
        print("✓ SUCCESS: >90% reduction achieved!")
    else:
        print("✗ INCOMPLETE: <90% reduction")

    # Save detailed report
    with open('replacement_analysis.txt', 'w', encoding='utf-8') as f:
        f.write("PM CONSTANT REPLACEMENT ANALYSIS\n")
        f.write("="*80 + "\n\n")
        f.write(f"{'File':<50} {'PM Refs':<10} {'Hardcoded':<10} {'Total':<10}\n")
        f.write("-"*80 + "\n")
        for stat in file_stats:
            f.write(f"{stat['file']:<50} {stat['pm']:<10} {stat['hardcoded']:<10} {stat['total']:<10}\n")
        f.write("-"*80 + "\n")
        f.write(f"{'TOTAL':<50} {total_pm:<10} {total_hardcoded:<10} {total_pm + total_hardcoded:<10}\n\n")
        f.write(f"Reduction: {reduction_pct:.1f}%\n")

    print(f"[OK] Saved detailed report to replacement_analysis.txt")

if __name__ == '__main__':
    main()
