#!/usr/bin/env python3
"""
Dimension Introduction Diagrams
================================

Generates introductory visualizations for dimensional concepts in
Principia Metaphysica:
1. dimension-analogy.png - Ant on a hose analogy for extra dimensions
2. kaluza-klein-intro.png - Introduction to Kaluza-Klein compactification

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.

Dedicated To:
    My Wife: Elizabeth May Watts
    Our Messiah: Jesus Of Nazareth
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import Circle, FancyBboxPatch, Polygon, Arc, Wedge
from matplotlib.lines import Line2D
import numpy as np
from pathlib import Path

# PM color palette
PM_COLORS = {
    "purple": "#8b7fff",
    "blue": "#60a5fa",
    "green": "#4ade80",
    "dark_purple": "#6b5fd9",
    "dark_blue": "#3b82f6",
    "dark_green": "#22c55e",
    "light_purple": "#a5a0ff",
    "light_blue": "#93c5fd",
    "light_green": "#86efac",
    "text": "#1f2937",
    "text_light": "#6b7280",
    "background": "#fafafa",
}


def set_publication_style():
    """Set publication-quality matplotlib style."""
    plt.rcParams.update({
        "font.family": "serif",
        "font.serif": ["Times New Roman", "DejaVu Serif"],
        "text.usetex": False,
        "axes.labelsize": 12,
        "xtick.labelsize": 10,
        "ytick.labelsize": 10,
        "legend.fontsize": 10,
        "figure.dpi": 150,
        "savefig.dpi": 300,
        "axes.grid": False,
        "figure.facecolor": "white",
        "axes.facecolor": "white",
    })


def generate_dimension_analogy(output_path: str = "../../images/dimension-analogy.png"):
    """
    Generate the ant-on-a-hose analogy diagram.

    This classic analogy explains how extra dimensions can exist but be
    invisible at large scales:
    - From far away: the hose looks like a 1D line
    - Up close: you see it's actually a 2D surface (cylinder)
    - An ant can move along the hose AND around its circumference

    In PM: our 4D spacetime has 7 extra compactified G2 dimensions.
    """
    set_publication_style()
    fig, axes = plt.subplots(1, 3, figsize=(14, 5))

    # === Panel 1: Far view - Hose looks 1D ===
    ax1 = axes[0]
    ax1.set_xlim(-0.5, 10.5)
    ax1.set_ylim(-3, 3)
    ax1.set_aspect('equal')
    ax1.axis('off')

    # Draw "line" (hose from far away)
    ax1.plot([0, 10], [0, 0], color=PM_COLORS["purple"], linewidth=8, solid_capstyle='round')

    # Observer (far away)
    ax1.scatter([5], [2.5], s=200, color=PM_COLORS["blue"], zorder=10, marker='o')
    ax1.annotate("Observer\n(far away)", (5, 2.5), (5, 3.2),
                fontsize=10, ha='center', va='bottom',
                color=PM_COLORS["text"])

    # Dotted lines showing "view"
    ax1.plot([5, 0], [2.5, 0], 'k--', alpha=0.3, linewidth=1)
    ax1.plot([5, 10], [2.5, 0], 'k--', alpha=0.3, linewidth=1)

    # Label
    ax1.text(5, -2, '"I see a 1D line"', fontsize=12, ha='center',
            style='italic', color=PM_COLORS["text_light"])
    ax1.set_title("Far View: 1 Dimension Visible", fontsize=14,
                 fontweight='bold', color=PM_COLORS["dark_purple"], pad=10)

    # === Panel 2: Close view - Hose is 2D cylinder ===
    ax2 = axes[1]
    ax2.set_xlim(-1, 11)
    ax2.set_ylim(-3, 3)
    ax2.set_aspect('equal')
    ax2.axis('off')

    # Draw 3D-like cylinder (garden hose)
    # Top edge
    theta = np.linspace(0, np.pi, 50)
    for i in range(20):
        x_offset = i * 0.5
        # Draw ellipse cross-section
        y_top = 0.5 * np.sin(theta)
        x_ell = x_offset + 0.1 * np.cos(theta)
        ax2.plot(x_ell, y_top + 0.5, color=PM_COLORS["purple"],
                alpha=0.3 if i < 19 else 1, linewidth=1)
        ax2.plot(x_ell, -y_top - 0.5, color=PM_COLORS["dark_purple"],
                alpha=0.3 if i < 19 else 1, linewidth=1)

    # Main body lines
    ax2.plot([0, 9.5], [0.5, 0.5], color=PM_COLORS["purple"], linewidth=2)
    ax2.plot([0, 9.5], [-0.5, -0.5], color=PM_COLORS["dark_purple"], linewidth=2)

    # End cap ellipse
    end_theta = np.linspace(0, 2*np.pi, 100)
    ax2.fill(9.5 + 0.1*np.cos(end_theta), 0.5*np.sin(end_theta),
            color=PM_COLORS["light_purple"], edgecolor=PM_COLORS["purple"], linewidth=2)

    # Front cap ellipse
    ax2.fill(0 + 0.1*np.cos(end_theta), 0.5*np.sin(end_theta),
            color=PM_COLORS["light_purple"], edgecolor=PM_COLORS["purple"], linewidth=2)

    # Ant on the hose (close view)
    ax2.scatter([5], [0.5], s=100, color=PM_COLORS["green"], zorder=10, marker='o')
    ax2.annotate("Ant", (5, 0.5), (5.5, 1.2), fontsize=10,
                arrowprops=dict(arrowstyle='->', color=PM_COLORS["dark_green"]),
                color=PM_COLORS["dark_green"])

    # Arrows showing two directions of movement
    ax2.annotate("", (6.5, 0.5), (5.3, 0.5),
                arrowprops=dict(arrowstyle='->', color=PM_COLORS["blue"], lw=2))
    ax2.text(6.8, 0.5, "x", fontsize=11, color=PM_COLORS["blue"], fontweight='bold')

    # Circular motion arrow
    arc = Arc((5, 0), 0.2, 1, angle=0, theta1=60, theta2=300,
             color=PM_COLORS["purple"], linewidth=2)
    ax2.add_patch(arc)
    ax2.annotate("", (5.07, -0.4), (5.1, -0.35),
                arrowprops=dict(arrowstyle='->', color=PM_COLORS["purple"], lw=1.5))
    ax2.text(4.3, 0, r"$\theta$", fontsize=11, color=PM_COLORS["purple"], fontweight='bold')

    ax2.text(5, -2, '"I can move in 2 directions!"', fontsize=12, ha='center',
            style='italic', color=PM_COLORS["text_light"])
    ax2.set_title("Close View: 2 Dimensions Revealed", fontsize=14,
                 fontweight='bold', color=PM_COLORS["dark_purple"], pad=10)

    # === Panel 3: PM analogy - Our universe ===
    ax3 = axes[2]
    ax3.set_xlim(-1, 11)
    ax3.set_ylim(-3, 3)
    ax3.set_aspect('equal')
    ax3.axis('off')

    # Draw grid representing 4D spacetime
    for i in range(11):
        ax3.plot([i, i], [-1.5, 1.5], color=PM_COLORS["light_blue"],
                linewidth=0.5, alpha=0.5)
    for j in np.linspace(-1.5, 1.5, 7):
        ax3.plot([0, 10], [j, j], color=PM_COLORS["light_blue"],
                linewidth=0.5, alpha=0.5)

    # 4D spacetime label
    ax3.add_patch(FancyBboxPatch((0.5, -1.2), 9, 2.4,
                                  boxstyle="round,pad=0.1",
                                  facecolor=PM_COLORS["light_blue"],
                                  edgecolor=PM_COLORS["blue"],
                                  alpha=0.3, linewidth=2))
    ax3.text(5, 1.5, "4D Spacetime", fontsize=11, ha='center',
            fontweight='bold', color=PM_COLORS["blue"])

    # Small circles representing compactified dimensions at various points
    compact_positions = [(2, 0), (4, 0.5), (6, -0.3), (8, 0.2)]
    for (cx, cy) in compact_positions:
        # Draw tiny circle (compactified dimension)
        circle = Circle((cx, cy), 0.25, facecolor=PM_COLORS["light_purple"],
                        edgecolor=PM_COLORS["purple"], linewidth=1.5, alpha=0.8)
        ax3.add_patch(circle)
        # G2 label
        ax3.text(cx, cy, r"G$_2$", fontsize=7, ha='center', va='center',
                color=PM_COLORS["dark_purple"], fontweight='bold')

    # Dimension count box
    ax3.add_patch(FancyBboxPatch((6.5, -2.8), 3.5, 1.3,
                                  boxstyle="round,pad=0.1",
                                  facecolor='white',
                                  edgecolor=PM_COLORS["purple"],
                                  linewidth=1.5))
    ax3.text(8.25, -2.2, "4D + 7D G₂ internal", fontsize=10, ha='center',
            fontweight='bold', color=PM_COLORS["dark_purple"])
    ax3.text(8.25, -2.6, "(PM: 26D→13D→6D→4D)", fontsize=9, ha='center',
            color=PM_COLORS["text_light"])

    # Annotation
    ax3.text(5, -2, 'Extra dimensions: curled up at each point', fontsize=12,
            ha='center', style='italic', color=PM_COLORS["text_light"])
    ax3.set_title("PM: 7 Hidden G$_2$ Dimensions", fontsize=14,
                 fontweight='bold', color=PM_COLORS["dark_purple"], pad=10)

    # Main title
    fig.suptitle("Extra Dimensions Analogy: The Garden Hose", fontsize=16,
                fontweight='bold', y=1.02, color=PM_COLORS["text"])

    plt.tight_layout()

    # Save
    output = Path(__file__).parent / output_path
    output.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f"[OK] Dimension analogy diagram saved to {output}")
    return str(output)


def generate_kaluza_klein_intro(output_path: str = "../../images/kaluza-klein-intro.png"):
    """
    Generate introduction to Kaluza-Klein compactification diagram.

    Shows:
    - 5D to 4D+1 compactification (original Kaluza-Klein)
    - How gauge fields emerge from geometry
    - PM extension: 26D → G₂ holonomy → 4D
    """
    set_publication_style()
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    # === Panel 1: Classic Kaluza-Klein (5D -> 4D + circle) ===
    ax1 = axes[0]
    ax1.set_xlim(-2, 12)
    ax1.set_ylim(-4, 4)
    ax1.set_aspect('equal')
    ax1.axis('off')

    # 5D spacetime representation (before compactification)
    # Draw as a thick 2D slice with depth
    ax1.add_patch(FancyBboxPatch((-1, -2), 6, 4,
                                  boxstyle="round,pad=0.1",
                                  facecolor=PM_COLORS["light_blue"],
                                  edgecolor=PM_COLORS["blue"],
                                  alpha=0.5, linewidth=2))
    ax1.text(2, 2.5, "5D Spacetime", fontsize=12, ha='center',
            fontweight='bold', color=PM_COLORS["blue"])

    # Coordinate labels
    ax1.text(2, -0.5, r"$(x, y, z, t, w)$", fontsize=11, ha='center',
            color=PM_COLORS["dark_blue"])

    # Arrow showing compactification
    ax1.annotate("", (8.5, 0), (5.5, 0),
                arrowprops=dict(arrowstyle='->', color=PM_COLORS["purple"],
                               lw=3, mutation_scale=20))
    ax1.text(7, 1, "Compactify\n$w$ dimension", fontsize=10, ha='center',
            color=PM_COLORS["dark_purple"], fontweight='bold')

    # 4D spacetime (after compactification)
    ax1.add_patch(FancyBboxPatch((7, -2), 4.5, 4,
                                  boxstyle="round,pad=0.1",
                                  facecolor=PM_COLORS["light_green"],
                                  edgecolor=PM_COLORS["green"],
                                  alpha=0.5, linewidth=2))
    ax1.text(9.25, 2.5, "4D Spacetime", fontsize=12, ha='center',
            fontweight='bold', color=PM_COLORS["dark_green"])
    ax1.text(9.25, 1.7, r"$(x, y, z, t)$", fontsize=10, ha='center',
            color=PM_COLORS["dark_green"])

    # Small circle representing compactified dimension at each point
    for (cx, cy) in [(8, 0), (9.5, 0.8), (10.5, -0.5)]:
        circle = Circle((cx, cy), 0.3, facecolor=PM_COLORS["light_purple"],
                        edgecolor=PM_COLORS["purple"], linewidth=1.5, alpha=0.8)
        ax1.add_patch(circle)
        # Arrow showing circular dimension
        arc = Arc((cx, cy), 0.5, 0.5, angle=0, theta1=30, theta2=330,
                 color=PM_COLORS["dark_purple"], linewidth=1.5)
        ax1.add_patch(arc)

    # What emerges box
    ax1.add_patch(FancyBboxPatch((6.8, -3.8), 5, 1.2,
                                  boxstyle="round,pad=0.1",
                                  facecolor='white',
                                  edgecolor=PM_COLORS["purple"],
                                  linewidth=1.5))
    ax1.text(9.3, -3.2, "Emerges: Electromagnetism!", fontsize=10, ha='center',
            fontweight='bold', color=PM_COLORS["dark_purple"])
    ax1.text(9.3, -3.6, r"$g_{5\mu} \rightarrow A_\mu$ (photon field)", fontsize=9,
            ha='center', color=PM_COLORS["text_light"])

    ax1.set_title("Classic Kaluza-Klein (1921-1926)", fontsize=14,
                 fontweight='bold', color=PM_COLORS["text"], pad=10)

    # === Panel 2: PM Extension (26D -> 13D -> 4D + G2) ===
    ax2 = axes[1]
    ax2.set_xlim(-2, 12)
    ax2.set_ylim(-4, 4)
    ax2.set_aspect('equal')
    ax2.axis('off')

    # 26D total spacetime (PM framework)
    ax2.add_patch(FancyBboxPatch((-1, -2), 5, 4,
                                  boxstyle="round,pad=0.1",
                                  facecolor=PM_COLORS["light_purple"],
                                  edgecolor=PM_COLORS["purple"],
                                  alpha=0.5, linewidth=2))
    ax2.text(1.5, 2.5, "26D Total", fontsize=12, ha='center',
            fontweight='bold', color=PM_COLORS["purple"])
    ax2.text(1.5, 1.7, r"$M^{26}_{(24,2)}$", fontsize=11, ha='center',
            color=PM_COLORS["dark_purple"])

    # Breakdown inside the 26D box
    ax2.text(1.5, 0.3, "→ 13D → 6D → 4D", fontsize=10, ha='center',
            color=PM_COLORS["text"])
    ax2.text(1.5, -0.5, r"$M^4 \times X^7$", fontsize=10, ha='center',
            color=PM_COLORS["text_light"])

    # Arrow showing compactification
    ax2.annotate("", (7, 0), (4.5, 0),
                arrowprops=dict(arrowstyle='->', color=PM_COLORS["green"],
                               lw=3, mutation_scale=20))
    ax2.text(5.75, 1.2, "G$_2$ Holonomy\nCompactification", fontsize=10, ha='center',
            color=PM_COLORS["dark_green"], fontweight='bold')

    # 4D spacetime result
    ax2.add_patch(FancyBboxPatch((6.5, 0.5), 2.5, 2,
                                  boxstyle="round,pad=0.1",
                                  facecolor=PM_COLORS["light_blue"],
                                  edgecolor=PM_COLORS["blue"],
                                  alpha=0.6, linewidth=2))
    ax2.text(7.75, 2.8, "4D Spacetime", fontsize=11, ha='center',
            fontweight='bold', color=PM_COLORS["blue"])
    ax2.text(7.75, 1.5, "Observable\nUniverse", fontsize=9, ha='center',
            color=PM_COLORS["dark_blue"])

    # G2 manifold representation
    ax2.add_patch(FancyBboxPatch((9.2, 0.5), 2.3, 2,
                                  boxstyle="round,pad=0.1",
                                  facecolor=PM_COLORS["light_green"],
                                  edgecolor=PM_COLORS["green"],
                                  alpha=0.6, linewidth=2))
    ax2.text(10.35, 2.8, "7D G$_2$", fontsize=11, ha='center',
            fontweight='bold', color=PM_COLORS["dark_green"])
    # Draw small G2 symbol (7-pointed star approximation)
    g2_center = (10.35, 1.3)
    n_points = 7
    outer_r, inner_r = 0.5, 0.25
    angles = np.linspace(-np.pi/2, 3*np.pi/2, n_points, endpoint=False)
    star_points = []
    for i, angle in enumerate(angles):
        star_points.append((g2_center[0] + outer_r*np.cos(angle),
                           g2_center[1] + outer_r*np.sin(angle)))
        next_angle = angle + np.pi/n_points
        star_points.append((g2_center[0] + inner_r*np.cos(next_angle),
                           g2_center[1] + inner_r*np.sin(next_angle)))
    star = Polygon(star_points, facecolor=PM_COLORS["green"],
                  edgecolor=PM_COLORS["dark_green"], alpha=0.7, linewidth=1)
    ax2.add_patch(star)

    # What emerges - multiple items
    emerge_y = -1.5
    ax2.add_patch(FancyBboxPatch((6, emerge_y-1.8), 5.8, 2.5,
                                  boxstyle="round,pad=0.1",
                                  facecolor='white',
                                  edgecolor=PM_COLORS["green"],
                                  linewidth=1.5))
    ax2.text(8.9, emerge_y+0.3, "What Emerges:", fontsize=11, ha='center',
            fontweight='bold', color=PM_COLORS["dark_green"])

    emerges = [
        (r"$\bullet$ Standard Model gauge group", PM_COLORS["purple"]),
        (r"$\bullet$ 3 fermion generations", PM_COLORS["blue"]),
        (r"$\bullet$ Yukawa couplings", PM_COLORS["green"]),
    ]
    for i, (text, color) in enumerate(emerges):
        ax2.text(8.9, emerge_y - 0.2 - i*0.4, text, fontsize=9, ha='center',
                color=color)

    # Scale annotation
    ax2.text(5.75, -3.5, r"Compactification scale: $\ell_{G_2} \sim \ell_{Pl}$",
            fontsize=10, ha='center', color=PM_COLORS["text_light"], style='italic')

    ax2.set_title("PM: 26D with G$_2$ Holonomy", fontsize=14,
                 fontweight='bold', color=PM_COLORS["text"], pad=10)

    # Main title
    fig.suptitle("Kaluza-Klein Compactification: From 5D to PM's 26D", fontsize=16,
                fontweight='bold', y=1.02, color=PM_COLORS["text"])

    plt.tight_layout()

    # Save
    output = Path(__file__).parent / output_path
    output.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f"[OK] Kaluza-Klein intro diagram saved to {output}")
    return str(output)


def main():
    """Generate all dimension introduction diagrams."""
    print("Generating dimension introduction diagrams...")
    print("=" * 50)

    generate_dimension_analogy()
    generate_kaluza_klein_intro()

    print("=" * 50)
    print("All dimension introduction diagrams generated successfully!")


if __name__ == "__main__":
    main()
