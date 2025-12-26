# Formulas Metadata Schema

This document describes the complete metadata schema for formulas in `theory_output.json`.

## Required Fields

All 62 formulas now have these required fields:

### Core Fields (Always Present)
```json
{
  "id": "string",              // Unique formula identifier (kebab-case)
  "label": "string",           // Human-readable label with section number
  "html": "string",            // HTML-formatted equation
  "latex": "string",           // LaTeX-formatted equation
  "plainText": "string",       // Plain text equation (Unicode)
  "category": "string",        // Formula category (DERIVED, PREDICTIONS, etc.)
  "description": "string",     // Brief description of formula meaning
  "attribution": "string",     // Source (usually "Principia Metaphysica")
  "section": "string",         // Section number in paper
  "relatedFormulas": ["array"] // IDs of related formulas
}
```

### Metadata Fields (Added by fix)
```json
{
  "validated": boolean,           // Whether formula has been computationally validated
  "inputParams": ["array"],       // Parameters that go INTO this formula
  "outputParams": ["array"],      // Parameters that come OUT of this formula
  "units": "string",              // Physical units of output
  "status": "string",             // Formula status: DERIVED, GEOMETRIC, or INPUT
  "references": [                 // Array of academic references
    {
      "id": "string",
      "title": "string",
      "authors": "string",
      "year": number,
      "arxiv": "string (optional)",
      "description": "string"
    }
  ]
}
```

## Parameter Naming Convention

Parameters use semantic naming: `category.PARAMETER_NAME`

### Categories

| Category | Description | Example Parameters |
|----------|-------------|-------------------|
| `topology` | Topological invariants | `topology.CHI_EFF`, `topology.n_gen`, `topology.B2` |
| `gauge` | Gauge theory parameters | `gauge.M_GUT`, `gauge.ALPHA_GUT`, `gauge.ALPHA_S` |
| `higgs` | Higgs sector | `higgs.VEV`, `higgs.M_H`, `higgs.LAMBDA` |
| `neutrino` | Neutrino sector | `neutrino.DELTA_M21_SQ`, `neutrino.M_MAJORANA` |
| `fermion` | Fermion masses | `fermion.M_TOP`, `fermion.M_BOTTOM`, `fermion.M_TAU` |
| `cosmology` | Cosmological parameters | `cosmology.W0`, `cosmology.WA`, `cosmology.H` |
| `pneuma` | Pneuma field | `pneuma.VEV`, `pneuma.DIRAC` |
| `moduli` | Moduli fields | `moduli.RE_S`, `moduli.RE_T` |
| `dimensions` | Spacetime dimensions | `dimensions.D_EFFECTIVE`, `dimensions.D_SPACETIME` |
| `thermal` | Thermal/statistical | `thermal.BETA`, `thermal.ALPHA_T` |
| `yukawa` | Yukawa couplings | `yukawa.Y_TOP`, `yukawa.Y_INSTANTON` |
| `mixing` | Mixing parameters | `mixing.V_CKM`, `mixing.DELTA_CP` |
| `kk` | Kaluza-Klein | `kk.M_KK` |
| `dm` | Dark matter | `dm.OMEGA_MIRROR`, `dm.RHO_DM` |
| `decay` | Decay parameters | `decay.TAU_PROTON`, `decay.BR_E_PI0` |

## Status Values

| Status | Meaning | Count |
|--------|---------|-------|
| `DERIVED` | Derived from theory/calculations | 52 formulas |
| `GEOMETRIC` | Fundamental geometric/topological fact | 10 formulas |
| `INPUT` | Experimental input value | 0 formulas |

## Units

Common unit values:

| Unit | Count | Example Formulas |
|------|-------|------------------|
| `dimensionless` | 40 | Couplings, ratios, numbers |
| `GeV` | 12 | Masses, scales |
| `GeV^4` | 3 | Potentials |
| `eV^2` | 2 | Neutrino mass splittings |
| `years` | 1 | Proton lifetime |
| `TeV` | 1 | KK graviton mass |
| `GeV^3` | 1 | Superpotential |
| `degrees` | 2 | Angles |

## Optional Enhancement Fields

These fields are present in many but not all formulas:

