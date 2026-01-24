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
GUT Diagrams for Principia Metaphysica
=======================================

Generates publication-quality visualizations for Grand Unified Theory concepts:
1. so10-breaking.png - SO(10) -> SU(5) -> SM symmetry breaking chain
2. sp2r-gauge-symmetry.png - Sp(2,R) gauge symmetry in two-time physics

Output directory: ../../images/ (project root images folder)

Physics Background:
- SO(10) unifies all SM fermions in a single 16-dimensional spinor representation
- Breaking chain: SO(10) -> SU(5) -> SU(3)xSU(2)xU(1) occurs at M_GUT ~ 10^16 GeV
- Sp(2,R) gauge symmetry constrains two-time physics in the PM framework
- Connection to G2 holonomy manifold provides geometric origin

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.

Dedicated To:
    My Wife: Elizabeth May Watts
    Our Messiah: Jesus Of Nazareth
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle, Ellipse
from matplotlib.patches import ConnectionPatch, Polygon, Rectangle
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


def draw_symmetry_box(ax, x, y, width, height, group_name, dim, color, rank=None):
    """Draw a decorated box representing a symmetry group."""
    # Main box
    rect = FancyBboxPatch(
        (x - width/2, y - height/2), width, height,
        boxstyle="round,pad=0.02,rounding_size=0.12",
        facecolor=color,
        edgecolor='white',
        linewidth=2.5,
        alpha=0.85
    )
    ax.add_patch(rect)

    # Group name
    txt = ax.text(x, y + 0.15, group_name, ha='center', va='center',
                  fontsize=14, fontweight='bold', color='white')
    txt.set_path_effects([
        path_effects.withStroke(linewidth=2, foreground='black')
    ])

    # Dimension
    ax.text(x, y - 0.25, f"dim = {dim}", ha='center', va='center',
           fontsize=10, color='white', alpha=0.9)

    if rank is not None:
        ax.text(x, y - 0.5, f"rank = {rank}", ha='center', va='center',
               fontsize=9, color='white', alpha=0.8)

    return rect


def draw_breaking_arrow(ax, x1, y1, x2, y2, label, mechanism, scale, color):
    """Draw a symmetry breaking arrow with annotations."""
    # Main arrow
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
               arrowprops=dict(arrowstyle='-|>', color=color,
                              lw=3, mutation_scale=20))

    # Midpoint for labels
    mx, my = (x1 + x2) / 2, (y1 + y2) / 2

    # Scale label (above arrow)
    ax.text(mx, my + 0.25, scale, ha='center', va='center',
           fontsize=10, fontweight='bold', color=PM_COLORS["gold"])

    # Mechanism label (below arrow)
    ax.text(mx, my - 0.25, mechanism, ha='center', va='center',
           fontsize=9, color=PM_COLORS["text"], style='italic')


