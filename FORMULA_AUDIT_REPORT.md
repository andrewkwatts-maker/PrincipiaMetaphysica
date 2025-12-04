# Principia Metaphysica Formula Audit Report

**Generated:** 2025-12-04
**Scope:** Complete formula audit across 9 primary HTML files
**Purpose:** Create centralized formula database to eliminate duplication

---

## Executive Summary

### Overall Statistics
- **Total equation boxes identified:** 181
- **Total formula instances:** 620
- **Files analyzed:** 9
- **Files with hover/tooltip logic:** 6 (67%)
- **Files needing hover logic:** 3 (33%)

### Key Finding
**Over 620 formula instances** are scattered across the website, with significant duplication. The top 9 formulas appear in **3-9 different files**, creating maintenance burden and inconsistency risk.

---

## 1. Most Frequently Repeated Formulas

### Priority 1: Universal Formulas (appear in 9 files)

#### M<sub>Pl</sub> (Planck Mass)
- **Total occurrences:** 120
- **Files:** ALL 9 files
- **Distribution:**
  - cosmology.html: 40x
  - principia-metaphysica-paper.html: 27x
  - geometric-framework.html: 17x
  - predictions.html: 16x
  - pneuma-lagrangian.html: 6x
  - gauge-unification.html: 4x
  - einstein-hilbert-term.html: 4x
  - fermion-sector.html: 3x
  - thermal-time.html: 3x

**Centralization Priority:** CRITICAL
**Reasoning:** Most used formula across entire site; appears 120 times

---

### Priority 2: Near-Universal Formulas (appear in 5-7 files)

#### M<sub>*</sub> (Fundamental Mass Scale)
- **Total occurrences:** 91
- **Files:** 7 files
- **Top appearances:**
  - geometric-framework.html: 47x
  - principia-metaphysica-paper.html: 23x
  - einstein-hilbert-term.html: 11x

**Centralization Priority:** HIGH

#### M<sub>GUT</sub> (GUT Scale)
- **Total occurrences:** 112
- **Files:** 5 files
- **Top appearances:**
  - gauge-unification.html: 54x
  - principia-metaphysica-paper.html: 36x
  - predictions.html: 10x

**Centralization Priority:** HIGH

---

### Priority 3: Multi-File Formulas (appear in 4 files)

#### w<sub>0</sub> (Dark Energy Equation of State)
- **Total occurrences:** 123
- **Files:** 4 files (cosmology, predictions, principia-metaphysica-paper, thermal-time)
- **Top appearances:**
  - cosmology.html: 66x
  - predictions.html: 27x

**Centralization Priority:** HIGH

#### w(z) (Redshift Evolution)
- **Total occurrences:** 76
- **Files:** 4 files
- **Formula:** w(z) = w₀[1 + (α_T/3)ln(1+z)]

**Centralization Priority:** HIGH

#### φ<sub>M</sub> (Mashiach Field)
- **Total occurrences:** 22
- **Files:** 4 files (principia-metaphysica-paper, geometric-framework, cosmology, pneuma-lagrangian)

**Centralization Priority:** MEDIUM

#### R<sub>μν</sub> (Ricci Tensor/Scalar)
- **Total occurrences:** 16
- **Files:** 4 files

**Centralization Priority:** MEDIUM

---

### Priority 4: Specialized Formulas (appear in 3 files)

#### τ<sub>p</sub> (Proton Decay Lifetime)
- **Total occurrences:** 23
- **Files:** 3 files (gauge-unification, predictions, principia-metaphysica-paper)

#### F(R,T,τ) (Modified Gravity)
- **Total occurrences:** 17
- **Files:** 3 files (einstein-hilbert-term, cosmology, principia-metaphysica-paper)
- **Formula:** F(R,T,τ) = R + αT + βT² + γτ + δτ²

---

## 2. Formula Display Methods Found

### A. Equation Boxes (181 total)
```html
<div class="equation-box">
  Formula content here
  <span class="equation-label">Label text</span>
</div>
```

