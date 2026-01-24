#!/usr/bin/env python3
# =============================================================================
# HISTORICAL ARCHIVE - v16/v20 Physics
# =============================================================================
# This file contains visualizations for the deprecated (24,2) two-time physics
# or Sp(2,R) gauge fixing framework. These have been superseded by the v22+
# unified (24,1) signature with 12×(2,0) Euclidean bridge pairs.
#
# Retained for historical reference and educational purposes.
# DO NOT use these visualizations for v23+ publication figures.
#
# Current framework: docs/appendices/appendix_g_euclidean_bridge.md
# =============================================================================
"""
g2_geometry_diagrams.py - G2 Geometry Visualization Diagrams

Generates two diagrams for Principia Metaphysica G2 geometry:
1. g2-manifold.png - Visualization of G2 holonomy manifold (7D with special structure)
2. signature-structure.png - Signature (24,2) structure showing space vs time dimensions

All visualizations emphasize b3=24 as the single topological input that determines
everything else in the theory.

Output: ../../images/g2-manifold.png, ../../images/signature-structure.png

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.
Licensed under the MIT License. See LICENSE file for details.
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import Circle, FancyBboxPatch, Polygon, Wedge, Arc
from matplotlib.collections import PatchCollection
import matplotlib.patheffects as pe
import os
import sys

# PM Colors
PM_PURPLE = '#8b7fff'  # Primary PM color
PM_GOLD = '#ffd43b'    # Predictions color
PM_DARK = '#2d1b4e'    # Dark purple
PM_LIGHT = '#d4ccff'   # Light purple
PM_GREEN = '#4ade80'   # Success/validation
PM_BLUE = '#60a5fa'    # Info

# Set publication-quality style
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.size'] = 11
plt.rcParams['axes.labelsize'] = 13
plt.rcParams['axes.titlesize'] = 15
plt.rcParams['legend.fontsize'] = 10
plt.rcParams['figure.dpi'] = 300
plt.rcParams['axes.facecolor'] = '#fafafa'
plt.rcParams['figure.facecolor'] = 'white'


def generate_g2_manifold_diagram(output_path: str) -> None:
    """
    Generate G2 holonomy manifold visualization.

    Shows the 7-dimensional G2 manifold structure with:
    - TCS (Twisted Connected Sum) construction
    - Associative 3-cycles (b3=24)
    - K3 fibration structure
    - Connection to physics outputs

    Args:
        output_path: Path to save the PNG file
    """
    fig, ax = plt.subplots(figsize=(14, 10))
    ax.set_xlim(-0.5, 13.5)
    ax.set_ylim(-0.5, 9.5)
    ax.set_aspect('equal')
    ax.axis('off')

    # Title
    ax.text(6.75, 9.2, r'$G_2$ Holonomy Manifold Structure', fontsize=18, fontweight='bold',
            ha='center', color=PM_DARK)
    ax.text(6.75, 8.7, 'TCS Construction #187 with b3=24 Associative 3-Cycles',
            fontsize=12, ha='center', color='#666666', style='italic')

    # ===========================================================================
    # Central G2 Manifold representation (stylized 7D structure)
    # ===========================================================================

    # Draw two interlocking structures representing TCS gluing
    center_x, center_y = 4.0, 5.0

    # Left ACyl piece (CY3+)
    theta1 = np.linspace(0.3, 2*np.pi - 0.3, 100)
    r1 = 1.8 + 0.3*np.sin(3*theta1)
    x1 = center_x - 1.2 + r1*np.cos(theta1)
    y1 = center_y + r1*np.sin(theta1)
    ax.fill(x1, y1, color=PM_PURPLE, alpha=0.3, edgecolor=PM_PURPLE, linewidth=2)
    ax.text(center_x - 1.5, center_y + 2.5, r'$Z_+$', fontsize=14, fontweight='bold',
            ha='center', color=PM_DARK)
    ax.text(center_x - 1.5, center_y + 2.0, 'ACyl CY3', fontsize=9, ha='center', color='#666666')

    # Right ACyl piece (CY3-)
    r2 = 1.8 + 0.3*np.sin(3*theta1 + np.pi/3)
    x2 = center_x + 1.2 + r2*np.cos(theta1)
    y2 = center_y + r2*np.sin(theta1)
    ax.fill(x2, y2, color=PM_GOLD, alpha=0.3, edgecolor=PM_GOLD, linewidth=2)
    ax.text(center_x + 1.5, center_y + 2.5, r'$Z_-$', fontsize=14, fontweight='bold',
            ha='center', color=PM_DARK)
    ax.text(center_x + 1.5, center_y + 2.0, 'ACyl CY3', fontsize=9, ha='center', color='#666666')

    # Gluing region (T3 neck)
    glue_ellipse = mpatches.Ellipse((center_x, center_y), 1.0, 2.0, angle=0,
                                     facecolor='white', edgecolor=PM_DARK,
                                     linewidth=2, linestyle='--', alpha=0.9)
    ax.add_patch(glue_ellipse)
    ax.text(center_x, center_y, r'$T^3$', fontsize=11, ha='center', va='center',
            fontweight='bold', color=PM_DARK)
    ax.text(center_x, center_y - 0.5, 'gluing', fontsize=8, ha='center', color='#666666')

    # Draw associative 3-cycles as small circles around the manifold
    n_cycles = 12  # Show 12 representative cycles (half of 24)
    cycle_r = 0.15
    cycle_dist = 2.5
    for i in range(n_cycles):
        angle = 2*np.pi*i/n_cycles
        cx = center_x + cycle_dist*np.cos(angle)
        cy = center_y + cycle_dist*np.sin(angle)
        # Alternate colors
        color = PM_PURPLE if i % 2 == 0 else PM_GOLD
        circle = Circle((cx, cy), cycle_r, facecolor=color, edgecolor='white',
                        linewidth=1, alpha=0.8)
        ax.add_patch(circle)

    # Label for 3-cycles
    ax.annotate(r'$b_3 = 24$ associative 3-cycles', xy=(center_x + 2.3, center_y + 1.8),
                xytext=(7.5, 7.5), fontsize=11, color=PM_DARK,
                arrowprops=dict(arrowstyle='->', color=PM_PURPLE, lw=1.5),
                bbox=dict(boxstyle='round,pad=0.3', facecolor=PM_LIGHT, alpha=0.8))

    # ===========================================================================
    # Key Topological Properties Box (left side)
    # ===========================================================================

    props_box = FancyBboxPatch((0.2, 0.3), 3.2, 3.2, boxstyle="round,pad=0.05",
                                facecolor='white', edgecolor=PM_PURPLE, linewidth=2)
    ax.add_patch(props_box)

    ax.text(1.8, 3.3, 'Topology Invariants', fontsize=12, fontweight='bold',
            ha='center', color=PM_DARK)

    props_text = [
        (r'$b_3 = 24$', 'THE INPUT', PM_GOLD),
        (r'$b_2 = 4$', 'Kahler moduli', PM_PURPLE),
        (r'$\chi_{eff} = 144$', 'Euler char.', PM_PURPLE),
        (r'$n_{gen} = 3$', 'Generations', PM_GREEN),
    ]

    for i, (formula, desc, color) in enumerate(props_text):
        y_pos = 2.8 - i*0.6
        ax.text(0.5, y_pos, formula, fontsize=13, fontweight='bold', color=color)
        ax.text(2.0, y_pos, desc, fontsize=10, color='#666666')

    # ===========================================================================
    # G2 Holonomy Conditions Box (right side)
    # ===========================================================================

    hol_box = FancyBboxPatch((8.5, 3.5), 4.5, 3.8, boxstyle="round,pad=0.05",
                              facecolor='white', edgecolor=PM_DARK, linewidth=2)
    ax.add_patch(hol_box)

    ax.text(10.75, 7.0, r'$G_2$ Holonomy Conditions', fontsize=12, fontweight='bold',
            ha='center', color=PM_DARK)

    conditions = [
        (r'$\nabla \eta = 0$', 'Parallel spinor'),
        (r'$R_{\mu\nu} = 0$', 'Ricci-flat'),
        (r'$d\Phi = 0$', 'Closed 3-form'),
        (r'$d(*\Phi) = 0$', 'Coclosed 4-form'),
    ]

    for i, (formula, desc) in enumerate(conditions):
        y_pos = 6.4 - i*0.7
        # Checkmark
        ax.text(8.7, y_pos, u'\u2713', fontsize=14, color=PM_GREEN, fontweight='bold')
        ax.text(9.2, y_pos, formula, fontsize=11, color=PM_DARK)
        ax.text(11.5, y_pos, desc, fontsize=9, color='#666666')

    # ===========================================================================
    # Physics Outputs (bottom right)
    # ===========================================================================

    phys_box = FancyBboxPatch((8.5, 0.3), 4.5, 2.8, boxstyle="round,pad=0.05",
                               facecolor=PM_LIGHT, edgecolor=PM_GOLD, linewidth=2)
    ax.add_patch(phys_box)

    ax.text(10.75, 2.9, 'Physics from Geometry', fontsize=12, fontweight='bold',
            ha='center', color=PM_DARK)

    physics = [
        (r'$n_{gen} = \chi_{eff}/48 = 3$', 'Fermion families'),
        (r'$\tau_p = 8.15 \times 10^{34}$ yr', 'Proton lifetime'),
        (r'$M_{KK} \sim 5$ TeV', 'KK gravitons'),
    ]

    for i, (formula, desc) in enumerate(physics):
        y_pos = 2.4 - i*0.6
        ax.text(8.7, y_pos, formula, fontsize=10, color=PM_DARK, fontweight='bold')
        ax.text(12.5, y_pos, desc, fontsize=9, color='#666666', ha='right')

    # ===========================================================================
    # Arrow showing derivation chain
    # ===========================================================================

    # Arrow from b3=24 to physics
    ax.annotate('', xy=(8.3, 2.0), xytext=(3.5, 1.5),
                arrowprops=dict(arrowstyle='->', color=PM_GOLD, lw=2.5,
                               connectionstyle='arc3,rad=0.2'))
    ax.text(5.9, 1.0, 'geometry constrains physics', fontsize=10, style='italic',
            color=PM_DARK, rotation=10)

    # ===========================================================================
    # K3 Fibration detail (top right)
    # ===========================================================================

    # Small K3 surface representation
    k3_center = (11, 8.2)
    k3_size = 0.6

    # Draw K3 as intersecting tori (simplified)
    for offset in [-0.15, 0, 0.15]:
        ellipse = mpatches.Ellipse((k3_center[0] + offset, k3_center[1]),
                                    k3_size, k3_size*0.4, angle=30 + offset*50,
                                    facecolor=PM_PURPLE, alpha=0.3, edgecolor=PM_PURPLE)
        ax.add_patch(ellipse)

    ax.text(k3_center[0], k3_center[1] - 0.6, r'K3 fiber', fontsize=9, ha='center',
            color=PM_DARK)
    ax.text(k3_center[0], k3_center[1] - 0.9, r'$h^{1,1}=4$', fontsize=9, ha='center',
            color='#666666')

    # Connection line to main manifold
    ax.plot([k3_center[0] - 0.8, center_x + 2.5], [k3_center[1] - 0.5, center_y + 2.0],
            'k--', alpha=0.3, lw=1)

    plt.tight_layout()

    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"[OK] G2 manifold diagram saved to: {output_path}")
    plt.close()


def generate_signature_structure_diagram(output_path: str) -> None:
    """
    Generate signature (24,2) structure diagram.

    Shows the dimensional structure:
    - 26D total with signature (24,2)
    - Decomposition into M_A^14 x M_B^14 sharing 2 time dimensions
    - Sp(2,R) gauge fixing
    - Reduction to 4D observed spacetime

    Args:
        output_path: Path to save the PNG file
    """
    fig, ax = plt.subplots(figsize=(14, 10))
    ax.set_xlim(-0.5, 13.5)
    ax.set_ylim(-0.5, 9.5)
    ax.set_aspect('equal')
    ax.axis('off')

    # Title
    ax.text(6.75, 9.2, 'Signature (24,2) Structure: Two-Time Physics', fontsize=18,
            fontweight='bold', ha='center', color=PM_DARK)
    ax.text(6.75, 8.7, r'$M_{26} = M_A^{14} \otimes_T M_B^{14}$ with shared timelike dimensions',
            fontsize=12, ha='center', color='#666666', style='italic')

    # ===========================================================================
    # 26D Block at top
    # ===========================================================================

    box_26d = FancyBboxPatch((4.5, 7.0), 4.5, 1.3, boxstyle="round,pad=0.1",
                              facecolor=PM_PURPLE, edgecolor=PM_DARK, linewidth=2, alpha=0.3)
    ax.add_patch(box_26d)

    ax.text(6.75, 7.8, '26D Spacetime', fontsize=14, fontweight='bold', ha='center', color=PM_DARK)
    ax.text(6.75, 7.35, 'Signature (24,2)', fontsize=11, ha='center', color='#444444')

    # Draw dimension bars for 26D
    bar_y = 7.1
    # 24 space dimensions (purple)
    ax.add_patch(FancyBboxPatch((4.7, bar_y), 3.6, 0.15), )
    rect_space = plt.Rectangle((4.7, bar_y), 3.6, 0.15, facecolor=PM_PURPLE, edgecolor='none')
    ax.add_patch(rect_space)
    ax.text(6.5, bar_y + 0.25, '24 space', fontsize=8, ha='center', color=PM_DARK)

    # 2 time dimensions (gold)
    rect_time = plt.Rectangle((8.35, bar_y), 0.45, 0.15, facecolor=PM_GOLD, edgecolor='none')
    ax.add_patch(rect_time)
    ax.text(8.57, bar_y + 0.25, '2 time', fontsize=8, ha='center', color=PM_DARK)

    # ===========================================================================
    # Two 14D halves in the middle
    # ===========================================================================

    # M_A^14 (left)
    box_ma = FancyBboxPatch((1.0, 4.5), 4.0, 1.8, boxstyle="round,pad=0.1",
                             facecolor=PM_PURPLE, edgecolor=PM_DARK, linewidth=2, alpha=0.2)
    ax.add_patch(box_ma)
    ax.text(3.0, 5.9, r'$M_A^{14}$', fontsize=14, fontweight='bold', ha='center', color=PM_DARK)
    ax.text(3.0, 5.5, 'Signature (12,2)', fontsize=10, ha='center', color='#444444')

    # Dimension breakdown for M_A
    ax.text(3.0, 5.0, '12 space + 2 time', fontsize=9, ha='center', color='#666666')

    # M_B^14 (right)
    box_mb = FancyBboxPatch((8.5, 4.5), 4.0, 1.8, boxstyle="round,pad=0.1",
                             facecolor=PM_GOLD, edgecolor=PM_DARK, linewidth=2, alpha=0.2)
    ax.add_patch(box_mb)
    ax.text(10.5, 5.9, r'$M_B^{14}$', fontsize=14, fontweight='bold', ha='center', color=PM_DARK)
    ax.text(10.5, 5.5, 'Signature (12,2)', fontsize=10, ha='center', color='#444444')

    # Dimension breakdown for M_B
    ax.text(10.5, 5.0, '12 space + 2 time', fontsize=9, ha='center', color='#666666')

    # Shared time region (center overlap)
    shared_box = FancyBboxPatch((5.5, 4.7), 2.5, 1.4, boxstyle="round,pad=0.05",
                                 facecolor=PM_GOLD, edgecolor=PM_DARK, linewidth=3, alpha=0.4)
    ax.add_patch(shared_box)
    ax.text(6.75, 5.6, 'Shared', fontsize=10, fontweight='bold', ha='center', color=PM_DARK)
    ax.text(6.75, 5.2, '2 Time Dims', fontsize=10, ha='center', color=PM_DARK)
    ax.text(6.75, 4.85, r'$\otimes_T$', fontsize=12, ha='center', color=PM_DARK)

    # Arrows from 26D to the two halves
    ax.annotate('', xy=(3.0, 6.3), xytext=(5.5, 7.0),
                arrowprops=dict(arrowstyle='->', color=PM_DARK, lw=2))
    ax.annotate('', xy=(10.5, 6.3), xytext=(8.0, 7.0),
                arrowprops=dict(arrowstyle='->', color=PM_DARK, lw=2))

    # ===========================================================================
    # Sp(2,R) Gauge Fixing Box
    # ===========================================================================

    sp2r_box = FancyBboxPatch((5.0, 2.8), 3.5, 1.3, boxstyle="round,pad=0.1",
                               facecolor='white', edgecolor=PM_GREEN, linewidth=2)
    ax.add_patch(sp2r_box)
    ax.text(6.75, 3.8, 'Sp(2,R) Gauge Fixing', fontsize=12, fontweight='bold',
            ha='center', color=PM_DARK)
    ax.text(6.75, 3.35, 'Eliminates ghosts from 2-time', fontsize=9, ha='center', color='#666666')
    ax.text(6.75, 3.0, r'$X^2=0, X\cdot P=0, P^2+M^2=0$', fontsize=9, ha='center', color=PM_DARK)

    # Arrow from halves to Sp(2,R)
    ax.annotate('', xy=(6.75, 4.1), xytext=(6.75, 4.5),
                arrowprops=dict(arrowstyle='->', color=PM_DARK, lw=2))

    # ===========================================================================
    # 4D Effective Spacetime at bottom
    # ===========================================================================

    box_4d = FancyBboxPatch((4.5, 0.5), 4.5, 1.8, boxstyle="round,pad=0.1",
                             facecolor=PM_GREEN, edgecolor=PM_DARK, linewidth=2, alpha=0.3)
    ax.add_patch(box_4d)
    ax.text(6.75, 2.0, '4D Spacetime', fontsize=14, fontweight='bold', ha='center', color=PM_DARK)
    ax.text(6.75, 1.55, 'Signature (3,1)', fontsize=11, ha='center', color='#444444')
    ax.text(6.75, 1.1, '3 space + 1 time', fontsize=10, ha='center', color='#666666')
    ax.text(6.75, 0.7, 'Observable Universe', fontsize=9, ha='center', color='#888888', style='italic')

    # Arrow from Sp(2,R) to 4D
    ax.annotate('', xy=(6.75, 2.3), xytext=(6.75, 2.8),
                arrowprops=dict(arrowstyle='->', color=PM_DARK, lw=2))

    # ===========================================================================
    # Dimensional Reduction Pathway (right side)
    # ===========================================================================

    path_box = FancyBboxPatch((10.0, 0.5), 3.2, 3.6, boxstyle="round,pad=0.1",
                               facecolor='white', edgecolor=PM_PURPLE, linewidth=2)
    ax.add_patch(path_box)
    ax.text(11.6, 3.85, 'Reduction Pathway', fontsize=11, fontweight='bold',
            ha='center', color=PM_DARK)

    stages = [
        ('26D (24,2)', 'Starting point'),
        (r'$\downarrow$ Sp(2,R)', 'Gauge fix'),
        ('13D (12,1)', 'Shadow'),
        (r'$\downarrow$ G$_2$', 'Compactify'),
        ('6D (5,1)', 'Bulk'),
        (r'$\downarrow$ Brane', 'Localize'),
        ('4D (3,1)', 'Observable'),
    ]

    for i, (stage, note) in enumerate(stages):
        y_pos = 3.4 - i * 0.42
        ax.text(10.3, y_pos, stage, fontsize=9, color=PM_DARK if i % 2 == 0 else PM_PURPLE,
                fontweight='bold' if i % 2 == 0 else 'normal')
        if i % 2 == 0:
            ax.text(12.8, y_pos, note, fontsize=8, color='#888888', ha='right')

    # ===========================================================================
    # Ghost Elimination Detail (left side)
    # ===========================================================================

    ghost_box = FancyBboxPatch((0.3, 0.5), 3.5, 3.6, boxstyle="round,pad=0.1",
                                facecolor='white', edgecolor=PM_DARK, linewidth=2)
    ax.add_patch(ghost_box)
    ax.text(2.05, 3.85, 'Two-Time Benefits', fontsize=11, fontweight='bold',
            ha='center', color=PM_DARK)

    benefits = [
        (u'\u2713', 'Ghost elimination'),
        (u'\u2713', 'CPT from geometry'),
        (u'\u2713', 'Dual holographic'),
        (u'\u2713', 'No negative norm'),
    ]

    for i, (check, benefit) in enumerate(benefits):
        y_pos = 3.3 - i * 0.55
        ax.text(0.6, y_pos, check, fontsize=12, color=PM_GREEN, fontweight='bold')
        ax.text(1.0, y_pos, benefit, fontsize=10, color=PM_DARK)

    # Spinor reduction note
    ax.text(2.05, 1.1, 'Spinor Components:', fontsize=9, ha='center', color='#666666')
    ax.text(2.05, 0.75, r'$8192 \rightarrow 64$', fontsize=11, ha='center',
            color=PM_PURPLE, fontweight='bold')

    # ===========================================================================
    # Key insight box
    # ===========================================================================

    insight_box = FancyBboxPatch((0.3, 7.0), 3.5, 1.3, boxstyle="round,pad=0.1",
                                  facecolor=PM_GOLD, edgecolor=PM_DARK, linewidth=2, alpha=0.3)
    ax.add_patch(insight_box)
    ax.text(2.05, 7.95, 'Key Insight', fontsize=11, fontweight='bold', ha='center', color=PM_DARK)
    ax.text(2.05, 7.5, r'$b_3 = 24$ constrains', fontsize=10, ha='center', color=PM_DARK)
    ax.text(2.05, 7.15, 'all dimensions', fontsize=10, ha='center', color=PM_DARK)

    plt.tight_layout()

    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"[OK] Signature structure diagram saved to: {output_path}")
    plt.close()


def main():
    """Generate all G2 geometry diagrams."""
    # Get output directory (relative to this script)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    images_dir = os.path.join(script_dir, '..', '..', 'images')

    print("\n" + "="*70)
    print(" G2 GEOMETRY DIAGRAMS GENERATOR")
    print("="*70)

    # Generate G2 manifold diagram
    print("\n[1/2] Generating G2 manifold diagram...")
    g2_path = os.path.join(images_dir, 'g2-manifold.png')
    generate_g2_manifold_diagram(g2_path)

    # Generate signature structure diagram
    print("\n[2/2] Generating signature structure diagram...")
    sig_path = os.path.join(images_dir, 'signature-structure.png')
    generate_signature_structure_diagram(sig_path)

    print("\n" + "="*70)
    print(" ALL DIAGRAMS GENERATED SUCCESSFULLY")
    print("="*70)
    print(f"\nOutput files:")
    print(f"  - {os.path.abspath(g2_path)}")
    print(f"  - {os.path.abspath(sig_path)}")


if __name__ == "__main__":
    main()
