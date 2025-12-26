#!/usr/bin/env python3
"""Check which formulas still need simulation_file"""
import re

NEEDED = {
    'KAPPA_GUT_COEFFICIENT': 'simulations/gauge_unification_precision_v12_4.py',
    'PLANCK_MASS_DERIVATION': 'simulations/gauge_unification_precision_v12_4.py',
    'DOUBLET_TRIPLET': 'simulations/doublet_triplet_splitting_v14_0.py',
    'HIGGS_MASS': 'simulations/higgs_mass_v12_4_moduli_stabilization.py',
    'HIGGS_POTENTIAL': 'simulations/pneuma_full_potential_v14_1.py',
    'HIGGS_QUARTIC': 'simulations/higgs_yukawa_rg_v12_4.py',
    'BOTTOM_QUARK_MASS': 'simulations/higgs_yukawa_rg_v12_4.py',
    'TAU_LEPTON_MASS': 'simulations/higgs_yukawa_rg_v12_4.py',
    'GW_DISPERSION_COEFF': 'simulations/gw_dispersion_v12_8.py',
    'GW_DISPERSION_ALT': 'simulations/gw_dispersion_v12_8.py',
    'EFFECTIVE_TORSION_SPINOR': 'simulations/torsion_spinor_fraction_v12_8.py',
    'GHOST_COEFFICIENT': 'simulations/virasoro_anomaly_v12_8.py',
    'MIRROR_TEMP_RATIO': 'simulations/mirror_dark_matter_abundance_v15_3.py',
    'PATI_SALAM_CHAIN': 'simulations/breaking_chain_geometric_v14_1.py',
}

with open('config.py', 'r', encoding='utf-8') as f:
    content = f.read()

print("Checking formulas that need simulation_file...\n")
still_needed = []

for formula_name, sim_file in NEEDED.items():
    pattern = rf'{formula_name}\s*=\s*Formula\('
    match = re.search(pattern, content)
    if match:
        start = match.start()
        pos = match.end()
        depth = 1
        while pos < len(content) and depth > 0:
            if content[pos] == '(':
                depth += 1
            elif content[pos] == ')':
                depth -= 1
            pos += 1

        formula_block = content[start:pos]
        has_sim_file = 'simulation_file=' in formula_block
        if not has_sim_file:
            still_needed.append(formula_name)
            print(f"  {formula_name}: NEEDS {sim_file}")
        else:
            print(f"  {formula_name}: ✓ HAS simulation_file")
    else:
        print(f"  {formula_name}: NOT FOUND")

print(f"\nSummary: {len(still_needed)} formulas still need simulation_file")
print(f"Total simulation_file count: {len(re.findall(r'simulation_file=', content))}")
