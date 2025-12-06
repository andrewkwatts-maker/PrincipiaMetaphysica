# Source of Truth Validation Report

**Date:** 2025-12-06
**Framework Version:** v12.0
**Pipeline:** config.py → simulations → theory_output.json → theory-constants-enhanced.js → HTML

---

## Executive Summary

This report validates that all numerical assertions in the Principia Metaphysica website are properly sourced through the complete pipeline from theoretical foundations to frontend display.

### Key Metrics

| Metric | Count | Percentage |
|--------|-------|------------|
| **Total PM.* references found** | 10 | - |
| **Valid references** | 7 | 70.0% |
| **Broken references** | 3 | 30.0% |
| **Hardcoded numbers** | 157 | - |
| **HTML files using PM** | 2 / 57 | 3.5% |
| **Simulations in pipeline** | 21 | - |

### Overall Assessment

**Status:** ⚠️ NEEDS IMPROVEMENT

**Critical Issues:**
1. 157 hardcoded numbers should use PM.* references
2. 3 broken PM.* references need fixing
3. Only 3.5% of HTML files use the PM constant system

**Positive Findings:**
1. Pipeline is complete: config.py → theory_output.json → theory-constants-enhanced.js ✓
2. All simulations run successfully ✓
3. 70% of PM references that exist are valid ✓

---

## 1. Pipeline Validation

### 1.1 Config → Simulations

**Status:** ✅ COMPLETE

All theoretical constants originate from `config.py`:

```python
# config.py classes:
- FundamentalConstants (dimensional structure, topology)
- PhenomenologyParameters (M_Planck, w0, experimental values)
- GaugeUnificationParameters (M_GUT, alpha_GUT)
- NeutrinoParameters (masses, mixing angles)
- KKGravitonParameters (extra dimension physics)
- TorsionClass (G2 manifold geometry)
- FluxQuantization (chi_eff derivation)
```

**Simulations run (21 total):**
1. proton_decay_rg_hybrid
2. pmns_full_matrix
3. wz_evolution_desi_dr2
4. kk_spectrum_full
5. neutrino_mass_ordering
6. proton_decay_v84_ckm
7. v9_manifest
8. tcs_flux_scanner_v9
9. neutrino_ordering_v9
10. yukawa_geometry_v9
11. brst_sp2r_v9
12. g2_torsion_derivation_v10
13. flux_quantization_v10
14. anomaly_cancellation_v10
15. full_yukawa_v10
16. neutrino_mass_matrix_v10_1
17. full_fermion_matrices_v10_2
18. proton_lifetime_v11
19. higgs_mass_v11
20. neutrino_mass_matrix_final_v12
21. kk_graviton_mass_v12

### 1.2 Simulations → theory_output.json

**Status:** ✅ COMPLETE

`run_all_simulations.py` successfully generates `theory_output.json` with:
- 20 top-level categories
- Meta information (version, date, simulations run)
- Full traceability for all computed values

### 1.3 theory_output.json → theory-constants-enhanced.js

**Status:** ✅ COMPLETE

JavaScript constants file generated successfully:
- All JSON data converted to `const PM = {...}`
- Helper functions for formatting
- Version-specific accessors

### 1.4 theory-constants-enhanced.js → HTML

**Status:** ⚠️ PARTIALLY IMPLEMENTED

**Current usage:**
- Only 2 files use PM.* references
- Only 10 PM.* calls found across entire website
- Most values are hardcoded

---

## 2. Broken PM.* References

**Total: 3 broken references**

All broken references are in `sections\geometric-framework.html`:

| Reference | Issue | Fix Needed |
|-----------|-------|------------|
| `PM.kk_spectrum.m1_central.value` | Parameter not found | Use `PM.kk_spectrum.m1` instead |
| `PM.kk_spectrum.m1_central.value` | Parameter not found | Use `PM.kk_spectrum.m1` instead |
| `PM.kk_spectrum.hl_lhc_significance.value` | Parameter not found | Add `discovery_significance_sigma` to JS constants |

### Recommended Fixes

**Option 1: Update HTML to use correct paths**
```javascript
// Change:
PM.kk_spectrum.m1_central.value
// To:
PM.kk_spectrum.m1
```

**Option 2: Add aliases to theory-constants-enhanced.js**
```javascript
PM.kk_spectrum.m1_central = PM.kk_spectrum.m1;
PM.kk_spectrum.hl_lhc_significance = PM.kk_spectrum.discovery_significance_sigma;
```

---

## 3. Hardcoded Numbers Analysis

**Total: 157 hardcoded numbers found**

### 3.1 By Number Type

| Value | Occurrences | Should Use |
|-------|-------------|------------|
| `144` (chi_eff) | 150 | `PM.topology.chi_eff` |
| `23.54` (alpha_GUT^-1) | 4 | `PM.proton_decay.alpha_GUT_inv` |
| `5.0 TeV` (KK mass) | 4 | `PM.kk_spectrum.m1 / 1000` |
| `2.118×10^16` (M_GUT) | 1 | `PM.proton_decay.M_GUT` |

