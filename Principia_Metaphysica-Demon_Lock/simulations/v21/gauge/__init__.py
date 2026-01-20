"""
Principia Metaphysica - Gauge Simulations v16/v18

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.

Dedicated To:
    My Wife: Elizabeth May Watts
    Our Messiah: Jesus Of Nazareth
"""

from .gauge_unification_v16_0 import GaugeUnificationSimulation
from .gauge_simulation_v18 import GaugeSimulationV18, run_gauge_simulation

__all__ = [
    # v16 modules
    'GaugeUnificationSimulation',
    # v18 consolidated wrapper
    'GaugeSimulationV18',
    'run_gauge_simulation',
]

__version__ = "19.2"
