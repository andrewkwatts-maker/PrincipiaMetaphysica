#!/usr/bin/env python3
"""
Validation script for theory_output.json
Checks parameters and formulas for completeness and correctness
"""

import json
import math
from pathlib import Path
from collections import defaultdict

def is_valid_value(value):
    """Check if a value is valid (not None, NaN, or Inf)"""
    if value is None:
        return False
    if isinstance(value, (int, float)):
        return not (math.isnan(value) or math.isinf(value))
    return True

def validate_parameters(params):
    """Validate all parameters in the theory output"""
    results = {
        'total': 0,
        'with_validation': 0,
        'missing_validation': [],
        'missing_source': [],
        'missing_status': [],
        'invalid_value': [],
        'missing_units': [],
        'derived_without_validation': [],
        'validation_status_issues': [],
        'by_source': defaultdict(list),
        'by_status': defaultdict(int)
    }

    for param_id, param in params.items():
        results['total'] += 1

        # Check value
        value = param.get('value')
        if not is_valid_value(value):
            results['invalid_value'].append(param_id)

        # Check source
        source = param.get('source', '').strip()
        if not source:
            results['missing_source'].append(param_id)
        else:
            results['by_source'][source].append(param_id)

        # Check status
        status = param.get('status', '').strip()
        if not status:
            results['missing_status'].append(param_id)
        else:
            results['by_status'][status] += 1

        # Check units for dimensional quantities
        units = param.get('units', '').strip()
        # Don't require units for dimensionless quantities
        param_name = param.get('name', param_id).lower()
        dimensionless_indicators = ['alpha', 'ratio', 'mixing', 'angle', 'sin', 'cos', 'tan']
        is_dimensionless = any(ind in param_name for ind in dimensionless_indicators)

        if not units and not is_dimensionless and value not in [0, 1]:
            results['missing_units'].append(param_id)

        # Check validation data
        validation = param.get('validation')
        experimental = param.get('experimentalBounds')

        has_validation = validation is not None or experimental is not None

        if has_validation:
            results['with_validation'] += 1
        else:
            results['missing_validation'].append(param_id)

            # Track DERIVED parameters without validation
            if status == 'DERIVED':
                results['derived_without_validation'].append(param_id)

        # Check validation status for parameters with experimental bounds
        if experimental:
            validation_status = param.get('validationStatus', '').strip()
            if not validation_status:
                results['validation_status_issues'].append({
                    'id': param_id,
                    'issue': 'Has experimental bounds but no validationStatus'
                })
            elif validation_status not in ['PASS', 'FAIL', 'MARGINAL']:
                results['validation_status_issues'].append({
                    'id': param_id,
                    'issue': f'Invalid validationStatus: {validation_status}'
                })

    return results

def validate_formulas(formulas):
    """Validate all formulas in the theory output"""
    results = {
        'total': 0,
        'with_derivation': 0,
        'missing_derivation': [],
        'missing_id': [],
        'duplicate_ids': [],
        'missing_latex': [],
        'invalid_latex': [],
        'missing_category': [],
        'missing_input_params': [],
        'missing_output_params': [],
        'empty_input_params': [],
        'empty_output_params': [],
        'by_category': defaultdict(int),
        'seen_ids': set()
    }

    # Handle both dict and list formats
    if isinstance(formulas, dict):
        formula_items = formulas.items()
    else:
        formula_items = [(f.get('id', f'formula_{i}'), f) for i, f in enumerate(formulas)]

    for formula_id_key, formula in formula_items:
        results['total'] += 1

        # Check if formula is a dict
        if not isinstance(formula, dict):
            results['invalid_latex'].append({
                'id': formula_id_key,
                'latex': f'Formula is not a dict: {type(formula)}'
            })
            continue

        # Check id - use the key if formula doesn't have an id field
        formula_id = formula.get('id', formula_id_key)
        if isinstance(formula_id, str):
            formula_id = formula_id.strip()
        else:
            formula_id = str(formula_id)

        if not formula_id:
            results['missing_id'].append(f"Formula #{results['total']}")
        else:
            if formula_id in results['seen_ids']:
                results['duplicate_ids'].append(formula_id)
            results['seen_ids'].add(formula_id)

        # Check latex
        latex = formula.get('latex', '').strip()
        if not latex:
            results['missing_latex'].append(formula_id or f"Formula #{results['total']}")
        elif '\\' not in latex:
            # Basic check for LaTeX commands
            results['invalid_latex'].append({
                'id': formula_id,
                'latex': latex[:50] + '...' if len(latex) > 50 else latex
            })

        # Check category
        category = formula.get('category', '').strip()
        if not category:
            results['missing_category'].append(formula_id)
        else:
            results['by_category'][category] += 1

        # Check input/output params
        input_params = formula.get('inputParams')
        output_params = formula.get('outputParams')

        if input_params is None:
            results['missing_input_params'].append(formula_id)
        elif isinstance(input_params, list) and len(input_params) == 0:
            results['empty_input_params'].append(formula_id)

        if output_params is None:
            results['missing_output_params'].append(formula_id)
        elif isinstance(output_params, list) and len(output_params) == 0:
            results['empty_output_params'].append(formula_id)

        # Check derivation
        derivation = formula.get('derivation')
        if derivation and derivation.get('steps'):
            results['with_derivation'] += 1
        else:
            results['missing_derivation'].append(formula_id)

    return results

