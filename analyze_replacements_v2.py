#!/usr/bin/env python3
"""
Analyze PM constant replacements vs hardcoded values - REFINED VERSION
"""

import re
from pathlib import Path
import sys

def count_pm_references(content):
    """Count PM constant references (data-category attributes)"""
    return len(re.findall(r'data-category="[^"]+"\s+data-param="[^"]+"', content))

def count_hardcoded_uncertainties(content):
    """Count actual hardcoded number ± number patterns"""
    # Patterns for actual uncertainty values
    patterns = [
        r'(?<!["\'])(\d+\.?\d*)\s*±\s*(\d+\.?\d*)',  # 5.0 ± 1.5 (not in quotes)
        r'(?<!["\'])(\d+\.?\d*)\s*&plusmn;\s*(\d+\.?\d*)',  # 5.0 &plusmn; 1.5
        r'(?<!["\'])(\d+\.?\d*)\s*\+/-\s*(\d+\.?\d*)',  # 5.0 +/- 1.5
    ]

    hardcoded = []
    lines = content.split('\n')

    for line_num, line in enumerate(lines, 1):
        # Skip lines with PM references
        if 'data-category=' in line:
            continue

        for pattern in patterns:
            matches = re.finditer(pattern, line)
            for match in matches:
                hardcoded.append({
                    'line': line_num,
                    'value': f"{match.group(1)} ± {match.group(2)}",
                    'context': line.strip()[:80]
                })

    return hardcoded

def main():
    html_files = []
    for f in Path('.').rglob('*.html'):
        if 'node_modules' not in str(f) and '.git' not in str(f):
            html_files.append(f)

    print("="*80)
    print("PM CONSTANT REPLACEMENT ANALYSIS - REFINED")
    print("="*80)
    print()

    file_stats = []
    total_pm = 0
    all_hardcoded = []

    for html_file in sorted(html_files):
        try:
            content = html_file.read_text(encoding='utf-8')
            pm_count = count_pm_references(content)
            hard_items = count_hardcoded_uncertainties(content)

            if pm_count > 0 or len(hard_items) > 0:
                file_stats.append({
                    'file': str(html_file),
                    'pm': pm_count,
                    'hardcoded': len(hard_items),
                    'hard_items': hard_items,
                    'total': pm_count + len(hard_items)
                })
                total_pm += pm_count
                all_hardcoded.extend([{**item, 'file': str(html_file)} for item in hard_items])
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
    print(f"{'TOTAL':<50} {total_pm:<10} {len(all_hardcoded):<10} {total_pm + len(all_hardcoded):<10}")
    print()

    # Calculate reduction
    original_estimate = 128  # From task description
    reduction_pct = ((original_estimate - len(all_hardcoded)) / original_estimate) * 100

    print("="*80)
    print("SUMMARY")
    print("="*80)
    print(f"Original hardcoded values (estimated): {original_estimate}")
    print(f"Remaining hardcoded values:            {len(all_hardcoded)}")
    print(f"PM constant references created:        {total_pm}")
    print(f"Reduction achieved:                    {reduction_pct:.1f}%")
    print()

    if reduction_pct >= 90:
        print("SUCCESS: >90% reduction achieved!")
        status = "PASS"
    else:
        print("INCOMPLETE: <90% reduction")
        status = "NEEDS MORE WORK"

    print()
    print("="*80)
    print("REMAINING HARDCODED VALUES")
    print("="*80)

    for item in all_hardcoded[:30]:  # Show first 30
        print(f"\n{item['file']}:{item['line']}")
        print(f"  Value: {item['value']}")
        print(f"  Context: {item['context'][:70]}...")

    if len(all_hardcoded) > 30:
        print(f"\n... and {len(all_hardcoded) - 30} more")

    # Save detailed report
    with open('replacement_analysis.txt', 'w', encoding='utf-8') as f:
        f.write("PM CONSTANT REPLACEMENT ANALYSIS\n")
        f.write("="*80 + "\n\n")
        f.write(f"{'File':<50} {'PM Refs':<10} {'Hardcoded':<10} {'Total':<10}\n")
        f.write("-"*80 + "\n")
        for stat in file_stats:
            f.write(f"{stat['file']:<50} {stat['pm']:<10} {stat['hardcoded']:<10} {stat['total']:<10}\n")
        f.write("-"*80 + "\n")
        f.write(f"{'TOTAL':<50} {total_pm:<10} {len(all_hardcoded):<10} {total_pm + len(all_hardcoded):<10}\n\n")
        f.write(f"Reduction: {reduction_pct:.1f}%\n")
        f.write(f"Status: {status}\n\n")

        f.write("\n" + "="*80 + "\n")
        f.write("ALL REMAINING HARDCODED VALUES\n")
        f.write("="*80 + "\n\n")
        for item in all_hardcoded:
            f.write(f"{item['file']}:{item['line']}\n")
            f.write(f"  Value: {item['value']}\n")
            f.write(f"  Context: {item['context']}\n\n")

    print(f"\n[OK] Saved detailed report to replacement_analysis.txt")
    print(f"\nOVERALL STATUS: {status}")

if __name__ == '__main__':
    main()