**Distribution:**
- cosmology.html: 70 equation boxes
- thermal-time.html: 40
- fermion-sector.html: 21
- geometric-framework.html: 18
- einstein-hilbert-term.html: 12
- pneuma-lagrangian.html: 9
- gauge-unification.html: 8
- predictions.html: 3
- principia-metaphysica-paper.html: 0 (uses inline formulas)

### B. Formula-Main (Expandable Headers)
```html
<div class="formula-main">
  Main formula display
</div>
```

### C. Main-Equation (Hero Display)
```html
<div class="main-equation">
  M<sub>*</sub><sup>11</sup>R
</div>
```

### D. Inline HTML with subscripts/superscripts
```html
M<sub>Pl</sub><sup>2</sup> = M<sub>*</sub><sup>11</sup> · V<sub>8</sub>
```

---

## 3. Hover/Tooltip Implementation Status

### Files WITH Hover Logic (6 files)
✅ **principia-metaphysica-paper.html**
- Data categories: validation, topology, gauge_unification, dark_energy, proton_decay, pmns_matrix, neutrino_mass_ordering

✅ **geometric-framework.html**
- Data categories: kk_spectrum, proton_decay, shared_dimensions, topology
- PM.* references: 3

✅ **cosmology.html**
- Data categories: dark_energy

✅ **fermion-sector.html**
- Data categories: pmns_matrix, neutrino_mass_ordering, topology

✅ **predictions.html**
- Data categories: pmns_matrix, dark_energy, gauge_unification

✅ **gauge-unification.html**
- Data categories: proton_decay, topology, gauge_unification

### Files WITHOUT Hover Logic (3 files - NEED IMPLEMENTATION)
❌ **thermal-time.html**
- 40 equation boxes
- High formula density (w₀: 13x, w(z): 4x, M_Pl: 3x)

❌ **pneuma-lagrangian.html**
- 9 equation boxes
- Contains Mashiach field details (7x), M_Pl (6x)

❌ **einstein-hilbert-term.html**
- 12 equation boxes
- Core gravity formulas (M_*: 11x, F(R,T,τ): 7x)

---

## 4. Key Formulas by Category

### Core Actions
- **S<sub>26D</sub>** (26D Master Action)
  - Appears in: 2 files (principia-metaphysica-paper, geometric-framework)
  - Formula: S₂₆D = ∫ d²⁶X √|G| R₂₆

- **S<sub>gravity</sub>** (13D Gravitational Action)
  - Appears in: einstein-hilbert-term.html (2x)
  - Formula: S_gravity = M*¹¹ ∫ d¹³x √|G| R₁₃

### Einstein Equations
- **G<sub>μν</sub> = 8πG T<sub>μν</sub>** (Einstein Field Equations)
  - Found across multiple files
  - Modified form: G_μν + Λg_μν = 8πG T_μν

### Particle Physics
- **U<sub>PMNS</sub>** (Neutrino Mixing Matrix)
  - Appears in: 2 files (principia-metaphysica-paper: 3x, fermion-sector: multiple)
  - Complete 4-parameter derivation

- **θ<sub>23</sub>, θ<sub>13</sub>, θ<sub>12</sub>, δ<sub>CP</sub>** (Mixing Angles)
  - neutrino_mixing pattern: 8 occurrences across 2 files

- **U<sub>CKM</sub>** (CKM Matrix)
  - Appears in: principia-metaphysica-paper (3x)

### Cosmology
- **w(z) = w₀[1 + (α_T/3)ln(1+z)]** (Dark Energy Evolution)
  - 76 total occurrences across 4 files
  - Signature prediction of the framework

- **F(R,T,τ) = R + αT + βT² + γτ + δτ²** (Modified Gravity)
  - 17 occurrences across 3 files
  - Includes torsion coupling

### Mass Scales
- **M<sub>Pl</sub>² = M<sub>*</sub>¹¹ · V₈** (Planck Mass Relation)
  - Fundamental relation appearing throughout

