#!/usr/bin/env python3
"""
Copyright (c) 2025 Andrew Keith Watts. All rights reserved.

Proton Decay Branching Ratios v8.4 - Hybrid Geometric + CKM Approach

This module combines:
1. Geometric Yukawa mixing from G₂ cycle intersections (sin(π b₂/b₃))
2. CKM rotation via Wolfenstein parameterization (λ_Cabibbo = 0.22)
3. Channel-specific Wilson coefficients from SO(10) group theory

Theoretical Basis:
- Yukawa hierarchies: Y ~ [1, λ², λ⁴] with λ = 0.22 (PDG Cabibbo)
- Geometric mixing: eps = sin(π b₂/b₃) = sin(π/6) = 0.5 from cycle overlaps
- CKM rotation: V_CKM = U_up† @ U_down (Wolfenstein to O(λ³))
- Wilson coefficients:
  * C_epi0 ~ det(Y_up) × det(Y_down_CKM) × Y_lepton / M_GUT²
  * C_Knu ~ trace(Y_up @ Y_down_CKM) × V_CKM[us] / M_GUT² (strange quark)
  * C_mupi0 ~ det(Y_up @ Y_down_CKM) × Y_mu / M_GUT²

Target: BR(e⁺π⁰) ~ 62% ± 5%, BR(K⁺ν̄) ~ 23% ± 4%

References:
- Babu-Pati-Wilczek (arXiv:hep-ph/9905477) - SO(10) proton decay with CKM
- Acharya et al. (arXiv:hep-th/0109152) - M-theory Yukawas from G₂
- PDG 2024 - CKM matrix (Wolfenstein parameters)

Version: 8.4 (resolves Issue 2.4 via CKM rotation)
"""

import numpy as np
from scipy.integrate import quad
import sys

# Import config if available
try:
    sys.path.append('..')
    from config import PM_CONSTANTS
except ImportError:
    # Fallback values
    PM_CONSTANTS = {
        'b2': 4, 'b3': 24, 'chi_eff': 144,
        'M_GUT': 2.118e16, 'alpha_GUT': 1/23.54
    }


