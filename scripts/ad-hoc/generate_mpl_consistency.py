"""
generate_mpl_consistency.py - Planck Mass Consistency Check

Plots M_Pl(calculated) / M_Pl(observed) vs warp parameter k
to show consistency of dimensional reduction.

Output: images/mpl-consistency-vs-k.png
"""

import numpy as np
import matplotlib.pyplot as plt
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import SharedDimensionsParameters, PhenomenologyParameters

# Set publication-quality style
plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams['font.size'] = 12
plt.rcParams['axes.labelsize'] = 14
plt.rcParams['axes.titlesize'] = 16
plt.rcParams['legend.fontsize'] = 11
plt.rcParams['figure.dpi'] = 300

# Create figure
fig, ax = plt.subplots(figsize=(11, 8))

# Parameters
M_obs = PhenomenologyParameters.M_PLANCK
M_star = PhenomenologyParameters.M_STAR
R_y = SharedDimensionsParameters.R_SHARED_Y
R_z = SharedDimensionsParameters.R_SHARED_Z

# Warp parameter range
k_vals = np.linspace(10, 100, 200)

# Calculate ratio for each k
ratios = []
for k in k_vals:
    # Physical k (dimensionful)
    k_physical = k * M_obs if k < 100 else k

    # Warp integral: ∫ dy e^(-2ky) = [1 - e^(-2k π R)] / (2k)
    warp_integral = (1 - np.exp(-2 * k_physical * np.pi * R_y)) / (2 * k_physical)

    # Torus volume
    V_2 = (2 * np.pi * R_y) * (2 * np.pi * R_z)

    # M_Pl² = M_6D^4 × V_2 × warp_integral
    # Using M_6D ≈ M_star for simplicity
    M_Pl_calc_squared = M_star**4 * V_2 * warp_integral
    M_calc = np.sqrt(M_Pl_calc_squared) if M_Pl_calc_squared > 0 else 0

    ratio = M_calc / M_obs if M_obs > 0 else 0
    ratios.append(ratio)

ratios = np.array(ratios)

# Plot main curve
ax.plot(k_vals, ratios, 'b-', linewidth=3, label='Dimensional reduction consistency', zorder=3)

# Acceptable band (0.5 < ratio < 2.0)
ax.fill_between(k_vals, 0.5, 2.0, color='green', alpha=0.2, label='Acceptable consistency (±factor of 2)', zorder=1)

# Ideal consistency line
ax.axhline(1.0, color='green', linestyle='--', linewidth=2, label='Perfect consistency', zorder=2)

# Current PM choice
k_current = SharedDimensionsParameters.WARP_PARAMETER_K
ratio_current = ratios[np.argmin(np.abs(k_vals - k_current))]

ax.plot(k_current, ratio_current, 'ro', markersize=12, markeredgecolor='black',
        markeredgewidth=2, label=f'PM choice: $k = {k_current}$', zorder=4)

# Annotate current value
ax.annotate(f'$k = {k_current}$\nRatio = {ratio_current:.3f}',
            xy=(k_current, ratio_current), xytext=(k_current + 10, ratio_current + 0.5),
            fontsize=11, fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.5', facecolor='yellow', alpha=0.9, edgecolor='black'),
            arrowprops=dict(arrowstyle='->', lw=2, color='black'))

# Labels
ax.set_xlabel(r'Warp Parameter $k$ (dimensionless)', fontsize=14, fontweight='bold')
ax.set_ylabel(r'$M_{\mathrm{Pl}}^{\mathrm{calc}} / M_{\mathrm{Pl}}^{\mathrm{obs}}$', fontsize=14, fontweight='bold')
ax.set_title('Planck Mass Consistency Check: 26D→13D→6D→4D Reduction',
             fontsize=16, fontweight='bold', pad=20)

# Set limits
ax.set_xlim(10, 100)
ax.set_ylim(0.1, 10)
ax.set_yscale('log')

# Grid
ax.grid(True, which='both', alpha=0.3, zorder=0)

# Legend
ax.legend(loc='upper right', fontsize=11, framealpha=0.95, edgecolor='black')

# Add text box with formula
formula_text = (
    r"$M_{\mathrm{Pl}}^2 = M_*^{11} \cdot V_9$" + "\n"
    r"$V_9 = V_7(G_2) \times V_2(T^2)$" + "\n\n"
    "Warped 6D→4D reduction:\n"
    r"$M_{\mathrm{Pl}}^2 = M_{6D}^4 \cdot V_2 \cdot \int dy \, e^{-2ky}$" + "\n\n"
    f"$M_{{\\mathrm{{Pl}}}}^{{\\mathrm{{obs}}}} = {M_obs:.2e}$ GeV\n"
    f"$M_* = {M_star:.2e}$ GeV\n"
    f"$R_y = R_z = {R_y:.2e}$ GeV$^{{-1}}$"
)
ax.text(0.02, 0.98, formula_text, transform=ax.transAxes,
        fontsize=10, verticalalignment='top', horizontalalignment='left',
        bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.9, edgecolor='black', linewidth=1.5),
        family='serif')

# Add interpretation box
interpretation_text = (
    "Interpretation:\n"
    "• Ratio = 1: Perfect match\n"
    "• 0.5 < Ratio < 2.0: Consistent\n"
    "• Ratio < 0.5 or > 2.0: Adjust k or R\n\n"
    "Current status: "
    f"{'CONSISTENT ✓' if 0.5 < ratio_current < 2.0 else 'NEEDS ADJUSTMENT ✗'}"
)
ax.text(0.98, 0.02, interpretation_text, transform=ax.transAxes,
        fontsize=10, verticalalignment='bottom', horizontalalignment='right',
        bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.95, edgecolor='black', linewidth=1.5))

plt.tight_layout()

# Save
output_path = os.path.join(os.path.dirname(__file__), '..', 'images', 'mpl-consistency-vs-k.png')
os.makedirs(os.path.dirname(output_path), exist_ok=True)
plt.savefig(output_path, dpi=300, bbox_inches='tight')
print(f"[OK] M_Pl consistency plot saved to: {output_path}")

# Print summary
print(f"\nConsistency Check:")
print(f"  Current k = {k_current}")
print(f"  Ratio = {ratio_current:.3f}")
print(f"  Status: {'CONSISTENT' if 0.5 < ratio_current < 2.0 else 'NEEDS ADJUSTMENT'}")

plt.close()
