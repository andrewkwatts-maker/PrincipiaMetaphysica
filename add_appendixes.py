#!/usr/bin/env python3
"""
Add Appendixes A-N to theory_output.json and sections.json
"""

import json
from pathlib import Path

# Define the appendixes A-N
APPENDIXES = {
    'A': {
        'title': 'Mathematical Framework',
        'shortTitle': 'Math Framework',
        'abstract': 'Detailed mathematical foundations including G2 holonomy manifolds, spinor structures, and differential geometry.',
        'description': 'This appendix provides rigorous mathematical foundations for the geometric framework, including detailed proofs of G2 holonomy properties, spinor classification theorems, and the construction of exceptional geometric structures.',
        'category': 'appendix',
        'keywords': ['G2 holonomy', 'differential geometry', 'spinors', 'exceptional structures']
    },
    'B': {
        'title': 'G2 Holonomy Details',
        'shortTitle': 'G2 Details',
        'abstract': 'Complete derivation of G2 holonomy manifold properties, including torsion-free conditions and parallel spinor existence.',
        'description': 'Detailed analysis of G2 holonomy manifolds, including the proof of torsion-free conditions, construction of parallel spinors, and derivation of the associative calibration form.',
        'category': 'appendix',
        'keywords': ['G2 holonomy', 'torsion-free', 'parallel spinor', 'calibration']
    },
    'C': {
        'title': 'Gauge Coupling RG Flow',
        'shortTitle': 'RG Flow',
        'abstract': 'Renormalization group flow analysis of gauge couplings from GUT scale to electroweak scale.',
        'description': 'Complete renormalization group equations for gauge coupling evolution, including threshold corrections, matching conditions at intermediate scales, and precision comparison with experimental data.',
        'category': 'appendix',
        'keywords': ['RG flow', 'gauge couplings', 'unification', 'running']
    },
    'D': {
        'title': 'Neutrino Sector Details',
        'shortTitle': 'Neutrino Details',
        'abstract': 'Detailed derivation of neutrino mass matrix, mixing angles, and oscillation parameters from geometric principles.',
        'description': 'Complete analysis of the neutrino sector including mass matrix construction, diagonalization, derivation of PMNS mixing angles, and comparison with NuFIT 6.0 data.',
        'category': 'appendix',
        'keywords': ['neutrinos', 'mass matrix', 'PMNS', 'oscillations']
    },
    'E': {
        'title': 'Proton Decay Calculations',
        'shortTitle': 'Proton Decay',
        'abstract': 'Complete calculation of proton decay rates including dimension-5 and dimension-6 operators.',
        'description': 'Detailed computation of proton decay channels, operator analysis, gauge boson and Higgs contributions, and comparison with Super-Kamiokande bounds.',
        'category': 'appendix',
        'keywords': ['proton decay', 'baryon violation', 'Super-K', 'lifetime']
    },
    'F': {
        'title': 'Cosmological Predictions',
        'shortTitle': 'Cosmology',
        'abstract': 'Detailed cosmological predictions including dark energy equation of state and structure formation.',
        'description': 'Complete derivation of cosmological parameters including w₀ = -11/13, wₐ predictions, S₈ tension resolution, and comparison with DESI 2024 and Planck data.',
        'category': 'appendix',
        'keywords': ['dark energy', 'w0', 'S8', 'DESI', 'cosmology']
    },
    'G': {
        'title': 'Wolfram Proofs',
        'shortTitle': 'Proofs',
        'abstract': 'Mathematica/Wolfram Language proofs and numerical verification of key analytical results.',
        'description': 'Computer-verified proofs of analytical results using Wolfram Language, including symbolic computations, numerical stability analysis, and precision tests.',
        'category': 'appendix',
        'keywords': ['Wolfram', 'proofs', 'verification', 'symbolic']
    },
    'H': {
        'title': 'Experimental Validation',
        'shortTitle': 'Experiments',
        'abstract': 'Summary of experimental tests and validation of theoretical predictions.',
        'description': 'Comprehensive comparison of theoretical predictions with experimental data from particle physics (LHC, neutrino experiments) and cosmology (DESI, Planck, gravitational waves).',
        'category': 'appendix',
        'keywords': ['experiments', 'validation', 'LHC', 'DESI']
    },
    'I': {
        'title': 'Numerical Methods',
        'shortTitle': 'Methods',
        'abstract': 'Description of numerical techniques used for RG flow, Monte Carlo sampling, and parameter estimation.',
        'description': 'Detailed documentation of numerical methods including RG integration schemes, Monte Carlo algorithms, error propagation, and convergence tests.',
        'category': 'appendix',
        'keywords': ['numerical methods', 'RG', 'Monte Carlo', 'algorithms']
    },
    'J': {
        'title': 'Parameter Tables',
        'shortTitle': 'Tables',
        'abstract': 'Complete tables of all derived parameters with uncertainties and comparisons to experimental values.',
        'description': 'Comprehensive tables listing all 58+ SM parameters, their geometric derivations, predicted values, uncertainties, and comparison with PDG values.',
        'category': 'appendix',
        'keywords': ['parameters', 'tables', 'PDG', 'comparison']
    },
    'K': {
        'title': 'Derivation Chains',
        'shortTitle': 'Derivations',
        'abstract': 'Complete derivation chains showing how each parameter flows from geometric first principles.',
        'description': 'Detailed derivation chains for all parameters, showing the logical flow from G2 holonomy → Kaluza-Klein reduction → gauge structure → SM parameters.',
        'category': 'appendix',
        'keywords': ['derivations', 'chains', 'logic', 'flow']
    },
    'L': {
        'title': 'Mirror Sector Analysis',
        'shortTitle': 'Mirror Sector',
        'abstract': 'Detailed analysis of the Z₂ mirror sector, dark matter candidates, and cosmological implications.',
        'description': 'Complete treatment of the mirror sector including symmetry breaking, particle spectrum, interaction strengths, and dark matter phenomenology.',
        'category': 'appendix',
        'keywords': ['mirror sector', 'Z2', 'dark matter', 'symmetry']
    },
    'M': {
        'title': 'Moduli Stabilization',
        'shortTitle': 'Moduli',
        'abstract': 'Detailed analysis of moduli stabilization mechanisms and their phenomenological consequences.',
        'description': 'Complete derivation of moduli stabilization using racetrack superpotentials, flux quantization, and geometric constraints.',
        'category': 'appendix',
        'keywords': ['moduli', 'stabilization', 'racetrack', 'flux']
    },
    'N': {
        'title': 'Future Directions',
        'shortTitle': 'Future Work',
        'abstract': 'Discussion of open questions, future theoretical developments, and experimental prospects.',
        'description': 'Analysis of outstanding theoretical questions, potential model extensions, and upcoming experimental tests that could further validate or constrain the theory.',
        'category': 'appendix',
        'keywords': ['future', 'prospects', 'open questions', 'extensions']
    }
}

