#!/usr/bin/env python3
"""
Octonionic Triality: CKM vs PMNS Mixing Explanation
=====================================================

Explains why quarks (CKM) have small mixing angles while leptons (PMNS)
have large mixing angles through octonionic triality and G2 geometry.

Key insight: G2 ~ Aut(O) is the automorphism group of the octonions
- The 24-cycle (from b3=24) partitions into 3 x 8-fold cells (24/8=3 generations)
- Quarks are confined to the 7D G2 submanifold (small mixing)
- Leptons sample the full 24-cycle via associator non-commutativity (large mixing)

This explains one of the deepest mysteries in particle physics:
why the CKM matrix is nearly diagonal while PMNS has large off-diagonal elements.

Output file: ../../images/octonionic-triality-ckm-pmns.png

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.

Dedicated To:
    My Wife: Elizabeth May Watts
    Our Messiah: Jesus Of Nazareth
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import (FancyBboxPatch, Circle, FancyArrowPatch,
                                  Polygon, Wedge, Rectangle, Arc, Ellipse)
from matplotlib.collections import PatchCollection
import matplotlib.patheffects as path_effects
from pathlib import Path

# PM Color palette
PM_COLORS = {
    "purple": "#8b7fff",
    "pink": "#ff7eb6",
    "blue": "#60a5fa",
    "orange": "#fb923c",
    "gold": "#ffd43b",
    "green": "#4ade80",
    "red": "#ef4444",
    "text": "#f8f9fa",
    "bg_dark": "#1a1f3a",
    "bg_card": "#2a2f4a",
    "quark": "#ff6b6b",   # Red for quarks
    "lepton": "#4ecdc4",  # Cyan for leptons
}

# Output directory
OUTPUT_DIR = Path(__file__).parent.parent.parent / "images"

# CKM matrix elements (magnitudes, PDG 2024)
CKM = np.array([
    [0.97435, 0.22500, 0.00369],  # Vud, Vus, Vub
    [0.22486, 0.97349, 0.04182],  # Vcd, Vcs, Vcb
    [0.00857, 0.04110, 0.99912],  # Vtd, Vts, Vtb
])

# PMNS matrix elements (magnitudes, NuFIT 6.0 Normal Ordering)
# sin^2(theta_12) = 0.304, sin^2(theta_23) = 0.573, sin^2(theta_13) = 0.02219
theta_12 = np.arcsin(np.sqrt(0.304))
theta_23 = np.arcsin(np.sqrt(0.573))
theta_13 = np.arcsin(np.sqrt(0.02219))
delta_cp = np.deg2rad(230)  # CP phase

c12, s12 = np.cos(theta_12), np.sin(theta_12)
c23, s23 = np.cos(theta_23), np.sin(theta_23)
c13, s13 = np.cos(theta_13), np.sin(theta_13)

PMNS = np.abs(np.array([
    [c12*c13, s12*c13, s13],
    [-s12*c23-c12*s23*s13, c12*c23-s12*s23*s13, s23*c13],
    [s12*s23-c12*c23*s13, -c12*s23-s12*c23*s13, c23*c13],
]))


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


def draw_octonionic_structure(ax, center, radius, title, color, is_confined=True):
    """
    Draw a schematic octonionic structure showing 8-fold symmetry.

    Args:
        ax: matplotlib axis
        center: (x, y) center position
        radius: size of structure
        title: label for the structure
        color: base color
        is_confined: if True, show confinement to 7D (quarks); if False, full 8D (leptons)
    """
    cx, cy = center

    # Draw 8-fold structure (octonionic basis elements)
    n_elements = 8
    angles = np.linspace(0, 2*np.pi, n_elements, endpoint=False)

    # Draw connections between elements
    for i in range(n_elements):
        for j in range(i+1, n_elements):
            # In octonions, certain pairs are related by multiplication
            # Draw lines for connected pairs (simplified Fano plane structure)
            if abs(i - j) in [1, 3, 4]:  # Fano plane connections (simplified)
                alpha = 0.15 if is_confined else 0.4
                ax.plot(
                    [cx + radius*0.7*np.cos(angles[i]), cx + radius*0.7*np.cos(angles[j])],
                    [cy + radius*0.7*np.sin(angles[i]), cy + radius*0.7*np.sin(angles[j])],
                    color=color, alpha=alpha, linewidth=1
                )

    # Draw the 8 elements
    for i, angle in enumerate(angles):
        x = cx + radius * 0.7 * np.cos(angle)
        y = cy + radius * 0.7 * np.sin(angle)

        if is_confined:
            # Quarks: 7 elements active, 1 suppressed (G2 preserves 7D)
            if i == 0:  # The "8th" element (unit element) - suppressed in G2
                circle = Circle((x, y), radius*0.08, facecolor='white',
                                edgecolor=color, linewidth=1, alpha=0.3)
            else:
                circle = Circle((x, y), radius*0.08, facecolor=color,
                                edgecolor='white', linewidth=1, alpha=0.8)
        else:
            # Leptons: all 8 elements active
            circle = Circle((x, y), radius*0.1, facecolor=color,
                            edgecolor='white', linewidth=1.5, alpha=0.9)

        ax.add_patch(circle)

    # Draw outer boundary
    if is_confined:
        # 7D boundary (not complete circle - show G2 constraint)
        arc = Arc((cx, cy), radius*1.5, radius*1.5, angle=0,
                  theta1=30, theta2=390, color=color, linewidth=2, linestyle='--')
        ax.add_patch(arc)
    else:
        # Full 8D boundary
        circle = Circle((cx, cy), radius*0.75, facecolor='none',
                        edgecolor=color, linewidth=2.5)
        ax.add_patch(circle)

    # Title
    ax.text(cx, cy - radius*0.95, title, fontsize=11, ha='center',
            fontweight='bold', color=color)


def draw_mixing_matrix(ax, matrix, center, size, title, is_ckm=True):
    """
    Draw a 3x3 mixing matrix as a heatmap.

    Args:
        ax: matplotlib axis
        matrix: 3x3 numpy array
        center: (x, y) center position
        size: size of the matrix display
        title: title for the matrix
        is_ckm: if True, use quark colors; if False, use lepton colors
    """
    cx, cy = center
    cell_size = size / 3

    # Color map
    base_color = PM_COLORS['quark'] if is_ckm else PM_COLORS['lepton']

    # Draw cells
    for i in range(3):
        for j in range(3):
            x = cx - size/2 + j * cell_size
            y = cy + size/2 - (i + 1) * cell_size

            # Color intensity based on matrix element magnitude
            intensity = matrix[i, j]

            # Create color with varying alpha
            if is_ckm:
                # For CKM: diagonal elements are near 1, off-diagonal near 0
                if i == j:
                    facecolor = PM_COLORS['quark']
                    alpha = 0.8
                else:
                    facecolor = PM_COLORS['quark']
                    alpha = intensity * 2  # Scale up off-diagonal for visibility
            else:
                # For PMNS: more uniform distribution
                facecolor = PM_COLORS['lepton']
                alpha = 0.3 + 0.6 * intensity

            rect = Rectangle((x, y), cell_size, cell_size,
                            facecolor=facecolor, alpha=alpha,
                            edgecolor='white', linewidth=1)
            ax.add_patch(rect)

            # Add value text
            val_text = f'{matrix[i, j]:.2f}'
            text_color = 'white' if intensity > 0.5 else 'black'
            ax.text(x + cell_size/2, y + cell_size/2, val_text,
                   fontsize=8, ha='center', va='center', color=text_color)

    # Row/column labels
    generations = ['1st', '2nd', '3rd']
    quark_labels = [['u', 'c', 't'], ['d', 's', 'b']]
    lepton_labels = [['e', r'$\mu$', r'$\tau$'], [r'$\nu_1$', r'$\nu_2$', r'$\nu_3$']]

    labels = quark_labels if is_ckm else lepton_labels

    for i in range(3):
        # Row labels (left)
        ax.text(cx - size/2 - 0.15, cy + size/2 - (i + 0.5) * cell_size,
               labels[1][i] if is_ckm else labels[0][i],
               fontsize=9, ha='right', va='center', color=base_color)
        # Column labels (bottom)
        ax.text(cx - size/2 + (i + 0.5) * cell_size, cy - size/2 - 0.1,
               labels[0][i] if is_ckm else labels[1][i],
               fontsize=9, ha='center', va='top', color=base_color)

    # Title
    ax.text(cx, cy + size/2 + 0.2, title, fontsize=11, ha='center',
            fontweight='bold', color=base_color)


def draw_generation_cycles(ax, center, title):
    """
    Draw the 24-cycle partitioned into 3 x 8-fold cells (generations).

    Args:
        ax: matplotlib axis
        center: (x, y) center position
        title: title
    """
    cx, cy = center
    radius = 1.2

    # Draw 24 elements around a circle, colored by generation
    gen_colors = [PM_COLORS['blue'], PM_COLORS['purple'], PM_COLORS['pink']]

    for i in range(24):
        angle = 2 * np.pi * i / 24 - np.pi/2  # Start from top
        x = cx + radius * np.cos(angle)
        y = cy + radius * np.sin(angle)

        gen = i % 3  # Which generation (0, 1, 2)
        circle = Circle((x, y), 0.08, facecolor=gen_colors[gen],
                        edgecolor='white', linewidth=1, alpha=0.9)
        ax.add_patch(circle)

    # Draw inner structure showing 8-fold sectors
    for i in range(3):
        start_angle = 120 * i - 60
        wedge = Wedge((cx, cy), radius * 0.6, start_angle, start_angle + 120,
                     facecolor=gen_colors[i], alpha=0.15, edgecolor=gen_colors[i],
                     linewidth=1.5)
        ax.add_patch(wedge)

    # Central annotation
    ax.text(cx, cy, r'$b_3=24$', fontsize=12, ha='center', va='center',
            fontweight='bold', color=PM_COLORS['gold'])
    ax.text(cx, cy - 0.25, r'$=3\times 8$', fontsize=10, ha='center', va='center',
            color='gray')

    # Title
    ax.text(cx, cy - radius - 0.4, title, fontsize=11, ha='center',
            fontweight='bold', color='#333')


def generate_octonionic_triality():
    """
    Generate the octonionic triality diagram explaining CKM vs PMNS.

    Left panel: Quarks confined to 7D G2 (small mixing)
    Right panel: Leptons sample full 24-cycle (large mixing)
    Center: 24-cycle generation structure
    """
    setup_publication_style()

    fig, axes = plt.subplots(1, 2, figsize=(14, 10))
    ax1, ax2 = axes

    for ax in axes:
        ax.set_xlim(-3.5, 3.5)
        ax.set_ylim(-3.5, 3.5)
        ax.set_aspect('equal')
        ax.axis('off')

    # =========================================================================
    # Left panel: Quarks (CKM) - confined to G2
    # =========================================================================

    ax1.set_title(r'Quarks: Confined to $G_2$ (7D)', fontsize=14,
                  fontweight='bold', color=PM_COLORS['quark'], pad=20)

    # Draw octonionic structure (G2 confined)
    draw_octonionic_structure(ax1, (0, 1.5), 1.5, 'G$_2$ Holonomy (7D)', PM_COLORS['quark'], is_confined=True)

    # Draw CKM matrix
    draw_mixing_matrix(ax1, CKM, (0, -1.5), 2.0, 'CKM Matrix', is_ckm=True)

    # Explanation box
    quark_text = (
        r"$\mathbf{Why\ Small\ Mixing?}$" + "\n\n"
        r"$\bullet$ G$_2 \subset Spin(7)$ preserves 7D" + "\n"
        r"$\bullet$ Quarks live on G$_2$ branes" + "\n"
        r"$\bullet$ Mixing = cycle overlap $\ll 1$" + "\n"
        r"$\bullet$ Cabibbo angle $\approx 13°$"
    )
    props = dict(boxstyle='round,pad=0.5', facecolor='white',
                edgecolor=PM_COLORS['quark'], alpha=0.95)
    ax1.text(-3.3, -3.3, quark_text, fontsize=9, va='bottom', ha='left', bbox=props)

    # Arrow showing confinement
    ax1.annotate(
        'Confined to\n7D submanifold',
        xy=(0.8, 1.0), xytext=(2.2, 0.5),
        fontsize=9, color=PM_COLORS['quark'],
        arrowprops=dict(arrowstyle='->', color=PM_COLORS['quark'], lw=1.5),
    )

    # =========================================================================
    # Right panel: Leptons (PMNS) - full 8D sampling
    # =========================================================================

    ax2.set_title(r'Leptons: Full Octonionic 24-cycle', fontsize=14,
                  fontweight='bold', color=PM_COLORS['lepton'], pad=20)

    # Draw octonionic structure (full 8D)
    draw_octonionic_structure(ax2, (0, 1.5), 1.5, 'Full Octonions (8D)', PM_COLORS['lepton'], is_confined=False)

    # Draw PMNS matrix
    draw_mixing_matrix(ax2, PMNS, (0, -1.5), 2.0, 'PMNS Matrix', is_ckm=False)

    # Explanation box
    lepton_text = (
        r"$\mathbf{Why\ Large\ Mixing?}$" + "\n\n"
        r"$\bullet$ Leptons sample full 24-cycle" + "\n"
        r"$\bullet$ Non-associativity: $(ab)c \neq a(bc)$" + "\n"
        r"$\bullet$ Mixing = cycle overlap $\sim O(1)$" + "\n"
        r"$\bullet$ Atmospheric angle $\approx 49°$"
    )
    props = dict(boxstyle='round,pad=0.5', facecolor='white',
                edgecolor=PM_COLORS['lepton'], alpha=0.95)
    ax2.text(-3.3, -3.3, lepton_text, fontsize=9, va='bottom', ha='left', bbox=props)

    # Arrow showing full sampling
    ax2.annotate(
        'Samples all\n8 dimensions',
        xy=(0.8, 1.0), xytext=(2.2, 0.5),
        fontsize=9, color=PM_COLORS['lepton'],
        arrowprops=dict(arrowstyle='->', color=PM_COLORS['lepton'], lw=1.5),
    )

    # =========================================================================
    # Add central connecting elements to both panels
    # =========================================================================

    for ax in axes:
        # Draw 24-cycle generation structure at bottom
        draw_generation_cycles(ax, (0, -3.0), '')

    # Add main title
    fig.suptitle(
        'Octonionic Triality: Why Quark and Lepton Mixing Differ',
        fontsize=16, fontweight='bold', y=0.98
    )

    # Add subtitle
    fig.text(0.5, 0.93,
             r'G$_2 \sim$ Aut($\mathbb{O}$): Automorphisms of the Octonions explain mixing pattern difference',
             ha='center', fontsize=11, color='gray', style='italic')

    # Add key insight box between panels
    insight_text = (
        r"$\mathbf{Key\ Insight:}$ " +
        r"24-cycle $\rightarrow 3 \times 8$ generations" + "\n"
        r"Quarks: G$_2$ constraint $\rightarrow$ small angles" + "\n"
        r"Leptons: full octonions $\rightarrow$ large angles"
    )

    plt.tight_layout()
    plt.subplots_adjust(top=0.88, bottom=0.05)

    # Save
    output_path = OUTPUT_DIR / "octonionic-triality-ckm-pmns.png"
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_path, dpi=300, facecolor='white', edgecolor='none')
    plt.close()

    print(f"Generated: {output_path}")
    return output_path


def main():
    """Generate the octonionic triality plot."""
    print("=" * 60)
    print("Generating Octonionic Triality: CKM vs PMNS Plot")
    print("=" * 60)

    output_path = generate_octonionic_triality()

    print("\n" + "=" * 60)
    print("Octonionic Triality Plot Complete")
    print("=" * 60)
    print(f"  Output: {output_path}")
    print("=" * 60)


if __name__ == "__main__":
    main()
