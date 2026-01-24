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
PRINCIPIA METAPHYSICA - Time Flow Visualization Diagrams
=========================================================

Licensed under the MIT License. See LICENSE file for details.

Generates visualization diagrams for time and thermodynamics concepts:
1. arrow-of-time.png - Thermodynamic arrow of time emergence
2. thermal-time-flow.png - Connes-Rovelli thermal time hypothesis

THEORETICAL FOUNDATION:
    The arrow of time emerges from the entropy gradient of the Pneuma field.
    The thermal time hypothesis (Connes-Rovelli 1994) posits that physical
    time emerges from thermodynamic properties via modular flow.

REFERENCES:
    - Connes, Rovelli (1994) arXiv:gr-qc/9406019
    - Rovelli (1993) "Statistical mechanics of gravity"
    - PM framework: Two-time physics with Sp(2,R) gauge symmetry

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.

Dedicated To:
    My Wife: Elizabeth May Watts
    Our Messiah: Jesus Of Nazareth
"""

import os
import sys
import numpy as np
from pathlib import Path

try:
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches
    from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Circle, Wedge
    from matplotlib.collections import PatchCollection
    import matplotlib.patheffects as pe
    HAS_MATPLOTLIB = True
except ImportError:
    HAS_MATPLOTLIB = False
    print("Warning: matplotlib not available. Visualization functions disabled.")

# PM Color Palette
PM_COLORS = {
    "purple": "#8b7fff",      # Primary PM purple
    "green": "#4ade80",       # PM green
    "blue": "#60a5fa",        # PM blue
    "dark_purple": "#6b5fdf", # Darker purple variant
    "light_purple": "#a899ff", # Lighter purple variant
    "dark_green": "#22c55e",  # Darker green
    "dark_blue": "#3b82f6",   # Darker blue
    "gray": "#6b7280",        # Neutral gray
    "light_gray": "#e5e7eb",  # Light background
    "white": "#ffffff",
    "text": "#1f2937",        # Dark text
}


def set_pm_style():
    """Set Principia Metaphysica publication-quality matplotlib style."""
    if not HAS_MATPLOTLIB:
        return

    plt.rcParams.update({
        # Font settings
        "font.family": "serif",
        "font.serif": ["Times New Roman", "Times", "DejaVu Serif"],
        "font.size": 11,

        # Axes
        "axes.labelsize": 12,
        "axes.titlesize": 14,
        "axes.linewidth": 1.0,
        "axes.facecolor": PM_COLORS["white"],
        "axes.edgecolor": PM_COLORS["gray"],

        # Figure
        "figure.figsize": (10, 8),
        "figure.dpi": 150,
        "figure.facecolor": PM_COLORS["white"],
        "savefig.dpi": 300,
        "savefig.bbox": "tight",
        "savefig.pad_inches": 0.2,

        # Text
        "text.color": PM_COLORS["text"],
        "mathtext.fontset": "stix",
    })


def draw_arrow(ax, start, end, color, width=0.02, head_width=0.08, head_length=0.05, **kwargs):
    """Draw a custom arrow with specified properties."""
    ax.annotate(
        "", xy=end, xytext=start,
        arrowprops=dict(
            arrowstyle=f"->,head_width={head_width*10},head_length={head_length*10}",
            color=color,
            lw=width * 50,
            shrinkA=0, shrinkB=0,
            **kwargs
        )
    )


def generate_arrow_of_time_diagram(output_path: str = "../../images/arrow-of-time.png"):
    """
    Generate the Arrow of Time diagram showing thermodynamic time emergence.

    Visualizes:
    - Low entropy initial state (Big Bang)
    - Entropy gradient driving time direction
    - Thermodynamic arrow emergence
    - Cause-effect relationships
    """
    if not HAS_MATPLOTLIB:
        print("Cannot generate diagram: matplotlib not available")
        return

    set_pm_style()
    fig, ax = plt.subplots(figsize=(12, 9))
    ax.set_xlim(-0.1, 1.1)
    ax.set_ylim(-0.1, 1.1)
    ax.set_aspect('equal')
    ax.axis('off')

    # Title
    ax.text(0.5, 1.02, "Thermodynamic Arrow of Time Emergence",
            fontsize=16, fontweight='bold', ha='center', va='bottom',
            color=PM_COLORS["text"])
    ax.text(0.5, 0.97, "From Pneuma Field Entropy Gradient",
            fontsize=12, ha='center', va='bottom', style='italic',
            color=PM_COLORS["gray"])

    # === LEFT SIDE: Low Entropy State ===
    # Initial state box
    low_entropy_box = FancyBboxPatch(
        (0.02, 0.55), 0.25, 0.35,
        boxstyle="round,pad=0.02,rounding_size=0.02",
        facecolor=PM_COLORS["light_purple"],
        edgecolor=PM_COLORS["purple"],
        linewidth=2
    )
    ax.add_patch(low_entropy_box)

    ax.text(0.145, 0.87, "LOW ENTROPY", fontsize=11, fontweight='bold',
            ha='center', color=PM_COLORS["dark_purple"])
    ax.text(0.145, 0.82, "Initial State", fontsize=10, ha='center',
            color=PM_COLORS["text"])

    # Draw ordered particles (grid pattern)
    particle_positions = [
        (0.08, 0.70), (0.12, 0.70), (0.16, 0.70), (0.20, 0.70),
        (0.08, 0.65), (0.12, 0.65), (0.16, 0.65), (0.20, 0.65),
        (0.08, 0.60), (0.12, 0.60), (0.16, 0.60), (0.20, 0.60),
    ]
    for pos in particle_positions:
        circle = Circle(pos, 0.015, facecolor=PM_COLORS["purple"],
                       edgecolor=PM_COLORS["dark_purple"], linewidth=1)
        ax.add_patch(circle)

    ax.text(0.145, 0.56, r"$S_{initial} \approx 0$", fontsize=10, ha='center',
            color=PM_COLORS["dark_purple"])

    # === RIGHT SIDE: High Entropy State ===
    high_entropy_box = FancyBboxPatch(
        (0.73, 0.55), 0.25, 0.35,
        boxstyle="round,pad=0.02,rounding_size=0.02",
        facecolor="#dcfce7",  # Light green
        edgecolor=PM_COLORS["green"],
        linewidth=2
    )
    ax.add_patch(high_entropy_box)

    ax.text(0.855, 0.87, "HIGH ENTROPY", fontsize=11, fontweight='bold',
            ha='center', color=PM_COLORS["dark_green"])
    ax.text(0.855, 0.82, "Future State", fontsize=10, ha='center',
            color=PM_COLORS["text"])

    # Draw disordered particles (random)
    np.random.seed(42)  # For reproducibility
    for _ in range(12):
        x = 0.77 + np.random.random() * 0.17
        y = 0.58 + np.random.random() * 0.22
        circle = Circle((x, y), 0.015, facecolor=PM_COLORS["green"],
                        edgecolor=PM_COLORS["dark_green"], linewidth=1)
        ax.add_patch(circle)

    ax.text(0.855, 0.56, r"$S_{final} \gg S_{initial}$", fontsize=10, ha='center',
            color=PM_COLORS["dark_green"])

    # === CENTRAL ARROW: Time Direction ===
    # Main time arrow
    ax.annotate(
        "", xy=(0.70, 0.725), xytext=(0.30, 0.725),
        arrowprops=dict(
            arrowstyle="->,head_width=0.4,head_length=0.3",
            color=PM_COLORS["blue"],
            lw=4,
            shrinkA=0, shrinkB=0,
        )
    )

    ax.text(0.5, 0.78, "TIME", fontsize=14, fontweight='bold',
            ha='center', va='bottom', color=PM_COLORS["dark_blue"])
    ax.text(0.5, 0.66, r"$\frac{dS_{Pneuma}}{dt_{thermal}} \geq 0$",
            fontsize=12, ha='center', va='top', color=PM_COLORS["dark_blue"])

    # === ENTROPY GRADIENT VISUALIZATION ===
    # Gradient bar below main diagram
    gradient_y = 0.42
    gradient_height = 0.06
    n_segments = 50

    for i in range(n_segments):
        x_start = 0.1 + (i / n_segments) * 0.8
        width = 0.8 / n_segments
        # Color gradient from purple to green
        r = int(139 + (74 - 139) * i / n_segments)
        g = int(127 + (222 - 127) * i / n_segments)
        b = int(255 + (128 - 255) * i / n_segments)
        color = f"#{r:02x}{g:02x}{b:02x}"
        rect = plt.Rectangle((x_start, gradient_y), width, gradient_height,
                             facecolor=color, edgecolor='none')
        ax.add_patch(rect)

    # Gradient border
    ax.add_patch(plt.Rectangle((0.1, gradient_y), 0.8, gradient_height,
                               facecolor='none', edgecolor=PM_COLORS["gray"], linewidth=1))

    ax.text(0.1, gradient_y - 0.03, "Low S", fontsize=10, ha='center',
            color=PM_COLORS["purple"])
    ax.text(0.9, gradient_y - 0.03, "High S", fontsize=10, ha='center',
            color=PM_COLORS["green"])
    ax.text(0.5, gradient_y + 0.08, "Entropy Gradient", fontsize=11, fontweight='bold',
            ha='center', color=PM_COLORS["text"])

    # === CAUSE-EFFECT ARROWS ===
    # Draw cause-effect flow diagram at bottom
    cause_y = 0.20

    # Cause box
    cause_box = FancyBboxPatch(
        (0.05, cause_y - 0.08), 0.22, 0.16,
        boxstyle="round,pad=0.01,rounding_size=0.02",
        facecolor=PM_COLORS["light_purple"],
        edgecolor=PM_COLORS["purple"],
        linewidth=1.5
    )
    ax.add_patch(cause_box)
    ax.text(0.16, cause_y + 0.03, "CAUSE", fontsize=10, fontweight='bold',
            ha='center', color=PM_COLORS["dark_purple"])
    ax.text(0.16, cause_y - 0.03, "Entropy increases", fontsize=9, ha='center',
            color=PM_COLORS["text"])

    # Arrow to mechanism
    ax.annotate("", xy=(0.32, cause_y), xytext=(0.28, cause_y),
                arrowprops=dict(arrowstyle="->", color=PM_COLORS["gray"], lw=2))

    # Mechanism box
    mech_box = FancyBboxPatch(
        (0.33, cause_y - 0.08), 0.34, 0.16,
        boxstyle="round,pad=0.01,rounding_size=0.02",
        facecolor="#dbeafe",  # Light blue
        edgecolor=PM_COLORS["blue"],
        linewidth=1.5
    )
    ax.add_patch(mech_box)
    ax.text(0.50, cause_y + 0.03, "MECHANISM", fontsize=10, fontweight='bold',
            ha='center', color=PM_COLORS["dark_blue"])
    ax.text(0.50, cause_y - 0.03, "Modular flow selects direction", fontsize=9, ha='center',
            color=PM_COLORS["text"])

    # Arrow to effect
    ax.annotate("", xy=(0.72, cause_y), xytext=(0.68, cause_y),
                arrowprops=dict(arrowstyle="->", color=PM_COLORS["gray"], lw=2))

    # Effect box
    effect_box = FancyBboxPatch(
        (0.73, cause_y - 0.08), 0.22, 0.16,
        boxstyle="round,pad=0.01,rounding_size=0.02",
        facecolor="#dcfce7",
        edgecolor=PM_COLORS["green"],
        linewidth=1.5
    )
    ax.add_patch(effect_box)
    ax.text(0.84, cause_y + 0.03, "EFFECT", fontsize=10, fontweight='bold',
            ha='center', color=PM_COLORS["dark_green"])
    ax.text(0.84, cause_y - 0.03, "Time arrow emerges", fontsize=9, ha='center',
            color=PM_COLORS["text"])

    # === KEY EQUATION BOX ===
    eq_box = FancyBboxPatch(
        (0.25, 0.01), 0.50, 0.08,
        boxstyle="round,pad=0.01,rounding_size=0.02",
        facecolor=PM_COLORS["white"],
        edgecolor=PM_COLORS["text"],
        linewidth=1
    )
    ax.add_patch(eq_box)
    ax.text(0.50, 0.05, r"Second Law: $\Delta S \geq 0$ defines past $\rightarrow$ future direction",
            fontsize=10, ha='center', va='center', color=PM_COLORS["text"])

    # Save figure
    script_dir = Path(__file__).parent
    output_file = script_dir / output_path
    output_file.parent.mkdir(parents=True, exist_ok=True)

    plt.tight_layout()
    plt.savefig(output_file, dpi=300, facecolor='white', edgecolor='none')
    plt.close()

    print(f"Generated: {output_file.resolve()}")
    return str(output_file.resolve())


def generate_thermal_time_flow_diagram(output_path: str = "../../images/thermal-time-flow.png"):
    """
    Generate the Thermal Time Flow diagram visualizing Connes-Rovelli hypothesis.

    Visualizes:
    - Modular Hamiltonian generation of time
    - Thermal state to time evolution connection
    - alpha_T coupling parameter
    - Two-time framework structure
    """
    if not HAS_MATPLOTLIB:
        print("Cannot generate diagram: matplotlib not available")
        return

    set_pm_style()
    fig, ax = plt.subplots(figsize=(12, 10))
    ax.set_xlim(-0.1, 1.1)
    ax.set_ylim(-0.1, 1.1)
    ax.set_aspect('equal')
    ax.axis('off')

    # Title
    ax.text(0.5, 1.02, "Connes-Rovelli Thermal Time Hypothesis",
            fontsize=16, fontweight='bold', ha='center', va='bottom',
            color=PM_COLORS["text"])
    ax.text(0.5, 0.97, "Time Emergence from Thermodynamic Properties",
            fontsize=12, ha='center', va='bottom', style='italic',
            color=PM_COLORS["gray"])

    # === CENTRAL CIRCULAR FLOW DIAGRAM ===
    center = (0.5, 0.58)
    radius = 0.25

    # Draw main circle
    circle = Circle(center, radius, facecolor='none',
                   edgecolor=PM_COLORS["blue"], linewidth=2, linestyle='--')
    ax.add_patch(circle)

    # Label: "Modular Flow"
    ax.text(center[0], center[1], "Modular\nFlow\n" + r"$\alpha_t(A)$",
            fontsize=12, ha='center', va='center',
            color=PM_COLORS["dark_blue"], fontweight='bold')

    # Draw flow arrows around circle
    angles = [30, 120, 210, 300]
    for angle in angles:
        rad = np.radians(angle)
        x = center[0] + radius * np.cos(rad)
        y = center[1] + radius * np.sin(rad)
        # Tangent direction
        dx = -np.sin(rad) * 0.08
        dy = np.cos(rad) * 0.08
        ax.annotate("", xy=(x + dx, y + dy), xytext=(x - dx, y - dy),
                    arrowprops=dict(arrowstyle="->", color=PM_COLORS["blue"],
                                   lw=2, mutation_scale=15))

    # === TOP: Thermal State ===
    thermal_box = FancyBboxPatch(
        (0.30, 0.86), 0.40, 0.10,
        boxstyle="round,pad=0.01,rounding_size=0.02",
        facecolor=PM_COLORS["light_purple"],
        edgecolor=PM_COLORS["purple"],
        linewidth=2
    )
    ax.add_patch(thermal_box)
    ax.text(0.50, 0.915, "THERMAL STATE", fontsize=11, fontweight='bold',
            ha='center', color=PM_COLORS["dark_purple"])
    ax.text(0.50, 0.875, r"$\rho = e^{-\beta K} / Z$", fontsize=11,
            ha='center', color=PM_COLORS["text"])

    # Arrow from thermal state to center
    ax.annotate("", xy=(0.50, center[1] + radius + 0.02), xytext=(0.50, 0.85),
                arrowprops=dict(arrowstyle="-|>", color=PM_COLORS["purple"],
                               lw=2, mutation_scale=15))
    ax.text(0.52, 0.80, "generates", fontsize=9, ha='left',
            color=PM_COLORS["gray"], style='italic')

    # === LEFT: Modular Hamiltonian ===
    mod_box = FancyBboxPatch(
        (0.02, 0.50), 0.20, 0.16,
        boxstyle="round,pad=0.01,rounding_size=0.02",
        facecolor="#dbeafe",
        edgecolor=PM_COLORS["blue"],
        linewidth=2
    )
    ax.add_patch(mod_box)
    ax.text(0.12, 0.625, "Modular", fontsize=10, fontweight='bold',
            ha='center', color=PM_COLORS["dark_blue"])
    ax.text(0.12, 0.585, "Hamiltonian", fontsize=10, fontweight='bold',
            ha='center', color=PM_COLORS["dark_blue"])
    ax.text(0.12, 0.53, r"$K = -\log(\rho)$", fontsize=10,
            ha='center', color=PM_COLORS["text"])

    # Arrow from left box to center
    ax.annotate("", xy=(center[0] - radius - 0.02, center[1]),
                xytext=(0.23, center[1]),
                arrowprops=dict(arrowstyle="-|>", color=PM_COLORS["blue"],
                               lw=2, mutation_scale=15))

    # === RIGHT: Time Evolution ===
    time_box = FancyBboxPatch(
        (0.78, 0.50), 0.20, 0.16,
        boxstyle="round,pad=0.01,rounding_size=0.02",
        facecolor="#dcfce7",
        edgecolor=PM_COLORS["green"],
        linewidth=2
    )
    ax.add_patch(time_box)
    ax.text(0.88, 0.625, "Physical", fontsize=10, fontweight='bold',
            ha='center', color=PM_COLORS["dark_green"])
    ax.text(0.88, 0.585, "Time", fontsize=10, fontweight='bold',
            ha='center', color=PM_COLORS["dark_green"])
    ax.text(0.88, 0.53, r"$t_{thermal}$", fontsize=10,
            ha='center', color=PM_COLORS["text"])

    # Arrow from center to right box
    ax.annotate("", xy=(0.77, center[1]),
                xytext=(center[0] + radius + 0.02, center[1]),
                arrowprops=dict(arrowstyle="-|>", color=PM_COLORS["green"],
                               lw=2, mutation_scale=15))
    ax.text(0.76, center[1] + 0.04, "emerges", fontsize=9, ha='right',
            color=PM_COLORS["gray"], style='italic')

    # === BOTTOM: Alpha_T Coupling ===
    alpha_box = FancyBboxPatch(
        (0.30, 0.22), 0.40, 0.12,
        boxstyle="round,pad=0.01,rounding_size=0.02",
        facecolor=PM_COLORS["white"],
        edgecolor=PM_COLORS["text"],
        linewidth=2
    )
    ax.add_patch(alpha_box)
    ax.text(0.50, 0.305, r"$\alpha_T = \frac{2\pi}{b_3} \cdot \gamma = 2.7$",
            fontsize=12, fontweight='bold', ha='center', color=PM_COLORS["text"])
    ax.text(0.50, 0.255, "Thermal Time Coupling (from G2 topology)",
            fontsize=10, ha='center', color=PM_COLORS["gray"])

    # Arrow from center to alpha box
    ax.annotate("", xy=(0.50, 0.35),
                xytext=(0.50, center[1] - radius - 0.02),
                arrowprops=dict(arrowstyle="-|>", color=PM_COLORS["text"],
                               lw=2, mutation_scale=15))
    ax.text(0.52, 0.30, "parametrized by", fontsize=9, ha='left',
            color=PM_COLORS["gray"], style='italic', rotation=90)

    # === INFORMATION FLOW ARROWS ===
    # Draw curved information/entropy arrows

    # Left side: Information input
    ax.text(0.02, 0.78, "Information", fontsize=9, fontweight='bold',
            ha='left', color=PM_COLORS["purple"])
    ax.annotate("", xy=(0.20, 0.72), xytext=(0.05, 0.76),
                arrowprops=dict(arrowstyle="->", color=PM_COLORS["purple"],
                               lw=1.5, connectionstyle="arc3,rad=0.2"))

    # Right side: Entropy output
    ax.text(0.98, 0.78, "Entropy", fontsize=9, fontweight='bold',
            ha='right', color=PM_COLORS["green"])
    ax.annotate("", xy=(0.95, 0.76), xytext=(0.80, 0.72),
                arrowprops=dict(arrowstyle="->", color=PM_COLORS["green"],
                               lw=1.5, connectionstyle="arc3,rad=-0.2"))

    # === TWO-TIME FRAMEWORK BOX ===
    two_time_box = FancyBboxPatch(
        (0.10, 0.02), 0.80, 0.14,
        boxstyle="round,pad=0.01,rounding_size=0.02",
        facecolor="#f3e8ff",  # Very light purple
        edgecolor=PM_COLORS["purple"],
        linewidth=1.5
    )
    ax.add_patch(two_time_box)

    ax.text(0.50, 0.135, "PM Two-Time Framework", fontsize=11, fontweight='bold',
            ha='center', color=PM_COLORS["dark_purple"])
    ax.text(0.50, 0.095, r"Signature (24,2): $t_{thermal}$ (observable) + $t_{ortho}$ (hidden)",
            fontsize=10, ha='center', color=PM_COLORS["text"])
    ax.text(0.50, 0.055, r"Related by Sp(2,$\mathbb{R}$) gauge symmetry",
            fontsize=10, ha='center', color=PM_COLORS["gray"], style='italic')

    # === KEY FORMULA (thermal flow) ===
    flow_eq_box = FancyBboxPatch(
        (0.72, 0.35), 0.26, 0.08,
        boxstyle="round,pad=0.005,rounding_size=0.01",
        facecolor="#dbeafe",
        edgecolor=PM_COLORS["blue"],
        linewidth=1
    )
    ax.add_patch(flow_eq_box)
    ax.text(0.85, 0.39, r"$\alpha_t(A) = e^{iKt} A e^{-iKt}$",
            fontsize=9, ha='center', color=PM_COLORS["dark_blue"])

    # Save figure
    script_dir = Path(__file__).parent
    output_file = script_dir / output_path
    output_file.parent.mkdir(parents=True, exist_ok=True)

    plt.tight_layout()
    plt.savefig(output_file, dpi=300, facecolor='white', edgecolor='none')
    plt.close()

    print(f"Generated: {output_file.resolve()}")
    return str(output_file.resolve())


def main():
    """Generate all time flow diagrams."""
    print("=" * 60)
    print("PRINCIPIA METAPHYSICA - Time Flow Visualization Diagrams")
    print("=" * 60)

    if not HAS_MATPLOTLIB:
        print("\nERROR: matplotlib is required for visualization generation.")
        print("Install with: pip install matplotlib")
        sys.exit(1)

    print("\n1. Generating Arrow of Time diagram...")
    arrow_path = generate_arrow_of_time_diagram()

    print("\n2. Generating Thermal Time Flow diagram...")
    thermal_path = generate_thermal_time_flow_diagram()

    print("\n" + "=" * 60)
    print("All diagrams generated successfully!")
    print("=" * 60)

    if arrow_path:
        print(f"\n  - {arrow_path}")
    if thermal_path:
        print(f"  - {thermal_path}")


if __name__ == "__main__":
    main()
