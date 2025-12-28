"""
Principia Metaphysica Simulations v16
=======================================

Version 16.0 simulations using the SimulationBase infrastructure.

This module contains modernized simulations that:
- Implement the SimulationBase abstract interface
- Use PMRegistry for parameter management
- Provide full section content with ContentBlocks
- Define complete formula derivation chains
- Include parameter definitions with experimental bounds

Available domains:
- pneuma: Pneuma field dynamics and geometric coupling
- proton: Proton decay lifetime calculations
- gauge: Gauge coupling unification and GUT scale determination
- neutrino: PMNS neutrino mixing from G2 geometry
- cosmology: Multi-sector cosmological dynamics

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.
"""

from . import pneuma
from . import gauge
from . import neutrino
from . import cosmology

__all__ = ['pneuma', 'gauge', 'neutrino', 'cosmology']
__version__ = "16.0"
