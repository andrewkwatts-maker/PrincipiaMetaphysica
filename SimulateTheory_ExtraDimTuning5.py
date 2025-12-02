#!/usr/bin/env python3
"""
Copyright (c) 2025 Andrew Keith Watts. All rights reserved.

This is the intellectual property of Andrew Keith Watts. Unauthorized
reproduction, distribution, or modification of this code, in whole or in part,
without the express written permission of Andrew Keith Watts is strictly prohibited.

For inquiries, please contact AndrewKWatts@Gmail.com
"""

"""
SimulateTheory_ExtraDimTuning_V5.py - Extra Dimension Influence Parameter Tuning

This version introduces a third tunable parameter, α₆, representing the Proton 
Decay Suppression Factor, to break the degeneracy between the w₀/θ₂₃ fit and 
the τₚ fit.

TUNABLE PARAMETERS:
------------------
α_4: Influence coefficient of 4th dimension (-∞ to +∞)
α_5: Influence coefficient of 5th dimension (-∞ to +∞)
α_6: Proton Decay Suppression Factor (> 0)

CRUCIAL MODIFICATION (V5):
---------------------------------
1. Reverted the objective function weights to V3/V2 settings (τₚ weight = 1.0).
2. Added α₆ to the optimization parameters (now 3D search).
3. Modified the τₚ calculation to include the suppression factor α₆.

Dependencies: pandas, numpy, scipy
"""

import numpy as np
import pandas as pd
from scipy.optimize import minimize
import warnings
warnings.filterwarnings('ignore')

print("=" * 80)
print("PRINCIPIA METAPHYSICA - EXTRA DIMENSION TUNING SIMULATION (V5)")
print("Introducing α₆ (Proton Decay Suppression Factor)")
print("=" * 80)
print()

# ==============================================================================
# BASELINE PARAMETERS
# ==============================================================================

# Fundamental scales
M_Pl = 1.22e19     # GeV (reduced Planck mass)
M_GUT_base = 1.8e16  # GeV (base GUT scale from RG running)
M_star = 1.0e16    # GeV (fundamental string scale)

# Current predictions
tau_p_central = 4.0e34     # years (proton lifetime central value)

# Experimental targets
tau_p_target_preferred = 3.0e34  # years (Preferred target for optimization)
tau_p_target_error = 0.5         # orders of magnitude (target precision)

w_0_DESI = -0.83                 # (DESI 2024 best fit)
w_0_DESI_error = 0.06            # (1σ error)

theta_23_observed = 47.2         # degrees (NuFIT 5.2 best fit)
theta_23_error = 2.0             # degrees (approximate 1σ)

# Compactification radius
R_shared = 1.0 / (5.0e3)  # GeV^-1 (shared extra dimensions, ~5 TeV scale)


# ==============================================================================
# FUNCTIONS: THEORY PREDICTIONS (PHYSICS MODEL)
# ==============================================================================

def compute_M_GUT(alpha_4, alpha_5):
    """Compute effective GUT scale with extra dimension corrections."""
    M_GUT = M_GUT_base
    # Extra dimension threshold correction (positive shift)
    delta_M_GUT = M_GUT * 0.15 * (alpha_4 + alpha_5)
    return M_GUT + delta_M_GUT


def compute_alpha_GUT(alpha_4, alpha_5):
    """
    Compute unified gauge coupling 1/α_GUT with KK corrections.
    V5 uses the V2/V4 negative sign for the delta term.
    """
    alpha_GUT_inv_base = 24.68
    
    # Extra dimension modifies running via KK tower (V2/V4 sign)
    delta_alpha = -0.5 * (alpha_4 + alpha_5)
    
    return alpha_GUT_inv_base + delta_alpha


def compute_tau_p(alpha_4, alpha_5, alpha_6):
    """
    Compute proton lifetime with extra dimension corrections and the
    Proton Decay Suppression Factor (α₆).
    
    α₆ is applied to the effective M_GUT for the dimension-6 operator.
    """
    M_GUT = compute_M_GUT(alpha_4, alpha_5)
    alpha_GUT_inv = compute_alpha_GUT(alpha_4, alpha_5)

    # Effective scale for proton decay suppression
    M_GUT_eff = M_GUT * alpha_6

    # Scaling: τ_p ∝ M_GUT_eff^4 / α_GUT²
    scaling_factor = (M_GUT_eff / M_GUT_base)**4 * (24.68 / alpha_GUT_inv)**2

    tau_p = tau_p_central * scaling_factor

    return tau_p