---

## 5. Formulas Lacking Hover Logic

### High Priority (appear in non-hover files frequently)

1. **Dark energy w₀ in thermal-time.html** (13 occurrences)
   - Current: Plain text
   - Should have: Tooltip with DESI value, error bars

2. **M<sub>*</sub> in einstein-hilbert-term.html** (11 occurrences)
   - Current: Plain text
   - Should have: Value, derivation path

3. **F(R,T,τ) in einstein-hilbert-term.html** (7 occurrences)
   - Current: Equation boxes without hover
   - Should have: Component breakdown, coefficients

4. **φ<sub>M</sub> in pneuma-lagrangian.html** (7 occurrences)
   - Current: Plain text
   - Should have: VEV value (2.493 M_Pl), uncertainty

---

## 6. Recommended Centralized Database Structure

### Proposed File: `formula-database.js`

```javascript
const FORMULA_DATABASE = {
  // ========================================
  // CATEGORY: Mass Scales
  // ========================================
  'M_Planck': {
    id: 'M_Planck',
    symbol: 'M<sub>Pl</sub>',
    latex: 'M_{\\text{Pl}}',
    value: '2.435 × 10¹⁸ GeV',
    uncertainty: 'Measured',
    description: '4D Planck mass - reduced Planck mass ℏc/G',
    longDescription: 'The fundamental mass scale of 4D gravity, derived from...',
    category: 'scales',
    derivation: 'M_Pl² = M_*¹¹ · V₈',
    usedIn: [
      'principia-metaphysica-paper.html',
      'geometric-framework.html',
      'cosmology.html',
      'fermion-sector.html',
      'predictions.html',
      'gauge-unification.html',
      'thermal-time.html',
      'pneuma-lagrangian.html',
      'einstein-hilbert-term.html'
    ],
    occurrences: 120,
    foundational: true
  },

  'M_star': {
    id: 'M_star',
    symbol: 'M<sub>*</sub>',
    latex: 'M_*',
    value: '~10¹⁶ GeV',
    uncertainty: 'Derived',
    description: 'Fundamental mass scale of 13D effective theory',
    category: 'scales',
    usedIn: ['geometric-framework.html', 'einstein-hilbert-term.html', ...],
    occurrences: 91
  },

  'M_GUT': {
    id: 'M_GUT',
    symbol: 'M<sub>GUT</sub>',
    latex: 'M_{\\text{GUT}}',
    value: '2.118 × 10¹⁶ GeV',
    uncertainty: '±0.12 OOM',
    description: 'Grand Unification scale where forces merge',
    category: 'scales',
    dataCategoryRef: 'gauge_unification',
    dataParamRef: 'M_GUT',
    usedIn: ['gauge-unification.html', 'principia-metaphysica-paper.html', ...],
    occurrences: 112
  },

  // ========================================
  // CATEGORY: Actions
  // ========================================
  'S_26D': {
    id: 'S_26D',
    symbol: 'S<sub>26D</sub>',
    latex: 'S_{26D}',
    formula: 'S<sub>26D</sub> = ∫ d²⁶X √|G| R<sub>26</sub>',
    latexFormula: 'S_{26D} = \\int d^{26}X \\sqrt{|G|} R_{26}',
    description: '26D master action with signature (24,2)',
    category: 'actions',
    usedIn: ['principia-metaphysica-paper.html', 'geometric-framework.html'],
    occurrences: 3
  },

  'S_gravity': {
    id: 'S_gravity',
    symbol: 'S<sub>gravity</sub>',
    formula: 'M<sub>*</sub><sup>11</sup> ∫ d¹³x √|G| R',
    description: '13D effective gravitational action',
    category: 'actions',
    derivedFrom: ['S_26D', 'Sp(2,R) gauge fixing'],
    usedIn: ['einstein-hilbert-term.html'],
    occurrences: 2
  },

  // ========================================
  // CATEGORY: Cosmology
  // ========================================
  'w_0': {
    id: 'w_0',
    symbol: 'w<sub>0</sub>',
    latex: 'w_0',
    value: '-0.8528',
    uncertainty: '±0.06 (DESI)',
    description: 'Present-day dark energy equation of state',
    category: 'cosmology',
    dataCategoryRef: 'dark_energy',
    dataParamRef: 'w0_PM',
    observedValue: '-0.83 ± 0.06',
    sigmaDeviation: '0.38σ',
    usedIn: ['cosmology.html', 'predictions.html', 'thermal-time.html', ...],
    occurrences: 123,
    exactMatch: false
  },

  'w_z': {
    id: 'w_z',
    symbol: 'w(z)',
    formula: 'w(z) = w<sub>0</sub>[1 + (α<sub>T</sub>/3)ln(1+z)]',
    latexFormula: 'w(z) = w_0\\left[1 + \\frac{\\alpha_T}{3}\\ln(1+z)\\right]',
    description: 'Logarithmic dark energy evolution with redshift',
    category: 'cosmology',
    usedIn: ['cosmology.html', 'principia-metaphysica-paper.html', ...],
    occurrences: 76,
    exactMatch: true
  },

  'phi_M': {
    id: 'phi_M',
    symbol: 'φ<sub>M</sub>',
    latex: '\\phi_M',
    value: '2.493 M<sub>Pl</sub>',
    uncertainty: '±5.027 M<sub>Pl</sub>',
    description: 'Mashiach field vacuum expectation value',
    category: 'cosmology',
    usedIn: ['pneuma-lagrangian.html', 'cosmology.html', ...],
    occurrences: 22
  },

  'F_R_T_tau': {
    id: 'F_R_T_tau',
    symbol: 'F(R,T,τ)',
    formula: 'R + αT + βT² + γτ + δτ²',
    description: 'Modified gravity function with torsion coupling',
    category: 'gravity',
    components: {
      'alpha': '0.0045 M<sub>Pl</sub><sup>-2</sup>',
      'gamma': '0.0001 M<sub>Pl</sub><sup>-2</sup>'
    },
    usedIn: ['einstein-hilbert-term.html', 'cosmology.html', ...],
    occurrences: 17
  },

  // ========================================
  // CATEGORY: Particle Physics
  // ========================================
  'U_PMNS': {
    id: 'U_PMNS',
    symbol: 'U<sub>PMNS</sub>',
    latex: 'U_{\\text{PMNS}}',
    description: 'Pontecorvo-Maki-Nakagawa-Sakata neutrino mixing matrix',
    category: 'particles',
    parameters: ['theta_23', 'theta_13', 'theta_12', 'delta_CP'],
    dataCategoryRef: 'pmns_matrix',
    usedIn: ['fermion-sector.html', 'principia-metaphysica-paper.html'],
    occurrences: 3,
    exactMatches: 2
  },

  'tau_p': {
    id: 'tau_p',
    symbol: 'τ<sub>p</sub>',
    latex: '\\tau_p',
    value: '3.84 × 10³⁴ years',
    uncertainty: '±0.18 OOM',
    description: 'Proton decay lifetime',
    category: 'predictions',
    dataCategoryRef: 'proton_decay',
    dataParamRef: 'tau_p_median',
    observedLimit: '> 1.67 × 10³⁴ years',
    usedIn: ['gauge-unification.html', 'predictions.html', ...],
    occurrences: 23
  },

  // ========================================
  // CATEGORY: Einstein Equations
  // ========================================
  'Einstein_equations': {
    id: 'Einstein_equations',
    symbol: 'G<sub>μν</sub>',
    formula: 'G<sub>μν</sub> + Λg<sub>μν</sub> = 8πG T<sub>μν</sub>',
    latexFormula: 'G_{\\mu\\nu} + \\Lambda g_{\\mu\\nu} = 8\\pi G T_{\\mu\\nu}',
    description: 'Einstein field equations with cosmological constant',
    category: 'gravity',
    foundational: true,
    establishedYear: 1915,
    usedIn: ['multiple files'],
    occurrences: 'varies'
  },

  'Ricci_scalar': {
    id: 'Ricci_scalar',
    symbol: 'R',
    latex: 'R',
    formula: 'R = g<sup>μν</sup>R<sub>μν</sub>',
    description: 'Ricci scalar - trace of Ricci tensor',
    category: 'gravity',
    foundational: true,
    usedIn: ['geometric-framework.html', 'einstein-hilbert-term.html', ...],
    occurrences: 16
  }
};

// Helper function to get formula by ID
function getFormula(id) {
  return FORMULA_DATABASE[id];
}

// Helper function to get formulas by category
function getFormulasByCategory(category) {
  return Object.values(FORMULA_DATABASE)
    .filter(f => f.category === category);
}

// Helper function to render formula with tooltip
function renderFormulaWithTooltip(id, options = {}) {
  const formula = FORMULA_DATABASE[id];
  if (!formula) return null;

  const tooltipContent = `
    <div class="var-name">${formula.symbol}</div>
    <div class="var-description">${formula.description}</div>
    ${formula.value ? `<div class="var-value">Value: ${formula.value}</div>` : ''}
    ${formula.uncertainty ? `<div class="var-uncertainty">Uncertainty: ${formula.uncertainty}</div>` : ''}
  `;

  return `
    <span class="formula-var" data-formula-id="${id}">
      ${formula.symbol}
      <div class="var-tooltip">${tooltipContent}</div>
    </span>
  `;
}

export { FORMULA_DATABASE, getFormula, getFormulasByCategory, renderFormulaWithTooltip };
```

