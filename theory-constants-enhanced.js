/**
 * Principia Metaphysica - Enhanced Theory Constants with Metadata
 * ================================================================
 *
 * AUTO-GENERATED - DO NOT EDIT MANUALLY
 *
 * Each constant includes:
 * - value: The actual number
 * - display: Formatted display string
 * - unit: Physical units
 * - formula: Mathematical derivation
 * - derivation: Physical explanation
 * - uncertainty: Error bars / confidence intervals
 * - experimental_value: Observed data (if available)
 * - agreement_sigma: σ deviation from experiment
 * - source: Config parameter or simulation that produced it
 * - references: Citations
 * - testable: Future experiments
 *
 * Usage: Hover over any .pm-value element to see full metadata
 *
 * Copyright (c) 2025 Andrew Keith Watts. All rights reserved.
 */

const PM = {
  "meta": {
    "version": "7.0",
    "last_updated": "2025-12-03",
    "description": "Enhanced theory constants with full metadata",
    "has_metadata": true,
    "hover_enabled": true
  },
  "dimensions": {
    "D_bulk": {
      "value": 26.0,
      "unit": "dimensions",
      "display": "26",
      "description": "Bosonic string critical dimension",
      "formula": "D = 26 from Virasoro anomaly cancellation",
      "derivation": "String theory consistency",
      "source": "fundamental",
      "references": [
        "Polchinski Vol 1"
      ]
    },
    "D_after_sp2r": {
      "value": 13.0,
      "unit": "dimensions",
      "display": "13",
      "description": "After Sp(2,R) gauge fixing",
      "formula": "26D \u2192 13D shadow via two-time projection",
      "derivation": "Sp(2,R) gauge symmetry",
      "source": "geometric",
      "references": [
        "Bars 2000"
      ]
    }
  },
  "topology": {
    "chi_eff": {
      "value": 144.0,
      "unit": "dimensionless",
      "display": "144",
      "description": "Effective Euler characteristic",
      "formula": "\u03c7_eff = 144 from TCS G\u2082 construction",
      "derivation": "Flux quantization on TCS manifold",
      "source": "geometric",
      "references": [
        "Corti et al 2013"
      ]
    },
    "b3": {
      "value": 24.0,
      "unit": "dimensionless",
      "display": "24",
      "description": "Number of coassociative 4-cycles",
      "formula": "b\u2083 = 24 from TCS matching",
      "derivation": "G\u2082 cohomology",
      "source": "geometric",
      "references": [
        "CHNP 2018"
      ]
    },
    "n_gen": {
      "value": 3.0,
      "unit": "generations",
      "display": "3",
      "description": "Number of fermion generations",
      "formula": "n_gen = \u03c7_eff / 48 = 144 / 48",
      "derivation": "Index theorem on G\u2082 manifold",
      "source": "geometric:exact",
      "experimental_value": 3,
      "experimental_source": "PDG 2024",
      "agreement_sigma": 0.0,
      "agreement_text": "EXACT MATCH",
      "references": [
        "PDG 2024"
      ]
    }
  },
  "shared_dimensions": {
    "alpha_4": {
      "value": 0.955732,
      "unit": "dimensionless",
      "display": "0.956",
      "uncertainty": 0.01,
      "description": "4th dimension coupling strength",
      "formula": "From TCS torsion: (\u03a3+\u0394)/2 with \u03a3=1.178, \u0394=0.733",
      "derivation": "G\u2082 torsion logarithms + \u03b8\u2082\u2083 matching",
      "source": "geometric",
      "references": [
        "PM Section 3.7a"
      ]
    },
    "alpha_5": {
      "value": 0.222399,
      "unit": "dimensionless",
      "display": "0.222",
      "uncertainty": 0.01,
      "description": "5th dimension coupling strength",
      "formula": "From TCS torsion: (\u03a3-\u0394)/2 with \u03a3=1.178, \u0394=0.733",
      "derivation": "G\u2082 torsion logarithms + \u03b8\u2082\u2083 matching",
      "source": "geometric",
      "references": [
        "PM Section 3.7a"
      ]
    },
    "d_eff": {
      "value": 12.5890655,
      "unit": "dimensions",
      "display": "12.589",
      "uncertainty": 0.01,
      "description": "Effective quantum-corrected dimension",
      "formula": "D_eff = 12 + 0.5\u00d7(\u03b1\u2084+\u03b1\u2085)",
      "derivation": "Shared dimension coupling + quantum corrections",
      "source": "geometric",
      "references": [
        "PM Section 6"
      ]
    }
  },
  "proton_decay": {
    "M_GUT": {
      "value": 2.1180954475766468e+16,
      "unit": "GeV",
      "display": "2.118\u00d710\u00b9\u2076",
      "uncertainty": 0.0,
      "uncertainty_percent": 0.0,
      "description": "Grand Unification scale",
      "formula": "M_GUT = M_base \u00d7 (1 + c_warp \u00d7 s)",
      "derivation": "TCS G\u2082 torsion logarithms: T_\u03c9=-0.884, s=1.178, c_warp=0.15",
      "source": "simulation:proton_decay_rg_hybrid",
      "references": [
        "Acharya-Witten 2001",
        "PM Section 3.7a"
      ]
    },
    "tau_p_median": {
      "value": 3.764188689612127e+34,
      "unit": "years",
      "display": "3.84\u00d710\u00b3\u2074",
      "uncertainty_lower": 2.479137899634815e+34,
      "uncertainty_upper": 5.509450111901326e+34,
      "uncertainty_oom": 0.17563480615789856,
      "confidence_level": "68%",
      "description": "Proton lifetime (Monte Carlo median)",
      "formula": "\u03c4_p = 3.82\u00d710\u00b3\u00b3 \u00d7 (M_GUT/10\u00b9\u2076)\u2074 \u00d7 (0.03/\u03b1_GUT)\u00b2",
      "derivation": "Monte Carlo (1000 samples) with 3-loop RG + KK thresholds",
      "source": "simulation:proton_decay_rg_hybrid",
      "experimental_bound": 1.67e+34,
      "experimental_source": "Super-K 2024",
      "agreement": "2.3\u00d7 above bound",
      "testable": "Hyper-K 2030s",
      "references": [
        "PDG 2024",
        "Super-K Collaboration"
      ]
    },
    "uncertainty_oom": {
      "value": 0.17563480615789856,
      "unit": "OOM",
      "display": "0.177",
      "description": "Proton decay uncertainty in orders of magnitude",
      "formula": "OOM = log\u2081\u2080(upper_68/lower_68) / 2",
      "derivation": "Monte Carlo 68% confidence interval width",
      "source": "simulation:proton_decay_rg_hybrid",
      "references": [
        "PM v7.0: 4.5\u00d7 improvement from 0.8 OOM"
      ]
    }
  },
  "pmns_matrix": {
    "theta_23": {
      "value": 47.199999,
      "unit": "degrees",
      "display": "47.20\u00b0",
      "uncertainty": 0.7863313041227135,
      "description": "Atmospheric mixing angle",
      "formula": "\u03b8\u2082\u2083 = 45\u00b0 + (\u03b1\u2084 - \u03b1\u2085) \u00d7 n_gen",
      "derivation": "Asymmetric coupling to shared extra dimensions",
      "source": "geometric",
      "experimental_value": 47.2,
      "experimental_uncertainty": 2.0,
      "experimental_source": "NuFIT 5.2 (2024)",
      "agreement_sigma": 5.00000002290335e-07,
      "agreement_text": "EXACT MATCH",
      "testable": "JUNO 2028, Hyper-K 2030s",
      "references": [
        "NuFIT 5.2"
      ]
    },
    "theta_12": {
      "value": 33.59329049922625,
      "unit": "degrees",
      "display": "33.59\u00b0",
      "uncertainty": 1.2155703063401921,
      "description": "Solar mixing angle",
      "formula": "\u03b8\u2081\u2082 = arcsin(1/\u221a3 \u00d7 |1 + \u03b4_pert|)",
      "derivation": "Tri-bimaximal mixing + G\u2082 cycle perturbation",
      "source": "geometric",
      "experimental_value": 33.41,
      "experimental_uncertainty": 0.75,
      "experimental_source": "NuFIT 5.2 (2024)",
      "agreement_sigma": 0.2443873323016703,
      "agreement_text": "Excellent (0.24\u03c3)",
      "testable": "JUNO 2028",
      "references": [
        "NuFIT 5.2"
      ]
    },
    "theta_13": {
      "value": 8.568979552196335,
      "unit": "degrees",
      "display": "8.57\u00b0",
      "uncertainty": 0.3545458207495298,
      "description": "Reactor mixing angle",
      "formula": "\u03b8\u2081\u2083 = arctan(b\u2082/b\u2083 \u00d7 exp(-\u03bd/n_gen))",
      "derivation": "G\u2082 cycle intersection asymmetry",
      "source": "geometric",
      "experimental_value": 8.57,
      "experimental_uncertainty": 0.12,
      "experimental_source": "NuFIT 5.2 (2024)",
      "agreement_sigma": 0.008503731697206973,
      "agreement_text": "EXACT MATCH",
      "testable": "JUNO 2028",
      "references": [
        "NuFIT 5.2"
      ]
    },
    "delta_cp": {
      "value": 235.0,
      "unit": "degrees",
      "display": "235.0",
      "uncertainty": 28.720686017549347,
      "description": "CP-violating phase",
      "formula": "\u03b4_CP from complex phase of cycle overlaps",
      "derivation": "G\u2082 complex structure modulus + optional moonshine",
      "source": "geometric",
      "experimental_value": 232.0,
      "experimental_uncertainty": 30.0,
      "experimental_source": "NuFIT 5.2 (2024)",
      "agreement_sigma": 0.1,
      "agreement_text": "Excellent (0.10\u03c3)",
      "testable": "DUNE 2028-2032",
      "references": [
        "NuFIT 5.2"
      ]
    },
    "avg_sigma": {
      "value": 0.08822289099971989,
      "unit": "\u03c3",
      "display": "0.09",
      "description": "Average deviation from NuFIT across all 4 parameters",
      "formula": "Average of |\u03b8_theory - \u03b8_exp| / \u03c3_exp",
      "derivation": "Geometric predictions vs NuFIT 5.2",
      "source": "simulation:pmns_full_matrix",
      "agreement_text": "Exceptional agreement (2 exact matches)",
      "references": [
        "NuFIT 5.2"
      ]
    },
    "delta_CP": {
      "value": 235.0,
      "unit": "degrees",
      "display": "235.0",
      "uncertainty": 28.720686017549347,
      "description": "CP-violating phase",
      "formula": "\u03b4_CP from complex phase of cycle overlaps",
      "derivation": "G\u2082 complex structure modulus + optional moonshine",
      "source": "geometric",
      "experimental_value": 232.0,
      "experimental_uncertainty": 30.0,
      "experimental_source": "NuFIT 5.2 (2024)",
      "agreement_sigma": 0.1,
      "agreement_text": "Excellent (0.10\u03c3)",
      "testable": "DUNE 2028-2032",
      "references": [
        "NuFIT 5.2"
      ]
    }
  },
  "dark_energy": {
    "w0_PM": {
      "value": -0.8528221355508132,
      "unit": "dimensionless",
      "display": "-0.853",
      "uncertainty": 0.001,
      "description": "Dark energy equation of state at z=0",
      "formula": "w\u2080 = -(D_eff - 1) / (D_eff + 1)",
      "derivation": "Maximum Entropy Principle with D_eff=12.589",
      "source": "geometric",
      "experimental_value": -0.83,
      "experimental_uncertainty": 0.06,
      "experimental_source": "DESI DR2 (Oct 2024)",
      "agreement_sigma": 0.38036892584688753,
      "agreement_text": "Excellent (0.38\u03c3)",
      "testable": "Euclid 2027-2028",
      "references": [
        "arXiv:2510.12627"
      ]
    },
    "wa_PM_effective": {
      "value": -0.9475801506120145,
      "unit": "dimensionless",
      "display": "-0.95",
      "uncertainty": 0.1,
      "description": "Effective evolution parameter",
      "formula": "w_a,eff = w\u2080 \u00d7 \u03b1_T / 3",
      "derivation": "Logarithmic w(z) evolution with \u03b1_T=2.7",
      "source": "simulation:wz_evolution_desi_dr2",
      "experimental_value": -0.75,
      "experimental_uncertainty": 0.3,
      "experimental_source": "DESI DR2 (Oct 2024)",
      "agreement_sigma": 0.6586005020400484,
      "agreement_text": "Good (0.66\u03c3)",
      "testable": "Euclid 2027-2028",
      "references": [
        "arXiv:2510.12627"
      ]
    },
    "w0_DESI_central": {
      "value": -0.83,
      "unit": "dimensionless",
      "display": "-0.83",
      "uncertainty": 0.06,
      "description": "DESI DR2 measured dark energy equation of state",
      "formula": "w\u2080 = P/\u03c1 for dark energy",
      "derivation": "DESI BAO + supernovae + CMB",
      "source": "experimental:DESI_DR2",
      "experimental_value": -0.83,
      "experimental_uncertainty": 0.06,
      "experimental_source": "DESI DR2 (Oct 2024)",
      "references": [
        "arXiv:2510.12627"
      ]
    },
    "w0_DESI_error": {
      "value": 0.06,
      "unit": "dimensionless",
      "display": "0.06",
      "description": "DESI DR2 uncertainty on w\u2080",
      "derivation": "Statistical + systematic uncertainties",
      "source": "experimental:DESI_DR2",
      "references": [
        "arXiv:2510.12627"
      ]
    },
    "w0_sigma": {
      "value": 0.38036892584688753,
      "unit": "\u03c3",
      "display": "0.38",
      "description": "Agreement between PM prediction and DESI measurement",
      "formula": "\u03c3 = |w\u2080_PM - w\u2080_DESI| / \u03c3_DESI",
      "derivation": "(\u22120.8528 \u2212 (\u22120.83)) / 0.06 = 0.38\u03c3",
      "source": "simulation:dark_energy_wz_evolution",
      "agreement_text": "Excellent agreement",
      "references": [
        "PM v7.0 validation"
      ]
    }
  },
  "kk_spectrum": {
    "m1_central": {
      "value": 5.0,
      "unit": "TeV",
      "display": "5.0\u00b11.5",
      "uncertainty": 1.5,
      "uncertainty_lower": 3.0,
      "uncertainty_upper": 7.0,
      "confidence_level": "95%",
      "description": "Lightest Kaluza-Klein graviton mass",
      "formula": "m\u2081 = 1/R_shared \u2248 5 TeV",
      "derivation": "Compactification radius from D_eff=12.589",
      "source": "config:V61Predictions",
      "experimental_bound": 3.5,
      "experimental_source": "ATLAS/CMS 2024",
      "testable": "HL-LHC 2027-2030 (6.2\u03c3 expected)",
      "references": [
        "ATLAS-CONF-2023-xxx"
      ]
    },
    "hl_lhc_significance": {
      "value": 6.2,
      "unit": "\u03c3",
      "display": "6.2\u03c3",
      "uncertainty": 0.5,
      "description": "Expected discovery significance at HL-LHC",
      "formula": "\u03c3 = \u221a(N_signal) / \u221a(N_background)",
      "derivation": "Monte Carlo with 3 ab\u207b\u00b9 luminosity",
      "source": "simulation:kk_spectrum_collider",
      "testable": "HL-LHC 2030",
      "references": [
        "PM predictions section"
      ]
    }
  },
  "planck_tension": {
    "initial_sigma": {
      "value": 6.0,
      "unit": "\u03c3",
      "display": "6.0\u03c3",
      "description": "Initial Planck-DESI tension",
      "source": "observational",
      "references": [
        "Planck 2018",
        "DESI DR2 2024"
      ]
    },
    "residual_sigma": {
      "value": 1.3,
      "unit": "\u03c3",
      "display": "1.3\u03c3",
      "description": "Residual tension after corrections",
      "formula": "Combined effect of log w(z) + F(R,T) bias",
      "derivation": "Logarithmic DE evolution + breathing mode systematic",
      "source": "simulation:wz_evolution_desi_dr2",
      "references": [
        "PM cosmology section"
      ]
    },
    "frt_bias": {
      "value": -0.1,
      "unit": "dimensionless",
      "display": "-0.10",
      "uncertainty": 0.03,
      "description": "F(R,T) breathing mode systematic bias",
      "formula": "\u0394w\u2080 = -\u03b2 \u00d7 (\u03a9_m/\u03a9_DE) \u00d7 C_ISW",
      "derivation": "Pneuma condensate VEV couples to matter",
      "source": "geometric",
      "references": [
        "PM Section 6.1a"
      ]
    }
  },
  "gauge_unification": {
    "alpha_GUT_inv": {
      "value": 23.538581563878598,
      "unit": "dimensionless",
      "display": "23.54",
      "uncertainty": 0.5,
      "description": "Inverse GUT coupling constant",
      "formula": "1/\u03b1_GUT from 3-loop RG + KK thresholds at 5 TeV",
      "derivation": "Renormalization group running from M_Z to M_GUT",
      "source": "simulation:proton_decay_rg_hybrid",
      "references": [
        "Acharya 2004",
        "Improved from 24.68 to 23.54 in v7.0"
      ]
    },
    "unification_precision": {
      "value": 0.953,
      "unit": "fraction",
      "display": "95.3%",
      "description": "Gauge coupling unification precision",
      "formula": "Relative agreement of SU(3), SU(2), U(1) at M_GUT",
      "derivation": "3-loop RG with threshold corrections",
      "source": "simulation:gauge_unification",
      "references": [
        "PM Section 3"
      ]
    }
  }
};


