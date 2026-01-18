#!/usr/bin/env python3
"""
Compactification Diagrams
==========================

Generates visualizations for compactification concepts in
Principia Metaphysica:
1. compactification-scales.png - Energy/length scale hierarchy
2. expanding-universe.png - Expanding 4D universe from compactified dimensions

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.

Dedicated To:
    My Wife: Elizabeth May Watts
    Our Messiah: Jesus Of Nazareth
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, Circle, Polygon, Arrow, FancyArrowPatch
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
    "orange": "#fb923c",
    "red": "#f87171",
    "yellow": "#fbbf24",
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


def generate_compactification_scales(output_path: str = "../../images/compactification-scales.png"):
    """
    Generate energy/length scale hierarchy diagram.

    Shows the scale hierarchy from Planck scale down to electroweak scale,
    indicating where different physics becomes relevant:
    - Planck scale: 10^19 GeV / 10^-35 m (quantum gravity, PM: 26D unified)
    - GUT scale: 10^16 GeV / 10^-32 m (gauge unification)
    - Intermediate scale: Compactification becomes important
    - Electroweak scale: 10^2 GeV / 10^-18 m (Standard Model)
    - Our scale: 10^0 eV / 10^0 m (everyday physics, 4D)
    """
    set_publication_style()
    fig, ax = plt.subplots(figsize=(14, 8))
    ax.set_xlim(-1, 14)
    ax.set_ylim(-1, 10)
    ax.axis('off')

    # === Main scale bar ===
    # Vertical scale bar on the left showing energy
    bar_x = 1.5
    bar_bottom, bar_top = 1, 9

    # Energy scale gradient bar
    gradient_colors = [PM_COLORS["purple"], PM_COLORS["blue"], PM_COLORS["green"]]
    for i in range(100):
        y_low = bar_bottom + (bar_top - bar_bottom) * i / 100
        y_high = bar_bottom + (bar_top - bar_bottom) * (i + 1) / 100
        # Interpolate color
        if i < 50:
            t = i / 50
            r1, g1, b1 = int(PM_COLORS["purple"][1:3], 16), int(PM_COLORS["purple"][3:5], 16), int(PM_COLORS["purple"][5:7], 16)
            r2, g2, b2 = int(PM_COLORS["blue"][1:3], 16), int(PM_COLORS["blue"][3:5], 16), int(PM_COLORS["blue"][5:7], 16)
        else:
            t = (i - 50) / 50
            r1, g1, b1 = int(PM_COLORS["blue"][1:3], 16), int(PM_COLORS["blue"][3:5], 16), int(PM_COLORS["blue"][5:7], 16)
            r2, g2, b2 = int(PM_COLORS["green"][1:3], 16), int(PM_COLORS["green"][3:5], 16), int(PM_COLORS["green"][5:7], 16)
        r = int(r1 + t * (r2 - r1))
        g = int(g1 + t * (g2 - g1))
        b = int(b1 + t * (b2 - b1))
        color = f"#{r:02x}{g:02x}{b:02x}"
        ax.fill_between([bar_x - 0.3, bar_x + 0.3], [y_low, y_low], [y_high, y_high],
                       color=color, alpha=0.8)

    # Scale bar labels
    ax.text(bar_x, bar_top + 0.3, "High Energy\n(Small Distance)", fontsize=10, ha='center',
           va='bottom', fontweight='bold', color=PM_COLORS["purple"])
    ax.text(bar_x, bar_bottom - 0.3, "Low Energy\n(Large Distance)", fontsize=10, ha='center',
           va='top', fontweight='bold', color=PM_COLORS["green"])

    # === Key scales with markers and descriptions ===
    scales = [
        {
            "y": 8.5,
            "energy": r"$10^{19}$ GeV",
            "length": r"$\ell_{Pl} \sim 10^{-35}$ m",
            "name": "Planck Scale",
            "description": "Quantum gravity\n26D unified (PM framework)",
            "color": PM_COLORS["purple"],
            "dimensions": "26D",
        },
        {
            "y": 7.0,
            "energy": r"$10^{16}$ GeV",
            "length": r"$\ell_{GUT} \sim 10^{-32}$ m",
            "name": "GUT Scale",
            "description": "Gauge unification\n$SU(3) \\times SU(2) \\times U(1)$ merge",
            "color": PM_COLORS["dark_purple"],
            "dimensions": "13D→6D",
        },
        {
            "y": 5.0,
            "energy": r"$10^{10}$ GeV",
            "length": r"$10^{-26}$ m",
            "name": "Seesaw Scale",
            "description": "Neutrino mass generation\nRight-handed neutrinos",
            "color": PM_COLORS["blue"],
            "dimensions": "4D + G$_2$ effects",
        },
        {
            "y": 3.0,
            "energy": r"$10^{2}$ GeV",
            "length": r"$10^{-18}$ m",
            "name": "Electroweak Scale",
            "description": "Higgs mechanism\nStandard Model physics",
            "color": PM_COLORS["dark_green"],
            "dimensions": "4D",
        },
        {
            "y": 1.5,
            "energy": r"$10^{0}$ eV",
            "length": r"$10^{0}$ m",
            "name": "Our Scale",
            "description": "Everyday physics\nClassical limit",
            "color": PM_COLORS["green"],
            "dimensions": "4D",
        },
    ]

    for scale in scales:
        y = scale["y"]
        color = scale["color"]

        # Marker on bar
        ax.scatter([bar_x], [y], s=150, color=color, zorder=10,
                  edgecolor='white', linewidth=2)

        # Horizontal line extending right
        ax.plot([bar_x + 0.3, 3.5], [y, y], color=color, linewidth=2, alpha=0.7)

        # Energy and length labels (left of bar)
        ax.text(bar_x - 0.5, y + 0.15, scale["energy"], fontsize=9, ha='right',
               color=color, fontweight='bold')
        ax.text(bar_x - 0.5, y - 0.15, scale["length"], fontsize=8, ha='right',
               color=scale["color"], alpha=0.8)

        # Scale name and description box
        box_x = 4
        box_width = 4.5
        ax.add_patch(FancyBboxPatch((box_x, y - 0.5), box_width, 1,
                                     boxstyle="round,pad=0.1",
                                     facecolor='white',
                                     edgecolor=color,
                                     linewidth=2, alpha=0.9))
        ax.text(box_x + 0.2, y + 0.2, scale["name"], fontsize=11,
               fontweight='bold', color=color, va='center')
        ax.text(box_x + 0.2, y - 0.2, scale["description"], fontsize=8,
               color=PM_COLORS["text_light"], va='center')

        # Dimension label (far right)
        ax.text(box_x + box_width + 0.5, y, scale["dimensions"], fontsize=10,
               color=color, fontweight='bold', va='center',
               bbox=dict(boxstyle='round,pad=0.3', facecolor=color, alpha=0.15))

    # === Compactification region annotation ===
    # Bracket showing where compactification happens
    bracket_x = 12.5
    ax.annotate('', xy=(bracket_x, 8.5), xytext=(bracket_x, 5.5),
               arrowprops=dict(arrowstyle='-[', color=PM_COLORS["orange"],
                             lw=3, mutation_scale=15))
    ax.text(bracket_x + 0.3, 7, "G$_2$ Holonomy\nCompactification\nRegion", fontsize=10,
           color=PM_COLORS["orange"], fontweight='bold', va='center')

    # === Dimensional hierarchy box ===
    dim_box_x = 9.5
    dim_box_y = 1.5
    ax.add_patch(FancyBboxPatch((dim_box_x, dim_box_y), 4, 3,
                                 boxstyle="round,pad=0.15",
                                 facecolor=PM_COLORS["light_purple"],
                                 edgecolor=PM_COLORS["purple"],
                                 linewidth=2, alpha=0.3))
    ax.text(dim_box_x + 2, dim_box_y + 2.6, "PM Dimensional Structure", fontsize=11,
           ha='center', fontweight='bold', color=PM_COLORS["dark_purple"])

    dim_info = [
        ("14D Total", PM_COLORS["purple"]),
        ("= 4D (spacetime)", PM_COLORS["blue"]),
        ("+ 7D (G$_2$ manifold)", PM_COLORS["green"]),
        ("+ 3D (gauge fiber)", PM_COLORS["orange"]),
    ]
    for i, (text, color) in enumerate(dim_info):
        ax.text(dim_box_x + 0.3, dim_box_y + 2.1 - i * 0.5, text, fontsize=9,
               color=color, fontweight='bold' if i == 0 else 'normal')

    # === Title ===
    ax.text(7, 9.5, "Compactification Scale Hierarchy in Principia Metaphysica",
           fontsize=16, ha='center', fontweight='bold', color=PM_COLORS["text"])

    plt.tight_layout()

    # Save
    output = Path(__file__).parent / output_path
    output.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f"[OK] Compactification scales diagram saved to {output}")
    return str(output)


def generate_expanding_universe(output_path: str = "../../images/expanding-universe.png"):
    """
    Generate diagram showing expanding 4D universe from compactified dimensions.

    Shows:
    - 4D spacetime expanding (Hubble flow)
    - 7D G2 manifold remaining compact at Planck scale
    - How dark energy/cosmological constant emerges
    """
    set_publication_style()
    fig, axes = plt.subplots(1, 2, figsize=(14, 7))

    # === Panel 1: Schematic of expansion ===
    ax1 = axes[0]
    ax1.set_xlim(-6, 6)
    ax1.set_ylim(-6, 6)
    ax1.set_aspect('equal')
    ax1.axis('off')

    # Draw expanding 4D universe (nested circles showing expansion)
    for i, (r, alpha, label) in enumerate([
        (1.5, 0.3, "Early"),
        (3.0, 0.4, "Middle"),
        (4.5, 0.5, "Now"),
    ]):
        circle = Circle((0, 0), r, facecolor=PM_COLORS["light_blue"],
                        edgecolor=PM_COLORS["blue"], linewidth=2, alpha=alpha)
        ax1.add_patch(circle)
        if i < 2:
            ax1.text(r * 0.7, r * 0.7, label, fontsize=9, color=PM_COLORS["dark_blue"],
                    alpha=0.7, style='italic')

    ax1.text(3.5, 3.5, "Now", fontsize=10, color=PM_COLORS["dark_blue"],
            fontweight='bold')

    # Expansion arrows
    arrow_angles = [0, 45, 90, 135, 180, 225, 270, 315]
    for angle in arrow_angles:
        rad = np.radians(angle)
        x_start, y_start = 2.5 * np.cos(rad), 2.5 * np.sin(rad)
        x_end, y_end = 4.2 * np.cos(rad), 4.2 * np.sin(rad)
        ax1.annotate("", xy=(x_end, y_end), xytext=(x_start, y_start),
                    arrowprops=dict(arrowstyle='->', color=PM_COLORS["purple"],
                                   lw=2, alpha=0.7))

    # Center label
    ax1.text(0, 0, "4D\nSpacetime", fontsize=12, ha='center', va='center',
            fontweight='bold', color=PM_COLORS["dark_blue"])

    # Small G2 manifolds at various points (showing they stay compact)
    g2_positions = [
        (1.0, 0), (-0.7, 0.7), (0, -1.0),
        (2.2, 1.0), (-1.5, -1.5), (2.0, -1.8),
        (3.5, 0.5), (-3.0, 2.0), (0.5, 3.2), (-2.5, -2.5),
    ]
    for (gx, gy) in g2_positions:
        # Tiny circle representing G2
        circle = Circle((gx, gy), 0.15, facecolor=PM_COLORS["light_green"],
                        edgecolor=PM_COLORS["green"], linewidth=1, alpha=0.8)
        ax1.add_patch(circle)

    # Legend for G2
    ax1.scatter([], [], s=100, color=PM_COLORS["green"], label='G$_2$ manifold (compact)')
    ax1.legend(loc='upper right', fontsize=9, framealpha=0.9)

    # Annotations
    ax1.text(0, -5.5, "4D expands (Hubble flow)", fontsize=11, ha='center',
            color=PM_COLORS["purple"], fontweight='bold')
    ax1.text(0, -5.9, r"G$_2$ stays compact at $\ell_{Pl}$", fontsize=10, ha='center',
            color=PM_COLORS["green"], style='italic')

    ax1.set_title("Cosmic Expansion with Compact Dimensions", fontsize=14,
                 fontweight='bold', color=PM_COLORS["text"], pad=10)

    # === Panel 2: Scale factor evolution and dark energy ===
    ax2 = axes[1]
    ax2.set_xlim(-1, 11)
    ax2.set_ylim(-1, 9)
    ax2.axis('off')

    # Time axis
    ax2.annotate("", xy=(10, 0.5), xytext=(0, 0.5),
                arrowprops=dict(arrowstyle='->', color=PM_COLORS["text"], lw=2))
    ax2.text(10.3, 0.5, "Time", fontsize=11, va='center', color=PM_COLORS["text"])

    # Scale axis
    ax2.annotate("", xy=(0.5, 8), xytext=(0.5, 0.5),
                arrowprops=dict(arrowstyle='->', color=PM_COLORS["text"], lw=2))
    ax2.text(0.5, 8.3, "Scale", fontsize=11, ha='center', color=PM_COLORS["text"])

    # 4D scale factor (expanding)
    t = np.linspace(0.5, 9.5, 100)
    a_4d = 0.8 + 0.7 * (t - 0.5) ** 0.6  # Approximate expansion curve
    ax2.plot(t, a_4d, color=PM_COLORS["blue"], linewidth=3,
            label='4D Scale Factor $a(t)$')
    ax2.fill_between(t, 0.5, a_4d, color=PM_COLORS["light_blue"], alpha=0.3)

    # 7D G2 scale (constant, compact)
    g2_scale = 1.0
    ax2.plot([0.5, 9.5], [g2_scale, g2_scale], color=PM_COLORS["green"],
            linewidth=3, linestyle='--', label=r'G$_2$ Scale $r_{G_2}$ (constant)')

    # Planck scale reference line
    ax2.plot([0.5, 9.5], [0.7, 0.7], color=PM_COLORS["purple"],
            linewidth=1.5, linestyle=':', alpha=0.7, label=r'$\ell_{Pl}$ (reference)')

    # Time markers
    time_markers = [
        (1.5, "Big\nBang", PM_COLORS["red"]),
        (4.0, "Matter\nDomination", PM_COLORS["orange"]),
        (7.5, "Dark Energy\nDomination", PM_COLORS["purple"]),
    ]
    for (tx, label, color) in time_markers:
        ax2.axvline(x=tx, color=color, linestyle=':', alpha=0.5, linewidth=1)
        y_pos = 0.8 + 0.7 * (tx - 0.5) ** 0.6
        ax2.text(tx, y_pos + 0.7, label, fontsize=8, ha='center',
                color=color, fontweight='bold')

    # Dark energy box
    ax2.add_patch(FancyBboxPatch((5.5, 5), 4, 2.5,
                                  boxstyle="round,pad=0.15",
                                  facecolor='white',
                                  edgecolor=PM_COLORS["purple"],
                                  linewidth=2, alpha=0.95))
    ax2.text(7.5, 7.1, "Dark Energy from G$_2$", fontsize=11, ha='center',
            fontweight='bold', color=PM_COLORS["dark_purple"])
    de_lines = [
        r"$\Lambda_{eff} = c_{G,\Lambda} \cdot \Lambda_{QFT}$",
        r"$w_0 = -1.03 \pm 0.03$",
        r"$w_a = -0.02$",
    ]
    for i, line in enumerate(de_lines):
        ax2.text(7.5, 6.5 - i * 0.45, line, fontsize=9, ha='center',
                color=PM_COLORS["text_light"])

    # Legend
    ax2.legend(loc='upper left', fontsize=9, framealpha=0.9)

    ax2.set_title("Scale Evolution: 4D Expands, G$_2$ Stays Compact", fontsize=14,
                 fontweight='bold', color=PM_COLORS["text"], pad=10)

    # === Main title ===
    fig.suptitle("Expanding Universe from Compactified Higher Dimensions",
                fontsize=16, fontweight='bold', y=1.02, color=PM_COLORS["text"])

    plt.tight_layout()

    # Save
    output = Path(__file__).parent / output_path
    output.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f"[OK] Expanding universe diagram saved to {output}")
    return str(output)


def main():
    """Generate all compactification diagrams."""
    print("Generating compactification diagrams...")
    print("=" * 50)

    generate_compactification_scales()
    generate_expanding_universe()

    print("=" * 50)
    print("All compactification diagrams generated successfully!")


if __name__ == "__main__":
    main()
