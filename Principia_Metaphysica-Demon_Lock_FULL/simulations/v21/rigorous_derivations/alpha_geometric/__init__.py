"""
Principia Metaphysica - Alpha Geometric Derivations
====================================================

Attempts to derive the fine structure constant from G2 holonomy
and related geometric structures.

AVAILABLE SIMULATIONS:
1. holonomy_alpha_v18 - Holonomy-based alpha derivation
   - Investigates G2 holonomy ratio 14/21 = 2/3
   - Examines Wilson loops, parallel transport, characteristic classes
   - Rigorous assessment of numerology vs derivation

Includes rigorous assessment of each approach.

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.

Dedicated To:
    My Wife: Elizabeth May Watts
    Our Messiah: Jesus Of Nazareth
"""

# Import only the holonomy module - other modules referenced by linter don't exist yet
try:
    from .holonomy_alpha_v18 import HolonomyAlphaSimulation, run_holonomy_alpha_demo
    __all__ = [
        'HolonomyAlphaSimulation',
        'run_holonomy_alpha_demo',
    ]
except ImportError as e:
    # Minimal exports if imports fail
    __all__ = []
    print(f"Warning: Could not import holonomy_alpha_v18: {e}")