def identify_responsible_simulations(param_results, params):
    """Identify which simulations are responsible for missing validation"""
    simulations_needed = defaultdict(list)

    for param_id in param_results['missing_validation']:
        param = params.get(param_id, {})
        source = param.get('source', 'UNKNOWN')
        status = param.get('status', 'UNKNOWN')

        # Only track if it's a derived parameter that should have validation
        if status == 'DERIVED':
            simulations_needed[source].append(param_id)

    return simulations_needed

def generate_markdown_report(param_results, formula_results, simulations_needed, params, formulas):
    """Generate a markdown validation report"""

    report = []
    report.append("# Theory Output Validation Report")
    report.append("")
    report.append(f"**Generated:** 2025-12-28")
    report.append(f"**Source File:** AutoGenerated/theory_output.json")
    report.append("")

    # Executive Summary
    report.append("## Executive Summary")
    report.append("")
    report.append(f"- **Total Parameters:** {param_results['total']}")
    report.append(f"- **Parameters with Validation:** {param_results['with_validation']} ({100*param_results['with_validation']/param_results['total']:.1f}%)")
    report.append(f"- **Parameters Missing Validation:** {len(param_results['missing_validation'])} ({100*len(param_results['missing_validation'])/param_results['total']:.1f}%)")
    report.append("")
    report.append(f"- **Total Formulas:** {formula_results['total']}")
    report.append(f"- **Formulas with Derivation:** {formula_results['with_derivation']} ({100*formula_results['with_derivation']/formula_results['total']:.1f}%)")
    report.append(f"- **Formulas Missing Derivation:** {len(formula_results['missing_derivation'])} ({100*len(formula_results['missing_derivation'])/formula_results['total']:.1f}%)")
    report.append("")

    # Parameters Section
    report.append("## Parameter Validation")
    report.append("")

    # Status breakdown
    report.append("### Parameters by Status")
    report.append("")
    for status, count in sorted(param_results['by_status'].items()):
        report.append(f"- **{status}:** {count}")
    report.append("")

    # Invalid values
    if param_results['invalid_value']:
        report.append("### Parameters with Invalid Values")
        report.append("")
        report.append(f"**Count:** {len(param_results['invalid_value'])}")
        report.append("")
        for param_id in param_results['invalid_value']:
            param = params.get(param_id, {})
            report.append(f"- `{param_id}`: {param.get('name', 'N/A')} = {param.get('value')}")
        report.append("")

    # Missing source
    if param_results['missing_source']:
        report.append("### Parameters Missing Source")
        report.append("")
        report.append(f"**Count:** {len(param_results['missing_source'])}")
        report.append("")
        for param_id in param_results['missing_source']:
            report.append(f"- `{param_id}`")
        report.append("")

    # Missing status
    if param_results['missing_status']:
        report.append("### Parameters Missing Status")
        report.append("")
        report.append(f"**Count:** {len(param_results['missing_status'])}")
        report.append("")
        for param_id in param_results['missing_status']:
            report.append(f"- `{param_id}`")
        report.append("")

    # Missing units
    if param_results['missing_units']:
        report.append("### Parameters Missing Units")
        report.append("")
        report.append(f"**Count:** {len(param_results['missing_units'])}")
        report.append("")
        report.append("These dimensional parameters should have units specified:")
        report.append("")
        for param_id in param_results['missing_units']:
            param = params.get(param_id, {})
            report.append(f"- `{param_id}`: {param.get('name', 'N/A')}")
        report.append("")

    # Derived parameters without validation
    if param_results['derived_without_validation']:
        report.append("### Derived Parameters Without Validation")
        report.append("")
        report.append(f"**Count:** {len(param_results['derived_without_validation'])}")
        report.append("")
        report.append("These DERIVED parameters should have experimental validation data:")
        report.append("")
        for param_id in param_results['derived_without_validation']:
            param = params.get(param_id, {})
            report.append(f"- `{param_id}`: {param.get('name', 'N/A')} = {param.get('value')}")
        report.append("")

    # Validation status issues
    if param_results['validation_status_issues']:
        report.append("### Validation Status Issues")
        report.append("")
        report.append(f"**Count:** {len(param_results['validation_status_issues'])}")
        report.append("")
        for issue in param_results['validation_status_issues']:
            report.append(f"- `{issue['id']}`: {issue['issue']}")
        report.append("")

    # All parameters missing validation
    report.append("### All Parameters Missing Validation")
    report.append("")
    report.append(f"**Count:** {len(param_results['missing_validation'])}")
    report.append("")
    if len(param_results['missing_validation']) <= 50:
        for param_id in param_results['missing_validation']:
            param = params.get(param_id, {})
            status = param.get('status', 'UNKNOWN')
            source = param.get('source', 'UNKNOWN')
            report.append(f"- `{param_id}` ({status}, {source}): {param.get('name', 'N/A')}")
    else:
        report.append(f"*Too many to list ({len(param_results['missing_validation'])} parameters)*")
        report.append("")
        report.append("See 'Simulations Needed' section below for breakdown by source.")
    report.append("")

    # Simulations needed
    if simulations_needed:
        report.append("## Simulations Responsible for Missing Validation")
        report.append("")
        report.append("The following simulations need to provide validation data:")
        report.append("")
        for source, param_ids in sorted(simulations_needed.items()):
            report.append(f"### {source}")
            report.append("")
            report.append(f"**Parameters needing validation:** {len(param_ids)}")
            report.append("")
            for param_id in param_ids:
                param = params.get(param_id, {})
                report.append(f"- `{param_id}`: {param.get('name', 'N/A')}")
            report.append("")

    # Formulas Section
    report.append("## Formula Validation")
    report.append("")

    # Category breakdown
    report.append("### Formulas by Category")
    report.append("")
    for category, count in sorted(formula_results['by_category'].items()):
        report.append(f"- **{category}:** {count}")
    report.append("")

    # Missing derivations
    if formula_results['missing_derivation']:
        report.append("### Formulas Missing Derivation")
        report.append("")
        report.append(f"**Count:** {len(formula_results['missing_derivation'])}")
        report.append("")

        # Get formula details
        if isinstance(formulas, dict):
            formula_list = formulas
        else:
            formula_list = {f.get('id', f'formula_{i}'): f for i, f in enumerate(formulas)}

        for formula_id in formula_results['missing_derivation']:
            formula = formula_list.get(formula_id, {})
            category = formula.get('category', 'UNKNOWN') if isinstance(formula, dict) else 'UNKNOWN'
            report.append(f"- `{formula_id}` ({category})")
        report.append("")

    # Missing IDs
    if formula_results['missing_id']:
        report.append("### Formulas Missing ID")
        report.append("")
        report.append(f"**Count:** {len(formula_results['missing_id'])}")
        report.append("")
        for item in formula_results['missing_id']:
            report.append(f"- {item}")
        report.append("")

    # Duplicate IDs
    if formula_results['duplicate_ids']:
        report.append("### Formulas with Duplicate IDs")
        report.append("")
        report.append(f"**Count:** {len(formula_results['duplicate_ids'])}")
        report.append("")
        for formula_id in formula_results['duplicate_ids']:
            report.append(f"- `{formula_id}`")
        report.append("")

    # Missing LaTeX
    if formula_results['missing_latex']:
        report.append("### Formulas Missing LaTeX")
        report.append("")
        report.append(f"**Count:** {len(formula_results['missing_latex'])}")
        report.append("")
        for formula_id in formula_results['missing_latex']:
            report.append(f"- `{formula_id}`")
        report.append("")

    # Invalid LaTeX
    if formula_results['invalid_latex']:
        report.append("### Formulas with Invalid LaTeX")
        report.append("")
        report.append(f"**Count:** {len(formula_results['invalid_latex'])}")
        report.append("")
        for item in formula_results['invalid_latex']:
            report.append(f"- `{item['id']}`: `{item['latex']}`")
        report.append("")

    # Missing category
    if formula_results['missing_category']:
        report.append("### Formulas Missing Category")
        report.append("")
        report.append(f"**Count:** {len(formula_results['missing_category'])}")
        report.append("")
        for formula_id in formula_results['missing_category']:
            report.append(f"- `{formula_id}`")
        report.append("")

    # Missing input/output params
    if formula_results['missing_input_params']:
        report.append("### Formulas Missing inputParams")
        report.append("")
        report.append(f"**Count:** {len(formula_results['missing_input_params'])}")
        report.append("")
        for formula_id in formula_results['missing_input_params']:
            report.append(f"- `{formula_id}`")
        report.append("")

    if formula_results['empty_input_params']:
        report.append("### Formulas with Empty inputParams")
        report.append("")
        report.append(f"**Count:** {len(formula_results['empty_input_params'])}")
        report.append("")
        for formula_id in formula_results['empty_input_params']:
            report.append(f"- `{formula_id}`")
        report.append("")

    if formula_results['missing_output_params']:
        report.append("### Formulas Missing outputParams")
        report.append("")
        report.append(f"**Count:** {len(formula_results['missing_output_params'])}")
        report.append("")
        for formula_id in formula_results['missing_output_params']:
            report.append(f"- `{formula_id}`")
        report.append("")

    if formula_results['empty_output_params']:
        report.append("### Formulas with Empty outputParams")
        report.append("")
        report.append(f"**Count:** {len(formula_results['empty_output_params'])}")
        report.append("")
        for formula_id in formula_results['empty_output_params']:
            report.append(f"- `{formula_id}`")
        report.append("")

    # Recommendations
    report.append("## Recommendations")
    report.append("")

    recommendations = []

    if param_results['invalid_value']:
        recommendations.append("1. **Fix Invalid Parameter Values:** Update parameters with null, NaN, or Inf values")

    if param_results['derived_without_validation']:
        recommendations.append(f"{len(recommendations)+1}. **Add Validation for Derived Parameters:** Run simulations to generate experimental validation data")

    if param_results['validation_status_issues']:
        recommendations.append(f"{len(recommendations)+1}. **Update Validation Status:** Set validationStatus (PASS/FAIL/MARGINAL) for parameters with experimental bounds")

    if formula_results['missing_derivation']:
        recommendations.append(f"{len(recommendations)+1}. **Add Formula Derivations:** Document derivation steps for theoretical formulas")

    if formula_results['empty_input_params'] or formula_results['empty_output_params']:
        recommendations.append(f"{len(recommendations)+1}. **Link Formula Parameters:** Connect formulas to their input and output parameters")

    if param_results['missing_units']:
        recommendations.append(f"{len(recommendations)+1}. **Add Units:** Specify units for dimensional parameters")

    if not recommendations:
        recommendations.append("No critical issues found. All validations passed!")

    for rec in recommendations:
        report.append(rec)

    report.append("")
    report.append("---")
    report.append("")
    report.append("*End of Report*")

    return "\n".join(report)