class ProtonDecayV84:
    """
    v8.4: Hybrid geometric + CKM approach for realistic BR

    Key improvements over v8.2:
    - Explicit CKM rotation (Wolfenstein parameterization)
    - Geometric mixing eps = sin(π b₂/b₃) = 0.5
    - Literature λ_Cabibbo = 0.22 hierarchies
    - Channel-specific Wilson coefficients
    """

    def __init__(self):
        # Geometric parameters
        self.b2 = PM_CONSTANTS['b2']
        self.b3 = PM_CONSTANTS['b3']
        self.chi_eff = PM_CONSTANTS['chi_eff']

        # GUT parameters
        self.M_GUT = PM_CONSTANTS['M_GUT']  # GeV
        self.alpha_GUT = PM_CONSTANTS['alpha_GUT']

        # Yukawa parameters
        self.lambda_cab = 0.22  # PDG 2024 Cabibbo angle
        self.eps_geo = np.sin(np.pi * self.b2 / self.b3)  # sin(π/6) = 0.5

        # Proton lifetime (from hybrid RG v7.0)
        self.tau_p_total = 3.93e34  # years

    def wolfenstein_ckm_matrix(self, lambda_param=None, A=0.81, rho=0.14, eta=0.35):
        """
        Construct CKM matrix using Wolfenstein parameterization

        Standard parameterization to O(λ³):
        V_CKM = [[1 - λ²/2,      λ,            A λ³(ρ - iη)],
                 [-λ,            1 - λ²/2,     A λ²         ],
                 [A λ³(1-ρ-iη),  -A λ²,        1            ]]

        Args:
            lambda_param: Cabibbo angle (default: self.lambda_cab = 0.22)
            A, rho, eta: Wolfenstein parameters (PDG 2024)

        Returns:
            V_CKM: 3×3 complex CKM matrix
        """
        if lambda_param is None:
            lambda_param = self.lambda_cab

        lam = lambda_param
        lam2 = lam**2
        lam3 = lam**3

        # Wolfenstein to O(λ³)
        V_CKM = np.array([
            [1 - lam2/2,        lam,              A*lam3*(rho - 1j*eta)],
            [-lam,              1 - lam2/2,       A*lam2                ],
            [A*lam3*(1-rho-1j*eta), -A*lam2,      1                     ]
        ], dtype=complex)

        return V_CKM

    def compute_yukawa_geometric(self, use_moonshine=False):
        """
        Compute Yukawa matrices with geometric mixing from G₂ cycles

        v8.4 Changes:
        - Hierarchical diagonal: [1, λ², λ⁴] with λ = 0.22
        - Geometric off-diagonals: eps = sin(π b₂/b₃) = 0.5
        - Optional moonshine bias (experimental)

        Returns:
            Y_up, Y_down, Y_lepton: 3×3 Yukawa matrices
        """
        # Geometric mixing strength
        eps = self.eps_geo

        # Optional: Moonshine enhancement
        if use_moonshine:
            # Fringe: Klein j-invariant for unified textures
            try:
                from mpmath import mp, klein_j
                mp.dps = 25
                tau = mp.mpc(0, self.b3 / self.chi_eff)
                j_val = klein_j(tau)
                j_mag = abs(mp.re(j_val))
                # Normalize to ~0.4 for PMNS/CKM unification
                eps = 0.5 + 0.1 * np.log10(j_mag / 1000)
            except ImportError:
                pass  # Fall back to geometric eps

        # Hierarchical diagonal from volume suppression
        # Y ~ exp(-Vol) with Vol ~ λ^n hierarchy
        lam = self.lambda_cab
        diag_up = np.array([1.0, lam**2, lam**4])
        diag_down = diag_up * 0.9  # Slight GUT asymmetry
        diag_lepton = diag_up * 0.3  # Lepton suppression

        # Off-diagonal mixing from G₂ cycle intersections
        # I_αβγ ~ sin(π b₂/b₃) + Gaussian noise from moduli
        off_matrix_up = eps * np.random.normal(0, 0.15, (3, 3))
        off_matrix_down = eps * np.random.normal(0, 0.15, (3, 3))
        off_matrix_lepton = eps * np.random.normal(0, 0.10, (3, 3))

        # Construct Yukawa matrices
        Y_up = np.diag(diag_up) + off_matrix_up
        Y_down = np.diag(diag_down) + off_matrix_down
        Y_lepton = np.diag(diag_lepton) + off_matrix_lepton

        # Symmetrize (Y + Y†)/2 for Hermiticity
        Y_up = (Y_up + Y_up.T) / 2
        Y_down = (Y_down + Y_down.T) / 2
        Y_lepton = (Y_lepton + Y_lepton.T) / 2

        return Y_up, Y_down, Y_lepton

    def compute_wilson_coefficients_ckm(self, Y_up, Y_down, Y_lepton, V_CKM):
        """
        Compute Wilson coefficients with CKM rotation

        Following Babu-Pati-Wilczek (arXiv:hep-ph/9905477):
        - C_epi0: e⁺π⁰ channel (gauge-mediated, dimension-6)
        - C_Knu: K⁺ν̄ channel (strange quark via CKM)
        - C_mupi0: μ⁺π⁰ channel (muon lepton flavor)
        - C_other: Other subdominant channels

        Key operators:
        - LLLL (qqℓℓ): Tr(Y_u @ Y_d @ Y_l) for e⁺π⁰
        - LLLL (qqℓℓ): Weighted by CKM for K⁺ν̄

        Args:
            Y_up, Y_down, Y_lepton: Yukawa matrices
            V_CKM: CKM rotation matrix

        Returns:
            Dictionary of Wilson coefficients {channel: C_value}
        """
        # Rotate Y_down by CKM
        Y_down_CKM = V_CKM.T.conj() @ Y_down @ V_CKM

        # Wilson coefficients (dimension-6 operators)
        # Suppressed by M_GUT²
        M_GUT_sq = self.M_GUT**2

        # e⁺π⁰: Trace of Yukawa product (LLLL operator)
        # C ~ Tr(Y_u @ Y_d @ Y_l) / M_GUT²
        # This is the standard dimension-6 operator for p → e⁺π⁰
        Yukawa_product = Y_up @ Y_down_CKM @ Y_lepton
        C_epi0 = np.trace(Yukawa_product) / M_GUT_sq

        # K⁺ν̄: Strange quark channel (CKM us-element weighted)
        # Weight by V_us for u→s transition
        V_us = V_CKM[0, 1]  # Up-strange CKM element ~ λ_Cabibbo
        # Use second generation (strange) weighted product
        C_Knu = np.trace(Y_up @ Y_down_CKM) * abs(V_us) / M_GUT_sq

        # μ⁺π⁰: Muon flavor channel (second generation lepton)
        # Weight by muon component
        Yukawa_mu = Y_up @ Y_down_CKM @ Y_lepton
        C_mupi0 = Yukawa_mu[1, 1] / M_GUT_sq  # Diagonal muon element

        # Other: Residual channels
        # Use Frobenius norm for subdominant channels
        C_other = np.linalg.norm(Yukawa_product, 'fro') / M_GUT_sq / 20

        return {
            'C_epi0': C_epi0,
            'C_Knu': C_Knu,
            'C_mupi0': C_mupi0,
            'C_other': C_other
        }

    def compute_branching_ratios(self, coeffs):
        """
        Compute branching ratios from Wilson coefficients

        BR(channel) = |C_channel|² / Σ_i |C_i|²

        Args:
            coeffs: Dictionary of Wilson coefficients

        Returns:
            Dictionary of branching ratios {channel: BR_value}
        """
        # Sum of squared magnitudes
        total_C2 = sum(abs(c)**2 for c in coeffs.values())

        if total_C2 == 0:
            # Fallback if all coefficients vanish
            return {key: 1.0/len(coeffs) for key in coeffs.keys()}

        # Compute branching ratios
        BR = {key: abs(coeffs[key])**2 / total_C2 for key in coeffs.keys()}

        return BR

    def compute_channel_lifetimes(self, BR):
        """
        Compute channel-specific lifetimes

        τ_p(channel) = τ_p(total) / BR(channel)

        Args:
            BR: Dictionary of branching ratios

        Returns:
            Dictionary of channel lifetimes {channel: tau_value}
        """
        tau_channels = {}

        for channel, br in BR.items():
            if br > 0:
                tau_channels[channel] = self.tau_p_total / br
            else:
                tau_channels[channel] = np.inf

        return tau_channels

    def run_mc_uncertainty(self, n_samples=1000, use_moonshine=False):
        """
        Monte Carlo uncertainty quantification

        v8.4 Changes:
        - Vary λ_Cabibbo ± 0.02 (PDG uncertainty)
        - Vary eps_geo ± 0.1 (cycle intersection noise)
        - Vary b₃ ± 2 (flux/moduli deformations)
        - Each sample: full Yukawa + CKM recomputation

        Args:
            n_samples: Number of MC samples
            use_moonshine: Use moonshine bias (experimental)

        Returns:
            Dictionary with mean/std for each BR
        """
        # Storage for samples
        BR_samples = {
            'epi0': [], 'Knu': [], 'mupi0': [], 'other': []
        }

        # Store original parameters
        orig_lambda = self.lambda_cab
        orig_eps = self.eps_geo
        orig_b3 = self.b3

        for _ in range(n_samples):
            # Vary parameters
            self.lambda_cab = np.random.normal(orig_lambda, 0.02)
            self.eps_geo = np.random.normal(orig_eps, 0.1)
            self.b3 = int(np.random.normal(orig_b3, 2))

            # Recompute Yukawas
            Y_up, Y_down, Y_lepton = self.compute_yukawa_geometric(use_moonshine)

            # Recompute CKM
            V_CKM = self.wolfenstein_ckm_matrix(self.lambda_cab)

            # Recompute Wilson coefficients
            coeffs = self.compute_wilson_coefficients_ckm(
                Y_up, Y_down, Y_lepton, V_CKM
            )

            # Recompute branching ratios
            BR = self.compute_branching_ratios(coeffs)

            # Store samples
            BR_samples['epi0'].append(BR['C_epi0'])
            BR_samples['Knu'].append(BR['C_Knu'])
            BR_samples['mupi0'].append(BR['C_mupi0'])
            BR_samples['other'].append(BR['C_other'])

        # Restore original parameters
        self.lambda_cab = orig_lambda
        self.eps_geo = orig_eps
        self.b3 = orig_b3

        # Compute statistics
        results = {}
        for channel, samples in BR_samples.items():
            results[f'BR_{channel}_mean'] = np.mean(samples)
            results[f'BR_{channel}_std'] = np.std(samples)
            results[f'BR_{channel}_median'] = np.median(samples)

        return results

    def run_full_calculation(self, verbose=True, use_moonshine=False):
        """
        Execute complete v8.4 calculation with CKM rotation

        Steps:
        1. Compute geometric Yukawa matrices
        2. Construct CKM matrix (Wolfenstein)
        3. Compute Wilson coefficients with CKM rotation
        4. Calculate branching ratios
        5. Run MC uncertainty quantification

        Args:
            verbose: Print detailed output
            use_moonshine: Use moonshine bias (experimental)

        Returns:
            Dictionary with all results
        """
        if verbose:
            print("=" * 70)
            print("PROTON DECAY BRANCHING RATIOS v8.4 (Geometric + CKM)")
            print("=" * 70)
            print(f"Geometric parameters: b2={self.b2}, b3={self.b3}, chi_eff={self.chi_eff}")
            print(f"GUT parameters: M_GUT={self.M_GUT:.3e} GeV, alpha_GUT={self.alpha_GUT:.4f}")
            print(f"Yukawa parameters: lambda_Cabibbo={self.lambda_cab}, eps_geo={self.eps_geo:.3f}")
            print(f"Total lifetime: tau_p = {self.tau_p_total:.2e} years")
            print()

        # Step 1: Compute Yukawa matrices
        Y_up, Y_down, Y_lepton = self.compute_yukawa_geometric(use_moonshine)

        if verbose:
            print("YUKAWA HIERARCHIES:")
            print(f"  Up-type diagonal: {np.diag(Y_up)}")
            print(f"  Down-type diagonal: {np.diag(Y_down)}")
            print(f"  Lepton diagonal: {np.diag(Y_lepton)}")
            print()

        # Step 2: Construct CKM matrix
        V_CKM = self.wolfenstein_ckm_matrix()

        if verbose:
            print("CKM MATRIX (Wolfenstein):")
            print(f"  |V_us| = {abs(V_CKM[0,1]):.4f} (Cabibbo)")
            print(f"  |V_cb| = {abs(V_CKM[1,2]):.4f}")
            print(f"  |V_ub| = {abs(V_CKM[0,2]):.4f}")
            print()

        # Step 3: Compute Wilson coefficients
        coeffs = self.compute_wilson_coefficients_ckm(Y_up, Y_down, Y_lepton, V_CKM)

        # Step 4: Compute branching ratios
        BR = self.compute_branching_ratios(coeffs)

        if verbose:
            print("BRANCHING RATIOS:")
            print(f"  BR(p -> e+pi0) = {BR['C_epi0']*100:.1f}%")
            print(f"  BR(p -> K+nu) = {BR['C_Knu']*100:.1f}%")
            print(f"  BR(p -> mu+pi0) = {BR['C_mupi0']*100:.1f}%")
            print(f"  BR(p -> other) = {BR['C_other']*100:.1f}%")
            print()

        # Step 5: Channel-specific lifetimes
        tau_channels = self.compute_channel_lifetimes(BR)

        if verbose:
            print("CHANNEL-SPECIFIC LIFETIMES:")
            for channel, tau in tau_channels.items():
                channel_name = channel.replace('C_', '')
                print(f"  tau_p({channel_name}) = {tau:.2e} years")
            print()

        # Step 6: MC uncertainty
        if verbose:
            print("Running Monte Carlo uncertainty quantification (n=1000)...")

        mc_results = self.run_mc_uncertainty(n_samples=1000, use_moonshine=use_moonshine)

        if verbose:
            print("MONTE CARLO RESULTS:")
            print(f"  BR(e+pi0) = {mc_results['BR_epi0_mean']*100:.1f}% +/- {mc_results['BR_epi0_std']*100:.1f}%")
            print(f"  BR(K+nu) = {mc_results['BR_Knu_mean']*100:.1f}% +/- {mc_results['BR_Knu_std']*100:.1f}%")
            print()

        # Step 7: Experimental validation
        if verbose:
            print("EXPERIMENTAL COMPARISON:")
            print("  Super-K bounds:")
            print(f"    tau_p(e+pi0) > 1.67e34 years")
            print(f"    Predicted: {tau_channels['C_epi0']:.2e} years")
            print(f"    Ratio: {tau_channels['C_epi0']/1.67e34:.2f}x bound")
            print()
            print("  Hyper-K sensitivity (2027-2035):")
            print(f"    Expected: BR(e+pi0) ~ 50-70% (SO(10))")
            print(f"    Predicted: {mc_results['BR_epi0_mean']*100:.1f}% ± {mc_results['BR_epi0_std']*100:.1f}%")
            print(f"    Status: {'CONSISTENT' if 50 <= mc_results['BR_epi0_mean']*100 <= 70 else 'OUTSIDE RANGE'}")
            print()
            print("=" * 70)

        # Compile results
        results = {
            'BR_epi0': BR['C_epi0'],
            'BR_Knu': BR['C_Knu'],
            'BR_mupi0': BR['C_mupi0'],
            'BR_other': BR['C_other'],
            'tau_epi0': tau_channels['C_epi0'],
            'tau_Knu': tau_channels['C_Knu'],
            'tau_mupi0': tau_channels['C_mupi0'],
            'tau_other': tau_channels['C_other'],
            **mc_results
        }

        return results


def main():
    """Test v8.4 implementation"""
    calc = ProtonDecayV84()
    results = calc.run_full_calculation(verbose=True, use_moonshine=False)

    print("\nTest with moonshine (fringe):")
    results_moonshine = calc.run_full_calculation(verbose=True, use_moonshine=True)


if __name__ == '__main__':
    main()
