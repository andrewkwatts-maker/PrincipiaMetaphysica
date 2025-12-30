#!/usr/bin/env python3
"""
Directional Alignment Swap Script (v12.9)

This script realigns the Greek letters to match their Enochian cardinal directions:
- East = Air (Α/Exarp)
- South = Fire (Π/Bitom)
- West = Water (Υ/Hcoma)
- North = Earth (Γ/Nanta)

While maintaining Chet/Kuf symbolism:
- Shadow_ח (Π, Υ) in Gate Mirror (tribes/material)
- Shadow_ק (Α, Γ) in Foundation Mirror (apostles/spiritual)

Changes Required:
1. Gate Mirror: Π (North-2) ↔ Τ (South-7) - Move Fire to South
2. Foundation Mirror: Γ (South-9) ↔ Η (North-3) - Move Earth to North
3. Foundation Mirror: Α (West-10) ↔ Θ (East-4) - Move Air to East
4. Gate Mirror: Υ already at West-10 ✓ - Water at West (no change)
"""

import json
import re
import os
import sys

# Ensure UTF-8 output
sys.stdout.reconfigure(encoding='utf-8')

# Define the swaps
GATE_SWAPS = {
    # position index: (old_letter, new_letter, old_name, new_name)
    1: ('Π', 'Τ', 'Pi', 'Tau'),      # North-2: Π→Τ (Judah gets Tau)
    6: ('Τ', 'Π', 'Tau', 'Pi'),      # South-7: Τ→Π (Simeon gets Pi/Fire)
}

FOUNDATION_SWAPS = {
    2: ('Η', 'Γ', 'Eta', 'Gamma'),   # North-3: Η→Γ (James Great gets Gamma/Earth)
    3: ('Θ', 'Α', 'Theta', 'Alpha'), # East-4: Θ→Α (John gets Alpha/Air)
    8: ('Γ', 'Η', 'Gamma', 'Eta'),   # South-9: Γ→Η (James Less gets Eta)
    9: ('Α', 'Θ', 'Alpha', 'Theta'), # West-10: Α→Θ (Jude gets Theta)
}

# Full new arrays after swaps
NEW_GATE_LETTERS = ('Ρ', 'Τ', 'Ζ', 'Ο', 'Ι', 'Σ', 'Π', 'Ω', 'Χ', 'Υ', 'Β', 'Κ')
NEW_GATE_NAMES = ('Rho', 'Tau', 'Zeta', 'Omicron', 'Iota', 'Sigma',
                  'Pi', 'Omega', 'Chi', 'Upsilon', 'Beta', 'Kappa')

NEW_FOUNDATION_LETTERS = ('Δ', 'Ε', 'Γ', 'Α', 'Λ', 'Μ', 'Ν', 'Ξ', 'Η', 'Θ', 'Φ', 'Ψ')
NEW_FOUNDATION_NAMES = ('Delta', 'Epsilon', 'Gamma', 'Alpha', 'Lambda', 'Mu',
                        'Nu', 'Xi', 'Eta', 'Theta', 'Phi', 'Psi')

# New pairings after swaps
NEW_WALL_PAIRINGS = {
    'north': ['X_{Ρ–Δ}', 'X_{Τ–Ε}', 'X_{Ζ–Γ}'],  # pos 3 now has Γ (Earth) ✓
    'east': ['X_{Ο–Α}', 'X_{Ι–Λ}', 'X_{Σ–Μ}'],   # pos 4 now has Α (Air) ✓
    'south': ['X_{Π–Ν}', 'X_{Ω–Ξ}', 'X_{Χ–Η}'],  # pos 7 now has Π (Fire) ✓
    'west': ['X_{Υ–Θ}', 'X_{Β–Φ}', 'X_{Κ–Ψ}'],   # pos 10 has Υ (Water) ✓
}

# Verification data
DIRECTIONAL_ALIGNMENT = {
    'Α': {'element': 'Air', 'direction': 'East', 'new_position': 4, 'new_wall': 'East'},
    'Π': {'element': 'Fire', 'direction': 'South', 'new_position': 7, 'new_wall': 'South'},
    'Υ': {'element': 'Water', 'direction': 'West', 'new_position': 10, 'new_wall': 'West'},
    'Γ': {'element': 'Earth', 'direction': 'North', 'new_position': 3, 'new_wall': 'North'},
}


