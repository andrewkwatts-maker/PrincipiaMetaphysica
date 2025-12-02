#!/usr/bin/env python3
"""
Copyright (c) 2025 Andrew Keith Watts. All rights reserved.

This is the intellectual property of Andrew Keith Watts. Unauthorized
reproduction, distribution, or modification of this code, in whole or in part,
without the express written permission of Andrew Keith Watts is strictly prohibited.

For inquiries, please contact AndrewKWatts@Gmail.com
"""

"""
SimulateTheory_ExtraDimTuning_V2.py - Extra Dimension Influence Parameter Tuning

This script explores how varying the influence of the 4th and 5th shared extra dimensions
in the (5,1) observable brane affects the outstanding prediction issues.

TUNABLE PARAMETERS:
------------------
α_4: Influence coefficient of 4th dimension (-∞ to +∞)
α_5: Influence coefficient of 5th dimension (-∞ to +∞)

MODIFICATIONS FROM V1:
--------------------
1. Optimization bounds removed (unconstrained search).
2. Weight for theta_23 objective increased to 2.0 to resolve tension.
3. Grid search range widened to [-10, 10].

Dependencies: pandas, sympy, numpy, scipy
"""

import numpy as np
import pandas as pd
from scipy.optimize import minimize, newton
from sympy import symbols, sqrt, N, pi, log, exp
import warnings
warnings.filterwarnings('ignore')

# Note: Assuming config import is working for compilation
# from config import (
#     FundamentalConstants as FC,
#     PhenomenologyParameters as PP,
#     RealWorldData as RWD
# )

print("=" * 80)
print("PRINCIPIA METAPHYSICA - EXTRA DIMENSION TUNING SIMULATION (V2)")
print("Unconstrained exploration with enhanced θ₂₃ weighting")
print("=" * 80)
print()

# ==============================================================================
# BASELINE PARAMETERS (from config.py and current theory)
# ==============================================================================

# Fundamental scales
M_Pl = 1.22e19     # GeV (reduced Planck mass)
M_GUT_base = 1.8e16  # GeV (base GUT scale from RG running)
M_star = 1.0e16    # GeV (fundamental string scale)

# Current predictions (from OUTSTANDING_ISSUES_REPORT.md)
tau_p_central = 4.0e34     # years (proton lifetime central value)
w_0_prediction = -11.0/13.0  # ≈ -0.846 (dark energy EOS at z=0)
theta_23_prediction = 45.0  # degrees (maximal mixing from SO(10))

# Experimental targets
# Note: tau_p_target is the experimental lower bound, not the preferred prediction
tau_p_target = 2.4e34     # years (Super-K lower bound)
tau_p_target_error = 0.5  # orders of magnitude (target precision)

w_0_DESI = -0.83     # (DESI 2024 best fit)
w_0_DESI_error = 0.06  # (1σ error)

theta_23_observed = 47.2  # degrees (NuFIT 5.2 best fit)
theta_23_error = 2.0    # degrees (approximate 1σ)

m_KK_LHC_limit = 3.5e3   # GeV (current LHC exclusion)

# Compactification radius and volume
R_shared = 1.0 / (5.0e3)  # GeV^-1 (shared extra dimensions, ~5 TeV scale)
V_7 = (2 * pi * R_shared)**2  # Volume of 2 shared extra dimensions

# ==============================================================================
# FUNCTIONS: THEORY PREDICTIONS AS FUNCTION OF (α_4, α_5)
# (NO CHANGES TO PHYSICS LOGIC)
# ==============================================================================

def compute_M_GUT(alpha_4, alpha_5):
    """Compute effective GUT scale with extra dimension corrections."""
    M_GUT = M_GUT_base
    # Extra dimension threshold correction (positive shift)
    delta_M_GUT = M_GUT * 0.15 * (alpha_4 + alpha_5)
    return M_GUT + delta_M_GUT


def compute_alpha_GUT(alpha_4, alpha_5):
    """Compute unified gauge coupling 1/α_GUT with KK corrections."""
    alpha_GUT_inv_base = 24.68
    # Extra dimension modifies running via KK tower (reduces 1/α_GUT)
    delta_alpha = -0.5 * (alpha_4 + alpha_5)
    return alpha_GUT_inv_base + delta_alpha


