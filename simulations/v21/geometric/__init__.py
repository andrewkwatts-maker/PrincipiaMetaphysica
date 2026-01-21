"""
Principia Metaphysica - Geometric Domain Simulations v16

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.

Dedicated To:
    My Wife: Elizabeth May Watts
    Our Messiah: Jesus Of Nazareth
"""

from .g2_geometry_v16_0 import G2GeometryV16
from .alpha_rigor_v16_1 import AlphaRigorSolver, run_alpha_derivation

# v16.2 - Unified Time Physics and Leech Partition
from .leech_partition_v16_2 import LeechPartitionV16
from .modular_invariance_v16_2 import ModularInvarianceV16

# v18.0 - Consolidated geometric simulation wrapper
from .geometric_simulation_v18 import GeometricSimulationV18, run_geometric_simulation

__all__ = [
    'G2GeometryV16',
    'AlphaRigorSolver',
    'run_alpha_derivation',
    # v16.2
    'LeechPartitionV16',
    'ModularInvarianceV16',
    # v18.0 - Consolidated wrapper
    'GeometricSimulationV18',
    'run_geometric_simulation',
]
# v23.0: Updated per comprehensive audit 2026-01-21
__version__ = "23.0"
