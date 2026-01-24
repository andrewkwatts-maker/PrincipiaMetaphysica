#!/usr/bin/env python3
# [ARCHIVED: v16 Historical Formulation]
# This file documents the historical (24,2) two-time framework from v16-v20.
# The v21+ framework uses unified time (24,1) with Euclidean bridge.
# Retained for historical comparison and educational purposes only.
"""
[HISTORICAL v16] Two-Time Structure Visualization

NOTE: This visualization was created for the v16-v20 (24,2) two-time framework.
The v21 framework uses unified time (24,1) with Euclidean bridge.
Retained for historical comparison and educational purposes.

Two-Time Structure Visualizations
==================================

Generates visual diagrams explaining the 14D x 2 = 28D structure
and two-time physics concepts for Principia Metaphysica.

Output files:
- 14d-times-2-structure.png: Shows the 26D = 24 space + 2 time structure
- two-time-analogy.png: Visual analogy for beginners

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.

Dedicated To:
    My Wife: Elizabeth May Watts
    Our Messiah: Jesus Of Nazareth
"""

import numpy as np
from pathlib import Path

try:
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches
    from matplotlib.patches import FancyBboxPatch, Circle, FancyArrowPatch, Rectangle
    from matplotlib.patches import ConnectionPatch, Wedge, Arc
    import matplotlib.patheffects as pe
    HAS_MATPLOTLIB = True
except ImportError:
    HAS_MATPLOTLIB = False
    print("Warning: matplotlib not available. Visualization disabled.")

# PM Color palette
PM_COLORS = {
    "purple": "#8b7fff",
    "pink": "#ff7eb6",
    "orange": "#fb923c",
    "dark": "#1a1a2e",
    "light": "#f8f9fa",
    "time1": "#e74c3c",  # Red for time t
    "time2": "#3498db",  # Blue for time tau
    "space": "#2ecc71",  # Green for space
    "text": "#2c3e50",
}


def set_pub_style():
    """Set publication-quality matplotlib style."""
    if not HAS_MATPLOTLIB:
        return

    plt.rcParams.update({
        "font.family": "serif",
        "font.serif": ["Times New Roman", "Times", "DejaVu Serif"],
        "font.size": 11,
        "axes.labelsize": 12,
        "axes.titlesize": 14,
        "axes.linewidth": 1.0,
        "figure.dpi": 150,
        "savefig.dpi": 300,
        "savefig.bbox": "tight",
        "savefig.pad_inches": 0.1,
        "text.usetex": False,
        "mathtext.fontset": "stix",
    })


