# Magic Number Elimination Strategy

## Problem Identified

During the deep dive implementation, **412 magic numbers were hard-coded** into the HTML files instead of being read from `theory-constants.js`. This violates the single source of truth principle.

## Current Status

**Audit Results**:
- `principia-metaphysica-paper.html`: 123 magic numbers
- `sections/cosmology.html`: 107 magic numbers
- `sections/predictions.html`: 103 magic numbers
- `sections/fermion-sector.html`: 62 magic numbers
- `sections/gauge-unification.html`: 17 magic numbers
- **Total**: 412 magic numbers to fix

**Root Cause**: Values were added directly to HTML instead of:
1. Adding to `config.py` first
2. Ensuring `run_all_simulations.py` exports them
3. Using `PM.*` references in HTML with `<script src="theory-constants.js"></script>`

---

## Fix Strategy

### Phase 1: Add Missing Constants to config.py ✓ (Mostly Done)

Most values are already in config.py:
- ✓ M_GUT, tau_p, alpha_GUT_inv
- ✓ PMNS angles (all 4)
- ✓ Dark energy w0, wa
- ✓ DESI DR2 data
- ✓ Shared dimensions (alpha_4, alpha_5)

**Missing** (need to add):
- KK spectrum parameters (currently in V61Predictions, need dedicated class)
- Planck tension values (initial 6.0σ, residual 1.3σ)
- F(R,T) bias correction (-0.10)
- Functional test statistics (Δχ²=12, 3.5σ)
- Confidence intervals (68% CI bounds)
- Monte Carlo uncertainties per parameter

### Phase 2: Update run_all_simulations.py

Ensure ALL config values are exported to `theory_output.json`:
```python
results['planck_tension'] = {
    'initial_sigma': 6.0,
    'residual_sigma': 1.3,
    'frt_bias': -0.10,
    # ... etc
}

results['kk_spectrum'] = {
    'm1_central': 5.0,
    'm1_uncertainty': 1.5,
    'm1_min_95cl': 3.0,
    'm1_max_95cl': 7.0,
    'sigma_diphoton': 0.10,
    'hl_lhc_significance': 6.2,
    # ... etc
}

results['functional_tests'] = {
    'delta_chi2_log_vs_cpl': 12.0,
    'sigma_preference': 3.5,
    # ... etc
}
```

### Phase 3: Regenerate theory-constants.js

Run `python run_all_simulations.py` to generate updated `theory-constants.js` with ALL values.

### Phase 4: Add Script Tags to HTML Files

Each of the 5 HTML files needs:
```html
<head>
    ...
    <script src="../theory-constants.js"></script>
    <!-- or <script src="theory-constants.js"></script> for root files -->
</head>
```

### Phase 5: Replace Magic Numbers with PM.* References

**Strategy**: Use agents to systematically replace based on patterns:

**Pattern 1: Inline numbers in text**
```html
<!-- Before -->
<p>The proton lifetime is predicted to be 3.84×10³⁴ years</p>

<!-- After -->
<p>The proton lifetime is predicted to be <span id="tau-p-value"></span> years</p>
<script>
document.getElementById('tau-p-value').textContent =
    PM.format.scientific(PM.proton_decay.tau_p_median, 2);
</script>
```

**Pattern 2: Table cells**
```html
<!-- Before -->
<td>3.84×10³⁴</td>

<!-- After -->
<td><span class="pm-value" data-pm="proton_decay.tau_p_median" data-format="scientific:2"></span></td>
```

**Pattern 3: Formula displays**
```html
<!-- Before -->
<p>M<sub>GUT</sub> = 2.118×10¹⁶ GeV</p>

<!-- After -->
<p>M<sub>GUT</sub> = <span id="mgut"></span> GeV</p>
<script>
document.getElementById('mgut').textContent =
    PM.format.scientific(PM.proton_decay.M_GUT, 3);
</script>
```

**Pattern 4: Universal helper function (add to each page)**
```html
<script>
// Universal PM value injector
function injectPMValues() {
    document.querySelectorAll('.pm-value').forEach(el => {
        const path = el.dataset.pm.split('.');
        let value = PM;
        for (const key of path) {
            value = value[key];
        }

        const format = el.dataset.format || 'fixed:2';
        const [formatType, decimals] = format.split(':');

        if (formatType === 'scientific') {
            el.textContent = PM.format.scientific(value, parseInt(decimals));
        } else if (formatType === 'sigma') {
            el.textContent = PM.format.sigma(value);
        } else {
            el.textContent = PM.format.fixed(value, parseInt(decimals));
        }
    });
}

// Run on page load
document.addEventListener('DOMContentLoaded', injectPMValues);
</script>
```

---

## Implementation Steps (Recommended Order)

1. **Add missing constants to config.py** (15 min)
   - KKSpectrumParameters class (full)
   - PlanckTensionParameters class (new)
   - FunctionalTestParameters class (new)

2. **Update run_all_simulations.py** (10 min)
   - Export kk_spectrum category
   - Export planck_tension category
   - Export functional_tests category

3. **Run simulations** (5 min)
   ```bash
   python run_all_simulations.py
   ```

4. **Verify theory-constants.js** (5 min)
   - Check PM.kk_spectrum exists
   - Check PM.planck_tension exists
   - Check PM.functional_tests exists

5. **Add script tags to 5 HTML files** (5 min)
   - principia-metaphysica-paper.html
   - sections/cosmology.html
   - sections/gauge-unification.html
   - sections/fermion-sector.html
   - sections/predictions.html

6. **Deploy replacement agent** (automated)
   - Agent scans for 412 magic numbers
   - Replaces with PM.* references using patterns above
   - Adds universal helper function to each page

7. **Test in browser** (10 min)
   - Open each HTML file
   - Check console for PM object
   - Verify all values display correctly
   - No "NaN" or "undefined" anywhere

---

## Success Criteria

✅ **Zero magic numbers** in HTML files (except dimensional structure like "26D" in prose)
✅ **All values** come from theory-constants.js
✅ **Single update point**: Change config.py → run simulations → website auto-updates
✅ **Traceable**: Every displayed number can be traced to config.py source
✅ **Maintainable**: No manual editing of numbers in HTML ever again

---

## Time Estimate

- **Total time**: 1-2 hours
- **Manual work**: 40 minutes (config updates, verification)
- **Automated**: 20-80 minutes (agent replacement, depending on complexity)

---

## Files to Modify

**Config/Simulation**:
- `config.py` (add 3 new classes)
- `run_all_simulations.py` (add 3 export categories)

**HTML** (script tags + magic number replacement):
- `principia-metaphysica-paper.html`
- `sections/cosmology.html`
- `sections/gauge-unification.html`
- `sections/fermion-sector.html`
- `sections/predictions.html`

**Generated** (auto-updated by simulation):
- `theory_output.json`
- `theory-constants.js`

---

## Next Steps

1. Start with adding missing constants to config.py
2. Update simulation orchestrator
3. Regenerate constants
4. Deploy automated replacement agent
5. Test and verify

Copyright (c) 2025 Andrew Keith Watts. All rights reserved.
