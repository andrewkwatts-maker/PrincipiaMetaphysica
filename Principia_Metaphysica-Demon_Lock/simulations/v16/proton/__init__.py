"""
Principia Metaphysica - Proton Physics Simulations v18.0

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.

Dedicated To:
    My Wife: Elizabeth May Watts
    Our Messiah: Jesus Of Nazareth

This module provides proton physics simulations:
- ProtonDecaySimulation: v17 proton decay lifetime from TCS geometry
- ProtonSimulationV18: Consolidated v18 wrapper for all proton physics
- run_proton_simulation: Convenience function to run v18 simulation
"""

from .proton_decay_v16_0 import ProtonDecaySimulation
from .proton_simulation_v18 import ProtonSimulationV18, run_proton_simulation

__all__ = [
    'ProtonDecaySimulation',
    'ProtonSimulationV18',
    'run_proton_simulation',
]