def plot_so10_breaking(output_path: str = None):
    """
    Generate SO(10) -> SU(5) -> SM symmetry breaking diagram.

    Shows:
    - Complete breaking chain from SO(10) to Standard Model
    - Energy scales at each breaking step
    - Higgs mechanisms involved
    - Fermion representations at each stage
    - Connection to G2 geometry

    Args:
        output_path: Output file path (default: ../../images/so10-breaking.png)
    """
    if output_path is None:
        output_path = OUTPUT_DIR / "so10-breaking.png"

    set_dark_style()
    fig, ax = plt.subplots(figsize=(14, 11), facecolor=PM_COLORS["bg_dark"])
    ax.set_facecolor(PM_COLORS["bg_dark"])

    # Title
    ax.set_title("SO(10) Grand Unification Breaking Chain",
                 fontsize=20, fontweight='bold', color=PM_COLORS["text"], pad=25)

    # Remove axes
    ax.set_xlim(-1, 15)
    ax.set_ylim(-1, 11)
    ax.axis('off')

    # ============================================================
    # TOP: Energy Scale Axis
    # ============================================================

    # Draw energy scale arrow
    ax.annotate('', xy=(14, 9.5), xytext=(0, 9.5),
               arrowprops=dict(arrowstyle='->', color=PM_COLORS["text"], lw=2))
    ax.text(7, 9.8, "Energy Scale (GeV)", ha='center', va='center',
           fontsize=12, color=PM_COLORS["text"])

    # Scale markers
    scales = [
        (1.5, "$M_{Pl}$\n$10^{19}$", PM_COLORS["purple"]),
        (4.5, "$M_{GUT}$\n$2 \\times 10^{16}$", PM_COLORS["pink"]),
        (8, "$M_{PS}$\n$10^{12}$", PM_COLORS["blue"]),
        (11, "$M_{EW}$\n$10^{2}$", PM_COLORS["green"]),
    ]

    for x, label, color in scales:
        ax.plot([x, x], [9.3, 9.7], color=color, lw=2)
        ax.text(x, 10.1, label, ha='center', va='center', fontsize=9, color=color)

    # ============================================================
    # MAIN: Symmetry Breaking Chain
    # ============================================================

    # Level 1: SO(10) at Planck/GUT scale
    draw_symmetry_box(ax, 3, 7.5, 2.5, 1.2, "SO(10)", 45, PM_COLORS["purple"], rank=5)

    # Level 2: SU(5) x U(1)_X
    draw_symmetry_box(ax, 6.5, 5.5, 2.8, 1.2, "SU(5) x U(1)$_X$", "24 + 1", PM_COLORS["pink"], rank=5)

    # Alternative path: Pati-Salam
    draw_symmetry_box(ax, 10, 7.5, 3.2, 1.0, "SU(4)$_C$ x SU(2)$_L$ x SU(2)$_R$", "15 + 3 + 3", PM_COLORS["blue"], rank=5)

    # Level 3: Standard Model
    draw_symmetry_box(ax, 10, 3.5, 3.5, 1.4, "SU(3)$_C$ x SU(2)$_L$ x U(1)$_Y$", "8 + 3 + 1", PM_COLORS["green"], rank=4)

    # Level 4: Low energy (after EW symmetry breaking)
    draw_symmetry_box(ax, 10, 1, 2.5, 1.0, "SU(3)$_C$ x U(1)$_{EM}$", "8 + 1", PM_COLORS["orange"], rank=2)

    # ============================================================
    # Breaking Arrows
    # ============================================================

    # SO(10) -> SU(5) x U(1)_X
    draw_breaking_arrow(ax, 4.2, 7.2, 5.2, 5.9,
                       "Breaking 1", "126$_H$ Higgs", "$M_{GUT}$", PM_COLORS["pink"])

    # SO(10) -> Pati-Salam (alternative)
    draw_breaking_arrow(ax, 4.2, 7.8, 8.5, 7.8,
                       "Alt. Path", "54$_H$ Higgs", "$M_{GUT}$", PM_COLORS["blue"])

    # SU(5) -> SM
    ax.annotate('', xy=(8.5, 4), xytext=(7.5, 5.2),
               arrowprops=dict(arrowstyle='-|>', color=PM_COLORS["green"],
                              lw=3, mutation_scale=20))
    ax.text(7.7, 4.6, "$24_H$\nHiggs", ha='center', va='center',
           fontsize=9, color=PM_COLORS["text"], style='italic')

    # Pati-Salam -> SM
    ax.annotate('', xy=(10, 4.2), xytext=(10, 7),
               arrowprops=dict(arrowstyle='-|>', color=PM_COLORS["green"],
                              lw=3, mutation_scale=20))
    ax.text(10.6, 5.6, "$M_{PS}$", ha='left', va='center',
           fontsize=10, fontweight='bold', color=PM_COLORS["gold"])

    # SM -> SU(3) x U(1)_EM
    draw_breaking_arrow(ax, 10, 2.8, 10, 1.7,
                       "EW Breaking", "Higgs doublet", "$v = 246$ GeV", PM_COLORS["orange"])

    # ============================================================
    # FERMION REPRESENTATIONS
    # ============================================================

    # Left side: Fermion content
    fermion_box = FancyBboxPatch(
        (0, 1.5), 2.5, 4.5,
        boxstyle="round,pad=0.02,rounding_size=0.1",
        facecolor=PM_COLORS["bg_card"],
        edgecolor=PM_COLORS["gold"],
        linewidth=2
    )
    ax.add_patch(fermion_box)

    ax.text(1.25, 5.7, "Fermion Unification",
            ha='center', va='center', fontsize=11, fontweight='bold',
            color=PM_COLORS["gold"])

    fermion_reps = [
        ("SO(10):", "$\\mathbf{16}$ spinor", PM_COLORS["purple"]),
        ("", "All SM fermions + $\\nu_R$", PM_COLORS["text"]),
        ("", "", PM_COLORS["text"]),
        ("SU(5):", "$\\mathbf{\\bar{5}} + \\mathbf{10}$", PM_COLORS["pink"]),
        ("", "$(d^c, L) + (Q, u^c, e^c)$", PM_COLORS["text"]),
        ("", "", PM_COLORS["text"]),
        ("SM:", "$(Q, u, d, L, e, \\nu)$", PM_COLORS["green"]),
        ("", "per generation", PM_COLORS["text"]),
    ]

    y_pos = 5.2
    for label, value, color in fermion_reps:
        if label:
            ax.text(0.2, y_pos, label, ha='left', va='center',
                   fontsize=9, fontweight='bold', color=color)
        ax.text(2.3, y_pos, value, ha='right', va='center',
               fontsize=9, color=color if label else PM_COLORS["text"])
        y_pos -= 0.45

    # ============================================================
    # G2 CONNECTION (Bottom Right)
    # ============================================================

    g2_box = FancyBboxPatch(
        (11.5, 0), 3, 3,
        boxstyle="round,pad=0.02,rounding_size=0.1",
        facecolor=PM_COLORS["bg_card"],
        edgecolor=PM_COLORS["purple"],
        linewidth=2
    )
    ax.add_patch(g2_box)

    ax.text(13, 2.7, "G$_2$ Geometry Origin",
            ha='center', va='center', fontsize=11, fontweight='bold',
            color=PM_COLORS["purple"])

    g2_content = [
        "M-theory on G$_2$ manifold",
        "7D $\\rightarrow$ 4D reduction",
        "$b_3 = 24$ moduli fields",
        "Torsion class determines",
        "$M_{GUT} = 2.1 \\times 10^{16}$ GeV",
    ]

    y_pos = 2.2
    for line in g2_content:
        ax.text(13, y_pos, line, ha='center', va='center',
               fontsize=9, color=PM_COLORS["text"])
        y_pos -= 0.4

    # ============================================================
    # GAUGE COUPLING EVOLUTION (Top Right)
    # ============================================================

    # Small inset showing coupling unification
    ax.text(12.5, 6.5, "Gauge Coupling Evolution",
            ha='center', va='center', fontsize=10, fontweight='bold',
            color=PM_COLORS["text"])

    # Simplified RG running plot
    inset_x = np.array([12, 12.5, 13])
    inset_y_base = 5

    # Three lines representing alpha_1, alpha_2, alpha_3
    ax.plot([11.5, 12.5], [inset_y_base + 0.8, inset_y_base + 0.3],
           color=PM_COLORS["red"], lw=2, label="$\\alpha_1^{-1}$")
    ax.plot([11.5, 12.5], [inset_y_base + 0.2, inset_y_base + 0.3],
           color=PM_COLORS["blue"], lw=2, label="$\\alpha_2^{-1}$")
    ax.plot([11.5, 12.5], [inset_y_base - 0.4, inset_y_base + 0.3],
           color=PM_COLORS["green"], lw=2, label="$\\alpha_3^{-1}$")

    # Convergence point
    ax.plot(12.5, inset_y_base + 0.3, 'o', color=PM_COLORS["gold"], markersize=10)
    ax.text(12.7, inset_y_base + 0.3, "$\\alpha_{GUT}$",
           ha='left', va='center', fontsize=9, color=PM_COLORS["gold"])

    # Axis labels for inset
    ax.text(11.5, inset_y_base - 0.8, "$M_Z$", ha='center', va='center',
           fontsize=8, color=PM_COLORS["text"])
    ax.text(12.5, inset_y_base - 0.8, "$M_{GUT}$", ha='center', va='center',
           fontsize=8, color=PM_COLORS["text"])

    # ============================================================
    # KEY PREDICTIONS BOX
    # ============================================================

    pred_box = FancyBboxPatch(
        (0, -0.8), 5, 1.5,
        boxstyle="round,pad=0.02,rounding_size=0.1",
        facecolor=PM_COLORS["green"],
        edgecolor='white',
        linewidth=2,
        alpha=0.8
    )
    ax.add_patch(pred_box)

    ax.text(2.5, 0.3, "Key PM Predictions",
            ha='center', va='center', fontsize=11, fontweight='bold',
            color='white')
    ax.text(2.5, -0.1, "$M_{GUT} = (2.1 \\pm 0.1) \\times 10^{16}$ GeV",
            ha='center', va='center', fontsize=10, color='white')
    ax.text(2.5, -0.45, "$\\alpha_{GUT}^{-1} = 23.54$ (geometric)",
            ha='center', va='center', fontsize=10, color='white')

    # Save figure
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight',
                facecolor=PM_COLORS["bg_dark"], edgecolor='none')
    plt.close()

    print(f"[OK] SO(10) breaking diagram saved to {output_path}")
    return output_path


