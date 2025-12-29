#!/usr/bin/env python3
"""
Link Auditor for Principia Metaphysica Website
Scans all HTML files for broken links (internal pages, CSS, JS, JSON, images, anchors)
"""

import os
import re
from pathlib import Path
from urllib.parse import urlparse
import json

# Base directory
BASE_DIR = Path(r'h:\Github\PrincipiaMetaphysica')

# Patterns to find links
PATTERNS = {
    'href': re.compile(r'href=["\']([^"\']+)["\']', re.IGNORECASE),
    'src': re.compile(r'src=["\']([^"\']+)["\']', re.IGNORECASE),
    'link_rel': re.compile(r'<link[^>]+rel=["\'][^"\']*stylesheet[^"\']*["\'][^>]*>', re.IGNORECASE),
    'script_src': re.compile(r'<script[^>]+src=["\']([^"\']+)["\'][^>]*>', re.IGNORECASE),
}

# Files/folders to exclude
EXCLUDE_PATTERNS = ['node_modules', '.git', 'zenodo_package', '__pycache__']

def should_exclude(path):
    """Check if path should be excluded"""
    path_str = str(path)
    return any(exclude in path_str for exclude in EXCLUDE_PATTERNS)

def find_html_files():
    """Find all HTML files in the project"""
    html_files = []
    for root, dirs, files in os.walk(BASE_DIR):
        # Filter out excluded directories
        dirs[:] = [d for d in dirs if not any(excl in d for excl in EXCLUDE_PATTERNS)]

        for file in files:
            if file.endswith('.html'):
                file_path = Path(root) / file
                if not should_exclude(file_path):
                    html_files.append(file_path)

    return sorted(html_files)

def extract_links(html_content, html_file):
    """Extract all links from HTML content"""
    links = {
        'internal_pages': [],
        'css': [],
        'js': [],
        'json': [],
        'images': [],
        'anchors': [],
        'external': []
    }

    # Find all href attributes
    for match in PATTERNS['href'].finditer(html_content):
        url = match.group(1)

        # Skip empty, mailto, tel, javascript
        if not url or url.startswith(('mailto:', 'tel:', 'javascript:', '#')):
            if url and url.startswith('#'):
                links['anchors'].append(url[1:])
            continue

        # External link
        if url.startswith(('http://', 'https://', '//')):
            links['external'].append(url)
        # Internal page link
        elif url.endswith('.html'):
            links['internal_pages'].append(url)
        # Other internal links
        else:
            # Could be anchor or relative path
            if '#' in url:
                path, anchor = url.split('#', 1)
                if path.endswith('.html'):
                    links['internal_pages'].append(path)
                links['anchors'].append(anchor)
            else:
                links['internal_pages'].append(url)

    # Find all CSS links
    for match in PATTERNS['link_rel'].finditer(html_content):
        href_match = re.search(r'href=["\']([^"\']+)["\']', match.group(0))
        if href_match:
            url = href_match.group(1)
            if not url.startswith(('http://', 'https://', '//')):
                links['css'].append(url)

    # Find all JS script sources
    for match in PATTERNS['script_src'].finditer(html_content):
        src_match = re.search(r'src=["\']([^"\']+)["\']', match.group(0))
        if src_match:
            url = src_match.group(1)
            if not url.startswith(('http://', 'https://', '//')):
                links['js'].append(url)

    # Find all img sources
    img_pattern = re.compile(r'<img[^>]+src=["\']([^"\']+)["\']', re.IGNORECASE)
    for match in img_pattern.finditer(html_content):
        url = match.group(1)
        if not url.startswith(('http://', 'https://', '//', 'data:')):
            links['images'].append(url)

    # Find JSON data paths (fetch calls, data attributes)
    json_pattern = re.compile(r'["\']([^"\']*\.json)["\']', re.IGNORECASE)
    for match in json_pattern.finditer(html_content):
        url = match.group(1)
        if not url.startswith(('http://', 'https://')):
            links['json'].append(url)

    return links

def resolve_path(link, source_file):
    """Resolve a relative path to absolute path"""
    source_dir = source_file.parent

    # Handle absolute paths from root
    if link.startswith('/'):
        return BASE_DIR / link.lstrip('/')

    # Handle relative paths
    resolved = source_dir / link
    try:
        return resolved.resolve()
    except:
        return resolved

def check_link_exists(link, source_file):
    """Check if a link target exists"""
    resolved = resolve_path(link, source_file)
    return resolved.exists()

