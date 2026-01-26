#!/usr/bin/env python3
"""
Audit Hardcoded Values in JavaScript Files

This script extracts all numeric physics values from JS files and compares
them against theory_output.json to identify discrepancies.

Usage:
    python scripts/audit_hardcoded_values.py

Outputs:
    reports/hardcoded_values_audit.json  - Full audit report
    reports/hardcoded_values_audit.txt   - Human-readable summary
"""

import re
import json
from pathlib import Path
from dataclasses import dataclass, asdict
from typing import Dict, List, Any, Optional
from collections import defaultdict

# Project root
PROJECT_ROOT = Path(__file__).parent.parent

# JS files to audit
JS_FILES = [
    "js/theory-constants.js",
    "js/theory-constants-enhanced.js",
    "js/formula-definitions.js",
    "js/formula-registry.js",
    "js/formula-database.js",
    "js/pm-parameter-data.js",
    "js/pm-constants-loader.js",
]

# Patterns to extract numeric values
PATTERNS = {
    # Property assignments: key: 0.123 or key: 1.23e-5
    "property": re.compile(r'(\w+)\s*:\s*(-?\d+\.?\d*(?:e[+-]?\d+)?)\s*[,\}\n]', re.IGNORECASE),

    # Scientific notation in strings: 1.23×10^16 or 10^-5
    "scientific_html": re.compile(r'(\d+\.?\d*)\s*[×x]\s*10\s*<sup>([+-]?\d+)</sup>', re.IGNORECASE),

    # Equals assignments in comments or strings: = 0.123
    "equals": re.compile(r'=\s*(-?\d+\.?\d*(?:e[+-]?\d+)?)\s*(?:GeV|eV|years|m|s|K|°)?'),

    # Standalone numbers with units: 0.082 eV
    "with_units": re.compile(r'(-?\d+\.?\d*(?:e[+-]?\d+)?)\s*(GeV|eV|years|m|s|K|TeV|MeV|keV)'),
}

# Categories for organizing values
CATEGORIES = {
    "dimensions": ["D_", "dimension", "26", "13", "spinor", "clifford"],
    "topology": ["b3", "chi", "generation", "n_gen", "h11", "h21", "h31"],
    "cosmology": ["w0", "w_", "wa", "H0", "Omega", "Lambda", "dark", "hubble"],
    "neutrino": ["nu", "neutrino", "theta_1", "theta_2", "delta_CP", "PMNS", "mNu"],
    "particle": ["higgs", "m_h", "GUT", "alpha", "proton", "decay", "mass"],
    "constants": ["Planck", "M_Pl", "G_N", "fine_structure", "137"],
    "ckm": ["V_us", "V_cb", "V_ub", "CKM", "Jarlskog"],
}


@dataclass
class ExtractedValue:
    """A value extracted from a JS file"""
    file: str
    line_number: int
    key: str
    value: float
    raw_text: str
    pattern_type: str
    category: str = "unknown"


def categorize_key(key: str, context: str = "") -> str:
    """Determine category based on key name and context"""
    combined = f"{key} {context}".lower()

    for category, keywords in CATEGORIES.items():
        for keyword in keywords:
            if keyword.lower() in combined:
                return category

    return "other"


def extract_values_from_file(filepath: Path) -> List[ExtractedValue]:
    """Extract all numeric values from a JS file"""
    values = []

    try:
        content = filepath.read_text(encoding='utf-8')
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        return values

    lines = content.split('\n')

    for line_num, line in enumerate(lines, 1):
        # Skip comments
        if line.strip().startswith('//') or line.strip().startswith('*'):
            continue

        # Try each pattern
        for pattern_name, pattern in PATTERNS.items():
            for match in pattern.finditer(line):
                try:
                    if pattern_name == "property":
                        key = match.group(1)
                        value_str = match.group(2)
                    elif pattern_name == "scientific_html":
                        # Convert 1.23×10^16 to float
                        mantissa = float(match.group(1))
                        exponent = int(match.group(2))
                        value_str = str(mantissa * (10 ** exponent))
                        key = f"scientific_{line_num}"
                    elif pattern_name == "with_units":
                        value_str = match.group(1)
                        unit = match.group(2)
                        key = f"value_with_{unit}_{line_num}"
                    else:
                        value_str = match.group(1)
                        key = f"equals_{line_num}"

                    # Parse value
                    value = float(value_str)

                    # Skip trivial values (0, 1, 2, etc.)
                    if abs(value) < 0.001 or (abs(value) < 100 and value == int(value) and value not in [26, 24, 13]):
                        continue

                    # Determine category
                    category = categorize_key(key, line)

                    values.append(ExtractedValue(
                        file=str(filepath.relative_to(PROJECT_ROOT)),
                        line_number=line_num,
                        key=key,
                        value=value,
                        raw_text=match.group(0)[:80],
                        pattern_type=pattern_name,
                        category=category
                    ))

                except (ValueError, IndexError):
                    continue

    return values


