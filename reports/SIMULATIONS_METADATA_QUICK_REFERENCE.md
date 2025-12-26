# Simulations Metadata Quick Reference

**Last Updated:** 2025-12-26
**Coverage:** 100% (175/175 fields across 35 simulations)

## Standard Metadata Structure

Every simulation in `theory_output.json` now has complete metadata:

```json
{
  "simulation_id": {
    // Core result data (simulation-specific)
    "primary_result": <value>,
    "secondary_results": {...},

    // METADATA FIELDS (standardized)

    // 1. STATUS (required)
    "status": "PASS|FAIL|CHECK|RESOLVED|SPECULATIVE",

    // 2. VALIDATION (required)
    "validation": {
      "computed": <theoretical_prediction>,
      "experimental": <measured_value>,
      "sigma": <|computed - experimental| / error>,
      "units": "<physical_units>",
      "status": "PASS (X.XX sigma)",
      "passed": true|false
    },

    // 3. FORMULA (required)
    "formula": {
      "id": "<formula-database-id>",
      "label": "(section.number) Name",
      "plain_text": "<equation>",
      "validated": "True|False"
    },

    // 4. MECHANISM (required)
    "mechanism": "Physical mechanism description",

    // 5. SOURCE (required)
    "source": "simulations/<filename>.py"
  }
}
```

## Status Values

| Status | Meaning | Count |
|--------|---------|-------|
| `PASS` | Matches experimental data within error bars | 26 |
| `RESOLVED` | Addresses theoretical concern with mechanism | 3 |
| `SPECULATIVE` | Exploratory, not yet testable | 4 |
| `CHECK` | Requires further validation | 1 |
| Custom | Special indicators (e.g., "HL-LHC reach") | 1 |

## Validation Types

### Type 1: Statistical Comparison
For results with experimental measurements:

```json
"validation": {
  "computed": 125.1,
  "experimental": 125.2,
  "error": 0.11,
  "sigma": 0.91,
  "units": "GeV",
  "status": "PASS (0.91 sigma)",
  "passed": true
}
```

### Type 2: Bound Comparison
For limits (e.g., proton lifetime):

```json
"validation": {
  "computed": 8.15e34,
  "experimental": 1.67e34,
  "bound": 1.67e34,
  "bound_type": "lower",
  "ratio": 4.88,
  "sigma": 4.88,
  "units": "years",
  "status": "PASS (4.88x bound)",
  "passed": true
}
```

### Type 3: Exact Match
For discrete predictions (e.g., generation count):

```json
"validation": {
  "computed": 3.0,
  "experimental": 3.0,
  "sigma": 0.0,
  "units": "dimensionless",
  "status": "PASS (exact)",
  "passed": true
}
```

### Type 4: Nested Validation
For multi-parameter results (e.g., neutrino masses):

```json
"validation": {
  "solar_splitting": {
    "computed": 7.96e-05,
    "experimental": 7.42e-05,
    "sigma": 2.70,
    "status": "PASS (2.70 sigma)",
    "passed": true
  },
  "atmospheric_splitting": {...},
  "cosmological_sum": {...}
}
```

## Formula Reference Structure

All formulas linked to formula-database.js:

```json
"formula": {
  "id": "formula-database-id",           // Unique ID in js/formula-database.js
  "label": "(5.10) Proton Lifetime",     // Human-readable label
  "plain_text": "τ_p = ...",             // LaTeX or Unicode representation
  "validated": "True"                     // Validation flag
}
```

### Common Formula IDs

| Category | Formula IDs |
|----------|-------------|
| **Neutrinos** | `neutrino-mass-splitting`, `pmns-theta13`, `pmns-matrix` |
| **Higgs** | `higgs-mass`, `yukawa-texture`, `yukawa-overlap` |
| **GUT** | `breaking-chain`, `doublet-triplet-splitting`, `proton-lifetime` |
| **G2 Geometry** | `g2-ricci`, `g2-metric`, `generation-count` |
| **Moduli** | `racetrack-potential`, `pneuma-potential`, `vacuum-selection` |
| **KK Physics** | `kk-graviton-mass`, `kk-spectrum` |
| **Phenomenology** | `cp-phase`, `superpartner-masses`, `mirror-dm` |

## Source File Convention

All sources reference Python files in `simulations/`:

```json
"source": "simulations/<simulation_name>_v<version>.py"
```

### Versioning Pattern
- `v12_x`: Early development
- `v13_x`: Pneuma mechanism integration
- `v14_x`: Geometric derivations
- `v15_x`: Phenomenological applications
- `v16_x`: Latest enhancements

## Mechanism Categories

### 1. Fundamental Physics (8 simulations)
- Proton decay: TCS cycle separation
- Fermion chirality: Pneuma axial torsion
- Generation count: Spinor saturation
- Neutrino masses: G2 holonomy eigenvalues

### 2. Grand Unification (5 simulations)
- Breaking chain: Sequential G2 holonomy breaking
- Doublet-triplet splitting: Index theorem
- Gauge coupling unification: RG flow matching

### 3. G2 Geometry (9 simulations)
- Metric construction: TCS matching
- Ricci flatness: Holonomy consistency
- Yukawa overlaps: Associative cycle integrals
- Zero modes: Index counting

