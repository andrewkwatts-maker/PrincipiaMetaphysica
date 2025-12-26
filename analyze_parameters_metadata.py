#!/usr/bin/env python3
"""
Analyze parameters section of theory_output.json for missing or incomplete metadata.
"""

import json
from pathlib import Path
from typing import Dict, List, Any, Set
from collections import defaultdict

def analyze_parameter_metadata(param_data: Dict[str, Any], param_path: str) -> Dict[str, Any]:
    """Analyze metadata completeness for a single parameter."""
    issues = {
        'missing_value': 'value' not in param_data and 'predicted' not in param_data,
        'missing_units': 'units' not in param_data,
        'missing_description': 'description' not in param_data and 'derivation' not in param_data,
        'missing_source': 'source' not in param_data,
        'missing_status': 'status' not in param_data,
        'missing_uncertainty': ('uncertainty' not in param_data and
                               'sigma' not in param_data and
                               'predicted_error' not in param_data and
                               'experimental_error' not in param_data)
    }

    return {
        'path': param_path,
        'has_value': 'value' in param_data or 'predicted' in param_data,
        'has_units': 'units' in param_data,
        'has_description': 'description' in param_data or 'derivation' in param_data,
        'has_source': 'source' in param_data,
        'has_status': 'status' in param_data,
        'has_uncertainty': ('uncertainty' in param_data or
                           'sigma' in param_data or
                           'predicted_error' in param_data or
                           'experimental_error' in param_data),
        'issues': issues,
        'all_keys': list(param_data.keys()),
        'data': param_data
    }

def is_leaf_parameter(value: Any) -> bool:
    """Check if a value is a leaf parameter (has value-like fields)."""
    if not isinstance(value, dict):
        return False

    # Check for value-like keys
    value_keys = {'value', 'predicted', 'experimental', 'observed'}
    metadata_keys = {'units', 'description', 'derivation', 'source', 'status', 'uncertainty', 'sigma'}

    keys = set(value.keys())

    # If it has value-like keys or metadata keys, it's likely a leaf
    if keys & (value_keys | metadata_keys):
        return True

    return False

def is_flat_param_collection(value: Any) -> bool:
    """Check if a dict is a flat collection of parameters (e.g., dimensions: {D_BULK: 26, D_INTERNAL: 7})."""
    if not isinstance(value, dict):
        return False

    # If all values are primitives (int, float, str), it's a flat collection
    if all(isinstance(v, (int, float, str, bool)) for v in value.values()):
        return True

    # If all values are lists of primitives, it's also a flat collection
    if all(isinstance(v, list) and all(isinstance(x, (int, float, str, bool)) for x in v) for v in value.values()):
        return True

    return False

def traverse_parameters(data: Dict, prefix: str = "", skip_keys: set = None) -> List[Dict[str, Any]]:
    """Recursively traverse parameter structure to find all leaf parameters."""
    if skip_keys is None:
        skip_keys = {'version'}  # Skip metadata keys

    results = []

    for key, value in data.items():
        if key in skip_keys:
            continue

        current_path = f"{prefix}.{key}" if prefix else key

        if isinstance(value, dict):
            # Check if this is a leaf parameter
            if is_leaf_parameter(value):
                # This is a well-structured parameter with metadata
                analysis = analyze_parameter_metadata(value, current_path)
                results.append(analysis)
            elif is_flat_param_collection(value):
                # This is a flat collection like dimensions: {D_BULK: 26, D_INTERNAL: 7}
                # Treat the whole collection as one parameter for now
                analysis = analyze_parameter_metadata(value, current_path)
                results.append(analysis)
            else:
                # This is a container, recurse
                results.extend(traverse_parameters(value, current_path, skip_keys))
        elif isinstance(value, (int, float, str, list)):
            # This is a direct value, create a minimal parameter entry
            param_data = {'value': value}
            analysis = analyze_parameter_metadata(param_data, current_path)
            results.append(analysis)

    return results