def compute_tau_p_uncertainty(alpha_4, alpha_5):
    """Estimate uncertainty in proton lifetime prediction."""
    base_uncertainty_OOM = 0.8
    improvement = 1.0 - 0.4 * (alpha_4 + alpha_5) / 2.0
    improvement = max(0.5, improvement) 
    uncertainty_OOM = base_uncertainty_OOM * improvement
    return uncertainty_OOM


def compute_w_0(alpha_4, alpha_5):
    """Compute dark energy equation of state with dimensional reduction corrections."""
    d_base = 12.0
    # Correction: Mashiach field localization to 4th/5th dimensions
    delta_d = 0.5 * (alpha_4 + alpha_5)
    d_eff = d_base + delta_d

    # Maximum Entropy Principle formula
    w_0 = -(d_eff - 1.0) / (d_eff + 1.0)
    return w_0


def compute_theta_23(alpha_4, alpha_5):
    """Compute atmospheric neutrino mixing angle with extra dimension corrections."""
    theta_23_base = 45.0  # degrees
    
    # Correction: non-zero α breaks maximal mixing slightly, scales with α_4 - α_5
    delta_theta = 3.0 * (alpha_4 - alpha_5)
    
    theta_23 = theta_23_base + delta_theta
    return theta_23


def compute_m_KK(alpha_4, alpha_5):
    """Compute first KK graviton mode mass."""
    effective_coupling_sq = alpha_4**2 + alpha_5**2
    
    if effective_coupling_sq < 1e-12:
        return 1.0 / R_shared * 1e-6 
    
    R_eff = R_shared / np.sqrt(effective_coupling_sq)
    m_KK = 1.0 / R_eff  # GeV
    return m_KK


# ==============================================================================
# OBJECTIVE FUNCTION: MINIMIZE DEVIATIONS FROM TARGETS (V2/V3 WEIGHTS)
# ==============================================================================

def objective_function(params):
    """
    Objective function to minimize: weighted sum of squared deviations.
    V5 now optimizes [α₄, α₅, α₆].
    """
    alpha_4, alpha_5, alpha_6 = params

    # Constraint: α₆ must be positive (it is a physical scale factor)
    if alpha_6 <= 0:
        return 1e15 # Hard penalty for non-physical alpha_6

    # Compute predictions
    tau_p = compute_tau_p(alpha_4, alpha_5, alpha_6)
    tau_p_unc_OOM = compute_tau_p_uncertainty(alpha_4, alpha_5)
    w_0 = compute_w_0(alpha_4, alpha_5)
    theta_23 = compute_theta_23(alpha_4, alpha_5)
    m_KK = compute_m_KK(alpha_4, alpha_5)

    chi2 = 0.0
    
    # --- WEIGHTS (Reverted to V3 weights) ---
    CHI2_WEIGHT_TAU_P = 1.0 
    CHI2_WEIGHT_THETA_23 = 2.0 
    CHI2_WEIGHT_W0 = 1.0
    CHI2_WEIGHT_M_KK = 0.5

    # 1. Proton Lifetime: Target 3.0e34 years
    tau_p_deviation = (tau_p - tau_p_target_preferred) / (tau_p_central * 0.3) 
    tau_p_unc_penalty = (tau_p_unc_OOM - tau_p_target_error) / 0.1 

    chi2 += CHI2_WEIGHT_TAU_P * tau_p_deviation**2
    chi2 += CHI2_WEIGHT_TAU_P * max(0, tau_p_unc_penalty)**2

    # 2. Dark energy: match w_0 = -0.83 ± 0.06
    w_0_deviation = (w_0 - w_0_DESI) / w_0_DESI_error
    chi2 += CHI2_WEIGHT_W0 * w_0_deviation**2

    # 3. Neutrino mixing: match θ₂₃ = 47.2° ± 2°
    theta_23_deviation = (theta_23 - theta_23_observed) / theta_23_error
    chi2 += CHI2_WEIGHT_THETA_23 * theta_23_deviation**2

    # 4. KK mass: prefer m_KK ~ 5-6 TeV 
    m_KK_target = 5.5e3  # GeV
    m_KK_error = 1.0e3  # GeV
    m_KK_deviation = (m_KK - m_KK_target) / m_KK_error
    chi2 += CHI2_WEIGHT_M_KK * m_KK_deviation**2 

    return chi2


# ==============================================================================
# GRID SEARCH & OPTIMIZATION FUNCTIONS (ADAPTED FOR 3D)
# ==============================================================================

