#!/usr/bin/env python3
"""
fix_latex_escaping.py - Fix double-escaped LaTeX backslashes in HTML files

This script fixes patterns like \\( to \( for proper MathJax rendering.

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.
"""

import re
from pathlib import Path


def fix_latex_escaping(filepath: Path) -> tuple[int, int]:
    """
    Fix double-escaped LaTeX backslashes.

    Returns:
        Tuple of (fixes_made, total_latex_commands)
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content
    fixes_made = 0

    # Pattern: \\( followed by LaTeX content followed by \\)
    # This captures inline math with double-escaped delimiters
    # We need to be careful to only fix the double-escaped ones, not the correct single-escaped ones

    # The file contains literal \\ followed by (
    # In regex, to match literal \\, we need \\\\
    # And to match literal \, we need \\

    # Fix double-escaped inline math delimiters
    # Match \\( that's not preceded by another backslash
    pattern_open = r'(?<!\\)\\\\\\('  # matches \\ followed by ( but not \\\ followed by (
    pattern_close = r'(?<!\\)\\\\\\)'  # matches \\ followed by ) but not \\\ followed by )

    # Actually, simpler approach: just replace literal \\\\ with \\
    # But we need to be more surgical

    # List of LaTeX commands that should NOT be double-escaped
    latex_commands = [
        'sigma', 'alpha', 'beta', 'gamma', 'delta', 'epsilon', 'zeta', 'eta',
        'theta', 'iota', 'kappa', 'lambda', 'mu', 'nu', 'xi', 'pi', 'rho',
        'tau', 'upsilon', 'phi', 'chi', 'psi', 'omega',
        'Gamma', 'Delta', 'Theta', 'Lambda', 'Xi', 'Pi', 'Sigma', 'Upsilon',
        'Phi', 'Psi', 'Omega',
        'text', 'frac', 'sqrt', 'sum', 'prod', 'int', 'partial',
        'approx', 'neq', 'leq', 'geq', 'in', 'notin', 'subset', 'supset',
        'times', 'cdot', 'pm', 'mp', 'div',
        'infty', 'nabla', 'hbar', 'ell',
        'dot', 'ddot', 'hat', 'bar', 'vec', 'tilde',
        'left', 'right', 'big', 'Big', 'bigg', 'Bigg',
        'begin', 'end',
        '*',  # for Hodge dual \*
    ]

    # Fix: \\\\command -> \\command (where command is a known LaTeX command)
    for cmd in latex_commands:
        # Match \\\\cmd but not \\\\\cmd (which would be \\\ followed by \cmd)
        # In the file: \\command appears as two literal backslashes
        old = '\\\\' + cmd
        new = '\\' + cmd
        count = content.count(old)
        if count > 0:
            content = content.replace(old, new)
            fixes_made += count

    # Fix: \\\\( -> \\( and \\\\) -> \\)
    old_open = '\\\\('
    new_open = '\\('
    count_open = content.count(old_open)
    content = content.replace(old_open, new_open)
    fixes_made += count_open

    old_close = '\\\\)'
    new_close = '\\)'
    count_close = content.count(old_close)
    content = content.replace(old_close, new_close)
    fixes_made += count_close

    # Count total LaTeX inline math environments
    total_latex = content.count('\\(') + content.count('$')

    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

    return fixes_made, total_latex


def main():
    project_root = Path(__file__).parent.parent
    paper_file = project_root / 'principia-metaphysica-paper.html'

    if not paper_file.exists():
        print(f"Error: {paper_file} not found")
        return

    print(f"Processing: {paper_file}")
    fixes, total = fix_latex_escaping(paper_file)

    print(f"\nResults:")
    print(f"  Fixes made: {fixes}")
    print(f"  Total LaTeX environments: {total}")

    if fixes > 0:
        print(f"\nFile updated successfully!")
    else:
        print(f"\nNo changes needed.")


if __name__ == '__main__':
    main()
