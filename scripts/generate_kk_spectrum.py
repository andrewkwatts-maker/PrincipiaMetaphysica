"""
generate_kk_spectrum.py - KK Graviton Spectrum Visualization

Creates a 2D grid plot showing the first 20 Kaluza-Klein graviton modes
from the 2D shared extra dimensions (T²) structure.

Output: images/kk-spectrum-2d-grid.png
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.colors import LinearSegmentedColormap
import sys
import os

# Add parent directory to path for config import
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import SharedDimensionsParameters, V61Predictions

# Set publication-quality style
plt.style.use('seaborn-v0_8-darkgrid')
plt.rcParams['font.size'] = 12
plt.rcParams['axes.labelsize'] = 14
plt.rcParams['axes.titlesize'] = 16
plt.rcParams['legend.fontsize'] = 11
plt.rcParams['xtick.labelsize'] = 11
plt.rcParams['ytick.labelsize'] = 11
plt.rcParams['figure.dpi'] = 300

# Generate KK spectrum
n_max = 5
m_max = 5
spectrum = []

for n in range(0, n_max + 1):
    for m in range(0, m_max + 1):
        if n == 0 and m == 0:
            continue  # Skip zero mode
        mass = SharedDimensionsParameters.kk_mass(n, m)
        spectrum.append((n, m, mass))

# Extract data
n_vals = np.array([s[0] for s in spectrum])
m_vals = np.array([s[1] for s in spectrum])
masses = np.array([s[2] for s in spectrum])

# Convert from GeV to TeV for display
masses_tev = masses / 1000.0

# Create figure
fig, ax = plt.subplots(figsize=(10, 8))

# Create color map (green to red for 5-15 TeV)
colors = ['#2ecc71', '#f1c40f', '#e67e22', '#e74c3c']  # Green -> Yellow -> Orange -> Red
cmap = LinearSegmentedColormap.from_list('kk_spectrum', colors)

# Normalize masses for color mapping (5-15 TeV range)
mass_min = 5.0
mass_max = 15.0
norm_masses = (masses_tev - mass_min) / (mass_max - mass_min)
norm_masses = np.clip(norm_masses, 0, 1)

# Size proportional to mass (scaled for visibility)
sizes = 100 + 400 * (masses_tev / masses_tev.max())

# Scatter plot
scatter = ax.scatter(n_vals, m_vals, c=norm_masses, s=sizes,
                     cmap=cmap, edgecolors='black', linewidths=1.5,
                     alpha=0.85, zorder=3)

# Annotate lightest modes
lightest_indices = np.argsort(masses)[:6]
for idx in lightest_indices:
    n, m, mass_tev = n_vals[idx], m_vals[idx], masses_tev[idx]
    ax.annotate(f'({n},{m})\n{mass_tev:.1f} TeV',
                xy=(n, m), xytext=(8, 8),
                textcoords='offset points', fontsize=9,
                bbox=dict(boxstyle='round,pad=0.3', facecolor='white',
                          edgecolor='black', alpha=0.8),
                arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0.2',
                                color='black', lw=1))

# Add grid
ax.grid(True, alpha=0.3, zorder=0)

# Labels and title
ax.set_xlabel(r'KK mode $n$ (y-direction)', fontsize=14, fontweight='bold')
ax.set_ylabel(r'KK mode $m$ (z-direction)', fontsize=14, fontweight='bold')
ax.set_title(r'Kaluza-Klein Graviton Spectrum from 2D Shared Extras ($T^2$)',
             fontsize=16, fontweight='bold', pad=20)

# Set integer ticks
ax.set_xticks(range(0, n_max + 1))
ax.set_yticks(range(0, m_max + 1))
ax.set_xlim(-0.5, n_max + 0.5)
ax.set_ylim(-0.5, m_max + 0.5)

# Colorbar
cbar = plt.colorbar(scatter, ax=ax, pad=0.02)
cbar.set_label('KK Graviton Mass [TeV]', fontsize=12, fontweight='bold')
cbar.set_ticks([0, 0.25, 0.5, 0.75, 1.0])
cbar.set_ticklabels(['5', '7.5', '10', '12.5', '15'])

# Add text box with key info
info_text = (
    f"Lightest mode: (1,0) at {SharedDimensionsParameters.M_KK_CENTRAL/1000:.1f} TeV\n"
    f"Compactification: $R_y = R_z = {SharedDimensionsParameters.R_SHARED_Y:.2e}$ GeV$^{{-1}}$\n"
    f"Current LHC bound: {V61Predictions.M_KK_CURRENT_BOUND:.1f} TeV (95% CL)\n"
    f"Point size ∝ mass"
)
ax.text(0.98, 0.02, info_text, transform=ax.transAxes,
        fontsize=10, verticalalignment='bottom', horizontalalignment='right',
        bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))

# Tight layout
plt.tight_layout()

# Save
output_path = os.path.join(os.path.dirname(__file__), '..', 'images', 'kk-spectrum-2d-grid.png')
os.makedirs(os.path.dirname(output_path), exist_ok=True)
plt.savefig(output_path, dpi=300, bbox_inches='tight')
print(f"[OK] KK spectrum saved to: {output_path}")

# Also show spectrum data
print("\nFirst 10 KK modes:")
spectrum_sorted = sorted(spectrum, key=lambda x: x[2])
for i, (n, m, mass) in enumerate(spectrum_sorted[:10], 1):
    print(f"  {i:2d}. ({n},{m}): {mass/1000:.2f} TeV")

plt.close()
