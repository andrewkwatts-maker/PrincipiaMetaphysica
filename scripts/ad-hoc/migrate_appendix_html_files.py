#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Migrate content from three appendix HTML files to theory_output.json:
- sections/appendix-e-delta-lat-probes.html -> New appendix section
- sections/appendix-f-subleading-dispersion.html -> New appendix section
- sections/cmb-bubble-collisions-comprehensive.html -> Section 7.7 and 7.8

This script extracts structured content from HTML and adds it to the JSON format.
"""

import json
import re
import sys
from pathlib import Path
from bs4 import BeautifulSoup

# Set UTF-8 encoding for stdout
if sys.stdout.encoding != 'utf-8':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


def extract_html_content(html_path):
    """Extract structured content from HTML file."""
    with open(html_path, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')

    # Find main article content
    article = soup.find('article') or soup.find('main')
    if not article:
        print(f"WARNING: No article/main found in {html_path}")
        return None

    # Extract title
    h1 = article.find('h1')
    title = h1.get_text(strip=True) if h1 else "Untitled"

    # Extract status if present
    status_elem = article.find(class_='section-status')
    status = status_elem.get_text(strip=True) if status_elem else None

    # Extract all sections
    subsections = []
    for section in article.find_all('section', recursive=False):
        subsection_data = extract_section(section)
        if subsection_data:
            subsections.append(subsection_data)

    return {
        'title': title,
        'status': status,
        'subsections': subsections
    }


def extract_section(section_elem):
    """Extract content from a section element."""
    section_id = section_elem.get('id', '')

    # Get section title (h2 or h3)
    title_elem = section_elem.find(['h2', 'h3'])
    title = title_elem.get_text(strip=True) if title_elem else ""

    # Extract content blocks
    content_blocks = []

    for elem in section_elem.children:
        if elem.name is None:  # Text node
            continue

        if elem.name in ['h2', 'h3', 'h4', 'h5']:
            # Skip title elements as they're already captured
            if elem == title_elem:
                continue
            # Sub-headings become text blocks
            content_blocks.append({
                'type': 'text',
                'content': f"**{elem.get_text(strip=True)}**"
            })

        elif elem.name == 'p':
            text = elem.get_text(strip=True)
            if text:
                content_blocks.append({
                    'type': 'text',
                    'content': text
                })

        elif elem.name == 'ul':
            items = [li.get_text(strip=True) for li in elem.find_all('li', recursive=False)]
            if items:
                content_blocks.append({
                    'type': 'list',
                    'items': items
                })

        elif elem.name == 'ol':
            items = [li.get_text(strip=True) for li in elem.find_all('li', recursive=False)]
            if items:
                content_blocks.append({
                    'type': 'list',
                    'ordered': True,
                    'items': items
                })

        elif elem.name == 'table':
            # Extract table structure
            table_data = extract_table(elem)
            if table_data:
                content_blocks.append(table_data)

        elif elem.name == 'div':
            # Handle special div types
            div_class = ' '.join(elem.get('class', []))

            if 'equation-box' in div_class or 'key-formula' in div_class:
                # Extract formula content
                formula_text = elem.get_text(strip=True)
                content_blocks.append({
                    'type': 'formula',
                    'content': formula_text
                })
            elif 'code-block' in div_class or elem.find('code'):
                # Extract code content
                code_text = elem.get_text(strip=True)
                content_blocks.append({
                    'type': 'code',
                    'content': code_text,
                    'language': 'python'
                })
            else:
                # Generic div - extract as text
                text = elem.get_text(strip=True)
                if text:
                    content_blocks.append({
                        'type': 'text',
                        'content': text
                    })

    return {
        'id': section_id,
        'title': title,
        'contentBlocks': content_blocks
    }


def extract_table(table_elem):
    """Extract table data."""
    headers = []
    rows = []

    # Extract headers
    thead = table_elem.find('thead')
    if thead:
        header_row = thead.find('tr')
        if header_row:
            headers = [th.get_text(strip=True) for th in header_row.find_all(['th', 'td'])]

    # Extract rows
    tbody = table_elem.find('tbody') or table_elem
    for tr in tbody.find_all('tr', recursive=False):
        # Skip header row if no thead
        if not thead and not rows and all(cell.name == 'th' for cell in tr.find_all(['th', 'td'])):
            headers = [th.get_text(strip=True) for th in tr.find_all(['th', 'td'])]
            continue

        cells = [td.get_text(strip=True) for td in tr.find_all(['th', 'td'])]
        if cells:
            rows.append(cells)

    if headers or rows:
        return {
            'type': 'table',
            'headers': headers,
            'rows': rows
        }
    return None


def add_to_theory_output(data, section_key, section_data):
    """Add section data to theory_output.json structure."""
    if 'sections' not in data:
        data['sections'] = {}

    data['sections'][section_key] = section_data
    return data


def main():
    base_path = Path(r"h:\Github\PrincipiaMetaphysica")

    # File paths
    html_files = {
        'appendix_e_delta_lat': base_path / 'sections' / 'appendix-e-delta-lat-probes.html',
        'appendix_f_subleading': base_path / 'sections' / 'appendix-f-subleading-dispersion.html',
        'cmb_bubble': base_path / 'sections' / 'cmb-bubble-collisions-comprehensive.html'
    }

    theory_output_path = base_path / 'AutoGenerated' / 'theory_output.json'

    # Load existing theory_output.json
    print(f"Reading {theory_output_path}...")
    with open(theory_output_path, 'r', encoding='utf-8') as f:
        theory_data = json.load(f)

    # Extract content from each HTML file
    extracted_content = {}

    for key, html_path in html_files.items():
        if html_path.exists():
            print(f"\nExtracting content from {html_path.name}...")
            content = extract_html_content(html_path)
            if content:
                extracted_content[key] = content
                print(f"  Title: {content['title']}")
                print(f"  Subsections: {len(content.get('subsections', []))}")
        else:
            print(f"WARNING: File not found: {html_path}")

    # Map content to appropriate sections in theory_output.json
    # Note: Based on existing structure, we need to find unique keys
    # Appendix E (delta_lat) - Let's use 'appendix_e_delta_lat'
    # Appendix F (subleading) - Let's use 'appendix_f_subleading'
    # CMB Bubble (Section 7.7-7.8) - Add to section 7 or create subsections

    if 'appendix_e_delta_lat' in extracted_content:
        print("\nAdding Appendix E (Delta Lat Probes) to theory_output.json...")
        # Create new appendix section with unique ID
        section_data = {
            'id': 'appendix_e_delta_lat',
            'title': extracted_content['appendix_e_delta_lat']['title'],
            'type': 'appendix',
            'status': extracted_content['appendix_e_delta_lat'].get('status'),
            'subsections': extracted_content['appendix_e_delta_lat']['subsections']
        }
        theory_data = add_to_theory_output(theory_data, 'appendix_e_delta_lat', section_data)

    if 'appendix_f_subleading' in extracted_content:
        print("Adding Appendix F (Subleading Dispersion) to theory_output.json...")
        section_data = {
            'id': 'appendix_f_subleading',
            'title': extracted_content['appendix_f_subleading']['title'],
            'type': 'appendix',
            'status': extracted_content['appendix_f_subleading'].get('status'),
            'subsections': extracted_content['appendix_f_subleading']['subsections']
        }
        theory_data = add_to_theory_output(theory_data, 'appendix_f_subleading', section_data)

    if 'cmb_bubble' in extracted_content:
        print("Adding CMB Bubble Collisions to theory_output.json as Section 7.7-7.8...")
        # This should be added as subsections of Section 7
        section_data = {
            'id': 'section_7_cmb_bubbles',
            'title': extracted_content['cmb_bubble']['title'],
            'type': 'section',
            'status': extracted_content['cmb_bubble'].get('status'),
            'subsections': extracted_content['cmb_bubble']['subsections']
        }
        theory_data = add_to_theory_output(theory_data, 'section_7_cmb_bubbles', section_data)

    # Update metadata
    if 'metadata' in theory_data:
        theory_data['metadata']['description'] = "Principia Metaphysica - Complete Theory Output (includes migrated appendices)"

    # Save updated theory_output.json
    print(f"\nWriting updated data to {theory_output_path}...")
    with open(theory_output_path, 'w', encoding='utf-8') as f:
        json.dump(theory_data, f, indent=2, ensure_ascii=False)

    print("\n✓ Migration completed successfully!")
    print(f"\nMigrated sections:")
    for key, content in extracted_content.items():
        print(f"  - {content['title']}")

    return 0


if __name__ == "__main__":
    import sys
    try:
        sys.exit(main())
    except Exception as e:
        print(f"\nERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
