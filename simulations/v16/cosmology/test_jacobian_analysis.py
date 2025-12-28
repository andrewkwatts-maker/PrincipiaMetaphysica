"""
Test and analyze different Jacobian formulations for G2 moduli space sampling.

This script compares:
1. Current implementation: sqrt(det(g)) ~ (Re(T))^{-7/2}
2. Proposed Vol_modulus^3 weighting: ~ (Re(T))^{+3}
3. No-scale Kähler geometry expectations

Mathematical background:
- G2 moduli space has dim_C(M_G2) that depends on the specific manifold
- For KKLT-type compactifications with moduli T, the Kähler potential is:
  K = -3 ln(2 Re(T)) (no-scale structure)
- The Kähler metric is: g_{T\bar{T}} = ∂_T ∂_{\bar{T}} K
- Volume modulus: Vol ~ (Re(T))^{3/2} in Calabi-Yau
- For G2: different relationship between Vol and moduli

Key question: What is the correct power law for sqrt(det(g))?
"""

import numpy as np
import matplotlib.pyplot as plt
from typing import Dict, Any

def compute_sector_weights_current(n_sectors: int = 4,
                                   sampling_position: float = 0.5,
                                   modulation_width: float = 0.408) -> Dict[str, Any]:
    """
    Current implementation with (Re(T))^{-7/2} Jacobian.
    """
    sector_positions = np.linspace(0, 1, n_sectors)

    # Base Gaussian weights
    weights = np.exp(-((sector_positions - sampling_position) ** 2)
                    / (2 * modulation_width ** 2))

    # Map to Re(T) values
    re_t_values = 1.0 + 9.0 * sector_positions  # Re(T) ∈ [1, 10]

    # CURRENT: (Re(T))^{-7/2}
    metric_jacobian = np.power(re_t_values, -7/2)
    metric_jacobian /= np.mean(metric_jacobian)

    # Apply weighting
    weighted = weights * metric_jacobian
    weighted /= np.sum(weighted)

    sm_idx = np.argmin(np.abs(sector_positions - 0.5))

    return {
        'weights': weighted,
        'positions': sector_positions,
        're_t': re_t_values,
        'jacobian': metric_jacobian,
        'sm_weight': weighted[sm_idx],
        'method': 'current_-7/2'
    }

def compute_sector_weights_proposed(n_sectors: int = 4,
                                   sampling_position: float = 0.5,
                                   modulation_width: float = 0.408) -> Dict[str, Any]:
    """
    Proposed implementation with Vol^3 ~ (Re(T))^{+3} Jacobian.

    For volume modulus compactifications:
    - Vol ~ (Re(T))^{3/2} in standard KKLT
    - Vol^3 ~ (Re(T))^{9/2}

    But need to check: is this the right power?
    Alternative: Vol ~ (Re(T))^{1} might give Vol^3 ~ (Re(T))^{3}
    """
    sector_positions = np.linspace(0, 1, n_sectors)

    # Base Gaussian weights
    weights = np.exp(-((sector_positions - sampling_position) ** 2)
                    / (2 * modulation_width ** 2))

    # Map to Re(T) values
    re_t_values = 1.0 + 9.0 * sector_positions

    # PROPOSED: (Re(T))^{+3}
    metric_jacobian = np.power(re_t_values, +3)
    metric_jacobian /= np.mean(metric_jacobian)

    # Apply weighting
    weighted = weights * metric_jacobian
    weighted /= np.sum(weighted)

    sm_idx = np.argmin(np.abs(sector_positions - 0.5))

    return {
        'weights': weighted,
        'positions': sector_positions,
        're_t': re_t_values,
        'jacobian': metric_jacobian,
        'sm_weight': weighted[sm_idx],
        'method': 'proposed_+3'
    }

