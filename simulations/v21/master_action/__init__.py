"""
Principia Metaphysica - Master Action Derivations v22.0

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.

Dedicated To:
    My Wife: Elizabeth May Watts
    Our Messiah: Jesus Of Nazareth

=======================================

This module contains explicit derivations of the effective 4D theory
from the 26D master action via Kaluza-Klein reduction over G2 manifolds.

v22.0: 12-Pair (2,0) Bridge System
===================================
Key structural change from v21:
- v21 used: 1x(2,0) bridge + 2x(11,0) shadows (LEGACY)
- v22 uses: 12x(2,0) + (0,1) WARP to create 2x13D(12,1) shadows

The 12-pair system provides:
- Metric: ds^2 = -dt^2 + sum_{i=1}^{12} (dy_{1i}^2 + dy_{2i}^2)
- Bridge Lagrangian: L_bridge = sum_{i=1}^{12} int d^2y_i sqrt(g_{(2,0)}^i) [rho_breath^i + OR^i(Psi_P)]
- Distributed OR: tensor_{i=1}^{12} R_perp_i where R_perp_i = [[0,-1],[1,0]]
- Breathing aggregation: rho_breath = (1/12) sum_{i=1}^{12} |T_normal_i - R_perp_i T_mirror_i|

Derivations include:
- kk_reduction_gr_gauge: 4D GR and U(1) gauge from higher-D EH term
- non_abelian_kk_gauge: Non-Abelian SU(N) gauge kinetics from G2 cycles
- su3_qcd_gauge: SU(3)_C QCD gluon Lagrangian from color cycles
- su2_weak_gauge: SU(2)_L electroweak gauge from weak cycles
- u1_hypercharge: U(1)_Y hypercharge from residual Abelian cycles
- electroweak_mixing: W^3-B mixing to A,Z via Weinberg angle

v18.0: SimulationBase-compliant wrappers with unified schema.
v22.0: 12-pair (2,0) bridge architecture with distributed OR reduction.
"""

# Core gauge derivation classes (v17 implementations)
from .kk_reduction_gr_gauge_v17 import KKReductionGRGauge
from .non_abelian_kk_gauge_v17 import NonAbelianKKGauge
from .su3_qcd_gauge_v17 import SU3QCDGauge
from .su2_weak_gauge_v17 import SU2WeakGauge
from .u1_hypercharge_v17 import U1Hypercharge
from .electroweak_mixing_v17 import ElectroweakMixing

# SimulationBase wrapper (v22 with v18 backward compatibility)
from .master_action_simulation_v18 import (
    MasterActionSimulationV22,
    MasterActionSimulationV18,  # Backward compatibility alias
    run_master_action_simulation,
    N_BRIDGE_PAIRS,
    R_PERP_MATRIX,
)

__all__ = [
    # Core classes
    'KKReductionGRGauge',
    'NonAbelianKKGauge',
    'SU3QCDGauge',
    'SU2WeakGauge',
    'U1Hypercharge',
    'ElectroweakMixing',
    # SimulationBase wrapper (v22)
    'MasterActionSimulationV22',
    'MasterActionSimulationV18',  # Backward compatibility
    'run_master_action_simulation',
    # v22.0: Bridge system constants
    'N_BRIDGE_PAIRS',
    'R_PERP_MATRIX',
]

__version__ = "22.0"
