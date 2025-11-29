#!/usr/bin/env python3
"""
Scan for Old Dimensional Model References

Searches for outdated 13D model terminology and other deprecated terms
that should be updated to the new 26D→14D×2 two-time framework.

OLD MODEL (to be replaced):
- 13D base dimension
- 26D = 13D + 13D decomposition
- References to "shadow" 13D
- Old dimensional flow pathways

NEW MODEL (correct):
- 26D base with (24,2) signature
- 14D×2 = M^14_A ⊗ M^14_B decomposition
- Sp(2,R) gauge symmetry (NOT compactification)
- Correct flow: 26D → 13D (gauge) → 6D (G₂) → 4D (torus)

REPORT ONLY - No automated editing
"""

import re
from pathlib import Path
from typing import Dict, List, Tuple
from collections import defaultdict

class OldDimensionalScanner:
    """Scanner for outdated dimensional model references"""

    # Patterns for old 13D model
    OLD_13D_PATTERNS = [
        (r'\b13D\b', '13D'),
        (r'\b13-D\b', '13-D'),
        (r'\b13\s*dimensional\b', '13 dimensional'),
        (r'\bthirteen-dimensional\b', 'thirteen-dimensional'),
        (r'M\^{?13}?\b', 'M^13 (13D manifold)'),
        (r'\(13,\s*0\)', '(13,0) signature'),
        (r'\(12,\s*1\)', '(12,1) signature (old context)'),
    ]

    # Patterns for incorrect 26D→13D+13D decomposition
    OLD_DECOMP_PATTERNS = [
        (r'26D?\s*=\s*13D?\s*\+\s*13D?', '26D = 13D + 13D'),
        (r'13D?\s*\+\s*13D?\s*=\s*26D?', '13D + 13D = 26D'),
        (r'split.*26.*into.*13', 'split 26 into 13'),
        (r'two.*13D.*spaces', 'two 13D spaces'),
        (r'pair.*of.*13D', 'pair of 13D'),
    ]

    # Patterns for "shadow" terminology (ambiguous - may be gauge or mirror)
    SHADOW_PATTERNS = [
        (r'shadow\s+13D', 'shadow 13D'),
        (r'13D\s+shadow', '13D shadow'),
        (r'shadow\s+universe.*13', 'shadow universe 13D'),
        (r'shadow\s+sector.*13', 'shadow sector 13D'),
    ]

    # Patterns for old dimensional flow
    OLD_FLOW_PATTERNS = [
        (r'26D?\s*→\s*13D?(?!\s*\()', '26D → 13D (without gauge context)'),
        (r'26D?\s*->\s*13D?(?!\s*\()', '26D -> 13D (without gauge context)'),
        (r'compactify.*26.*13', 'compactify 26 to 13'),
        (r'reduce.*26.*13(?!D\s*\()', 'reduce 26 to 13 (without gauge context)'),
    ]

    # Patterns for missing 14D×2 structure
    MISSING_14D_PATTERNS = [
        # Look for 26D discussions WITHOUT 14D×2 mention
        (r'26D(?!.*14D)', '26D (missing 14D×2 context)'),
    ]

    # Patterns for old M-theory references (11D instead of 26D base)
    OLD_MTHEORY_PATTERNS = [
        (r'\b11D\s+M-theory', '11D M-theory (should be 26D)'),
        (r'M-theory.*11D', 'M-theory 11D'),
        (r'eleven-dimensional.*M-theory', 'eleven-dimensional M-theory'),
    ]

    # Patterns for incorrect Sp(2,R) description
    SP2R_CONFUSION_PATTERNS = [
        (r'Sp\(2,\s*R\).*compactif', 'Sp(2,R) compactification (WRONG - it\'s gauge)'),
        (r'compactif.*Sp\(2,\s*R\)', 'compactification Sp(2,R) (WRONG)'),
        (r'Sp\(2,\s*R\).*compact.*13', 'Sp(2,R) compact to 13'),
    ]

    def __init__(self, root_dir: str = '.'):
        self.root_dir = Path(root_dir)
        self.matches = defaultdict(list)
        self.pattern_stats = defaultdict(int)

        # File patterns to include
        self.include_patterns = [
            '**/*.html',
            '**/*.py',
            '**/*.md',
            '**/*.js',
            '**/*.txt',
        ]

        # Directories to exclude
        self.exclude_dirs = {
            '.git', '__pycache__', 'node_modules', '.venv', 'venv',
            '.backup', 'backups'
        }

        # Files to exclude
        self.exclude_files = {
            'scan_old_dimensional_terms.py',
            'scan_v6_references.py',
            'remove_v65_references.py',
            'v6_references_report.txt',
            'v6_scan_output.txt',
            'old_dimensional_report.txt',
        }

    def should_scan(self, file_path: Path) -> bool:
        """Check if file should be scanned"""
        # Check excluded directories
        for parent in file_path.parents:
            if parent.name in self.exclude_dirs:
                return False

        # Check excluded files
        if file_path.name in self.exclude_files:
            return False

        return True

    def scan_file(self, file_path: Path):
        """Scan a single file for old dimensional references"""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()

            matches = []

            for line_num, line in enumerate(lines, 1):
                # Check all pattern categories
                pattern_groups = [
                    ('13D_MODEL', self.OLD_13D_PATTERNS),
                    ('OLD_DECOMP', self.OLD_DECOMP_PATTERNS),
                    ('SHADOW_AMBIGUOUS', self.SHADOW_PATTERNS),
                    ('OLD_FLOW', self.OLD_FLOW_PATTERNS),
                    ('OLD_MTHEORY', self.OLD_MTHEORY_PATTERNS),
                    ('SP2R_CONFUSION', self.SP2R_CONFUSION_PATTERNS),
                ]

                for category, patterns in pattern_groups:
                    for pattern, description in patterns:
                        if re.search(pattern, line, re.IGNORECASE):
                            matches.append((line_num, line.strip(), category, description))
                            self.pattern_stats[description] += 1

            if matches:
                rel_path = str(file_path.relative_to(self.root_dir))
                self.matches[rel_path] = matches

        except Exception as e:
            print(f"[WARNING] Could not scan {file_path}: {e}")

    def scan(self):
        """Scan all files"""
        print("=" * 80)
        print("SCANNING FOR OLD DIMENSIONAL MODEL REFERENCES")
        print("=" * 80)
        print()
        print("OLD MODEL: 13D base, 26D = 13D + 13D")
        print("NEW MODEL: 26D base (24,2), 14D×2 decomposition, Sp(2,R) gauge")
        print()
        print("Scanning...")

        for pattern in self.include_patterns:
            for file_path in self.root_dir.glob(pattern):
                if file_path.is_file() and self.should_scan(file_path):
                    self.scan_file(file_path)

        return self.matches

    def report(self):
        """Print comprehensive report"""
        if not self.matches:
            print("\n[OK] No old dimensional model references found!")
            return

        total_matches = sum(len(m) for m in self.matches.values())

        print(f"\n[REPORT] Found {total_matches} old dimensional model references")
        print(f"         in {len(self.matches)} files")
        print()

        # Pattern breakdown
        print("PATTERN BREAKDOWN:")
        print("-" * 80)
        for pattern in sorted(self.pattern_stats.keys(), key=lambda x: -self.pattern_stats[x]):
            count = self.pattern_stats[pattern]
            # Strip Unicode for console output
            safe_pattern = pattern.encode('ascii', 'ignore').decode('ascii')
            print(f"  {safe_pattern}: {count} occurrences")
        print()

        # Group by file type
        html_files = {}
        python_files = {}
        md_files = {}
        js_files = {}
        other_files = {}

        for file_path, matches in self.matches.items():
            if file_path.endswith('.html'):
                html_files[file_path] = matches
            elif file_path.endswith('.py'):
                python_files[file_path] = matches
            elif file_path.endswith('.md'):
                md_files[file_path] = matches
            elif file_path.endswith('.js'):
                js_files[file_path] = matches
            else:
                other_files[file_path] = matches

        # Report by file type
        for file_type, file_dict, type_name in [
            (html_files, html_files, "HTML FILES"),
            (python_files, python_files, "PYTHON FILES"),
            (js_files, js_files, "JAVASCRIPT FILES"),
            (md_files, md_files, "MARKDOWN FILES"),
            (other_files, other_files, "OTHER FILES"),
        ]:
            if file_dict:
                print(f"\n{type_name} ({len(file_dict)} files, {sum(len(m) for m in file_dict.values())} matches):")
                print("=" * 80)

                for file_path in sorted(file_dict.keys(), key=lambda x: -len(file_dict[x])):
                    matches = file_dict[file_path]
                    print(f"\n{file_path}: {len(matches)} matches")
                    print("-" * 80)

                    # Show first 5 matches
                    for line_num, line_text, category, description in matches[:5]:
                        safe_text = line_text[:120].encode('ascii', 'ignore').decode('ascii')
                        print(f"  Line {line_num}: [{category}] {safe_text}")

                    if len(matches) > 5:
                        print(f"  ... and {len(matches) - 5} more matches")

        # Summary statistics
        print("\n" + "=" * 80)
        print("SUMMARY STATISTICS")
        print("=" * 80)
        print(f"  Total old dimensional references: {total_matches}")
        print(f"  Total files affected: {len(self.matches)}")
        print()
        print("  By file type:")
        print(f"    HTML:     {sum(len(m) for m in html_files.values())} references")
        print(f"    Python:   {sum(len(m) for m in python_files.values())} references")
        print(f"    JavaScript: {sum(len(m) for m in js_files.values())} references")
        print(f"    Markdown: {sum(len(m) for m in md_files.values())} references")
        print(f"    Other:    {sum(len(m) for m in other_files.values())} references")
        print()

        # Category breakdown
        category_counts = defaultdict(int)
        for matches in self.matches.values():
            for _, _, category, _ in matches:
                category_counts[category] += 1

        print("  By category:")
        for category in sorted(category_counts.keys(), key=lambda x: -category_counts[x]):
            count = category_counts[category]
            print(f"    {category}: {count} references")

    def save_detailed_report(self, output_file='old_dimensional_report.txt'):
        """Save detailed report to file"""
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("=" * 80 + "\n")
            f.write("OLD DIMENSIONAL MODEL REFERENCES - DETAILED REPORT\n")
            f.write("=" * 80 + "\n\n")

            f.write("OLD MODEL (to be replaced):\n")
            f.write("- 13D base dimension\n")
            f.write("- 26D = 13D + 13D decomposition\n")
            f.write("- Sp(2,R) as compactification (WRONG)\n\n")

            f.write("NEW MODEL (correct):\n")
            f.write("- 26D base with (24,2) signature\n")
            f.write("- 14D×2 = M^14_A ⊗ M^14_B decomposition\n")
            f.write("- Sp(2,R) as GAUGE symmetry (not compactification)\n")
            f.write("- Flow: 26D → 13D (gauge) → 6D (G₂) → 4D (torus)\n\n")

            f.write("=" * 80 + "\n\n")

            # List all matches by file
            for file_path in sorted(self.matches.keys()):
                matches = self.matches[file_path]
                f.write(f"\n{file_path}: {len(matches)} matches\n")
                f.write("-" * 80 + "\n")

                for line_num, line_text, category, description in matches:
                    f.write(f"Line {line_num} [{category}]:\n")
                    f.write(f"  Pattern: {description}\n")
                    f.write(f"  Content: {line_text}\n\n")

        print(f"\n[OK] Detailed report saved to: {output_file}")

    def generate_cleanup_tasks(self, output_file='old_dimensional_cleanup_tasks.json'):
        """Generate task list for cleanup"""
        import json

        tasks = []

        # Prioritize user-facing files
        priority_map = {
            '.html': 'HIGH',
            '.js': 'HIGH',
            '.py': 'MEDIUM',
            '.md': 'LOW',
        }

        for file_path, matches in self.matches.items():
            file_ext = Path(file_path).suffix
            priority = priority_map.get(file_ext, 'LOW')

            tasks.append({
                'file': file_path,
                'priority': priority,
                'match_count': len(matches),
                'categories': list(set(cat for _, _, cat, _ in matches)),
                'sample_matches': [
                    {
                        'line': line_num,
                        'category': category,
                        'pattern': description,
                    }
                    for line_num, _, category, description in matches[:3]
                ]
            })

        # Sort by priority and match count
        priority_order = {'HIGH': 0, 'MEDIUM': 1, 'LOW': 2}
        tasks.sort(key=lambda x: (priority_order[x['priority']], -x['match_count']))

        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(tasks, f, indent=2)

        print(f"[OK] Cleanup tasks saved to: {output_file}")
        print(f"     HIGH priority: {sum(1 for t in tasks if t['priority'] == 'HIGH')} files")
        print(f"     MEDIUM priority: {sum(1 for t in tasks if t['priority'] == 'MEDIUM')} files")
        print(f"     LOW priority: {sum(1 for t in tasks if t['priority'] == 'LOW')} files")


if __name__ == '__main__':
    scanner = OldDimensionalScanner()
    scanner.scan()
    scanner.report()
    scanner.save_detailed_report()
    scanner.generate_cleanup_tasks()

    print("\n" + "=" * 80)
    print("Scan complete - review the report above and old_dimensional_report.txt")
    print("=" * 80)
