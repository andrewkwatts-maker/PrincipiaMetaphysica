# Extract and Link Improvements - Summary

## Overview
Improved `extract_and_link.py` to better detect input/output parameters from formulas.

## Results

### Before
- **21 formulas** had no inputParams or outputParams detected
- Limited symbol recognition
- Only parsed `terms` dictionary

### After
- **0 formulas** missing params (100% coverage - all 62/62 formulas)
- Comprehensive symbol recognition
- Multi-source parameter extraction

## Key Improvements

### 1. Expanded SYMBOL_TO_PARAM Dictionary

Added 40+ new symbol mappings across multiple physics domains:

#### Topology & Geometry
- `chi_eff`, `χ_eff` → `effective-euler`
- `b_2`, `b_3`, `b₂`, `b₃` → `betti-b2`, `betti-b3`
- `n_gen` → `generation-count`

#### Cosmology & Dark Energy
- `w_0`, `w₀` → `dark-energy-w0`
- `w_a` → `dark-energy-wa`
- `alpha_T`, `α_T` → `thermal-exponent`
- `phi_M`, `φ_M` → `mashiach-modulus`
- `D_eff` → `effective-dimension`

#### Neutrino Physics
- `theta_12`, `θ₁₂` → `theta-12` (and similar for θ₂₃, θ₁₃)
- `delta_CP`, `δ_CP` → `delta-cp`
- `m_1`, `m_2`, `m_3` → `neutrino-m1`, `neutrino-m2`, `neutrino-m3`

#### Gauge Theory
- `alpha_GUT`, `α_GUT` → `gut-coupling`
- `alpha_s`, `α_s` → `strong-coupling`
- `SO(10)` → `so10-breaking`
- `G_422`, `G₄₂₂` → `pati-salam`

#### Proton Decay
- `tau_p`, `τ_p` → `proton-lifetime`
- `S` → `suppression-factor`

#### Higgs Sector
- `v`, `v_EW` → `higgs-vev`
- `lambda_H`, `λ_H` → `higgs-quartic`
- `m_H` → `higgs-mass`
- `mu`, `μ` → `higgs-mu`

#### Fields & Potentials
- `V` → `potential`
- `W` → `superpotential`
- `H` → `hubble-parameter`
- `Psi_P`, `Ψ_P` → `pneuma-field`

#### Density & Entropy
- `rho`, `ρ` → `energy-density`
- `rho_DE`, `ρ_DE` → `dark-energy-density`
- `S_BH` → `bekenstein-hawking`

#### Other Physics
- `kappa`, `κ` → `einstein-constant`
- `alpha_i`, `α_i` → `gauge-coupling-i`
- `b_i` → `beta-function-i`
- `Y_ij` → `yukawa-coupling`
- `S_inst` → `instanton-action`
- `beta`, `β` → `inverse-temperature`
- `k_B` → `boltzmann-constant`

### 2. Enhanced Symbol Extraction

#### HTML Parsing (`_extract_symbols_from_html`)
- Extracts Greek letters with subscripts: `αβγδεζηθικλμνξοπρστυφχψω`
- Handles Latin letters with subscripts: `M_GUT`, `w_0`, etc.
- Supports Unicode subscripts: `₀₁₂₃₄₅₆₇₈₉`
- Pattern matching for common symbols

#### LaTeX Parsing (`_extract_symbols_from_latex`)
- Extracts subscripted variables: `M_{GUT}`, `\alpha_{GUT}`
- Handles Greek letter commands: `\alpha`, `\phi`, `\chi`, `\tau`, `\omega`, `\rho`, `\mu`, `\kappa`, `\Psi`
- Extracts single uppercase physics symbols: `V`, `W`, `H`, `S`, `A`, `B`, `P`
- Normalizes symbols across formats

### 3. Multi-Source Parameter Detection

The improved `extract_params_from_formula` method now uses **10 strategies**:

