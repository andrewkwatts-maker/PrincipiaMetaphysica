# Cosmology Simulations v16.0

## Overview

This module contains version 16.0 implementations of cosmological simulations for the Principia Metaphysica framework. The simulations implement the `SimulationBase` interface and integrate with the `PMRegistry` system.

## Available Simulations

### MultiSectorV16 (`multi_sector_v16_0.py`)

**ID:** `multi_sector_v16_0`
**Version:** 16.0
**Domain:** cosmology
**Section:** 5.3

Multi-sector cosmological dynamics with geometric modulation width derived from G2 holonomy wavefunction overlaps or racetrack curvature.

#### Key Features

1. **Geometric Width Derivation**: Eliminates phenomenological tuning by deriving the modulation width from G2 geometry
2. **Dark Matter Prediction**: Computes Omega_DM/Omega_b ~ 5.4 from temperature asymmetry (no free parameters)
3. **Dark Energy EoS**: Derives effective equation of state w_eff ~ -0.853 from dimensional reduction
4. **Sector Blending**: Analyzes multi-sector structure from G2 compactification

#### Required Inputs

The simulation requires the following established parameters:

- `desi.w0` - Dark energy equation of state at z=0 (DESI DR2: -0.827 ± 0.063)
- `desi.wa` - Dark energy evolution parameter (DESI DR2: -0.75 ± 0.30)
- `desi.H0` - Hubble constant (Planck 2018: 67.4 ± 0.5 km/s/Mpc)
- `desi.Omega_m` - Matter density parameter (Planck 2018: 0.3111 ± 0.0056)
- `topology.chi_eff` - Effective Euler characteristic (default: 144)

#### Computed Outputs

The simulation computes the following parameters:

| Parameter | Description | Typical Value | Status |
|-----------|-------------|---------------|--------|
| `cosmology.w_eff` | Effective dark energy EoS | -0.853 | DERIVED |
| `cosmology.Omega_DM_over_b` | Dark matter to baryon ratio | 5.40 | PREDICTED |
| `cosmology.T_mirror_ratio` | Mirror sector temperature ratio | 0.57 | DERIVED |
| `cosmology.modulation_width` | Sector modulation width | 0.35 | GEOMETRIC |
| `cosmology.sm_weight` | Standard Model sector weight | 0.36 | DERIVED |
| `cosmology.mirror_weight` | Mirror sector weight | 0.14 | DERIVED |
| `cosmology.hierarchy_ratio` | Mass hierarchy ratio | 0.71 | DERIVED |

#### Formulas

The simulation provides the following formulas with complete derivation chains:

1. **dark-energy-eos** (5.14): Effective dark energy equation of state
   - w_eff = -(D_eff - 1)/(D_eff + 1) = -0.853
   - Agrees with DESI DR2 within 0.4σ

2. **moduli-potential** (5.15): Racetrack moduli potential
   - V(T) = V_0 [exp(-aT) - b*exp(-cT)]²
   - Determines geometric width from curvature

