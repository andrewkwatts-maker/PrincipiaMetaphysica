"""
Principia Metaphysica - Central Configuration
---------------------------------------------
This file stores the fundamental constants and optimized geometric parameters
derived from the fine-tuning simulations. It serves as the single source of
truth for the PrincipiaMetaphysica repository.

Reference: Principia Metaphysica - A Unified Theory of Physics (Nov 2025)
Optimization Status: CONVERGED (Nov 2025)
"""

import math

# ==============================================================================
# 1. OPTIMIZED GEOMETRIC PARAMETERS (From Fine Tuning)
# ==============================================================================
# These values minimize tension between Dark Energy, Neutrino Mixing, and Proton Decay.
# Derived via 'SimulateTheory_Principia_FineTune.py'
ALPHA_4 = 0.9651  # Influence of 4th shared dimension
ALPHA_5 = 0.2016  # Influence of 5th shared dimension

# ==============================================================================
# 2. FUNDAMENTAL CONSTANTS (Natural Units / GeV)
# ==============================================================================
M_PLANCK = 1.22e19       # GeV (Reduced Planck Mass)
M_GUT_BASE = 1.8e16      # GeV (Base scale before geometric correction)
M_STAR = 1.0e16          # GeV (Fundamental String Scale)

# Geometric Constants from Paper (Section 3)
EULER_CHAR_EFF = 144     # Flux-dressed Euler characteristic
DIVISOR_SO10 = 48        # SO(10) embedding factor
NUM_GENERATIONS = EULER_CHAR_EFF / DIVISOR_SO10  # = 3.0

# ==============================================================================
# 3. DERIVED GEOMETRIC PROPERTIES
# ==============================================================================
# Effective dimensionality of the bulk (Base 12 + Influence)
# Used for Dark Energy EOS calculation (MEP)
D_BASE = 12.0
D_EFF = D_BASE + 0.5 * (ALPHA_4 + ALPHA_5)

# Unified Gauge Coupling (Inverse) with KK corrections
# Ref: Paper Section 4.2b
ALPHA_GUT_INV_BASE = 24.68
ALPHA_GUT_INV_EFF = ALPHA_GUT_INV_BASE - 0.5 * (ALPHA_4 + ALPHA_5)

# Effective GUT Scale with geometric warping
# Ref: Paper Section 7.1
M_GUT_EFF = M_GUT_BASE * (1.0 + 0.15 * (ALPHA_4 + ALPHA_5))

# ==============================================================================
# 4. COSMOLOGICAL PARAMETERS (DERIVED)
# ==============================================================================
# Dark Energy Equation of State (Maximum Entropy Principle)
# w0 = -(d_eff - 1) / (d_eff + 1)
W_0_THEORY = -(D_EFF - 1.0) / (D_EFF + 1.0)

# Thermal Time Parameter (Paper Section 5.2)
ALPHA_T = 2.7 

# ==============================================================================
# 5. EXPERIMENTAL TARGETS (FOR VALIDATION)
# ==============================================================================
TARGETS = {
    "tau_p_limit": 2.4e34,      # Years (Super-K)
    "w_0_desi": -0.83,          # DESI 2024
    "w_0_sigma": 0.06,
    "theta_23": 47.2,           # Degrees (NuFIT)
    "theta_23_sigma": 2.0,
    "m_kk_min": 3500.0,         # GeV (LHC Exclusion)
}

def print_configuration():
    """Helper to display the current model configuration."""
    print("="*60)
    print("PRINCIPIA METAPHYSICA - CORE CONFIGURATION")
    print("="*60)
    print(f"Geometric Parameters:")
    print(f"  α₄ (4th Dim Influence) : {ALPHA_4:.4f}")
    print(f"  α₅ (5th Dim Influence) : {ALPHA_5:.4f}")
    print("-" * 60)
    print(f"Derived Physics:")
    print(f"  Effective Dimension d  : {D_EFF:.4f}")
    print(f"  Predicted w₀ (MEP)     : {W_0_THEORY:.4f}")
    print(f"  Effective M_GUT        : {M_GUT_EFF:.3e} GeV")
    print(f"  Effective 1/α_GUT      : {ALPHA_GUT_INV_EFF:.4f}")
    print("="*60)

if __name__ == "__main__":
    print_configuration()