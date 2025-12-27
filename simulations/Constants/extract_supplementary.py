#!/usr/bin/env python3
"""
Extract Supplementary Content to JSON
======================================

Extracts content from supplementary HTML pages into structured JSON
for caching and dynamic loading.

Supplementary pages contain extended/speculative content not in the main paper:
- Delta_lat probes (consciousness experiments)
- CMB bubble collisions (multiverse)
- Subleading dispersion parameters

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.
"""

import json
import re
import sys
import io
from pathlib import Path
from typing import Dict, List, Any, Optional

# Fix Windows console encoding
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')


# Supplementary files to extract
SUPPLEMENTARY_FILES = {
    'delta-lat-probes': {
        'file': 'sections/appendix-e-delta-lat-probes.html',
        'id': 'supp-delta-lat',
        'title': 'Empirical Probes of Lattice Configuration Dispersion (δ_lat)',
        'category': 'speculative',
        'status': 'SPECULATIVE',
        'relatedParams': ['delta_lat', 'consciousness.coherence_time'],
        'relatedFormulas': ['pm-modulation', 'orch-or-collapse'],
        'description': 'Future experimental framework for testing microtubule-PM coupling'
    },
    'cmb-bubble-collisions': {
        'file': 'sections/cmb-bubble-collisions-comprehensive.html',
        'id': 'supp-cmb-bubble',
        'title': 'CMB Bubble Collisions - Comprehensive Treatment',
        'category': 'speculative',
        'status': 'THEORETICAL',
        'relatedParams': ['bubble_nucleation_rate', 'eternal_inflation'],
        'relatedFormulas': ['cdl-tunneling', 'bubble-collision-rate'],
        'description': 'Multiverse bubble collision signatures in CMB data'
    },
    'subleading-dispersion': {
        'file': 'sections/appendix-f-subleading-dispersion.html',
        'id': 'supp-dispersion',
        'title': 'Subleading Dispersion Parameters (v16.1)',
        'category': 'theoretical',
        'status': 'THEORETICAL',
        'relatedParams': ['epsilon_atm', 'phi_CP', 'delta_race', 'delta_gamma'],
        'relatedFormulas': ['atmospheric-mixing', 'cp-phase-dispersion'],
        'description': 'Theoretical uncertainty bands for brittle predictions'
    }
}


