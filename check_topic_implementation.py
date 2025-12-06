"""
Validate that all section topics defined in sections_content.py are implemented in HTML files

Checks:
- All topic IDs defined in sections_content.py exist in corresponding HTML files
- All topic IDs in HTML files have entries in sections_content.py
- Reports missing or orphaned topics

Copyright (c) 2025 Andrew Keith Watts. All rights reserved.
"""

import os
import re
import json
from bs4 import BeautifulSoup

def load_sections_content():
    """Load section definitions from sections_content.py"""
    filepath = "h:/Github/PrincipiaMetaphysica/sections_content.py"

    if not os.path.exists(filepath):
        print(f"ERROR: {filepath} not found")
        return {}

    # Import the SECTIONS dictionary
    import sys
    sys.path.insert(0, os.path.dirname(filepath))

    try:
        from sections_content import SECTIONS
    except Exception as e:
        print(f"ERROR importing SECTIONS: {e}")
        return {}

    # Convert to our expected format
    sections = {}

    for section_name, section_data in SECTIONS.items():
        # Extract topic IDs from content if they exist
        # Look for id="..." patterns in HTML content
        topics = []

        # Check for topics in section data
        if 'topics' in section_data:
            for topic in section_data['topics']:
                if 'id' in topic:
                    topics.append(topic['id'])

        # Also scan content for topic markers
        if 'content' in section_data:
            content = section_data['content']
            # Find all id="..." patterns
            id_pattern = r'id="([^"]+)"'
            found_ids = re.findall(id_pattern, content)
            topics.extend(found_ids)

        sections[section_name] = {
            'topics': list(set(topics)),  # Remove duplicates
            'count': len(set(topics))
        }

    return sections

def extract_topic_ids_from_html(filepath):
    """Extract all topic IDs from an HTML file"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Look for id="topic-id" patterns
    # Typically in <section> or <div> tags
    soup = BeautifulSoup(content, 'html.parser')

    topic_ids = set()

    # Find all tags with IDs
    for tag in soup.find_all(id=True):
        topic_id = tag['id']
        # Skip common non-topic IDs
        if topic_id not in ['header', 'footer', 'main', 'nav', 'content']:
            topic_ids.add(topic_id)

    return topic_ids

def check_topic_implementation():
    """Check if all topics are implemented in HTML files"""
    sections_def = load_sections_content()

    if not sections_def:
        print("ERROR: No sections found in sections_content.py")
        return

    root = "h:/Github/PrincipiaMetaphysica"

    # Map section names to HTML files
    section_file_map = {
        'abstract': 'principia-metaphysica-paper.html',
        'introduction': 'sections/introduction.html',
        'geometric_framework': 'sections/geometric-framework.html',
        'gauge_unification': 'sections/gauge-unification.html',
        'pneuma_manifold': 'sections/pneuma-lagrangian.html',
        'thermal_time': 'sections/thermal-time.html',
        'cosmology': 'sections/cosmology.html',
        'fermion_sector': 'sections/fermion-sector.html',
        'predictions': 'sections/predictions.html',
        'conclusion': 'sections/conclusion.html',
        'pneuma_lagrangian': 'sections/pneuma-lagrangian.html',
        'einstein_hilbert': 'sections/einstein-hilbert-term.html',
        'formulas': 'sections/formulas.html',
        'theory_analysis': 'sections/theory-analysis.html',
        'resolution_status': 'sections/theory-analysis.html',
        'division_algebras': 'sections/division-algebra-section.html',
        'xy_gauge_bosons': 'sections/xy-gauge-bosons.html',
        'cmb_bubble_collisions': 'sections/cmb-bubble-collisions-comprehensive.html',
    }

    results = {
        'total_sections': len(sections_def),
        'total_topics_defined': sum(s['count'] for s in sections_def.values()),
        'missing_topics': [],
        'orphaned_topics': [],
        'implemented_topics': 0
    }

    print("=== TOPIC IMPLEMENTATION VALIDATION ===\n")

    for section_name, section_data in sorted(sections_def.items()):
        html_file = section_file_map.get(section_name)

        if not html_file:
            print(f"WARNING: No HTML file mapped for section '{section_name}'")
            continue

        html_path = os.path.join(root, html_file)

        if not os.path.exists(html_path):
            print(f"ERROR: File not found: {html_file}")
            for topic_id in section_data['topics']:
                results['missing_topics'].append({
                    'section': section_name,
                    'topic_id': topic_id,
                    'file': html_file,
                    'reason': 'file_not_found'
                })
            continue

        # Extract topic IDs from HTML
        html_topics = extract_topic_ids_from_html(html_path)

        # Check each defined topic
        for topic_id in section_data['topics']:
            if topic_id in html_topics:
                results['implemented_topics'] += 1
            else:
                results['missing_topics'].append({
                    'section': section_name,
                    'topic_id': topic_id,
                    'file': html_file,
                    'reason': 'not_found_in_html'
                })

        # Check for orphaned topics (in HTML but not in sections_content.py)
        for html_topic_id in html_topics:
            if html_topic_id not in section_data['topics']:
                results['orphaned_topics'].append({
                    'section': section_name,
                    'topic_id': html_topic_id,
                    'file': html_file
                })

    # Print summary
    print(f"Total sections: {results['total_sections']}")
    print(f"Total topics defined: {results['total_topics_defined']}")
    print(f"Implemented topics: {results['implemented_topics']}")
    print(f"Missing topics: {len(results['missing_topics'])}")
    print(f"Orphaned topics: {len(results['orphaned_topics'])}\n")

    if results['missing_topics']:
        print("=== MISSING TOPICS ===")
        for item in results['missing_topics']:
            print(f"  {item['file']}")
            print(f"    Topic ID: {item['topic_id']}")
            print(f"    Section: {item['section']}")
            print(f"    Reason: {item['reason']}\n")

    if results['orphaned_topics']:
        print("=== ORPHANED TOPICS (in HTML but not in sections_content.py) ===")
        for item in results['orphaned_topics']:
            print(f"  {item['file']}")
            print(f"    Topic ID: {item['topic_id']}")
            print(f"    Section: {item['section']}\n")

    # Save report
    with open('topic_implementation_report.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2)

    print(f"Report saved to: topic_implementation_report.json")

    # Calculate score
    if results['total_topics_defined'] > 0:
        implementation_rate = (results['implemented_topics'] / results['total_topics_defined']) * 100
        print(f"\nImplementation Rate: {implementation_rate:.1f}%")

        if implementation_rate == 100:
            print("OK: All topics implemented!")
        elif implementation_rate >= 90:
            print("GOOD: Most topics implemented")
        else:
            print("WARNING: Significant topics missing")

if __name__ == "__main__":
    check_topic_implementation()
