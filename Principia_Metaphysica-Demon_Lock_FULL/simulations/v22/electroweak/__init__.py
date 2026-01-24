"""
Principia Metaphysica v22 Electroweak Simulations
==================================================

This module contains the v22 electroweak simulation suite.

Key simulations:
- WeakMixingBridgeV22: Enhanced weak mixing angle from bridge rotation (WS-3)

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.
"""

from .weak_mixing_bridge_v22 import (
    WeakMixingBridgeV22,
    BridgeRotationConfig,
    WeakMixingBridgeResult,
)

__all__ = [
    'WeakMixingBridgeV22',
    'BridgeRotationConfig',
    'WeakMixingBridgeResult',
]