def add_appendixes_to_json(input_file, output_file=None):
    """Add appendixes A-N to theory_output.json or sections.json"""

    if output_file is None:
        output_file = input_file

    # Load existing data
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Get sections (handle both direct sections and nested format)
    if 'sections' in data:
        sections = data['sections']
    else:
        sections = data

    # Add each appendix
    for appendix_id, appendix_info in APPENDIXES.items():
        # Create full section structure
        section = {
            'id': appendix_id,
            'type': 'appendix',
            'title': appendix_info['title'],
            'shortTitle': appendix_info['shortTitle'],
            'order': 8 + ord(appendix_id) - ord('A') + 1,  # After section 8
            'abstract': appendix_info['abstract'],
            'description': appendix_info['description'],
            'category': appendix_info['category'],
            'keywords': appendix_info['keywords'],
            'contentBlocks': [
                {
                    'type': 'paragraph',
                    'content': appendix_info['description']
                },
                {
                    'type': 'callout',
                    'calloutType': 'note',
                    'title': 'Note',
                    'children': [
                        {
                            'type': 'paragraph',
                            'content': 'This appendix is under development. Complete derivations and proofs will be added in future versions.'
                        }
                    ]
                }
            ],
            'content_blocks': [
                {
                    'type': 'paragraph',
                    'content': appendix_info['description']
                }
            ],
            'formulaRefs': [],
            'paramRefs': [],
            'formula_refs': [],
            'param_refs': [],
            'timestamp': '2025-12-29T12:00:00'
        }

        sections[appendix_id] = section

    # Update data
    if 'sections' in data:
        data['sections'] = sections
    else:
        data = sections

    # Write back
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"[OK] Added {len(APPENDIXES)} appendixes to {output_file}")
    print(f"  Appendix IDs: {', '.join(sorted(APPENDIXES.keys()))}")
    return True

def main():
    """Add appendixes to both theory_output.json and sections.json"""
    base_dir = Path(__file__).parent / 'AutoGenerated'

    files = [
        base_dir / 'theory_output.json',
        base_dir / 'sections.json'
    ]

    for file_path in files:
        if file_path.exists():
            print(f"\nProcessing: {file_path.name}")
            add_appendixes_to_json(file_path)
        else:
            print(f"[WARNING] File not found: {file_path}")

    print("\n[OK] All appendixes added successfully!")
    print("\nYou can now:")
    print("  1. View sections.html to see appendixes A-N")
    print("  2. Navigate to individual appendixes")
    print("  3. Further populate appendix content as needed")

if __name__ == '__main__':
    main()
