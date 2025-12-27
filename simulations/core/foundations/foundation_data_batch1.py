"""
Foundation Data Batch 1
=======================

Structured data extracted from foundation HTML pages for migration to theory_output.json.
This batch includes: Boltzmann Entropy, Calabi-Yau Manifolds, Clifford Algebra, and Dirac Equation.

Copyright (c) 2025 Andrew Keith Watts. All rights reserved.
"""

FOUNDATIONS_BATCH1 = {
    "boltzmann-entropy": {
        "id": "boltzmann-entropy",
        "title": "Boltzmann Entropy",
        "category": "thermodynamics",
        "year_established": 1877,
        "badge_type": "established",
        "main_equation": "S = k_B ln Ω",
        "main_equation_latex": "S = k_B \\ln \\Omega",
        "summary": "The fundamental bridge between microscopic statistical mechanics and macroscopic thermodynamics, connecting the number of microstates to entropy.",
        "key_properties": [
            "Entropy is the logarithm of the number of ways a system can be arranged",
            "S measures macroscopic disorder or information content",
            "Ω is the number of microscopic configurations (microstates)",
            "k_B = 1.38×10⁻²³ J/K is the fundamental bridge between energy and temperature",
            "The logarithm makes entropy additive: S_total = S_1 + S_2",
            "Always increases in isolated systems (Second Law of Thermodynamics)",
            "Provides statistical foundation for classical thermodynamics",
            "Connects to Shannon information theory: entropy measures missing information"
        ],
        "pm_connection": "Boltzmann entropy plays a crucial role in PM's dimensional framework through the thermal time hypothesis. The flow of time is related to entropy increase: t ∝ S = k_B ln Ω. In higher dimensions, entropy generalizes to 26D bulk (S_26 = k_B ln Ω_26) and 13D shadow (S_13 = k_B ln Ω_13). Dimensional reduction preserves entropy through compactification. Black hole entropy S_BH = k_B A/(4ℓ_P²) suggests entropy is fundamentally geometric in higher-dimensional theories.",
        "formulas": [
            {
                "id": "boltzmann-entropy-main",
                "label": "Boltzmann Entropy",
                "plain_text": "S = k_B ln Ω",
                "latex": "S = k_B \\ln \\Omega",
                "description": "The fundamental relation between entropy and microstates"
            },
            {
                "id": "boltzmann-gibbs-generalization",
                "label": "Gibbs Entropy",
                "plain_text": "S = -k_B Σ_i p_i ln p_i",
                "latex": "S = -k_B \\sum_i p_i \\ln p_i",
                "description": "Generalization for non-equilibrium systems with probability distribution p_i"
            },
            {
                "id": "boltzmann-bh-entropy",
                "label": "Black Hole Entropy",
                "plain_text": "S_BH = k_B A/(4ℓ_P²) = k_B ln Ω_horizon",
                "latex": "S_{\\text{BH}} = \\frac{k_B A}{4\\ell_P^2} = k_B \\ln \\Omega_{\\text{horizon}}",
                "description": "Bekenstein-Hawking entropy connecting area to microstates"
            },
            {
                "id": "boltzmann-thermal-time",
                "label": "Thermal Time Hypothesis",
                "plain_text": "t ∝ S = k_B ln Ω",
                "latex": "t \\propto S = k_B \\ln \\Omega",
                "description": "Time emergence from entropy increase (Carlo Rovelli)"
            }
        ],
        "used_in_sections": [
            {
                "section": "thermal-time",
                "description": "Entropy and time emergence"
            },
            {
                "section": "cosmology",
                "description": "Thermodynamic arrow of time"
            }
        ]
    },

    "calabi-yau": {
        "id": "calabi-yau",
        "title": "Calabi-Yau Manifolds",
        "category": "geometry",
        "year_established": 1977,
        "badge_type": "established",
        "main_equation": "R_{i j̄} = 0, c_1(M) = 0",
        "main_equation_latex": "R_{i\\bar{j}} = 0, \\quad c_1(M) = 0",
        "summary": "Special geometric spaces that preserve supersymmetry when used for dimensional compactification, central to string theory and F-theory.",
        "key_properties": [
            "Compact Kähler manifolds with vanishing first Chern class",
            "Ricci-flat metric: no intrinsic curvature in compact dimensions",
            "Preserve N=1 supersymmetry in compactification",
            "Kähler structure provides geometric stability",
            "Non-trivial topology allows chiral matter from index theorems",
            "Holonomy group determines preserved gauge symmetry",
            "Mirror symmetry relates different CY manifolds"
        ],
        "pm_connection": "In the 2T framework, the 26D bulk (24,2) projects via Sp(2,R) to 13D shadow (12,1), which undergoes G₂ compactification rather than CY4 (though CY4 concepts inform topology). Two CY4 spaces (CY4_A and CY4_B) are mirror pairs with χ_A = χ_B = 72, giving χ_eff = 144 total. Fermion generations: n_gen = χ_eff/48 = 144/48 = 3, where divisor 48 comes from SO(10) GUT embedding. KKLT flux stabilization with modulus VEV φ_M = 2.493 M_Pl provides the effective topology.",
        "formulas": [
            {
                "id": "cy-ricci-flat",
                "label": "Ricci-Flat Condition",
                "plain_text": "R_{i j̄} = 0",
                "latex": "R_{i\\bar{j}} = 0",
                "description": "Ricci curvature vanishes for Calabi-Yau manifolds"
            },
            {
                "id": "cy-chern-class",
                "label": "First Chern Class",
                "plain_text": "c_1(M) = 0",
                "latex": "c_1(M) = 0",
                "description": "Topological condition equivalent to Ricci-flatness (Calabi conjecture)"
            },
            {
                "id": "cy-euler-characteristic",
                "label": "Euler Characteristic",
                "plain_text": "χ = Σ_{p,q} (-1)^{p+q} h^{p,q}",
                "latex": "\\chi = \\sum_{p,q} (-1)^{p+q} h^{p,q}",
                "description": "Topological invariant from Hodge numbers"
            },
            {
                "id": "cy-generation-formula",
                "label": "Fermion Generation Formula",
                "plain_text": "n_gen = χ_eff/48 = 144/48 = 3",
                "latex": "n_{\\text{gen}} = \\frac{\\chi_{\\text{eff}}}{48} = \\frac{144}{48} = 3",
                "description": "Number of generations from effective Euler characteristic in 2T framework"
            },
            {
                "id": "cy-mirror-symmetry",
                "label": "Mirror Symmetry",
                "plain_text": "χ_A + χ_B = 72 + 72 = 144",
                "latex": "\\chi_A + \\chi_B = 72 + 72 = 144",
                "description": "Combined Euler characteristic from mirror CY4 pair"
            },
            {
                "id": "cy-kklt-flux",
                "label": "KKLT Flux Stabilization",
                "plain_text": "χ_eff = χ_bare + Δχ_flux, φ_M = 2.493 M_Pl",
                "latex": "\\chi_{\\text{eff}} = \\chi_{\\text{bare}} + \\Delta\\chi_{\\text{flux}}, \\quad \\varphi_M = 2.493 M_{\\text{Pl}}",
                "description": "Flux dressing modifies effective topology with modulus VEV"
            }
        ],
        "used_in_sections": [
            {
                "section": "geometric-framework",
                "description": "Comparison with G₂ compactification"
            }
        ]
    },

    "clifford-algebra": {
        "id": "clifford-algebra",
        "title": "Clifford Algebra",
        "category": "algebra",
        "year_established": 1878,
        "badge_type": "established",
        "main_equation": "{γ^μ, γ^ν} = 2g^{μν}",
        "main_equation_latex": "\\{\\gamma^\\mu, \\gamma^\\nu\\} = 2g^{\\mu\\nu}",
        "summary": "The mathematical framework that unifies real numbers, complex numbers, quaternions, and geometric algebra - essential for describing spinors and fermions in physics.",
        "key_properties": [
            "Natural generalization of complex numbers and quaternions to arbitrary dimensions",
            "Geometric product combines dot product and wedge product",
            "Spinors arise as elements of minimal left ideals (irreducible representations)",
            "Spinor dimension formula: 2^⌊n/2⌋ for n-dimensional space",
            "360° rotation changes sign of spinor; 720° returns to original (double cover)",
            "Fundamental for describing fermions (spin-1/2 particles)",
            "Hierarchy: R → C → H → Cl(p,q) generalizes number systems"
        ],
        "pm_connection": "Clifford algebras provide the mathematical framework for spinors at each dimensional level in PM. 26D bulk: Cl(24,2) with 8192-component spinors (2^13). 13D shadow: Cl(12,1) with 64-component spinors (2^6). Reduction factor: 8192/64 = 128 = 2^7 preserves power-of-two structure. The 64 components in 13D encode fermion generation structure: 64 = 4×16 suggests SO(10) GUT embedding with 3 generations from topology.",
        "formulas": [
            {
                "id": "clifford-anticommutator",
                "label": "Clifford Algebra Relation",
                "plain_text": "{γ^μ, γ^ν} = 2g^{μν}",
                "latex": "\\{\\gamma^\\mu, \\gamma^\\nu\\} = 2g^{\\mu\\nu}",
                "description": "Fundamental anticommutation relation defining Clifford algebra"
            },
            {
                "id": "clifford-geometric-product",
                "label": "Geometric Product",
                "plain_text": "ab = a·b + a∧b",
                "latex": "ab = a \\cdot b + a \\wedge b",
                "description": "Combines inner and outer products into unified algebraic structure"
            },
            {
                "id": "clifford-spinor-dimension",
                "label": "Spinor Dimension",
                "plain_text": "dim(Spinor) = 2^⌊n/2⌋",
                "latex": "\\dim(\\text{Spinor}) = 2^{\\lfloor n/2 \\rfloor}",
                "description": "Irreducible spinor representation dimension for Cl(p,q) with n=p+q"
            },
            {
                "id": "clifford-26d-bulk",
                "label": "26D Bulk Spinor",
                "plain_text": "Cl(24,2) → 2^13 = 8192 components",
                "latex": "\\text{Cl}(24,2) \\to 2^{13} = 8192 \\text{ components}",
                "description": "Spinor dimension in PM's 26D bulk with signature (24,2)"
            },
            {
                "id": "clifford-13d-shadow",
                "label": "13D Shadow Spinor",
                "plain_text": "Cl(12,1) → 2^6 = 64 components",
                "latex": "\\text{Cl}(12,1) \\to 2^6 = 64 \\text{ components}",
                "description": "Spinor dimension in PM's 13D shadow manifold"
            },
            {
                "id": "clifford-4d-dirac",
                "label": "4D Dirac Spinor",
                "plain_text": "Cl(3,1) → 2^2 = 4 components",
                "latex": "\\text{Cl}(3,1) \\to 2^2 = 4 \\text{ components}",
                "description": "Standard Dirac spinor in 4D spacetime"
            }
        ],
        "used_in_sections": [
            {
                "section": "fermion-sector",
                "description": "Spinor representations and chirality"
            },
            {
                "section": "pneuma-lagrangian",
                "description": "8192-component bulk spinor"
            },
            {
                "section": "geometric-framework",
                "description": "Cl(24,2) → Cl(12,1) reduction"
            }
        ]
    },

    "dirac-equation": {
        "id": "dirac-equation",
        "title": "Dirac Equation",
        "category": "quantum",
        "year_established": 1928,
        "badge_type": "established",
        "main_equation": "(iγ^μ∂_μ - m)ψ = 0",
        "main_equation_latex": "(i\\gamma^\\mu\\partial_\\mu - m)\\psi = 0",
        "summary": "The relativistic wave equation for spin-½ particles, unifying quantum mechanics and special relativity. First equation to predict antimatter.",
        "key_properties": [
            "Describes particles with spin-½ (electrons, quarks, neutrinos)",
            "Combines quantum mechanics, special relativity, and spin",
            "Predicts existence of antimatter (negative energy solutions)",
            "Uses 4×4 gamma matrices satisfying Clifford algebra",
            "ψ is a 4-component Dirac spinor field",
            "Lorentz invariant under proper Lorentz transformations",
            "Lagrangian form: L = ψ̄(iγ^μ∂_μ - m)ψ with Dirac adjoint ψ̄ = ψ†γ^0"
        ],
        "pm_connection": "The Pneuma Lagrangian is a 26D generalization of the Dirac equation in the 2T framework with fermionic primacy. 26D bulk: Ψ_P has 8192 components from Cl(24,2) - geometry emerges from spinor condensate g_MN ~ ⟨Ψ̄_P Γ_(MN) Ψ_P⟩. 13D shadow: 64 components from Cl(12,1) after dimensional reduction (factor 128 = 2^7). The 64-component shadow spinor connects to SO(10) GUT and 3 generations: 64 = 4×16 with each generation containing 16 fermions in SO(10).",
        "formulas": [
            {
                "id": "dirac-equation-main",
                "label": "Dirac Equation",
                "plain_text": "(iγ^μ∂_μ - m)ψ = 0",
                "latex": "(i\\gamma^\\mu\\partial_\\mu - m)\\psi = 0",
                "description": "Relativistic wave equation for spin-½ particles"
            },
            {
                "id": "dirac-lagrangian",
                "label": "Dirac Lagrangian",
                "plain_text": "L = ψ̄(iγ^μ∂_μ - m)ψ",
                "latex": "\\mathcal{L} = \\bar{\\psi}(i\\gamma^\\mu\\partial_\\mu - m)\\psi",
                "description": "Lagrangian density for Dirac field"
            },
            {
                "id": "dirac-adjoint",
                "label": "Dirac Adjoint",
                "plain_text": "ψ̄ = ψ†γ^0",
                "latex": "\\bar{\\psi} = \\psi^\\dagger \\gamma^0",
                "description": "Adjoint spinor ensuring Lorentz invariance"
            },
            {
                "id": "dirac-pneuma-26d",
                "label": "26D Pneuma Lagrangian",
                "plain_text": "Ψ̄_P(iΓ^A D_A - m_P)Ψ_P",
                "latex": "\\bar{\\Psi}_P(i\\Gamma^A D_A - m_P)\\Psi_P",
                "description": "26D generalization with 8192-component spinor in Cl(24,2)"
            },
            {
                "id": "dirac-spinor-reduction",
                "label": "Spinor Reduction Pathway",
                "plain_text": "8192 (26D) → 64 (13D) → 4 (4D) components",
                "latex": "8192 \\text{ (26D)} \\to 64 \\text{ (13D)} \\to 4 \\text{ (4D) components}",
                "description": "Dimensional reduction preserves Clifford structure"
            },
            {
                "id": "dirac-geometry-emergence",
                "label": "Geometry from Spinor Condensate",
                "plain_text": "g_MN ~ ⟨Ψ̄_P Γ_(MN) Ψ_P⟩",
                "latex": "g_{MN} \\sim \\langle \\bar{\\Psi}_P \\Gamma_{(MN)} \\Psi_P \\rangle",
                "description": "Metric emerges from spinor bivector condensate (fermionic primacy)"
            },
            {
                "id": "dirac-6d-reduction",
                "label": "6D Dirac Equation",
                "plain_text": "(iΓ^M∂_M - m)Ψ = 0, M=0,1,2,3,5,6",
                "latex": "(i\\Gamma^M\\partial_M - m)\\Psi = 0, \\quad M=0,1,2,3,5,6",
                "description": "Intermediate 6D stage with 8-component spinor from Cl(5,1)"
            },
            {
                "id": "dirac-kk-tower",
                "label": "KK Mode Expansion",
                "plain_text": "Ψ(x^μ,y,z) = Σ_{n,m} ψ_{n,m}(x^μ) Y_{n,m}(y,z)",
                "latex": "\\Psi(x^\\mu,y,z) = \\sum_{n,m} \\psi_{n,m}(x^\\mu) Y_{n,m}(y,z)",
                "description": "Kaluza-Klein decomposition on T² torus"
            }
        ],
        "used_in_sections": [
            {
                "section": "pneuma-lagrangian",
                "description": "26D generalization of Dirac equation"
            },
            {
                "section": "fermion-sector",
                "description": "Spinor fields"
            }
        ]
    }
}


