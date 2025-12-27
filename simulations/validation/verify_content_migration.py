#!/usr/bin/env python3
"""
Content Migration Verification Script
=====================================

Compares text content from old static HTML files against theory_output.json
to verify content migration completeness.

Reports coverage percentage and identifies missing content.

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.
"""

import json
import re
import sys
import io
from pathlib import Path
from typing import Dict, List, Set, Tuple

# Fix Windows console encoding
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')


def extract_html_text(html_content: str) -> str:
    """Extract readable text from HTML content using regex."""
    # Remove script and style blocks
    html = re.sub(r'<script[^>]*>.*?</script>', '', html_content, flags=re.DOTALL | re.IGNORECASE)
    html = re.sub(r'<style[^>]*>.*?</style>', '', html, flags=re.DOTALL | re.IGNORECASE)
    html = re.sub(r'<svg[^>]*>.*?</svg>', '', html, flags=re.DOTALL | re.IGNORECASE)
    html = re.sub(r'<!--.*?-->', '', html, flags=re.DOTALL)

    # Extract text from paragraph, heading, list item, and table cell tags
    text_parts = []

    # Extract from <p> tags
    for match in re.finditer(r'<p[^>]*>(.*?)</p>', html, re.DOTALL | re.IGNORECASE):
        text_parts.append(match.group(1))

    # Extract from heading tags
    for match in re.finditer(r'<h[1-6][^>]*>(.*?)</h[1-6]>', html, re.DOTALL | re.IGNORECASE):
        text_parts.append(match.group(1))

    # Extract from <li> tags
    for match in re.finditer(r'<li[^>]*>(.*?)</li>', html, re.DOTALL | re.IGNORECASE):
        text_parts.append(match.group(1))

    # Extract from <td> tags
    for match in re.finditer(r'<td[^>]*>(.*?)</td>', html, re.DOTALL | re.IGNORECASE):
        text_parts.append(match.group(1))

    # Remove remaining HTML tags from extracted text
    cleaned = []
    for part in text_parts:
        # Remove HTML tags
        text = re.sub(r'<[^>]+>', ' ', part)
        # Decode HTML entities
        text = text.replace('&nbsp;', ' ').replace('&amp;', '&')
        text = text.replace('&lt;', '<').replace('&gt;', '>')
        text = text.replace('&sigma;', 'sigma').replace('&tau;', 'tau')
        text = re.sub(r'&#?\w+;', '', text)  # Remove other entities
        # Clean whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        if text and len(text) > 5:
            cleaned.append(text)

    return ' '.join(cleaned)


def normalize_text(text: str) -> str:
    """Normalize text for comparison."""
    # Remove LaTeX/MathJax expressions
    text = re.sub(r'\$[^$]+\$', '', text)
    text = re.sub(r'\\[a-zA-Z]+\{[^}]*\}', '', text)
    text = re.sub(r'\\[a-zA-Z]+', '', text)

    # Remove special characters and normalize whitespace
    text = re.sub(r'[^\w\s.,;:!?-]', ' ', text)
    text = re.sub(r'\s+', ' ', text)

    return text.lower().strip()


def extract_sentences(text: str, min_length: int = 20) -> Set[str]:
    """Extract unique sentences from text."""
    # Normalize first
    text = normalize_text(text)

    # Split on sentence boundaries
    sentences = re.split(r'[.!?]+', text)

    # Filter and normalize
    unique = set()
    for s in sentences:
        s = s.strip()
        if len(s) >= min_length:
            # Further normalize for comparison
            s = re.sub(r'\s+', ' ', s)
            unique.add(s)

    return unique


