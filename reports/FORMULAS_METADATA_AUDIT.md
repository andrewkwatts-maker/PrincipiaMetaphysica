# Formulas Metadata Audit Report

**Generated:** 2025-12-26
**Source:** `theory_output.json`

## Summary

- **Total Formulas:** 62
- **Complete Formulas:** 0 (0.0%)
- **Incomplete Formulas:** 62 (100.0%)

### Key Findings

All 62 formulas are missing at least some required metadata fields. The most critical gaps are:
- **100% missing `validated`**: No formula has validation status tracked
- **100% missing `inputs`**: Using `inputParams` instead (present in 51.6% of formulas)
- **100% missing `outputs`**: Using `outputParams` instead (present in 29.0% of formulas)
- **50% missing `status`**: Lifecycle tracking incomplete
- **43.5% missing derivation/references**: 27 formulas lack provenance information

### Current Field Usage

The formulas use alternative field names rather than the checked standard fields:
- `plainText` (100%) instead of `plain_text`
- `inputParams` (51.6%) instead of `inputs`
- `outputParams` (29.0%) instead of `outputs`
- `references` (56.5%) exists but not `derivation_chain`

## Missing Fields Statistics

Note: This table shows fields that were checked against standard naming conventions. The actual data uses alternative field names (see Key Findings above).

| Field | Count | Percentage |
|-------|-------|------------|
| `validated` | 62 | 100.0% |
| `inputs` | 62 | 100.0% |
| `outputs` | 62 | 100.0% |
| `status` | 31 | 50.0% |
| `derivation_chain/references` | 27 | 43.5% |

## Actual Field Coverage Statistics

This shows the actual fields present in the formulas:

| Field | Present | Missing | Coverage |
|-------|---------|---------|----------|
| **Universal fields (100%)** ||||
| `id`, `label`, `html`, `latex`, `plainText` | 62 | 0 | 100.0% |
| `category`, `description`, `attribution` | 62 | 0 | 100.0% |
| `section`, `relatedFormulas` | 62 | 0 | 100.0% |
| **High coverage (>80%)** ||||
| `simulationFile` | 54 | 8 | 87.1% |
| `terms` | 51 | 11 | 82.3% |
| **Medium coverage (50-80%)** ||||
| `references` | 35 | 27 | 56.5% |
| `computedValue` | 34 | 28 | 54.8% |
| `inputParams` | 32 | 30 | 51.6% |
| `status` | 31 | 31 | 50.0% |
| **Low coverage (<50%)** ||||
| `units` | 26 | 36 | 41.9% |
| `learningResources` | 23 | 39 | 37.1% |
| `outputParams` | 18 | 44 | 29.0% |
| `notes` | 17 | 45 | 27.4% |
| `experimentalValue` | 15 | 47 | 24.2% |
| `sigmaDeviation` | 15 | 47 | 24.2% |
| `derivation` | 13 | 49 | 21.0% |
| `experimentalError` | 7 | 55 | 11.3% |
| `testability` | 2 | 60 | 3.2% |
| **Critical missing (0%)** ||||
| `validated` | 0 | 62 | 0.0% |

## Priority Formulas Needing Attention

The following formulas are missing the most critical metadata fields (status, inputParams, outputParams, references/derivation, units):

### Highest Priority (Missing 6 of 6 fields)

These 11 formulas need the most work:

1. `division-algebra`
2. `effective-torsion-spinor`
3. `ghost-coefficient`
4. `gw-dispersion-alt`
5. `gw-dispersion-coeff`
6. `higgs-quartic`
7. `kappa-gut-coefficient`
8. `kms-condition`
9. `proton-branching`
10. `thermal-time`
11. `tomita-takesaki`

### High Priority (Missing 5 of 6 fields)

These formulas have `inputParams` but are missing other critical metadata:

- `attractor-potential`
- `de-sitter-attractor`
- `dirac-pneuma`
- `friedmann-constraint`
- `gw-dispersion`
- `hidden-variables`
- `higgs-potential`
- `pati-salam-chain`
- `rg-running-couplings`
- `vacuum-minimization`

### Completeness Breakdown

- **11 formulas** missing 6 critical fields (highest priority)
- **10 formulas** missing 5 critical fields (high priority)
- **8 formulas** missing 4 critical fields (medium priority)
- **33 formulas** missing 1-3 critical fields (lower priority)

## Incomplete Formulas (Detailed)

Found 62 formulas with missing metadata (based on checked field names):

### `attractor-potential`

**Missing fields:** `validated`, `inputs`, `outputs`, `derivation_chain/references`, `status`

