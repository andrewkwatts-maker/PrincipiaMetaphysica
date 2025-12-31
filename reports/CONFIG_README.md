# Configuration Management - Single Source of Truth

## Overview

The Principia Metaphysica project now uses a **centralized configuration system** in `config.py` as the single source of truth for all theoretical parameters, phenomenological values, and computational settings.

## Architecture

### config.py Structure

All configuration values are organized into **6 main classes**:

```
config.py
├── FundamentalConstants      # Theory-derived constants
├── PhenomenologyParameters    # Experimentally fitted values
├── MultiTimeParameters        # Two-time physics parameters
├── ModuliParameters           # KKLT stabilization values
├── LandscapeParameters        # Multiverse/landscape values
└── ComputationalSettings      # Numerical simulation settings
```

### Design Principles

1. **Single Source of Truth**: All magic numbers live in config.py
2. **Separation of Concerns**: Constants grouped by physical/computational category
3. **Traceability**: Every value documented with physical meaning
4. **Type Safety**: Classes provide structure and auto-completion
5. **Backward Compatibility**: `get_config_dict()` for legacy code

## Usage

### Basic Import

```python
from config import (
    FundamentalConstants as FC,
    PhenomenologyParameters as PP,
    MultiTimeParameters as MTP,
    ModuliParameters as MP,
    LandscapeParameters as LP,
    ComputationalSettings as CS,
    RealWorldData as RWD
)
```

### Accessing Values

```python
# Fundamental constants
D_bulk = FC.D_BULK                    # 26
D_internal = FC.D_INTERNAL            # 13
generations = FC.fermion_generations() # 3

# Phenomenology
M_Pl = PP.M_PLANCK                    # 1.2195e19 GeV
w_0 = PP.w0_value()                   # -0.9583 (v16.2 thawing)

# Multi-time physics
g = MTP.G_COUPLING                    # 0.1
eta = MTP.eta_linear()                # 0.1 (= g/E_F)

# Moduli stabilization
a = MP.a_swampland()                  # 1.414214 (= sqrt(26/13))
Delta = MP.condensate_gap()           # 0.909091 TeV

# Landscape
S_landscape = LP.landscape_entropy()  # 1151.29

# Computational
N_qutip = CS.N_QUTIP_HILBERT         # 4
time_array = CS.time_array()         # [0, 0.1, ..., 10]
```

### Legacy Compatibility

For older code expecting a dictionary:

```python
from config import get_config_dict

CONFIG = get_config_dict()
D_bulk = CONFIG['D_bulk']      # 26
M_Pl = CONFIG['M_Pl']          # 1.2195e19
```

## Configuration Classes

### 1. FundamentalConstants

**Theory-derived values that should NOT change unless the theory changes.**

| Constant | Value | Meaning |
|----------|-------|---------|
| `D_BULK` | 26 | Bosonic string critical dimension |
| `D_INTERNAL` | 13 | Compactified dimensions (26D → 13D) |
| `D_OBSERVED` | 4 | Observable 4D spacetime |
| `N_BRANES` | 4 | Number of D-branes in hierarchy |
| `SPATIAL_DIMS` | 3 | Spatial dimensions per brane |
| `TIME_DIMS` | 1 | Shared time dimension |
| `HODGE_H11` | 4 | h^{1,1} Hodge number (CY4) |
| `HODGE_H21` | 0 | h^{2,1} Hodge number |
| `HODGE_H31` | 72 | h^{3,1} Hodge number (doubled) |
| `FLUX_REDUCTION` | 2 | Z₂ orbifold flux reduction |
| `GAUGING_DOFS` | 12 | Sp(2,R) gauge degrees of freedom |
| `MIRRORING_FACTOR` | 2 | Z₂ mirror symmetry |
| `SM_BOSONS` | 12 | Standard Model gauge bosons (8+3+1) |

**Derived Methods:**
- `euler_characteristic()` → -300 (raw χ from Hodge numbers)
- `euler_characteristic_effective()` → 144 (after flux constraints)
- `fermion_generations()` → 3 (= floor(144/48))
- `pneuma_dimension_full()` → 8192 (= 2^13)
- `pneuma_dimension_reduced()` → 64 (after gauging)

### 2. PhenomenologyParameters

**Experimentally measured or fitted values (update as new data arrives).**

