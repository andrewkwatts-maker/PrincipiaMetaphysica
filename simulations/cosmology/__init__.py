"""
Principia Metaphysica - Cosmology Simulations
==============================================

This module contains cosmological simulations for the PM framework,
including Hubble tension resolution, dark energy derivations, and
Ricci flow dynamics.

Simulations:
- ricci_flow_integrator_v16_2: Hamilton-Perelman Ricci flow for H(z) evolution

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.

Dedicated To:
    My Wife: Elizabeth May Watts
    Our Messiah: Jesus Of Nazareth
"""

from .ricci_flow_integrator_v16_2 import (
    RicciFlowCosmology,
    export_ricci_flow_integrator_v16_2,
    H0_PLANCK,
    H0_SHOES,
    Z_CMB,
)

__all__ = [
    'RicciFlowCosmology',
    'export_ricci_flow_integrator_v16_2',
    'H0_PLANCK',
    'H0_SHOES',
    'Z_CMB',
]

__version__ = "19.2"
