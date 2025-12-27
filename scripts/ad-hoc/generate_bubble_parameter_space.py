"""
generate_bubble_parameter_space.py - CMB Bubble Collision Parameter Space

Creates log-log plot showing the testable regime vs unfalsifiable regime
for Coleman-De Luccia bubble nucleation.

Output: images/cmb-bubble-parameter-space.png
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import Rectangle
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import LandscapeParameters, PhenomenologyParameters

# Set publication-quality style
plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams['font.size'] = 12
plt.rcParams['axes.labelsize'] = 14
plt.rcParams['axes.titlesize'] = 16
plt.rcParams['legend.fontsize'] = 11
plt.rcParams['figure.dpi'] = 300

# Create figure
fig, ax = plt.subplots(figsize=(12, 9))

# Fixed ΔV = 10^60 GeV^4 (Principia Metaphysica choice)
DeltaV = 1e60  # GeV^4

# Define sigma range (10^45 to 10^60 GeV^3)
sigma_vals = np.logspace(45, 60, 200)

# Calculate S_E(sigma) for fixed ΔV
# S_E = 27π²σ⁴ / (2ΔV³)
S_E_vals = 27 * np.pi**2 * sigma_vals**4 / (2 * DeltaV**3)

# Main curve
ax.loglog(sigma_vals, S_E_vals, 'b-', linewidth=3, label=r'$S_E(\sigma)$ for $\Delta V = 10^{60}$ GeV$^4$', zorder=5)

# Horizontal threshold lines
S_E_testable = 100  # CMB-S4 detection threshold
S_E_standard = 1e12  # Standard landscape (unfalsifiable)

ax.axhline(S_E_testable, color='green', linestyle='--', linewidth=2.5,
           label=f'Testable: $S_E \\sim {S_E_testable:.0f}$ (CMB-S4)', zorder=4)
ax.axhline(S_E_standard, color='red', linestyle='--', linewidth=2.5,
           label=f'Unfalsifiable: $S_E \\sim 10^{{12}}$ (std landscape)', zorder=4)

# Vertical line for PM choice
sigma_PM = LandscapeParameters.SIGMA_TENSION  # 10^51 GeV^3
S_E_PM = LandscapeParameters.euclidean_action()

ax.axvline(sigma_PM, color='purple', linestyle=':', linewidth=2.5,
           label=f'PM choice: $\\sigma = 10^{{51}}$ GeV$^3$', zorder=4)

# Mark PM operating point
ax.plot(sigma_PM, S_E_PM, 'o', color='purple', markersize=12,
        markeredgecolor='black', markeredgewidth=2, zorder=6,
        label=f'PM: $S_E \\approx {S_E_PM:.0f}$')

# Color-coded regions
# Green: Testable (S_E < 100)
# Yellow: Marginal (100 < S_E < 10^4)
# Red: Unfalsifiable (S_E > 10^4)

y_min, y_max = 1, 1e15
ax.fill_between([1e45, 1e60], 1, S_E_testable, color='green', alpha=0.15, label='Testable regime', zorder=1)
ax.fill_between([1e45, 1e60], S_E_testable, 1e4, color='yellow', alpha=0.15, label='Marginal regime', zorder=1)
ax.fill_between([1e45, 1e60], 1e4, y_max, color='red', alpha=0.15, label='Unfalsifiable regime', zorder=1)

# Labels
ax.set_xlabel(r'Domain Wall Tension $\sigma$ [GeV$^3$]', fontsize=14, fontweight='bold')
ax.set_ylabel(r'Euclidean Action $S_E = \frac{27\pi^2 \sigma^4}{2 \Delta V^3}$', fontsize=14, fontweight='bold')
ax.set_title('CMB Bubble Collision Parameter Space: Testable vs Unfalsifiable Regimes',
             fontsize=16, fontweight='bold', pad=20)

# Set limits
ax.set_xlim(1e45, 1e60)
ax.set_ylim(y_min, y_max)

# Grid
ax.grid(True, which='both', alpha=0.3, zorder=0)

# Legend (outside plot area)
ax.legend(loc='upper left', fontsize=11, framealpha=0.95, edgecolor='black')

# Add annotations
# Testable region annotation
ax.annotate('Two-time enhancement\nmakes PM testable',
            xy=(sigma_PM, S_E_PM), xytext=(1e53, 1e3),
            fontsize=11, color='darkgreen', fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.5', facecolor='lightgreen', alpha=0.9),
            arrowprops=dict(arrowstyle='->', lw=2, color='darkgreen'))

# Standard landscape annotation
ax.annotate('Standard landscape:\n$\\sigma \\sim M_{Pl}^3$\n$\\Delta V \\sim M_{Pl}^4$\n(unobservable)',
            xy=(1e57, 1e12), xytext=(1e53, 1e10),
            fontsize=10, color='darkred', fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.5', facecolor='salmon', alpha=0.9),
            arrowprops=dict(arrowstyle='->', lw=2, color='darkred'))

# Add text box with key info
info_text = (
    f"Principia Metaphysica Parameters:\n"
    f"  $\\sigma = {sigma_PM:.2e}$ GeV$^3$ (effective TeV$^3$ scale)\n"
    f"  $\\Delta V = {DeltaV:.2e}$ GeV$^4$ (reduced from $M_{{Pl}}^4$)\n"
    f"  $S_E \\approx {S_E_PM:.0f}$ (edge of CMB-S4 detection)\n"
    f"  Tunneling rate: $\\Gamma \\sim \\exp(-{S_E_PM:.0f}) \\sim 10^{{-44}}$ yr$^{{-1}}$ Mpc$^{{-3}}$\n"
    f"  Expected bubble size: $\\lambda \\sim 10^{{-3}}$ rad (CMB angular scale)"
)
ax.text(0.98, 0.02, info_text, transform=ax.transAxes,
        fontsize=10, verticalalignment='bottom', horizontalalignment='right',
        bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.95, edgecolor='black', linewidth=1.5),
        family='monospace')

plt.tight_layout()

# Save
output_path = os.path.join(os.path.dirname(__file__), '..', 'images', 'cmb-bubble-parameter-space.png')
os.makedirs(os.path.dirname(output_path), exist_ok=True)
plt.savefig(output_path, dpi=300, bbox_inches='tight')
print(f"[OK] CMB bubble parameter space saved to: {output_path}")

# Print key values
print(f"\nKey Values:")
print(f"  sigma (PM) = {sigma_PM:.2e} GeV^3")
print(f"  DeltaV (PM) = {DeltaV:.2e} GeV^4")
print(f"  S_E (PM) = {S_E_PM:.2f}")
print(f"  Gamma (PM) ~ exp(-{S_E_PM:.0f}) ~ {np.exp(-S_E_PM):.2e} yr^-1 Mpc^-3")

plt.close()
