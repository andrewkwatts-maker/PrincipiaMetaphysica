/**
 * Centralized Content Templates for Principia Metaphysica
 *
 * Provides reusable content snippets, descriptions, and formatted values
 * that can be used across all pages (paper, website, beginner's guide, etc.)
 *
 * This ensures consistency: change once here, update everywhere.
 *
 * Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.
 */

// Import PM object (available globally after theory-constants-enhanced.js loads)
const getContentTemplates = () => {
  const PM = window.PM || {};

  return {
    // ========================================================================
    // META INFORMATION
    // ========================================================================
    meta: {
      title: 'Principia Metaphysica',
      latinTitle: 'Philosophiae Metaphysicae Principia Mathematica',
      subtitle: 'A First-Principles Geometric Theory',
      version: PM.meta?.version || '12.7',
      author: 'Andrew Keith Watts',
      copyright: `Copyright © 2025-2026 Andrew Keith Watts. All rights reserved.`,
      aiAttribution: 'Developed with assistance from Claude (Anthropic), Grok (xAI), and Gemini (Google).'
    },

    // ========================================================================
    // ABSTRACT / SUMMARY
    // ========================================================================
    abstract: {
      short: `A unified geometric framework deriving all 58 Standard Model parameters from a single G₂ manifold with minimal calibration (2 fitted parameters).`,

      medium: `Principia Metaphysica presents a unified geometric framework that derives all 58 Standard Model parameters from first principles. Starting from a ${PM.dimensions?.D_bulk || 26}D bulk spacetime with signature (24,2), the theory employs Sp(2,R) gauge symmetry to eliminate ghosts while preserving G₂ holonomy compactification. The framework achieves ${PM.validation?.predictions_within_1sigma || 45}/${PM.validation?.total_predictions || 48} predictions within 1σ of experimental values.`,

      full: `Principia Metaphysica (PM) establishes a unified geometric framework for deriving all Standard Model parameters from topological and geometric first principles. The theory begins with a ${PM.dimensions?.D_bulk || 26}-dimensional bulk spacetime possessing signature (24,2), incorporating two timelike dimensions. Through Sp(2,R) gauge symmetry, the framework eliminates negative-norm states while preserving the mathematical structure necessary for G₂ holonomy compactification. The Euler characteristic χ = ${PM.topology?.chi_eff || 144} yields exactly ${PM.topology?.n_gen || 3} fermion generations via the topological formula n_gen = χ/48. All quark and lepton masses emerge from b₃ = ${PM.topology?.b3 || 24} associative cycles on the G₂ manifold. The framework requires only 2 fitted parameters (VEV scale, α_GUT normalization) out of 58 total, achieving ${PM.validation?.predictions_within_1sigma || 45}/${PM.validation?.total_predictions || 48} predictions within 1σ of experiment.`
    },

    // ========================================================================
    // VALIDATION SUMMARY
    // ========================================================================
    validation: {
      successRate: `${((PM.validation?.predictions_within_1sigma / PM.validation?.total_predictions) * 100).toFixed(1)}%`,
      predictionsWithin1Sigma: PM.validation?.predictions_within_1sigma || 45,
      totalPredictions: PM.validation?.total_predictions || 48,
      exactMatches: PM.validation?.exact_matches || 12,
      overallGrade: PM.validation?.overall_grade || 'A-',

      summaryText: `${PM.validation?.predictions_within_1sigma || 45} of ${PM.validation?.total_predictions || 48} predictions agree with experiment within 1σ (${((PM.validation?.predictions_within_1sigma / PM.validation?.total_predictions) * 100).toFixed(1)}% success rate)`,

      calibration: {
        fitted: 2,
        derived: 56,
        total: 58,
        fittedList: ['VEV scale factor (1.5859)', 'α_GUT normalization'],
        note: 'Only 2 of 58 Standard Model parameters require calibration - 96.6% are derived from geometry'
      }
    },

    // ========================================================================
    // KEY PREDICTIONS (for reuse across pages)
    // ========================================================================
    predictions: {
      neutrinoHierarchy: {
        name: 'Normal Neutrino Hierarchy',
        value: 'NH with 76% confidence',
        test: 'JUNO experiment (2027)',
        status: 'pending',
        description: 'The framework predicts normal mass ordering (m₁ < m₂ < m₃) based on geometric constraints.'
      },

      kkGraviton: {
        name: 'KK Graviton Mass',
        value: `${PM.kk_graviton?.mass_TeV?.toFixed(2) || '5.00'} TeV`,
        test: 'HL-LHC (2029+)',
        status: 'pending',
        description: 'First Kaluza-Klein graviton excitation from G₂ compactification scale.'
      },

      protonDecay: {
        name: 'Proton Lifetime',
        value: `${(PM.proton_decay?.tau_p_median / 1e34).toFixed(2) || '3.87'}×10³⁴ years`,
        test: 'Hyper-Kamiokande (2032-2038)',
        status: 'pending',
        description: 'Proton decay via p → e⁺π⁰ mediated by XY gauge bosons at M_GUT.'
      },

      darkEnergy: {
        name: 'Dark Energy w₀',
        value: PM.dark_energy?.w0_PM?.toFixed(4) || '-0.8528',
        test: 'DESI DR2 (ongoing)',
        status: 'consistent',
        deviation: '0.38σ',
        description: 'Dark energy equation of state from moduli dynamics, consistent with DESI DR2.'
      },

      maximalMixing: {
        name: 'Maximal θ₂₃ Mixing',
        value: `${PM.pmns_matrix?.theta_23?.toFixed(1) || '45.0'}°`,
        test: 'NuFIT 6.0 (2025)',
        status: 'confirmed',
        description: 'Maximal atmospheric mixing from α₄ = α₅ geometric symmetry.'
      }
    },

    // ========================================================================
    // DIMENSIONAL CASCADE
    // ========================================================================
    dimensions: {
      cascade: [
        {
          dim: PM.dimensions?.D_bulk || 26,
          signature: '(24,2)',
          name: '26D Bulk',
          short: 'Bosonic string critical dimension',
          description: 'The full bulk spacetime has 24 spatial and 2 timelike dimensions, required for bosonic string consistency.'
        },
        {
          dim: PM.dimensions?.D_after_sp2r || 13,
          signature: '(12,1)',
          name: '13D Shadow',
          short: 'Sp(2,R) gauge-fixed',
          description: 'After Sp(2,R) gauge symmetry eliminates one time dimension, we obtain a 13D effective shadow with one time.'
        },
        {
          dim: 8,
          signature: '(7,1)',
          name: '8D G₂ × Time',
          short: 'G₂ manifold with time',
          description: 'The 7D G₂ holonomy manifold embedded in 8D with a single timelike direction.'
        },
        {
          dim: 6,
          signature: '(5,1)',
          name: '6D Observable Brane',
          short: 'Brane with extra dims',
          description: 'Observable brane B₁ with 5 spatial dimensions plus time, hosting the Standard Model.'
        },
        {
          dim: PM.dimensions?.D_observable || 4,
          signature: '(3,1)',
          name: '4D Spacetime',
          short: 'Our universe',
          description: 'The 3+1 dimensional world we observe, emerging from dimensional reduction.'
        }
      ],

      twoTime: {
        thermal: 't_therm - Thermal time from KMS state (experienced/physical time)',
        orthogonal: 't_ortho - Orthogonal time eliminated by Sp(2,R) gauge'
      }
    },

    // ========================================================================
    // TOPOLOGY
    // ========================================================================
    topology: {
      chi: {
        value: PM.topology?.chi_eff || 144,
        formula: 'χ_eff = 144',
        description: 'Euler characteristic of the G₂ manifold with Z₂ orbifold, yielding 3 generations via χ/48.'
      },
      b2: {
        value: PM.topology?.b2 || 4,
        description: 'Second Betti number from TCS (Twisted Connected Sum) G₂ construction.'
      },
      b3: {
        value: PM.topology?.b3 || 24,
        description: 'Third Betti number counting associative 3-cycles that determine Yukawa couplings.'
      },
      generations: {
        value: PM.topology?.n_gen || 3,
        formula: 'n_gen = χ_eff / 48 = 144 / 48 = 3',
        description: 'Three fermion generations emerge topologically from flux quantization on G₂.'
      }
    },

    // ========================================================================
    // GUT SCALE PHYSICS
    // ========================================================================
    gut: {
      mass: {
        value: PM.proton_decay?.M_GUT || 2.118e16,
        formatted: `${((PM.proton_decay?.M_GUT || 2.118e16) / 1e16).toFixed(2)}×10¹⁶ GeV`,
        description: 'Grand Unified Theory scale derived from G₂ torsion.'
      },
      alphaInverse: {
        value: PM.proton_decay?.alpha_GUT_inv || 23.54,
        description: 'Inverse GUT coupling at unification scale.'
      }
    },

    // ========================================================================
    // HIGGS SECTOR
    // ========================================================================
    higgs: {
      mass: {
        value: 125.10,
        unit: 'GeV',
        description: 'Higgs boson mass from moduli stabilization with Re(T) = 7.086.'
      },
      vev: {
        value: PM.v12_6_geometric_derivations?.vev_pneuma?.v_EW || 173.97,
        unit: 'GeV',
        description: 'Electroweak VEV derived from Pneuma field condensation.'
      }
    },

    // ========================================================================
    // NEUTRINO PHYSICS
    // ========================================================================
    neutrinos: {
      pmns: {
        theta23: {
          value: PM.pmns_matrix?.theta_23 || 45.0,
          unit: '°',
          description: 'Atmospheric mixing angle (maximal from α₄ = α₅).'
        },
        theta12: {
          value: PM.pmns_matrix?.theta_12 || 33.59,
          unit: '°',
          description: 'Solar mixing angle.'
        },
        theta13: {
          value: PM.pmns_matrix?.theta_13 || 8.57,
          unit: '°',
          description: 'Reactor mixing angle.'
        },
        deltaCP: {
          value: PM.pmns_matrix?.delta_cp || 235,
          unit: '°',
          description: 'CP-violating phase.'
        }
      },
      masses: {
        m1: PM.neutrino_mass?.m1_eV || 0.00841,
        m2: PM.neutrino_mass?.m2_eV || 0.01227,
        m3: PM.neutrino_mass?.m3_eV || 0.05018,
        sum: PM.neutrino_mass?.sum_masses_eV || 0.0709,
        unit: 'eV',
        hierarchy: 'Normal'
      }
    },

    // ========================================================================
    // EXPERIMENTAL TESTS
    // ========================================================================
    experiments: {
      nearTerm: [
        { name: 'JUNO', year: 2027, test: 'Neutrino mass hierarchy' },
        { name: 'Euclid', year: 2028, test: 'Dark energy w(z) evolution' }
      ],
      mediumTerm: [
        { name: 'HL-LHC', year: '2029+', test: 'KK graviton at 5.0 TeV' },
        { name: 'Hyper-K', year: '2032-2038', test: 'Proton decay τ_p ~ 10³⁴ years' }
      ]
    },

    // ========================================================================
    // HELPER FUNCTIONS
    // ========================================================================

    /**
     * Format a physics value with proper scientific notation
     */
    formatValue(value, options = {}) {
      const { decimals = 4, unit = '', scientific = 'auto' } = options;

      if (value === null || value === undefined) return 'N/A';

      if (scientific === 'auto') {
        if (Math.abs(value) > 1e6 || (Math.abs(value) < 0.001 && value !== 0)) {
          return `${value.toExponential(decimals)}${unit ? ' ' + unit : ''}`;
        }
      } else if (scientific) {
        return `${value.toExponential(decimals)}${unit ? ' ' + unit : ''}`;
      }

      return `${value.toFixed(decimals)}${unit ? ' ' + unit : ''}`;
    },

    /**
     * Get validation status badge HTML
     */
    getValidationBadge() {
      const v = this.validation;
      return `<span class="validation-badge grade-${v.overallGrade.replace(/[^A-Z]/g, '')}">${v.successRate} within 1σ (${v.overallGrade})</span>`;
    },

    /**
     * Get prediction status indicator
     */
    getPredictionStatus(status) {
      const icons = {
        'confirmed': '✓',
        'consistent': '≈',
        'pending': '◯',
        'failed': '✗'
      };
      return icons[status] || '?';
    }
  };
};

// Export for use in modules
if (typeof module !== 'undefined' && module.exports) {
  module.exports = { getContentTemplates };
}

// Make available globally for browser use
if (typeof window !== 'undefined') {
  window.getContentTemplates = getContentTemplates;
  window.ContentTemplates = getContentTemplates;
}
