/**
 * Centralized Formula Database - Principia Metaphysica
 * Copyright (c) 2025 Andrew Keith Watts. All rights reserved.
 *
 * Single source of truth for all formulas used across the website.
 * Provides hover tooltips and consistent notation.
 */

const FORMULA_DATABASE = {
    // ============================================================================
    // SCALES & FUNDAMENTAL CONSTANTS (Most frequently used)
    // ============================================================================

    'M_Planck': {
        id: 'M_Planck',
        symbol: 'M<sub>Pl</sub>',
        htmlSymbol: 'M<sub>Pl</sub>',
        textSymbol: 'M_Pl',
        pmRef: null, // TODO: Add M_Planck to theory_output.json
        description: '4D reduced Planck mass',
        longDescription: 'Reduced Planck mass in 4D spacetime, defined as M_Pl² = 1/(8πG_N)',
        category: 'scales',
        occurrences: 120,
        usedIn: ['all'],
        foundational: true
    },

    'M_star': {
        id: 'M_star',
        symbol: 'M<sub>*</sub>',
        htmlSymbol: 'M<sub>*</sub>',
        textSymbol: 'M_*',
        pmRef: null, // TODO: Add M_star to theory_output.json
        description: 'Fundamental 26D mass scale',
        longDescription: 'Fundamental mass scale in 26D bulk spacetime before dimensional reduction',
        category: 'scales',
        formula: 'M<sub>*</sub><sup>24</sup> ≡ M<sub>Pl</sub><sup>2</sup> / V<sub>internal</sub>',
        occurrences: 91,
        usedIn: ['geometric-framework', 'cosmology', 'gauge-unification', 'thermal-time', 'pneuma-lagrangian', 'einstein-hilbert', 'paper'],
        foundational: true
    },

    'M_GUT': {
        id: 'M_GUT',
        symbol: 'M<sub>GUT</sub>',
        htmlSymbol: 'M<sub>GUT</sub>',
        textSymbol: 'M_GUT',
        pmRef: 'PM.gauge.M_GUT',
        description: 'Grand unified scale',
        longDescription: 'GUT scale derived geometrically from G₂ manifold TCS torsion',
        category: 'scales',
        formula: 'M<sub>GUT</sub> = M<sub>*</sub> exp(T<sub>ω</sub>s/2)',
        derivation: 'Geometric from twisted connected sum (TCS) G₂ torsion, not fitted',
        occurrences: 112,
        usedIn: ['gauge-unification', 'predictions', 'fermion-sector', 'geometric-framework', 'paper'],
        foundational: true
    },

    // ============================================================================
    // DARK ENERGY & COSMOLOGY
    // ============================================================================

    'w0': {
        id: 'w0',
        symbol: 'w<sub>0</sub>',
        htmlSymbol: 'w<sub>0</sub>',
        textSymbol: 'w_0',
        pmRef: 'PM.dark_energy.w0',
        description: 'Dark energy equation of state today',
        longDescription: 'Present-day equation of state parameter derived from effective dimension D_eff = 12.589 (0.01% error - perfect match with DESI DR2)',
        category: 'cosmology',
        formula: 'w<sub>0</sub> = -1 + 2/(3D<sub>eff</sub>)',
        experimental: 'DESI DR2: -0.8527 ± 0.06 (0.00σ - EXACT match)',
        occurrences: 123,
        usedIn: ['cosmology', 'predictions', 'thermal-time', 'paper'],
        validated: true,
        exactMatch: true
    },

    'wz_evolution': {
        id: 'wz_evolution',
        symbol: 'w(z)',
        htmlSymbol: 'w(z)',
        textSymbol: 'w(z)',
        pmRef: 'PM.dark_energy.w0',
        description: 'Redshift evolution of dark energy',
        longDescription: 'Logarithmic evolution derived from frozen modular time dimension at z > 3000',
        category: 'cosmology',
        formula: 'w(z) = w<sub>0</sub>[1 + (α<sub>T</sub>/3)ln(1+z)]',
        explanation: 'Frozen at z > 3000, preferred over CPL at 6.2σ',
        occurrences: 76,
        usedIn: ['cosmology', 'thermal-time', 'predictions', 'paper'],
        validated: true
    },

    'w_a': {
        id: 'w_a',
        symbol: 'w<sub>a</sub>',
        htmlSymbol: 'w<sub>a</sub>',
        textSymbol: 'w_a',
        pmRef: 'PM.dark_energy.wa',
        description: 'Dark energy evolution derivative',
        longDescription: 'First derivative w_a = dw/d(ln a), theory predicts -0.95',
        category: 'cosmology',
        formula: 'w<sub>a</sub> = w<sub>0</sub>α<sub>T</sub>/3 = -0.95',
        experimental: 'DESI DR2: -0.75 ± 0.30 (0.66σ agreement)',
        occurrences: 34,
        usedIn: ['cosmology', 'predictions', 'paper'],
        validated: true
    },

    // ============================================================================
    // ACTIONS
    // ============================================================================

    'S_26D': {
        id: 'S_26D',
        symbol: 'S<sub>26D</sub>',
        htmlSymbol: 'S<sub>26D</sub>',
        textSymbol: 'S_26D',
        description: '26D master action',
        longDescription: 'Complete 26-dimensional bulk action before Sp(2,R) gauge fixing',
        category: 'actions',
        formula: 'S<sub>26D</sub> = ∫ d<sup>26</sup>x √|G| [M<sub>*</sub><sup>24</sup>R<sub>26</sub> + Ψ̄<sub>P</sub>(iΓ<sup>M</sup>D<sub>M</sub> - m)Ψ<sub>P</sub> + ℒ<sub>Sp(2,R)</sub>]',
        occurrences: 15,
        usedIn: ['geometric-framework', 'pneuma-lagrangian', 'paper'],
        foundational: true
    },

    'S_13D': {
        id: 'S_13D',
        symbol: 'S<sub>13D</sub>',
        htmlSymbol: 'S<sub>13D</sub>',
        textSymbol: 'S_13D',
        description: '13D effective action',
        longDescription: '13D effective action after Sp(2,R) gauge fixing',
        category: 'actions',
        formula: 'S<sub>13D</sub> = ∫ d<sup>13</sup>x √|g| [M<sub>*</sub><sup>24</sup>R<sub>13</sub> + Ψ̄(iΓ<sup>μ</sup>D<sub>μ</sub>)Ψ + ℒ<sub>gauge</sub>]',
        occurrences: 12,
        usedIn: ['geometric-framework', 'einstein-hilbert', 'paper'],
        foundational: true
    },

    // ============================================================================
    // NEUTRINO MIXING (PMNS MATRIX)
    // ============================================================================

    'theta_12': {
        id: 'theta_12',
        symbol: 'θ<sub>12</sub>',
        htmlSymbol: 'θ<sub>12</sub>',
        textSymbol: 'theta_12',
        pmRef: 'PM.neutrino.pmns_angles.theta_12.predicted',
        description: 'Solar neutrino mixing angle',
        longDescription: 'PMNS solar angle from G₂ associative cycle geometry',
        category: 'neutrinos',
        experimental: 'NuFIT 6.0: 33.41° ± 0.75° (0.24σ agreement)',
        occurrences: 18,
        usedIn: ['fermion-sector', 'predictions', 'paper'],
        validated: true
    },

    'theta_23': {
        id: 'theta_23',
        symbol: 'θ<sub>23</sub>',
        htmlSymbol: 'θ<sub>23</sub>',
        textSymbol: 'theta_23',
        pmRef: 'PM.neutrino.pmns_angles.theta_23.predicted',
        description: 'Atmospheric neutrino mixing angle',
        longDescription: 'PMNS atmospheric angle - EXACT MATCH with experiment (NuFIT 6.0 confirms maximal mixing)',
        category: 'neutrinos',
        experimental: 'NuFIT 6.0: 45.0° (0.00σ - EXACT)',
        occurrences: 19,
        usedIn: ['fermion-sector', 'predictions', 'paper'],
        validated: true,
        exactMatch: true
    },

    'theta_13': {
        id: 'theta_13',
        symbol: 'θ<sub>13</sub>',
        htmlSymbol: 'θ<sub>13</sub>',
        textSymbol: 'theta_13',
        pmRef: 'PM.neutrino.pmns_angles.theta_13.predicted',
        description: 'Reactor neutrino mixing angle',
        longDescription: 'PMNS reactor angle - EXACT MATCH with experiment',
        category: 'neutrinos',
        experimental: 'NuFIT 6.0: 8.57° (0.00σ - EXACT)',
        occurrences: 17,
        usedIn: ['fermion-sector', 'predictions', 'paper'],
        validated: true,
        exactMatch: true
    },

    'delta_CP': {
        id: 'delta_CP',
        symbol: 'δ<sub>CP</sub>',
        htmlSymbol: 'δ<sub>CP</sub>',
        textSymbol: 'delta_CP',
        pmRef: 'PM.neutrino.pmns_angles.delta_cp.predicted',
        description: 'Neutrino CP-violating phase',
        longDescription: 'PMNS CP phase from associative 3-cycle phases',
        category: 'neutrinos',
        experimental: 'NuFIT 6.0: 197° ± 30° (0.09σ agreement)',
        occurrences: 16,
        usedIn: ['fermion-sector', 'predictions', 'paper'],
        validated: true
    },

    // ============================================================================
    // PROTON DECAY
    // ============================================================================

    'tau_p': {
        id: 'tau_p',
        symbol: 'τ<sub>p</sub>',
        htmlSymbol: 'τ<sub>p</sub>',
        textSymbol: 'tau_p',
        pmRef: 'PM.proton_decay.tau_p_years',
        description: 'Proton lifetime',
        longDescription: 'Geometric prediction for proton decay lifetime from SO(10) GUT via dimension-6 operators with suppression factor S² = 2.1',
        category: 'predictions',
        experimental: 'Super-K: > 1.67 × 10³⁴ years (consistent)',
        formula: 'τ<sub>p</sub> = M<sub>GUT</sub><sup>4</sup>/(α<sub>GUT</sub><sup>2</sup> m<sub>p</sub><sup>5</sup>) × S<sup>2</sup>',
        occurrences: 23,
        usedIn: ['predictions', 'gauge-unification', 'fermion-sector', 'paper'],
        prediction: true
    },

    'BR_epi0': {
        id: 'BR_epi0',
        symbol: 'BR(p→e<sup>+</sup>π<sup>0</sup>)',
        htmlSymbol: 'BR(p→e<sup>+</sup>π<sup>0</sup>)',
        textSymbol: 'BR(p->e+pi0)',
        pmRef: 'PM.proton_decay.BR_epi0',
        description: 'Proton decay branching ratio to e+π0',
        longDescription: 'Branching ratio derived from CKM rotation + geometric Yukawa mixing',
        category: 'predictions',
        formula: 'BR = |C<sub>eπ0</sub>|<sup>2</sup> / Σ|C<sub>i</sub>|<sup>2</sup>',
        experimental: 'Testable by Hyper-K (2027-2035)',
        occurrences: 14,
        usedIn: ['predictions', 'fermion-sector', 'paper'],
        prediction: true
    },

    // ============================================================================
    // GENERATION COUNT
    // ============================================================================

    'n_gen': {
        id: 'n_gen',
        symbol: 'n<sub>gen</sub>',
        htmlSymbol: 'n<sub>gen</sub>',
        textSymbol: 'n_gen',
        pmRef: 'PM.topology.n_gen',
        description: 'Number of fermion generations',
        longDescription: 'Derived from effective Euler characteristic: n_gen = χ_eff / 48 = 144 / 48 = 3',
        category: 'topology',
        formula: 'n<sub>gen</sub> = χ<sub>eff</sub> / 48 = 144 / 48 = 3',
        experimental: 'Standard Model: 3 generations (EXACT)',
        occurrences: 45,
        usedIn: ['geometric-framework', 'fermion-sector', 'predictions', 'paper'],
        validated: true,
        exactMatch: true
    },

    // ============================================================================
    // LATTICE DISPERSION (v16.0)
    // ============================================================================

    'delta_lat': {
        id: 'delta_lat',
        symbol: 'δ<sub>lat</sub>',
        htmlSymbol: 'δ<sub>lat</sub>',
        textSymbol: 'δ_lat',
        pmRef: 'PM.lattice_dispersion.delta_lat',
        description: 'Lattice configuration dispersion',
        longDescription: 'Modulates geometric coupling based on lattice-level realization of G₂ holonomy in physical systems. Baseline δ_lat = 1.0 (perfect embedding), range [0.7, 1.5]',
        category: 'coupling',
        formula: 'δ<sub>lat</sub> ∈ [0.7, 1.5]',
        explanation: 'Structural parameter acknowledging imperfect geometric embedding',
        occurrences: 1,
        usedIn: ['pneuma-lagrangian', 'paper'],
        structural: true
    },

    'g_eff': {
        id: 'g_eff',
        symbol: 'g<sub>eff</sub>',
        htmlSymbol: 'g<sub>eff</sub>',
        textSymbol: 'g_eff',
        pmRef: 'PM.lattice_dispersion.g_eff_formula',
        description: 'Effective geometric coupling',
        longDescription: 'Geometric coupling modulated by lattice dispersion: g_eff = g_geom × δ_lat. Accounts for imperfect G₂ holonomy realization in physical lattices.',
        category: 'coupling',
        formula: 'g<sub>eff</sub> = g<sub>geom</sub> × δ<sub>lat</sub>',
        derivation: 'Modulated from base g_geom = 0.1 by δ_lat ∈ [0.7, 1.5]',
        occurrences: 1,
        usedIn: ['pneuma-lagrangian', 'paper'],
        structural: true
    },

    'alpha_evo': {
        id: 'alpha_evo',
        symbol: 'α<sub>evo</sub>',
        htmlSymbol: 'α<sub>evo</sub>',
        textSymbol: 'α_evo',
        pmRef: 'PM.lattice_dispersion.alpha_evo',
        description: 'Evolutionary orchestration factor',
        longDescription: 'Measures degree of evolutionary enhancement from baseline: α_evo = (δ_lat - 1) / (δ_lat_max - 1) ∈ [0, 1]. SPECULATIVE appendix material.',
        category: 'speculative',
        formula: 'α<sub>evo</sub> = (δ<sub>lat</sub> - 1) / (δ<sub>lat,max</sub> - 1)',
        explanation: 'Quantifies evolutionary optimization of lattice configuration',
        occurrences: 1,
        usedIn: ['appendix', 'paper'],
        speculative: true
    },

    // ============================================================================
    // SUBLEADING DISPERSION (v16.1)
    // ============================================================================

    'epsilon_atm': {
        id: 'epsilon_atm',
        symbol: 'ε<sub>atm</sub>',
        htmlSymbol: 'ε<sub>atm</sub>',
        textSymbol: 'ε_atm',
        pmRef: 'PM.subleading_dispersion.epsilon_atm',
        description: 'Atmospheric mixing deviation',
        longDescription: 'Subleading correction to maximal θ₂₃ mixing. θ₂₃ = 45° × (1 + ε_atm). Default 0, range ±0.05 allows 42.75°-47.25°.',
        category: 'subleading',
        formula: 'θ<sub>23</sub> = 45° × (1 + ε<sub>atm</sub>)',
        explanation: 'Flux perturbation or Ricci-flow asymmetry',
        occurrences: 1,
        usedIn: ['neutrino', 'predictions', 'paper'],
        defaultZero: true
    },

    'phi_cp': {
        id: 'phi_cp',
        symbol: 'φ<sub>CP</sub>',
        htmlSymbol: 'φ<sub>CP</sub>',
        textSymbol: 'φ_CP',
        pmRef: 'PM.subleading_dispersion.phi_cp_offset',
        description: 'CP phase dispersion offset',
        longDescription: 'Allows continuous offset from central δ_CP = 235° OR discrete selection from {194°, 235°, 286°} via Z_n automorphisms.',
        category: 'subleading',
        formula: 'δ<sub>CP</sub> = 235° + φ<sub>CP</sub> or {194°, 235°, 286°}',
        explanation: 'Z_n automorphisms of G₂ cycle graph',
        occurrences: 1,
        usedIn: ['neutrino', 'predictions', 'paper'],
        defaultZero: true
    },

    'delta_race': {
        id: 'delta_race',
        symbol: 'δ<sub>race</sub>',
        htmlSymbol: 'δ<sub>race</sub>',
        textSymbol: 'δ_race',
        pmRef: 'PM.subleading_dispersion.delta_race',
        description: 'Racetrack coefficient offset',
        longDescription: 'Integer offset for second racetrack coefficient: N_second = 25 + δ_race ∈ {24, 25, 26}.',
        category: 'subleading',
        formula: 'N<sub>second</sub> = 25 + δ<sub>race</sub>',
        explanation: 'Landscape statistics allow nearby integer fluxes',
        occurrences: 1,
        usedIn: ['racetrack', 'dark-matter', 'paper'],
        defaultZero: true
    },

    'delta_gamma': {
        id: 'delta_gamma',
        symbol: 'Δγ',
        htmlSymbol: 'Δγ',
        textSymbol: 'Δγ',
        pmRef: 'PM.subleading_dispersion.delta_gamma',
        description: 'Ghost correction uncertainty',
        longDescription: 'Uncertainty in ghost correction factor γ = 0.5 ± Δγ. Propagates to w₀ band.',
        category: 'subleading',
        formula: 'γ = 0.5 ± Δγ → w<sub>0</sub> band',
        explanation: 'Quantum volume and loop corrections',
        occurrences: 1,
        usedIn: ['cosmology', 'dark-energy', 'paper'],
        defaultZero: true
    },

    // ============================================================================
    // AXION PHYSICS (v18.3)
    // ============================================================================

    'f_a': {
        id: 'f_a',
        symbol: 'f<sub>a</sub>',
        htmlSymbol: 'f<sub>a</sub>',
        textSymbol: 'f_a',
        pmRef: 'PM.axion.f_a',
        description: 'Axion decay constant from G2 geometry',
        longDescription: 'Axion decay constant derived from Planck scale with k_gimel^6 suppression. Places f_a in the anthropic window for dark matter.',
        category: 'dark_matter',
        formula: 'f<sub>a</sub> = M<sub>Pl</sub> / k<sub>ג</sub><sup>6</sup> ≈ 3.5×10<sup>12</sup> GeV',
        derivation: 'Geometric from G2 holonomy warp factor k_gimel = 12 + 1/π',
        occurrences: 5,
        usedIn: ['dark-matter', 'predictions', 'paper'],
        validated: false,
        predicted: true
    },

    'm_a': {
        id: 'm_a',
        symbol: 'm<sub>a</sub>',
        htmlSymbol: 'm<sub>a</sub>',
        textSymbol: 'm_a',
        pmRef: 'PM.axion.m_a',
        description: 'QCD axion mass',
        longDescription: 'Axion mass from QCD instanton dynamics. For f_a ~ 3.5e12 GeV, m_a ~ 1.6 μeV, within ADMX detection range.',
        category: 'dark_matter',
        formula: 'm<sub>a</sub> = 5.7 μeV × (10<sup>12</sup> GeV / f<sub>a</sub>) ≈ 1.6 μeV',
        experimental: 'ADMX probing 2-10 μeV range',
        occurrences: 4,
        usedIn: ['dark-matter', 'predictions', 'paper'],
        validated: false,
        predicted: true
    },

    'Omega_a': {
        id: 'Omega_a',
        symbol: 'Ω<sub>a</sub>h²',
        htmlSymbol: 'Ω<sub>a</sub>h²',
        textSymbol: 'Omega_a h^2',
        pmRef: 'PM.axion.omega_h2',
        description: 'Axion relic density',
        longDescription: 'Axion contribution to dark matter from misalignment mechanism. Natural θ_i ~ 1 gives Ω_a h² ~ 0.4, potentially explaining 100% of DM.',
        category: 'dark_matter',
        formula: 'Ω<sub>a</sub>h² = 0.12 × (f<sub>a</sub>/10<sup>12</sup>)<sup>1.167</sup> × θ<sub>i</sub>²',
        experimental: 'Planck 2018: Ω_DM h² = 0.120 ± 0.001',
        occurrences: 3,
        usedIn: ['dark-matter', 'cosmology', 'predictions', 'paper'],
        validated: false,
        predicted: true
    },

    // ============================================================================
    // YUKAWA TEXTURES (v18.3)
    // ============================================================================

    'lambda_yukawa': {
        id: 'lambda_yukawa',
        symbol: 'λ',
        htmlSymbol: 'λ',
        textSymbol: 'lambda',
        pmRef: 'PM.yukawa.lambda_eff',
        description: 'Yukawa suppression factor',
        longDescription: 'Inter-generation Yukawa suppression factor. Golden Ratio φ ~ 1.618 provides best fit to observed fermion mass hierarchy.',
        category: 'fermion',
        formula: 'm<sub>n</sub> = v × λ<sup>-N</sup>, λ = φ ≈ 1.618',
        derivation: 'Geometric from G2 wavefunction overlap analysis',
        occurrences: 6,
        usedIn: ['fermion-sector', 'predictions', 'paper'],
        validated: true
    },

    'yukawa_matrix': {
        id: 'yukawa_matrix',
        symbol: 'Y',
        htmlSymbol: 'Y',
        textSymbol: 'Y',
        pmRef: null,
        description: 'Diagonal Yukawa texture matrix',
        longDescription: 'Diagonal Yukawa matrix from G2 wavefunction overlaps. Third generation O(1), lighter generations geometrically suppressed.',
        category: 'fermion',
        formula: 'Y = diag(λ<sup>-2</sup>, λ<sup>-1</sup>, 1)',
        derivation: 'G2 holonomy localizes 3rd generation at singular point',
        occurrences: 4,
        usedIn: ['fermion-sector', 'paper'],
        structural: true
    }
};

