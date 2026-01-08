"""
Principia Metaphysica - Dirac Equation Simulations v17.2

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.

This module contains numerical simulations of the Dirac equation
in various contexts, validating the master action's prediction of
relativistic fermion dynamics from the Pneuma spinor descent.

Includes:
- Multi-force wavefunction validation
- 1+1D Dirac evolution (free and with potentials)
- 3+1D Dirac evolution (coarse grid)
- Gravitational coupling (weak field/curved spacetime)
"""

from .wavefunction_validation_v17 import WavefunctionValidation, run_wavefunction_validation
from .dirac_1plus1d_v17 import Dirac1Plus1D, run_dirac_1d_demo
from .dirac_3plus1d_v17 import Dirac3Plus1D, run_dirac_3d_demo
from .dirac_gravity_v17 import DiracGravity, run_dirac_gravity_demo

__all__ = [
    'WavefunctionValidation',
    'Dirac1Plus1D',
    'Dirac3Plus1D',
    'DiracGravity',
    'run_wavefunction_validation',
    'run_dirac_1d_demo',
    'run_dirac_3d_demo',
    'run_dirac_gravity_demo',
]
