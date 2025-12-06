#!/usr/bin/env python3
"""
Fix Unicode characters in all simulation files for Windows compatibility
"""

import os
import glob

# Unicode replacements
replacements = {
    '→': '->',
    '✓': '[OK]',
    '✗': '[FAIL]',
    '±': '+/-',
    '×': 'x',
    'σ': 'sigma',
    'χ': 'chi',
    'α': 'alpha',
    'β': 'beta',
    'γ': 'gamma',
    'δ': 'delta',
    'θ': 'theta',
    'κ': 'kappa',
    'λ': 'lambda',
    'μ': 'mu',
    'ν': 'nu',
    'π': 'pi',
    'ρ': 'rho',
    'τ': 'tau',
    'φ': 'phi',
    'ω': 'omega',
    'Δ': 'Delta',
    'Σ': 'Sigma',
    'Ω': 'Omega',
    'ℓ': 'l',
    'ℒ': 'L',
    'ℋ': 'H',
    # Subscripts
    '₀': '_0',
    '₁': '_1',
    '₂': '_2',
    '₃': '_3',
    '₄': '_4',
    '₅': '_5',
    '₆': '_6',
    '₇': '_7',
    '₈': '_8',
    '₉': '_9',
    # Superscripts
    '⁰': '^0',
    '¹': '^1',
    '²': '^2',
    '³': '^3',
    '⁴': '^4',
    '⁵': '^5',
    '⁶': '^6',
    '⁷': '^7',
    '⁸': '^8',
    '⁹': '^9',
    '⁺': '^+',
    '⁻': '^-',
    '⁼': '^=',
    # Math symbols
    '≈': '~',
    '≠': '!=',
    '≤': '<=',
    '≥': '>=',
    '∈': 'in',
    '∩': '^',
    '∫': 'int',
    '∧': '^',
}

def fix_file(filepath):
    """Fix Unicode in a single file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        original = content
        for old, new in replacements.items():
            content = content.replace(old, new)

        if content != original:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Fixed: {filepath}")
            return True
        else:
            return False
    except Exception as e:
        print(f"Error fixing {filepath}: {e}")
        return False

def main():
    # Fix simulations directory
    sim_files = glob.glob('simulations/*.py')

    # Fix run_all_simulations.py (already mostly done)
    all_files = sim_files + ['run_all_simulations.py']

    fixed_count = 0
    for filepath in all_files:
        if os.path.exists(filepath):
            if fix_file(filepath):
                fixed_count += 1

    print(f"\nTotal files fixed: {fixed_count}/{len(all_files)}")

if __name__ == '__main__':
    main()