def generate_14d_times_2_structure(output_path: str = "../../images/14d-times-2-structure.png"):
    """
    Generate diagram showing the 26D = 24 space + 2 time structure.

    Shows:
    - The full 26D structure with signature (24, 2)
    - 24 spatial dimensions arranged in a pattern
    - 2 time dimensions (t and tau) clearly distinguished
    - Connection to the 14D x 2 interpretation
    """
    if not HAS_MATPLOTLIB:
        print("Cannot generate plot: matplotlib not available")
        return

    set_pub_style()
    fig, ax = plt.subplots(figsize=(14, 10))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 10)
    ax.set_aspect('equal')
    ax.axis('off')

    # Title
    ax.text(7, 9.5, "26D Spacetime Structure: Signature (24, 2)",
            fontsize=18, fontweight='bold', ha='center', va='center',
            color=PM_COLORS["dark"])
    ax.text(7, 9.0, "14 Dimensions x 2 (Space + Time Components)",
            fontsize=12, ha='center', va='center', color=PM_COLORS["text"])

    # Main container box for 26D
    main_box = FancyBboxPatch((0.5, 1.5), 13, 7,
                               boxstyle="round,pad=0.05,rounding_size=0.3",
                               facecolor='white', edgecolor=PM_COLORS["purple"],
                               linewidth=3, alpha=0.9)
    ax.add_patch(main_box)

    # Label for main box
    ax.text(7, 8.2, "26D Bulk Spacetime", fontsize=14, fontweight='bold',
            ha='center', va='center', color=PM_COLORS["purple"])

    # === Spatial Dimensions Section (24 dimensions) ===
    space_box = FancyBboxPatch((1, 4), 9, 3.5,
                                boxstyle="round,pad=0.02,rounding_size=0.2",
                                facecolor='#e8f8f5', edgecolor=PM_COLORS["space"],
                                linewidth=2)
    ax.add_patch(space_box)

    ax.text(5.5, 7.2, "24 Spatial Dimensions (+)", fontsize=12, fontweight='bold',
            ha='center', va='center', color=PM_COLORS["space"])

    # Draw 24 small circles representing spatial dimensions
    # Arranged as 2 rows of 12 (representing the two shadow sectors)
    for row in range(2):
        y_pos = 5.8 - row * 1.2
        row_label = "Shadow" + ("_Chet" if row == 0 else "_Qof") + " (12D)"
        ax.text(1.5, y_pos + 0.5, row_label, fontsize=9, ha='left',
                color=PM_COLORS["text"], style='italic')
        for col in range(12):
            x_pos = 2.2 + col * 0.65
            circle = Circle((x_pos, y_pos), 0.22,
                           facecolor=PM_COLORS["space"], edgecolor='white',
                           linewidth=1, alpha=0.7)
            ax.add_patch(circle)
            # Add dimension index
            ax.text(x_pos, y_pos, str(col + 1 + row * 12), fontsize=6,
                   ha='center', va='center', color='white', fontweight='bold')

    # Mirror symmetry indicator
    ax.annotate('', xy=(5.5, 4.3), xytext=(5.5, 5.3),
                arrowprops=dict(arrowstyle='<->', color=PM_COLORS["pink"], lw=2))
    ax.text(6.2, 4.8, "Z2 Mirror", fontsize=9, color=PM_COLORS["pink"],
            style='italic', va='center')

    # === Time Dimensions Section (2 dimensions) ===
    time_box = FancyBboxPatch((10.5, 4), 2.5, 3.5,
                               boxstyle="round,pad=0.02,rounding_size=0.2",
                               facecolor='#fef5e7', edgecolor=PM_COLORS["orange"],
                               linewidth=2)
    ax.add_patch(time_box)

    ax.text(11.75, 7.2, "2 Time (-)", fontsize=12, fontweight='bold',
            ha='center', va='center', color=PM_COLORS["orange"])

    # Time dimension t (physical time)
    t_circle = Circle((11.25, 5.8), 0.35,
                      facecolor=PM_COLORS["time1"], edgecolor='white',
                      linewidth=2)
    ax.add_patch(t_circle)
    ax.text(11.25, 5.8, "t", fontsize=12, ha='center', va='center',
            color='white', fontweight='bold')
    ax.text(11.25, 5.2, "Physical\nTime", fontsize=8, ha='center', va='center',
            color=PM_COLORS["time1"])

    # Time dimension tau (orthogonal time)
    tau_circle = Circle((12.25, 5.8), 0.35,
                        facecolor=PM_COLORS["time2"], edgecolor='white',
                        linewidth=2)
    ax.add_patch(tau_circle)
    ax.text(12.25, 5.8, r"$\tau$", fontsize=12, ha='center', va='center',
            color='white', fontweight='bold')
    ax.text(12.25, 5.2, "Orthogonal\nTime", fontsize=8, ha='center', va='center',
            color=PM_COLORS["time2"])

    # Sp(2,R) connection between times
    ax.annotate('', xy=(11.6, 5.8), xytext=(11.9, 5.8),
                arrowprops=dict(arrowstyle='<->', color=PM_COLORS["purple"], lw=2))
    ax.text(11.75, 6.4, "Sp(2,R)", fontsize=9, ha='center', va='center',
            color=PM_COLORS["purple"], fontweight='bold')

    # === Metric Signature Box ===
    sig_box = FancyBboxPatch((1, 2), 5.5, 1.5,
                              boxstyle="round,pad=0.02,rounding_size=0.1",
                              facecolor=PM_COLORS["light"], edgecolor=PM_COLORS["dark"],
                              linewidth=1.5)
    ax.add_patch(sig_box)

    ax.text(3.75, 3.2, "Metric Signature", fontsize=11, fontweight='bold',
            ha='center', va='center', color=PM_COLORS["dark"])
    ax.text(3.75, 2.5, r"$ds^2 = -dt^2 - d\tau^2 + \sum_{i=1}^{24} dx_i^2$",
            fontsize=11, ha='center', va='center', color=PM_COLORS["text"])
    ax.text(3.75, 2.0, "(24, 2) = 24 spacelike (+) + 2 timelike (-)",
            fontsize=9, ha='center', va='center', color=PM_COLORS["text"])

    # === 14D x 2 Interpretation Box ===
    interp_box = FancyBboxPatch((7, 2), 6, 1.5,
                                 boxstyle="round,pad=0.02,rounding_size=0.1",
                                 facecolor='#f0e6ff', edgecolor=PM_COLORS["purple"],
                                 linewidth=1.5)
    ax.add_patch(interp_box)

    ax.text(10, 3.2, "14D x 2 Interpretation", fontsize=11, fontweight='bold',
            ha='center', va='center', color=PM_COLORS["purple"])
    ax.text(10, 2.6, "14 total dimensions (12 space + 2 time) per sector",
            fontsize=9, ha='center', va='center', color=PM_COLORS["text"])
    ax.text(10, 2.1, "Two mirror sectors: 14D x 2 = 28D effective",
            fontsize=9, ha='center', va='center', color=PM_COLORS["text"])

    # === Dimensional Reduction Arrow ===
    ax.annotate('', xy=(7, 1.1), xytext=(7, 1.7),
                arrowprops=dict(arrowstyle='->', color=PM_COLORS["pink"],
                               lw=3, mutation_scale=20))
    ax.text(7, 0.8, "Sp(2,R) Gauge Fixing: 26D (24,2) ---> 13D (12,1)",
            fontsize=11, ha='center', va='center', color=PM_COLORS["pink"],
            fontweight='bold')
    ax.text(7, 0.4, "Projects out orthogonal time, reduces to single shadow",
            fontsize=9, ha='center', va='center', color=PM_COLORS["text"])

    # Save figure
    output_file = Path(__file__).parent / output_path
    output_file.parent.mkdir(exist_ok=True, parents=True)
    plt.tight_layout()
    plt.savefig(output_file, facecolor='white', edgecolor='none')
    plt.close()
    print(f"Saved: {output_file.resolve()}")


