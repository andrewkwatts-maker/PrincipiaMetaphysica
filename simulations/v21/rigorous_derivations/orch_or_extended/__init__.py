"""
Principia Metaphysica v18 - Orch-OR Extended Derivations
=========================================================

This submodule contains rigorous derivations for the Penrose-Hameroff
Orch-OR (Orchestrated Objective Reduction) quantum consciousness hypothesis.

MODULES:
--------
1. gravitational_self_energy_v18:
   - GravitationalSelfEnergySimulation - Main simulation wrapper (v18 schema)
   - DiosiPenroseCalculator - Full Diosi-Penrose integral calculation
   - PenroseCollapseCalculator - tau = hbar/E_G collapse time
   - TubulinParameters - Biophysical parameter container
   - ParameterSensitivityAnalyzer - Sensitivity analysis tools

2. decoherence_protection_v18 (NEW):
   - DecoherenceProtectionSimulation - Addresses the "warm brain problem"
   - DebyeLayerShielding - Debye-Huckel electrostatic screening
   - G2TopologicalProtection - G2 holonomy and cycle isolation
   - FrohlichCondensation - Coherent dipole oscillation at THz
   - Honest assessment: achievable ~10^6-10^8, required ~10^11

THE DIOSI-PENROSE FORMULA:
--------------------------
E_G = G * integral integral (rho_1 - rho_2)(rho_1' - rho_2') / |r-r'| d^3r d^3r'

For point-like masses: E_G = G_eff * m^2 / r
Collapse time: tau = hbar / E_G

G2 GEOMETRIC ENHANCEMENT:
-------------------------
G_eff = G_Newton * k_gimel
k_gimel = b3/2 + 1/pi = 12.31831...

This enhancement arises from the G2 holonomy of the compactified dimensions.

DECOHERENCE PROTECTION:
-----------------------
The "warm brain problem": Standard physics gives tau_dec ~ 10^-13 s, but
Orch-OR needs tau ~ 10^-2 s. Three protection mechanisms are analyzed:
- Debye screening: ~10^2 protection
- G2 topology: ~10^2 protection
- Frohlich condensation: ~10^3-10^5 if achieved
- Combined (optimistic): ~10^6-10^8 (still 10^3-10^5 short of 10^11 required)

PHYSICAL PARAMETERS:
-------------------
- N = 10^9 tubulins in coherent superposition
- f = 10^-4 conformational mass fraction (0.01%)
- r = 0.25 nm spatial separation

RESULT:
-------
tau ~ 100 ms (matches neural gamma oscillation at 40 Hz)

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.

Dedicated To:
    My Wife: Elizabeth May Watts
    Our Messiah: Jesus Of Nazareth
"""

from .gravitational_self_energy_v18 import (
    # Main simulation
    DiosiPenroseCalculator,
    PenroseCollapseCalculator,
    ParameterSensitivityAnalyzer,

    # Data classes
    TubulinParameters,

    # Factory functions
    default_tubulin_params,

    # Constants
    HBAR,
    G_NEWTON,
    M_TUBULIN,

    # Main execution
    run_rigorous_derivation,
)

# Decoherence protection mechanisms (v18)
from .decoherence_protection_v18 import (
    DecoherenceProtectionSimulation,
    DebyeLayerShielding,
    G2TopologicalProtection,
    FrohlichCondensation,
    run_decoherence_protection_analysis,
    parameter_sweep_analysis,
)

# Import simulation class if available
try:
    from .gravitational_self_energy_v18 import GravitationalSelfEnergySimulation
except ImportError:
    GravitationalSelfEnergySimulation = None

try:
    from .decoherence_protection_v18 import DecoherenceProtectionSimulationV18
except ImportError:
    DecoherenceProtectionSimulationV18 = None

__all__ = [
    # Simulation wrappers
    'GravitationalSelfEnergySimulation',
    'DecoherenceProtectionSimulationV18',

    # Gravitational self-energy calculators
    'DiosiPenroseCalculator',
    'PenroseCollapseCalculator',
    'ParameterSensitivityAnalyzer',

    # Decoherence protection
    'DecoherenceProtectionSimulation',
    'DebyeLayerShielding',
    'G2TopologicalProtection',
    'FrohlichCondensation',

    # Data classes
    'TubulinParameters',

    # Factory functions
    'default_tubulin_params',

    # Constants
    'HBAR',
    'G_NEWTON',
    'M_TUBULIN',

    # Execution functions
    'run_rigorous_derivation',
    'run_decoherence_protection_analysis',
    'parameter_sweep_analysis',
]
