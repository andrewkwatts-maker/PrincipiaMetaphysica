/**
 * Centralized Theory Constants for Principia Metaphysica
 *
 * This file contains ALL numerical values, predictions, and assumptions
 * used throughout the theory. Edit values here to update everywhere.
 *
 * USAGE: Import and reference these constants in all HTML/JS files
 * to ensure consistency across the entire project.
 */

const TheoryConstants = {

    // ================================================================
    // DIMENSIONAL STRUCTURE
    // ================================================================

    dimensions: {
        full: 26,                    // Full theory dimensionality
        signature: { space: 24, time: 2 },  // (24,2) signature
        effective: 13,               // Gauge-fixed shadow dimensionality
        effectiveSignature: { space: 12, time: 1 },  // (12,1) effective
        observable: 4,               // Macroscopic spacetime
        internal: 9,                 // Internal manifold (CY4-fold)
        internalCompact: 8,          // K_Pneuma dimensions

        // Derived values
        get effectiveSpatial() { return this.full / 2 - 1; },  // 12
        get dEff() { return 12; }    // Effective spatial dimensions for MEP
    },

    // ================================================================
    // SPINOR STRUCTURE
    // ================================================================

    spinors: {
        full26D: Math.pow(2, 13),    // 8192 components in Cl(24,2)
        effective13D: Math.pow(2, 6), // 64 components after Sp(2,R) gauge fixing
        decomposition4D: 4,           // 4D Dirac spinor
        internalModes: 16,            // Internal CY4 modes

        // Clifford algebras
        clifford26D: "Cl(24,2)",
        clifford13D: "Cl(12,1)",
        clifford4D: "Cl(3,1)",

        // Descriptions
        get reductionRatio() { return this.full26D / this.effective13D; }  // 128
    },

    // ================================================================
    // BRANE STRUCTURE
    // ================================================================

    branes: {
        totalCount: 8,               // Total branes (4 × 2 mirror copies)
        perSector: 4,                // Branes per Z₂ sector
        hierarchy: "1+3",            // 1 B₀ + 3 B_i pattern

        observable: {
            B0: { name: "B₀", role: "Time-generating", dim: "point-like" },
            B1: { name: "B₁", role: "String-like", dim: 1 },
            B2: { name: "B₂", role: "Membrane", dim: 2 },
            B3: { name: "B₃", role: "3-brane (our universe)", dim: 3 }
        },

        mirror: {
            B0_prime: { name: "B₀'", role: "Mirror time-generating", sector: "hidden" },
            B1_prime: { name: "B₁'", role: "Mirror string-like", sector: "hidden" },
            B2_prime: { name: "B₂'", role: "Mirror membrane", sector: "hidden" },
            B3_prime: { name: "B₃'", role: "Mirror 3-brane", sector: "hidden" }
        },

        // Z₂ orbifold structure
        z2Symmetry: "B¹₁:₄ ↔ B²₁:₄",
        mirrorCoupling: "gravitational only"
    },

    // ================================================================
    // GENERATION FORMULA
    // ================================================================

    generations: {
        count: 3,                    // Observed fermion generations

        // 26D derivation
        eulerChar26D: 144,           // χ_total for Z₂-doubled CY4
        divisor26D: 48,              // Index formula divisor
        formula26D: "n_gen = χ_total/48 = 144/48 = 3",

        // Effective 13D derivation (F-theory)
        eulerChar13D: 72,            // χ(CY4) for single sector
        divisor13D: 24,              // F-theory index divisor
        formula13D: "n_gen = χ(CY4)/24 = 72/24 = 3",

        // Consistency check
        get isConsistent() {
            return (this.eulerChar26D / this.divisor26D) ===
                   (this.eulerChar13D / this.divisor13D);
        }
    },

    // ================================================================
    // COSMOLOGICAL PREDICTIONS
    // ================================================================

    cosmology: {
        // Dark energy equation of state
        w0: {
            value: -11/13,
            decimal: -0.846153846,
            rounded: -0.846,
            formula: "w₀ = -(d_eff - 1)/(d_eff + 1)",
            derivation: "MEP with d_eff = 12 spatial dimensions",
            status: "SEMI-DERIVED",
            observational: {
                DESI_2024: { value: -0.827, uncertainty: 0.063 },
                Planck_2018: { value: -1.03, uncertainty: 0.03 }
            }
        },

        wa: {
            value: -0.75,
            formula: "w_a ≈ -3/4 (from two-time dynamics)",
            derivation: "Two-time modular flow with Z₂ coupling",
            status: "DERIVED",
            observational: {
                DESI_2024: { value: -0.75, uncertainty: 0.25 }
            }
        },

        // Thermal time parameter
        alphaT: {
            base: 2.5,
            z2Correction: 0.2,
            value: 2.7,
            formula: "α_T = (d ln τ / d ln a) - (d ln H / d ln a) + δ_Z₂",
            derivation: "Matter-era thermal time evolution + Z₂ mirror entropy",
            status: "DERIVED"
        },

        // Hubble constant
        H0: {
            value: 67.4,
            units: "km/s/Mpc",
            source: "Planck 2018"
        },

        // Other parameters
        omegaLambda: 0.685,
        omegaMatter: 0.315,
        omegaBaryon: 0.049
    },

    // ================================================================
    // GAUGE STRUCTURE
    // ================================================================

    gauge: {
        // Two-time gauge symmetry
        sp2r: {
            name: "Sp(2,R)",
            role: "Two-time gauge fixing",
            constraints: ["X² = 0", "X·P = 0", "P² + M² = 0"],
            eliminates: "Negative-norm ghost states"
        },

        // GUT structure
        gut: {
            group: "SO(10)",
            breakingChain: "SO(10) → SU(5) → SU(3)×SU(2)×U(1)",
            scale: 2e16,  // GeV
            scaleStr: "2 × 10¹⁶ GeV"
        },

        // Standard Model
        sm: {
            group: "SU(3)_C × SU(2)_L × U(1)_Y",
            electroweakScale: 246,  // GeV
            qcdScale: 0.2  // GeV (Λ_QCD)
        },

        // Exceptional structures
        exceptional: {
            g2: { role: "Automorphisms of octonions", dim: 14 },
            f4: { role: "Automorphisms of J₃(O)", dim: 52 },
            e6: { role: "Collineations of OP²", dim: 78 }
        }
    },

    // ================================================================
    // MASS SCALES
    // ================================================================

    masses: {
        planck4D: 1.22e19,           // GeV - 4D Planck mass
        fundamental13D: 1e16,        // GeV - M_* fundamental scale
        gut: 2e16,                   // GeV - GUT scale
        electroweak: 246,            // GeV - EW breaking scale

        // Planck relation
        planckRelation: "M_Pl² = M_*¹¹ · V₈",

        // Hierarchy
        hierarchyExplanation: "Large volume V₈ explains M_Pl >> M_*"
    },

    // ================================================================
    // TIME STRUCTURE
    // ================================================================

    time: {
        dimensions: 2,

        thermal: {
            name: "t_therm",
            role: "Observable thermal time",
            emergence: "From modular flow of quantum state",
            equation: "τ(t) = exp(α_T · t)"
        },

        orthogonal: {
            name: "t_ortho",
            role: "Hidden orthogonal time",
            emergence: "Gauge-fixed via Sp(2,R)",
            coupling: "g_T·t_ortho term in Pneuma Lagrangian"
        },

        combined: {
            formula: "t_total = t_therm + β·t_ortho",
            beta: "cos(θ_mirror)",
            physicalMeaning: "Observable time includes small mirror correction"
        }
    },

    // ================================================================
    // ENTROPY AND THERMODYNAMICS
    // ================================================================

    entropy: {
        // Mirror sector contribution
        mirrorEntropy: {
            formula: "S_mirror = S₀ · exp(-|Δt_ortho|/τ_mirror)",
            coupling: "Exponentially suppressed at late times"
        },

        // Total entropy
        totalEntropy: {
            formula: "S_total = S_observable + S_mirror",
            z2Symmetry: "Equal contributions at t = 0"
        },

        // Bekenstein bound
        bekenstein: {
            formula: "S ≤ 2πER/ℏc",
            role: "Maximum entropy bound"
        }
    },

    // ================================================================
    // TESTABLE PREDICTIONS
    // ================================================================

    predictions: {

        // Near-term (current/next-gen experiments)
        nearTerm: {
            w0_DESI: {
                prediction: -0.846,
                range: [-0.88, -0.81],
                experiment: "DESI Year 5",
                timeline: "2025-2027",
                status: "Consistent with DESI 2024"
            },
            wa_DESI: {
                prediction: -0.75,
                range: [-0.85, -0.65],
                experiment: "DESI + CMB-S4",
                timeline: "2025-2030",
                status: "Exact match with DESI 2024 central value"
            },
            alphaT_cosmology: {
                prediction: 2.7,
                range: [2.5, 2.9],
                experiment: "BAO + weak lensing",
                timeline: "2025-2030"
            }
        },

        // Medium-term
        mediumTerm: {
            protonDecay: {
                prediction: "> 10³⁴ years",
                channel: "p → e⁺π⁰",
                experiment: "Hyper-Kamiokande",
                timeline: "2030s"
            },
            gravitationalWaves: {
                prediction: "Modified dispersion at high frequency",
                experiment: "Einstein Telescope, LISA",
                timeline: "2030-2040"
            }
        },

        // Long-term/theoretical
        longTerm: {
            mirrorMatter: {
                prediction: "Gravitational effects only",
                signature: "Anomalous lensing without EM counterpart"
            },
            extraDimensions: {
                prediction: "KK modes at M_* ~ 10¹⁶ GeV",
                status: "Beyond current collider reach"
            }
        }
    },

    // ================================================================
    // MATHEMATICAL STRUCTURES
    // ================================================================

    mathematics: {
        // Division algebras
        divisionAlgebras: {
            R: { dim: 1, role: "Emergent thermal time" },
            C: { dim: 2, role: "Not used (no worldsheet)" },
            H: { dim: 4, role: "Quaternionic spacetime/Lorentz" },
            O: { dim: 8, role: "Octonionic internal manifold" }
        },

        // Key decomposition
        decomposition13D: "13 = 1 + 4 + 8 = R + H + O",

        // Cobordism vanishing
        cobordism: {
            spin13: 0,
            string13: 0,
            significance: "No global anomalies in 13D"
        },

        // CICY matrix for K_Pneuma
        cicyMatrix: [
            [3, 0, 1],
            [0, 3, 1],
            [1, 1, 2]
        ],
        cicyEuler: 72
    },

    // ================================================================
    // VERSION INFO
    // ================================================================

    version: {
        number: "6.0",
        codename: "Temporal Mirrors",
        date: "2025",

        keyFeatures: [
            "26D with signature (24,2)",
            "Two time dimensions",
            "Sp(2,R) gauge symmetry",
            "Z₂ mirror brane structure",
            "8 total branes (4 × 2)",
            "Effective 13D shadow"
        ]
    },

    // ================================================================
    // HELPER METHODS
    // ================================================================

    /**
     * Get formatted w₀ value with uncertainty
     */
    getW0Display(precision = 3) {
        return this.cosmology.w0.rounded.toFixed(precision);
    },

    /**
     * Get formatted α_T with Z₂ correction breakdown
     */
    getAlphaTDisplay() {
        const c = this.cosmology.alphaT;
        return `${c.base} + ${c.z2Correction} = ${c.value}`;
    },

    /**
     * Get generation formula display
     */
    getGenerationFormula(use26D = true) {
        const g = this.generations;
        return use26D ? g.formula26D : g.formula13D;
    },

    /**
     * Format a prediction with its observational comparison
     */
    formatPrediction(key) {
        const pred = this.predictions.nearTerm[key];
        if (!pred) return null;
        return {
            theory: pred.prediction,
            range: pred.range,
            status: pred.status
        };
    }
};

// Make available globally and for module systems
if (typeof window !== 'undefined') {
    window.TheoryConstants = TheoryConstants;
}
if (typeof module !== 'undefined' && module.exports) {
    module.exports = TheoryConstants;
}