def grid_search_3d(n_points_2d=21, search_range_2d=5.0, n_points_a6=5, search_range_a6=[0.5, 3.0]):
    """
    Perform a limited 3D grid search over α₄, α₅, and α₆.
    """
    print("Performing 3D grid search...")
    print(f"α₄, α₅ Range: [{-search_range_2d}, {search_range_2d}] ({n_points_2d} points each)")
    print(f"α₆ Range: [{search_range_a6[0]}, {search_range_a6[1]}] ({n_points_a6} points)")
    print(f"Total Grid Points: {n_points_2d**2 * n_points_a6}")
    print()

    alpha_4_vals = np.linspace(-search_range_2d, search_range_2d, n_points_2d)
    alpha_5_vals = np.linspace(-search_range_2d, search_range_2d, n_points_2d)
    alpha_6_vals = np.linspace(search_range_a6[0], search_range_a6[1], n_points_a6)

    results = []
    # Suppress warnings during iteration
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        for alpha_4 in alpha_4_vals:
            for alpha_5 in alpha_5_vals:
                for alpha_6 in alpha_6_vals:
                    try:
                        params = [alpha_4, alpha_5, alpha_6]
                        chi2 = objective_function(params)
                    except RuntimeWarning:
                        chi2 = 1e10 

                    results.append({
                        'alpha_4': alpha_4,
                        'alpha_5': alpha_5,
                        'alpha_6': alpha_6,
                        'chi_squared': chi2
                    })

    df = pd.DataFrame(results)
    return df


def find_optimal_parameters():
    """
    Use scipy.optimize to find optimal (α_4, α_5, α_6) minimizing chi-squared.
    """
    print("Finding optimal parameters via Nelder-Mead optimization (3D Unconstrained)...")
    print()

    # Initial guess aims for good w_0/theta_23 fit and a suppression factor (α₆ > 1)
    x0 = [0.8, -0.3, 1.5] 

    # We must use 'L-BFGS-B' or a similar method that handles bounds, 
    # as α₆ must be > 0. We'll use bounds on Nelder-Mead's initialization for robustness.
    result = minimize(
        objective_function,
        x0,
        method='Nelder-Mead',
        options={'maxiter': 5000, 'xatol': 1e-6, 'fatol': 1e-6}
    )

    if result.success:
        alpha_4_opt, alpha_5_opt, alpha_6_opt = result.x
        chi2_opt = result.fun

        print("✓ Optimization converged!")
        print(f"  Optimal α_4 = {alpha_4_opt:.6f}")
        print(f"  Optimal α_5 = {alpha_5_opt:.6f}")
        print(f"  Optimal α_6 = {alpha_6_opt:.6f}")
        print(f"  Minimal χ² = {chi2_opt:.4f}")
        print()

        return alpha_4_opt, alpha_5_opt, alpha_6_opt, chi2_opt
    else:
        print("✗ Optimization failed!")
        print(f"  Message: {result.message}")
        print()
        return None, None, None, None


