"""
Check for broken internal links in all HTML files

Validates:
- Internal anchor links (#section-id)
- Relative file links (./file.html, ../file.html)
- Links between HTML files

Copyright (c) 2025 Andrew Keith Watts. All rights reserved.
"""

import os
import re
from pathlib import Path
from bs4 import BeautifulSoup
import json

def find_html_files(root_dir):
    """Find all HTML files in the repository"""
    html_files = []
    for root, dirs, files in os.walk(root_dir):
        # Skip hidden directories and __pycache__
        dirs[:] = [d for d in dirs if not d.startswith('.') and d != '__pycache__']
        for file in files:
            if file.endswith('.html'):
                html_files.append(os.path.join(root, file))
    return html_files

def extract_links_and_anchors(filepath):
    """Extract all links and anchor IDs from an HTML file"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    soup = BeautifulSoup(content, 'html.parser')

    # Extract all anchor IDs
    anchors = set()
    for tag in soup.find_all(id=True):
        anchors.add(tag['id'])

    # Extract all links
    links = []
    for a in soup.find_all('a', href=True):
        links.append(a['href'])

    return anchors, links

def check_broken_links(root_dir):
    """Check for broken links across all HTML files"""
    html_files = find_html_files(root_dir)

    # Build index of all files and their anchors
    file_index = {}
    for filepath in html_files:
        rel_path = os.path.relpath(filepath, root_dir)
        anchors, links = extract_links_and_anchors(filepath)
        file_index[rel_path] = {
            'absolute_path': filepath,
            'anchors': anchors,
            'links': links
        }

    broken_links = []

    # Check each file's links
    for rel_path, data in file_index.items():
        current_dir = os.path.dirname(data['absolute_path'])

        for link in data['links']:
            # Skip external links
            if link.startswith('http://') or link.startswith('https://') or link.startswith('mailto:'):
                continue

            # Skip javascript and special links
            if link.startswith('javascript:') or link.startswith('#') and not link[1:]:
                continue

            # Internal anchor link in same file
            if link.startswith('#'):
                anchor_id = link[1:]
                if anchor_id not in data['anchors']:
                    broken_links.append({
                        'file': rel_path,
                        'link': link,
                        'type': 'missing_anchor',
                        'target': rel_path,
                        'message': f"Anchor #{anchor_id} not found in {rel_path}"
                    })

            # Relative file link
            elif '/' in link or link.endswith('.html'):
                # Split anchor from path
                if '#' in link:
                    path_part, anchor_part = link.split('#', 1)
                else:
                    path_part, anchor_part = link, None

                # Resolve relative path
                target_path = os.path.normpath(os.path.join(current_dir, path_part))
                target_rel_path = os.path.relpath(target_path, root_dir)

                # Check if file exists
                if target_rel_path not in file_index and not os.path.exists(target_path):
                    broken_links.append({
                        'file': rel_path,
                        'link': link,
                        'type': 'missing_file',
                        'target': target_rel_path,
                        'message': f"File {target_rel_path} not found"
                    })
                # Check anchor if specified
                elif anchor_part and target_rel_path in file_index:
                    if anchor_part not in file_index[target_rel_path]['anchors']:
                        broken_links.append({
                            'file': rel_path,
                            'link': link,
                            'type': 'missing_anchor',
                            'target': f"{target_rel_path}#{anchor_part}",
                            'message': f"Anchor #{anchor_part} not found in {target_rel_path}"
                        })

    return broken_links, file_index

def main():
    root_dir = "h:/Github/PrincipiaMetaphysica"

    print("Scanning HTML files for broken links...")
    broken_links, file_index = check_broken_links(root_dir)

    # Generate report
    print(f"\n=== BROKEN LINK REPORT ===")
    print(f"Total HTML files: {len(file_index)}")
    print(f"Total broken links: {len(broken_links)}\n")

    if broken_links:
        # Group by file
        by_file = {}
        for link in broken_links:
            if link['file'] not in by_file:
                by_file[link['file']] = []
            by_file[link['file']].append(link)

        for file, links in sorted(by_file.items()):
            print(f"\n{file} ({len(links)} broken links):")
            for link in links:
                print(f"  - {link['link']}")
                print(f"    Type: {link['type']}")
                print(f"    {link['message']}")

        # Save to JSON
        with open('broken_links_report.json', 'w', encoding='utf-8') as f:
            json.dump({
                'total_files': len(file_index),
                'total_broken': len(broken_links),
                'broken_links': broken_links
            }, f, indent=2)

        print(f"\nFull report saved to: broken_links_report.json")
    else:
        print("OK: No broken links found!")

if __name__ == "__main__":
    main()
