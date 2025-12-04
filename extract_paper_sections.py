#!/usr/bin/env python3
"""
Extract Paper Sections to sections_content.py
==============================================

Systematically extracts all content from principia-metaphysica-paper.html
and populates sections_content.py with complete structure.

Copyright (c) 2025 Andrew Keith Watts. All rights reserved.
"""

import re
from pathlib import Path
from bs4 import BeautifulSoup

def extract_text_content(soup_element):
    """Extract clean text from HTML element, preserving structure"""
    # Get text but preserve paragraph breaks
    text = soup_element.get_text(separator='\n', strip=True)
    # Clean up excessive newlines
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()

def find_subsections(content_html, section_start, section_end):
    """Find h3/h4 subsections within a section"""
    soup = BeautifulSoup(content_html, 'html.parser')

    subsections = []
    for heading in soup.find_all(['h3', 'h4']):
        subsection_id = heading.get('id', '')
        if subsection_id:
            subsections.append({
                'id': subsection_id,
                'title': heading.get_text(strip=True),
                'level': int(heading.name[1])  # h3 -> 3, h4 -> 4
            })

    return subsections

def extract_paper_structure():
    """Extract complete paper structure"""

    paper_path = Path('principia-metaphysica-paper.html')

    with open(paper_path, 'r', encoding='utf-8') as f:
        html_content = f.read()

    soup = BeautifulSoup(html_content, 'html.parser')

    # Find all h2 sections
    sections = []
    h2_tags = soup.find_all('h2', id=True)

    print(f"Found {len(h2_tags)} main sections\n")

    for i, h2 in enumerate(h2_tags):
        section_id = h2.get('id')
        section_title = h2.get_text(strip=True)

        # Skip footnotes and references
        if section_id in ['footnotes'] or 'References' in section_title:
            continue

        print(f"\nSection {i+1}: {section_title}")
        print(f"  ID: {section_id}")

        # Find the content between this h2 and the next h2
        content_elements = []
        current = h2.find_next_sibling()

        while current:
            if current.name == 'h2':
                break
            content_elements.append(current)
            current = current.find_next_sibling()

        # Extract text content
        content_text = ""
        for elem in content_elements[:5]:  # First few paragraphs for overview
            if elem.name in ['p', 'div']:
                text = extract_text_content(elem)
                if text and len(text) > 20:  # Skip very short fragments
                    content_text += text + "\n\n"

        # Find subsections
        content_html = ''.join(str(e) for e in content_elements)
        subsections = find_subsections(content_html, section_id, None)

        print(f"  Subsections: {len(subsections)}")
        for sub in subsections[:3]:  # Show first 3
            print(f"    - {sub['title']} (id={sub['id']})")

        sections.append({
            'id': section_id,
            'title': section_title,
            'content': content_text.strip()[:500],  # First 500 chars
            'subsections': subsections
        })

    return sections

def generate_sections_content_code(sections):
    """Generate Python code for sections_content.py"""

    code_parts = []

    for section in sections:
        section_id = section['id']
        section_title = section['title']
        content = section['content'].replace('"', '\\"').replace('\n', '\\n')

        # Map paper section IDs to our naming scheme
        id_mapping = {
            'intro': 'introduction',
            'framework': 'geometric_framework',
            'geometry': 'pneuma_manifold',
            'gauge': 'gauge_unification',
            'thermal': 'thermal_time',
            'cosmology': 'cosmology',
            'predictions': 'predictions',
            'concerns': 'resolution_status',
            'conclusion': 'conclusion'
        }

        mapped_id = id_mapping.get(section_id, section_id)

        # Generate topics from subsections
        topics = []
        for sub in section['subsections']:
            sub_id = sub['id'].replace('-', '_')
            topics.append(f'''
        {{
            "id": "{sub_id}",
            "title": "{sub['title']}",
            "template_type": "subsection"
        }}''')

        topics_str = ','.join(topics) if topics else ''

        code_parts.append(f'''
    "{mapped_id}": {{
        "pages": [
            {{
                "file": "https://www.metaphysicæ.com/principia-metaphysica-paper.html",
                "section": "#{section_id}",
                "order": {len(code_parts) + 1},
                "include": ["title", "content", "topics"],
                "hover_details": True,
                "template_type": "Paper Section"
            }}
        ],
        "title": "{section_title}",
        "content": """{content}...""",
        "topics": [{topics_str}
        ]
    }}''')

    return ',\n'.join(code_parts)

if __name__ == "__main__":
    import sys
    import io
    # Force UTF-8 encoding for stdout
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

    print("Extracting paper structure...\n")
    print("=" * 80)

    sections = extract_paper_structure()

    print("\n" + "=" * 80)
    print(f"\nTotal sections extracted: {len(sections)}")

    print("\n" + "=" * 80)
    print("Section IDs:")
    for s in sections:
        print(f"  - {s['id']}: {s['title']}")

    # Generate code snippet
    print("\n" + "=" * 80)
    print("Generating sections_content.py code...\n")

    code = generate_sections_content_code(sections)

    # Save to file
    with open('PAPER_SECTIONS_EXTRACT.py', 'w', encoding='utf-8') as f:
        f.write("# Auto-extracted paper sections for sections_content.py\n")
        f.write("# Copy this into SECTIONS dictionary\n\n")
        f.write(code)

    print("Code saved to: PAPER_SECTIONS_EXTRACT.py")
    print("\nNext steps:")
    print("1. Review PAPER_SECTIONS_EXTRACT.py")
    print("2. Merge into sections_content.py")
    print("3. Add values arrays for each section")
    print("4. Regenerate theory-constants-enhanced.js")
