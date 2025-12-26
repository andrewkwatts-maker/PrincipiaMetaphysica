# Validation Fix Checklist

**Based on:** DYNAMIC_VS_HARDCODED_VALIDATION.md
**Created:** 2025-12-25

## Issue Resolution Checklist

### 🔴 Critical Issues

#### [ ] Issue 1: Dark Energy w₀ Mismatch

**Problem:** One file has `-0.8527` instead of `-0.8528`

**File to fix:**
- [ ] `sections/cosmology.html:4415`

**Current:**
```html
<li><strong>Dark energy w₀ = -0.8527:</strong> Geometrically derived from d<sub>eff</sub> = 12.576 (TCS G₂ with Betti numbers)</li>
```

**Fix to:**
```html
<li><strong>Dark energy w₀ = -0.8528:</strong> Geometrically derived from d<sub>eff</sub> = 12.576 (TCS G₂ with Betti numbers)</li>
```

**Or make dynamic:**
```html
<li><strong>Dark energy w₀ = <span class="pm-value" data-param="dark_energy.w0"></span>:</strong> Geometrically derived from d<sub>eff</sub> = 12.576 (TCS G₂ with Betti numbers)</li>
```

---

#### [ ] Issue 2: KK Mass Inconsistency

**Problem:** HTML has both 4.5 TeV and 5.0 TeV values

**Decision needed:** Which value is canonical?
- [ ] **Option A:** Use 4.5 TeV (matches JSON calculated value)
- [ ] **Option B:** Use 5.0 TeV (geometric ideal, update JSON)
- [ ] **Option C:** Keep both (document calculated vs target)

**If Option A (4.5 TeV):**

Files with 5.0 TeV to update:
- [ ] `sections/conclusion.html:457`
- [ ] `sections/conclusion.html:2836`
- [ ] `sections/predictions.html:262`
- [ ] `sections/predictions.html:392`
- [ ] `sections/predictions.html:609`
- [ ] `sections/predictions.html:641`
- [ ] `sections/predictions.html:646`
- [ ] `sections/predictions.html:654`
- [ ] `sections/predictions.html:658`
- [ ] `sections/predictions.html:665` (section heading)
- [ ] `sections/predictions.html:699`
- [ ] `sections/predictions.html:701`
- [ ] `sections/predictions.html:710`
- [ ] `sections/predictions.html:711`
- [ ] `sections/predictions.html:817`
- [ ] `sections/predictions.html:832`
- [ ] `sections/predictions.html:846`

**If Option B (5.0 TeV):**

Files with 4.5 TeV to update:
- [ ] `sections/conclusion.html:390`
- [ ] `sections/gauge-unification.html:3617`
- [ ] `sections/gauge-unification.html:3875`
- [ ] `sections/geometric-framework.html:7669`
- [ ] `sections/geometric-framework.html:7775`
- [ ] `sections/introduction.html:1436`
- [ ] `sections/introduction.html:1438`
- [ ] `sections/predictions.html:552`
- [ ] `sections/predictions.html:556`

Plus update JSON:
- [ ] Update `simulations/kk_spectrum_*.py` to target 5.0 TeV exactly
- [ ] Regenerate `theory_output.json`

**If Option C (Both):**

- [ ] Add `target_tev = 5.0` to JSON clearly marked
- [ ] Add `calculated_tev = 4.542` to JSON clearly marked
- [ ] Update HTML to clarify: "target: 5.0 TeV, calculated: 4.5 TeV"

---

### 🟡 Medium Priority

#### [ ] Issue 3: M_GUT Precision Variance

**File to update:**
- [ ] `sections/geometric-framework.html:4134`

**Current:**
```javascript
PM.proton_decay.M_GUT = 2.1181×10^16 GeV
```

**Fix to:**
```javascript
PM.proton_decay.M_GUT = 2.118×10^16 GeV
```

---

#### [ ] Issue 4: Missing Values in JSON

**Add to theory_output.json:**

- [ ] Add `branching_ratios` to `simulations.proton_decay`:
  ```json
  "branching_ratios": {
    "e_plus_pi0": {"value": 0.642, "error": 0.094},
    "k_plus_nubar": {"value": 0.356, "error": 0.094}
  }
  ```

- [ ] Add `geometric_suppression` to `simulations.proton_decay`:
  ```json
  "geometric_suppression": {
    "S": 2.125,
    "mechanism": "TCS discrete torsion"
  }
  ```

