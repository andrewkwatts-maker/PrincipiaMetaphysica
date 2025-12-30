#!/usr/bin/env python3
"""
Ricci Flow Hubble Evolution: Visual Hubble Tension Resolution
===============================================================

Shows how H(z) evolves from z=1100 (CMB) to z=0 (local) through
G2 manifold Ricci flow dynamics.

This visualization demonstrates the PM resolution of the Hubble tension:
- Early universe (CMB, z~1100): H0 = 67.4 km/s/Mpc (Planck)
- Late universe (local, z=0): H0 = 73.04 km/s/Mpc (SH0ES)
- PM prediction: Smooth interpolation via Ricci flow

The G2 manifold's Ricci flow creates a time-dependent effective
curvature that modifies the Hubble expansion rate. The "tension"
is not a contradiction but a natural consequence of manifold evolution.

Output file: ../../images/ricci-flow-hubble-evolution.png

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.

Dedicated To:
    My Wife: Elizabeth May Watts
    Our Messiah: Jesus Of Nazareth
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Circle, FancyArrowPatch, Rectangle
from matplotlib.collections import PatchCollection
import matplotlib.patheffects as path_effects
from pathlib import Path

# PM Color palette
PM_COLORS = {
    "purple": "#8b7fff",
    "pink": "#ff7eb6",
    "blue": "#60a5fa",
    "orange": "#fb923c",
    "gold": "#ffd43b",
    "green": "#4ade80",
    "red": "#ef4444",
    "text": "#f8f9fa",
    "bg_dark": "#1a1f3a",
    "bg_card": "#2a2f4a",
}

# Output directory
OUTPUT_DIR = Path(__file__).parent.parent.parent / "images"

# Cosmological constants
H0_PLANCK = 67.4  # km/s/Mpc (Planck 2018)
H0_PLANCK_SIGMA = 0.5
H0_SHOES = 73.04  # km/s/Mpc (SH0ES 2025)
H0_SHOES_SIGMA = 1.04
OMEGA_M = 0.311  # Matter density
OMEGA_DE = 0.689  # Dark energy density

# PM parameters
B3 = 24
K_GIMEL = B3 / 2 + 1 / np.pi  # ~12.318
TAU = K_GIMEL / B3  # ~0.513 (Ricci flow timescale)
Z_STAR = 1 / TAU  # ~1.95 (transition redshift)


def setup_publication_style():
    """Configure matplotlib for publication-quality output."""
    plt.rcParams.update({
        'font.family': 'serif',
        'font.size': 11,
        'axes.titlesize': 14,
        'axes.labelsize': 12,
        'xtick.labelsize': 10,
        'ytick.labelsize': 10,
        'legend.fontsize': 10,
        'figure.dpi': 150,
        'savefig.dpi': 300,
        'savefig.bbox': 'tight',
        'axes.linewidth': 1.2,
        'axes.grid': True,
        'grid.alpha': 0.3,
        'grid.linestyle': '--',
    })


def compute_lcdm_H(z, H0=H0_PLANCK):
    """
    Compute H(z) for standard LCDM cosmology.

    H(z) = H0 * sqrt(Omega_m * (1+z)^3 + Omega_de)
    """
    return H0 * np.sqrt(OMEGA_M * (1 + z)**3 + OMEGA_DE)


def compute_pm_H(z, H0_local=H0_SHOES, H0_early=H0_PLANCK, z_star=Z_STAR):
    """
    Compute H(z) with PM Ricci flow interpolation.

    The effective H0 smoothly transitions from H0_local at z=0
    to H0_early at z >> z_star via the interpolation function f(z).

    f(z) = 1 / (1 + (z/z_star)^2)
    """
    # Interpolation function from Ricci flow
    alpha = 2.0  # Exponent from flow rate
    f = 1.0 / (1.0 + (z / z_star) ** alpha)

    # Interpolated H0
    H0_eff = H0_local * f + H0_early * (1 - f)

    # Standard E(z) factor
    E_z = np.sqrt(OMEGA_M * (1 + z)**3 + OMEGA_DE)

    return H0_eff * E_z


def compute_pm_w_correction_H(z, H0_local=H0_SHOES, H0_early=H0_PLANCK, z_star=Z_STAR):
    """
    Compute H(z) with PM w(z) dark energy correction.

    In PM, dark energy has w0 = -11/13 and evolves with redshift.
    This provides additional evolution beyond pure interpolation.
    """
    # w0 from dimensional reduction
    w0 = -11 / 13  # ~-0.846

    # w(z) evolution (CPL-like parametrization)
    wa = 0.1  # Approximate evolution parameter

    # Dark energy density evolution
    def rho_de(z_val):
        # Integrate w(z') from 0 to z
        # For w(z) = w0 + wa * z / (1+z)
        # rho_de / rho_de0 = (1+z)^(3*(1+w0+wa)) * exp(-3*wa*z/(1+z))
        w_eff = w0 + wa * z_val / (1 + z_val)
        return (1 + z_val) ** (3 * (1 + w0)) * np.exp(-3 * wa * z_val / (1 + z_val))

    # Interpolation for H0
    alpha = 2.0
    f = 1.0 / (1.0 + (z / z_star) ** alpha)
    H0_eff = H0_local * f + H0_early * (1 - f)

    # Modified E(z) with w(z) correction
    E_z = np.sqrt(OMEGA_M * (1 + z)**3 + OMEGA_DE * rho_de(z))

    return H0_eff * E_z


def generate_ricci_flow_evolution():
    """
    Generate Ricci flow Hubble evolution plot.

    Shows H(z) from z=0 (local) to z=1100 (CMB) with:
    - LCDM prediction (Planck-normalized)
    - LCDM prediction (SH0ES-normalized)
    - PM Ricci flow interpolation
    - PM w(z) correction
    """
    setup_publication_style()

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 7))

    # =========================================================================
    # Left panel: Full redshift range (log scale)
    # =========================================================================

    # Redshift array (logarithmic for full range)
    z_full = np.logspace(-2, 3.04, 500)  # z=0.01 to z=1100

    # Compute H(z) for each model
    H_lcdm_planck = compute_lcdm_H(z_full, H0=H0_PLANCK)
    H_lcdm_shoes = compute_lcdm_H(z_full, H0=H0_SHOES)
    H_pm = compute_pm_H(z_full)
    H_pm_wz = compute_pm_w_correction_H(z_full)

    # Normalize to H0 for cleaner display (H(z)/H0 vs z)
    # Instead show actual H(z) values

    ax1.loglog(z_full, H_lcdm_planck, '--', color='gray', linewidth=2,
               label=r'$\Lambda$CDM (Planck $H_0$=67.4)')
    ax1.loglog(z_full, H_lcdm_shoes, ':', color='gray', linewidth=2,
               label=r'$\Lambda$CDM (SH0ES $H_0$=73.0)')
    ax1.loglog(z_full, H_pm, '-', color=PM_COLORS['purple'], linewidth=3,
               label='PM: Ricci Flow')
    ax1.loglog(z_full, H_pm_wz, '-', color=PM_COLORS['pink'], linewidth=2,
               label=r'PM: + $w(z)$ correction')

    # Mark key epochs
    # CMB (z ~ 1089)
    z_cmb = 1089
    H_cmb_pm = compute_pm_H(z_cmb)
    ax1.axvline(x=z_cmb, color=PM_COLORS['orange'], linestyle='--', alpha=0.5, linewidth=1.5)
    ax1.scatter([z_cmb], [H_cmb_pm], color=PM_COLORS['orange'], s=100, zorder=5,
                marker='o', edgecolors='white', linewidths=2)
    ax1.text(z_cmb * 1.3, H_cmb_pm * 1.3, 'CMB\n$z=1089$', fontsize=9,
             color=PM_COLORS['orange'], ha='left', va='bottom')

    # Transition region (z ~ z_star)
    ax1.axvline(x=Z_STAR, color=PM_COLORS['gold'], linestyle='--', alpha=0.7, linewidth=1.5)
    H_trans = compute_pm_H(Z_STAR)
    ax1.scatter([Z_STAR], [H_trans], color=PM_COLORS['gold'], s=100, zorder=5,
                marker='s', edgecolors='white', linewidths=2)
    ax1.text(Z_STAR * 0.5, H_trans * 0.7, f'Transition\n$z_*={Z_STAR:.2f}$', fontsize=9,
             color=PM_COLORS['gold'], ha='right', va='top')

    # Local (z ~ 0)
    ax1.scatter([0.01], [H_pm[0]], color=PM_COLORS['blue'], s=100, zorder=5,
                marker='^', edgecolors='white', linewidths=2)
    ax1.text(0.015, H_pm[0] * 1.1, 'Local\n$z\\approx0$', fontsize=9,
             color=PM_COLORS['blue'], ha='left', va='bottom')

    ax1.set_xlabel('Redshift $z$', fontsize=12)
    ax1.set_ylabel('$H(z)$ [km/s/Mpc]', fontsize=12)
    ax1.set_title('Hubble Evolution: Full Cosmic History', fontsize=13, fontweight='bold')
    ax1.legend(loc='upper left', fontsize=9, framealpha=0.95)
    ax1.set_xlim(0.01, 1500)
    ax1.set_ylim(60, 1e8)

    # =========================================================================
    # Right panel: Low redshift detail (linear scale)
    # =========================================================================

    # Redshift array (linear for low z)
    z_low = np.linspace(0, 3, 500)

    # Compute H(z)/E(z) to show effective H0(z) evolution
    # E(z) = sqrt(Omega_m (1+z)^3 + Omega_de)
    E_z = np.sqrt(OMEGA_M * (1 + z_low)**3 + OMEGA_DE)

    # Effective H0 from each model
    H0_eff_lcdm_planck = compute_lcdm_H(z_low, H0=H0_PLANCK) / E_z
    H0_eff_lcdm_shoes = compute_lcdm_H(z_low, H0=H0_SHOES) / E_z
    H0_eff_pm = compute_pm_H(z_low) / E_z
    H0_eff_pm_wz = compute_pm_w_correction_H(z_low) / E_z

    # Plot effective H0
    ax2.fill_between([0, 3], H0_PLANCK - 2*H0_PLANCK_SIGMA, H0_PLANCK + 2*H0_PLANCK_SIGMA,
                     color='blue', alpha=0.1, label=r'Planck $2\sigma$')
    ax2.fill_between([0, 3], H0_SHOES - 2*H0_SHOES_SIGMA, H0_SHOES + 2*H0_SHOES_SIGMA,
                     color='red', alpha=0.1, label=r'SH0ES $2\sigma$')

    ax2.axhline(y=H0_PLANCK, color='blue', linestyle='--', linewidth=1.5, alpha=0.7)
    ax2.axhline(y=H0_SHOES, color='red', linestyle='--', linewidth=1.5, alpha=0.7)

    ax2.plot(z_low, H0_eff_lcdm_planck, '--', color='gray', linewidth=1.5,
             label=r'$\Lambda$CDM: constant $H_0$')
    ax2.plot(z_low, H0_eff_pm, '-', color=PM_COLORS['purple'], linewidth=3,
             label='PM: evolving $H_0(z)$')
    ax2.plot(z_low, H0_eff_pm_wz, '-', color=PM_COLORS['pink'], linewidth=2,
             label=r'PM: + $w(z)$')

    # Annotate the tension
    ax2.annotate('', xy=(0.1, H0_SHOES), xytext=(0.1, H0_PLANCK),
                arrowprops=dict(arrowstyle='<->', color=PM_COLORS['red'], lw=2))
    ax2.text(0.15, (H0_SHOES + H0_PLANCK) / 2, r'$5\sigma$ Tension!',
             fontsize=10, color=PM_COLORS['red'], fontweight='bold', va='center')

    # Annotate PM resolution
    ax2.annotate(
        'PM Resolution:\nSmooth evolution\nvia Ricci flow',
        xy=(1.5, 70), xytext=(2.0, 68),
        fontsize=9, color=PM_COLORS['purple'],
        arrowprops=dict(arrowstyle='->', color=PM_COLORS['purple'], lw=1.5),
        bbox=dict(boxstyle='round,pad=0.3', facecolor='white',
                  edgecolor=PM_COLORS['purple'], alpha=0.9)
    )

    # Mark key values
    ax2.text(2.8, H0_PLANCK + 0.5, r'$H_0^{early}$=67.4', fontsize=9, color='blue',
             ha='right', va='bottom')
    ax2.text(2.8, H0_SHOES - 0.5, r'$H_0^{local}$=73.0', fontsize=9, color='red',
             ha='right', va='top')

    # Mark transition
    ax2.axvline(x=Z_STAR, color=PM_COLORS['gold'], linestyle='--', alpha=0.7, linewidth=1.5)
    ax2.text(Z_STAR + 0.05, 66, f'$z_*$={Z_STAR:.2f}', fontsize=9, color=PM_COLORS['gold'],
             ha='left', va='bottom', rotation=90)

    ax2.set_xlabel('Redshift $z$', fontsize=12)
    ax2.set_ylabel('Effective $H_0(z)$ [km/s/Mpc]', fontsize=12)
    ax2.set_title('Hubble Tension Resolution: $H_0$ Evolution', fontsize=13, fontweight='bold')
    ax2.legend(loc='lower left', fontsize=9, framealpha=0.95)
    ax2.set_xlim(0, 3)
    ax2.set_ylim(64, 76)

    # Add equation box
    eqn_box = (
        r"$\mathbf{PM\ Ricci\ Flow\ Model}$" + "\n\n"
        r"$f(z) = \frac{1}{1 + (z/z_*)^2}$" + "\n\n"
        r"$H_0^{eff}(z) = H_0^{local} f(z) + H_0^{early}(1-f(z))$" + "\n\n"
        r"$z_* = \frac{b_3}{k_\gimel} = \frac{24}{12.318} \approx 1.95$"
    )
    props = dict(boxstyle='round,pad=0.5', facecolor='white',
                edgecolor=PM_COLORS['purple'], alpha=0.95)
    ax2.text(0.98, 0.98, eqn_box, transform=ax2.transAxes, fontsize=9,
            verticalalignment='top', horizontalalignment='right', bbox=props)

    plt.tight_layout()

    # Save
    output_path = OUTPUT_DIR / "ricci-flow-hubble-evolution.png"
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_path, dpi=300, facecolor='white', edgecolor='none')
    plt.close()

    print(f"Generated: {output_path}")
    return output_path


def main():
    """Generate the Ricci flow evolution plot."""
    print("=" * 60)
    print("Generating Ricci Flow Hubble Evolution Plot")
    print("=" * 60)

    output_path = generate_ricci_flow_evolution()

    print("\n" + "=" * 60)
    print("Ricci Flow Evolution Plot Complete")
    print("=" * 60)
    print(f"  Output: {output_path}")
    print("=" * 60)


if __name__ == "__main__":
    main()