// Enhanced formatting with metadata support
PM.format = {
    scientific: (obj, decimals = 2) => {
        const val = (typeof obj === 'object') ? obj.value : obj;
        return val.toExponential(decimals);
    },

    withUnit: (obj) => {
        if (typeof obj !== 'object') return obj.toString();
        return `${obj.display || obj.value} ${obj.unit || ''}`.trim();
    },

    withError: (obj) => {
        if (typeof obj !== 'object') return obj.toString();
        if (obj.uncertainty_lower && obj.uncertainty_upper) {
            const lower = typeof obj.uncertainty_lower === 'number' ? obj.uncertainty_lower.toExponential(2) : obj.uncertainty_lower;
            const upper = typeof obj.uncertainty_upper === 'number' ? obj.uncertainty_upper.toExponential(2) : obj.uncertainty_upper;
            return `${obj.display} [${lower}-${upper}]`;
        } else if (obj.uncertainty) {
            return `${obj.display} ± ${obj.uncertainty}`;
        }
        return obj.display || obj.value.toString();
    },

    sigma: (obj) => {
        const val = (typeof obj === 'object') ? obj.value : obj;
        return val.toFixed(2) + 'σ';
    },

    display: (obj) => {
        if (typeof obj !== 'object') return obj.toString();
        return obj.display || obj.value.toString();
    }
};

