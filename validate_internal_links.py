#!/usr/bin/env python3
"""
Validate Internal Links Across Website
Finds broken internal navigation links (href="#..." and href="file.html#...")
"""

import re
from pathlib import Path
from collections import defaultdict

def extract_links_and_anchors(html_file):
    """Extract all internal links and anchor IDs from HTML file"""
    content = html_file.read_text(encoding='utf-8')

    # Find all internal anchor links
    internal_links = []

    # Pattern 1: Same-page anchors href="#anchor"
    same_page = re.findall(r'href=["\']#([^"\']+)["\']', content)
    internal_links.extend([(None, anchor) for anchor in same_page])

    # Pattern 2: Cross-file anchors href="file.html#anchor"
    cross_file = re.findall(r'href=["\']([^"\']+\.html)#([^"\']+)["\']', content)
    internal_links.extend(cross_file)

    # Pattern 3: Cross-file no anchor href="file.html"
    file_only = re.findall(r'href=["\']([^"\']+\.html)["\'](?!\#)', content)

    # Find all anchor IDs (id="..." and <a name="...">)
    anchor_ids = re.findall(r'(?:id|name)=["\']([^"\']+)["\']', content)

    return internal_links, file_only, set(anchor_ids)

def validate_internal_links(base_dir):
    """Validate all internal links across the website"""
    base_path = Path(base_dir)

    # Build index of all files and their anchors
    file_anchors = {}
    all_links = defaultdict(list)

    # Scan all HTML files
    html_files = list(base_path.rglob('*.html'))

    print(f"Scanning {len(html_files)} HTML files...")
    print()

    for html_file in html_files:
        rel_path = html_file.relative_to(base_path)
        internal_links, file_links, anchors = extract_links_and_anchors(html_file)
        file_anchors[str(rel_path)] = anchors

        for target_file, anchor in internal_links:
            all_links[str(rel_path)].append((target_file, anchor, html_file))

    # Validate links
    broken_links = []

    for source_file, links in all_links.items():
        for target_file, anchor, full_path in links:
            # Same-page anchor
            if target_file is None:
                if anchor not in file_anchors.get(source_file, set()):
                    broken_links.append({
                        'source': source_file,
                        'target': f'#{anchor}',
                        'type': 'same-page',
                        'issue': 'Anchor ID not found in same file'
                    })
            else:
                # Cross-file anchor
                # Resolve relative path
                source_path = Path(source_file)
                target_path = (source_path.parent / target_file).as_posix()

                # Normalize path
                target_path = target_path.replace('\\', '/')

                # Check if target file exists in our index
                matching_files = [f for f in file_anchors.keys() if target_path in f or f in target_path]

                if not matching_files:
                    broken_links.append({
                        'source': source_file,
                        'target': f'{target_file}#{anchor}',
                        'type': 'cross-file',
                        'issue': f'Target file not found: {target_file}'
                    })
                else:
                    # Check if anchor exists in target file
                    found = False
                    for matched_file in matching_files:
                        if anchor in file_anchors.get(matched_file, set()):
                            found = True
                            break

                    if not found:
                        broken_links.append({
                            'source': source_file,
                            'target': f'{target_file}#{anchor}',
                            'type': 'cross-file',
                            'issue': f'Anchor #{anchor} not found in {target_file}'
                        })

    return broken_links, file_anchors

def main():
    base_dir = 'H:/Github/PrincipiaMetaphysica'

    print("=" * 80)
    print("INTERNAL LINK VALIDATION REPORT")
    print("=" * 80)
    print()

    broken_links, file_anchors = validate_internal_links(base_dir)

    # Categorize broken links
    critical = []  # Navigation menus
    high = []      # Main content
    low = []       # Footnotes/references

    for link in broken_links:
        source = link['source']
        # Critical: links in index, navigation
        if 'index.html' in source or 'navigation' in source.lower():
            critical.append(link)
        # Low: links in references
        elif 'reference' in source.lower() or 'footnote' in link['target'].lower():
            low.append(link)
        else:
            high.append(link)

    # Report results
    print(f"SUMMARY:")
    print(f"  Total broken links found: {len(broken_links)}")
    print(f"    CRITICAL (navigation): {len(critical)}")
    print(f"    HIGH (main content): {len(high)}")
    print(f"    LOW (footnotes/refs): {len(low)}")
    print()

    if critical:
        print("CRITICAL BROKEN LINKS (Navigation Menus):")
        print("-" * 80)
        for link in critical:
            print(f"  Source: {link['source']}")
            print(f"  Target: {link['target']}")
            print(f"  Issue:  {link['issue']}")
            print()

    if high:
        print("HIGH PRIORITY BROKEN LINKS (Main Content):")
        print("-" * 80)
        for link in high[:20]:  # Show first 20
            print(f"  Source: {link['source']}")
            print(f"  Target: {link['target']}")
            print(f"  Issue:  {link['issue']}")
            print()
        if len(high) > 20:
            print(f"  ... and {len(high) - 20} more")
            print()

    if low:
        print(f"LOW PRIORITY: {len(low)} broken links in footnotes/references")
        print()

    # File statistics
    print("FILE STATISTICS:")
    print("-" * 80)
    for file, anchors in sorted(file_anchors.items()):
        print(f"  {file}: {len(anchors)} anchors")

    return len(broken_links)

if __name__ == '__main__':
    exit_code = main()
    print()
    print("=" * 80)
    print(f"Validation complete. Exit code: {exit_code}")
    print("=" * 80)
