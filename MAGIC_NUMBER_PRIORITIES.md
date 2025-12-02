# Magic Number Replacement Priorities

This report identifies which HTML files likely contain magic numbers
in contexts where they should be replaced with `PM.*` constants.

## Summary

- **Script tags added**: 36 files
- **Already had script**: 2 files
- **Failed**: 3 files
- **Priority for review**: 1 files

## Files Updated with Script Tag

- `beginners-guide-printable.html`
- `beginners-guide.html`
- `computational-appendices.html`
- `diagrams\theory-diagrams.html`
- `foundations\boltzmann-entropy.html`
- `foundations\calabi-yau.html`
- `foundations\clifford-algebra.html`
- `foundations\dirac-equation.html`
- `foundations\einstein-field-equations.html`
- `foundations\einstein-hilbert-action.html`
- `foundations\g2-manifolds.html`
- `foundations\index.html`
- `foundations\kaluza-klein.html`
- `foundations\kms-condition.html`
- `foundations\ricci-tensor.html`
- `foundations\so10-gut.html`
- `foundations\tomita-takesaki.html`
- `foundations\yang-mills.html`
- `philosophical-implications.html`
- `principia-metaphysica-paper.html`
- `references.html`
- `sections\cmb-bubble-collisions-comprehensive.html`
- `sections\conclusion.html`
- `sections\cosmology.html`
- `sections\einstein-hilbert-term.html`
- `sections\fermion-sector.html`
- `sections\formulas.html`
- `sections\gauge-unification.html`
- `sections\geometric-framework.html`
- `sections\index.html`
- `sections\introduction.html`
- `sections\pneuma-lagrangian-new.html`
- `sections\pneuma-lagrangian.html`
- `sections\theory-analysis.html`
- `sections\thermal-time.html`
- `visualization-index.html`

## Priority Files for Manual Review

These files contain patterns suggesting magic numbers in replaceable contexts:

### `gauge-unification.html`
Path: `sections\gauge-unification.html`

**Detected patterns:**
- Form values


## Failed Files

- `PAPER_2T_UPDATE_SECTION.html`: No </head> tag found
- `sections\division-algebra-section.html`: No </head> tag found
- `solutions\time-circularity-section.html`: No </head> tag found

## Next Steps

1. **Theory sections** (geometric-framework, gauge-unification, etc):
   - Review formulas and replace hard-coded values with PM constants
   - Example: `2.118×10¹⁶` → `PM.format.scientific(PM.proton_decay.M_GUT, 3)`

2. **Beginner's guide and paper:**
   - Replace scientific notation in predictions with PM constants
   - Keep prose numbers (like "26-dimensional") as-is for readability

3. **Foundation pages:**
   - Replace example values with actual PM constants where relevant

## Replacement Examples

```html
<!-- Before -->
<strong>M<sub>GUT</sub> = 2.118×10¹⁶ GeV</strong>

<!-- After -->
<strong>M<sub>GUT</sub> = <span id="mgut-value"></span> GeV</strong>
<script>
document.getElementById('mgut-value').textContent = 
    PM.format.scientific(PM.proton_decay.M_GUT, 3);
</script>
```

Or for data attributes:
```html
<!-- Before -->
<div data-mgut="2.118e16">...</

<!-- After -->
<div data-mgut="" id="data-mgut">...</div>
<script>
document.getElementById('data-mgut').dataset.mgut = PM.proton_decay.M_GUT;
</script>
```