---

## 7. Implementation Recommendations

### Phase 1: High-Priority Centralization (Week 1)
1. Create `formula-database.js` with 9 priority formulas:
   - M_Planck, M_star, M_GUT
   - w_0, w(z)
   - phi_M, F(R,T,tau)
   - tau_p, U_PMNS

2. Add hover tooltips to 3 files lacking them:
   - thermal-time.html
   - pneuma-lagrangian.html
   - einstein-hilbert-term.html

3. Create `formula-renderer.js` utility:
   - Auto-generate HTML from database
   - Ensure consistency across files

### Phase 2: Complete Database (Week 2)
4. Add remaining formulas to database:
   - S_26D, S_gravity, Einstein equations
   - Ricci tensor/scalar
   - CKM matrix, neutrino mixing angles
   - All mass hierarchy relations

5. Integrate data-category references:
   - Link to theory-constants-enhanced.js
   - Enable dynamic value updates

### Phase 3: Refactor Existing Files (Week 3)
6. Replace hardcoded formulas with database calls:
   - Start with most-repeated (M_Planck: 120 instances)
   - Move through priority list

7. Standardize display formats:
   - Equation boxes use consistent styling
   - All tooltips follow same pattern

### Phase 4: Validation & Testing (Week 4)
8. Cross-check all formulas for accuracy
9. Verify tooltip functionality
10. Ensure mobile responsiveness

