#!/usr/bin/env python3
"""
Categorize remaining hardcoded uncertainty values
"""

import re
from pathlib import Path

def is_experimental_reference(context):
    """Check if context suggests this is an experimental reference"""
    exp_keywords = [
        'DESI', 'Planck', 'Super-K', 'NuFIT', 'PDG', 'CERN',
        'experimental', 'measured', 'observed', 'data',
        'LHC', 'ATLAS', 'CMS', 'SH0ES', 'BAO'
    ]
    return any(kw in context for kw in exp_keywords)

def is_in_svg(context):
    """Check if value is in SVG diagram (text label)"""
    return '<text' in context or '</text>' in context or 'svg' in context.lower()

def is_pm_prediction(context):
    """Check if this is a PM prediction that should be replaced"""
    pm_keywords = ['PM prediction', 'predicts', 'theoretical', 'calculated', 'derived']
    exp_keywords = ['DESI', 'Planck', 'measured', 'observed']

    has_pm = any(kw in context for kw in pm_keywords)
    has_exp = any(kw in context for kw in exp_keywords)

    # If it has experimental keywords, it's a reference
    if has_exp:
        return False
    # If it has PM keywords, it's a prediction
    return has_pm

def count_hardcoded_uncertainties(content):
    """Count actual hardcoded number ± number patterns with categorization"""
    patterns = [
        r'(?<!["\'])(\d+\.?\d*)\s*±\s*(\d+\.?\d*)',
        r'(?<!["\'])(\d+\.?\d*)\s*&plusmn;\s*(\d+\.?\d*)',
    ]

    hardcoded = []
    lines = content.split('\n')

    for line_num, line in enumerate(lines, 1):
        if 'data-category=' in line:
            continue

        for pattern in patterns:
            matches = re.finditer(pattern, line)
            for match in matches:
                context = line.strip()
                category = 'UNKNOWN'

                if is_in_svg(context):
                    category = 'SVG_DIAGRAM'
                elif is_experimental_reference(context):
                    category = 'EXP_REFERENCE'
                elif is_pm_prediction(context):
                    category = 'PM_PREDICTION'
                elif 'BR(' in context or 'branching' in context.lower():
                    category = 'BRANCHING_RATIO'
                elif 'TeV' in context and ('5.0' in match.group(1) or '5.02' in match.group(1)):
                    category = 'KK_MASS'
                elif 'w_a' in context or 'w₀' in context or 'w<sub>0</sub>' in context:
                    category = 'DARK_ENERGY'
                else:
                    category = 'OTHER'

                hardcoded.append({
                    'line': line_num,
                    'value': f"{match.group(1)} ± {match.group(2)}",
                    'context': context[:100],
                    'category': category
                })

    return hardcoded

def main():
    html_files = []
    for f in Path('.').rglob('*.html'):
        if 'node_modules' not in str(f) and '.git' not in str(f):
            html_files.append(f)

    print("="*80)
    print("CATEGORIZATION OF REMAINING HARDCODED VALUES")
    print("="*80)
    print()

    all_hardcoded = []

    for html_file in sorted(html_files):
        try:
            content = html_file.read_text(encoding='utf-8')
            hard_items = count_hardcoded_uncertainties(content)
            all_hardcoded.extend([{**item, 'file': str(html_file)} for item in hard_items])
        except Exception as e:
            print(f"Error: {e}")

    # Group by category
    by_category = {}
    for item in all_hardcoded:
        cat = item['category']
        if cat not in by_category:
            by_category[cat] = []
        by_category[cat].append(item)

    print(f"TOTAL REMAINING HARDCODED VALUES: {len(all_hardcoded)}")
    print()

    for cat in sorted(by_category.keys()):
        items = by_category[cat]
        print(f"\n{cat}: {len(items)} values")
        print("-" * 80)
        for item in items[:5]:  # Show first 5
            print(f"  {item['value']:<15} in {item['file']}")
            print(f"    {item['context'][:75]}...")
        if len(items) > 5:
            print(f"  ... and {len(items) - 5} more")

    # Legitimate vs should-be-replaced
    legitimate = len(by_category.get('EXP_REFERENCE', [])) + len(by_category.get('SVG_DIAGRAM', []))
    should_replace = len(all_hardcoded) - legitimate

    print()
    print("="*80)
    print("ASSESSMENT")
    print("="*80)
    print(f"Total remaining:           {len(all_hardcoded)}")
    print(f"Legitimate (exp refs):     {legitimate}")
    print(f"Should be replaced:        {should_replace}")
    print()

    original = 128
    actual_replaced = original - should_replace
    reduction_pct = (actual_replaced / original) * 100

    print(f"Original hardcoded:        {original}")
    print(f"Actually replaced:         {actual_replaced}")
    print(f"Effective reduction:       {reduction_pct:.1f}%")
    print()

    if reduction_pct >= 90:
        print("STATUS: PASS (>90% reduction)")
    else:
        print(f"STATUS: PARTIAL ({reduction_pct:.0f}% reduction, need {int(original * 0.9 - actual_replaced)} more)")

if __name__ == '__main__':
    main()
