"""
Cosmology Simulations v16
==========================

Multi-sector cosmology with geometric width derivation and dark energy dynamics.

This module contains v16 implementations of cosmological simulations that
implement the SimulationBase interface from simulations.base.

Available simulations:
- DarkEnergyV16: Dark energy from dimensional reduction (Section 5.2)
- MultiSectorV16: Multi-sector sampling with geometric modulation width (Section 5.3)

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.
"""

from .dark_energy_v16_0 import DarkEnergyV16
from .multi_sector_v16_0 import MultiSectorV16

__all__ = ['DarkEnergyV16', 'MultiSectorV16']

__version__ = "16.0"
