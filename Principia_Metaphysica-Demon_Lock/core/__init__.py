"""
Principia Metaphysica Core Module
=================================
Single Source of Truth (SSoT) implementation for v16.2 Demon Lock.

This module provides:
- FormulasRegistry: The SSoT class with Ten Pillar Seeds and derived formulas
- DemonLockGuard: Guard rail validation to ensure manifold sterility

Usage:
    from core import get_registry, DemonLockGuard

    # Get the singleton registry
    registry = get_registry()
    h0 = registry.h0_local  # 71.55

    # Run guard rail verification
    guard = DemonLockGuard()
    guard.run_preflight()

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.
"""

from .FormulasRegistry import FormulasRegistry, get_registry
from .demon_lock_guard import DemonLockGuard, require_demon_lock

__all__ = [
    'FormulasRegistry',
    'get_registry',
    'DemonLockGuard',
    'require_demon_lock',
]

__version__ = "16.2"
