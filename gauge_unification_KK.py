"""
gauge_unification_KK.py - Gauge Coupling Unification via Kaluza-Klein Tower

Implements gauge coupling unification mechanism through extra-dimensional
Kaluza-Klein mode contributions, bypassing the need for SUSY.

Framework: Principia Metaphysica v6.1
Author: Claude (Agent Implementation)
Date: 2025-11-27

Reference: ISSUE2_EXTRADIM_SOLUTION.md

Physical Mechanism:
    - Below M_c: Standard 4D RG running (logarithmic)
    - Above M_c: KK tower activates, power-law corrections dominate
    - Differential localization allows α₁, α₂, α₃ to unify at M_GUT

Key Equations:
    dα_i⁻¹/d ln μ = -b_i^{eff}(μ) / (2π)
    b_i^{eff}(μ) = b_i^{4D} + ε_i × N_KK(μ) × Δb_KK

where:
    - ε_i: Localization parameter (0 = brane, 1 = bulk)
    - N_KK(μ): Number of active KK modes ~ μ/M_c
    - Δb_KK: Beta correction per KK mode
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
from scipy.optimize import minimize, differential_evolution
from typing import Dict, Tuple, List, Callable
import sys

# ==============================================================================
# PHYSICAL CONSTANTS
# ==============================================================================

class PhysicsConstants:
    """Energy scales and gauge couplings"""

    # Energy scales (GeV)
    M_PLANCK = 1.2195e19        # Reduced Planck mass
    M_GUT_TARGET = 1.8e16       # SO(10) GUT scale (target)
    M_KK = 5.0e3                # KK compactification scale (5 TeV)
    M_Z = 91.1876               # Z boson mass

    # Gauge couplings at M_Z (PDG 2024)
    # α_i = g_i² / (4π)
    ALPHA_1_INV_MZ = 59.0       # U(1)_Y (GUT normalized)
    ALPHA_2_INV_MZ = 29.6       # SU(2)_L
    ALPHA_3_INV_MZ = 8.5        # SU(3)_c

    # Target unification value (MSSM-like)
    ALPHA_GUT_INV_TARGET = 24.0

    # SM beta coefficients (one-loop)
    # dα_i⁻¹/dt = -b_i/(2π), t = ln(μ/M_Z)
    B_1_SM = 41/10              # U(1)_Y
    B_2_SM = -19/6              # SU(2)_L
    B_3_SM = -7                 # SU(3)_c

    # KK contribution per mode (group theory factors)
    # For adjoint representation gauge bosons
    DELTA_B_KK = 2/3            # Standard normalization


# ==============================================================================
# KK TOWER SPECTRUM
# ==============================================================================

def kk_tower_masses(n_max: int, M_c: float = PhysicsConstants.M_KK) -> np.ndarray:
    """
    Generate KK mode mass spectrum.

    For a single compactified dimension (S¹ of radius R = 1/M_c):
        m_n = n × M_c,  n = 1, 2, 3, ..., n_max

    Args:
        n_max: Maximum KK level (cutoff)
        M_c: Compactification scale (GeV)

    Returns:
        Array of KK masses [GeV]
    """
    n_values = np.arange(1, n_max + 1)
    return n_values * M_c


def n_active_modes(mu: float, M_c: float = PhysicsConstants.M_KK) -> int:
    """
    Number of KK modes active at energy scale μ.

    Modes with m_n < μ contribute to RG running.

    Args:
        mu: Energy scale (GeV)
        M_c: Compactification scale (GeV)

    Returns:
        N_active = floor(μ / M_c)
    """
    if mu < M_c:
        return 0
    else:
        return int(mu / M_c)


# ==============================================================================
# BETA FUNCTIONS WITH KK CORRECTIONS
# ==============================================================================

def beta_coefficients_effective(mu: float,
                                 localization: Tuple[float, float, float],
                                 M_c: float = PhysicsConstants.M_KK) -> np.ndarray:
    """
    Effective beta coefficients including KK tower contributions.

    b_i^{eff}(μ) = b_i^{SM} + ε_i × N_KK(μ) × Δb_KK

    Args:
        mu: Energy scale (GeV)
        localization: (ε₁, ε₂, ε₃) localization parameters (0-1)
        M_c: Compactification scale (GeV)

    Returns:
        Array [b₁^eff, b₂^eff, b₃^eff]
    """
    # Standard 4D beta coefficients
    b_SM = np.array([PhysicsConstants.B_1_SM,
                     PhysicsConstants.B_2_SM,
                     PhysicsConstants.B_3_SM])

    # Number of active KK modes
    N_KK = n_active_modes(mu, M_c)

    # KK corrections
    # Positive contribution: each KK mode is like adding new gauge bosons
    epsilon = np.array(localization)
    b_KK = epsilon * N_KK * PhysicsConstants.DELTA_B_KK

    # Total effective beta
    b_eff = b_SM + b_KK

    return b_eff


def beta_function_rhs(alpha_inv: np.ndarray,
                      ln_mu: float,
                      localization: Tuple[float, float, float],
                      M_c: float = PhysicsConstants.M_KK) -> np.ndarray:
    """
    Right-hand side of RG equation for scipy.integrate.odeint.

    dα_i⁻¹/d ln μ = -b_i^{eff}(μ) / (2π)

    Args:
        alpha_inv: [α₁⁻¹, α₂⁻¹, α₃⁻¹]
        ln_mu: ln(μ/M_Z)
        localization: (ε₁, ε₂, ε₃)
        M_c: Compactification scale (GeV)

    Returns:
        d(alpha_inv)/d(ln_mu)
    """
    mu = PhysicsConstants.M_Z * np.exp(ln_mu)
    b_eff = beta_coefficients_effective(mu, localization, M_c)

    # dα⁻¹/d ln μ = -b/(2π)
    d_alpha_inv_d_ln_mu = -b_eff / (2 * np.pi)

    return d_alpha_inv_d_ln_mu


# ==============================================================================
# RG EVOLUTION
# ==============================================================================

def run_gauge_couplings(mu_initial: float,
                        mu_final: float,
                        alpha_inv_initial: np.ndarray,
                        localization: Tuple[float, float, float],
                        M_c: float = PhysicsConstants.M_KK,
                        n_steps: int = 10000) -> Tuple[np.ndarray, np.ndarray]:
    """
    Evolve gauge couplings from μ_initial to μ_final.

    Args:
        mu_initial: Starting scale (GeV)
        mu_final: Ending scale (GeV)
        alpha_inv_initial: [α₁⁻¹, α₂⁻¹, α₃⁻¹] at μ_initial
        localization: (ε₁, ε₂, ε₃)
        M_c: Compactification scale (GeV)
        n_steps: Number of integration steps

    Returns:
        (ln_mu_array, alpha_inv_array)
        - ln_mu_array: ln(μ/M_Z) values
        - alpha_inv_array: shape (n_steps, 3) array of [α₁⁻¹, α₂⁻¹, α₃⁻¹]
    """
    # RG time array
    ln_mu_initial = np.log(mu_initial / PhysicsConstants.M_Z)
    ln_mu_final = np.log(mu_final / PhysicsConstants.M_Z)
    ln_mu_array = np.linspace(ln_mu_initial, ln_mu_final, n_steps)

    # Solve ODE system
    alpha_inv_array = odeint(beta_function_rhs, alpha_inv_initial, ln_mu_array,
                             args=(localization, M_c))

    return ln_mu_array, alpha_inv_array


def run_couplings_two_stage(localization: Tuple[float, float, float],
                             M_c: float = PhysicsConstants.M_KK,
                             M_GUT: float = PhysicsConstants.M_GUT_TARGET,
                             verbose: bool = False) -> Dict:
    """
    Run gauge couplings in two stages: M_Z → M_c → M_GUT.

    Stage 1: M_Z → M_c (4D running, no KK)
    Stage 2: M_c → M_GUT (5D running, with KK tower)

    Args:
        localization: (ε₁, ε₂, ε₃)
        M_c: Compactification scale (GeV)
        M_GUT: Target GUT scale (GeV)
        verbose: Print intermediate results

    Returns:
        dict with keys:
            - 'alpha_inv_at_M_c': [α₁⁻¹, α₂⁻¹, α₃⁻¹] at M_c
            - 'alpha_inv_at_M_GUT': [α₁⁻¹, α₂⁻¹, α₃⁻¹] at M_GUT
            - 'unification_spread': max - min of α_i⁻¹ at M_GUT
            - 'evolution_M_Z_to_M_c': (ln_mu, alpha_inv)
            - 'evolution_M_c_to_M_GUT': (ln_mu, alpha_inv)
    """
    # Initial conditions at M_Z
    alpha_inv_M_Z = np.array([PhysicsConstants.ALPHA_1_INV_MZ,
                              PhysicsConstants.ALPHA_2_INV_MZ,
                              PhysicsConstants.ALPHA_3_INV_MZ])

    # Stage 1: M_Z → M_c (no KK, set localization = 0)
    ln_mu_1, alpha_inv_1 = run_gauge_couplings(
        PhysicsConstants.M_Z, M_c, alpha_inv_M_Z,
        localization=(0, 0, 0),  # No KK below M_c
        M_c=M_c, n_steps=1000
    )
    alpha_inv_M_c = alpha_inv_1[-1]

    if verbose:
        print(f"At M_c = {M_c:.2e} GeV:")
        print(f"  alpha_1^-1 = {alpha_inv_M_c[0]:.2f}")
        print(f"  alpha_2^-1 = {alpha_inv_M_c[1]:.2f}")
        print(f"  alpha_3^-1 = {alpha_inv_M_c[2]:.2f}")

    # Stage 2: M_c → M_GUT (with KK tower)
    ln_mu_2, alpha_inv_2 = run_gauge_couplings(
        M_c, M_GUT, alpha_inv_M_c,
        localization=localization,
        M_c=M_c, n_steps=5000  # More steps for power-law regime
    )
    alpha_inv_M_GUT = alpha_inv_2[-1]

    if verbose:
        print(f"\nAt M_GUT = {M_GUT:.2e} GeV:")
        print(f"  alpha_1^-1 = {alpha_inv_M_GUT[0]:.2f}")
        print(f"  alpha_2^-1 = {alpha_inv_M_GUT[1]:.2f}")
        print(f"  alpha_3^-1 = {alpha_inv_M_GUT[2]:.2f}")

    # Unification quality
    spread = np.max(alpha_inv_M_GUT) - np.min(alpha_inv_M_GUT)

    if verbose:
        print(f"\nUnification spread: {spread:.3f}")
        print(f"Target: α_GUT⁻¹ = {PhysicsConstants.ALPHA_GUT_INV_TARGET}")

    return {
        'alpha_inv_at_M_c': alpha_inv_M_c,
        'alpha_inv_at_M_GUT': alpha_inv_M_GUT,
        'unification_spread': spread,
        'alpha_GUT_average': np.mean(alpha_inv_M_GUT),
        'evolution_M_Z_to_M_c': (ln_mu_1, alpha_inv_1),
        'evolution_M_c_to_M_GUT': (ln_mu_2, alpha_inv_2)
    }


# ==============================================================================
# OPTIMIZATION: FIND LOCALIZATION FOR UNIFICATION
# ==============================================================================

def unification_objective(localization: np.ndarray,
                          M_c: float = PhysicsConstants.M_KK,
                          M_GUT: float = PhysicsConstants.M_GUT_TARGET) -> float:
    """
    Objective function for localization optimization.

    Minimize: spread of α_i⁻¹ at M_GUT

    Args:
        localization: [ε₁, ε₂, ε₃] (0 to 1)
        M_c: Compactification scale (GeV)
        M_GUT: GUT scale (GeV)

    Returns:
        Unification spread (smaller = better)
    """
    # Ensure localization in valid range
    localization = np.clip(localization, 0, 1)

    # Run RG evolution
    result = run_couplings_two_stage(tuple(localization), M_c, M_GUT, verbose=False)

    # Return spread
    return result['unification_spread']


def optimize_localization(method: str = 'differential_evolution',
                          M_c: float = PhysicsConstants.M_KK,
                          M_GUT: float = PhysicsConstants.M_GUT_TARGET) -> Dict:
    """
    Find optimal localization parameters for gauge unification.

    Args:
        method: Optimization method ('minimize', 'differential_evolution', 'grid')
        M_c: Compactification scale (GeV)
        M_GUT: GUT scale (GeV)

    Returns:
        dict with keys:
            - 'localization': Optimal (ε₁, ε₂, ε₃)
            - 'spread': Final unification spread
            - 'alpha_inv_at_M_GUT': Gauge couplings at M_GUT
            - 'converged': Whether optimization succeeded
    """
    print("="*80)
    print("OPTIMIZING LOCALIZATION PARAMETERS FOR GAUGE UNIFICATION")
    print("="*80)
    print(f"Method: {method}")
    print(f"M_c = {M_c:.2e} GeV")
    print(f"M_GUT = {M_GUT:.2e} GeV")
    print()

    bounds = [(0, 1), (0, 1), (0, 1)]

    if method == 'differential_evolution':
        # Global optimization (slower but more robust)
        print("Running differential evolution (global search)...")
        result = differential_evolution(
            lambda x: unification_objective(x, M_c, M_GUT),
            bounds=bounds,
            maxiter=100,
            popsize=15,
            seed=42,
            disp=True
        )
        localization_opt = result.x
        spread_opt = result.fun
        converged = result.success

    elif method == 'minimize':
        # Local optimization (faster but may get stuck)
        print("Running local minimization...")
        x0 = [0.5, 0.5, 0.5]  # Initial guess: equal localization
        result = minimize(
            lambda x: unification_objective(x, M_c, M_GUT),
            x0=x0,
            bounds=bounds,
            method='L-BFGS-B'
        )
        localization_opt = result.x
        spread_opt = result.fun
        converged = result.success

    elif method == 'grid':
        # Grid search (very slow but guaranteed to find best)
        print("Running grid search (20^3 = 8000 points)...")
        epsilon_range = np.linspace(0, 1, 20)
        best_spread = np.inf
        best_loc = None

        for i, e1 in enumerate(epsilon_range):
            if i % 5 == 0:
                print(f"  Progress: {i}/{len(epsilon_range)}")
            for e2 in epsilon_range:
                for e3 in epsilon_range:
                    spread = unification_objective([e1, e2, e3], M_c, M_GUT)
                    if spread < best_spread:
                        best_spread = spread
                        best_loc = [e1, e2, e3]

        localization_opt = best_loc
        spread_opt = best_spread
        converged = True

    else:
        raise ValueError(f"Unknown method: {method}")

    # Re-run with optimal localization to get full results
    final_result = run_couplings_two_stage(
        tuple(localization_opt), M_c, M_GUT, verbose=True
    )

    print()
    print("="*80)
    print("OPTIMIZATION RESULTS")
    print("="*80)
    print(f"Optimal localization:")
    print(f"  epsilon_1 (U(1)_Y) = {localization_opt[0]:.4f}")
    print(f"  epsilon_2 (SU(2)_L) = {localization_opt[1]:.4f}")
    print(f"  epsilon_3 (SU(3)_c) = {localization_opt[2]:.4f}")
    print()
    print(f"Unification spread: {spread_opt:.4f}")
    print(f"Converged: {converged}")
    print("="*80)

    return {
        'localization': localization_opt,
        'spread': spread_opt,
        'alpha_inv_at_M_GUT': final_result['alpha_inv_at_M_GUT'],
        'alpha_GUT_average': final_result['alpha_GUT_average'],
        'converged': converged,
        'full_result': final_result
    }


# ==============================================================================
# VISUALIZATION
# ==============================================================================

def plot_gauge_running(localization: Tuple[float, float, float],
                       M_c: float = PhysicsConstants.M_KK,
                       M_GUT: float = PhysicsConstants.M_GUT_TARGET,
                       save_path: str = None):
    """
    Plot gauge coupling evolution from M_Z to M_GUT.

    Args:
        localization: (ε₁, ε₂, ε₃)
        M_c: Compactification scale (GeV)
        M_GUT: GUT scale (GeV)
        save_path: Optional path to save figure
    """
    print("\nGenerating gauge coupling evolution plot...")

    # Run evolution
    result = run_couplings_two_stage(localization, M_c, M_GUT, verbose=False)

    # Extract data
    ln_mu_1, alpha_inv_1 = result['evolution_M_Z_to_M_c']
    ln_mu_2, alpha_inv_2 = result['evolution_M_c_to_M_GUT']

    mu_1 = PhysicsConstants.M_Z * np.exp(ln_mu_1)
    mu_2 = PhysicsConstants.M_Z * np.exp(ln_mu_2)

    # Create figure
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

    # Left plot: Full evolution
    ax1.plot(mu_1, alpha_inv_1[:, 0], 'b-', linewidth=2, label='alpha_1^-1 (U(1)_Y)')
    ax1.plot(mu_1, alpha_inv_1[:, 1], 'g-', linewidth=2, label='alpha_2^-1 (SU(2)_L)')
    ax1.plot(mu_1, alpha_inv_1[:, 2], 'r-', linewidth=2, label='alpha_3^-1 (SU(3)_c)')

    ax1.plot(mu_2, alpha_inv_2[:, 0], 'b--', linewidth=2.5)
    ax1.plot(mu_2, alpha_inv_2[:, 1], 'g--', linewidth=2.5)
    ax1.plot(mu_2, alpha_inv_2[:, 2], 'r--', linewidth=2.5)

    ax1.axvline(M_c, color='purple', linestyle=':', linewidth=2,
                label=f'M_c = {M_c/1e3:.1f} TeV (KK threshold)')
    ax1.axvline(M_GUT, color='orange', linestyle=':', linewidth=2,
                label=f'M_GUT = {M_GUT:.2e} GeV')
    ax1.axhline(PhysicsConstants.ALPHA_GUT_INV_TARGET, color='gray',
                linestyle='--', linewidth=1.5, alpha=0.7,
                label=f'alpha_GUT^-1 = {PhysicsConstants.ALPHA_GUT_INV_TARGET}')

    ax1.set_xscale('log')
    ax1.set_xlabel('Energy Scale mu [GeV]', fontsize=13)
    ax1.set_ylabel('Inverse Coupling alpha^-1', fontsize=13)
    ax1.set_title('Gauge Coupling Unification with KK Tower', fontsize=15, fontweight='bold')
    ax1.legend(fontsize=10, loc='best')
    ax1.grid(True, alpha=0.3)

    # Right plot: Zoom near M_GUT
    # Take last 20% of evolution
    idx_zoom = int(0.8 * len(mu_2))
    mu_2_zoom = mu_2[idx_zoom:]
    alpha_inv_2_zoom = alpha_inv_2[idx_zoom:]

    ax2.plot(mu_2_zoom, alpha_inv_2_zoom[:, 0], 'b-', linewidth=3, label='alpha_1^-1')
    ax2.plot(mu_2_zoom, alpha_inv_2_zoom[:, 1], 'g-', linewidth=3, label='alpha_2^-1')
    ax2.plot(mu_2_zoom, alpha_inv_2_zoom[:, 2], 'r-', linewidth=3, label='alpha_3^-1')

    ax2.axvline(M_GUT, color='orange', linestyle=':', linewidth=2,
                label=f'M_GUT')
    ax2.axhline(PhysicsConstants.ALPHA_GUT_INV_TARGET, color='gray',
                linestyle='--', linewidth=1.5, alpha=0.7)

    # Mark final values
    alpha_final = result['alpha_inv_at_M_GUT']
    ax2.scatter([M_GUT]*3, alpha_final, s=100, marker='o',
                c=['blue', 'green', 'red'], edgecolors='black', linewidths=2,
                zorder=5)

    ax2.set_xscale('log')
    ax2.set_xlabel('Energy Scale mu [GeV]', fontsize=13)
    ax2.set_ylabel('Inverse Coupling alpha^-1', fontsize=13)
    ax2.set_title('Unification Region (Zoom)', fontsize=15, fontweight='bold')
    ax2.legend(fontsize=11, loc='best')
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Plot saved to: {save_path}")

    plt.show()


def plot_localization_scan(M_c: float = PhysicsConstants.M_KK,
                            M_GUT: float = PhysicsConstants.M_GUT_TARGET,
                            save_path: str = None):
    """
    2D scan of localization parameter space (fixing ε₃ = 0.1).

    Args:
        M_c: Compactification scale (GeV)
        M_GUT: GUT scale (GeV)
        save_path: Optional path to save figure
    """
    print("\nGenerating localization parameter scan...")

    epsilon_1_range = np.linspace(0, 1, 30)
    epsilon_2_range = np.linspace(0, 1, 30)
    epsilon_3_fixed = 0.1  # SU(3) mostly brane-localized

    spread_grid = np.zeros((len(epsilon_1_range), len(epsilon_2_range)))

    for i, e1 in enumerate(epsilon_1_range):
        if i % 5 == 0:
            print(f"  Progress: {i}/{len(epsilon_1_range)}")
        for j, e2 in enumerate(epsilon_2_range):
            spread = unification_objective([e1, e2, epsilon_3_fixed], M_c, M_GUT)
            spread_grid[i, j] = spread

    # Plot heatmap
    fig, ax = plt.subplots(figsize=(10, 8))

    im = ax.contourf(epsilon_2_range, epsilon_1_range, spread_grid,
                     levels=20, cmap='RdYlGn_r')
    cbar = plt.colorbar(im, ax=ax)
    cbar.set_label('Unification Spread', fontsize=12)

    # Find minimum
    i_min, j_min = np.unravel_index(np.argmin(spread_grid), spread_grid.shape)
    e1_min = epsilon_1_range[i_min]
    e2_min = epsilon_2_range[j_min]
    spread_min = spread_grid[i_min, j_min]

    ax.scatter(e2_min, e1_min, marker='*', s=500, c='white',
               edgecolors='black', linewidths=2, zorder=5,
               label=f'Minimum: e1={e1_min:.2f}, e2={e2_min:.2f}\nSpread={spread_min:.3f}')

    ax.set_xlabel('epsilon_2 (SU(2) Localization)', fontsize=13)
    ax.set_ylabel('epsilon_1 (U(1) Localization)', fontsize=13)
    ax.set_title(f'Unification Quality vs Localization (epsilon_3 = {epsilon_3_fixed})',
                 fontsize=14, fontweight='bold')
    ax.legend(fontsize=11, loc='upper right')
    ax.grid(True, alpha=0.3, linestyle='--')

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Plot saved to: {save_path}")

    plt.show()


# ==============================================================================
# MAIN ANALYSIS
# ==============================================================================

def main():
    """
    Main execution: optimize localization and visualize results.
    """
    print("\n" + "#"*80)
    print("# GAUGE UNIFICATION VIA KALUZA-KLEIN TOWER")
    print("# Framework: Principia Metaphysica v6.1")
    print("#"*80)
    print()

    # Step 1: Check baseline (no KK)
    print("="*80)
    print("BASELINE: NO KK CORRECTIONS (Standard SM Running)")
    print("="*80)
    baseline = run_couplings_two_stage((0, 0, 0), verbose=True)
    print()

    # Step 2: Optimize localization
    print("\n")
    opt_result = optimize_localization(method='differential_evolution')
    print()

    # Step 3: Plot results
    print("\n")
    plot_gauge_running(
        tuple(opt_result['localization']),
        save_path='gauge_unification_KK_plot.png'
    )

    # Step 4: Parameter space scan
    print("\n")
    plot_localization_scan(save_path='localization_scan.png')

    # Summary
    print("\n" + "="*80)
    print("FINAL SUMMARY")
    print("="*80)
    print(f"Baseline (no KK) spread: {baseline['unification_spread']:.3f}")
    print(f"Optimized (with KK) spread: {opt_result['spread']:.3f}")
    print()
    print(f"Improvement: {baseline['unification_spread'] - opt_result['spread']:.3f}")
    print()
    print("Optimal localization:")
    print(f"  epsilon_1 (U(1)_Y) = {opt_result['localization'][0]:.4f}  "
          f"{'(mostly bulk)' if opt_result['localization'][0] > 0.5 else '(mostly brane)'}")
    print(f"  epsilon_2 (SU(2)_L) = {opt_result['localization'][1]:.4f}  "
          f"{'(mostly bulk)' if opt_result['localization'][1] > 0.5 else '(mostly brane)'}")
    print(f"  epsilon_3 (SU(3)_c) = {opt_result['localization'][2]:.4f}  "
          f"{'(mostly bulk)' if opt_result['localization'][2] > 0.5 else '(mostly brane)'}")
    print()
    print(f"Unified coupling: alpha_GUT^-1 ~ {opt_result['alpha_GUT_average']:.2f}")
    print(f"Target value: alpha_GUT^-1 = {PhysicsConstants.ALPHA_GUT_INV_TARGET}")
    print()

    if opt_result['spread'] < 1.0:
        print("STATUS: UNIFICATION ACHIEVED ✓")
    else:
        print("STATUS: UNIFICATION NOT ACHIEVED (spread > 1.0)")

    print("="*80)

    return opt_result


if __name__ == '__main__':
    results = main()
