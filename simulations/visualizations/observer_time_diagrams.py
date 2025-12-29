#!/usr/bin/env python3
"""
PRINCIPIA METAPHYSICA - Observer and Consciousness Time Visualization Diagrams
===============================================================================

Licensed under the MIT License. See LICENSE file for details.

Generates visualization diagrams for observer and consciousness concepts:
1. observer-time-selection.png - How observers select their time direction
2. subjective-time.png - Connection between physical and subjective time experience

THEORETICAL FOUNDATION:
    In the PM framework, observers select a time direction through interaction
    with the Pneuma field's entropy gradient. The subjective experience of time
    emerges from the interface between physical thermal time and conscious
    information processing.

    Key concepts:
    - Observer-dependent time selection via decoherence
    - Pneuma field mediates consciousness-time interface
    - Information flow determines subjective time rate
    - Two-time structure allows observer flexibility

REFERENCES:
    - Connes, Rovelli (1994) arXiv:gr-qc/9406019
    - Penrose, Hameroff - Orchestrated Objective Reduction
    - PM framework: Pneuma mechanism and consciousness

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
    from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Circle, Wedge, Ellipse
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
    "gold": "#fbbf24",        # Accent gold
    "orange": "#fb923c",      # Accent orange
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


def draw_brain_icon(ax, center, size, color):
    """Draw a simplified brain icon at the specified location."""
    x, y = center

    # Brain outline (simplified oval shapes)
    # Left hemisphere
    left = Ellipse((x - size * 0.15, y), size * 0.35, size * 0.45,
                   facecolor=color, edgecolor=PM_COLORS["dark_purple"],
                   linewidth=1.5, alpha=0.8)
    ax.add_patch(left)

    # Right hemisphere
    right = Ellipse((x + size * 0.15, y), size * 0.35, size * 0.45,
                    facecolor=color, edgecolor=PM_COLORS["dark_purple"],
                    linewidth=1.5, alpha=0.8)
    ax.add_patch(right)

    # Center connection
    center_oval = Ellipse((x, y), size * 0.2, size * 0.3,
                          facecolor=color, edgecolor='none')
    ax.add_patch(center_oval)


def draw_eye_icon(ax, center, size, color):
    """Draw a simplified eye icon at the specified location."""
    x, y = center

    # Eye outline
    eye = Ellipse((x, y), size * 0.5, size * 0.25,
                  facecolor=PM_COLORS["white"],
                  edgecolor=PM_COLORS["text"], linewidth=1.5)
    ax.add_patch(eye)

    # Iris
    iris = Circle((x, y), size * 0.08,
                  facecolor=color, edgecolor=PM_COLORS["dark_blue"])
    ax.add_patch(iris)

    # Pupil
    pupil = Circle((x, y), size * 0.03, facecolor=PM_COLORS["text"])
    ax.add_patch(pupil)


def generate_observer_time_selection_diagram(output_path: str = "../../images/observer-time-selection.png"):
    """
    Generate the Observer Time Selection diagram.

    Visualizes:
    - How observers select their time direction from two-time structure
    - Decoherence mechanism for time selection
    - Entropy gradient guiding observer's time
    - Information flow arrows
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
    ax.text(0.5, 1.02, "Observer Time Direction Selection",
            fontsize=16, fontweight='bold', ha='center', va='bottom',
            color=PM_COLORS["text"])
    ax.text(0.5, 0.97, "From Two-Time Framework to Single Observer Time",
            fontsize=12, ha='center', va='bottom', style='italic',
            color=PM_COLORS["gray"])

    # === TWO-TIME STRUCTURE (Top) ===
    two_time_box = FancyBboxPatch(
        (0.15, 0.78), 0.70, 0.15,
        boxstyle="round,pad=0.01,rounding_size=0.02",
        facecolor="#f3e8ff",
        edgecolor=PM_COLORS["purple"],
        linewidth=2
    )
    ax.add_patch(two_time_box)

    ax.text(0.50, 0.905, "TWO-TIME STRUCTURE", fontsize=12, fontweight='bold',
            ha='center', color=PM_COLORS["dark_purple"])
    ax.text(0.50, 0.865, r"Signature (24,2): $t_{thermal} \oplus t_{orthogonal}$",
            fontsize=11, ha='center', color=PM_COLORS["text"])
    ax.text(0.50, 0.82, "Sp(2,R) gauge symmetry relates both time dimensions",
            fontsize=10, ha='center', color=PM_COLORS["gray"], style='italic')

    # Draw two time axis arrows inside box
    # t_thermal arrow
    ax.annotate("", xy=(0.40, 0.80), xytext=(0.22, 0.80),
                arrowprops=dict(arrowstyle="->", color=PM_COLORS["green"], lw=2))
    ax.text(0.31, 0.785, r"$t_{th}$", fontsize=10, ha='center', va='top',
            color=PM_COLORS["dark_green"])

    # t_ortho arrow (perpendicular)
    ax.annotate("", xy=(0.78, 0.80), xytext=(0.60, 0.80),
                arrowprops=dict(arrowstyle="->", color=PM_COLORS["blue"], lw=2))
    ax.text(0.69, 0.785, r"$t_{ort}$", fontsize=10, ha='center', va='top',
            color=PM_COLORS["dark_blue"])

    # === CENTRAL: OBSERVER (Decoherence mechanism) ===
    # Observer circle
    observer_circle = Circle((0.50, 0.52), 0.12,
                             facecolor="#fef3c7",  # Light gold
                             edgecolor=PM_COLORS["gold"],
                             linewidth=2.5)
    ax.add_patch(observer_circle)

    # Draw eye icon inside
    draw_eye_icon(ax, (0.50, 0.54), 0.18, PM_COLORS["blue"])

    ax.text(0.50, 0.44, "OBSERVER", fontsize=11, fontweight='bold',
            ha='center', color=PM_COLORS["text"])

    # Arrow from two-time to observer
    ax.annotate("", xy=(0.50, 0.64), xytext=(0.50, 0.77),
                arrowprops=dict(arrowstyle="-|>", color=PM_COLORS["purple"],
                               lw=2, mutation_scale=15))

    # === LEFT: Decoherence Process ===
    decoher_box = FancyBboxPatch(
        (0.02, 0.42), 0.25, 0.20,
        boxstyle="round,pad=0.01,rounding_size=0.02",
        facecolor="#dbeafe",
        edgecolor=PM_COLORS["blue"],
        linewidth=1.5
    )
    ax.add_patch(decoher_box)

    ax.text(0.145, 0.595, "DECOHERENCE", fontsize=10, fontweight='bold',
            ha='center', color=PM_COLORS["dark_blue"])
    ax.text(0.145, 0.555, "Environment selects", fontsize=9, ha='center',
            color=PM_COLORS["text"])
    ax.text(0.145, 0.515, "preferred time basis", fontsize=9, ha='center',
            color=PM_COLORS["text"])
    ax.text(0.145, 0.46, r"$|\psi\rangle \rightarrow \rho_{mixed}$", fontsize=10,
            ha='center', color=PM_COLORS["dark_blue"])

    # Arrow from decoherence to observer
    ax.annotate("", xy=(0.38, 0.52), xytext=(0.28, 0.52),
                arrowprops=dict(arrowstyle="->", color=PM_COLORS["blue"],
                               lw=1.5, connectionstyle="arc3,rad=0"))

    # === RIGHT: Entropy Gradient Guide ===
    entropy_box = FancyBboxPatch(
        (0.73, 0.42), 0.25, 0.20,
        boxstyle="round,pad=0.01,rounding_size=0.02",
        facecolor="#dcfce7",
        edgecolor=PM_COLORS["green"],
        linewidth=1.5
    )
    ax.add_patch(entropy_box)

    ax.text(0.855, 0.595, "ENTROPY", fontsize=10, fontweight='bold',
            ha='center', color=PM_COLORS["dark_green"])
    ax.text(0.855, 0.555, "GRADIENT", fontsize=10, fontweight='bold',
            ha='center', color=PM_COLORS["dark_green"])
    ax.text(0.855, 0.505, r"$\nabla S_{Pneuma}$", fontsize=10, ha='center',
            color=PM_COLORS["dark_green"])
    ax.text(0.855, 0.455, "guides direction", fontsize=9, ha='center',
            color=PM_COLORS["text"], style='italic')

    # Arrow from entropy to observer
    ax.annotate("", xy=(0.62, 0.52), xytext=(0.72, 0.52),
                arrowprops=dict(arrowstyle="->", color=PM_COLORS["green"],
                               lw=1.5, connectionstyle="arc3,rad=0"))

    # === SELECTED TIME (Bottom) ===
    # Single selected time arrow
    selected_box = FancyBboxPatch(
        (0.25, 0.18), 0.50, 0.15,
        boxstyle="round,pad=0.01,rounding_size=0.02",
        facecolor=PM_COLORS["light_purple"],
        edgecolor=PM_COLORS["purple"],
        linewidth=2
    )
    ax.add_patch(selected_box)

    ax.text(0.50, 0.305, "SELECTED OBSERVER TIME", fontsize=11, fontweight='bold',
            ha='center', color=PM_COLORS["dark_purple"])

    # Time arrow
    ax.annotate("", xy=(0.68, 0.235), xytext=(0.32, 0.235),
                arrowprops=dict(arrowstyle="->,head_width=0.3,head_length=0.2",
                               color=PM_COLORS["purple"], lw=3))
    ax.text(0.50, 0.22, r"$t_{observer}$", fontsize=11, ha='center', va='top',
            color=PM_COLORS["dark_purple"])

    # Arrow from observer to selected time
    ax.annotate("", xy=(0.50, 0.34), xytext=(0.50, 0.40),
                arrowprops=dict(arrowstyle="-|>", color=PM_COLORS["text"],
                               lw=2, mutation_scale=15))
    ax.text(0.52, 0.37, "selects", fontsize=9, ha='left',
            color=PM_COLORS["gray"], style='italic')

    # === INFORMATION FLOW INDICATORS ===
    # Past information (left)
    ax.text(0.08, 0.32, "PAST", fontsize=9, fontweight='bold', ha='center',
            color=PM_COLORS["gray"])
    ax.text(0.08, 0.29, "memories", fontsize=8, ha='center',
            color=PM_COLORS["gray"], style='italic')
    ax.annotate("", xy=(0.25, 0.28), xytext=(0.12, 0.28),
                arrowprops=dict(arrowstyle="->", color=PM_COLORS["gray"],
                               lw=1.5, alpha=0.7))

    # Future information (right)
    ax.text(0.92, 0.32, "FUTURE", fontsize=9, fontweight='bold', ha='center',
            color=PM_COLORS["gray"])
    ax.text(0.92, 0.29, "anticipation", fontsize=8, ha='center',
            color=PM_COLORS["gray"], style='italic')
    ax.annotate("", xy=(0.88, 0.28), xytext=(0.75, 0.28),
                arrowprops=dict(arrowstyle="->", color=PM_COLORS["gray"],
                               lw=1.5, alpha=0.7))

    # === KEY EQUATION BOX ===
    eq_box = FancyBboxPatch(
        (0.15, 0.02), 0.70, 0.10,
        boxstyle="round,pad=0.01,rounding_size=0.02",
        facecolor=PM_COLORS["white"],
        edgecolor=PM_COLORS["text"],
        linewidth=1
    )
    ax.add_patch(eq_box)

    ax.text(0.50, 0.085, "Selection Principle", fontsize=10, fontweight='bold',
            ha='center', color=PM_COLORS["text"])
    ax.text(0.50, 0.045, r"Observer aligns with $\nabla S$: $t_{obs} \parallel$ entropy increase direction",
            fontsize=10, ha='center', color=PM_COLORS["gray"])

    # Save figure
    script_dir = Path(__file__).parent
    output_file = script_dir / output_path
    output_file.parent.mkdir(parents=True, exist_ok=True)

    plt.tight_layout()
    plt.savefig(output_file, dpi=300, facecolor='white', edgecolor='none')
    plt.close()

    print(f"Generated: {output_file.resolve()}")
    return str(output_file.resolve())