**Present fields:** `id`, `label`, `plain_text/latex`, `category`

**All available fields:** `id`, `label`, `html`, `latex`, `plainText`, `category`, `description`, `attribution`, `section`, `terms`, `simulationFile`, `learningResources`, `relatedFormulas`, `inputParams`

### `de-sitter-attractor`

**Missing fields:** `validated`, `inputs`, `outputs`, `derivation_chain/references`, `status`

**Present fields:** `id`, `label`, `plain_text/latex`, `category`

**All available fields:** `id`, `label`, `html`, `latex`, `plainText`, `category`, `description`, `attribution`, `section`, `simulationFile`, `learningResources`, `relatedFormulas`, `inputParams`, `notes`

### `dirac-pneuma`

**Missing fields:** `validated`, `inputs`, `outputs`, `derivation_chain/references`, `status`

**Present fields:** `id`, `label`, `plain_text/latex`, `category`

**All available fields:** `id`, `label`, `html`, `latex`, `plainText`, `category`, `description`, `attribution`, `section`, `terms`, `simulationFile`, `relatedFormulas`, `inputParams`

### `division-algebra`

**Missing fields:** `validated`, `inputs`, `outputs`, `derivation_chain/references`, `status`

**Present fields:** `id`, `label`, `plain_text/latex`, `category`

**All available fields:** `id`, `label`, `html`, `latex`, `plainText`, `category`, `description`, `attribution`, `section`, `terms`, `learningResources`, `relatedFormulas`, `notes`

### `effective-torsion-spinor`

**Missing fields:** `validated`, `inputs`, `outputs`, `derivation_chain/references`, `status`

**Present fields:** `id`, `label`, `plain_text/latex`, `category`

**All available fields:** `id`, `label`, `html`, `latex`, `plainText`, `category`, `description`, `attribution`, `section`, `terms`, `computedValue`, `experimentalValue`, `sigmaDeviation`, `simulationFile`, `relatedFormulas`, `notes`

### `friedmann-constraint`

**Missing fields:** `validated`, `inputs`, `outputs`, `derivation_chain/references`, `status`

**Present fields:** `id`, `label`, `plain_text/latex`, `category`

**All available fields:** `id`, `label`, `html`, `latex`, `plainText`, `category`, `description`, `attribution`, `section`, `terms`, `simulationFile`, `learningResources`, `relatedFormulas`, `inputParams`

### `ghost-coefficient`

**Missing fields:** `validated`, `inputs`, `outputs`, `derivation_chain/references`, `status`

**Present fields:** `id`, `label`, `plain_text/latex`, `category`

**All available fields:** `id`, `label`, `html`, `latex`, `plainText`, `category`, `description`, `attribution`, `section`, `terms`, `computedValue`, `simulationFile`, `relatedFormulas`

### `gw-dispersion`

**Missing fields:** `validated`, `inputs`, `outputs`, `derivation_chain/references`, `status`

**Present fields:** `id`, `label`, `plain_text/latex`, `category`

**All available fields:** `id`, `label`, `html`, `latex`, `plainText`, `category`, `description`, `attribution`, `section`, `terms`, `simulationFile`, `relatedFormulas`, `inputParams`, `testability`

### `gw-dispersion-alt`

**Missing fields:** `validated`, `inputs`, `outputs`, `derivation_chain/references`, `status`

**Present fields:** `id`, `label`, `plain_text/latex`, `category`

**All available fields:** `id`, `label`, `html`, `latex`, `plainText`, `category`, `description`, `attribution`, `section`, `terms`, `computedValue`, `simulationFile`, `relatedFormulas`, `notes`

### `gw-dispersion-coeff`

**Missing fields:** `validated`, `inputs`, `outputs`, `derivation_chain/references`, `status`

**Present fields:** `id`, `label`, `plain_text/latex`, `category`

**All available fields:** `id`, `label`, `html`, `latex`, `plainText`, `category`, `description`, `attribution`, `section`, `computedValue`, `simulationFile`, `relatedFormulas`

### `hidden-variables`

**Missing fields:** `validated`, `inputs`, `outputs`, `derivation_chain/references`, `status`

**Present fields:** `id`, `label`, `plain_text/latex`, `category`

**All available fields:** `id`, `label`, `html`, `latex`, `plainText`, `category`, `description`, `attribution`, `section`, `terms`, `learningResources`, `relatedFormulas`, `inputParams`, `notes`

### `higgs-potential`

**Missing fields:** `validated`, `inputs`, `outputs`, `derivation_chain/references`, `status`

**Present fields:** `id`, `label`, `plain_text/latex`, `category`

