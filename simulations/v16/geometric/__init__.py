"""
Geometric Domain Simulations v16
=================================

G2 geometry, topology, and cycle structure simulations.

This module contains root simulations that compute fundamental
geometric parameters from the TCS G2 manifold topology.

Available simulations:
- G2GeometryV16: G2 holonomy, Betti numbers, and topology invariants
- AlphaRigorSolver: Fine structure constant derivation from G2 topology

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.
"""

from .g2_geometry_v16_0 import G2GeometryV16
from .alpha_rigor_v16_1 import AlphaRigorSolver, run_alpha_derivation

__all__ = ['G2GeometryV16', 'AlphaRigorSolver', 'run_alpha_derivation']
__version__ = "16.1"
