"""
Principia Metaphysica - Master Action Derivations v18.0

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.

Dedicated To:
    My Wife: Elizabeth May Watts
    Our Messiah: Jesus Of Nazareth

=======================================

This module contains explicit derivations of the effective 4D theory
from the 26D master action via Kaluza-Klein reduction over G2 manifolds.

Derivations include:
- kk_reduction_gr_gauge: 4D GR and U(1) gauge from higher-D EH term
- non_abelian_kk_gauge: Non-Abelian SU(N) gauge kinetics from G2 cycles
- su3_qcd_gauge: SU(3)_C QCD gluon Lagrangian from color cycles
- su2_weak_gauge: SU(2)_L electroweak gauge from weak cycles
- u1_hypercharge: U(1)_Y hypercharge from residual Abelian cycles
- electroweak_mixing: W^3-B mixing to A,Z via Weinberg angle

v18.0: SimulationBase-compliant wrappers with unified schema.
"""

# Core gauge derivation classes (v17 implementations)
from .kk_reduction_gr_gauge_v17 import KKReductionGRGauge
from .non_abelian_kk_gauge_v17 import NonAbelianKKGauge
from .su3_qcd_gauge_v17 import SU3QCDGauge
from .su2_weak_gauge_v17 import SU2WeakGauge
from .u1_hypercharge_v17 import U1Hypercharge
from .electroweak_mixing_v17 import ElectroweakMixing

# SimulationBase wrapper (v18)
from .master_action_simulation_v18 import MasterActionSimulationV18, run_master_action_simulation

__all__ = [
    # Core classes
    'KKReductionGRGauge',
    'NonAbelianKKGauge',
    'SU3QCDGauge',
    'SU2WeakGauge',
    'U1Hypercharge',
    'ElectroweakMixing',
    # SimulationBase wrapper
    'MasterActionSimulationV18',
    'run_master_action_simulation',
]

__version__ = "19.2"
