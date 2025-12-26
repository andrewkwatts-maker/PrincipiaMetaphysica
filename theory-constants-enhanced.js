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
    "version": "8.4",
    "last_updated": "2025-12-25",
    "description": "Enhanced theory constants with full metadata - v8.4 with CKM rotation and TCS cycle orientations",
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
      "derivation": "Flux quantization on TCS manifold #187",
      "source": "geometric:TCSTopologyParameters",
      "references": [
        "Corti-Haskins-Nordstr\u00f6m-Pacini 2015"
      ]
    },
    "b2": {
      "value": 4.0,
      "unit": "dimensionless",
      "display": "4",
      "description": "Second Betti number (h^{1,1})",
      "formula": "b\u2082 = K = 4 matching K3 fibres",
      "derivation": "TCS gluing construction",
      "source": "geometric:TCSTopologyParameters",
      "references": [
        "CHNP 2015"
      ]
    },
    "b3": {
      "value": 24.0,
      "unit": "dimensionless",
      "display": "24",
      "description": "Number of coassociative 4-cycles",
      "formula": "b\u2083 = b\u2082(X\u2081) + b\u2082(X\u2082) + K + 1 = 24",
      "derivation": "G\u2082 cohomology from TCS gluing",
      "source": "geometric:TCSTopologyParameters",
      "references": [
        "CHNP 2015"
      ]
    },
    "k_matching": {
      "value": 4.0,
      "unit": "dimensionless",
      "display": "4",
      "description": "Number of matching K3 fibres",
      "formula": "K = b\u2082 = 4",
      "derivation": "TCS construction parameter",
      "source": "geometric:TCSTopologyParameters",
      "references": [
        "CHNP 2015"
      ]
    },
    "n_flux": {
      "value": 24.0,
      "unit": "dimensionless",
      "display": "24",
      "description": "Flux quantization number",
      "formula": "N_flux = \u03c7_eff / 6 = 144 / 6",
      "derivation": "Index theorem on G\u2082 manifold",
      "source": "geometric:TCSTopologyParameters",
      "references": [
        "CHNP 2015"
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
    },
    "hodge_h11": {
      "value": 4.0,
      "unit": "dimensionless",
      "display": "4",
      "description": "K\u00e4hler moduli dimension",
      "formula": "h^{1,1} = 4",
      "derivation": "G\u2082 Hodge theory",
      "source": "geometric:TCSTopologyParameters",
      "references": [
        "CHNP 2015"
      ]
    },
    "hodge_h31": {
      "value": 68.0,
      "unit": "dimensionless",
      "display": "68",
      "description": "Associative 3-cycle moduli dimension",
      "formula": "h^{3,1} = 68",
      "derivation": "G\u2082 Hodge theory",
      "source": "geometric:TCSTopologyParameters",
      "references": [
        "CHNP 2015"
      ]
    }
  },
  "shared_dimensions": {
    "shadow_kuf": {
      "value": 0.576152,
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
    "shadow_chet": {
      "value": 0.576152,
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
      "value": 12.576152,
      "unit": "dimensions",
      "display": "12.589",
      "uncertainty": 0.01,
      "description": "Effective quantum-corrected dimension",
      "formula": "D_eff = 12 + 0.5\u00d7(Shadow_\u05e7+Shadow_\u05d7)",
      "derivation": "Shared dimension coupling + quantum corrections",
      "source": "geometric",
      "references": [
        "PM Section 6"
      ]
    }
  },
  "proton_decay": {},
  "pmns_matrix": {},
  "dark_energy": {},
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
  "neutrino_mass_ordering": {},
  "proton_decay_channels": {},
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
  "xy_bosons": {
    "M_X": {
      "value": 2.118e+16,
      "unit": "GeV",
      "display": "2.118\u00d710\u00b9\u2076",
      "uncertainty": 900000000000000.0,
      "description": "X boson mass (heavy gauge boson)",
      "formula": "M_X = M_GUT from SO(10) symmetry",
      "derivation": "Geometrically derived from TCS G\u2082 torsion",
      "source": "geometric:M_GUT",
      "charge": 1.3333333333333333,
      "charge_display": "\u00b14/3 e",
      "references": [
        "Acharya-Witten 2001",
        "SO(10) GUT"
      ]
    },
    "M_Y": {
      "value": 2.118e+16,
      "unit": "GeV",
      "display": "2.118\u00d710\u00b9\u2076",
      "uncertainty": 900000000000000.0,
      "description": "Y boson mass (heavy gauge boson)",
      "formula": "M_Y = M_GUT from SO(10) symmetry",
      "derivation": "Assumed degenerate with M_X (mass splitting unknown)",
      "source": "geometric:M_GUT",
      "charge": 0.3333333333333333,
      "charge_display": "\u00b11/3 e",
      "references": [
        "Acharya-Witten 2001",
        "SO(10) GUT"
      ]
    },
    "alpha_GUT": {
      "value": 0.04248088360237893,
      "unit": "dimensionless",
      "display": "0.0425",
      "description": "GUT coupling strength (fine structure at M_GUT)",
      "formula": "\u03b1_GUT = 1/23.54",
      "derivation": "3-loop RG running from M_Z to M_GUT",
      "source": "simulation:gauge_unification",
      "references": [
        "PM Section 3"
      ]
    },
    "tau_estimate": {
      "value": 1e-41,
      "unit": "seconds",
      "display": "~10\u207b\u2074\u00b9 s",
      "description": "X,Y boson lifetime (theoretical estimate)",
      "formula": "\u03c4 ~ \u210f/M_GUT",
      "derivation": "Order of magnitude from decay width estimate",
      "source": "theoretical_estimate",
      "uncertainty_type": "order_of_magnitude",
      "references": [
        "Standard GUT phenomenology"
      ]
    },
    "N_total": {
      "value": 45.0,
      "unit": "bosons",
      "display": "45",
      "description": "Total SO(10) gauge bosons",
      "formula": "dim[SO(10) adjoint] = 45",
      "derivation": "SO(10) Lie algebra dimension",
      "source": "group_theory",
      "fixed": true,
      "references": [
        "Georgi-Glashow 1974"
      ]
    },
    "N_X": {
      "value": 12.0,
      "unit": "bosons",
      "display": "12",
      "description": "Number of X-type bosons (charge \u00b14/3)",
      "formula": "From SO(10) representation decomposition",
      "derivation": "SO(10) \u2192 SU(5) \u2192 SM breaking pattern",
      "source": "group_theory",
      "fixed": true,
      "references": [
        "SO(10) GUT literature"
      ]
    },
    "N_Y": {
      "value": 12.0,
      "unit": "bosons",
      "display": "12",
      "description": "Number of Y-type bosons (charge \u00b11/3)",
      "formula": "From SO(10) representation decomposition",
      "derivation": "SO(10) \u2192 SU(5) \u2192 SM breaking pattern",
      "source": "group_theory",
      "fixed": true,
      "references": [
        "SO(10) GUT literature"
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