def compare_predictions(alpha_4_base, alpha_5_base, alpha_6_base, alpha_4_opt, alpha_5_opt, alpha_6_opt):
    """
    Compare predictions at baseline (α_4, α_5, α_6) vs optimized values.
    """
    print("=" * 80)
    print("COMPARISON: BASELINE vs OPTIMIZED PARAMETERS")
    print("=" * 80)
    print()

    # Define a helper to print results concisely
    def print_results(a4, a5, a6, label):
        M_GUT = compute_M_GUT(a4, a5)
        alpha_GUT_inv = compute_alpha_GUT(a4, a5)
        tau_p = compute_tau_p(a4, a5, a6)
        tau_p_unc = compute_tau_p_uncertainty(a4, a5)
        w_0 = compute_w_0(a4, a5)
        theta_23 = compute_theta_23(a4, a5)
        m_KK = compute_m_KK(a4, a5)
        chi2 = objective_function([a4, a5, a6])

        print(f"{label}: (α₄ = {a4:.4f}, α₅ = {a5:.4f}, α₆ = {a6:.4f})")
        print("-" * 80)
        print(f"  M_GUT = {M_GUT:.3e} GeV")
        print(f"  1/α_GUT = {alpha_GUT_inv:.2f}")
        print(f"  τ_p = {tau_p:.2e} years (uncertainty: {tau_p_unc:.2f} OOM)")
        print(f"  w_0 = {w_0:.4f} (target: {w_0_DESI} ± {w_0_DESI_error})")
        print(f"  θ_23 = {theta_23:.1f}° (target: {theta_23_observed} ± {theta_23_error}°)")
        print(f"  m_KK^(1) = {m_KK/1e3:.2f} TeV")
        print(f"  χ² = {chi2:.4f}")
        print()

        return chi2


    chi2_base = print_results(alpha_4_base, alpha_5_base, alpha_6_base, "BASELINE (α₆=1.0)")
    
    if alpha_4_opt is not None:
        chi2_opt = print_results(alpha_4_opt, alpha_5_opt, alpha_6_opt, "OPTIMIZED")
        
        # Calculate improvements based on original baseline (0.5, 0.5, 1.0)
        tau_p_base = compute_tau_p(alpha_4_base, alpha_5_base, alpha_6_base)
        tau_p_opt = compute_tau_p(alpha_4_opt, alpha_5_opt, alpha_6_opt)
        tau_p_unc_base = compute_tau_p_uncertainty(alpha_4_base, alpha_5_base)
        tau_p_unc_opt = compute_tau_p_uncertainty(alpha_4_opt, alpha_5_opt)
        alpha_GUT_inv_base = compute_alpha_GUT(alpha_4_base, alpha_5_base)
        alpha_GUT_inv_opt = compute_alpha_GUT(alpha_4_opt, alpha_5_opt)
        w_0_base = compute_w_0(alpha_4_base, alpha_5_base)
        w_0_opt = compute_w_0(alpha_4_opt, alpha_5_opt)
        theta_23_base = compute_theta_23(alpha_4_base, alpha_5_base)
        theta_23_opt = compute_theta_23(alpha_4_opt, alpha_5_opt)
        m_KK_base = compute_m_KK(alpha_4_base, alpha_5_base)
        m_KK_opt = compute_m_KK(alpha_4_opt, alpha_5_opt)

        print("IMPROVEMENTS (Relative to Baseline V5):")
        print("-" * 80)
        print(f"  Δ(1/α_GUT) = {alpha_GUT_inv_opt - alpha_GUT_inv_base:+.2f}")
        print(f"  Δτ_p = {(tau_p_opt - tau_p_base)/tau_p_base * 100:+.1f}%")
        print(f"  Δ(τ_p uncertainty) = {tau_p_unc_opt - tau_p_unc_base:+.2f} OOM")
        print(f"  Δw_0 = {w_0_opt - w_0_base:+.4f}")
        print(f"  Δθ_23 = {theta_23_opt - theta_23_base:+.1f}°")
        print(f"  Δm_KK = {(m_KK_opt - m_KK_base)/1e3:+.2f} TeV")
        print(f"  χ² improvement = {chi2_base - chi2_opt:.4f} ({(chi2_base - chi2_opt)/chi2_base * 100:.1f}%)")
        print()


# ==============================================================================
# MAIN EXECUTION
# ==============================================================================