**All available fields:** `id`, `label`, `html`, `latex`, `plainText`, `category`, `description`, `attribution`, `section`, `terms`, `derivation`, `simulationFile`, `relatedFormulas`, `inputParams`, `notes`

### `higgs-quartic`

**Missing fields:** `validated`, `inputs`, `outputs`, `derivation_chain/references`, `status`

**Present fields:** `id`, `label`, `plain_text/latex`, `category`

**All available fields:** `id`, `label`, `html`, `latex`, `plainText`, `category`, `description`, `attribution`, `section`, `terms`, `computedValue`, `experimentalValue`, `sigmaDeviation`, `simulationFile`, `relatedFormulas`

### `kappa-gut-coefficient`

**Missing fields:** `validated`, `inputs`, `outputs`, `derivation_chain/references`, `status`

**Present fields:** `id`, `label`, `plain_text/latex`, `category`

**All available fields:** `id`, `label`, `html`, `latex`, `plainText`, `category`, `description`, `attribution`, `section`, `terms`, `computedValue`, `simulationFile`, `relatedFormulas`

### `kms-condition`

**Missing fields:** `validated`, `inputs`, `outputs`, `derivation_chain/references`, `status`

**Present fields:** `id`, `label`, `plain_text/latex`, `category`

**All available fields:** `id`, `label`, `html`, `latex`, `plainText`, `category`, `description`, `attribution`, `section`, `terms`, `learningResources`, `relatedFormulas`, `notes`

### `pati-salam-chain`

**Missing fields:** `validated`, `inputs`, `outputs`, `derivation_chain/references`, `status`

**Present fields:** `id`, `label`, `plain_text/latex`, `category`

**All available fields:** `id`, `label`, `html`, `latex`, `plainText`, `category`, `description`, `attribution`, `section`, `terms`, `derivation`, `simulationFile`, `relatedFormulas`, `inputParams`, `notes`

### `proton-branching`

**Missing fields:** `validated`, `inputs`, `outputs`, `derivation_chain/references`, `status`

**Present fields:** `id`, `label`, `plain_text/latex`, `category`

**All available fields:** `id`, `label`, `html`, `latex`, `plainText`, `category`, `description`, `attribution`, `section`, `computedValue`, `simulationFile`, `relatedFormulas`, `testability`

### `rg-running-couplings`

**Missing fields:** `validated`, `inputs`, `outputs`, `derivation_chain/references`, `status`

**Present fields:** `id`, `label`, `plain_text/latex`, `category`

**All available fields:** `id`, `label`, `html`, `latex`, `plainText`, `category`, `description`, `attribution`, `section`, `terms`, `simulationFile`, `relatedFormulas`, `inputParams`, `notes`

### `thermal-time`

**Missing fields:** `validated`, `inputs`, `outputs`, `derivation_chain/references`, `status`

**Present fields:** `id`, `label`, `plain_text/latex`, `category`

**All available fields:** `id`, `label`, `html`, `latex`, `plainText`, `category`, `description`, `attribution`, `section`, `terms`, `simulationFile`, `relatedFormulas`

### `tomita-takesaki`

**Missing fields:** `validated`, `inputs`, `outputs`, `derivation_chain/references`, `status`

**Present fields:** `id`, `label`, `plain_text/latex`, `category`

**All available fields:** `id`, `label`, `html`, `latex`, `plainText`, `category`, `description`, `attribution`, `section`, `terms`, `learningResources`, `relatedFormulas`, `notes`

### `vacuum-minimization`

**Missing fields:** `validated`, `inputs`, `outputs`, `derivation_chain/references`, `status`

**Present fields:** `id`, `label`, `plain_text/latex`, `category`

**All available fields:** `id`, `label`, `html`, `latex`, `plainText`, `category`, `description`, `attribution`, `section`, `terms`, `derivation`, `simulationFile`, `relatedFormulas`, `inputParams`

### `bekenstein-hawking`

**Missing fields:** `validated`, `inputs`, `outputs`, `derivation_chain/references`

**Present fields:** `id`, `label`, `plain_text/latex`, `category`, `status`

**All available fields:** `id`, `label`, `html`, `latex`, `plainText`, `category`, `description`, `attribution`, `status`, `section`, `terms`, `units`, `relatedFormulas`, `notes`

### `bottom-quark-mass`

**Missing fields:** `validated`, `inputs`, `outputs`, `derivation_chain/references`

**Present fields:** `id`, `label`, `plain_text/latex`, `category`, `status`

