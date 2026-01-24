"""
Principia Metaphysica v16 Fermion Simulations
==============================================

This module contains fermion sector simulations for PM v16+.

Simulations:
- spin_shadow_mapping_v22: WS-4 Per-pair Spin(7) fraction distribution
- chirality_flip_v22: WS-10 Möbius chirality asymmetry effects

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.

Dedicated To:
    My Wife: Elizabeth May Watts
    Our Messiah: Jesus Of Nazareth
"""

from .spin_shadow_mapping_v22 import (
    SpinShadowMappingSimulation,
    run_spin_shadow_mapping,
)

from .chirality_flip_v22 import (
    ChiralityFlipSimulation,
    run_chirality_flip,
)

__all__ = [
    "SpinShadowMappingSimulation",
    "run_spin_shadow_mapping",
    "ChiralityFlipSimulation",
    "run_chirality_flip",
]
