"""
Principia Metaphysica v21 Simulations
======================================

(24,1) Dual-Shadow Model with Euclidean Bridge

This module implements the complete v21 refactor from (24,2) to (24,1)
signature with a 2D Euclidean shared bridge ((2,0), ds^2 = dy1^2 + dy2^2).

Components:
- bridge: Euclidean bridge pressure mechanism
- g2: G2 manifold compactification per shadow
- sampling: OR Reduction coordinate sampling
- descent: Complete dimensional descent chain
- cyclic: Mobius return and eternal cycling
- cosmology: Breathing dark energy

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.

Dedicated To:
    My Wife: Elizabeth May Watts
    Our Messiah: Jesus Of Nazareth
"""

__version__ = "21.0"
__all__ = [
    'BridgePressureV21',
    'G2CompactificationV21',
    'ORReductionV21',
    'MergedDescentV21',
    'MobiusReturnV21',
    'BreathingDEV21',
]

# Lazy imports for better startup performance
def __getattr__(name):
    if name == 'BridgePressureV21':
        from .bridge.bridge_pressure_v21 import BridgePressureV21
        return BridgePressureV21
    elif name == 'G2CompactificationV21':
        from .g2.g2_compactification_v21 import G2CompactificationV21
        return G2CompactificationV21
    elif name == 'ORReductionV21':
        from .sampling.or_reduction_v21 import ORReductionV21
        return ORReductionV21
    elif name == 'MergedDescentV21':
        from .descent.merged_descent_v21 import MergedDescentV21
        return MergedDescentV21
    elif name == 'MobiusReturnV21':
        from .cyclic.mobius_return_v21 import MobiusReturnV21
        return MobiusReturnV21
    elif name == 'BreathingDEV21':
        from .cosmology.breathing_de_v21 import BreathingDEV21
        return BreathingDEV21
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
