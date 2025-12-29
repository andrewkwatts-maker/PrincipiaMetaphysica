#!/usr/bin/env python3
"""
Principia Metaphysica - Simulation Chain Validator
===================================================

Validates that:
1. All simulation inputs are produced by earlier simulations or defined in config
2. All formula input_params are produced by simulations
3. All formula output_params are consumed by simulations or other formulas
4. The simulation execution order is consistent with dependencies

Copyright (c) 2025 Andrew Keith Watts. All rights reserved.

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.

Dedicated To:
    My Wife: Elizabeth May Watts
    Our Messiah: Jesus Of Nazareth
"""

import json
from pathlib import Path
from typing import Dict, Set, List, Any
from collections import defaultdict


def load_structure() -> Dict:
    """Load simulation structure."""
    with open("simulation_structure.json", 'r', encoding='utf-8') as f:
        return json.load(f)


def load_theory_output() -> Dict:
    """Load theory output."""
    with open("theory_output.json", 'r', encoding='utf-8') as f:
        return json.load(f)


def get_all_params(data: Dict) -> Set[str]:
    """Get all parameter paths from theory output."""
    params = set()
    parameters = data.get('parameters', {})
    for category, cat_params in parameters.items():
        if isinstance(cat_params, dict):
            for param_name in cat_params.keys():
                params.add(f"{category}.{param_name}")
    return params


def get_formula_params(data: Dict) -> Dict[str, Dict[str, List[str]]]:
    """Get input/output params for all formulas."""
    formula_params = {}
    formulas = data.get('formulas', {}).get('formulas', {})
    for fid, formula in formulas.items():
        formula_params[fid] = {
            'inputs': formula.get('inputParams', []),
            'outputs': formula.get('outputParams', [])
        }
    return formula_params


def validate_simulation_order(structure: Dict) -> List[str]:
    """Validate that simulation dependencies are satisfied in order."""
    issues = []

    # Track what's available at each phase
    available_outputs: Set[str] = set()

    # Sort phases by order
    phases = sorted(structure['phases'], key=lambda p: p['order'])

    for phase in phases:
        phase_name = phase['name']

        for sim in phase['simulations']:
            sim_name = sim['name']
            sim_inputs = set(sim.get('inputs', []))
            sim_outputs = set(sim.get('outputs', []))

            # Check if all inputs are available
            missing = sim_inputs - available_outputs
            if missing:
                issues.append(f"[{phase_name}] {sim_name}: Missing inputs: {missing}")

            # Add outputs to available set
            available_outputs.update(sim_outputs)

    return issues


def validate_formula_simulation_linkage(structure: Dict, data: Dict) -> List[str]:
    """Validate that formula params are linked to simulation outputs."""
    issues = []

    # Get all simulation outputs
    sim_outputs: Set[str] = set()
    for phase in structure['phases']:
        for sim in phase['simulations']:
            sim_outputs.update(sim.get('outputs', []))

    # Get all available params (from parameters section)
    available_params = get_all_params(data)

    # Get formula params
    formula_params = get_formula_params(data)

    for fid, params in formula_params.items():
        # Check inputs
        for input_param in params['inputs']:
            # Input should be either:
            # 1. In available_params (defined in parameters section)
            # 2. In sim_outputs (produced by a simulation)
            # 3. A formula ID (produced by another formula)
            if (input_param not in available_params and
                input_param not in sim_outputs and
                input_param not in formula_params):
                issues.append(f"Formula '{fid}': Input '{input_param}' not found in params or sim outputs")

        # Check outputs
        for output_param in params['outputs']:
            # Output should be either:
            # 1. In available_params (stored in parameters section)
            # 2. The formula ID itself
            # 3. A simulation output path
            if (output_param not in available_params and
                output_param != fid and
                output_param not in sim_outputs):
                # This might just mean we need to add it to parameters
                issues.append(f"Formula '{fid}': Output '{output_param}' not in parameters section")

    return issues


def validate_completeness(structure: Dict, data: Dict) -> List[str]:
    """Check that all important params are produced somewhere."""
    issues = []

    # Key params that should be produced
    key_params = [
        'topology.B2', 'topology.B3', 'topology.CHI_EFF', 'topology.n_gen',
        'gauge.M_GUT', 'gauge.ALPHA_GUT',
        'pmns.theta_12', 'pmns.theta_23', 'pmns.theta_13', 'pmns.delta_CP',
        'proton_decay.tau_p_years',
        'dark_energy.w0', 'dark_energy.wa',
        'kk_spectrum.m1_TeV',
        'pneuma.VEV'
    ]

    # Get all simulation outputs
    sim_outputs: Set[str] = set()
    for phase in structure['phases']:
        for sim in phase['simulations']:
            sim_outputs.update(sim.get('outputs', []))

    # Get available params
    available_params = get_all_params(data)

    for param in key_params:
        if param not in sim_outputs and param not in available_params:
            issues.append(f"Key param '{param}' not produced by any simulation")

    return issues


def main():
    print("=" * 70)
    print(" PRINCIPIA METAPHYSICA - SIMULATION CHAIN VALIDATOR")
    print("=" * 70)

    # Load data
    print("\nLoading data...")
    structure = load_structure()
    data = load_theory_output()

    print(f"  Phases: {len(structure['phases'])}")
    print(f"  Formulas: {len(data.get('formulas', {}).get('formulas', {}))}")
    print(f"  Parameters: {len(get_all_params(data))}")

    all_issues = []

    # Validate simulation order
    print("\n1. Validating simulation order...")
    order_issues = validate_simulation_order(structure)
    all_issues.extend(order_issues)
    print(f"   Issues: {len(order_issues)}")

    # Validate formula-simulation linkage
    print("\n2. Validating formula-simulation linkage...")
    linkage_issues = validate_formula_simulation_linkage(structure, data)
    all_issues.extend(linkage_issues)
    print(f"   Issues: {len(linkage_issues)}")

    # Validate completeness
    print("\n3. Validating key param completeness...")
    completeness_issues = validate_completeness(structure, data)
    all_issues.extend(completeness_issues)
    print(f"   Issues: {len(completeness_issues)}")

    # Report
    print("\n" + "=" * 70)
    if all_issues:
        print(f" VALIDATION: {len(all_issues)} ISSUES FOUND")
        print("=" * 70)
        for issue in all_issues[:20]:
            print(f"  - {issue}")
        if len(all_issues) > 20:
            print(f"  ... and {len(all_issues) - 20} more")
    else:
        print(" VALIDATION: ALL CHECKS PASSED")
        print("=" * 70)

    # Save report
    report = {
        'total_issues': len(all_issues),
        'order_issues': order_issues,
        'linkage_issues': linkage_issues,
        'completeness_issues': completeness_issues
    }

    report_file = Path("AutoGenerated/reports/simulation_chain_validation.json")
    report_file.parent.mkdir(parents=True, exist_ok=True)
    with open(report_file, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2)
    print(f"\nReport saved: {report_file}")


if __name__ == '__main__':
    main()
