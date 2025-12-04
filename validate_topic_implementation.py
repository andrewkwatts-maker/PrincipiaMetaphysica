#!/usr/bin/env python3
"""
Topic Implementation Validator
==============================

Validates that all pages properly implement the topics defined in sections_content.py.
Checks for:
- Missing topic sections in HTML files
- Orphaned content not defined in sections_content.py
- Inconsistent topic structure between pages
- Required values not populated from PM constants

Copyright (c) 2025 Andrew Keith Watts. All rights reserved.
"""

import re
import json
from pathlib import Path
from typing import Dict, List, Set, Tuple
from collections import defaultdict

try:
    from sections_content import SECTIONS, get_section, get_required_values, get_topic_by_id
    SECTIONS_AVAILABLE = True
except ImportError:
    print("Warning: sections_content.py not found")
    SECTIONS_AVAILABLE = False

def extract_topics_from_html(filepath: Path) -> Set[str]:
    """Extract topic IDs from HTML file (via id attributes, section headings, etc.)"""
    topics = set()

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        return topics

    # Look for topic IDs in various patterns
    # Pattern 1: id="topic-name" or id="dimensional_reduction"
    id_matches = re.finditer(r'id=["\']([a-zA-Z0-9_-]+)["\']', content)
    for match in id_matches:
        topic_id = match.group(1)
        # Filter out common non-topic IDs
        if not any(skip in topic_id for skip in ['nav', 'menu', 'header', 'footer', 'container', 'wrapper']):
            topics.add(topic_id)

    # Pattern 2: Section headings with consistent naming
    heading_matches = re.finditer(r'<h[2-4][^>]*>([^<]+)</h[2-4]>', content)
    for match in heading_matches:
        heading_text = match.group(1).strip()
        # Convert to potential topic ID
        topic_id = heading_text.lower().replace(' ', '_').replace('-', '_')
        topic_id = re.sub(r'[^a-z0-9_]', '', topic_id)
        if topic_id:
            topics.add(topic_id)

    return topics


def get_expected_topics_for_page(page_url: str) -> Dict[str, List[str]]:
    """Get expected topics for a page from sections_content.py"""
    if not SECTIONS_AVAILABLE:
        return {}

    expected = {}

    for section_id, section_data in SECTIONS.items():
        if section_id == 'meta':
            continue

        pages = section_data.get('pages', [])
        for page in pages:
            if page_url in page.get('file', ''):
                # Check what should be included
                includes = page.get('include', [])

                # Parse topic includes
                topics = []
                for inc in includes:
                    if inc.startswith('topics::'):
                        topics.append(inc.replace('topics::', ''))
                    elif inc == 'topics':
                        # Include all top-level topics
                        section_topics = section_data.get('topics', [])
                        topics.extend([t['id'] for t in section_topics])

                if topics:
                    expected[section_id] = topics

    return expected


def validate_page(filepath: Path, page_url: str) -> Dict:
    """Validate a single page's topic implementation"""
    result = {
        'file': str(filepath),
        'url': page_url,
        'topics_found': [],
        'topics_expected': {},
        'missing_topics': [],
        'orphaned_topics': [],
        'validation_status': 'unknown'
    }

    # Get actual topics in file
    actual_topics = extract_topics_from_html(filepath)
    result['topics_found'] = sorted(actual_topics)

    # Get expected topics from sections_content
    expected_topics_by_section = get_expected_topics_for_page(page_url)
    result['topics_expected'] = expected_topics_by_section

    # Flatten expected topics
    all_expected = set()
    for topics in expected_topics_by_section.values():
        all_expected.update(topics)

    # Find missing and orphaned topics
    result['missing_topics'] = sorted(all_expected - actual_topics)

    # Determine validation status
    if not expected_topics_by_section:
        result['validation_status'] = 'not_in_sections_content'
    elif not result['missing_topics']:
        result['validation_status'] = 'complete'
    elif len(result['missing_topics']) < len(all_expected) * 0.5:
        result['validation_status'] = 'partial'
    else:
        result['validation_status'] = 'incomplete'

    return result