**All available fields:** `id`, `label`, `html`, `latex`, `plainText`, `category`, `description`, `attribution`, `status`, `section`, `terms`, `computedValue`, `units`, `experimentalValue`, `experimentalError`, `sigmaDeviation`, `simulationFile`, `relatedFormulas`

### `cp-phase-geometric`

**Missing fields:** `validated`, `inputs`, `outputs`, `status`

**Present fields:** `id`, `label`, `plain_text/latex`, `category`, `derivation_chain/references`

**All available fields:** `id`, `label`, `html`, `latex`, `plainText`, `category`, `description`, `attribution`, `section`, `terms`, `computedValue`, `units`, `simulationFile`, `references`, `relatedFormulas`

### `doublet-triplet`

**Missing fields:** `validated`, `inputs`, `outputs`, `status`

**Present fields:** `id`, `label`, `plain_text/latex`, `category`, `derivation_chain/references`

**All available fields:** `id`, `label`, `html`, `latex`, `plainText`, `category`, `description`, `attribution`, `section`, `terms`, `references`, `learningResources`, `relatedFormulas`, `inputParams`, `notes`

### `hierarchy-ratio`

**Missing fields:** `validated`, `inputs`, `outputs`, `status`

**Present fields:** `id`, `label`, `plain_text/latex`, `category`, `derivation_chain/references`

**All available fields:** `id`, `label`, `html`, `latex`, `plainText`, `category`, `description`, `attribution`, `section`, `terms`, `references`, `learningResources`, `relatedFormulas`, `notes`

### `higgs-mass`

**Missing fields:** `validated`, `inputs`, `outputs`, `derivation_chain/references`

**Present fields:** `id`, `label`, `plain_text/latex`, `category`, `status`

**All available fields:** `id`, `label`, `html`, `latex`, `plainText`, `category`, `description`, `attribution`, `status`, `section`, `terms`, `computedValue`, `units`, `experimentalValue`, `experimentalError`, `sigmaDeviation`, `simulationFile`, `relatedFormulas`, `inputParams`, `notes`

### `higgs-vev`

**Missing fields:** `validated`, `inputs`, `outputs`, `status`

**Present fields:** `id`, `label`, `plain_text/latex`, `category`, `derivation_chain/references`

**All available fields:** `id`, `label`, `html`, `latex`, `plainText`, `category`, `description`, `attribution`, `section`, `terms`, `computedValue`, `units`, `simulationFile`, `references`, `relatedFormulas`, `inputParams`

### `mirror-temp-ratio`

**Missing fields:** `validated`, `inputs`, `outputs`, `derivation_chain/references`

**Present fields:** `id`, `label`, `plain_text/latex`, `category`, `status`

**All available fields:** `id`, `label`, `html`, `latex`, `plainText`, `category`, `description`, `attribution`, `status`, `section`, `terms`, `derivation`, `computedValue`, `simulationFile`, `relatedFormulas`

### `planck-mass-derivation`

**Missing fields:** `validated`, `inputs`, `outputs`, `status`

**Present fields:** `id`, `label`, `plain_text/latex`, `category`, `derivation_chain/references`

**All available fields:** `id`, `label`, `html`, `latex`, `plainText`, `category`, `description`, `attribution`, `section`, `terms`, `references`, `learningResources`, `relatedFormulas`

### `racetrack-superpotential`

**Missing fields:** `validated`, `inputs`, `outputs`, `status`

**Present fields:** `id`, `label`, `plain_text/latex`, `category`, `derivation_chain/references`

**All available fields:** `id`, `label`, `html`, `latex`, `plainText`, `category`, `description`, `attribution`, `section`, `terms`, `derivation`, `simulationFile`, `references`, `relatedFormulas`, `inputParams`, `outputParams`

### `scalar-potential`

**Missing fields:** `validated`, `inputs`, `outputs`, `derivation_chain/references`

**Present fields:** `id`, `label`, `plain_text/latex`, `category`, `status`

**All available fields:** `id`, `label`, `html`, `latex`, `plainText`, `category`, `description`, `attribution`, `status`, `section`, `terms`, `units`, `simulationFile`, `learningResources`, `relatedFormulas`

### `seesaw-mechanism`

**Missing fields:** `validated`, `inputs`, `outputs`, `status`

**Present fields:** `id`, `label`, `plain_text/latex`, `category`, `derivation_chain/references`

**All available fields:** `id`, `label`, `html`, `latex`, `plainText`, `category`, `description`, `attribution`, `section`, `terms`, `simulationFile`, `references`, `learningResources`, `relatedFormulas`, `inputParams`, `outputParams`

### `so10-breaking`

**Missing fields:** `validated`, `inputs`, `outputs`, `status`