def compute_tau_p(alpha_4, alpha_5):
    """Compute proton lifetime with extra dimension corrections."""
    M_GUT = compute_M_GUT(alpha_4, alpha_5)
    alpha_GUT_inv = compute_alpha_GUT(alpha_4, alpha_5)

    # Scaling: τ_p ∝ M_GUT^4 / α_GUT²
    scaling_factor = (M_GUT / M_GUT_base)**4 * (24.68 / alpha_GUT_inv)**2

    tau_p = tau_p_central * scaling_factor

    return tau_p


def compute_tau_p_uncertainty(alpha_4, alpha_5):
    """Estimate uncertainty in proton lifetime prediction."""
    # Base uncertainty (0.8 orders of magnitude)
    base_uncertainty_OOM = 0.8

    # Improvement factor: extra dimensions constrain M_GUT
    # Full coupling (α_4 + α_5 = 2) reduces uncertainty by 40%
    improvement = 1.0 - 0.4 * (alpha_4 + alpha_5) / 2.0
    
    # Ensure uncertainty is not negative in unconstrained search
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
    # Effective inverse radius: R_eff = R_shared / sqrt(α_4² + α_5²)
    effective_coupling_sq = alpha_4**2 + alpha_5**2
    
    # Handle the case where coupling is near zero
    if effective_coupling_sq < 1e-12:
        return 1.0 / R_shared * 1e-6 # Return a very small mass (near zero TeV)
    
    R_eff = R_shared / np.sqrt(effective_coupling_sq)
    
    m_KK = 1.0 / R_eff  # GeV

    return m_KK


# ==============================================================================
# OBJECTIVE FUNCTION: MINIMIZE DEVIATIONS FROM TARGETS (WEIGHTING MODIFIED)
# ==============================================================================

def objective_function(params):
    """
    Objective function to minimize: weighted sum of squared deviations.
    
    MODIFICATION: θ₂₃ penalty weight increased to 2.0.
    """
    alpha_4, alpha_5 = params

    # Compute predictions
    tau_p = compute_tau_p(alpha_4, alpha_5)
    tau_p_unc_OOM = compute_tau_p_uncertainty(alpha_4, alpha_5)
    w_0 = compute_w_0(alpha_4, alpha_5)
    theta_23 = compute_theta_23(alpha_4, alpha_5)
    m_KK = compute_m_KK(alpha_4, alpha_5)

    chi2 = 0.0

    # We want tau_p to be near the experimental target/base, let's target 3.0e34
    tau_p_target_preferred = 3.0e34
    tau_p_deviation = (tau_p - tau_p_target_preferred) / (tau_p_central * 0.3)
    tau_p_unc_penalty = (tau_p_unc_OOM - tau_p_target_error) / 0.1

    chi2 += tau_p_deviation**2
    chi2 += max(0, tau_p_unc_penalty)**2

    # 2. Dark energy: match DESI w_0 = -0.83 ± 0.06
    w_0_deviation = (w_0 - w_0_DESI) / w_0_DESI_error
    chi2 += w_0_deviation**2

    # 3. Neutrino mixing: match θ₂₃ = 47.2° ± 2°
    theta_23_deviation = (theta_23 - theta_23_observed) / theta_23_error
    
    # Increased weight for Neutrino Mixing to enforce better fit
    CHI2_WEIGHT_THETA_23 = 2.0
    chi2 += CHI2_WEIGHT_THETA_23 * theta_23_deviation**2

    # 4. KK mass: prefer m_KK ~ 5-6 TeV (testable, not excluded)
    m_KK_target = 5.5e3  # GeV (mid-range)
    m_KK_error = 1.0e3  # GeV (allow ±1 TeV variation)
    m_KK_deviation = (m_KK - m_KK_target) / m_KK_error
    chi2 += 0.5 * m_KK_deviation**2  # half weight

    return chi2


# ==============================================================================
# GRID SEARCH: EXPLORE PARAMETER SPACE (RANGE WIDENED)
# ==============================================================================

def grid_search(n_points=21, search_range=10.0):
    """
    Perform grid search over α_4, α_5 ∈ [-search_range, search_range].
    """
    print("Performing grid search...")
    print(f"Grid Range: [{-search_range}, {search_range}]")
    print(f"Grid: {n_points} × {n_points} = {n_points**2} points")
    print()

    alpha_4_vals = np.linspace(-search_range, search_range, n_points)
    alpha_5_vals = np.linspace(-search_range, search_range, n_points)

    results = []

    for i, alpha_4 in enumerate(alpha_4_vals):
        for j, alpha_5 in enumerate(alpha_5_vals):
            # Compute chi-squared
            try:
                chi2 = objective_function([alpha_4, alpha_5])
            except RuntimeWarning:
                chi2 = 1e10 # Penalize numerical instability

            # Store results
            results.append({
                'alpha_4': alpha_4,
                'alpha_5': alpha_5,
                'alpha_sum': alpha_4 + alpha_5,
                'alpha_diff': alpha_4 - alpha_5,
                'tau_p_years': compute_tau_p(alpha_4, alpha_5),
                'w_0': compute_w_0(alpha_4, alpha_5),
                'theta_23_deg': compute_theta_23(alpha_4, alpha_5),
                'm_KK_TeV': compute_m_KK(alpha_4, alpha_5) / 1e3,
                'chi_squared': chi2
            })

    df = pd.DataFrame(results)
    return df


