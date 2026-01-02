#!/usr/bin/env python3
"""
theory_overview_diagrams.py - Theory Overview Visualization Diagrams

Generates two diagrams for Principia Metaphysica theory overview:
1. parameter-space.png - PM parameter space showing constraints from b3=24
2. experimental-signatures.png - Key experimental signatures to test PM predictions

All visualizations emphasize b3=24 as the single topological input that determines
everything else in the theory.

Output: ../../images/parameter-space.png, ../../images/experimental-signatures.png

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.
Licensed under the MIT License. See LICENSE file for details.
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import Circle, FancyBboxPatch, Polygon, Wedge, Rectangle
from matplotlib.collections import PatchCollection
import matplotlib.patheffects as pe
import os
import sys

# PM Colors
PM_PURPLE = '#8b7fff'  # Primary PM color
PM_GOLD = '#ffd43b'    # Predictions color
PM_DARK = '#2d1b4e'    # Dark purple
PM_LIGHT = '#d4ccff'   # Light purple
PM_GREEN = '#4ade80'   # Success/validation
PM_BLUE = '#60a5fa'    # Info
PM_RED = '#f87171'     # Warning/excluded

# Set publication-quality style
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.size'] = 11
plt.rcParams['axes.labelsize'] = 13
plt.rcParams['axes.titlesize'] = 15
plt.rcParams['legend.fontsize'] = 10
plt.rcParams['figure.dpi'] = 300
plt.rcParams['axes.facecolor'] = '#fafafa'
plt.rcParams['figure.facecolor'] = 'white'


def generate_parameter_space_diagram(output_path: str) -> None:
    """
    Generate PM parameter space diagram.

    Shows how b3=24 constrains the entire theory:
    - Single topological input
    - Derivation chains to all physical parameters
    - Comparison with Standard Model free parameters

    Args:
        output_path: Path to save the PNG file
    """
    fig, ax = plt.subplots(figsize=(14, 11))
    ax.set_xlim(-0.5, 13.5)
    ax.set_ylim(-0.5, 10.5)
    ax.set_aspect('equal')
    ax.axis('off')

    # Title
    ax.text(6.75, 10.2, 'PM Parameter Space: Geometry Constrains Physics',
            fontsize=18, fontweight='bold', ha='center', color=PM_DARK)
    ax.text(6.75, 9.7, r'Single topological input $b_3=24$ determines all physical parameters',
            fontsize=12, ha='center', color='#666666', style='italic')

    # ===========================================================================
    # Central INPUT box - b3=24
    # ===========================================================================

    input_box = FancyBboxPatch((5.0, 7.5), 3.5, 1.6, boxstyle="round,pad=0.15",
                                facecolor=PM_GOLD, edgecolor=PM_DARK, linewidth=3, alpha=0.9)
    ax.add_patch(input_box)

    ax.text(6.75, 8.7, 'THE INPUT', fontsize=10, ha='center', color=PM_DARK,
            fontweight='bold', style='italic')
    ax.text(6.75, 8.2, r'$b_3 = 24$', fontsize=24, ha='center', color=PM_DARK,
            fontweight='bold')
    ax.text(6.75, 7.7, 'Associative 3-cycles', fontsize=10, ha='center', color='#444444')

    # ===========================================================================
    # Derived Geometry Layer
    # ===========================================================================

    # chi_eff box
    chi_box = FancyBboxPatch((1.5, 5.5), 2.5, 1.3, boxstyle="round,pad=0.1",
                              facecolor=PM_LIGHT, edgecolor=PM_PURPLE, linewidth=2, alpha=0.8)
    ax.add_patch(chi_box)
    ax.text(2.75, 6.5, r'$\chi_{eff} = 144$', fontsize=12, ha='center', color=PM_DARK,
            fontweight='bold')
    ax.text(2.75, 6.0, 'Euler char.', fontsize=9, ha='center', color='#666666')
    ax.text(2.75, 5.7, r'$= 2(h^{1,1}-h^{2,1}+h^{3,1})$', fontsize=8, ha='center', color='#888888')

    # Arrow from b3 to chi_eff
    ax.annotate('', xy=(3.5, 6.8), xytext=(5.0, 7.8),
                arrowprops=dict(arrowstyle='->', color=PM_PURPLE, lw=2))

    # b2 box
    b2_box = FancyBboxPatch((5.5, 5.5), 2.5, 1.3, boxstyle="round,pad=0.1",
                             facecolor=PM_LIGHT, edgecolor=PM_PURPLE, linewidth=2, alpha=0.8)
    ax.add_patch(b2_box)
    ax.text(6.75, 6.5, r'$b_2 = 4$', fontsize=12, ha='center', color=PM_DARK,
            fontweight='bold')
    ax.text(6.75, 6.0, 'Kahler moduli', fontsize=9, ha='center', color='#666666')
    ax.text(6.75, 5.7, 'Gauge sectors', fontsize=8, ha='center', color='#888888')

    # Arrow from b3 to b2
    ax.annotate('', xy=(6.75, 6.8), xytext=(6.75, 7.5),
                arrowprops=dict(arrowstyle='->', color=PM_PURPLE, lw=2))

    # d/R box
    dr_box = FancyBboxPatch((9.5, 5.5), 2.5, 1.3, boxstyle="round,pad=0.1",
                             facecolor=PM_LIGHT, edgecolor=PM_PURPLE, linewidth=2, alpha=0.8)
    ax.add_patch(dr_box)
    ax.text(10.75, 6.5, r'$d/R = 0.12$', fontsize=12, ha='center', color=PM_DARK,
            fontweight='bold')
    ax.text(10.75, 6.0, 'Cycle separation', fontsize=9, ha='center', color='#666666')
    ax.text(10.75, 5.7, 'TCS gluing', fontsize=8, ha='center', color='#888888')

    # Arrow from b3 to d/R
    ax.annotate('', xy=(10.0, 6.8), xytext=(8.5, 7.8),
                arrowprops=dict(arrowstyle='->', color=PM_PURPLE, lw=2))

    # ===========================================================================
    # Physics Outputs Layer
    # ===========================================================================

    # Generations box
    gen_box = FancyBboxPatch((0.3, 3.2), 2.5, 1.5, boxstyle="round,pad=0.1",
                              facecolor=PM_GREEN, edgecolor=PM_DARK, linewidth=2, alpha=0.3)
    ax.add_patch(gen_box)
    ax.text(1.55, 4.35, r'$n_{gen} = 3$', fontsize=13, ha='center', color=PM_DARK,
            fontweight='bold')
    ax.text(1.55, 3.9, 'Fermion families', fontsize=9, ha='center', color='#444444')
    ax.text(1.55, 3.5, r'$= \chi_{eff}/48$', fontsize=9, ha='center', color='#666666')

    # Arrow from chi_eff to generations
    ax.annotate('', xy=(1.8, 4.7), xytext=(2.5, 5.5),
                arrowprops=dict(arrowstyle='->', color=PM_GREEN, lw=2))

    # Gauge unification box
    gauge_box = FancyBboxPatch((3.2, 3.2), 2.8, 1.5, boxstyle="round,pad=0.1",
                                facecolor=PM_GREEN, edgecolor=PM_DARK, linewidth=2, alpha=0.3)
    ax.add_patch(gauge_box)
    ax.text(4.6, 4.35, r'$\alpha_{GUT}^{-1} = 25.3$', fontsize=12, ha='center',
            color=PM_DARK, fontweight='bold')
    ax.text(4.6, 3.9, 'GUT coupling', fontsize=9, ha='center', color='#444444')
    ax.text(4.6, 3.5, 'From moduli', fontsize=9, ha='center', color='#666666')

    # Arrow from b2 to gauge
    ax.annotate('', xy=(4.6, 4.7), xytext=(5.8, 5.5),
                arrowprops=dict(arrowstyle='->', color=PM_GREEN, lw=2))

    # Proton decay box
    proton_box = FancyBboxPatch((6.3, 3.2), 2.8, 1.5, boxstyle="round,pad=0.1",
                                 facecolor=PM_GREEN, edgecolor=PM_DARK, linewidth=2, alpha=0.3)
    ax.add_patch(proton_box)
    ax.text(7.7, 4.35, r'$\tau_p = 8.15 \times 10^{34}$ yr', fontsize=10, ha='center',
            color=PM_DARK, fontweight='bold')
    ax.text(7.7, 3.9, 'Proton lifetime', fontsize=9, ha='center', color='#444444')
    ax.text(7.7, 3.5, 'From d/R', fontsize=9, ha='center', color='#666666')

    # Arrow from d/R to proton
    ax.annotate('', xy=(8.2, 4.7), xytext=(10.0, 5.5),
                arrowprops=dict(arrowstyle='->', color=PM_GREEN, lw=2))

    # KK masses box
    kk_box = FancyBboxPatch((9.5, 3.2), 2.8, 1.5, boxstyle="round,pad=0.1",
                             facecolor=PM_GREEN, edgecolor=PM_DARK, linewidth=2, alpha=0.3)
    ax.add_patch(kk_box)
    ax.text(10.9, 4.35, r'$M_{KK} \sim 5$ TeV', fontsize=12, ha='center',
            color=PM_DARK, fontweight='bold')
    ax.text(10.9, 3.9, 'KK gravitons', fontsize=9, ha='center', color='#444444')
    ax.text(10.9, 3.5, 'From topology', fontsize=9, ha='center', color='#666666')

    # Arrow from d/R to KK
    ax.annotate('', xy=(10.9, 4.7), xytext=(10.75, 5.5),
                arrowprops=dict(arrowstyle='->', color=PM_GREEN, lw=2))

    # ===========================================================================
    # Comparison with Standard Model (bottom left)
    # ===========================================================================

    sm_box = FancyBboxPatch((0.3, 0.3), 5.5, 2.5, boxstyle="round,pad=0.1",
                             facecolor='white', edgecolor=PM_RED, linewidth=2)
    ax.add_patch(sm_box)

    ax.text(3.05, 2.55, 'Standard Model Comparison', fontsize=11, fontweight='bold',
            ha='center', color=PM_DARK)

    # SM parameters count
    ax.text(0.6, 2.1, 'SM free parameters:', fontsize=10, color='#666666')
    ax.text(4.5, 2.1, '19+', fontsize=14, color=PM_RED, fontweight='bold')

    ax.text(0.6, 1.65, '  - 3 gauge couplings', fontsize=9, color='#888888')
    ax.text(0.6, 1.35, '  - 6 quark masses', fontsize=9, color='#888888')
    ax.text(0.6, 1.05, '  - 3 lepton masses', fontsize=9, color='#888888')
    ax.text(0.6, 0.75, '  - 4 CKM parameters', fontsize=9, color='#888888')
    ax.text(0.6, 0.45, '  - Higgs params, etc.', fontsize=9, color='#888888')

    ax.text(3.3, 1.65, 'PM free parameters:', fontsize=10, color='#666666')
    ax.text(5.3, 1.65, '1', fontsize=14, color=PM_GOLD, fontweight='bold')
    ax.text(3.3, 1.2, r'Just $b_3 = 24$!', fontsize=11, color=PM_GOLD, fontweight='bold')

    # ===========================================================================
    # Derivation Chain Legend (bottom right)
    # ===========================================================================

    chain_box = FancyBboxPatch((6.5, 0.3), 6.5, 2.5, boxstyle="round,pad=0.1",
                                facecolor=PM_LIGHT, edgecolor=PM_PURPLE, linewidth=2, alpha=0.5)
    ax.add_patch(chain_box)

    ax.text(9.75, 2.55, 'The Derivation Chain', fontsize=11, fontweight='bold',
            ha='center', color=PM_DARK)

    chain_items = [
        (r'$b_3 = 24$', 'Topological input', PM_GOLD),
        (r'$\rightarrow$', '', PM_DARK),
        ('Geometry', '(TCS G2)', PM_PURPLE),
        (r'$\rightarrow$', '', PM_DARK),
        ('Physics', '(testable)', PM_GREEN),
    ]

    x_pos = 6.8
    for item, desc, color in chain_items:
        if item == r'$\rightarrow$':
            ax.text(x_pos, 1.9, item, fontsize=14, color=color, fontweight='bold')
            x_pos += 0.6
        else:
            ax.text(x_pos, 2.0, item, fontsize=11, color=color, fontweight='bold')
            ax.text(x_pos, 1.6, desc, fontsize=8, color='#666666')
            x_pos += 2.0

    # Key formula
    ax.text(9.75, 0.9, 'Everything derives from topology:', fontsize=10,
            ha='center', color=PM_DARK, style='italic')
    ax.text(9.75, 0.5, r'No adjustable parameters beyond $b_3$', fontsize=10,
            ha='center', color=PM_DARK, fontweight='bold')

    # ===========================================================================
    # Layer labels on right side
    # ===========================================================================

    # Layer indicator
    ax.text(13.3, 8.2, 'TOPOLOGY', fontsize=9, ha='right', color=PM_GOLD, fontweight='bold',
            rotation=90, va='center')
    ax.text(13.3, 6.1, 'GEOMETRY', fontsize=9, ha='right', color=PM_PURPLE, fontweight='bold',
            rotation=90, va='center')
    ax.text(13.3, 3.9, 'PHYSICS', fontsize=9, ha='right', color=PM_GREEN, fontweight='bold',
            rotation=90, va='center')

    # Vertical guide lines
    ax.plot([12.8, 12.8], [7.5, 9.1], color=PM_GOLD, lw=3, alpha=0.5)
    ax.plot([12.8, 12.8], [5.5, 6.8], color=PM_PURPLE, lw=3, alpha=0.5)
    ax.plot([12.8, 12.8], [3.2, 4.7], color=PM_GREEN, lw=3, alpha=0.5)

    plt.tight_layout()

    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"[OK] Parameter space diagram saved to: {output_path}")
    plt.close()


def generate_experimental_signatures_diagram(output_path: str) -> None:
    """
    Generate experimental signatures diagram.

    Shows key experimental tests for PM predictions:
    - Proton decay (Super-K, Hyper-K)
    - KK gravitons (LHC, HL-LHC)
    - Neutrino parameters (DUNE, JUNO)
    - Dark energy (DESI, Euclid)

    Args:
        output_path: Path to save the PNG file
    """
    fig, ax = plt.subplots(figsize=(14, 11))
    ax.set_xlim(-0.5, 13.5)
    ax.set_ylim(-0.5, 10.5)
    ax.set_aspect('equal')
    ax.axis('off')

    # Title
    ax.text(6.75, 10.2, 'Experimental Signatures: Testing PM Predictions',
            fontsize=18, fontweight='bold', ha='center', color=PM_DARK)
    ax.text(6.75, 9.7, 'Five falsifiable predictions with timelines (2025-2040)',
            fontsize=12, ha='center', color='#666666', style='italic')

    # ===========================================================================
    # Timeline axis
    # ===========================================================================

    timeline_y = 0.8
    ax.plot([0.5, 12.5], [timeline_y, timeline_y], 'k-', lw=2, alpha=0.5)

    years = [2025, 2030, 2035, 2040]
    for i, year in enumerate(years):
        x = 0.5 + (year - 2025) * 0.8
        ax.plot([x, x], [timeline_y - 0.1, timeline_y + 0.1], 'k-', lw=2)
        ax.text(x, timeline_y - 0.35, str(year), fontsize=9, ha='center', color='#666666')

    ax.text(6.5, timeline_y - 0.6, 'Timeline', fontsize=10, ha='center', color='#888888')

    # ===========================================================================
    # Prediction boxes with experimental tests
    # ===========================================================================

    predictions = [
        {
            'title': 'Proton Decay',
            'prediction': r'$\tau_p = 8.15 \times 10^{34}$ yr',
            'experiment': 'Hyper-Kamiokande',
            'timeline': '2027-2035',
            'status': 'Critical test',
            'color': PM_PURPLE,
            'pos': (0.5, 7.5),
            'size': (3.8, 2.0),
            'detail': r'4.9$\times$ above Super-K limit',
            'icon': 'p'
        },
        {
            'title': 'KK Gravitons',
            'prediction': r'$M_{KK} \sim 5$ TeV',
            'experiment': 'HL-LHC',
            'timeline': '2029-2035',
            'status': 'Discovery mode',
            'color': PM_GOLD,
            'pos': (4.7, 7.5),
            'size': (3.8, 2.0),
            'detail': r'$5.2\sigma$ with 3 ab$^{-1}$',
            'icon': 'G'
        },
        {
            'title': 'Neutrino Mixing',
            'prediction': r'$\theta_{23} = 45.0°$ (maximal)',
            'experiment': 'DUNE / JUNO',
            'timeline': '2025-2030',
            'status': 'Ongoing',
            'color': PM_GREEN,
            'pos': (9.0, 7.5),
            'size': (4.0, 2.0),
            'detail': r'$\delta_{CP} = 197°$ (IO)',
            'icon': r'$\nu$'
        },
        {
            'title': 'Dark Energy EoS',
            'prediction': r'$w_0 = -0.994$, $w_a = 0.026$',
            'experiment': 'DESI / Euclid',
            'timeline': '2025-2032',
            'status': 'Ongoing',
            'color': PM_BLUE,
            'pos': (0.5, 4.5),
            'size': (4.0, 2.0),
            'detail': 'Mashiach field quintessence',
            'icon': r'$\Lambda$'
        },
        {
            'title': 'Generation Count',
            'prediction': r'$n_{gen} = 3$ (geometric)',
            'experiment': 'Cosmological surveys',
            'timeline': 'Validated',
            'status': 'Confirmed',
            'color': PM_GREEN,
            'pos': (4.9, 4.5),
            'size': (3.8, 2.0),
            'detail': r'$= \chi_{eff}/48 = 144/48$',
            'icon': '3'
        },
    ]

    for pred in predictions:
        # Draw prediction box
        box = FancyBboxPatch(pred['pos'], pred['size'][0], pred['size'][1],
                             boxstyle="round,pad=0.1", facecolor='white',
                             edgecolor=pred['color'], linewidth=2.5)
        ax.add_patch(box)

        cx, cy = pred['pos'][0] + pred['size'][0]/2, pred['pos'][1] + pred['size'][1]/2

        # Icon circle
        icon_circle = Circle((pred['pos'][0] + 0.4, cy + 0.3), 0.25,
                              facecolor=pred['color'], edgecolor='white', linewidth=2, alpha=0.8)
        ax.add_patch(icon_circle)
        ax.text(pred['pos'][0] + 0.4, cy + 0.3, pred['icon'], fontsize=10, ha='center',
                va='center', color='white', fontweight='bold')

        # Title
        ax.text(cx, cy + 0.7, pred['title'], fontsize=12, ha='center',
                fontweight='bold', color=PM_DARK)

        # Prediction value
        ax.text(cx, cy + 0.25, pred['prediction'], fontsize=10, ha='center',
                color=pred['color'], fontweight='bold')

        # Detail
        ax.text(cx, cy - 0.15, pred['detail'], fontsize=8, ha='center', color='#666666')

        # Experiment
        ax.text(cx, cy - 0.55, pred['experiment'], fontsize=9, ha='center',
                color='#444444', style='italic')

        # Timeline
        ax.text(cx, cy - 0.85, pred['timeline'], fontsize=8, ha='center', color='#888888')

        # Status indicator
        status_colors = {'Critical test': PM_PURPLE, 'Discovery mode': PM_GOLD,
                        'Ongoing': PM_BLUE, 'Confirmed': PM_GREEN}
        status_color = status_colors.get(pred['status'], PM_DARK)
        ax.text(pred['pos'][0] + pred['size'][0] - 0.2, pred['pos'][1] + pred['size'][1] - 0.15,
                pred['status'], fontsize=7, ha='right', color=status_color, fontweight='bold')

    # ===========================================================================
    # Summary statistics box (bottom right)
    # ===========================================================================

    stats_box = FancyBboxPatch((9.0, 4.5), 4.0, 2.0, boxstyle="round,pad=0.1",
                                facecolor=PM_LIGHT, edgecolor=PM_PURPLE, linewidth=2, alpha=0.5)
    ax.add_patch(stats_box)

    ax.text(11.0, 6.2, 'Validation Status', fontsize=12, fontweight='bold',
            ha='center', color=PM_DARK)

    stats = [
        ('Confirmed predictions:', '2', PM_GREEN),
        ('Testing in progress:', '3', PM_BLUE),
        ('Falsifiable by 2035:', '5', PM_GOLD),
    ]

    for i, (label, value, color) in enumerate(stats):
        y = 5.7 - i * 0.4
        ax.text(9.3, y, label, fontsize=10, color='#666666')
        ax.text(12.6, y, value, fontsize=12, ha='right', color=color, fontweight='bold')

    # ===========================================================================
    # Key insight: b3=24 constrains all
    # ===========================================================================

    insight_box = FancyBboxPatch((0.5, 2.2), 12.0, 1.5, boxstyle="round,pad=0.1",
                                  facecolor=PM_GOLD, edgecolor=PM_DARK, linewidth=2, alpha=0.2)
    ax.add_patch(insight_box)

    ax.text(6.5, 3.3, 'Key Insight: One Input, Five Predictions', fontsize=13,
            fontweight='bold', ha='center', color=PM_DARK)
    ax.text(6.5, 2.8, r'All predictions derive geometrically from $b_3 = 24$ — no tuning, no free parameters',
            fontsize=11, ha='center', color=PM_DARK)
    ax.text(6.5, 2.45, 'If any prediction fails experimental test, the entire framework is falsified',
            fontsize=10, ha='center', color='#666666', style='italic')

    # ===========================================================================
    # Experiment icons/logos area (left side indicators)
    # ===========================================================================

    # Draw connecting lines from predictions to timeline
    connections = [
        ((2.4, 7.5), (2.5, timeline_y + 0.15), 'Hyper-K'),  # Proton decay
        ((6.6, 7.5), (4.5, timeline_y + 0.15), 'HL-LHC'),   # KK
        ((11.0, 7.5), (1.5, timeline_y + 0.15), 'DUNE'),    # Neutrino
        ((2.5, 4.5), (1.0, timeline_y + 0.15), 'DESI'),     # Dark energy
    ]

    for start, end, label in connections:
        ax.plot([start[0], end[0]], [start[1], end[1]], '--', color='#cccccc', lw=1, alpha=0.5)

    plt.tight_layout()

    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"[OK] Experimental signatures diagram saved to: {output_path}")
    plt.close()


def main():
    """Generate all theory overview diagrams."""
    # Get output directory (relative to this script)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    images_dir = os.path.join(script_dir, '..', '..', 'images')

    print("\n" + "="*70)
    print(" THEORY OVERVIEW DIAGRAMS GENERATOR")
    print("="*70)

    # Generate parameter space diagram
    print("\n[1/2] Generating parameter space diagram...")
    param_path = os.path.join(images_dir, 'parameter-space.png')
    generate_parameter_space_diagram(param_path)

    # Generate experimental signatures diagram
    print("\n[2/2] Generating experimental signatures diagram...")
    exp_path = os.path.join(images_dir, 'experimental-signatures.png')
    generate_experimental_signatures_diagram(exp_path)

    print("\n" + "="*70)
    print(" ALL DIAGRAMS GENERATED SUCCESSFULLY")
    print("="*70)
    print(f"\nOutput files:")
    print(f"  - {os.path.abspath(param_path)}")
    print(f"  - {os.path.abspath(exp_path)}")


if __name__ == "__main__":
    main()
