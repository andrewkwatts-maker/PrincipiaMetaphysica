#!/usr/bin/env python3
"""
Validate that all parameter metadata has been properly fixed.
"""

import json
from pathlib import Path
from typing import Dict, Any, List, Tuple

def load_theory_output(filepath: str) -> Dict[str, Any]:
    """Load theory_output.json"""
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def count_params_recursive(params: Dict[str, Any], prefix: str = "") -> List[Tuple[str, Dict]]:
    """Recursively count parameters and return list of (path, param_dict) tuples"""
    result = []

    for key, value in params.items():
        if key == 'version':
            continue

        current_path = f"{prefix}.{key}" if prefix else key

        # If value has a 'value' key, it's a parameter
        if isinstance(value, dict) and 'value' in value:
            result.append((current_path, value))
        # Otherwise, recurse into nested structure
        elif isinstance(value, dict):
            result.extend(count_params_recursive(value, current_path))

    return result

def check_metadata_completeness(params_list: List[Tuple[str, Dict]]) -> Dict[str, Any]:
    """Check metadata completeness for all parameters"""

    stats = {
        'total': len(params_list),
        'has_value': 0,
        'has_units': 0,
        'has_description': 0,
        'has_status': 0,
        'has_source': 0,
        'has_uncertainty': 0,
        'missing_units': [],
        'missing_description': [],
        'missing_status': [],
        'missing_source': [],
    }

    for path, param in params_list:
        # Check for value
        if 'value' in param:
            stats['has_value'] += 1

        # Check for units
        if 'units' in param:
            stats['has_units'] += 1
        else:
            stats['missing_units'].append(path)

        # Check for description or derivation
        if 'description' in param or 'derivation' in param:
            stats['has_description'] += 1
        else:
            stats['missing_description'].append(path)

        # Check for status
        if 'status' in param:
            stats['has_status'] += 1
        else:
            stats['missing_status'].append(path)

        # Check for source or derivation
        if 'source' in param or 'derivation' in param:
            stats['has_source'] += 1
        else:
            stats['missing_source'].append(path)

        # Check for uncertainty (various field names)
        if any(k in param for k in ['uncertainty', 'sigma', 'predicted_error', 'experimental_error']):
            stats['has_uncertainty'] += 1

    return stats

def print_report(stats: Dict[str, Any]) -> None:
    """Print validation report"""
    total = stats['total']

    print("="*70)
    print("PARAMETER METADATA VALIDATION REPORT")
    print("="*70)
    print(f"\nTotal Parameters Found: {total}")
    print(f"\nMetadata Completeness:")
    print(f"  - Values present:       {stats['has_value']:2d}/{total} ({100*stats['has_value']/total:5.1f}%)")
    print(f"  - Units present:        {stats['has_units']:2d}/{total} ({100*stats['has_units']/total:5.1f}%)")
    print(f"  - Descriptions present: {stats['has_description']:2d}/{total} ({100*stats['has_description']/total:5.1f}%)")
    print(f"  - Status present:       {stats['has_status']:2d}/{total} ({100*stats['has_status']/total:5.1f}%)")
    print(f"  - Source present:       {stats['has_source']:2d}/{total} ({100*stats['has_source']/total:5.1f}%)")
    print(f"  - Uncertainty present:  {stats['has_uncertainty']:2d}/{total} ({100*stats['has_uncertainty']/total:5.1f}%)")

    # Check for missing fields
    if stats['missing_units']:
        print(f"\n[WARNING] Missing units in {len(stats['missing_units'])} parameters:")
        for path in stats['missing_units'][:5]:
            print(f"  - {path}")
        if len(stats['missing_units']) > 5:
            print(f"  ... and {len(stats['missing_units'])-5} more")

    if stats['missing_description']:
        print(f"\n[WARNING] Missing description in {len(stats['missing_description'])} parameters:")
        for path in stats['missing_description'][:5]:
            print(f"  - {path}")
        if len(stats['missing_description']) > 5:
            print(f"  ... and {len(stats['missing_description'])-5} more")

    if stats['missing_status']:
        print(f"\n[WARNING] Missing status in {len(stats['missing_status'])} parameters:")
        for path in stats['missing_status'][:5]:
            print(f"  - {path}")
        if len(stats['missing_status']) > 5:
            print(f"  ... and {len(stats['missing_status'])-5} more")

    if stats['missing_source']:
        print(f"\n[WARNING] Missing source/derivation in {len(stats['missing_source'])} parameters:")
        for path in stats['missing_source'][:5]:
            print(f"  - {path}")
        if len(stats['missing_source']) > 5:
            print(f"  ... and {len(stats['missing_source'])-5} more")

    # Success criteria
    print("\n" + "="*70)
    completeness = (
        stats['has_units'] + stats['has_description'] +
        stats['has_status'] + stats['has_source']
    ) / (4 * total) * 100

    print(f"Overall Completeness: {completeness:.1f}%")

    if completeness >= 95:
        print("Status: [PASS] Metadata is sufficiently complete!")
    elif completeness >= 80:
        print("Status: [WARNING] Metadata is mostly complete but needs improvement")
    else:
        print("Status: [FAIL] Metadata needs significant work")

    print("="*70)

def main():
    filepath = Path(__file__).parent / 'theory_output.json'

    print(f"Loading {filepath}...")
    data = load_theory_output(str(filepath))

    params = data.get('parameters', {})

    print("Analyzing parameter metadata...")
    params_list = count_params_recursive(params)

    stats = check_metadata_completeness(params_list)

    print_report(stats)

if __name__ == '__main__':
    main()
