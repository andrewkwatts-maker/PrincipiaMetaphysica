# Bi-Directional Linking System

**Principia Metaphysica - Simulation-Theory Integration**

This document describes the bi-directional linking system that connects simulation files with formulas and parameters in `theory_output.json`.

## Overview

The bi-directional linking system provides:

1. **Simulation → Theory Links**: Each simulation file documents which formulas it implements and which parameters it reads/writes
2. **Theory → Simulation Links**: Each formula in `theory_output.json` includes a `simulationFile` field pointing to its implementation
3. **Validation**: Automated validation ensures all links are correct and up-to-date

## Simulation File Header Format

Each simulation file should include a bi-directional links header in its docstring:

```python
#!/usr/bin/env python3
"""
Simulation Description

# =============================================================================
# Bi-directional Links
# =============================================================================
# IMPLEMENTS: formula-id-1, formula-id-2
# READS:
#   - parameter/path/1: Description (value)
#   - parameter/path/2: Description (value)
# WRITES:
#   - output/path/1: Description
#   - output/path/2: Description
# VALIDATES:
#   - Validation criterion 1
#   - Validation criterion 2
# =============================================================================
"""
```

### Example

See `simulations/proton_decay_br_v12_8.py`:

```python
# =============================================================================
# Bi-directional Links
# =============================================================================
# IMPLEMENTS: proton-decay-branching-ratio
# READS:
#   - geometry/b3: Third Betti number (24 associative 3-cycles)
#   - geometry/shadow_spatial_dims: Shadow spacetime dimensions (12 spatial)
#   - topology/orientation_sum: Number of cycles oriented toward e+ channel (12)
# WRITES:
#   - simulations/proton_decay/br_e_pi0: Branching ratio p → e+ + pi0
#   - simulations/proton_decay/br_mu_pi0: Branching ratio p → mu+ + pi0
# VALIDATES:
#   - BR(e+pi0) = 0.25 (geometric prediction, testable by Hyper-K)
#   - Sum of branching ratios = 1.0
#   - Consistency with b3=24 cycle structure
# =============================================================================
```

## Theory Output Format

Each formula in `theory_output.json` includes a `simulationFile` field:

```json
{
  "formulas": {
    "formulas": {
      "proton-decay-branching-ratio": {
        "id": "proton-decay-branching-ratio",
        "label": "(5.11) Proton Decay Branching Ratio",
        "plainText": "BR(p → e⁺π⁰) = (N_orient/b₃)² = (12/24)² = 0.25",
        "simulationFile": "simulations/proton_decay_br_v12_8.py",
        "validated": false,
        "status": "PREDICTION"
      }
    }
  }
}
```

## Validation

### Running Validation

To validate all simulation links:

```bash
python simulations/validation/validate_simulation_links.py --verbose
```

This will:
- Scan all simulation files for bi-directional link headers
- Check that all formula IDs exist in `theory_output.json`
- Check that parameter paths follow standard conventions
- Generate a detailed report

### Expected Output

```
================================================================================
SIMULATION LINK VALIDATION REPORT
================================================================================

Scanned 5 simulation files with bi-directional links
Total formula implementations: 9
Total parameter reads: 24
Total parameter writes: 19

Known formula IDs in theory_output.json: 68

[PASS] No broken formula links found!
[PASS] No suspicious parameter paths found!

[SUCCESS] All validation checks passed!
```

## Adding New Simulations

When creating a new simulation file:

1. **Add the bi-directional links header** to your docstring
2. **Document IMPLEMENTS**: List formula IDs this simulation computes
3. **Document READS**: List all input parameters with descriptions
4. **Document WRITES**: List all output parameters
5. **Document VALIDATES**: List validation criteria

Example workflow:

```python
#!/usr/bin/env python3
"""
New Dark Energy Simulation

# =============================================================================
# Bi-directional Links
# =============================================================================
# IMPLEMENTS: dark-energy-equation-of-state
# READS:
#   - cosmology/H0: Hubble constant (67.4 km/s/Mpc)
#   - cosmology/Omega_m: Matter density (0.315)
# WRITES:
#   - simulations/dark_energy/w0: Equation of state today
#   - simulations/dark_energy/wa: EOS evolution parameter
# VALIDATES:
#   - w0 ≈ -0.83 ± 0.06 (DESI 2024 constraint)
#   - |wa| < 0.5 (quintessence bound)
# =============================================================================
"""

import numpy as np

def compute_equation_of_state():
    # Implementation here
    pass
```