**Present fields:** `id`, `label`, `plain_text/latex`, `category`, `derivation_chain/references`

**All available fields:** `id`, `label`, `html`, `latex`, `plainText`, `category`, `description`, `attribution`, `section`, `simulationFile`, `references`, `relatedFormulas`, `inputParams`

### `sp2r-constraints`

**Missing fields:** `validated`, `inputs`, `outputs`, `status`

**Present fields:** `id`, `label`, `plain_text/latex`, `category`, `derivation_chain/references`

**All available fields:** `id`, `label`, `html`, `latex`, `plainText`, `category`, `description`, `attribution`, `section`, `terms`, `derivation`, `simulationFile`, `references`, `learningResources`, `relatedFormulas`, `inputParams`, `outputParams`

### `tau-lepton-mass`

**Missing fields:** `validated`, `inputs`, `outputs`, `derivation_chain/references`

**Present fields:** `id`, `label`, `plain_text/latex`, `category`, `status`

**All available fields:** `id`, `label`, `html`, `latex`, `plainText`, `category`, `description`, `attribution`, `status`, `section`, `terms`, `computedValue`, `units`, `experimentalValue`, `experimentalError`, `sigmaDeviation`, `simulationFile`, `relatedFormulas`

### `yukawa-instanton`

**Missing fields:** `validated`, `inputs`, `outputs`, `status`

**Present fields:** `id`, `label`, `plain_text/latex`, `category`, `derivation_chain/references`

**All available fields:** `id`, `label`, `html`, `latex`, `plainText`, `category`, `description`, `attribution`, `section`, `terms`, `simulationFile`, `references`, `learningResources`, `relatedFormulas`, `inputParams`, `notes`

### `ckm-elements`

**Missing fields:** `validated`, `inputs`, `outputs`

**Present fields:** `id`, `label`, `plain_text/latex`, `category`, `derivation_chain/references`, `status`

**All available fields:** `id`, `label`, `html`, `latex`, `plainText`, `category`, `description`, `attribution`, `status`, `section`, `simulationFile`, `references`, `learningResources`, `relatedFormulas`, `notes`

### `dark-energy-w0`

**Missing fields:** `validated`, `inputs`, `outputs`

**Present fields:** `id`, `label`, `plain_text/latex`, `category`, `derivation_chain/references`, `status`

**All available fields:** `id`, `label`, `html`, `latex`, `plainText`, `category`, `description`, `attribution`, `status`, `section`, `terms`, `derivation`, `computedValue`, `units`, `experimentalValue`, `sigmaDeviation`, `simulationFile`, `references`, `learningResources`, `relatedFormulas`, `inputParams`, `outputParams`

### `dark-energy-wa`

**Missing fields:** `validated`, `inputs`, `outputs`

**Present fields:** `id`, `label`, `plain_text/latex`, `category`, `derivation_chain/references`, `status`

**All available fields:** `id`, `label`, `html`, `latex`, `plainText`, `category`, `description`, `attribution`, `status`, `section`, `terms`, `computedValue`, `units`, `experimentalValue`, `experimentalError`, `sigmaDeviation`, `simulationFile`, `references`, `relatedFormulas`, `inputParams`, `outputParams`

### `effective-dimension`

**Missing fields:** `validated`, `inputs`, `outputs`

**Present fields:** `id`, `label`, `plain_text/latex`, `category`, `derivation_chain/references`, `status`

**All available fields:** `id`, `label`, `html`, `latex`, `plainText`, `category`, `description`, `attribution`, `status`, `section`, `terms`, `computedValue`, `units`, `simulationFile`, `references`, `relatedFormulas`

### `effective-euler`

**Missing fields:** `validated`, `inputs`, `outputs`

**Present fields:** `id`, `label`, `plain_text/latex`, `category`, `derivation_chain/references`, `status`

**All available fields:** `id`, `label`, `html`, `latex`, `plainText`, `category`, `description`, `attribution`, `status`, `section`, `terms`, `computedValue`, `units`, `simulationFile`, `references`, `relatedFormulas`, `inputParams`, `outputParams`

### `effective-torsion`

**Missing fields:** `validated`, `inputs`, `outputs`

**Present fields:** `id`, `label`, `plain_text/latex`, `category`, `derivation_chain/references`, `status`

**All available fields:** `id`, `label`, `html`, `latex`, `plainText`, `category`, `description`, `attribution`, `status`, `section`, `terms`, `computedValue`, `units`, `simulationFile`, `references`, `relatedFormulas`, `inputParams`

### `flux-quantization`

**Missing fields:** `validated`, `inputs`, `outputs`