def main():
    # Load theory_output.json
    theory_file = Path(r'h:\Github\PrincipiaMetaphysica\theory_output.json')
    with open(theory_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    parameters = data.get('parameters', {})

    # Identify top-level structure
    top_level_keys = list(parameters.keys())

    # Traverse to find all parameters
    all_params = traverse_parameters(parameters)

    total_parameters = len(all_params)

    # Count categories (depth-1 items)
    categories = set()
    for p in all_params:
        parts = p['path'].split('.')
        if len(parts) >= 1:
            categories.add(parts[0])

    total_categories = len(categories)

    # Generate report
    report_lines = []
    report_lines.append("# Parameters Metadata Audit Report")
    report_lines.append("")
    report_lines.append(f"**Generated:** {Path(__file__).name}")
    report_lines.append(f"**Source:** theory_output.json")
    report_lines.append(f"**Date:** 2025-12-26")
    report_lines.append("")

    # Summary
    report_lines.append("## Executive Summary")
    report_lines.append("")
    report_lines.append(f"- **Total Top-Level Categories:** {total_categories}")
    report_lines.append(f"- **Total Individual Parameters:** {total_parameters}")
    report_lines.append(f"- **Top-Level Keys in Parameters:** {len(top_level_keys)}")
    report_lines.append("")

    # Category list with counts
    report_lines.append("## Parameter Categories")
    report_lines.append("")
    category_counts = defaultdict(int)
    for p in all_params:
        cat = p['path'].split('.')[0]
        category_counts[cat] += 1

    for i, (cat, count) in enumerate(sorted(category_counts.items()), 1):
        report_lines.append(f"{i}. **{cat}** ({count} parameters)")
    report_lines.append("")

    # Top-level keys
    report_lines.append("## Top-level Keys in Parameters Section")
    report_lines.append("")
    for key in sorted(top_level_keys):
        count = category_counts.get(key, 0)
        if count > 0:
            report_lines.append(f"- `{key}` ({count} parameters)")
        else:
            report_lines.append(f"- `{key}` (metadata)")
    report_lines.append("")

    # Missing metadata analysis
    missing_value = [p for p in all_params if p['issues']['missing_value']]
    missing_units = [p for p in all_params if p['issues']['missing_units']]
    missing_description = [p for p in all_params if p['issues']['missing_description']]
    missing_source = [p for p in all_params if p['issues']['missing_source']]
    missing_status = [p for p in all_params if p['issues']['missing_status']]
    missing_uncertainty = [p for p in all_params if p['issues']['missing_uncertainty']]

    # Missing values
    report_lines.append("## 1. Parameters with Missing Values")
    report_lines.append("")
    if missing_value:
        report_lines.append(f"**Count:** {len(missing_value)} / {total_parameters}")
        report_lines.append("")
        report_lines.append("| Parameter Path | Available Keys |")
        report_lines.append("|----------------|----------------|")
        for p in missing_value[:20]:  # Limit to first 20
            keys_str = ", ".join(p['all_keys'][:6])
            if len(p['all_keys']) > 6:
                keys_str += "..."
            report_lines.append(f"| `{p['path']}` | {keys_str} |")
        if len(missing_value) > 20:
            report_lines.append(f"| ... | {len(missing_value) - 20} more |")
    else:
        report_lines.append("**Count:** 0 - All parameters have values!")
    report_lines.append("")

    # Missing units
    report_lines.append("## 2. Parameters with Missing Units")
    report_lines.append("")
    if missing_units:
        report_lines.append(f"**Count:** {len(missing_units)} / {total_parameters}")
        report_lines.append("")
        report_lines.append("| Parameter Path | Available Keys |")
        report_lines.append("|----------------|----------------|")
        for p in missing_units[:20]:
            keys_str = ", ".join(p['all_keys'][:6])
            if len(p['all_keys']) > 6:
                keys_str += "..."
            report_lines.append(f"| `{p['path']}` | {keys_str} |")
        if len(missing_units) > 20:
            report_lines.append(f"| ... | {len(missing_units) - 20} more |")
    else:
        report_lines.append("**Count:** 0 - All parameters have units!")
    report_lines.append("")

    # Missing descriptions
    report_lines.append("## 3. Parameters with Missing Descriptions")
    report_lines.append("")
    if missing_description:
        report_lines.append(f"**Count:** {len(missing_description)} / {total_parameters}")
        report_lines.append("")
        report_lines.append("Note: Accepts 'description' or 'derivation' fields.")
        report_lines.append("")
        report_lines.append("| Parameter Path | Available Keys |")
        report_lines.append("|----------------|----------------|")
        for p in missing_description[:20]:
            keys_str = ", ".join(p['all_keys'][:6])
            if len(p['all_keys']) > 6:
                keys_str += "..."
            report_lines.append(f"| `{p['path']}` | {keys_str} |")
        if len(missing_description) > 20:
            report_lines.append(f"| ... | {len(missing_description) - 20} more |")
    else:
        report_lines.append("**Count:** 0 - All parameters have descriptions!")
    report_lines.append("")

    # Missing source
    report_lines.append("## 4. Parameters with Missing Source/Derivation Info")
    report_lines.append("")
    if missing_source:
        report_lines.append(f"**Count:** {len(missing_source)} / {total_parameters}")
        report_lines.append("")
        report_lines.append("| Parameter Path | Has Derivation | Available Keys |")
        report_lines.append("|----------------|----------------|----------------|")
        for p in missing_source[:20]:
            has_deriv = "derivation" in p['all_keys']
            keys_str = ", ".join(p['all_keys'][:6])
            if len(p['all_keys']) > 6:
                keys_str += "..."
            deriv_str = "Yes" if has_deriv else "No"
            report_lines.append(f"| `{p['path']}` | {deriv_str} | {keys_str} |")
        if len(missing_source) > 20:
            report_lines.append(f"| ... | ... | {len(missing_source) - 20} more |")
    else:
        report_lines.append("**Count:** 0 - All parameters have source info!")
    report_lines.append("")

    # Missing status
    report_lines.append("## 5. Parameters with Missing Status")
    report_lines.append("")
    if missing_status:
        report_lines.append(f"**Count:** {len(missing_status)} / {total_parameters}")
        report_lines.append("")
        report_lines.append("Expected status values: INPUT, DERIVED, GEOMETRIC")
        report_lines.append("")
        report_lines.append("| Parameter Path | Available Keys |")
        report_lines.append("|----------------|----------------|")
        for p in missing_status[:20]:
            keys_str = ", ".join(p['all_keys'][:6])
            if len(p['all_keys']) > 6:
                keys_str += "..."
            report_lines.append(f"| `{p['path']}` | {keys_str} |")
        if len(missing_status) > 20:
            report_lines.append(f"| ... | ... | {len(missing_status) - 20} more |")
    else:
        report_lines.append("**Count:** 0 - All parameters have status!")
    report_lines.append("")

    # Missing uncertainty
    report_lines.append("## 6. Parameters with Missing Uncertainty")
    report_lines.append("")
    if missing_uncertainty:
        report_lines.append(f"**Count:** {len(missing_uncertainty)} / {total_parameters}")
        report_lines.append("")
        report_lines.append("Note: Accepts 'uncertainty', 'sigma', 'predicted_error', or 'experimental_error'.")
        report_lines.append("")
        report_lines.append("| Parameter Path | Status | Available Keys |")
        report_lines.append("|----------------|--------|----------------|")
        for p in missing_uncertainty[:20]:
            status = p['data'].get('status', 'N/A')
            keys_str = ", ".join(p['all_keys'][:6])
            if len(p['all_keys']) > 6:
                keys_str += "..."
            report_lines.append(f"| `{p['path']}` | {status} | {keys_str} |")
        if len(missing_uncertainty) > 20:
            report_lines.append(f"| ... | ... | {len(missing_uncertainty) - 20} more |")
    else:
        report_lines.append("**Count:** 0 - All parameters have uncertainty info!")
    report_lines.append("")

    # Metadata completeness by category
    report_lines.append("## Metadata Completeness by Category")
    report_lines.append("")
    report_lines.append("| Category | Parameters | Missing Units | Missing Desc | Missing Source | Missing Status | Missing Uncertainty |")
    report_lines.append("|----------|------------|---------------|--------------|----------------|----------------|---------------------|")

    for category in sorted(categories):
        cat_params = [p for p in all_params if p['path'].startswith(category)]
        total = len(cat_params)
        m_units = sum(1 for p in cat_params if p['issues']['missing_units'])
        m_desc = sum(1 for p in cat_params if p['issues']['missing_description'])
        m_source = sum(1 for p in cat_params if p['issues']['missing_source'])
        m_status = sum(1 for p in cat_params if p['issues']['missing_status'])
        m_uncertain = sum(1 for p in cat_params if p['issues']['missing_uncertainty'])

        report_lines.append(f"| {category} | {total} | {m_units} | {m_desc} | {m_source} | {m_status} | {m_uncertain} |")
    report_lines.append("")

    # Completeness percentage
    report_lines.append("## Overall Completeness Metrics")
    report_lines.append("")

    def pct(count, total):
        return f"{(total - count) / total * 100:.1f}%" if total > 0 else "N/A"

    report_lines.append(f"- **Values present:** {pct(len(missing_value), total_parameters)} ({total_parameters - len(missing_value)}/{total_parameters})")
    report_lines.append(f"- **Units present:** {pct(len(missing_units), total_parameters)} ({total_parameters - len(missing_units)}/{total_parameters})")
    report_lines.append(f"- **Descriptions present:** {pct(len(missing_description), total_parameters)} ({total_parameters - len(missing_description)}/{total_parameters})")
    report_lines.append(f"- **Source info present:** {pct(len(missing_source), total_parameters)} ({total_parameters - len(missing_source)}/{total_parameters})")
    report_lines.append(f"- **Status present:** {pct(len(missing_status), total_parameters)} ({total_parameters - len(missing_status)}/{total_parameters})")
    report_lines.append(f"- **Uncertainty present:** {pct(len(missing_uncertainty), total_parameters)} ({total_parameters - len(missing_uncertainty)}/{total_parameters})")
    report_lines.append("")

    # Recommendations
    report_lines.append("## Recommendations")
    report_lines.append("")
    report_lines.append("### High Priority")
    report_lines.append("")

    priority_items = []

    if missing_status:
        priority_items.append((len(missing_status), "status", "INPUT, DERIVED, or GEOMETRIC"))
    if missing_description:
        priority_items.append((len(missing_description), "description/derivation", "physical meaning"))
    if missing_source:
        priority_items.append((len(missing_source), "source", "experimental reference or theoretical basis"))

    priority_items.sort(reverse=True)

    for i, (count, field, detail) in enumerate(priority_items[:3], 1):
        pct_missing = count / total_parameters * 100
        report_lines.append(f"{i}. **Add {field}** to {count} parameters ({pct_missing:.1f}% of total)")
        report_lines.append(f"   - Should specify: {detail}")
        report_lines.append("   - Critical for understanding data flow and provenance")
        report_lines.append("")

    report_lines.append("### Medium Priority")
    report_lines.append("")

    med_items = []

    if missing_units:
        med_items.append((len(missing_units), "units"))
    if missing_uncertainty:
        med_items.append((len(missing_uncertainty), "uncertainty"))

    for i, (count, field) in enumerate(med_items, 1):
        pct_missing = count / total_parameters * 100
        report_lines.append(f"{i}. **Add {field}** to {count} parameters ({pct_missing:.1f}% of total)")
        if field == "units":
            report_lines.append("   - Use SI or natural units (GeV, eV^2, degrees, dimensionless, etc.)")
        else:
            report_lines.append("   - Express as experimental error, predicted error, sigma, or uncertainty")
        report_lines.append("")

    report_lines.append("### Standard Metadata Schema")
    report_lines.append("")
    report_lines.append("Recommended fields for each parameter:")
    report_lines.append("```json")
    report_lines.append("{")
    report_lines.append('  "value": <number or array>,          // or "predicted", "experimental", "observed"')
    report_lines.append('  "units": "GeV" | "degrees" | ...,    // Physical units')
    report_lines.append('  "description": "...",                 // Physical meaning (or "derivation")')
    report_lines.append('  "status": "INPUT|DERIVED|GEOMETRIC", // Origin type')
    report_lines.append('  "source": "...",                      // Experimental ref or calculation method')
    report_lines.append('  "uncertainty": <number>,              // or "sigma", "predicted_error", etc.')
    report_lines.append("}")
    report_lines.append("```")
    report_lines.append("")

    # Sample well-documented parameters
    report_lines.append("## Examples of Well-Documented Parameters")
    report_lines.append("")

    complete_params = [p for p in all_params
                      if not any(p['issues'].values())]

    if complete_params:
        report_lines.append(f"Found {len(complete_params)} parameters with complete metadata ({len(complete_params)/total_parameters*100:.1f}%):")
        report_lines.append("")
        for p in complete_params[:10]:  # Show first 10
            report_lines.append(f"- `{p['path']}`")
        if len(complete_params) > 10:
            report_lines.append(f"- ... and {len(complete_params) - 10} more")
    else:
        report_lines.append("No parameters have complete metadata across all checked fields.")
    report_lines.append("")

    # Sample parameter with details
    if all_params:
        report_lines.append("## Sample Parameter Details")
        report_lines.append("")

        # Find a well-documented one
        good_param = None
        for p in all_params:
            issue_count = sum(1 for v in p['issues'].values() if v)
            if issue_count <= 2:
                good_param = p
                break

        if not good_param:
            good_param = all_params[0]

        report_lines.append(f"### `{good_param['path']}`")
        report_lines.append("")
        report_lines.append("```json")
        report_lines.append(json.dumps(good_param['data'], indent=2))
        report_lines.append("```")
        report_lines.append("")

        report_lines.append("**Metadata Present:**")
        for key, present in [
            ('value', good_param['has_value']),
            ('units', good_param['has_units']),
            ('description', good_param['has_description']),
            ('source', good_param['has_source']),
            ('status', good_param['has_status']),
            ('uncertainty', good_param['has_uncertainty'])
        ]:
            status = "✓" if present else "✗"
            report_lines.append(f"- {status} {key}")
        report_lines.append("")

    # Write report
    report_path = Path(r'h:\Github\PrincipiaMetaphysica\reports\PARAMETERS_METADATA_AUDIT.md')
    report_path.parent.mkdir(parents=True, exist_ok=True)

    with open(report_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(report_lines))

    print(f"Report written to: {report_path}")
    print(f"\nSummary:")
    print(f"  Total categories: {total_categories}")
    print(f"  Total parameters: {total_parameters}")
    print(f"  Missing values: {len(missing_value)}")
    print(f"  Missing units: {len(missing_units)}")
    print(f"  Missing descriptions: {len(missing_description)}")
    print(f"  Missing source/derivation: {len(missing_source)}")
    print(f"  Missing status: {len(missing_status)}")
    print(f"  Missing uncertainty: {len(missing_uncertainty)}")
    print(f"  Complete parameters: {len(complete_params)}")

if __name__ == '__main__':
    main()
