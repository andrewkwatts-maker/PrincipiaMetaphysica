/**
 * Centralized Formula Definitions for Principia Metaphysica v6.0
 * "Temporal Mirrors" - 26D Two-Time Framework
 *
 * STRUCTURE:
 * - ESTABLISHED: Well-known physics formulas with citations
 * - THEORY: New formulas specific to Principia Metaphysica
 * - DERIVED: Results derived from the theory
 * - PREDICTIONS: Testable predictions
 *
 * Each formula has:
 * - id: Unique identifier for referencing
 * - html: HTML-safe equation string
 * - latex: LaTeX version (for future use)
 * - label: Equation number and name
 * - category: ESTABLISHED | THEORY | DERIVED | PREDICTION
 * - description: Plain English explanation
 * - attribution: Source/citation
 * - terms: Object mapping symbols to descriptions
 * - status: Current validation status
 *
 * VERSION 6.0 CHANGES:
 * - Extended from 13D to 26D with signature (24,2)
 * - Two time dimensions: t_therm (thermal) + t_ortho (orthogonal)
 * - Z₂ mirror brane structure: B¹_{1:4} ↔ B²_{1:4}
 * - Sp(2,R) gauge symmetry for ghost elimination
 * - Observable 13D is gauge-fixed shadow of 26D
 */

