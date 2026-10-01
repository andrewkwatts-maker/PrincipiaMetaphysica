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

// Import PM object (available globally after pm-constants-loader.js loads)
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
      version: PM.meta?.version,
      author: 'Andrew Keith Watts',
      copyright: `Copyright © 2025-2026 Andrew Keith Watts. All rights reserved.`,
      dedication: 'Dedicated to my Dearest Wife, Elizabeth May Watts & The Ruler and Restorer of all, The final Logos, The Messiah, Jesus of Nazareth'
    },

    // ========================================================================
    // ABSTRACT / SUMMARY
    // ========================================================================
    abstract: {
      short: `A geometric framework: a 26D bulk of signature (24,2), one time per 13D shadow, compactified on the G₂ manifold Y₇ (Joyce's resolution of T⁷/(ℤ/2)³, with (b₂, b₃) = (12, 43)). Some quantities are derived, others are calibrated, and several problems are open.`,

      medium: `Principia Metaphysica is a geometric framework. It starts from a ${PM.dimensions?.D_bulk}D bulk spacetime with signature (24,2): 24 space directions and 2 times, one per 13D shadow. The internal space is the compact G₂ manifold Y₇, Joyce's resolution of T⁷/(ℤ/2)³, with (b₂, b₃) = (12, 43); three generations come from n_gen = b₂/4, the number of singular involutions. Ghost control for the second time, chirality, the moduli, dark energy and flavour are open problems.`,

      full: `Principia Metaphysica (PM) is a geometric framework for the Standard Model. It begins with a ${PM.dimensions?.D_bulk}-dimensional bulk spacetime of signature (24,2): 24 space directions and two times, one per 13D shadow of signature (12,1). Ghost control for the second time is open; Bars' Sp(2,R) ghost-freedom theorem is not inherited. The internal space is Y₇, Joyce's resolution of T⁷/(ℤ/2)³, a compact 7-manifold with Betti numbers (b₂, b₃) = (12, 43) and Euler characteristic 0. Three generations come from n_gen = b₂/4, the number of singular involutions; on the K3 reading the effective index χ_eff = 2 Σ χ(K3) = 48n = 144 restates that count. Chirality, the moduli, dark energy and flavour are open, and quantities built on the retired seed b₃ = 24 are labelled calibrated.`
    },

    // ========================================================================
    // VALIDATION SUMMARY
    // ========================================================================
    validation: {
      successRate: `${((PM.validation?.predictions_within_1sigma / PM.validation?.total_predictions) * 100).toFixed(1)}%`,
      predictionsWithin1Sigma: PM.validation?.predictions_within_1sigma,
      totalPredictions: PM.validation?.total_predictions,
      exactMatches: PM.validation?.exact_matches,
      overallGrade: PM.validation?.overall_grade,

      summaryText: `${PM.validation?.predictions_within_1sigma} of ${PM.validation?.total_predictions} predictions agree with experiment within 1σ (${((PM.validation?.predictions_within_1sigma / PM.validation?.total_predictions) * 100).toFixed(1)}% success rate)`,

      calibration: {
        fitted: 2,
        derived: 56,
        total: 58,
        fittedList: ['VEV scale factor (1.5859)', 'α_GUT normalization'],
        note: 'Legacy count. Quantities built on the retired seed b₃ = 24 (the k_ℷ layer, the racetrack) are calibrated, not derived; see the free-variable ledger for the current count.'
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
        value: `${PM.kk_graviton?.mass_TeV?.toFixed(2)} TeV`,
        test: 'HL-LHC (2029+)',
        status: 'pending',
        description: 'First Kaluza-Klein graviton excitation from G₂ compactification scale.'
      },

      protonDecay: {
        name: 'Proton Lifetime',
        value: `${(PM.proton_decay?.tau_p_median / 1e34).toFixed(2)}×10³⁴ years`,
        test: 'Hyper-Kamiokande (2032-2038)',
        status: 'pending',
        description: 'Proton decay via p → e⁺π⁰ mediated by XY gauge bosons at M_GUT.'
      },

      darkEnergy: {
        name: 'Dark Energy w₀',
        value: PM.dark_energy?.w0_PM?.toFixed(4),
        test: 'DESI DR2 (ongoing)',
        status: 'consistent',
        deviation: '0.38σ',
        description: 'Dark energy equation of state w₀ = -23/24, frozen at the off-path seed b₃ = 24. The DESI DR2 w₀w_aCDM headline is w₀ = -0.752 ± 0.057, more than 3σ away; dark energy is open on the adopted path.'
      },

      maximalMixing: {
        name: 'Maximal θ₂₃ Mixing',
        value: `${PM.pmns_matrix?.theta_23?.toFixed(1)}°`,
        test: 'NuFIT 6.0 (2025)',
        status: 'confirmed',
        description: 'Maximal atmospheric mixing from the Shadow_ק = Shadow_ח symmetry, a model construct (flavour is open on the adopted path).'
      }
    },

    // ========================================================================
    // DIMENSIONAL CASCADE
    // ========================================================================
    dimensions: {
      cascade: [
        {
          dim: PM.dimensions?.D_bulk,
          signature: '(24,2)',
          name: '26D Bulk',
          short: '24 space directions and 2 times',
          description: 'The full bulk spacetime has 24 space directions and 2 times, one per 13D shadow. (The earlier claim that 26 is the critical dimension is withdrawn: the two-time critical dimension is 27-28.)'
        },
        {
          dim: PM.dimensions?.D_after_sp2r,
          signature: '(12,1)',
          name: '13D Shadow',
          short: 'One time per shadow',
          description: 'The bulk splits into two 13D shadows of signature (12,1), each carrying one of the two times; no time is shared between them.'
        },
        {
          dim: 8,
          signature: '(7,1)',
          name: '8D G₂ × Time',
          short: 'G₂ manifold with time',
          description: 'The 7D G₂ manifold Y₇ together with the shadow\'s own time direction.'
        },
        {
          dim: 6,
          signature: '(5,1)',
          name: '6D Observable Brane',
          short: 'Brane with extra dims',
          description: 'Observable brane B₁ with 5 spatial dimensions plus time, hosting the Standard Model.'
        },
        {
          dim: PM.dimensions?.D_observable,
          signature: '(3,1)',
          name: '4D Spacetime',
          short: 'Our universe',
          description: 'The 3+1 dimensional world we observe, emerging from dimensional reduction.'
        }
      ],

      twoTime: {
        thermal: 't_therm - Thermal time from KMS state (experienced/physical time)',
        orthogonal: 't_ortho - The second time, carried by the other shadow (ghost control is open)'
      }
    },

    // ========================================================================
    // TOPOLOGY
    // ========================================================================
    topology: {
      chi: {
        value: PM.topology?.chi_eff,
        formula: 'χ_eff = 144',
        description: 'Effective index on the K3 reading: χ_eff = 2 Σ χ(K3) = 48n = 144, the Kummer K3 surfaces transverse to the singular involutions, once per shadow. It is not the Euler characteristic of Y₇, which is 0.'
      },
      b2: {
        value: PM.topology?.b2,
        description: 'Second Betti number of Y₇ (Joyce\'s resolution of T⁷/(ℤ/2)³): b₂ = 12, four resolved A₁ families for each singular involution.'
      },
      b3: {
        value: PM.topology?.b3,
        description: 'Third Betti number of Y₇: b₃ = 7 + 3b₂ = 43 (7 flat plus 36 twisted). Yukawa couplings need a chiral sector, which is open.'
      },
      generations: {
        value: PM.topology?.n_gen,
        formula: 'n_gen = b₂/4 = 12/4 = 3',
        description: 'Three generations: n_gen = b₂/4, the number of singular involutions of Y₇. On the K3 reading χ_eff/48 = n restates the same count. Chirality is open.'
      }
    },

    // ========================================================================
    // GUT SCALE PHYSICS
    // ========================================================================
    gut: {
      mass: {
        value: PM.proton_decay?.M_GUT,
        formatted: `${(PM.proton_decay?.M_GUT / 1e16).toFixed(2)}×10¹⁶ GeV`,
        description: 'Grand Unified Theory scale from torsion inputs and a modulus calibrated at the off-path seed b₃ = 24 (calibrated, not derived).'
      },
      alphaInverse: {
        value: PM.proton_decay?.alpha_GUT_inv,
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
        description: 'Higgs boson mass computed with Re(T) = 7.086, calibrated at the off-path seed b₃ = 24; Re(T) is an open modulus.'
      },
      vev: {
        value: PM.v12_6_geometric_derivations?.vev_pneuma?.v_EW,
        unit: 'GeV',
        description: 'Electroweak VEV from Pneuma field condensation, calibrated at the off-path seed b₃ = 24 (the k_ℷ layer).'
      }
    },

    // ========================================================================
    // NEUTRINO PHYSICS
    // ========================================================================
    neutrinos: {
      pmns: {
        theta23: {
          value: PM.pmns_matrix?.theta_23,
          unit: '°',
          description: 'Atmospheric mixing angle (maximal from Shadow_ק = Shadow_ח).'
        },
        theta12: {
          value: PM.pmns_matrix?.theta_12,
          unit: '°',
          description: 'Solar mixing angle.'
        },
        theta13: {
          value: PM.pmns_matrix?.theta_13,
          unit: '°',
          description: 'Reactor mixing angle.'
        },
        deltaCP: {
          value: PM.pmns_matrix?.delta_cp,
          unit: '°',
          description: 'CP-violating phase.'
        }
      },
      masses: {
        m1: PM.neutrino_mass?.m1_eV,
        m2: PM.neutrino_mass?.m2_eV,
        m3: PM.neutrino_mass?.m3_eV,
        sum: PM.neutrino_mass?.sum_masses_eV,
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
