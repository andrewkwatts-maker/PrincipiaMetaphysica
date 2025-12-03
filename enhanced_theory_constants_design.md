# Enhanced Theory Constants with Metadata

## Vision

Every constant displayed on the website should be hoverable and show:
- **Value**: The actual number
- **Formula/Derivation**: How it was calculated
- **Uncertainty/Error**: ±σ or OOM
- **Experimental Value**: Observed data (if available)
- **Agreement**: σ deviation from experiment
- **Source**: Which config parameter or simulation produced it

## Enhanced JavaScript Structure

```javascript
const PM = {
    meta: { version: "7.0", ... },

    // Enhanced structure with metadata
    proton_decay: {
        M_GUT: {
            value: 2.118e16,
            unit: "GeV",
            uncertainty: 0.09e16,
            uncertainty_percent: 4.25,
            formula: "M_GUT = M_base × (1 + c_warp × s)",
            derivation: "TCS G₂ torsion logarithms",
            source: "geometric",
            references: ["Acharya-Witten 2001"],
            display: "2.118×10¹⁶"
        },

        tau_p_median: {
            value: 3.764188689612127e34,
            unit: "years",
            uncertainty_lower: 2.41e34,
            uncertainty_upper: 5.61e34,
            uncertainty_oom: 0.177,
            formula: "τ_p = 3.82×10³³ × (M_GUT/10¹⁶)⁴ × (0.03/α_GUT)²",
            derivation: "Monte Carlo (1000 samples) with 3-loop RG",
            source: "simulation:proton_decay_rg_hybrid",
            experimental_bound: 1.67e34,
            experimental_source: "Super-K 2024",
            agreement: "2.3× above bound",
            references: ["PDG 2024"],
            display: "3.84×10³⁴"
        },

        alpha_GUT_inv: {
            value: 23.538581563878598,
            unit: "dimensionless",
            uncertainty: 0.5,
            formula: "1/α_GUT from 3-loop RG + KK thresholds",
            derivation: "Renormalization group running from M_Z to M_GUT",
            source: "simulation:proton_decay_rg_hybrid",
            references: ["Acharya 2004"],
            display: "23.54"
        }
    },

    pmns_matrix: {
        theta_23: {
            value: 47.199999,
            unit: "degrees",
            uncertainty: 0.80,
            formula: "θ₂₃ = 45° + (α₄ - α₅) × n_gen",
            derivation: "Shared extra dimension asymmetry",
            source: "geometric",
            experimental_value: 47.2,
            experimental_uncertainty: 2.0,
            experimental_source: "NuFIT 5.2 (2024)",
            agreement_sigma: 0.00,
            agreement_text: "EXACT MATCH",
            references: ["NuFIT collaboration"],
            display: "47.20°"
        },

        theta_12: {
            value: 33.59329049922625,
            unit: "degrees",
            uncertainty: 1.18,
            formula: "θ₁₂ = arcsin(1/√3 × |1 + δ_pert|)",
            derivation: "Tri-bimaximal mixing + G₂ perturbation",
            source: "geometric",
            experimental_value: 33.41,
            experimental_uncertainty: 0.75,
            experimental_source: "NuFIT 5.2 (2024)",
            agreement_sigma: 0.24,
            agreement_text: "Excellent (0.24σ)",
            references: ["NuFIT collaboration"],
            display: "33.59°"
        }

        // ... similar for theta_13, delta_cp
    },

    dark_energy: {
        w0_PM: {
            value: -0.8528221355508132,
            unit: "dimensionless",
            uncertainty: 0.001,
            formula: "w₀ = -(D_eff - 1)/(D_eff + 1)",
            derivation: "Maximum Entropy Principle with D_eff=12.589",
            source: "geometric",
            experimental_value: -0.83,
            experimental_uncertainty: 0.06,
            experimental_source: "DESI DR2 (Oct 2024)",
            agreement_sigma: 0.38,
            agreement_text: "Excellent (0.38σ)",
            references: ["arXiv:2510.12627"],
            display: "-0.853"
        },

        wa_PM_effective: {
            value: -0.9475801506120145,
            unit: "dimensionless",
            uncertainty: 0.1,
            formula: "w_a,eff = w₀ × α_T / 3",
            derivation: "Logarithmic w(z) evolution",
            source: "simulation:wz_evolution_desi_dr2",
            experimental_value: -0.75,
            experimental_uncertainty: 0.30,
            experimental_source: "DESI DR2 (Oct 2024)",
            agreement_sigma: 0.66,
            agreement_text: "Good (0.66σ)",
            references: ["arXiv:2510.12627"],
            display: "-0.95"
        }
    },

    // NEW: Extended categories
    kk_spectrum: {
        m1_central: {
            value: 5.0,
            unit: "TeV",
            uncertainty: 1.5,
            uncertainty_lower: 3.0,
            uncertainty_upper: 7.0,
            confidence_level: "95%",
            formula: "m₁ = 1/R_shared = M_KK",
            derivation: "Compactification radius from D_eff",
            source: "config:V61Predictions",
            experimental_bound: 3.5,
            experimental_source: "ATLAS/CMS 2024",
            testable: "HL-LHC 2027-2030",
            references: ["ATLAS-CONF-2023-xxx"],
            display: "5.0±1.5"
        },

        hl_lhc_significance: {
            value: 6.2,
            unit: "σ",
            uncertainty: 0.5,
            formula: "σ = √(N_signal/√N_background)",
            derivation: "Monte Carlo simulation with 3 ab⁻¹",
            source: "simulation:kk_spectrum_collider",
            testable: "HL-LHC 2030",
            display: "6.2σ"
        }
    },

    planck_tension: {
        initial_sigma: {
            value: 6.0,
            unit: "σ",
            description: "Initial tension before corrections",
            source: "observational",
            references: ["Planck 2018", "DESI DR2 2024"],
            display: "6.0σ"
        },

        residual_sigma: {
            value: 1.3,
            unit: "σ",
            description: "Residual after log w(z) + F(R,T) corrections",
            formula: "Combined tension with systematic corrections",
            derivation: "Logarithmic DE evolution + breathing mode bias",
            source: "simulation:wz_evolution_desi_dr2",
            display: "1.3σ"
        },

        frt_bias: {
            value: -0.10,
            unit: "dimensionless",
            uncertainty: 0.03,
            formula: "Δw₀ = -β × (Ω_m/Ω_DE) × C_ISW",
            derivation: "F(R,T) breathing mode systematic",
            source: "geometric",
            references: ["PM cosmology section"],
            display: "-0.10"
        }
    }
};

// Enhanced formatting functions with metadata
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
            return `${obj.display} [${obj.uncertainty_lower}-${obj.uncertainty_upper}]`;
        } else if (obj.uncertainty) {
            return `${obj.display} ± ${obj.uncertainty}`;
        }
        return obj.display || obj.value.toString();
    },

    sigma: (obj) => {
        const val = (typeof obj === 'object') ? obj.value : obj;
        return val.toFixed(2) + 'σ';
    }
};

// Tooltip generator
PM.getTooltip = (category, parameter) => {
    const obj = PM[category][parameter];
    if (typeof obj !== 'object') return null;

    let tooltip = `<div class="pm-tooltip">`;
    tooltip += `<div class="pm-tooltip-value"><strong>${obj.display || obj.value}</strong> ${obj.unit || ''}</div>`;

    if (obj.formula) {
        tooltip += `<div class="pm-tooltip-formula"><em>Formula:</em> ${obj.formula}</div>`;
    }

    if (obj.derivation) {
        tooltip += `<div class="pm-tooltip-derivation"><em>Derivation:</em> ${obj.derivation}</div>`;
    }

    if (obj.uncertainty !== undefined || obj.uncertainty_oom !== undefined) {
        const unc = obj.uncertainty_oom ? `±${obj.uncertainty_oom} OOM` : `±${obj.uncertainty}`;
        tooltip += `<div class="pm-tooltip-uncertainty"><em>Uncertainty:</em> ${unc}</div>`;
    }

    if (obj.experimental_value !== undefined) {
        tooltip += `<div class="pm-tooltip-experiment">`;
        tooltip += `<em>Experiment:</em> ${obj.experimental_value} ± ${obj.experimental_uncertainty} (${obj.experimental_source})`;
        tooltip += `</div>`;
    }

    if (obj.agreement_sigma !== undefined) {
        const color = obj.agreement_sigma < 1 ? 'green' : obj.agreement_sigma < 3 ? 'orange' : 'red';
        tooltip += `<div class="pm-tooltip-agreement" style="color:${color}">`;
        tooltip += `<em>Agreement:</em> ${obj.agreement_text || `${obj.agreement_sigma.toFixed(2)}σ`}`;
        tooltip += `</div>`;
    }

    if (obj.source) {
        tooltip += `<div class="pm-tooltip-source"><em>Source:</em> ${obj.source}</div>`;
    }

    tooltip += `</div>`;
    return tooltip;
};
```