def extract_text_content(html: str) -> str:
    """Extract plain text from HTML."""
    # Remove script and style
    html = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL | re.IGNORECASE)
    html = re.sub(r'<style[^>]*>.*?</style>', '', html, flags=re.DOTALL | re.IGNORECASE)
    html = re.sub(r'<!--.*?-->', '', html, flags=re.DOTALL)

    # Remove tags but keep content
    text = re.sub(r'<[^>]+>', ' ', html)

    # Decode entities
    text = text.replace('&nbsp;', ' ').replace('&amp;', '&')
    text = text.replace('&lt;', '<').replace('&gt;', '>')
    text = text.replace('&mdash;', '—').replace('&ndash;', '–')
    text = text.replace('&plusmn;', '±').replace('&asymp;', '≈')
    text = text.replace('&isin;', '∈').replace('&deg;', '°')
    text = re.sub(r'&#?\w+;', '', text)

    # Normalize whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def extract_sections(html: str) -> List[Dict[str, Any]]:
    """Extract sections from HTML."""
    sections = []

    # Strategy 1: Find all <section> elements with IDs
    section_pattern = r'<section[^>]*id="([^"]*)"[^>]*>(.*?)</section>'
    matches = re.findall(section_pattern, html, re.DOTALL | re.IGNORECASE)

    # Strategy 2: If no sections found, split by <h2> headers
    if not matches:
        # Find all h2 headers and extract content between them
        h2_pattern = r'<h2[^>]*>(.*?)</h2>'
        h2_matches = list(re.finditer(h2_pattern, html, re.DOTALL | re.IGNORECASE))

        for i, h2_match in enumerate(h2_matches):
            title = extract_text_content(h2_match.group(1))
            # Get content from this h2 to the next h2 (or end of body)
            start = h2_match.end()
            if i + 1 < len(h2_matches):
                end = h2_matches[i + 1].start()
            else:
                # Find </body> or </main> or end
                body_end = html.find('</body>', start)
                main_end = html.find('</main>', start)
                end = min(e for e in [body_end, main_end, len(html)] if e > 0)

            content = html[start:end]
            section_id = re.sub(r'[^a-z0-9]+', '-', title.lower())[:30]
            matches.append((section_id, content))

    for section_id, content in matches:
        # Extract title from h2/h3
        title_match = re.search(r'<h[23][^>]*>(.*?)</h[23]>', content, re.DOTALL | re.IGNORECASE)
        title = extract_text_content(title_match.group(1)) if title_match else section_id

        # Extract paragraphs
        paragraphs = []
        for p_match in re.finditer(r'<p[^>]*>(.*?)</p>', content, re.DOTALL | re.IGNORECASE):
            text = extract_text_content(p_match.group(1))
            if text and len(text) > 20:
                paragraphs.append(text)

        # Extract list items
        list_items = []
        for li_match in re.finditer(r'<li[^>]*>(.*?)</li>', content, re.DOTALL | re.IGNORECASE):
            text = extract_text_content(li_match.group(1))
            if text and len(text) > 10:
                list_items.append(text)

        # Extract tables
        tables = []
        for table_match in re.finditer(r'<table[^>]*>(.*?)</table>', content, re.DOTALL | re.IGNORECASE):
            rows = []
            for tr_match in re.finditer(r'<tr[^>]*>(.*?)</tr>', table_match.group(1), re.DOTALL | re.IGNORECASE):
                cells = []
                for cell_match in re.finditer(r'<t[hd][^>]*>(.*?)</t[hd]>', tr_match.group(1), re.DOTALL | re.IGNORECASE):
                    cells.append(extract_text_content(cell_match.group(1)))
                if cells:
                    rows.append(cells)
            if rows:
                tables.append(rows)

        # Extract equations/formulas
        equations = []
        for eq_match in re.finditer(r'<(?:div|p)[^>]*class="[^"]*formula[^"]*"[^>]*>(.*?)</(?:div|p)>', content, re.DOTALL | re.IGNORECASE):
            eq_text = extract_text_content(eq_match.group(1))
            if eq_text:
                equations.append(eq_text)

        sections.append({
            'id': section_id,
            'title': title,
            'paragraphs': paragraphs,
            'listItems': list_items,
            'tables': tables,
            'equations': equations
        })

    return sections