| Parameter | Value | Source |
|-----------|-------|--------|
| `M_PLANCK` | 1.2195×10¹⁹ GeV | PDG 2024 |
| `M_STAR` | 1×10¹⁹ GeV | 13D fundamental scale |
| `TAU_PROTON` | 3.5×10³⁴ years | SO(10) GUT central value |
| `W0_NUMERATOR` | -23 | Dark energy w(z=0) numerator |
| `W0_DENOMINATOR` | 24 | w₀ = -23/24 from thawing (b₃) |
| `WA_EVOLUTION` | -0.204 | Dark energy evolution (-1/√24) |
| `OMEGA_LAMBDA` | 0.6889 | Dark energy density (Planck) |
| `H0` | 67.4 km/s/Mpc | Hubble constant |

**Derived Methods:**
- `w0_value()` → -0.9583 (= -23/24 from b₃ = 24)

### 3. MultiTimeParameters

**Parameters specific to two-time (t, t_ortho) structure.**

| Parameter | Value | Meaning |
|-----------|-------|---------|
| `G_COUPLING` | 0.1 | Multi-time coupling g |
| `E_FERMI` | 1.0 TeV | Fermi energy (condensate scale) |
| `XI_QUADRATIC` | 1×10¹⁰ | Quadratic GW coefficient ξ |
| `DELTA_T_ORTHO` | 1×10⁻¹⁸ s | Orthogonal time delay |
| `R_ORTHO` | 1.0 | Orthogonal compactification radius |
| `K_LISA_DEFAULT` | 1×10⁻¹⁰ Hz | LISA frequency (conservative) |
| `ALPHA_TTH` | 1.0 | Thermal time hypothesis normalization |
| `THETA_MIRROR_DEFAULT` | 0.0 rad | Mirror mixing angle |

**Derived Methods:**
- `eta_linear()` → 0.1 (= g/E_F)
- `beta_mixing(theta)` → cos(θ)

### 4. ModuliParameters

**Values controlling moduli stabilization: V(φ) = |F|² e^(-aφ) + κ e^(-b/φ) + μ cos(φ/R)**

| Parameter | Value | Term |
|-----------|-------|------|
| `F_TERM_NORMALIZED` | 1.0 | SUSY F-term coefficient |
| `KAPPA_UPLIFT` | 1.0 | Non-perturbative uplift |
| `S_INSTANTON_NORM` | 1.0 | Normalized instanton exponent (simplified) |
| `MU_PERIODIC` | 0.5 | Axionic modulation amplitude |
| `LAMBDA_COUPLING` | 0.5 TeV⁻² | Pneuma quartic coupling λ |
| `V_VEV` | 2.0 TeV | VEV scale (condensate) |
| `T_ORTHO_NORMALIZED` | 1.0 | Orthogonal time parameter |

**Derived Methods:**
- `a_swampland()` → 1.414214 (= √(26/13))
- `condensate_gap()` → 0.909091 TeV (= λv/(1 + g·t/E_F))

**Constraint:** `a > SWAMPLAND_BOUND = √(2/3) ≈ 0.816` ✓ SATISFIED

### 5. LandscapeParameters

**Multiverse and string landscape phenomenology.**

| Parameter | Value | Meaning |
|-----------|-------|---------|
| `N_VAC_EXPONENT` | 500 | N_vac ~ 10^500 |
| `SIGMA_TENSION` | 1.0 | Domain wall tension |
| `DELTA_V_MULTIVERSE` | 1×10¹⁰ | Vacuum energy difference |
| `BUBBLE_RADIUS_MPC` | 100 Mpc | Bubble collision radius |
| `CMB_TEMPERATURE_UK` | 100 μK | CMB cold spot amplitude |

**Derived Methods:**
- `vacuum_count()` → 10^500
- `landscape_entropy()` → 1151.29 (= 500×ln(10))
- `euclidean_action()` → S_E (CDL instanton)
- `tunneling_rate()` → Γ = exp(-S_E)

### 6. ComputationalSettings

**Numerical simulation parameters.**

| Setting | Value | Purpose |
|---------|-------|---------|
| `N_QUTIP_HILBERT` | 4 | QuTiP Hilbert space (toy) |
| `N_QUTIP_PRODUCTION` | 10 | Production simulations |
| `TIME_START` | 0 | Evolution start time |
| `TIME_END` | 10 | Evolution end time |
| `TIME_STEPS` | 100 | Number of time steps |
| `TOLERANCE_UNITARITY` | 1×10⁻¹⁰ | Unitary evolution check |
| `A_LIMIT_EXPONENT` | 10 | a → exp(10) for late-time limit |
| `SYMPY_PRECISION_DIGITS` | 10 | Symbolic precision |

**Derived Methods:**
- `time_array()` → np.linspace(0, 10, 100)

