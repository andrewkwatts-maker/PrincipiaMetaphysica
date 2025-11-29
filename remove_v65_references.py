"""
remove_v65_references.py - Find and Report v6.5 References

This script scans for v6.5 and MASTERPLAN2 references, then generates
a report for agent-based cleanup to preserve HTML formatting.

Usage:
    python remove_v65_references.py
"""

import os
import re
from pathlib import Path
from typing import List, Tuple, Dict
import json

# Specific patterns to search for
V65_PATTERNS = [
    r'v6\.5',
    r'v\s*6\.5',
    r'version\s+6\.5',
    r'MASTERPLAN2',
    r'Issue\s+[1-6]',
]

# File extensions to scan
SCAN_EXTENSIONS = ['.html', '.py', '.md', '.txt']

# Files to skip
SKIP_FILES = [
    'remove_v65_references.py',
    'remove_versioning.py',
    '__pycache__',
    '.git',
]

class V65Scanner:
    def __init__(self, root_dir: str):
        self.root_dir = Path(root_dir)
        self.file_matches: Dict[str, List[Tuple[int, str]]] = {}

    def scan(self) -> Dict[str, List[Tuple[int, str]]]:
        """Scan all files for v6.5 references"""
        print("Scanning for v6.5 and MASTERPLAN2 references...")
        print("=" * 80)

        for file_path in self._get_files():
            matches = self._scan_file(file_path)
            if matches:
                rel_path = str(file_path.relative_to(self.root_dir))
                self.file_matches[rel_path] = matches

        return self.file_matches

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

    def _scan_file(self, file_path: Path) -> List[Tuple[int, str]]:
        """Scan a single file and return matching lines"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
        except Exception as e:
            return []

        matches = []
        for line_num, line in enumerate(lines, 1):
            for pattern in V65_PATTERNS:
                if re.search(pattern, line, re.IGNORECASE):
                    matches.append((line_num, line.strip()[:200]))  # Limit line length
                    break  # Only count each line once

        return matches

    def report(self):
        """Print report of all matches"""
        if not self.file_matches:
            print("\n[OK] No v6.5 references found!")
            return

        total_lines = sum(len(m) for m in self.file_matches.values())
        print(f"\n[REPORT] Found {total_lines} lines with v6.5/MASTERPLAN2 references")
        print(f"          in {len(self.file_matches)} files\n")

        # Group by file type
        html_files = []
        python_files = []
        other_files = []

        for file_path, matches in sorted(self.file_matches.items()):
            if file_path.endswith('.html'):
                html_files.append((file_path, len(matches)))
            elif file_path.endswith('.py'):
                python_files.append((file_path, len(matches)))
            else:
                other_files.append((file_path, len(matches)))

        if html_files:
            print(f"\nHTML FILES ({len(html_files)} files):")
            print("-" * 80)
            for file_path, count in sorted(html_files, key=lambda x: -x[1]):
                print(f"  {file_path}: {count} matches")

        if python_files:
            print(f"\nPYTHON FILES ({len(python_files)} files):")
            print("-" * 80)
            for file_path, count in sorted(python_files, key=lambda x: -x[1]):
                print(f"  {file_path}: {count} matches")

        if other_files:
            print(f"\nOTHER FILES ({len(other_files)} files):")
            print("-" * 80)
            for file_path, count in sorted(other_files, key=lambda x: -x[1]):
                print(f"  {file_path}: {count} matches")

    def generate_agent_tasks(self, output_file: str = 'v65_cleanup_tasks.json'):
        """Generate task list for agents"""
        if not self.file_matches:
            print("\n[OK] No cleanup tasks needed!")
            return

        tasks = []

        # Prioritize HTML files (most important for presentation)
        html_files = [f for f in self.file_matches.keys() if f.endswith('.html')]

        for file_path in sorted(html_files):
            matches = self.file_matches[file_path]
            tasks.append({
                'file': file_path,
                'type': 'HTML',
                'matches': len(matches),
                'priority': 'HIGH',
                'sample_lines': [f"Line {m[0]}: {m[1][:100]}" for m in matches[:3]]
            })

        # Then Python files
        py_files = [f for f in self.file_matches.keys() if f.endswith('.py')]

        for file_path in sorted(py_files):
            matches = self.file_matches[file_path]
            tasks.append({
                'file': file_path,
                'type': 'Python',
                'matches': len(matches),
                'priority': 'MEDIUM',
                'sample_lines': [f"Line {m[0]}: {m[1][:100]}" for m in matches[:3]]
            })

        # Save to JSON
        output_path = self.root_dir / output_file
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(tasks, f, indent=2)

        print(f"\n[OK] Generated {len(tasks)} agent tasks")
        print(f"     Saved to: {output_file}")
        print(f"\n     HTML files:   {len(html_files)} (HIGH priority)")
        print(f"     Python files: {len(py_files)} (MEDIUM priority)")


if __name__ == '__main__':
    root = r'h:\Github\PrincipiaMetaphysica'
    scanner = V65Scanner(root)

    # Scan for references
    scanner.scan()
    scanner.report()

    # Generate agent task list
    scanner.generate_agent_tasks()

    print("\n" + "=" * 80)
    print("Next steps:")
    print("  1. Review v65_cleanup_tasks.json")
    print("  2. Deploy agents to clean each file")
    print("  3. Agents will preserve HTML formatting while removing version refs")
