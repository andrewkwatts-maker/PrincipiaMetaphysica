# Gauge Simulation v16.0

## Overview

This module implements gauge coupling unification for the Principia Metaphysica framework using the SimulationBase interface.

## Files

- `__init__.py` - Module initialization
- `gauge_unification_v16_0.py` - Main gauge unification simulation
- `README.md` - This file

## GaugeUnificationSimulation

Computes the GUT scale M_GUT and unified coupling alpha_GUT from 3-loop RG evolution of Standard Model gauge couplings.

### Metadata
- **ID**: `gauge_unification_v16_0`
- **Version**: `16.0`
- **Domain**: `gauge`
- **Section**: `3` (Gauge Coupling Unification and the GUT Scale)

### Required Inputs
1. `constants.M_PLANCK` - Planck mass for asymptotic safety
2. `pdg.alpha_s_MZ` - Strong coupling at M_Z
3. `pdg.sin2_theta_W` - Weak mixing angle at M_Z
4. `pdg.m_Z` - Z boson mass
5. `constants.alpha_em` - EM fine structure constant

### Output Parameters
1. `gauge.M_GUT` - Grand Unification scale (GeV)
2. `gauge.ALPHA_GUT` - Unified coupling (dimensionless)
3. `gauge.ALPHA_GUT_INV` - Inverse unified coupling (dimensionless)
4. `gauge.sin2_theta_W_gut` - Weak mixing angle at GUT scale

### Output Formulas
1. `gut-scale` - M_GUT determination from unification condition
2. `gauge-coupling-unification` - Numerical results for M_GUT and alpha_GUT
3. `gauge-rg-evolution` - 3-loop RG equations

## Physics Implementation

### Method
1. Start from SM gauge couplings at M_Z (PDG 2024)
2. Evolve using 3-loop RG equations with Pneuma contributions
3. Apply KK tower threshold corrections at M_* ~ 5 TeV (from CY4 with h^{1,1} = 24)
4. Apply asymptotic safety corrections (15% weight toward 1/alpha* ~ 24)
5. Find M_GUT where coupling spread is minimized

### Results
- **M_GUT** = (6.3 ± 0.3) × 10^15 GeV
- **1/alpha_GUT** = 42.7 ± 2.0
- **Precision**: ~4.7% (spread/mean)

### Key Features
- **3-loop RG running**: Standard Model beta functions plus Pneuma corrections
- **KK thresholds**: From Kaluza-Klein tower at compactification scale
- **Asymptotic safety**: UV fixed point from quantum gravity
- **G2 connection**: AS fixed point pulls toward 1/alpha* ~ 24 = b3

### Notes
The standard 3-loop running gives M_GUT ~ 6 × 10^15 GeV, which is lower than the geometric/torsion prediction M_GUT ~ 2 × 10^16 GeV. This suggests intermediate physics (e.g., Pati-Salam breaking at M_PS ~ 10^12 GeV) may modify the running. This is an active area of refinement in the PM framework.

## Usage Example

```python
from simulations.v16.gauge import GaugeUnificationSimulation
from simulations.base import PMRegistry
from simulations.base.established import EstablishedPhysics

# Create registry and load established physics
registry = PMRegistry()
EstablishedPhysics.load_into_registry(registry)

# Create and run simulation
sim = GaugeUnificationSimulation()
results = sim.execute(registry, verbose=True)

# Access results
M_GUT = registry.get_param("gauge.M_GUT")
alpha_GUT_inv = registry.get_param("gauge.ALPHA_GUT_INV")

print(f"M_GUT = {M_GUT:.4e} GeV")
print(f"1/alpha_GUT = {alpha_GUT_inv:.2f}")
```

## References

- Langacker (1981): "Grand Unified Theories and Proton Decay"
- Dienes et al. (1999): "Power-law running from KK states"
- Reuter (1998): "Nonperturbative Evolution in Quantum Gravity"
- v12_4 gauge_unification_precision.py: Previous implementation

## Copyright

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.