def extract_theory_text(data: Dict) -> str:
    """Extract all text content from theory_output.json."""
    all_text = []

    # Extract from sections
    sections = data.get('sections', {})
    for section_id, section in sections.items():
        # Title and abstract
        if section.get('title'):
            all_text.append(section['title'])
        if section.get('abstract'):
            all_text.append(section['abstract'])
        if section.get('description'):
            all_text.append(section['description'])

        # Content blocks
        for block in section.get('contentBlocks', []):
            if isinstance(block, dict):
                if block.get('text'):
                    all_text.append(block['text'])
                if block.get('content'):
                    content = block['content']
                    if isinstance(content, str):
                        all_text.append(content)
                    elif isinstance(content, list):
                        all_text.extend([str(c) for c in content])
                if block.get('items'):
                    all_text.extend([str(i) for i in block['items']])

        # Subsections
        for subsection in section.get('subsections', []):
            if isinstance(subsection, dict):
                if subsection.get('title'):
                    all_text.append(subsection['title'])
                if subsection.get('content'):
                    all_text.append(subsection['content'])
                for block in subsection.get('contentBlocks', []):
                    if isinstance(block, dict):
                        if block.get('text'):
                            all_text.append(block['text'])
                        if block.get('content'):
                            content = block['content']
                            if isinstance(content, str):
                                all_text.append(content)

        # Key takeaways
        for takeaway in section.get('keyTakeaways', []):
            if isinstance(takeaway, str):
                all_text.append(takeaway)

        # Beginner summary
        if section.get('beginnerSummary'):
            all_text.append(section['beginnerSummary'])

    # Extract from formulas
    formulas = data.get('formulas', {})
    for formula_id, formula in formulas.items():
        if not isinstance(formula, dict):
            continue
        if formula.get('description'):
            all_text.append(formula['description'])
        if formula.get('derivation'):
            all_text.append(formula['derivation'])
        for term in formula.get('terms', []):
            if isinstance(term, dict) and term.get('description'):
                all_text.append(term['description'])

    # Extract from parameters
    params = data.get('parameters', {})
    def extract_param_text(obj, prefix=''):
        if isinstance(obj, dict):
            if 'description' in obj:
                all_text.append(obj['description'])
            for key, val in obj.items():
                if key not in ['value', 'unit', 'symbol', 'type']:
                    extract_param_text(val, f"{prefix}.{key}")

    extract_param_text(params)

    # Flatten any lists and ensure all items are strings
    flattened = []
    for item in all_text:
        if isinstance(item, list):
            flattened.extend([str(x) for x in item])
        elif item is not None:
            flattened.append(str(item))

    return ' '.join(flattened)


def check_sentence_coverage(source_sentences: Set[str], target_text: str) -> Tuple[Set[str], Set[str]]:
    """Check how many source sentences appear in target text."""
    target_normalized = normalize_text(target_text)

    found = set()
    missing = set()

    for sentence in source_sentences:
        # Check for exact or fuzzy match
        if sentence in target_normalized:
            found.add(sentence)
        else:
            # Try word-based matching (at least 70% of words present)
            words = sentence.split()
            if len(words) >= 3:
                matched_words = sum(1 for w in words if w in target_normalized)
                if matched_words / len(words) >= 0.7:
                    found.add(sentence)
                else:
                    missing.add(sentence)
            else:
                missing.add(sentence)

    return found, missing


def categorize_missing(missing: Set[str]) -> Dict[str, List[str]]:
    """Categorize missing content by type."""
    categories = {
        'navigation': [],      # Nav/menu items
        'boilerplate': [],     # Common HTML boilerplate
        'technical': [],       # Actual technical content
        'references': [],      # Citations/references
        'metadata': [],        # Copyright, dates, etc.
    }

    for sentence in missing:
        lower = sentence.lower()

        if any(kw in lower for kw in ['click', 'menu', 'navigation', 'home', 'next', 'previous', 'back']):
            categories['navigation'].append(sentence)
        elif any(kw in lower for kw in ['copyright', 'all rights', 'licensed', 'version', 'updated']):
            categories['metadata'].append(sentence)
        elif any(kw in lower for kw in ['reference', 'citation', 'see also', 'cf.', 'ibid']):
            categories['references'].append(sentence)
        elif any(kw in lower for kw in ['loading', 'please wait', 'javascript', 'browser']):
            categories['boilerplate'].append(sentence)
        else:
            categories['technical'].append(sentence)

    return categories


def verify_file(html_path: Path, theory_text: str) -> Dict:
    """Verify a single HTML file against theory_output.json."""
    result = {
        'file': html_path.name,
        'total_sentences': 0,
        'found': 0,
        'missing': 0,
        'coverage': 0.0,
        'missing_technical': [],
        'categories': {}
    }

    try:
        with open(html_path, 'r', encoding='utf-8', errors='replace') as f:
            html_content = f.read()
    except Exception as e:
        result['error'] = str(e)
        return result

    # Extract and process text
    html_text = extract_html_text(html_content)
    sentences = extract_sentences(html_text)

    result['total_sentences'] = len(sentences)

    if not sentences:
        result['coverage'] = 100.0  # No content to verify
        return result

    # Check coverage
    found, missing = check_sentence_coverage(sentences, theory_text)

    result['found'] = len(found)
    result['missing'] = len(missing)
    result['coverage'] = (len(found) / len(sentences)) * 100 if sentences else 100.0

    # Categorize missing
    categories = categorize_missing(missing)
    result['categories'] = {k: len(v) for k, v in categories.items()}
    result['missing_technical'] = categories['technical'][:10]  # First 10 technical

    return result