```json
{
  "terms": {                    // Glossary of terms in equation
    "symbol": {
      "name": "string",
      "description": "string",
      "link": "string (optional)"
    }
  },
  "derivation": {               // Step-by-step derivation
    "parentFormulas": ["array"],
    "establishedPhysics": ["array"],
    "steps": ["array"],
    "method": "string",
    "difficulty": "string",
    "verificationPage": "string"
  },
  "computedValue": number,      // Theoretical prediction
  "experimentalValue": number,  // Measured value
  "experimentalError": number,  // Measurement uncertainty
  "sigmaDeviation": number,     // Statistical significance
  "simulationFile": "string",   // Python simulation file
  "learningResources": [        // Educational materials
    {
      "title": "string",
      "url": "string",
      "type": "string",
      "level": "string",
      "duration": "string (optional)",
      "description": "string"
    }
  ],
  "notes": "string",            // Additional context
  "testability": {              // Experimental verification info
    "observable": "string",
    "method": "string",
    "timeline": "string"
  }
}
```

## Example: Complete Formula

```json
{
  "id": "proton-lifetime",
  "label": "(5.10) Proton Lifetime",
  "html": "τ<sub>p</sub> = M<sub>GUT</sub>⁴/(α<sub>GUT</sub>² m<sub>p</sub>⁵) × S² = 8.15 × 10³⁴ years",
  "latex": "\\tau_p = \\frac{M_{GUT}^4}{\\alpha_{GUT}^2 m_p^5} \\times S^2 = 8.15 \\times 10^{34}\\,\\text{years}",
  "plainText": "τ_p = M_GUT⁴/(α_GUT² m_p⁵) × S² = 8.15 × 10³⁴ years",
  "category": "PREDICTIONS",
  "description": "Predicted proton lifetime from geometric GUT suppression",
  "attribution": "Principia Metaphysica",
  "status": "DERIVED",
  "section": "5",

  "validated": false,
  "inputParams": [
    "gauge.M_GUT",
    "gauge.ALPHA_GUT"
  ],
  "outputParams": [
    "decay.TAU_PROTON"
  ],
  "units": "years",

  "terms": { /* ... */ },
  "derivation": { /* ... */ },

  "computedValue": 8.149598829720118e+34,
  "simulationFile": "simulations/proton_decay_geometric_v13_0.py",

  "references": [
    {
      "id": "nath2006",
      "title": "Proton Stability in Grand Unified Theories",
      "authors": "Nath, P., Fileviez Perez, P.",
      "year": 2006,
      "arxiv": "hep-ph/0601023",
      "description": "Review of proton decay in GUT models"
    }
  ],

  "learningResources": [ /* ... */ ],
  "relatedFormulas": [
    "gut-scale",
    "proton-branching",
    "gut-coupling"
  ]
}
```

## Validation Checklist

When adding or modifying formulas, ensure:

- [ ] `validated` field is present (boolean)
- [ ] `inputParams` array is present (empty `[]` for axioms/constants)
- [ ] `outputParams` array is present and non-empty
- [ ] `units` string is present and accurate
- [ ] `status` is one of: `DERIVED`, `GEOMETRIC`, `INPUT`
- [ ] Either `references` array OR `derivation` object is present
- [ ] Parameter names follow `category.PARAMETER_NAME` convention
- [ ] All referenced parameters match those in parameters section

## Usage Examples

### Finding formulas by input parameter
```python
formulas_using_gut_scale = [
    f for f in formulas.values()
    if 'gauge.M_GUT' in f.get('inputParams', [])
]
```

### Building dependency graph
```python
dependencies = {}
for fid, f in formulas.items():
    inputs = f.get('inputParams', [])
    outputs = f.get('outputParams', [])
    dependencies[fid] = {'inputs': inputs, 'outputs': outputs}
```

### Filtering by status
```python
geometric_formulas = [
    f for f in formulas.values()
    if f.get('status') == 'GEOMETRIC'
]
```

### Finding unvalidated predictions
```python
unvalidated = [
    f for f in formulas.values()
    if not f.get('validated', False) and f.get('category') == 'PREDICTIONS'
]
```

## Change Log

### 2025-12-26: Initial Complete Schema
- Added `validated` to all 62 formulas
- Added `inputParams` to 30 formulas (32→62)
- Added `outputParams` to 44 formulas (18→62)
- Added `units` to 36 formulas (26→62)
- Normalized `status` for 31 formulas (31→62)
- Added `references` to 27 formulas (35→62 with refs or derivation)
