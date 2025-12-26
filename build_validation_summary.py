#!/usr/bin/env python3
"""
Build enhanced validation_summary from theory_output.json simulations
"""

import json
from pathlib import Path

# Load theory_output.json
with open('theory_output.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

old_validation_summary = data.get('validation_summary', [])
simulations = data.get('simulations', {})

print(f"Current validation entries: {len(old_validation_summary)}")
print(f"Available simulations: {len(simulations)}")

# Enhanced validation_summary
new_validation_summary = []

# Define extraction logic for each validation entry
def extract_validation_data(name, status, sim_key, sim_data):
    """Extract validation data from simulation"""

    entry = {
        "id": sim_key,
        "name": name,
        "status": status,
        "computed": None,
        "experimental": None,
        "bound_type": None,
        "sigma": None,
        "ratio": None,
        "units": None,
        "source": None,
        "notes": None
    }

    # If simulation has error, note it
    if 'error' in sim_data:
        entry['notes'] = f"Simulation error: {sim_data['error']}"
        return entry

    # If simulation has validation key (structured format)
    if 'validation' in sim_data:
        val = sim_data['validation']

        # Handle nested validation (like neutrino_masses)
        if isinstance(val, dict) and all(isinstance(v, dict) for v in val.values()):
            # Take the first sub-validation or aggregate
            if 'solar_splitting' in val:
                sub_val = val['solar_splitting']
                entry['computed'] = sub_val.get('computed')
                entry['experimental'] = sub_val.get('experimental')
                entry['sigma'] = sub_val.get('sigma')
                entry['units'] = sub_val.get('units')
                entry['notes'] = "Solar splitting validation (multiple validations available)"
            else:
                # Take first available
                first_key = list(val.keys())[0]
                sub_val = val[first_key]
                entry['computed'] = sub_val.get('computed')
                entry['experimental'] = sub_val.get('experimental')
                entry['sigma'] = sub_val.get('sigma')
                entry['units'] = sub_val.get('units')
                entry['notes'] = f"From {first_key} validation"
        else:
            # Simple validation format
            entry['computed'] = val.get('computed')
            entry['experimental'] = val.get('experimental')
            entry['bound_type'] = val.get('bound_type')
            entry['sigma'] = val.get('sigma')
            entry['ratio'] = val.get('ratio')
            entry['units'] = val.get('units')

    # Extract source information
    if 'formula' in sim_data:
        formula = sim_data['formula']
        if isinstance(formula, dict):
            entry['source'] = formula.get('id', 'formula')

    # Add mechanism/status notes if available
    if 'mechanism' in sim_data and not entry['notes']:
        entry['notes'] = f"Mechanism: {sim_data['mechanism']}"
    elif 'status' in sim_data and not entry['notes'] and sim_data['status'] not in ['PASS', 'FAIL', 'CHECK', 'ERROR']:
        entry['notes'] = sim_data['status']

    return entry

# Mapping from validation names to simulation keys
validation_sim_mapping = {
    "Proton Decay": "proton_decay",
    "Neutrino Masses": "neutrino_masses",
    "Higgs Mass": "higgs_mass",
    "KK Graviton": "kk_graviton",
    "DT Splitting": "doublet_triplet",
    "Breaking Chain": "breaking_chain",
    "Fermion Chirality": "fermion_chirality",
    "Pneuma Stability": "pneuma_stability",
    "Hebrew Physics": "hebrew_physics",
    "KK Spectrum (v14.2)": "kk_spectrum_v14_2",
    "Yukawa Textures": "yukawa_textures",
    "CP Phase": "cp_phase",
    "G2 Ricci-Flatness": "g2_metric_ricci",
    "Yukawa Overlaps": "yukawa_overlap",
    "Asymptotic Safety": "asymptotic_safety",
    "Moduli Racetrack (v15.0)": "moduli_racetrack_v15",
    "G2 Metric+Perturbation (v15.0)": "g2_metric_v15",
    "Yukawa 7D MC (v15.0)": "yukawa_overlap_v15",
    "Pneuma-Vielbein Bridge (v15.1)": "pneuma_bridge_v15_1",
    "Multi-Sector Sampling (v16.0)": "multi_sector_v16_0",
    "Microtubule-PM Coupling (v15.2)": "microtubule_v15_2",
    "Lattice Dispersion (v16.0)": "lattice_dispersion_v16_0",
    "Evolutionary Orchestration (v16.1)": "evolutionary_orchestration_v16_1",
    "Subleading Dispersion (v16.1)": "subleading_dispersion_v16_1",
    "PMNS Geometric (v14.1)": "pmns_geometric_v14_1",
    "Pneuma Potential (v14.1)": "pneuma_potential_v14_1",
    "G2 Landscape (v14.1)": "g2_landscape_v14_1",
    "Superpartner Bounds (v14.1)": "superpartner_bounds_v14_1",
    "LQG Timescale (v14.1)": "lqg_timescale_v14_1",
    "Mirror Dark Matter (v15.3)": "mirror_dm_v15_3",
    "Landscape Selection (v15.4)": "landscape_selection_v15_4",
    "Virasoro Anomaly (v12.8)": "virasoro_v12_8",
    "Sp(2,R) Gauge Fixing (v13.0)": "sp2r_validation_v13_0",
    "Orientation Sum (v12.8)": "orientation_sum_v12_8",
    "Zero Modes (v12.8)": "zero_modes_v12_8"
}

# Process each validation entry
for name, status in old_validation_summary:
    sim_key = validation_sim_mapping.get(name)
    if not sim_key:
        print(f"WARNING: No simulation key mapping for '{name}'")
        continue

    sim_data = simulations.get(sim_key, {})
    entry = extract_validation_data(name, status, sim_key, sim_data)
    new_validation_summary.append(entry)

# Display summary
print(f"\n{'='*60}")
print("Enhanced Validation Summary")
print('='*60)

status_counts = {}
for entry in new_validation_summary:
    status_counts[entry['status']] = status_counts.get(entry['status'], 0) + 1

print(f"\nStatus Distribution:")
for status, count in sorted(status_counts.items()):
    print(f"  {status}: {count}")

# Show examples
print(f"\n{'='*60}")
print("Example Entries")
print('='*60)

# Show one PASS with full data
for entry in new_validation_summary:
    if entry['status'] == 'PASS' and entry['computed'] is not None:
        print(f"\nPASS with data: {entry['name']}")
        print(json.dumps(entry, indent=2))
        break

# Show one ERROR
for entry in new_validation_summary:
    if entry['status'] == 'ERROR':
        print(f"\nERROR: {entry['name']}")
        print(json.dumps(entry, indent=2))
        break

# Show one CHECK
for entry in new_validation_summary:
    if entry['status'] == 'CHECK':
        print(f"\nCHECK: {entry['name']}")
        print(json.dumps(entry, indent=2))
        break

# Save enhanced validation summary
output_file = Path('validation_summary_enhanced.json')
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(new_validation_summary, f, indent=2, ensure_ascii=False)

print(f"\n{'='*60}")
print(f"Enhanced validation summary saved to: {output_file}")
print(f"Total entries: {len(new_validation_summary)}")
print('='*60)