def main():
    """Main validation function"""

    # Load theory output
    theory_file = Path(r"h:/Github/PrincipiaMetaphysica/AutoGenerated/theory_output.json")

    print(f"Loading {theory_file}...")
    with open(theory_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    params = data.get('parameters', {})
    formulas = data.get('formulas', [])

    print(f"Found {len(params)} parameters and {len(formulas)} formulas")

    # Validate parameters
    print("\nValidating parameters...")
    param_results = validate_parameters(params)

    # Validate formulas
    print("Validating formulas...")
    formula_results = validate_formulas(formulas)

    # Identify simulations needed
    print("Identifying simulations responsible for missing validation...")
    simulations_needed = identify_responsible_simulations(param_results, params)

    # Generate report
    print("Generating report...")
    report = generate_markdown_report(param_results, formula_results, simulations_needed, params, formulas)

    # Save report
    report_file = Path(r"h:/Github/PrincipiaMetaphysica/reports/THEORY_OUTPUT_VALIDATION_REPORT.md")
    report_file.parent.mkdir(parents=True, exist_ok=True)

    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(report)

    print(f"\nReport saved to: {report_file}")

    # Print summary
    print("\n" + "="*60)
    print("VALIDATION SUMMARY")
    print("="*60)
    print(f"\nPARAMETERS:")
    print(f"  Total: {param_results['total']}")
    print(f"  With validation: {param_results['with_validation']} ({100*param_results['with_validation']/param_results['total']:.1f}%)")
    print(f"  Missing validation: {len(param_results['missing_validation'])}")
    print(f"  Invalid values: {len(param_results['invalid_value'])}")
    print(f"  Missing source: {len(param_results['missing_source'])}")
    print(f"  Missing status: {len(param_results['missing_status'])}")
    print(f"  Missing units: {len(param_results['missing_units'])}")
    print(f"  Validation status issues: {len(param_results['validation_status_issues'])}")

    print(f"\nFORMULAS:")
    print(f"  Total: {formula_results['total']}")
    print(f"  With derivation: {formula_results['with_derivation']} ({100*formula_results['with_derivation']/formula_results['total']:.1f}%)")
    print(f"  Missing derivation: {len(formula_results['missing_derivation'])}")
    print(f"  Missing/duplicate IDs: {len(formula_results['missing_id']) + len(formula_results['duplicate_ids'])}")
    print(f"  Missing LaTeX: {len(formula_results['missing_latex'])}")
    print(f"  Missing input/output params: {len(formula_results['missing_input_params']) + len(formula_results['missing_output_params'])}")
    print(f"  Empty input/output params: {len(formula_results['empty_input_params']) + len(formula_results['empty_output_params'])}")

    print(f"\nSIMULATIONS NEEDED:")
    for source, param_ids in sorted(simulations_needed.items()):
        print(f"  {source}: {len(param_ids)} parameters")

    print("\n" + "="*60)

if __name__ == "__main__":
    main()