# ==============================================================================
# OPTIMIZATION: FIND BEST-FIT (α_4, α_5) (BOUNDS REMOVED)
# ==============================================================================

def find_optimal_parameters():
    """
    Use scipy.optimize to find optimal (α_4, α_5) minimizing chi-squared.
    
    Method: Nelder-Mead simplex (unconstrained).
    """
    print("Finding optimal parameters via Nelder-Mead optimization (Unconstrained)...")
    print()

    # Initial guess
    x0 = [0.5, 0.5] # Start near the origin

    # Optimize - Bounds are removed
    result = minimize(
        objective_function,
        x0,
        method='Nelder-Mead',
        options={'maxiter': 1000, 'xatol': 1e-6, 'fatol': 1e-6}
    )

    if result.success:
        alpha_4_opt, alpha_5_opt = result.x
        chi2_opt = result.fun

        print("✓ Optimization converged!")
        print(f"  Optimal α_4 = {alpha_4_opt:.6f}")
        print(f"  Optimal α_5 = {alpha_5_opt:.6f}")
        print(f"  Minimal χ² = {chi2_opt:.4f}")
        print()

        return alpha_4_opt, alpha_5_opt, chi2_opt
    else:
        print("✗ Optimization failed!")
        print(f"  Message: {result.message}")
        print()
        return None, None, None


# ==============================================================================
# ANALYSIS: COMPARE BASELINE VS OPTIMIZED
# ==============================================================================

