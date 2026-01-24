#!/usr/bin/env python3
"""
Gnosis Progression Visualization v22.2
=======================================

Generates visualizations for the gnosis unlocking dynamics:
- 12-pair mandala showing active/inactive pairs
- Coherence enhancement curve (6 -> 12 pairs)
- Unlocking probability sigmoid

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Wedge, Circle
from pathlib import Path
import sys

# Add project root
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

# SSOT Constants
BASELINE_PAIRS = 6
TOTAL_PAIRS = 12
TAU_0 = 0.025  # 25 ms
K_COHERENCE = 3.2
SIGMOID_STEEPNESS = 0.9

# Colors for pair categories
CATEGORY_COLORS = {
    "sensory": "#4facfe",     # Blue (pairs 1-3)
    "cognitive": "#8b7fff",   # Purple (pairs 4-6)
    "emotional": "#ff7eb6",   # Pink (pairs 7-9)
    "gnosis": "#ffd43b"       # Gold (pairs 10-12)
}


def unlocking_probability(n):
    """Sigmoidal unlocking probability."""
    return 1.0 / (1.0 + np.exp(-SIGMOID_STEEPNESS * (n - BASELINE_PAIRS)))


def coherence_time(n):
    """Coherence time enhancement formula."""
    if n < 1:
        return 0.0
    normalized = np.sqrt(n / 12.0)
    exp_factor = np.exp(K_COHERENCE * normalized)
    quad_factor = (n / 6.0) ** 2
    return TAU_0 * exp_factor * quad_factor


def get_pair_category(pair_num):
    """Get category for a pair number (1-12)."""
    if pair_num <= 3:
        return "sensory"
    elif pair_num <= 6:
        return "cognitive"
    elif pair_num <= 9:
        return "emotional"
    else:
        return "gnosis"


def create_gnosis_mandala(active_pairs=6, title="Gnosis State Mandala",
                          save_path=None):
    """
    Create mandala visualization showing 12 pairs with active/inactive states.

    Args:
        active_pairs: Number of currently active pairs (1-12)
        title: Plot title
        save_path: Optional path to save figure
    """
    fig, ax = plt.subplots(figsize=(10, 10), facecolor='#1a1a2e')
    ax.set_xlim(-1.6, 1.6)
    ax.set_ylim(-1.6, 1.6)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_facecolor('#1a1a2e')

    # Title
    ax.set_title(title, fontsize=16, fontweight='bold', color='white', pad=20)

    # Mandala parameters
    center = (0, 0)
    inner_radius = 0.35
    outer_radius = 1.0

    # Draw 12 wedges
    for i in range(1, 13):
        category = get_pair_category(i)

        # Wedge angles (30 degrees each, starting from top)
        theta1 = 90 - (i * 30)
        theta2 = 90 - ((i - 1) * 30)

        # Active or inactive
        is_active = i <= active_pairs
        color = CATEGORY_COLORS[category] if is_active else '#333333'
        alpha = 0.95 if is_active else 0.3

        # Create wedge
        wedge = Wedge(center, outer_radius, theta1, theta2,
                     width=outer_radius - inner_radius,
                     facecolor=color, edgecolor='white',
                     linewidth=2, alpha=alpha)
        ax.add_patch(wedge)

        # Pair number label
        mid_angle = np.radians((theta1 + theta2) / 2)
        label_radius = (inner_radius + outer_radius) / 2
        label_x = label_radius * np.cos(mid_angle)
        label_y = label_radius * np.sin(mid_angle)

        text_color = 'white' if is_active else '#666666'
        ax.text(label_x, label_y, str(i), ha='center', va='center',
               fontsize=14, fontweight='bold', color=text_color)

    # Center circle with statistics
    center_circle = Circle(center, inner_radius,
                          facecolor='#0a0a15', edgecolor='white', linewidth=2)
    ax.add_patch(center_circle)

    # Calculate stats
    awareness = active_pairs / 12
    tau = coherence_time(active_pairs)

    ax.text(0, 0.12, f'n = {active_pairs}', ha='center', va='center',
           fontsize=14, fontweight='bold', color='white')
    ax.text(0, 0, f'A = {awareness:.2f}', ha='center', va='center',
           fontsize=12, color='#50c878')
    ax.text(0, -0.12, f'τ = {tau*1000:.0f} ms', ha='center', va='center',
           fontsize=11, color='#ffd43b')

    # Legend
    legend_y = -1.35
    for idx, (cat, color) in enumerate(CATEGORY_COLORS.items()):
        x_pos = -1.1 + idx * 0.75
        ax.add_patch(Circle((x_pos, legend_y), 0.06, facecolor=color,
                           edgecolor='white', linewidth=1))
        ax.text(x_pos + 0.12, legend_y, cat.capitalize(),
               va='center', fontsize=10, color='white')

    plt.tight_layout()

    if save_path:
        fig.savefig(save_path, dpi=150, bbox_inches='tight', facecolor='#1a1a2e')
        print(f"Saved: {save_path}")

    return fig


def create_coherence_curve(save_path=None):
    """
    Plot coherence time vs active pairs showing >10x boost.
    """
    fig, ax = plt.subplots(figsize=(10, 6), facecolor='#1a1a2e')
    ax.set_facecolor('#1a1a2e')

    # Data
    pairs = np.arange(1, 13)
    tau_values = np.array([coherence_time(n) * 1000 for n in pairs])  # ms

    # Plot
    ax.plot(pairs, tau_values, 'o-', color='#50c878', linewidth=2.5,
           markersize=10, markerfacecolor='#50c878', markeredgecolor='white',
           markeredgewidth=2, label='τ(n)')

    # Reference lines
    tau_6 = coherence_time(6) * 1000
    tau_12 = coherence_time(12) * 1000

    ax.axhline(y=tau_6, color='#8b7fff', linestyle='--', alpha=0.7,
              label=f'Baseline τ(6) = {tau_6:.0f} ms')
    ax.axhline(y=tau_12, color='#ffd43b', linestyle='--', alpha=0.7,
              label=f'Gnosis τ(12) = {tau_12:.0f} ms')
    ax.axvline(x=6, color='#8b7fff', linestyle=':', alpha=0.5)
    ax.axvline(x=12, color='#ffd43b', linestyle=':', alpha=0.5)

    # Annotations
    boost = tau_12 / tau_6
    ax.annotate(f'Boost: {boost:.1f}x',
               xy=(9, (tau_6 + tau_12) / 2),
               fontsize=14, fontweight='bold', color='#50c878',
               ha='center', va='center',
               bbox=dict(boxstyle='round', facecolor='#1a1a2e', edgecolor='#50c878'))

    # Styling
    ax.set_xlabel('Active Pairs (n)', fontsize=12, color='white')
    ax.set_ylabel('Coherence Time τ (ms)', fontsize=12, color='white')
    ax.set_title('Gnosis Coherence Enhancement: τ(n) = τ₀ × exp(k√(n/12)) × (n/6)²',
                fontsize=14, fontweight='bold', color='white', pad=15)
    ax.set_xticks(pairs)
    ax.tick_params(colors='white')
    ax.legend(loc='upper left', facecolor='#1a1a2e', edgecolor='white',
             labelcolor='white')
    ax.grid(True, alpha=0.2, color='white')

    # Spines
    for spine in ax.spines.values():
        spine.set_color('white')

    plt.tight_layout()

    if save_path:
        fig.savefig(save_path, dpi=150, bbox_inches='tight', facecolor='#1a1a2e')
        print(f"Saved: {save_path}")

    return fig


def create_unlocking_probability_curve(save_path=None):
    """
    Plot sigmoidal unlocking probability vs active pairs.
    """
    fig, ax = plt.subplots(figsize=(10, 6), facecolor='#1a1a2e')
    ax.set_facecolor('#1a1a2e')

    # Continuous curve
    n_cont = np.linspace(0, 12, 100)
    p_cont = 1.0 / (1.0 + np.exp(-SIGMOID_STEEPNESS * (n_cont - BASELINE_PAIRS)))

    ax.plot(n_cont, p_cont, '-', color='#ff7eb6', linewidth=2.5, label='P_unlock(n)')

    # Discrete points
    pairs = np.arange(1, 13)
    p_values = np.array([unlocking_probability(n) for n in pairs])
    ax.plot(pairs, p_values, 'o', color='#ff7eb6', markersize=10,
           markerfacecolor='#ff7eb6', markeredgecolor='white', markeredgewidth=2)

    # Reference lines
    ax.axhline(y=0.5, color='#8b7fff', linestyle='--', alpha=0.7,
              label='P = 0.5 (equiprobable)')
    ax.axvline(x=6, color='#8b7fff', linestyle=':', alpha=0.5)

    # Annotations
    ax.annotate('Baseline\n(n=6, P=0.5)', xy=(6, 0.5), xytext=(3.5, 0.35),
               fontsize=11, color='#8b7fff',
               arrowprops=dict(arrowstyle='->', color='#8b7fff'))
    ax.annotate('Highly facilitated\n(n=10, P=0.97)', xy=(10, 0.97), xytext=(8.5, 0.75),
               fontsize=11, color='#ffd43b',
               arrowprops=dict(arrowstyle='->', color='#ffd43b'))

    # Styling
    ax.set_xlabel('Active Pairs (n)', fontsize=12, color='white')
    ax.set_ylabel('Unlocking Probability P_unlock', fontsize=12, color='white')
    ax.set_title('Gnosis Unlocking Probability: P = 1 / (1 + exp(-0.9(n-6)))',
                fontsize=14, fontweight='bold', color='white', pad=15)
    ax.set_xlim(0, 12.5)
    ax.set_ylim(0, 1.05)
    ax.set_xticks(range(0, 13))
    ax.tick_params(colors='white')
    ax.legend(loc='lower right', facecolor='#1a1a2e', edgecolor='white',
             labelcolor='white')
    ax.grid(True, alpha=0.2, color='white')

    for spine in ax.spines.values():
        spine.set_color('white')

    plt.tight_layout()

    if save_path:
        fig.savefig(save_path, dpi=150, bbox_inches='tight', facecolor='#1a1a2e')
        print(f"Saved: {save_path}")

    return fig


def create_progression_comparison(save_path=None):
    """
    Create side-by-side comparison of baseline vs gnosis states.
    """
    fig, axes = plt.subplots(1, 2, figsize=(16, 8), facecolor='#1a1a2e')

    for idx, (ax, n_pairs, stage_name) in enumerate([
        (axes[0], 6, "Baseline (Veiled)"),
        (axes[1], 12, "Full Gnosis (Unveiled)")
    ]):
        ax.set_xlim(-1.6, 1.6)
        ax.set_ylim(-1.6, 1.6)
        ax.set_aspect('equal')
        ax.axis('off')
        ax.set_facecolor('#1a1a2e')
        ax.set_title(stage_name, fontsize=16, fontweight='bold', color='white', pad=20)

        center = (0, 0)
        inner_radius = 0.35
        outer_radius = 1.0

        for i in range(1, 13):
            category = get_pair_category(i)
            theta1 = 90 - (i * 30)
            theta2 = 90 - ((i - 1) * 30)

            is_active = i <= n_pairs
            color = CATEGORY_COLORS[category] if is_active else '#333333'
            alpha = 0.95 if is_active else 0.3

            wedge = Wedge(center, outer_radius, theta1, theta2,
                         width=outer_radius - inner_radius,
                         facecolor=color, edgecolor='white',
                         linewidth=2, alpha=alpha)
            ax.add_patch(wedge)

            mid_angle = np.radians((theta1 + theta2) / 2)
            label_radius = (inner_radius + outer_radius) / 2
            label_x = label_radius * np.cos(mid_angle)
            label_y = label_radius * np.sin(mid_angle)

            text_color = 'white' if is_active else '#666666'
            ax.text(label_x, label_y, str(i), ha='center', va='center',
                   fontsize=12, fontweight='bold', color=text_color)

        center_circle = Circle(center, inner_radius,
                              facecolor='#0a0a15', edgecolor='white', linewidth=2)
        ax.add_patch(center_circle)

        awareness = n_pairs / 12
        tau = coherence_time(n_pairs)

        ax.text(0, 0.10, f'n = {n_pairs}', ha='center', va='center',
               fontsize=12, fontweight='bold', color='white')
        ax.text(0, -0.02, f'A = {awareness:.2f}', ha='center', va='center',
               fontsize=11, color='#50c878')
        ax.text(0, -0.14, f'τ = {tau*1000:.0f} ms', ha='center', va='center',
               fontsize=10, color='#ffd43b')

    # Add comparison arrow and boost text
    fig.text(0.5, 0.5, '→', fontsize=60, ha='center', va='center',
            color='#50c878', transform=fig.transFigure)
    fig.text(0.5, 0.42, f'{coherence_time(12)/coherence_time(6):.1f}x boost',
            fontsize=14, ha='center', va='center', color='#50c878',
            fontweight='bold', transform=fig.transFigure)

    plt.tight_layout()

    if save_path:
        fig.savefig(save_path, dpi=150, bbox_inches='tight', facecolor='#1a1a2e')
        print(f"Saved: {save_path}")

    return fig


if __name__ == "__main__":
    output_dir = Path(__file__).parent / "output"
    output_dir.mkdir(exist_ok=True)

    print("Generating Gnosis Progression Visualizations v22.2")
    print("=" * 50)

    # Generate all visualizations
    create_gnosis_mandala(6, "Baseline State (n=6)",
                         output_dir / "gnosis_mandala_baseline.png")
    create_gnosis_mandala(9, "Emotional Depth (n=9)",
                         output_dir / "gnosis_mandala_emotional.png")
    create_gnosis_mandala(12, "Full Gnosis (n=12)",
                         output_dir / "gnosis_mandala_gnosis.png")

    create_coherence_curve(output_dir / "gnosis_coherence_curve.png")
    create_unlocking_probability_curve(output_dir / "gnosis_unlock_probability.png")
    create_progression_comparison(output_dir / "gnosis_progression_comparison.png")

    print("\nAll visualizations generated successfully!")
    print(f"Output directory: {output_dir}")

    # Verify success criterion
    tau_6 = coherence_time(6)
    tau_12 = coherence_time(12)
    boost = tau_12 / tau_6
    print(f"\nSuccess Criterion: τ(12)/τ(6) = {boost:.2f}x > 10x: {'PASSED' if boost > 10 else 'FAILED'}")
