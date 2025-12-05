"""
Comprehensive Centralization Validator

This script validates that ALL content has been properly migrated to the
centralized content management system, ensuring:

1. All pages reference sections_content.py topics
2. All numerical values use PM.* references (not hardcoded)
3. No orphaned HTML files or broken links
4. All formulas/panels/info are in topic sections (not standalone)
5. Single source of truth architecture is complete

Copyright (c) 2025 Andrew Keith Watts. All rights reserved.
"""

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

from pathlib import Path
import re
import json
from bs4 import BeautifulSoup
from typing import Dict, List, Set, Tuple
from collections import defaultdict

# Import our centralized system
try:
    from sections_content import SECTIONS, get_required_values
except ImportError:
    print("ERROR: Cannot import sections_content.py")
    sys.exit(1)

class CentralizationValidator:
    def __init__(self):
        self.root = Path('.')
        self.results = {
            'pm_references': {'valid': [], 'hardcoded': [], 'invalid': []},
            'topic_integration': {'integrated': [], 'orphaned_content': []},
            'file_status': {'defined': [], 'orphaned': [], 'broken_links': []},
            'formulas': {'in_topics': [], 'hardcoded': []},
            'panels': {'in_topics': [], 'hardcoded': []},
            'statistics': {}
        }

        # Get all defined pages from sections_content.py
        self.defined_pages = self._get_defined_pages()

        # Common hardcoded number patterns to detect
        self.number_patterns = [
            r'\b\d+\.\d+e[+-]?\d+\b',  # Scientific notation
            r'\b\d+\.\d{2,}\b',         # Multi-decimal numbers
            r'\b[0-9]{2,}\.[0-9]+\b',   # Large decimals
        ]

    def _get_defined_pages(self) -> Set[str]:
        """Extract all page URLs defined in sections_content.py"""
        pages = set()
        for section_data in SECTIONS.values():
            for page in section_data.get('pages', []):
                file_path = page.get('file', '')
                if file_path:
                    # Convert URL to local path
                    local_path = file_path.replace('https://www.metaphysicæ.com/', '')
                    pages.add(local_path)
        return pages

    def validate_pm_references(self, html_file: Path) -> Dict:
        """Check that all numerical values use PM.* references"""
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()

        soup = BeautifulSoup(content, 'html.parser')

        results = {
            'file': str(html_file),
            'pm_refs': [],
            'hardcoded_numbers': [],
            'suspicious_values': []
        }

        # Find all PM references (data-category and data-param attributes)
        pm_elements = soup.find_all(attrs={'data-category': True, 'data-param': True})
        for elem in pm_elements:
            cat = elem.get('data-category')
            param = elem.get('data-param')
            results['pm_refs'].append(f"PM.{cat}.{param}")

        # Find hardcoded numbers in text content
        # Exclude script tags and style tags
        for tag in soup.find_all(['script', 'style']):
            tag.decompose()

        text_content = soup.get_text()

        # Look for scientific notation and precise decimals
        for pattern in self.number_patterns:
            matches = re.findall(pattern, text_content)
            for match in matches:
                # Exclude common non-physics numbers (years, page numbers, etc.)
                if self._is_suspicious_number(match):
                    results['hardcoded_numbers'].append(match)

        # Find spans/divs with numerical content but no PM reference
        for tag in soup.find_all(['span', 'div', 'td', 'p']):
            if not tag.get('data-category'):
                text = tag.get_text(strip=True)
                for pattern in self.number_patterns:
                    if re.search(pattern, text):
                        # Check if this element is inside a PM-referenced parent
                        parent_has_pm = any(
                            p.get('data-category') for p in tag.parents
                        )
                        if not parent_has_pm:
                            results['suspicious_values'].append({
                                'tag': tag.name,
                                'text': text[:100],  # First 100 chars
                                'class': tag.get('class', [])
                            })

        return results

    def _is_suspicious_number(self, num_str: str) -> bool:
        """Determine if a number is likely a physics value (not year/page/etc)"""
        try:
            num = float(num_str)
            # Exclude common non-physics numbers
            if 1900 <= num <= 2100:  # Years
                return False
            if num.is_integer() and num < 100:  # Small integers (likely counts)
                return False
            if 'e' in num_str.lower():  # Scientific notation is suspicious
                return True
            if len(num_str.split('.')[-1]) > 2:  # More than 2 decimals
                return True
            return False
        except:
            return False

    def validate_topic_integration(self, html_file: Path) -> Dict:
        """Check that content is organized into topic sections"""
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()

        soup = BeautifulSoup(content, 'html.parser')

        results = {
            'file': str(html_file),
            'topic_sections': [],
            'orphaned_content': []
        }

        # Find all elements with topic IDs
        topic_elements = soup.find_all(id=True)
        for elem in topic_elements:
            topic_id = elem.get('id')
            # Check if this ID matches our topic structure
            if self._is_valid_topic_id(topic_id):
                results['topic_sections'].append(topic_id)

        # Find content blocks outside topic sections
        # Look for cards, sections, panels not under a topic heading
        for tag in soup.find_all(['div', 'section'], class_=True):
            classes = tag.get('class', [])
            # Check for common content containers
            if any(c in ['card', 'panel', 'detail-section', 'info-box'] for c in classes):
                # Check if this element is under a topic heading
                parent_has_topic = self._has_topic_ancestor(tag)
                if not parent_has_topic:
                    results['orphaned_content'].append({
                        'classes': classes,
                        'text': tag.get_text(strip=True)[:100],
                        'has_formula': bool(tag.find(['math', 'span'], class_='formula'))
                    })

        return results

    def _is_valid_topic_id(self, topic_id: str) -> bool:
        """Check if an ID matches our topic naming convention"""
        # Topic IDs should be descriptive snake_case or kebab-case
        # Not generic like 'section1', 'div2', etc.
        if not topic_id:
            return False
        if re.match(r'^(div|section|span|p)\d+$', topic_id):
            return False
        if len(topic_id) < 3:
            return False
        return True

    def _has_topic_ancestor(self, tag) -> bool:
        """Check if tag is nested under a heading with a topic ID"""
        for parent in tag.parents:
            if parent.name in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
                if parent.get('id') and self._is_valid_topic_id(parent.get('id')):
                    return True
            if parent.name == 'section' and parent.get('id'):
                if self._is_valid_topic_id(parent.get('id')):
                    return True
        return False

    def find_orphaned_files(self) -> Dict:
        """Find HTML files not referenced in sections_content.py"""
        results = {
            'orphaned_html': [],
            'all_html_files': [],
            'defined_in_sections': list(self.defined_pages)
        }

        # Find all HTML files
        for html_file in self.root.glob('**/*.html'):
            # Skip test files, templates, components
            if any(x in str(html_file) for x in ['test', 'template', 'component', 'node_modules']):
                continue

            rel_path = str(html_file.relative_to(self.root)).replace('\\', '/')
            results['all_html_files'].append(rel_path)

            # Check if this file is defined in sections_content.py
            if rel_path not in self.defined_pages:
                # Also check without trailing paths
                if not any(defined.endswith(html_file.name) for defined in self.defined_pages):
                    results['orphaned_html'].append(rel_path)

        return results

    def find_broken_links(self, html_file: Path) -> List[str]:
        """Find broken internal links in HTML file"""
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()

        soup = BeautifulSoup(content, 'html.parser')
        broken = []

        # Find all internal links
        for link in soup.find_all('a', href=True):
            href = link['href']
            # Skip external links, anchors, mailto, etc.
            if href.startswith(('http', 'mailto:', '#', 'javascript:')):
                continue

            # Resolve relative path
            link_path = (html_file.parent / href).resolve()
            if not link_path.exists():
                broken.append(href)

        return broken

    def validate_formulas(self, html_file: Path) -> Dict:
        """Check that formulas are integrated into topic sections"""
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()

        soup = BeautifulSoup(content, 'html.parser')

        results = {
            'file': str(html_file),
            'formulas_in_topics': [],
            'formulas_orphaned': []
        }

        # Find all formula elements (math tags, formula classes, LaTeX)
        formula_selectors = [
            soup.find_all('math'),
            soup.find_all(class_=re.compile(r'formula|equation|latex')),
            soup.find_all('span', attrs={'data-formula': True})
        ]

        for formula_list in formula_selectors:
            for formula in formula_list:
                has_topic = self._has_topic_ancestor(formula)
                formula_text = formula.get_text(strip=True)[:50]

                if has_topic:
                    results['formulas_in_topics'].append(formula_text)
                else:
                    results['formulas_orphaned'].append(formula_text)

        return results

    def run_full_validation(self) -> Dict:
        """Run all validation checks"""
        print("=" * 80)
        print("COMPREHENSIVE CENTRALIZATION VALIDATION")
        print("=" * 80)
        print()

        # First, regenerate constants to ensure latest
        print("Step 1: Regenerating theory-constants-enhanced.js...")
        import generate_enhanced_constants
        print("✓ Constants regenerated\n")

        # Get all HTML files to check
        html_files = []
        for pattern in ['*.html', 'sections/*.html', 'foundations/*.html', 'diagrams/*.html']:
            html_files.extend(self.root.glob(pattern))

        # Remove duplicates and test files
        html_files = [f for f in set(html_files) if 'test' not in str(f)]

        print(f"Step 2: Validating {len(html_files)} HTML files...")
        print()

        # Validate each file
        for html_file in html_files:
            print(f"  Checking {html_file.name}...")

            # PM references
            pm_results = self.validate_pm_references(html_file)
            self.results['pm_references']['valid'].extend(pm_results['pm_refs'])
            self.results['pm_references']['hardcoded'].extend(
                [(str(html_file), num) for num in pm_results['hardcoded_numbers']]
            )

            # Topic integration
            topic_results = self.validate_topic_integration(html_file)
            self.results['topic_integration']['integrated'].extend(topic_results['topic_sections'])
            self.results['topic_integration']['orphaned_content'].extend(
                [(str(html_file), content) for content in topic_results['orphaned_content']]
            )

            # Broken links
            broken = self.find_broken_links(html_file)
            if broken:
                self.results['file_status']['broken_links'].append({
                    'file': str(html_file),
                    'broken': broken
                })

            # Formulas
            formula_results = self.validate_formulas(html_file)
            self.results['formulas']['in_topics'].extend(formula_results['formulas_in_topics'])
            self.results['formulas']['hardcoded'].extend(
                [(str(html_file), f) for f in formula_results['formulas_orphaned']]
            )

        print()
        print("Step 3: Finding orphaned files...")
        orphaned_results = self.find_orphaned_files()
        self.results['file_status']['orphaned'] = orphaned_results['orphaned_html']
        self.results['file_status']['defined'] = orphaned_results['defined_in_sections']

        print()
        print("Step 4: Calculating statistics...")
        self._calculate_statistics()

        return self.results

    def _calculate_statistics(self):
        """Calculate summary statistics"""
        self.results['statistics'] = {
            'total_pm_references': len(set(self.results['pm_references']['valid'])),
            'total_hardcoded_numbers': len(self.results['pm_references']['hardcoded']),
            'total_topic_sections': len(set(self.results['topic_integration']['integrated'])),
            'total_orphaned_content': len(self.results['topic_integration']['orphaned_content']),
            'total_orphaned_files': len(self.results['file_status']['orphaned']),
            'total_broken_links': sum(len(x['broken']) for x in self.results['file_status']['broken_links']),
            'formulas_integrated': len(self.results['formulas']['in_topics']),
            'formulas_orphaned': len(self.results['formulas']['hardcoded']),
            'centralization_score': 0.0
        }

        # Calculate centralization score (0-100)
        total_content = (
            self.results['statistics']['total_topic_sections'] +
            self.results['statistics']['total_orphaned_content']
        )
        if total_content > 0:
            integrated_ratio = self.results['statistics']['total_topic_sections'] / total_content
        else:
            integrated_ratio = 1.0

        total_formulas = (
            self.results['statistics']['formulas_integrated'] +
            self.results['statistics']['formulas_orphaned']
        )
        if total_formulas > 0:
            formula_ratio = self.results['statistics']['formulas_integrated'] / total_formulas
        else:
            formula_ratio = 1.0

        # Score components
        score = 0
        score += integrated_ratio * 40  # 40 points for topic integration
        score += formula_ratio * 30     # 30 points for formula integration
        score += (1 - min(1, self.results['statistics']['total_orphaned_files'] / 10)) * 20  # 20 points for file organization
        score += (1 - min(1, self.results['statistics']['total_broken_links'] / 10)) * 10    # 10 points for link integrity

        self.results['statistics']['centralization_score'] = round(score, 1)

    def generate_report(self, output_file: str = 'CENTRALIZATION_VALIDATION_REPORT.md'):
        """Generate detailed markdown report"""
        stats = self.results['statistics']

        report = f"""# Centralization Validation Report

Generated: {Path(output_file).stem}

## Executive Summary

**Centralization Score: {stats['centralization_score']}/100**

{'🟢 EXCELLENT' if stats['centralization_score'] >= 90 else '🟡 GOOD' if stats['centralization_score'] >= 70 else '🟠 NEEDS WORK' if stats['centralization_score'] >= 50 else '🔴 CRITICAL'}

## Key Metrics

| Metric | Count | Status |
|--------|-------|--------|
| PM References | {stats['total_pm_references']} | {'✅' if stats['total_pm_references'] > 50 else '⚠️'} |
| Hardcoded Numbers | {stats['total_hardcoded_numbers']} | {'✅' if stats['total_hardcoded_numbers'] < 50 else '⚠️' if stats['total_hardcoded_numbers'] < 200 else '🔴'} |
| Topic Sections | {stats['total_topic_sections']} | {'✅' if stats['total_topic_sections'] > 100 else '⚠️'} |
| Orphaned Content Blocks | {stats['total_orphaned_content']} | {'✅' if stats['total_orphaned_content'] == 0 else '⚠️' if stats['total_orphaned_content'] < 20 else '🔴'} |
| Orphaned HTML Files | {stats['total_orphaned_files']} | {'✅' if stats['total_orphaned_files'] == 0 else '⚠️'} |
| Broken Links | {stats['total_broken_links']} | {'✅' if stats['total_broken_links'] == 0 else '🔴'} |
| Formulas (Integrated) | {stats['formulas_integrated']} | {'✅' if stats['formulas_integrated'] > stats['formulas_orphaned'] else '⚠️'} |
| Formulas (Orphaned) | {stats['formulas_orphaned']} | {'✅' if stats['formulas_orphaned'] == 0 else '⚠️'} |

---

## 1. PM Reference Analysis

### Valid PM References Found
Total unique PM references: **{stats['total_pm_references']}**

Sample of PM references in use:
"""
        # Show unique PM references
        unique_refs = sorted(set(self.results['pm_references']['valid']))[:20]
        for ref in unique_refs:
            report += f"\n- `{ref}`"

        if len(unique_refs) == 20:
            report += f"\n- ... and {stats['total_pm_references'] - 20} more"

        report += f"""

### Hardcoded Numbers Detected
Total hardcoded numbers: **{stats['total_hardcoded_numbers']}**

"""

        if stats['total_hardcoded_numbers'] > 0:
            report += "⚠️ **ACTION REQUIRED**: Replace these hardcoded values with PM references\n\n"

            # Group by file
            by_file = defaultdict(list)
            for file_path, num in self.results['pm_references']['hardcoded'][:50]:
                by_file[Path(file_path).name].append(num)

            for filename, numbers in sorted(by_file.items()):
                report += f"\n**{filename}**: {len(numbers)} hardcoded numbers\n"
                for num in numbers[:5]:
                    report += f"  - `{num}`\n"
                if len(numbers) > 5:
                    report += f"  - ... and {len(numbers) - 5} more\n"
        else:
            report += "✅ **EXCELLENT**: No hardcoded numbers detected!\n"

        report += f"""

---

## 2. Topic Integration Analysis

### Topic Sections Implemented
Total topic sections: **{stats['total_topic_sections']}**

### Orphaned Content Blocks
Total orphaned blocks: **{stats['total_orphaned_content']}**

"""

        if stats['total_orphaned_content'] > 0:
            report += "⚠️ **ACTION REQUIRED**: Integrate these content blocks into topic sections\n\n"

            # Group by file
            by_file = defaultdict(list)
            for file_path, content in self.results['topic_integration']['orphaned_content'][:30]:
                by_file[Path(file_path).name].append(content)

            for filename, blocks in sorted(by_file.items()):
                report += f"\n**{filename}**: {len(blocks)} orphaned blocks\n"
                for block in blocks[:3]:
                    report += f"  - Classes: `{block['classes']}` - Text: {block['text'][:60]}...\n"
                if len(blocks) > 3:
                    report += f"  - ... and {len(blocks) - 3} more\n"
        else:
            report += "✅ **EXCELLENT**: All content is integrated into topic sections!\n"

        report += f"""

---

## 3. File Organization

### Defined Pages (in sections_content.py)
Total: **{len(self.results['file_status']['defined'])}**

"""
        for page in sorted(self.results['file_status']['defined']):
            report += f"- {page}\n"

        report += f"""

### Orphaned HTML Files
Total: **{stats['total_orphaned_files']}**

"""

        if stats['total_orphaned_files'] > 0:
            report += "⚠️ **ACTION REQUIRED**: Add these files to sections_content.py or document why they're excluded\n\n"
            for orphan in sorted(self.results['file_status']['orphaned']):
                report += f"- `{orphan}`\n"
        else:
            report += "✅ **EXCELLENT**: All HTML files are defined in sections_content.py!\n"

        report += """

---

## 4. Link Integrity

"""

        if stats['total_broken_links'] > 0:
            report += f"🔴 **CRITICAL**: {stats['total_broken_links']} broken links detected\n\n"
            for item in self.results['file_status']['broken_links']:
                report += f"\n**{Path(item['file']).name}**:\n"
                for link in item['broken']:
                    report += f"  - `{link}`\n"
        else:
            report += "✅ **EXCELLENT**: No broken links detected!\n"

        report += f"""

---

## 5. Formula Integration

### Formulas in Topic Sections
Total: **{stats['formulas_integrated']}**

### Orphaned Formulas
Total: **{stats['formulas_orphaned']}**

"""

        if stats['formulas_orphaned'] > 0:
            report += "⚠️ **ACTION REQUIRED**: Integrate these formulas into topic sections\n\n"

            # Group by file
            by_file = defaultdict(list)
            for file_path, formula in self.results['formulas']['hardcoded'][:30]:
                by_file[Path(file_path).name].append(formula)

            for filename, formulas in sorted(by_file.items()):
                report += f"\n**{filename}**: {len(formulas)} orphaned formulas\n"
                for f in formulas[:3]:
                    report += f"  - `{f}`\n"
                if len(formulas) > 3:
                    report += f"  - ... and {len(formulas) - 3} more\n"
        else:
            report += "✅ **EXCELLENT**: All formulas are integrated into topic sections!\n"

        report += """

---

## Recommendations

### Priority 1: Critical Issues
"""

        if stats['total_broken_links'] > 0:
            report += f"- 🔴 Fix {stats['total_broken_links']} broken links\n"

        if stats['total_hardcoded_numbers'] > 200:
            report += f"- 🔴 Replace {stats['total_hardcoded_numbers']} hardcoded numbers with PM references\n"

        if stats['total_orphaned_content'] > 50:
            report += f"- 🔴 Integrate {stats['total_orphaned_content']} orphaned content blocks\n"

        report += """
### Priority 2: Important Improvements
"""

        if stats['total_orphaned_files'] > 0:
            report += f"- 🟡 Document or integrate {stats['total_orphaned_files']} orphaned HTML files\n"

        if stats['formulas_orphaned'] > 0:
            report += f"- 🟡 Integrate {stats['formulas_orphaned']} orphaned formulas\n"

        if 50 <= stats['total_hardcoded_numbers'] <= 200:
            report += f"- 🟡 Replace {stats['total_hardcoded_numbers']} hardcoded numbers with PM references\n"

        report += """
### Priority 3: Nice to Have
- 🟢 Continue expanding topic sections for better organization
- 🟢 Add more PM references for dynamic value population
- 🟢 Document rationale for any intentionally orphaned files

---

## Next Steps

1. **Review this report** and prioritize fixes based on severity
2. **Run migration scripts** for hardcoded numbers → PM references
3. **Integrate orphaned content** into appropriate topic sections
4. **Fix broken links** to ensure site navigation works
5. **Re-run validation** to verify improvements

---

*Report generated by validate_centralization.py*

Copyright (c) 2025 Andrew Keith Watts. All rights reserved.
"""

        # Write report
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(report)

        print(f"\n✅ Report generated: {output_file}")
        return report

def main():
    validator = CentralizationValidator()
    results = validator.run_full_validation()

    print()
    print("=" * 80)
    print("VALIDATION COMPLETE")
    print("=" * 80)
    print()
    print(f"Centralization Score: {results['statistics']['centralization_score']}/100")
    print()
    print("Key Findings:")
    print(f"  - PM References: {results['statistics']['total_pm_references']}")
    print(f"  - Hardcoded Numbers: {results['statistics']['total_hardcoded_numbers']}")
    print(f"  - Topic Sections: {results['statistics']['total_topic_sections']}")
    print(f"  - Orphaned Content: {results['statistics']['total_orphaned_content']}")
    print(f"  - Orphaned Files: {results['statistics']['total_orphaned_files']}")
    print(f"  - Broken Links: {results['statistics']['total_broken_links']}")
    print()

    # Generate report
    validator.generate_report()

    # Also save JSON for programmatic access
    with open('centralization_validation_results.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print(f"✅ JSON results saved: centralization_validation_results.json")
    print()

if __name__ == '__main__':
    main()
