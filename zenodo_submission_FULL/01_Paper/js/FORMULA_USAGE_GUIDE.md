# PM Formula Component Usage Guide

## Overview

The Principia Metaphysica website uses a standardized formula component system that provides:
- **Hoverable term definitions** - Mouse over any mathematical term to see its meaning
- **Expandable derivations** - Click to see step-by-step derivation chains
- **Consistent formatting** - All formulas render uniformly across desktop and mobile
- **Plain text fallback** - For paper versions and accessibility
- **Category badges** - Visual distinction between ESTABLISHED, THEORY, DERIVED, and PREDICTIONS

## Quick Start

### Basic Usage

```html
<!-- Load the required scripts -->
<script src="../js/formula-registry.js"></script>
<script src="../js/pm-formula-component.js"></script>

<!-- Use the component -->
<pm-formula formula-id="generation-number"></pm-formula>
```

### With Derivation Chain

```html
<pm-formula formula-id="gut-scale" show-derivation="true"></pm-formula>
```

### Without Label

```html
<pm-formula formula-id="w0-formula" show-label="false"></pm-formula>
```

## Gold Standard: Master Action 26D

The `master-action-26d` formula serves as the reference implementation:

```html
<pm-formula formula-id="master-action-26d" show-derivation="true"></pm-formula>
```

This demonstrates all features:
- Complex HTML with subscripts/superscripts
- Multiple term definitions with hover tooltips
- Derivation chain showing parent formulas and established physics
- Category badge (THEORY)
- Links to related pages

## Key Formulas Reference

### 1. Generation Number

**ID:** `generation-number`

**Formula:** n_gen = χ_eff/48 = 144/48 = 3

**Usage:**
```html
<pm-formula formula-id="generation-number"></pm-formula>
```

**Terms with hover:**
- **n_gen**: Number of fermion generations (= 3 observed)
- **χ_eff**: Effective Euler characteristic (144 from flux-dressed topology)
- **48**: 2T Index Divisor (24 × 2 for two-time framework)

**Derivation chain:**
- Parent formulas: spacetime-26d, clifford-26d
- Established physics: f-theory-index
- Verification page: sections.html#2

---

### 2. Dark Energy w₀

**ID:** `w0-formula`

**Formula:** w₀ = -1 + 1/b₃ = -23/24 ≈ -0.9583

**Usage:**
```html
<pm-formula formula-id="w0-formula" show-derivation="true"></pm-formula>
```

