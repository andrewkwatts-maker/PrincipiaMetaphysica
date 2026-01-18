#!/usr/bin/env python3
"""
[HISTORICAL v16] Two-Time Comparison Visualization

NOTE: This visualization was created for the v16-v20 (24,2) two-time framework.
The v21 framework uses unified time (24,1) with Euclidean bridge.
Retained for historical comparison and educational purposes.

Two-Time Comparison Visualizations
===================================

Generates diagrams comparing 1-time vs 2-time physics and
explaining Sp(2,R) gauge fixing for Principia Metaphysica.

Output files:
- 2t-vs-1t-comparison.png: Side-by-side comparison of physics frameworks
- gauge-fixing-time.png: How Sp(2,R) gauge fixing selects physical time

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
    from matplotlib.patches import FancyBboxPatch, Circle, Ellipse, Rectangle
    from matplotlib.patches import FancyArrowPatch, Polygon, Wedge
    from matplotlib.lines import Line2D
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
    "time1": "#e74c3c",      # Red for time t
    "time2": "#3498db",      # Blue for time tau
    "space": "#2ecc71",      # Green for space
    "text": "#2c3e50",
    "highlight": "#9b59b6",  # Purple highlight
    "warning": "#f39c12",    # Warning orange
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


def generate_2t_vs_1t_comparison(output_path: str = "../../images/2t-vs-1t-comparison.png"):
    """
    Generate side-by-side comparison of 1-time vs 2-time physics.

    Shows:
    - Standard Model (1 time): Linear evolution, single worldline
    - Two-Time Physics (2 times): 2D time evolution, constraint surface
    - Key differences in symmetry, dynamics, and predictions
    """
    if not HAS_MATPLOTLIB:
        print("Cannot generate plot: matplotlib not available")
        return

    set_pub_style()
    fig = plt.figure(figsize=(16, 12))

    # Create main grid
    gs = fig.add_gridspec(3, 2, height_ratios=[1.2, 1, 0.8],
                          hspace=0.3, wspace=0.3)

    # === Header ===
    ax_title = fig.add_subplot(gs[0, :])
    ax_title.set_xlim(0, 10)
    ax_title.set_ylim(0, 2)
    ax_title.axis('off')

    ax_title.text(5, 1.8, "One-Time vs Two-Time Physics: A Comparison",
                  fontsize=20, fontweight='bold', ha='center', va='center',
                  color=PM_COLORS["dark"])

    # Column headers
    header1 = FancyBboxPatch((0.3, 0.3), 4, 1.2,
                             boxstyle="round,pad=0.02,rounding_size=0.1",
                             facecolor='#fff0f0', edgecolor=PM_COLORS["time1"],
                             linewidth=3)
    ax_title.add_patch(header1)
    ax_title.text(2.3, 1.0, "Standard Physics", fontsize=14, fontweight='bold',
                  ha='center', va='center', color=PM_COLORS["time1"])
    ax_title.text(2.3, 0.55, "1 Time Dimension", fontsize=11,
                  ha='center', va='center', color=PM_COLORS["text"])

    header2 = FancyBboxPatch((5.7, 0.3), 4, 1.2,
                             boxstyle="round,pad=0.02,rounding_size=0.1",
                             facecolor='#f0f0ff', edgecolor=PM_COLORS["purple"],
                             linewidth=3)
    ax_title.add_patch(header2)
    ax_title.text(7.7, 1.0, "Two-Time Physics", fontsize=14, fontweight='bold',
                  ha='center', va='center', color=PM_COLORS["purple"])
    ax_title.text(7.7, 0.55, "2 Time Dimensions", fontsize=11,
                  ha='center', va='center', color=PM_COLORS["text"])

    # === Left Panel: One-Time Physics ===
    ax1 = fig.add_subplot(gs[1, 0])
    ax1.set_xlim(0, 10)
    ax1.set_ylim(0, 10)
    ax1.set_aspect('equal')
    ax1.axis('off')
    ax1.set_title("Worldline in Spacetime", fontsize=12, fontweight='bold',
                  color=PM_COLORS["time1"], pad=10)

    # Background spacetime grid
    for i in range(11):
        ax1.axhline(y=i, color='gray', alpha=0.2, lw=0.5)
        ax1.axvline(x=i, color='gray', alpha=0.2, lw=0.5)

    # Time axis
    ax1.annotate('', xy=(5, 9.5), xytext=(5, 0.5),
                arrowprops=dict(arrowstyle='->', color=PM_COLORS["time1"],
                               lw=2.5, mutation_scale=15))
    ax1.text(5.5, 9.3, "Time t", fontsize=11, color=PM_COLORS["time1"],
             fontweight='bold')

    # Space axis
    ax1.annotate('', xy=(9.5, 2), xytext=(0.5, 2),
                arrowprops=dict(arrowstyle='->', color=PM_COLORS["space"],
                               lw=2.5, mutation_scale=15))
    ax1.text(9.0, 1.4, "Space x", fontsize=11, color=PM_COLORS["space"],
             fontweight='bold')

    # Worldline (curved path through spacetime)
    t_vals = np.linspace(2.5, 8.5, 100)
    x_vals = 2 + 2 * np.sin(0.5 * (t_vals - 2.5)) + 0.3 * (t_vals - 2.5)
    ax1.plot(x_vals, t_vals, '-', color=PM_COLORS["purple"], lw=3)

    # Events on worldline
    for t, label in [(3, "A"), (5.5, "B"), (8, "C")]:
        x = 2 + 2 * np.sin(0.5 * (t - 2.5)) + 0.3 * (t - 2.5)
        circle = Circle((x, t), 0.25, facecolor=PM_COLORS["orange"],
                        edgecolor='white', linewidth=2)
        ax1.add_patch(circle)
        ax1.text(x + 0.4, t, label, fontsize=10, fontweight='bold',
                color=PM_COLORS["orange"])

    # Light cone at event B
    x_b = 2 + 2 * np.sin(0.5 * (5.5 - 2.5)) + 0.3 * (5.5 - 2.5)
    # Future light cone
    ax1.plot([x_b - 2, x_b], [7.5, 5.5], '--', color=PM_COLORS["warning"], lw=1.5, alpha=0.7)
    ax1.plot([x_b, x_b + 2], [5.5, 7.5], '--', color=PM_COLORS["warning"], lw=1.5, alpha=0.7)
    ax1.text(x_b + 1.5, 7.2, "Light\ncone", fontsize=8, color=PM_COLORS["warning"],
             ha='center')

    # Signature annotation
    sig_box = FancyBboxPatch((0.3, 0.3), 4.2, 1.5,
                             boxstyle="round,pad=0.02,rounding_size=0.1",
                             facecolor=PM_COLORS["light"], edgecolor=PM_COLORS["time1"],
                             linewidth=1.5)
    ax1.add_patch(sig_box)
    ax1.text(2.4, 1.4, "Signature: (3, 1)", fontsize=10, fontweight='bold',
             ha='center', color=PM_COLORS["time1"])
    ax1.text(2.4, 0.7, "3 space + 1 time", fontsize=9, ha='center',
             color=PM_COLORS["text"])

    # === Right Panel: Two-Time Physics ===
    ax2 = fig.add_subplot(gs[1, 1])
    ax2.set_xlim(0, 10)
    ax2.set_ylim(0, 10)
    ax2.set_aspect('equal')
    ax2.axis('off')
    ax2.set_title("Worldsheet in Extended Spacetime", fontsize=12, fontweight='bold',
                  color=PM_COLORS["purple"], pad=10)

    # Background spacetime grid
    for i in range(11):
        ax2.axhline(y=i, color='gray', alpha=0.2, lw=0.5)
        ax2.axvline(x=i, color='gray', alpha=0.2, lw=0.5)

    # Time t axis
    ax2.annotate('', xy=(3, 9.5), xytext=(3, 0.5),
                arrowprops=dict(arrowstyle='->', color=PM_COLORS["time1"],
                               lw=2.5, mutation_scale=15))
    ax2.text(3.5, 9.3, "Time t", fontsize=11, color=PM_COLORS["time1"],
             fontweight='bold')

    # Time tau axis
    ax2.annotate('', xy=(9.5, 3), xytext=(3.5, 3),
                arrowprops=dict(arrowstyle='->', color=PM_COLORS["time2"],
                               lw=2.5, mutation_scale=15))
    ax2.text(9.0, 2.4, r"Time $\tau$", fontsize=11, color=PM_COLORS["time2"],
             fontweight='bold')

    # 2D Time plane (constraint surface)
    from matplotlib.patches import Polygon as MplPolygon
    plane_verts = [(3.5, 3.5), (9, 3.5), (8, 8.5), (3.5, 8.5)]
    plane = MplPolygon(plane_verts, facecolor=PM_COLORS["purple"], alpha=0.15,
                       edgecolor=PM_COLORS["purple"], linewidth=2)
    ax2.add_patch(plane)

    # Constraint surface label
    ax2.text(6.5, 6.5, "Constraint\nSurface", fontsize=10, ha='center',
             color=PM_COLORS["purple"], fontweight='bold',
             bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

    # Worldsheet grid on constraint surface
    for i in range(3):
        t_start = 4 + i * 1.5
        tau_line_y = np.linspace(t_start, min(t_start + 2.5, 8), 20)
        tau_line_x = 4 + (tau_line_y - t_start) * 0.8 + i * 1.2
        ax2.plot(tau_line_x, tau_line_y, '-', color=PM_COLORS["time1"], lw=1, alpha=0.5)

    for i in range(3):
        tau_val = 4.5 + i * 1.5
        t_line_y = np.linspace(4, 8, 20)
        t_line_x = tau_val + (t_line_y - 4) * 0.3
        ax2.plot(t_line_x, t_line_y, '-', color=PM_COLORS["time2"], lw=1, alpha=0.5)

    # Event point on surface
    event = Circle((6, 6), 0.3, facecolor=PM_COLORS["orange"],
                   edgecolor='white', linewidth=2, zorder=5)
    ax2.add_patch(event)
    ax2.text(6.5, 6.3, "Event E", fontsize=10, fontweight='bold',
             color=PM_COLORS["orange"])

    # Projections to axes
    ax2.plot([6, 6], [3, 6], '--', color=PM_COLORS["time1"], lw=1.5, alpha=0.7)
    ax2.plot([3, 6], [6, 6], '--', color=PM_COLORS["time2"], lw=1.5, alpha=0.7)

    # Sp(2,R) gauge orbit (dashed ellipse)
    ellipse = Ellipse((6, 6), 2, 1.2, angle=30,
                      facecolor='none', edgecolor=PM_COLORS["pink"],
                      linewidth=2, linestyle='--')
    ax2.add_patch(ellipse)
    ax2.text(7.5, 7.2, "Sp(2,R)\norbit", fontsize=9, ha='center',
             color=PM_COLORS["pink"], fontweight='bold')

    # Signature annotation
    sig_box2 = FancyBboxPatch((0.3, 0.3), 4.2, 1.5,
                              boxstyle="round,pad=0.02,rounding_size=0.1",
                              facecolor=PM_COLORS["light"], edgecolor=PM_COLORS["purple"],
                              linewidth=1.5)
    ax2.add_patch(sig_box2)
    ax2.text(2.4, 1.4, "Signature: (24, 2)", fontsize=10, fontweight='bold',
             ha='center', color=PM_COLORS["purple"])
    ax2.text(2.4, 0.7, "24 space + 2 time", fontsize=9, ha='center',
             color=PM_COLORS["text"])

    # === Bottom Panel: Feature Comparison Table ===
    ax3 = fig.add_subplot(gs[2, :])
    ax3.set_xlim(0, 10)
    ax3.set_ylim(0, 4)
    ax3.axis('off')

    # Table structure
    table_data = [
        ("Feature", "1-Time Physics", "2-Time Physics"),
        ("Dimension", "(3,1) = 4D", "(24,2) = 26D"),
        ("Evolution", "Linear worldline", "2D constraint surface"),
        ("Symmetry", "Poincare", "Conformal + Sp(2,R)"),
        ("Gauge", "Fixed time", "Time emerges from gauge fixing"),
    ]

    row_height = 0.7
    col_widths = [2.5, 3.5, 3.5]
    col_starts = [0.3, 2.8, 6.3]

    # Header row
    for i, (col_start, col_width, text) in enumerate(zip(col_starts, col_widths, table_data[0])):
        header = FancyBboxPatch((col_start, 3.0), col_width, row_height,
                                boxstyle="square,pad=0",
                                facecolor=PM_COLORS["dark"], edgecolor='white',
                                linewidth=1)
        ax3.add_patch(header)
        ax3.text(col_start + col_width/2, 3.35, text, fontsize=10,
                fontweight='bold', ha='center', va='center', color='white')

    # Data rows
    for row_idx, row_data in enumerate(table_data[1:]):
        y_pos = 2.3 - row_idx * row_height
        colors = [PM_COLORS["light"], '#fff0f0', '#f0f0ff']

        for col_idx, (col_start, col_width, text) in enumerate(zip(col_starts, col_widths, row_data)):
            cell = FancyBboxPatch((col_start, y_pos), col_width, row_height,
                                  boxstyle="square,pad=0",
                                  facecolor=colors[col_idx], edgecolor='gray',
                                  linewidth=0.5)
            ax3.add_patch(cell)
            text_color = PM_COLORS["text"]
            if col_idx == 1:
                text_color = PM_COLORS["time1"]
            elif col_idx == 2:
                text_color = PM_COLORS["purple"]
            ax3.text(col_start + col_width/2, y_pos + row_height/2, text,
                    fontsize=9, ha='center', va='center', color=text_color)

    # Key insight box
    insight_box = FancyBboxPatch((0.3, -0.5), 9.4, 0.8,
                                 boxstyle="round,pad=0.03,rounding_size=0.1",
                                 facecolor='#fff9e6', edgecolor=PM_COLORS["warning"],
                                 linewidth=2)
    ax3.add_patch(insight_box)
    ax3.text(5, 0, "Key Insight: Two-time physics isn't \"two futures\" - it's a richer "
             "mathematical structure where physical time emerges via gauge fixing!",
             fontsize=10, ha='center', va='center', color=PM_COLORS["text"],
             fontweight='bold')

    # Save figure
    output_file = Path(__file__).parent / output_path
    output_file.parent.mkdir(exist_ok=True, parents=True)
    plt.tight_layout()
    plt.savefig(output_file, facecolor='white', edgecolor='none')
    plt.close()
    print(f"Saved: {output_file.resolve()}")


def generate_gauge_fixing_time(output_path: str = "../../images/gauge-fixing-time.png"):
    """
    Generate diagram showing how Sp(2,R) gauge fixing selects physical time.

    Shows:
    - The Sp(2,R) group action on 2D time plane
    - Three gauge constraints: X^2=0, X.P=0, P^2+M^2=0
    - How gauge fixing projects (24,2) -> (12,1)
    """
    if not HAS_MATPLOTLIB:
        print("Cannot generate plot: matplotlib not available")
        return

    set_pub_style()
    fig = plt.figure(figsize=(14, 12))

    # Create grid
    gs = fig.add_gridspec(2, 2, height_ratios=[1.2, 1],
                          hspace=0.25, wspace=0.25)

    # === Main Title ===
    fig.suptitle("Sp(2,R) Gauge Fixing: How Physical Time Emerges",
                 fontsize=18, fontweight='bold', color=PM_COLORS["dark"], y=0.97)

    # === Panel 1: 2D Time Plane with Gauge Orbits ===
    ax1 = fig.add_subplot(gs[0, 0])
    ax1.set_xlim(-5, 5)
    ax1.set_ylim(-5, 5)
    ax1.set_aspect('equal')
    ax1.set_title("Sp(2,R) Gauge Orbits in 2D Time", fontsize=13, fontweight='bold',
                  color=PM_COLORS["purple"], pad=10)

    # Grid
    ax1.axhline(y=0, color='gray', lw=0.5, alpha=0.5)
    ax1.axvline(x=0, color='gray', lw=0.5, alpha=0.5)

    # Time axes
    ax1.annotate('', xy=(4.5, 0), xytext=(-4.5, 0),
                arrowprops=dict(arrowstyle='->', color=PM_COLORS["time1"],
                               lw=2, mutation_scale=15))
    ax1.text(4.2, -0.5, r"$t$", fontsize=14, color=PM_COLORS["time1"],
             fontweight='bold')

    ax1.annotate('', xy=(0, 4.5), xytext=(0, -4.5),
                arrowprops=dict(arrowstyle='->', color=PM_COLORS["time2"],
                               lw=2, mutation_scale=15))
    ax1.text(0.3, 4.2, r"$\tau$", fontsize=14, color=PM_COLORS["time2"],
             fontweight='bold')

    # Gauge orbits (hyperbolas for Sp(2,R))
    t_vals = np.linspace(-4, 4, 200)
    for c in [1, 2, 3]:
        # Hyperbola: t^2 - tau^2 = c^2 (spacelike separation)
        mask = t_vals**2 > c**2
        tau_plus = np.sqrt(t_vals[mask]**2 - c**2)
        tau_minus = -tau_plus
        ax1.plot(t_vals[mask], tau_plus, '-', color=PM_COLORS["purple"],
                lw=1.5, alpha=0.5)
        ax1.plot(t_vals[mask], tau_minus, '-', color=PM_COLORS["purple"],
                lw=1.5, alpha=0.5)

    # Light-cone (t^2 = tau^2)
    ax1.plot([-4, 4], [-4, 4], '--', color=PM_COLORS["warning"], lw=2, label='Light cone')
    ax1.plot([-4, 4], [4, -4], '--', color=PM_COLORS["warning"], lw=2)

    # Physical time line (gauge-fixed: tau = 0)
    ax1.axhline(y=0, color=PM_COLORS["pink"], lw=3, label=r'Physical time ($\tau=0$)')

    # Sample points and their gauge orbits
    points = [(2, 1.5, 'A'), (-1.5, 2, 'B'), (3, -1, 'C')]
    for x, y, label in points:
        circle = Circle((x, y), 0.2, facecolor=PM_COLORS["orange"],
                        edgecolor='white', linewidth=2, zorder=5)
        ax1.add_patch(circle)
        ax1.text(x + 0.3, y + 0.3, label, fontsize=10, fontweight='bold',
                color=PM_COLORS["orange"])

        # Arrow to gauge-fixed position
        # For Sp(2,R), gauge fixing maps (t, tau) to (sqrt(t^2-tau^2), 0) if t^2 > tau^2
        if x**2 > y**2:
            t_fixed = np.sqrt(x**2 - y**2) * np.sign(x)
            ax1.annotate('', xy=(t_fixed, 0), xytext=(x, y),
                        arrowprops=dict(arrowstyle='->', color=PM_COLORS["pink"],
                                       lw=1.5, ls='--', mutation_scale=10))
            # Fixed point
            circle_fixed = Circle((t_fixed, 0), 0.15, facecolor=PM_COLORS["pink"],
                                  edgecolor='white', linewidth=1.5, zorder=5)
            ax1.add_patch(circle_fixed)

    ax1.legend(loc='upper left', fontsize=9)
    ax1.set_xlabel("t (physical time component)", fontsize=10)
    ax1.set_ylabel(r"$\tau$ (orthogonal time component)", fontsize=10)

    # === Panel 2: Sp(2,R) Constraints ===
    ax2 = fig.add_subplot(gs[0, 1])
    ax2.set_xlim(0, 10)
    ax2.set_ylim(0, 10)
    ax2.axis('off')
    ax2.set_title("The Three Sp(2,R) Constraints", fontsize=13, fontweight='bold',
                  color=PM_COLORS["purple"], pad=10)

    # Constraint boxes
    constraints = [
        (r"$X^2 = X^\mu X_\mu = 0$", "Position is null", "Worldline on light-cone", "#e74c3c"),
        (r"$X \cdot P = X^\mu P_\mu = 0$", "Orthogonality", "Position orthogonal to momentum", "#3498db"),
        (r"$P^2 + M^2 = 0$", "Mass-shell condition", "On-shell propagation", "#2ecc71"),
    ]

    for i, (formula, name, meaning, color) in enumerate(constraints):
        y_pos = 7.5 - i * 2.5

        # Box
        box = FancyBboxPatch((0.5, y_pos - 0.8), 9, 2,
                             boxstyle="round,pad=0.03,rounding_size=0.15",
                             facecolor='white', edgecolor=color, linewidth=2.5)
        ax2.add_patch(box)

        # Number badge
        badge = Circle((1.2, y_pos + 0.2), 0.35, facecolor=color,
                       edgecolor='white', linewidth=2)
        ax2.add_patch(badge)
        ax2.text(1.2, y_pos + 0.2, str(i+1), fontsize=12, fontweight='bold',
                ha='center', va='center', color='white')

        # Content
        ax2.text(5.25, y_pos + 0.5, formula, fontsize=13, fontweight='bold',
                ha='center', va='center', color=color)
        ax2.text(5.25, y_pos - 0.1, f"{name}: {meaning}", fontsize=9,
                ha='center', va='center', color=PM_COLORS["text"])

    # Summary box
    summary = FancyBboxPatch((0.5, 0.3), 9, 1.5,
                             boxstyle="round,pad=0.03,rounding_size=0.1",
                             facecolor='#f0e6ff', edgecolor=PM_COLORS["purple"],
                             linewidth=2)
    ax2.add_patch(summary)
    ax2.text(5, 1.35, "Together: 3 constraints eliminate 3 DOF", fontsize=11,
             fontweight='bold', ha='center', va='center', color=PM_COLORS["purple"])
    ax2.text(5, 0.7, "(24,2) --[Sp(2,R)]--> (12,1) + gauge redundancy",
             fontsize=10, ha='center', va='center', color=PM_COLORS["text"])

    # === Panel 3: Dimensional Reduction Flow ===
    ax3 = fig.add_subplot(gs[1, 0])
    ax3.set_xlim(0, 10)
    ax3.set_ylim(0, 8)
    ax3.axis('off')
    ax3.set_title("Dimensional Reduction via Gauge Fixing", fontsize=13,
                  fontweight='bold', color=PM_COLORS["pink"], pad=10)

    # Stage boxes
    stages = [
        ("26D Bulk", "(24, 2)", "24 space + 2 time", PM_COLORS["purple"], 1),
        ("Sp(2,R) Fix", "Constraints", r"$\tau \to 0$", PM_COLORS["pink"], 4),
        ("13D Shadow", "(12, 1)", "12 space + 1 time", PM_COLORS["space"], 7),
    ]

    for i, (title, sub1, sub2, color, x_pos) in enumerate(stages):
        box = FancyBboxPatch((x_pos - 0.8, 3), 2.6, 4,
                             boxstyle="round,pad=0.03,rounding_size=0.2",
                             facecolor='white', edgecolor=color, linewidth=2.5)
        ax3.add_patch(box)

        ax3.text(x_pos + 0.5, 6.3, title, fontsize=11, fontweight='bold',
                ha='center', va='center', color=color)
        ax3.text(x_pos + 0.5, 5.3, sub1, fontsize=13, fontweight='bold',
                ha='center', va='center', color=PM_COLORS["dark"])
        ax3.text(x_pos + 0.5, 4.3, sub2, fontsize=9, ha='center',
                va='center', color=PM_COLORS["text"])

        # Arrows between stages
        if i < 2:
            next_x = stages[i+1][4]
            ax3.annotate('', xy=(next_x - 1, 5), xytext=(x_pos + 1.5, 5),
                        arrowprops=dict(arrowstyle='->', color=PM_COLORS["dark"],
                                       lw=2.5, mutation_scale=20))

    # Bottom explanation
    explain = FancyBboxPatch((0.5, 0.5), 9, 2,
                             boxstyle="round,pad=0.03,rounding_size=0.1",
                             facecolor=PM_COLORS["light"], edgecolor=PM_COLORS["dark"],
                             linewidth=1.5)
    ax3.add_patch(explain)
    ax3.text(5, 2.0, "The \"Extra\" Time is Not Lost!", fontsize=11, fontweight='bold',
             ha='center', va='center', color=PM_COLORS["dark"])
    ax3.text(5, 1.3, r"It becomes a gauge degree of freedom. Different $\tau$ slices",
             fontsize=9, ha='center', va='center', color=PM_COLORS["text"])
    ax3.text(5, 0.8, "give equivalent physics - that's the Sp(2,R) gauge symmetry!",
             fontsize=9, ha='center', va='center', color=PM_COLORS["text"])

    # === Panel 4: Physical Interpretation ===
    ax4 = fig.add_subplot(gs[1, 1])
    ax4.set_xlim(0, 10)
    ax4.set_ylim(0, 8)
    ax4.axis('off')
    ax4.set_title("Physical Interpretation", fontsize=13, fontweight='bold',
                  color=PM_COLORS["orange"], pad=10)

    # Analogy: Latitude/Longitude
    analogy_box = FancyBboxPatch((0.5, 4.5), 9, 3,
                                 boxstyle="round,pad=0.03,rounding_size=0.15",
                                 facecolor='#fff9e6', edgecolor=PM_COLORS["orange"],
                                 linewidth=2)
    ax4.add_patch(analogy_box)

    ax4.text(5, 7.0, "Analogy: Choosing a Coordinate System", fontsize=11,
             fontweight='bold', ha='center', va='center', color=PM_COLORS["orange"])

    ax4.text(5, 6.2, "Just as you can describe a point on Earth using", fontsize=9,
             ha='center', va='center', color=PM_COLORS["text"])
    ax4.text(5, 5.6, "different coordinate systems (lat/long, UTM, etc.),", fontsize=9,
             ha='center', va='center', color=PM_COLORS["text"])
    ax4.text(5, 5.0, "the two times are different 'coordinates' on the", fontsize=9,
             ha='center', va='center', color=PM_COLORS["text"])
    ax4.text(5, 4.4, "same underlying reality. Gauge fixing picks one.", fontsize=9,
             ha='center', va='center', color=PM_COLORS["text"], fontweight='bold')

    # Key points
    points_data = [
        (r"$\tau = 0$ gives standard (3+1)D physics", PM_COLORS["time1"]),
        ("Different gauges = same physics", PM_COLORS["purple"]),
        ("Extra symmetry constrains predictions", PM_COLORS["space"]),
    ]

    for i, (text, color) in enumerate(points_data):
        y_pos = 3.5 - i * 1.0
        bullet = Circle((1.2, y_pos), 0.15, facecolor=color, edgecolor='white')
        ax4.add_patch(bullet)
        ax4.text(1.8, y_pos, text, fontsize=10, va='center', color=PM_COLORS["text"])

    # Result box
    result = FancyBboxPatch((0.5, 0.3), 9, 1.2,
                            boxstyle="round,pad=0.03,rounding_size=0.1",
                            facecolor='#e8f8f5', edgecolor=PM_COLORS["space"],
                            linewidth=2)
    ax4.add_patch(result)
    ax4.text(5, 1.1, "Result: The mathematics of 2T physics", fontsize=10,
             fontweight='bold', ha='center', va='center', color=PM_COLORS["space"])
    ax4.text(5, 0.55, "explains why our universe has the symmetries it does!",
             fontsize=10, ha='center', va='center', color=PM_COLORS["text"])

    # Save figure
    output_file = Path(__file__).parent / output_path
    output_file.parent.mkdir(exist_ok=True, parents=True)
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    plt.savefig(output_file, facecolor='white', edgecolor='none')
    plt.close()
    print(f"Saved: {output_file.resolve()}")


def main():
    """Generate all two-time comparison visualizations."""
    if not HAS_MATPLOTLIB:
        print("Matplotlib not available. Skipping visualization generation.")
        return

    print("=" * 60)
    print("GENERATING TWO-TIME COMPARISON VISUALIZATIONS")
    print("=" * 60)

    print("\n1. Generating 2T vs 1T Comparison diagram...")
    generate_2t_vs_1t_comparison()

    print("\n2. Generating Gauge Fixing Time diagram...")
    generate_gauge_fixing_time()

    print("\n" + "=" * 60)
    print("All visualizations generated successfully!")
    print("=" * 60)


if __name__ == "__main__":
    main()
