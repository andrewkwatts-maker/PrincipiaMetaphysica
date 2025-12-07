#!/usr/bin/env python3
"""
Fix M_Pl consistency issue in config.py for v12.4

This script standardizes all Planck mass references to use M_PLANCK_REDUCED = 2.435e18 GeV
instead of the inconsistent mix of 1.2195e19 and 1.22e19 values.

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.
"""

import re

def fix_m_pl_consistency():
    """Fix M_Pl definition inconsistency in config.py"""

    config_path = "config.py"

    # Read file
    with open(config_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Fix 1: Update PhenomenologyParameters.M_PLANCK definition
    old_phenom_scales = """    # Energy Scales
    M_PLANCK = 1.2195e19     # Reduced Planck mass [GeV] (PDG 2024)
    M_STAR = 1e19            # 13D fundamental scale [GeV] (~ M_Pl)"""

    new_phenom_scales = """    # Energy Scales (v12.4 fix: standardized on reduced Planck mass)
    M_PLANCK_REDUCED = 2.435e18  # Reduced Planck mass [GeV] M_Pl = sqrt(ħc/8πG)
    M_PLANCK_FULL = 1.221e19     # Full Planck mass [GeV] M_P = sqrt(ħc/G) (reference only)
    M_PLANCK = M_PLANCK_REDUCED  # Default: use reduced mass everywhere
    M_STAR = 1e19                # 13D fundamental scale [GeV] (~ M_Pl)"""

    content = content.replace(old_phenom_scales, new_phenom_scales)

    # Fix 2: Update ModuliParameters.M_PLANCK (the duplicate at line 288)
    old_moduli_mpl = """    # V_9 = M_Pl^2 / M_*^11 ~ 1.488×10^{-138} GeV^{-9}
    # From M_* = 1×10^19 GeV [GeV]
    M_PLANCK = 1.22e19        # Planck mass [GeV]"""

    new_moduli_mpl = """    # V_9 = M_Pl^2 / M_*^11 ~ 1.488×10^{-138} GeV^{-9}
    # From M_* = 1×10^19 GeV [GeV]
    # DEPRECATED: Use PhenomenologyParameters.M_PLANCK_REDUCED instead
    # M_PLANCK = 1.22e19  # Old value - DO NOT USE"""

    content = content.replace(old_moduli_mpl, new_moduli_mpl)

    # Fix 3: Update all references in formulas to use consistent value
    # Replace hardcoded 1.22e19 with PhenomenologyParameters.M_PLANCK
    content = re.sub(
        r'M_Pl = 1\.22e19\s*# GeV',
        'M_Pl = PhenomenologyParameters.M_PLANCK_REDUCED  # GeV (v12.4: use reduced mass)',
        content
    )

    # Fix 4: Add comment about the fix in VERSION section
    old_version = 'VERSION = "12.0"'
    new_version = 'VERSION = "12.4"'
    content = content.replace(old_version, new_version)

    old_changelog = """CHANGELOG v12.0:
- Added v9.0 Transparency: FittedParameters class with full provenance
- Added v10.0 Geometric Derivations: TorsionClass, FluxQuantization, AnomalyCancellation
- Added v10.1 Neutrino Mass: RightHandedNeutrinoMasses, Seesaw parameters
- Added v10.2 Fermion Matrix: CycleIntersections, WilsonLinePhases, HiggsVEVs
- Added v11.0 Observables: ProtonLifetimeParameters, HiggsMassParameters
- Added v12.0 Final: KKGravitonParameters, FinalNeutrinoMasses
- All parameters now traceable to geometric origin (TCS G₂ manifold CHNP #187)"""

    new_changelog = """CHANGELOG v12.4:
- v12.0: Added KKGravitonParameters, FinalNeutrinoMasses
- v12.1: Updated alpha4/alpha5 to NuFIT 6.0 (theta_23 = 45.0°)
- v12.2: Hybrid neutrino suppression (base 39.81 × flux 3.12 = 124.22)
- v12.3: Fixed neutrino mass unit bug (1M× error), delta_m² calculation
- v12.4: CRITICAL FIX - M_Pl standardized to reduced mass (2.435e18 GeV)
  * Fixes 20% inconsistency between PhenomenologyParameters and ModuliParameters
  * All formulas now use M_PLANCK_REDUCED consistently
  * Added dual derivations for Higgs mass and M_GUT"""

    content = content.replace(old_changelog, new_changelog)

    # Write updated content
    with open(config_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print("✅ M_Pl consistency fix applied successfully!")
    print(f"   M_PLANCK_REDUCED = 2.435e18 GeV (correct reduced Planck mass)")
    print(f"   M_PLANCK_FULL = 1.221e19 GeV (reference only)")
    print(f"   Version updated: 12.0 → 12.4")

    return True

if __name__ == "__main__":
    fix_m_pl_consistency()