# Validation and metadata
BATCH1_METADATA = {
    "batch_name": "Foundation Data Batch 1",
    "num_foundations": len(FOUNDATIONS_BATCH1),
    "foundation_ids": list(FOUNDATIONS_BATCH1.keys()),
    "categories": list(set(f["category"] for f in FOUNDATIONS_BATCH1.values())),
    "year_range": (
        min(f["year_established"] for f in FOUNDATIONS_BATCH1.values()),
        max(f["year_established"] for f in FOUNDATIONS_BATCH1.values())
    ),
    "total_formulas": sum(len(f["formulas"]) for f in FOUNDATIONS_BATCH1.values()),
    "extraction_date": "2025-12-26",
    "source_files": [
        "h:\\Github\\PrincipiaMetaphysica\\foundations\\boltzmann-entropy.html",
        "h:\\Github\\PrincipiaMetaphysica\\foundations\\calabi-yau.html",
        "h:\\Github\\PrincipiaMetaphysica\\foundations\\clifford-algebra.html",
        "h:\\Github\\PrincipiaMetaphysica\\foundations\\dirac-equation.html"
    ]
}


def get_foundation_by_id(foundation_id):
    """Retrieve foundation data by ID."""
    return FOUNDATIONS_BATCH1.get(foundation_id)


