#!/usr/bin/env python3
"""
Focused Magic Number Fixer for Principia Metaphysica
====================================================

This script:
1. Adds <script src="theory-constants.js"></script> to all HTML files (if not present)
2. Creates a PRIORITIES.md file listing which pages need manual review

The goal is to establish the JS constants as available, then let agents/manual review
handle contextual replacements where appropriate.

Copyright (c) 2025 Andrew Keith Watts. All rights reserved.
"""

import re
import json
from pathlib import Path
from collections import defaultdict

def check_has_script_tag(filepath):
    """Check if file already has theory-constants.js script tag"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            return 'theory-constants.js' in content
    except:
        return False

def add_script_tag_to_html(filepath):
    """Add script tag to HTML file if not present"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # Check if already has the script
        if 'theory-constants.js' in content:
            return False, "Already has script tag"

        # Find the </head> tag and insert before it
        if '</head>' in content:
            script_tag = '    <script src="theory-constants.js"></script>\n'
            content = content.replace('</head>', script_tag + '</head>', 1)

            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return True, "Added script tag"
        else:
            return False, "No </head> tag found"
    except Exception as e:
        return False, f"Error: {e}"

def scan_and_prioritize():
    """Scan HTML files and create priority list"""

    # Get all HTML files
    html_files = list(Path('.').rglob('*.html'))
    excluded_dirs = {'node_modules', '.git', 'venv', '__pycache__', 'components'}
    html_files = [f for f in html_files if not any(ex in str(f) for ex in excluded_dirs)]

    # Track results
    results = {
        'script_added': [],
        'already_has_script': [],
        'failed': [],
        'priority_files': []
    }

    # Priority patterns - these indicate files that likely need review
    priority_patterns = [
        (r'<strong>\d+\.?\d*e[+\-]?\d+', 'Scientific notation in bold text'),
        (r'data-\w+="[\d.]+"', 'Data attributes with numeric values'),
        (r'value="\d+"', 'Form values'),
        (r'<code>[^<]*\d+\.?\d*e[+\-]?\d+', 'Scientific notation in code blocks'),
    ]

    for filepath in sorted(html_files):
        # Add script tag
        added, msg = add_script_tag_to_html(filepath)

        if added:
            results['script_added'].append(str(filepath))
        elif 'Already' in msg:
            results['already_has_script'].append(str(filepath))
        else:
            results['failed'].append((str(filepath), msg))

        # Check if file needs priority review
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

            priority_reasons = []
            for pattern, reason in priority_patterns:
                if re.search(pattern, content):
                    priority_reasons.append(reason)

            if priority_reasons:
                results['priority_files'].append({
                    'file': str(filepath),
                    'reasons': priority_reasons
                })
        except:
            pass

    return results

def generate_priorities_report(results):
    """Generate markdown report of priorities"""

    report = []
    report.append("# Magic Number Replacement Priorities")
    report.append("")
    report.append("This report identifies which HTML files likely contain magic numbers")
    report.append("in contexts where they should be replaced with `PM.*` constants.")
    report.append("")
    report.append("## Summary")
    report.append("")
    report.append(f"- **Script tags added**: {len(results['script_added'])} files")
    report.append(f"- **Already had script**: {len(results['already_has_script'])} files")
    report.append(f"- **Failed**: {len(results['failed'])} files")
    report.append(f"- **Priority for review**: {len(results['priority_files'])} files")
    report.append("")

    report.append("## Files Updated with Script Tag")
    report.append("")
    if results['script_added']:
        for filepath in results['script_added']:
            report.append(f"- `{filepath}`")
    else:
        report.append("*None - all files already had script tag*")
    report.append("")

    report.append("## Priority Files for Manual Review")
    report.append("")
    report.append("These files contain patterns suggesting magic numbers in replaceable contexts:")
    report.append("")

    if results['priority_files']:
        for item in sorted(results['priority_files'], key=lambda x: len(x['reasons']), reverse=True):
            report.append(f"### `{Path(item['file']).name}`")
            report.append(f"Path: `{item['file']}`")
            report.append("")
            report.append("**Detected patterns:**")
            for reason in item['reasons']:
                report.append(f"- {reason}")
            report.append("")
    else:
        report.append("*No high-priority files detected*")

    report.append("")
    report.append("## Failed Files")
    report.append("")
    if results['failed']:
        for filepath, reason in results['failed']:
            report.append(f"- `{filepath}`: {reason}")
    else:
        report.append("*No failures*")

    report.append("")
    report.append("## Next Steps")
    report.append("")
    report.append("1. **Theory sections** (geometric-framework, gauge-unification, etc):")
    report.append("   - Review formulas and replace hard-coded values with PM constants")
    report.append("   - Example: `2.118×10¹⁶` → `PM.format.scientific(PM.proton_decay.M_GUT, 3)`")
    report.append("")
    report.append("2. **Beginner's guide and paper:**")
    report.append("   - Replace scientific notation in predictions with PM constants")
    report.append("   - Keep prose numbers (like \"26-dimensional\") as-is for readability")
    report.append("")
    report.append("3. **Foundation pages:**")
    report.append("   - Replace example values with actual PM constants where relevant")
    report.append("")
    report.append("## Replacement Examples")
    report.append("")
    report.append("```html")
    report.append("<!-- Before -->")
    report.append("<strong>M<sub>GUT</sub> = 2.118×10¹⁶ GeV</strong>")
    report.append("")
    report.append("<!-- After -->")
    report.append("<strong>M<sub>GUT</sub> = <span id=\"mgut-value\"></span> GeV</strong>")
    report.append("<script>")
    report.append("document.getElementById('mgut-value').textContent = ")
    report.append("    PM.format.scientific(PM.proton_decay.M_GUT, 3);")
    report.append("</script>")
    report.append("```")
    report.append("")
    report.append("Or for data attributes:")
    report.append("```html")
    report.append("<!-- Before -->")
    report.append('<div data-mgut="2.118e16">...</')
    report.append("")
    report.append("<!-- After -->")
    report.append('<div data-mgut="" id="data-mgut">...</div>')
    report.append("<script>")
    report.append("document.getElementById('data-mgut').dataset.mgut = PM.proton_decay.M_GUT;")
    report.append("</script>")
    report.append("```")

    return "\n".join(report)

if __name__ == '__main__':
    print("Principia Metaphysica - Focused Magic Number Fixer")
    print("=" * 70)
    print()
    print("Step 1: Adding theory-constants.js script tags to HTML files...")

    results = scan_and_prioritize()

    print(f"\nResults:")
    print(f"  - Added script tag: {len(results['script_added'])} files")
    print(f"  - Already had script: {len(results['already_has_script'])} files")
    print(f"  - Failed: {len(results['failed'])} files")
    print(f"  - Priority for review: {len(results['priority_files'])} files")

    # Generate and save report
    report = generate_priorities_report(results)

    with open('MAGIC_NUMBER_PRIORITIES.md', 'w', encoding='utf-8') as f:
        f.write(report)

    print("\nStep 2: Generated priority report")
    print("  - Saved: MAGIC_NUMBER_PRIORITIES.md")

    print("\n" + "=" * 70)
    print("COMPLETE")
    print("=" * 70)
    print("\nNext: Review MAGIC_NUMBER_PRIORITIES.md for manual replacement guidance")
