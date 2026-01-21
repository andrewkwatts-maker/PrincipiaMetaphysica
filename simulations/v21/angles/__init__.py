"""
Principia Metaphysica - Geometric Angles v18.0

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.

Dedicated To:
    My Wife: Elizabeth May Watts
    Our Messiah: Jesus Of Nazareth

=======================================

This module computes key geometric angles in the theory:
- Bazien angles: Shadow brane intersection angles in dimensional descent
- Octonion angles: Division algebra angles (golden, triality, Fano)
- G2 holonomy angles: Calibration and symmetry locking angles
- SU(3) embedding angles: Regular and irregular embeddings in G2

v18.0: SimulationBase-compliant wrappers with unified schema.
"""

# Core angle classes (v17 implementations)
from .bazien_angles_v17 import BazienAngles, run_bazien_demo
from .octonion_angles_v17 import OctonionAngles, run_octonion_demo
from .g2_holonomy_angles_v17 import G2HolonomyAngles, run_g2_holonomy_demo
from .su3_embedding_angles_v17 import SU3EmbeddingAngles, run_su3_embedding_demo

# SimulationBase wrapper (v18)
from .angles_simulation_v18 import AnglesSimulationV18, run_angles_simulation

__all__ = [
    # Core classes
    'BazienAngles',
    'OctonionAngles',
    'G2HolonomyAngles',
    'SU3EmbeddingAngles',
    # Demo functions
    'run_bazien_demo',
    'run_octonion_demo',
    'run_g2_holonomy_demo',
    'run_su3_embedding_demo',
    # SimulationBase wrapper
    'AnglesSimulationV18',
    'run_angles_simulation',
]

# v23.0: Updated per comprehensive audit 2026-01-21
__version__ = "23.0"
