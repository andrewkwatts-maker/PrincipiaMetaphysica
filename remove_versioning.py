"""
remove_versioning.py - Search and Remove Version Terminology

This script finds all mentions of version numbers and versioning terminology
across the Principia Metaphysica project, then removes them to present the
theory as a first-pass/fresh framework without references to prior versions.

Usage:
    python remove_versioning.py --scan     # Just scan and report
    python remove_versioning.py --remove   # Remove all versioning
"""

import os
import re
from pathlib import Path
from typing import List, Tuple, Dict

# Versioning patterns to search for
VERSION_PATTERNS = [
    # Version numbers
    r'v6\.\d+',
    r'v\d+\.\d+',
    r'version\s+6\.\d+',
    r'version\s+\d+\.\d+',

    # MASTERPLAN references
    r'MASTERPLAN2?\s+v\d+\.\d+',
    r'MASTERPLAN2?\s+Implementation',
    r'\(MASTERPLAN2?[^\)]*\)',

    # Update/upgrade language
    r'v6\.\d+\s+update[ds]?',
    r'v\d+\.\d+\s+update[ds]?',
    r'upgraded?\s+to\s+v?\d+\.\d+',
    r'enhanced\s+in\s+v?\d+\.\d+',

    # Fix/resolution references
    r'Issue\s+\d+\s+[^\n]*fixed',
    r'resolves?\s+Issue\s+\d+',
    r'MASTERPLAN2?\s+fix',
    r'\(Issue\s+\d+[^\)]*\)',

    # Status markers
    r'\[RESOLVED\s+v\d+\.\d+\]',
    r'✓\s+v\d+\.\d+',
    r'NEW\s+in\s+v\d+\.\d+',
    r'\(v\d+\.\d+\s+corrected\)',
    r'\(v\d+\.\d+\s+derived\)',

    # Historical references
    r'previous\s+version[s]?',
    r'prior\s+version[s]?',
    r'from\s+v\d+\.\d+',
    r'since\s+v\d+\.\d+',

    # Badge/label markers
    r'<.*?v\d+\.\d+.*?>',
    r'"v\d+\.\d+"',
    r"'v\d+\.\d+'",
]

# File extensions to scan
SCAN_EXTENSIONS = ['.html', '.py', '.md', '.txt', '.csv']

# Files to skip
SKIP_FILES = [
    'remove_versioning.py',
    '__pycache__',
    '.git',
    'node_modules',
]