3. **sector-temperature-ratio** (5.16): Mirror sector temperature
   - T'/T = (g_*/g'_*)^(1/3) * (Gamma'/Gamma)^(1/2) = 0.57
   - From asymmetric reheating

4. **dark-matter-abundance** (5.17): Dark matter abundance
   - Omega_DM/Omega_b = (T/T')³ ≈ 5.4
   - Agrees with Planck 2018 (5.38 ± 0.15)

#### Section Content

The simulation generates complete section content for Section 5.3, including:

- 7 content blocks (paragraphs and formulas)
- 4 formula references
- 4 parameter references
- Complete LaTeX equations
- Physical interpretations

## Usage

### Basic Usage

```python
from simulations.v16.cosmology import MultiSectorV16
from simulations.base import PMRegistry
from simulations.base.established import EstablishedPhysics

# Create registry and load established parameters
registry = PMRegistry.get_instance()
EstablishedPhysics.load_into_registry(registry)

# Add topology parameter if needed
registry.set_param('topology.chi_eff', 144,
                  source='ESTABLISHED:G2_topology',
                  status='ESTABLISHED')

# Create and run simulation
sim = MultiSectorV16()
results = sim.execute(registry, verbose=True)

# Access results
w_eff = registry.get_param('cosmology.w_eff')
dm_ratio = registry.get_param('cosmology.Omega_DM_over_b')

print(f"Dark energy EoS: {w_eff}")
print(f"DM/baryon ratio: {dm_ratio}")
```

### Standalone Execution

```bash
cd h:\Github\PrincipiaMetaphysica
python simulations/v16/cosmology/multi_sector_v16_0.py
```

### Export for Integration

```python
from simulations.v16.cosmology.multi_sector_v16_0 import export_multi_sector_v16

results = export_multi_sector_v16()
print(results['outputs'])
```

## Physics Background

### Multi-Sector Structure

The G2 compactification naturally admits multiple sectors related by discrete symmetries. We consider a Z2 mirror sector that:

1. Has identical gauge groups to the Standard Model
2. Couples only gravitationally (no direct interactions)
3. Inherits different temperature from asymmetric reheating
4. Provides natural dark matter candidate

### Geometric Width Derivation

The modulation width between sectors is derived from G2 geometry via:

**Primary Method**: Wavefunction overlap
- Width = sqrt(Variance of |Psi|² distribution on G2)
- Uses same wavefunctions that determine Yukawa couplings
- Connects DM abundance to fermion mass hierarchy

**Secondary Method**: Racetrack curvature
- Width ~ 1/sqrt(V''(T_min))
- Modulus potential curvature sets quantum fluctuation scale
- Steeper potential = narrower width = more distinct sectors

### Dark Matter Abundance

The mirror sector inherits temperature T' < T from asymmetric reheating:

1. Decay rates: Gamma'/Gamma = (chi_eff/b3²)² from topology
2. Temperature ratio: T'/T = 0.57 (includes loop corrections)
3. Number density: n'/n = (T'/T)³ from entropy conservation
4. Abundance: Omega_DM/Omega_b = (T/T')³ = 5.4

**Key Result**: DM/baryon ratio is a PREDICTION, not a tuned parameter.

### Dark Energy from Dimensional Reduction

Effective dark energy equation of state emerges from dimensional reduction:

1. Shadow dimensions contribute: D_eff = 12 + alpha_shadow = 12.576
2. Map to dark energy: w = -(D_eff - 1)/(D_eff + 1)
3. Numerical value: w_eff = -0.853
4. Agreement: DESI DR2 measures w0 = -0.827 ± 0.063 (0.4σ)

## Validation

### Observational Agreement

| Prediction | Computed | Observed | Agreement |
|------------|----------|----------|-----------|
| w_eff | -0.853 | -0.827 ± 0.063 | 0.4σ |
| Omega_DM/Omega_b | 5.40 | 5.38 ± 0.15 | 0.1σ |

### Integration Tests

Run comprehensive tests:

```bash
cd h:\Github\PrincipiaMetaphysica
python -c "
from simulations.v16.cosmology import MultiSectorV16
from simulations.base import PMRegistry
from simulations.base.established import EstablishedPhysics

registry = PMRegistry.get_instance()
EstablishedPhysics.load_into_registry(registry)
registry.set_param('topology.chi_eff', 144, source='ESTABLISHED:G2_topology', status='ESTABLISHED')

sim = MultiSectorV16()
results = sim.execute(registry, verbose=True)

# Verify all outputs present
assert 'cosmology.w_eff' in results
assert 'cosmology.Omega_DM_over_b' in results
assert abs(results['cosmology.Omega_DM_over_b'] - 5.4) < 0.1

print('All tests passed!')
"
```

## References

### Mirror Dark Matter
- Berezhiani-Mohapatra (1995) arXiv:hep-ph/9505385
- Foot-Volkas (2004) arXiv:hep-ph/0407113
- Planck 2018: arXiv:1807.06209

### Dark Energy
- DESI DR2 (2024) arXiv:2510.12627
- Planck 2018: arXiv:1807.06209

### Moduli Stabilization
- Denef-Douglas (2004) arXiv:hep-th/0404116
- KKLT (2003) arXiv:hep-th/0301240

### G2 Geometry
- Acharya et al. (2007) arXiv:hep-th/0701034
- Randall-Sundrum (1999) arXiv:hep-ph/9905221

## File Structure

```
simulations/v16/cosmology/
├── __init__.py                  # Module initialization
├── multi_sector_v16_0.py        # Main simulation implementation
└── README.md                    # This file
```

## Version History

### v16.0 (2025-12-28)
- Initial implementation using SimulationBase infrastructure
- Geometric width derivation from G2 wavefunction overlaps
- Dark matter abundance as geometric prediction
- Dark energy EoS from dimensional reduction
- Complete formula derivation chains
- Full section content generation
- Integration with PMRegistry system

## Copyright

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.
