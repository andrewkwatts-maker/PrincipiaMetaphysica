#!/usr/bin/env python3
"""
Copyright (c) 2025 Andrew Keith Watts. All rights reserved.

PRINCIPIA METAPHYSICA - GEOMETRIC FINE TUNING (THEORY ALIGNED)
--------------------------------------------------------------
Reference: Principia Metaphysica - A Unified Theory of Physics (Nov 2025)
Context:   (5,1) Observable Brane embedded in 13D Shadow Bulk

GOAL:
Find the natural geometric influence parameters (α₄, α₅) of the
shared extra dimensions that align the theory's predictions with 
experimental data, without using arbitrary suppression factors.

THEORETICAL CONSTRAINTS (from Paper):
1. Dark Energy (w₀): Determined by effective bulk dimension d_eff.
   Theory base: d_eff = 12 => w₀ = -11/13 ≈ -0.846.
   (Section 8.3)

2. Neutrino Mixing (θ₂₃): Deviations from maximal 45° mixing driven
   by geometric asymmetry in the extra dimensions.
   (Section 7.4)

3. Proton Decay (τₚ): Standard GUT formula (Eq 7.3) modified by
   geometric corrections to M_GUT and α_GUT via KK towers.
   (Section 7.1)

Dependencies: pandas, numpy, scipy
"""

import numpy as np
import pandas as pd
from scipy.optimize import minimize
import warnings
warnings.filterwarnings('ignore')

print("=" * 80)
print("PRINCIPIA METAPHYSICA: GEOMETRIC INFLUENCE TUNING")
print("Aligning (5,1) Brane Geometry with Experimental Data")
print("=" * 80)
print()

# ==============================================================================
# 1. FUNDAMENTAL CONSTANTS & EXPERIMENTAL TARGETS
# ==============================================================================

# --- Theory Constants (from Paper) ---
M_GUT_base = 1.8e16       # GeV (Section 4.2 / Eq 4.4)
Alpha_GUT_inv_base = 24.68 # Base unified coupling (Section 4.2b)
Alpha_H = 0.015           # GeV^3 (Hadronic matrix element, Eq 7.2 text)
m_proton = 0.938          # GeV

# --- Experimental Targets (The "Truth") ---
# 1. Proton Lifetime (Super-K Lower Bound)
#    Paper prediction: 4.0e34 (+2.5/-1.5). 
#    Constraint: Must be > 2.4e34.
tau_p_limit = 2.4e34      # years

# 2. Dark Energy EOS (DESI 2024)
#    Paper status: -0.846 (0.3 sigma match).
#    Optimization Target: Try to get closer to -0.83 if geometry allows.
w_0_target = -0.83
w_0_sigma = 0.06

# 3. Neutrino Mixing Angle (NuFIT 5.2)
#    Target: 47.2 degrees.
theta_23_target = 47.2
theta_23_sigma = 2.0

# 4. KK Graviton Mass (LHC Constraints)
#    Paper prediction: ~5 TeV (Section 7.4).
#    Constraint: > 3.5 TeV (LHC exclusion).
m_KK_target = 5000.0      # GeV
m_KK_sigma = 1000.0


# ==============================================================================
# 2. PHYSICS ENGINE: DERIVATIONS FROM GEOMETRY
# ==============================================================================

def get_effective_dimension(alpha_4, alpha_5):
    """
    Calculates effective bulk dimension d_eff.
    Base theory uses d=12 (from 13D shadow - 1 time).
    Geometric influence (α₄, α₅) perturbs the effective volume/dimension.
    """
    d_base = 12.0
    # Perturbation from extra dimensional influence
    delta_d = 0.5 * (alpha_4 + alpha_5)
    return d_base + delta_d

def predict_w0(alpha_4, alpha_5):
    """
    Calculates Dark Energy EOS using Maximum Entropy Principle.
    Ref: Section 8.3 / Eq 6.1 context
    w₀ = -(d_eff - 1) / (d_eff + 1)
    """
    d_eff = get_effective_dimension(alpha_4, alpha_5)
    w_0 = -(d_eff - 1.0) / (d_eff + 1.0)
    return w_0

def predict_theta_23(alpha_4, alpha_5):
    """
    Calculates Atmospheric Neutrino Mixing Angle.
    Ref: Section 7.4
    Asymmetry (α₄ - α₅) breaks the maximal 45° symmetry.
    """
    base_angle = 45.0
    shift = 3.0 * (alpha_4 - alpha_5)
    return base_angle + shift