def load_theory_output() -> Dict[str, Any]:
    """Load theory_output.json"""
    theory_path = PROJECT_ROOT / "AutoGenerated" / "theory_output.json"
    if not theory_path.exists():
        print(f"Warning: {theory_path} not found")
        return {}

    try:
        with open(theory_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading theory_output.json: {e}")
        return {}


def flatten_dict(d: Dict, prefix: str = '') -> Dict[str, float]:
    """Flatten nested dict to key.subkey format"""
    items = {}
    for k, v in d.items():
        new_key = f"{prefix}.{k}" if prefix else k
        if isinstance(v, dict):
            if 'value' in v and isinstance(v['value'], (int, float)) and not isinstance(v['value'], bool):
                items[new_key] = float(v['value'])
            else:
                items.update(flatten_dict(v, new_key))
        elif isinstance(v, (int, float)) and not isinstance(v, bool):
            items[new_key] = float(v)
    return items


def find_matching_theory_value(extracted: ExtractedValue, theory_values: Dict[str, float]) -> Optional[tuple]:
    """Try to find a matching value in theory_output"""
    # Try exact key match
    if extracted.key in theory_values:
        return (extracted.key, theory_values[extracted.key])

    # Try partial key match
    key_lower = extracted.key.lower()
    for theory_key, theory_value in theory_values.items():
        if key_lower in theory_key.lower() or theory_key.lower() in key_lower:
            # Check if values are close
            if abs(extracted.value - theory_value) / max(abs(theory_value), 1e-10) < 0.01:
                return (theory_key, theory_value)

    # Try value match (within 1%)
    for theory_key, theory_value in theory_values.items():
        if abs(theory_value) > 1e-20:
            if abs(extracted.value - theory_value) / abs(theory_value) < 0.01:
                return (theory_key, theory_value)

    return None


def generate_report(all_values: List[ExtractedValue], theory_output: Dict) -> Dict:
    """Generate comprehensive audit report"""

    # Flatten theory output parameters
    theory_values = {}
    if 'parameters' in theory_output:
        theory_values = flatten_dict(theory_output['parameters'])

    # Categorize findings
    by_file = defaultdict(list)
    by_category = defaultdict(list)
    matched = []
    unmatched = []

    for val in all_values:
        by_file[val.file].append(val)
        by_category[val.category].append(val)

        match = find_matching_theory_value(val, theory_values)
        if match:
            matched.append({
                "extracted": asdict(val),
                "theory_key": match[0],
                "theory_value": match[1],
                "difference": val.value - match[1]
            })
        else:
            unmatched.append(asdict(val))

    return {
        "summary": {
            "total_values_found": len(all_values),
            "matched_to_theory": len(matched),
            "unmatched": len(unmatched),
            "files_audited": len(by_file),
            "categories": {k: len(v) for k, v in by_category.items()}
        },
        "by_file": {k: [asdict(v) for v in vals] for k, vals in by_file.items()},
        "by_category": {k: [asdict(v) for v in vals] for k, vals in by_category.items()},
        "matched": matched,
        "unmatched": unmatched,
        "theory_values_count": len(theory_values)
    }


def generate_text_report(report: Dict) -> str:
    """Generate human-readable summary"""
    lines = [
        "=" * 70,
        "HARDCODED VALUES AUDIT REPORT",
        "Principia Metaphysica v16.2",
        "=" * 70,
        "",
        "SUMMARY",
        "-" * 40,
        f"Total values extracted from JS:  {report['summary']['total_values_found']}",
        f"Matched to theory_output.json:   {report['summary']['matched_to_theory']}",
        f"Unmatched (need migration):      {report['summary']['unmatched']}",
        f"Theory output parameters:        {report['theory_values_count']}",
        "",
        "BY CATEGORY",
        "-" * 40,
    ]

    for cat, count in sorted(report['summary']['categories'].items(), key=lambda x: -x[1]):
        lines.append(f"  {cat:20} {count:5}")

    lines.extend([
        "",
        "BY FILE",
        "-" * 40,
    ])

    for file, vals in sorted(report['by_file'].items(), key=lambda x: -len(x[1])):
        lines.append(f"  {file:45} {len(vals):5} values")

    lines.extend([
        "",
        "TOP UNMATCHED VALUES (need geometric derivation)",
        "-" * 40,
    ])

    for val in report['unmatched'][:20]:
        lines.append(f"  {val['key']:30} = {val['value']:<15} ({val['category']})")

    if len(report['unmatched']) > 20:
        lines.append(f"  ... and {len(report['unmatched']) - 20} more")

    lines.extend([
        "",
        "MATCHED VALUES WITH DIFFERENCES",
        "-" * 40,
    ])

    for match in report['matched']:
        if abs(match['difference']) > 1e-10:
            lines.append(f"  {match['theory_key']:40}")
            lines.append(f"    JS:     {match['extracted']['value']}")
            lines.append(f"    Theory: {match['theory_value']}")
            lines.append(f"    Diff:   {match['difference']}")

    lines.append("")
    lines.append("=" * 70)

    return "\n".join(lines)


def main():
    """Run the audit"""
    print("Auditing hardcoded values in JavaScript files...")
    print()

    # Extract values from all JS files
    all_values = []
    for js_file in JS_FILES:
        filepath = PROJECT_ROOT / js_file
        if filepath.exists():
            values = extract_values_from_file(filepath)
            all_values.extend(values)
            print(f"  {js_file}: {len(values)} values found")
        else:
            print(f"  {js_file}: NOT FOUND")

    print()
    print(f"Total: {len(all_values)} values extracted")
    print()

    # Load theory output
    theory_output = load_theory_output()

    # Generate report
    report = generate_report(all_values, theory_output)

    # Save JSON report
    reports_dir = PROJECT_ROOT / "reports"
    reports_dir.mkdir(exist_ok=True)

    json_path = reports_dir / "hardcoded_values_audit.json"
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2)
    print(f"JSON report: {json_path}")

    # Save text report
    text_report = generate_text_report(report)
    txt_path = reports_dir / "hardcoded_values_audit.txt"
    with open(txt_path, 'w', encoding='utf-8') as f:
        f.write(text_report)
    print(f"Text report: {txt_path}")

    # Print summary
    print()
    print(text_report)


if __name__ == "__main__":
    main()