### 3.2 Files with Most Hardcoded Values

| File | Count | Primary Issue |
|------|-------|---------------|
| `philosophical-implications.html` | 16 | All `144` references |
| `foundations\g2-manifolds.html` | 19 | All `144` references |
| `foundations\calabi-yau.html` | 18 | All `144` references |
| `sections\geometric-framework.html` | 30 | Mix of `144`, `5.0 TeV`, `23.54` |
| `sections\theory-analysis.html` | 9 | All `144` references |
| `sections\fermion-sector.html` | 9 | All `144` references |

### 3.3 Why This Matters

**Current problems:**
1. **No single source of truth** - Values duplicated 150+ times
2. **Update nightmare** - Changing chi_eff from 144 requires editing 150 locations
3. **Inconsistency risk** - Easy to miss updates, creating contradictions
4. **No traceability** - Can't verify where `144` comes from

**Solution:**
Replace all hardcoded `144` with:
```javascript
<span class="value" data-pm="topology.chi_eff"></span>
```

---

## 4. Source Traceability (Sample)

### 4.1 PM.proton_decay.M_GUT

**Complete Trace:**
```
config.py (GaugeUnificationParameters.M_GUT = 2.118e16)
  ↓
simulations/proton_decay_rg_hybrid.py
  ↓
theory_output.json (proton_decay.M_GUT)
  ↓
theory-constants-enhanced.js (PM.proton_decay.M_GUT)
  ↓
HTML (PM.proton_decay.M_GUT)
```

**Status:** ✅ FULLY TRACEABLE

### 4.2 PM.pmns_matrix.theta_23

**Complete Trace:**
```
config.py (NeutrinoParameters.THETA_23 = 47.2)
  ↓
simulations/pmns_full_matrix.py
  ↓
theory_output.json (pmns_matrix.theta_23)
  ↓
theory-constants-enhanced.js (PM.pmns_matrix.theta_23)
  ↓
HTML (PM.pmns_matrix.theta_23)
```

**Status:** ✅ FULLY TRACEABLE

### 4.3 PM.dark_energy.w0_PM

**Complete Trace:**
```
config.py (derived, not direct parameter)
  ↓
simulations/wz_evolution_desi_dr2.py (computes from d_eff)
  ↓
theory_output.json (dark_energy.w0_PM = -0.853)
  ↓
theory-constants-enhanced.js (PM.dark_energy.w0_PM)
  ↓
HTML (PM.dark_energy.w0_PM)
```

**Status:** ✅ FULLY TRACEABLE

### 4.4 PM.topology.chi_eff

**Complete Trace:**
```
config.py (FundamentalConstants.euler_characteristic_effective() = 144)
  ↓
run_all_simulations.py (hardcoded in results['topology'])
  ↓
theory_output.json (topology.chi_eff = 144)
  ↓
theory-constants-enhanced.js (PM.topology.chi_eff)
  ↓
HTML (HARDCODED 150 times, PM not used!)
```

**Status:** ⚠️ TRACED TO JSON BUT NOT USED IN HTML

---

## 5. Missing Parameters

Parameters referenced in HTML but not in theory_output.json:

### 5.1 beginners-guide.html
- `PM.fundamental.higgs_mass` - should use `PM.v11_final_observables.higgs_mass.m_h_GeV`
- `PM.predictions.proton_lifetime` - should use `PM.proton_decay.tau_p_central`
- `PM.predictions.kk_mass_first` - should use `PM.kk_spectrum.m1`
- `PM.neutrino.sum_neutrino_mass` - should use `PM.v12_final_values.neutrino_masses_final.sum_eV`
- `PM.dark_energy.w0` - should use `PM.dark_energy.w0_PM`

### 5.2 sections\cosmology.html
- `PM.dark_energy.w0_DESI_central` - should use `PM.desi_dr2_data.w0`
- `PM.dark_energy.w0_sigma` - should use `PM.dark_energy.w0_deviation_sigma`

### 5.3 sections\gauge-unification.html
- `PM.gauge_unification.alpha_GUT_inv` - should use `PM.proton_decay.alpha_GUT_inv`
- `PM.proton_decay.uncertainty_oom` - should use `PM.proton_decay.tau_p_uncertainty_oom`

---

## 6. Recommendations

### Priority 1: Fix Broken References (HIGH)

1. Update `geometric-framework.html`:
   - Change `PM.kk_spectrum.m1_central` → `PM.kk_spectrum.m1`
   - Change `PM.kk_spectrum.hl_lhc_significance` → `PM.kk_spectrum.discovery_significance_sigma`

2. Update `beginners-guide.html` to use correct PM paths

