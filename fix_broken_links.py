#!/usr/bin/env python3
"""
Broken Link Fixer for PrincipiaMetaphysica
==========================================

Analyzes broken links from centralization_validation_results.json and intelligently
fixes them with multiple strategies:
- Update paths for moved files
- Add missing anchors
- Remove non-existent links
- Create redirects or pages
- Fix typos

Features:
- Dry-run mode
- Automatic backups
- Detailed logging
- JSON report generation
- Preserves HTML formatting
- Interactive mode for ambiguous cases
"""

import json
import os
import re
import shutil
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Set
from datetime import datetime
from collections import defaultdict
import argparse
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup


class BrokenLinkFixer:
    """Intelligent broken link analyzer and fixer."""

    FIX_STRATEGIES = {
        'update_path': 'File exists but at different location',
        'add_anchor': 'Target file exists but missing anchor ID',
        'remove_link': 'Target does not exist and should not be created',
        'create_page': 'Target should exist - suggest creating it',
        'create_redirect': 'Create redirect to actual location',
        'fix_typo': 'Link has typo in filename',
        'manual': 'Requires manual intervention'
    }

    # Pages that should exist (based on context)
    SHOULD_EXIST = {
        'metric-tensor.html': 'foundations',
        'dirac-spinor.html': 'foundations',
        'hawking-temperature.html': 'foundations',
        'unruh-effect.html': 'foundations',
        'dark-sector.html': 'sections',
    }

    # Known moved files
    MOVED_FILES = {
        'beginners-guide-printable.html': 'docs/beginners-guide-printable.html',
        'computational-appendices.html': 'docs/computational-appendices.html',
    }

    # Files that should NOT be created (dead links)
    SHOULD_NOT_EXIST = {
        'dirac-lagrangian.html',
        'generation-formula.html',
        'thermal-time-relation.html',
        'quantum-foundations.html',
    }

    def __init__(self, root_dir: str, validation_file: str, dry_run: bool = True,
                 interactive: bool = True, backup: bool = True):
        """
        Initialize the fixer.

        Args:
            root_dir: Root directory of the project
            validation_file: Path to centralization_validation_results.json
            dry_run: If True, don't make actual changes
            interactive: If True, ask user for ambiguous cases
            backup: If True, create backups before modifying files
        """
        # Logging (must be first!)
        self.log_messages: List[str] = []

        self.root_dir = Path(root_dir)
        self.validation_file = Path(validation_file)
        self.dry_run = dry_run
        self.interactive = interactive
        self.backup = backup

        # Track all HTML files in project
        self.all_html_files: Dict[str, Path] = {}

        # Track all anchors in each HTML file
        self.file_anchors: Dict[Path, Set[str]] = {}

        # Results tracking
        self.fixes_applied: List[Dict] = []
        self.fixes_manual: List[Dict] = []
        self.fixes_pending: List[Dict] = []

        # Index files
        self._index_html_files()

    def _index_html_files(self):
        """Build index of all HTML files in the project."""
        self.log("Indexing HTML files...")
        files_by_name = defaultdict(list)

        for html_file in self.root_dir.rglob('*.html'):
            if '.git' in str(html_file) or 'node_modules' in str(html_file):
                continue
            filename = html_file.name
            files_by_name[filename].append(html_file)

        self.all_html_files = dict(files_by_name)
        self.log(f"Found {sum(len(v) for v in self.all_html_files.values())} HTML files")

    def _get_anchors_in_file(self, file_path: Path) -> Set[str]:
        """Extract all anchor IDs from an HTML file."""
        if file_path in self.file_anchors:
            return self.file_anchors[file_path]

        anchors = set()
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                soup = BeautifulSoup(content, 'html.parser')

                # Find all elements with id attribute
                for element in soup.find_all(id=True):
                    anchors.add(element['id'])

        except Exception as e:
            self.log(f"Error reading {file_path}: {e}", level='warning')

        self.file_anchors[file_path] = anchors
        return anchors

    def log(self, message: str, level: str = 'info'):
        """Log a message with timestamp."""
        timestamp = datetime.now().strftime('%H:%M:%S')
        levels = {'info': 'INFO', 'warning': 'WARN', 'error': 'ERROR', 'success': 'OK'}
        prefix = levels.get(level, 'INFO')
        log_msg = f"[{timestamp}] [{prefix}] {message}"
        self.log_messages.append(log_msg)
        print(log_msg)

    def load_validation_results(self) -> Dict:
        """Load the validation results JSON file."""
        self.log(f"Loading validation results from {self.validation_file}")
        with open(self.validation_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        broken_links = data.get('file_status', {}).get('broken_links', [])
        self.log(f"Found {len(broken_links)} files with broken links")
        return broken_links

    def resolve_path(self, source_file: str, broken_link: str) -> Tuple[Path, Optional[str]]:
        """
        Resolve a relative link to an absolute path and extract anchor.

        Args:
            source_file: The file containing the broken link
            broken_link: The broken link URL

        Returns:
            Tuple of (resolved_path, anchor)
        """
        # Split anchor from path
        if '#' in broken_link:
            path_part, anchor = broken_link.split('#', 1)
        else:
            path_part, anchor = broken_link, None

        # Resolve relative path
        source_path = self.root_dir / source_file
        if path_part:
            target_path = (source_path.parent / path_part).resolve()
        else:
            target_path = source_path  # Same file anchor

        return target_path, anchor

    def find_file_location(self, filename: str) -> Optional[Path]:
        """Find where a file actually exists in the project."""
        if filename in self.all_html_files:
            locations = self.all_html_files[filename]
            if len(locations) == 1:
                return locations[0]
            else:
                # Multiple locations - need context
                return None
        return None

    def calculate_relative_path(self, from_file: Path, to_file: Path) -> str:
        """Calculate relative path from one file to another."""
        try:
            return os.path.relpath(to_file, from_file.parent).replace('\\', '/')
        except ValueError:
            # Files on different drives
            return str(to_file)

    def analyze_broken_link(self, source_file: str, broken_link: str) -> Dict:
        """
        Analyze a broken link and determine the fix strategy.

        Returns:
            Dict with keys: strategy, old_link, new_link, reason, confidence
        """
        result = {
            'source_file': source_file,
            'broken_link': broken_link,
            'strategy': None,
            'new_link': None,
            'reason': '',
            'confidence': 0.0,  # 0.0 to 1.0
            'metadata': {}
        }

        target_path, anchor = self.resolve_path(source_file, broken_link)
        filename = target_path.name if target_path else None

        # Strategy 1: Check if file was moved (known moves)
        if filename in self.MOVED_FILES:
            correct_path = self.MOVED_FILES[filename]
            new_link = self.calculate_relative_path(
                self.root_dir / source_file,
                self.root_dir / correct_path
            )
            if anchor:
                new_link += f'#{anchor}'

            result.update({
                'strategy': 'update_path',
                'new_link': new_link,
                'reason': f'File moved to {correct_path}',
                'confidence': 1.0,
                'metadata': {'old_location': broken_link, 'new_location': correct_path}
            })
            return result

        # Strategy 2: Check if file exists elsewhere in project
        if filename and not target_path.exists():
            actual_location = self.find_file_location(filename)
            if actual_location:
                new_link = self.calculate_relative_path(
                    self.root_dir / source_file,
                    actual_location
                )
                if anchor:
                    new_link += f'#{anchor}'

                result.update({
                    'strategy': 'update_path',
                    'new_link': new_link,
                    'reason': f'File found at {actual_location.relative_to(self.root_dir)}',
                    'confidence': 0.9,
                    'metadata': {'found_at': str(actual_location.relative_to(self.root_dir))}
                })
                return result

        # Strategy 3: Check if it's just a missing anchor
        if anchor and target_path.exists():
            anchors = self._get_anchors_in_file(target_path)

            if anchor not in anchors:
                # Try to find similar anchor (typo fix)
                similar = self._find_similar_anchor(anchor, anchors)

                if similar:
                    new_link = broken_link.replace(f'#{anchor}', f'#{similar}')
                    result.update({
                        'strategy': 'fix_typo',
                        'new_link': new_link,
                        'reason': f'Anchor typo: "{anchor}" → "{similar}"',
                        'confidence': 0.8,
                        'metadata': {'similar_anchor': similar, 'available_anchors': list(anchors)[:10]}
                    })
                else:
                    result.update({
                        'strategy': 'add_anchor',
                        'new_link': None,
                        'reason': f'Add anchor #{anchor} to {target_path.name}',
                        'confidence': 0.5,
                        'metadata': {'required_anchor': anchor, 'available_anchors': list(anchors)[:10]}
                    })
                return result

        # Strategy 4: Should this file be created?
        if filename in self.SHOULD_EXIST:
            suggested_dir = self.SHOULD_EXIST[filename]
            result.update({
                'strategy': 'create_page',
                'new_link': None,
                'reason': f'Page should exist in {suggested_dir}/',
                'confidence': 0.7,
                'metadata': {'suggested_location': f'{suggested_dir}/{filename}'}
            })
            return result

        # Strategy 5: Should NOT exist (dead link)
        if filename in self.SHOULD_NOT_EXIST:
            result.update({
                'strategy': 'remove_link',
                'new_link': None,
                'reason': 'Dead link - should be removed',
                'confidence': 0.9,
                'metadata': {}
            })
            return result

        # Strategy 6: Check for typos in filename (only if file doesn't exist)
        if filename and not target_path.exists():
            similar_file = self._find_similar_filename(filename)
            if similar_file:
                new_link = self.calculate_relative_path(
                    self.root_dir / source_file,
                    similar_file
                )
                if anchor:
                    new_link += f'#{anchor}'

                result.update({
                    'strategy': 'fix_typo',
                    'new_link': new_link,
                    'reason': f'Filename typo: "{filename}" → "{similar_file.name}"',
                    'confidence': 0.7,
                    'metadata': {'corrected_filename': similar_file.name}
                })
                return result

        # Default: Manual intervention needed
        result.update({
            'strategy': 'manual',
            'new_link': None,
            'reason': 'Requires manual review',
            'confidence': 0.0,
            'metadata': {
                'file_exists': target_path.exists() if target_path else False,
                'target_path': str(target_path) if target_path else None
            }
        })
        return result

    def _find_similar_anchor(self, anchor: str, available: Set[str], threshold: float = 0.7) -> Optional[str]:
        """Find similar anchor name (for typo detection)."""
        from difflib import SequenceMatcher

        best_match = None
        best_ratio = 0.0

        for available_anchor in available:
            ratio = SequenceMatcher(None, anchor.lower(), available_anchor.lower()).ratio()
            if ratio > best_ratio and ratio >= threshold:
                best_ratio = ratio
                best_match = available_anchor

        return best_match

    def _find_similar_filename(self, filename: str, threshold: float = 0.75) -> Optional[Path]:
        """Find similar filename (for typo detection)."""
        from difflib import SequenceMatcher

        best_match = None
        best_ratio = 0.0

        for existing_file in self.all_html_files.keys():
            ratio = SequenceMatcher(None, filename.lower(), existing_file.lower()).ratio()
            if ratio > best_ratio and ratio >= threshold:
                best_ratio = ratio
                if existing_file in self.all_html_files:
                    best_match = self.all_html_files[existing_file][0]

        return best_match

    def apply_fix(self, fix: Dict) -> bool:
        """
        Apply a fix to the source file.

        Args:
            fix: Fix dictionary from analyze_broken_link

        Returns:
            True if fix was applied successfully
        """
        if self.dry_run:
            self.log(f"[DRY RUN] Would fix: {fix['source_file']} - {fix['broken_link']}")
            return True

        source_file_path = self.root_dir / fix['source_file']

        # Backup file
        if self.backup:
            backup_path = source_file_path.with_suffix('.html.bak')
            shutil.copy2(source_file_path, backup_path)

        try:
            with open(source_file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            soup = BeautifulSoup(content, 'html.parser')
            modified = False

            if fix['strategy'] == 'update_path' or fix['strategy'] == 'fix_typo':
                # Find and replace the link
                for link in soup.find_all(['a', 'link']):
                    href = link.get('href', '')
                    if href == fix['broken_link']:
                        link['href'] = fix['new_link']
                        modified = True
                        self.log(f"Updated link: {fix['broken_link']} → {fix['new_link']}", level='success')

            elif fix['strategy'] == 'remove_link':
                # Remove the link but keep the text
                for link in soup.find_all('a'):
                    href = link.get('href', '')
                    if href == fix['broken_link']:
                        link.replace_with(link.get_text())
                        modified = True
                        self.log(f"Removed link: {fix['broken_link']}", level='success')

            if modified:
                # Write back with preserved formatting
                with open(source_file_path, 'w', encoding='utf-8') as f:
                    f.write(str(soup.prettify()))

                return True
            else:
                self.log(f"Link not found in file: {fix['broken_link']}", level='warning')
                return False

        except Exception as e:
            self.log(f"Error applying fix: {e}", level='error')
            return False

    def process_all_broken_links(self) -> Dict:
        """
        Process all broken links and categorize fixes.

        Returns:
            Dict with categorized fixes
        """
        broken_links = self.load_validation_results()

        all_fixes = []
        auto_fixable = []
        needs_confirmation = []
        needs_manual = []

        total_links = sum(len(item['broken']) for item in broken_links)
        self.log(f"\nAnalyzing {total_links} broken links...")

        for item in broken_links:
            source_file = item['file']
            for broken_link in item['broken']:
                fix = self.analyze_broken_link(source_file, broken_link)
                all_fixes.append(fix)

                # Categorize by confidence and strategy
                if fix['confidence'] >= 0.9 and fix['strategy'] in ['update_path', 'fix_typo']:
                    auto_fixable.append(fix)
                elif fix['confidence'] >= 0.5 and fix['strategy'] != 'manual':
                    needs_confirmation.append(fix)
                else:
                    needs_manual.append(fix)

        self.log(f"\nAnalysis complete:")
        self.log(f"  Auto-fixable: {len(auto_fixable)}")
        self.log(f"  Needs confirmation: {len(needs_confirmation)}")
        self.log(f"  Needs manual review: {len(needs_manual)}")

        return {
            'all_fixes': all_fixes,
            'auto_fixable': auto_fixable,
            'needs_confirmation': needs_confirmation,
            'needs_manual': needs_manual
        }

    def run_interactive_session(self, fixes: List[Dict]):
        """
        Run interactive session to confirm ambiguous fixes.

        Args:
            fixes: List of fixes that need user confirmation
        """
        if not self.interactive or not fixes:
            return

        self.log("\n" + "="*80)
        self.log("INTERACTIVE FIX CONFIRMATION")
        self.log("="*80)

        for i, fix in enumerate(fixes, 1):
            print(f"\n[{i}/{len(fixes)}] Fix proposal:")
            print(f"  File: {fix['source_file']}")
            print(f"  Broken link: {fix['broken_link']}")
            print(f"  Strategy: {fix['strategy']}")
            print(f"  Reason: {fix['reason']}")
            print(f"  Confidence: {fix['confidence']:.0%}")

            if fix['new_link']:
                print(f"  New link: {fix['new_link']}")

            if fix['metadata']:
                print(f"  Metadata: {json.dumps(fix['metadata'], indent=4)}")

            response = input("\n  Apply this fix? [y/n/skip]: ").lower().strip()

            if response == 'y':
                if self.apply_fix(fix):
                    self.fixes_applied.append(fix)
            elif response == 'skip':
                self.fixes_pending.append(fix)
            else:
                self.fixes_manual.append(fix)

    def apply_auto_fixes(self, fixes: List[Dict]):
        """Apply all auto-fixable changes."""
        if not fixes:
            return

        self.log(f"\nApplying {len(fixes)} automatic fixes...")

        for fix in fixes:
            if self.apply_fix(fix):
                self.fixes_applied.append(fix)
            else:
                self.fixes_manual.append(fix)

    def generate_report(self, output_file: str = 'broken_links_fix_report.json', all_fixes: List[Dict] = None):
        """Generate detailed JSON report of all fixes."""
        report = {
            'timestamp': datetime.now().isoformat(),
            'dry_run': self.dry_run,
            'summary': {
                'total_fixes_applied': len(self.fixes_applied),
                'total_manual_needed': len(self.fixes_manual),
                'total_pending': len(self.fixes_pending),
                'total_analyzed': len(all_fixes) if all_fixes else 0
            },
            'all_fixes_analyzed': all_fixes or [],
            'fixes_applied': self.fixes_applied,
            'fixes_manual': self.fixes_manual,
            'fixes_pending': self.fixes_pending,
            'logs': self.log_messages
        }

        report_path = self.root_dir / output_file
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2)

        self.log(f"\nReport saved to: {report_path}", level='success')

        # Print summary
        print("\n" + "="*80)
        print("FIX SUMMARY")
        print("="*80)
        print(f"Fixes applied: {len(self.fixes_applied)}")
        print(f"Manual review needed: {len(self.fixes_manual)}")
        print(f"Pending: {len(self.fixes_pending)}")

        if self.fixes_manual:
            print("\nManual review required for:")
            for fix in self.fixes_manual[:10]:  # Show first 10
                print(f"  - {fix['source_file']}: {fix['broken_link']}")
                print(f"    Reason: {fix['reason']}")

        return report


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Fix broken links in PrincipiaMetaphysica project',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Dry run (no changes, just analysis)
  python fix_broken_links.py --dry-run

  # Auto-fix safe cases only
  python fix_broken_links.py --auto-only

  # Interactive mode (ask for confirmation)
  python fix_broken_links.py --interactive

  # Apply all fixes automatically (use with caution!)
  python fix_broken_links.py --apply-all --no-dry-run
        """
    )

    parser.add_argument(
        '--root-dir',
        default='.',
        help='Root directory of the project (default: current directory)'
    )

    parser.add_argument(
        '--validation-file',
        default='centralization_validation_results.json',
        help='Path to validation results JSON file'
    )

    parser.add_argument(
        '--dry-run',
        action='store_true',
        default=True,
        help='Do not make actual changes (default: True)'
    )

    parser.add_argument(
        '--no-dry-run',
        action='store_true',
        help='Actually make changes to files'
    )

    parser.add_argument(
        '--interactive',
        action='store_true',
        default=False,
        help='Ask for confirmation on ambiguous fixes'
    )

    parser.add_argument(
        '--auto-only',
        action='store_true',
        help='Only apply high-confidence automatic fixes'
    )

    parser.add_argument(
        '--apply-all',
        action='store_true',
        help='Apply all fixes without confirmation (requires --no-dry-run)'
    )

    parser.add_argument(
        '--no-backup',
        action='store_true',
        help='Do not create .bak backup files'
    )

    parser.add_argument(
        '--report',
        default='broken_links_fix_report.json',
        help='Output report filename'
    )

    args = parser.parse_args()

    # Determine dry_run mode
    dry_run = not args.no_dry_run

    if args.apply_all and dry_run:
        print("ERROR: --apply-all requires --no-dry-run")
        return 1

    # Create fixer instance
    fixer = BrokenLinkFixer(
        root_dir=args.root_dir,
        validation_file=args.validation_file,
        dry_run=dry_run,
        interactive=args.interactive,
        backup=not args.no_backup
    )

    # Process all broken links
    categorized = fixer.process_all_broken_links()

    # Apply fixes based on mode
    if args.auto_only:
        fixer.apply_auto_fixes(categorized['auto_fixable'])
    elif args.apply_all:
        fixer.apply_auto_fixes(categorized['auto_fixable'])
        fixer.apply_auto_fixes(categorized['needs_confirmation'])
    elif args.interactive:
        fixer.apply_auto_fixes(categorized['auto_fixable'])
        fixer.run_interactive_session(categorized['needs_confirmation'])
    else:
        # Dry run - just show what would be done
        pass

    # Collect manual fixes
    fixer.fixes_manual.extend(categorized['needs_manual'])

    # Generate report
    fixer.generate_report(args.report, all_fixes=categorized['all_fixes'])

    print("\nDone!")
    return 0


if __name__ == '__main__':
    exit(main())
