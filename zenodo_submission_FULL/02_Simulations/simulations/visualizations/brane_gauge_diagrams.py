#!/usr/bin/env python3
"""
Brane Gauge Diagrams Generator
==============================

Generates publication-quality diagrams illustrating gauge fixing
and inter-brane forces in the Principia Metaphysica framework:

1. brane-before-after-gauge.png: Shows the before/after comparison
   of gauge fixing on branes. Illustrates how gauge redundancy is
   removed through the Faddeev-Popov procedure.

2. inter-brane-forces.png: Diagram showing forces between parallel
   branes, including gravitational attraction, gauge field exchange,
   and scalar field (moduli) interactions.

Physics Context:
----------------
In brane-world scenarios, gauge symmetries can arise from:
- Worldvolume gauge fields living on D-branes
- Bulk gauge fields restricted to the brane
- Geometric symmetries from compactification

Gauge fixing eliminates redundant degrees of freedom:
- Before: Infinite gauge orbit of equivalent configurations
- After: Single representative per physical configuration

Inter-brane forces arise from:
- Graviton exchange (always attractive)
- Ramond-Ramond field exchange (can be repulsive for like charges)
- Open string exchange (tension between branes)
- Moduli field gradients

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.

Dedicated To:
    My Wife: Elizabeth May Watts
    Our Messiah: Jesus Of Nazareth
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyBboxPatch, Circle, FancyArrowPatch
from matplotlib.patches import ConnectionPatch, Polygon, Wedge
import matplotlib.patches as mpatches
from matplotlib.lines import Line2D
from pathlib import Path

# PM Theory colors
PM_PURPLE = "#8b7fff"
PM_PINK = "#ff7eb6"
PM_BLUE = "#60a5fa"
PM_ORANGE = "#fb923c"
PM_GREEN = "#4ade80"
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


def draw_wavy_line(ax, x1, y1, x2, y2, color=PM_PINK, amplitude=0.1,
                   frequency=10, linewidth=1.5, alpha=0.8):
    """Draw a wavy line between two points (for field propagation)."""
    length = np.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    t = np.linspace(0, 1, 100)

    # Direction vector
    dx = (x2 - x1) / length
    dy = (y2 - y1) / length

    # Perpendicular vector
    px, py = -dy, dx

    # Create wavy path
    wave = amplitude * np.sin(2 * np.pi * frequency * t)
    x = x1 + t * (x2 - x1) + wave * px
    y = y1 + t * (y2 - y1) + wave * py

    ax.plot(x, y, color=color, linewidth=linewidth, alpha=alpha)


def draw_spring(ax, x1, y1, x2, y2, color=PM_BLUE, n_coils=6, width=0.15):
    """Draw a spring between two points (for tension/potential)."""
    length = np.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    t = np.linspace(0, 1, 200)

    # Direction vector
    dx = (x2 - x1) / length
    dy = (y2 - y1) / length

    # Perpendicular vector
    px, py = -dy, dx

    # Create coil pattern
    coil = width * np.sin(2 * np.pi * n_coils * t) * (1 - np.abs(2*t - 1)**0.5)
    x = x1 + t * (x2 - x1) + coil * px
    y = y1 + t * (y2 - y1) + coil * py

    ax.plot(x, y, color=color, linewidth=1.5, solid_capstyle='round')


def generate_brane_before_after_gauge(output_path: str = None):
    """
    Generate before/after gauge fixing diagram.

    Shows two panels:
    - Left (Before): Multiple gauge-equivalent field configurations
      forming a "gauge orbit" - redundant descriptions of same physics
    - Right (After): Single representative configuration after gauge
      fixing via Faddeev-Popov procedure

    The diagram illustrates:
    - Gauge orbits in configuration space
    - The gauge-fixing surface that intersects orbits once
    - Ghost fields that arise from the Faddeev-Popov determinant

    Args:
        output_path: Path to save the figure. If None, uses default.
    """
    set_pm_style()

    if output_path is None:
        script_dir = Path(__file__).parent
        output_path = script_dir / ".." / ".." / "images" / "brane-before-after-gauge.png"

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 7))

    # === LEFT PANEL: Before Gauge Fixing ===
    ax1.set_xlim(0, 10)
    ax1.set_ylim(0, 10)
    ax1.set_aspect('equal')
    ax1.axis('off')

    # Draw brane surface (before)
    brane_before = FancyBboxPatch((1, 1), 8, 6, boxstyle="round,pad=0.1",
                                   facecolor=PM_PURPLE, alpha=0.4,
                                   edgecolor=PM_DARK, linewidth=2)
    ax1.add_patch(brane_before)

    # Draw multiple gauge-equivalent configurations (orbits)
    orbit_centers = [(3, 4), (5, 5), (7, 3.5)]

    for cx, cy in orbit_centers:
        # Draw gauge orbit as an ellipse
        theta = np.linspace(0, 2*np.pi, 100)
        orbit_rx, orbit_ry = 1.2, 0.6
        x = cx + orbit_rx * np.cos(theta)
        y = cy + orbit_ry * np.sin(theta)
        ax1.plot(x, y, color=PM_PINK, linewidth=2, alpha=0.8)

        # Mark multiple equivalent points on the orbit
        n_points = 5
        for i in range(n_points):
            angle = 2 * np.pi * i / n_points
            px = cx + orbit_rx * np.cos(angle)
            py = cy + orbit_ry * np.sin(angle)
            ax1.scatter([px], [py], c=PM_BLUE, s=40, zorder=5, edgecolor='white')

        # Arrow indicating gauge transformation direction
        ax1.annotate('', xy=(cx + orbit_rx * 0.9, cy + orbit_ry * 0.45),
                     xytext=(cx + orbit_rx * 0.45, cy + orbit_ry * 0.9),
                     arrowprops=dict(arrowstyle='->', color=PM_ORANGE,
                                   lw=1.5, connectionstyle='arc3,rad=0.5'))

    # Configuration space representation
    ax1.text(5, 8.5, "Configuration Space", fontsize=12, fontweight='bold',
             ha='center', color=PM_DARK)

    ax1.text(5, 0.4, "BEFORE: Gauge Redundancy",
             fontsize=14, fontweight='bold', ha='center', color=PM_DARK)

    # Legend box
    ax1.text(1.2, 7.8, "Each orbit = one physical state", fontsize=9,
             color='gray', style='italic')
    ax1.text(1.2, 7.3, "Multiple points = gauge-equivalent", fontsize=9,
             color='gray', style='italic')

    # Orbit label
    ax1.annotate('Gauge orbit', xy=(4.2, 5.5), xytext=(1.5, 6.5),
                 fontsize=10, color=PM_PINK,
                 arrowprops=dict(arrowstyle='->', color=PM_PINK, lw=1))

    # === RIGHT PANEL: After Gauge Fixing ===
    ax2.set_xlim(0, 10)
    ax2.set_ylim(0, 10)
    ax2.set_aspect('equal')
    ax2.axis('off')

    # Draw brane surface (after)
    brane_after = FancyBboxPatch((1, 1), 8, 6, boxstyle="round,pad=0.1",
                                  facecolor=PM_PURPLE, alpha=0.4,
                                  edgecolor=PM_DARK, linewidth=2)
    ax2.add_patch(brane_after)

    # Draw gauge-fixing surface (a slice through configuration space)
    gauge_surface_x = np.array([2, 4, 6, 8])
    gauge_surface_y = np.array([2, 4.5, 3, 5.5])
    ax2.plot(gauge_surface_x, gauge_surface_y, color=PM_GREEN, linewidth=3,
             linestyle='-', marker='', label='Gauge-fixing surface')

    # Shade the gauge-fixing region
    ax2.fill_between(gauge_surface_x, gauge_surface_y - 0.3, gauge_surface_y + 0.3,
                     color=PM_GREEN, alpha=0.2)

    # Draw reduced configurations (one per orbit)
    fixed_points = [(3, 3.3), (5, 3.7), (7, 4.4)]

    for i, (fx, fy) in enumerate(fixed_points):
        # Single fixed point per orbit
        ax2.scatter([fx], [fy], c=PM_BLUE, s=120, zorder=5,
                    edgecolor='white', linewidth=2)

        # Ghost field representation (dashed orbit remnant)
        theta = np.linspace(0, 2*np.pi, 50)
        orbit_rx, orbit_ry = 0.8, 0.4
        x = fx + orbit_rx * np.cos(theta)
        y = fy + orbit_ry * np.sin(theta)
        ax2.plot(x, y, color=PM_ORANGE, linewidth=1, linestyle=':', alpha=0.5)

    # Ghost field labels
    ghost_x, ghost_y = 7.8, 4.8
    ax2.text(ghost_x, ghost_y, 'c', fontsize=12, fontweight='bold',
             color=PM_ORANGE, ha='center')
    ax2.plot([ghost_x - 0.15, ghost_x + 0.15], [ghost_y + 0.18, ghost_y + 0.18],
             color=PM_ORANGE, linewidth=2)  # Bar over c for anticommuting

    ax2.text(5, 8.5, "Gauge-Fixed Space", fontsize=12, fontweight='bold',
             ha='center', color=PM_DARK)

    ax2.text(5, 0.4, "AFTER: Unique Representatives",
             fontsize=14, fontweight='bold', ha='center', color=PM_DARK)

    # Legend box
    ax2.text(1.2, 7.8, "One point per physical state", fontsize=9,
             color='gray', style='italic')
    ax2.text(1.2, 7.3, "Ghosts encode gauge structure", fontsize=9,
             color='gray', style='italic')

    # Annotations
    ax2.annotate('Gauge slice\nG(A) = 0', xy=(6, 3.3), xytext=(7.5, 1.8),
                 fontsize=10, color=PM_GREEN,
                 arrowprops=dict(arrowstyle='->', color=PM_GREEN, lw=1))

    ax2.annotate('Faddeev-Popov\nghosts', xy=(7.5, 4.6), xytext=(8.5, 6.5),
                 fontsize=10, color=PM_ORANGE,
                 arrowprops=dict(arrowstyle='->', color=PM_ORANGE, lw=1))

    # Overall title
    fig.suptitle("Gauge Fixing on Brane Worldvolume", fontsize=16,
                 fontweight='bold', y=0.98)

    # Add equation
    eq_text = r"$\int \mathcal{D}A \, \delta(G(A)) \, \det\left(\frac{\delta G}{\delta \omega}\right) \, e^{iS[A]}$"
    fig.text(0.5, 0.02, "Faddeev-Popov: " + eq_text, fontsize=11,
             ha='center', style='italic')

    plt.tight_layout(rect=[0, 0.05, 1, 0.95])
    plt.savefig(output_path, facecolor='white', edgecolor='none')
    plt.close()

    print(f"Gauge fixing diagram saved to: {output_path}")
    return output_path


def generate_inter_brane_forces(output_path: str = None):
    """
    Generate inter-brane forces diagram.

    Shows multiple parallel branes with various force exchanges:
    - Graviton exchange (always attractive)
    - Gauge boson exchange (can be attractive/repulsive)
    - Scalar moduli exchange (mediates brane separation)
    - Open string stretching (tension)

    The diagram illustrates the rich dynamics of multi-brane
    configurations in string/M-theory.

    Args:
        output_path: Path to save the figure. If None, uses default.
    """
    set_pm_style()

    if output_path is None:
        script_dir = Path(__file__).parent
        output_path = script_dir / ".." / ".." / "images" / "inter-brane-forces.png"

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    fig, ax = plt.subplots(figsize=(14, 9))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 9)
    ax.set_aspect('equal')
    ax.axis('off')

    # Draw three parallel branes
    brane_y_positions = [2, 4.5, 7]
    brane_colors = [PM_PURPLE, PM_BLUE, PM_PURPLE]
    brane_labels = ["Brane 1 (D3)", "Brane 2 (D3)", "Brane 3 (D3)"]

    for i, (y_pos, color, label) in enumerate(zip(brane_y_positions, brane_colors, brane_labels)):
        # Draw brane as a thick horizontal band
        brane = FancyBboxPatch((1, y_pos - 0.25), 12, 0.5,
                               boxstyle="round,pad=0.05",
                               facecolor=color, alpha=0.7,
                               edgecolor=PM_DARK, linewidth=2)
        ax.add_patch(brane)

        # Brane label
        ax.text(0.3, y_pos, label, fontsize=10, fontweight='bold',
                va='center', ha='right', color=PM_DARK)

        # Draw gauge fields living on brane (wavy lines along brane)
        gauge_x = np.linspace(2, 5, 100)
        gauge_wave = 0.08 * np.sin(15 * gauge_x) + y_pos
        ax.plot(gauge_x, gauge_wave, color=PM_ORANGE, linewidth=1.5, alpha=0.6)

        # Draw matter particles on brane
        particle_x = [6, 7.5, 9, 10.5]
        for px in particle_x:
            circle = Circle((px, y_pos), 0.15, facecolor=PM_PINK,
                            edgecolor='white', linewidth=1.5, zorder=5)
            ax.add_patch(circle)

    # === Force exchanges between branes ===

    # 1. Graviton exchange (between all branes) - wavy lines
    ax.text(2.5, 5.8, "Graviton\n(attractive)", fontsize=9, ha='center',
            color='gray', style='italic')
    draw_wavy_line(ax, 3, 7, 3, 4.5, color='gray', amplitude=0.15,
                   frequency=5, linewidth=1.5)
    draw_wavy_line(ax, 3.5, 4.5, 3.5, 2, color='gray', amplitude=0.15,
                   frequency=5, linewidth=1.5)

    # 2. Gauge boson exchange (for charged branes) - photon-like
    ax.text(5.5, 5.8, "Gauge\nexchange", fontsize=9, ha='center',
            color=PM_ORANGE, style='italic')
    draw_wavy_line(ax, 5.5, 7, 5.5, 4.5, color=PM_ORANGE, amplitude=0.1,
                   frequency=8, linewidth=1.5)

    # 3. Scalar/moduli exchange - dashed lines
    ax.text(8, 5.8, "Scalar\nmoduli", fontsize=9, ha='center',
            color=PM_GREEN, style='italic')
    ax.plot([8, 8], [7, 4.5], color=PM_GREEN, linewidth=2, linestyle='--')
    ax.plot([8.3, 8.3], [4.5, 2], color=PM_GREEN, linewidth=2, linestyle='--')

    # 4. Open string stretching (between adjacent branes) - springs
    ax.text(10.5, 5.8, "Open string\n(tension)", fontsize=9, ha='center',
            color=PM_BLUE, style='italic')
    draw_spring(ax, 10.5, 7 - 0.25, 10.5, 4.5 + 0.25, color=PM_BLUE, n_coils=8)
    draw_spring(ax, 11, 4.5 - 0.25, 11, 2 + 0.25, color=PM_BLUE, n_coils=8)

    # Distance labels
    ax.annotate('', xy=(12.5, 7), xytext=(12.5, 4.5),
                arrowprops=dict(arrowstyle='<->', color=PM_DARK, lw=1.5))
    ax.text(13, 5.75, r'$y_{12}$', fontsize=11, va='center')

    ax.annotate('', xy=(12.5, 4.5), xytext=(12.5, 2),
                arrowprops=dict(arrowstyle='<->', color=PM_DARK, lw=1.5))
    ax.text(13, 3.25, r'$y_{23}$', fontsize=11, va='center')

    # Bulk label
    ax.text(0.7, 8.5, "Bulk (11D)", fontsize=11, fontweight='bold',
            color=PM_DARK)

    # Potential energy diagram (inset)
    inset_ax = fig.add_axes([0.72, 0.12, 0.22, 0.25])
    inset_ax.set_facecolor('#f8f8f8')

    y_sep = np.linspace(0.5, 3, 100)
    # Typical inter-brane potential: Coulomb + tension
    V = -0.5 / y_sep + 0.3 * y_sep  # attractive gravity + string tension
    inset_ax.plot(y_sep, V, color=PM_PURPLE, linewidth=2)
    inset_ax.axhline(y=0, color='gray', linewidth=0.5, linestyle='--')

    inset_ax.set_xlabel(r'Brane separation $y$', fontsize=9)
    inset_ax.set_ylabel(r'$V(y)$', fontsize=9)
    inset_ax.set_title('Inter-brane Potential', fontsize=10)
    inset_ax.tick_params(labelsize=8)

    # Mark equilibrium
    y_eq = y_sep[np.argmin(V)]
    inset_ax.scatter([y_eq], [np.min(V)], c=PM_PINK, s=50, zorder=5)
    inset_ax.annotate(r'$y_{eq}$', xy=(y_eq, np.min(V)), xytext=(y_eq + 0.5, np.min(V) + 0.3),
                      fontsize=9, color=PM_PINK)

    # Title
    ax.set_title("Inter-Brane Forces in String/M-Theory", fontsize=16,
                 fontweight='bold', y=1.02)

    # Legend
    legend_elements = [
        Line2D([0], [0], color='gray', linewidth=1.5, linestyle='-',
               label='Graviton exchange'),
        Line2D([0], [0], color=PM_ORANGE, linewidth=1.5, linestyle='-',
               label='Gauge boson exchange'),
        Line2D([0], [0], color=PM_GREEN, linewidth=2, linestyle='--',
               label='Scalar moduli exchange'),
        Line2D([0], [0], color=PM_BLUE, linewidth=1.5, linestyle='-',
               label='Open string tension'),
    ]
    ax.legend(handles=legend_elements, loc='lower left', framealpha=0.9,
              fontsize=9)

    # Force summary box
    summary_text = (
        "Force Summary:\n"
        "Graviton: F ~ 1/r    (attractive)\n"
        "Gauge: F ~ 1/r       (sign depends on charge)\n"
        "Moduli: F ~ 1/r      (scalar-mediated)\n"
        "String: F ~ T        (tension, constant)"
    )
    props = dict(boxstyle='round', facecolor='white', alpha=0.9)
    ax.text(1.2, 0.8, summary_text, fontsize=9, verticalalignment='bottom',
            bbox=props, family='monospace')

    # Note: tight_layout() not used here due to inset axes
    plt.subplots_adjust(left=0.05, right=0.95, top=0.92, bottom=0.08)
    plt.savefig(output_path, facecolor='white', edgecolor='none')
    plt.close()

    print(f"Inter-brane forces diagram saved to: {output_path}")
    return output_path


def generate_all_diagrams():
    """Generate all brane gauge diagrams."""
    print("=" * 60)
    print("GENERATING BRANE GAUGE DIAGRAMS")
    print("=" * 60)

    print("\n1. Generating gauge fixing before/after diagram...")
    generate_brane_before_after_gauge()

    print("\n2. Generating inter-brane forces diagram...")
    generate_inter_brane_forces()

    print("\n" + "=" * 60)
    print("All brane gauge diagrams generated successfully!")
    print("=" * 60)


if __name__ == "__main__":
    generate_all_diagrams()