**Present fields:** `id`, `label`, `plain_text/latex`, `category`, `derivation_chain/references`, `status`

**All available fields:** `id`, `label`, `html`, `latex`, `plainText`, `category`, `description`, `attribution`, `status`, `section`, `terms`, `computedValue`, `units`, `simulationFile`, `references`, `relatedFormulas`, `inputParams`, `outputParams`

### `generation-number`

**Missing fields:** `validated`, `inputs`, `outputs`

**Present fields:** `id`, `label`, `plain_text/latex`, `category`, `derivation_chain/references`, `status`

**All available fields:** `id`, `label`, `html`, `latex`, `plainText`, `category`, `description`, `attribution`, `status`, `section`, `terms`, `derivation`, `computedValue`, `units`, `experimentalValue`, `sigmaDeviation`, `simulationFile`, `references`, `learningResources`, `relatedFormulas`, `inputParams`, `outputParams`

### `gut-coupling`

**Missing fields:** `validated`, `inputs`, `outputs`

**Present fields:** `id`, `label`, `plain_text/latex`, `category`, `derivation_chain/references`, `status`

**All available fields:** `id`, `label`, `html`, `latex`, `plainText`, `category`, `description`, `attribution`, `status`, `section`, `terms`, `computedValue`, `simulationFile`, `references`, `relatedFormulas`

### `gut-scale`

**Missing fields:** `validated`, `inputs`, `outputs`

**Present fields:** `id`, `label`, `plain_text/latex`, `category`, `derivation_chain/references`, `status`

**All available fields:** `id`, `label`, `html`, `latex`, `plainText`, `category`, `description`, `attribution`, `status`, `section`, `terms`, `derivation`, `computedValue`, `units`, `simulationFile`, `references`, `learningResources`, `relatedFormulas`, `inputParams`, `outputParams`

### `kk-graviton-mass`

**Missing fields:** `validated`, `inputs`, `outputs`

**Present fields:** `id`, `label`, `plain_text/latex`, `category`, `derivation_chain/references`, `status`

**All available fields:** `id`, `label`, `html`, `latex`, `plainText`, `category`, `description`, `attribution`, `status`, `section`, `terms`, `derivation`, `computedValue`, `units`, `simulationFile`, `references`, `learningResources`, `relatedFormulas`

### `master-action-26d`

**Missing fields:** `validated`, `inputs`, `outputs`

**Present fields:** `id`, `label`, `plain_text/latex`, `category`, `derivation_chain/references`, `status`

**All available fields:** `id`, `label`, `html`, `latex`, `plainText`, `category`, `description`, `attribution`, `status`, `section`, `terms`, `derivation`, `units`, `simulationFile`, `references`, `learningResources`, `relatedFormulas`, `outputParams`

### `mirror-dm-ratio`

**Missing fields:** `validated`, `inputs`, `outputs`

**Present fields:** `id`, `label`, `plain_text/latex`, `category`, `derivation_chain/references`, `status`

**All available fields:** `id`, `label`, `html`, `latex`, `plainText`, `category`, `description`, `attribution`, `status`, `section`, `computedValue`, `experimentalValue`, `sigmaDeviation`, `simulationFile`, `references`, `relatedFormulas`, `outputParams`

### `neutrino-mass-21`

**Missing fields:** `validated`, `inputs`, `outputs`

**Present fields:** `id`, `label`, `plain_text/latex`, `category`, `derivation_chain/references`, `status`

**All available fields:** `id`, `label`, `html`, `latex`, `plainText`, `category`, `description`, `attribution`, `status`, `section`, `computedValue`, `units`, `experimentalValue`, `sigmaDeviation`, `simulationFile`, `references`, `relatedFormulas`, `inputParams`, `outputParams`

### `neutrino-mass-31`

**Missing fields:** `validated`, `inputs`, `outputs`

**Present fields:** `id`, `label`, `plain_text/latex`, `category`, `derivation_chain/references`, `status`

**All available fields:** `id`, `label`, `html`, `latex`, `plainText`, `category`, `description`, `attribution`, `status`, `section`, `computedValue`, `units`, `experimentalValue`, `sigmaDeviation`, `simulationFile`, `references`, `relatedFormulas`, `inputParams`, `outputParams`

### `pneuma-vev`

**Missing fields:** `validated`, `inputs`, `outputs`

**Present fields:** `id`, `label`, `plain_text/latex`, `category`, `derivation_chain/references`, `status`

**All available fields:** `id`, `label`, `html`, `latex`, `plainText`, `category`, `description`, `attribution`, `status`, `section`, `terms`, `computedValue`, `units`, `simulationFile`, `references`, `relatedFormulas`, `outputParams`

