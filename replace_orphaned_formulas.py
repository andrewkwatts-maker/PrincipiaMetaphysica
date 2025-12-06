"""
Replace Orphaned Formulas with Centralized References

Identifies orphaned formulas in HTML files and replaces them with
references to formula_definitions.py using data-formula-id attributes.

This enables:
- Dynamic formula tooltips
- Consistent formula presentation
- Single source of truth for all formulas
- Easy updates when formulas change

Copyright (c) 2025 Andrew Keith Watts. All rights reserved.
"""

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

import json
import re
from pathlib import Path
from bs4 import BeautifulSoup, NavigableString
from formula_definitions import ALL_FORMULAS

class FormulaReplacer:
    def __init__(self, dry_run=True):
        self.dry_run = dry_run
        self.replacements_made = 0
        self.files_modified = 0

        # Load orphaned formula analysis
        with open('orphaned_formulas_analysis.json', 'r', encoding='utf-8') as f:
            self.orphaned_data = json.load(f)

    def find_formula_match(self, formula_text):
        """
        Find matching formula in formula_definitions.py

        Returns: (formula_id, formula_data) or (None, None)
        """
        formula_text_clean = formula_text.strip().lower()

        # Try exact match first
        for formula_id, formula_data in ALL_FORMULAS.items():
            html_clean = formula_data['html'].lower()
            if formula_text_clean in html_clean or html_clean in formula_text_clean:
                return formula_id, formula_data

        # Try keyword matching for common formulas
        keywords_map = {
            'd_eff': ['d_eff_formula', 'w0_from_d_eff'],
            'w0': ['w0_from_d_eff', 'w_z_evolution', 'desi_validation'],
            'chi_eff': ['chi_eff', 'generation_formula'],
            'n_gen': ['generation_formula'],
            'theta_23': ['theta_23_formula'],
            'theta_12': ['theta_12_formula'],
            'theta_13': ['theta_13_formula'],
            'delta_cp': ['delta_cp_formula'],
            'm_gut': ['m_gut_derivation', 'tau_p_formula'],
            'tau_p': ['tau_p_formula'],
            'br(e': ['br_epi0'],
            'br(k': ['br_knu'],
            'm_kk': ['kk_mass_formula'],
            'thermal time': ['thermal_time_equation'],
            'kms': ['kms_condition'],
            'einstein': ['einstein_field_equations'],
            'clifford': ['cl_26_dimension', 'gamma_decomposition'],
            'gamma': ['gamma_decomposition'],
            'm_x': ['x_boson_mass'],
            'alpha_4': ['alpha_sum', 'alpha_diff'],
        }

        for keyword, formula_ids in keywords_map.items():
            if keyword in formula_text_clean:
                for formula_id in formula_ids:
                    if formula_id in ALL_FORMULAS:
                        return formula_id, ALL_FORMULAS[formula_id]

        return None, None

    def replace_formulas_in_file(self, html_file):
        """Replace orphaned formulas in a single HTML file"""
        with open(html_file, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f.read(), 'html.parser')

        file_replacements = 0

        # Find all equation-box divs
        equation_boxes = soup.find_all('div', class_='equation-box')

        for box in equation_boxes:
            # Skip if already has data-formula-id
            if box.get('data-formula-id'):
                continue

            # Check if under a topic heading
            has_topic = self._has_topic_ancestor(box)
            if has_topic:
                continue  # Don't touch formulas under topics

            # Get formula text
            formula_text = box.get_text(strip=True)

            # Try to find match
            formula_id, formula_data = self.find_formula_match(formula_text)

            if formula_id and formula_data:
                # Replace with centralized reference
                if not self.dry_run:
                    # Add data-formula-id attribute
                    box['data-formula-id'] = formula_id
                    box['data-centralized'] = 'true'

                    # Update content to use formula_data['html']
                    box.clear()
                    box.append(NavigableString(formula_data['html']))

                file_replacements += 1
                print(f"  ✓ Replaced: {formula_text[:60]}...")
                print(f"    → {formula_id}")

        if file_replacements > 0:
            if not self.dry_run:
                with open(html_file, 'w', encoding='utf-8') as f:
                    f.write(str(soup))

            self.replacements_made += file_replacements
            self.files_modified += 1

        return file_replacements

    def _has_topic_ancestor(self, element):
        """Check if element is under a heading with id attribute (topic marker)"""
        parent = element.parent
        while parent:
            if parent.name in ['h2', 'h3', 'h4', 'h5'] and parent.get('id'):
                return True
            parent = parent.parent
        return False

    def process_all_html_files(self):
        """Process all HTML files in the project"""
        print("=" * 80)
        mode = "DRY RUN" if self.dry_run else "LIVE RUN"
        print(f"FORMULA REPLACEMENT - {mode}")
        print("=" * 80)
        print()

        html_files = []

        # Scan for HTML files
        for pattern in ['*.html', 'sections/*.html', 'foundations/*.html']:
            html_files.extend(Path('.').glob(pattern))

        print(f"Scanning {len(html_files)} HTML files...")
        print()

        for html_file in sorted(html_files):
            file_rel = str(html_file).replace('\\', '/')

            # Skip certain files
            if any(skip in file_rel for skip in ['test', 'backup', 'old']):
                continue

            replacements = self.replace_formulas_in_file(html_file)

            if replacements > 0:
                print(f"{file_rel}: {replacements} replacements")
                print()

        print("=" * 80)
        print("SUMMARY")
        print("=" * 80)
        print(f"Total replacements: {self.replacements_made}")
        print(f"Files modified: {self.files_modified}")

        if self.dry_run:
            print()
            print("⚠️  This was a DRY RUN. No files were modified.")
            print("   Run with --live to apply changes.")
        else:
            print()
            print("✅ Changes applied successfully!")

        print("=" * 80)


def main():
    import argparse
    parser = argparse.ArgumentParser(description='Replace orphaned formulas with centralized references')
    parser.add_argument('--live', action='store_true', help='Apply changes (default is dry-run)')
    parser.add_argument('--file', type=str, help='Process a single file instead of all files')
    args = parser.parse_args()

    replacer = FormulaReplacer(dry_run=not args.live)

    if args.file:
        print(f"Processing single file: {args.file}")
        replacements = replacer.replace_formulas_in_file(Path(args.file))
        print(f"Replacements: {replacements}")
    else:
        replacer.process_all_html_files()


if __name__ == '__main__':
    main()
