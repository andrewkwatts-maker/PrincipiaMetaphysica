"""
Fermion Simulations v16
========================

Fermion generation and Yukawa texture simulations implementing SimulationBase.

Available simulations:
- chirality_v16_0: Chirality and spinorial structure from G2 holonomy
- fermion_generations_v16_0: Three generations from G2 topology via Pneuma mechanism
- ckm_matrix_v16_0: CKM matrix and quark mixing from G2 phases

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.
"""

from .chirality_v16_0 import ChiralitySpinorSimulation
from .fermion_generations_v16_0 import FermionGenerationsV16
from .ckm_matrix_v16_0 import CKMMatrixSimulation

__all__ = ['ChiralitySpinorSimulation', 'FermionGenerationsV16', 'CKMMatrixSimulation']
