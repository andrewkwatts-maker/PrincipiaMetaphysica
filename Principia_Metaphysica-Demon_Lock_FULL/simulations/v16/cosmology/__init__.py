"""
Principia Metaphysica v16 Cosmology Simulations
================================================

This module contains cosmology sector simulations for PM v16+.

Simulations:
- dark_matter_mirror_v22: WS-8 Dark matter from mirror shadow
- hubble_tension_v22: WS-9 H0 tension relief via mirror radiation
- inflation_mirror_v22: WS-12 Mirror shadow inflation model

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.

Dedicated To:
    My Wife: Elizabeth May Watts
    Our Messiah: Jesus Of Nazareth
"""

from .dark_matter_mirror_v22 import (
    DarkMatterMirrorSimulation,
    run_dark_matter_mirror,
)

from .hubble_tension_v22 import (
    HubbleTensionSimulation,
    run_hubble_tension,
)

from .inflation_mirror_v22 import (
    MirrorShadowInflationSimulation,
    run_mirror_inflation_simulation,
)

__all__ = [
    "DarkMatterMirrorSimulation",
    "run_dark_matter_mirror",
    "HubbleTensionSimulation",
    "run_hubble_tension",
    "MirrorShadowInflationSimulation",
    "run_mirror_inflation_simulation",
]