def find_anchor_in_file(anchor_id, file_path):
    """Check if an anchor ID exists in a file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            # Look for id="anchor" or id='anchor'
            pattern = rf'id=["\']({re.escape(anchor_id)})["\']'
            return bool(re.search(pattern, content))
    except:
        return False

def audit_html_file(html_file):
    """Audit a single HTML file for broken links"""
    issues = []

    try:
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        issues.append({
            'type': 'ERROR',
            'message': f'Could not read file: {e}',
            'file': str(html_file.relative_to(BASE_DIR))
        })
        return issues

    links = extract_links(content, html_file)

    # Check internal page links
    for link in set(links['internal_pages']):
        if not link:
            continue

        # Remove anchor if present
        clean_link = link.split('#')[0] if '#' in link else link

        if not check_link_exists(clean_link, html_file):
            issues.append({
                'type': 'BROKEN_LINK',
                'category': 'Internal Page',
                'link': link,
                'file': str(html_file.relative_to(BASE_DIR)),
                'resolved': str(resolve_path(clean_link, html_file))
            })

    # Check CSS files
    for link in set(links['css']):
        if not check_link_exists(link, html_file):
            issues.append({
                'type': 'BROKEN_LINK',
                'category': 'CSS',
                'link': link,
                'file': str(html_file.relative_to(BASE_DIR)),
                'resolved': str(resolve_path(link, html_file))
            })

    # Check JS files
    for link in set(links['js']):
        if not check_link_exists(link, html_file):
            issues.append({
                'type': 'BROKEN_LINK',
                'category': 'JavaScript',
                'link': link,
                'file': str(html_file.relative_to(BASE_DIR)),
                'resolved': str(resolve_path(link, html_file))
            })

    # Check JSON files
    for link in set(links['json']):
        # Try multiple common paths for JSON
        found = False
        paths_to_try = [
            link,
            f'AutoGenerated/{link}',
            f'../AutoGenerated/{link}',
            f'./AutoGenerated/{link}',
        ]

        for path in paths_to_try:
            if check_link_exists(path, html_file):
                found = True
                break

        if not found:
            issues.append({
                'type': 'BROKEN_LINK',
                'category': 'JSON',
                'link': link,
                'file': str(html_file.relative_to(BASE_DIR)),
                'tried_paths': [str(resolve_path(p, html_file)) for p in paths_to_try]
            })

    # Check images
    for link in set(links['images']):
        if not check_link_exists(link, html_file):
            issues.append({
                'type': 'BROKEN_LINK',
                'category': 'Image',
                'link': link,
                'file': str(html_file.relative_to(BASE_DIR)),
                'resolved': str(resolve_path(link, html_file))
            })

    # Note: Anchor checking is complex and may produce false positives
    # We'll skip it for now as it requires loading target files

    return issues

def main():
    """Main audit function"""
    print("=" * 80)
    print("LINK AUDIT FOR PRINCIPIA METAPHYSICA")
    print("=" * 80)
    print()

    html_files = find_html_files()
    print(f"Found {len(html_files)} HTML files to audit")
    print()

    all_issues = []

    for html_file in html_files:
        rel_path = html_file.relative_to(BASE_DIR)
        print(f"Auditing: {rel_path}")

        issues = audit_html_file(html_file)
        if issues:
            all_issues.extend(issues)
            print(f"  [!] Found {len(issues)} issue(s)")
        else:
            print(f"  [OK] No issues")

    print()
    print("=" * 80)
    print(f"AUDIT COMPLETE - Found {len(all_issues)} total issues")
    print("=" * 80)
    print()

    if all_issues:
        # Group by category
        by_category = {}
        for issue in all_issues:
            cat = issue.get('category', 'Other')
            if cat not in by_category:
                by_category[cat] = []
            by_category[cat].append(issue)

        # Print summary
        print("SUMMARY BY CATEGORY:")
        print("-" * 80)
        for cat, issues in sorted(by_category.items()):
            print(f"{cat}: {len(issues)} issue(s)")
        print()

        # Print detailed breakdown
        print("DETAILED BREAKDOWN:")
        print("-" * 80)

        for cat, issues in sorted(by_category.items()):
            print(f"\n{cat} ({len(issues)} issues):")
            print("-" * 80)

            for issue in issues:
                print(f"\n  File: {issue['file']}")
                print(f"  Link: {issue['link']}")
                if 'resolved' in issue:
                    print(f"  Resolved to: {issue['resolved']}")
                if 'tried_paths' in issue:
                    print(f"  Tried paths:")
                    for path in issue['tried_paths']:
                        print(f"    - {path}")

                # Suggest fix
                if cat == 'CSS':
                    if '../css/' in issue['link']:
                        print(f"  [FIX] Suggestion: Check if CSS file exists or update path")
                elif cat == 'JavaScript':
                    if '../js/' in issue['link']:
                        print(f"  [FIX] Suggestion: Check if JS file exists or update path")
                elif cat == 'JSON':
                    print(f"  [FIX] Suggestion: Ensure JSON file is in AutoGenerated/ folder")
                elif cat == 'Internal Page':
                    print(f"  [FIX] Suggestion: Check if HTML file exists or update link")

        # Save to JSON
        report_path = BASE_DIR / 'link_audit_report.json'
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump({
                'total_files': len(html_files),
                'total_issues': len(all_issues),
                'issues_by_category': {cat: len(issues) for cat, issues in by_category.items()},
                'issues': all_issues
            }, f, indent=2)

        print(f"\n\nFull report saved to: {report_path}")
    else:
        print("[OK] No broken links found!")

    return len(all_issues)

if __name__ == '__main__':
    num_issues = main()
    exit(0 if num_issues == 0 else 1)
