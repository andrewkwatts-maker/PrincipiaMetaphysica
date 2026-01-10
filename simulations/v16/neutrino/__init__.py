"""
Principia Metaphysica - Neutrino Simulations v18.0

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.

Dedicated To:
    My Wife: Elizabeth May Watts
    Our Messiah: Jesus Of Nazareth

v18.0 Updates:
- New NeutrinoSimulationV18 wrapper consolidating neutrino physics
- PMNS mixing angles from G2 topology
- Neutrino mass spectrum with Inverted Ordering
- Full SSOT compliance via PMRegistry
"""

from .neutrino_mixing_v16_0 import NeutrinoMixingSimulation

# V18 SimulationBase wrapper (primary export)
from .neutrino_simulation_v18 import NeutrinoSimulationV18, run_neutrino_simulation

__all__ = [
    # V16/V17 modules
    'NeutrinoMixingSimulation',
    # V18 wrapper
    'NeutrinoSimulationV18',
    'run_neutrino_simulation',
]

__version__ = "18.0"
