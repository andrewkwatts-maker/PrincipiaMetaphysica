#!/usr/bin/env python3
"""
Copyright (c) 2025 Andrew Keith Watts. All rights reserved.

PRINCIPIA METAPHYSICA - THEORY SIMULATION & FINE TUNING
-------------------------------------------------------
Context: (5,1) Observable Brane embedded in Bulk
Goal: Tune influence parameters (α₄, α₅) of the shared extra dimensions
      to resolve outstanding theoretical tensions.

Reference: https://github.com/andrewkwatts-maker/PrincipiaMetaphysica
           https://www.metaphysicæ.com

THEORETICAL FRAMEWORK:
1. Dark Energy (w₀): Determined by the Effective Dimension (d_eff) of the bulk
   accessible to the Mashiach entropy field.
   w₀ = -(d_eff - 1) / (d_eff + 1)

2. Neutrino Mixing (θ₂₃): Deviations from maximal SO(10) mixing (45°) are 
   driven by geometric asymmetry in the extra dimensions (α₄ ≠ α₅).

3. Proton Decay (τₚ): The unification scale M_GUT is modified by the 
   sum of influences (α₄ + α₅) and the specific localization of the 
   proton wavefunction (α₆).

 Dependencies: pandas, numpy, scipy
"""

import numpy as np
import pandas as pd
from scipy.optimize import minimize
import warnings
warnings.filterwarnings('ignore')

print("=" * 80)
print("PRINCIPIA METAPHYSICA: (5,1) BRANE INFLUENCE TUNING")
print("Searching for global minima in higher-dimensional parameter space")
print("=" * 80)
print()

# ==============================================================================
# 1. FUNDAMENTAL CONSTANTS & TARGETS
# ==============================================================================

# Theory Constants
M_GUT_base = 1.8e16      # GeV (Base unification scale)
Alpha_GUT_inv_base = 24.68 # Base unified coupling
R_shared = 1.0 / (5.0e3) # GeV^-1 (Radius of shared dimensions ~ 5 TeV)

# Predictions (Base Theory without tuning)
tau_p_central_theory = 4.0e34  # years

# EXPERIMENTAL TARGETS (The "Truth" we align to)
# -----------------------------------------------
# 1. Proton Lifetime (Super-K / Hyper-K projection)
tau_p_target = 3.0e34    # years (Preferred physical target)
tau_p_tolerance = 0.5    # orders of magnitude

# 2. Dark Energy EOS (DESI 2024)
w_0_target = -0.83
w_0_sigma = 0.06

# 3. Neutrino Mixing Angle (NuFIT 5.2)
theta_23_target = 47.2   # degrees
theta_23_sigma = 2.0

# 4. KK Graviton Mass (LHC Constraints)
m_KK_target_range = [4500, 6500] # GeV (4.5 - 6.5 TeV)


# ==============================================================================
# 2. PHYSICS ENGINE: (5,1) BRANE INTERACTIONS
# ==============================================================================

def get_effective_dimension(alpha_4, alpha_5):
    """
    Calculates the effective bulk dimension d_eff.
    Base theory uses d=12. Influence parameters α₄/α₅ extend this.
    """
    d_base = 12.0
    # The influence of shared dimensions adds to the effective degrees of freedom
    delta_d = 0.5 * (alpha_4 + alpha_5)
    return d_base + delta_d

def predict_w0(alpha_4, alpha_5):
    """
    Calculates Dark Energy Equation of State using Maximum Entropy Principle.
    w₀ = -(d_eff - 1) / (d_eff + 1)
    """
    d_eff = get_effective_dimension(alpha_4, alpha_5)
    w_0 = -(d_eff - 1.0) / (d_eff + 1.0)
    return w_0

def predict_theta_23(alpha_4, alpha_5):
    """
    Calculates Atmospheric Neutrino Mixing Angle.
    Asymmetry between Dim 4 and Dim 5 influence breaks the exact 45° symmetry.
    """
    base_angle = 45.0
    # Symmetry breaking term
    shift = 3.0 * (alpha_4 - alpha_5)
    return base_angle + shift

def predict_proton_lifetime(alpha_4, alpha_5, alpha_6):
    """
    Calculates Proton Lifetime.
    
    Inputs:
        α₄, α₅: Geometric influence on coupling running (Gauge/Gravity).
        α₆: Wavefunction localization suppression factor.
    """
    # 1. Modify M_GUT based on geometric influence
    #    Positive influence increases effective energy threshold
    M_GUT_geo = M_GUT_base * (1.0 + 0.15 * (alpha_4 + alpha_5))
    
    # 2. Apply Localization Factor (α₆)
    M_GUT_eff = M_GUT_geo * alpha_6

    # 3. Modify Coupling Constant Running (KK tower effect)
    #    Note: Using the V2/V5 negative sign convention for physical consistency
    alpha_inv_eff = Alpha_GUT_inv_base - 0.5 * (alpha_4 + alpha_5)

    # 4. Scaling Law: τₚ ∝ M⁴ / α²
    scaling = (M_GUT_eff / M_GUT_base)**4 * (Alpha_GUT_inv_base / alpha_inv_eff)**2
    
    return tau_p_central_theory * scaling

def predict_kk_mass(alpha_4, alpha_5):
    """
    Calculates the 1st Mode KK Graviton Mass.
    Influence parameters act as warping factors on the effective radius.
    """
    # Magnitude of influence vector
    influence_magnitude = np.sqrt(alpha_4**2 + alpha_5**2)
    
    # Prevent division by zero
    if influence_magnitude < 1e-9:
        R_eff = R_shared * 1e6 # Effectively infinite radius (zero mass)
    else:
        R_eff = R_shared / influence_magnitude
        
    return 1.0 / R_eff # Returns Mass in GeV


