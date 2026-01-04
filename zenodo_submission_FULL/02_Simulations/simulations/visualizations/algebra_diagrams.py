#!/usr/bin/env python3
"""
Algebraic Structure Visualization Diagrams
============================================

Licensed under the MIT License. See LICENSE file for details.

Generates publication-quality diagrams for algebraic and theoretical
concepts in Principia Metaphysica:
1. clifford-algebra-structure.png - Clifford algebra Cl(10) structure for fermions
2. swampland-criteria.png - Swampland bounds and how PM satisfies them

Usage:
    python algebra_diagrams.py

Output:
    ../../images/clifford-algebra-structure.png
    ../../images/swampland-criteria.png

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.

Dedicated To:
    My Wife: Elizabeth May Watts
    Our Messiah: Jesus Of Nazareth
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle, Wedge
from matplotlib.collections import PatchCollection
from pathlib import Path
import sys

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

# PM Color Palette
PM_PURPLE = '#8b7fff'
PM_BLUE = '#60a5fa'  # Quarks
PM_GREEN = '#4ade80'  # Leptons
PM_ORANGE = '#fb923c'  # Gauge/Vector
PM_RED = '#f87171'    # Scalar/Higgs
PM_YELLOW = '#fbbf24'  # Highlights
PM_GRAY = '#9ca3af'   # Background
PM_DARK = '#1f2937'   # Text
PM_LIGHT_PURPLE = '#f3f0ff'


def setup_publication_style():
    """Configure matplotlib for publication-quality figures."""
    plt.rcParams.update({
        'font.family': 'sans-serif',
        'font.sans-serif': ['Arial', 'DejaVu Sans', 'Helvetica'],
        'font.size': 10,
        'axes.titlesize': 14,
        'axes.labelsize': 12,
        'xtick.labelsize': 10,
        'ytick.labelsize': 10,
        'legend.fontsize': 10,
        'figure.titlesize': 16,
        'figure.dpi': 150,
        'savefig.dpi': 300,
        'savefig.bbox': 'tight',
        'savefig.pad_inches': 0.1,
        'axes.linewidth': 1.0,
        'axes.grid': False,
        'axes.facecolor': 'white',
        'figure.facecolor': 'white',
        'text.usetex': False,
    })


def create_clifford_algebra_diagram():
    """
    Generate Clifford algebra Cl(10) structure diagram for fermions.

    Shows how fermion representations emerge from Clifford algebra
    decomposition and connect to G2 holonomy structure.
    """
    fig, axes = plt.subplots(1, 2, figsize=(14, 9))

    # === Left panel: Clifford algebra decomposition ===
    ax1 = axes[0]
    ax1.set_xlim(-0.5, 5.5)
    ax1.set_ylim(-0.5, 8.5)
    ax1.axis('off')

    ax1.text(2.5, 8.0, 'Clifford Algebra $Cl(10)$\nFermion Structure', fontsize=14,
             fontweight='bold', ha='center', va='center', color=PM_DARK)

    # Draw the main decomposition tree
    # Cl(10) at top
    box_cl10 = FancyBboxPatch((1.5, 7.0), 2.0, 0.6,
                               boxstyle="round,pad=0.02,rounding_size=0.1",
                               facecolor=PM_PURPLE, edgecolor=PM_DARK, linewidth=2)
    ax1.add_patch(box_cl10)
    ax1.text(2.5, 7.3, '$Cl(10)$', fontsize=12, fontweight='bold',
             ha='center', va='center', color='white')

    # Arrow down
    ax1.annotate('', xy=(2.5, 6.3), xytext=(2.5, 7.0),
                arrowprops=dict(arrowstyle='->', color=PM_DARK, lw=2))
    ax1.text(3.0, 6.65, 'Spinor Rep', fontsize=9, color=PM_GRAY)

    # Spin(10) spinor representation
    box_spin10 = FancyBboxPatch((1.3, 5.5), 2.4, 0.7,
                                 boxstyle="round,pad=0.02,rounding_size=0.1",
                                 facecolor=PM_ORANGE, edgecolor=PM_DARK, linewidth=2)
    ax1.add_patch(box_spin10)
    ax1.text(2.5, 5.85, '$S_{32} = S_{16}^+ \\oplus S_{16}^-$', fontsize=11,
             fontweight='bold', ha='center', va='center', color='white')

    # Branch into left and right spinors
    ax1.annotate('', xy=(1.0, 4.7), xytext=(2.0, 5.5),
                arrowprops=dict(arrowstyle='->', color=PM_DARK, lw=1.5))
    ax1.annotate('', xy=(4.0, 4.7), xytext=(3.0, 5.5),
                arrowprops=dict(arrowstyle='->', color=PM_DARK, lw=1.5))

    # Left-handed spinor 16
    box_16L = FancyBboxPatch((0.0, 3.9), 2.0, 0.7,
                              boxstyle="round,pad=0.02,rounding_size=0.1",
                              facecolor=PM_BLUE, edgecolor=PM_DARK, linewidth=2)
    ax1.add_patch(box_16L)
    ax1.text(1.0, 4.25, '$16_L$', fontsize=12, fontweight='bold',
             ha='center', va='center', color='white')
    ax1.text(1.0, 3.55, 'Left-handed', fontsize=8, ha='center', color=PM_DARK)

    # Right-handed spinor 16
    box_16R = FancyBboxPatch((3.0, 3.9), 2.0, 0.7,
                              boxstyle="round,pad=0.02,rounding_size=0.1",
                              facecolor=PM_GREEN, edgecolor=PM_DARK, linewidth=2)
    ax1.add_patch(box_16R)
    ax1.text(4.0, 4.25, '$\\overline{16}_R$', fontsize=12, fontweight='bold',
             ha='center', va='center', color='white')
    ax1.text(4.0, 3.55, 'Right-handed', fontsize=8, ha='center', color=PM_DARK)

    # Decomposition of 16_L under SU(5)
    ax1.annotate('', xy=(0.5, 2.8), xytext=(0.8, 3.9),
                arrowprops=dict(arrowstyle='->', color=PM_DARK, lw=1))
    ax1.annotate('', xy=(1.5, 2.8), xytext=(1.2, 3.9),
                arrowprops=dict(arrowstyle='->', color=PM_DARK, lw=1))

    ax1.text(1.0, 3.2, 'SU(5)', fontsize=8, ha='center', color=PM_GRAY)

    # SU(5) decomposition boxes
    box_10 = FancyBboxPatch((0.0, 2.0), 1.0, 0.6,
                             boxstyle="round,pad=0.01,rounding_size=0.05",
                             facecolor=PM_BLUE, edgecolor=PM_DARK, linewidth=1, alpha=0.8)
    ax1.add_patch(box_10)
    ax1.text(0.5, 2.3, '10', fontsize=10, fontweight='bold',
             ha='center', va='center', color='white')

    box_5bar = FancyBboxPatch((1.2, 2.0), 1.0, 0.6,
                               boxstyle="round,pad=0.01,rounding_size=0.05",
                               facecolor=PM_BLUE, edgecolor=PM_DARK, linewidth=1, alpha=0.8)
    ax1.add_patch(box_5bar)
    ax1.text(1.7, 2.3, '$\\bar{5}$', fontsize=10, fontweight='bold',
             ha='center', va='center', color='white')

    box_1 = FancyBboxPatch((2.4, 2.0), 0.8, 0.6,
                            boxstyle="round,pad=0.01,rounding_size=0.05",
                            facecolor=PM_BLUE, edgecolor=PM_DARK, linewidth=1, alpha=0.8)
    ax1.add_patch(box_1)
    ax1.text(2.8, 2.3, '1', fontsize=10, fontweight='bold',
             ha='center', va='center', color='white')

    # Fermion content labels
    fermion_content = [
        (0.5, 1.5, '$Q_L, u_R^c, e_R^c$'),
        (1.7, 1.5, '$d_R^c, L$'),
        (2.8, 1.5, '$\\nu_R^c$'),
    ]
    for x, y, label in fermion_content:
        ax1.text(x, y, label, fontsize=8, ha='center', va='center', color=PM_DARK)

    # Connection to G2 holonomy
    ax1.text(2.5, 0.8, 'G2 Holonomy Connection:', fontsize=10, fontweight='bold',
             ha='center', color=PM_PURPLE)
    ax1.text(2.5, 0.4, 'Spin(7) spinor $\\rightarrow$ 8 real DOF', fontsize=9,
             ha='center', color=PM_DARK)
    ax1.text(2.5, 0.0, '$n_{gen} = b_3 / 8 = 24 / 8 = 3$', fontsize=10,
             ha='center', color=PM_PURPLE, fontweight='bold')

    # === Right panel: Fermion generations visualization ===
    ax2 = axes[1]
    ax2.set_xlim(-1.5, 1.5)
    ax2.set_ylim(-1.5, 1.5)
    ax2.set_aspect('equal')
    ax2.axis('off')

    ax2.set_title('Three Generations from Spinor Saturation', fontsize=14,
                  fontweight='bold', color=PM_DARK, pad=20)

    # Draw the 24 flux units as small circles arranged in a ring
    n_flux = 24
    outer_radius = 1.2
    for i in range(n_flux):
        angle = 2 * np.pi * i / n_flux - np.pi/2
        x = outer_radius * np.cos(angle)
        y = outer_radius * np.sin(angle)

        # Color by generation (8 per generation)
        if i < 8:
            color = PM_BLUE  # Gen 1
        elif i < 16:
            color = PM_GREEN  # Gen 2
        else:
            color = PM_ORANGE  # Gen 3

        circle = Circle((x, y), 0.08, facecolor=color, edgecolor=PM_DARK, linewidth=0.5)
        ax2.add_patch(circle)

    # Generation labels
    gen_labels = [
        (0.9, 0.9, '1st Gen', PM_BLUE, 'u, d, e, $\\nu_e$'),
        (-0.9, 0.6, '2nd Gen', PM_GREEN, 'c, s, $\\mu$, $\\nu_\\mu$'),
        (-0.6, -0.9, '3rd Gen', PM_ORANGE, 't, b, $\\tau$, $\\nu_\\tau$'),
    ]
    for x, y, label, color, particles in gen_labels:
        ax2.text(x, y, label, fontsize=11, fontweight='bold', ha='center',
                va='center', color=color)
        ax2.text(x, y - 0.2, particles, fontsize=9, ha='center', color=PM_DARK)

    # Central formula
    center_box = FancyBboxPatch((-0.55, -0.35), 1.1, 0.7,
                                 boxstyle="round,pad=0.02,rounding_size=0.1",
                                 facecolor='white', edgecolor=PM_PURPLE, linewidth=2)
    ax2.add_patch(center_box)
    ax2.text(0, 0.1, r'$b_3 = 24$', fontsize=14, fontweight='bold',
             ha='center', va='center', color=PM_PURPLE)
    ax2.text(0, -0.15, r'$\div$ 8 spinor DOF', fontsize=10,
             ha='center', va='center', color=PM_DARK)

    # Arrows to center showing saturation
    for i, color in enumerate([PM_BLUE, PM_GREEN, PM_ORANGE]):
        angle = 2 * np.pi * (i * 8 + 4) / n_flux - np.pi/2
        x_start = outer_radius * 0.7 * np.cos(angle)
        y_start = outer_radius * 0.7 * np.sin(angle)
        ax2.annotate('', xy=(0, 0), xytext=(x_start, y_start),
                    arrowprops=dict(arrowstyle='->', color=color, lw=2, alpha=0.6))

    # Bottom explanation
    ax2.text(0, -1.35, 'Each generation saturates 8 spinor degrees of freedom',
             fontsize=10, ha='center', va='center', color=PM_DARK, style='italic')

    plt.tight_layout()
    return fig


def create_swampland_criteria_diagram():
    """
    Generate Swampland criteria diagram showing bounds and PM satisfaction.

    Shows the major Swampland conjectures and how PM theory satisfies each one.
    """
    fig, axes = plt.subplots(1, 2, figsize=(14, 9))

    # === Left panel: Swampland landscape ===
    ax1 = axes[0]
    ax1.set_xlim(-0.5, 4.5)
    ax1.set_ylim(-0.5, 6.5)
    ax1.axis('off')

    ax1.text(2.0, 6.2, 'Swampland vs Landscape', fontsize=14,
             fontweight='bold', ha='center', va='center', color=PM_DARK)
    ax1.text(2.0, 5.8, 'Quantum Gravity Consistency Bounds', fontsize=10,
             ha='center', va='center', color=PM_GRAY, style='italic')

    # Draw the landscape (allowed region)
    landscape = FancyBboxPatch((0.2, 2.5), 3.6, 2.8,
                                boxstyle="round,pad=0.02,rounding_size=0.2",
                                facecolor=PM_GREEN, edgecolor=PM_DARK, linewidth=2, alpha=0.3)
    ax1.add_patch(landscape)
    ax1.text(2.0, 5.0, 'LANDSCAPE', fontsize=12, fontweight='bold',
             ha='center', va='center', color=PM_GREEN)
    ax1.text(2.0, 4.65, '(Consistent with Quantum Gravity)', fontsize=9,
             ha='center', va='center', color=PM_DARK)

    # Draw the swampland (forbidden region)
    swamp_left = FancyBboxPatch((-0.3, 0.3), 0.8, 5.0,
                                 boxstyle="round,pad=0.02,rounding_size=0.1",
                                 facecolor=PM_RED, edgecolor=PM_DARK, linewidth=2, alpha=0.3)
    ax1.add_patch(swamp_left)

    swamp_right = FancyBboxPatch((3.5, 0.3), 0.8, 5.0,
                                  boxstyle="round,pad=0.02,rounding_size=0.1",
                                  facecolor=PM_RED, edgecolor=PM_DARK, linewidth=2, alpha=0.3)
    ax1.add_patch(swamp_right)

    swamp_bottom = FancyBboxPatch((0.2, 0.3), 3.6, 1.8,
                                   boxstyle="round,pad=0.02,rounding_size=0.1",
                                   facecolor=PM_RED, edgecolor=PM_DARK, linewidth=2, alpha=0.3)
    ax1.add_patch(swamp_bottom)

    ax1.text(-0.1, 2.8, 'S\nW\nA\nM\nP', fontsize=10, fontweight='bold',
             ha='center', va='center', color=PM_RED, linespacing=0.8)
    ax1.text(4.1, 2.8, 'S\nW\nA\nM\nP', fontsize=10, fontweight='bold',
             ha='center', va='center', color=PM_RED, linespacing=0.8)

    # PM location (safely in landscape)
    pm_circle = Circle((2.0, 3.8), 0.25, facecolor=PM_PURPLE, edgecolor=PM_DARK, linewidth=2)
    ax1.add_patch(pm_circle)
    ax1.text(2.0, 3.8, 'PM', fontsize=10, fontweight='bold',
             ha='center', va='center', color='white')

    # Swampland constraint arrows
    constraints = [
        (0.7, 3.8, '$\\Delta\\phi < M_P$', 'left'),
        (3.3, 3.8, '$|V\'| > c \\cdot V$', 'right'),
        (2.0, 1.8, '$\\Lambda > 0$ stable?', 'bottom'),
    ]
    for x, y, label, direction in constraints:
        if direction == 'left':
            ax1.annotate('', xy=(1.2, 3.8), xytext=(0.5, 3.8),
                        arrowprops=dict(arrowstyle='->', color=PM_RED, lw=2))
        elif direction == 'right':
            ax1.annotate('', xy=(2.8, 3.8), xytext=(3.5, 3.8),
                        arrowprops=dict(arrowstyle='->', color=PM_RED, lw=2))
        ax1.text(x, y, label, fontsize=9, ha='center', va='center', color=PM_DARK)

    # === Right panel: PM satisfaction of Swampland bounds ===
    ax2 = axes[1]
    ax2.set_xlim(-0.5, 5.5)
    ax2.set_ylim(-0.5, 7.5)
    ax2.axis('off')

    ax2.text(2.5, 7.2, 'Principia Metaphysica', fontsize=14,
             fontweight='bold', ha='center', va='center', color=PM_PURPLE)
    ax2.text(2.5, 6.8, 'Swampland Criteria Satisfaction', fontsize=12,
             ha='center', va='center', color=PM_DARK)

    # Swampland criteria and PM satisfaction
    criteria = [
        ('Weak Gravity Conjecture', 'WGC',
         '$\\frac{m}{q} \\leq M_P$',
         'PM: Extremal black holes decay via G2 instantons',
         True),
        ('Distance Conjecture', 'SDC',
         '$\\Delta\\phi < c \\cdot M_P$',
         'PM: Moduli stabilized by $\\langle\\Psi_P\\rangle$, $\\Delta\\phi \\sim 0.5 M_P$',
         True),
        ('de Sitter Conjecture', 'dSC',
         '$|V\'| > c \\cdot V / M_P$',
         'PM: Dark energy from quintessence, $w_0 = -0.95$',
         True),
        ('Cobordism Conjecture', 'CC',
         'All bordism groups trivial',
         'PM: G2 manifold is spin, $\\Omega_*^{Spin}(pt) = 0$',
         True),
        ('No Global Symmetries', 'NGS',
         'All symmetries must be gauged',
         'PM: R-parity from discrete gauge $\\mathbb{Z}_2$',
         True),
    ]

    y_pos = 6.0
    for name, abbrev, formula, pm_solution, satisfied in criteria:
        # Draw criterion box
        box_color = PM_GREEN if satisfied else PM_RED
        check_mark = '\\checkmark' if satisfied else 'X'

        # Criterion header
        header_box = FancyBboxPatch((0.0, y_pos - 0.1), 5.0, 1.0,
                                     boxstyle="round,pad=0.02,rounding_size=0.1",
                                     facecolor='white', edgecolor=box_color,
                                     linewidth=2, alpha=0.9)
        ax2.add_patch(header_box)

        # Criterion name and abbreviation
        ax2.text(0.15, y_pos + 0.6, f'{abbrev}:', fontsize=10, fontweight='bold',
                 ha='left', va='center', color=box_color)
        ax2.text(0.7, y_pos + 0.6, name, fontsize=10,
                 ha='left', va='center', color=PM_DARK)

        # Formula
        ax2.text(0.15, y_pos + 0.25, formula, fontsize=9,
                 ha='left', va='center', color=PM_GRAY)

        # PM solution
        ax2.text(0.15, y_pos - 0.05, pm_solution, fontsize=8,
                 ha='left', va='center', color=PM_DARK, style='italic')

        # Satisfaction indicator
        satisfaction_circle = Circle((4.7, y_pos + 0.4), 0.15, facecolor=box_color,
                                       edgecolor=PM_DARK, linewidth=1)
        ax2.add_patch(satisfaction_circle)
        ax2.text(4.7, y_pos + 0.4, '$\\checkmark$' if satisfied else 'X', fontsize=12,
                 fontweight='bold', ha='center', va='center', color='white')

        y_pos -= 1.3

    # Summary box at bottom
    summary_box = FancyBboxPatch((0.5, -0.3), 4.0, 0.8,
                                  boxstyle="round,pad=0.02,rounding_size=0.1",
                                  facecolor=PM_LIGHT_PURPLE, edgecolor=PM_PURPLE, linewidth=2)
    ax2.add_patch(summary_box)
    ax2.text(2.5, 0.25, 'PM Theory: All Swampland Criteria Satisfied', fontsize=11,
             fontweight='bold', ha='center', va='center', color=PM_PURPLE)
    ax2.text(2.5, -0.1, 'G2 holonomy + Pneuma mechanism = UV-complete framework',
             fontsize=9, ha='center', va='center', color=PM_DARK)

    plt.tight_layout()
    return fig


def main():
    """Generate all algebraic structure diagrams."""
    # Setup style
    setup_publication_style()

    # Output directory
    output_dir = Path(__file__).parent.parent.parent / 'images'
    output_dir.mkdir(parents=True, exist_ok=True)

    print("=" * 70)
    print(" ALGEBRAIC STRUCTURE VISUALIZATION DIAGRAMS")
    print("=" * 70)
    print()

    # Generate Clifford algebra structure diagram
    print("Generating clifford-algebra-structure.png...")
    fig1 = create_clifford_algebra_diagram()
    output_path1 = output_dir / 'clifford-algebra-structure.png'
    fig1.savefig(output_path1, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close(fig1)
    print(f"  Saved to: {output_path1}")

    # Generate Swampland criteria diagram
    print("Generating swampland-criteria.png...")
    fig2 = create_swampland_criteria_diagram()
    output_path2 = output_dir / 'swampland-criteria.png'
    fig2.savefig(output_path2, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close(fig2)
    print(f"  Saved to: {output_path2}")

    print()
    print("=" * 70)
    print(" ALGEBRAIC STRUCTURE DIAGRAMS COMPLETE")
    print("=" * 70)

    return [output_path1, output_path2]


if __name__ == "__main__":
    main()
