"""
Foundation Data Batch 2: Dirac Spinor, Einstein Field Equations, Einstein-Hilbert Action, G₂ Manifolds

Extracted from foundation HTML files for migration to theory_output.json
"""

FOUNDATIONS_BATCH2 = {
    "dirac-spinor": {
        "id": "dirac-spinor",
        "title": "Dirac Spinors",
        "category": "quantum_field_theory",
        "year_established": 1928,
        "badge_type": "established",
        "main_equation": "ψ = (ψ₁, ψ₂, ψ₃, ψ₄)ᵀ",
        "main_equation_latex": r"\psi = \begin{pmatrix} \psi_1 \\ \psi_2 \\ \psi_3 \\ \psi_4 \end{pmatrix}",
        "summary": "The mathematical objects that describe fermions with spin-1/2 in relativistic quantum mechanics, transforming under Lorentz symmetry in a unique double-valued way.",
        "key_properties": [
            "4-component complex column vector in C⁴ space",
            "Transform under spinor representation of Lorentz group",
            "Change sign under 360° rotation, return to original after 720°",
            "Decompose into left-handed and right-handed Weyl spinors",
            "Double-valued representation: Spin(3,1) → SO(3,1) is 2-to-1 map",
            "Arise from Clifford algebra Cl(3,1) representation"
        ],
        "pm_connection": "In PM, the Pneuma field ΨₚƖ is fundamentally a spinor field in higher dimensions. The framework emphasizes fermionic primacy: spinors are the fundamental entities, and bosonic fields emerge from spinor bilinears. After dimensional reduction from 26D bulk (signature 24,2), the Pneuma field becomes a 64-component spinor in the 13D shadow manifold (signature 12,1). The metric tensor emerges from spinor bivector condensates: g_MN ~ ⟨Ψ̄ₚ Γ_(MN) Ψₚ⟩.",
        "formulas": [
            {
                "id": "dirac-spinor-main",
                "latex": r"\psi = \begin{pmatrix} \psi_1 \\ \psi_2 \\ \psi_3 \\ \psi_4 \end{pmatrix}",
                "plaintext": "ψ = (ψ₁, ψ₂, ψ₃, ψ₄)ᵀ",
                "description": "4-component Dirac spinor - column vector in complex Hilbert space"
            },
            {
                "id": "weyl-decomposition",
                "latex": r"\psi = \begin{pmatrix} \psi_L \\ \psi_R \end{pmatrix}",
                "plaintext": "ψ = (ψ_L, ψ_R)ᵀ",
                "description": "Weyl decomposition into left-handed and right-handed components"
            },
            {
                "id": "chirality-projector-left",
                "latex": r"\psi_L = P_L \psi = \frac{1}{2}(1 - \gamma^5)\psi",
                "plaintext": "ψ_L = P_L ψ = (1/2)(1 - γ⁵)ψ",
                "description": "Left-handed chirality projector"
            },
            {
                "id": "chirality-projector-right",
                "latex": r"\psi_R = P_R \psi = \frac{1}{2}(1 + \gamma^5)\psi",
                "plaintext": "ψ_R = P_R ψ = (1/2)(1 + γ⁵)ψ",
                "description": "Right-handed chirality projector"
            },
            {
                "id": "lorentz-transformation",
                "latex": r"\psi(x) \to \psi'(x') = S(\Lambda)\psi(x)",
                "plaintext": "ψ(x) → ψ'(x') = S(Λ)ψ(x)",
                "description": "Spinor transformation under Lorentz transformation Λ"
            },
            {
                "id": "spin-rotation-matrix",
                "latex": r"S(\Lambda) = \exp\left(\frac{1}{4}\omega_{\mu\nu}\sigma^{\mu\nu}\right)",
                "plaintext": "S(Λ) = exp((1/4)ω_μν σ^μν)",
                "description": "Spin transformation matrix from gamma matrices"
            },
            {
                "id": "clifford-relation",
                "latex": r"\{\gamma^\mu, \gamma^\nu\} = 2\eta^{\mu\nu}",
                "plaintext": "{γ^μ, γ^ν} = 2η^μν",
                "description": "Clifford algebra relation for signature η = diag(+1,-1,-1,-1)"
            },
            {
                "id": "dirac-adjoint",
                "latex": r"\bar{\psi} = \psi^\dagger \gamma^0",
                "plaintext": "ψ̄ = ψ† γ⁰",
                "description": "Dirac adjoint (row vector)"
            },
            {
                "id": "spinor-dimension-formula",
                "latex": r"\text{dim}(\text{Spinor}) = 2^{\lfloor D/2 \rfloor}",
                "plaintext": "dim(Spinor) = 2^⌊D/2⌋",
                "description": "General spinor dimension formula for D-dimensional spacetime"
            },
            {
                "id": "pm-pneuma-spinor-64",
                "latex": r"\Psi_{P,\text{shadow}} \in \mathbb{C}^{64}",
                "plaintext": "Ψ_P,shadow ∈ C⁶⁴",
                "description": "PM Pneuma spinor: 64 components from Cl(12,1) in 13D shadow manifold"
            },
            {
                "id": "pm-metric-from-spinor",
                "latex": r"g_{MN} \sim \langle \bar{\Psi}_P \Gamma_{(MN)} \Psi_P \rangle",
                "plaintext": "g_MN ~ ⟨Ψ̄_P Γ_(MN) Ψ_P⟩",
                "description": "PM: Metric tensor emerges from spinor bivector condensate"
            }
        ]
    },

    "einstein-field-equations": {
        "id": "einstein-field-equations",
        "title": "Einstein Field Equations",
        "category": "gravity",
        "year_established": 1915,
        "badge_type": "established",
        "main_equation": "G_μν + Λg_μν = 8πG T_μν",
        "main_equation_latex": r"G_{\mu\nu} + \Lambda g_{\mu\nu} = 8\pi G T_{\mu\nu}",
        "summary": "The fundamental equations of General Relativity that describe how matter and energy curve spacetime, and how curved spacetime tells matter how to move.",
        "key_properties": [
            "Connects spacetime curvature (Einstein tensor G_μν) to matter/energy (stress-energy tensor T_μν)",
            "Diffeomorphism invariant (coordinate independent)",
            "Einstein tensor is divergence-free: ∇^μ G_μν = 0",
            "Reduces to Newton's law of gravity in weak-field, slow-velocity limit",
            "Contains cosmological constant Λ for dark energy",
            "10 independent components (4D symmetric tensor)"
        ],
        "pm_connection": "Principia Metaphysica extends Einstein's General Relativity to higher dimensions in the 2T physics framework. The Einstein Field Equations generalize to each dimensional stage: 26D bulk (24,2), 13D shadow (12,1), 6D bulk (5,1), and 4D observed (3,1). The G₂ compactification maintains Ricci-flatness through TCS gluing, with flux corrections modifying the effective geometry. The cosmological constant connects to PM's dark energy prediction w₀ = -1.0269.",
        "formulas": [
            {
                "id": "efe-main",
                "latex": r"G_{\mu\nu} + \Lambda g_{\mu\nu} = 8\pi G T_{\mu\nu}",
                "plaintext": "G_μν + Λg_μν = 8πG T_μν",
                "description": "Einstein Field Equations with cosmological constant"
            },
            {
                "id": "einstein-tensor",
                "latex": r"G_{\mu\nu} = R_{\mu\nu} - \frac{1}{2}Rg_{\mu\nu}",
                "plaintext": "G_μν = R_μν - (1/2)Rg_μν",
                "description": "Einstein tensor from Ricci tensor and Ricci scalar"
            },
            {
                "id": "line-element",
                "latex": r"ds^2 = g_{\mu\nu} dx^\mu dx^\nu",
                "plaintext": "ds² = g_μν dx^μ dx^ν",
                "description": "Spacetime interval (line element)"
            },
            {
                "id": "schwarzschild-metric",
                "latex": r"ds^2 = -\left(1 - \frac{2GM}{r}\right)dt^2 + \left(1 - \frac{2GM}{r}\right)^{-1}dr^2 + r^2 d\Omega^2",
                "plaintext": "ds² = -(1 - 2GM/r)dt² + (1 - 2GM/r)⁻¹dr² + r²dΩ²",
                "description": "Schwarzschild metric around spherical mass"
            },
            {
                "id": "pm-efe-26d",
                "latex": r"G_{AB} + \Lambda_{26} g_{AB} = 8\pi G_{26} T_{AB}",
                "plaintext": "G_AB + Λ_26 g_AB = 8πG_26 T_AB",
                "description": "PM: Einstein equations in 26D bulk with signature (24,2)"
            },
            {
                "id": "pm-efe-13d",
                "latex": r"G_{MN} + \Lambda_{13} g_{MN} = 8\pi G_{13} T_{MN}",
                "plaintext": "G_MN + Λ_13 g_MN = 8πG_13 T_MN",
                "description": "PM: Einstein equations in 13D shadow after Sp(2,R) gauge fixing"
            },
            {
                "id": "pm-g2-ricci-flat",
                "latex": r"\text{Ric}(g_{G_2}) = 0",
                "plaintext": "Ric(g_G₂) = 0",
                "description": "PM: G₂ manifold is Ricci-flat (satisfies vacuum Einstein equations)"
            },
            {
                "id": "pm-flux-corrected-efe",
                "latex": r"G_{\mu\nu} = 8\pi G\left(T_{\mu\nu} + T_{\mu\nu}^{\text{flux}}\right)",
                "plaintext": "G_μν = 8πG(T_μν + T_μν^flux)",
                "description": "PM: Flux corrections modify effective geometry"
            }
        ]
    },

    "einstein-hilbert-action": {
        "id": "einstein-hilbert-action",
        "title": "Einstein-Hilbert Action",
        "category": "gravity",
        "year_established": 1915,
        "badge_type": "established",
        "main_equation": "S = (1/16πG) ∫ d⁴x √|g| R",
        "main_equation_latex": r"S = \frac{1}{16\pi G} \int d^4x \sqrt{|g|} R",
        "summary": "The action principle from which Einstein's field equations of General Relativity are derived through variational calculus.",
        "key_properties": [
            "Variational principle: extremizing δS = 0 yields Einstein field equations",
            "Proportional to total curvature integrated over spacetime",
            "Coordinate invariant (diffeomorphism invariant)",
            "Factor 1/16πG ensures correct coupling strength",
            "√|g| ensures proper volume element in curved spacetime",
            "R = Ricci scalar measures total curvature"
        ],
        "pm_connection": "In Principia Metaphysica, the Einstein-Hilbert action generalizes to 26 dimensions with signature (24,2) in the 2T physics framework. The action undergoes dimensional reduction: 26D (24,2) bulk → 13D (12,1) shadow via Sp(2,R) gauge fixing → 6D bulk via G₂ compactification → 4D observed. The 4D Planck mass emerges from compactification: M_Pl² = M_*²⁴ × V_22, where V_22 is the 22-dimensional compact volume.",
        "formulas": [
            {
                "id": "eh-action-4d",
                "latex": r"S_{\text{EH}} = \frac{1}{16\pi G} \int d^4x \sqrt{|g|} R",
                "plaintext": "S_EH = (1/16πG) ∫ d⁴x √|g| R",
                "description": "4D Einstein-Hilbert action"
            },
            {
                "id": "pm-eh-action-26d",
                "latex": r"S_{26D} = M_*^{24} \int d^{26}X \sqrt{|G_{(24,2)}|} R_{26}",
                "plaintext": "S_26D = M_*²⁴ ∫ d²⁶X √|G_(24,2)| R_26",
                "description": "PM: 26D Einstein-Hilbert action with signature (24,2)"
            },
            {
                "id": "pm-eh-action-14x2",
                "latex": r"S_{14\times 2} = M_*^{24} \int \left[d^{14}x_1 \sqrt{|g_1|} R_{14,1} + d^{14}x_2 \sqrt{|g_2|} R_{14,2}\right]",
                "plaintext": "S_14×2 = M_*²⁴ ∫ [d¹⁴x₁ √|g₁| R_14,1 + d¹⁴x₂ √|g₂| R_14,2]",
                "description": "PM: After Sp(2,R) gauge fixing to dual 14D sectors"
            },
            {
                "id": "pm-eh-action-7x2",
                "latex": r"S_{7\times 2} = M_7^5 \int \left[d^7x_1 \sqrt{|h_1|} R_{7,1} + d^7x_2 \sqrt{|h_2|} R_{7,2}\right]",
                "plaintext": "S_7×2 = M_7⁵ ∫ [d⁷x₁ √|h₁| R_7,1 + d⁷x₂ √|h₂| R_7,2]",
                "description": "PM: After G₂ compactification to dual 7D sectors"
            },
            {
                "id": "pm-eh-action-4d",
                "latex": r"S_{4D} = M_{\text{Pl}}^2 \int d^4x \sqrt{|g|} R",
                "plaintext": "S_4D = M_Pl² ∫ d⁴x √|g| R",
                "description": "PM: 4D effective action after full compactification"
            },
            {
                "id": "pm-planck-mass-kk",
                "latex": r"M_{\text{Pl}}^2 = M_*^{24} \times V_{22}",
                "plaintext": "M_Pl² = M_*²⁴ × V_22",
                "description": "PM: 4D Planck mass from Kaluza-Klein compactification"
            },
            {
                "id": "pm-v22-volume",
                "latex": r"V_{22} = \text{Vol}(M_1^7) \times \text{Vol}(M_2^7) \times (\text{Sp}(2,\mathbb{R}) \text{ volume factor})",
                "plaintext": "V_22 = Vol(M₁⁷) × Vol(M₂⁷) × (Sp(2,R) volume factor)",
                "description": "PM: 22-dimensional compact volume"
            }
        ]
    },

    "g2-manifolds": {
        "id": "g2-manifolds",
        "title": "G₂ Manifolds",
        "category": "geometry",
        "year_established": 1987,
        "badge_type": "established",
        "main_equation": "dφ = 0 and d(*φ) = 0",
        "main_equation_latex": r"d\varphi = 0 \quad \text{and} \quad d(\star\varphi) = 0",
        "summary": "7-dimensional Riemannian manifolds with holonomy group G₂, the smallest exceptional Lie group. These manifolds are Ricci-flat and preserve N=1 supersymmetry in M-theory compactifications.",
        "key_properties": [
            "7-dimensional with holonomy group G₂ ⊂ SO(7)",
            "Ricci-flat: Ric(g) = 0 (satisfy vacuum Einstein equations)",
            "Exactly one parallel spinor (8 real components)",
            "Defined by associative 3-form φ satisfying dφ = 0 and d(*φ) = 0",
            "No complex structure (purely real geometry)",
            "Preserves N=1 supersymmetry in 4D after M-theory compactification",
            "Bare Euler characteristic χ(G₂) = 0 for smooth compact G₂ manifolds"
        ],
        "pm_connection": "In PM's 2T physics framework, the 13D shadow (from 26D bulk via Sp(2,R) gauge fixing) compactifies on a 7D G₂ manifold constructed via Twisted Connected Sum (TCS). The specific construction uses extra-twisted TCS with involution blocks 3.25₁ and 3.25₂, gluing angle θ = π/6, yielding Betti numbers b₂ = 4, b₃ = 24. G₄ flux backreaction modifies bare topology χ = 0 to effective χ_eff = 72 per G₂ copy, giving 3 fermion generations via n_gen = χ_eff/24 = 3. D₅ ADE singularities provide SO(10) GUT gauge group. The GUT scale M_GUT = 2.118×10¹⁶ GeV emerges topologically via logarithmic torsion formula. Total internal space: V₉ = V₇(G₂) × V₂(T²).",
        "formulas": [
            {
                "id": "g2-defining-equations",
                "latex": r"d\varphi = 0 \quad \text{and} \quad d(\star\varphi) = 0",
                "plaintext": "dφ = 0 and d(*φ) = 0",
                "description": "Defining equations for torsion-free G₂ structure"
            },
            {
                "id": "g2-ricci-flat",
                "latex": r"\text{Ric}(g) = 0",
                "plaintext": "Ric(g) = 0",
                "description": "G₂ manifolds are Ricci-flat"
            },
            {
                "id": "g2-parallel-spinor",
                "latex": r"\nabla \eta = 0",
                "plaintext": "∇η = 0",
                "description": "Unique parallel spinor η (8 real components)"
            },
            {
                "id": "pm-g2-tcs",
                "latex": r"M^7 = M_1^7 \cup_{S^3 \times S^1} M_2^7",
                "plaintext": "M⁷ = M₁⁷ ∪_S³×S¹ M₂⁷",
                "description": "PM: Twisted Connected Sum construction"
            },
            {
                "id": "pm-g2-bare-euler",
                "latex": r"\chi(M^7) = 0",
                "plaintext": "χ(M⁷) = 0",
                "description": "PM: Bare Euler characteristic (before flux)"
            },
            {
                "id": "pm-g2-flux-dressed-euler",
                "latex": r"\chi_{\text{eff}}(M^7) = 72",
                "plaintext": "χ_eff(M⁷) = 72",
                "description": "PM: Flux-dressed effective Euler characteristic per G₂ copy"
            },
            {
                "id": "pm-g2-generation-count",
                "latex": r"n_{\text{gen}} = \frac{\chi_{\text{eff}}}{24} = \frac{72}{24} = 3",
                "plaintext": "n_gen = χ_eff/24 = 72/24 = 3",
                "description": "PM: 3 fermion generations from flux-dressed topology"
            },
            {
                "id": "pm-g2-total-euler",
                "latex": r"\chi_{\text{total}} = 144",
                "plaintext": "χ_total = 144",
                "description": "PM: Total Euler characteristic from dual G₂ pair"
            },
            {
                "id": "pm-g2-betti-2",
                "latex": r"b_2(M) = 4",
                "plaintext": "b₂(M) = 4",
                "description": "PM: Second Betti number (associative 3-cycles)"
            },
            {
                "id": "pm-g2-betti-3",
                "latex": r"b_3(M) = 24",
                "plaintext": "b₃(M) = 24",
                "description": "PM: Third Betti number (coassociative 4-cycles)"
            },
            {
                "id": "pm-g2-torsion-invariant",
                "latex": r"\nu = 24",
                "plaintext": "ν = 24",
                "description": "PM: Crowley-Nordenstam torsion invariant mod 48"
            },
            {
                "id": "pm-g2-gut-scale-formula",
                "latex": r"\ln\left(\frac{M_{\text{GUT}}}{M_{\text{Planck}}}\right) = -2\pi \frac{b_2 + b_3}{\nu}",
                "plaintext": "ln(M_GUT/M_Planck) = -2π(b₂ + b₃)/ν",
                "description": "PM: Torsion logarithm formula for GUT scale"
            },
            {
                "id": "pm-g2-gut-scale-value",
                "latex": r"M_{\text{GUT}} = M_{\text{Planck}} \times e^{-7.33} = 2.118 \times 10^{16} \text{ GeV}",
                "plaintext": "M_GUT = M_Planck × e^(-7.33) = 2.118×10¹⁶ GeV",
                "description": "PM: GUT scale from torsion topology"
            },
            {
                "id": "pm-g2-v9-volume",
                "latex": r"V_9 = V_7(G_2) \times V_2(T^2)",
                "plaintext": "V₉ = V₇(G₂) × V₂(T²)",
                "description": "PM: 9D internal volume factorization"
            },
            {
                "id": "pm-g2-susy-preservation",
                "latex": r"\text{Hol}(g) \subseteq G_2 \quad \Rightarrow \quad N=1 \text{ SUSY preserved}",
                "plaintext": "Hol(g) ⊆ G₂ → N=1 SUSY preserved",
                "description": "PM: G₂ holonomy preserves N=1 supersymmetry in 4D"
            },
            {
                "id": "pm-g2-flux-quantization",
                "latex": r"\int_{\Sigma_4} \frac{G_4}{2\pi \ell_P^3} \in \mathbb{Z}",
                "plaintext": "∫_Σ₄ G₄/(2πℓ_P³) ∈ ℤ",
                "description": "PM: G₄ flux quantization condition"
            },
            {
                "id": "pm-g2-dimensional-reduction",
                "latex": r"26D(24,2) \xrightarrow{\text{Sp}(2,\mathbb{R})} 14D_1(12,2) \otimes 14D_2(12,2) \xrightarrow{G_2} 7D_1 \otimes 7D_2 \xrightarrow{\text{shared time}} 4D(3,1)",
                "plaintext": "26D(24,2) --[Sp(2,R)]--> 14D₁(12,2)⊗14D₂(12,2) --[G₂]--> 7D₁⊗7D₂ --[shared time]--> 4D(3,1)",
                "description": "PM: Full dimensional reduction pathway in 2T framework"
            }
        ]
    }
}
