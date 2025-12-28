# Fix Guide: multi_sector_sampling_v16_0.py

## Overview

This document provides specific code fixes for the two critical issues found in the validation.

---

## CRITICAL FIX #1: TopologicalParameters Import

**File:** `h:/Github/PrincipiaMetaphysica/simulations/core/cosmology/multi_sector_sampling_v16_0.py`

**Lines:** 52-57

### Current Code (INCORRECT)

```python
try:
    from config import TopologicalParameters
    H11 = getattr(TopologicalParameters, 'H11', 4)
except ImportError:
    H11 = 4
```

### Problem

The class `TopologicalParameters` does NOT exist in `config.py`. The actual classes available are:
- `FundamentalConstants.HODGE_H11 = 4`
- `TCSTopologyParameters.HODGE_H11 = 4`

### Solution A: Use FundamentalConstants (Recommended)

```python
try:
    from config import FundamentalConstants
    H11 = FundamentalConstants.HODGE_H11
except ImportError:
    H11 = 4
```

**Rationale:** FundamentalConstants is the primary topology class used throughout the framework.

### Solution B: Use TCSTopologyParameters

```python
try:
    from config import TCSTopologyParameters
    H11 = TCSTopologyParameters.HODGE_H11
except ImportError:
    H11 = 4
```

**Rationale:** More specific to TCS G₂ topology, clearly indicates the G₂ manifold source.

### Verification

After applying the fix, verify the import works:

```bash
cd h:/Github/PrincipiaMetaphysica
python3 -c "from config import FundamentalConstants; print('H11 =', FundamentalConstants.HODGE_H11)"
# Output: H11 = 4
```

Or with Solution B:

```bash
python3 -c "from config import TCSTopologyParameters; print('H11 =', TCSTopologyParameters.HODGE_H11)"
# Output: H11 = 4
```

---

## CRITICAL FIX #2: theory_output.json Export

**File:** `h:/Github/PrincipiaMetaphysica/simulations/core/cosmology/multi_sector_sampling_v16_0.py`

**Lines:** 261-286 (in `__main__` block)

### Current Code (INCOMPLETE)

```python
if __name__ == "__main__":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

    print("\n" + "=" * 70)
    print(" Running Multi-Sector Sampling v16.0 (Geometric Width)")
    print("=" * 70)

    # Run v16.0 with geometric width derivation
    sampler = MultiSectorSamplingV16(use_geometric_width=True)
    results = sampler.run_full_analysis()

    # Also show what the legacy v15.2 would give for comparison
    print("\n" + "=" * 70)
    print(" COMPARISON: v15.2 (calibrated) vs v16.0 (geometric)")
    print("=" * 70)
    sampler_legacy = MultiSectorSamplingV16(use_geometric_width=False)
    results_legacy = sampler_legacy.run_full_analysis(verbose=False)

    print(f"  v15.2 width (calibrated): 0.35")
    print(f"  v16.0 width (geometric):  {results['width_derivation']['value']:.4f}")
    print(f"  v15.2 DM ratio: {results_legacy['dark_matter']['mirror_dm_fraction']:.2f}")
    print(f"  v16.0 DM ratio: {results['dark_matter']['mirror_dm_fraction']:.2f}")
    print(f"  Observed DM ratio: 5.4")
    print("=" * 70)
```

### Problem

- The `export_multi_sector_v16()` function is defined but **never called**
- Results are printed to console but **never persisted** to JSON
- No integration with `theory_output.json`

### Solution: Add JSON Export

Replace the `__main__` block with this enhanced version:

```python
if __name__ == "__main__":
    import io
    import json
    from pathlib import Path

    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

    print("\n" + "=" * 70)
    print(" Running Multi-Sector Sampling v16.0 (Geometric Width)")
    print("=" * 70)

    # Run v16.0 with geometric width derivation
    sampler = MultiSectorSamplingV16(use_geometric_width=True)
    results = sampler.run_full_analysis()

    # Also show what the legacy v15.2 would give for comparison
    print("\n" + "=" * 70)
    print(" COMPARISON: v15.2 (calibrated) vs v16.0 (geometric)")
    print("=" * 70)
    sampler_legacy = MultiSectorSamplingV16(use_geometric_width=False)
    results_legacy = sampler_legacy.run_full_analysis(verbose=False)

    print(f"  v15.2 width (calibrated): 0.35")
    print(f"  v16.0 width (geometric):  {results['width_derivation']['value']:.4f}")
    print(f"  v15.2 DM ratio: {results_legacy['dark_matter']['mirror_dm_fraction']:.2f}")
    print(f"  v16.0 DM ratio: {results['dark_matter']['mirror_dm_fraction']:.2f}")
    print(f"  Observed DM ratio: 5.4")
    print("=" * 70)

    # NEW: Export results to theory_output.json
    print("\n" + "=" * 70)
    print(" EXPORTING RESULTS TO theory_output.json")
    print("=" * 70)

    export_dict = export_multi_sector_v16()

    # Get path to theory_output.json in parent directory
    current_dir = Path(__file__).parent.parent.parent
    output_file = current_dir / 'theory_output.json'

    try:
        # Load existing theory_output.json if it exists
        if output_file.exists():
            with open(output_file, 'r') as f:
                theory_data = json.load(f)
        else:
            theory_data = {}

        # Add/update multi_sector_v16 section
        theory_data['multi_sector_v16_0'] = export_dict

        # Write updated data back
        with open(output_file, 'w') as f:
            json.dump(theory_data, f, indent=2)

        print(f"✓ Results exported to: {output_file}")
        print(f"  Timestamp: {export_dict['VERSION']}")
        print(f"  DM Ratio: {export_dict['MIRROR_DM_FRACTION']:.2f} (observed: 5.4)")
        print(f"  Valid: {export_dict['OVERALL_VALID']}")

    except Exception as e:
        print(f"✗ Error writing to theory_output.json: {e}")
        print(f"  Falling back to stdout output only")

    print("=" * 70)
```