def predict_proton_lifetime(alpha_4, alpha_5):
    """
    Calculates Proton Lifetime using Eq 7.3 form.
    τₚ ≈ (M_X⁴ / m_p⁵) * (1/α_GUT²) * C_factors
    
    Geometric Updates:
    - M_GUT scales with (α₄ + α₅) due to KK threshold corrections (Paper §4.2b).
    - α_GUT runs differently due to KK tower modifications (Paper §4.2b).
    """
    # 1. Geometric Correction to M_GUT (Threshold Correction Δ_TC)
    #    Paper says Δ_TC is positive. Influence increases effective scale.
    #    Scaling factor assumption: 15% per unit influence.
    M_GUT_eff = M_GUT_base * (1.0 + 0.15 * (alpha_4 + alpha_5))
    
    # 2. Geometric Correction to 1/α_GUT (KK Correction Δ_KK)
    #    Paper says Δ_KK contributes ~10%.
    #    Standard KK towers reduce 1/α (make coupling stronger/larger).
    #    However, previous script logic found we need 1/α to INCREASE to suppress decay.
    #    Let's stick to the paper's RG logic: KK modes usually accelerate running,
    #    lowering M_GUT if not careful, but here we assume the unified coupling value 
    #    changes.
    #    Let's model the shift in 1/α directly.
    #    (1/α)_eff = 24.68 - 0.5 * (α₄ + α₅)
    alpha_inv_eff = Alpha_GUT_inv_base - 0.5 * (alpha_4 + alpha_5)
    
    # Avoid unphysical coupling
    if alpha_inv_eff < 1.0: alpha_inv_eff = 1.0

    # 3. Calculate Lifetime (Eq 7.3 approx)
    #    Constants grouped into C_prefactor based on the base prediction 
    #    of 4.0e34 using base parameters.
    #    τ_base = C * (M_base)^4 * (1/α_base)^2
    #    τ_new  = τ_base * (M_new/M_base)^4 * ((1/α_new)/(1/α_base))^2
    
    base_prediction = 4.0e34 # Years (Section 7.1)
    
    scaling_M = (M_GUT_eff / M_GUT_base)**4
    scaling_alpha = (alpha_inv_eff / Alpha_GUT_inv_base)**2 # Note: τ ∝ 1/α² = (1/α)²
    
    # Note on Eq 7.3: τ ∝ 1/α² means τ ∝ (Inverse_Alpha)²
    
    return base_prediction * scaling_M * scaling_alpha

def predict_kk_mass(alpha_4, alpha_5):
    """
    Calculates 1st KK Mode Mass.
    Ref: Eq 7.4b (m ~ 1/R)
    Influence parameters warp the effective radius R_eff.
    """
    R_shared_base = 1.0 / 5000.0 # 5 TeV base
    
    # Geometric influence: Magnitude determines warping
    warp_factor = np.sqrt(alpha_4**2 + alpha_5**2)
    
    # If no influence, mass is base. If influence > 1, mass drops (radius grows).
    # If influence < 1, mass increases (radius shrinks).
    # We model it as R_eff = R_base / warp_factor (if warp > 0)
    # This implies m_eff = m_base * warp_factor
    
    # Regularization for zero influence
    if warp_factor < 0.01: warp_factor = 1.0
        
    return 5000.0 * warp_factor # GeV


# ==============================================================================
# 3. OPTIMIZATION CORE
# ==============================================================================