### `primordial-spinor-13d`

**Missing fields:** `validated`, `inputs`, `outputs`

**Present fields:** `id`, `label`, `plain_text/latex`, `category`, `derivation_chain/references`, `status`

**All available fields:** `id`, `label`, `html`, `latex`, `plainText`, `category`, `description`, `attribution`, `status`, `section`, `terms`, `computedValue`, `units`, `simulationFile`, `references`, `relatedFormulas`, `inputParams`

### `proton-lifetime`

**Missing fields:** `validated`, `inputs`, `outputs`

**Present fields:** `id`, `label`, `plain_text/latex`, `category`, `derivation_chain/references`, `status`

**All available fields:** `id`, `label`, `html`, `latex`, `plainText`, `category`, `description`, `attribution`, `status`, `section`, `terms`, `derivation`, `computedValue`, `units`, `simulationFile`, `references`, `learningResources`, `relatedFormulas`, `inputParams`, `outputParams`

### `reduction-cascade`

**Missing fields:** `validated`, `inputs`, `outputs`

**Present fields:** `id`, `label`, `plain_text/latex`, `category`, `derivation_chain/references`, `status`

**All available fields:** `id`, `label`, `html`, `latex`, `plainText`, `category`, `description`, `attribution`, `status`, `section`, `terms`, `units`, `simulationFile`, `references`, `relatedFormulas`, `inputParams`, `outputParams`

### `strong-coupling`

**Missing fields:** `validated`, `inputs`, `outputs`

**Present fields:** `id`, `label`, `plain_text/latex`, `category`, `derivation_chain/references`, `status`

**All available fields:** `id`, `label`, `html`, `latex`, `plainText`, `category`, `description`, `attribution`, `status`, `section`, `computedValue`, `experimentalValue`, `experimentalError`, `sigmaDeviation`, `simulationFile`, `references`, `relatedFormulas`

### `tcs-topology`

**Missing fields:** `validated`, `inputs`, `outputs`

**Present fields:** `id`, `label`, `plain_text/latex`, `category`, `derivation_chain/references`, `status`

**All available fields:** `id`, `label`, `html`, `latex`, `plainText`, `category`, `description`, `attribution`, `status`, `section`, `terms`, `simulationFile`, `references`, `relatedFormulas`, `outputParams`, `notes`

### `theta23-maximal`

**Missing fields:** `validated`, `inputs`, `outputs`

**Present fields:** `id`, `label`, `plain_text/latex`, `category`, `derivation_chain/references`, `status`

**All available fields:** `id`, `label`, `html`, `latex`, `plainText`, `category`, `description`, `attribution`, `status`, `section`, `terms`, `derivation`, `computedValue`, `units`, `experimentalValue`, `sigmaDeviation`, `simulationFile`, `references`, `learningResources`, `relatedFormulas`, `outputParams`

### `top-quark-mass`

**Missing fields:** `validated`, `inputs`, `outputs`

**Present fields:** `id`, `label`, `plain_text/latex`, `category`, `derivation_chain/references`, `status`

**All available fields:** `id`, `label`, `html`, `latex`, `plainText`, `category`, `description`, `attribution`, `status`, `section`, `computedValue`, `units`, `experimentalValue`, `experimentalError`, `sigmaDeviation`, `simulationFile`, `references`, `relatedFormulas`, `inputParams`

### `virasoro-anomaly`

**Missing fields:** `validated`, `inputs`, `outputs`

**Present fields:** `id`, `label`, `plain_text/latex`, `category`, `derivation_chain/references`, `status`

**All available fields:** `id`, `label`, `html`, `latex`, `plainText`, `category`, `description`, `attribution`, `status`, `section`, `terms`, `computedValue`, `units`, `simulationFile`, `references`, `learningResources`, `relatedFormulas`, `inputParams`

### `weak-mixing-angle`

**Missing fields:** `validated`, `inputs`, `outputs`

**Present fields:** `id`, `label`, `plain_text/latex`, `category`, `derivation_chain/references`, `status`

**All available fields:** `id`, `label`, `html`, `latex`, `plainText`, `category`, `description`, `attribution`, `status`, `section`, `computedValue`, `experimentalValue`, `experimentalError`, `sigmaDeviation`, `simulationFile`, `references`, `relatedFormulas`

## Recommendations

### Priority 1: Critical Missing Metadata

1. **Add `validated` field to all formulas** (62 formulas need this)
   - Boolean flag indicating if formula has been tested/verified
   - Default to `false` if untested, set to `true` after simulation validation
   - This is critical for tracking which formulas have been computationally verified

