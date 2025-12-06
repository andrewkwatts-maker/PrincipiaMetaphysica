"""
Formula Database Generator

This script audits ALL formulas across the website and creates a centralized
formula database that can be referenced by formula ID.

Copyright (c) 2025 Andrew Keith Watts. All rights reserved.
"""

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

from pathlib import Path
import re
import json
from bs4 import BeautifulSoup
from collections import defaultdict
import hashlib

class FormulaAuditor:
    def __init__(self):
        self.root = Path('.')
        self.formulas = {}
        self.formula_locations = defaultdict(list)
        self.formula_types = {
            'latex': [],
            'mathml': [],
            'unicode': [],
            'html_entity': []
        }

    def extract_formulas_from_file(self, html_file):
        """Extract all formulas from an HTML file"""
        try:
            with open(html_file, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            print(f"  Warning: Error reading {html_file}: {e}")
            return

        soup = BeautifulSoup(content, 'html.parser')
        file_rel = str(html_file.relative_to(self.root)).replace('\', '/')

        # Find LaTeX formulas
        latex_patterns = [
            (r'\$\$([^$]+)\$\$', 'display'),
            (r'\$([^$]+)\$', 'inline'),
        ]

        for pattern, math_type in latex_patterns:
            matches = re.findall(pattern, content, re.DOTALL)
            for match in matches:
                formula_id = self._generate_formula_id(match)
                self._add_formula(formula_id, match, 'latex', math_type, file_rel)

        # Find MathML formulas
        for math_tag in soup.find_all('math'):
            formula_text = str(math_tag)
            formula_id = self._generate_formula_id(formula_text)
            self._add_formula(formula_id, formula_text, 'mathml', 'mathml', file_rel)

        # Find formulas in specific classes
        formula_classes = ['formula', 'equation', 'math', 'latex']
        for cls in formula_classes:
            for elem in soup.find_all(class_=re.compile(cls, re.I)):
                formula_text = elem.get_text(strip=True)
                if formula_text and len(formula_text) > 3:
                    formula_id = self._generate_formula_id(formula_text)
                    self._add_formula(formula_id, formula_text, 'html_class', cls, file_rel)

    def _generate_formula_id(self, formula_text):
        """Generate unique ID for formula"""
        normalized = re.sub(r'\s+', ' ', formula_text.strip())
        normalized = normalized[:200]
        return hashlib.md5(normalized.encode('utf-8')).hexdigest()[:12]

    def _add_formula(self, formula_id, text, formula_type, subtype, location):
        """Add formula to database"""
        if formula_id not in self.formulas:
            self.formulas[formula_id] = {
                'id': formula_id,
                'text': text[:500],
                'type': formula_type,
                'subtype': subtype,
                'locations': [],
                'has_pm_refs': False,
                'pm_refs': []
            }
            self.formula_types[formula_type].append(formula_id)

        if location not in self.formulas[formula_id]['locations']:
            self.formulas[formula_id]['locations'].append(location)

    def run_audit(self):
        """Run complete formula audit"""
        print("=" * 80)
        print("FORMULA DATABASE GENERATOR")
        print("=" * 80)
        
        html_files = []
        for pattern in ['*.html', 'sections/*.html', 'foundations/*.html']:
            html_files.extend(self.root.glob(pattern))

        html_files = [f for f in set(html_files) if 'test' not in str(f)]

        print(f"\nProcessing {len(html_files)} HTML files...")
        for html_file in html_files:
            self.extract_formulas_from_file(html_file)

        print(f"\nTotal unique formulas: {len(self.formulas)}")
        print("\nBy Type:")
        for ftype, fids in self.formula_types.items():
            print(f"  {ftype}: {len(fids)}")

        return self.formulas

    def save_results(self):
        """Save results to JSON"""
        with open('formula_audit_results.json', 'w', encoding='utf-8') as f:
            json.dump(self.formulas, f, indent=2, ensure_ascii=False)
        print(f"\nResults saved: formula_audit_results.json")

def main():
    auditor = FormulaAuditor()
    auditor.run_audit()
    auditor.save_results()

if __name__ == '__main__':
    main()
