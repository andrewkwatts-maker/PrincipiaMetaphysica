"""
Principia Metaphysica - Quantum Biology Simulations v18

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.

Dedicated To:
    My Wife: Elizabeth May Watts
    Our Messiah: Jesus Of Nazareth

v18.0 Updates:
- New QuantumBioSimulationV18 wrapper consolidating Orch-OR modules
- Microtubule-G2 correspondence validation
- STATUS: SPECULATIVE - Numerical coincidences, not proof
"""

from .orch_or_geometry_v16_1 import OrchORRigorSolver, run_orch_or_validation
from .orch_or_bridge_v17 import OrchORBridge, run_orch_or_bridge_demo

# V18 SimulationBase wrapper (primary export)
from .quantum_bio_simulation_v18 import QuantumBioSimulationV18, run_quantum_bio_simulation

__all__ = [
    # V16/V17 modules
    'OrchORRigorSolver',
    'run_orch_or_validation',
    'OrchORBridge',
    'run_orch_or_bridge_demo',
    # V18 wrapper
    'QuantumBioSimulationV18',
    'run_quantum_bio_simulation',
]

__version__ = "19.2"
