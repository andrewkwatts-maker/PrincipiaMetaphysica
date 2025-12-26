#!/usr/bin/env python3
"""
Principia Metaphysica - Auto-Fix Validation Issues
====================================================

Automatically fixes issues identified in auto_fixable.json:
1. Add missing OOM (order of magnitude) to parameters
2. Add missing bi-directional related formula links
3. Add missing units where derivable
4. Add missing section references

Copyright (c) 2025 Andrew Keith Watts. All rights reserved.
"""

import json
import math
import re
from pathlib import Path
from typing import Dict, Any, List

REPORTS_DIR = Path("AUTO_GENERATED/reports")
THEORY_FILE = "theory_output.json"


def load_fixable_issues() -> List[Dict]:
    """Load auto-fixable issues from report."""
    fix_file = REPORTS_DIR / "auto_fixable.json"
    if not fix_file.exists():
        print("No auto_fixable.json found - run validate_theory_output.py first")
        return []

    with open(fix_file, 'r', encoding='utf-8') as f:
        return json.load(f)


def load_theory_data() -> Dict:
    """Load theory_output.json."""
    with open(THEORY_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_theory_data(data: Dict):
    """Save theory_output.json."""
    with open(THEORY_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)

    # Also save to AUTO_GENERATED
    auto_gen_file = Path("AUTO_GENERATED") / "theory_output.json"
    with open(auto_gen_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)


def fix_missing_oom(data: Dict) -> int:
    """Add OOM to parameters missing it."""
    fixes = 0
    params = data.get('parameters', {})

    for category, cat_params in params.items():
        if not isinstance(cat_params, dict):
            continue
        for pid, param in cat_params.items():
            if not isinstance(param, dict):
                continue
            if 'oom' not in param or param['oom'] is None:
                value = param.get('value', 0)
                if isinstance(value, (int, float)) and value != 0:
                    try:
                        oom = int(math.floor(math.log10(abs(value))))
                        param['oom'] = oom
                        fixes += 1
                    except (ValueError, OverflowError):
                        pass

    return fixes


def fix_bi_directional_formulas(data: Dict) -> int:
    """Ensure related formulas point back to each other."""
    formulas = data.get('formulas', {}).get('formulas', {})
    fixes = 0

    for fid, formula in formulas.items():
        related = formula.get('relatedFormulas', [])
        for related_id in related:
            if related_id in formulas:
                related_formula = formulas[related_id]
                related_refs = related_formula.get('relatedFormulas', [])
                if fid not in related_refs:
                    if 'relatedFormulas' not in related_formula:
                        related_formula['relatedFormulas'] = []
                    related_formula['relatedFormulas'].append(fid)
                    fixes += 1

    return fixes


def fix_missing_simulation_files(data: Dict) -> int:
    """Try to auto-assign simulation files based on formula category."""
    formulas = data.get('formulas', {}).get('formulas', {})
    fixes = 0

    # Map of formula IDs to likely simulation files
    SIMULATION_MAP = {
        'generation-number': 'simulations/fermion_chirality_generations_v13_0.py',
        'virasoro-anomaly': 'simulations/virasoro_anomaly_v12_8.py',
        'sp2r-constraints': 'simulations/sp2r_gauge_fixing_validation_v13_0.py',
        'tcs-topology': 'simulations/g2_spinor_geometry_validation_v13_0.py',
        'master-action-26d': 'simulations/sp2r_gauge_fixing_validation_v13_0.py',
    }

    for fid, formula in formulas.items():
        if not formula.get('simulationFile'):
            if fid in SIMULATION_MAP:
                formula['simulationFile'] = SIMULATION_MAP[fid]
                fixes += 1

    return fixes


def fix_missing_units(data: Dict) -> int:
    """Add units based on formula category/type."""
    formulas = data.get('formulas', {}).get('formulas', {})
    fixes = 0

    # Map of formula ID patterns to units
    UNIT_PATTERNS = {
        'mass': 'GeV',
        'scale': 'GeV',
        'energy': 'GeV',
        'lifetime': 'years',
        'angle': 'degrees',
        'coupling': 'dimensionless',
        'ratio': 'dimensionless',
        'count': 'dimensionless',
        'generation': 'dimensionless',
        'euler': 'dimensionless',
        'betti': 'dimensionless',
    }

    for fid, formula in formulas.items():
        if not formula.get('units'):
            for pattern, unit in UNIT_PATTERNS.items():
                if pattern in fid.lower():
                    formula['units'] = unit
                    fixes += 1
                    break

    return fixes


def main():
    print("=" * 70)
    print("PRINCIPIA METAPHYSICA - AUTO-FIX ISSUES")
    print("=" * 70)

    # Load data
    print("\nLoading theory_output.json...")
    data = load_theory_data()

    total_fixes = 0

    # Fix OOM
    print("\n1. Fixing missing OOM values...")
    oom_fixes = fix_missing_oom(data)
    print(f"   Fixed: {oom_fixes} parameters")
    total_fixes += oom_fixes

    # Fix bi-directional
    print("\n2. Fixing bi-directional formula links...")
    bi_fixes = fix_bi_directional_formulas(data)
    print(f"   Fixed: {bi_fixes} links")
    total_fixes += bi_fixes

    # Fix simulation files
    print("\n3. Fixing missing simulation files...")
    sim_fixes = fix_missing_simulation_files(data)
    print(f"   Fixed: {sim_fixes} formulas")
    total_fixes += sim_fixes

    # Fix units
    print("\n4. Fixing missing units...")
    unit_fixes = fix_missing_units(data)
    print(f"   Fixed: {unit_fixes} formulas")
    total_fixes += unit_fixes

    # Save
    if total_fixes > 0:
        print(f"\nSaving {total_fixes} total fixes...")
        save_theory_data(data)
        print("   Saved to theory_output.json and AUTO_GENERATED/")
    else:
        print("\nNo fixes needed!")

    print("\n" + "=" * 70)
    print(f"TOTAL FIXES: {total_fixes}")
    print("=" * 70)

    # Suggest re-running validation
    if total_fixes > 0:
        print("\nRun validation again to verify:")
        print("  python validate_theory_output.py")


if __name__ == '__main__':
    main()