def cost_function(params):
    """
    Chi-Squared Cost Function.
    Optimizes only α₄, α₅. No arbitrary alpha_6.
    """
    a4, a5 = params
    
    # Calculate predictions
    w0_pred = predict_w0(a4, a5)
    theta_pred = predict_theta_23(a4, a5)
    tau_pred = predict_proton_lifetime(a4, a5)
    m_kk_pred = predict_kk_mass(a4, a5)
    
    # --- Cost Components ---
    
    # 1. Dark Energy (w0)
    #    Target: -0.83 +/- 0.06
    chi_w0 = ((w0_pred - w_0_target) / w_0_sigma) ** 2
    
    # 2. Neutrino Mixing (theta_23)
    #    Target: 47.2 +/- 2.0
    chi_theta = ((theta_pred - theta_23_target) / theta_23_sigma) ** 2
    
    # 3. Proton Decay (Lower Bound Constraint)
    #    We don't punish if > 2.4e34. We punish heavily if < 2.4e34.
    if tau_pred < tau_p_limit:
        # Exponential penalty for violating the bound
        chi_tau = 10.0 + ((tau_p_limit - tau_pred) / 1.0e33) ** 2
    else:
        # Slight reward for being higher, or just zero?
        # Let's add a weak potential to guide it towards the theory prediction (4.0)
        # to prevent it running off to infinity unphysically.
        chi_tau = ((tau_pred - 4.0e34) / 4.0e34) ** 2 * 0.1
        
    # 4. KK Mass
    #    Soft constraint around 5 TeV
    chi_kk = ((m_kk_pred - m_KK_target) / m_KK_sigma) ** 2 * 0.5
    
    return chi_w0 + chi_theta + chi_tau + chi_kk

def run_fine_tuning():
    """
    Finds optimal geometric parameters.
    """
    # Initial Guess: Previous results suggested α4 ~ 1.0, α5 ~ 0.5
    initial_guess = [1.0, 0.5]
    
    # Unconstrained bounds (Let geometry find its natural state)
    bounds = ((None, None), (None, None))
    
    print(f"Starting Optimization...")
    result = minimize(
        cost_function, 
        initial_guess, 
        method='L-BFGS-B', 
        bounds=bounds
    )
    return result

# ==============================================================================
# 4. MAIN EXECUTION
# ==============================================================================

if __name__ == "__main__":
    res = run_fine_tuning()
    
    a4_opt, a5_opt = res.x
    
    # Final values
    w0_final = predict_w0(a4_opt, a5_opt)
    theta_final = predict_theta_23(a4_opt, a5_opt)
    tau_final = predict_proton_lifetime(a4_opt, a5_opt)
    m_kk_final = predict_kk_mass(a4_opt, a5_opt)
    d_eff_final = get_effective_dimension(a4_opt, a5_opt)
    
    print("\n" + "="*80)
    print("FINE TUNING RESULTS (ALPHA 6 REMOVED)")
    print("="*80)
    
    print(f"\nOptimal Geometric Parameters:")
    print(f"α₄ (4th Dim) : {a4_opt:.4f}")
    print(f"α₅ (5th Dim) : {a5_opt:.4f}")
    
    print(f"\nModel Predictions vs Experimental Data:")
    
    print(f"\n1. Proton Lifetime (τₚ)")
    print(f"   Prediction : {tau_final:.3e} years")
    print(f"   Limit      : > {tau_p_limit:.3e} years")
    print(f"   Theory Ref : 4.0e34 years")
    status_tau = "PASS" if tau_final > tau_p_limit else "FAIL"
    print(f"   Status     : {status_tau}")
    
    print(f"\n2. Dark Energy EOS (w₀)")
    print(f"   Prediction : {w0_final:.4f}")
    print(f"   Target     : {w_0_target} ± {w_0_sigma}")
    print(f"   d_eff      : {d_eff_final:.4f}")
    status_w0 = "PASS" if abs(w0_final - w_0_target) < w_0_sigma else "FAIL"
    print(f"   Status     : {status_w0}")
    
    print(f"\n3. Neutrino Mixing (θ₂₃)")
    print(f"   Prediction : {theta_final:.2f}°")
    print(f"   Target     : {theta_23_target}° ± {theta_23_sigma}°")
    status_theta = "PASS" if abs(theta_final - theta_23_target) < theta_23_sigma else "FAIL"
    print(f"   Status     : {status_theta}")
    
    print(f"\n4. KK Graviton Mass")
    print(f"   Prediction : {m_kk_final/1000.0:.2f} TeV")
    print(f"   Target     : ~5.00 TeV")
    
    print("\n" + "="*80)
    if status_tau == "PASS" and status_w0 == "PASS" and status_theta == "PASS":
        print("CONCLUSION: The model can reproduce experimental data using ONLY")
        print("            geometric influence parameters (α₄, α₅).")
        print("            Arbitrary suppression factors are not required.")
    else:
        print("CONCLUSION: Tension remains. Pure geometry may not be sufficient")
        print("            to satisfy all constraints simultaneously.")
    print("="*80)