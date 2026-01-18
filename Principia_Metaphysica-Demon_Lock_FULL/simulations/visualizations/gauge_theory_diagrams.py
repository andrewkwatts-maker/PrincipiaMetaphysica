#!/usr/bin/env python3
"""
Gauge Theory Diagrams for Principia Metaphysica
=================================================

Generates publication-quality visualizations for gauge theory concepts:
1. anomaly-cancellation.png - Shows how anomalies cancel in PM framework
2. brst-cohomology.png - BRST cohomology structure visualization

Output directory: ../../images/ (project root images folder)

Physics Background:
- Anomaly cancellation is crucial for consistency of gauge theories
- In PM, anomalies cancel via G2 holonomy constraints + SO(10) embedding
- BRST cohomology provides ghost field structure for gauge fixing
- The third Betti number b3=24 determines the physical state space

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.

Dedicated To:
    My Wife: Elizabeth May Watts
    Our Messiah: Jesus Of Nazareth
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle, Ellipse
from matplotlib.patches import ConnectionPatch, Polygon
import matplotlib.patheffects as path_effects
import numpy as np
from pathlib import Path
import os
import sys

# Add project root to path
_project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)

# Import PM color palette
try:
    from simulations.visualizations import PM_COLORS, OUTPUT_DIR, FIGURE_DEFAULTS
except ImportError:
    PM_COLORS = {
        "purple": "#8b7fff",
        "pink": "#ff7eb6",
        "blue": "#60a5fa",
        "orange": "#fb923c",
        "green": "#4ade80",
        "gold": "#ffd43b",
        "red": "#ef4444",
        "text": "#f8f9fa",
        "bg_dark": "#1a1f3a",
        "bg_card": "#2a2f4a",
    }
    OUTPUT_DIR = Path(__file__).parent.parent.parent / "images"
    FIGURE_DEFAULTS = {"dpi": 300, "figsize": (10, 8)}


def set_dark_style():
    """Set dark publication style for PM visualizations."""
    plt.rcParams.update({
        "font.family": "sans-serif",
        "font.sans-serif": ["DejaVu Sans", "Arial", "Helvetica"],
        "text.usetex": False,
        "axes.labelsize": 14,
        "xtick.labelsize": 12,
        "ytick.labelsize": 12,
        "legend.fontsize": 11,
        "figure.dpi": 300,
        "savefig.dpi": 300,
        "axes.facecolor": PM_COLORS["bg_dark"],
        "figure.facecolor": PM_COLORS["bg_dark"],
        "axes.edgecolor": PM_COLORS["text"],
        "axes.labelcolor": PM_COLORS["text"],
        "xtick.color": PM_COLORS["text"],
        "ytick.color": PM_COLORS["text"],
        "text.color": PM_COLORS["text"],
    })


def create_gradient_box(ax, x, y, width, height, color1, color2, text, fontsize=12):
    """Create a gradient-filled box with text label."""
    # Create rectangle with solid color (gradient approximation)
    rect = FancyBboxPatch(
        (x - width/2, y - height/2), width, height,
        boxstyle="round,pad=0.02,rounding_size=0.1",
        facecolor=color1,
        edgecolor=color2,
        linewidth=2,
        alpha=0.9
    )
    ax.add_patch(rect)

    # Add text
    txt = ax.text(x, y, text, ha='center', va='center',
                  fontsize=fontsize, fontweight='bold', color='white')
    txt.set_path_effects([
        path_effects.withStroke(linewidth=2, foreground='black')
    ])

    return rect


def plot_anomaly_cancellation(output_path: str = None):
    """
    Generate anomaly cancellation diagram showing how gauge anomalies cancel
    in the Principia Metaphysica framework.

    The diagram shows:
    - Triangle anomaly diagrams for U(1), SU(2), SU(3)
    - G2 holonomy constraints
    - SO(10) embedding ensuring tracelessness
    - Net cancellation summing to zero

    Args:
        output_path: Output file path (default: ../../images/anomaly-cancellation.png)
    """
    if output_path is None:
        output_path = OUTPUT_DIR / "anomaly-cancellation.png"

    set_dark_style()
    fig, ax = plt.subplots(figsize=(12, 10), facecolor=PM_COLORS["bg_dark"])
    ax.set_facecolor(PM_COLORS["bg_dark"])

    # Title
    ax.set_title("Anomaly Cancellation in Principia Metaphysica",
                 fontsize=18, fontweight='bold', color=PM_COLORS["text"], pad=20)

    # Remove axes
    ax.set_xlim(-0.5, 10.5)
    ax.set_ylim(-0.5, 8.5)
    ax.axis('off')

    # ============================================================
    # TOP SECTION: Triangle Anomaly Diagrams
    # ============================================================

    # Section header
    ax.text(5, 8, "Gauge Anomaly Triangle Diagrams",
            ha='center', va='center', fontsize=14, fontweight='bold',
            color=PM_COLORS["gold"])

    # Draw three triangle diagrams representing different anomaly types
    triangle_centers = [(1.5, 6.5), (5, 6.5), (8.5, 6.5)]
    triangle_labels = [
        ("U(1)$_Y^3$", PM_COLORS["purple"]),
        ("SU(2)$_L^2$U(1)$_Y$", PM_COLORS["pink"]),
        ("SU(3)$_c^2$U(1)$_Y$", PM_COLORS["blue"])
    ]

    for (cx, cy), (label, color) in zip(triangle_centers, triangle_labels):
        # Draw triangle vertices (fermion loop)
        size = 0.7
        vertices = [
            (cx, cy + size),
            (cx - size * 0.866, cy - size * 0.5),
            (cx + size * 0.866, cy - size * 0.5)
        ]

        # Draw triangle edges with arrows
        for i in range(3):
            start = vertices[i]
            end = vertices[(i + 1) % 3]
            ax.annotate('', xy=end, xytext=start,
                       arrowprops=dict(arrowstyle='->', color=color,
                                      lw=2, connectionstyle="arc3,rad=0.1"))

        # Add gauge boson lines (wiggly lines approximated)
        for vx, vy in vertices:
            dx = (vx - cx) * 0.5
            dy = (vy - cy) * 0.5
            ax.plot([vx, vx + dx], [vy, vy + dy],
                   color=PM_COLORS["orange"], lw=2, linestyle='--')
            ax.plot(vx + dx, vy + dy, 'o', color=PM_COLORS["orange"], markersize=6)

        # Label
        ax.text(cx, cy - 1.2, label, ha='center', va='center',
               fontsize=11, color=color, fontweight='bold')

    # ============================================================
    # MIDDLE SECTION: Cancellation Mechanism
    # ============================================================

    # Arrow pointing down
    ax.annotate('', xy=(5, 4.8), xytext=(5, 5.3),
               arrowprops=dict(arrowstyle='->', color=PM_COLORS["gold"], lw=3))

    # Central mechanism box
    mechanism_box = FancyBboxPatch(
        (2, 3.5), 6, 1.5,
        boxstyle="round,pad=0.03,rounding_size=0.15",
        facecolor=PM_COLORS["bg_card"],
        edgecolor=PM_COLORS["purple"],
        linewidth=3
    )
    ax.add_patch(mechanism_box)

    ax.text(5, 4.5, "G$_2$ Holonomy Constraint",
            ha='center', va='center', fontsize=14, fontweight='bold',
            color=PM_COLORS["purple"])

    ax.text(5, 3.9, r"$\sum_f Q_f^3 = 0$ via SO(10) embedding",
            ha='center', va='center', fontsize=12, color=PM_COLORS["text"])

    # ============================================================
    # BOTTOM LEFT: Fermion Charge Table
    # ============================================================

    # Table header
    ax.text(2, 2.5, "Fermion Charges per Generation",
            ha='center', va='center', fontsize=12, fontweight='bold',
            color=PM_COLORS["pink"])

    # Simplified fermion charge listing
    fermions = [
        ("$Q_L$ (u,d)", "+1/6", PM_COLORS["blue"]),
        ("$u_R$", "+2/3", PM_COLORS["blue"]),
        ("$d_R$", "-1/3", PM_COLORS["blue"]),
        ("$L$ (e,$\\nu$)", "-1/2", PM_COLORS["pink"]),
        ("$e_R$", "-1", PM_COLORS["pink"]),
    ]

    y_pos = 2.0
    for fermion, charge, color in fermions:
        ax.text(1.2, y_pos, fermion, ha='left', va='center', fontsize=10, color=color)
        ax.text(2.8, y_pos, f"Y = {charge}", ha='right', va='center', fontsize=10, color=PM_COLORS["text"])
        y_pos -= 0.35

    # ============================================================
    # BOTTOM RIGHT: Cancellation Sum
    # ============================================================

    ax.text(8, 2.5, "Anomaly Coefficients",
            ha='center', va='center', fontsize=12, fontweight='bold',
            color=PM_COLORS["green"])

    # Anomaly contributions
    contributions = [
        ("U(1)$_Y^3$:", "+6 - 4 - 1 + 2 - 2 = 0", PM_COLORS["purple"]),
        ("SU(2)$^2$U(1):", "+3 + 1 = 0 (with L)", PM_COLORS["pink"]),
        ("SU(3)$^2$U(1):", "+1 + 1 - 2 = 0", PM_COLORS["blue"]),
        ("Grav$^2$U(1):", "$\\sum Q = 0$", PM_COLORS["orange"]),
    ]

    y_pos = 2.0
    for label, formula, color in contributions:
        ax.text(6.5, y_pos, label, ha='left', va='center', fontsize=10, color=color)
        ax.text(9.5, y_pos, formula, ha='right', va='center', fontsize=9, color=PM_COLORS["text"])
        y_pos -= 0.4

    # ============================================================
    # BOTTOM: Final Result
    # ============================================================

    # Result box
    result_box = FancyBboxPatch(
        (2.5, -0.3), 5, 0.8,
        boxstyle="round,pad=0.02,rounding_size=0.1",
        facecolor=PM_COLORS["green"],
        edgecolor='white',
        linewidth=2,
        alpha=0.8
    )
    ax.add_patch(result_box)

    ax.text(5, 0.1, r"$\mathcal{A}_{total} = 0$ : Quantum Consistency",
            ha='center', va='center', fontsize=14, fontweight='bold',
            color='white')

    # Connection arrow from mechanism to result
    ax.annotate('', xy=(5, 0.5), xytext=(5, 3.5),
               arrowprops=dict(arrowstyle='->', color=PM_COLORS["green"], lw=2))

    # ============================================================
    # SIDE ANNOTATIONS
    # ============================================================

    # Left annotation: G2 manifold
    ax.text(0.2, 4.2, "G$_2$ Manifold\n$b_3 = 24$\nHodge diamond\nconstraints",
            ha='left', va='center', fontsize=9, color=PM_COLORS["purple"],
            bbox=dict(boxstyle='round', facecolor=PM_COLORS["bg_card"], alpha=0.8))

    # Right annotation: SO(10) embedding
    ax.text(10.3, 4.2, "SO(10) GUT\n$\\mathbf{16}$ spinor\ncontains all\nSM fermions",
            ha='right', va='center', fontsize=9, color=PM_COLORS["pink"],
            bbox=dict(boxstyle='round', facecolor=PM_COLORS["bg_card"], alpha=0.8))

    # Save figure
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight',
                facecolor=PM_COLORS["bg_dark"], edgecolor='none')
    plt.close()

    print(f"[OK] Anomaly cancellation diagram saved to {output_path}")
    return output_path


def plot_brst_cohomology(output_path: str = None):
    """
    Generate BRST cohomology structure visualization.

    Shows:
    - Ghost number grading (-2 to +2)
    - BRST operator Q action
    - Physical state space H^0(Q)
    - Connection to G2 topology (b3 = 24 physical states)

    Args:
        output_path: Output file path (default: ../../images/brst-cohomology.png)
    """
    if output_path is None:
        output_path = OUTPUT_DIR / "brst-cohomology.png"

    set_dark_style()
    fig, ax = plt.subplots(figsize=(12, 10), facecolor=PM_COLORS["bg_dark"])
    ax.set_facecolor(PM_COLORS["bg_dark"])

    # Title
    ax.set_title("BRST Cohomology Structure in G$_2$ Gauge Theory",
                 fontsize=18, fontweight='bold', color=PM_COLORS["text"], pad=20)

    # Remove axes
    ax.set_xlim(-0.5, 10.5)
    ax.set_ylim(-0.5, 9)
    ax.axis('off')

    # ============================================================
    # TOP: Ghost Number Grading
    # ============================================================

    ax.text(5, 8.5, "Ghost Number Decomposition",
            ha='center', va='center', fontsize=14, fontweight='bold',
            color=PM_COLORS["gold"])

    # Ghost number levels
    ghost_levels = [
        (-2, "$\\mathcal{F}^{-2}$", "Anti-ghost squared", PM_COLORS["red"]),
        (-1, "$\\mathcal{F}^{-1}$", "Anti-ghost ($\\bar{c}$)", PM_COLORS["orange"]),
        (0, "$\\mathcal{F}^{0}$", "Physical fields", PM_COLORS["green"]),
        (+1, "$\\mathcal{F}^{+1}$", "Ghost ($c$)", PM_COLORS["blue"]),
        (+2, "$\\mathcal{F}^{+2}$", "Ghost squared", PM_COLORS["purple"]),
    ]

    box_y = 7.2
    box_height = 0.6
    box_width = 1.6
    spacing = 2.0

    for i, (gh_num, symbol, desc, color) in enumerate(ghost_levels):
        x = 1 + i * spacing

        # Box for each ghost level
        rect = FancyBboxPatch(
            (x - box_width/2, box_y - box_height/2), box_width, box_height,
            boxstyle="round,pad=0.02,rounding_size=0.08",
            facecolor=color,
            edgecolor='white',
            linewidth=2,
            alpha=0.8
        )
        ax.add_patch(rect)

        # Ghost number label
        ax.text(x, box_y, symbol, ha='center', va='center',
               fontsize=11, fontweight='bold', color='white')

        # Description below
        ax.text(x, box_y - 0.6, desc, ha='center', va='center',
               fontsize=8, color=color)

        # Ghost number indicator above
        ax.text(x, box_y + 0.5, f"gh# = {gh_num:+d}",
               ha='center', va='center', fontsize=9, color=PM_COLORS["text"])

    # ============================================================
    # MIDDLE: BRST Operator and Cohomology
    # ============================================================

    # BRST operator Q arrows between levels
    ax.text(5, 5.8, "BRST Operator $Q$ : $Q^2 = 0$",
            ha='center', va='center', fontsize=14, fontweight='bold',
            color=PM_COLORS["pink"])

    # Draw Q action arrows
    for i in range(4):
        x1 = 1 + i * spacing + box_width/2 + 0.1
        x2 = 1 + (i + 1) * spacing - box_width/2 - 0.1

        # Curved arrow
        ax.annotate('', xy=(x2, box_y), xytext=(x1, box_y),
                   arrowprops=dict(arrowstyle='->', color=PM_COLORS["pink"],
                                  lw=2, connectionstyle="arc3,rad=-0.2"))

        # Q label on arrow
        ax.text((x1 + x2)/2, box_y + 0.25, "Q",
               ha='center', va='center', fontsize=10, color=PM_COLORS["pink"])

    # ============================================================
    # Cohomology diagram
    # ============================================================

    # Central cohomology representation
    cohom_y = 4.2

    ax.text(5, cohom_y + 0.8, "Physical States = Cohomology $H^\\bullet(Q)$",
            ha='center', va='center', fontsize=12, fontweight='bold',
            color=PM_COLORS["green"])

    # Cohomology boxes
    cohom_levels = [
        ("$H^{-1}(Q)$", "= 0", PM_COLORS["orange"]),
        ("$H^{0}(Q)$", "= Physical", PM_COLORS["green"]),
        ("$H^{+1}(Q)$", "= 0", PM_COLORS["blue"]),
    ]

    for i, (symbol, value, color) in enumerate(cohom_levels):
        x = 3 + i * 2

        # Box
        rect = FancyBboxPatch(
            (x - 0.8, cohom_y - 0.4), 1.6, 0.8,
            boxstyle="round,pad=0.02,rounding_size=0.08",
            facecolor=PM_COLORS["bg_card"],
            edgecolor=color,
            linewidth=2
        )
        ax.add_patch(rect)

        ax.text(x, cohom_y + 0.1, symbol, ha='center', va='center',
               fontsize=11, fontweight='bold', color=color)
        ax.text(x, cohom_y - 0.2, value, ha='center', va='center',
               fontsize=10, color=PM_COLORS["text"])

    # ============================================================
    # BOTTOM: Connection to G2 Topology
    # ============================================================

    # Arrow down to G2 connection
    ax.annotate('', xy=(5, 2.8), xytext=(5, 3.5),
               arrowprops=dict(arrowstyle='->', color=PM_COLORS["purple"], lw=3))

    # G2 topology box
    g2_box = FancyBboxPatch(
        (1.5, 0.8), 7, 2,
        boxstyle="round,pad=0.03,rounding_size=0.15",
        facecolor=PM_COLORS["bg_card"],
        edgecolor=PM_COLORS["purple"],
        linewidth=3
    )
    ax.add_patch(g2_box)

    ax.text(5, 2.4, "Connection to G$_2$ Manifold Topology",
            ha='center', va='center', fontsize=13, fontweight='bold',
            color=PM_COLORS["purple"])

    # Key relationship
    ax.text(5, 1.8, r"dim $H^0(Q)$ = $b_3$(G$_2$) = 24",
            ha='center', va='center', fontsize=14, fontweight='bold',
            color=PM_COLORS["gold"])

    ax.text(5, 1.3, "Third Betti number counts independent 3-cycles",
            ha='center', va='center', fontsize=11, color=PM_COLORS["text"])

    ax.text(5, 0.95, r"$\Rightarrow$ 24 physical gauge field degrees of freedom",
            ha='center', va='center', fontsize=11, color=PM_COLORS["green"])

    # ============================================================
    # SIDE ANNOTATIONS
    # ============================================================

    # Left: BRST transformation
    brst_box = FancyBboxPatch(
        (0, 3), 2.2, 2,
        boxstyle="round,pad=0.02,rounding_size=0.1",
        facecolor=PM_COLORS["bg_card"],
        edgecolor=PM_COLORS["blue"],
        linewidth=2,
        alpha=0.9
    )
    ax.add_patch(brst_box)

    ax.text(1.1, 4.7, "BRST Action",
            ha='center', va='center', fontsize=10, fontweight='bold',
            color=PM_COLORS["blue"])
    ax.text(1.1, 4.3, "$Qc = c \\wedge c$",
            ha='center', va='center', fontsize=10, color=PM_COLORS["text"])
    ax.text(1.1, 3.9, "$Q\\bar{c} = B$",
            ha='center', va='center', fontsize=10, color=PM_COLORS["text"])
    ax.text(1.1, 3.5, "$QA = D_A c$",
            ha='center', va='center', fontsize=10, color=PM_COLORS["text"])
    ax.text(1.1, 3.1, "$Q\\psi = c \\cdot \\psi$",
            ha='center', va='center', fontsize=10, color=PM_COLORS["text"])

    # Right: Physical states
    phys_box = FancyBboxPatch(
        (8.3, 3), 2.2, 2,
        boxstyle="round,pad=0.02,rounding_size=0.1",
        facecolor=PM_COLORS["bg_card"],
        edgecolor=PM_COLORS["green"],
        linewidth=2,
        alpha=0.9
    )
    ax.add_patch(phys_box)

    ax.text(9.4, 4.7, "Physical States",
            ha='center', va='center', fontsize=10, fontweight='bold',
            color=PM_COLORS["green"])
    ax.text(9.4, 4.3, "$Q|\\psi\\rangle = 0$",
            ha='center', va='center', fontsize=10, color=PM_COLORS["text"])
    ax.text(9.4, 3.9, "Q-closed",
            ha='center', va='center', fontsize=9, color=PM_COLORS["text"])
    ax.text(9.4, 3.5, "$|\\psi\\rangle \\neq Q|\\chi\\rangle$",
            ha='center', va='center', fontsize=10, color=PM_COLORS["text"])
    ax.text(9.4, 3.1, "Not Q-exact",
            ha='center', va='center', fontsize=9, color=PM_COLORS["text"])

    # Nilpotency note
    ax.text(5, 5.3, "Nilpotency $Q^2 = 0$ ensures gauge invariance of physical observables",
            ha='center', va='center', fontsize=10, style='italic',
            color=PM_COLORS["text"])

    # Save figure
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight',
                facecolor=PM_COLORS["bg_dark"], edgecolor='none')
    plt.close()

    print(f"[OK] BRST cohomology diagram saved to {output_path}")
    return output_path


def generate_all():
    """Generate all gauge theory diagrams."""
    print("=" * 70)
    print("GAUGE THEORY DIAGRAMS FOR PRINCIPIA METAPHYSICA")
    print("=" * 70)
    print()

    output_dir = OUTPUT_DIR
    print(f"Output directory: {output_dir}")
    print()

    # Ensure output directory exists
    output_dir.mkdir(parents=True, exist_ok=True)

    # Generate diagrams
    print("Generating diagrams...")
    print()

    plot_anomaly_cancellation()
    plot_brst_cohomology()

    print()
    print("=" * 70)
    print("[SUCCESS] All gauge theory diagrams generated!")
    print("=" * 70)
    print()
    print("Files:")
    print(f"  1. {output_dir / 'anomaly-cancellation.png'}")
    print(f"  2. {output_dir / 'brst-cohomology.png'}")
    print()


if __name__ == "__main__":
    generate_all()
