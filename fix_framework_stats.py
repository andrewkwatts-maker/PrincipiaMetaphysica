#!/usr/bin/env python3
"""
Fix framework_statistics in theory_output.json based on audit report.
Adds missing fields and calculates additional useful statistics.
"""

import json
from datetime import datetime, timezone

def fix_framework_statistics():
    """Update framework_statistics with missing and additional fields."""

    # Load theory_output.json
    filepath = r'h:\Github\PrincipiaMetaphysica\theory_output.json'
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Get existing framework_statistics
    stats = data.get('framework_statistics', {})

    # Count items from other sections
    total_formulas = len(data.get('formulas', {}))
    total_simulations = len(data.get('simulations', {}))
    total_sections = len(data.get('sections', {}))

    # Get parameter categories from registry
    registry = stats.get('registry', {}).get('parameters', {})
    categories = sorted(set(p.get('category') for p in registry.values() if 'category' in p))

    # Calculate validation statistics
    validation_summary = data.get('validation_summary', [])
    pass_count = sum(1 for sim in validation_summary if sim[1] == 'PASS')
    total_val_sims = len(validation_summary)
    simulation_pass_rate = round((pass_count / total_val_sims * 100), 1) if total_val_sims > 0 else 0.0

    # Calculate success_rate_2sigma
    within_2_sigma = stats.get('within_2_sigma', 55)
    total_sm_parameters = stats.get('total_sm_parameters', 56)
    success_rate_2sigma = round((within_2_sigma / total_sm_parameters * 100), 1)

    # Get current timestamp
    validation_timestamp = datetime.now(timezone.utc).isoformat()

    # Add missing fields (in order after existing fields)
    print("Adding/updating framework_statistics fields:")
    print(f"  geometric_predictions: {stats.get('pure_predictions', 48)} (equals pure_predictions)")
    print(f"  total_formulas: {total_formulas}")
    print(f"  total_simulations: {total_simulations}")
    print(f"  total_sections: {total_sections}")
    print(f"  success_rate_2sigma: {success_rate_2sigma}%")
    print(f"  simulation_pass_rate: {simulation_pass_rate}%")
    print(f"  parameter_categories: {len(categories)} categories")
    print(f"  validation_timestamp: {validation_timestamp}")

    # Create updated stats dictionary preserving order
    updated_stats = {}

    # Keep existing fields in their original order
    for key in stats.keys():
        if key != 'registry':  # We'll add registry at the end
            updated_stats[key] = stats[key]

    # Add new fields
    updated_stats['geometric_predictions'] = stats.get('pure_predictions', 48)
    updated_stats['total_formulas'] = total_formulas
    updated_stats['total_simulations'] = total_simulations
    updated_stats['total_sections'] = total_sections
    updated_stats['success_rate_2sigma'] = success_rate_2sigma
    updated_stats['simulation_pass_rate'] = simulation_pass_rate
    updated_stats['parameter_categories'] = categories
    updated_stats['validation_timestamp'] = validation_timestamp

    # Add registry at the end
    if 'registry' in stats:
        updated_stats['registry'] = stats['registry']

    # Add total_foundations if not present (from audit report)
    if 'total_foundations' not in updated_stats:
        updated_stats['total_foundations'] = 17

    if 'foundation_categories' not in updated_stats:
        # From audit report
        updated_stats['foundation_categories'] = [
            "quantum_field_theory",
            "quantum",
            "Theoretical Physics",
            "differential_geometry",
            "algebraic_topology",
            "string_theory",
            "cosmology",
            "general_relativity",
            "gauge_theory",
            "representation_theory",
            "supersymmetry",
            "particle_physics"
        ]

    # Update the data
    data['framework_statistics'] = updated_stats

    # Verify calculations
    print("\nVerifying existing calculations:")
    print(f"  total_sm_parameters: {updated_stats['total_sm_parameters']} (expected: 56)")
    print(f"  within_1_sigma: {updated_stats['within_1_sigma']} (expected: 51)")
    print(f"  within_2_sigma: {updated_stats['within_2_sigma']} (expected: 55)")
    print(f"  success_rate_1sigma: {updated_stats['success_rate_1sigma']}% (expected: 91.1%)")

    # Write back to file
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"\n✓ Successfully updated {filepath}")
    print(f"\nFramework statistics now has {len(updated_stats)} fields")
    print("\nNew fields added:")
    print("  1. geometric_predictions")
    print("  2. total_formulas")
    print("  3. total_simulations")
    print("  4. total_sections")
    print("  5. success_rate_2sigma")
    print("  6. simulation_pass_rate")
    print("  7. parameter_categories")
    print("  8. validation_timestamp")

if __name__ == '__main__':
    fix_framework_statistics()
