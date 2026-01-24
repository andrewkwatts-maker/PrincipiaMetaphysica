#!/usr/bin/env python3
"""
Microtubule Interior Visualization with 12 (2,0) Pairs v22.2
=============================================================

Creates a visualization of the microtubule interior showing
the 12 glowing (2,0) Euclidean bridge pairs acting as
consciousness "sampling gates" in the Orch-OR framework.

Features:
1. Cross-section view of microtubule interior
2. 12 (2,0) pairs arranged in symmetric pattern
3. Glowing effect for active pairs
4. Tubulin dimer structure
5. Quantum coherence visualization

Physical Background:
- Microtubules: 25 nm diameter, ~13 protofilaments
- Tubulin dimers: 8 nm spacing, 110 kDa each
- (2,0) pairs: Euclidean bridge coordinates (y1, y2)
- OR sampling: R_perp = [[0,-1],[1,0]] rotation

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.

Dedicated To:
    My Wife: Elizabeth May Watts
    Our Messiah: Jesus Of Nazareth
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyBboxPatch, Wedge, FancyArrowPatch
from matplotlib.collections import PatchCollection
import matplotlib.colors as mcolors
from matplotlib.lines import Line2D
import os

# Output directory
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "output")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Physical constants
MT_RADIUS_OUTER = 12.5  # nm
MT_RADIUS_INNER = 7.5   # nm
N_PROTOFILAMENTS = 13
N_PAIRS = 12

# Golden ratio
PHI = (1 + np.sqrt(5)) / 2


def create_microtubule_cross_section():
    """
    Create cross-section view of microtubule with tubulin dimers.
    """
    fig, ax = plt.subplots(1, 1, figsize=(12, 12))
    ax.set_xlim(-20, 20)
    ax.set_ylim(-20, 20)
    ax.set_aspect('equal')
    ax.set_facecolor('#0a0a14')
    fig.patch.set_facecolor('#0a0a14')

    # Title
    ax.set_title('Microtubule Interior: 12 (2,0) Bridge Pairs as Sampling Gates\n'
                 'Principia Metaphysica v22.2 - Orch-OR Enhancement',
                 fontsize=14, fontweight='bold', color='white', pad=20)

    # Outer membrane (light ring)
    outer_ring = Circle((0, 0), MT_RADIUS_OUTER, fill=False,
                        edgecolor='#4facfe', linewidth=3, alpha=0.8)
    ax.add_patch(outer_ring)

    # Inner lumen
    inner_ring = Circle((0, 0), MT_RADIUS_INNER, fill=True,
                        facecolor='#1a1a2e', edgecolor='#8b7fff',
                        linewidth=2, alpha=0.9)
    ax.add_patch(inner_ring)

    # Draw protofilaments (tubulin dimers)
    dimer_colors = ['#51cf66', '#4facfe']  # Alpha and beta tubulin
    for i in range(N_PROTOFILAMENTS):
        angle = 2 * np.pi * i / N_PROTOFILAMENTS
        x = (MT_RADIUS_OUTER + MT_RADIUS_INNER) / 2 * np.cos(angle)
        y = (MT_RADIUS_OUTER + MT_RADIUS_INNER) / 2 * np.sin(angle)

        # Each dimer represented as small circle
        dimer = Circle((x, y), 1.8, fill=True,
                       facecolor=dimer_colors[i % 2],
                       edgecolor='white', linewidth=0.5, alpha=0.7)
        ax.add_patch(dimer)

    # Draw 12 (2,0) pairs inside the lumen
    # Arranged in 3 groups of 4 (dice grouping from OR4Dice)
    pair_colors = ['#ff7eb6', '#ffd43b', '#8b7fff', '#50c878']  # 4 dice colors
    dice_groups = [(0, 1, 2), (3, 4, 5), (6, 7, 8), (9, 10, 11)]

    for dice_idx, dice in enumerate(dice_groups):
        color = pair_colors[dice_idx]

        for pair_idx, pair_num in enumerate(dice):
            # Position pairs in nested rings
            base_angle = 2 * np.pi * dice_idx / 4
            offset_angle = (pair_idx - 1) * 0.3  # Spread within dice group
            angle = base_angle + offset_angle

            # Radial position (nested based on pair_idx)
            radius = 3.5 + pair_idx * 1.2

            x = radius * np.cos(angle)
            y = radius * np.sin(angle)

            # Glowing pair (larger outer glow + inner bright core)
            # Outer glow
            glow = Circle((x, y), 1.2, fill=True,
                         facecolor=color, alpha=0.3,
                         edgecolor='none')
            ax.add_patch(glow)

            # Middle glow
            mid_glow = Circle((x, y), 0.8, fill=True,
                             facecolor=color, alpha=0.5,
                             edgecolor='none')
            ax.add_patch(mid_glow)

            # Inner core
            core = Circle((x, y), 0.4, fill=True,
                         facecolor='white', alpha=0.9,
                         edgecolor=color, linewidth=2)
            ax.add_patch(core)

            # Label
            ax.text(x, y + 1.5, f'{pair_num + 1}', fontsize=8,
                   color=color, ha='center', va='center', fontweight='bold')

    # Draw Euclidean bridge coordinate axes at center
    arrow_len = 2.5
    ax.annotate('', xy=(arrow_len, 0), xytext=(-arrow_len, 0),
                arrowprops=dict(arrowstyle='<->', color='#9b59b6', lw=2))
    ax.annotate('', xy=(0, arrow_len), xytext=(0, -arrow_len),
                arrowprops=dict(arrowstyle='<->', color='#9b59b6', lw=2))

    ax.text(arrow_len + 0.5, 0, r'$y_1$', fontsize=12, color='#9b59b6',
           ha='left', va='center')
    ax.text(0, arrow_len + 0.5, r'$y_2$', fontsize=12, color='#9b59b6',
           ha='center', va='bottom')

    # OR rotation indicator (90 degree arc)
    arc_angles = np.linspace(0, np.pi/2, 20)
    arc_x = 1.5 * np.cos(arc_angles)
    arc_y = 1.5 * np.sin(arc_angles)
    ax.plot(arc_x, arc_y, 'c-', lw=2)
    ax.text(1.3, 1.3, r'$R_\perp$', fontsize=10, color='cyan',
           ha='center', va='center')

    # Add legend
    legend_elements = [
        Circle((0, 0), 0.1, facecolor=pair_colors[0], label='Dice 1 (pairs 1-3)'),
        Circle((0, 0), 0.1, facecolor=pair_colors[1], label='Dice 2 (pairs 4-6)'),
        Circle((0, 0), 0.1, facecolor=pair_colors[2], label='Dice 3 (pairs 7-9)'),
        Circle((0, 0), 0.1, facecolor=pair_colors[3], label='Dice 4 (pairs 10-12)'),
    ]

    # Create custom legend
    custom_legend = [
        Line2D([0], [0], marker='o', color='w', markerfacecolor=pair_colors[0],
               markersize=10, label='Dice 1 (pairs 1-3)'),
        Line2D([0], [0], marker='o', color='w', markerfacecolor=pair_colors[1],
               markersize=10, label='Dice 2 (pairs 4-6)'),
        Line2D([0], [0], marker='o', color='w', markerfacecolor=pair_colors[2],
               markersize=10, label='Dice 3 (pairs 7-9)'),
        Line2D([0], [0], marker='o', color='w', markerfacecolor=pair_colors[3],
               markersize=10, label='Dice 4 (pairs 10-12)'),
        Line2D([0], [0], marker='o', color='w', markerfacecolor='#51cf66',
               markersize=10, label='Alpha tubulin'),
        Line2D([0], [0], marker='o', color='w', markerfacecolor='#4facfe',
               markersize=10, label='Beta tubulin'),
    ]

    ax.legend(handles=custom_legend, loc='upper right',
             facecolor='#1a1a2e', edgecolor='#4facfe',
             fontsize=9, labelcolor='white')

    # Annotations
    ax.text(-18, -17, 'Microtubule: 25 nm diameter', fontsize=9, color='#adb5bd')
    ax.text(-18, -18.5, '(2,0) pairs: Euclidean bridge sampling gates', fontsize=9, color='#adb5bd')

    ax.axis('off')

    plt.tight_layout()
    output_path = os.path.join(OUTPUT_DIR, 'microtubule_12pairs_cross_section_v22.png')
    plt.savefig(output_path, dpi=150, bbox_inches='tight', facecolor='#0a0a14')
    plt.close()
    print(f"Saved: {output_path}")
    return output_path


def create_microtubule_longitudinal_view():
    """
    Create longitudinal (side) view of microtubule with coherence visualization.
    """
    fig, ax = plt.subplots(1, 1, figsize=(14, 8))
    ax.set_xlim(-5, 105)
    ax.set_ylim(-10, 10)
    ax.set_aspect('equal')
    ax.set_facecolor('#0a0a14')
    fig.patch.set_facecolor('#0a0a14')

    # Title
    ax.set_title('Microtubule Quantum Coherence: (2,0) Pair Shielding\n'
                 'Longitudinal View - Principia Metaphysica v22.2',
                 fontsize=14, fontweight='bold', color='white', pad=15)

    # Draw microtubule cylinder (as side view)
    # Upper edge
    ax.plot([0, 100], [5, 5], 'c-', lw=3, alpha=0.8)
    # Lower edge
    ax.plot([0, 100], [-5, -5], 'c-', lw=3, alpha=0.8)
    # End caps
    ax.plot([0, 0], [-5, 5], 'c-', lw=3, alpha=0.8)
    ax.plot([100, 100], [-5, 5], 'c-', lw=3, alpha=0.8)

    # Draw tubulin dimers along length
    n_dimers = 12
    for i in range(n_dimers):
        x = 4 + i * 8
        # Alpha tubulin (top)
        alpha = Circle((x, 3), 2.5, fill=True, facecolor='#51cf66', alpha=0.7)
        ax.add_patch(alpha)
        # Beta tubulin (bottom)
        beta = Circle((x, -3), 2.5, fill=True, facecolor='#4facfe', alpha=0.7)
        ax.add_patch(beta)

    # Draw coherence wave pattern (representing quantum state)
    x_wave = np.linspace(0, 100, 500)
    # Coherent oscillation
    y_wave = 0.8 * np.sin(2 * np.pi * x_wave / 20) * np.exp(-((x_wave - 50)**2) / 2000)

    # Multiple overlapping waves for quantum superposition effect
    for offset in [-0.3, 0, 0.3]:
        ax.plot(x_wave, y_wave + offset, color='#9b59b6', alpha=0.5, lw=2)

    # Draw 12 sampling gates along the microtubule
    gate_positions = np.linspace(8, 92, 12)
    pair_colors = ['#ff7eb6', '#ff7eb6', '#ff7eb6',  # Dice 1
                   '#ffd43b', '#ffd43b', '#ffd43b',  # Dice 2
                   '#8b7fff', '#8b7fff', '#8b7fff',  # Dice 3
                   '#50c878', '#50c878', '#50c878']  # Dice 4

    for i, (pos, color) in enumerate(zip(gate_positions, pair_colors)):
        # Vertical gate line
        ax.plot([pos, pos], [-6, 6], color=color, lw=2, alpha=0.7)

        # Glowing gate marker
        glow = Circle((pos, 0), 1.2, fill=True, facecolor=color,
                     alpha=0.4, edgecolor='none')
        ax.add_patch(glow)

        core = Circle((pos, 0), 0.6, fill=True, facecolor='white',
                     alpha=0.9, edgecolor=color, linewidth=1)
        ax.add_patch(core)

        # Pair number
        ax.text(pos, -7.5, str(i + 1), fontsize=8, color=color,
               ha='center', va='center', fontweight='bold')

    # Add dimension annotations
    ax.annotate('', xy=(100, -8), xytext=(0, -8),
                arrowprops=dict(arrowstyle='<->', color='white', lw=1))
    ax.text(50, -9, '~25 micrometers (typical MT length)', fontsize=9,
           color='white', ha='center', va='center')

    # Coherence region indicator
    ax.fill_between(x_wave, -6, 6,
                   where=(x_wave > 20) & (x_wave < 80),
                   alpha=0.1, color='#9b59b6')
    ax.text(50, 7.5, 'Quantum coherent region', fontsize=10,
           color='#9b59b6', ha='center', va='center', style='italic')

    # Legend
    custom_legend = [
        Line2D([0], [0], color='#9b59b6', lw=2, label='Coherent wavefunction'),
        Line2D([0], [0], marker='o', color='w', markerfacecolor='#51cf66',
               markersize=10, label='Alpha tubulin'),
        Line2D([0], [0], marker='o', color='w', markerfacecolor='#4facfe',
               markersize=10, label='Beta tubulin'),
        Line2D([0], [0], marker='|', color='#ff7eb6', markersize=10,
               lw=0, label='(2,0) sampling gates'),
    ]
    ax.legend(handles=custom_legend, loc='upper right',
             facecolor='#1a1a2e', edgecolor='#4facfe',
             fontsize=9, labelcolor='white')

    ax.axis('off')

    plt.tight_layout()
    output_path = os.path.join(OUTPUT_DIR, 'microtubule_longitudinal_v22.png')
    plt.savefig(output_path, dpi=150, bbox_inches='tight', facecolor='#0a0a14')
    plt.close()
    print(f"Saved: {output_path}")
    return output_path


def create_pair_mandala():
    """
    Create mandala visualization of 12 (2,0) pairs arranged geometrically.
    Shows the 4-dice grouping for OR4Dice consciousness sampling.
    """
    fig, ax = plt.subplots(1, 1, figsize=(12, 12))
    ax.set_xlim(-1.5, 1.5)
    ax.set_ylim(-1.5, 1.5)
    ax.set_aspect('equal')
    ax.set_facecolor('#0a0a14')
    fig.patch.set_facecolor('#0a0a14')

    # Title
    ax.set_title('12 (2,0) Bridge Pairs: Consciousness Sampling Mandala\n'
                 'Principia Metaphysica v22.2 - 4 Dice Grouping',
                 fontsize=14, fontweight='bold', color='white', pad=20)

    # Central Euclidean bridge symbol
    bridge = Circle((0, 0), 0.15, fill=True, facecolor='#9b59b6',
                   edgecolor='white', linewidth=2)
    ax.add_patch(bridge)
    ax.text(0, 0, 'B', fontsize=12, color='white', ha='center', va='center',
           fontweight='bold')

    # Draw 12 pairs in 4 groups
    pair_colors = ['#ff7eb6', '#ffd43b', '#8b7fff', '#50c878']
    dice_labels = ['Dice 1', 'Dice 2', 'Dice 3', 'Dice 4']

    outer_radius = 1.0
    inner_radius = 0.6

    for dice_idx in range(4):
        base_angle = 2 * np.pi * dice_idx / 4 - np.pi / 4  # Rotate by 45 deg
        color = pair_colors[dice_idx]

        # Draw dice arc (wedge)
        wedge = Wedge((0, 0), outer_radius + 0.25, np.degrees(base_angle) - 40,
                     np.degrees(base_angle) + 40, width=0.1,
                     facecolor=color, alpha=0.2, edgecolor=color, linewidth=1)
        ax.add_patch(wedge)

        # Dice label
        label_angle = base_angle
        label_r = outer_radius + 0.35
        ax.text(label_r * np.cos(label_angle), label_r * np.sin(label_angle),
               dice_labels[dice_idx], fontsize=10, color=color,
               ha='center', va='center', fontweight='bold')

        for pair_idx in range(3):
            pair_num = dice_idx * 3 + pair_idx
            angle = base_angle + (pair_idx - 1) * 0.35  # Spread within dice

            # Alternating radii for visual interest
            if pair_idx == 1:
                radius = outer_radius
            else:
                radius = inner_radius + 0.1 * (pair_idx % 2)

            x = radius * np.cos(angle)
            y = radius * np.sin(angle)

            # Connection line to center
            ax.plot([0, x * 0.9], [0, y * 0.9], color=color, alpha=0.3, lw=1)

            # Outer glow
            glow1 = Circle((x, y), 0.12, fill=True, facecolor=color, alpha=0.3)
            ax.add_patch(glow1)

            # Middle glow
            glow2 = Circle((x, y), 0.08, fill=True, facecolor=color, alpha=0.5)
            ax.add_patch(glow2)

            # Inner core
            core = Circle((x, y), 0.04, fill=True, facecolor='white', alpha=1.0)
            ax.add_patch(core)

            # Pair number
            num_x = (radius + 0.18) * np.cos(angle)
            num_y = (radius + 0.18) * np.sin(angle)
            ax.text(num_x, num_y, str(pair_num + 1), fontsize=9, color=color,
                   ha='center', va='center', fontweight='bold')

    # Draw interconnecting arcs between pairs
    for i in range(12):
        angle1 = 2 * np.pi * i / 12 - np.pi / 4
        angle2 = 2 * np.pi * ((i + 1) % 12) / 12 - np.pi / 4

        # Curved connection
        arc_angles = np.linspace(angle1, angle2, 20)
        arc_x = 0.45 * np.cos(arc_angles)
        arc_y = 0.45 * np.sin(arc_angles)
        ax.plot(arc_x, arc_y, color='#9b59b6', alpha=0.3, lw=1)

    # Golden ratio annotation
    ax.text(0, -1.35, f'Bridge period: L = 2$\\pi\\sqrt{{\\phi}}$ ({2 * np.pi * np.sqrt(PHI):.2f})',
           fontsize=10, color='#9b59b6', ha='center', va='center')

    # OR operator annotation
    ax.text(1.2, -1.2, r'$R_\perp = \begin{pmatrix} 0 & -1 \\ 1 & 0 \end{pmatrix}$',
           fontsize=10, color='cyan', ha='center', va='center',
           bbox=dict(boxstyle='round', facecolor='#1a1a2e', edgecolor='cyan', alpha=0.8))

    ax.axis('off')

    plt.tight_layout()
    output_path = os.path.join(OUTPUT_DIR, 'pair_mandala_v22.png')
    plt.savefig(output_path, dpi=150, bbox_inches='tight', facecolor='#0a0a14')
    plt.close()
    print(f"Saved: {output_path}")
    return output_path


def create_shielding_diagram():
    """
    Create diagram showing pair shielding effect on decoherence.
    """
    fig, ax = plt.subplots(1, 1, figsize=(12, 8))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 8)
    ax.set_facecolor('#0a0a14')
    fig.patch.set_facecolor('#0a0a14')

    # Title
    ax.set_title('Pair Shielding: Geometric Protection from Decoherence\n'
                 'Principia Metaphysica v22.2',
                 fontsize=14, fontweight='bold', color='white', pad=15)

    # Draw three scenarios side by side

    # Scenario 1: No shielding (Tegmark regime)
    ax.add_patch(FancyBboxPatch((0.5, 4.5), 3, 3, boxstyle="round,pad=0.1",
                                facecolor='#2c3e50', edgecolor='#ff6b6b', linewidth=2))
    ax.text(2, 7.2, 'No Shielding', fontsize=11, color='#ff6b6b',
           ha='center', va='center', fontweight='bold')
    ax.text(2, 6.5, '(Tegmark 2000)', fontsize=9, color='#adb5bd', ha='center')

    # Decoherence arrows (many, aggressive)
    for i in range(8):
        angle = np.random.uniform(0, 2 * np.pi)
        start_x = 2 + 1.2 * np.cos(angle)
        start_y = 5.5 + 1.0 * np.sin(angle)
        ax.annotate('', xy=(2, 5.5), xytext=(start_x, start_y),
                   arrowprops=dict(arrowstyle='->', color='#ff6b6b', lw=1, alpha=0.7))

    ax.text(2, 4.8, r'$\tau \sim 10^{-13}$ s', fontsize=9, color='#ff6b6b', ha='center')

    # Scenario 2: 6 pairs (baseline)
    ax.add_patch(FancyBboxPatch((4.5, 4.5), 3, 3, boxstyle="round,pad=0.1",
                                facecolor='#2c3e50', edgecolor='#ffd43b', linewidth=2))
    ax.text(6, 7.2, '6 Pairs (Baseline)', fontsize=11, color='#ffd43b',
           ha='center', va='center', fontweight='bold')

    # Partial shield
    shield_angles = np.linspace(-np.pi/3, np.pi/3, 6)
    for angle in shield_angles:
        x = 6 + 1.0 * np.cos(angle)
        y = 5.5 + 0.8 * np.sin(angle)
        ax.plot([6, x], [5.5, y], color='#ffd43b', lw=2, alpha=0.5)

    # Some decoherence gets through
    for i in range(4):
        angle = np.random.uniform(np.pi/3, 5*np.pi/3)
        start_x = 6 + 1.2 * np.cos(angle)
        start_y = 5.5 + 1.0 * np.sin(angle)
        ax.annotate('', xy=(6, 5.5), xytext=(start_x, start_y),
                   arrowprops=dict(arrowstyle='->', color='#ff6b6b', lw=1, alpha=0.4))

    ax.text(6, 4.8, r'$\tau \sim 10^{-9}$ s', fontsize=9, color='#ffd43b', ha='center')

    # Scenario 3: 12 pairs (full gnosis)
    ax.add_patch(FancyBboxPatch((8.5, 4.5), 3, 3, boxstyle="round,pad=0.1",
                                facecolor='#2c3e50', edgecolor='#50c878', linewidth=2))
    ax.text(10, 7.2, '12 Pairs (Gnosis)', fontsize=11, color='#50c878',
           ha='center', va='center', fontweight='bold')

    # Full shield
    shield_angles = np.linspace(0, 2*np.pi, 12, endpoint=False)
    for angle in shield_angles:
        x = 10 + 1.0 * np.cos(angle)
        y = 5.5 + 0.8 * np.sin(angle)
        ax.plot([10, x], [5.5, y], color='#50c878', lw=2, alpha=0.7)
        # Glowing point
        glow = Circle((x, y), 0.1, fill=True, facecolor='#50c878', alpha=0.6)
        ax.add_patch(glow)

    ax.text(10, 4.8, r'$\tau > 10$ ms', fontsize=9, color='#50c878',
           ha='center', fontweight='bold')

    # Formula box at bottom
    ax.add_patch(FancyBboxPatch((1, 0.5), 10, 2.5, boxstyle="round,pad=0.1",
                                facecolor='#1a1a2e', edgecolor='#8b7fff', linewidth=2))

    ax.text(6, 2.5, 'Pair Shielding Formula', fontsize=11, color='#8b7fff',
           ha='center', va='center', fontweight='bold')

    formula = r'$\tau = \tau_0 \cdot \exp\left(k \sqrt{\frac{n}{12}}\right) \cdot \left(\frac{n}{6}\right)^2$'
    ax.text(6, 1.7, formula, fontsize=14, color='white', ha='center', va='center')

    ax.text(6, 0.9, r'$\tau_0 = 25$ fs (Penrose timescale), $k = 2.5$ (shielding coefficient)',
           fontsize=9, color='#adb5bd', ha='center', va='center')

    ax.axis('off')

    plt.tight_layout()
    output_path = os.path.join(OUTPUT_DIR, 'pair_shielding_diagram_v22.png')
    plt.savefig(output_path, dpi=150, bbox_inches='tight', facecolor='#0a0a14')
    plt.close()
    print(f"Saved: {output_path}")
    return output_path


if __name__ == "__main__":
    print("=== Generating Microtubule 12-Pair Visualizations v22.2 ===")
    print()

    create_microtubule_cross_section()
    create_microtubule_longitudinal_view()
    create_pair_mandala()
    create_shielding_diagram()

    print()
    print("All microtubule visualizations generated successfully!")
