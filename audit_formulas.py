#!/usr/bin/env python3
"""
Formula Audit Script for Principia Metaphysica
Extracts and catalogs all formulas across the website
"""

import re
import json
from pathlib import Path
from collections import defaultdict
from html.parser import HTMLParser

class FormulaExtractor(HTMLParser):
    """Extract formulas from HTML files"""

    def __init__(self):
        super().__init__()
        self.formulas = []
        self.current_formula = None
        self.in_formula_context = False
        self.in_equation_box = False
        self.in_formula_main = False
        self.in_main_equation = False
        self.formula_contexts = ['equation-box', 'formula-main', 'main-equation',
                                'expandable-formula', 'formula-expansion']
        self.current_tag_stack = []

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        classes = attrs_dict.get('class', '').split()

        # Track context
        if any(ctx in classes for ctx in self.formula_contexts):
            self.in_formula_context = True
            if 'equation-box' in classes:
                self.in_equation_box = True
                self.current_formula = {
                    'type': 'equation-box',
                    'content': '',
                    'has_tooltip': False,
                    'data_category': None,
                    'label': None
                }
            elif 'formula-main' in classes:
                self.in_formula_main = True
                self.current_formula = {
                    'type': 'formula-main',
                    'content': '',
                    'has_tooltip': False,
                    'data_category': None,
                    'label': None
                }
            elif 'main-equation' in classes:
                self.in_main_equation = True
                self.current_formula = {
                    'type': 'main-equation',
                    'content': '',
                    'has_tooltip': False,
                    'data_category': None,
                    'label': None
                }

        # Check for tooltip/hover logic
        if self.current_formula:
            if 'data-category' in attrs_dict:
                self.current_formula['has_tooltip'] = True
                self.current_formula['data_category'] = attrs_dict['data-category']
            if 'class' in attrs_dict and 'formula-var' in attrs_dict['class']:
                self.current_formula['has_tooltip'] = True

        # Track equation labels
        if 'equation-label' in classes and self.current_formula:
            self.current_formula['label_tag'] = True

        self.current_tag_stack.append((tag, attrs_dict))

    def handle_endtag(self, tag):
        if self.current_tag_stack:
            self.current_tag_stack.pop()

        if self.in_equation_box or self.in_formula_main or self.in_main_equation:
            if tag == 'div':
                if self.current_formula:
                    self.formulas.append(self.current_formula)
                    self.current_formula = None
                self.in_equation_box = False
                self.in_formula_main = False
                self.in_main_equation = False
                self.in_formula_context = False

    def handle_data(self, data):
        if self.current_formula:
            # Clean up whitespace but preserve formula content
            cleaned = data.strip()
            if cleaned:
                if self.current_formula['content']:
                    self.current_formula['content'] += ' ' + cleaned
                else:
                    self.current_formula['content'] = cleaned

def extract_key_formulas(html_content, file_path):
    """Extract key formula patterns from HTML"""
    formulas = {
        'file': str(file_path),
        'equation_boxes': [],
        'key_patterns': defaultdict(list),
        'has_hover': False,
        'pm_references': []
    }

    # Use HTMLParser
    parser = FormulaExtractor()
    try:
        parser.feed(html_content)
        formulas['equation_boxes'] = parser.formulas
    except Exception as e:
        print(f"  Warning: Parser error in {file_path}: {e}")

    # Key formula patterns to search for
    patterns = {
        'S_26D': r'S<sub>26D</sub>',
        'S_gravity': r'S<sub>gravity</sub>',
        'Einstein_equations': r'G<sub>&mu;&nu;</sub>.*?T<sub>&mu;&nu;</sub>',
        'PMNS_matrix': r'U<sub>PMNS</sub>',
        'proton_decay': r'&tau;<sub>p</sub>',
        'w(z)': r'w\(z\)',
        'M_Planck': r'M<sub>Pl</sub>',
        'M_star': r'M<sub>\*</sub>',
        'F(R,T,tau)': r'F\(R,T,&tau;\)',
        'Ricci_scalar': r'R<sub>(&mu;&nu;|\d+)</sub>',
        'CKM_matrix': r'U<sub>CKM</sub>',
        'neutrino_mixing': r'&theta;<sub>\d+</sub>',
        'dark_energy_w0': r'w<sub>0</sub>',
        'GUT_scale': r'M<sub>GUT</sub>',
        'Mashiach_field': r'&phi;<sub>M</sub>',
    }

    for pattern_name, pattern in patterns.items():
        matches = re.findall(pattern, html_content)
        if matches:
            formulas['key_patterns'][pattern_name] = len(matches)

    # Check for PM.* references and data-category attributes
    pm_matches = re.findall(r'PM\.\w+', html_content)
    formulas['pm_references'] = list(set(pm_matches))
    formulas['has_hover'] = len(pm_matches) > 0 or 'data-category=' in html_content

    # Count data-category references
    data_category_matches = re.findall(r'data-category="([^"]+)"', html_content)
    formulas['data_categories'] = list(set(data_category_matches))

    return formulas

