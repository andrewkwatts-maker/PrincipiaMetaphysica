"""
Principia Metaphysica - Dirac Equation Simulations v18.0

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.

This module contains numerical simulations of the Dirac equation
in various contexts, validating the master action's prediction of
relativistic fermion dynamics from the Pneuma spinor descent.

v18.0: SimulationBase-compliant wrappers with unified validation.

Includes:
- Multi-force wavefunction validation
- 1+1D Dirac evolution (free and with potentials)
- 3+1D Dirac evolution (coarse grid)
- Gravitational coupling (weak field/curved spacetime)
"""

# Core simulation classes (v17 implementations)
from .wavefunction_validation_v17 import WavefunctionValidation, run_wavefunction_validation
from .dirac_1plus1d_v17 import Dirac1Plus1D, run_dirac_1d_demo
from .dirac_3plus1d_v17 import Dirac3Plus1D, run_dirac_3d_demo
from .dirac_gravity_v17 import DiracGravity, run_dirac_gravity_demo

# SimulationBase wrapper (v18)
from .dirac_simulation_v18 import DiracSimulationV18, run_dirac_simulation

__all__ = [
    # Core classes
    'WavefunctionValidation',
    'Dirac1Plus1D',
    'Dirac3Plus1D',
    'DiracGravity',
    # Demo functions
    'run_wavefunction_validation',
    'run_dirac_1d_demo',
    'run_dirac_3d_demo',
    'run_dirac_gravity_demo',
    # SimulationBase wrapper
    'DiracSimulationV18',
    'run_dirac_simulation',
]

__version__ = "18.0"
