#!/usr/bin/env python3
"""
Fix corrupted LaTeX in principia-metaphysica-paper.html
where backslashes were removed from LaTeX commands.
"""

import re

def fix_latex_backslashes(content):
    """
    Fix corrupted LaTeX in HTML where backslashes were replaced with
    tab/form-feed characters or simply removed.

    This happens when text processing corrupts the backslash character.
    """

    # Track changes
    changes = []
    original = content

    # Strategy: Clean within math mode blocks only (between $ or $$)
    # This is safer than trying to fix individual patterns

    def clean_math_block(match):
        """Clean a single math mode block"""
        math_content = match.group(0)
        original_math = math_content

        # CRITICAL FIX: Backslashes got corrupted to \f (form feed) and \t (tab)
        # For example: \frac became \f\frac, \text became \t\text
        # We need to replace these corrupted patterns

        # Fix \f\f -> \  (doubled form feed before command)
        math_content = re.sub(r'\\f\\f', r'\\', math_content)

        # Fix \t\t -> \  (doubled tab before command)
        math_content = re.sub(r'\\t\\t', r'\\', math_content)

        # Fix \f -> \  (single form feed)
        math_content = re.sub(r'\\f(?=\\[a-z])', r'', math_content)

        # Fix \t -> \  (single tab)
        math_content = re.sub(r'\\t(?=\\[a-z])', r'', math_content)

        # Remove any remaining tab and form-feed characters (not escaped)
        math_content = math_content.replace('\t', '')
        math_content = math_content.replace('\x0c', '')
        math_content = math_content.replace('\x0b', '')

        # Fix common missing backslash patterns
        # These patterns look for the command name without a preceding backslash
        # We need to be careful not to match when preceded by \

        # Fix \frac
        math_content = re.sub(r'(?<!\\)frac\{', r'\\frac{', math_content)

        # Fix \text
        math_content = re.sub(r'(?<!\\)text\{', r'\\text{', math_content)

        # Fix \times
        math_content = re.sub(r'(?<!\\)times\b', r'\\times', math_content)

        # Fix \mathrm
        math_content = re.sub(r'(?<!\\)mathrm\{', r'\\mathrm{', math_content)

        # Fix \mathcal
        math_content = re.sub(r'(?<!\\)mathcal\{', r'\\mathcal{', math_content)

        # Fix \left and \right
        math_content = re.sub(r'(?<!\\)left\b', r'\\left', math_content)
        math_content = re.sub(r'(?<!\\)right\b', r'\\right', math_content)

        # Fix common Greek letters
        for greek in ['alpha', 'beta', 'gamma', 'delta', 'epsilon', 'theta',
                      'lambda', 'mu', 'nu', 'pi', 'rho', 'sigma', 'tau',
                      'phi', 'chi', 'psi', 'omega', 'Delta', 'Omega', 'Sigma']:
            math_content = re.sub(rf'(?<!\\){greek}\b', rf'\\{greek}', math_content)

        # Fix other common commands
        for cmd in ['sqrt', 'cdot', 'partial', 'nabla', 'approx', 'sim',
                    'rightarrow', 'leftarrow', 'infty', 'sum', 'int', 'prod']:
            math_content = re.sub(rf'(?<!\\){cmd}\b', rf'\\{cmd}', math_content)

        # CRITICAL FIX 2: Fix merged commands where spaces were removed
        # e.g., \timesrac -> \times \frac, \timesc -> \times c
        math_content = re.sub(r'\\times([a-z])', r'\\times \1', math_content)
        math_content = re.sub(r'\\text([a-z])', r'\\text \1', math_content)
        math_content = re.sub(r'\\frac([a-z])', r'\\frac \1', math_content)

        # Fix specific merged patterns
        math_content = re.sub(r'\\timesrac\{', r'\\times \\frac{', math_content)
        math_content = re.sub(r'\\timesc', r'\\times c', math_content)
        math_content = re.sub(r'\\timesv', r'\\times v', math_content)

        return math_content

    # Process display math ($$...$$)
    original_content = content
    content = re.sub(r'\$\$[^$]+\$\$', clean_math_block, content, flags=re.DOTALL)
    if content != original_content:
        count = len(re.findall(r'\$\$[^$]+\$\$', original_content, re.DOTALL))
        changes.append(f"Cleaned {count} display math blocks ($$...$$)")
        original_content = content

    # Process inline math ($...$)
    content = re.sub(r'\$[^$]+\$', clean_math_block, content, flags=re.DOTALL)
    if content != original_content:
        count = len(re.findall(r'\$[^$]+\$', original_content, re.DOTALL))
        changes.append(f"Cleaned {count} inline math blocks ($...$)")

    return content, changes


def main():
    html_file = 'principia-metaphysica-paper.html'

    print("Reading HTML file...")
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()

    print("Fixing LaTeX backslashes...")
    fixed_content, changes = fix_latex_backslashes(content)

    if not changes:
        print("No changes needed!")
        return

    print("\nChanges made:")
    for change in changes:
        print(f"  - {change}")

    # Write backup
    backup_file = html_file + '.backup'
    print(f"\nCreating backup: {backup_file}")
    with open(backup_file, 'w', encoding='utf-8') as f:
        f.write(content)

    # Write fixed version
    print(f"Writing fixed version: {html_file}")
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(fixed_content)

    print("\nDone! LaTeX should now render correctly.")
    print("  If you need to revert, restore from:", backup_file)


if __name__ == '__main__':
    main()
