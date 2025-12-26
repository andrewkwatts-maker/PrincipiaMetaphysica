#!/usr/bin/env python3
"""
Fix HTML entities inside MathJax math blocks.
MathJax requires actual characters, not HTML entities.

Common issues:
- &lt; should be < inside $...$
- &gt; should be > inside $...$
- &amp; should be & inside $...$
- &sigma; should be \sigma inside $...$
"""

import re
import os
from pathlib import Path

def fix_math_entities(content, filename):
    """Fix HTML entities inside math blocks"""
    fixes = []
    modified = content

    # Entity mappings for math mode
    entity_map = {
        '&lt;': '<',
        '&gt;': '>',
        '&amp;': '&',
        '&sigma;': r'\\sigma',
        '&alpha;': r'\\alpha',
        '&beta;': r'\\beta',
        '&gamma;': r'\\gamma',
        '&delta;': r'\\delta',
        '&epsilon;': r'\\epsilon',
        '&theta;': r'\\theta',
        '&lambda;': r'\\lambda',
        '&mu;': r'\\mu',
        '&nu;': r'\\nu',
        '&pi;': r'\\pi',
        '&rho;': r'\\rho',
        '&tau;': r'\\tau',
        '&phi;': r'\\phi',
        '&chi;': r'\\chi',
        '&psi;': r'\\psi',
        '&omega;': r'\\omega',
        '&Sigma;': r'\\Sigma',
        '&Omega;': r'\\Omega',
        '&Delta;': r'\\Delta',
        '&Gamma;': r'\\Gamma',
        '&minus;': '-',
        '&plusmn;': r'\\pm',
        '&times;': r'\\times',
        '&divide;': r'\\div',
        '&asymp;': r'\\approx',
        '&ne;': r'\\neq',
        '&le;': r'\\leq',
        '&ge;': r'\\geq',
        '&rarr;': r'\\rightarrow',
        '&larr;': r'\\leftarrow',
        '&harr;': r'\\leftrightarrow',
    }

    # Find inline math $...$
    # Use a function to replace entities only within math blocks
    def fix_inline_math(match):
        math_content = match.group(1)
        original = math_content
        for entity, replacement in entity_map.items():
            if entity in math_content:
                math_content = math_content.replace(entity, replacement)
        if math_content != original:
            fixes.append({
                'type': 'inline',
                'original': f"${original}$",
                'fixed': f"${math_content}$"
            })
        return f"${math_content}$"

    def fix_display_math(match):
        math_content = match.group(1)
        original = math_content
        for entity, replacement in entity_map.items():
            if entity in math_content:
                math_content = math_content.replace(entity, replacement)
        if math_content != original:
            fixes.append({
                'type': 'display',
                'original': f"$${original[:50]}...$$" if len(original) > 50 else f"$${original}$$",
                'fixed': f"$${math_content[:50]}...$$" if len(math_content) > 50 else f"$${math_content}$$"
            })
        return f"$${math_content}$$"

    # Fix display math first ($$...$$)
    modified = re.sub(r'\$\$(.*?)\$\$', fix_display_math, modified, flags=re.DOTALL)

    # Fix inline math ($...$) - but not $$
    # More careful pattern to avoid matching $$ delimiters
    modified = re.sub(r'(?<!\$)\$(?!\$)((?:[^$]|\\\$)*?)(?<!\$)\$(?!\$)', fix_inline_math, modified)

    return modified, fixes

def process_file(filepath, dry_run=True):
    """Process a single file"""
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()

        modified, fixes = fix_math_entities(content, str(filepath))

        if fixes:
            print(f"\n{'='*60}")
            print(f"FILE: {filepath}")
            print(f"{'='*60}")
            for fix in fixes:
                print(f"  [{fix['type']}]")
                print(f"    Before: {fix['original'][:100]}")
                print(f"    After:  {fix['fixed'][:100]}")

            if not dry_run:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(modified)
                print(f"  -> FILE UPDATED")

        return len(fixes)

    except Exception as e:
        print(f"Error processing {filepath}: {e}")
        return 0

def main():
    import sys

    dry_run = '--fix' not in sys.argv

    if dry_run:
        print("=" * 70)
        print("DRY RUN - No files will be modified")
        print("Run with --fix to apply changes")
        print("=" * 70)
    else:
        print("=" * 70)
        print("APPLYING FIXES")
        print("=" * 70)

    base_path = Path('.')

    # Files to process
    html_files = (
        list(base_path.glob('*.html')) +
        list(base_path.glob('sections/*.html')) +
        list(base_path.glob('foundations/*.html'))
    )

    total_fixes = 0
    for filepath in html_files:
        fixes = process_file(filepath, dry_run)
        total_fixes += fixes

    print(f"\n{'='*70}")
    print(f"TOTAL: {total_fixes} fixes {'would be applied' if dry_run else 'applied'}")
    print("=" * 70)

if __name__ == '__main__':
    main()
