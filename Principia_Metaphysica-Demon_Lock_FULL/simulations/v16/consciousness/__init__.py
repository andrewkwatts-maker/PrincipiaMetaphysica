"""
Principia Metaphysica v16 Consciousness Simulations
=====================================================

This module contains consciousness sector simulations for PM v16+.

Simulations:
- four_dice_or_v22: WS-2 - 4 Dice Rolls for Condensate OR Reduction
- gnosis_unlocking_v22: WS-6 Progressive pair activation dynamics

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.

Dedicated To:
    My Wife: Elizabeth May Watts
    Our Messiah: Jesus Of Nazareth
"""

from .four_dice_or_v22 import (
    FourDiceORSimulation,
    run_four_dice_or,
)
from .gnosis_unlocking_v22 import (
    GnosisUnlockingSimulation,
    run_gnosis_unlocking,
)

__all__ = [
    "FourDiceORSimulation",
    "run_four_dice_or",
    "GnosisUnlockingSimulation",
    "run_gnosis_unlocking",
]