def update_config_py(filepath):
    """Update config.py with new letter assignments."""
    print(f"\n{'='*60}")
    print("Updating config.py")
    print('='*60)

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content

    # Update GATE_LETTERS
    old_gate = r'GATE_LETTERS = \("Ρ", "Π", "Ζ", "Ο", "Ι", "Σ", "Τ", "Ω", "Χ", "Υ", "Β", "Κ"\)'
    new_gate = 'GATE_LETTERS = ("Ρ", "Τ", "Ζ", "Ο", "Ι", "Σ", "Π", "Ω", "Χ", "Υ", "Β", "Κ")'
    content = re.sub(old_gate, new_gate, content)

    # Update GATE_NAMES
    old_gate_names = r'GATE_NAMES = \("Rho", "Pi", "Zeta", "Omicron", "Iota", "Sigma",\s*"Tau", "Omega", "Chi", "Upsilon", "Beta", "Kappa"\)'
    new_gate_names = '''GATE_NAMES = ("Rho", "Tau", "Zeta", "Omicron", "Iota", "Sigma",
                  "Pi", "Omega", "Chi", "Upsilon", "Beta", "Kappa")'''
    content = re.sub(old_gate_names, new_gate_names, content, flags=re.DOTALL)

    # Update FOUNDATION_LETTERS
    old_found = r'FOUNDATION_LETTERS = \("Δ", "Ε", "Η", "Θ", "Λ", "Μ", "Ν", "Ξ", "Γ", "Α", "Φ", "Ψ"\)'
    new_found = 'FOUNDATION_LETTERS = ("Δ", "Ε", "Γ", "Α", "Λ", "Μ", "Ν", "Ξ", "Η", "Θ", "Φ", "Ψ")'
    content = re.sub(old_found, new_found, content)

    # Update FOUNDATION_NAMES
    old_found_names = r'FOUNDATION_NAMES = \("Delta", "Epsilon", "Eta", "Theta", "Lambda", "Mu",\s*"Nu", "Xi", "Gamma", "Alpha", "Phi", "Psi"\)'
    new_found_names = '''FOUNDATION_NAMES = ("Delta", "Epsilon", "Gamma", "Alpha", "Lambda", "Mu",
                        "Nu", "Xi", "Eta", "Theta", "Phi", "Psi")'''
    content = re.sub(old_found_names, new_found_names, content, flags=re.DOTALL)

    # Update SYMBOLIC_MEANINGS comments
    content = content.replace('# Π–Ε: Judah/Andrew', '# Τ–Ε: Judah/Andrew')
    content = content.replace('# Ζ–Η: Levi/James Great', '# Ζ–Γ: Levi/James Great')
    content = content.replace('# Ο–Θ: Joseph/John', '# Ο–Α: Joseph/John')
    content = content.replace('# Τ–Ν: Simeon/Matthew', '# Π–Ν: Simeon/Matthew')
    content = content.replace('# Χ–Γ: Zebulun/James Less', '# Χ–Η: Zebulun/James Less')
    content = content.replace('# Υ–Α: Gad/Jude', '# Υ–Θ: Gad/Jude')

    # Update comments about which letters are in which mirror
    content = content.replace(
        '# Gate Mirror Greek letters - 12 dimensions (includes Π, Υ for Shadow_ח coupling)',
        '# Gate Mirror Greek letters - 12 dimensions (Π at South, Υ at West for Shadow_ח)'
    )
    content = content.replace(
        '# Foundation Mirror Greek letters - 12 dimensions (includes Α, Γ for Shadow_ק coupling)',
        '# Foundation Mirror Greek letters - 12 dimensions (Α at East, Γ at North for Shadow_ק)'
    )

    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print("  ✓ config.py updated")
        return True
    else:
        print("  ✗ No changes made to config.py")
        return False


