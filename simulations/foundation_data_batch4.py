"""
Foundation Data Batch 4 - Extracted from HTML files
Generated: 2025-12-26

Contains structured data for:
- ricci-tensor
- so10-gut
- unruh-effect
- yang-mills
- tomita-takesaki
"""

FOUNDATIONS_BATCH4 = {
    "ricci-tensor": {
        "id": "ricci-tensor",
        "title": "Ricci Tensor & Ricci Scalar",
        "category": "Established Mathematics",
        "year_established": "1854-1903",
        "badge_type": "established",
        "main_equation": "R_μν = R^λ_μλν | R = g^μν R_μν",
        "main_equation_latex": r"R_{\mu\nu} = R^{\lambda}_{\mu\lambda\nu} \quad | \quad R = g^{\mu\nu} R_{\mu\nu}",
        "summary": "The fundamental measures of spacetime curvature that describe how matter and energy bend space, forming the building blocks of Einstein's field equations.",
        "key_properties": [
            "Riemann tensor has 20 independent components in 4D spacetime",
            "Ricci tensor is a contraction of the Riemann tensor with 10 independent components",
            "Ricci scalar is the trace of the Ricci tensor - single number measuring total curvature",
            "Measures volume distortion: geodesic deviation and focusing of geodesics",
            "Appears in Einstein-Hilbert action as fundamental curvature invariant",
            "Symmetric tensor: R_μν = R_νμ",
            "Connected to stress-energy tensor via Einstein field equations"
        ],
        "pm_connection": "In Principia Metaphysica's 2T physics framework, the Ricci tensor and scalar generalize to higher dimensions during the dimensional reduction cascade (26D → 13D → 6D → 4D). The Ricci curvature describes how matter/energy curves space at each dimensional level, with G₂ compactification and Kaluza-Klein modes contributing to the effective 4D curvature.",
        "formulas": [
            {
                "symbol": "R^ρ_σμν",
                "name": "Riemann Curvature Tensor",
                "latex": r"R^{\rho}_{\sigma\mu\nu} = \partial_{\mu}\Gamma^{\rho}_{\nu\sigma} - \partial_{\nu}\Gamma^{\rho}_{\mu\sigma} + \Gamma^{\rho}_{\mu\lambda}\Gamma^{\lambda}_{\nu\sigma} - \Gamma^{\rho}_{\nu\lambda}\Gamma^{\lambda}_{\mu\sigma}",
                "description": "The fundamental measure of spacetime curvature - measures how vectors change when parallel transported around closed loops"
            },
            {
                "symbol": "R_μν",
                "name": "Ricci Tensor",
                "latex": r"R_{\mu\nu} = R^{\lambda}_{\mu\lambda\nu}",
                "description": "Contraction of Riemann tensor measuring volume distortion in curved space"
            },
            {
                "symbol": "R",
                "name": "Ricci Scalar",
                "latex": r"R = g^{\mu\nu} R_{\mu\nu}",
                "description": "Trace of Ricci tensor - single number measuring total average curvature at a point"
            },
            {
                "symbol": "Γ^λ_μν",
                "name": "Christoffel Symbols",
                "latex": r"\Gamma^{\lambda}_{\mu\nu} = \frac{1}{2} g^{\lambda\rho}(\partial_{\mu}g_{\nu\rho} + \partial_{\nu}g_{\rho\mu} - \partial_{\rho}g_{\mu\nu})",
                "description": "Connection coefficients describing how basis vectors change in curved spacetime"
            },
            {
                "symbol": "G_μν",
                "name": "Einstein Tensor",
                "latex": r"G_{\mu\nu} = R_{\mu\nu} - \frac{1}{2}Rg_{\mu\nu}",
                "description": "Automatically divergence-free combination used in Einstein field equations"
            },
            {
                "symbol": "d²V/dτ²",
                "name": "Raychaudhuri Equation",
                "latex": r"\frac{d^2 V}{d\tau^2} = -R_{\mu\nu} u^{\mu} u^{\nu} V",
                "description": "Describes evolution of volume for geodesic congruences - shows how Ricci tensor controls focusing"
            }
        ]
    },

    "so10-gut": {
        "id": "so10-gut",
        "title": "SO(10) Grand Unified Theory",
        "category": "Theoretical Physics",
        "year_established": "1974",
        "badge_type": "theoretical",
        "main_equation": "SO(10) ⊃ SU(3) × SU(2) × U(1)",
        "main_equation_latex": r"\text{SO}(10) \supset \text{SU}(3) \times \text{SU}(2) \times \text{U}(1)",
        "summary": "The most elegant grand unification: all Standard Model forces and one generation of matter (including the right-handed neutrino) fit into a single 16-dimensional spinor representation.",
        "key_properties": [
            "16-dimensional spinor contains exactly one generation of fermions plus right-handed neutrino",
            "45 gauge bosons in adjoint representation (12 SM + 33 new X,Y bosons)",
            "Gauge coupling unification at M_GUT ≈ 2.118 × 10^16 GeV",
            "Predicts proton decay: p → e⁺π⁰ with lifetime τ_p ≈ 4.09 × 10^34 years",
            "Explains charge quantization automatically via group structure",
            "Seesaw mechanism naturally explains tiny neutrino masses",
            "Three generations require three copies of 16-plet"
        ],
        "pm_connection": "In Principia Metaphysica, SO(10) emerges from G₂ compactification on associative cycles (b₂=4) via D5-brane wrapping. The effective Euler characteristic χ_eff = 144 = 3 × 48 provides topological origin for three generations. The 64-component 13D spinor decomposes as 16_SO(10) × 4_internal, connecting grand unification to fundamental spinor structure.",
        "formulas": [
            {
                "symbol": "16",
                "name": "Spinor Representation",
                "latex": r"16 = u_{R,G,B}, d_{R,G,B}, Q_L, e_L, e_R, \nu_L, \nu_R",
                "description": "Minimal spinor representation containing all fermions of one generation"
            },
            {
                "symbol": "45",
                "name": "Gauge Bosons",
                "latex": r"\dim(\text{SO}(10)) = \frac{10 \times 9}{2} = 45",
                "description": "Adjoint representation: 12 SM gauge bosons + 33 X,Y bosons mediating proton decay"
            },
            {
                "symbol": "M_GUT",
                "name": "GUT Scale",
                "latex": r"M_{\text{GUT}} = 2.118 \times 10^{16} \text{ GeV}",
                "description": "Energy scale where three SM coupling constants unify"
            },
            {
                "symbol": "α_GUT",
                "name": "Unified Coupling",
                "latex": r"\alpha_1(M_{\text{GUT}}) = \alpha_2(M_{\text{GUT}}) = \alpha_3(M_{\text{GUT}})",
                "description": "Running coupling constants converge at GUT scale"
            },
            {
                "symbol": "m_ν",
                "name": "Seesaw Mechanism",
                "latex": r"m_{\nu} \sim \frac{m_D^2}{M_R}",
                "description": "Type-I seesaw formula explaining tiny neutrino masses via heavy right-handed neutrinos"
            },
            {
                "symbol": "τ_p",
                "name": "Proton Lifetime",
                "latex": r"\tau_p = 4.09 \times 10^{34} \text{ years}",
                "description": "PM prediction for proton decay lifetime via X,Y boson exchange"
            },
            {
                "symbol": "χ_eff",
                "name": "Three Generations",
                "latex": r"\chi_{\text{eff}} = 144 = 3 \times 48 = 3 \times (16 + \bar{16} + 16_{\text{vector}})",
                "description": "Topological explanation for three generations from G₂ Euler characteristic"
            }
        ]
    },

    "unruh-effect": {
        "id": "unruh-effect",
        "title": "Unruh Effect",
        "category": "Established Physics",
        "year_established": "1976",
        "badge_type": "established",
        "main_equation": "T_U = ℏa / (2πck_B)",
        "main_equation_latex": r"T_U = \frac{\hbar a}{2\pi c k_B}",
        "summary": "Accelerated observers perceive the quantum vacuum as a thermal bath, revealing the profound observer-dependence of temperature and particles in quantum field theory.",
        "key_properties": [
            "Uniformly accelerated observers detect thermal radiation in Minkowski vacuum",
            "Temperature proportional to proper acceleration: T ∝ a",
            "Rindler horizon at distance c²/a behind accelerated observer",
            "Particle content is observer-dependent (vacuum for inertial, thermal for accelerated)",
            "Related to Hawking radiation via equivalence principle",
            "KMS condition characterizes thermal equilibrium state",
            "Earth surface acceleration gives T_U ≈ 4 × 10^-20 K (unobservably small)"
        ],
        "pm_connection": "The Unruh effect demonstrates observer-dependent temperature crucial to PM's thermal time hypothesis. In the dimensional cascade (26D → 13D → 6D → 4D), each transition induces effective 'acceleration' in compactified dimensions, generating thermal radiation. Temperature emerges from the observer's relationship to the Pneuma field state via modular flow.",
        "formulas": [
            {
                "symbol": "T_U",
                "name": "Unruh Temperature",
                "latex": r"T_U = \frac{\hbar a}{2\pi c k_B}",
                "description": "Temperature measured by observer with proper acceleration a"
            },
            {
                "symbol": "a",
                "name": "Proper Acceleration",
                "latex": r"a",
                "description": "Acceleration in observer's own reference frame (m/s²)"
            },
            {
                "symbol": "β_U",
                "name": "Inverse Temperature",
                "latex": r"\beta_U = \frac{2\pi c}{a} = \frac{1}{k_B T_U}",
                "description": "Inverse Unruh temperature from modular flow period"
            },
            {
                "symbol": "ρ,η",
                "name": "Rindler Coordinates",
                "latex": r"t = \frac{\rho}{a}\sinh(a\eta), \quad x = \frac{\rho}{a}\cosh(a\eta)",
                "description": "Coordinate system adapted to uniformly accelerated observer"
            },
            {
                "symbol": "ds²_R",
                "name": "Rindler Metric",
                "latex": r"ds^2 = -(a\rho)^2 d\eta^2 + d\rho^2 + dy^2 + dz^2",
                "description": "Metric in Rindler coordinates (looks like gravitational field)"
            },
            {
                "symbol": "ρ_R",
                "name": "Thermal State",
                "latex": r"\rho_R = Z^{-1} \exp(-2\pi\omega H_R/a)",
                "description": "Minkowski vacuum appears as thermal state to Rindler observer"
            },
            {
                "symbol": "κ",
                "name": "Surface Gravity",
                "latex": r"\kappa = a \quad \text{(Rindler)}, \quad \kappa = \frac{c^4}{4GM} \quad \text{(Schwarzschild)}",
                "description": "Effective surface gravity of horizon - determines temperature"
            }
        ]
    },

    "yang-mills": {
        "id": "yang-mills",
        "title": "Yang-Mills Theory",
        "category": "Established Physics",
        "year_established": "1954",
        "badge_type": "established",
        "main_equation": "ℒ = -¼ F^a_μν F^aμν",
        "main_equation_latex": r"\mathcal{L} = -\frac{1}{4} F^a_{\mu\nu} F^{a\mu\nu}",
        "summary": "The foundation of modern particle physics: a non-abelian gauge theory that underlies the strong and electroweak forces of the Standard Model.",
        "key_properties": [
            "Non-abelian gauge symmetry: transformations don't commute",
            "Gauge bosons carry charge and self-interact (unlike photons)",
            "Structure constants f^abc define Lie algebra: [T^a, T^b] = if^abc T^c",
            "Field strength includes self-interaction: F^a_μν = ∂_μA^a_ν - ∂_νA^a_μ - gf^abc A^b_μ A^c_ν",
            "3-gluon and 4-gluon vertices arise from non-abelian structure",
            "Asymptotic freedom: coupling decreases at high energies",
            "Confinement at low energies: only color-neutral states observed"
        ],
        "pm_connection": "Yang-Mills gauge fields emerge from 26D bulk theory via dimensional reduction. SO(10) GUT gauge symmetry arises from D5-branes wrapping b₂=4 associative 3-cycles in the G₂ manifold. The bulk 26D Yang-Mills action reduces to Standard Model SU(3)×SU(2)×U(1) after compactification and symmetry breaking, with gauge couplings unifying at M_GUT.",
        "formulas": [
            {
                "symbol": "F^a_μν",
                "name": "Field Strength Tensor",
                "latex": r"F^a_{\mu\nu} = \partial_{\mu}A^a_{\nu} - \partial_{\nu}A^a_{\mu} - gf^{abc}A^b_{\mu}A^c_{\nu}",
                "description": "Non-abelian field strength - distinguishes from Maxwell theory via gf^abc term"
            },
            {
                "symbol": "A^a_μ",
                "name": "Gauge Fields",
                "latex": r"A^a_{\mu}",
                "description": "Vector potentials in adjoint representation: 8 gluons (SU(3)), 3 weak bosons (SU(2)), 1 photon (U(1))"
            },
            {
                "symbol": "f^abc",
                "name": "Structure Constants",
                "latex": r"[T^a, T^b] = if^{abc}T^c",
                "description": "Define Lie algebra commutation relations - completely antisymmetric"
            },
            {
                "symbol": "D_μ",
                "name": "Covariant Derivative",
                "latex": r"D_{\mu} = \partial_{\mu} + igA^a_{\mu}T^a",
                "description": "Ensures gauge covariance of fermion kinetic terms"
            },
            {
                "symbol": "α_s(μ)",
                "name": "Running Coupling",
                "latex": r"\alpha_s(\mu) = \frac{\alpha_s(\mu_0)}{1 + \alpha_s(\mu_0)b\ln(\mu/\mu_0)}",
                "description": "QCD coupling constant evolution - asymptotic freedom when b > 0"
            },
            {
                "symbol": "ℒ_YM",
                "name": "Yang-Mills Lagrangian",
                "latex": r"\mathcal{L}_{\text{YM}} = -\frac{1}{4} F^a_{\mu\nu} F^{a\mu\nu} + \bar{\psi}(i\gamma^{\mu}D_{\mu} - m)\psi",
                "description": "Full Yang-Mills Lagrangian with gauge fields and matter"
            },
            {
                "symbol": "N²-1",
                "name": "Number of Gluons",
                "latex": r"\dim(\text{SU}(N)) = N^2 - 1",
                "description": "Dimension of Lie algebra: 8 for SU(3), 3 for SU(2)"
            }
        ]
    },

    "tomita-takesaki": {
        "id": "tomita-takesaki",
        "title": "Tomita-Takesaki Theory",
        "category": "Established Mathematics",
        "year_established": "1970",
        "badge_type": "established",
        "main_equation": "σ_t(A) = Δ^it A Δ^-it",
        "main_equation_latex": r"\sigma_t(A) = \Delta^{it} A \Delta^{-it}",
        "summary": "Modular automorphism group and the profound connection between quantum states and intrinsic time evolution in von Neumann algebras.",
        "key_properties": [
            "Every faithful normal state naturally defines modular flow σ_t",
            "Modular operator Δ = S*S is positive self-adjoint",
            "Modular conjugation J exchanges algebra with commutant: JMJ = M'",
            "State becomes KMS thermal state with respect to modular flow",
            "Tomita operator S: AΩ ↦ A*Ω is anti-linear and closed",
            "Modular Hamiltonian K = -log(Δ) generates time evolution",
            "Thermal time hypothesis: physical time emerges from modular flow"
        ],
        "pm_connection": "Tomita-Takesaki theory is central to PM's thermal time hypothesis. Time at each dimensional level (26D → 13D → 6D → 4D) emerges from modular flow of the Pneuma field state. The observable algebras form type III factors, with modular automorphisms generating intrinsic dynamics and thermodynamic behavior from the KMS condition.",
        "formulas": [
            {
                "symbol": "S",
                "name": "Tomita Operator",
                "latex": r"S(A\Omega) = A^*\Omega \quad \text{for } A \in M",
                "description": "Anti-linear closed operator encoding relation between operator and its adjoint"
            },
            {
                "symbol": "Δ",
                "name": "Modular Operator",
                "latex": r"\Delta = S^*S = J\Delta^{1/2}",
                "description": "Positive self-adjoint operator generating modular automorphisms"
            },
            {
                "symbol": "J",
                "name": "Modular Conjugation",
                "latex": r"J = S\Delta^{-1/2}, \quad JMJ = M'",
                "description": "Anti-unitary operator from polar decomposition - exchanges algebra with commutant"
            },
            {
                "symbol": "σ_t",
                "name": "Modular Automorphism Group",
                "latex": r"\sigma_t(A) = \Delta^{it} A \Delta^{-it}",
                "description": "One-parameter group of *-automorphisms representing intrinsic time evolution"
            },
            {
                "symbol": "Ω",
                "name": "Cyclic and Separating Vector",
                "latex": r"\{A\Omega | A \in M\} \text{ dense}, \quad A\Omega = 0 \Rightarrow A = 0",
                "description": "GNS vector representing the state - both cyclic and separating"
            },
            {
                "symbol": "KMS",
                "name": "KMS Condition",
                "latex": r"\omega(AB) = \omega(B\sigma_{i\beta}(A))",
                "description": "Thermal equilibrium condition at inverse temperature β with respect to modular flow"
            },
            {
                "symbol": "K",
                "name": "Modular Hamiltonian",
                "latex": r"K = -\log(\Delta), \quad \sigma_t(A) = e^{itK} A e^{-itK}",
                "description": "Natural notion of energy generating modular time evolution"
            },
            {
                "symbol": "(M,H,J,P_+)",
                "name": "Standard Form",
                "latex": r"P_+ = \{A\Omega | A \geq 0, A \in M\}, \quad JP_+ = P_+",
                "description": "Canonical representation with natural positive self-dual cone"
            }
        ]
    }
}
