#!/usr/bin/env python3
"""
Fix foundations metadata in theory_output.json based on audit report.
This version is idempotent - safe to run multiple times.
"""

import json
from pathlib import Path

def main():
    json_path = Path(r'h:\Github\PrincipiaMetaphysica\theory_output.json')

    # Load full JSON
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    foundations = data['foundations']

    # ==============================================================
    # FIX 1: Standardize ALL category values to snake_case
    # ==============================================================

    category_updates = {
        'yang-mills': 'quantum_field_theory',
        'unruh-effect': 'quantum_field_theory',
        'ricci-tensor': 'differential_geometry',
        'tomita-takesaki': 'operator_algebras',
        'so10-gut': 'grand_unification'
    }

    for foundation in foundations:
        if foundation['id'] in category_updates:
            old_cat = foundation['category']
            new_cat = category_updates[foundation['id']]
            if old_cat != new_cat:
                print(f"  Category: {foundation['id']}: '{old_cat}' -> '{new_cat}'")
                foundation['category'] = new_cat

    # ==============================================================
    # FIX 2: Expand PM connections (add 200-300 chars each)
    # Only add if not already expanded (check length)
    # ==============================================================

    pm_connection_expansions = {
        "tomita-takesaki": """ The modular operator Δ = S*S from Tomita-Takesaki theory provides the mathematical foundation for PM's thermal time hypothesis at each dimensional level. In the 26D bulk, the Pneuma field algebra forms a type III von Neumann factor, with modular flow σ_t generating intrinsic dynamics. The KMS condition β_H = 1/(k_B T_H) connects to Hawking temperature at horizons. Each dimensional reduction (26D → 13D → 6D → 4D) has an associated modular Hamiltonian K = -log(Δ), with the 4D CMB temperature T_CMB = 2.725 K emerging as a fossil record of primordial thermalization.""",

        "yang-mills": """ The Yang-Mills gauge principle underlies PM's treatment of all fundamental forces. In the 26D bulk, gauge symmetry is embedded in the Sp(2,R) × G structure, with SO(10) GUT arising from D5-branes wrapping the b₂ = 4 associative 3-cycles of the TCS G₂ manifold. The non-abelian structure constants f^abc encode how gauge bosons self-interact. Dimensional reduction preserves Yang-Mills structure: 26D → 13D (gauge fields on shadow) → 6D → 4D where SU(3)×SU(2)×U(1) emerges. Asymptotic freedom in QCD is crucial for validating coupling unification at M_GUT = 2.118×10¹⁶ GeV.""",

        "ricci-tensor": """ The Ricci tensor and scalar are fundamental to PM's geometric framework across all dimensional levels. In the 26D bulk with signature (24,2), the Ricci tensor R_AB describes how the Pneuma field curves spacetime via Einstein equations G_AB + Λ₂₆ g_AB = 8πG₂₆ T_AB. The G₂ manifold satisfies Ric(g_G₂) = 0 (Ricci-flat), ensuring vacuum Einstein equations in the compact directions. Flux backreaction modifies the effective curvature: G₄ flux threading coassociative 4-cycles (b₃ = 24) dresses the bare topology. The 4D Ricci scalar appears in the effective Einstein-Hilbert action after compactification, with corrections from KK modes and flux contributions.""",

        "so10-gut": """ SO(10) grand unification is topologically embedded in PM's framework via D5-branes on the G₂ manifold. The 16-dimensional spinor representation contains exactly one fermion generation plus right-handed neutrino. PM's 64-component 13D shadow spinor from Cl(12,1) decomposes as 64 = 4 × 16, where each of 4 'slots' can hold a 16-plet. Three generations arise from χ_eff = 144 = 3 × 48, with divisor 48 from SO(10) index theorem on G₂. The GUT scale M_GUT = 2.118×10¹⁶ GeV emerges from torsion topology: ln(M_GUT/M_Pl) = -2π(b₂+b₃)/ν = -7.33. Proton decay p → e⁺π⁰ with lifetime τ_p = 4.09×10³⁴ years provides testable prediction.""",

        "unruh-effect": """ The Unruh effect demonstrates observer-dependent temperature T_U = ℏa/(2πck_B) that is foundational to PM's thermal time hypothesis. In PM's dimensional cascade, each stage (26D → 13D → 6D → 4D) induces effective 'acceleration' in compactified dimensions, generating thermal radiation via the Unruh mechanism. The Rindler horizon at c²/a provides a local analog to cosmological and black hole horizons. The KMS condition ⟨AB⟩_β = ⟨B α_{iβ}(A)⟩ characterizes thermal equilibrium, with modular flow from Tomita-Takesaki theory generating time evolution. The Pneuma field appears thermal to observers undergoing dimensional transitions, with the CMB temperature T_CMB = 2.725 K emerging from primordial 'deceleration' after inflation."""
    }

    for foundation in foundations:
        if foundation['id'] in pm_connection_expansions:
            current_len = len(foundation['pm_connection'])
            # Only expand if current length is less than 500 chars (original short ones)
            if current_len < 500:
                old_len = current_len
                foundation['pm_connection'] += pm_connection_expansions[foundation['id']]
                new_len = len(foundation['pm_connection'])
                print(f"  PM connection: {foundation['id']}: {old_len} -> {new_len} chars (+{new_len-old_len})")

    # ==============================================================
    # FIX 3: Add more formulas to specific foundations
    # Check for duplicates before adding
    # ==============================================================

    # Helper function to check if formula ID already exists
    def has_formula(foundation, formula_id):
        return any(f.get('id') == formula_id for f in foundation['formulas'])

    # boltzmann-entropy: currently 4, add 4 more related formulas
    boltzmann_new_formulas = [
        {
            "id": "boltzmann-microcanonical",
            "label": "Microcanonical Entropy",
            "plain_text": "S(E,V,N) = k_B ln Ω(E,V,N)",
            "latex": "S(E,V,N) = k_B \\ln \\Omega(E,V,N)",
            "description": "Entropy for isolated system with fixed energy E, volume V, particle number N"
        },
        {
            "id": "boltzmann-sackur-tetrode",
            "label": "Sackur-Tetrode Equation",
            "plain_text": "S = Nk_B[ln(V/N) + (3/2)ln(2πmk_BT/h²) + 5/2]",
            "latex": "S = Nk_B\\left[\\ln\\left(\\frac{V}{N}\\right) + \\frac{3}{2}\\ln\\left(\\frac{2\\pi mk_BT}{h^2}\\right) + \\frac{5}{2}\\right]",
            "description": "Entropy of ideal monatomic gas from quantum statistical mechanics"
        },
        {
            "id": "boltzmann-von-neumann",
            "label": "von Neumann Entropy",
            "plain_text": "S = -k_B Tr(ρ ln ρ)",
            "latex": "S = -k_B \\text{Tr}(\\rho \\ln \\rho)",
            "description": "Quantum generalization of Boltzmann entropy for density matrix ρ"
        },
        {
            "id": "boltzmann-canonical-ensemble",
            "label": "Canonical Ensemble Entropy",
            "plain_text": "S = k_B(ln Z + βE) = k_B ln Z + E/T",
            "latex": "S = k_B(\\ln Z + \\beta E) = k_B \\ln Z + \\frac{E}{T}",
            "description": "Entropy in canonical ensemble with partition function Z and average energy E"
        }
    ]

    # calabi-yau: currently 6, add 2 more
    calabi_yau_new_formulas = [
        {
            "id": "cy-kahler-form",
            "label": "Kähler Form",
            "plain_text": "ω = (i/2)g_{ij̄} dz^i ∧ dz̄^j",
            "latex": "\\omega = \\frac{i}{2}g_{i\\bar{j}} dz^i \\wedge d\\bar{z}^j",
            "description": "Kähler form defining the Kähler structure from the metric"
        },
        {
            "id": "cy-holonomy-su3",
            "label": "SU(3) Holonomy",
            "plain_text": "Hol(g) ⊆ SU(3) for CY3",
            "latex": "\\text{Hol}(g) \\subseteq \\text{SU}(3) \\text{ for CY}_3",
            "description": "Restricted holonomy group for 6D Calabi-Yau threefolds (3 complex dimensions)"
        }
    ]

    # clifford-algebra: currently 6, add 2 more
    clifford_new_formulas = [
        {
            "id": "clifford-pseudoscalar",
            "label": "Pseudoscalar (Volume Element)",
            "plain_text": "I = γ^0 γ^1 γ^2 γ^3, I² = ±1",
            "latex": "I = \\gamma^0 \\gamma^1 \\gamma^2 \\gamma^3, \\quad I^2 = \\pm 1",
            "description": "Pseudoscalar element for 4D spacetime, chirality operator γ⁵ = iI"
        },
        {
            "id": "clifford-periodicity",
            "label": "Bott Periodicity (Clifford)",
            "plain_text": "Cl(p+8,q) ≅ Cl(p,q) ⊗ Cl(8,0)",
            "latex": "\\text{Cl}(p+8,q) \\cong \\text{Cl}(p,q) \\otimes \\text{Cl}(8,0)",
            "description": "Clifford algebras are periodic with period 8 (Bott periodicity)"
        }
    ]

    # Apply formula additions (only if not already present)
    for foundation in foundations:
        if foundation['id'] == 'boltzmann-entropy':
            added = 0
            for formula in boltzmann_new_formulas:
                if not has_formula(foundation, formula['id']):
                    foundation['formulas'].append(formula)
                    added += 1
            if added > 0:
                print(f"  Formulas: boltzmann-entropy: added {added} formulas (now {len(foundation['formulas'])} total)")

        elif foundation['id'] == 'calabi-yau':
            added = 0
            for formula in calabi_yau_new_formulas:
                if not has_formula(foundation, formula['id']):
                    foundation['formulas'].append(formula)
                    added += 1
            if added > 0:
                print(f"  Formulas: calabi-yau: added {added} formulas (now {len(foundation['formulas'])} total)")

        elif foundation['id'] == 'clifford-algebra':
            added = 0
            for formula in clifford_new_formulas:
                if not has_formula(foundation, formula['id']):
                    foundation['formulas'].append(formula)
                    added += 1
            if added > 0:
                print(f"  Formulas: clifford-algebra: added {added} formulas (now {len(foundation['formulas'])} total)")

    # ==============================================================
    # Write back to JSON
    # ==============================================================

    data['foundations'] = foundations

    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print("\nCompleted foundations metadata fixes!")

if __name__ == '__main__':
    main()
