"""
QCD Confinement from G2 Flux Tube Dynamics
==========================================

This module derives QCD color confinement from the geometry of G2 manifold
associative 3-cycles. The key insight is that color flux is confined to
b3=24 associative cycles, forming flux tubes between quarks with quantized
string tension.

Mathematical Foundation (Established Physics):
---------------------------------------------
1. Wilson Loop Area Law: In confining theories, <W(C)> ~ exp(-sigma * Area)
   where sigma is the string tension.

2. QCD Vacuum Structure: Dual superconductor picture - color magnetic monopoles
   condense, squeezing color electric flux into tubes.

3. Flux Tube Model: Linear confinement potential V(r) = sigma * r
   at large distances, with Coulomb-like 1/r at short distances.

4. Lattice QCD Result: sigma ~ 0.18 GeV^2 (well-established from simulations)

G2 Geometry Connection (PM Framework):
-------------------------------------
- Associative 3-cycles in G2 manifolds provide natural flux tube geometry
- Color flux confined to b3=24 3-cycles, preventing color from spreading
- String tension sigma arises from cycle area/volume ratio
- Asymptotic freedom at short distances from dimensional reduction

Key Components:
--------------
1. FluxTubeConfinementV18: Flux tube approach to confinement
2. WilsonLoopConfinementV18: Wilson loop area law approach (v18)

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.

Dedicated To:
    My Wife: Elizabeth May Watts
    Our Messiah: Jesus Of Nazareth
"""

# Flux tube approach
try:
    from .flux_tube_v18 import (
        FluxTubeConfinementV18,
        G2FluxTubeGeometry,
        ConfinementResult as FluxTubeConfinementResult,
        run_confinement_simulation,
    )
except ImportError:
    FluxTubeConfinementV18 = None
    G2FluxTubeGeometry = None
    FluxTubeConfinementResult = None
    run_confinement_simulation = None

# Wilson loop approach (v18)
from .wilson_loop_v18 import (
    WilsonLoopOperator,
    WilsonLoopConfinementV18,
    WilsonLoopResult,
    ConfinementResult,
    run_wilson_loop_demo,
    run_wilson_loop_analysis,
)

__all__ = [
    # Flux tube approach
    'FluxTubeConfinementV18',
    'G2FluxTubeGeometry',
    'FluxTubeConfinementResult',
    'run_confinement_simulation',
    # Wilson loop approach (v18)
    'WilsonLoopOperator',
    'WilsonLoopConfinementV18',
    'WilsonLoopResult',
    'ConfinementResult',
    'run_wilson_loop_demo',
    'run_wilson_loop_analysis',
]