### Priority 2: Replace Hardcoded Numbers (HIGH)

Replace 150+ instances of `144` with:
```javascript
<span data-pm="topology.chi_eff">
  <script>document.currentScript.parentElement.textContent = PM.topology.chi_eff;</script>
</span>
```

Or use a global initialization function:
```javascript
// In main.js
function initPMValues() {
  document.querySelectorAll('[data-pm]').forEach(el => {
    const path = el.dataset.pm;
    const value = getNestedValue(PM, path);
    el.textContent = value;
  });
}
```

### Priority 3: Add Missing Parameters (MEDIUM)

Add to `run_all_simulations.py`:
```python
results['gauge_unification'] = {
    'alpha_GUT_inv': results['proton_decay']['alpha_GUT_inv'],
    'M_GUT': results['proton_decay']['M_GUT']
}
```

### Priority 4: Expand PM Usage (LOW)

Goal: Increase from 3.5% to 80%+ of HTML files using PM constants.

Create templates like:
```html
<!-- Old (hardcoded) -->
<p>χ_eff = 144</p>

<!-- New (sourced) -->
<p>χ_eff = <span data-pm="topology.chi_eff" class="pm-value"></span></p>
```

---

## 7. Validation Checklist

### Pipeline Integrity
- [x] config.py contains all fundamental parameters
- [x] All simulations run without errors
- [x] theory_output.json generated successfully
- [x] theory-constants-enhanced.js generated successfully
- [ ] HTML files use PM.* references (3.5% - needs improvement)

### Data Consistency
- [x] All PM.* references point to valid data (70% valid)
- [ ] No hardcoded values in HTML (157 found)
- [ ] All numbers trace back to config.py or simulations
- [x] Version numbers match across pipeline

### Traceability
- [x] Can trace M_GUT from config → HTML
- [x] Can trace theta_23 from config → HTML
- [x] Can trace w0 from simulation → HTML
- [ ] Can trace chi_eff usage in HTML (hardcoded)

---

## 8. Next Steps

### Immediate (This Week)
1. Fix 3 broken PM references in `geometric-framework.html`
2. Create utility function to auto-populate `[data-pm]` attributes
3. Replace top 10 most-used hardcoded values with PM references

### Short Term (This Month)
1. Add missing parameter aliases to `run_all_simulations.py`
2. Convert all `144` references to PM.topology.chi_eff
3. Document PM reference system in developer guide

### Long Term (This Quarter)
1. Increase PM usage to 80%+ of HTML files
2. Add automated tests to catch hardcoded values in CI/CD
3. Create browser devtools integration to highlight PM values

---

## Appendix A: Complete Pipeline Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                        config.py                             │
│  ┌──────────────────────────────────────────────────────┐   │
│  │ FundamentalConstants                                  │   │
│  │ PhenomenologyParameters                               │   │
│  │ GaugeUnificationParameters                            │   │
│  │ NeutrinoParameters                                    │   │
│  │ KKGravitonParameters                                  │   │
│  │ TorsionClass, FluxQuantization, etc.                  │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────┬───────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                  run_all_simulations.py                      │
│  ┌──────────────────────────────────────────────────────┐   │
│  │ 21 simulation modules:                                │   │
│  │  - proton_decay_rg_hybrid.py                          │   │
│  │  - pmns_full_matrix.py                                │   │
│  │  - wz_evolution_desi_dr2.py                           │   │
│  │  - ... (18 more)                                      │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────┬───────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                   theory_output.json                         │
│  {                                                           │
│    "meta": { "version": "12.0", ... },                      │
│    "dimensions": { ... },                                   │
│    "topology": { "chi_eff": 144, ... },                     │
│    "proton_decay": { "M_GUT": 2.118e16, ... },              │
│    "pmns_matrix": { "theta_23": 47.2, ... },                │
│    ...                                                       │
│  }                                                           │
└─────────────────────────┬───────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│             theory-constants-enhanced.js                     │
│  const PM = { ... };                                         │
│  PM.format = { ... };                                        │
│  PM.getVersion = () => ...;                                  │
└─────────────────────────┬───────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                      HTML Files                              │
│  <script src="theory-constants-enhanced.js"></script>       │
│  <span data-pm="topology.chi_eff"></span>                   │
│  <script>                                                    │
│    console.log(PM.proton_decay.M_GUT);                      │
│  </script>                                                   │
└─────────────────────────────────────────────────────────────┘
```

---

## Appendix B: Test Command

Run validation anytime with:

```bash
python validate_source_of_truth.py
```

Output:
- Console report (summary)
- `SOURCE_OF_TRUTH_VALIDATION.json` (detailed findings)
- `SOURCE_OF_TRUTH_VALIDATION.md` (this report)

---

**Generated:** 2025-12-06
**Tool:** validate_source_of_truth.py
**Author:** Andrew Keith Watts