def update_theory_output_json(filepath):
    """Update theory_output.json with new letter assignments."""
    print(f"\n{'='*60}")
    print("Updating theory_output.json")
    print('='*60)

    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Update gate_mirror letters
    if 'shadow_dimension_nomenclature' in data:
        sdn = data['shadow_dimension_nomenclature']

        # Update gate_mirror
        if 'gate_mirror' in sdn:
            sdn['gate_mirror']['letters'] = list(NEW_GATE_LETTERS)
            sdn['gate_mirror']['letter_names'] = list(NEW_GATE_NAMES)
            sdn['gate_mirror']['description'] = 'Tribes/Gemstones (Sitra Gate - Π at South, Υ at West for Shadow_ח)'
            print("  ✓ gate_mirror updated")

        # Update foundation_mirror
        if 'foundation_mirror' in sdn:
            sdn['foundation_mirror']['letters'] = list(NEW_FOUNDATION_LETTERS)
            sdn['foundation_mirror']['letter_names'] = list(NEW_FOUNDATION_NAMES)
            sdn['foundation_mirror']['description'] = 'Apostles (Sitra Foundation - Α at East, Γ at North for Shadow_ק)'
            print("  ✓ foundation_mirror updated")

        # Update wall_pairings
        if 'wall_pairings' in sdn:
            walls = sdn['wall_pairings']

            # North wall
            if 'north' in walls:
                walls['north']['pairs'][1]['gate'] = 'Τ'  # Was Π
                walls['north']['pairs'][2]['foundation'] = 'Γ'  # Was Η
                walls['north']['notation'] = ['X_{Ρ–Δ}', 'X_{Τ–Ε}', 'X_{Ζ–Γ}']

            # East wall
            if 'east' in walls:
                walls['east']['pairs'][0]['foundation'] = 'Α'  # Was Θ
                walls['east']['notation'] = ['X_{Ο–Α}', 'X_{Ι–Λ}', 'X_{Σ–Μ}']

            # South wall
            if 'south' in walls:
                walls['south']['pairs'][0]['gate'] = 'Π'  # Was Τ
                walls['south']['pairs'][2]['foundation'] = 'Η'  # Was Γ
                walls['south']['notation'] = ['X_{Π–Ν}', 'X_{Ω–Ξ}', 'X_{Χ–Η}']

            # West wall
            if 'west' in walls:
                walls['west']['pairs'][0]['foundation'] = 'Θ'  # Was Α
                walls['west']['notation'] = ['X_{Υ–Θ}', 'X_{Β–Φ}', 'X_{Κ–Ψ}']

            print("  ✓ wall_pairings updated")

    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    return True


def update_svg_diagram(filepath):
    """Update the SVG diagram with new letter listings."""
    print(f"\n{'='*60}")
    print("Updating dimensional-reduction-pathway.svg")
    print('='*60)

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content

    # Update Gate Mirror listing (now with directional alignment note)
    content = content.replace(
        'Gate: Ρ,Π,Ζ,Ο,Ι,Σ,Τ,Ω,Χ,Υ,Β,Κ',
        'Gate: Ρ,Τ,Ζ,Ο,Ι,Σ,Π,Ω,Χ,Υ,Β,Κ'
    )

    # Update Foundation Mirror listing
    content = content.replace(
        'Found: Δ,Ε,Η,Θ,Λ,Μ,Ν,Ξ,Γ,Α,Φ,Ψ',
        'Found: Δ,Ε,Γ,Α,Λ,Μ,Ν,Ξ,Η,Θ,Φ,Ψ'
    )

    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print("  ✓ SVG updated")
        return True
    else:
        print("  ✗ No changes to SVG")
        return False