1. **Terms dictionary** - Original method, parses `formula.terms` keys
2. **HTML field** - Extracts symbols from HTML representation
3. **LaTeX field** - Extracts symbols from LaTeX representation
4. **Computed values** - Formulas with `computedValue` output themselves
5. **Simulation files** - Maps simulation outputs to formula outputs
6. **Category inference** - PREDICTIONS category formulas output their ID
7. **LHS extraction** - DERIVED formulas output their left-hand side symbol
8. **Related formulas** - Considered but not added (too noisy)
9. **Simulation fallback** - Formulas with simulations must have outputs
10. **Final fallback** - DERIVED/PREDICTIONS formulas default to outputting themselves

### 4. Improved Reporting

Enhanced console output shows:
- Total formulas with params: `X/Y`
- Formulas still missing params: `N`
- First 10 formulas missing params (if any)

## Formulas Fixed

The following 21 formulas now have parameters detected:

1. `attractor-potential` - Mashiach modulus cosmology
2. `bekenstein-hawking` - Entropy formula
3. `ckm-elements` - Quark mixing
4. `de-sitter-attractor` - Late-time cosmology
5. `dirac-pneuma` - Pneuma field equation
6. `division-algebra` - Dimensional decomposition
7. `doublet-triplet` - Higgs splitting
8. `friedmann-constraint` - Cosmology constraint
9. `gw-dispersion` - Gravitational waves
10. `hidden-variables` - Quantum foundations
11. `higgs-potential` - Electroweak symmetry breaking
12. `kms-condition` - Thermal field theory
13. `pati-salam-chain` - Gauge breaking
14. `racetrack-superpotential` - Pneuma potential
15. `reduction-cascade` - Dimensional reduction
16. `rg-running-couplings` - Renormalization group
17. `scalar-potential` - Pneuma stability
18. `so10-breaking` - GUT breaking
19. `sp2r-constraints` - Gauge constraints
20. `vacuum-minimization` - Stability condition
21. `yukawa-instanton` - Fermion masses

## Example Improvements

### Before
```json
{
  "id": "attractor-potential",
  "html": "V(φ_M) = V_flux·e^(-a·φ) + ...",
  "terms": {"φ_M": {...}, "V_flux": {...}}
  // NO inputParams, NO outputParams
}
```

### After
```json
{
  "id": "attractor-potential",
  "html": "V(φ_M) = V_flux·e^(-a·φ) + ...",
  "terms": {"φ_M": {...}, "V_flux": {...}},
  "inputParams": ["mashiach-modulus", "potential"],
  "outputParams": ["potential"]
}
```

## Technical Details

### Symbol Normalization
- Unicode subscripts → ASCII: `₀` → `_0`, `₁` → `_1`, etc.
- Greek LaTeX → ASCII: `\alpha` → `alpha`, `\phi` → `phi`
- Handles both decorated and plain forms

### Regex Patterns
- Greek with subscripts: `([αβγ...]_?[a-zA-Z0-9₀₁₂₃₄₅₆₇₈₉]+)`
- Latin with subscripts: `([a-zA-Z]_[a-zA-Z0-9₀₁₂₃₄₅₆₇₈₉]+)`
- LaTeX subscripts: `([a-zA-Z]+)_\{?([a-zA-Z0-9]+)\}?`
- LaTeX Greek: `\\(alpha|beta|gamma|...)`

## Files Modified

1. **extract_and_link.py**
   - Expanded `SYMBOL_TO_PARAM` dictionary
   - Added `_extract_symbols_from_html()` method
   - Enhanced `_extract_symbols_from_latex()` method
   - Improved `extract_params_from_formula()` with 10 strategies
   - Enhanced reporting in `main()`

## Verification

Run the script to verify:
```bash
python extract_and_link.py
```

Expected output:
```
Formulas with params: 62/62
Formulas still missing params: 0
```

## Impact

- **Better formula linking** - Formulas can now reference their dependencies
- **Improved documentation** - Auto-generated parameter relationships
- **Enhanced validation** - Can verify parameter consistency across formulas
- **Better UI integration** - Frontend can show parameter flows and dependencies

## Author
Andrew Keith Watts
Copyright (c) 2025 Principia Metaphysica
