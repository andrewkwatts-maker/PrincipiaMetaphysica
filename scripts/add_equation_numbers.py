#!/usr/bin/env python3
"""
add_equation_numbers.py - Add equation numbering to Principia Metaphysica paper

This script identifies key equations in the paper and adds systematic numbering
using LaTeX equation environments with labels for cross-referencing.

Strategy:
1. Identify key equations by pattern matching
2. Add (Eq. N) labels or convert to numbered equation environments
3. Create cross-reference index
4. Validate no broken references

Key Equations to Number:
- Master Actions (Eq. 1-3)
- Topological formulas (Eq. 4-5)
- Gauge coupling (Eq. 6-7)
- Dark energy (Eq. 8-9)
- Neutrino (Eq. 10-11)
- Predictions (Eq. 12-15)

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.
"""

import re
import sys
from pathlib import Path
from typing import List, Tuple, Dict

# =============================================================================
# EQUATION DEFINITIONS
# =============================================================================

# Format: (pattern_to_match, equation_label, equation_number, description)
EQUATIONS_TO_NUMBER: List[Tuple[str, str, int, str]] = [
    # Master Actions
    (r'S_{26}.*?=.*?\\int.*?d\^{26}x', 'master-action-26d', 1, 'Master 26D Action'),
    (r'S_D.*?=.*?\\int.*?d\^{13}x', 'shadow-action-13d', 2, '13D Shadow Action'),
    (r'S_4.*?=.*?\\int.*?d\^4x', 'effective-action-4d', 3, '4D Effective Action'),

    # Topological formulas
    (r'n_{\\text{gen}}.*?=.*?\\chi.*?/.*?48', 'generation-number', 4, 'Generation Number Formula'),
    (r'\\chi_{\\text{eff}}.*?=.*?2.*?h\^{11}', 'euler-characteristic', 5, 'Effective Euler Characteristic'),

    # Gauge coupling
    (r'\\alpha_{GUT}.*?=.*?1/\(10\\pi\)', 'alpha-gut', 6, 'GUT Coupling from 10pi'),
    (r'M_{GUT}.*?=.*?M_{Pl}.*?\\exp', 'mgut-formula', 7, 'GUT Scale Formula'),

    # Dark energy
    (r'w_0.*?=.*?-\\frac{d_{eff}.*?-.*?1}{d_{eff}.*?\\+.*?1}', 'w0-formula', 8, 'Dark Energy EoS w0'),
    (r'w\(z\).*?=.*?w_0.*?\\+.*?w_a', 'w-z-evolution', 9, 'DE Evolution w(z)'),

    # Neutrino
    (r'\\tan\^2.*?\\theta_{23}.*?=.*?\\shadow_kuf/\\shadow_chet', 'theta23-maximal', 10, 'Maximal Mixing Formula'),
    (r'm_\\nu.*?=.*?y\^2.*?v\^2/M_R', 'seesaw-formula', 11, 'Seesaw Mechanism'),

    # Predictions
    (r'\\tau_p.*?=.*?M_{GUT}\^4', 'proton-lifetime', 12, 'Proton Lifetime'),
    (r'm_{KK}.*?=.*?\\sqrt', 'kk-graviton-mass', 13, 'KK Graviton Mass'),
    (r'BR.*?p.*?\\to.*?e\^\\+.*?\\pi\^0', 'proton-br', 14, 'Proton Decay BR'),
    (r'\\eta.*?=.*?\\exp.*?T_\\omega', 'gw-dispersion', 15, 'GW Dispersion'),
]

# =============================================================================
# PROCESSING FUNCTIONS
# =============================================================================

def find_equations_in_file(content: str) -> List[Dict]:
    """Find all equations that should be numbered."""
    found_equations = []

    for pattern, label, num, description in EQUATIONS_TO_NUMBER:
        matches = list(re.finditer(pattern, content, re.IGNORECASE | re.DOTALL))
        for match in matches:
            found_equations.append({
                'match': match,
                'label': label,
                'number': num,
                'description': description,
                'text': match.group(0)[:100] + '...' if len(match.group(0)) > 100 else match.group(0)
            })

    return sorted(found_equations, key=lambda x: x['match'].start())


def add_equation_label(content: str, match, number: int) -> str:
    """Add equation number label after the equation."""
    # Find the end of the equation (closing $$ or \])
    start_pos = match.end()

    # Look for equation terminators
    terminators = ['$$', r'\]', r'\end{equation}', r'\end{align}']

    for term in terminators:
        pos = content.find(term, start_pos)
        if pos != -1 and pos < start_pos + 500:  # Within reasonable distance
            # Insert equation label
            label = f' \\tag{{{number}}}'
            return content[:pos] + label + content[pos:]

    return content  # No change if terminator not found


def generate_equation_index(equations: List[Dict]) -> str:
    """Generate a markdown index of all numbered equations."""
    lines = [
        "# Equation Index",
        "",
        "| Eq. | Label | Description |",
        "|-----|-------|-------------|"
    ]

    for eq in sorted(equations, key=lambda x: x['number']):
        lines.append(f"| {eq['number']} | `{eq['label']}` | {eq['description']} |")

    return '\n'.join(lines)


def process_paper(input_file: str, output_file: str = None, dry_run: bool = True):
    """Process the paper and add equation numbers."""

    input_path = Path(input_file)
    if not input_path.exists():
        print(f"Error: File not found: {input_file}")
        return False

    content = input_path.read_text(encoding='utf-8')

    # Find equations
    equations = find_equations_in_file(content)

    print(f"\n{'='*60}")
    print(f"Equation Numbering Report")
    print(f"{'='*60}")
    print(f"\nFound {len(equations)} equations to number:\n")

    for eq in equations:
        print(f"  Eq. {eq['number']:2d}: {eq['description']}")
        print(f"         Label: {eq['label']}")
        print(f"         Preview: {eq['text'][:60]}...")
        print()

    if dry_run:
        print("\n[DRY RUN] No changes made. Use --apply to make changes.")
        return True

    # Apply numbering (in reverse order to preserve positions)
    modified_content = content
    for eq in reversed(equations):
        modified_content = add_equation_label(modified_content, eq['match'], eq['number'])

    # Write output
    output_path = Path(output_file) if output_file else input_path
    output_path.write_text(modified_content, encoding='utf-8')

    print(f"\n[APPLIED] Equation numbers added to: {output_path}")

    # Generate index
    index = generate_equation_index(equations)
    index_path = input_path.parent / 'EQUATION_INDEX.md'
    index_path.write_text(index, encoding='utf-8')
    print(f"[CREATED] Equation index: {index_path}")

    return True


# =============================================================================
# MAIN
# =============================================================================

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Add equation numbering to PM paper')
    parser.add_argument('input_file', help='Input HTML file')
    parser.add_argument('-o', '--output', help='Output file (default: overwrite input)')
    parser.add_argument('--apply', action='store_true', help='Apply changes (default: dry run)')

    args = parser.parse_args()

    success = process_paper(
        args.input_file,
        args.output,
        dry_run=not args.apply
    )

    sys.exit(0 if success else 1)