### Key Changes

1. **Import json and Path modules** at the top of the `__main__` block
2. **Call export_multi_sector_v16()** to get the export dictionary
3. **Locate theory_output.json** in the parent directory
4. **Load existing data** if file exists, or create new dict
5. **Add multi_sector_v16_0 section** to the data
6. **Write back to JSON** with proper formatting
7. **Handle errors gracefully** with try/except
8. **Print status messages** for debugging

### Testing the Fix

After applying the fix, run the simulation:

```bash
cd h:/Github/PrincipiaMetaphysica
python3 simulations/core/cosmology/multi_sector_sampling_v16_0.py
```

Expected output:
```
...
======================================================================
 EXPORTING RESULTS TO theory_output.json
======================================================================
✓ Results exported to: h:/Github/PrincipiaMetaphysica/theory_output.json
  Timestamp: v16.0
  DM Ratio: 5.35 (observed: 5.4)
  Valid: True
======================================================================
```

### Verification

Check that theory_output.json was updated:

```bash
python3 -c "import json; data = json.load(open('theory_output.json')); print('multi_sector_v16_0' in data)"
# Output: True

python3 -c "import json; data = json.load(open('theory_output.json')); print(data['multi_sector_v16_0']['VERSION'])"
# Output: v16.0
```

---

## MINOR FIX #1: Document export_multi_sector_v16()

**File:** `h:/Github/PrincipiaMetaphysica/simulations/core/cosmology/multi_sector_sampling_v16_0.py`

**Lines:** 239-258

### Current Code (MINIMAL DOCUMENTATION)

```python
def export_multi_sector_v16() -> Dict:
    """Export v16.0 results for integration."""
    sampler = MultiSectorSamplingV16()
    results = sampler.run_full_analysis(verbose=False)

    return {
        'N_SECTORS': results['input_parameters']['n_sectors'],
        'SAMPLING_POSITION': results['input_parameters']['sampling_position'],
        'MODULATION_WIDTH': results['width_derivation']['value'],
        'WIDTH_SOURCE': results['width_derivation']['source'],
        'IS_GEOMETRIC': results['width_derivation']['is_geometric'],
        'SM_WEIGHT': results['sector_structure']['sm_weight'],
        'MIRROR_WEIGHT': results['sector_structure']['mirror_weight'],
        'HIERARCHY_RATIO': results['blended_observables']['hierarchy_ratio'],
        'GRAVITY_DILUTION': results['blended_observables']['gravity_dilution'],
        'MIRROR_DM_FRACTION': results['dark_matter']['mirror_dm_fraction'],
        'DM_DEVIATION_PCT': results['dm_validation']['deviation_pct'],
        'OVERALL_VALID': results['overall_valid'],
        'VERSION': 'v16.0'
    }
```

### Enhanced Documentation