def plot_sp2r_gauge_symmetry(output_path: str = None):
    """
    Generate Sp(2,R) gauge symmetry diagram for two-time physics.

    Shows:
    - Sp(2,R) as local symmetry of two-time phase space
    - Constraint structure eliminating ghost degrees of freedom
    - Connection to conformal symmetry in 1T physics
    - Gauge fixing to Standard Model 1-time formulation

    Args:
        output_path: Output file path (default: ../../images/sp2r-gauge-symmetry.png)
    """
    if output_path is None:
        output_path = OUTPUT_DIR / "sp2r-gauge-symmetry.png"

    set_dark_style()
    fig, ax = plt.subplots(figsize=(14, 11), facecolor=PM_COLORS["bg_dark"])
    ax.set_facecolor(PM_COLORS["bg_dark"])

    # Title
    ax.set_title("Sp(2,R) Gauge Symmetry in Two-Time Physics",
                 fontsize=20, fontweight='bold', color=PM_COLORS["text"], pad=25)

    # Remove axes
    ax.set_xlim(-1, 15)
    ax.set_ylim(-1, 11)
    ax.axis('off')

    # ============================================================
    # TOP: Two-Time Phase Space
    # ============================================================

    ax.text(7, 10.2, "Two-Time Phase Space: (d+2, 2) Signature",
            ha='center', va='center', fontsize=14, fontweight='bold',
            color=PM_COLORS["gold"])

    # Phase space representation
    phase_box = FancyBboxPatch(
        (2, 8), 10, 1.8,
        boxstyle="round,pad=0.02,rounding_size=0.15",
        facecolor=PM_COLORS["bg_card"],
        edgecolor=PM_COLORS["purple"],
        linewidth=3
    )
    ax.add_patch(phase_box)

    ax.text(7, 9.4, "Extended Phase Space: $(X^M, P^M)$ with $M = 0, 1, ..., d+1$",
            ha='center', va='center', fontsize=12, fontweight='bold',
            color=PM_COLORS["purple"])

    ax.text(7, 8.9, "$\\eta^{MN} = \\text{diag}(-1, -1, +1, +1, ..., +1)$ : Two timelike directions",
            ha='center', va='center', fontsize=11, color=PM_COLORS["text"])

    ax.text(7, 8.4, "Total dimensions: $2(d+2) = 2 \\times 6 = 12$ for $d=4$",
            ha='center', va='center', fontsize=10, color=PM_COLORS["pink"])

    # ============================================================
    # MIDDLE: Sp(2,R) Structure
    # ============================================================

    # Sp(2,R) group box
    sp2r_box = FancyBboxPatch(
        (1, 4.5), 5, 2.8,
        boxstyle="round,pad=0.02,rounding_size=0.12",
        facecolor=PM_COLORS["pink"],
        edgecolor='white',
        linewidth=3,
        alpha=0.85
    )
    ax.add_patch(sp2r_box)

    ax.text(3.5, 6.9, "Sp(2,R) Gauge Group",
            ha='center', va='center', fontsize=14, fontweight='bold',
            color='white')

    # Sp(2,R) generators
    ax.text(3.5, 6.3, "Generators: $\\{J^{ab}\\}$ with $a,b \\in \\{1,2\\}$",
            ha='center', va='center', fontsize=11, color='white')
    ax.text(3.5, 5.8, "dim Sp(2,R) = 3",
            ha='center', va='center', fontsize=10, color='white', alpha=0.9)

    ax.text(3.5, 5.2, "$J^{11} \\propto X \\cdot P$",
            ha='center', va='center', fontsize=10, color='white')
    ax.text(3.5, 4.8, "$J^{12} \\propto \\frac{1}{2}(X^2 + P^2)$",
            ha='center', va='center', fontsize=10, color='white')
    ax.text(3.5, 4.4, "$J^{22} \\propto \\frac{1}{2}(X^2 - P^2)$",
            ha='center', va='center', fontsize=10, color='white')

    # Constraints box
    const_box = FancyBboxPatch(
        (8, 4.5), 5.5, 2.8,
        boxstyle="round,pad=0.02,rounding_size=0.12",
        facecolor=PM_COLORS["blue"],
        edgecolor='white',
        linewidth=3,
        alpha=0.85
    )
    ax.add_patch(const_box)

    ax.text(10.75, 6.9, "First-Class Constraints",
            ha='center', va='center', fontsize=14, fontweight='bold',
            color='white')

    ax.text(10.75, 6.3, "$X^M X_M = 0$ (massless in 2T)",
            ha='center', va='center', fontsize=11, color='white')
    ax.text(10.75, 5.8, "$X^M P_M = 0$ (gauge constraint)",
            ha='center', va='center', fontsize=11, color='white')
    ax.text(10.75, 5.3, "$P^M P_M = 0$ (null momentum)",
            ha='center', va='center', fontsize=11, color='white')

    ax.text(10.75, 4.7, "Removes 3 + 3 = 6 d.o.f.",
            ha='center', va='center', fontsize=10, color='white', alpha=0.9)

    # Arrow between boxes
    ax.annotate('', xy=(7.9, 5.9), xytext=(6.1, 5.9),
               arrowprops=dict(arrowstyle='<->', color=PM_COLORS["gold"],
                              lw=3, mutation_scale=20))
    ax.text(7, 6.3, "Generate",
            ha='center', va='center', fontsize=10, color=PM_COLORS["gold"])

    # ============================================================
    # BOTTOM: Gauge Fixing to 1T Physics
    # ============================================================

    ax.text(7, 3.5, "Gauge Fixing: 2T $\\rightarrow$ 1T Physics",
            ha='center', va='center', fontsize=14, fontweight='bold',
            color=PM_COLORS["orange"])

    # 1T result box
    result_box = FancyBboxPatch(
        (2, 0.3), 10, 2.5,
        boxstyle="round,pad=0.02,rounding_size=0.12",
        facecolor=PM_COLORS["green"],
        edgecolor='white',
        linewidth=3,
        alpha=0.85
    )
    ax.add_patch(result_box)

    ax.text(7, 2.5, "Standard Model in 1-Time",
            ha='center', va='center', fontsize=14, fontweight='bold',
            color='white')

    ax.text(7, 2, "$(X^M, P^M)$ with 12 d.o.f.  $\\longrightarrow$  $(x^\\mu, p^\\mu)$ with 8 d.o.f.",
            ha='center', va='center', fontsize=11, color='white')

    ax.text(7, 1.5, "Gauge choice: $X^+ = \\tau$ (proper time) + conformal frame",
            ha='center', va='center', fontsize=10, color='white')

    ax.text(7, 1, "Result: Lorentz-covariant 4D physics with single time",
            ha='center', va='center', fontsize=10, color='white')

    ax.text(7, 0.5, "Conformal symmetry SO(4,2) emerges as residual gauge symmetry",
            ha='center', va='center', fontsize=10, color=PM_COLORS["gold"], fontweight='bold')

    # Arrows from constraints to result
    ax.annotate('', xy=(5, 2.8), xytext=(4, 4.4),
               arrowprops=dict(arrowstyle='->', color=PM_COLORS["green"],
                              lw=2, connectionstyle="arc3,rad=0.2"))
    ax.annotate('', xy=(9, 2.8), xytext=(10, 4.4),
               arrowprops=dict(arrowstyle='->', color=PM_COLORS["green"],
                              lw=2, connectionstyle="arc3,rad=-0.2"))

    # ============================================================
    # LEFT ANNOTATION: Symplectic Structure
    # ============================================================

    symp_box = FancyBboxPatch(
        (-0.8, 0.3), 2.5, 3.5,
        boxstyle="round,pad=0.02,rounding_size=0.1",
        facecolor=PM_COLORS["bg_card"],
        edgecolor=PM_COLORS["purple"],
        linewidth=2
    )
    ax.add_patch(symp_box)

    ax.text(0.45, 3.5, "Symplectic Form",
            ha='center', va='center', fontsize=10, fontweight='bold',
            color=PM_COLORS["purple"])

    symp_content = [
        "$\\omega = dX^M \\wedge dP_M$",
        "",
        "Preserved by Sp(2,R):",
        "$\\omega(g \\cdot v, g \\cdot w)$",
        "$= \\omega(v, w)$",
        "",
        "Poisson bracket:",
        "$\\{X^M, P_N\\} = \\delta^M_N$",
    ]

    y_pos = 3.1
    for line in symp_content:
        ax.text(0.45, y_pos, line, ha='center', va='center',
               fontsize=9, color=PM_COLORS["text"])
        y_pos -= 0.35

    # ============================================================
    # RIGHT ANNOTATION: Physical Implications
    # ============================================================

    phys_box = FancyBboxPatch(
        (12.3, 0.3), 2.7, 3.5,
        boxstyle="round,pad=0.02,rounding_size=0.1",
        facecolor=PM_COLORS["bg_card"],
        edgecolor=PM_COLORS["gold"],
        linewidth=2
    )
    ax.add_patch(phys_box)

    ax.text(13.65, 3.5, "Physical Content",
            ha='center', va='center', fontsize=10, fontweight='bold',
            color=PM_COLORS["gold"])

    phys_content = [
        "No ghosts:",
        "Sp(2,R) removes",
        "negative norm states",
        "",
        "Hidden symmetries:",
        "Same 2T action yields",
        "different 1T physics",
        "(H-atom, oscillator, etc.)",
    ]

    y_pos = 3.1
    for line in phys_content:
        ax.text(13.65, y_pos, line, ha='center', va='center',
               fontsize=9, color=PM_COLORS["text"])
        y_pos -= 0.35

    # ============================================================
    # CONNECTING ARROW FROM TOP TO MIDDLE
    # ============================================================

    ax.annotate('', xy=(7, 7.3), xytext=(7, 7.9),
               arrowprops=dict(arrowstyle='->', color=PM_COLORS["gold"],
                              lw=3, mutation_scale=20))
    ax.text(7.5, 7.6, "Local Gauge Symmetry",
            ha='left', va='center', fontsize=10, color=PM_COLORS["gold"])

    # ============================================================
    # G2 CONNECTION NOTE
    # ============================================================

    g2_note = FancyBboxPatch(
        (9.5, 7.5), 4.5, 0.7,
        boxstyle="round,pad=0.02,rounding_size=0.08",
        facecolor=PM_COLORS["purple"],
        edgecolor='white',
        linewidth=2,
        alpha=0.8
    )
    ax.add_patch(g2_note)

    ax.text(11.75, 7.85, "In PM: Sp(2,R) $\\subset$ SO(24,2) bulk symmetry",
            ha='center', va='center', fontsize=10, fontweight='bold',
            color='white')

    # Save figure
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight',
                facecolor=PM_COLORS["bg_dark"], edgecolor='none')
    plt.close()

    print(f"[OK] Sp(2,R) gauge symmetry diagram saved to {output_path}")
    return output_path


def generate_all():
    """Generate all GUT diagrams."""
    print("=" * 70)
    print("GUT DIAGRAMS FOR PRINCIPIA METAPHYSICA")
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

    plot_so10_breaking()
    plot_sp2r_gauge_symmetry()

    print()
    print("=" * 70)
    print("[SUCCESS] All GUT diagrams generated!")
    print("=" * 70)
    print()
    print("Files:")
    print(f"  1. {output_dir / 'so10-breaking.png'}")
    print(f"  2. {output_dir / 'sp2r-gauge-symmetry.png'}")
    print()


if __name__ == "__main__":
    generate_all()
