#!/usr/bin/env python3
"""
Dark Energy Diagrams for Principia Metaphysica
===============================================

Generates publication-quality dark energy visualizations:
1. Dark Energy Introduction - explaining the concept visually
2. Dark Energy Mechanism - how G2 geometry produces Lambda

Based on PM v16.2 theory derivation:
- Dimensional reduction: 26D -> 13D -> 4D
- w0 = -23/24 ≈ -0.9583 from G2 thawing quintessence (b₃=24)
- Lambda from G2 entropy density

Output files:
- dark-energy-intro.png
- dark-energy-mechanism.png

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.

Dedicated To:
    My Wife: Elizabeth May Watts
    Our Messiah: Jesus Of Nazareth
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Circle, FancyArrowPatch, Polygon, Wedge
from matplotlib.patches import Arc, Rectangle, Ellipse
from matplotlib.collections import PatchCollection
import matplotlib.patheffects as path_effects
from pathlib import Path

# PM Color palette
PM_COLORS = {
    "purple": "#8b7fff",
    "orange": "#fb923c",
    "pink": "#ff7eb6",
    "blue": "#60a5fa",
    "dark": "#1a1a2e",
    "light": "#f8f9fa",
    "grid": "#e0e0e0",
    "de_glow": "#c4b5fd",  # Light purple for dark energy glow
    "space": "#0f0f23",    # Deep space color
}

# Output directory
OUTPUT_DIR = Path(__file__).parent.parent.parent / "images"


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
    })


def generate_dark_energy_intro():
    """
    Generate introductory diagram explaining dark energy concept.

    Shows:
    - Expanding universe with galaxies
    - Dark energy as repulsive force
    - Comparison with matter/radiation
    - PM equation of state w0 = -23/24 (v16.2 thawing)
    """
    setup_publication_style()

    fig, axes = plt.subplots(1, 2, figsize=(14, 8))

    # Left panel: Conceptual visualization
    ax1 = axes[0]
    ax1.set_xlim(-5, 5)
    ax1.set_ylim(-5, 5)
    ax1.set_aspect('equal')
    ax1.axis('off')

    # Background - deep space
    ax1.add_patch(Rectangle((-5, -5), 10, 10, facecolor=PM_COLORS['space']))

    # Central dark energy glow
    for r, alpha in [(4, 0.05), (3, 0.1), (2, 0.15), (1.5, 0.2)]:
        circle = Circle((0, 0), r, color=PM_COLORS['purple'], alpha=alpha)
        ax1.add_patch(circle)

    # Draw galaxies being pushed apart
    galaxy_positions = [
        (2.5, 0), (-2.5, 0), (0, 2.5), (0, -2.5),
        (1.8, 1.8), (-1.8, 1.8), (1.8, -1.8), (-1.8, -1.8)
    ]

    for i, (gx, gy) in enumerate(galaxy_positions):
        # Galaxy as small ellipse
        angle = np.arctan2(gy, gx) * 180 / np.pi
        galaxy = Ellipse((gx, gy), 0.4, 0.2, angle=angle + 45,
                        color=PM_COLORS['orange'], alpha=0.9)
        ax1.add_patch(galaxy)

        # Arrow showing outward motion (dark energy expansion)
        direction = np.array([gx, gy])
        direction = direction / np.linalg.norm(direction) * 0.6
        ax1.annotate('', xy=(gx + direction[0], gy + direction[1]),
                    xytext=(gx, gy),
                    arrowprops=dict(arrowstyle='->', color=PM_COLORS['de_glow'],
                                   lw=2, mutation_scale=15))

    # Central label
    ax1.text(0, 0, 'DARK\nENERGY', fontsize=14, ha='center', va='center',
            color='white', fontweight='bold',
            path_effects=[path_effects.withStroke(linewidth=3, foreground=PM_COLORS['purple'])])

    # Title for left panel
    ax1.text(0, 4.5, 'Dark Energy: The Cosmic Accelerator', fontsize=13,
            ha='center', fontweight='bold', color='white')
    ax1.text(0, -4.5, 'Galaxies accelerate apart', fontsize=10,
            ha='center', color=PM_COLORS['de_glow'], style='italic')

    # Right panel: Equation of state comparison
    ax2 = axes[1]
    ax2.set_xlim(-0.5, 10)
    ax2.set_ylim(-2, 5)
    ax2.axis('off')

    # Title
    ax2.text(5, 4.5, 'Equation of State: $w = P/\\rho$', fontsize=14,
            ha='center', fontweight='bold')

    # Components comparison
    components = [
        {"name": "Radiation", "w": "+1/3", "desc": "Photons, neutrinos",
         "color": "#ff6b6b", "y": 3.5, "behavior": "Slows expansion"},
        {"name": "Matter", "w": "0", "desc": "Baryons, dark matter",
         "color": "#4ecdc4", "y": 2.3, "behavior": "Slows expansion"},
        {"name": "Cosmological\nConstant", "w": "-1", "desc": "Einstein's $\\Lambda$",
         "color": "#666", "y": 1.1, "behavior": "Constant acceleration"},
        {"name": "PM Dark Energy", "w": "-23/24", "desc": "v16.2 thawing (b₃=24)",
         "color": PM_COLORS['purple'], "y": -0.2, "behavior": "Thawing quintessence"},
    ]

    for comp in components:
        y = comp['y']

        # Component box
        box = FancyBboxPatch((0, y - 0.35), 2.5, 0.7,
                            boxstyle="round,pad=0.05,rounding_size=0.1",
                            facecolor=comp['color'], alpha=0.8,
                            edgecolor='white', linewidth=1)
        ax2.add_patch(box)

        # Name
        ax2.text(1.25, y, comp['name'], fontsize=10, ha='center', va='center',
                color='white', fontweight='bold')

        # w value
        ax2.text(3.5, y, f"$w = {comp['w']}$", fontsize=12, ha='left', va='center',
                color=comp['color'], fontweight='bold')

        # Description
        ax2.text(5.8, y + 0.15, comp['desc'], fontsize=9, ha='left', va='center',
                color='#333')

        # Behavior
        ax2.text(5.8, y - 0.2, comp['behavior'], fontsize=8, ha='left', va='center',
                color='#666', style='italic')

    # Highlight PM prediction
    highlight = FancyBboxPatch((-0.2, -0.75), 9.5, 1.1,
                              boxstyle="round,pad=0.1",
                              facecolor=PM_COLORS['purple'], alpha=0.1,
                              edgecolor=PM_COLORS['purple'], linewidth=2)
    ax2.add_patch(highlight)

    # DESI validation box (v16.2: thawing constraint)
    ax2.text(5, -1.5, 'DESI 2025 Thawing: $w_0 = -0.957 \\pm 0.067$',
            fontsize=10, ha='center', color='#333')
    ax2.text(5, -1.9, 'PM Prediction: $w_0 = -23/24 \\approx -0.9583$ (0.02$\\sigma$ agreement!)',
            fontsize=10, ha='center', color=PM_COLORS['purple'], fontweight='bold')

    plt.tight_layout()

    # Save
    output_path = OUTPUT_DIR / "dark-energy-intro.png"
    plt.savefig(output_path, dpi=300, facecolor='white', edgecolor='none')
    plt.close()

    print(f"Generated: {output_path}")
    return output_path


def generate_dark_energy_mechanism():
    """
    Generate diagram showing PM mechanism for dark energy.

    Shows:
    - 26D -> 13D -> 4D dimensional reduction cascade
    - G2 manifold structure
    - Shadow dimension contribution
    - Derivation of w0 = -23/24 (v16.2 thawing from b₃=24)
    """
    setup_publication_style()

    fig, ax = plt.subplots(figsize=(14, 10))
    ax.set_xlim(-1, 15)
    ax.set_ylim(-1, 11)
    ax.axis('off')

    # Title
    ax.text(7, 10.5, 'Dark Energy from G$_2$ Dimensional Reduction',
           fontsize=16, ha='center', fontweight='bold')
    ax.text(7, 9.9, 'How Extra Dimensions Create Cosmic Acceleration',
           fontsize=12, ha='center', color='gray', style='italic')

    # ==================
    # Dimensional Cascade (top section)
    # ==================

    cascade_y = 8

    # 26D box
    box_26d = FancyBboxPatch((0, cascade_y - 0.6), 3, 1.2,
                             boxstyle="round,pad=0.1",
                             facecolor='#e74c3c', alpha=0.8,
                             edgecolor='#c0392b', linewidth=2)
    ax.add_patch(box_26d)
    ax.text(1.5, cascade_y, '26D', fontsize=16, ha='center', va='center',
           color='white', fontweight='bold')
    ax.text(1.5, cascade_y + 0.8, 'Bosonic String', fontsize=9, ha='center', color='#c0392b')
    ax.text(1.5, cascade_y - 0.9, '(24,2) signature', fontsize=8, ha='center', color='gray')

    # Arrow 26D -> 13D
    ax.annotate('', xy=(4.5, cascade_y), xytext=(3.2, cascade_y),
               arrowprops=dict(arrowstyle='->', color='#333', lw=2, mutation_scale=20))
    ax.text(3.85, cascade_y + 0.4, 'Sp(2,R)', fontsize=9, ha='center', color='#333')
    ax.text(3.85, cascade_y - 0.4, 'gauge', fontsize=8, ha='center', color='gray')

    # 13D box
    box_13d = FancyBboxPatch((4.5, cascade_y - 0.6), 3, 1.2,
                             boxstyle="round,pad=0.1",
                             facecolor=PM_COLORS['orange'], alpha=0.8,
                             edgecolor='#ea580c', linewidth=2)
    ax.add_patch(box_13d)
    ax.text(6, cascade_y, '13D', fontsize=16, ha='center', va='center',
           color='white', fontweight='bold')
    ax.text(6, cascade_y + 0.8, 'Heterotic Shadow', fontsize=9, ha='center', color='#ea580c')
    ax.text(6, cascade_y - 0.9, '(12,1) signature', fontsize=8, ha='center', color='gray')

    # Arrow 13D -> 4D
    ax.annotate('', xy=(9, cascade_y), xytext=(7.7, cascade_y),
               arrowprops=dict(arrowstyle='->', color='#333', lw=2, mutation_scale=20))
    ax.text(8.35, cascade_y + 0.4, 'G$_2$', fontsize=9, ha='center', color='#333')
    ax.text(8.35, cascade_y - 0.4, 'compact', fontsize=8, ha='center', color='gray')

    # 4D box
    box_4d = FancyBboxPatch((9, cascade_y - 0.6), 3, 1.2,
                            boxstyle="round,pad=0.1",
                            facecolor=PM_COLORS['blue'], alpha=0.8,
                            edgecolor='#2563eb', linewidth=2)
    ax.add_patch(box_4d)
    ax.text(10.5, cascade_y, '4D', fontsize=16, ha='center', va='center',
           color='white', fontweight='bold')
    ax.text(10.5, cascade_y + 0.8, 'Observable', fontsize=9, ha='center', color='#2563eb')
    ax.text(10.5, cascade_y - 0.9, '(3,1) spacetime', fontsize=8, ha='center', color='gray')

    # Plus shadow
    ax.text(12.5, cascade_y, '+', fontsize=20, ha='center', va='center', color='#666')

    # Shadow box
    box_shadow = FancyBboxPatch((13, cascade_y - 0.5), 1.5, 1,
                                boxstyle="round,pad=0.05",
                                facecolor=PM_COLORS['purple'], alpha=0.3,
                                edgecolor=PM_COLORS['purple'], linewidth=2,
                                linestyle='--')
    ax.add_patch(box_shadow)
    ax.text(13.75, cascade_y, '$\\alpha$', fontsize=14, ha='center', va='center',
           color=PM_COLORS['purple'], fontweight='bold')
    ax.text(13.75, cascade_y - 0.8, 'Shadow', fontsize=8, ha='center', color=PM_COLORS['purple'])

    # ==================
    # G2 Manifold visualization (middle section)
    # ==================

    g2_center = (4, 5)

    # Draw G2 manifold schematically (7D compact space)
    # Represented as interconnected circles (Joyce's calibrated geometry)
    g2_circles = [
        (0, 0), (0.8, 0.5), (-0.8, 0.5), (0.5, -0.7), (-0.5, -0.7),
        (0.3, 0.8), (-0.3, 0.8)
    ]

    for i, (dx, dy) in enumerate(g2_circles):
        x, y = g2_center[0] + dx * 1.5, g2_center[1] + dy * 1.5
        circle = Circle((x, y), 0.3, facecolor=PM_COLORS['purple'],
                        alpha=0.6, edgecolor=PM_COLORS['purple'], linewidth=1)
        ax.add_patch(circle)

    # Connect circles (calibrated 3-forms)
    for i in range(len(g2_circles)):
        for j in range(i + 1, len(g2_circles)):
            x1, y1 = g2_center[0] + g2_circles[i][0] * 1.5, g2_center[1] + g2_circles[i][1] * 1.5
            x2, y2 = g2_center[0] + g2_circles[j][0] * 1.5, g2_center[1] + g2_circles[j][1] * 1.5
            dist = np.sqrt((x2-x1)**2 + (y2-y1)**2)
            if dist < 1.8:
                ax.plot([x1, x2], [y1, y2], color=PM_COLORS['purple'], alpha=0.3, lw=1)

    ax.text(g2_center[0], g2_center[1] - 2.2, 'G$_2$ Holonomy Manifold',
           fontsize=11, ha='center', fontweight='bold', color=PM_COLORS['purple'])
    ax.text(g2_center[0], g2_center[1] - 2.7, '7 compact dimensions, $b_3 = 24$ 3-cycles',
           fontsize=9, ha='center', color='gray')

    # ==================
    # Equation derivation (right section)
    # ==================

    eq_x = 10
    eq_y = 5.5

    # Box for equations
    eq_box = FancyBboxPatch((7.5, 3), 6.5, 4,
                            boxstyle="round,pad=0.2",
                            facecolor='white', alpha=0.95,
                            edgecolor=PM_COLORS['purple'], linewidth=2)
    ax.add_patch(eq_box)

    ax.text(eq_x + 0.75, eq_y + 1.2, 'Derivation of Dark Energy EoS',
           fontsize=12, ha='center', fontweight='bold', color=PM_COLORS['purple'])

    # Step 1
    ax.text(8, eq_y + 0.4, '1. Effective dimension from cascade:',
           fontsize=9, ha='left', color='#333')
    ax.text(8.3, eq_y - 0.1, r'$D_{eff} = 12$ (shared dimensions)',
           fontsize=10, ha='left', color='black')

    # Step 2
    ax.text(8, eq_y - 0.7, '2. Equation of state formula:',
           fontsize=9, ha='left', color='#333')
    ax.text(8.3, eq_y - 1.2, r'$w = -\frac{D_{eff} - 1}{D_{eff} + 1}$',
           fontsize=11, ha='left', color='black')

    # Step 3 (result)
    ax.text(8, eq_y - 1.9, '3. Result:',
           fontsize=9, ha='left', color='#333')

    # Highlighted result
    result_box = FancyBboxPatch((8.2, eq_y - 2.9), 5.3, 0.8,
                                boxstyle="round,pad=0.1",
                                facecolor=PM_COLORS['purple'], alpha=0.15,
                                edgecolor=PM_COLORS['purple'], linewidth=1)
    ax.add_patch(result_box)
    ax.text(10.85, eq_y - 2.5, r'$w_0 = -\frac{23}{24} \approx -0.9583$ (thawing)',
           fontsize=14, ha='center', fontweight='bold', color=PM_COLORS['purple'])

    # ==================
    # Bottom: Physical interpretation
    # ==================

    bottom_y = 1.2

    # Three explanation boxes
    explanations = [
        {"title": "Why Negative?", "x": 2,
         "text": "w < 0 means negative\npressure: repulsive\ngravity"},
        {"title": "Why -23/24?", "x": 7,
         "text": "b₃ = 24 cycles\nThawing deviation\n= 1/b₃ from Λ"},
        {"title": "What's Shadow?", "x": 12,
         "text": "$\\alpha_{shadow} = 0.576$\nresidual DOF from\ncompact space"},
    ]

    for exp in explanations:
        box = FancyBboxPatch((exp['x'] - 1.8, bottom_y - 0.7), 3.6, 1.8,
                            boxstyle="round,pad=0.1",
                            facecolor=PM_COLORS['light'], alpha=0.9,
                            edgecolor=PM_COLORS['purple'], linewidth=1)
        ax.add_patch(box)
        ax.text(exp['x'], bottom_y + 0.7, exp['title'],
               fontsize=10, ha='center', fontweight='bold', color=PM_COLORS['purple'])
        ax.text(exp['x'], bottom_y - 0.1, exp['text'],
               fontsize=9, ha='center', va='center', color='#333', linespacing=1.2)

    # Connection arrows from G2 to explanations
    ax.annotate('', xy=(2, 2.5), xytext=(g2_center[0] - 1, g2_center[1] - 1.8),
               arrowprops=dict(arrowstyle='->', color='gray', lw=1,
                              connectionstyle="arc3,rad=-0.2"))
    ax.annotate('', xy=(7, 2.5), xytext=(g2_center[0] + 0.5, g2_center[1] - 1.8),
               arrowprops=dict(arrowstyle='->', color='gray', lw=1,
                              connectionstyle="arc3,rad=0"))

    plt.tight_layout()

    # Save
    output_path = OUTPUT_DIR / "dark-energy-mechanism.png"
    plt.savefig(output_path, dpi=300, facecolor='white', edgecolor='none')
    plt.close()

    print(f"Generated: {output_path}")
    return output_path


def main():
    """Generate all dark energy diagrams."""
    print("=" * 60)
    print("Generating Dark Energy Diagrams")
    print("=" * 60)

    # Ensure output directory exists
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Generate diagrams
    intro_path = generate_dark_energy_intro()
    mechanism_path = generate_dark_energy_mechanism()

    print("\n" + "=" * 60)
    print("Dark Energy Diagrams Complete")
    print("=" * 60)
    print(f"  Introduction: {intro_path}")
    print(f"  Mechanism:    {mechanism_path}")
    print("=" * 60)


if __name__ == "__main__":
    main()