```python
def export_multi_sector_v16() -> Dict:
    """
    Export v16.0 multi-sector sampling results for theory_output.json.

    Runs a complete v16.0 simulation with geometric width derivation and
    extracts the 13 key parameters for storage in the central results file.

    Calls run_full_analysis(verbose=False) internally to avoid stdout output.

    Returns:
        Dict with the following keys:
        - N_SECTORS (int): Number of sectors from G₂ topology (default 4)
        - SAMPLING_POSITION (float): Position in moduli space [0-1], typically 0.5
        - MODULATION_WIDTH (float): Gaussian width for sector sampling
          Units: Dimensionless, typical range [0.2, 0.5]
        - WIDTH_SOURCE (str): Method used to derive width
          Values: 'G2_wavefunction_overlap', 'racetrack_curvature', 'calibrated_fallback'
        - IS_GEOMETRIC (bool): True if width was geometrically derived from G2,
          False if using calibrated fallback value
        - SM_WEIGHT (float): Weight of Standard Model sector in blended physics [0-1]
        - MIRROR_WEIGHT (float): Weight of mirror/shadow sector [0-1]
        - HIERARCHY_RATIO (float): Effective hierarchy from sector blending
          Dimensionless, typical value ~10^15
        - GRAVITY_DILUTION (float): Dilution factor for gravitational strength
          Dimensionless, typical value ~10^-32
        - MIRROR_DM_FRACTION (float): Predicted Omega_DM / Omega_b ratio
          Dimensionless, observed value ~5.4 from Planck 2018
        - DM_DEVIATION_PCT (float): Percentage deviation from Planck observed value
          Range: typically 0-50% for valid models
        - OVERALL_VALID (bool): True if hierarchy maintained AND DM ratio within 3-8
        - VERSION (str): Version identifier 'v16.0'

    Integration:
        Designed to be called from __main__ and results stored in theory_output.json:

        if __name__ == "__main__":
            export_dict = export_multi_sector_v16()
            with open('theory_output.json', 'r+') as f:
                data = json.load(f)
                data['multi_sector_v16_0'] = export_dict
                f.seek(0)
                json.dump(data, f, indent=2)

    References:
        - Multi-sector sampling: Randall-Sundrum (1999) arXiv:hep-ph/9905221
        - Mirror dark matter: Foot (2004) arXiv:hep-ph/0402267
        - G2 geometry: Acharya et al. (2007) arXiv:hep-th/0701034
    """
    sampler = MultiSectorSamplingV16()
    results = sampler.run_full_analysis(verbose=False)

    return {
        'N_SECTORS': results['input_parameters']['n_sectors'],
        'SAMPLING_POSITION': results['input_parameters']['sampling_position'],
        'MODULATION_WIDTH': results['width_derivation']['value'],
        'WIDTH_SOURCE': results['width_derivation']['source'],
        'IS_GEOMETRIC': results['width_derivation']['is_geometric'],
        'SM_WEIGHT': results['sector_structure']['sm_weight'],
        'MIRROR_WEIGHT': results['sector_structure']['mirror_weight'],
        'HIERARCHY_RATIO': results['blended_observables']['hierarchy_ratio'],
        'GRAVITY_DILUTION': results['blended_observables']['gravity_dilution'],
        'MIRROR_DM_FRACTION': results['dark_matter']['mirror_dm_fraction'],
        'DM_DEVIATION_PCT': results['dm_validation']['deviation_pct'],
        'OVERALL_VALID': results['overall_valid'],
        'VERSION': 'v16.0'
    }
```

---

## Implementation Order

### For Maximum Impact:

1. **Fix #1: Config Import** (5 minutes)
   - Quick fix, prevents potential future issues
   - Clarifies intent to maintainers
   - No functional impact (fallback works)

2. **Fix #2: JSON Export** (15 minutes)
   - Critical for framework integration
   - Required for results to be accessible to other simulations
   - Completes the intended architecture

3. **Fix #1: Documentation** (10 minutes)
   - Improves maintainability
   - Helps future developers understand the export format
   - Optional but recommended

### Total Time: 30 minutes

---

## Verification Checklist

After applying all fixes:

- [ ] Import runs without errors: `python3 -c "from simulations.core.cosmology.multi_sector_sampling_v16_0 import MultiSectorSamplingV16"`
- [ ] Simulation runs: `python3 simulations/core/cosmology/multi_sector_sampling_v16_0.py`
- [ ] JSON file is created/updated: `ls -la theory_output.json`
- [ ] JSON is valid: `python3 -c "import json; json.load(open('theory_output.json'))"`
- [ ] v16.0 section exists: `python3 -c "import json; data = json.load(open('theory_output.json')); print('multi_sector_v16_0' in data)"`
- [ ] All required keys present:
  ```python
  import json
  data = json.load(open('theory_output.json'))
  required_keys = [
      'N_SECTORS', 'SAMPLING_POSITION', 'MODULATION_WIDTH', 'WIDTH_SOURCE',
      'IS_GEOMETRIC', 'SM_WEIGHT', 'MIRROR_WEIGHT', 'HIERARCHY_RATIO',
      'GRAVITY_DILUTION', 'MIRROR_DM_FRACTION', 'DM_DEVIATION_PCT',
      'OVERALL_VALID', 'VERSION'
  ]
  export = data['multi_sector_v16_0']
  missing = [k for k in required_keys if k not in export]
  assert not missing, f"Missing keys: {missing}"
  print("✓ All keys present")
  ```

---

## Rollback Plan

If something goes wrong:

1. **Before applying fixes**, commit your current state:
   ```bash
   git add -A
   git commit -m "Pre-fix backup: multi_sector_sampling_v16_0.py"
   ```

2. **If the fix doesn't work**, revert:
   ```bash
   git checkout HEAD~ -- simulations/core/cosmology/multi_sector_sampling_v16_0.py
   ```

3. **Check what went wrong**, and re-apply with corrections

---

## Questions?

Refer to the main validation report:
`h:/Github/PrincipiaMetaphysica/VALIDATION_REPORT_MULTI_SECTOR_SAMPLING_V16.md`

For specific sections:
- Import validation: Section 1
- Dependency chain: Section 3
- Output structure: Section 5
- JSON integration: Section 6