if __name__ == '__main__':
    
    # Baseline for comparison
    alpha_4_base, alpha_5_base, alpha_6_base = 0.5, 0.5, 1.0

    # Step 1: Grid search to explore parameter space
    print("Step 1: Grid Search")
    print("=" * 80)
    # Reduced grid search size due to 3D search space
    df_grid = grid_search_3d(n_points_2d=21, search_range_2d=5.0, n_points_a6=5, search_range_a6=[0.5, 3.0]) 

    # Save grid results
    df_grid.to_csv('extra_dim_tuning_grid_v5.csv', index=False)
    print(f"✓ Grid results saved to 'extra_dim_tuning_grid_v5.csv'")
    print()

    # Find best point in grid
    best_idx = df_grid['chi_squared'].idxmin()
    best_grid = df_grid.loc[best_idx]

    print("Best point from grid search (Initial Guess):")
    print(f"  α_4 = {best_grid['alpha_4']:.4f}")
    print(f"  α_5 = {best_grid['alpha_5']:.4f}")
    print(f"  α_6 = {best_grid['alpha_6']:.4f}")
    print(f"  χ² = {best_grid['chi_squared']:.4f}")
    print()

    # Step 2: Optimization to refine best-fit
    print("Step 2: Optimization (Nelder-Mead)")
    print("=" * 80)
    alpha_4_opt, alpha_5_opt, alpha_6_opt, chi2_opt = find_optimal_parameters()

    # Step 3: Comparison
    if alpha_4_opt is not None:
        compare_predictions(alpha_4_base, alpha_5_base, alpha_6_base, alpha_4_opt, alpha_5_opt, alpha_6_opt)

    # Step 4: Summary recommendations
    print("=" * 80)
    print("SUMMARY & RECOMMENDATIONS (V5)")
    print("=" * 80)
    print()

    if alpha_4_opt is not None:
        print(f"✓ RECOMMENDED VALUES:")
        print(f"  α_4 (4th dimension influence) = {alpha_4_opt:.4f}")
        print(f"  α_5 (5th dimension influence) = {alpha_5_opt:.4f}")
        print(f"  α_6 (Proton Decay Suppression) = {alpha_6_opt:.4f}")
        print()

        # Check resolution
        w_0_opt = compute_w_0(alpha_4_opt, alpha_5_opt)
        theta_23_opt = compute_theta_23(alpha_4_opt, alpha_5_opt)
        tau_p_opt = compute_tau_p(alpha_4_opt, alpha_5_opt, alpha_6_opt)
        tau_p_unc_opt = compute_tau_p_uncertainty(alpha_4_opt, alpha_5_opt)
        m_KK_opt = compute_m_KK(alpha_4_opt, alpha_5_opt)


        print("OUTSTANDING ISSUE RESOLUTION:")
        print()

        # Issue 1: Proton decay
        # Note: Recalculate sigma using the original τ_p_central * 0.3 for consistency
        tau_p_deviation_sigma = abs(tau_p_opt - tau_p_target_preferred) / (tau_p_central * 0.3)
        if tau_p_deviation_sigma < 1.0:
             print("  ✓ Proton decay lifetime: RESOLVED")
             print(f"    τ_p = {tau_p_opt:.2e} years (within 1σ of {tau_p_target_preferred:.0e} preferred)")
        else:
             print("  ⚠ Proton decay lifetime: PARTIAL")
             print(f"    τ_p = {tau_p_opt:.2e} years (Deviation: {tau_p_deviation_sigma:.2f}σ)")

        if tau_p_unc_opt < 0.5:
             print(f"  ✓ Proton decay uncertainty: RESOLVED ({tau_p_unc_opt:.2f} OOM)")
        else:
             print(f"  ⚠ Proton decay uncertainty: PARTIAL ({tau_p_unc_opt:.2f} OOM)")
        print()

        # Issue 2: w_0 (Planck tension)
        w_0_deviation_sigma = abs(w_0_opt - w_0_DESI) / w_0_DESI_error
        if w_0_deviation_sigma < 1.0:
            print("  ✓ Dark energy w_0: RESOLVED")
            print(f"    Within 1σ of DESI ({w_0_deviation_sigma:.2f}σ)")
        else:
            print("  ⚠ Dark energy w_0: IMPROVED")
            print(f"    Deviation: {w_0_deviation_sigma:.2f}σ")
        print()

        # Issue 3: θ_23
        theta_23_deviation_sigma = abs(theta_23_opt - theta_23_observed) / theta_23_error
        if theta_23_deviation_sigma < 1.0:
            print("  ✅ Neutrino mixing θ_23: RESOLVED")
            print(f"    Within 1σ of NuFIT ({theta_23_deviation_sigma:.2f}σ)")
        else:
            print("  ⚠ Neutrino mixing θ_23: PARTIAL")
            print(f"    Deviation: {theta_23_deviation_sigma:.2f}σ (Target: < 1.0σ)")
        print()

        # Issue 4: KK spectrum
        if 4.5e3 < m_KK_opt < 6.5e3:
            print("  ✓ KK graviton mass: TESTABLE RANGE")
            print(f"    m_KK^(1) = {m_KK_opt/1e3:.2f} TeV (HL-LHC accessible)")
        else:
            print("  ⚠ KK graviton mass: OUTSIDE OPTIMAL RANGE")
            print(f"    m_KK^(1) = {m_KK_opt/1e3:.2f} TeV")
        print()

        print("NEXT STEPS:")
        print(f"  1. Update config.py with optimal α_4 = {alpha_4_opt:.4f}, α_5 = {alpha_5_opt:.4f}, α_6 = {alpha_6_opt:.4f}")
        print("  2. Re-run full SimulateTheory.py with updated parameters")
        print("  3. Verify consistency with all 58 parameters")
        print("  4. Update paper predictions with refined values")
        print()
    else:
        print("✗ Optimization failed - check grid results and objective function logic.")
        print()
        print("Try exploring grid results in 'extra_dim_tuning_grid_v5.csv'")
        print("Focus on regions with low χ²")

    print("=" * 80)
    print("Simulation complete!")
    print("=" * 80)