**Terms with hover:**
- **w₀**: Present equation of state (-0.9583 from thawing quintessence)
- **b₃**: Associative 3-cycles (= 24 from G₂ topology TCS #187)

**Experimental comparison:**
- Theory: -0.9583 (-23/24)
- DESI 2025 thawing: -0.957 ± 0.067
- Agreement: 0.02σ

---

### 3. GUT Scale

**ID:** `gut-scale`

**Formula:** M_GUT = M_* exp(T_ω s/2) = 2.118 × 10¹⁶ GeV

**Usage:**
```html
<pm-formula formula-id="gut-scale"></pm-formula>
```

**Terms with hover:**
- **M_GUT**: GUT Scale (2.118 × 10¹⁶ GeV)
- **T_ω**: Torsion (-0.875 from Spin(7) spinor fraction 7/8)
- **s**: s-parameter (1.178 from G₂ moduli)

**Key insight:** Pure geometric derivation - no fitting parameters!

---

### 4. Proton Lifetime

**ID:** `proton-lifetime`

**Formula:** τ_p = (3.83 ± 1.47) × 10³⁴ years

**Usage:**
```html
<pm-formula formula-id="proton-lifetime"></pm-formula>
```

**Terms with hover:**
- **τ_p**: Proton lifetime (mean decay time)
- **M_GUT**: GUT Scale (2.118 × 10¹⁶ GeV)

**Test by:** Hyper-Kamiokande (2030-2037)

---

### 5. Effective Dimension

**ID:** `d-eff-formula`

**Formula:** d_eff = 12 + 0.5(Shadow_ק + Shadow_ח) = 12.576

**Usage:**
```html
<pm-formula formula-id="d-eff-formula"></pm-formula>
```

**Terms with hover:**
- **d_eff**: Effective dimension (12.576 from torsion)
- **0.5**: Ghost coefficient (|c_ghost|/(2*c_matter))

**Python derivation:** `simulations/derive_d_eff_v12_8.py`

---

## Formula Categories

### ESTABLISHED (Green)
Well-known physics formulas with standard citations.

Examples:
- `einstein-field` - Einstein Field Equations
- `clifford-algebra` - Clifford Algebra
- `f-theory-index` - F-theory Generation Formula
- `seesaw-mechanism` - See-saw Mechanism

### THEORY (Purple)
Foundational PM formulas.

Examples:
- `master-action-26d` - Master 26D Action
- `spacetime-26d` - 26D Spacetime Structure
- `clifford-26d` - 26D Clifford Algebra
- `two-time-structure` - Two-Time Structure

### DERIVED (Blue)
Results derived from the theory.

Examples:
- `generation-number` - Three Generations Formula
- `gut-scale` - GUT Scale from Torsion
- `w0-formula` - Dark Energy EoS w₀
- `d-eff-formula` - Effective Dimension

### PREDICTIONS (Pink)
Testable predictions.

Examples:
- `proton-lifetime` - Proton Lifetime
- `normal-hierarchy` - Normal Mass Hierarchy
- `kk-graviton-mass` - KK Graviton Masses
- `gw-dispersion` - GW Dispersion Parameter

---

## Advanced Usage

### Inline Formulas (not in registry)

```html
<pm-formula
    html="E = mc<sup>2</sup>"
    plain="E = mc²"
    label="Einstein's Mass-Energy"
></pm-formula>
```

### Responsive Design

The component automatically adapts to screen size:
- **Desktop:** Tooltips appear above terms
- **Mobile:** Tooltips appear below terms, optimized for touch
- **Small screens:** Formula font size reduces, horizontal scroll enabled

### Custom Styling

The component uses CSS variables for theming:
- `--accent-primary`: Main accent color (#8b7fff)
- `--accent-secondary`: Secondary accent (#ff7eb6)
- `--bg-card`: Card background
- `--text-muted`: Muted text color

---

## Migration Guide

### From Static HTML

**Before:**
```html
<div class="equation-box">
    <span class="eq-content">
        n<sub>gen</sub> = χ<sub>eff</sub>/48 = 144/48 = 3
    </span>
</div>
```

**After:**
```html
<pm-formula formula-id="generation-number"></pm-formula>
```

### From Inline Math

**Before:**
```html
<p>
    The generation number is n<sub>gen</sub> = 3.
</p>
```

**After:**
```html
<p>
    The generation number is <pm-formula formula-id="generation-number" show-label="false"></pm-formula>.
</p>
```

---

## Best Practices

1. **Always use formula IDs** when the formula exists in the registry
2. **Show derivations** for key theoretical results
3. **Hide labels** when embedding formulas inline in text
4. **Group related formulas** in sections for better readability
5. **Link to verification pages** in the derivation metadata

---

## Browser Support

- **Chrome/Edge:** Full support including Shadow DOM
- **Firefox:** Full support
- **Safari:** Full support (iOS 10+)
- **Mobile:** Touch-optimized hover states

---

## Troubleshooting

### Formula not found

**Error:** `Formula not found: my-formula-id`

**Solution:** Check that:
1. The formula ID exists in `formula-registry.js`
2. The registry is loaded before the component
3. The ID spelling is correct (case-sensitive)

### Terms not hoverable

**Solution:** Ensure terms are defined in the formula's `terms` object in the registry.

### Derivation not showing

**Solution:** Add `show-derivation="true"` attribute and ensure the formula has a `derivation` object.

---

## Performance

- **Lazy loading:** Components render on-demand
- **Shadow DOM:** Isolated styles prevent conflicts
- **Minimal dependencies:** Pure vanilla JavaScript
- **Mobile-optimized:** Touch events handled efficiently

---

## Future Enhancements

Planned features:
- LaTeX rendering option
- Export to PDF with formulas
- Copy formula to clipboard
- MathML output for accessibility
- Interactive formula calculator

---

## Examples in the Wild

See these pages for live examples:

- `sections.html#2` - Generation number and topology
- `sections/cosmology.html` - Dark energy formulas
- `sections/gauge-unification.html` - GUT scale and proton decay
- `sections/fermion-sector.html` - PMNS mixing angles
- `sections/predictions.html` - All testable predictions

---

## Version History

- **v13.0** - Enhanced derivation chains, category badges
- **v12.8** - Added d_eff formula with G₂ torsion derivation
- **v12.7** - Initial pm-formula component release
- **v12.6** - Formula registry created

---

## Contact

For questions about the formula system, contact:
- Andrew Keith Watts: AndrewKWatts@Gmail.com
- Documentation: See `js/pm-formula-component.js` for implementation details

---

*Last updated: 2025-12-25*
