"""
Principia Metaphysica - Higgs Simulations v16/v18

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.

Dedicated To:
    My Wife: Elizabeth May Watts
    Our Messiah: Jesus Of Nazareth
"""

from .higgs_mass_v16_0 import HiggsMassSimulation
from .higgs_vev_derivation_v16_1 import HiggsVEVDerivationV16
from .higgs_brane_partition_v16_2 import HiggsBranePartitionSimulation
from .higgs_simulation_v18 import HiggsSimulationV18, run_higgs_simulation
from .higgs_vev_refined_v18 import HiggsVEVRefinedV18

__all__ = [
    # v16 modules
    'HiggsMassSimulation',
    'HiggsVEVDerivationV16',
    'HiggsBranePartitionSimulation',
    # v18 consolidated wrapper
    'HiggsSimulationV18',
    'run_higgs_simulation',
    # v18 refined VEV (addresses G_F precision)
    'HiggsVEVRefinedV18',
]

__version__ = "18.3"
