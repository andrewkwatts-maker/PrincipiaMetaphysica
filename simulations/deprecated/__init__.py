"""
Deprecated simulation files - v14.1 cleanup

These files are kept for backward compatibility only.
Do NOT use for new development - use the canonical v13.0+ files instead.

Files moved here:
- proton_decay_v84_ckm.py (replaced by proton_decay_geometric_v13_0.py)
- proton_decay_channels.py (integrated into proton_decay_geometric_v13_0.py)
- proton_lifetime_v11.py (replaced by proton_decay_geometric_v13_0.py)
- proton_decay_rg_hybrid.py (replaced by proton_decay_geometric_v13_0.py)
- neutrino_mass_matrix_final_v12.py (replaced by neutrino_mass_matrix_final_v12_7.py)
- neutrino_mass_matrix_v10_1.py (replaced by neutrino_mass_matrix_final_v12_7.py)
- tune_neutrino_v12_3.py (no longer needed with exact formulas)
- validate_neutrino_fix_v12_3.py (no longer needed)
- neutrino_ordering_v9.py (replaced by neutrino_mass_ordering.py)
- higgs_mass_v11.py (replaced by higgs_mass_v12_4_moduli_stabilization.py)
- full_yukawa_v10.py (replaced by higgs_yukawa_rg_v12_4.py)
- gauge_unification_merged.py (replaced by g2_torsion_m_gut_v12_4.py)
- kk_graviton_mass_v12.py (CRITICAL BUG - 10^13x error, use kk_graviton_mass_v12_fixed.py)

Copyright (c) 2025 Andrew Keith Watts. All rights reserved.
"""

DEPRECATED_VERSION = "v14.1"
DEPRECATED_REASON = "Replaced by geometric v13.0+ simulations"
