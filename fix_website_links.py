#!/usr/bin/env python3
"""
Fix broken links in Website HTML files.

This script:
1. Scans Website/*.html for broken/outdated links
2. Creates a mapping of old -> new links
3. Applies fixes with diff preview
4. Validates changes before committing

Usage:
    python fix_website_links.py --check    # Preview changes only
    python fix_website_links.py --apply    # Apply fixes
"""

import os
import re
import sys
from pathlib import Path
from difflib import unified_diff

# Link replacements mapping
LINK_REPLACEMENTS = {
    # CSS links are correct (../css/ points to root css folder)
    # Keep these as-is since Website/ is a subfolder

    # Fix sections links (sections/ folder is deprecated, use Website/)
    '../sections/index.html': 'sections.html',
    '../sections/formulas.html': 'formulas.html',

    # Missing foundation pages - link to foundations.html with anchors
    '../foundations/einstein-field-equations.html': 'foundations.html#einstein-field-equations',
    '../foundations/einstein-hilbert-action.html': 'foundations.html#einstein-hilbert-action',
    '../foundations/ricci-tensor.html': 'foundations.html#ricci-tensor',
    '../foundations/kaluza-klein.html': 'foundations.html#kaluza-klein',

    # These foundation pages exist - keep linking to them
    # But use relative path from Website/
    # '../foundations/boltzmann-entropy.html' -> OK (exists)
    # '../foundations/clifford-algebra.html' -> OK (exists)
    # etc.
}

# Regex-based replacements for dynamic links
REGEX_REPLACEMENTS = [
    # Fix template variable links
    (r'href="\.\./sections/formulas\.html#\$\{([^}]+)\}"', r'href="formulas.html#${\1}"'),
]

# Patterns to check for potential issues
CHECK_PATTERNS = [
    (r'href="\.\./sections/', 'Deprecated sections/ path'),
    (r'href="foundations\.html#', 'Foundation anchor (OK)'),
    (r'href="\.\./foundations/(?!boltzmann|clifford|dirac|hawking|kms|so10|tomita|unruh|yang)', 'Missing foundation page'),
]


def find_html_files(base_path: Path) -> list:
    """Find all HTML files in Website folder."""
    website_path = base_path / 'Website'
    if not website_path.exists():
        print(f"Error: Website folder not found at {website_path}")
        return []
    return list(website_path.glob('*.html'))


def analyze_file(filepath: Path) -> dict:
    """Analyze a file for broken links."""
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    issues = []
    replacements = []

    # Find all href links
    href_pattern = r'href="([^"]*)"'
    for match in re.finditer(href_pattern, content):
        link = match.group(1)

        # Check if link needs replacement
        if link in LINK_REPLACEMENTS:
            new_link = LINK_REPLACEMENTS[link]
            replacements.append({
                'old': link,
                'new': new_link,
                'line': content[:match.start()].count('\n') + 1
            })

        # Check for known issues
        for pattern, desc in CHECK_PATTERNS:
            if re.match(pattern.replace('href="', ''), link):
                issues.append({
                    'link': link,
                    'issue': desc,
                    'line': content[:match.start()].count('\n') + 1
                })

    return {
        'file': filepath,
        'issues': issues,
        'replacements': replacements,
        'content': content
    }


def apply_fixes(filepath: Path, content: str, replacements: list) -> str:
    """Apply link replacements to content."""
    new_content = content
    for rep in replacements:
        old_href = f'href="{rep["old"]}"'
        new_href = f'href="{rep["new"]}"'
        new_content = new_content.replace(old_href, new_href)

    # Apply regex replacements
    for pattern, replacement in REGEX_REPLACEMENTS:
        new_content = re.sub(pattern, replacement, new_content)

    return new_content


def show_diff(filepath: Path, old_content: str, new_content: str):
    """Show unified diff of changes."""
    old_lines = old_content.splitlines(keepends=True)
    new_lines = new_content.splitlines(keepends=True)

    diff = unified_diff(
        old_lines, new_lines,
        fromfile=f'a/{filepath.name}',
        tofile=f'b/{filepath.name}'
    )

    diff_text = ''.join(diff)
    if diff_text:
        print(f"\n{'='*60}")
        print(f"Changes for: {filepath.name}")
        print('='*60)
        # Handle unicode in Windows console
        try:
            print(diff_text)
        except UnicodeEncodeError:
            print(diff_text.encode('ascii', 'replace').decode('ascii'))
    return diff_text


def main():
    check_only = '--check' in sys.argv
    apply_mode = '--apply' in sys.argv

    if not check_only and not apply_mode:
        print("Usage: python fix_website_links.py --check|--apply")
        print("  --check  Preview changes without applying")
        print("  --apply  Apply fixes to files")
        sys.exit(1)

    base_path = Path(__file__).parent
    html_files = find_html_files(base_path)

    if not html_files:
        print("No HTML files found in Website/")
        sys.exit(1)

    print(f"Scanning {len(html_files)} HTML files in Website/")
    print("-" * 60)

    total_issues = 0
    total_replacements = 0
    files_to_update = []

    for filepath in html_files:
        analysis = analyze_file(filepath)

        if analysis['issues']:
            print(f"\n{filepath.name}:")
            for issue in analysis['issues']:
                print(f"  Line {issue['line']}: {issue['issue']}")
                print(f"    Link: {issue['link']}")
            total_issues += len(analysis['issues'])

        if analysis['replacements']:
            new_content = apply_fixes(
                filepath,
                analysis['content'],
                analysis['replacements']
            )

            if check_only:
                show_diff(filepath, analysis['content'], new_content)

            files_to_update.append({
                'path': filepath,
                'old': analysis['content'],
                'new': new_content,
                'count': len(analysis['replacements'])
            })
            total_replacements += len(analysis['replacements'])

    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"Files scanned: {len(html_files)}")
    print(f"Total issues found: {total_issues}")
    print(f"Total replacements needed: {total_replacements}")
    print(f"Files to update: {len(files_to_update)}")

    if apply_mode and files_to_update:
        print("\nApplying fixes...")
        for file_info in files_to_update:
            with open(file_info['path'], 'w', encoding='utf-8') as f:
                f.write(file_info['new'])
            print(f"  Updated: {file_info['path'].name} ({file_info['count']} changes)")
        print("\nDone! Review changes with: git diff Website/")
    elif check_only:
        print("\nRun with --apply to make changes")


if __name__ == "__main__":
    main()
