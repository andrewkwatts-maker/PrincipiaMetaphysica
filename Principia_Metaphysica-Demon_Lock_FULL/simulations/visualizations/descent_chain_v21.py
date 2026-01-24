#!/usr/bin/env python3
"""
Descent Chain Visualization v21
================================

Visualizes the (24,1) → dual shadows → 4D descent chain for Principia Metaphysica v21.

Features:
1. Descent chain diagram showing dimensional flow
2. Euclidean bridge structure
3. OR reduction operator visualization
4. G2 compactification per shadow

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.

Dedicated To:
    My Wife: Elizabeth May Watts
    Our Messiah: Jesus Of Nazareth
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle, Rectangle
from matplotlib.patches import ConnectionPatch
import matplotlib.patches as mpatches
import os

# Output directory
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "output")
os.makedirs(OUTPUT_DIR, exist_ok=True)


def create_descent_chain_diagram():
    """Create the main descent chain visualization."""
    fig, ax = plt.subplots(1, 1, figsize=(14, 10))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 10)
    ax.axis('off')

    # Title
    ax.text(7, 9.5, 'Principia Metaphysica v21.0 - Descent Chain',
            ha='center', va='center', fontsize=16, fontweight='bold')
    ax.text(7, 9.0, '(24,1) Dual-Shadow Model with Euclidean Bridge',
            ha='center', va='center', fontsize=12, style='italic', color='#666666')

    # Level 1: 26D Bulk
    box_26d = FancyBboxPatch((4.5, 7.5), 5, 1, boxstyle="round,pad=0.1",
                              facecolor='#2C3E50', edgecolor='black', linewidth=2)
    ax.add_patch(box_26d)
    ax.text(7, 8, '25D(24,1) Bulk', ha='center', va='center',
            fontsize=12, fontweight='bold', color='white')
    ax.text(7, 7.65, r'$ds^2 = \sum_{i=1}^{24} dx_i^2 - dt^2$',
            ha='center', va='center', fontsize=10, color='#ECF0F1')

    # Arrow down
    ax.annotate('', xy=(7, 6.5), xytext=(7, 7.5),
                arrowprops=dict(arrowstyle='->', color='#2C3E50', lw=2))
    ax.text(7.3, 7, 'Descent', ha='left', va='center', fontsize=9, color='#2C3E50')

    # Level 2: Dual Shadows + Bridge (side by side)
    # Normal Shadow
    box_normal = FancyBboxPatch((1, 5.2), 3.5, 1.3, boxstyle="round,pad=0.1",
                                 facecolor='#3498DB', edgecolor='black', linewidth=2)
    ax.add_patch(box_normal)
    ax.text(2.75, 6.1, 'Normal Shadow', ha='center', va='center',
            fontsize=11, fontweight='bold', color='white')
    ax.text(2.75, 5.7, '13D(12,1)', ha='center', va='center', fontsize=10, color='#ECF0F1')
    ax.text(2.75, 5.35, r'$b_3 = 12$', ha='center', va='center', fontsize=9, color='#ECF0F1')

    # Euclidean Bridge (center)
    box_bridge = FancyBboxPatch((5.25, 5.2), 3.5, 1.3, boxstyle="round,pad=0.1",
                                 facecolor='#9B59B6', edgecolor='black', linewidth=2)
    ax.add_patch(box_bridge)
    ax.text(7, 6.1, 'Euclidean Bridge', ha='center', va='center',
            fontsize=11, fontweight='bold', color='white')
    ax.text(7, 5.7, '(2,0) Timeless', ha='center', va='center', fontsize=10, color='#ECF0F1')
    ax.text(7, 5.35, r'$ds^2 = dy_1^2 + dy_2^2$', ha='center', va='center', fontsize=9, color='#ECF0F1')

    # Mirror Shadow
    box_mirror = FancyBboxPatch((9.5, 5.2), 3.5, 1.3, boxstyle="round,pad=0.1",
                                 facecolor='#E74C3C', edgecolor='black', linewidth=2)
    ax.add_patch(box_mirror)
    ax.text(11.25, 6.1, 'Mirror Shadow', ha='center', va='center',
            fontsize=11, fontweight='bold', color='white')
    ax.text(11.25, 5.7, '13D(12,1)', ha='center', va='center', fontsize=10, color='#ECF0F1')
    ax.text(11.25, 5.35, r'$b_3 = 12$', ha='center', va='center', fontsize=9, color='#ECF0F1')

    # OR Reduction connections
    ax.annotate('', xy=(5.25, 5.85), xytext=(4.5, 5.85),
                arrowprops=dict(arrowstyle='<->', color='#9B59B6', lw=1.5,
                               connectionstyle="arc3,rad=0.1"))
    ax.annotate('', xy=(9.5, 5.85), xytext=(8.75, 5.85),
                arrowprops=dict(arrowstyle='<->', color='#9B59B6', lw=1.5,
                               connectionstyle="arc3,rad=-0.1"))
    ax.text(7, 4.9, 'OR: R_perp = [[0,-1],[1,0]]',
            ha='center', va='center', fontsize=9, color='#9B59B6')

    # Arrows down from shadows to G2
    ax.annotate('', xy=(2.75, 4.0), xytext=(2.75, 5.2),
                arrowprops=dict(arrowstyle='->', color='#3498DB', lw=2))
    ax.annotate('', xy=(11.25, 4.0), xytext=(11.25, 5.2),
                arrowprops=dict(arrowstyle='->', color='#E74C3C', lw=2))
    ax.text(2.0, 4.6, 'G2', ha='center', va='center', fontsize=9, color='#3498DB')
    ax.text(12.0, 4.6, 'G2', ha='center', va='center', fontsize=9, color='#E74C3C')

    # Level 3: G2 Compactification per shadow
    # Normal G2
    box_g2_normal = FancyBboxPatch((1, 2.8), 3.5, 1.2, boxstyle="round,pad=0.1",
                                    facecolor='#27AE60', edgecolor='black', linewidth=2)
    ax.add_patch(box_g2_normal)
    ax.text(2.75, 3.55, r'$G_2(7,0)$ Compactification', ha='center', va='center',
            fontsize=10, fontweight='bold', color='white')
    ax.text(2.75, 3.1, r'$n_{gen} = \chi_{eff}/(4 \cdot b_3) = 3$',
            ha='center', va='center', fontsize=9, color='#ECF0F1')

    # Mirror G2
    box_g2_mirror = FancyBboxPatch((9.5, 2.8), 3.5, 1.2, boxstyle="round,pad=0.1",
                                    facecolor='#27AE60', edgecolor='black', linewidth=2)
    ax.add_patch(box_g2_mirror)
    ax.text(11.25, 3.55, r'$G_2(7,0)$ Compactification', ha='center', va='center',
            fontsize=10, fontweight='bold', color='white')
    ax.text(11.25, 3.1, r'$n_{gen} = 3$ per shadow',
            ha='center', va='center', fontsize=9, color='#ECF0F1')

    # Arrows down to condensate
    ax.annotate('', xy=(2.75, 1.7), xytext=(2.75, 2.8),
                arrowprops=dict(arrowstyle='->', color='#27AE60', lw=2))
    ax.annotate('', xy=(11.25, 1.7), xytext=(11.25, 2.8),
                arrowprops=dict(arrowstyle='->', color='#27AE60', lw=2))

    # Level 4: 4D Condensates
    # Observable structure box
    box_4d = FancyBboxPatch((1.5, 0.5), 11, 1.2, boxstyle="round,pad=0.1",
                             facecolor='#F39C12', edgecolor='black', linewidth=2)
    ax.add_patch(box_4d)
    ax.text(7, 1.25, 'Observable 4D Condensate', ha='center', va='center',
            fontsize=12, fontweight='bold', color='white')
    ax.text(7, 0.85, r'$2 \times \left[(5,1)_{bridge} \oplus \bigoplus_{k=1}^{3} (3,1)_k\right]$',
            ha='center', va='center', fontsize=10, color='white')
    ax.text(7, 0.55, r'Breathing DE: $w_0 = -23/24$, DESI $\Delta = 0.02\sigma$',
            ha='center', va='center', fontsize=9, color='#FCF3CF')

    # Legend
    legend_elements = [
        mpatches.Patch(facecolor='#2C3E50', edgecolor='black', label='26D Bulk (24,1)'),
        mpatches.Patch(facecolor='#3498DB', edgecolor='black', label='Normal Shadow'),
        mpatches.Patch(facecolor='#E74C3C', edgecolor='black', label='Mirror Shadow'),
        mpatches.Patch(facecolor='#9B59B6', edgecolor='black', label='Euclidean Bridge (2,0)'),
        mpatches.Patch(facecolor='#27AE60', edgecolor='black', label='G2 Compactification'),
        mpatches.Patch(facecolor='#F39C12', edgecolor='black', label='4D Observable'),
    ]
    ax.legend(handles=legend_elements, loc='upper left', framealpha=0.95, fontsize=9)

    plt.tight_layout()
    output_path = os.path.join(OUTPUT_DIR, 'descent_chain_v21.png')
    plt.savefig(output_path, dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f"Saved: {output_path}")
    return output_path


def create_bridge_pressure_diagram():
    """Create bridge pressure and OR sampling visualization."""
    fig, ax = plt.subplots(1, 1, figsize=(10, 8))

    # Set up coordinate system
    ax.set_xlim(-2, 2)
    ax.set_ylim(-2, 2)
    ax.set_aspect('equal')
    ax.set_xlabel(r'$y_1$', fontsize=12)
    ax.set_ylabel(r'$y_2$', fontsize=12)
    ax.set_title('Euclidean Bridge: OR Reduction Sampling\nv21.0', fontsize=14, fontweight='bold')

    # Draw bridge torus (as a circle in 2D projection)
    theta = np.linspace(0, 2*np.pi, 100)
    R = 1.5
    ax.plot(R*np.cos(theta), R*np.sin(theta), 'b-', lw=2, alpha=0.3, label='Bridge Torus')

    # Draw condensate pressure contours
    Y1, Y2 = np.meshgrid(np.linspace(-1.8, 1.8, 50), np.linspace(-1.8, 1.8, 50))
    phi = 1.618  # Golden ratio
    sigma = np.sqrt(phi)

    # Normal shadow pressure
    r2_normal = Y1**2 + Y2**2
    P_normal = np.log(1 + np.exp(-r2_normal / (2 * sigma**2)))

    # Mirror shadow pressure (rotated by 90 degrees)
    Y1_rot = -Y2
    Y2_rot = Y1
    r2_mirror = Y1_rot**2 + Y2_rot**2
    P_mirror = np.log(1 + 0.9 * np.exp(-r2_mirror / (2 * sigma**2)))  # Slight offset

    # Breathing density (difference)
    rho_breath = np.abs(P_normal - P_mirror)

    # Plot breathing density
    contour = ax.contourf(Y1, Y2, rho_breath, levels=20, cmap='viridis', alpha=0.7)
    plt.colorbar(contour, ax=ax, label=r'$\rho_{breath} = |T_{normal} - R_\perp T_{mirror}|$')

    # Draw OR rotation vectors
    # Normal vector
    ax.arrow(0, 0, 1, 0, head_width=0.1, head_length=0.08, fc='blue', ec='blue', lw=2)
    ax.text(1.15, 0, r'$z_{normal}$', fontsize=11, color='blue')

    # OR-rotated vector
    ax.arrow(0, 0, 0, 1, head_width=0.1, head_length=0.08, fc='red', ec='red', lw=2)
    ax.text(0.08, 1.15, r'$R_\perp z = z_{mirror}$', fontsize=11, color='red')

    # Rotation arc
    arc_theta = np.linspace(0, np.pi/2, 30)
    ax.plot(0.4*np.cos(arc_theta), 0.4*np.sin(arc_theta), 'g-', lw=2)
    ax.text(0.5, 0.35, '90 deg', fontsize=10, color='green')

    # OR operator annotation
    ax.text(-1.7, 1.7, 'R_perp = [[0,-1],[1,0]]',
            fontsize=12, bbox=dict(boxstyle='round', facecolor='white', alpha=0.9))
    ax.text(-1.7, 1.3, 'R_perp^2 = -I (Mobius)', fontsize=10,
            bbox=dict(boxstyle='round', facecolor='white', alpha=0.9))

    ax.grid(True, alpha=0.3)
    ax.legend(loc='lower right')

    plt.tight_layout()
    output_path = os.path.join(OUTPUT_DIR, 'bridge_pressure_v21.png')
    plt.savefig(output_path, dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f"Saved: {output_path}")
    return output_path


def create_w_evolution_diagram():
    """Create dark energy w(a) evolution diagram."""
    fig, ax = plt.subplots(1, 1, figsize=(10, 6))

    # Parameters from v21
    b3 = 24
    w0 = -1 + 1/b3  # -23/24
    wa = -1/np.sqrt(b3)  # -1/sqrt(24)

    # Scale factor range
    a = np.linspace(0.3, 1.0, 100)

    # w(a) evolution
    w_a = w0 + wa * (1 - a)

    # DESI constraints (approximate)
    w_desi_center = -0.957
    w_desi_err = 0.067

    # Plot
    ax.plot(a, w_a, 'b-', lw=3, label='PM v21.0: w0 = -23/24, wa = -1/sqrt(24)')
    ax.axhline(y=-1, color='gray', linestyle='--', lw=1, label='LCDM (w = -1)')

    # DESI band (at a=1)
    ax.fill_between([0.95, 1.05], w_desi_center - w_desi_err, w_desi_center + w_desi_err,
                     color='orange', alpha=0.3, label='DESI 2025 (w0)')
    ax.scatter([1.0], [w0], s=100, c='blue', zorder=5, marker='*',
               label=f'PM w0 = {w0:.6f}')

    # Deviation annotation
    deviation = abs(w0 - w_desi_center) / w_desi_err
    ax.annotate(f'Delta = {deviation:.2f} sigma', xy=(1.0, w0),
                xytext=(0.85, w0 - 0.03), fontsize=11,
                arrowprops=dict(arrowstyle='->', color='blue'))

    ax.set_xlabel('Scale Factor a', fontsize=12)
    ax.set_ylabel('Dark Energy EOS w(a)', fontsize=12)
    ax.set_title('Breathing Dark Energy: Thawing Quintessence\n'
                 'w(a) = w0 + wa(1-a) from Topological Derivation',
                 fontsize=14, fontweight='bold')
    ax.legend(loc='upper left', framealpha=0.95)
    ax.grid(True, alpha=0.3)
    ax.set_xlim(0.3, 1.05)
    ax.set_ylim(-1.05, -0.85)

    plt.tight_layout()
    output_path = os.path.join(OUTPUT_DIR, 'w_evolution_v21.png')
    plt.savefig(output_path, dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f"Saved: {output_path}")
    return output_path


if __name__ == "__main__":
    print("=== Generating v21 Visualizations ===")
    print()
    create_descent_chain_diagram()
    create_bridge_pressure_diagram()
    create_w_evolution_diagram()
    print()
    print("All visualizations generated successfully!")
