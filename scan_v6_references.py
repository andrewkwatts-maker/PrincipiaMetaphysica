"""
scan_v6_references.py - Scan for ANY v6.x version references

This script scans for all v6 version references (v6.0, v6.1, v6.2, v6.3, v6.4, v6.5, v6.6, etc.)
and generates a comprehensive report without making any edits.

Usage:
    python scan_v6_references.py
"""

import os
import re
from pathlib import Path
from typing import List, Tuple, Dict
import json

# Patterns to search for
V6_PATTERNS = [
    r'v6\.\d+',           # v6.0, v6.1, v6.5, etc.
    r'v\s*6\.\d+',        # v 6.5 (with space)
    r'version\s+6\.\d+',  # version 6.5
    r'Version\s+6\.\d+',  # Version 6.5
    r'VERSION\s+6\.\d+',  # VERSION 6.5
]

# File extensions to scan
SCAN_EXTENSIONS = ['.html', '.py', '.md', '.txt', '.csv', '.json', '.js']

# Files to skip
SKIP_FILES = [
    'scan_v6_references.py',
    'remove_v65_references.py',
    'remove_versioning.py',
    '__pycache__',
    '.git',
    'node_modules',
    '.vscode',
]

class V6Scanner:
    def __init__(self, root_dir: str):
        self.root_dir = Path(root_dir)
        self.matches: Dict[str, List[Tuple[int, str, str]]] = {}
        self.version_breakdown: Dict[str, int] = {}

    def scan(self) -> Dict[str, List[Tuple[int, str, str]]]:
        """Scan all files for v6.x references"""
        print("=" * 80)
        print("SCANNING FOR v6.x VERSION REFERENCES")
        print("=" * 80)
        print()

        for file_path in self._get_files():
            self._scan_file(file_path)

        return self.matches

    def _get_files(self) -> List[Path]:
        """Get all files to scan"""
        files = []
        for ext in SCAN_EXTENSIONS:
            files.extend(self.root_dir.rglob(f'*{ext}'))

        # Filter out skipped files
        filtered = []
        for f in files:
            if any(skip in str(f) for skip in SKIP_FILES):
                continue
            filtered.append(f)

        return filtered

    def _scan_file(self, file_path: Path):
        """Scan a single file and return matching lines"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
        except Exception as e:
            return

        matches = []
        for line_num, line in enumerate(lines, 1):
            for pattern in V6_PATTERNS:
                match = re.search(pattern, line, re.IGNORECASE)
                if match:
                    matched_text = match.group(0)
                    matches.append((line_num, line.strip()[:200], matched_text))

                    # Track version breakdown
                    version_key = matched_text.lower()
                    self.version_breakdown[version_key] = self.version_breakdown.get(version_key, 0) + 1
                    break  # Only count each line once

        if matches:
            rel_path = str(file_path.relative_to(self.root_dir))
            self.matches[rel_path] = matches

    def report(self):
        """Print comprehensive report"""
        if not self.matches:
            print("\n[OK] No v6.x version references found!")
            return

        total_matches = sum(len(m) for m in self.matches.values())

        print(f"[REPORT] Found {total_matches} v6.x version references")
        print(f"         in {len(self.matches)} files")
        print()

        # Version breakdown
        print("VERSION BREAKDOWN:")
        print("-" * 80)
        for version in sorted(self.version_breakdown.keys()):
            count = self.version_breakdown[version]
            print(f"  {version}: {count} occurrences")
        print()

        # Group by file type
        html_files = {}
        python_files = {}
        md_files = {}
        other_files = {}

        for file_path, matches in self.matches.items():
            if file_path.endswith('.html'):
                html_files[file_path] = matches
            elif file_path.endswith('.py'):
                python_files[file_path] = matches
            elif file_path.endswith('.md'):
                md_files[file_path] = matches
            else:
                other_files[file_path] = matches

        # Report HTML files
        if html_files:
            print(f"\nHTML FILES ({len(html_files)} files, {sum(len(m) for m in html_files.values())} matches):")
            print("=" * 80)
            for file_path in sorted(html_files.keys(), key=lambda x: -len(html_files[x])):
                matches = html_files[file_path]
                print(f"\n{file_path}: {len(matches)} matches")
                print("-" * 80)

                # Show first 5 matches (with Unicode handling)
                for line_num, line_text, matched_version in matches[:5]:
                    # Strip Unicode for console output
                    safe_text = line_text[:150].encode('ascii', 'ignore').decode('ascii')
                    print(f"  Line {line_num}: [{matched_version}] {safe_text}")

                if len(matches) > 5:
                    print(f"  ... and {len(matches) - 5} more matches")

        # Report Python files
        if python_files:
            print(f"\nPYTHON FILES ({len(python_files)} files, {sum(len(m) for m in python_files.values())} matches):")
            print("=" * 80)
            for file_path in sorted(python_files.keys(), key=lambda x: -len(python_files[x])):
                matches = python_files[file_path]
                print(f"\n{file_path}: {len(matches)} matches")
                print("-" * 80)

                for line_num, line_text, matched_version in matches[:5]:
                    safe_text = line_text[:150].encode('ascii', 'ignore').decode('ascii')
                    print(f"  Line {line_num}: [{matched_version}] {safe_text}")

                if len(matches) > 5:
                    print(f"  ... and {len(matches) - 5} more matches")

        # Report Markdown files
        if md_files:
            print(f"\nMARKDOWN FILES ({len(md_files)} files, {sum(len(m) for m in md_files.values())} matches):")
            print("=" * 80)
            for file_path in sorted(md_files.keys(), key=lambda x: -len(md_files[x])):
                matches = md_files[file_path]
                print(f"  {file_path}: {len(matches)} matches")

        # Report other files
        if other_files:
            print(f"\nOTHER FILES ({len(other_files)} files, {sum(len(m) for m in other_files.values())} matches):")
            print("=" * 80)
            for file_path in sorted(other_files.keys(), key=lambda x: -len(other_files[x])):
                matches = other_files[file_path]
                print(f"  {file_path}: {len(matches)} matches")

    def save_detailed_report(self, output_file: str = 'v6_references_report.txt'):
        """Save detailed report to file"""
        output_path = self.root_dir / output_file

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("=" * 80 + "\n")
            f.write("DETAILED v6.x VERSION REFERENCES REPORT\n")
            f.write("=" * 80 + "\n\n")

            total_matches = sum(len(m) for m in self.matches.values())
            f.write(f"Total matches: {total_matches}\n")
            f.write(f"Total files: {len(self.matches)}\n\n")

            # Version breakdown
            f.write("VERSION BREAKDOWN:\n")
            f.write("-" * 80 + "\n")
            for version in sorted(self.version_breakdown.keys()):
                count = self.version_breakdown[version]
                f.write(f"  {version}: {count} occurrences\n")
            f.write("\n")

            # Detailed file listings
            for file_path in sorted(self.matches.keys()):
                matches = self.matches[file_path]
                f.write("\n" + "=" * 80 + "\n")
                f.write(f"FILE: {file_path} ({len(matches)} matches)\n")
                f.write("=" * 80 + "\n\n")

                for line_num, line_text, matched_version in matches:
                    f.write(f"Line {line_num}: [{matched_version}]\n")
                    f.write(f"  {line_text}\n\n")

        print(f"\n[OK] Detailed report saved to: {output_file}")

    def generate_summary_stats(self):
        """Generate summary statistics"""
        if not self.matches:
            return

        total_matches = sum(len(m) for m in self.matches.values())

        html_count = sum(len(m) for f, m in self.matches.items() if f.endswith('.html'))
        py_count = sum(len(m) for f, m in self.matches.items() if f.endswith('.py'))
        md_count = sum(len(m) for f, m in self.matches.items() if f.endswith('.md'))
        other_count = total_matches - html_count - py_count - md_count

        print("\n" + "=" * 80)
        print("SUMMARY STATISTICS")
        print("=" * 80)
        print(f"  Total v6.x references: {total_matches}")
        print(f"  Total files affected: {len(self.matches)}")
        print()
        print("  By file type:")
        print(f"    HTML:     {html_count} references ({html_count/total_matches*100:.1f}%)")
        print(f"    Python:   {py_count} references ({py_count/total_matches*100:.1f}%)")
        print(f"    Markdown: {md_count} references ({md_count/total_matches*100:.1f}%)")
        print(f"    Other:    {other_count} references ({other_count/total_matches*100:.1f}%)")
        print()
        print("  Most common versions:")
        for i, (version, count) in enumerate(sorted(self.version_breakdown.items(),
                                                     key=lambda x: -x[1])[:5], 1):
            print(f"    {i}. {version}: {count} occurrences")


if __name__ == '__main__':
    root = r'h:\Github\PrincipiaMetaphysica'
    scanner = V6Scanner(root)

    # Scan for references
    scanner.scan()

    # Print report to console
    scanner.report()

    # Generate summary statistics
    scanner.generate_summary_stats()

    # Save detailed report to file
    scanner.save_detailed_report()

    print("\n" + "=" * 80)
    print("Scan complete - review the report above and v6_references_report.txt")
    print("=" * 80)