class VersionScanner:
    def __init__(self, root_dir: str):
        self.root_dir = Path(root_dir)
        self.matches: Dict[str, List[Tuple[int, str, str]]] = {}

    def scan(self) -> Dict[str, List[Tuple[int, str, str]]]:
        """Scan all files for version references"""
        print("Scanning for version references...")
        print("=" * 80)

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
        """Scan a single file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
            return

        matches = []
        for line_num, line in enumerate(lines, 1):
            for pattern in VERSION_PATTERNS:
                if re.search(pattern, line, re.IGNORECASE):
                    matches.append((line_num, line.strip(), pattern))

        if matches:
            self.matches[str(file_path)] = matches

    def report(self):
        """Print report of all matches"""
        if not self.matches:
            print("\n[OK] No version references found!")
            return

        total = sum(len(m) for m in self.matches.values())
        print(f"\n[REPORT] Found {total} version references in {len(self.matches)} files:\n")

        for file_path, matches in sorted(self.matches.items()):
            rel_path = Path(file_path).relative_to(self.root_dir)
            print(f"\n{rel_path} ({len(matches)} matches):")
            print("-" * 80)

            for line_num, line, pattern in matches[:10]:  # Show first 10
                try:
                    print(f"  Line {line_num}: {line[:100]}")
                except UnicodeEncodeError:
                    print(f"  Line {line_num}: [Unicode content - see file]")

            if len(matches) > 10:
                print(f"  ... and {len(matches) - 10} more")

    def remove_versioning(self, dry_run=False):
        """Remove version references from files"""
        if not self.matches:
            print("\n[OK] No version references to remove!")
            return

        mode = "DRY RUN" if dry_run else "REMOVING"
        print(f"\n{mode}: Removing version references...")
        print("=" * 80)

        for file_path in self.matches.keys():
            self._clean_file(file_path, dry_run)

        if dry_run:
            print("\n[WARNING] This was a DRY RUN. Use --remove to actually modify files.")
        else:
            print(f"\n[OK] Successfully cleaned {len(self.matches)} files!")

    def _clean_file(self, file_path: str, dry_run: bool):
        """Clean a single file of version references"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
            return

        original = content

        # Apply replacements
        # 1. Version badges/labels in HTML
        content = re.sub(r'<[^>]*v\d+\.\d+[^>]*badge[^>]*>.*?</[^>]+>', '', content, flags=re.DOTALL)
        content = re.sub(r'v\d+\.\d+\s+-\s+\d+%\s+Validation', 'Validated Framework', content)

        # 2. Version numbers in text
        content = re.sub(r'\bv6\.\d+\b', '', content)
        content = re.sub(r'\bv\d+\.\d+\b', '', content)
        content = re.sub(r'[Vv]ersion\s+6\.\d+', '', content)
        content = re.sub(r'[Vv]ersion\s+\d+\.\d+', '', content)

        # 3. MASTERPLAN references
        content = re.sub(r'MASTERPLAN2?\s+v\d+\.\d+', '', content)
        content = re.sub(r'MASTERPLAN2?\s+Implementation', '', content)
        content = re.sub(r'\(MASTERPLAN2?[^\)]*\)', '', content)

        # 4. Update/fix language
        content = re.sub(r'v\d+\.\d+\s+update[ds]?', 'update', content, flags=re.IGNORECASE)
        content = re.sub(r'upgraded?\s+to\s+v?\d+\.\d+', 'derived', content, flags=re.IGNORECASE)
        content = re.sub(r'enhanced\s+in\s+v?\d+\.\d+', 'enhanced', content, flags=re.IGNORECASE)

        # 5. Issue references
        content = re.sub(r'Issue\s+\d+\s+[^\n]*fixed', 'resolved', content, flags=re.IGNORECASE)
        content = re.sub(r'resolves?\s+Issue\s+\d+', 'resolved', content, flags=re.IGNORECASE)
        content = re.sub(r'MASTERPLAN2?\s+fix', 'correction', content, flags=re.IGNORECASE)
        content = re.sub(r'\(Issue\s+\d+[^\)]*\)', '', content)

        # 6. Status markers
        content = re.sub(r'\[RESOLVED\s+v\d+\.\d+\]', '', content)
        content = re.sub(r'NEW\s+in\s+v\d+\.\d+', '', content, flags=re.IGNORECASE)
        content = re.sub(r'\(v\d+\.\d+\s+corrected\)', '', content)
        content = re.sub(r'\(v\d+\.\d+\s+derived\)', '', content)
        content = re.sub(r'\(v\d+\.\d+\s+[^\)]+\)', '', content)

        # 7. Historical references
        content = re.sub(r'previous\s+version[s]?', 'earlier work', content, flags=re.IGNORECASE)
        content = re.sub(r'prior\s+version[s]?', 'earlier formulation', content, flags=re.IGNORECASE)
        content = re.sub(r'from\s+v\d+\.\d+', '', content)
        content = re.sub(r'since\s+v\d+\.\d+', '', content)

        # 8. Clean up extra spaces
        content = re.sub(r'\s+', ' ', content)
        content = re.sub(r'\n\s*\n\s*\n+', '\n\n', content)
        content = re.sub(r'  +', ' ', content)

        # 9. Clean up orphaned parentheses and brackets
        content = re.sub(r'\(\s*\)', '', content)
        content = re.sub(r'\[\s*\]', '', content)

        if content != original:
            rel_path = Path(file_path).relative_to(self.root_dir)
            print(f"  Cleaning: {rel_path}")

            if not dry_run:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)


if __name__ == '__main__':
    import sys

    root = r'h:\Github\PrincipiaMetaphysica'
    scanner = VersionScanner(root)

    if '--scan' in sys.argv or len(sys.argv) == 1:
        # Scan only
        scanner.scan()
        scanner.report()
        print("\n" + "=" * 80)
        print("Run with --remove to clean all files, or --dry-run to preview changes")

    elif '--dry-run' in sys.argv:
        # Dry run
        scanner.scan()
        scanner.remove_versioning(dry_run=True)

    elif '--remove' in sys.argv:
        # Actually remove
        scanner.scan()
        scanner.report()

        print("\n" + "=" * 80)
        response = input("Proceed with removing version references? (yes/no): ")

        if response.lower() in ['yes', 'y']:
            scanner.remove_versioning(dry_run=False)
            print("\n[OK] Version references removed successfully!")
        else:
            print("\n[CANCELLED]")

    else:
        print("Usage:")
        print("  python remove_versioning.py --scan      # Scan and report")
        print("  python remove_versioning.py --dry-run   # Preview changes")
        print("  python remove_versioning.py --remove    # Remove versioning")
