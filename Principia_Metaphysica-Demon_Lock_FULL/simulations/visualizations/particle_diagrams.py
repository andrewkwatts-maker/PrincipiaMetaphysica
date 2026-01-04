#!/usr/bin/env python3
"""
Particle Physics Visualization Diagrams
=========================================

Licensed under the MIT License. See LICENSE file for details.

Generates publication-quality diagrams for particle physics concepts
in Principia Metaphysica:
1. standard-model-particles.png - Standard Model particle table with PM origins
2. yukawa-couplings.png - Yukawa coupling hierarchy from G2 geometry

Usage:
    python particle_diagrams.py

Output:
    ../../images/standard-model-particles.png
    ../../images/yukawa-couplings.png

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.

Dedicated To:
    My Wife: Elizabeth May Watts
    Our Messiah: Jesus Of Nazareth
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch
from pathlib import Path
import sys
import os

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

# PM Color Palette
PM_PURPLE = '#8b7fff'
PM_BLUE = '#60a5fa'  # Quarks
PM_GREEN = '#4ade80'  # Leptons
PM_ORANGE = '#fb923c'  # Gauge bosons
PM_RED = '#f87171'    # Higgs
PM_GRAY = '#9ca3af'   # Background
PM_DARK = '#1f2937'   # Text


def setup_publication_style():
    """Configure matplotlib for publication-quality figures."""
    plt.rcParams.update({
        'font.family': 'sans-serif',
        'font.sans-serif': ['Arial', 'DejaVu Sans', 'Helvetica'],
        'font.size': 10,
        'axes.titlesize': 14,
        'axes.labelsize': 12,
        'xtick.labelsize': 10,
        'ytick.labelsize': 10,
        'legend.fontsize': 10,
        'figure.titlesize': 16,
        'figure.dpi': 150,
        'savefig.dpi': 300,
        'savefig.bbox': 'tight',
        'savefig.pad_inches': 0.1,
        'axes.linewidth': 1.0,
        'axes.grid': False,
        'axes.facecolor': 'white',
        'figure.facecolor': 'white',
        'text.usetex': False,
    })


def create_standard_model_particles_diagram():
    """
    Generate Standard Model particle table with PM origins noted.

    Shows all SM particles organized by type (quarks, leptons, gauge bosons, Higgs)
    with annotations showing how each emerges from G2 geometry.
    """
    fig, ax = plt.subplots(figsize=(14, 10))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 10)
    ax.axis('off')

    # Title
    ax.text(7, 9.5, 'Standard Model Particles', fontsize=18, fontweight='bold',
            ha='center', va='center', color=PM_DARK)
    ax.text(7, 9.0, 'with Principia Metaphysica Origins', fontsize=12,
            ha='center', va='center', color=PM_PURPLE, style='italic')

    # Particle data: (symbol, name, mass, charge, spin, PM_origin)
    # Quarks - Generation 1
    quarks_gen1 = [
        ('u', 'up', '2.2 MeV', '+2/3', '1/2', 'Q_f=4'),
        ('d', 'down', '4.7 MeV', '-1/3', '1/2', 'Q_f=4'),
    ]
    # Quarks - Generation 2
    quarks_gen2 = [
        ('c', 'charm', '1.27 GeV', '+2/3', '1/2', 'Q_f=2'),
        ('s', 'strange', '93 MeV', '-1/3', '1/2', 'Q_f=3'),
    ]
    # Quarks - Generation 3
    quarks_gen3 = [
        ('t', 'top', '173 GeV', '+2/3', '1/2', 'Q_f=0'),
        ('b', 'bottom', '4.18 GeV', '-1/3', '1/2', 'Q_f=2'),
    ]

    # Leptons - Generation 1
    leptons_gen1 = [
        ('e', 'electron', '0.511 MeV', '-1', '1/2', 'Q_f=6'),
        (r'$\nu_e$', 'e-neutrino', '<1 eV', '0', '1/2', 'Majorana'),
    ]
    # Leptons - Generation 2
    leptons_gen2 = [
        (r'$\mu$', 'muon', '106 MeV', '-1', '1/2', 'Q_f=4'),
        (r'$\nu_\mu$', 'mu-neutrino', '<0.2 MeV', '0', '1/2', 'Majorana'),
    ]
    # Leptons - Generation 3
    leptons_gen3 = [
        (r'$\tau$', 'tau', '1.78 GeV', '-1', '1/2', 'Q_f=2'),
        (r'$\nu_\tau$', 'nu-tau', '<18 MeV', '0', '1/2', 'Majorana'),
    ]

    # Gauge bosons
    gauge_bosons = [
        (r'$\gamma$', 'photon', '0', '0', '1', 'U(1)_Y'),
        ('W', 'W boson', '80.4 GeV', r'$\pm$1', '1', 'SU(2)_L'),
        ('Z', 'Z boson', '91.2 GeV', '0', '1', 'SU(2)_L'),
        ('g', 'gluon', '0', '0', '1', 'SU(3)_c'),
    ]

    # Higgs
    higgs = [
        ('H', 'Higgs', '125 GeV', '0', '0', 'Moduli'),
    ]

    def draw_particle_box(ax, x, y, symbol, name, mass, charge, spin, pm_origin, color, width=1.8, height=1.3):
        """Draw a single particle box."""
        box = FancyBboxPatch((x - width/2, y - height/2), width, height,
                              boxstyle="round,pad=0.02,rounding_size=0.1",
                              facecolor=color, edgecolor=PM_DARK, linewidth=1.5, alpha=0.9)
        ax.add_patch(box)

        # Symbol (large)
        ax.text(x, y + 0.35, symbol, fontsize=20, fontweight='bold',
                ha='center', va='center', color='white')

        # Name (small)
        ax.text(x, y - 0.05, name, fontsize=8, ha='center', va='center', color='white')

        # Mass (very small)
        ax.text(x, y - 0.35, mass, fontsize=7, ha='center', va='center', color='white', alpha=0.9)

        # PM origin annotation (bottom right corner)
        ax.text(x + width/2 - 0.05, y - height/2 + 0.1, pm_origin, fontsize=6,
                ha='right', va='bottom', color=PM_PURPLE, fontweight='bold',
                bbox=dict(boxstyle='round,pad=0.1', facecolor='white', alpha=0.8, edgecolor='none'))

    # Draw generation labels
    ax.text(2.5, 8.2, '1st Gen', fontsize=11, fontweight='bold', ha='center', color=PM_DARK)
    ax.text(5.0, 8.2, '2nd Gen', fontsize=11, fontweight='bold', ha='center', color=PM_DARK)
    ax.text(7.5, 8.2, '3rd Gen', fontsize=11, fontweight='bold', ha='center', color=PM_DARK)

    # Draw section labels
    ax.text(0.5, 7.0, 'QUARKS', fontsize=10, fontweight='bold', ha='left', va='center',
            color=PM_BLUE, rotation=90)
    ax.text(0.5, 4.0, 'LEPTONS', fontsize=10, fontweight='bold', ha='left', va='center',
            color=PM_GREEN, rotation=90)
    ax.text(11.0, 5.5, 'GAUGE\nBOSONS', fontsize=10, fontweight='bold', ha='center', va='center',
            color=PM_ORANGE)
    ax.text(13.0, 2.5, 'SCALAR', fontsize=10, fontweight='bold', ha='center', va='center',
            color=PM_RED)

    # Draw quarks
    y_up = 7.5
    y_down = 6.0
    for i, (gen1, gen2, gen3) in enumerate([(quarks_gen1[0], quarks_gen2[0], quarks_gen3[0]),
                                             (quarks_gen1[1], quarks_gen2[1], quarks_gen3[1])]):
        y = y_up if i == 0 else y_down
        draw_particle_box(ax, 2.5, y, *gen1, PM_BLUE)
        draw_particle_box(ax, 5.0, y, *gen2, PM_BLUE)
        draw_particle_box(ax, 7.5, y, *gen3, PM_BLUE)

    # Draw leptons
    y_charged = 4.5
    y_neutrino = 3.0
    for i, (gen1, gen2, gen3) in enumerate([(leptons_gen1[0], leptons_gen2[0], leptons_gen3[0]),
                                             (leptons_gen1[1], leptons_gen2[1], leptons_gen3[1])]):
        y = y_charged if i == 0 else y_neutrino
        draw_particle_box(ax, 2.5, y, *gen1, PM_GREEN)
        draw_particle_box(ax, 5.0, y, *gen2, PM_GREEN)
        draw_particle_box(ax, 7.5, y, *gen3, PM_GREEN)

    # Draw gauge bosons
    gauge_positions = [(10.5, 7.5), (10.5, 6.0), (10.5, 4.5), (10.5, 3.0)]
    for pos, boson in zip(gauge_positions, gauge_bosons):
        draw_particle_box(ax, pos[0], pos[1], *boson, PM_ORANGE)

    # Draw Higgs
    draw_particle_box(ax, 13.0, 5.5, *higgs[0], PM_RED, width=1.8, height=1.5)

    # Draw PM mechanism explanations
    explanations = [
        (2.5, 1.2, r'$n_{gen} = \frac{b_3}{\mathrm{spinor\ DOF}} = \frac{24}{8} = 3$', 'Generation count from G2 topology'),
        (7.5, 1.2, r'$Y_f = A_f \cdot \epsilon^{Q_f}$, $\epsilon = e^{-1.5} \approx 0.223$', 'Yukawa hierarchy from Froggatt-Nielsen'),
        (12.0, 1.2, r'Gauge group: $SO(10) \subset SO(24,2)$', 'Bulk symmetry reduction via G2'),
    ]

    for x, y, formula, label in explanations:
        ax.text(x, y, formula, fontsize=9, ha='center', va='center', color=PM_PURPLE,
                bbox=dict(boxstyle='round,pad=0.2', facecolor='#f3f0ff', edgecolor=PM_PURPLE, alpha=0.9))
        ax.text(x, y - 0.5, label, fontsize=7, ha='center', va='center', color=PM_DARK, style='italic')

    # Legend for Q_f values
    ax.text(9.5, 0.5, 'PM Key:', fontsize=9, fontweight='bold', ha='left', color=PM_DARK)
    ax.text(10.5, 0.5, r'$Q_f$ = Topological distance (graph hops) from Higgs cycle',
            fontsize=8, ha='left', color=PM_GRAY)

    return fig


def create_yukawa_couplings_diagram():
    """
    Generate Yukawa coupling hierarchy diagram from G2 geometry.

    Shows how the mass hierarchy emerges from topological distances
    in the G2 manifold cycle graph.
    """
    fig, axes = plt.subplots(1, 2, figsize=(14, 8))

    # === Left panel: Mass hierarchy bar chart ===
    ax1 = axes[0]

    # Fermion data from simulations
    fermions = {
        'Quarks': {
            'up': (2.2e-3, 4, PM_BLUE),
            'down': (4.7e-3, 4, PM_BLUE),
            'strange': (0.093, 3, PM_BLUE),
            'charm': (1.27, 2, PM_BLUE),
            'bottom': (4.18, 2, PM_BLUE),
            'top': (172.7, 0, PM_BLUE),
        },
        'Leptons': {
            'electron': (0.000511, 6, PM_GREEN),
            'muon': (0.1057, 4, PM_GREEN),
            'tau': (1.777, 2, PM_GREEN),
        }
    }

    # Prepare data for bar chart
    all_particles = []
    all_masses = []
    all_colors = []
    all_Q_f = []

    for category, particles in fermions.items():
        for name, (mass, Q_f, color) in sorted(particles.items(), key=lambda x: x[1][0]):
            all_particles.append(name)
            all_masses.append(mass)
            all_colors.append(color)
            all_Q_f.append(Q_f)

    # Sort by mass
    sorted_indices = np.argsort(all_masses)
    all_particles = [all_particles[i] for i in sorted_indices]
    all_masses = [all_masses[i] for i in sorted_indices]
    all_colors = [all_colors[i] for i in sorted_indices]
    all_Q_f = [all_Q_f[i] for i in sorted_indices]

    y_pos = np.arange(len(all_particles))
    bars = ax1.barh(y_pos, np.log10(np.array(all_masses) * 1000), color=all_colors, alpha=0.8)

    ax1.set_yticks(y_pos)
    ax1.set_yticklabels([f'{p} ($Q_f$={q})' for p, q in zip(all_particles, all_Q_f)])
    ax1.set_xlabel('log$_{10}$(mass / MeV)', fontsize=12)
    ax1.set_title('Fermion Mass Hierarchy', fontsize=14, fontweight='bold', color=PM_DARK)

    # Add mass values as text
    for i, (bar, mass) in enumerate(zip(bars, all_masses)):
        if mass >= 1:
            label = f'{mass:.2f} GeV'
        else:
            label = f'{mass*1000:.2f} MeV'
        ax1.text(bar.get_width() + 0.1, bar.get_y() + bar.get_height()/2,
                 label, va='center', fontsize=8, color=PM_DARK)

    ax1.set_xlim(-1, 6.5)
    ax1.axvline(x=0, color=PM_GRAY, linestyle='--', alpha=0.5)

    # Add legend for colors
    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor=PM_BLUE, alpha=0.8, label='Quarks'),
        Patch(facecolor=PM_GREEN, alpha=0.8, label='Leptons'),
    ]
    ax1.legend(handles=legend_elements, loc='lower right')

    # === Right panel: G2 cycle graph with Froggatt-Nielsen ===
    ax2 = axes[1]
    ax2.set_xlim(-1.5, 1.5)
    ax2.set_ylim(-1.5, 1.5)
    ax2.set_aspect('equal')
    ax2.axis('off')

    ax2.set_title('G2 Cycle Graph: Froggatt-Nielsen Mechanism', fontsize=14,
                  fontweight='bold', color=PM_DARK)

    # Draw Higgs at center
    higgs_circle = plt.Circle((0, 0), 0.15, facecolor=PM_RED, edgecolor=PM_DARK, linewidth=2)
    ax2.add_patch(higgs_circle)
    ax2.text(0, 0, 'H', fontsize=14, fontweight='bold', ha='center', va='center', color='white')
    ax2.text(0, -0.25, 'Higgs\n$Q_f=0$', fontsize=8, ha='center', va='top', color=PM_DARK)

    # Draw concentric rings for topological distance
    for Q_f in [2, 4, 6]:
        radius = Q_f * 0.18 + 0.2
        ring = plt.Circle((0, 0), radius, fill=False, edgecolor=PM_PURPLE,
                          linestyle='--', alpha=0.5, linewidth=1)
        ax2.add_patch(ring)
        ax2.text(radius + 0.05, 0.05, f'$Q_f={Q_f}$', fontsize=8, color=PM_PURPLE, alpha=0.7)

    # Place fermions on the graph based on Q_f
    fermion_positions = {
        # Q_f = 0 (at Higgs): top
        'top': (0.3, 0.15, 0, PM_BLUE),
        # Q_f = 2: inner ring
        'charm': (-0.4, 0.4, 2, PM_BLUE),
        'bottom': (0.4, 0.4, 2, PM_BLUE),
        'tau': (0, 0.55, 2, PM_GREEN),
        # Q_f = 3
        'strange': (-0.65, 0.2, 3, PM_BLUE),
        # Q_f = 4: middle ring
        'up': (-0.8, -0.4, 4, PM_BLUE),
        'down': (-0.4, -0.7, 4, PM_BLUE),
        'muon': (0.6, -0.55, 4, PM_GREEN),
        # Q_f = 6: outer ring
        'electron': (0.2, -1.1, 6, PM_GREEN),
    }

    for name, (x, y, Q_f, color) in fermion_positions.items():
        circle = plt.Circle((x, y), 0.1, facecolor=color, edgecolor=PM_DARK, linewidth=1.5, alpha=0.9)
        ax2.add_patch(circle)
        ax2.text(x, y, name[0].upper(), fontsize=10, fontweight='bold',
                ha='center', va='center', color='white')

        # Draw connection to Higgs (suppression path)
        ax2.plot([0, x], [0, y], color=PM_GRAY, linestyle=':', alpha=0.4, linewidth=1)

    # Add Froggatt-Nielsen formula
    ax2.text(0, -1.4, r'$Y_f = A_f \cdot \epsilon^{Q_f}$', fontsize=14, ha='center',
             va='center', color=PM_PURPLE, fontweight='bold')
    ax2.text(0, -1.55, r'$\epsilon = e^{-\lambda} = e^{-1.5} \approx 0.223$ (Cabibbo angle)',
             fontsize=10, ha='center', va='center', color=PM_DARK)

    # Add explanation box
    explanation = (
        "Yukawa Hierarchy from G2 Geometry:\n"
        "- Fermions localize on associative 3-cycles\n"
        "- Topological distance $Q_f$ = graph hops from Higgs\n"
        "- Each hop suppresses coupling by $\\epsilon \\approx 0.223$\n"
        "- Result: $m_t / m_e \\sim \\epsilon^{-6} \\approx 10^5$"
    )
    ax2.text(1.0, 1.2, explanation, fontsize=9, ha='left', va='top', color=PM_DARK,
             bbox=dict(boxstyle='round,pad=0.3', facecolor='#f8fafc', edgecolor=PM_PURPLE, alpha=0.9),
             linespacing=1.5)

    plt.tight_layout()
    return fig


def main():
    """Generate all particle physics diagrams."""
    # Setup style
    setup_publication_style()

    # Output directory
    output_dir = Path(__file__).parent.parent.parent / 'images'
    output_dir.mkdir(parents=True, exist_ok=True)

    print("=" * 70)
    print(" PARTICLE PHYSICS VISUALIZATION DIAGRAMS")
    print("=" * 70)
    print()

    # Generate Standard Model particles diagram
    print("Generating standard-model-particles.png...")
    fig1 = create_standard_model_particles_diagram()
    output_path1 = output_dir / 'standard-model-particles.png'
    fig1.savefig(output_path1, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close(fig1)
    print(f"  Saved to: {output_path1}")

    # Generate Yukawa couplings diagram
    print("Generating yukawa-couplings.png...")
    fig2 = create_yukawa_couplings_diagram()
    output_path2 = output_dir / 'yukawa-couplings.png'
    fig2.savefig(output_path2, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close(fig2)
    print(f"  Saved to: {output_path2}")

    print()
    print("=" * 70)
    print(" PARTICLE DIAGRAMS COMPLETE")
    print("=" * 70)

    return [output_path1, output_path2]


if __name__ == "__main__":
    main()
