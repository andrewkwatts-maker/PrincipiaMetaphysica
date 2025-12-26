#!/usr/bin/env python3
"""
Audit all formulas/equations in principia-metaphysica-paper.html
and compare with theory_output.json to ensure single source of truth.
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Tuple
from collections import defaultdict

def extract_equations_from_html(html_file: Path) -> List[Dict]:
    """Extract all MathJax equations from HTML file."""
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()

    equations = []

    # Pattern to find section titles
    section_pattern = r'<h2[^>]*id="([^"]*)"[^>]*>(.*?)</h2>'
    subsection_pattern = r'<h3[^>]*id="([^"]*)"[^>]*>(.*?)</h3>'

    # Build section map
    sections = {}
    for match in re.finditer(section_pattern, content):
        section_id = match.group(1)
        section_title = re.sub(r'<[^>]+>', '', match.group(2)).strip()
        sections[match.start()] = (section_id, section_title, 'h2')

    for match in re.finditer(subsection_pattern, content):
        section_id = match.group(1)
        section_title = re.sub(r'<[^>]+>', '', match.group(2)).strip()
        sections[match.start()] = (section_id, section_title, 'h3')

    # Pattern to find derivation boxes
    derivation_pattern = r'<div[^>]*class="[^"]*derivation-box[^"]*"[^>]*>(.*?)</div>\s*</div>'
    derivations = {}
    for match in re.finditer(derivation_pattern, content, re.DOTALL):
        # Extract title
        title_match = re.search(r'<h4[^>]*>(.*?)</h4>', match.group(1))
        title = re.sub(r'<[^>]+>', '', title_match.group(1)).strip() if title_match else "Unnamed"
        derivations[match.start()] = title

    # Patterns for equations
    patterns = [
        # Display math: $$ ... $$ with optional equation number
        (r'\$\$(.*?)\$\$(?:\s*<span[^>]*equation-number[^>]*>\(([^)]+)\)</span>)?', 'display'),
        # Display math: \[ ... \]
        (r'\\\[(.*?)\\\]', 'display'),
        # Inline math: $ ... $ (but not $$)
        (r'(?<!\$)\$(?!\$)(.*?)\$(?!\$)', 'inline'),
        # Inline math: \( ... \)
        (r'\\\((.*?)\\\)', 'inline'),
    ]

    eq_counter = 0

    for pattern, eq_type in patterns:
        for match in re.finditer(pattern, content, re.DOTALL):
            eq_counter += 1
            latex = match.group(1).strip()
            eq_number = match.group(2) if len(match.groups()) > 1 and match.group(2) else None
            position = match.start()

            # Find current section
            current_section = ("unknown", "Unknown Section", "h2")
            for pos in sorted(sections.keys(), reverse=True):
                if pos < position:
                    current_section = sections[pos]
                    break

            # Find current derivation box (if any)
            current_derivation = None
            for pos in sorted(derivations.keys(), reverse=True):
                if pos < position < pos + 5000:  # Rough heuristic
                    current_derivation = derivations[pos]
                    break

            # Skip very short inline equations (likely variable names)
            if eq_type == 'inline' and len(latex) < 3:
                continue

            equations.append({
                'id': eq_counter,
                'latex': latex,
                'type': eq_type,
                'equation_number': eq_number,
                'section_id': current_section[0],
                'section_title': current_section[1],
                'section_level': current_section[2],
                'derivation_box': current_derivation,
                'position': position
            })

    return equations

def load_theory_formulas(json_file: Path) -> Dict:
    """Load formulas from theory_output.json."""
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Navigate nested structure
    if 'formulas' in data and isinstance(data['formulas'], dict):
        return data['formulas'].get('formulas', {})
    return {}

def normalize_latex(latex: str) -> str:
    """Normalize LaTeX for comparison."""
    # Remove extra whitespace
    latex = re.sub(r'\s+', ' ', latex).strip()
    # Remove display math delimiters
    latex = re.sub(r'^\\\[|\\\]$', '', latex)
    latex = re.sub(r'^\$\$|\$\$$', '', latex)
    return latex

def find_matches(equations: List[Dict], theory_formulas: Dict) -> Tuple[List, List, List]:
    """Find matches between paper equations and theory formulas."""
    matched = []
    paper_only = []
    theory_only = list(theory_formulas.keys())

    for eq in equations:
        eq_latex = normalize_latex(eq['latex'])

        # Try to match with theory formulas
        found_match = False
        for fid, formula_data in theory_formulas.items():
            theory_latex = normalize_latex(formula_data.get('latex', ''))

            # Check if substantially similar (accounting for minor formatting differences)
            if eq_latex == theory_latex or eq_latex in theory_latex or theory_latex in eq_latex:
                matched.append({
                    'formula_id': fid,
                    'equation': eq,
                    'theory_latex': theory_latex
                })
                if fid in theory_only:
                    theory_only.remove(fid)
                found_match = True
                break

        if not found_match:
            paper_only.append(eq)

    return matched, paper_only, theory_only

def generate_report(equations: List[Dict], theory_formulas: Dict,
                   matched: List, paper_only: List, theory_only: List,
                   output_file: Path):
    """Generate markdown audit report."""

    lines = [
        "# Paper Formula Audit Report",
        "",
        f"**Generated:** {Path(__file__).name}",
        f"**Date:** 2025-12-26",
        "",
        "## Executive Summary",
        "",
        f"- **Total equations in paper:** {len(equations)}",
        f"- **Total formulas in theory_output.json:** {len(theory_formulas)}",
        f"- **Matched:** {len(matched)}",
        f"- **Paper only (not in theory_output.json):** {len(paper_only)}",
        f"- **Theory only (not referenced in paper):** {len(theory_only)}",
        "",
        "---",
        "",
    ]

    # Section 1: Matched Formulas
    lines.extend([
        "## 1. Matched Formulas",
        "",
        f"These {len(matched)} equations appear in both the paper and theory_output.json:",
        "",
    ])

    for item in matched[:20]:  # Limit to first 20
        eq = item['equation']
        lines.append(f"### {item['formula_id']}")
        lines.append(f"- **Section:** {eq['section_title']}")
        if eq['equation_number']:
            lines.append(f"- **Equation number:** ({eq['equation_number']})")
        if eq['derivation_box']:
            lines.append(f"- **Derivation box:** {eq['derivation_box']}")
        lines.append(f"- **LaTeX:** `{eq['latex'][:100]}...`")
        lines.append("")

    if len(matched) > 20:
        lines.append(f"*... and {len(matched) - 20} more matched formulas*")
        lines.append("")

    # Section 2: Paper-only equations (NEED TO ADD)
    lines.extend([
        "---",
        "",
        "## 2. Paper Equations NOT in theory_output.json",
        "",
        f"These {len(paper_only)} equations appear in the paper but are MISSING from theory_output.json.",
        "They should be added to ensure single source of truth.",
        "",
    ])

    # Group by section
    by_section = defaultdict(list)
    for eq in paper_only:
        by_section[eq['section_title']].append(eq)

    for section_title in sorted(by_section.keys()):
        eqs = by_section[section_title]
        lines.append(f"### {section_title} ({len(eqs)} equations)")
        lines.append("")

        for eq in eqs[:10]:  # Limit per section
            lines.append(f"#### Equation {eq.get('equation_number', 'unnumbered')}")
            if eq['derivation_box']:
                lines.append(f"- **Context:** {eq['derivation_box']}")
            lines.append(f"- **Type:** {eq['type']}")
            lines.append(f"- **LaTeX:**")
            lines.append("```latex")
            lines.append(eq['latex'][:500])
            lines.append("```")
            lines.append("")

            # Suggest formula ID
            suggested_id = suggest_formula_id(eq)
            lines.append(f"**Suggested formula ID:** `{suggested_id}`")
            lines.append("")

        if len(eqs) > 10:
            lines.append(f"*... and {len(eqs) - 10} more equations in this section*")
            lines.append("")

    # Section 3: Theory-only formulas
    lines.extend([
        "---",
        "",
        "## 3. Theory Formulas NOT Referenced in Paper",
        "",
        f"These {len(theory_only)} formulas exist in theory_output.json but are not found in the paper:",
        "",
    ])

    for fid in theory_only[:30]:
        formula_data = theory_formulas[fid]
        lines.append(f"### {fid}")
        lines.append(f"- **Description:** {formula_data.get('description', 'N/A')}")
        lines.append(f"- **LaTeX:** `{formula_data.get('latex', 'N/A')[:100]}...`")
        lines.append("")

    if len(theory_only) > 30:
        lines.append(f"*... and {len(theory_only) - 30} more theory formulas*")
        lines.append("")

    # Section 4: Statistics by section
    lines.extend([
        "---",
        "",
        "## 4. Equation Distribution by Section",
        "",
        "| Section | Display Equations | Inline Equations | Total |",
        "|---------|-------------------|------------------|-------|",
    ])

    by_section_stats = defaultdict(lambda: {'display': 0, 'inline': 0})
    for eq in equations:
        by_section_stats[eq['section_title']][eq['type']] += 1

    for section in sorted(by_section_stats.keys()):
        stats = by_section_stats[section]
        total = stats['display'] + stats['inline']
        lines.append(f"| {section} | {stats['display']} | {stats['inline']} | {total} |")

    lines.extend([
        "",
        "---",
        "",
        "## 5. Recommendations",
        "",
        "### Priority 1: Add Missing Core Equations",
        "The following numbered equations in Sections 1-6 should be added to theory_output.json:",
        "",
    ])

    # Find numbered equations in first 6 sections
    priority_equations = [eq for eq in paper_only
                         if eq['equation_number']
                         and any(sec in eq['section_title'] for sec in ['1.', '2.', '3.', '4.', '5.', '6.'])]

    for eq in priority_equations[:15]:
        lines.append(f"- **({eq['equation_number']})** {eq['section_title']}")
        lines.append(f"  - Suggested ID: `{suggest_formula_id(eq)}`")
        lines.append(f"  - LaTeX: `{eq['latex'][:80]}...`")
        lines.append("")

    lines.extend([
        "### Priority 2: Verify Theory-Only Formulas",
        "Consider whether these theory formulas should appear in the paper:",
        "",
    ])

    for fid in theory_only[:10]:
        lines.append(f"- `{fid}`: {theory_formulas[fid].get('description', 'N/A')}")

    lines.extend([
        "",
        "### Priority 3: Inline Math Consolidation",
        f"There are {len([e for e in equations if e['type'] == 'inline'])} inline math expressions.",
        "Review whether frequently-used expressions should be promoted to named formulas.",
        "",
        "---",
        "",
        "## Appendix: Full Paper Equation List",
        "",
        f"Complete list of all {len(equations)} equations extracted from the paper:",
        "",
    ])

    for i, eq in enumerate(equations[:100], 1):
        lines.append(f"{i}. **{eq['section_title']}** - "
                    f"{'(' + eq['equation_number'] + ')' if eq['equation_number'] else 'unnumbered'} - "
                    f"{eq['type']}")

    if len(equations) > 100:
        lines.append(f"*... and {len(equations) - 100} more equations*")

    # Write report
    output_file.write_text('\n'.join(lines), encoding='utf-8')
    print(f"Report written to: {output_file}")

def suggest_formula_id(eq: Dict) -> str:
    """Suggest a formula ID based on equation context."""
    # Extract key terms from section title and derivation box
    section = eq['section_title'].lower()
    derivation = (eq['derivation_box'] or '').lower()
    latex = eq['latex'].lower()

    # Look for key terms
    if 'virasoro' in section or 'virasoro' in latex:
        return 'virasoro-central-charge' if 'central' in latex else 'virasoro-constraint'
    elif 'pneuma' in section or 'pneuma' in derivation:
        if 'stress' in latex or 't_{' in latex:
            return 'pneuma-stress-energy'
        elif 'lagrangian' in derivation or 'lagrangian' in latex:
            return 'pneuma-lagrangian'
        elif 'vev' in derivation or 'langle' in latex:
            return 'pneuma-vev-dynamics'
    elif 'master action' in section or 'master action' in derivation:
        return 'master-action-full'
    elif 'cascade' in section or 'reduction' in section:
        return 'dimensional-reduction'
    elif 'entropy' in section or 'entropy' in derivation:
        return 'holographic-entropy'
    elif 'racetrack' in section or 'racetrack' in derivation:
        if 'potential' in latex or 'v(' in latex:
            return 'racetrack-potential'
        else:
            return 'racetrack-vev'
    elif 'g_2' in latex or 'g2' in section.replace('₂', '2'):
        return 'g2-manifold-property'

    # Default: use equation number if available
    if eq['equation_number']:
        return f"eq-{eq['equation_number'].replace('.', '-')}"

    return f"unnamed-{eq['id']}"

def main():
    base_dir = Path(r'h:\Github\PrincipiaMetaphysica')
    html_file = base_dir / 'principia-metaphysica-paper.html'
    json_file = base_dir / 'theory_output.json'
    output_file = base_dir / 'reports' / 'PAPER_FORMULA_AUDIT.md'

    output_file.parent.mkdir(exist_ok=True)

    print("Extracting equations from paper...")
    equations = extract_equations_from_html(html_file)
    print(f"Found {len(equations)} equations")

    print("\nLoading theory formulas...")
    theory_formulas = load_theory_formulas(json_file)
    print(f"Found {len(theory_formulas)} theory formulas")

    print("\nMatching equations...")
    matched, paper_only, theory_only = find_matches(equations, theory_formulas)

    print(f"\nResults:")
    print(f"  Matched: {len(matched)}")
    print(f"  Paper only: {len(paper_only)}")
    print(f"  Theory only: {len(theory_only)}")

    print("\nGenerating report...")
    generate_report(equations, theory_formulas, matched, paper_only, theory_only, output_file)

    print("\n✓ Audit complete!")

if __name__ == '__main__':
    main()