const PrincipiaFormulas = {

    // ================================================================
    // ESTABLISHED PHYSICS - Well-known formulas from standard physics
    // ================================================================

    ESTABLISHED: {

        // --- General Relativity ---

        einsteinFieldEquations: {
            id: "einstein-field",
            html: "R<sub>μν</sub> - ½g<sub>μν</sub>R + Λg<sub>μν</sub> = 8πGT<sub>μν</sub>",
            latex: "R_{\\mu\\nu} - \\frac{1}{2}g_{\\mu\\nu}R + \\Lambda g_{\\mu\\nu} = 8\\pi G T_{\\mu\\nu}",
            label: "Einstein Field Equations",
            category: "ESTABLISHED",
            attribution: "[Einstein 1915]",
            description: "Relates spacetime curvature to energy-momentum content",
            terms: {
                "R<sub>μν</sub>": { name: "Ricci Tensor", description: "Curvature contraction" },
                "g<sub>μν</sub>": { name: "Metric Tensor", description: "Spacetime geometry" },
                "R": { name: "Ricci Scalar", description: "Scalar curvature" },
                "Λ": { name: "Cosmological Constant", description: "Vacuum energy density" },
                "T<sub>μν</sub>": { name: "Stress-Energy Tensor", description: "Matter/energy content" }
            }
        },

        einsteinHilbertAction: {
            id: "einstein-hilbert",
            html: "S<sub>EH</sub> = (1/16πG) ∫ d<sup>4</sup>x √(-g) R",
            latex: "S_{EH} = \\frac{1}{16\\pi G} \\int d^4x \\sqrt{-g} R",
            label: "Einstein-Hilbert Action",
            category: "ESTABLISHED",
            attribution: "[Hilbert 1915]",
            description: "Action principle for general relativity",
            terms: {
                "S<sub>EH</sub>": { name: "Einstein-Hilbert Action", description: "Gravitational action" },
                "G": { name: "Newton's Constant", description: "G = 6.67 × 10⁻¹¹ m³/(kg·s²)" },
                "√(-g)": { name: "Metric Determinant", description: "Coordinate invariant volume" },
                "R": { name: "Ricci Scalar", description: "Spacetime curvature" }
            }
        },

        friedmannEquation: {
            id: "friedmann",
            html: "H² = (8πG/3)(ρ<sub>m</sub> + ρ<sub>r</sub> + ρ<sub>Λ</sub>) - k/a²",
            latex: "H^2 = \\frac{8\\pi G}{3}(\\rho_m + \\rho_r + \\rho_\\Lambda) - \\frac{k}{a^2}",
            label: "Friedmann Equation",
            category: "ESTABLISHED",
            attribution: "[Friedmann 1922]",
            description: "Governs expansion rate of the universe",
            terms: {
                "H": { name: "Hubble Parameter", description: "H = ȧ/a ≈ 67.4 km/s/Mpc" },
                "ρ<sub>m</sub>": { name: "Matter Density", description: "Dark + baryonic matter" },
                "ρ<sub>r</sub>": { name: "Radiation Density", description: "Photons + relativistic particles" },
                "ρ<sub>Λ</sub>": { name: "Dark Energy Density", description: "Vacuum/cosmological constant" },
                "k": { name: "Spatial Curvature", description: "k = 0, ±1" },
                "a": { name: "Scale Factor", description: "Cosmic expansion factor" }
            }
        },

        wheelerDeWitt: {
            id: "wheeler-dewitt",
            html: "HΨ[g<sub>ab</sub>] = 0",
            latex: "\\hat{H}\\Psi[g_{ab}] = 0",
            label: "(5.1) Wheeler-DeWitt Equation",
            category: "ESTABLISHED",
            attribution: "[DeWitt 1967, Wheeler 1968]",
            description: "Fundamental equation of quantum gravity - time disappears",
            terms: {
                "H": { name: "Hamiltonian Constraint", description: "Wheeler-DeWitt Hamiltonian" },
                "Ψ[g<sub>ab</sub>]": { name: "Wave Function", description: "Functional of 3-geometries" },
                "0": { name: "Zero Energy", description: "Total energy of closed universe is zero" }
            }
        },

        // --- Quantum Field Theory ---

        diracEquation: {
            id: "dirac",
            html: "(iγ<sup>μ</sup>∂<sub>μ</sub> - m)ψ = 0",
            latex: "(i\\gamma^\\mu \\partial_\\mu - m)\\psi = 0",
            label: "Dirac Equation",
            category: "ESTABLISHED",
            attribution: "[Dirac 1928]",
            description: "Relativistic wave equation for spin-1/2 particles",
            terms: {
                "γ<sup>μ</sup>": { name: "Gamma Matrices", description: "4×4 Dirac matrices" },
                "∂<sub>μ</sub>": { name: "Partial Derivative", description: "Spacetime derivative" },
                "m": { name: "Mass", description: "Particle rest mass" },
                "ψ": { name: "Dirac Spinor", description: "4-component spinor field" }
            }
        },

        cliffordAlgebra: {
            id: "clifford",
            html: "{γ<sup>μ</sup>, γ<sup>ν</sup>} = 2η<sup>μν</sup>",
            latex: "\\{\\gamma^\\mu, \\gamma^\\nu\\} = 2\\eta^{\\mu\\nu}",
            label: "Clifford Algebra",
            category: "ESTABLISHED",
            attribution: "[Clifford 1878]",
            description: "Anticommutation relation defining gamma matrices",
            terms: {
                "{,}": { name: "Anticommutator", description: "AB + BA" },
                "η<sup>μν</sup>": { name: "Minkowski Metric", description: "diag(-1,+1,+1,+1)" }
            }
        },

        // --- Statistical Mechanics ---

        kmsCondition: {
            id: "kms",
            html: "⟨A σ<sub>t</sub>(B)⟩ = ⟨B σ<sub>t+iβ</sub>(A)⟩",
            latex: "\\langle A \\sigma_t(B) \\rangle = \\langle B \\sigma_{t+i\\beta}(A) \\rangle",
            label: "(5.4) KMS Condition",
            category: "ESTABLISHED",
            attribution: "[Kubo 1957, Martin-Schwinger 1959]",
            description: "Characterizes thermal equilibrium states",
            terms: {
                "σ<sub>t</sub>": { name: "Time Evolution", description: "Automorphism group" },
                "β": { name: "Inverse Temperature", description: "β = 1/k_B T" },
                "iβ": { name: "Imaginary Time", description: "Analytic continuation" }
            }
        },

        modularFlow: {
            id: "modular-flow",
            html: "σ<sub>t</sub>(A) = Δ<sup>it</sup> A Δ<sup>-it</sup>",
            latex: "\\sigma_t(A) = \\Delta^{it} A \\Delta^{-it}",
            label: "(5.3) Modular Automorphism",
            category: "ESTABLISHED",
            attribution: "[Tomita 1967, Takesaki 1970]",
            description: "Time evolution from thermal state via modular operator",
            terms: {
                "σ<sub>t</sub>(A)": { name: "Evolved Observable", description: "A at thermal time t" },
                "Δ": { name: "Modular Operator", description: "From Tomita-Takesaki theory" },
                "A": { name: "Observable", description: "Von Neumann algebra element" }
            }
        },

        unruhTemperature: {
            id: "unruh",
            html: "T<sub>Unruh</sub> = ℏa / (2πck<sub>B</sub>)",
            latex: "T_{Unruh} = \\frac{\\hbar a}{2\\pi c k_B}",
            label: "(5.10) Unruh Effect",
            category: "ESTABLISHED",
            attribution: "[Unruh 1976]",
            description: "Accelerating observer sees thermal bath",
            terms: {
                "T<sub>Unruh</sub>": { name: "Unruh Temperature", description: "Perceived temperature" },
                "a": { name: "Acceleration", description: "Proper acceleration" },
                "ℏ": { name: "Planck Constant", description: "Reduced Planck constant" }
            }
        },

        // --- Grand Unified Theory ---

        gaugeUnification: {
            id: "gauge-unification",
            html: "α<sub>1</sub>(M<sub>GUT</sub>) = α<sub>2</sub>(M<sub>GUT</sub>) = α<sub>3</sub>(M<sub>GUT</sub>)",
            latex: "\\alpha_1(M_{GUT}) = \\alpha_2(M_{GUT}) = \\alpha_3(M_{GUT})",
            label: "Gauge Coupling Unification",
            category: "ESTABLISHED",
            attribution: "[Georgi-Glashow 1974]",
            description: "All gauge couplings meet at GUT scale",
            terms: {
                "α<sub>1,2,3</sub>": { name: "Gauge Couplings", description: "U(1), SU(2), SU(3) couplings" },
                "M<sub>GUT</sub>": { name: "GUT Scale", description: "≈ 2 × 10¹⁶ GeV" }
            }
        },

        so10Spinor: {
            id: "so10-spinor",
            html: "16 = (3,2)<sub>1/6</sub> ⊕ (3̄,1)<sub>-2/3</sub> ⊕ (3̄,1)<sub>1/3</sub> ⊕ (1,2)<sub>-1/2</sub> ⊕ (1,1)<sub>1</sub> ⊕ (1,1)<sub>0</sub>",
            latex: "\\mathbf{16} = (3,2)_{1/6} \\oplus (\\bar{3},1)_{-2/3} \\oplus ...",
            label: "SO(10) Decomposition",
            category: "ESTABLISHED",
            attribution: "[Fritzsch-Minkowski 1975]",
            description: "One generation of SM fermions in single SO(10) spinor",
            terms: {
                "16": { name: "Spinor Rep", description: "16-dimensional SO(10) spinor" },
                "(3,2)": { name: "Quark Doublet", description: "Left-handed quarks" }
            }
        },

        seesawMechanism: {
            id: "seesaw",
            html: "m<sub>ν</sub> ≈ m<sub>D</sub>²/M<sub>R</sub>",
            latex: "m_\\nu \\approx \\frac{m_D^2}{M_R}",
            label: "See-saw Mechanism",
            category: "ESTABLISHED",
            attribution: "[Minkowski 1977, Gell-Mann et al. 1979]",
            description: "Explains smallness of neutrino masses",
            terms: {
                "m<sub>ν</sub>": { name: "Light Neutrino Mass", description: "~ 0.01-0.1 eV" },
                "m<sub>D</sub>": { name: "Dirac Mass", description: "~ electroweak scale" },
                "M<sub>R</sub>": { name: "Right-handed Mass", description: "~ GUT scale" }
            }
        },

        // --- Cosmology ---

        cplParameterization: {
            id: "cpl",
            html: "w(z) = w<sub>0</sub> + w<sub>a</sub> × (z / (1+z))",
            latex: "w(z) = w_0 + w_a \\frac{z}{1+z}",
            label: "(6.15) CPL Parameterization",
            category: "ESTABLISHED",
            attribution: "[Chevallier-Polarski 2001, Linder 2003]",
            description: "Standard dark energy equation of state parameterization",
            terms: {
                "w(z)": { name: "Equation of State", description: "p/ρ for dark energy" },
                "w<sub>0</sub>": { name: "Present Value", description: "w at z=0" },
                "w<sub>a</sub>": { name: "Evolution", description: "Rate of change" },
                "z": { name: "Redshift", description: "Cosmological redshift" }
            }
        },

        // --- Kaluza-Klein ---

        kkReduction: {
            id: "kk-reduction",
            html: "M<sub>Pl</sub>² = V<sub>n</sub> × M<sub>*</sub><sup>n+2</sup>",
            latex: "M_{Pl}^2 = V_n \\times M_*^{n+2}",
            label: "Kaluza-Klein Mass Relation",
            category: "ESTABLISHED",
            attribution: "[Kaluza 1921, Klein 1926]",
            description: "4D Planck mass from higher-dimensional reduction",
            terms: {
                "M<sub>Pl</sub>": { name: "4D Planck Mass", description: "2.4 × 10¹⁸ GeV" },
                "V<sub>n</sub>": { name: "Compact Volume", description: "Volume of extra dimensions" },
                "M<sub>*</sub>": { name: "Fundamental Scale", description: "Higher-D Planck mass" }
            }
        },

        fTheoryIndex: {
            id: "f-theory-index",
            html: "n<sub>gen</sub> = χ/24",
            latex: "n_{gen} = \\frac{\\chi}{24}",
            label: "F-theory Generation Formula",
            category: "ESTABLISHED",
            attribution: "[Sethi, Vafa, Witten 1996]",
            description: "Number of generations from Euler characteristic in F-theory",
            terms: {
                "n<sub>gen</sub>": { name: "Generations", description: "Number of fermion families" },
                "χ": { name: "Euler Characteristic", description: "Topological invariant of CY4" },
                "24": { name: "Index Divisor", description: "From D3-brane index theorem" }
            }
        },

        // --- Two-Time Physics ---

        twoTimePhysics: {
            id: "two-time-physics",
            html: "S = ∫ dτ [X'·P - ½λ(P² + M²) - ½μ(X·P)]",
            latex: "S = \\int d\\tau [X' \\cdot P - \\frac{1}{2}\\lambda(P^2 + M^2) - \\frac{1}{2}\\mu(X \\cdot P)]",
            label: "Two-Time Physics Action",
            category: "ESTABLISHED",
            attribution: "[Bars 1998-2010]",
            description: "Sp(2,R) gauge invariant action with two time dimensions",
            terms: {
                "X'·P": { name: "Symplectic Term", description: "Phase space kinetic term" },
                "λ, μ": { name: "Lagrange Multipliers", description: "Sp(2,R) gauge fields" },
                "X·P = 0": { name: "First Constraint", description: "Scale invariance" },
                "P² + M² = 0": { name: "Second Constraint", description: "Mass shell" }
            }
        },

        bosonicString: {
            id: "bosonic-string",
            html: "D<sub>crit</sub> = 26 (from c = D - 26 = 0)",
            latex: "D_{crit} = 26 \\text{ from } c = D - 26 = 0",
            label: "Bosonic String Critical Dimension",
            category: "ESTABLISHED",
            attribution: "[Lovelace 1971]",
            description: "Virasoro anomaly cancellation requires D = 26",
            terms: {
                "D<sub>crit</sub>": { name: "Critical Dimension", description: "D = 26 for bosonic string" },
                "c": { name: "Central Charge", description: "Virasoro anomaly" }
            }
        },

        sp2rConstraints: {
            id: "sp2r-constraints",
            html: "X² = 0, X·P = 0, P² + M² = 0",
            latex: "X^2 = 0, X \\cdot P = 0, P^2 + M^2 = 0",
            label: "Sp(2,R) Gauge Constraints",
            category: "ESTABLISHED",
            attribution: "[Bars 2006]",
            description: "Three constraints eliminate ghosts from second time",
            terms: {
                "X² = 0": { name: "Null Constraint", description: "Position null" },
                "X·P = 0": { name: "Orthogonality", description: "Phase space constraint" },
                "P² + M² = 0": { name: "Mass Shell", description: "Relativistic dispersion" }
            }
        },

        // --- Quantum Information ---

        bellInequality: {
            id: "bell-chsh",
            html: "|⟨CHSH⟩| ≤ 2 (classical) vs ≤ 2√2 (quantum)",
            latex: "|\\langle CHSH \\rangle| \\leq 2 \\text{ vs } \\leq 2\\sqrt{2}",
            label: "(8.3) CHSH Inequality",
            category: "ESTABLISHED",
            attribution: "[Bell 1964, CHSH 1969]",
            description: "Quantum correlations exceed classical bounds",
            terms: {
                "CHSH": { name: "Bell Operator", description: "Clauser-Horne-Shimony-Holt" },
                "2": { name: "Classical Bound", description: "Local hidden variables" },
                "2√2": { name: "Tsirelson Bound", description: "Maximum quantum value ≈ 2.83" }
            }
        },

        partialTrace: {
            id: "partial-trace",
            html: "ρ<sub>A</sub> = Tr<sub>B</sub>[ρ<sub>AB</sub>]",
            latex: "\\rho_A = \\text{Tr}_B[\\rho_{AB}]",
            label: "Partial Trace",
            category: "ESTABLISHED",
            attribution: "Quantum Information Theory",
            description: "Reduced density matrix from tracing out subsystem",
            terms: {
                "ρ<sub>A</sub>": { name: "Reduced State", description: "State of subsystem A" },
                "Tr<sub>B</sub>": { name: "Partial Trace", description: "Trace over system B" },
                "ρ<sub>AB</sub>": { name: "Joint State", description: "Full system density matrix" }
            }
        }
    },

    // ================================================================
    // THEORY FORMULAS - New physics specific to Principia Metaphysica
    // ================================================================

    THEORY: {

        // --- Fundamental Structure (26D Two-Time Framework) ---

        masterAction26D: {
            id: "master-action-26d",
            html: "S = ∫ d<sup>26</sup>x √|G| [M<sub>*</sub><sup>24</sup>R<sub>26</sub> + <span style='text-decoration:overline'>Ψ</span><sub>P</sub>(iΓ<sup>M</sup>D<sub>M</sub> - m)Ψ<sub>P</sub> + ℒ<sub>Sp(2,R)</sub>]",
            latex: "S = \\int d^{26}x \\sqrt{|G|} [M_*^{24}R_{26} + \\bar{\\Psi}_P(i\\Gamma^M D_M - m)\\Psi_P + \\mathcal{L}_{Sp(2,R)}]",
            label: "(1.1) Master Action [26D]",
            category: "THEORY",
            attribution: "Principia Metaphysica v6.0",
            description: "Complete 26D action with two times and Sp(2,R) gauge symmetry",
            status: "FOUNDATIONAL",
            terms: {
                "S": { name: "Action", description: "Total action functional" },
                "d<sup>26</sup>x": { name: "26D Volume", description: "Signature (24,2)" },
                "M<sub>*</sub><sup>24</sup>": { name: "26D Planck Scale", description: "Fundamental mass scale" },
                "R<sub>26</sub>": { name: "26D Ricci Scalar", description: "Full spacetime curvature" },
                "Ψ<sub>P</sub>": { name: "Pneuma Field", description: "8192-component spinor (gauge-reduced to 64)" },
                "ℒ<sub>Sp(2,R)</sub>": { name: "Sp(2,R) Gauge Terms", description: "Ghost elimination" }
            }
        },

        masterAction: {
            id: "master-action",
            html: "S<sub>eff</sub> = ∫ d<sup>13</sup>x √|G| [M<sub>*</sub><sup>11</sup>R + <span style='text-decoration:overline'>Ψ</span><sub>P</sub>(iΓ∇ - m)Ψ<sub>P</sub>]",
            latex: "S_{eff} = \\int d^{13}x \\sqrt{|G|} [M_*^{11}R + \\bar{\\Psi}_P(i\\Gamma\\nabla - m)\\Psi_P]",
            label: "(1.2) Effective 13D Action",
            category: "THEORY",
            attribution: "Principia Metaphysica",
            description: "Gauge-fixed 13D shadow of 26D action",
            status: "DERIVED",
            terms: {
                "S<sub>eff</sub>": { name: "Effective Action", description: "After Sp(2,R) gauge fixing" },
                "d<sup>13</sup>x": { name: "13D Volume", description: "4 macroscopic + 9 compact" },
                "M<sub>*</sub><sup>11</sup>": { name: "13D Planck Scale", description: "M* ≈ 10¹⁶ GeV" },
                "R": { name: "13D Ricci Scalar", description: "Spacetime curvature" },
                "Ψ<sub>P</sub>": { name: "Pneuma Field", description: "64-component reduced spinor" }
            }
        },

        spacetimeStructure26D: {
            id: "spacetime-structure-26d",
            html: "M<sub>26</sub> = M<sup>(4,2)</sup> × K<sub>Pneuma</sub> × K̃<sub>Pneuma</sub>",
            latex: "M_{26} = M^{(4,2)} \\times K_{Pneuma} \\times \\tilde{K}_{Pneuma}",
            label: "(2.1) 26D Spacetime Structure",
            category: "THEORY",
            attribution: "Principia Metaphysica v6.0",
            description: "26D = 6D two-time base × CY4 × Mirror CY4",
            status: "ANSATZ",
            terms: {
                "M<sub>26</sub>": { name: "26D Spacetime", description: "Full manifold with signature (24,2)" },
                "M<sup>(4,2)</sup>": { name: "6D Two-Time Base", description: "4 space + 2 time dimensions" },
                "K<sub>Pneuma</sub>": { name: "Pneuma Manifold", description: "CY4 with χ = 72" },
                "K̃<sub>Pneuma</sub>": { name: "Mirror Manifold", description: "Z₂-related CY4" }
            }
        },

        spacetimeStructure: {
            id: "spacetime-structure",
            html: "M<sub>13</sub> = M<sup>4</sup> × K<sub>Pneuma</sub>",
            latex: "M_{13} = M^4 \\times K_{Pneuma}",
            label: "(2.2) Observable Spacetime",
            category: "THEORY",
            attribution: "Principia Metaphysica",
            description: "13D gauge-fixed projection = 4D Minkowski × CY4",
            status: "DERIVED",
            terms: {
                "M<sub>13</sub>": { name: "13D Spacetime", description: "Observable shadow" },
                "M<sup>4</sup>": { name: "4D Minkowski", description: "Observable spacetime" },
                "K<sub>Pneuma</sub>": { name: "Pneuma Manifold", description: "CY4 with χ = 72" }
            }
        },

        symmetryBreaking: {
            id: "symmetry-breaking",
            html: "SO(10) → SU(3)<sub>C</sub> × SU(2)<sub>L</sub> × U(1)<sub>Y</sub>",
            latex: "SO(10) \\to SU(3)_C \\times SU(2)_L \\times U(1)_Y",
            label: "(2.1b) Symmetry Breaking Chain",
            category: "THEORY",
            attribution: "Principia Metaphysica + [Fritzsch-Minkowski 1975]",
            description: "SO(10) from K_Pneuma isometries breaks to Standard Model",
            status: "DERIVED",
            terms: {
                "SO(10)": { name: "GUT Group", description: "From CY4 isometries" },
                "SU(3)<sub>C</sub>": { name: "Color", description: "Strong force" },
                "SU(2)<sub>L</sub>": { name: "Weak Isospin", description: "Weak force" },
                "U(1)<sub>Y</sub>": { name: "Hypercharge", description: "Electroweak" }
            }
        },

        // --- Pneuma Field (26D Extended) ---

        pneumaLagrangian26D: {
            id: "pneuma-lagrangian-26d",
            html: "ℒ<sub>Pneuma</sub><sup>26D</sup> = <span style='text-decoration:overline'>Ψ</span><sub>P</sub>(iΓ<sup>M</sup>D<sub>M</sub> - m<sub>P</sub> + g<sub>T</sub>·t<sub>ortho</sub>)Ψ<sub>P</sub>",
            latex: "\\mathcal{L}_{Pneuma}^{26D} = \\bar{\\Psi}_P(i\\Gamma^M D_M - m_P + g_T \\cdot t_{ortho})\\Psi_P",
            label: "(3.1) Pneuma Lagrangian [26D]",
            category: "THEORY",
            attribution: "Principia Metaphysica v6.0",
            description: "26D Pneuma with orthogonal time coupling",
            status: "FOUNDATIONAL",
            terms: {
                "ℒ<sub>Pneuma</sub><sup>26D</sup>": { name: "26D Lagrangian", description: "Full two-time Pneuma action" },
                "<span style='text-decoration:overline'>Ψ</span><sub>P</sub>": { name: "Conjugate", description: "8192-component (gauge-reduced to 64)" },
                "Γ<sup>M</sup>": { name: "26D Gammas", description: "8192×8192 matrices" },
                "g<sub>T</sub>·t<sub>ortho</sub>": { name: "Time Coupling", description: "Orthogonal time interaction" }
            }
        },

        pneumaLagrangian: {
            id: "pneuma-lagrangian",
            html: "ℒ<sub>Pneuma</sub> = <span style='text-decoration:overline'>Ψ</span><sub>P</sub>(iΓ<sup>M</sup>D<sub>M</sub> - m<sub>P</sub>)Ψ<sub>P</sub>",
            latex: "\\mathcal{L}_{Pneuma} = \\bar{\\Psi}_P(i\\Gamma^M D_M - m_P)\\Psi_P",
            label: "(3.2) Effective 13D Pneuma Lagrangian",
            category: "THEORY",
            attribution: "Principia Metaphysica",
            description: "Gauge-fixed 64-component Pneuma spinor",
            status: "DERIVED",
            terms: {
                "ℒ<sub>Pneuma</sub>": { name: "Lagrangian Density", description: "Effective Pneuma action" },
                "<span style='text-decoration:overline'>Ψ</span><sub>P</sub>": { name: "Conjugate", description: "Ψ̄ = Ψ†Γ⁰" },
                "Γ<sup>M</sup>": { name: "13D Gammas", description: "64×64 matrices" },
                "D<sub>M</sub>": { name: "Covariant Derivative", description: "∂ + ω + A" }
            }
        },

        clifford26D: {
            id: "clifford-26d",
            html: "{Γ<sup>M</sup>, Γ<sup>N</sup>} = 2G<sup>MN</sup>, dim = 2<sup>13</sup> = 8192",
            latex: "\\{\\Gamma^M, \\Gamma^N\\} = 2G^{MN}, \\dim = 2^{13}",
            label: "(3.3) 26D Clifford Algebra",
            category: "THEORY",
            attribution: "Principia Metaphysica v6.0",
            description: "Cl(24,2) gives 8192-dimensional spinors",
            status: "FOUNDATIONAL",
            terms: {
                "Γ<sup>M</sup>": { name: "26D Gamma", description: "M = 0,1,...,25" },
                "G<sup>MN</sup>": { name: "26D Metric", description: "Signature (24,2)" },
                "2<sup>13</sup>": { name: "Spinor Dimension", description: "8192 components" }
            }
        },

        clifford13D: {
            id: "clifford-13d",
            html: "{Γ<sup>M</sup>, Γ<sup>N</sup>} = 2G<sup>MN</sup>",
            latex: "\\{\\Gamma^M, \\Gamma^N\\} = 2G^{MN}",
            label: "(3.4) Effective 13D Clifford Algebra",
            category: "THEORY",
            attribution: "Principia Metaphysica",
            description: "13D gamma matrices from Sp(2,R) gauge fixing",
            status: "DERIVED",
            terms: {
                "Γ<sup>M</sup>": { name: "13D Gamma", description: "M = 0,1,...,12" },
                "G<sup>MN</sup>": { name: "13D Metric", description: "Signature (-,+,+,...,+)" }
            }
        },

        cliffordDecomposition: {
            id: "clifford-decomp",
            html: "Cl(24,2) → Cl(1,12) ⊗ Cl(11,1) / Sp(2,R) → 64×64 effective",
            latex: "Cl(24,2) \\to Cl(1,12) \\otimes Cl(11,1) / Sp(2,R)",
            label: "(3.5) Clifford Reduction Chain",
            category: "THEORY",
            attribution: "Principia Metaphysica v6.0",
            description: "26D Clifford reduces to 13D × mirror via gauge fixing",
            status: "DERIVED",
            terms: {
                "Cl(24,2)": { name: "26D Clifford", description: "Full two-time algebra" },
                "Cl(1,12)": { name: "Observable Sector", description: "64×64 matrices" },
                "Cl(11,1)": { name: "Mirror Sector", description: "Hidden dimensions" },
                "Sp(2,R)": { name: "Gauge Group", description: "Ghost elimination" }
            }
        },

        covariantDerivative: {
            id: "covariant-derivative",
            html: "D<sub>M</sub> = ∂<sub>M</sub> + ¼ω<sub>M</sub><sup>AB</sup>Γ<sub>AB</sub> + A<sub>M</sub><sup>a</sup>T<sup>a</sup>",
            latex: "D_M = \\partial_M + \\frac{1}{4}\\omega_M^{AB}\\Gamma_{AB} + A_M^a T^a",
            label: "(3.4) Full Covariant Derivative",
            category: "THEORY",
            attribution: "Principia Metaphysica",
            description: "Includes spin connection and gauge connection",
            status: "FOUNDATIONAL",
            terms: {
                "∂<sub>M</sub>": { name: "Partial", description: "Coordinate derivative" },
                "ω<sub>M</sub><sup>AB</sup>": { name: "Spin Connection", description: "Gravity coupling" },
                "A<sub>M</sub><sup>a</sup>T<sup>a</sup>": { name: "Gauge Connection", description: "SO(10) gauge" }
            }
        },

        emergentMetric: {
            id: "emergent-metric",
            html: "g<sub>mn</sub> ∝ ⟨<span style='text-decoration:overline'>Ψ</span><sub>P</sub>Γ<sub>mn</sub>Ψ<sub>P</sub>⟩",
            latex: "g_{mn} \\propto \\langle \\bar{\\Psi}_P \\Gamma_{mn} \\Psi_P \\rangle",
            label: "(3.5) Emergent Metric",
            category: "THEORY",
            attribution: "Principia Metaphysica",
            description: "Geometry emerges from Pneuma condensates",
            status: "HYPOTHESIS",
            terms: {
                "g<sub>mn</sub>": { name: "Internal Metric", description: "K_Pneuma geometry" },
                "⟨...⟩": { name: "VEV", description: "Vacuum expectation value" },
                "Γ<sub>mn</sub>": { name: "Antisymmetric", description: "½[Γ_m, Γ_n]" }
            }
        },

        // --- Geometric Framework ---

        hodgeNumbers: {
            id: "hodge-numbers",
            html: "h<sup>1,1</sup> = 4, h<sup>2,1</sup> = 0, h<sup>3,1</sup> = 0, h<sup>2,2</sup> = 60",
            latex: "h^{1,1} = 4, h^{2,1} = 0, h^{3,1} = 0, h^{2,2} = 60",
            label: "(2.3) Hodge Numbers",
            category: "THEORY",
            attribution: "Principia Metaphysica",
            description: "K_Pneuma Hodge diamond satisfying CY4 constraint",
            status: "SPECIFIED",
            terms: {
                "h<sup>1,1</sup>": { name: "Kähler Moduli", description: "4 size parameters" },
                "h<sup>2,2</sup>": { name: "Middle Cohomology", description: "= 60" }
            }
        },

        eulerCharacteristic: {
            id: "euler-char",
            html: "χ(K<sub>Pneuma</sub>) = 72",
            latex: "\\chi(K_{Pneuma}) = 72",
            label: "(2.4) Euler Characteristic",
            category: "THEORY",
            attribution: "Principia Metaphysica",
            description: "Required for exactly 3 generations via F-theory",
            status: "SPECIFIED",
            terms: {
                "χ": { name: "Euler Characteristic", description: "Topological invariant" },
                "72": { name: "Value", description: "Via Z₂×Z₂ quotient of χ=288 CICY" }
            }
        },

        // --- Two-Time Thermal Hypothesis ---

        twoTimeStructure: {
            id: "two-time-structure",
            html: "t<sub>total</sub> = t<sub>therm</sub> + β·t<sub>ortho</sub>, β = cos(θ<sub>mirror</sub>)",
            latex: "t_{total} = t_{therm} + \\beta \\cdot t_{ortho}, \\beta = \\cos(\\theta_{mirror})",
            label: "(5.1) Two-Time Structure",
            category: "THEORY",
            attribution: "Principia Metaphysica v6.0",
            description: "Observable time is projection of two-time plane",
            status: "FOUNDATIONAL",
            terms: {
                "t<sub>total</sub>": { name: "Total Time", description: "Effective time coordinate" },
                "t<sub>therm</sub>": { name: "Thermal Time", description: "Observable thermal flow" },
                "t<sub>ortho</sub>": { name: "Orthogonal Time", description: "Hidden second time" },
                "θ<sub>mirror</sub>": { name: "Mirror Angle", description: "Rotation in time plane" }
            }
        },

        thermalTimeParameter: {
            id: "thermal-time-param",
            html: "α<sub>T</sub> = (d ln τ / d ln a) - (d ln H / d ln a) = (+1) - (-3/2) = 2.5",
            latex: "\\alpha_T = \\frac{d\\ln\\tau}{d\\ln a} - \\frac{d\\ln H}{d\\ln a} = 2.5",
            label: "(5.2) Thermal Time Parameter",
            category: "THEORY",
            attribution: "Principia Metaphysica + TTH [Connes-Rovelli 1994]",
            description: "Mismatch between thermal and cosmic time scales",
            status: "DERIVED",
            terms: {
                "α<sub>T</sub>": { name: "Thermal Parameter", description: "= 2.5 in matter era" },
                "τ": { name: "Thermal Time", description: "τ = 1/Γ ∝ a" },
                "H": { name: "Hubble Rate", description: "H ∝ a^(-3/2)" }
            }
        },

        mirrorEntropy: {
            id: "mirror-entropy",
            html: "S<sub>total</sub> = S<sub>obs</sub> + S<sub>mirror</sub>, dS<sub>mirror</sub>/dt<sub>ortho</sub> ≥ 0",
            latex: "S_{total} = S_{obs} + S_{mirror}, dS_{mirror}/dt_{ortho} \\geq 0",
            label: "(5.3) Mirror Entropy",
            category: "THEORY",
            attribution: "Principia Metaphysica v6.0",
            description: "Independent entropy flows in each time direction",
            status: "HYPOTHESIS",
            terms: {
                "S<sub>total</sub>": { name: "Total Entropy", description: "Sum of both sectors" },
                "S<sub>obs</sub>": { name: "Observable Entropy", description: "Our universe" },
                "S<sub>mirror</sub>": { name: "Mirror Entropy", description: "Hidden sector" },
                "dS/dt ≥ 0": { name: "Second Law", description: "Each sector independently" }
            }
        },

        thermalDarkEnergy: {
            id: "thermal-de",
            html: "w<sub>thermal</sub>(z) = w<sub>0</sub> × [1 + (α<sub>T</sub>/3) × ln(1+z)]",
            latex: "w_{thermal}(z) = w_0 \\times [1 + (\\alpha_T/3) \\times \\ln(1+z)]",
            label: "(6.3) Thermal Dark Energy",
            category: "THEORY",
            attribution: "Principia Metaphysica",
            description: "Dark energy EOS from thermal time mechanism",
            status: "DERIVED",
            terms: {
                "w<sub>thermal</sub>": { name: "Thermal w(z)", description: "From τ/H mismatch" },
                "α<sub>T</sub>/3": { name: "Evolution Rate", description: "≈ 0.83" }
            }
        },

        // --- Mirror Brane Structure (Z₂ Extended) ---

        mirrorBraneStructure: {
            id: "mirror-brane-structure",
            html: "B¹<sub>1:4</sub> ↔ B²<sub>1:4</sub> (Z₂ orbifold identification)",
            latex: "B^1_{1:4} \\leftrightarrow B^2_{1:4} \\text{ (Z}_2 \\text{ orbifold)}",
            label: "(8.1) Z₂ Mirror Brane Structure",
            category: "THEORY",
            attribution: "Principia Metaphysica v6.0",
            description: "Observable 1+3 branes mirrored by hidden 1+3 branes via Z₂",
            status: "FOUNDATIONAL",
            terms: {
                "B¹<sub>1:4</sub>": { name: "Observable Branes", description: "Our 1+3 brane stack" },
                "B²<sub>1:4</sub>": { name: "Mirror Branes", description: "Hidden 1+3 brane stack" },
                "Z₂": { name: "Orbifold Action", description: "Exchanges brane stacks" }
            }
        },

        braneStructure: {
            id: "brane-structure",
            html: "|Ψ⟩ ∈ ℋ = ℋ<sub>B₁</sub> ⊗ ℋ<sub>B₂</sub> ⊗ ℋ<sub>B₃</sub> ⊗ ℋ<sub>B₄</sub>",
            latex: "|\\Psi\\rangle \\in \\mathcal{H} = \\mathcal{H}_{B_1} \\otimes ...",
            label: "(8.2) 1+3 Brane Hilbert Space",
            category: "THEORY",
            attribution: "Principia Metaphysica",
            description: "4 branes sharing thermal time: 1 observable + 3 hidden",
            status: "HYPOTHESIS",
            terms: {
                "|Ψ⟩": { name: "Total State", description: "Complete 26D state" },
                "ℋ<sub>B₁</sub>": { name: "Observable Brane", description: "Our 4D universe" },
                "ℋ<sub>B₂,₃,₄</sub>": { name: "Hidden Branes", description: "3 additional 4D branes" }
            }
        },

        branePartialTrace: {
            id: "brane-trace",
            html: "ρ<sub>B₁</sub> = Tr<sub>B₂</sub>[Tr<sub>B₃</sub>[Tr<sub>B₄</sub>[Tr<sub>mirror</sub>[|Ψ⟩⟨Ψ|]]]]",
            latex: "\\rho_{B_1} = \\text{Tr}_{B_2}[\\text{Tr}_{B_3}[\\text{Tr}_{B_4}[\\text{Tr}_{mirror}[|\\Psi\\rangle\\langle\\Psi|]]]]",
            label: "(8.3) Full Brane Partial Trace",
            category: "THEORY",
            attribution: "Principia Metaphysica v6.0",
            description: "Observable state from tracing hidden + mirror branes",
            status: "DERIVED",
            terms: {
                "ρ<sub>B₁</sub>": { name: "Observable State", description: "Mixed state on our brane" },
                "Tr<sub>Bi</sub>": { name: "Hidden Traces", description: "Over hidden branes" },
                "Tr<sub>mirror</sub>": { name: "Mirror Trace", description: "Over Z₂ partner stack" }
            }
        },

        mirrorCoupling: {
            id: "mirror-coupling",
            html: "ℒ<sub>int</sub> = λ<sub>Z₂</sub>(Ψ<sub>P</sub><sup>†</sup>·Ψ̃<sub>P</sub> + h.c.)",
            latex: "\\mathcal{L}_{int} = \\lambda_{Z_2}(\\Psi_P^\\dagger \\cdot \\tilde{\\Psi}_P + h.c.)",
            label: "(8.4) Mirror Sector Coupling",
            category: "THEORY",
            attribution: "Principia Metaphysica v6.0",
            description: "Interaction between observable and mirror Pneuma fields",
            status: "HYPOTHESIS",
            terms: {
                "ℒ<sub>int</sub>": { name: "Interaction", description: "Mirror coupling Lagrangian" },
                "λ<sub>Z₂</sub>": { name: "Mirror Coupling", description: "Strength of Z₂ interaction" },
                "Ψ̃<sub>P</sub>": { name: "Mirror Pneuma", description: "Z₂ partner field" }
            }
        }
    },

    // ================================================================
    // DERIVED RESULTS - Consequences of the theory
    // ================================================================

    DERIVED: {

        generationNumber26D: {
            id: "generation-number-26d",
            html: "n<sub>gen</sub> = χ(K<sub>Pneuma</sub> × K̃<sub>Pneuma</sub>)/48 = 144/48 = 3",
            latex: "n_{gen} = \\chi(K_{Pneuma} \\times \\tilde{K}_{Pneuma})/48 = 144/48 = 3",
            label: "(2.3) Three Generations [26D]",
            category: "DERIVED",
            attribution: "Principia Metaphysica v6.0",
            description: "3 generations preserved via Z₂-doubled Euler characteristic",
            status: "VERIFIED",
            terms: {
                "n<sub>gen</sub>": { name: "Generations", description: "= 3 (observed)" },
                "χ = 144": { name: "Total Euler Char", description: "72 × 2 from mirror doubling" },
                "48": { name: "2T Index Divisor", description: "24 × 2 for two-time framework" }
            }
        },

        generationNumber: {
            id: "generation-number",
            html: "n<sub>gen</sub> = χ(K<sub>Pneuma</sub>)/24 = 72/24 = 3",
            latex: "n_{gen} = \\chi(K_{Pneuma})/24 = 72/24 = 3",
            label: "(2.4) Three Generations [Effective]",
            category: "DERIVED",
            attribution: "Principia Metaphysica + [Sethi, Vafa, Witten 1996]",
            description: "Gauge-fixed result: same 3 generations",
            status: "VERIFIED",
            terms: {
                "n<sub>gen</sub>": { name: "Generations", description: "= 3 (observed)" },
                "χ = 72": { name: "Euler Char", description: "Of effective K_Pneuma" },
                "24": { name: "F-theory Divisor", description: "Index theorem" }
            }
        },

        gutScale: {
            id: "gut-scale",
            html: "M<sub>GUT</sub> = 2 × 10<sup>16</sup> GeV",
            latex: "M_{GUT} = 2 \\times 10^{16} \\text{ GeV}",
            label: "(4.1) Unification Scale",
            category: "DERIVED",
            attribution: "Principia Metaphysica",
            description: "Energy where gauge couplings unify",
            status: "CONSISTENT",
            terms: {
                "M<sub>GUT</sub>": { name: "GUT Scale", description: "From RG running" }
            }
        },

        mepDerivation: {
            id: "mep-w0",
            html: "w<sub>0</sub> = -(d<sub>eff</sub> - 1)/(d<sub>eff</sub> + 1) = -11/13 ≈ -0.846",
            latex: "w_0 = -\\frac{d_{eff} - 1}{d_{eff} + 1} = -\\frac{11}{13}",
            label: "(6.2) MEP Derivation of w₀",
            category: "DERIVED",
            attribution: "Maximum Entropy Principle + Principia Metaphysica",
            description: "w₀ fixed by effective dimensionality d_eff = 12",
            status: "SEMI-DERIVED",
            terms: {
                "w<sub>0</sub>": { name: "Present EOS", description: "≈ -0.846" },
                "d<sub>eff</sub>": { name: "Effective Dim", description: "= 12 (13 - 1 time)" },
                "-11/13": { name: "Prediction", description: "Matches DESI to 0.3σ" }
            }
        },

        waDerivation: {
            id: "wa-derivation",
            html: "w<sub>a</sub> = -α<sub>T</sub>w<sub>0</sub>/3 ≈ -0.71",
            latex: "w_a = -\\alpha_T w_0 / 3 \\approx -0.71",
            label: "(6.4) w_a from Thermal Time",
            category: "DERIVED",
            attribution: "Principia Metaphysica",
            description: "Evolution parameter follows from α_T derivation",
            status: "SEMI-DERIVED",
            terms: {
                "w<sub>a</sub>": { name: "Evolution Param", description: "≈ -0.71" },
                "α<sub>T</sub>": { name: "Thermal Param", description: "= 2.5" }
            }
        },

        planckMassRelation: {
            id: "planck-mass",
            html: "M<sub>Pl</sub>² = V<sub>8</sub> × M<sub>*</sub><sup>11</sup>",
            latex: "M_{Pl}^2 = V_8 \\times M_*^{11}",
            label: "(2.5) 4D Planck Mass",
            category: "DERIVED",
            attribution: "Principia Metaphysica",
            description: "4D gravity from 13D compactification",
            status: "CONSISTENT",
            terms: {
                "M<sub>Pl</sub>": { name: "4D Planck", description: "2.4 × 10¹⁸ GeV" },
                "V<sub>8</sub>": { name: "Internal Volume", description: "Volume of K_Pneuma" },
                "M<sub>*</sub>": { name: "13D Scale", description: "≈ 10¹⁶ GeV" }
            }
        }
    },

    // ================================================================
    // PREDICTIONS - Testable predictions of the theory
    // ================================================================

    PREDICTIONS: {

        normalHierarchy: {
            id: "normal-hierarchy",
            html: "m<sub>1</sub> < m<sub>2</sub> < m<sub>3</sub> (Normal Hierarchy required)",
            latex: "m_1 < m_2 < m_3",
            label: "(7.1) Neutrino Hierarchy",
            category: "PREDICTION",
            attribution: "Principia Metaphysica",
            description: "SO(10) breaking pattern requires Normal Hierarchy",
            status: "PRIMARY FALSIFIABLE TEST",
            testBy: "JUNO/DUNE (2025-2028)",
            falsification: "Inverted Hierarchy confirmed → THEORY FALSIFIED",
            terms: {
                "m<sub>1,2,3</sub>": { name: "Mass Eigenstates", description: "Neutrino masses" },
                "NH": { name: "Normal Hierarchy", description: "m₁ < m₂ << m₃" }
            }
        },

        neutrinoMassSum: {
            id: "neutrino-sum",
            html: "Σm<sub>ν</sub> = 0.060 eV",
            latex: "\\Sigma m_\\nu = 0.060 \\text{ eV}",
            label: "(7.2) Neutrino Mass Sum",
            category: "PREDICTION",
            attribution: "Principia Metaphysica",
            description: "From NH + minimal m₁ → 0",
            status: "CONSISTENT (but not unique)",
            testBy: "DESI + CMB",
            currentData: "< 0.072 eV (DESI + Planck)",
            terms: {
                "Σm<sub>ν</sub>": { name: "Mass Sum", description: "m₁ + m₂ + m₃" }
            }
        },

        protonLifetime: {
            id: "proton-decay",
            html: "τ<sub>p</sub> ~ 10<sup>34</sup> - 10<sup>36</sup> years",
            latex: "\\tau_p \\sim 10^{34} - 10^{36} \\text{ years}",
            label: "(4.2) Proton Lifetime",
            category: "PREDICTION",
            attribution: "Principia Metaphysica + GUT theory",
            description: "From dimension-6 operators at M_GUT",
            status: "TESTABLE",
            testBy: "Hyper-Kamiokande (2030-2037)",
            currentLimit: "> 2.4 × 10³⁴ years (Super-K)",
            terms: {
                "τ<sub>p</sub>": { name: "Proton Lifetime", description: "Mean decay time" }
            }
        },

        darkEnergyW0: {
            id: "de-w0",
            html: "w<sub>0</sub> = -11/13 ≈ -0.846",
            latex: "w_0 = -11/13 \\approx -0.846",
            label: "(6.2) Dark Energy w₀",
            category: "PREDICTION",
            attribution: "Principia Metaphysica (MEP)",
            description: "Semi-derived from effective dimensionality",
            status: "CONSISTENT",
            testBy: "DESI, Euclid, Roman",
            currentData: "-0.83 ± 0.06 (DESI 2024) - agrees to 0.3σ",
            terms: {
                "w<sub>0</sub>": { name: "Present EOS", description: "-0.846" },
                "-11/13": { name: "MEP Value", description: "For d_eff = 12" }
            }
        },

        darkEnergyWa: {
            id: "de-wa",
            html: "w<sub>a</sub> ≈ -0.71",
            latex: "w_a \\approx -0.71",
            label: "(6.4) Dark Energy w_a",
            category: "PREDICTION",
            attribution: "Principia Metaphysica",
            description: "From thermal time parameter α_T = 2.5",
            status: "CONSISTENT",
            testBy: "DESI DR3 (2026)",
            currentData: "-0.75 ± 0.3 (DESI 2024) - agrees to 1σ",
            falsification: "w_a > 0 confirmed → THERMAL TIME FALSIFIED",
            terms: {
                "w<sub>a</sub>": { name: "Evolution", description: "≈ -0.71" }
            }
        },

        effectiveNeutrinos: {
            id: "n-eff",
            html: "ΔN<sub>eff</sub> = 0.08 - 0.16",
            latex: "\\Delta N_{eff} = 0.08 - 0.16",
            label: "(7.3) Extra Radiation",
            category: "PREDICTION",
            attribution: "Principia Metaphysica",
            description: "From pNG fermions in thermal bath",
            status: "TESTABLE",
            testBy: "CMB-S4 (2028+)",
            sensitivity: "Δ(N_eff) ~ 0.06",
            terms: {
                "ΔN<sub>eff</sub>": { name: "Extra Radiation", description: "Beyond 3 SM neutrinos" },
                "pNG": { name: "Pseudo-NG", description: "Fermions from Pneuma condensate" }
            }
        }
    }
};

