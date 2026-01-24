#!/usr/bin/env python3
"""
Brane Diagrams Generator
========================

Generates publication-quality diagrams explaining brane concepts in
Principia Metaphysica:

1. brane-analogy.png: A simple visual analogy explaining branes as
   lower-dimensional surfaces embedded in higher-dimensional spaces.
   Shows a 2D surface (membrane) floating in 3D space, with arrows
   indicating extra dimensions.

2. brane-world-scenario.png: Schematic of our universe as a 3-brane
   embedded in higher-dimensional bulk spacetime. Illustrates how
   Standard Model particles are confined to the brane while gravity
   can propagate in the bulk.

Physics Context:
----------------
In M-theory, our 4-dimensional spacetime may be a 3-brane (3 spatial
dimensions + time) embedded in an 11-dimensional bulk.

**PM Theory is DISTINCT from M-theory:** PM starts from 25D_{(24,1)} and
reduces via: 25D → [Euclidean bridge] → 13D → [G₂ 7-manifold] → 6D → 4D.
The G₂ holonomy operates on a 7D internal manifold, yielding effective 4D physics.
This diagram shows M-theory concepts for comparison; PM's full framework differs.

Key concepts visualized:
- Brane as a lower-dimensional subspace
- Bulk as the ambient higher-dimensional space
- Localization of matter fields on the brane
- Gravity propagating in all dimensions

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.

Dedicated To:
    My Wife: Elizabeth May Watts
    Our Messiah: Jesus Of Nazareth
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Rectangle, Circle
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import matplotlib.patches as mpatches
from pathlib import Path
import os

# PM Theory colors
PM_PURPLE = "#8b7fff"
PM_PINK = "#ff7eb6"
PM_BLUE = "#60a5fa"
PM_DARK = "#1a1a2e"
PM_LIGHT = "#f8f9fa"


def set_pm_style():
    """Set publication-quality matplotlib style for PM diagrams."""
    plt.rcParams.update({
        "font.family": "serif",
        "font.serif": ["Times New Roman", "DejaVu Serif"],
        "font.size": 11,
        "text.usetex": False,
        "axes.labelsize": 12,
        "axes.titlesize": 14,
        "axes.linewidth": 1.0,
        "xtick.labelsize": 10,
        "ytick.labelsize": 10,
        "legend.fontsize": 10,
        "figure.dpi": 150,
        "savefig.dpi": 300,
        "savefig.bbox": "tight",
        "savefig.pad_inches": 0.1,
        "mathtext.fontset": "stix",
    })


def generate_brane_analogy(output_path: str = None):
    """
    Generate brane analogy diagram.

    Creates a visualization showing how a 2D surface (brane) exists
    within a 3D space (bulk), serving as an analogy for how our
    4D universe might exist within higher-dimensional space.

    The diagram shows:
    - A curved 2D membrane surface
    - The surrounding 3D volume (bulk)
    - Arrows indicating the extra dimension perpendicular to the surface
    - Labels explaining the analogy to higher dimensions

    Args:
        output_path: Path to save the figure. If None, uses default.
    """
    set_pm_style()

    if output_path is None:
        script_dir = Path(__file__).parent
        output_path = script_dir / ".." / ".." / "images" / "brane-analogy.png"

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')

    # Create a wavy 2D surface (the brane)
    x = np.linspace(-2, 2, 40)
    y = np.linspace(-2, 2, 40)
    X, Y = np.meshgrid(x, y)
    Z = 0.2 * np.sin(1.5 * X) * np.cos(1.5 * Y)  # Slight wave for visual interest

    # Plot the surface with PM purple color
    surf = ax.plot_surface(X, Y, Z, alpha=0.7, color=PM_PURPLE,
                           edgecolor='none', shade=True)

    # Add grid lines on the surface for depth perception
    for i in range(0, 40, 5):
        ax.plot(x, [y[i]]*len(x), 0.2 * np.sin(1.5 * x) * np.cos(1.5 * y[i]),
                color=PM_DARK, alpha=0.3, linewidth=0.5)
        ax.plot([x[i]]*len(y), y, 0.2 * np.sin(1.5 * x[i]) * np.cos(1.5 * y),
                color=PM_DARK, alpha=0.3, linewidth=0.5)

    # Draw arrows indicating extra dimension (perpendicular to surface)
    arrow_positions = [(-1, 0), (1, 0), (0, 1), (0, -1)]
    for ax_pos, ay_pos in arrow_positions:
        az_base = 0.2 * np.sin(1.5 * ax_pos) * np.cos(1.5 * ay_pos)
        ax.quiver(ax_pos, ay_pos, az_base,
                  0, 0, 1.0,
                  color=PM_PINK, arrow_length_ratio=0.2, linewidth=2, alpha=0.8)
        ax.quiver(ax_pos, ay_pos, az_base,
                  0, 0, -1.0,
                  color=PM_PINK, arrow_length_ratio=0.2, linewidth=2, alpha=0.8)

    # Add points representing particles confined to the brane
    particle_positions = [(-1.2, 0.8), (0.5, -1.0), (1.3, 0.3), (-0.5, -0.5)]
    for px, py in particle_positions:
        pz = 0.2 * np.sin(1.5 * px) * np.cos(1.5 * py)
        ax.scatter([px], [py], [pz], c=PM_BLUE, s=100, edgecolor='white',
                   linewidth=1.5, zorder=5)

    # Draw coordinate axes
    ax.quiver(-2.5, -2.5, -1.5, 1.5, 0, 0, color='gray', arrow_length_ratio=0.1, linewidth=1.5)
    ax.quiver(-2.5, -2.5, -1.5, 0, 1.5, 0, color='gray', arrow_length_ratio=0.1, linewidth=1.5)
    ax.quiver(-2.5, -2.5, -1.5, 0, 0, 1.5, color='gray', arrow_length_ratio=0.1, linewidth=1.5)

    # Labels for axes
    ax.text(-1.2, -2.5, -1.5, 'x', fontsize=12, fontweight='bold')
    ax.text(-2.5, -1.2, -1.5, 'y', fontsize=12, fontweight='bold')
    ax.text(-2.5, -2.5, 0, 'z (extra)', fontsize=12, fontweight='bold', color=PM_PINK)

    # Add text annotations
    ax.text2D(0.5, 0.95, "Brane Analogy: 2D Surface in 3D Space",
              transform=ax.transAxes, fontsize=14, fontweight='bold',
              ha='center', va='top')

    ax.text2D(0.5, 0.02,
              "Particles (blue dots) are confined to the 2D brane surface\n"
              "Pink arrows show the extra dimension (bulk direction)",
              transform=ax.transAxes, fontsize=10, ha='center', va='bottom',
              bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

    # Set viewing angle
    ax.view_init(elev=25, azim=45)
    ax.set_xlim(-2.5, 2.5)
    ax.set_ylim(-2.5, 2.5)
    ax.set_zlim(-1.5, 1.5)

    # Remove axis ticks for cleaner look
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_zticks([])

    # Make panes transparent
    ax.xaxis.pane.fill = False
    ax.yaxis.pane.fill = False
    ax.zaxis.pane.fill = False
    ax.xaxis.pane.set_edgecolor('none')
    ax.yaxis.pane.set_edgecolor('none')
    ax.zaxis.pane.set_edgecolor('none')

    plt.tight_layout()
    plt.savefig(output_path, facecolor='white', edgecolor='none')
    plt.close()

    print(f"Brane analogy diagram saved to: {output_path}")
    return output_path


def generate_brane_world_scenario(output_path: str = None):
    """
    Generate brane-world scenario diagram.

    Creates a schematic showing our universe as a 3-brane embedded
    in higher-dimensional bulk spacetime. Illustrates:
    - Our 4D spacetime as a brane (hypersurface)
    - Standard Model fields confined to the brane
    - Gravity propagating through the bulk
    - Extra dimensions compactified on G2 manifold

    Args:
        output_path: Path to save the figure. If None, uses default.
    """
    set_pm_style()

    if output_path is None:
        script_dir = Path(__file__).parent
        output_path = script_dir / ".." / ".." / "images" / "brane-world-scenario.png"

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    fig, ax = plt.subplots(figsize=(12, 8))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 8)
    ax.set_aspect('equal')
    ax.axis('off')

    # Background representing the bulk (11D spacetime)
    bulk_bg = Rectangle((0.5, 0.5), 11, 7, facecolor='#f0f0ff',
                         edgecolor=PM_BLUE, linewidth=2, linestyle='--', alpha=0.3)
    ax.add_patch(bulk_bg)

    # Draw the main brane (our universe) as a tilted rectangle
    brane_vertices = np.array([
        [2, 2], [10, 2.5], [10, 5.5], [2, 5]
    ])
    brane = plt.Polygon(brane_vertices, facecolor=PM_PURPLE, alpha=0.6,
                        edgecolor=PM_DARK, linewidth=2)
    ax.add_patch(brane)

    # Grid lines on the brane to show spacetime coordinates
    for t in np.linspace(0, 1, 6):
        # Horizontal lines (time direction)
        x_start = 2 + t * 0.3
        x_end = 10 + t * 0.3
        y_start = 2 + t * 3
        y_end = 2.5 + t * 3
        ax.plot([x_start + i*(x_end-x_start)/5 for i in range(6)],
                [y_start + i*(y_end-y_start)/5 for i in range(6)],
                color=PM_DARK, alpha=0.2, linewidth=0.5)

    for t in np.linspace(0, 1, 8):
        # Vertical lines (space direction)
        x = 2 + t * 8
        ax.plot([x, x + 0.3], [2 + t * 0.5, 5 + t * 0.5],
                color=PM_DARK, alpha=0.2, linewidth=0.5)

    # Draw particles on the brane (SM fields)
    particles = [
        (4, 3.3, 'e', 'electron'),
        (5.5, 3.8, 'q', 'quark'),
        (7, 3.5, 'W', 'W boson'),
        (8.5, 4.2, 'H', 'Higgs'),
    ]

    for x, y, symbol, name in particles:
        circle = Circle((x, y), 0.3, facecolor=PM_BLUE, edgecolor='white',
                        linewidth=2, zorder=5)
        ax.add_patch(circle)
        ax.text(x, y, symbol, fontsize=10, fontweight='bold', color='white',
                ha='center', va='center', zorder=6)

    # Draw graviton escaping into bulk
    graviton_path_x = [6, 5.5, 5.2, 5.5, 6.2]
    graviton_path_y = [3.6, 4.5, 5.5, 6.5, 7.2]
    ax.plot(graviton_path_x, graviton_path_y, color=PM_PINK, linewidth=2,
            linestyle='--', alpha=0.8)

    # Graviton waves in bulk
    for i in range(3):
        wave_y = 5.5 + i * 0.5
        wave_x = np.linspace(4.5 + i*0.3, 7.5 - i*0.3, 50)
        wave = 0.15 * np.sin(10 * (wave_x - 4.5))
        ax.plot(wave_x, wave_y + wave, color=PM_PINK, alpha=0.5 - i*0.1, linewidth=1)

    # Graviton symbol
    graviton_circle = Circle((6.2, 7.2), 0.25, facecolor=PM_PINK,
                             edgecolor='white', linewidth=2, zorder=5)
    ax.add_patch(graviton_circle)
    ax.text(6.2, 7.2, 'g', fontsize=10, fontweight='bold', color='white',
            ha='center', va='center', zorder=6)

    # Extra dimension arrows (perpendicular to brane)
    for x, y in [(3, 2.7), (6, 3.3), (9, 4)]:
        ax.annotate('', xy=(x - 0.3, y + 1.5), xytext=(x, y),
                    arrowprops=dict(arrowstyle='->', color=PM_PINK,
                                  lw=2, shrinkA=0, shrinkB=0))

    # G2 manifold representation (stylized)
    g2_center = (1.8, 6.5)
    g2_radius = 0.6
    theta = np.linspace(0, 2*np.pi, 7, endpoint=False)
    for i, t in enumerate(theta):
        x = g2_center[0] + g2_radius * np.cos(t)
        y = g2_center[1] + g2_radius * np.sin(t)
        small_circle = Circle((x, y), 0.12, facecolor=PM_BLUE, alpha=0.6,
                              edgecolor=PM_DARK, linewidth=1)
        ax.add_patch(small_circle)

    # Connect G2 circles
    for i, t in enumerate(theta):
        x1 = g2_center[0] + g2_radius * np.cos(t)
        y1 = g2_center[1] + g2_radius * np.sin(t)
        x2 = g2_center[0] + g2_radius * np.cos(theta[(i+2) % 7])
        y2 = g2_center[1] + g2_radius * np.sin(theta[(i+2) % 7])
        ax.plot([x1, x2], [y1, y2], color=PM_BLUE, alpha=0.4, linewidth=1)

    # Labels
    ax.text(6, 1.5, "Our Universe (3-brane)", fontsize=12, fontweight='bold',
            ha='center', color=PM_DARK)
    ax.text(6, 0.9, "Standard Model fields confined here", fontsize=10,
            ha='center', color='gray', style='italic')

    ax.text(10.5, 7, "11D Bulk", fontsize=11, fontweight='bold',
            ha='center', color=PM_BLUE)

    ax.text(1.8, 5.5, "G2\nmanifold", fontsize=9, ha='center', color=PM_DARK)
    ax.text(1.8, 5.0, "(7 compact\ndimensions)", fontsize=8, ha='center',
            color='gray', style='italic')

    ax.text(7.5, 6.8, "Gravitons\nescape to bulk", fontsize=9,
            ha='left', color=PM_PINK)

    # Title
    ax.text(6, 7.7, "Brane-World Scenario in M-Theory", fontsize=14,
            fontweight='bold', ha='center')

    # Legend
    legend_elements = [
        mpatches.Patch(facecolor=PM_PURPLE, alpha=0.6, edgecolor=PM_DARK,
                       label='3-brane (4D spacetime)'),
        mpatches.Patch(facecolor=PM_BLUE, alpha=0.6, label='SM particles (confined)'),
        mpatches.Patch(facecolor=PM_PINK, alpha=0.6, label='Gravitons (bulk propagation)'),
    ]
    ax.legend(handles=legend_elements, loc='lower right', framealpha=0.9)

    plt.tight_layout()
    plt.savefig(output_path, facecolor='white', edgecolor='none')
    plt.close()

    print(f"Brane-world scenario diagram saved to: {output_path}")
    return output_path


def generate_all_diagrams():
    """Generate all brane diagrams."""
    print("=" * 60)
    print("GENERATING BRANE DIAGRAMS")
    print("=" * 60)

    print("\n1. Generating brane analogy diagram...")
    generate_brane_analogy()

    print("\n2. Generating brane-world scenario diagram...")
    generate_brane_world_scenario()

    print("\n" + "=" * 60)
    print("All brane diagrams generated successfully!")
    print("=" * 60)


if __name__ == "__main__":
    generate_all_diagrams()
