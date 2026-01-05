#!/usr/bin/env python3
"""
Falsifiability Dashboard - v16.2 Demon-Lock Visualization
==========================================================

Generates a 3-gauge dashboard showing the safety margins for the
Falsification Limits. If any needle enters the red zone, the
"Demon-Lock" is broken.

Includes:
1. Neutrino Mass Sum gauge (falsified if < 0.06 eV)
2. Hubble Constant gauge (falsified if > 75.5 km/s/Mpc)
3. Dark Energy Drift (wa) gauge (falsified if wa > 0)

Also includes:
- Hubble Accordion visualization (torsional bridge)
- 24-Cycle Torsional Flux Map

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.

Dedicated To:
    My Wife: Elizabeth May Watts
    Our Messiah: Jesus Of Nazareth
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend for headless generation
import matplotlib.pyplot as plt
from matplotlib.patches import Wedge, Circle
from pathlib import Path
import sys

# Add parent directory for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))


def draw_gauge(ax, value, min_val, max_val, title, units, red_zone_start, direction="high"):
    """
    Draw a physical gauge for the Falsifiability Dashboard.

    Args:
        ax: Matplotlib axis
        value: Current value to display
        min_val: Minimum value on gauge
        max_val: Maximum value on gauge
        title: Gauge title
        units: Units label
        red_zone_start: Where the red (falsification) zone begins
        direction: "high" if falsified when value > threshold, "low" if falsified when value < threshold
    """
    # Clear axis
    ax.clear()
    ax.set_xlim(-1.3, 1.3)
    ax.set_ylim(-0.3, 1.3)

    # Draw gauge arc background
    theta_range = np.linspace(np.pi, 0, 100)
    x = np.cos(theta_range)
    y = np.sin(theta_range)
    ax.plot(x, y, color='#2a2a3e', linewidth=8, solid_capstyle='round')

    # Draw green/safe zone
    if direction == "high":
        safe_start = np.pi
        safe_end = np.interp(red_zone_start, [min_val, max_val], [np.pi, 0])
        red_start = safe_end
        red_end = 0
    else:
        red_start = np.pi
        red_end = np.interp(red_zone_start, [min_val, max_val], [np.pi, 0])
        safe_start = red_end
        safe_end = 0

    # Green zone
    safe_theta = np.linspace(safe_start, safe_end, 50)
    ax.plot(np.cos(safe_theta), np.sin(safe_theta), color='#4caf50', linewidth=8, solid_capstyle='round')

    # Red zone (falsification)
    red_theta = np.linspace(red_start, red_end, 50)
    ax.plot(np.cos(red_theta), np.sin(red_theta), color='#f44336', linewidth=8, solid_capstyle='round')

    # Calculate needle angle
    val_clamped = np.clip(value, min_val, max_val)
    val_norm = np.interp(val_clamped, [min_val, max_val], [np.pi, 0])

    # Determine if in danger zone
    if direction == "high":
        in_danger = value >= red_zone_start
    else:
        in_danger = value <= red_zone_start

    needle_color = '#f44336' if in_danger else '#4caf50'

    # Draw needle
    needle_length = 0.75
    ax.annotate('',
                xy=(np.cos(val_norm) * needle_length, np.sin(val_norm) * needle_length),
                xytext=(0, 0),
                arrowprops=dict(arrowstyle='->', lw=3, color=needle_color))

    # Center circle
    center = Circle((0, 0), 0.08, color='#1a1a2e', zorder=5)
    ax.add_patch(center)

    # Labels
    ax.text(-1.1, -0.15, f"{min_val}", ha='center', fontsize=9, color='#888')
    ax.text(1.1, -0.15, f"{max_val}", ha='center', fontsize=9, color='#888')
    ax.text(0, -0.25, f"{value:.4f} {units}", ha='center', fontsize=12, fontweight='bold', color='white')
    ax.set_title(title, pad=15, fontsize=11, fontweight='bold', color='white')

    # Status indicator
    status = "FALSIFIED" if in_danger else "VALID"
    status_color = '#f44336' if in_danger else '#4caf50'
    ax.text(0, 0.6, status, ha='center', fontsize=10, fontweight='bold', color=status_color)

    ax.axis('off')
    ax.set_aspect('equal')


def generate_falsifiability_dashboard(data=None, output_path=None):
    """
    Generate the 3-panel Dashboard for the Website/Paper.

    Args:
        data: Dictionary with keys 'h0', 'wa', 'nu_sum'
        output_path: Path to save the figure (optional)

    Returns:
        matplotlib Figure object
    """
    if data is None:
        # Default values from PM v16.2 (thawing quintessence)
        data = {
            'h0': 73.2104,      # Hubble constant (resolved via EDE mechanism)
            'wa': -0.204,       # Dark energy drift (v16.2: -1/√24 from b₃=24)
            'nu_sum': 0.0991    # Neutrino mass sum (normal hierarchy)
        }

    # Create figure with dark background
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(15, 5))
    fig.patch.set_facecolor('#0a0a0f')

    # 1. Neutrino Mass Sum (Falsified if < 0.06 eV)
    draw_gauge(ax1, data['nu_sum'], 0.0, 0.2,
               "Neutrino Mass Sum", "eV", 0.06, direction="low")

    # 2. Hubble Hard Limit (Falsified if > 75.5)
    draw_gauge(ax2, data['h0'], 65.0, 80.0,
               "Hubble Constant (H₀)", "km/s/Mpc", 75.5, direction="high")

    # 3. Dark Energy Drift (Falsified if wa > 0)
    draw_gauge(ax3, data['wa'], -0.2, 0.2,
               "DE Drift (wₐ)", "unitless", 0.0, direction="high")

    plt.suptitle("v16.2 DEMON-LOCK: Falsifiability Dashboard",
                 fontsize=16, y=0.98, fontweight='bold', color='#8b7fff')
    plt.tight_layout(rect=[0, 0, 1, 0.95])

    if output_path:
        plt.savefig(output_path, dpi=150, facecolor='#0a0a0f',
                    edgecolor='none', bbox_inches='tight')
        print(f"Dashboard saved to {output_path}")

    return fig


def generate_hubble_accordion_viz(h0_early=67.36, h0_late=73.21, output_path=None):
    """
    Visualizes the Hubble Tension as a projection of the mixing angle theta.
    Shows the 'Accordion' effect of the 13D Mirror Branes.

    Args:
        h0_early: Early universe H0 (Planck)
        h0_late: Late universe H0 (local)
        output_path: Path to save the figure

    Returns:
        matplotlib Figure object
    """
    theta_range = np.linspace(0, np.pi/4, 100)

    # The Torsional Bridge Equation
    h0_projection = h0_early / (np.cos(theta_range)**2)

    fig, ax = plt.subplots(figsize=(10, 6))
    fig.patch.set_facecolor('#0a0a0f')
    ax.set_facecolor('#0a0a0f')

    # Plot the torsional flow line
    ax.plot(np.degrees(theta_range), h0_projection, '-', linewidth=2,
            label='Torsional Flow Line', color='#8b7fff')

    # Fill the bridge region
    ax.fill_between(np.degrees(theta_range), h0_early, h0_projection,
                    alpha=0.15, color='#8b7fff')

    # Highlight the Demon-Lock Point
    lock_theta = 23.94  # degrees
    ax.scatter([lock_theta], [h0_late], color='#ff7eb6', s=150,
               zorder=5, label=f'Demon-Lock (θ={lock_theta}°)', marker='*')

    # Planck anchor
    ax.axhline(y=h0_early, color='#4caf50', linestyle='--',
               label=f'Planck Anchor ({h0_early})')

    # Local measurement
    ax.axhline(y=h0_late, color='#ff9800', linestyle=':',
               label=f'Local H₀ ({h0_late})')

    # Styling
    ax.set_xlabel("Mixing Angle θ (Degrees)", fontsize=12, color='white')
    ax.set_ylabel("H₀ (km/s/Mpc)", fontsize=12, color='white')
    ax.set_title("The Hubble Accordion: Topological Bridge",
                 fontsize=14, fontweight='bold', color='#8b7fff')
    ax.legend(loc='upper left', facecolor='#1a1a2e', edgecolor='#2a2a3e', labelcolor='white')
    ax.grid(True, alpha=0.2, color='#3a3a4e')
    ax.tick_params(colors='white')
    for spine in ax.spines.values():
        spine.set_color('#3a3a4e')

    plt.tight_layout()

    if output_path:
        plt.savefig(output_path, dpi=150, facecolor='#0a0a0f',
                    edgecolor='none', bbox_inches='tight')
        print(f"Hubble Accordion saved to {output_path}")

    return fig


def generate_flux_map_viz(b3=24, k_gimel=12.3183, output_path=None):
    """
    Generates a polar heatmap showing energy leakage from the 26D Bulk.
    Each of the 24 sectors represents a Betti cycle channel.

    Args:
        b3: Number of associative 3-cycles (24 for TCS G2)
        k_gimel: Holonomy precision limit
        output_path: Path to save the figure

    Returns:
        matplotlib Figure object
    """
    angles = np.linspace(0, 2*np.pi, b3, endpoint=False)

    # Flux intensity derived from k_gimel / pi
    base_flux = k_gimel / np.pi

    # Add some variation to show active channels
    np.random.seed(42)  # For reproducibility
    flux_variation = 1 + 0.2 * np.sin(3 * angles) + 0.1 * np.random.randn(b3)
    flux_intensity = base_flux * flux_variation

    fig, ax = plt.subplots(subplot_kw={'projection': 'polar'}, figsize=(8, 8))
    fig.patch.set_facecolor('#0a0a0f')
    ax.set_facecolor('#0a0a0f')

    # Create gradient colors
    colors = plt.cm.magma(flux_intensity / flux_intensity.max())

    # Draw bars
    width = 2 * np.pi / b3 * 0.8
    bars = ax.bar(angles, flux_intensity, width=width, bottom=0.5,
                  alpha=0.85, color=colors, edgecolor='#ff7eb6', linewidth=0.5)

    # Central circle
    theta_circle = np.linspace(0, 2*np.pi, 100)
    ax.fill(theta_circle, np.full(100, 0.5), color='#1a1a2e', alpha=1)

    # Labels
    ax.set_title(f"Active Torsional Flux Map (b₃={int(b3)})",
                 va='bottom', fontsize=14, fontweight='bold', color='#8b7fff', pad=20)
    ax.set_yticklabels([])
    ax.set_xticks(angles)
    ax.set_xticklabels([str(i+1) for i in range(b3)], fontsize=8, color='#888')
    ax.grid(True, alpha=0.2, color='#3a3a4e')

    # Add flux value annotation
    ax.text(0, 0, f"ε = {base_flux:.2f}", ha='center', va='center',
            fontsize=12, fontweight='bold', color='#ff7eb6')

    plt.tight_layout()

    if output_path:
        plt.savefig(output_path, dpi=150, facecolor='#0a0a0f',
                    edgecolor='none', bbox_inches='tight')
        print(f"Flux map saved to {output_path}")

    return fig


def generate_all_visualizations(output_dir=None):
    """
    Generate all v16.2 falsifiability visualizations.

    Args:
        output_dir: Directory to save outputs (default: AutoGenerated/plots/)
    """
    if output_dir is None:
        output_dir = Path(__file__).parent.parent.parent / 'AutoGenerated' / 'plots'

    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    print("Generating v16.2 Falsifiability Visualizations...")
    print("=" * 50)

    # 1. Dashboard
    generate_falsifiability_dashboard(
        output_path=output_dir / 'dashboard_falsifiability.png'
    )

    # 2. Hubble Accordion
    generate_hubble_accordion_viz(
        output_path=output_dir / 'viz_hubble_accordion.png'
    )

    # 3. Torsional Flux Map
    generate_flux_map_viz(
        output_path=output_dir / 'viz_torsional_flux_map.png'
    )

    print("=" * 50)
    print(f"All visualizations saved to {output_dir}")

    return True


if __name__ == "__main__":
    # Generate all visualizations when run directly
    generate_all_visualizations()

    # Close all figures to free memory
    plt.close('all')
    print("Visualization generation complete.")