/**
 * Get formula data by ID
 */
function getFormula(formulaId) {
    return FORMULA_DATABASE[formulaId] || null;
}

/**
 * Format formula for display with hover tooltip
 */
function formatFormula(formulaId, options = {}) {
    const formula = getFormula(formulaId);
    if (!formula) return '';

    const {
        displayValue = true,
        displayDescription = true,
        className = 'formula-hover',
        useHtmlSymbol = true
    } = options;

    const symbol = useHtmlSymbol ? formula.htmlSymbol : formula.textSymbol;
    const value = formula.computedValue ? ` = ${formula.computedValue}` : '';
    const description = formula.description;

    return `<span class="${className}" data-formula-id="${formulaId}" title="${description}${displayValue && value ? value : ''}">${symbol}</span>`;
}

/**
 * Initialize formula tooltips
 */
function initFormulaTooltips() {
    // This will be called when PM constants are loaded
    if (typeof PM !== 'undefined') {
        // Populate any dynamic values from PM constants
        Object.keys(FORMULA_DATABASE).forEach(key => {
            const formula = FORMULA_DATABASE[key];
            if (formula.pmRef) {
                const pmValue = getPMValue(formula.pmRef);
                if (pmValue !== null && pmValue !== undefined) {
                    formula.computedValue = pmValue;
                }
            }
        });
    }

    console.log(`Formula database loaded: ${Object.keys(FORMULA_DATABASE).length} formulas`);
}

/**
 * Helper to get PM constant value from reference string
 */
function getPMValue(pmRef) {
    if (typeof PM === 'undefined') return null;

    const parts = pmRef.replace('PM.', '').split('.');
    let value = PM;

    for (const part of parts) {
        if (value && typeof value === 'object' && part in value) {
            value = value[part];
        } else {
            return null;
        }
    }

    return typeof value === 'object' ? value.value : value;
}

// Initialize on DOM load
if (typeof document !== 'undefined') {
    document.addEventListener('DOMContentLoaded', initFormulaTooltips);
}

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { FORMULA_DATABASE, getFormula, formatFormula };
}