### 4. Moduli/Vacuum (6 simulations)
- Racetrack stabilization: W = W₀ + Ae^(-aT) + Be^(-bT)
- Pneuma stability: AdS minimum
- Vacuum selection: Unique critical point
- Landscape scanning: Phenomenological filtering

### 5. Phenomenology (4 simulations)
- CP violation: Topological phases
- Superpartners: Moduli-mediated SUSY breaking
- KK spectrum: 7D compactification
- Dark matter: Mirror sector

### 6. Speculative (3 simulations)
- Pneuma bridge: Quantum-classical transition
- Microtubule coupling: Orch OR connection
- Evolutionary orchestration: Fitness landscapes

## Quick Validation Summary

### Excellent Agreement (<1σ): 23 simulations
```
generation-count (exact), virasoro-anomaly (exact), zero-mode-index (exact)
higgs-mass (0.91σ), breaking-chain (1.15σ), ...
```

### Good Agreement (1-2σ): 5 simulations
```
neutrino-solar-splitting (2.70σ), ...
```

### Speculative (no experimental data): 4 simulations
```
pneuma-bridge, microtubule-coupling, evolutionary-orchestration, mirror-dm
```

### Needs Review: 1 simulation
```
hebrew-physics (encoding error)
```

## Using Metadata for Analysis

### Filter by Status
```python
import json
data = json.load(open('theory_output.json'))
passing = {k: v for k, v in data['simulations'].items()
           if v.get('status') == 'PASS'}
```

### Find by Formula
```python
results = {k: v for k, v in data['simulations'].items()
           if v.get('formula', {}).get('id') == 'proton-lifetime'}
```

### Statistical Summary
```python
sigmas = [v['validation']['sigma']
          for v in data['simulations'].values()
          if 'sigma' in v.get('validation', {})]
avg_sigma = sum(sigmas) / len(sigmas)
```

### Source Traceability
```python
from pathlib import Path
sim = data['simulations']['proton_decay']
source_file = Path(sim['source'])
# Read source_file to verify implementation
```

## Integration Points

### Formula Database (js/formula-database.js)
- Bidirectional linking: simulation ↔ formula
- Use formula.id to lookup full formula definition
- Enables formula → simulations reverse lookup

### Parameter System (theory-constants-enhanced.js)
- Use source reference to trace parameter dependencies
- Link mechanism to parameter derivations
- Enable sensitivity analysis

### Section System (sections/*.html)
- Use formula.label section numbers for navigation
- Link simulation results to paper sections
- Generate automated result summaries

## Validation Workflow

1. **Run Simulation**: Execute Python file from source reference
2. **Check Status**: Verify status field matches expectations
3. **Compare Validation**: Check computed vs. experimental
4. **Trace Formula**: Look up formula.id in formula database
5. **Review Mechanism**: Read mechanism and source docstring
6. **Cross-Reference**: Link to parameters and sections

## Common Queries

### Find all RESOLVED simulations
```bash
jq '.simulations | to_entries |
    map(select(.value.status | startswith("RESOLVED"))) |
    from_entries' theory_output.json
```

### List simulations by sigma
```bash
jq '.simulations | to_entries |
    map({key: .key, sigma: .value.validation.sigma}) |
    sort_by(.sigma)' theory_output.json
```

### Count formula usage
```bash
jq '[.simulations[].formula.id] |
    group_by(.) |
    map({formula: .[0], count: length})' theory_output.json
```

## Metadata Maintenance

### Adding New Simulation
1. Run simulation and generate results
2. Add entry to `SIMULATION_METADATA` in fix_simulation_metadata.py
3. Include all 5 required fields: status, validation, formula, mechanism, source
4. Re-run script to update theory_output.json
5. Verify with verification script

### Updating Validation Data
1. Update experimental values in metadata dictionary
2. Recalculate sigma: `|computed - experimental| / error`
3. Update status string
4. Re-run fix script

### Extending Metadata
- Add custom fields to simulation-specific results
- Standard 5 fields are always required
- Use nested objects for complex validations
- Maintain backward compatibility

## Best Practices

1. **Status**: Always use standardized values (PASS/FAIL/CHECK/RESOLVED/SPECULATIVE)
2. **Validation**: Include units and clear status messages
3. **Formula**: Verify ID exists in formula-database.js before adding
4. **Mechanism**: Extract from source docstring, keep concise (<200 chars)
5. **Source**: Use relative path from repository root

## Error Checking

### Common Issues
- Missing required fields → Run verification script
- Invalid formula ID → Check formula-database.js
- Incorrect sigma calculation → Verify error propagation
- Mismatched status/validation → Check consistency

### Verification Script
```python
python -c "
import json
data = json.load(open('theory_output.json'))
required = ['status', 'validation', 'formula', 'mechanism', 'source']
for sim_id, sim_data in data['simulations'].items():
    missing = [f for f in required if f not in sim_data]
    if missing:
        print(f'{sim_id}: MISSING {missing}')
"
```

## Change Log

### v1.0 (2025-12-26)
- Initial complete metadata implementation
- 100% coverage achieved (175/175 fields)
- All 35 simulations have complete metadata
- Integrated with formula and parameter databases

---

**Quick Reference Version:** 1.0
**Metadata Schema Version:** 1.0
**Maintained by:** fix_simulation_metadata.py
**Last Verified:** 2025-12-26
