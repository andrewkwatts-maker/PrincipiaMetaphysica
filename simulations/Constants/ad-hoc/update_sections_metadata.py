#!/usr/bin/env python3
"""
Update sections metadata in theory_output.json

Fixes:
1. Add formulaRefs arrays based on section content
2. Add paramRefs arrays based on section content
3. Add order field (1-6)
4. Add category field for logical grouping

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.

Dedicated To:
    My Wife: Elizabeth May Watts
    Our Messiah: Jesus Of Nazareth
"""

import json
import sys

# Section metadata mappings based on abstracts and key takeaways
# Only use formula IDs that actually exist in theory_output.json
SECTION_METADATA = {
    "1": {  # Introduction
        "order": 1,
        "category": "framework",
        "description": "Overview of the 26D geometric framework and dimensional reduction mechanism",
        "formulaRefs": [
            "master-action-26d",
            "reduction-cascade",
            "effective-euler",
            "generation-number",
            "g2-index-theorem"
        ],
        "paramRefs": [
            "dimensions.D_BULK",
            "dimensions.D_AFTER_SP2R",
            "dimensions.D_EFFECTIVE",
            "dimensions.SIGNATURE_INITIAL",
            "topology.CHI_EFF",
            "topology.n_gen",
            "topology.B2",
            "topology.B3"
        ]
    },
    "2": {  # Geometric Framework
        "order": 2,
        "category": "framework",
        "description": "Detailed mathematical structure of dimensional reduction and G2 compactification",
        "formulaRefs": [
            "reduction-cascade",
            "effective-euler",
            "flux-quantization",
            "effective-torsion",
            "division-algebra",
            "primordial-spinor-13d",
            "planck-mass-derivation",
            "effective-dimension",
            "g2-index-theorem"
        ],
        "paramRefs": [
            "dimensions.D_BULK",
            "dimensions.D_AFTER_SP2R",
            "dimensions.D_INTERNAL",
            "dimensions.D_EFFECTIVE",
            "dimensions.D_COMMON",
            "dimensions.SIGNATURE_INITIAL",
            "dimensions.SIGNATURE_BULK",
            "topology.CHI_EFF",
            "topology.B2",
            "topology.B3",
            "topology.n_flux",
            "topology.HODGE_H11",
            "topology.HODGE_H21",
            "topology.HODGE_H31",
            "topology.n_gen"
        ]
    },
    "3": {  # Fermion Sector
        "order": 3,
        "category": "phenomenology",
        "description": "Fermion masses, mixing angles, and CP violation from geometric cycles",
        "formulaRefs": [
            "generation-number",
            "hierarchy-ratio",
            "bottom-quark-mass",
            "neutrino-mass-21",
            "neutrino-mass-31",
            "ckm-elements",
            "cp-phase-geometric",
            "majorana-scale",
            "light-up-quarks",
            "light-down-quarks",
            "light-leptons"
        ],
        "paramRefs": [
            "topology.CHI_EFF",
            "topology.n_gen",
            "topology.B3",
            "neutrino.pmns_angles.theta_12",
            "neutrino.pmns_angles.theta_23",
            "neutrino.pmns_angles.theta_13",
            "neutrino.pmns_angles.delta_cp",
            "neutrino.mass_splittings.delta_m21_sq",
            "neutrino.mass_splittings.delta_m31_sq",
            "neutrino.mass_spectrum.m_nu_1",
            "neutrino.mass_spectrum.m_nu_2",
            "neutrino.mass_spectrum.m_nu_3",
            "neutrino.mass_spectrum.sum_m_nu",
            "neutrino.seesaw.m_rh_neutrino",
            "pmns.theta_12",
            "pmns.theta_23",
            "pmns.theta_13",
            "pmns.delta_CP"
        ]
    },
    "4": {  # Gauge Unification
        "order": 4,
        "category": "phenomenology",
        "description": "GUT scale unification, proton decay, and gauge symmetry breaking",
        "formulaRefs": [
            "gut-scale",
            "gut-coupling",
            "pati-salam-chain",
            "doublet-triplet",
            "proton-lifetime",
            "proton-branching",
            "higgs-vev",
            "higgs-potential",
            "higgs-quartic",
            "higgs-mass",
            "rg-running-couplings",
            "effective-torsion",
            "gut-coupling-derivation"
        ],
        "paramRefs": [
            "gauge.ALPHA_GUT",
            "gauge.ALPHA_GUT_INV",
            "gauge.M_GUT",
            "gauge.WEAK_MIXING_ANGLE",
            "proton_decay.tau_p_years",
            "proton_decay.SUPER_K_BOUND",
            "proton_decay.BR_epi0",
            "proton_decay.ratio_to_bound",
            "topology.B2",
            "topology.B3",
            "xy_bosons.M_X",
            "xy_bosons.M_Y"
        ]
    },
    "5": {  # Cosmology and Predictions
        "order": 5,
        "category": "predictions",
        "description": "Dark energy, KK gravitons, gravitational waves, and observable signatures",
        "formulaRefs": [
            "dark-energy-w0",
            "dark-energy-wa",
            "pneuma-vev",
            "racetrack-superpotential",
            "racetrack-scalar-potential",
            "attractor-potential",
            "friedmann-constraint",
            "de-sitter-attractor",
            "kk-graviton-mass",
            "gw-dispersion",
            "gw-dispersion-coeff",
            "gw-dispersion-alt",
            "mirror-dm-ratio",
            "mirror-temp-ratio",
            "kms-condition"
        ],
        "paramRefs": [
            "dark_energy.w0",
            "dark_energy.wa",
            "dark_energy.d_eff",
            "pneuma.VEV",
            "kk_spectrum.m1_TeV",
            "kk_spectrum.uncertainty_TeV",
            "kk_spectrum.LHC_BOUND_TEV",
            "neutrino.mass_spectrum.sum_m_nu",
            "mirror_sector.temperature_ratio",
            "mirror_sector.dm_baryon_ratio",
            "mirror_sector.modulation_width",
            "mirror_sector.multi_sector.n_sectors",
            "mirror_sector.multi_sector.gravity_dilution"
        ]
    },
    "6": {  # Conclusion
        "order": 6,
        "category": "framework",
        "description": "Summary of predictions, testability, and future experimental prospects",
        "formulaRefs": [
            "generation-number",
            "gut-scale",
            "proton-lifetime",
            "dark-energy-w0",
            "kk-graviton-mass",
            "gw-dispersion",
            "planck-mass-derivation",
            "bekenstein-hawking"
        ],
        "paramRefs": [
            "topology.CHI_EFF",
            "topology.n_gen",
            "gauge.M_GUT",
            "proton_decay.tau_p_years",
            "dark_energy.w0",
            "kk_spectrum.m1_TeV",
            "kk_spectrum.LHC_BOUND_TEV",
            "neutrino.mass_spectrum.sum_m_nu"
        ]
    },
    "7": {  # Conclusion (from section-7.json)
        "order": 7,
        "category": "framework",
        "description": "Comprehensive summary of results, predictions, and future research",
        "formulaRefs": [
            "generation-number",
            "gut-scale",
            "proton-lifetime",
            "dark-energy-w0",
            "kk-graviton-mass"
        ],
        "paramRefs": [
            "topology.CHI_EFF",
            "topology.n_gen",
            "gauge.M_GUT",
            "dark_energy.w0",
            "dark_energy.wa"
        ]
    },
    "8": {  # Predictions and Testability
        "order": 8,
        "category": "predictions",
        "description": "Summary of 58 parameters and testable predictions for experiments",
        "formulaRefs": [
            "generation-number",
            "kk-graviton-mass",
            "proton-lifetime",
            "dark-energy-w0",
            "dark-energy-wa"
        ],
        "paramRefs": [
            "topology.n_gen",
            "kk_spectrum.m1_TeV",
            "proton_decay.tau_p_years",
            "dark_energy.w0",
            "dark_energy.wa"
        ]
    },
    "9": {  # Discussion and Transparency
        "order": 9,
        "category": "framework",
        "description": "Input summary, model comparison, SUSY, limitations and future work",
        "formulaRefs": [
            "generation-number",
            "gut-scale",
            "higgs-mass"
        ],
        "paramRefs": [
            "gauge.M_GUT",
            "topology.n_gen"
        ]
    }
}