- [ ] Add `cabibbo_angle` to `parameters`:
  ```json
  "cabibbo_angle": {
    "epsilon": 0.2257,
    "source": "racetrack superpotential"
  }
  ```

- [ ] Add `k_effective` to `parameters`:
  ```json
  "k_effective": {
    "value": 10.80,
    "formula": "b3 / (2 + epsilon)"
  }
  ```

- [ ] Add `super_kamiokande_ratio` to `simulations.proton_decay`:
  ```json
  "super_k_ratio": 4.9,
  "super_k_bound": "1.6e34 years"
  ```

- [ ] Add `discovery_significance` to `simulations.kk_spectrum`:
  ```json
  "discovery_significance": {
    "sigma": 6.8,
    "luminosity": "3 ab^-1",
    "channel": "diphoton"
  }
  ```

---

### 🟢 Low Priority (Enhancement)

#### [ ] Issue 5: Increase Dynamic Loading

**Replace hardcoded values with dynamic:**

**Proton lifetime references:**
- [ ] `sections/gauge-unification.html:4380`
- [ ] `sections/predictions.html:329`
- [ ] `sections/predictions.html:864`
- [ ] `sections/predictions.html:1051, 1058`
- [ ] `sections/predictions.html:2370, 2921, 3237, 3323`
- [ ] `sections/xy-gauge-bosons.html:446`

**M_GUT references:**
- [ ] `sections/gauge-unification.html:358, 3764, 4055`
- [ ] `sections/predictions.html:324, 1023`

**Pattern to use:**
```html
<span class="pm-value" data-source="simulations.proton_decay.tau_p_years" data-format="scientific:2"></span> years
<span class="pm-value" data-source="simulations.proton_decay.m_gut" data-format="scientific:3"></span> GeV
```

---

#### [ ] Issue 6: Add Missing Display Values

**Neutrino parameters to add:**
- [ ] Display θ₁₂ (solar angle)
- [ ] Display θ₁₃ (reactor angle)
- [ ] Display δ_CP (CP violation phase)
- [ ] Display mass splittings Δm²₂₁, Δm²₃₁

**Dark energy to add:**
- [ ] Display wa parameter
- [ ] Display d_eff explicitly

**Location:** `sections/predictions.html` or `sections/fermion-sector.html`

---

#### [ ] Issue 7: Standardize Formatting

**Define and document precision rules:**
- [ ] M_GUT: Always 3 significant figures (2.118×10¹⁶)
- [ ] Proton lifetime: 3 significant figures (8.15×10³⁴)
- [ ] w₀: 4 decimal places (-0.8528)
- [ ] θ₂₃: 1 decimal place (45.0°)
- [ ] KK mass: 1 decimal place (4.5 TeV or 5.0 TeV)

**Document in:**
- [ ] Create `docs/FORMATTING_CONVENTIONS.md`

---

#### [ ] Issue 8: Add Validation Indicators

**Add status indicators to predictions:**

```html
<span class="pm-validation" data-source="simulations.proton_decay.status"></span>
```

**Files to update:**
- [ ] `sections/predictions.html` (all major predictions)
- [ ] `sections/gauge-unification.html` (GUT predictions)

---

## Verification Steps

After making fixes:

1. **Run validation again:**
   - [ ] Execute `validate_dynamic_vs_hardcoded.py`
   - [ ] Verify all mismatches resolved

2. **Check consistency:**
   - [ ] Search for all instances of each value
   - [ ] Verify no conflicting numbers remain

3. **Test dynamic loading:**
   - [ ] Load pages in browser
   - [ ] Verify all `pm-value` spans populate correctly
   - [ ] Check console for errors

4. **Regenerate theory_output.json:**
   - [ ] If JSON structure changed, run all simulations
   - [ ] Verify new values propagate to HTML

5. **Documentation:**
   - [ ] Update CHANGELOG if needed
   - [ ] Note any value changes in commit message

---

## Completion Checklist

- [ ] All critical issues resolved
- [ ] All medium priority issues resolved
- [ ] Enhancement tasks completed (optional)
- [ ] Validation script passes
- [ ] Browser testing complete
- [ ] Documentation updated
- [ ] Changes committed

---

## Notes

**Decision Log:**

KK Mass Resolution:
- Decision: [ Option A / Option B / Option C ]
- Rationale: _______________
- Date decided: _______________

**Issues Encountered:**

(Add any issues found during fixes)

---

**Checklist Last Updated:** 2025-12-25