## Updating theory_output.json

After adding new formulas to simulations, update `theory_output.json`:

```bash
python simulations/validation/add_simulation_links_to_theory.py
```

This will:
- Add `simulationFile` fields to existing formulas
- Create new formula entries for formulas implemented in simulations
- Update the formula count

## Key Simulation Files

Currently documented with bi-directional links:

1. **`proton_decay_br_v12_8.py`**
   - Implements: `proton-decay-branching-ratio`
   - Predicts BR(p → e⁺π⁰) = 0.25 from geometric cycle orientations

2. **`gauge_unification_precision_v12_4.py`**
   - Implements: `gut-unification`, `gut-coupling`
   - Derives M_GUT = 2.118×10¹⁶ GeV and α_GUT⁻¹ = 23.54

3. **`neutrino_mass_ordering.py`**
   - Implements: `neutrino-mass-ordering`, `neutrino-atiyah-singer-index`
   - Predicts normal hierarchy from Atiyah-Singer index

4. **`kk_graviton_mass_v12_fixed.py`**
   - Implements: `kk-graviton-mass`, `kk-graviton-tower`
   - Computes m_KK = 5.0 TeV from G₂ compactification

5. **`higgs_mass_v12_4_moduli_stabilization.py`**
   - Implements: `higgs-mass`, `higgs-quartic-coupling`
   - Derives m_h = 125.1 GeV from moduli stabilization

## Parameter Path Conventions

Use these standard prefixes for parameter paths:

- `config/`: Configuration constants
- `geometry/`: Geometric parameters (b2, b3, chi_eff, T_omega)
- `gauge/`: Gauge coupling parameters
- `fermion/`: Fermion masses and mixing
- `neutrino/`: Neutrino-specific parameters
- `higgs/`: Higgs sector parameters
- `yukawa/`: Yukawa coupling parameters
- `moduli/`: Moduli field values
- `energy_scales/`: Energy scales (M_GUT, M_Planck, etc.)
- `topology/`: Topological invariants
- `compactification/`: Compactification parameters
- `simulations/`: Simulation outputs

## Benefits

### For Development
- Easy to find which simulation implements a formula
- Clear documentation of parameter dependencies
- Automated validation catches broken links early

### For Users
- Navigate from theory to implementation and back
- Understand data flow between simulations
- Verify validation criteria

### For Maintenance
- Refactoring becomes safer (validator catches broken links)
- New contributors can understand the codebase structure
- Documentation stays synchronized with code

## Files

### Simulation Files (with links)
- `simulations/proton_decay_br_v12_8.py`
- `simulations/gauge_unification_precision_v12_4.py`
- `simulations/neutrino_mass_ordering.py`
- `simulations/kk_graviton_mass_v12_fixed.py`
- `simulations/higgs_mass_v12_4_moduli_stabilization.py`

### Validation Scripts
- `simulations/validation/validate_simulation_links.py` - Validates all links
- `simulations/validation/add_simulation_links_to_theory.py` - Updates theory_output.json

### Data Files
- `AutoGenerated/theory_output.json` - Theory data with `simulationFile` fields

## Future Enhancements

Potential improvements:

1. **Automatic Link Generation**: Parse simulation files to auto-generate theory entries
2. **Parameter Validation**: Verify parameter values match between simulations and theory
3. **Dependency Graph**: Visualize the full simulation → parameter → formula dependency graph
4. **Coverage Report**: Identify formulas without simulation implementations
5. **Link Testing**: Run simulations and verify outputs match theory_output.json

## Contact

For questions or issues with the bi-directional linking system:
- Check validation output for specific error messages
- Review this README for header format
- Examine existing simulation files for examples

---

**Last Updated**: 2025-12-27
**Version**: 1.0
**Status**: Active - 5 simulation files documented, 68 formulas linked