def compare_predictions(alpha_4_base, alpha_5_base, alpha_4_opt, alpha_5_opt):
    """
    Compare predictions at baseline (α_4, α_5) vs optimized values.
    """
    print("=" * 80)
    print("COMPARISON: BASELINE vs OPTIMIZED PARAMETERS")
    print("=" * 80)
    print()

    # Baseline predictions
    print("BASELINE (α_4 = 0.5, α_5 = 0.5):")
    print("-" * 80)

    M_GUT_base = compute_M_GUT(alpha_4_base, alpha_5_base)
    alpha_GUT_inv_base = compute_alpha_GUT(alpha_4_base, alpha_5_base)
    tau_p_base = compute_tau_p(alpha_4_base, alpha_5_base)
    tau_p_unc_base = compute_tau_p_uncertainty(alpha_4_base, alpha_5_base)
    w_0_base = compute_w_0(alpha_4_base, alpha_5_base)
    theta_23_base = compute_theta_23(alpha_4_base, alpha_5_base)
    m_KK_base = compute_m_KK(alpha_4_base, alpha_5_base)
    chi2_base = objective_function([alpha_4_base, alpha_5_base])

    print(f"  M_GUT = {M_GUT_base:.3e} GeV")
    print(f"  1/α_GUT = {alpha_GUT_inv_base:.2f}")
    print(f"  τ_p = {tau_p_base:.2e} years (uncertainty: {tau_p_unc_base:.2f} OOM)")
    print(f"  w_0 = {w_0_base:.4f} (target: {w_0_DESI} ± {w_0_DESI_error})")
    print(f"  θ_23 = {theta_23_base:.1f}° (target: {theta_23_observed} ± {theta_23_error}°)")
    print(f"  m_KK^(1) = {m_KK_base/1e3:.2f} TeV")
    print(f"  χ² = {chi2_base:.4f}")
    print()

    # Optimized predictions
    if alpha_4_opt is not None:
        print(f"OPTIMIZED (α_4 = {alpha_4_opt:.4f}, α_5 = {alpha_5_opt:.4f}):")
        print("-" * 80)

        M_GUT_opt = compute_M_GUT(alpha_4_opt, alpha_5_opt)
        alpha_GUT_inv_opt = compute_alpha_GUT(alpha_4_opt, alpha_5_opt)
        tau_p_opt = compute_tau_p(alpha_4_opt, alpha_5_opt)
        tau_p_unc_opt = compute_tau_p_uncertainty(alpha_4_opt, alpha_5_opt)
        w_0_opt = compute_w_0(alpha_4_opt, alpha_5_opt)
        theta_23_opt = compute_theta_23(alpha_4_opt, alpha_5_opt)
        m_KK_opt = compute_m_KK(alpha_4_opt, alpha_5_opt)
        chi2_opt = objective_function([alpha_4_opt, alpha_5_opt])

        print(f"  M_GUT = {M_GUT_opt:.3e} GeV")
        print(f"  1/α_GUT = {alpha_GUT_inv_opt:.2f}")
        print(f"  τ_p = {tau_p_opt:.2e} years (uncertainty: {tau_p_unc_opt:.2f} OOM)")
        print(f"  w_0 = {w_0_opt:.4f} (target: {w_0_DESI} ± {w_0_DESI_error})")
        print(f"  θ_23 = {theta_23_opt:.1f}° (target: {theta_23_observed} ± {theta_23_error}°)")
        print(f"  m_KK^(1) = {m_KK_opt/1e3:.2f} TeV")
        print(f"  χ² = {chi2_opt:.4f}")
        print()

        # Improvements
        print("IMPROVEMENTS:")
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

    # Step 1: Grid search to explore parameter space
    print("Step 1: Grid Search")
    print("=" * 80)
    df_grid = grid_search(n_points=41, search_range=10.0) # Increased points for better sampling

    # Save grid results
    df_grid.to_csv('extra_dim_tuning_grid_v2.csv', index=False)
    print(f"✓ Grid results saved to 'extra_dim_tuning_grid_v2.csv'")
    print()

    # Find best point in grid
    best_idx = df_grid['chi_squared'].idxmin()
    best_grid = df_grid.loc[best_idx]

    print("Best point from grid search:")
    print(f"  α_4 = {best_grid['alpha_4']:.4f}")
    print(f"  α_5 = {best_grid['alpha_5']:.4f}")
    print(f"  χ² = {best_grid['chi_squared']:.4f}")
    print()

    # Step 2: Optimization to refine best-fit
    print("Step 2: Optimization (Nelder-Mead)")
    print("=" * 80)
    alpha_4_opt, alpha_5_opt, chi2_opt = find_optimal_parameters()

    # Step 3: Comparison
    if alpha_4_opt is not None:
        compare_predictions(0.5, 0.5, alpha_4_opt, alpha_5_opt)

    # Step 4: Summary recommendations
    print("=" * 80)
    print("SUMMARY & RECOMMENDATIONS (V2)")
    print("=" * 80)
    print()

    if alpha_4_opt is not None:
        print(f"✓ RECOMMENDED VALUES:")
        print(f"  α_4 (4th dimension influence) = {alpha_4_opt:.4f}")
        print(f"  α_5 (5th dimension influence) = {alpha_5_opt:.4f}")
        print()

        # Check which predictions improved
        w_0_opt = compute_w_0(alpha_4_opt, alpha_5_opt)
        theta_23_opt = compute_theta_23(alpha_4_opt, alpha_5_opt)
        tau_p_unc_opt = compute_tau_p_uncertainty(alpha_4_opt, alpha_5_opt)
        m_KK_opt = compute_m_KK(alpha_4_opt, alpha_5_opt)


        print("OUTSTANDING ISSUE RESOLUTION:")
        print()

        # Issue 1: Proton decay
        tau_p_opt = compute_tau_p(alpha_4_opt, alpha_5_opt)
        tau_p_deviation_sigma = abs(tau_p_opt - 3.0e34) / (0.3 * 4.0e34) # Approximate sigma
        if tau_p_deviation_sigma < 1.0:
             print("  ✓ Proton decay lifetime: RESOLVED")
             print(f"    τ_p = {tau_p_opt:.2e} years (within 1σ of 3.0e34 preferred)")
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
        print(f"  1. Update config.py with optimal α_4 = {alpha_4_opt:.4f}, α_5 = {alpha_5_opt:.4f}")
        print("  2. Re-run full SimulateTheory.py with updated parameters")
        print("  3. Verify consistency with all 58 parameters")
        print("  4. Update paper predictions with refined values")
        print()
    else:
        print("✗ Optimization failed - check grid results and objective function logic.")
        print()
        print("Try exploring grid results in 'extra_dim_tuning_grid_v2.csv'")
        print("Focus on regions with low χ²")

    print("=" * 80)
    print("Simulation complete!")
    print("=" * 80)