---

## 8. Benefits of Centralization

### Consistency
- Single source of truth for all formulas
- Eliminates copy-paste errors
- Ensures uniform notation

### Maintainability
- Update formula once, propagates everywhere
- Reduce 620 instances to ~50 unique formulas
- Easy to add new formulas

### Enhanced Features
- Centralized hover logic
- Automatic LaTeX rendering
- Dynamic value updates from theory-constants
- Cross-references between formulas

### User Experience
- Consistent tooltips
- Better mobile display
- Search/filter capabilities

---

## 9. Critical Action Items

### Immediate (This Week)
1. ✅ Audit complete (this report)
2. Create formula-database.js skeleton
3. Implement for top 3 formulas (M_Planck, w_0, M_GUT)
4. Add hover logic to thermal-time.html

### Short-term (Next 2 Weeks)
5. Complete formula database (50 formulas)
6. Add hover to pneuma-lagrangian.html, einstein-hilbert-term.html
7. Refactor cosmology.html (highest formula density: 70 boxes)

### Medium-term (Next Month)
8. Refactor all 9 files to use centralized database
9. Add LaTeX rendering support
10. Create formula documentation page

---

## 10. Estimated Impact

### Before Centralization
- 620 formula instances scattered across 9 files
- ~50 unique formulas, each duplicated 3-12 times
- Inconsistent notation in some cases
- 33% of files lack hover tooltips