def generate_two_time_analogy(output_path: str = "../../images/two-time-analogy.png"):
    """
    Generate a visual analogy explaining two-time physics to beginners.

    Uses the river/stream analogy:
    - Physical time t: the main river flow (downstream)
    - Orthogonal time tau: cross-currents (perpendicular)
    - Sp(2,R) gauge fixing: choosing to measure only downstream flow
    """
    if not HAS_MATPLOTLIB:
        print("Cannot generate plot: matplotlib not available")
        return

    set_pub_style()
    fig = plt.figure(figsize=(14, 10))

    # Create grid for subplots
    gs = fig.add_gridspec(2, 2, height_ratios=[1, 1], width_ratios=[1, 1],
                          hspace=0.3, wspace=0.25)

    # === Panel 1: The River Analogy ===
    ax1 = fig.add_subplot(gs[0, 0])
    ax1.set_xlim(0, 10)
    ax1.set_ylim(0, 10)
    ax1.set_aspect('equal')
    ax1.axis('off')
    ax1.set_title("1. The River Analogy", fontsize=14, fontweight='bold',
                  color=PM_COLORS["purple"], pad=10)

    # Draw river background
    river = FancyBboxPatch((1, 2), 8, 6,
                           boxstyle="round,pad=0.05,rounding_size=0.5",
                           facecolor='#e3f2fd', edgecolor=PM_COLORS["time2"],
                           linewidth=2, alpha=0.7)
    ax1.add_patch(river)

    # Main flow arrows (physical time t)
    for y in [3.5, 5, 6.5]:
        ax1.annotate('', xy=(8, y), xytext=(2, y),
                    arrowprops=dict(arrowstyle='->', color=PM_COLORS["time1"],
                                   lw=2.5, mutation_scale=15))

    ax1.text(5, 7.5, r"Physical Time $t$", fontsize=11, ha='center',
             color=PM_COLORS["time1"], fontweight='bold')
    ax1.text(5, 7.0, "(Main River Flow)", fontsize=9, ha='center',
             color=PM_COLORS["time1"])

    # Cross-current arrows (orthogonal time tau)
    for x in [3, 5, 7]:
        ax1.annotate('', xy=(x, 6.2), xytext=(x, 3.8),
                    arrowprops=dict(arrowstyle='->', color=PM_COLORS["time2"],
                                   lw=1.5, ls='--', mutation_scale=12))

    ax1.text(9.2, 5, r"$\tau$", fontsize=12, ha='left',
             color=PM_COLORS["time2"], fontweight='bold')
    ax1.text(1.5, 1.5, r"Orthogonal Time $\tau$", fontsize=10, ha='left',
             color=PM_COLORS["time2"])
    ax1.text(1.5, 1.0, "(Cross-currents)", fontsize=9, ha='left',
             color=PM_COLORS["time2"])

    # Boat/observer
    boat = FancyBboxPatch((4.5, 4.5), 1, 0.8,
                          boxstyle="round,pad=0.02,rounding_size=0.2",
                          facecolor=PM_COLORS["orange"], edgecolor='white',
                          linewidth=2)
    ax1.add_patch(boat)
    ax1.text(5, 4.9, "You", fontsize=9, ha='center', va='center',
             color='white', fontweight='bold')

    # === Panel 2: Standard Physics View ===
    ax2 = fig.add_subplot(gs[0, 1])
    ax2.set_xlim(0, 10)
    ax2.set_ylim(0, 10)
    ax2.set_aspect('equal')
    ax2.axis('off')
    ax2.set_title("2. Standard Physics (1 Time)", fontsize=14, fontweight='bold',
                  color=PM_COLORS["pink"], pad=10)

    # Single time axis
    ax2.annotate('', xy=(9, 5), xytext=(1, 5),
                arrowprops=dict(arrowstyle='->', color=PM_COLORS["time1"],
                               lw=4, mutation_scale=25))
    ax2.text(5, 6, "Time t", fontsize=14, ha='center', fontweight='bold',
             color=PM_COLORS["time1"])

    # Events on timeline
    for i, (x, label) in enumerate([(2, "Past"), (5, "Now"), (8, "Future")]):
        circle = Circle((x, 5), 0.3, facecolor=PM_COLORS["purple"],
                        edgecolor='white', linewidth=2)
        ax2.add_patch(circle)
        ax2.text(x, 4.2, label, fontsize=10, ha='center', color=PM_COLORS["text"])

    # Caption box
    caption1 = FancyBboxPatch((1, 1), 8, 2.5,
                              boxstyle="round,pad=0.03,rounding_size=0.1",
                              facecolor=PM_COLORS["light"], edgecolor=PM_COLORS["pink"],
                              linewidth=1.5)
    ax2.add_patch(caption1)
    ax2.text(5, 2.8, "In everyday physics:", fontsize=10, fontweight='bold',
             ha='center', color=PM_COLORS["text"])
    ax2.text(5, 2.2, "Events flow along one time axis", fontsize=9,
             ha='center', color=PM_COLORS["text"])
    ax2.text(5, 1.6, "Signature: (3,1) = 3 space + 1 time", fontsize=9,
             ha='center', color=PM_COLORS["text"])

    # === Panel 3: Two-Time Physics View ===
    ax3 = fig.add_subplot(gs[1, 0])
    ax3.set_xlim(0, 10)
    ax3.set_ylim(0, 10)
    ax3.set_aspect('equal')
    ax3.axis('off')
    ax3.set_title("3. Two-Time Physics (2 Times)", fontsize=14, fontweight='bold',
                  color=PM_COLORS["purple"], pad=10)

    # Two time axes
    ax3.annotate('', xy=(9, 3), xytext=(1, 3),
                arrowprops=dict(arrowstyle='->', color=PM_COLORS["time1"],
                               lw=3, mutation_scale=20))
    ax3.text(5, 2.2, r"Physical Time $t$", fontsize=11, ha='center',
             fontweight='bold', color=PM_COLORS["time1"])

    ax3.annotate('', xy=(5, 8.5), xytext=(5, 4),
                arrowprops=dict(arrowstyle='->', color=PM_COLORS["time2"],
                               lw=3, mutation_scale=20))
    ax3.text(6.5, 6.5, r"Orthogonal Time $\tau$", fontsize=11, ha='left',
             fontweight='bold', color=PM_COLORS["time2"], rotation=90)

    # Event point in 2D time plane
    event = Circle((5, 5.5), 0.35, facecolor=PM_COLORS["orange"],
                   edgecolor='white', linewidth=2)
    ax3.add_patch(event)
    ax3.text(5, 5.5, "E", fontsize=10, ha='center', va='center',
             color='white', fontweight='bold')

    # Dashed projections
    ax3.plot([5, 5], [3, 5.5], '--', color=PM_COLORS["time1"], lw=1.5, alpha=0.7)
    ax3.plot([1, 5], [5.5, 5.5], '--', color=PM_COLORS["time2"], lw=1.5, alpha=0.7)

    # Projection labels
    ax3.text(5.3, 4.2, r"$t_E$", fontsize=10, color=PM_COLORS["time1"])
    ax3.text(3, 5.8, r"$\tau_E$", fontsize=10, color=PM_COLORS["time2"])

    # 2D time plane shading
    from matplotlib.patches import Polygon
    plane = Polygon([(1.5, 3.5), (8.5, 3.5), (8.5, 8), (1.5, 8)],
                    facecolor=PM_COLORS["purple"], alpha=0.1)
    ax3.add_patch(plane)
    ax3.text(7.5, 7.5, "2D Time\nPlane", fontsize=9, ha='center',
             color=PM_COLORS["purple"], alpha=0.7)

    # Caption
    ax3.text(5, 1.2, "Events have TWO time coordinates (t, " + r"$\tau$" + ")",
             fontsize=10, ha='center', color=PM_COLORS["text"])
    ax3.text(5, 0.6, "Signature: (24, 2) = 24 space + 2 time", fontsize=9,
             ha='center', color=PM_COLORS["text"])

    # === Panel 4: Gauge Fixing Process ===
    ax4 = fig.add_subplot(gs[1, 1])
    ax4.set_xlim(0, 10)
    ax4.set_ylim(0, 10)
    ax4.set_aspect('equal')
    ax4.axis('off')
    ax4.set_title("4. Sp(2,R) Gauge Fixing", fontsize=14, fontweight='bold',
                  color=PM_COLORS["pink"], pad=10)

    # Before: 2D time plane
    before_box = FancyBboxPatch((0.5, 5), 3.5, 4,
                                boxstyle="round,pad=0.02,rounding_size=0.2",
                                facecolor='#f0e6ff', edgecolor=PM_COLORS["purple"],
                                linewidth=2)
    ax4.add_patch(before_box)
    ax4.text(2.25, 8.6, "Before", fontsize=11, fontweight='bold',
             ha='center', color=PM_COLORS["purple"])

    # Mini 2D time axes
    ax4.annotate('', xy=(3.5, 5.5), xytext=(0.8, 5.5),
                arrowprops=dict(arrowstyle='->', color=PM_COLORS["time1"], lw=2))
    ax4.annotate('', xy=(2.25, 8.3), xytext=(2.25, 5.8),
                arrowprops=dict(arrowstyle='->', color=PM_COLORS["time2"], lw=2))
    ax4.text(2.1, 5.3, "t", fontsize=10, color=PM_COLORS["time1"])
    ax4.text(2.5, 7.5, r"$\tau$", fontsize=10, color=PM_COLORS["time2"])

    # Gauge constraint visualization
    event_before = Circle((2.25, 6.8), 0.2, facecolor=PM_COLORS["orange"],
                          edgecolor='white', linewidth=1.5)
    ax4.add_patch(event_before)

    # Arrow for transformation
    ax4.annotate('', xy=(6, 7), xytext=(4.5, 7),
                arrowprops=dict(arrowstyle='->', color=PM_COLORS["pink"],
                               lw=3, mutation_scale=20))
    ax4.text(5.25, 7.7, "Sp(2,R)", fontsize=10, ha='center',
             color=PM_COLORS["pink"], fontweight='bold')
    ax4.text(5.25, 6.3, r"$\tau \to 0$", fontsize=10, ha='center',
             color=PM_COLORS["pink"])

    # After: 1D time
    after_box = FancyBboxPatch((6, 5), 3.5, 4,
                               boxstyle="round,pad=0.02,rounding_size=0.2",
                               facecolor='#e8f8f5', edgecolor=PM_COLORS["space"],
                               linewidth=2)
    ax4.add_patch(after_box)
    ax4.text(7.75, 8.6, "After", fontsize=11, fontweight='bold',
             ha='center', color=PM_COLORS["space"])

    # Single time axis
    ax4.annotate('', xy=(9.2, 6.8), xytext=(6.3, 6.8),
                arrowprops=dict(arrowstyle='->', color=PM_COLORS["time1"], lw=2.5))
    ax4.text(7.75, 6.3, "Physical t only", fontsize=9, ha='center',
             color=PM_COLORS["time1"])

    event_after = Circle((7.75, 6.8), 0.2, facecolor=PM_COLORS["orange"],
                         edgecolor='white', linewidth=1.5)
    ax4.add_patch(event_after)

    # Bottom caption
    caption2 = FancyBboxPatch((0.5, 0.5), 9, 4,
                              boxstyle="round,pad=0.03,rounding_size=0.1",
                              facecolor=PM_COLORS["light"], edgecolor=PM_COLORS["dark"],
                              linewidth=1.5)
    ax4.add_patch(caption2)

    ax4.text(5, 4.0, "The Key Insight:", fontsize=11, fontweight='bold',
             ha='center', color=PM_COLORS["dark"])
    ax4.text(5, 3.3, "Two-time physics is not science fiction!", fontsize=10,
             ha='center', color=PM_COLORS["text"])
    ax4.text(5, 2.5, "The second time is a mathematical tool that helps", fontsize=9,
             ha='center', color=PM_COLORS["text"])
    ax4.text(5, 1.9, "explain particle properties. Sp(2,R) symmetry 'fixes'", fontsize=9,
             ha='center', color=PM_COLORS["text"])
    ax4.text(5, 1.3, "the gauge so we only observe one time dimension.", fontsize=9,
             ha='center', color=PM_COLORS["text"])
    ax4.text(5, 0.7, "(24,2) --> (12,1): Two times become one", fontsize=9,
             ha='center', color=PM_COLORS["purple"], fontweight='bold')

    # Overall title
    fig.suptitle("Understanding Two-Time Physics: A Visual Guide",
                 fontsize=16, fontweight='bold', color=PM_COLORS["dark"], y=0.98)

    # Save figure
    output_file = Path(__file__).parent / output_path
    output_file.parent.mkdir(exist_ok=True, parents=True)
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig(output_file, facecolor='white', edgecolor='none')
    plt.close()
    print(f"Saved: {output_file.resolve()}")


def main():
    """Generate all two-time structure visualizations."""
    if not HAS_MATPLOTLIB:
        print("Matplotlib not available. Skipping visualization generation.")
        return

    print("=" * 60)
    print("GENERATING TWO-TIME STRUCTURE VISUALIZATIONS")
    print("=" * 60)

    print("\n1. Generating 14D x 2 Structure diagram...")
    generate_14d_times_2_structure()

    print("\n2. Generating Two-Time Analogy diagram...")
    generate_two_time_analogy()

    print("\n" + "=" * 60)
    print("All visualizations generated successfully!")
    print("=" * 60)


if __name__ == "__main__":
    main()