def update_html_archive(filepath):
    """Update mystical-nomenclature-archive.html with new letter assignments."""
    print(f"\n{'='*60}")
    print("Updating mystical-nomenclature-archive.html")
    print('='*60)

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content

    # Gate Mirror table updates
    # North-2: Π→Τ
    content = content.replace(
        '<tr><td class="greek-large">Π (Pi)</td><td>Judah</td><td>Emerald</td><td>X_Π</td></tr>',
        '<tr><td class="greek-large">Τ (Tau)</td><td>Judah</td><td>Emerald</td><td>X_Τ</td></tr>'
    )
    # South-7: Τ→Π
    content = content.replace(
        '<tr><td rowspan="3">South</td><td class="greek-large">Τ (Tau)</td><td>Simeon</td><td>Topaz</td><td>X_Τ</td></tr>',
        '<tr><td rowspan="3">South</td><td class="greek-large">Π (Pi)</td><td>Simeon</td><td>Topaz</td><td>X_Π</td></tr>'
    )

    # Foundation Mirror table updates
    # North-3: Η→Γ
    content = content.replace(
        '<tr><td class="greek-large">Η (Eta)</td><td>James the Great</td><td>X_Η</td></tr>',
        '<tr><td class="greek-large">Γ (Gamma)</td><td>James the Great</td><td>X_Γ</td></tr>'
    )
    # East-4: Θ→Α
    content = content.replace(
        '<tr><td rowspan="3">East</td><td class="greek-large">Θ (Theta)</td><td>John</td><td>X_Θ</td></tr>',
        '<tr><td rowspan="3">East</td><td class="greek-large">Α (Alpha)</td><td>John</td><td>X_Α</td></tr>'
    )
    # South-9: Γ→Η
    content = content.replace(
        '<tr><td class="greek-large">Γ (Gamma)</td><td>James the Less</td><td>X_Γ</td></tr>',
        '<tr><td class="greek-large">Η (Eta)</td><td>James the Less</td><td>X_Η</td></tr>'
    )
    # West-10: Α→Θ
    content = content.replace(
        '<tr><td rowspan="3">West</td><td class="greek-large">Α (Alpha)</td><td>Jude</td><td>X_Α</td></tr>',
        '<tr><td rowspan="3">West</td><td class="greek-large">Θ (Theta)</td><td>Jude</td><td>X_Θ</td></tr>'
    )

    # Update paired dimension notation
    content = content.replace(
        '<li><strong>North:</strong> X_{Ρ–Δ}, X_{Π–Ε}, X_{Ζ–Η}</li>',
        '<li><strong>North:</strong> X_{Ρ–Δ}, X_{Τ–Ε}, X_{Ζ–Γ}</li>'
    )
    content = content.replace(
        '<li><strong>East:</strong> X_{Ο–Θ}, X_{Ι–Λ}, X_{Σ–Μ}</li>',
        '<li><strong>East:</strong> X_{Ο–Α}, X_{Ι–Λ}, X_{Σ–Μ}</li>'
    )
    content = content.replace(
        '<li><strong>South:</strong> X_{Τ–Ν}, X_{Ω–Ξ}, X_{Χ–Γ}</li>',
        '<li><strong>South:</strong> X_{Π–Ν}, X_{Ω–Ξ}, X_{Χ–Η}</li>'
    )
    content = content.replace(
        '<li><strong>West:</strong> X_{Υ–Α}, X_{Β–Φ}, X_{Κ–Ψ}</li>',
        '<li><strong>West:</strong> X_{Υ–Θ}, X_{Β–Φ}, X_{Κ–Ψ}</li>'
    )

    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print("  ✓ HTML archive updated")
        return True
    else:
        print("  ✗ No changes to HTML")
        return False


def update_markdown_doc(filepath):
    """Update NOMENCLATURE_HISTORICAL_MAPPINGS.md with new letter assignments."""
    print(f"\n{'='*60}")
    print("Updating NOMENCLATURE_HISTORICAL_MAPPINGS.md")
    print('='*60)

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content

    # Gate Mirror table updates
    content = content.replace(
        '| North | Π (Pi) | Judah | Emerald |',
        '| North | Τ (Tau) | Judah | Emerald |'
    )
    content = content.replace(
        '| South | Τ (Tau) | Simeon | Topaz |',
        '| South | Π (Pi) | Simeon | Topaz |'
    )

    # Foundation Mirror table updates
    content = content.replace(
        '| North | Η (Eta) | James the Great |',
        '| North | Γ (Gamma) | James the Great |'
    )
    content = content.replace(
        '| East | Θ (Theta) | John |',
        '| East | Α (Alpha) | John |'
    )
    content = content.replace(
        '| South | Γ (Gamma) | James the Less |',
        '| South | Η (Eta) | James the Less |'
    )
    content = content.replace(
        '| West | Α (Alpha) | Jude |',
        '| West | Θ (Theta) | Jude |'
    )

    # Update paired notation
    content = content.replace(
        '- North: X_{Ρ-Δ}, X_{Π-Ε}, X_{Ζ-Η}',
        '- North: X_{Ρ-Δ}, X_{Τ-Ε}, X_{Ζ-Γ}'
    )
    content = content.replace(
        '- East: X_{Ο-Θ}, X_{Ι-Λ}, X_{Σ-Μ}',
        '- East: X_{Ο-Α}, X_{Ι-Λ}, X_{Σ-Μ}'
    )
    content = content.replace(
        '- South: X_{Τ-Ν}, X_{Ω-Ξ}, X_{Χ-Γ}',
        '- South: X_{Π-Ν}, X_{Ω-Ξ}, X_{Χ-Η}'
    )
    content = content.replace(
        '- West: X_{Υ-Α}, X_{Β-Φ}, X_{Κ-Ψ}',
        '- West: X_{Υ-Θ}, X_{Β-Φ}, X_{Κ-Ψ}'
    )

    # Update description
    content = content.replace(
        '*Contains Π, Υ for Shadow_ח coupling*',
        '*Contains Π (South), Υ (West) for Shadow_ח - directionally aligned*'
    )
    content = content.replace(
        '*Contains Α, Γ for Shadow_ק coupling*',
        '*Contains Α (East), Γ (North) for Shadow_ק - directionally aligned*'
    )

    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print("  ✓ Markdown doc updated")
        return True
    else:
        print("  ✗ No changes to Markdown")
        return False


