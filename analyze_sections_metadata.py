#!/usr/bin/env python3
"""
Analyze sections metadata in theory_output.json
"""

import json
from pathlib import Path
from typing import Dict, List, Any

def analyze_sections_metadata(theory_output_path: str) -> Dict[str, Any]:
    """Analyze sections for missing or incomplete metadata."""

    with open(theory_output_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    sections = data.get('sections', {})

    results = {
        'total_sections': len(sections),
        'missing_description': [],
        'missing_formula_refs': [],
        'missing_parameter_refs': [],
        'missing_nav_links': [],
        'missing_id': [],
        'missing_title': [],
        'missing_category_chapter': [],
        'missing_order_number': [],
        'complete_sections': [],
        'section_details': {}
    }

    for section_key, section_data in sections.items():
        detail = {
            'key': section_key,
            'has_id': False,
            'has_title': False,
            'has_description': False,
            'has_category_or_chapter': False,
            'has_order_or_number': False,
            'has_formulas': False,
            'has_parameters': False,
            'has_link': False,
            'formula_count': 0,
            'parameter_count': 0
        }

        # Check id
        if 'id' in section_data and section_data['id']:
            detail['has_id'] = True
        else:
            results['missing_id'].append(section_key)

        # Check title
        if 'title' in section_data and section_data['title']:
            detail['has_title'] = True
            detail['title'] = section_data['title']
        else:
            results['missing_title'].append(section_key)

        # Check description
        if 'description' in section_data and section_data['description']:
            detail['has_description'] = True
        else:
            results['missing_description'].append(section_key)

        # Check category or chapter
        if ('category' in section_data and section_data['category']) or \
           ('chapter' in section_data and section_data['chapter']):
            detail['has_category_or_chapter'] = True
        else:
            results['missing_category_chapter'].append(section_key)

        # Check order or number
        if ('order' in section_data and section_data['order'] is not None) or \
           ('number' in section_data and section_data['number'] is not None):
            detail['has_order_or_number'] = True
        else:
            results['missing_order_number'].append(section_key)

        # Check formulas
        if 'formulas' in section_data and isinstance(section_data['formulas'], list):
            if len(section_data['formulas']) > 0:
                detail['has_formulas'] = True
                detail['formula_count'] = len(section_data['formulas'])
            else:
                results['missing_formula_refs'].append(section_key)
        else:
            results['missing_formula_refs'].append(section_key)

        # Check parameters
        if 'parameters' in section_data and isinstance(section_data['parameters'], list):
            if len(section_data['parameters']) > 0:
                detail['has_parameters'] = True
                detail['parameter_count'] = len(section_data['parameters'])
            else:
                results['missing_parameter_refs'].append(section_key)
        else:
            results['missing_parameter_refs'].append(section_key)

        # Check link/href
        if ('link' in section_data and section_data['link']) or \
           ('href' in section_data and section_data['href']):
            detail['has_link'] = True
        else:
            results['missing_nav_links'].append(section_key)

        # Check if section is complete
        if all([
            detail['has_id'],
            detail['has_title'],
            detail['has_description'],
            detail['has_category_or_chapter'],
            detail['has_order_or_number'],
            detail['has_formulas'],
            detail['has_parameters'],
            detail['has_link']
        ]):
            results['complete_sections'].append(section_key)

        results['section_details'][section_key] = detail

    return results, sections

def generate_report(results: Dict[str, Any], sections: Dict[str, Any], output_path: str):
    """Generate markdown report."""

    report = []
    report.append("# Sections Metadata Audit Report\n")
    report.append(f"**Generated:** {Path(__file__).name}\n")
    report.append(f"**Source:** theory_output.json\n\n")

    # Summary
    report.append("## Summary\n")
    report.append(f"- **Total Sections:** {results['total_sections']}\n")
    report.append(f"- **Complete Sections:** {len(results['complete_sections'])}\n")
    report.append(f"- **Incomplete Sections:** {results['total_sections'] - len(results['complete_sections'])}\n\n")

    # Completeness percentage
    if results['total_sections'] > 0:
        completeness = (len(results['complete_sections']) / results['total_sections']) * 100
        report.append(f"**Overall Completeness:** {completeness:.1f}%\n\n")

    # Missing metadata breakdown
    report.append("## Missing Metadata Breakdown\n\n")

    report.append(f"### 1. Missing IDs: {len(results['missing_id'])}\n")
    if results['missing_id']:
        for key in results['missing_id']:
            title = sections[key].get('title', 'Unknown')
            report.append(f"- Section `{key}`: {title}\n")
    else:
        report.append("- None (All sections have IDs)\n")
    report.append("\n")

    report.append(f"### 2. Missing Titles: {len(results['missing_title'])}\n")
    if results['missing_title']:
        for key in results['missing_title']:
            report.append(f"- Section `{key}`\n")
    else:
        report.append("- None (All sections have titles)\n")
    report.append("\n")

    report.append(f"### 3. Missing Descriptions: {len(results['missing_description'])}\n")
    if results['missing_description']:
        for key in results['missing_description']:
            title = sections[key].get('title', 'Unknown')
            report.append(f"- Section `{key}`: {title}\n")
    else:
        report.append("- None (All sections have descriptions)\n")
    report.append("\n")

    report.append(f"### 4. Missing Category/Chapter: {len(results['missing_category_chapter'])}\n")
    if results['missing_category_chapter']:
        for key in results['missing_category_chapter']:
            title = sections[key].get('title', 'Unknown')
            report.append(f"- Section `{key}`: {title}\n")
    else:
        report.append("- None (All sections have category/chapter)\n")
    report.append("\n")

    report.append(f"### 5. Missing Order/Number: {len(results['missing_order_number'])}\n")
    if results['missing_order_number']:
        for key in results['missing_order_number']:
            title = sections[key].get('title', 'Unknown')
            report.append(f"- Section `{key}`: {title}\n")
    else:
        report.append("- None (All sections have order/number)\n")
    report.append("\n")

    report.append(f"### 6. Missing Formula References: {len(results['missing_formula_refs'])}\n")
    if results['missing_formula_refs']:
        for key in results['missing_formula_refs']:
            title = sections[key].get('title', 'Unknown')
            report.append(f"- Section `{key}`: {title}\n")
    else:
        report.append("- None (All sections have formula references)\n")
    report.append("\n")

    report.append(f"### 7. Missing Parameter References: {len(results['missing_parameter_refs'])}\n")
    if results['missing_parameter_refs']:
        for key in results['missing_parameter_refs']:
            title = sections[key].get('title', 'Unknown')
            report.append(f"- Section `{key}`: {title}\n")
    else:
        report.append("- None (All sections have parameter references)\n")
    report.append("\n")

    report.append(f"### 8. Missing Navigation Links: {len(results['missing_nav_links'])}\n")
    if results['missing_nav_links']:
        for key in results['missing_nav_links']:
            title = sections[key].get('title', 'Unknown')
            report.append(f"- Section `{key}`: {title}\n")
    else:
        report.append("- None (All sections have navigation links)\n")
    report.append("\n")

    # Detailed section analysis
    report.append("## Detailed Section Analysis\n\n")

    for section_key in sorted(results['section_details'].keys()):
        detail = results['section_details'][section_key]
        section = sections[section_key]

        title = section.get('title', 'Unknown Title')
        report.append(f"### Section {section_key}: {title}\n\n")

        # Metadata checklist
        report.append("**Metadata Checklist:**\n\n")
        report.append(f"- [{'x' if detail['has_id'] else ' '}] ID: `{section.get('id', 'MISSING')}`\n")
        report.append(f"- [{'x' if detail['has_title'] else ' '}] Title: {title}\n")
        report.append(f"- [{'x' if detail['has_description'] else ' '}] Description\n")
        report.append(f"- [{'x' if detail['has_category_or_chapter'] else ' '}] Category/Chapter\n")
        report.append(f"- [{'x' if detail['has_order_or_number'] else ' '}] Order/Number\n")
        report.append(f"- [{'x' if detail['has_formulas'] else ' '}] Formulas ({detail['formula_count']} referenced)\n")
        report.append(f"- [{'x' if detail['has_parameters'] else ' '}] Parameters ({detail['parameter_count']} referenced)\n")
        report.append(f"- [{'x' if detail['has_link'] else ' '}] Navigation Link\n\n")

        # Show actual data
        report.append("**Current Data:**\n\n")
        report.append("```json\n")
        report.append(json.dumps(section, indent=2))
        report.append("\n```\n\n")

    # Recommendations
    report.append("## Recommendations\n\n")

    report.append("### Priority 1: Critical Metadata\n\n")

    if results['missing_id']:
        report.append("**Missing IDs:**\n")
        report.append("- Every section must have a unique `id` field for reliable referencing\n")
        report.append("- Recommended format: `section-{number}` or descriptive kebab-case\n\n")

    if results['missing_title']:
        report.append("**Missing Titles:**\n")
        report.append("- Every section must have a `title` field for display\n")
        report.append("- Titles should be concise but descriptive\n\n")

    if results['missing_order_number']:
        report.append("**Missing Order/Number:**\n")
        report.append("- Add `order` or `number` field to enable proper sequencing\n")
        report.append("- This is critical for navigation and table of contents generation\n\n")

    report.append("### Priority 2: Content Metadata\n\n")

    if results['missing_description']:
        report.append("**Missing Descriptions:**\n")
        report.append("- Add brief `description` field (1-2 sentences) explaining section content\n")
        report.append("- Helps with navigation, search, and user comprehension\n\n")

    if results['missing_category_chapter']:
        report.append("**Missing Category/Chapter:**\n")
        report.append("- Add `category` or `chapter` field for logical grouping\n")
        report.append("- Enables hierarchical organization and filtering\n\n")

    report.append("### Priority 3: Cross-References\n\n")

    if results['missing_formula_refs']:
        report.append("**Missing Formula References:**\n")
        report.append("- Add `formulas` array listing all formulas used in this section\n")
        report.append("- Format: `[\"formula-id-1\", \"formula-id-2\", ...]`\n")
        report.append("- Enables formula validation and cross-referencing\n\n")

    if results['missing_parameter_refs']:
        report.append("**Missing Parameter References:**\n")
        report.append("- Add `parameters` array listing all parameters used in this section\n")
        report.append("- Format: `[\"param-id-1\", \"param-id-2\", ...]`\n")
        report.append("- Enables parameter validation and cross-referencing\n\n")

    report.append("### Priority 4: Navigation\n\n")

    if results['missing_nav_links']:
        report.append("**Missing Navigation Links:**\n")
        report.append("- Add `link` or `href` field pointing to section HTML file\n")
        report.append("- Format: `sections/{section-name}.html`\n")
        report.append("- Enables automatic navigation menu generation\n\n")

    # Action items
    report.append("## Suggested Action Items\n\n")

    if results['total_sections'] - len(results['complete_sections']) > 0:
        report.append("1. **Complete Missing Critical Fields:**\n")
        report.append("   - Ensure all sections have: `id`, `title`, `order`/`number`\n\n")

        report.append("2. **Add Descriptions:**\n")
        report.append("   - Write brief descriptions for sections lacking them\n")
        report.append("   - Focus on what the section covers and why it's important\n\n")

        report.append("3. **Build Cross-Reference Arrays:**\n")
        report.append("   - Analyze each section's HTML content\n")
        report.append("   - Extract formula and parameter references\n")
        report.append("   - Add to `formulas` and `parameters` arrays\n\n")

        report.append("4. **Add Navigation Links:**\n")
        report.append("   - Map each section to its HTML file\n")
        report.append("   - Verify files exist and paths are correct\n\n")

        report.append("5. **Consider Additional Metadata:**\n")
        report.append("   - `dependencies`: sections that should be read first\n")
        report.append("   - `tags`: keywords for search/filtering\n")
        report.append("   - `difficulty`: beginner/intermediate/advanced\n")
        report.append("   - `estimatedReadTime`: reading time estimate\n\n")
    else:
        report.append("**All sections have complete metadata!** Consider:\n\n")
        report.append("- Adding enhanced metadata (tags, dependencies, difficulty)\n")
        report.append("- Validating cross-references are accurate\n")
        report.append("- Ensuring navigation links work correctly\n\n")

    # Write report
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(''.join(report))

    print(f"Report generated: {output_path}")
    print(f"\nSummary:")
    print(f"  Total sections: {results['total_sections']}")
    print(f"  Complete: {len(results['complete_sections'])}")
    print(f"  Incomplete: {results['total_sections'] - len(results['complete_sections'])}")

if __name__ == '__main__':
    theory_output = 'theory_output.json'
    report_output = 'reports/SECTIONS_METADATA_AUDIT.md'

    results, sections = analyze_sections_metadata(theory_output)
    generate_report(results, sections, report_output)