def main():
    """Main entry point."""
    base_dir = Path(__file__).parent.parent.parent
    theory_path = base_dir / 'AutoGenerated' / 'theory_output.json'

    # Files to verify
    files_to_verify = [
        base_dir / 'old_paper_v16.html',
        base_dir / 'sections' / 'appendix-e-delta-lat-probes.html',
        base_dir / 'sections' / 'appendix-f-subleading-dispersion.html',
        base_dir / 'sections' / 'cmb-bubble-collisions-comprehensive.html',
        base_dir / 'sections' / 'division-algebra-section.html',
        base_dir / 'sections' / 'einstein-hilbert-term.html',
        base_dir / 'sections' / 'xy-gauge-bosons.html',
    ]

    # Skip utility pages (not content)
    skip_files = ['index.html', 'formulas.html', 'parameters.html']

    print("=" * 70)
    print("Content Migration Verification")
    print("=" * 70)
    print(f"\nTheory output: {theory_path}")

    # Load theory_output.json
    if not theory_path.exists():
        print(f"ERROR: {theory_path} not found")
        return 1

    with open(theory_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    theory_text = extract_theory_text(data)
    print(f"Extracted {len(theory_text):,} characters from theory_output.json")

    # Verify each file
    print("\n" + "-" * 70)
    results = []

    for file_path in files_to_verify:
        if not file_path.exists():
            print(f"SKIP: {file_path.name} (not found)")
            continue

        if file_path.name in skip_files:
            print(f"SKIP: {file_path.name} (utility page)")
            continue

        print(f"\nVerifying: {file_path.name}")
        result = verify_file(file_path, theory_text)
        results.append(result)

        status = "PASS" if result['coverage'] >= 95 else "REVIEW" if result['coverage'] >= 80 else "FAIL"
        print(f"  Sentences: {result['total_sentences']}")
        print(f"  Found: {result['found']}, Missing: {result['missing']}")
        print(f"  Coverage: {result['coverage']:.1f}% [{status}]")

        if result['categories']:
            cats = result['categories']
            print(f"  Missing breakdown: tech={cats.get('technical', 0)}, nav={cats.get('navigation', 0)}, meta={cats.get('metadata', 0)}, ref={cats.get('references', 0)}, boiler={cats.get('boilerplate', 0)}")

        if result.get('missing_technical') and result['coverage'] < 95:
            print(f"  Sample missing technical content:")
            for i, text in enumerate(result['missing_technical'][:3]):
                print(f"    {i+1}. {text[:80]}...")

    # Summary
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)

    total_sentences = sum(r['total_sentences'] for r in results)
    total_found = sum(r['found'] for r in results)
    total_missing = sum(r['missing'] for r in results)
    overall_coverage = (total_found / total_sentences * 100) if total_sentences > 0 else 100

    print(f"\nTotal sentences analyzed: {total_sentences}")
    print(f"Total found in theory_output.json: {total_found}")
    print(f"Total missing: {total_missing}")
    print(f"Overall coverage: {overall_coverage:.1f}%")

    # Recommendations
    print("\n" + "-" * 70)
    print("RECOMMENDATIONS")
    print("-" * 70)

    can_delete = []
    need_review = []

    for r in results:
        if r['coverage'] >= 95:
            can_delete.append(r['file'])
        elif r['coverage'] >= 80:
            # Check if missing is just boilerplate/nav
            tech_missing = r['categories'].get('technical', 0)
            if tech_missing <= 5:
                can_delete.append(r['file'])
            else:
                need_review.append(r['file'])
        else:
            need_review.append(r['file'])

    if can_delete:
        print("\nFiles safe to delete (>=95% coverage or non-technical missing):")
        for f in can_delete:
            print(f"  - {f}")

    if need_review:
        print("\nFiles needing content review before deletion:")
        for f in need_review:
            print(f"  - {f}")

    # Return success if overall coverage is good
    return 0 if overall_coverage >= 80 else 1


if __name__ == "__main__":
    sys.exit(main())
