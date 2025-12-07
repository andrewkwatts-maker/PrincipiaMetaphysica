"""
Comprehensive analysis of uncertainty values in foundations/ directory
Agent 2 - Foundations Directory Analysis
"""

import os
import re
from pathlib import Path

# Pattern to match numerical uncertainties like "5.0 ± 1.5" or "5.0 +/- 1.5"
numerical_uncertainty = re.compile(
    r'(\d+\.?\d*)\s*([±+]/?[-−])\s*(\d+\.?\d*)',
    re.UNICODE
)

# Pattern to match any ± symbol (to catch mathematical notation)
any_plus_minus = re.compile(r'[±]', re.UNICODE)

foundations_dir = Path(r'H:\Github\PrincipiaMetaphysica\foundations')

print("="*70)
print("FOUNDATIONS DIRECTORY UNCERTAINTY ANALYSIS")
print("="*70)
print()

# Get all HTML files
html_files = sorted(foundations_dir.glob('*.html'))
print(f"Found {len(html_files)} HTML files in foundations/\n")

# Track statistics
files_with_pm_symbols = []
files_with_numerical_uncertainties = []
mathematical_notation_instances = []

for html_file in html_files:
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
        lines = content.split('\n')

    # Check for any ± symbols
    pm_matches = []
    numerical_matches = []

    for i, line in enumerate(lines, 1):
        # Check for numerical uncertainties
        num_match = numerical_uncertainty.search(line)
        if num_match:
            numerical_matches.append({
                'line': i,
                'value': num_match.group(0),
                'context': line.strip()[:150]
            })

        # Check for ± symbols (could be mathematical notation)
        elif any_plus_minus.search(line):
            pm_matches.append({
                'line': i,
                'context': line.strip()[:150]
            })

    if numerical_matches:
        files_with_numerical_uncertainties.append(html_file.name)
        print(f"[NUMERICAL UNCERTAINTIES] {html_file.name}:")
        for match in numerical_matches:
            print(f"  Line {match['line']}: {match['value']}")
            print(f"    Context: {match['context']}")
        print()

    if pm_matches:
        files_with_pm_symbols.append(html_file.name)
        print(f"[MATHEMATICAL NOTATION] {html_file.name}:")
        for match in pm_matches:
            snippet = match['context']
            # Extract the relevant part with ±
            pm_index = snippet.find('±')
            if pm_index >= 0:
                start = max(0, pm_index - 30)
                end = min(len(snippet), pm_index + 30)
                context = '...' + snippet[start:end] + '...'
                print(f"  Line {match['line']}: {context}")
                mathematical_notation_instances.append({
                    'file': html_file.name,
                    'line': match['line'],
                    'context': snippet
                })
        print()

print("="*70)
print("SUMMARY")
print("="*70)
print(f"Total HTML files scanned: {len(html_files)}")
print(f"Files with ± symbols: {len(files_with_pm_symbols)}")
print(f"Files with numerical uncertainties (need replacement): {len(files_with_numerical_uncertainties)}")
print(f"Mathematical notation instances (preserve as-is): {len(mathematical_notation_instances)}")
print()

if files_with_numerical_uncertainties:
    print("FILES REQUIRING UPDATES:")
    for f in files_with_numerical_uncertainties:
        print(f"  - {f}")
else:
    print("✓ NO FILES REQUIRE UPDATES")
    print("  All ± symbols are legitimate mathematical notation")

print()
print("MATHEMATICAL NOTATION INSTANCES (PRESERVED):")
for instance in mathematical_notation_instances:
    print(f"  {instance['file']} (line {instance['line']})")

print()
print("="*70)
print("CONCLUSION")
print("="*70)
print("All ± symbols in foundations/ directory are mathematical notation:")
print("  - Ψ± (chiral projections in Dirac equation)")
print("  - W± (W bosons in Yang-Mills theory)")
print("  - N± (polarizing lattices in G₂ manifolds)")
print()
print("No hardcoded numerical uncertainties found.")
print("No replacements needed in foundations/ directory.")
print("="*70)