def audit_all_files():
    """Audit all HTML files for formulas"""

    files_to_audit = [
        'principia-metaphysica-paper.html',
        'sections/geometric-framework.html',
        'sections/cosmology.html',
        'sections/fermion-sector.html',
        'sections/predictions.html',
        'sections/gauge-unification.html',
        'sections/thermal-time.html',
        'sections/pneuma-lagrangian.html',
        'sections/einstein-hilbert-term.html',
    ]

    base_path = Path(__file__).parent
    results = {}

    print("=" * 80)
    print("PRINCIPIA METAPHYSICA FORMULA AUDIT")
    print("=" * 80)

    for file_rel_path in files_to_audit:
        file_path = base_path / file_rel_path

        if not file_path.exists():
            print(f"\n[ERROR] File not found: {file_path}")
            continue

        print(f"\n[FILE] Analyzing: {file_rel_path}")

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                html_content = f.read()

            formulas = extract_key_formulas(html_content, file_path)
            results[file_rel_path] = formulas

            # Print summary
            print(f"  • Equation boxes: {len(formulas['equation_boxes'])}")
            print(f"  • Has hover logic: {formulas['has_hover']}")
            if formulas['pm_references']:
                print(f"  • PM.* references: {len(formulas['pm_references'])}")
            if formulas['data_categories']:
                print(f"  • Data categories: {', '.join(formulas['data_categories'][:3])}...")

            # Print key patterns found
            if formulas['key_patterns']:
                print(f"  • Key formulas found:")
                for pattern, count in sorted(formulas['key_patterns'].items(),
                                            key=lambda x: x[1], reverse=True)[:5]:
                    print(f"    - {pattern}: {count} occurrences")

        except Exception as e:
            print(f"  [ERROR] Error reading {file_path}: {e}")

    return results

def analyze_repetition(results):
    """Analyze which formulas are repeated across files"""

    print("\n" + "=" * 80)
    print("REPEATED FORMULAS ANALYSIS")
    print("=" * 80)

    # Track pattern occurrences across files
    pattern_files = defaultdict(list)

    for file_path, data in results.items():
        for pattern, count in data['key_patterns'].items():
            if count > 0:
                pattern_files[pattern].append((file_path, count))

    # Print most repeated formulas
    print("\n[REPEAT] Formulas appearing in multiple files:")
    for pattern, files in sorted(pattern_files.items(),
                                 key=lambda x: len(x[1]), reverse=True):
        if len(files) > 1:
            print(f"\n  • {pattern}: appears in {len(files)} files")
            for file_path, count in files:
                file_name = file_path.split('/')[-1]
                print(f"    - {file_name}: {count}x")

def analyze_hover_coverage(results):
    """Analyze which formulas have hover/tooltip logic"""

    print("\n" + "=" * 80)
    print("HOVER/TOOLTIP COVERAGE ANALYSIS")
    print("=" * 80)

    files_with_hover = []
    files_without_hover = []

    for file_path, data in results.items():
        file_name = file_path.split('/')[-1]
        if data['has_hover']:
            files_with_hover.append(file_name)
        else:
            files_without_hover.append(file_name)

    print(f"\n[HOVER+] Files WITH hover/tooltip logic ({len(files_with_hover)}):")
    for file_name in files_with_hover:
        print(f"  • {file_name}")

    if files_without_hover:
        print(f"\n[HOVER-] Files WITHOUT hover/tooltip logic ({len(files_without_hover)}):")
        for file_name in files_without_hover:
            print(f"  • {file_name}")

def generate_recommendations(results):
    """Generate recommendations for centralized formula database"""

    print("\n" + "=" * 80)
    print("RECOMMENDATIONS FOR CENTRALIZED FORMULA DATABASE")
    print("=" * 80)

    # Count total formulas
    total_equation_boxes = sum(len(data['equation_boxes']) for data in results.values())
    total_patterns = sum(sum(data['key_patterns'].values()) for data in results.values())

    print(f"\n[STATS] Statistics:")
    print(f"  • Total equation boxes: {total_equation_boxes}")
    print(f"  • Total formula instances: {total_patterns}")
    print(f"  • Files analyzed: {len(results)}")

    # Identify most frequently repeated
    pattern_files = defaultdict(list)
    for file_path, data in results.items():
        for pattern, count in data['key_patterns'].items():
            if count > 0:
                pattern_files[pattern].append((file_path, count))

    print("\n[PRIORITY] Priority formulas for centralization (appear in 3+ files):")
    priority = []
    for pattern, files in sorted(pattern_files.items(),
                                 key=lambda x: len(x[1]), reverse=True):
        if len(files) >= 3:
            total_occurrences = sum(count for _, count in files)
            priority.append((pattern, len(files), total_occurrences))
            print(f"  • {pattern}: {len(files)} files, {total_occurrences} total occurrences")

    print("\n[RECOMMEND] Recommended Structure:")
    print("  See formula_centralized_database.js for recommended implementation")
    print("  Key categories:")
    print("    - actions (S_26D, S_gravity, etc.)")
    print("    - gravity (Einstein equations, Ricci, etc.)")
    print("    - scales (M_Planck, M_GUT, M_star)")
    print("    - cosmology (w(z), w0, Mashiach field)")
    print("    - particles (PMNS, CKM, neutrino mixing)")
    print("    - predictions (proton decay, etc.)")

def main():
    """Main execution"""
    results = audit_all_files()

    if results:
        analyze_repetition(results)
        analyze_hover_coverage(results)
        generate_recommendations(results)

        # Save results to JSON
        output_path = Path(__file__).parent / 'formula_audit_results.json'
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2)

        print(f"\n[SAVED] Full results saved to: {output_path}")

    print("\n" + "=" * 80)
    print("AUDIT COMPLETE")
    print("=" * 80)

if __name__ == '__main__':
    main()
