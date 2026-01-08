"""
Principia Metaphysica - Simulations v16

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.

Dedicated To:
    My Wife: Elizabeth May Watts
    Our Messiah: Jesus Of Nazareth

=======================================

Version 16.0 simulations using the SimulationBase infrastructure.

This module contains modernized simulations that:
- Implement the SimulationBase abstract interface
- Use PMRegistry for parameter management
- Provide full section content with ContentBlocks
- Define complete formula derivation chains
- Include parameter definitions with experimental bounds

Available domains:
- introduction: Introduction and framework overview (Section 1)
- geometric: G2 geometry and topology (Section 2)
- pneuma: Pneuma field dynamics and geometric coupling (Section 2)
- gauge: Gauge coupling unification and GUT scale (Section 3)
- fermion: Fermion generations and Yukawa hierarchy (Section 4)
- higgs: Higgs mass from moduli stabilization (Section 4.4)
- neutrino: PMNS neutrino mixing from G2 geometry (Section 4.5)
- proton: Proton decay lifetime calculations (Section 4.6)
- cosmology: Multi-sector cosmological dynamics (Section 5)
- thermal: Thermal time hypothesis (Section 5 - thermal-time)
- predictions: Falsifiable predictions aggregator (Section 6)
- discussion: Discussion and future directions (Section 7)
- master_action: Master action derivations (KK reduction, gauge sectors)
- angles: Geometric angles (Bazien, octonion, G2 holonomy, SU3 embedding)
- constants: Physical constants derivations (alpha, c, weak mixing, etc.)
- dirac: Dirac equation simulations (1+1D, 3+1D, curved spacetime)
- validation: Validation scripts (residue calculator, cosmology)
"""

from . import introduction
from . import master_action
from . import angles
from . import constants
from . import dirac
from . import validation
from . import geometric
from . import pneuma
from . import gauge
from . import fermion
from . import higgs
from . import neutrino
from . import proton
from . import cosmology
from . import thermal
from . import predictions
from . import discussion

__all__ = [
    'introduction',
    'master_action',
    'angles',
    'constants',
    'dirac',
    'validation',
    'geometric',
    'pneuma',
    'gauge',
    'fermion',
    'higgs',
    'neutrino',
    'proton',
    'cosmology',
    'thermal',
    'predictions',
    'discussion',
]
__version__ = "17.2"