// ================================================================
// UTILITY FUNCTIONS
// ================================================================

/**
 * Get formula by ID from any category
 */
function getFormula(id) {
    for (const category of ['ESTABLISHED', 'THEORY', 'DERIVED', 'PREDICTIONS']) {
        for (const [key, formula] of Object.entries(PrincipiaFormulas[category])) {
            if (formula.id === id) {
                return { ...formula, key, category };
            }
        }
    }
    return null;
}

/**
 * Get all formulas in a category
 */
function getFormulasByCategory(category) {
    return PrincipiaFormulas[category] || {};
}

/**
 * Generate HTML for a formula with tooltips
 */
function renderFormula(id, options = {}) {
    const formula = getFormula(id);
    if (!formula) return `<span class="error">Formula not found: ${id}</span>`;

    const bgColor = {
        'ESTABLISHED': 'rgba(139, 127, 255, 0.08)',
        'THEORY': 'rgba(255, 126, 182, 0.08)',
        'DERIVED': 'rgba(81, 207, 102, 0.08)',
        'PREDICTIONS': 'rgba(79, 172, 254, 0.08)'
    }[formula.category] || 'rgba(139, 127, 255, 0.08)';

    const borderColor = {
        'ESTABLISHED': 'rgba(139, 127, 255, 0.25)',
        'THEORY': 'rgba(255, 126, 182, 0.25)',
        'DERIVED': 'rgba(81, 207, 102, 0.25)',
        'PREDICTIONS': 'rgba(79, 172, 254, 0.25)'
    }[formula.category] || 'rgba(139, 127, 255, 0.25)';

    return `
        <div class="interactive-formula" data-formula-id="${id}" style="background: ${bgColor}; border: 1px solid ${borderColor}; border-radius: 10px; padding: 1.25rem; margin: 1rem 0;">
            <div class="formula-display" style="text-align: center; font-size: 1.3rem; font-family: 'Crimson Text', serif;">
                ${formula.html}
            </div>
            <div class="formula-label" style="text-align: center; margin-top: 0.75rem; color: var(--text-muted);">
                ${formula.label} ${formula.attribution || ''}
            </div>
        </div>
    `;
}