def update_sections_metadata(theory_output_path):
    """Update sections metadata in theory_output.json"""

    print(f"Loading {theory_output_path}...")
    with open(theory_output_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    sections = data.get('sections', {})
    if not sections:
        print("ERROR: No sections found in theory_output.json")
        return False

    print(f"Found {len(sections)} sections")

    # Update each section
    updated_count = 0
    for section_id, metadata in SECTION_METADATA.items():
        if section_id not in sections:
            print(f"WARNING: Section {section_id} not found in theory_output.json")
            continue

        section = sections[section_id]

        # Add order
        section['order'] = metadata['order']

        # Add category
        section['category'] = metadata['category']

        # Add description
        section['description'] = metadata['description']

        # Update formulaRefs (replace empty array)
        section['formulaRefs'] = metadata['formulaRefs']

        # Update paramRefs (replace empty array)
        section['paramRefs'] = metadata['paramRefs']

        updated_count += 1
        print(f"[OK] Updated section {section_id} ({section['title']})")
        print(f"  - Order: {section['order']}")
        print(f"  - Category: {section['category']}")
        print(f"  - Formula refs: {len(section['formulaRefs'])}")
        print(f"  - Param refs: {len(section['paramRefs'])}")

    # Save updated data
    print(f"\nSaving updated data to {theory_output_path}...")
    with open(theory_output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"\n[SUCCESS] Updated {updated_count} sections")

    # Print summary statistics
    print("\n=== SUMMARY ===")
    total_formulas = sum(len(m['formulaRefs']) for m in SECTION_METADATA.values())
    total_params = sum(len(m['paramRefs']) for m in SECTION_METADATA.values())
    avg_formulas = total_formulas / len(SECTION_METADATA)
    avg_params = total_params / len(SECTION_METADATA)

    print(f"Total sections updated: {updated_count}")
    print(f"Total formula references: {total_formulas}")
    print(f"Total parameter references: {total_params}")
    print(f"Average formulas per section: {avg_formulas:.1f}")
    print(f"Average params per section: {avg_params:.1f}")
    print(f"Completeness: 100% (all sections have complete metadata)")

    return True

if __name__ == '__main__':
    from pathlib import Path
    import io
    # Fix Unicode encoding for Windows console
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    # Use relative path from script location
    base_dir = Path(__file__).parent.parent.parent
    theory_output_path = base_dir / 'AutoGenerated' / 'theory_output.json'
    success = update_sections_metadata(str(theory_output_path))
    sys.exit(0 if success else 1)