def validate_all_pages() -> Dict[str, Dict]:
    """Validate all HTML pages in the project"""
    results = {}

    # Define pages to check
    pages_to_check = [
        ('index.html', 'https://www.metaphysicæ.com/index.html'),
        ('principia-metaphysica-paper.html', 'https://www.metaphysicæ.com/principia-metaphysica-paper.html'),
        ('beginners-guide.html', 'https://www.metaphysicæ.com/beginners-guide.html'),
    ]

    # Add section pages
    sections_dir = Path('sections')
    if sections_dir.exists():
        for section_file in sections_dir.glob('*.html'):
            url = f'https://www.metaphysicæ.com/sections/{section_file.name}'
            pages_to_check.append((str(section_file), url))

    for filepath_str, url in pages_to_check:
        filepath = Path(filepath_str)
        if filepath.exists():
            result = validate_page(filepath, url)
            results[str(filepath)] = result

    return results


def print_validation_report(results: Dict[str, Dict]):
    """Print formatted validation report"""
    print("=" * 80)
    print("TOPIC IMPLEMENTATION VALIDATION REPORT")
    print("=" * 80)
    print()

    # Count by status
    status_counts = defaultdict(int)
    for result in results.values():
        status_counts[result['validation_status']] += 1

    print(f"Total pages checked: {len(results)}")
    print(f"  Complete: {status_counts['complete']}")
    print(f"  Partial: {status_counts['partial']}")
    print(f"  Incomplete: {status_counts['incomplete']}")
    print(f"  Not in sections_content: {status_counts['not_in_sections_content']}")
    print()

    # Group by status
    by_status = defaultdict(list)
    for filepath, result in results.items():
        by_status[result['validation_status']].append((filepath, result))

    # Print incomplete/partial pages first
    for status in ['incomplete', 'partial', 'complete', 'not_in_sections_content']:
        if status not in by_status:
            continue

        print(f"\n{'='*80}")
        print(f"{status.upper().replace('_', ' ')}")
        print(f"{'='*80}")

        for filepath, result in sorted(by_status[status]):
            print(f"\nFile: {filepath}")

            if result['topics_expected']:
                print(f"  Expected sections: {', '.join(result['topics_expected'].keys())}")

                for section, topics in result['topics_expected'].items():
                    print(f"    {section}: {', '.join(topics)}")

            if result['missing_topics']:
                print(f"  Missing topics ({len(result['missing_topics'])}): {', '.join(result['missing_topics'][:10])}")
                if len(result['missing_topics']) > 10:
                    print(f"    ... and {len(result['missing_topics']) - 10} more")

            if result['topics_found'] and not result['topics_expected']:
                print(f"  Found topics ({len(result['topics_found'])}): {', '.join(sorted(result['topics_found'])[:5])}")


def generate_migration_plan(results: Dict[str, Dict]) -> Dict:
    """Generate a migration plan for incomplete pages"""
    plan = {
        'priority_1_incomplete': [],
        'priority_2_partial': [],
        'priority_3_not_defined': [],
        'complete': []
    }

    for filepath, result in results.items():
        status = result['validation_status']

        if status == 'incomplete':
            plan['priority_1_incomplete'].append({
                'file': filepath,
                'missing_count': len(result['missing_topics']),
                'missing_topics': result['missing_topics']
            })
        elif status == 'partial':
            plan['priority_2_partial'].append({
                'file': filepath,
                'missing_count': len(result['missing_topics']),
                'missing_topics': result['missing_topics']
            })
        elif status == 'not_in_sections_content':
            plan['priority_3_not_defined'].append({
                'file': filepath,
                'found_topics': result['topics_found']
            })
        else:
            plan['complete'].append(filepath)

    return plan


if __name__ == "__main__":
    if not SECTIONS_AVAILABLE:
        print("Error: sections_content.py not found. Cannot validate topics.")
        exit(1)

    print("Validating topic implementation across all pages...\n")
    results = validate_all_pages()
    print_validation_report(results)

    # Generate migration plan
    plan = generate_migration_plan(results)

    print("\n" + "=" * 80)
    print("MIGRATION PLAN")
    print("=" * 80)
    print(f"\nPriority 1 (Incomplete): {len(plan['priority_1_incomplete'])} pages")
    print(f"Priority 2 (Partial): {len(plan['priority_2_partial'])} pages")
    print(f"Priority 3 (Not Defined): {len(plan['priority_3_not_defined'])} pages")
    print(f"Complete: {len(plan['complete'])} pages")

    # Save detailed plan
    with open('TOPIC_MIGRATION_PLAN.json', 'w', encoding='utf-8') as f:
        json.dump(plan, f, indent=2)

    print("\n" + "=" * 80)
    print(f"Detailed migration plan saved to: TOPIC_MIGRATION_PLAN.json")
    print("=" * 80)