def generate_subjective_time_diagram(output_path: str = "../../images/subjective-time.png"):
    """
    Generate the Subjective Time diagram.

    Visualizes:
    - Connection between physical thermal time and subjective experience
    - Pneuma field interface between physics and consciousness
    - Information processing rate determining time perception
    - Cause-effect in conscious experience
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
    ax.text(0.5, 1.02, "Subjective Time Experience",
            fontsize=16, fontweight='bold', ha='center', va='bottom',
            color=PM_COLORS["text"])
    ax.text(0.5, 0.97, "Physical Time to Conscious Time via Pneuma Interface",
            fontsize=12, ha='center', va='bottom', style='italic',
            color=PM_COLORS["gray"])

    # === TOP LEFT: Physical Time ===
    phys_box = FancyBboxPatch(
        (0.02, 0.72), 0.30, 0.20,
        boxstyle="round,pad=0.01,rounding_size=0.02",
        facecolor="#dcfce7",
        edgecolor=PM_COLORS["green"],
        linewidth=2
    )
    ax.add_patch(phys_box)

    ax.text(0.17, 0.895, "PHYSICAL TIME", fontsize=11, fontweight='bold',
            ha='center', color=PM_COLORS["dark_green"])
    ax.text(0.17, 0.855, r"$t_{thermal}$", fontsize=12, ha='center',
            color=PM_COLORS["dark_green"])
    ax.text(0.17, 0.80, "Modular flow from", fontsize=9, ha='center',
            color=PM_COLORS["text"])
    ax.text(0.17, 0.76, "thermal state", fontsize=9, ha='center',
            color=PM_COLORS["text"])

    # Physical time arrow
    ax.annotate("", xy=(0.30, 0.74), xytext=(0.06, 0.74),
                arrowprops=dict(arrowstyle="->", color=PM_COLORS["green"], lw=2))

    # === TOP RIGHT: Subjective Time ===
    subj_box = FancyBboxPatch(
        (0.68, 0.72), 0.30, 0.20,
        boxstyle="round,pad=0.01,rounding_size=0.02",
        facecolor=PM_COLORS["light_purple"],
        edgecolor=PM_COLORS["purple"],
        linewidth=2
    )
    ax.add_patch(subj_box)

    ax.text(0.83, 0.895, "SUBJECTIVE TIME", fontsize=11, fontweight='bold',
            ha='center', color=PM_COLORS["dark_purple"])
    ax.text(0.83, 0.855, r"$t_{conscious}$", fontsize=12, ha='center',
            color=PM_COLORS["dark_purple"])
    ax.text(0.83, 0.80, "Experienced flow of", fontsize=9, ha='center',
            color=PM_COLORS["text"])
    ax.text(0.83, 0.76, "consciousness", fontsize=9, ha='center',
            color=PM_COLORS["text"])

    # Subjective time arrow (wavy to suggest perception)
    ax.annotate("", xy=(0.96, 0.74), xytext=(0.72, 0.74),
                arrowprops=dict(arrowstyle="->", color=PM_COLORS["purple"], lw=2))

    # === CENTRAL: PNEUMA INTERFACE ===
    # Large central ellipse for Pneuma
    pneuma_ellipse = Ellipse((0.50, 0.55), 0.40, 0.30,
                             facecolor="#dbeafe",
                             edgecolor=PM_COLORS["blue"],
                             linewidth=2.5)
    ax.add_patch(pneuma_ellipse)

    ax.text(0.50, 0.62, "PNEUMA", fontsize=14, fontweight='bold',
            ha='center', color=PM_COLORS["dark_blue"])
    ax.text(0.50, 0.57, "INTERFACE", fontsize=12, fontweight='bold',
            ha='center', color=PM_COLORS["dark_blue"])
    ax.text(0.50, 0.50, r"$\Psi_P$ field mediates", fontsize=10, ha='center',
            color=PM_COLORS["text"])
    ax.text(0.50, 0.46, "physics-consciousness", fontsize=10, ha='center',
            color=PM_COLORS["text"])

    # Draw brain icon inside Pneuma
    draw_brain_icon(ax, (0.50, 0.54), 0.06, PM_COLORS["light_purple"])

    # Arrows from physical to Pneuma
    ax.annotate("", xy=(0.32, 0.60), xytext=(0.28, 0.72),
                arrowprops=dict(arrowstyle="-|>", color=PM_COLORS["green"],
                               lw=2, connectionstyle="arc3,rad=0.2"))

    # Arrows from Pneuma to subjective
    ax.annotate("", xy=(0.72, 0.72), xytext=(0.68, 0.60),
                arrowprops=dict(arrowstyle="-|>", color=PM_COLORS["purple"],
                               lw=2, connectionstyle="arc3,rad=0.2"))

    # === BOTTOM: Information Processing ===
    # Information flow visualization
    info_y = 0.28

    # Input information (left)
    info_in_box = FancyBboxPatch(
        (0.05, info_y - 0.06), 0.22, 0.12,
        boxstyle="round,pad=0.01,rounding_size=0.02",
        facecolor="#dcfce7",
        edgecolor=PM_COLORS["green"],
        linewidth=1.5
    )
    ax.add_patch(info_in_box)

    ax.text(0.16, info_y + 0.035, "Sensory Input", fontsize=10, fontweight='bold',
            ha='center', color=PM_COLORS["dark_green"])
    ax.text(0.16, info_y - 0.02, "Information rate", fontsize=9, ha='center',
            color=PM_COLORS["text"])

    # Processing (center)
    proc_box = FancyBboxPatch(
        (0.35, info_y - 0.08), 0.30, 0.16,
        boxstyle="round,pad=0.01,rounding_size=0.02",
        facecolor="#dbeafe",
        edgecolor=PM_COLORS["blue"],
        linewidth=1.5
    )
    ax.add_patch(proc_box)

    ax.text(0.50, info_y + 0.05, "NEURAL", fontsize=10, fontweight='bold',
            ha='center', color=PM_COLORS["dark_blue"])
    ax.text(0.50, info_y + 0.01, "PROCESSING", fontsize=10, fontweight='bold',
            ha='center', color=PM_COLORS["dark_blue"])
    ax.text(0.50, info_y - 0.04, r"Rate $\propto$ time perception", fontsize=9, ha='center',
            color=PM_COLORS["text"])

    # Output (right)
    info_out_box = FancyBboxPatch(
        (0.73, info_y - 0.06), 0.22, 0.12,
        boxstyle="round,pad=0.01,rounding_size=0.02",
        facecolor=PM_COLORS["light_purple"],
        edgecolor=PM_COLORS["purple"],
        linewidth=1.5
    )
    ax.add_patch(info_out_box)

    ax.text(0.84, info_y + 0.035, "Time Experience", fontsize=10, fontweight='bold',
            ha='center', color=PM_COLORS["dark_purple"])
    ax.text(0.84, info_y - 0.02, "Subjective duration", fontsize=9, ha='center',
            color=PM_COLORS["text"])

    # Flow arrows
    ax.annotate("", xy=(0.34, info_y), xytext=(0.28, info_y),
                arrowprops=dict(arrowstyle="->", color=PM_COLORS["gray"], lw=2))
    ax.annotate("", xy=(0.72, info_y), xytext=(0.66, info_y),
                arrowprops=dict(arrowstyle="->", color=PM_COLORS["gray"], lw=2))

    # Arrow from Pneuma to processing
    ax.annotate("", xy=(0.50, info_y + 0.10), xytext=(0.50, 0.40),
                arrowprops=dict(arrowstyle="-|>", color=PM_COLORS["blue"],
                               lw=2, mutation_scale=12))

    # === CAUSE-EFFECT CHAIN (Bottom) ===
    cause_y = 0.08

    # Cause
    ax.add_patch(FancyBboxPatch(
        (0.02, cause_y - 0.04), 0.18, 0.08,
        boxstyle="round,pad=0.005,rounding_size=0.01",
        facecolor=PM_COLORS["light_gray"],
        edgecolor=PM_COLORS["gray"],
        linewidth=1
    ))
    ax.text(0.11, cause_y, "Physical\nEvent", fontsize=8, ha='center', va='center',
            color=PM_COLORS["text"])

    ax.annotate("", xy=(0.22, cause_y), xytext=(0.20, cause_y),
                arrowprops=dict(arrowstyle="->", color=PM_COLORS["gray"], lw=1.5))

    # Perception
    ax.add_patch(FancyBboxPatch(
        (0.23, cause_y - 0.04), 0.18, 0.08,
        boxstyle="round,pad=0.005,rounding_size=0.01",
        facecolor="#dcfce7",
        edgecolor=PM_COLORS["green"],
        linewidth=1
    ))
    ax.text(0.32, cause_y, "Sensory\nPerception", fontsize=8, ha='center', va='center',
            color=PM_COLORS["dark_green"])

    ax.annotate("", xy=(0.43, cause_y), xytext=(0.41, cause_y),
                arrowprops=dict(arrowstyle="->", color=PM_COLORS["gray"], lw=1.5))

    # Pneuma interaction
    ax.add_patch(FancyBboxPatch(
        (0.44, cause_y - 0.04), 0.18, 0.08,
        boxstyle="round,pad=0.005,rounding_size=0.01",
        facecolor="#dbeafe",
        edgecolor=PM_COLORS["blue"],
        linewidth=1
    ))
    ax.text(0.53, cause_y, "Pneuma\nInteraction", fontsize=8, ha='center', va='center',
            color=PM_COLORS["dark_blue"])

    ax.annotate("", xy=(0.64, cause_y), xytext=(0.62, cause_y),
                arrowprops=dict(arrowstyle="->", color=PM_COLORS["gray"], lw=1.5))

    # Conscious experience
    ax.add_patch(FancyBboxPatch(
        (0.65, cause_y - 0.04), 0.18, 0.08,
        boxstyle="round,pad=0.005,rounding_size=0.01",
        facecolor=PM_COLORS["light_purple"],
        edgecolor=PM_COLORS["purple"],
        linewidth=1
    ))
    ax.text(0.74, cause_y, "Conscious\nExperience", fontsize=8, ha='center', va='center',
            color=PM_COLORS["dark_purple"])

    ax.annotate("", xy=(0.85, cause_y), xytext=(0.83, cause_y),
                arrowprops=dict(arrowstyle="->", color=PM_COLORS["gray"], lw=1.5))

    # Response
    ax.add_patch(FancyBboxPatch(
        (0.86, cause_y - 0.04), 0.12, 0.08,
        boxstyle="round,pad=0.005,rounding_size=0.01",
        facecolor=PM_COLORS["light_gray"],
        edgecolor=PM_COLORS["gray"],
        linewidth=1
    ))
    ax.text(0.92, cause_y, "Action", fontsize=8, ha='center', va='center',
            color=PM_COLORS["text"])

    ax.text(0.50, cause_y - 0.06, "Cause-Effect Chain in Conscious Experience",
            fontsize=9, ha='center', color=PM_COLORS["gray"], style='italic')

    # === KEY RELATIONSHIP ===
    rel_box = FancyBboxPatch(
        (0.20, 0.36), 0.60, 0.07,
        boxstyle="round,pad=0.005,rounding_size=0.01",
        facecolor=PM_COLORS["white"],
        edgecolor=PM_COLORS["text"],
        linewidth=1
    )
    ax.add_patch(rel_box)

    ax.text(0.50, 0.395, r"$\frac{dt_{conscious}}{dt_{thermal}} = f(\text{information processing rate})$",
            fontsize=11, ha='center', color=PM_COLORS["text"])

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
    """Generate all observer and consciousness time diagrams."""
    print("=" * 60)
    print("PRINCIPIA METAPHYSICA - Observer Time Visualization Diagrams")
    print("=" * 60)

    if not HAS_MATPLOTLIB:
        print("\nERROR: matplotlib is required for visualization generation.")
        print("Install with: pip install matplotlib")
        sys.exit(1)

    print("\n1. Generating Observer Time Selection diagram...")
    observer_path = generate_observer_time_selection_diagram()

    print("\n2. Generating Subjective Time diagram...")
    subjective_path = generate_subjective_time_diagram()

    print("\n" + "=" * 60)
    print("All diagrams generated successfully!")
    print("=" * 60)

    if observer_path:
        print(f"\n  - {observer_path}")
    if subjective_path:
        print(f"  - {subjective_path}")


if __name__ == "__main__":
    main()