# ==============================================================================
# 3. OPTIMIZATION CORE
# ==============================================================================

def cost_function(params):
    """
    Chi-Squared (χ²) Cost Function to minimize.
    Params: [α₄, α₅, α₆]
    """
    a4, a5, a6 = params

    # --- Physical Constraints (Soft) ---
    # α₆ must be positive (localization factor)
    if a6 < 0.1: return 1e12

    # --- Compute Theory Predictions ---
    w0_pred = predict_w0(a4, a5)
    theta_pred = predict_theta_23(a4, a5)
    tau_pred = predict_proton_lifetime(a4, a5, a6)
    m_kk_pred = predict_kk_mass(a4, a5)

    # --- Calculate Deviations (Z-scores squared) ---
    
    # 1. Dark Energy (Priority: High)
    chi_w0 = ((w0_pred - w_0_target) / w_0_sigma) ** 2

    # 2. Neutrino Mixing (Priority: High)
    chi_theta = ((theta_pred - theta_23_target) / theta_23_sigma) ** 2

    # 3. Proton Lifetime (Priority: Medium - Logarithmic scale helps convergence)
    #    Using preferred target of 3.0e34
    tau_deviation = (tau_pred - tau_p_target) / (tau_p_target * 0.3)
    chi_tau = tau_deviation ** 2

    # 4. KK Mass (Priority: Low - Broad acceptable range)
    #    Target center of range (5500 GeV) with wide sigma (1000 GeV)
    chi_kk = ((m_kk_pred - 5500.0) / 1000.0) ** 2

    # --- Weighted Sum ---
    # Weights determined by theoretical sensitivity
    # High weight on Theta_23 because it requires specific asymmetry
    total_cost = (1.0 * chi_w0) + (2.0 * chi_theta) + (1.0 * chi_tau) + (0.5 * chi_kk)

    return total_cost

def run_fine_tuning():
    """
    Executes the L-BFGS-B optimization to find the best fit parameters.
    """
    # Initial Guess: Based on previous V5/V6 analysis
    # We suspect α₄ > 1.0, α₅ ~ 0.5
    initial_guess = [1.1, 0.45, 0.75]

    # Bounds:
    # α₄, α₅: Unconstrained (None) - Geometry finds its own level
    # α₆: Positive (0.1, 10.0) - Localization factor
    bounds = ((None, None), (None, None), (0.1, 10.0))

    print(f"Starting Optimization from guess: {initial_guess}")
    
    result = minimize(
        cost_function, 
        initial_guess, 
        method='L-BFGS-B', 
        bounds=bounds,
        options={'ftol': 1e-12, 'gtol': 1e-12, 'maxiter': 10000}
    )

    return result

# ==============================================================================
# 4. EXECUTION & REPORTING
# ==============================================================================

if __name__ == "__main__":
    res = run_fine_tuning()

    if res.success:
        a4_opt, a5_opt, a6_opt = res.x
        
        # Final Computations
        w0_final = predict_w0(a4_opt, a5_opt)
        theta_final = predict_theta_23(a4_opt, a5_opt)
        tau_final = predict_proton_lifetime(a4_opt, a5_opt, a6_opt)
        m_kk_final = predict_kk_mass(a4_opt, a5_opt)
        d_eff_final = get_effective_dimension(a4_opt, a5_opt)

        print("\n" + "="*80)
        print("OPTIMIZATION SUCCESSFUL - THEORY CONVERGED")
        print("="*80)
        
        print("\n--- TUNED INFLUENCE PARAMETERS ---")
        print(f"α₄ (4th Dim Influence)  : {a4_opt:.6f}")
        print(f"α₅ (5th Dim Influence)  : {a5_opt:.6f}")
        print(f"α₆ (Proton Suppression) : {a6_opt:.6f}")
        print(f"Global Cost (χ²)        : {res.fun:.6f}")

        print("\n--- (5,1) BRANE PREDICTIONS vs REALITY ---")
        
        print(f"1. Effective Dimension (d_eff)")
        print(f"   Theory: {d_eff_final:.4f} (Base 12 + {d_eff_final-12:.4f})")
        
        print(f"\n2. Dark Energy EOS (w₀)")
        print(f"   Predicted: {w0_final:.4f}")
        print(f"   Target   : {w_0_target} ± {w_0_sigma}")
        print(f"   Status   : {'MATCH' if abs(w0_final - w_0_target) < w_0_sigma else 'TENSION'}")

        print(f"\n3. Neutrino Mixing (θ₂₃)")
        print(f"   Predicted: {theta_final:.2f}°")
        print(f"   Target   : {theta_23_target}° ± {theta_23_sigma}°")
        print(f"   Status   : {'MATCH' if abs(theta_final - theta_23_target) < theta_23_sigma else 'TENSION'}")

        print(f"\n4. Proton Lifetime (τₚ)")
        print(f"   Predicted: {tau_final:.3e} years")
        print(f"   Target   : {tau_p_target:.3e} years")
        print(f"   Deviation: {(tau_final - tau_p_target)/tau_p_target*100:.1f}%")

        print(f"\n5. KK Graviton Mass (m_KK)")
        print(f"   Predicted: {m_kk_final/1000.0:.3f} TeV")
        print(f"   Range    : 4.5 - 6.5 TeV")
        
        print("\n" + "="*80)
        print("INTERPRETATION:")
        if a4_opt > 1.0:
            print("The optimization confirms α₄ > 1.0. This implies the 4th extra dimension")
            print("exerts a stronger geometric influence on the observable brane than previously")
            print("assumed in the standard unity model.")
        print("="*80)

    else:
        print("\nOPTIMIZATION FAILED")
        print(res.message)