2. **Standardize field naming convention** (affects all formulas)
   - **Option A**: Rename existing fields to match expected names:
     - `plainText` → `plain_text`
     - `inputParams` → `inputs`
     - `outputParams` → `outputs`
   - **Option B**: Update checking code to recognize current field names
   - **Recommendation**: Keep current camelCase naming (consistent with JavaScript conventions)

3. **Complete input/output parameter coverage**
   - **30 formulas (48.4%) missing `inputParams`**: Add input parameter lists
   - **44 formulas (71.0%) missing `outputParams`**: Add output parameter lists
   - These enable automatic dependency tracking and workflow construction

### Priority 2: Provenance & Lifecycle Tracking

1. **Add `status` field** (31 formulas missing, 50%)
   - Suggested values: `active`, `deprecated`, `experimental`, `draft`
   - Helps track formula lifecycle and maturity
   - **Action**: Add status to all formulas, marking production-ready as `active`

2. **Add derivation/references** (27 formulas missing, 43.5%)
   - Either `derivation` field (step-by-step derivation text) **OR**
   - `references` array (citations/external sources)
   - **Note**: 35 formulas already have `references`, 13 have `derivation`
   - **Action**: Add one or both to remaining 27 formulas

3. **Add `units` field** (36 formulas missing, 58.1%)
   - Specify dimensional units for formula outputs
   - Critical for physical interpretations
   - Examples: `GeV`, `dimensionless`, `GeV^4`, `years`
   - **Note**: 26 formulas already have units

### Priority 3: Enhanced Metadata for Usability

1. **Add validation metadata** (where applicable)
   - `computedValue`: Theoretical prediction (34 formulas have this, 54.8%)
   - `experimentalValue`: Measured value (15 formulas have this, 24.2%)
   - `experimentalError`: Measurement uncertainty (7 formulas have this, 11.3%)
   - `sigmaDeviation`: Statistical significance of agreement (15 formulas have this)
   - **Action**: Add these to remaining formulas where experimental data exists

2. **Improve parameter documentation** (48.4% missing)
   - Ensure all 62 formulas have `inputParams` defined
   - Current coverage: 32/62 formulas (51.6%)
   - Missing from formulas like: `attractor-potential`, `bekenstein-hawking`, `ckm-elements`, etc.

3. **Complete output parameters** (71.0% missing)
   - Ensure all formulas specify what they calculate
   - Current coverage: 18/62 formulas (29.0%)
   - Particularly important for automated workflow generation

### Structural Observations

**Fields with excellent coverage (>80%):**
- `id`, `label`, `html`, `latex`, `plainText`, `category`, `description`, `attribution`, `section`, `relatedFormulas`: 100%
- `simulationFile`: 87.1% (54 formulas)
- `terms`: 82.3% (51 formulas)

**Fields needing expansion:**
- `testability`: Only 2 formulas (3.2%) have this field - consider adding to predictions
- `learningResources`: 23 formulas (37.1%) - could add more educational links
- `notes`: 17 formulas (27.4%) - useful for additional context

### Recommended Field Schema

Based on the analysis, here's the recommended complete schema:

**Required fields (all formulas should have):**
- `id`, `label`, `plainText`, `latex`, `html`
- `category`, `description`, `attribution`, `section`
- `validated` (boolean) ← **MISSING FROM ALL**
- `status` (string) ← **MISSING FROM 50%**
- `relatedFormulas` (array)
- `inputParams` (array) ← **MISSING FROM 48.4%**
- `outputParams` (array) ← **MISSING FROM 71.0%**

**Strongly recommended fields:**
- `simulationFile` (string) - if computable
- `references` (array) or `derivation` (string) - for provenance
- `units` (string) - for dimensional analysis
- `terms` (array) - key concepts/terminology

**Optional enhancement fields:**
- `computedValue`, `experimentalValue`, `experimentalError`, `sigmaDeviation` - for predictions
- `learningResources` (array) - educational materials
- `notes` (string) - additional context
- `testability` (object) - experimental verification proposals

### Action Items Summary

1. **Immediate**: Add `validated: false` to all 62 formulas (can batch update)
2. **High Priority**: Add `status: "active"` or appropriate status to 31 missing formulas
3. **High Priority**: Add `inputParams` to 30 formulas missing this field
4. **High Priority**: Add `outputParams` to 44 formulas missing this field
5. **Medium Priority**: Add `references` or `derivation` to 27 formulas lacking provenance
6. **Medium Priority**: Add `units` to 36 formulas missing dimensional information
7. **Nice to have**: Expand `testability` field to more prediction formulas