def compute_sector_weights_kahler_derived(n_sectors: int = 4,
                                         sampling_position: float = 0.5,
                                         modulation_width: float = 0.408) -> Dict[str, Any]:
    """
    Derive from Kähler geometry: g_{T\bar{T}} = ∂_T ∂_{\bar{T}} K.

    For no-scale Kähler potential K = -3 ln(2 Re(T)):
    - g_{T\bar{T}} = 3/(2 Re(T))^2
    - In n-dimensional moduli space, need det(g)

    For single modulus: sqrt(det(g)) = sqrt(g_{T\bar{T}}) ~ (Re(T))^{-1}
    For n moduli with similar structure: sqrt(det(g)) ~ (Re(T))^{-n}

    Question: What is the effective dimension n for G2 moduli space?
    - Could be h^{1,1} = 4 (Kähler moduli in CY analog)
    - Could be 7 (dimension of G2 itself)
    - Could be 1 (if single dominant modulus)
    """
    sector_positions = np.linspace(0, 1, n_sectors)

    # Base Gaussian weights
    weights = np.exp(-((sector_positions - sampling_position) ** 2)
                    / (2 * modulation_width ** 2))

    # Map to Re(T) values
    re_t_values = 1.0 + 9.0 * sector_positions

    # KÄHLER-DERIVED: Try different powers
    results = {}

    for n in [1, 2, 3, 4, 7, 11]:  # Various dimension candidates
        metric_jacobian = np.power(re_t_values, -n)
        metric_jacobian /= np.mean(metric_jacobian)

        weighted = weights * metric_jacobian
        weighted /= np.sum(weighted)

        sm_idx = np.argmin(np.abs(sector_positions - 0.5))

        results[f'n={n}'] = {
            'weights': weighted,
            'sm_weight': weighted[sm_idx],
            'jacobian': metric_jacobian
        }

    return {
        'positions': sector_positions,
        're_t': re_t_values,
        'base_weights': weights / np.sum(weights),
        'results': results,
        'method': 'kahler_scan'
    }

def analyze_yukawa_consistency():
    """
    Check consistency with Yukawa overlap formula.

    The code claims sigma = sqrt(b3/chi_eff) comes from the same geometry.
    For Yukawa overlaps on 3-cycles, we expect:
    - Wavefunction spread: sigma^2 ~ R^2 / chi_eff
    - 3-cycle volume: Vol_3 ~ R^3
    - Therefore: R^2 ~ Vol_3^{2/3}

    If Vol_3 ~ b3, then R^2 ~ b3^{2/3}
    But the code uses R^2 ~ b3 (linear scaling)

    Need to verify which is correct.
    """
    b3 = 24
    chi_eff = 144

    # Current formula
    sigma_current = np.sqrt(b3 / chi_eff)

    # Alternative: R^2 ~ b3^{2/3}
    sigma_alt = (b3 / chi_eff)**(1/3)

    print("\n" + "="*70)
    print("YUKAWA OVERLAP CONSISTENCY CHECK")
    print("="*70)
    print(f"b3 (associative 3-cycles): {b3}")
    print(f"chi_eff (Euler characteristic): {chi_eff}")
    print(f"\nCurrent formula: sigma = sqrt(b3/chi_eff)")
    print(f"  -> sigma = {sigma_current:.6f}")
    print(f"\nAlternative formula: sigma = (b3/chi_eff)^(1/3)")
    print(f"  -> sigma = {sigma_alt:.6f}")
    print(f"\nRatio: current/alt = {sigma_current/sigma_alt:.6f}")

    return {
        'sigma_current': sigma_current,
        'sigma_alt': sigma_alt,
        'b3': b3,
        'chi_eff': chi_eff
    }