def get_foundations_by_category(category):
    """Retrieve all foundations in a given category."""
    return {
        fid: fdata
        for fid, fdata in FOUNDATIONS_BATCH1.items()
        if fdata["category"] == category
    }


def get_all_formulas():
    """Extract all formulas from all foundations."""
    all_formulas = []
    for fid, fdata in FOUNDATIONS_BATCH1.items():
        for formula in fdata["formulas"]:
            formula_copy = formula.copy()
            formula_copy["foundation_id"] = fid
            formula_copy["foundation_title"] = fdata["title"]
            all_formulas.append(formula_copy)
    return all_formulas


def validate_structure():
    """Validate the structure of the foundation data."""
    required_keys = {
        "id", "title", "category", "year_established", "badge_type",
        "main_equation", "main_equation_latex", "summary",
        "key_properties", "pm_connection", "formulas"
    }

    for fid, fdata in FOUNDATIONS_BATCH1.items():
        # Check all required keys present
        missing_keys = required_keys - set(fdata.keys())
        if missing_keys:
            print(f"Warning: {fid} missing keys: {missing_keys}")

        # Validate formulas
        for formula in fdata["formulas"]:
            required_formula_keys = {"id", "label", "plain_text", "latex", "description"}
            missing_formula_keys = required_formula_keys - set(formula.keys())
            if missing_formula_keys:
                print(f"Warning: Formula in {fid} missing keys: {missing_formula_keys}")

    print(f"Validation complete: {len(FOUNDATIONS_BATCH1)} foundations checked")
    return True


if __name__ == "__main__":
    # Run validation
    validate_structure()

    # Print summary
    print(f"\n{BATCH1_METADATA['batch_name']}")
    print("=" * 60)
    print(f"Foundations: {BATCH1_METADATA['num_foundations']}")
    print(f"Categories: {', '.join(BATCH1_METADATA['categories'])}")
    print(f"Year range: {BATCH1_METADATA['year_range'][0]}-{BATCH1_METADATA['year_range'][1]}")
    print(f"Total formulas: {BATCH1_METADATA['total_formulas']}")
    print(f"\nFoundations included:")
    for fid in BATCH1_METADATA['foundation_ids']:
        fdata = FOUNDATIONS_BATCH1[fid]
        print(f"  - {fdata['title']} ({fdata['year_established']}) - {len(fdata['formulas'])} formulas")