### After Centralization
- ~50 formulas in central database
- 9 files reference database
- 100% consistent notation
- 100% hover coverage
- 80% reduction in maintenance burden

---

## Appendix A: File-by-File Summary

### principia-metaphysica-paper.html
- Equation boxes: 0 (uses inline formulas)
- Has hover: YES
- Top formulas: M_GUT (36x), M_Pl (27x), w(z) (23x), M_* (23x)
- Data categories: 8 (validation, topology, gauge_unification, dark_energy, proton_decay, pmns_matrix, neutrino_mass_ordering)

### sections/geometric-framework.html
- Equation boxes: 18
- Has hover: YES (3 PM.* refs)
- Top formulas: M_* (47x), M_Pl (17x), M_GUT (9x)
- Data categories: kk_spectrum, proton_decay, shared_dimensions, topology

### sections/cosmology.html
- Equation boxes: 70 (HIGHEST)
- Has hover: YES
- Top formulas: w_0 (66x), M_Pl (40x), w(z) (39x)
- Data categories: dark_energy

### sections/fermion-sector.html
- Equation boxes: 21
- Has hover: YES
- Top formulas: neutrino_mixing (4x), M_Pl (3x)
- Data categories: pmns_matrix, neutrino_mass_ordering, topology

### sections/predictions.html
- Equation boxes: 3
- Has hover: YES
- Top formulas: w_0 (27x), M_Pl (16x), w(z) (10x), M_GUT (10x)
- Data categories: pmns_matrix, dark_energy, gauge_unification

### sections/gauge-unification.html
- Equation boxes: 8
- Has hover: YES
- Top formulas: M_GUT (54x), tau_p (13x), M_Pl (4x)
- Data categories: proton_decay, topology, gauge_unification

### sections/thermal-time.html ⚠️
- Equation boxes: 40 (SECOND HIGHEST)
- Has hover: NO - NEEDS IMPLEMENTATION
- Top formulas: w_0 (13x), w(z) (4x), M_Pl (3x)

### sections/pneuma-lagrangian.html ⚠️
- Equation boxes: 9
- Has hover: NO - NEEDS IMPLEMENTATION
- Top formulas: phi_M (7x), M_Pl (6x), M_* (3x)

### sections/einstein-hilbert-term.html ⚠️
- Equation boxes: 12
- Has hover: NO - NEEDS IMPLEMENTATION
- Top formulas: M_* (11x), F(R,T,tau) (7x), M_Pl (4x)

---

## Appendix B: Data Category Coverage

Current `data-category` attributes found:
- validation
- topology
- gauge_unification
- dark_energy
- proton_decay_channels
- proton_decay
- pmns_matrix
- neutrino_mass_ordering
- kk_spectrum
- shared_dimensions

All integrate with `theory-constants-enhanced.js` tooltip system.

---

## Conclusion

This audit reveals significant opportunity for consolidation. By centralizing the ~50 unique formulas currently scattered across 620 instances, we can dramatically improve maintainability, consistency, and user experience. The three files lacking hover logic (thermal-time, pneuma-lagrangian, einstein-hilbert-term) represent immediate wins for enhancement.

**Recommended next step:** Implement the centralized `formula-database.js` starting with the top 9 formulas (those appearing in 3+ files), which will immediately impact 580+ instances (94% of all formula occurrences).

---

**Report Generated by:** audit_formulas.py
**Full JSON results:** formula_audit_results.json
**Audit output log:** formula_audit_output.txt