def theoretical_analysis():
    """
    Theoretical analysis of the correct Jacobian form.

    G2 MANIFOLDS:
    - dim_R(G2) = 7 (real dimension)
    - No complex structure, but has associative 3-cycles
    - Moduli space dim depends on b^3(M)

    MODULI PARAMETERIZATION:
    - In KKLT/LVS: single Kähler modulus T = τ + iθ
    - Volume: Vol ~ τ^{3/2} (for Calabi-Yau)
    - For G2: relationship unclear from code

    KÄHLER METRIC:
    - K = -3 ln(2 Re(T)) gives g_{TT̄} = 3/(2Re(T))^2
    - For measure: d^2T √g = dτ dθ · (const/τ)
    - This gives (Re(T))^{-1} NOT (Re(T))^{-7/2}

    QUESTIONS:
    1. Where does -7/2 come from? Is it b^3(M)/2 = 24/2 = 12? No, that's not 7/2.
    2. Is it from dim(G2)/2 = 7/2? Possible, but needs justification.
    3. Or is it from a different geometric structure?
    """
    print("\n" + "="*70)
    print("THEORETICAL ANALYSIS OF JACOBIAN POWER")
    print("="*70)

    print("\nCASE 1: Standard Kahler geometry")
    print("  K = -3 ln(2 Re(T))")
    print("  g_TT* = d_T d_T* K = 3/(2 Re(T))^2")
    print("  sqrt(det(g)) ~ (Re(T))^{-1} for 1D moduli space")
    print("  sqrt(det(g)) ~ (Re(T))^{-n} for n-dim moduli space")

    print("\nCASE 2: Volume modulus weighting")
    print("  Vol ~ (Re(T))^{3/2} (standard KKLT)")
    print("  Vol^3 ~ (Re(T))^{9/2}")
    print("  But this is POSITIVE power, opposite sign from current!")

    print("\nCASE 3: G2 manifold dimension")
    print("  dim_R(G2) = 7")
    print("  If sqrt(det(g)) ~ (Re(T))^{-dim/2} then:")
    print("  sqrt(det(g)) ~ (Re(T))^{-7/2}")
    print("  MATCHES current implementation!")

    print("\nCASE 4: Moduli space dimension")
    print("  For G2 with b3 = 24 associative 3-cycles")
    print("  Moduli space could be ~24 dimensional (one modulus per cycle)")
    print("  Then sqrt(det(g)) ~ (Re(T))^{-12} (if each gives -1/2)")

    print("\nCONCLUSION:")
    print("  The -7/2 power likely comes from dim(G2)/2 = 7/2")
    print("  This assumes the Kähler metric scales uniformly across")
    print("  the 7-dimensional G2 manifold.")
    print("  HOWEVER: This mixes the internal manifold dimension (7)")
    print("  with the moduli space dimension (which could be different).")

def compare_predictions():
    """
    Compare predictions from different Jacobian formulations.
    """
    print("\n" + "="*70)
    print("COMPARISON OF DIFFERENT JACOBIAN FORMULATIONS")
    print("="*70)

    # Compute with different methods
    current = compute_sector_weights_current()
    proposed = compute_sector_weights_proposed()
    kahler = compute_sector_weights_kahler_derived()

    print(f"\nCurrent (-7/2 power):")
    print(f"  SM weight: {current['sm_weight']:.6f}")
    print(f"  Jacobian range: [{current['jacobian'].min():.4f}, {current['jacobian'].max():.4f}]")

    print(f"\nProposed (+3 power):")
    print(f"  SM weight: {proposed['sm_weight']:.6f}")
    print(f"  Jacobian range: [{proposed['jacobian'].min():.4f}, {proposed['jacobian'].max():.4f}]")

    print(f"\nKähler-derived (various n):")
    for key, data in kahler['results'].items():
        print(f"  {key}: SM weight = {data['sm_weight']:.6f}")

    # The key test: Does Omega_DM/b stay at 5.4?
    # This depends on sector weights, which feed into temperature calculations
    print("\n" + "="*70)
    print("IMPACT ON OBSERVABLES")
    print("="*70)
    print("\nNOTE: The final observable Omega_DM/b ~ 5.4 depends on:")
    print("  1. Temperature ratio T'/T = 0.57 (from decay asymmetry)")
    print("  2. Abundance ratio = (T/T')^3")
    print("\nThe sector weights affect SECTOR BLENDING, not the core DM prediction.")
    print("So changing Jacobian should NOT break Omega_DM/b ~ 5.4 constraint.")
    print("\nWhat DOES change:")
    print("  - SM sector weight (how much SM vs mirror contributes)")
    print("  - Hierarchy ratio (mass hierarchy stability)")
    print("  - Effective blending of multi-sector observables")

    return {
        'current': current,
        'proposed': proposed,
        'kahler': kahler
    }

