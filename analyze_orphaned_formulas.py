"""
Orphaned Formula Analyzer

Extracts all formulas from HTML files, identifies which are orphaned (not under topic IDs),
categorizes them by topic/type, and assesses relevance to v8.4 framework.

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

class FormulaAnalyzer:
    def __init__(self):
        self.root = Path('.')
        self.formulas = defaultdict(list)
        self.orphaned_formulas = []
        self.topic_formulas = []

    def extract_formulas_from_file(self, html_file):
        """Extract all formulas and check if they're under topic headings"""
        try:
            with open(html_file, 'r', encoding='utf-8') as f:
                soup = BeautifulSoup(f.read(), 'html.parser')
        except Exception as e:
            print(f"Error reading {html_file}: {e}")
            return

        file_rel = str(html_file.relative_to(self.root)).replace('\\', '/')

        # Find all formula elements - look for equation-box and detail-formula classes
        formula_elements = []

        # Method 1: Find equation-box divs
        for elem in soup.find_all('div', class_='equation-box'):
            formula_elements.append(('equation-box', elem))

        # Method 2: Find detail-formula spans
        for elem in soup.find_all('span', class_='detail-formula'):
            formula_elements.append(('detail-formula', elem))

        # Method 3: Find math tags
        for elem in soup.find_all('math'):
            formula_elements.append(('mathml', elem))

        for selector_type, elem in formula_elements:
            formula_text = elem.get_text(strip=True)
            if not formula_text or len(formula_text) < 3:
                continue

            # Check if under a topic heading
            has_topic = self._has_topic_ancestor(elem)

            # Categorize by content
            category = self._categorize_formula(formula_text)

            formula_data = {
                'text': formula_text[:200],
                'type': selector_type,
                'file': file_rel,
                'has_topic': has_topic,
                'category': category,
                'html': str(elem)[:500]
            }

            if has_topic:
                self.topic_formulas.append(formula_data)
            else:
                self.orphaned_formulas.append(formula_data)

            self.formulas[category].append(formula_data)

    def _has_topic_ancestor(self, element):
        """Check if element is under a heading with valid topic ID"""
        for parent in element.parents:
            if parent.name in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'section']:
                topic_id = parent.get('id', '')
                if topic_id and self._is_valid_topic_id(topic_id):
                    return True
        return False

    def _is_valid_topic_id(self, topic_id):
        """Check if ID is a valid topic"""
        if not topic_id:
            return False
        if re.match(r'^(div|section|span|p)\d+$', topic_id):
            return False
        if len(topic_id) < 3:
            return False
        return True

    def _categorize_formula(self, text):
        """Categorize formula by mathematical content"""
        text_lower = text.lower()

        # Check for specific patterns
        if any(kw in text_lower for kw in ['action', 'lagrangian', 'integral']):
            return 'action'
        elif any(kw in text_lower for kw in ['metric', 'g_μν', 'tensor']):
            return 'metric'
        elif any(kw in text_lower for kw in ['einstein', 'r_μν', 'ricci']):
            return 'field_equation'
        elif any(kw in text_lower for kw in ['gauge', 'yang-mills', 'so(10)', 'su(']):
            return 'gauge'
        elif any(kw in text_lower for kw in ['w(z)', 'w_0', 'dark energy']):
            return 'dark_energy'
        elif any(kw in text_lower for kw in ['pmns', 'neutrino', 'mixing']):
            return 'neutrino'
        elif any(kw in text_lower for kw in ['proton', 'decay']):
            return 'proton_decay'
        elif any(kw in text_lower for kw in ['dimension', 'd_eff', '26d', '13d']):
            return 'dimension'
        elif any(kw in text_lower for kw in ['generation', 'χ_eff', '144']):
            return 'generation'
        elif any(kw in text_lower for kw in ['euler', 'topology', 'manifold']):
            return 'topology'
        elif any(kw in text_lower for kw in ['thermal', 'kms', 'temperature']):
            return 'thermal'
        else:
            return 'other'

    def get_unique_formulas(self):
        """Get unique formulas by content hash"""
        unique = {}
        for formula_list in self.formulas.values():
            for formula in formula_list:
                normalized = re.sub(r'\s+', ' ', formula['text']).strip().lower()
                formula_hash = hashlib.md5(normalized.encode()).hexdigest()[:12]

                if formula_hash not in unique:
                    unique[formula_hash] = formula
                    formula['count'] = 1
                    formula['hash'] = formula_hash
                else:
                    unique[formula_hash]['count'] += 1

        return list(unique.values())

    def generate_report(self):
        """Generate analysis report"""
        print("=" * 80)
        print("ORPHANED FORMULA ANALYSIS")
        print("=" * 80)
        print()
        total = len(self.topic_formulas) + len(self.orphaned_formulas)
        if total == 0:
            print("No formulas found!")
            return

        print(f"Total formulas found: {total}")
        print(f"  Under topic headings: {len(self.topic_formulas)} ({len(self.topic_formulas)/total*100:.1f}%)")
        print(f"  Orphaned: {len(self.orphaned_formulas)} ({len(self.orphaned_formulas)/total*100:.1f}%)")
        print()

        print("By Category:")
        for category in sorted(self.formulas.keys()):
            count = len(self.formulas[category])
            orphaned_count = sum(1 for f in self.formulas[category] if not f['has_topic'])
            print(f"  {category:20s}: {count:4d} total, {orphaned_count:4d} orphaned")
        print()

        unique = self.get_unique_formulas()
        print(f"Unique formulas (by content): {len(unique)}")
        print()

        orphaned_unique = [f for f in unique if not f.get('has_topic', True)]
        orphaned_unique.sort(key=lambda x: x.get('count', 0), reverse=True)

        print("Most Common Orphaned Formulas:")
        for i, formula in enumerate(orphaned_unique[:20], 1):
            print(f"{i:2d}. [{formula['category']:15s}] Count: {formula.get('count', 1):3d}")
            print(f"    {formula['text'][:100]}")
            print()

        results = {
            'summary': {
                'total': total,
                'orphaned': len(self.orphaned_formulas),
                'under_topics': len(self.topic_formulas),
                'unique': len(unique),
                'unique_orphaned': len(orphaned_unique)
            },
            'by_category': {cat: len(formulas) for cat, formulas in self.formulas.items()},
            'unique_formulas': unique[:100],
            'orphaned_formulas': self.orphaned_formulas[:100]
        }

        with open('orphaned_formulas_analysis.json', 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)

        print("✅ Detailed results saved to: orphaned_formulas_analysis.json")

def main():
    analyzer = FormulaAnalyzer()

    print("Scanning HTML files for formulas...")
    for pattern in ['*.html', 'sections/*.html', 'foundations/*.html']:
        for html_file in Path('.').glob(pattern):
            if 'test' not in str(html_file):
                print(f"  {html_file.name}...")
                analyzer.extract_formulas_from_file(html_file)

    print()
    analyzer.generate_report()

if __name__ == '__main__':
    main()