/**
 * Get status badge HTML
 */
function getStatusBadge(status) {
    const colors = {
        'DERIVED': { bg: '#51cf66', text: 'white' },
        'SEMI-DERIVED': { bg: '#ffc107', text: 'black' },
        'PREDICTION': { bg: '#4facfe', text: 'white' },
        'ESTABLISHED': { bg: '#8b7fff', text: 'white' },
        'FOUNDATIONAL': { bg: '#8b7fff', text: 'white' },
        'HYPOTHESIS': { bg: '#ff9f43', text: 'white' },
        'TESTABLE': { bg: '#4facfe', text: 'white' },
        'CONSISTENT': { bg: '#51cf66', text: 'white' },
        'VERIFIED': { bg: '#51cf66', text: 'white' }
    };

    const style = colors[status] || { bg: '#6c757d', text: 'white' };
    return `<span class="formula-status" style="background: ${style.bg}; color: ${style.text}; padding: 0.25rem 0.75rem; border-radius: 20px; font-size: 0.75rem; font-weight: 600;">${status}</span>`;
}

// Export for use in other scripts
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { PrincipiaFormulas, getFormula, getFormulasByCategory, renderFormula, getStatusBadge };
}

// Make available globally in browser
if (typeof window !== 'undefined') {
    window.PrincipiaFormulas = PrincipiaFormulas;
    window.getFormula = getFormula;
    window.getFormulasByCategory = getFormulasByCategory;
    window.renderFormula = renderFormula;
    window.getStatusBadge = getStatusBadge;
}