def extract_supplementary_file(base_dir: Path, config: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Extract content from a single supplementary file."""
    file_path = base_dir / config['file']

    if not file_path.exists():
        print(f"  [SKIP] {config['file']} not found")
        return None

    try:
        html = file_path.read_text(encoding='utf-8', errors='replace')
    except Exception as e:
        print(f"  [ERROR] Reading {config['file']}: {e}")
        return None

    # Extract main title
    title_match = re.search(r'<h1[^>]*>(.*?)</h1>', html, re.DOTALL | re.IGNORECASE)
    main_title = extract_text_content(title_match.group(1)) if title_match else config['title']

    # Extract sections
    sections = extract_sections(html)

    # Build result
    result = {
        'id': config['id'],
        'title': main_title,
        'shortTitle': config['title'],
        'category': config['category'],
        'status': config['status'],
        'description': config['description'],
        'file': config['file'],
        'relatedParams': config.get('relatedParams', []),
        'relatedFormulas': config.get('relatedFormulas', []),
        'sections': sections,
        'sectionCount': len(sections),
        'wordCount': sum(len(' '.join(s.get('paragraphs', [])).split()) for s in sections)
    }

    print(f"  [OK] {config['id']}: {len(sections)} sections, ~{result['wordCount']} words")
    return result


def extract_all_supplementary(base_dir: Path) -> Dict[str, Any]:
    """Extract all supplementary content."""
    print("Extracting supplementary content...")

    supplementary = {
        'version': '16.2',
        'count': 0,
        'items': {}
    }

    for key, config in SUPPLEMENTARY_FILES.items():
        result = extract_supplementary_file(base_dir, config)
        if result:
            supplementary['items'][key] = result
            supplementary['count'] += 1

    return supplementary


def add_supplementary_refs(theory_path: Path, supplementary: Dict[str, Any]) -> None:
    """Add supplementary references to formulas and parameters in theory_output.json."""
    if not theory_path.exists():
        print("  [SKIP] theory_output.json not found for ref updates")
        return

    try:
        data = json.loads(theory_path.read_text(encoding='utf-8'))
    except Exception as e:
        print(f"  [ERROR] Loading theory_output.json: {e}")
        return

    # Add supplementaryRefs to formulas
    formulas = data.get('formulas', {}).get('formulas', {})
    for supp_key, supp_item in supplementary['items'].items():
        for formula_id in supp_item.get('relatedFormulas', []):
            if formula_id in formulas:
                if 'supplementaryRefs' not in formulas[formula_id]:
                    formulas[formula_id]['supplementaryRefs'] = []
                if supp_key not in formulas[formula_id]['supplementaryRefs']:
                    formulas[formula_id]['supplementaryRefs'].append(supp_key)

    # Add supplementaryRefs to parameters
    def add_param_refs(obj, param_path, supp_key):
        if isinstance(obj, dict):
            for key, val in obj.items():
                current_path = f"{param_path}.{key}" if param_path else key
                if isinstance(val, dict) and 'value' in val:
                    # This is a parameter
                    if 'supplementaryRefs' not in val:
                        val['supplementaryRefs'] = []
                    if supp_key not in val['supplementaryRefs']:
                        val['supplementaryRefs'].append(supp_key)
                else:
                    add_param_refs(val, current_path, supp_key)

    params = data.get('parameters', {})
    for supp_key, supp_item in supplementary['items'].items():
        for param_name in supp_item.get('relatedParams', []):
            # Try to find and update the parameter
            parts = param_name.split('.')
            target = params
            for part in parts[:-1]:
                if part in target:
                    target = target[part]
                else:
                    break
            if parts[-1] in target and isinstance(target[parts[-1]], dict):
                if 'supplementaryRefs' not in target[parts[-1]]:
                    target[parts[-1]]['supplementaryRefs'] = []
                if supp_key not in target[parts[-1]]['supplementaryRefs']:
                    target[parts[-1]]['supplementaryRefs'].append(supp_key)

    # Save updated data
    theory_path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding='utf-8')
    print("  [OK] Added supplementary refs to theory_output.json")


def main():
    """Main entry point."""
    base_dir = Path(__file__).parent.parent.parent
    output_dir = base_dir / 'AutoGenerated'
    theory_path = output_dir / 'theory_output.json'

    print("=" * 60)
    print("Supplementary Content Extraction")
    print("=" * 60)

    # Extract supplementary content
    supplementary = extract_all_supplementary(base_dir)

    # Save to AutoGenerated/supplementary.json
    output_path = output_dir / 'supplementary.json'
    output_path.write_text(json.dumps(supplementary, indent=2, ensure_ascii=False), encoding='utf-8')

    print(f"\n[SUCCESS] Created {output_path.name}")
    print(f"  Items: {supplementary['count']}")
    print(f"  Total sections: {sum(item['sectionCount'] for item in supplementary['items'].values())}")

    # Add refs to theory_output.json
    print("\nAdding supplementary refs to theory_output.json...")
    add_supplementary_refs(theory_path, supplementary)

    print("\n" + "=" * 60)
    return 0


if __name__ == '__main__':
    sys.exit(main())