// Generate tooltip HTML for a constant
PM.getTooltip = (category, parameter) => {
    const obj = PM[category][parameter];
    if (typeof obj !== 'object') return null;

    let tooltip = `<div class="pm-tooltip">`;
    tooltip += `<div class="pm-tooltip-value"><strong>${obj.display || obj.value}</strong> ${obj.unit || ''}</div>`;

    if (obj.description) {
        tooltip += `<div class="pm-tooltip-desc">${obj.description}</div>`;
    }

    if (obj.formula) {
        tooltip += `<div class="pm-tooltip-formula"><em>Formula:</em> ${obj.formula}</div>`;
    }

    if (obj.derivation) {
        tooltip += `<div class="pm-tooltip-derivation"><em>Derivation:</em> ${obj.derivation}</div>`;
    }

    if (obj.uncertainty !== undefined || obj.uncertainty_oom !== undefined) {
        const unc = obj.uncertainty_oom
            ? `±${obj.uncertainty_oom} OOM`
            : obj.uncertainty_lower && obj.uncertainty_upper
                ? `${obj.confidence_level || '68%'} CI: [${obj.uncertainty_lower}-${obj.uncertainty_upper}]`
                : `±${obj.uncertainty}`;
        tooltip += `<div class="pm-tooltip-uncertainty"><em>Uncertainty:</em> ${unc}</div>`;
    }

    if (obj.experimental_value !== undefined) {
        tooltip += `<div class="pm-tooltip-experiment">`;
        tooltip += `<em>Experiment:</em> ${obj.experimental_value} ± ${obj.experimental_uncertainty} (${obj.experimental_source})`;
        tooltip += `</div>`;
    }

    if (obj.agreement_sigma !== undefined || obj.agreement) {
        const sigma = obj.agreement_sigma || 0;
        const color = sigma < 1 ? '#4caf50' : sigma < 3 ? '#ff9800' : '#f44336';
        tooltip += `<div class="pm-tooltip-agreement" style="color:${color}">`;
        tooltip += `<em>Agreement:</em> ${obj.agreement_text || obj.agreement || `${sigma.toFixed(2)}σ`}`;
        tooltip += `</div>`;
    }

    if (obj.testable) {
        tooltip += `<div class="pm-tooltip-testable"><em>Testable:</em> ${obj.testable}</div>`;
    }

    if (obj.source) {
        tooltip += `<div class="pm-tooltip-source"><em>Source:</em> ${obj.source}</div>`;
    }

    if (obj.references && obj.references.length > 0) {
        tooltip += `<div class="pm-tooltip-refs"><em>Refs:</em> ${obj.references.join(', ')}</div>`;
    }

    tooltip += `</div>`;
    return tooltip;
};

// Export for ES6 modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = PM;
}
