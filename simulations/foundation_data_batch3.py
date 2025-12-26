"""
Foundation data extraction - Batch 3
Extracted from HTML foundation files for migration to theory_output.json

Files processed:
- hawking-temperature.html
- kaluza-klein.html
- kms-condition.html
- metric-tensor.html

Copyright (c) 2025 Andrew Keith Watts. All rights reserved.
"""

FOUNDATIONS_BATCH3 = {
    "hawking-temperature": {
        "id": "hawking-temperature",
        "title": "Hawking Temperature",
        "category": "thermodynamics",
        "year_established": 1974,
        "badge_type": "established",
        "main_equation": "T_H = ℏc³/(8πGMk_B) = ℏκ/(2πck_B)",
        "main_equation_latex": r"T_H = \frac{\hbar c^3}{8\pi G M k_B} = \frac{\hbar \kappa}{2\pi c k_B}",
        "summary": "The temperature at which black holes emit thermal radiation, unifying quantum mechanics, general relativity, and thermodynamics.",
        "key_properties": [
            "Black holes are not completely black—they emit thermal radiation at a temperature inversely proportional to their mass",
            "T_H ∝ 1/M: Smaller black holes are hotter and evaporate faster",
            "Contains ℏ (quantum), G (gravity), and c (relativity)—a window into quantum gravity",
            "Surface gravity κ at the event horizon determines the temperature",
            "For a solar mass black hole: T_H ≈ 60 nanokelvin (much colder than the CMB)",
            "Evaporation time scales as t_evap ∝ M³, making stellar-mass black holes effectively eternal",
            "Primordial black holes of mass ~10¹⁵ g could be evaporating now",
            "Leads to the black hole information paradox: how is quantum information preserved during evaporation?"
        ],
        "pm_connection": "Hawking temperature plays a crucial role in PM's treatment of black holes and dimensional reduction. In the thermal time hypothesis, Hawking radiation provides a concrete example where the vacuum state satisfies the KMS condition with β_H = 1/(k_B T_H). The modular flow generates evolution at the horizon, with temperature emerging from geometry (surface gravity κ). PM extends black hole thermodynamics to the 26D bulk, where higher-dimensional horizons have different topology and thermodynamics. In Kaluza-Klein black holes, compactified dimensions affect black hole properties. The Hawking temperature indicates where quantum gravity becomes important: near the Planck mass M_Planck = √(ℏc/G), the semiclassical approximation breaks down and PM's higher-dimensional quantum geometry becomes relevant.",
        "formulas": [
            {
                "name": "Hawking Temperature (Mass Form)",
                "equation": "T_H = ℏc³/(8πGMk_B)",
                "latex": r"T_H = \frac{\hbar c^3}{8\pi G M k_B}",
                "description": "Temperature as a function of black hole mass M. Inversely proportional to mass."
            },
            {
                "name": "Hawking Temperature (Surface Gravity Form)",
                "equation": "T_H = ℏκ/(2πck_B)",
                "latex": r"T_H = \frac{\hbar \kappa}{2\pi c k_B}",
                "description": "Temperature expressed in terms of surface gravity κ at the event horizon."
            },
            {
                "name": "Surface Gravity (Schwarzschild)",
                "equation": "κ = c⁴/(4GM) = GM/r_s²",
                "latex": r"\kappa = \frac{c^4}{4GM} = \frac{GM}{r_s^2}",
                "description": "Surface gravity for a Schwarzschild black hole, where r_s = 2GM/c² is the Schwarzschild radius."
            },
            {
                "name": "Bekenstein-Hawking Entropy",
                "equation": "S_BH = k_B A/(4ℓ_P²) = k_B c³A/(4ℏG)",
                "latex": r"S_{BH} = \frac{k_B A}{4\ell_P^2} = \frac{k_B c^3 A}{4\hbar G}",
                "description": "Black hole entropy proportional to horizon area A. Holographic principle."
            },
            {
                "name": "Evaporation Time",
                "equation": "t_evap = (5120πG²M³)/(ℏc⁴)",
                "latex": r"t_{evap} = \frac{5120\pi G^2 M^3}{\hbar c^4}",
                "description": "Time for a Schwarzschild black hole to completely evaporate via Hawking radiation."
            },
            {
                "name": "First Law of Black Hole Thermodynamics",
                "equation": "dM = (κ/8πG)dA + Ω_H dJ + Φ_H dQ",
                "latex": r"dM = \frac{\kappa}{8\pi G}dA + \Omega_H dJ + \Phi_H dQ",
                "description": "Analogue of thermodynamic first law for black holes with rotation and charge."
            },
            {
                "name": "Kerr Black Hole Temperature",
                "equation": "T_H = ℏc³(r₊ - r₋)/(4πGk_B(r₊² + a²))",
                "latex": r"T_H = \frac{\hbar c^3 (r_+ - r_-)}{4\pi G k_B (r_+^2 + a^2)}",
                "description": "Hawking temperature for rotating (Kerr) black hole with spin parameter a = J/(Mc)."
            },
            {
                "name": "Unruh Temperature",
                "equation": "T_U = ℏa/(2πck_B)",
                "latex": r"T_U = \frac{\hbar a}{2\pi c k_B}",
                "description": "Temperature experienced by an accelerating observer with proper acceleration a. Related to Hawking temperature via equivalence principle."
            }
        ]
    },

    "kaluza-klein": {
        "id": "kaluza-klein",
        "title": "Kaluza-Klein Theory",
        "category": "dimensional_reduction",
        "year_established": 1921,
        "badge_type": "established",
        "main_equation": "Higher D → 4D | Compactification on S¹",
        "main_equation_latex": r"\text{Higher } D \rightarrow 4D \quad | \quad \text{Compactification on } S^1",
        "summary": "The groundbreaking theory showing how extra spatial dimensions can be 'curled up' so small they become invisible, unifying gravity and electromagnetism in higher dimensions.",
        "key_properties": [
            "Extra dimensions can be compactified (curled up) to such small sizes that they're invisible at low energies",
            "Like a garden hose looks 1D from far away but is really 2D with a tiny circular dimension",
            "Motion in the compact dimension appears as massive particles in 4D with mass m_n = n/R",
            "The n=0 mode is massless and corresponds to the 4D fields we observe (photon, graviton)",
            "Heavy KK modes (n≥1) are too massive to produce at current energies",
            "Current LHC limit: R < 10⁻¹⁹ m from lack of observed KK modes",
            "5D metric component g_μ5 becomes the electromagnetic potential A_μ in 4D",
            "Kaluza-Klein theory is the foundation for string theory's extra dimensions"
        ],
        "pm_connection": "Principia Metaphysica employs a multi-stage compactification process from 26D down to the observed 4D. The pathway is: 26D → 13D → 6D → 4D. The 26D → 13D stage involves Sp(2,R) gauge fixing in 2T physics (not standard KK compactification but gauge-theoretic reduction). The 13D → 6D stage uses a G₂ manifold compactification (7D with holonomy G₂), preserving N=1 supersymmetry. The specific construction is TCS G₂ with b₂=4, b₃=24, χ=-540. The KK mass scale is m_KK ~ 1/R_G₂ where R_G₂ ~ 10⁻³⁵ m (Planck scale). Finally, 6D → 4D involves further compactification on a 2D surface. Unlike single-scale KK theory, PM has multiple compactification scales at different stages, potentially explaining the hierarchy problem. PM likely employs flux compactification to stabilize the moduli (size and shape of compact dimensions), with background fluxes generating a potential that fixes the compactification radius.",
        "formulas": [
            {
                "name": "5D Kaluza-Klein Metric",
                "equation": "ds²₍₅D₎ = g_μν dx^μ dx^ν + φ²(dy + A_μ dx^μ)²",
                "latex": r"ds^2_{(5D)} = g_{\mu\nu} dx^\mu dx^\nu + \phi^2(dy + A_\mu dx^\mu)^2",
                "description": "5D metric decomposed into 4D metric g_μν, gauge field A_μ (photon), and radion φ (dilaton)."
            },
            {
                "name": "KK Mass Spectrum",
                "equation": "m_n² = (n/R)²",
                "latex": r"m_n^2 = \left(\frac{n}{R}\right)^2",
                "description": "Tower of massive states from quantized momentum in compact dimension. n = 0,1,2,3,..."
            },
            {
                "name": "Compactification Periodicity",
                "equation": "y₅ ~ y₅ + 2πR",
                "latex": r"y_5 \sim y_5 + 2\pi R",
                "description": "Periodic identification for circle compactification of radius R."
            },
            {
                "name": "KK Mode Wavefunction",
                "equation": "ψ_n(y) = e^(iny/R) / √(2πR)",
                "latex": r"\psi_n(y) = \frac{e^{iny/R}}{\sqrt{2\pi R}}",
                "description": "Normalized wavefunction for nth KK mode in compact direction."
            },
            {
                "name": "Higher-Dimensional Bekenstein-Hawking Entropy",
                "equation": "S_BH = k_B A_{d-2} / (4ℓ_{P,d}^{d-2})",
                "latex": r"S_{BH} = \frac{k_B A_{d-2}}{4\ell_{P,d}^{d-2}}",
                "description": "Black hole entropy in d spacetime dimensions, generalizing 4D formula."
            },
            {
                "name": "Fundamental vs Observed Planck Scale (ADD Model)",
                "equation": "M_Pl² ~ M_*^{n+2} R^n",
                "latex": r"M_{Pl}^2 \sim M_*^{n+2} R^n",
                "description": "Relation between 4D Planck scale M_Pl and fundamental scale M_* with n extra dimensions of size R."
            }
        ]
    },

    "kms-condition": {
        "id": "kms-condition",
        "title": "KMS Condition",
        "category": "thermal_qft",
        "year_established": 1967,
        "badge_type": "established",
        "main_equation": "⟨AB⟩_β = ⟨B α_{iβ}(A)⟩",
        "main_equation_latex": r"\langle AB \rangle_\beta = \langle B \alpha_{i\beta}(A) \rangle",
        "summary": "The mathematical condition characterizing thermal equilibrium states in quantum field theory, connecting temperature to the analytic structure of correlation functions.",
        "key_properties": [
            "Thermal states exhibit periodicity in imaginary time with period β = 1/(k_B T)",
            "Left side ⟨AB⟩_β is the thermal correlation between operators A and B",
            "Right side α_{iβ}(A) is the operator A evolved in imaginary time by iβ (modular automorphism)",
            "Relates correlation functions to their analytically continued counterparts",
            "Correlation functions are analytic in the strip 0 < Im(t) < β",
            "Boundary conditions at Im(t) = 0 and Im(t) = β give the KMS relation",
            "Generalizes thermal equilibrium beyond systems with a Hamiltonian to arbitrary quantum systems",
            "Appears naturally in curved spacetime: Hawking radiation and Unruh effect satisfy KMS condition"
        ],
        "pm_connection": "The KMS condition plays a crucial role in the thermodynamic properties of the pneuma field and the emergence of time in PM. In the thermal time hypothesis, the flow of time emerges from the thermal properties of quantum states. The modular flow σ_t from the KMS condition provides a notion of 'thermal time' independent of external clocks. Physical time is identified with modular automorphism evolution, with inverse temperature β setting the timescale for thermal processes. The pneuma field Ψ in the 26D bulk exhibits thermal characteristics related to dimensional reduction. Dimensional compactification induces effective thermal states, and each dimensional shadow (26D → 13D → 6D → 4D) has associated KMS thermal properties. The holographic thermality relates KMS states in different dimensions via bulk-boundary correspondence. The observed CMB temperature T_CMB = 2.725 K connects to the KMS condition for the cosmological horizon, with horizon thermality exhibited by both cosmological and black hole horizons. The CMB temperature serves as a fossil record of early universe thermalization.",
        "formulas": [
            {
                "name": "KMS Condition",
                "equation": "⟨AB⟩_β = ⟨B α_{iβ}(A)⟩",
                "latex": r"\langle AB \rangle_\beta = \langle B \alpha_{i\beta}(A) \rangle",
                "description": "Fundamental KMS relation for thermal states at inverse temperature β = 1/(k_B T)."
            },
            {
                "name": "Thermal Density Matrix",
                "equation": "ρ_β = e^{-βH} / Z",
                "latex": r"\rho_\beta = \frac{e^{-\beta H}}{Z}",
                "description": "Gibbs thermal state with partition function Z = Tr(e^{-βH})."
            },
            {
                "name": "Thermal Expectation Value",
                "equation": "⟨A⟩_β = Tr(e^{-βH}A)/Z",
                "latex": r"\langle A \rangle_\beta = \frac{\text{Tr}(e^{-\beta H}A)}{Z}",
                "description": "Expectation value in the thermal state."
            },
            {
                "name": "Time Evolution Automorphism",
                "equation": "α_t(A) = e^{iHt} A e^{-iHt}",
                "latex": r"\alpha_t(A) = e^{iHt} A e^{-iHt}",
                "description": "Heisenberg time evolution. For imaginary time t → iβ, becomes modular flow."
            },
            {
                "name": "Euclidean Correlation Function",
                "equation": "G(τ) = ⟨A(τ)B(0)⟩_β = Tr(e^{-βH} A(e^{-Hτ})B e^{Hτ})/Z",
                "latex": r"G(\tau) = \langle A(\tau)B(0) \rangle_\beta = \frac{\text{Tr}(e^{-\beta H} A(e^{-H\tau})B e^{H\tau})}{Z}",
                "description": "Correlation function in imaginary (Euclidean) time, periodic with period β."
            },
            {
                "name": "Imaginary Time Periodicity",
                "equation": "G(τ + β) = G(τ)",
                "latex": r"G(\tau + \beta) = G(\tau)",
                "description": "Thermal Green's functions are periodic in imaginary time with period β."
            },
            {
                "name": "Hawking Temperature (KMS Form)",
                "equation": "T_H = ℏc³/(8πGk_B M) = ℏκ/(2πck_B)",
                "latex": r"T_H = \frac{\hbar c^3}{8\pi G k_B M} = \frac{\hbar \kappa}{2\pi c k_B}",
                "description": "Black holes emit thermal radiation satisfying KMS condition with this temperature."
            },
            {
                "name": "Unruh Temperature (KMS Form)",
                "equation": "T_U = ℏa/(2πck_B)",
                "latex": r"T_U = \frac{\hbar a}{2\pi c k_B}",
                "description": "Accelerating observer sees Minkowski vacuum as thermal bath at this temperature, satisfying KMS."
            },
            {
                "name": "Modular Automorphism (General)",
                "equation": "σ_t(A) = Δ^{it} A Δ^{-it}",
                "latex": r"\sigma_t(A) = \Delta^{it} A \Delta^{-it}",
                "description": "Modular automorphism from Tomita-Takesaki theory, generalizing thermal time evolution."
            }
        ]
    },

    "metric-tensor": {
        "id": "metric-tensor",
        "title": "Metric Tensor",
        "category": "differential_geometry",
        "year_established": 1854,
        "badge_type": "established",
        "main_equation": "ds² = g_μν dx^μ dx^ν",
        "main_equation_latex": r"ds^2 = g_{\mu\nu} dx^\mu dx^\nu",
        "summary": "The fundamental mathematical object that encodes the geometry of spacetime, defining distances, angles, and the causal structure of the universe.",
        "key_properties": [
            "The metric tensor g_μν tells you how to measure distances and time intervals in curved spacetime",
            "Line element ds² generalizes the Pythagorean theorem to curved spaces",
            "Metric signature determines which directions are timelike, spacelike, or null",
            "Standard 4D signature: (3,1) or (-,+,+,+) representing 3 space + 1 time dimensions",
            "Contains all geometric information: distances, angles, volumes, geodesics, and curvature derive from g_μν",
            "Invariant under coordinate transformations: all observers agree on ds²",
            "In 4D, the metric is a symmetric matrix with 10 independent components",
            "Inverse metric g^μν is used to raise indices and compute curvature tensors"
        ],
        "pm_connection": "The metric tensor is fundamental to PM's geometric framework. At each dimensional stage, a metric defines the geometry with specific signatures. The 26D bulk metric g_AB^(26) has signature (24,2) - two timelike directions allowing Sp(2,R) gauge symmetry. The extra time dimension enables causal paradox resolution. After Sp(2,R) gauge fixing, the 13D shadow metric g_MN^(13) has signature (12,1), returning to standard (n-1,1) signature spacetime. The 6D bulk metric g_μν^(6) has signature (5,1), with the G₂ manifold internal space contributing to this geometry. Finally, the observed 4D metric g_μν^(4) has signature (3,1), the standard spacetime metric we measure. The line element generalizes at each stage: ds² = g_AB^(D) dx^A dx^B. The (n,2) signature in higher dimensions is essential for two-time physics. The Sp(2,R) gauge symmetry acts on the two timelike directions, and gauge fixing reduces to a single observed time dimension, resolving the apparent contradiction while maintaining mathematical consistency. All curvature quantities (Ricci tensor, Einstein tensor) are ultimately derived from the metric at each dimensional stage.",
        "formulas": [
            {
                "name": "Spacetime Interval (Line Element)",
                "equation": "ds² = g_μν dx^μ dx^ν",
                "latex": r"ds^2 = g_{\mu\nu} dx^\mu dx^\nu",
                "description": "Infinitesimal distance between nearby events in spacetime. Invariant under coordinate transformations."
            },
            {
                "name": "Minkowski Metric",
                "equation": "η_μν = diag(-1, 1, 1, 1)",
                "latex": r"\eta_{\mu\nu} = \text{diag}(-1, 1, 1, 1)",
                "description": "Flat spacetime metric for Special Relativity. Signature (3,1) or (-,+,+,+)."
            },
            {
                "name": "Minkowski Line Element",
                "equation": "ds² = -dt² + dx² + dy² + dz²",
                "latex": r"ds^2 = -dt^2 + dx^2 + dy^2 + dz^2",
                "description": "Flat spacetime interval in Cartesian coordinates."
            },
            {
                "name": "Schwarzschild Metric",
                "equation": "ds² = -(1-r_s/r)dt² + (1-r_s/r)⁻¹dr² + r²dΩ²",
                "latex": r"ds^2 = -\left(1-\frac{r_s}{r}\right)dt^2 + \left(1-\frac{r_s}{r}\right)^{-1}dr^2 + r^2 d\Omega^2",
                "description": "Metric around a non-rotating spherical mass or black hole. r_s = 2GM/c² is Schwarzschild radius."
            },
            {
                "name": "FLRW Metric",
                "equation": "ds² = -dt² + a(t)²[dr²/(1-kr²) + r²dΩ²]",
                "latex": r"ds^2 = -dt^2 + a(t)^2\left[\frac{dr^2}{1-kr^2} + r^2 d\Omega^2\right]",
                "description": "Friedmann-Lemaître-Robertson-Walker metric for expanding universe. a(t) is scale factor, k is curvature."
            },
            {
                "name": "Inverse Metric Relation",
                "equation": "g^{μλ}g_{λν} = δ^μ_ν",
                "latex": r"g^{\mu\lambda}g_{\lambda\nu} = \delta^\mu_\nu",
                "description": "Inverse metric g^μν satisfies this relation (Kronecker delta on right side)."
            },
            {
                "name": "Index Raising",
                "equation": "V^μ = g^{μν} V_ν",
                "latex": r"V^\mu = g^{\mu\nu} V_\nu",
                "description": "Convert covariant vector to contravariant using inverse metric."
            },
            {
                "name": "Index Lowering",
                "equation": "V_μ = g_{μν} V^ν",
                "latex": r"V_\mu = g_{\mu\nu} V^\nu",
                "description": "Convert contravariant vector to covariant using metric."
            },
            {
                "name": "Proper Time",
                "equation": "dτ² = -ds²/c²",
                "latex": r"d\tau^2 = -\frac{ds^2}{c^2}",
                "description": "Proper time along timelike worldline. Time measured by a clock following the path."
            },
            {
                "name": "Christoffel Symbols",
                "equation": "Γ^λ_{μν} = ½ g^{λρ}(∂_μ g_{νρ} + ∂_ν g_{ρμ} - ∂_ρ g_{μν})",
                "latex": r"\Gamma^\lambda_{\mu\nu} = \frac{1}{2} g^{\lambda\rho}(\partial_\mu g_{\nu\rho} + \partial_\nu g_{\rho\mu} - \partial_\rho g_{\mu\nu})",
                "description": "Connection coefficients derived from metric. Describe parallel transport and geodesics."
            },
            {
                "name": "Volume Element",
                "equation": "d^4x √|g|",
                "latex": r"d^4x \sqrt{|g|}",
                "description": "Invariant volume element in curved spacetime. g = det(g_μν)."
            },
            {
                "name": "Riemann Curvature Tensor (from metric)",
                "equation": "R^ρ_{σμν} = ∂_μ Γ^ρ_{νσ} - ∂_ν Γ^ρ_{μσ} + Γ^ρ_{μλ}Γ^λ_{νσ} - Γ^ρ_{νλ}Γ^λ_{μσ}",
                "latex": r"R^\rho_{\sigma\mu\nu} = \partial_\mu \Gamma^\rho_{\nu\sigma} - \partial_\nu \Gamma^\rho_{\mu\sigma} + \Gamma^\rho_{\mu\lambda}\Gamma^\lambda_{\nu\sigma} - \Gamma^\rho_{\nu\lambda}\Gamma^\lambda_{\mu\sigma}",
                "description": "Full curvature tensor derived from Christoffel symbols (and thus from metric)."
            }
        ]
    }
}