def main():
    """Run full analysis."""
    print("\n" + "="*70)
    print("G2 MODULI SPACE JACOBIAN ANALYSIS")
    print("="*70)

    # Part 1: Yukawa consistency
    yukawa_results = analyze_yukawa_consistency()

    # Part 2: Theoretical analysis
    theoretical_analysis()

    # Part 3: Compare predictions
    comparison = compare_predictions()

    # Part 4: Visualize
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))

    # Plot 1: Jacobian functions
    ax = axes[0, 0]
    re_t = np.linspace(1, 10, 100)
    ax.plot(re_t, re_t**(-7/2), label='Current: (Re(T))^{-7/2}', linewidth=2)
    ax.plot(re_t, re_t**(+3), label='Proposed: (Re(T))^{+3}', linewidth=2)
    ax.plot(re_t, re_t**(-1), label='1D Kähler: (Re(T))^{-1}', linewidth=2, linestyle='--')
    ax.plot(re_t, re_t**(-4), label='4D Kähler: (Re(T))^{-4}', linewidth=2, linestyle='--')
    ax.set_xlabel('Re(T)')
    ax.set_ylabel('Jacobian (unnormalized)')
    ax.set_title('Jacobian Functions')
    ax.legend()
    ax.grid(True, alpha=0.3)
    ax.set_yscale('log')

    # Plot 2: Sector weights comparison
    ax = axes[0, 1]
    curr = comparison['current']
    prop = comparison['proposed']
    ax.plot(curr['positions'], curr['weights'], 'o-', label='Current (-7/2)', linewidth=2)
    ax.plot(prop['positions'], prop['weights'], 's-', label='Proposed (+3)', linewidth=2)
    ax.axvline(0.5, color='red', linestyle='--', alpha=0.5, label='SM sector (pos=0.5)')
    ax.set_xlabel('Sector Position')
    ax.set_ylabel('Normalized Weight')
    ax.set_title('Sector Weights')
    ax.legend()
    ax.grid(True, alpha=0.3)

    # Plot 3: Kähler scan
    ax = axes[1, 0]
    kahler_data = comparison['kahler']
    for n in [1, 2, 3, 4, 7]:
        weights = kahler_data['results'][f'n={n}']['weights']
        ax.plot(kahler_data['positions'], weights, 'o-', label=f'n={n}: (Re(T))^-{n}', linewidth=2)
    ax.axvline(0.5, color='red', linestyle='--', alpha=0.5)
    ax.set_xlabel('Sector Position')
    ax.set_ylabel('Normalized Weight')
    ax.set_title('Kähler Dimension Scan')
    ax.legend()
    ax.grid(True, alpha=0.3)

    # Plot 4: SM weight vs power
    ax = axes[1, 1]
    powers = np.linspace(-7, 5, 50)
    sm_weights = []
    for p in powers:
        sector_positions = np.linspace(0, 1, 4)
        weights = np.exp(-((sector_positions - 0.5) ** 2) / (2 * 0.408 ** 2))
        re_t_values = 1.0 + 9.0 * sector_positions
        jacobian = np.power(re_t_values, p)
        jacobian /= np.mean(jacobian)
        weighted = weights * jacobian
        weighted /= np.sum(weighted)
        sm_idx = np.argmin(np.abs(sector_positions - 0.5))
        sm_weights.append(weighted[sm_idx])

    ax.plot(powers, sm_weights, linewidth=2)
    ax.axvline(-7/2, color='red', linestyle='--', label='Current: -7/2', linewidth=2)
    ax.axvline(+3, color='blue', linestyle='--', label='Proposed: +3', linewidth=2)
    ax.set_xlabel('Jacobian Power')
    ax.set_ylabel('SM Sector Weight')
    ax.set_title('SM Weight vs Jacobian Power')
    ax.legend()
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('h:\\Github\\PrincipiaMetaphysica\\simulations\\v16\\cosmology\\jacobian_analysis.png', dpi=150)
    print("\n" + "="*70)
    print("Plot saved to: jacobian_analysis.png")
    print("="*70)

    return comparison

if __name__ == "__main__":
    results = main()