## Validation

The configuration system includes built-in validation:

```bash
python config.py
```

**Output:**
```
FUNDAMENTAL CONSTANTS:
  D_bulk = 26
  D_internal = 13
  Euler characteristic = -300
  Generations = 3
  Pneuma (full) = 8192
  Pneuma (reduced) = 64

DERIVED PARAMETERS:
  w_0 = 0.846154
  eta = g/E_F = 0.100
  a_swampland = 1.414214
  Delta (gap) = 0.909091 TeV
  S_landscape = 1151.29

VALIDATION:
  swampland: PASS [1.414, 0.816]
  generations: PASS [3]
  dimensions: PASS [13]

Overall: ALL CHECKS PASSED
```

## Real-World Data

The `RealWorldData` class contains experimental values for validation:

```python
from config import RealWorldData as RWD

# Each entry is a tuple: (value, error, source_link)
planck_mass = RWD.PLANCK_MASS
# → (1.2205e19, 0.0003e19, 'https://pdg.lbl.gov/...')

w0_measured = RWD.W0_DARK_ENERGY
# → (-0.827, 0.063, 'https://arxiv.org/abs/2404.03002')
```

## Migration Guide

### Before (Hard-Coded)

```python
M_Pl = 1e19  # Where did this come from?
w_0 = -0.846  # Why this value?
xi = 1e10  # Magic number alert!
```

### After (Centralized)

```python
from config import PhenomenologyParameters as PP
from config import MultiTimeParameters as MTP

M_Pl = PP.M_PLANCK  # PDG 2024 value with documentation
w_0 = PP.w0_value()  # Derived from -23/24 (thawing quintessence)
xi = MTP.XI_QUADRATIC  # 1-loop estimate, clearly documented
```

## Benefits

1. **No More Magic Numbers**: Every value has a home and documentation
2. **Easy Parameter Tuning**: Change CONFIG once, updates everywhere
3. **Version Control**: Track parameter evolution over time
4. **Collaboration**: Clear definitions prevent confusion
5. **Testing**: Centralized validation catches inconsistencies
6. **Extensibility**: Easy to add new parameter categories

## Files Using Config

- **SimulateTheory.py**: Main parameter generation script
- **config.py**: Single source of truth (this file)
- **Future scripts**: Import from config.py instead of hard-coding

## Best Practices

1. **Never hard-code values** in calculation scripts
2. **Always import from config.py**
3. **Document** any new parameters you add
4. **Update** RealWorldData when new experimental results arrive
5. **Run validation** after modifying config.py
6. **Use class methods** for derived quantities

## Examples

### Example 1: Adding a New Parameter

```python
# In config.py
class MultiTimeParameters:
    # ... existing parameters ...

    DELTA_T_PLANCK = 5.391e-44  # Planck time [seconds]

    @staticmethod
    def time_scale_ratio():
        """Ratio of orthogonal time to Planck time"""
        return MultiTimeParameters.DELTA_T_ORTHO / MultiTimeParameters.DELTA_T_PLANCK
```

### Example 2: Using Derived Values

```python
from config import ModuliParameters as MP, MultiTimeParameters as MTP

# Calculate GW dispersion with centralized values
def gw_dispersion(k):
    eta = MTP.eta_linear()
    xi = MTP.XI_QUADRATIC
    Delta_t = MTP.DELTA_T_ORTHO
    M_Pl = PP.M_PLANCK

    term1 = eta * k * Delta_t
    term2 = xi**2 * (k / M_Pl)**2

    return term1 + term2
```

### Example 3: Parameter Exploration

```python
# Create a modified configuration for sensitivity analysis
import config

# Save original
original_g = config.MultiTimeParameters.G_COUPLING

# Test different values
for g_test in [0.05, 0.1, 0.15, 0.2]:
    config.MultiTimeParameters.G_COUPLING = g_test

    eta_new = config.MultiTimeParameters.eta_linear()
    Delta_new = config.ModuliParameters.condensate_gap()

    print(f"g={g_test}: η={eta_new:.3f}, Δ={Delta_new:.3f} TeV")

# Restore original
config.MultiTimeParameters.G_COUPLING = original_g
```

## Summary

The centralized `config.py` system ensures:

✅ **Single source of truth** for all parameters
✅ **No magic numbers** scattered across codebase
✅ **Clear documentation** of every value's origin
✅ **Easy tuning** via one configuration file
✅ **Built-in validation** catches errors early
✅ **Real-world comparison** with experimental data

**Result:** Cleaner code, fewer bugs, easier collaboration, better science.