def verify_alignment():
    """Verify that all brane letters are at correct cardinal positions."""
    print(f"\n{'='*60}")
    print("VERIFICATION: Directional Alignment")
    print('='*60)

    walls = ['North', 'North', 'North', 'East', 'East', 'East',
             'South', 'South', 'South', 'West', 'West', 'West']

    print("\nGate Mirror (tribes - Shadow_ח letters Π, Υ):")
    for i, letter in enumerate(NEW_GATE_LETTERS):
        if letter in DIRECTIONAL_ALIGNMENT:
            info = DIRECTIONAL_ALIGNMENT[letter]
            wall = walls[i]
            match = '✓' if wall == info['direction'] else '✗'
            print(f"  Position {i+1} ({wall}): {letter} ({info['element']}) - Expected: {info['direction']} {match}")

    print("\nFoundation Mirror (apostles - Shadow_ק letters Α, Γ):")
    for i, letter in enumerate(NEW_FOUNDATION_LETTERS):
        if letter in DIRECTIONAL_ALIGNMENT:
            info = DIRECTIONAL_ALIGNMENT[letter]
            wall = walls[i]
            match = '✓' if wall == info['direction'] else '✗'
            print(f"  Position {i+1} ({wall}): {letter} ({info['element']}) - Expected: {info['direction']} {match}")

    print("\nSitra Coupling Verification:")
    print(f"  Shadow_ח (Π, Υ) in Gate Mirror: {'Π' in NEW_GATE_LETTERS and 'Υ' in NEW_GATE_LETTERS}")
    print(f"  Shadow_ק (Α, Γ) in Foundation Mirror: {'Α' in NEW_FOUNDATION_LETTERS and 'Γ' in NEW_FOUNDATION_LETTERS}")


def main():
    """Main execution."""
    print("="*60)
    print("DIRECTIONAL ALIGNMENT SWAP SCRIPT")
    print("="*60)
    print("\nThis script will update all files to align brane letters")
    print("with their Enochian cardinal directions:")
    print("  • Α (Air) → East")
    print("  • Π (Fire) → South")
    print("  • Υ (Water) → West")
    print("  • Γ (Earth) → North")
    print()

    # Define file paths
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    files = {
        'config': os.path.join(base_path, 'config.py'),
        'theory_json': os.path.join(base_path, 'theory_output.json'),
        'svg': os.path.join(base_path, 'images', 'dimensional-reduction-pathway.svg'),
        'html': os.path.join(base_path, 'mystical-nomenclature-archive.html'),
        'markdown': os.path.join(base_path, 'reports', 'NOMENCLATURE_HISTORICAL_MAPPINGS.md'),
    }

    # Check all files exist
    for name, path in files.items():
        if not os.path.exists(path):
            print(f"ERROR: {name} not found at {path}")
            return False

    # Execute updates
    results = {}
    results['config'] = update_config_py(files['config'])
    results['theory_json'] = update_theory_output_json(files['theory_json'])
    results['svg'] = update_svg_diagram(files['svg'])
    results['html'] = update_html_archive(files['html'])
    results['markdown'] = update_markdown_doc(files['markdown'])

    # Verify alignment
    verify_alignment()

    # Summary
    print(f"\n{'='*60}")
    print("SUMMARY")
    print('='*60)
    for name, success in results.items():
        status = '✓' if success else '✗'
        print(f"  {status} {name}")

    all_success = all(results.values())
    print(f"\nOverall: {'SUCCESS' if all_success else 'PARTIAL'}")

    return all_success


if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
