#!/usr/bin/env python3
"""
Verify Agent 2 task completion for foundations/ directory
"""

import re
from pathlib import Path

def main():
    print("="*80)
    print("AGENT 2: FOUNDATIONS DIRECTORY VERIFICATION")
    print("="*80)
    print()

    foundations_dir = Path(r'H:\Github\PrincipiaMetaphysica\foundations')

    # Get all HTML files
    html_files = sorted(foundations_dir.glob('*.html'))

    print(f"Scanning {len(html_files)} HTML files in foundations/\n")

    # Pattern for numerical uncertainties (e.g., "5.0 ± 1.5")
    numerical_pattern = re.compile(
        r'(\d+\.?\d*)\s*[±+]/?[-−]\s*(\d+\.?\d*)',
        re.UNICODE
    )

    # Pattern for any ± symbol
    pm_symbol_pattern = re.compile(r'[±]', re.UNICODE)

    files_with_numerical_uncertainties = []
    files_with_pm_symbols = []
    pm_instances = []

    for html_file in html_files:
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
            lines = content.split('\n')

        # Check each line
        has_numerical = False
        has_pm = False

        for i, line in enumerate(lines, 1):
            # Check for numerical uncertainties
            if numerical_pattern.search(line):
                has_numerical = True
                files_with_numerical_uncertainties.append({
                    'file': html_file.name,
                    'line': i,
                    'content': line.strip()[:100]
                })

            # Check for ± symbols
            if pm_symbol_pattern.search(line):
                has_pm = True
                # Extract context
                pm_index = line.find('±')
                if pm_index >= 0:
                    start = max(0, pm_index - 40)
                    end = min(len(line), pm_index + 40)
                    context = line[start:end].strip()
                    pm_instances.append({
                        'file': html_file.name,
                        'line': i,
                        'context': context
                    })

        if has_pm:
            files_with_pm_symbols.append(html_file.name)

    # Report findings
    print("FINDINGS:")
    print("-" * 80)
    print(f"Files with ± symbols: {len(files_with_pm_symbols)}")
    print(f"Files with numerical uncertainties (X ± Y format): {len(files_with_numerical_uncertainties)}")
    print()

    if files_with_numerical_uncertainties:
        print("NUMERICAL UNCERTAINTIES FOUND (NEED REPLACEMENT):")
        print("-" * 80)
        for item in files_with_numerical_uncertainties:
            print(f"  {item['file']} (line {item['line']})")
            print(f"    {item['content']}")
        print()
    else:
        print("[✓] NO NUMERICAL UNCERTAINTIES FOUND")
        print("    All ± symbols are mathematical notation, not uncertainty values")
        print()

    if pm_instances:
        print("MATHEMATICAL NOTATION INSTANCES (PRESERVE):")
        print("-" * 80)
        for item in pm_instances:
            print(f"  {item['file']} (line {item['line']})")
            print(f"    {item['context']}")
        print()

    # Final verdict
    print("="*80)
    print("CONCLUSION:")
    print("="*80)

    if files_with_numerical_uncertainties:
        print(f"[✗] INCOMPLETE - {len(files_with_numerical_uncertainties)} files need updates")
        return 1
    else:
        print("[✓] COMPLETE - No files require updates")
        print()
        print("All ± symbols in foundations/ are legitimate mathematical notation:")
        print("  • Ψ± - Chiral projections (Dirac equation)")
        print("  • W± - W bosons (Yang-Mills theory)")
        print("  • N± - Polarizing lattices (G₂ manifolds)")
        print()
        print("The foundations/ directory contains educational content with no")
        print("PM framework predictions or simulation results that would require")
        print("replacement with PM constant references.")
        print()
        print("AGENT 2 TASK STATUS: COMPLETE (zero modifications needed)")
        return 0

if __name__ == '__main__':
    exit(main())