## HTML Usage

```html
<!-- Automatic replacement with hover -->
<span class="pm-value"
      data-category="proton_decay"
      data-param="tau_p_median"
      data-format="scientific:2"></span>

<!-- Will display: 3.84×10³⁴ with full hover tooltip -->
```

## Universal JavaScript (add to each page)

```javascript
<script>
// Inject PM values and setup hover tooltips
function setupPMValues() {
    document.querySelectorAll('.pm-value').forEach(el => {
        const category = el.dataset.category;
        const param = el.dataset.param;
        const format = el.dataset.format || 'display';

        const obj = PM[category][param];
        if (!obj) {
            console.error(`PM.${category}.${param} not found`);
            return;
        }

        // Display value
        if (format === 'display') {
            el.textContent = (typeof obj === 'object') ? obj.display : obj;
        } else if (format.startsWith('scientific:')) {
            const decimals = parseInt(format.split(':')[1]);
            el.textContent = PM.format.scientific(obj, decimals);
        } else if (format === 'withUnit') {
            el.textContent = PM.format.withUnit(obj);
        } else if (format === 'withError') {
            el.textContent = PM.format.withError(obj);
        }

        // Add hover tooltip if metadata exists
        if (typeof obj === 'object') {
            el.classList.add('pm-hoverable');
            el.dataset.tooltip = PM.getTooltip(category, param);

            el.addEventListener('mouseenter', showTooltip);
            el.addEventListener('mouseleave', hideTooltip);
        }
    });
}

function showTooltip(e) {
    const tooltipHTML = e.target.dataset.tooltip;
    if (!tooltipHTML) return;

    let tooltip = document.getElementById('pm-tooltip-popup');
    if (!tooltip) {
        tooltip = document.createElement('div');
        tooltip.id = 'pm-tooltip-popup';
        tooltip.className = 'pm-tooltip-popup';
        document.body.appendChild(tooltip);
    }

    tooltip.innerHTML = tooltipHTML;
    tooltip.style.display = 'block';

    const rect = e.target.getBoundingClientRect();
    tooltip.style.left = (rect.left + rect.width / 2) + 'px';
    tooltip.style.top = (rect.bottom + 10) + 'px';
}

function hideTooltip() {
    const tooltip = document.getElementById('pm-tooltip-popup');
    if (tooltip) tooltip.style.display = 'none';
}

document.addEventListener('DOMContentLoaded', setupPMValues);
</script>

<style>
.pm-value {
    font-weight: 600;
    color: #2196F3;
}

.pm-hoverable {
    cursor: help;
    border-bottom: 1px dotted #2196F3;
}

.pm-tooltip-popup {
    position: fixed;
    background: white;
    border: 2px solid #2196F3;
    border-radius: 8px;
    padding: 12px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    z-index: 10000;
    max-width: 400px;
    font-size: 0.9em;
    display: none;
    transform: translateX(-50%);
}

.pm-tooltip-value {
    font-size: 1.2em;
    color: #2196F3;
    margin-bottom: 8px;
}

.pm-tooltip-formula,
.pm-tooltip-derivation,
.pm-tooltip-uncertainty,
.pm-tooltip-experiment,
.pm-tooltip-agreement,
.pm-tooltip-source {
    margin: 4px 0;
    line-height: 1.4;
}

.pm-tooltip em {
    color: #666;
    font-style: normal;
    font-weight: 600;
}
</style>
```

## Implementation Priority

1. **High Priority** (testable predictions):
   - All PMNS angles (with NuFIT comparison)
   - Proton decay (with Super-K bound)
   - Dark energy w0, wa (with DESI DR2)
   - M_GUT, alpha_GUT (with derivation)

2. **Medium Priority** (pre-registered tests):
   - KK spectrum (HL-LHC)
   - Planck tension (resolution mechanism)
   - Functional tests (Δχ²)

3. **Low Priority** (theoretical):
   - Dimensional structure (26D→13D→6D→4D)
   - Topology (b₂, b₃, χ_eff, ν)

## Benefits

✅ **Transparency**: Every number shows its derivation
✅ **Educational**: Users learn where values come from
✅ **Verifiable**: Experimental comparisons built-in
✅ **Maintainable**: Update config.py → everything updates
✅ **Professional**: Rich metadata like modern physics tools
✅ **Traceable**: Source field shows simulation/geometric origin

Copyright (c) 2025 Andrew Keith Watts. All rights reserved.