def get_foundation_data(foundation_id):
    """
    Retrieve foundation data by ID.

    Args:
        foundation_id (str): The foundation identifier

    Returns:
        dict: Foundation data dictionary, or None if not found
    """
    return FOUNDATIONS_BATCH3.get(foundation_id)


def get_all_foundation_ids():
    """
    Get list of all foundation IDs in this batch.

    Returns:
        list: List of foundation ID strings
    """
    return list(FOUNDATIONS_BATCH3.keys())


def get_foundations_by_category(category):
    """
    Get all foundations in a specific category.

    Args:
        category (str): Category name

    Returns:
        list: List of foundation data dictionaries
    """
    return [
        data for data in FOUNDATIONS_BATCH3.values()
        if data.get("category") == category
    ]


def get_foundations_by_year_range(start_year, end_year):
    """
    Get foundations established within a year range.

    Args:
        start_year (int): Start year (inclusive)
        end_year (int): End year (inclusive)

    Returns:
        list: List of foundation data dictionaries
    """
    return [
        data for data in FOUNDATIONS_BATCH3.values()
        if start_year <= data.get("year_established", 0) <= end_year
    ]


if __name__ == "__main__":
    # Example usage and validation
    print("Foundation Data Batch 3 - Summary")
    print("=" * 60)
    print(f"\nTotal foundations in batch: {len(FOUNDATIONS_BATCH3)}")
    print("\nFoundations included:")

    for fid, fdata in FOUNDATIONS_BATCH3.items():
        print(f"\n  {fid}:")
        print(f"    Title: {fdata['title']}")
        print(f"    Year: {fdata['year_established']}")
        print(f"    Category: {fdata['category']}")
        print(f"    Formulas: {len(fdata['formulas'])}")
        print(f"    Properties: {len(fdata['key_properties'])}")

    print("\n" + "=" * 60)
    print("\nCategories represented:")
    categories = set(f["category"] for f in FOUNDATIONS_BATCH3.values())
    for cat in sorted(categories):
        count = len(get_foundations_by_category(cat))
        print(f"  - {cat}: {count} foundation(s)")

    print("\n" + "=" * 60)
    print("\nYear range: {} - {}".format(
        min(f["year_established"] for f in FOUNDATIONS_BATCH3.values()),
        max(f["year_established"] for f in FOUNDATIONS_BATCH3.values())
    ))

    print("\n" + "=" * 60)
    print("\nTotal formulas extracted:",
          sum(len(f["formulas"]) for f in FOUNDATIONS_BATCH3.values()))

    print("\n✓ Foundation data batch 3 ready for migration to theory_output.json")
