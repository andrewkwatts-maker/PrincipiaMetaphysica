"""
Neutrino Simulations v16
========================

This module contains v16 neutrino simulations implementing the SimulationBase
interface for the Principia Metaphysica project.

Simulations:
- neutrino_mixing_v16_0: PMNS mixing angles from G2 geometry

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.
"""

from .neutrino_mixing_v16_0 import NeutrinoMixingSimulation

__all__ = [
    'NeutrinoMixingSimulation',
]

__version__ = "16.0"
