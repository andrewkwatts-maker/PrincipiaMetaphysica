"""
Principia Metaphysica v22 Simulations
=====================================

This module contains the v22 simulation suite for PM.

Key simulations:
- electroweak: Enhanced weak mixing angle derivation (WS-3)

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.
"""

from .electroweak.weak_mixing_bridge_v22 import (
    WeakMixingBridgeV22,
    BridgeRotationConfig,
    WeakMixingBridgeResult,
)

__all__ = [
    'WeakMixingBridgeV22',
    'BridgeRotationConfig',
    'WeakMixingBridgeResult',
]
