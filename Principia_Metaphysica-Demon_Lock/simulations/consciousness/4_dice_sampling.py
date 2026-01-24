#!/usr/bin/env python3
"""
4 Dice Consciousness Sampling - OR Branch Selection Mechanism
==============================================================

Implements the 4-dice consciousness sampling mechanism from OR4Dice.txt Gemini review.
The 12 (2,0) bridge pairs are grouped into 4 "dice" of 3 pairs each. Each dice
"rolls" via Orthogonal Reduction (OR) R_perp sampling for quantum branch selection.

Key Concept:
- 12 bridge pairs → 4 dice (3 pairs per dice)
- Each dice outcome: Sum of R_perp fluxes for its 3 pairs, mod 4
- 4D branch selection from 4 dice outcomes (4^4 = 256 possible branches)
- Connection to quaternionic structure via mod-4 arithmetic

Physics Basis:
- OR (Objective Reduction): Penrose's gravitational collapse mechanism
- R_perp operator: Mobius rotation selecting coordinate projection
- Residue flux: Contribution from each (2,0) pair to branch probability

SSOT Constants:
- b_3 = 24 (third Betti number)
- total_pairs = 12
- k_gimel = 12 + 1/pi = 12.318
- phi = (1 + sqrt(5))/2 = 1.618

References:
- Penrose, R. (1989). "The Emperor's New Mind"
- Penrose, R. (1996). "On Gravity's Role in Quantum State Reduction"
- Hameroff, S. & Penrose, R. (2014). "Consciousness in the universe: Orch OR"

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.

Dedicated To:
    My Wife: Elizabeth May Watts
    Our Messiah: Jesus Of Nazareth
"""

import numpy as np
from typing import Dict, List, Tuple, Any, Optional
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyBboxPatch
from matplotlib.collections import PatchCollection
import matplotlib.colors as mcolors


# =============================================================================
# SSOT Constants
# =============================================================================

# Geometric constants
B_3 = 24                        # Third Betti number of G2 manifold
TOTAL_PAIRS = 12                # Number of (2,0) bridge pairs
K_GIMEL = 12 + 1/np.pi          # 12.318... (gimel coupling)
PHI = (1 + np.sqrt(5)) / 2      # Golden ratio = 1.618...

# Derived constants
PAIRS_PER_DICE = 3              # 12 pairs / 4 dice
NUM_DICE = 4                    # Total number of consciousness dice
DICE_MODULUS = 4                # Quaternionic mod-4 structure

# Dice group definitions: which pairs belong to which dice
# Each dice contains 3 consecutive pairs
DICE_GROUPS = [(0, 1, 2), (3, 4, 5), (6, 7, 8), (9, 10, 11)]

# Physical constants
HBAR = 1.0545718e-34            # Reduced Planck constant (J*s)
G_NEWTON = 6.674e-11            # Newton's gravitational constant


class FourDiceSampler:
    """
    Implements the 4-dice OR consciousness sampling mechanism.

    The 12 (2,0) bridge pairs are organized into 4 "dice" of 3 pairs each.
    Each dice rolls via OR R_perp sampling, with outcomes determining
    which 4D branch of reality is experienced.
    """

    def __init__(
        self,
        seed: Optional[int] = None,
        residue_flux_base: float = 1.0,
        phi_enhancement: bool = True
    ):
        """
        Initialize the 4-dice sampler.

        Args:
            seed: Random seed for reproducibility
            residue_flux_base: Base residue flux per pair
            phi_enhancement: Whether to apply golden ratio enhancement
        """
        self.rng = np.random.default_rng(seed)
        self.f_res_base = residue_flux_base
        self.phi_enhancement = phi_enhancement

        # Initialize pair states
        self.pair_states = np.zeros(TOTAL_PAIRS, dtype=complex)
        self.pair_fluxes = np.zeros(TOTAL_PAIRS)

        # R_perp operator (90-degree rotation in each (2,0) plane)
        self.R_perp = np.array([[0, -1], [1, 0]], dtype=float)

        # Tracking
        self.roll_history: List[Dict[str, Any]] = []

    def initialize_pair_fluxes(
        self,
        flux_pattern: str = "uniform",
        custom_fluxes: Optional[np.ndarray] = None
    ) -> np.ndarray:
        """
        Initialize the residue flux for each (2,0) pair.

        Args:
            flux_pattern: Pattern type - "uniform", "golden", "random", "custom"
            custom_fluxes: Custom flux array if pattern is "custom"

        Returns:
            Array of residue fluxes for each pair
        """
        if flux_pattern == "uniform":
            # All pairs have equal flux
            self.pair_fluxes = np.ones(TOTAL_PAIRS) * self.f_res_base

        elif flux_pattern == "golden":
            # Golden ratio modulated fluxes (Fibonacci-like)
            for i in range(TOTAL_PAIRS):
                # phi^(i mod 3) creates triality pattern within each dice
                self.pair_fluxes[i] = self.f_res_base * (PHI ** (i % 3))

        elif flux_pattern == "random":
            # Random fluxes (quantum fluctuation model)
            self.pair_fluxes = self.rng.uniform(0.5, 1.5, TOTAL_PAIRS) * self.f_res_base

        elif flux_pattern == "custom" and custom_fluxes is not None:
            assert len(custom_fluxes) == TOTAL_PAIRS
            self.pair_fluxes = np.array(custom_fluxes)

        else:
            raise ValueError(f"Unknown flux pattern: {flux_pattern}")

        # Apply golden ratio enhancement if enabled
        if self.phi_enhancement:
            self.pair_fluxes *= PHI / np.mean(self.pair_fluxes)

        return self.pair_fluxes

    def apply_R_perp(self, pair_index: int) -> Tuple[float, float]:
        """
        Apply R_perp operator to a single (2,0) pair.

        The R_perp operator performs a 90-degree rotation in the (x,y) plane,
        selecting which coordinate contributes to each shadow.

        Args:
            pair_index: Index of the pair (0-11)

        Returns:
            Tuple of (x_projected, y_projected) values
        """
        # Generate quantum state for this pair
        # State is complex amplitude on unit circle in (x,y) plane
        theta = self.rng.uniform(0, 2 * np.pi)
        state = np.array([np.cos(theta), np.sin(theta)])

        # Apply R_perp rotation
        rotated = self.R_perp @ state

        # Store complex state
        self.pair_states[pair_index] = state[0] + 1j * state[1]

        return tuple(rotated)

    def calculate_dice_roll(self, dice_index: int) -> Dict[str, Any]:
        """
        Calculate the outcome of a single dice roll.

        Each dice "rolls" by:
        1. Applying R_perp to its 3 pairs
        2. Summing the residue fluxes weighted by projected coordinates
        3. Taking mod-4 to get the quaternionic outcome

        The key insight: R_perp selects ONE coordinate from each (2,0) pair.
        The "roll" is determined by which coordinate is selected (x or y)
        and the magnitude of the flux in that direction.

        Args:
            dice_index: Which dice (0-3)

        Returns:
            Dictionary containing roll details
        """
        pairs = DICE_GROUPS[dice_index]

        # Calculate weighted flux sum for this dice
        flux_sum = 0.0
        pair_contributions = []

        for pair_idx in pairs:
            # Apply R_perp and get projection
            x_proj, y_proj = self.apply_R_perp(pair_idx)

            # The OR selection: use the MAGNITUDE of the x-projection
            # This gives the "shadow" coordinate contribution
            # Positive contribution when x > 0, negative when x < 0
            # This creates the actual quantum sampling variance
            contribution = self.pair_fluxes[pair_idx] * x_proj  # NOT x**2
            flux_sum += contribution

            pair_contributions.append({
                "pair": pair_idx,
                "flux": float(self.pair_fluxes[pair_idx]),
                "x_proj": float(x_proj),
                "y_proj": float(y_proj),
                "contribution": float(contribution)
            })

        # Scale flux to positive range and take mod-4
        # P_branch = sum(R_perp_i * f_res^i)
        # Use abs() and floor() to ensure proper modular arithmetic
        # The sign information is preserved in the quaternionic structure
        scaled_flux_raw = abs(flux_sum) * K_GIMEL
        scaled_flux = int(np.floor(scaled_flux_raw)) % DICE_MODULUS

        return {
            "dice_index": dice_index,
            "pairs": pairs,
            "flux_sum": float(flux_sum),
            "flux_magnitude": float(abs(flux_sum)),
            "scaled_flux_raw": float(scaled_flux_raw),
            "scaled_flux": scaled_flux,
            "outcome": scaled_flux,  # The actual dice face (0-3)
            "pair_contributions": pair_contributions
        }

    def roll_all_dice(self) -> Dict[str, Any]:
        """
        Roll all 4 dice and determine branch selection.

        The 4 dice outcomes determine a position in 4D branch space:
        branch = d0 + 4*d1 + 16*d2 + 64*d3

        This gives 4^4 = 256 possible branches, corresponding to
        different realized configurations of spacetime.

        Returns:
            Complete roll result with branch selection
        """
        dice_outcomes = []
        dice_details = []

        for dice_idx in range(NUM_DICE):
            result = self.calculate_dice_roll(dice_idx)
            dice_outcomes.append(result["outcome"])
            dice_details.append(result)

        # Calculate branch selection using quaternionic base-4 encoding
        # branch_selected = d0 + 4*d1 + 16*d2 + 64*d3
        branch = (
            dice_outcomes[0] +
            4 * dice_outcomes[1] +
            16 * dice_outcomes[2] +
            64 * dice_outcomes[3]
        )

        # Calculate branch probability (proportional to total flux)
        total_flux = sum(d["flux_sum"] for d in dice_details)

        roll_result = {
            "dice_outcomes": dice_outcomes,
            "dice_details": dice_details,
            "branch_selected": branch,
            "total_branches": DICE_MODULUS ** NUM_DICE,  # 256
            "total_flux": float(total_flux),
            "branch_probability": float(1 / (DICE_MODULUS ** NUM_DICE)),  # Uniform for now
            "quaternionic_encoding": f"{dice_outcomes[3]}{dice_outcomes[2]}{dice_outcomes[1]}{dice_outcomes[0]}"
        }

        self.roll_history.append(roll_result)
        return roll_result

    def calculate_branch_probability(
        self,
        target_branch: int,
        n_samples: int = 10000
    ) -> Dict[str, Any]:
        """
        Calculate the probability of reaching a specific branch via Monte Carlo.

        Args:
            target_branch: Target branch number (0-255)
            n_samples: Number of Monte Carlo samples

        Returns:
            Probability analysis for the target branch
        """
        hits = 0
        branch_counts = np.zeros(DICE_MODULUS ** NUM_DICE)

        for _ in range(n_samples):
            # Re-initialize fluxes with random pattern for true sampling
            self.initialize_pair_fluxes("random")
            result = self.roll_all_dice()
            branch_counts[result["branch_selected"]] += 1
            if result["branch_selected"] == target_branch:
                hits += 1

        probability = hits / n_samples
        expected = 1 / (DICE_MODULUS ** NUM_DICE)  # 1/256 for uniform

        return {
            "target_branch": target_branch,
            "n_samples": n_samples,
            "hits": hits,
            "probability": probability,
            "expected_uniform": expected,
            "deviation": abs(probability - expected) / expected,
            "all_branch_counts": branch_counts.tolist(),
            "entropy": float(-np.sum(
                (branch_counts / n_samples) * np.log2(branch_counts / n_samples + 1e-10)
            ))
        }

    def analyze_dice_correlations(
        self,
        n_samples: int = 1000
    ) -> Dict[str, Any]:
        """
        Analyze correlations between dice outcomes.

        Checks if the 4 dice are truly independent or if there are
        geometric correlations from the G2 structure.

        Args:
            n_samples: Number of samples for correlation analysis

        Returns:
            Correlation analysis results
        """
        outcomes = np.zeros((n_samples, NUM_DICE))

        for i in range(n_samples):
            self.initialize_pair_fluxes("golden")
            result = self.roll_all_dice()
            outcomes[i] = result["dice_outcomes"]

        # Compute correlation matrix
        correlation_matrix = np.corrcoef(outcomes.T)

        # Check for independence: off-diagonal should be ~0
        off_diagonal = []
        for i in range(NUM_DICE):
            for j in range(i + 1, NUM_DICE):
                off_diagonal.append(correlation_matrix[i, j])

        mean_correlation = np.mean(np.abs(off_diagonal))

        return {
            "correlation_matrix": correlation_matrix.tolist(),
            "mean_abs_correlation": float(mean_correlation),
            "independent": mean_correlation < 0.1,
            "dice_means": [float(np.mean(outcomes[:, i])) for i in range(NUM_DICE)],
            "dice_stds": [float(np.std(outcomes[:, i])) for i in range(NUM_DICE)],
            "expected_mean": (DICE_MODULUS - 1) / 2,  # 1.5 for mod-4
            "expected_std": np.sqrt((DICE_MODULUS**2 - 1) / 12)  # ~1.12 for mod-4
        }


class MandalaVisualizer:
    """
    Visualizes the 12-pair mandala with dice group highlighting.

    The visualization shows:
    - 12 (2,0) pairs arranged in a circle (mandala pattern)
    - 4 dice groups distinguished by color
    - Current flux states for each pair
    - Branch selection result
    """

    def __init__(self, figsize: Tuple[int, int] = (12, 12)):
        """
        Initialize the mandala visualizer.

        Args:
            figsize: Figure size in inches
        """
        self.figsize = figsize

        # Color scheme for 4 dice (quaternion colors)
        self.dice_colors = ['#E74C3C', '#3498DB', '#2ECC71', '#F39C12']  # Red, Blue, Green, Orange
        self.dice_names = ['Dice 0 (Real)', 'Dice 1 (i)', 'Dice 2 (j)', 'Dice 3 (k)']

    def draw_mandala(
        self,
        pair_fluxes: np.ndarray,
        dice_outcomes: Optional[List[int]] = None,
        branch: Optional[int] = None,
        title: str = "12-Pair Consciousness Mandala"
    ) -> plt.Figure:
        """
        Draw the 12-pair mandala with dice groupings.

        Args:
            pair_fluxes: Array of flux values for each pair
            dice_outcomes: Optional list of dice outcomes to display
            branch: Optional branch number to display
            title: Plot title

        Returns:
            Matplotlib figure
        """
        fig, ax = plt.subplots(figsize=self.figsize)
        ax.set_aspect('equal')
        ax.set_xlim(-1.8, 1.8)
        ax.set_ylim(-1.8, 1.8)
        ax.axis('off')

        # Draw outer ring (representing the 25D bulk boundary)
        outer_circle = plt.Circle((0, 0), 1.5, fill=False,
                                   edgecolor='gray', linewidth=2, linestyle='--')
        ax.add_patch(outer_circle)

        # Draw inner circle (representing the 4D observable)
        inner_circle = plt.Circle((0, 0), 0.3, fill=True,
                                   facecolor='lightgray', edgecolor='black', linewidth=2)
        ax.add_patch(inner_circle)
        ax.text(0, 0, '4D', ha='center', va='center', fontsize=14, fontweight='bold')

        # Draw 12 pairs around the mandala
        angles = np.linspace(0, 2*np.pi, TOTAL_PAIRS, endpoint=False) - np.pi/2
        radius = 1.0

        for i in range(TOTAL_PAIRS):
            # Determine which dice this pair belongs to
            dice_idx = i // PAIRS_PER_DICE
            color = self.dice_colors[dice_idx]

            # Position of pair
            x = radius * np.cos(angles[i])
            y = radius * np.sin(angles[i])

            # Size proportional to flux
            size = 0.08 + 0.04 * (pair_fluxes[i] / np.max(pair_fluxes))

            # Draw pair as circle
            pair_circle = plt.Circle((x, y), size, fill=True,
                                     facecolor=color, edgecolor='black',
                                     linewidth=1.5, alpha=0.8)
            ax.add_patch(pair_circle)

            # Label with pair number
            label_r = radius + 0.2
            lx = label_r * np.cos(angles[i])
            ly = label_r * np.sin(angles[i])
            ax.text(lx, ly, f'P{i}', ha='center', va='center', fontsize=10)

            # Draw connection line to center
            ax.plot([0, x], [0, y], color=color, alpha=0.3, linewidth=1)

        # Draw dice group arcs
        for dice_idx in range(NUM_DICE):
            pairs = DICE_GROUPS[dice_idx]
            start_angle = np.degrees(angles[pairs[0]]) - 15
            end_angle = np.degrees(angles[pairs[2]]) + 15

            # Draw arc segment for dice group
            theta1 = min(start_angle, end_angle)
            theta2 = max(start_angle, end_angle)
            arc = plt.matplotlib.patches.Arc(
                (0, 0), 2.6, 2.6,
                angle=0, theta1=theta1, theta2=theta2,
                color=self.dice_colors[dice_idx], linewidth=4
            )
            ax.add_patch(arc)

        # Add legend for dice
        legend_y = 1.6
        for dice_idx in range(NUM_DICE):
            ax.add_patch(plt.Rectangle(
                (-1.7, legend_y - dice_idx * 0.15), 0.15, 0.1,
                facecolor=self.dice_colors[dice_idx], edgecolor='black'
            ))
            text = self.dice_names[dice_idx]
            if dice_outcomes is not None:
                text += f' = {dice_outcomes[dice_idx]}'
            ax.text(-1.5, legend_y - dice_idx * 0.15 + 0.05, text,
                   va='center', fontsize=10)

        # Title and branch info
        ax.text(0, 1.7, title, ha='center', va='center', fontsize=14, fontweight='bold')

        if branch is not None:
            ax.text(0, -1.7, f'Branch Selected: {branch} / 256',
                   ha='center', va='center', fontsize=12)

        # Add SSOT constants box
        info_text = (
            f'SSOT Constants:\n'
            f'b_3 = {B_3}\n'
            f'total_pairs = {TOTAL_PAIRS}\n'
            f'k_gimel = {K_GIMEL:.3f}\n'
            f'phi = {PHI:.3f}'
        )
        ax.text(1.4, -1.2, info_text, fontsize=9,
               family='monospace', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

        plt.tight_layout()
        return fig

    def draw_branch_distribution(
        self,
        branch_counts: np.ndarray,
        title: str = "Branch Selection Distribution"
    ) -> plt.Figure:
        """
        Draw histogram of branch selection distribution.

        Args:
            branch_counts: Array of counts for each branch (256 elements)
            title: Plot title

        Returns:
            Matplotlib figure
        """
        fig, ax = plt.subplots(figsize=(14, 6))

        n_branches = len(branch_counts)
        x = np.arange(n_branches)

        # Color by dice 0 outcome (first 2 bits)
        colors = [self.dice_colors[i % 4] for i in range(n_branches)]

        ax.bar(x, branch_counts, color=colors, alpha=0.7, width=1.0)

        # Expected uniform line
        expected = np.mean(branch_counts)
        ax.axhline(y=expected, color='red', linestyle='--', label=f'Expected (uniform) = {expected:.1f}')

        ax.set_xlabel('Branch Number (0-255)', fontsize=12)
        ax.set_ylabel('Count', fontsize=12)
        ax.set_title(title, fontsize=14)
        ax.legend()

        # Add quaternionic structure indicators
        for i in range(4):
            ax.axvline(x=64*i, color='gray', linestyle=':', alpha=0.5)
            ax.text(64*i + 32, ax.get_ylim()[1] * 0.95, f'k={i}',
                   ha='center', fontsize=10)

        plt.tight_layout()
        return fig


class OrchORIntegrator:
    """
    Integrates 4-dice sampling with Orch-OR (Orchestrated Objective Reduction).

    Connects the branch selection mechanism to Penrose's gravitational
    collapse timescale and the microtubule coherence framework.
    """

    def __init__(self, n_tubulins: float = 1e16):
        """
        Initialize Orch-OR integrator.

        Args:
            n_tubulins: Number of tubulins in coherent superposition
        """
        self.n_tubulins = n_tubulins
        self.sampler = FourDiceSampler()

        # Tubulin parameters
        self.m_tubulin = 1.8e-22    # kg
        self.separation = 4e-9       # m (tubulin diameter)

    def calculate_collapse_time(self) -> float:
        """
        Calculate Penrose-Diosi gravitational collapse time.

        tau_G = hbar / E_G where E_G = G * m^2 * N / r

        Returns:
            Collapse time in seconds
        """
        E_G = G_NEWTON * (self.m_tubulin ** 2) * self.n_tubulins / self.separation
        tau_G = HBAR / E_G
        return tau_G

    def consciousness_moment(
        self,
        flux_pattern: str = "golden"
    ) -> Dict[str, Any]:
        """
        Simulate a single consciousness moment (OR collapse event).

        This combines:
        1. 4-dice roll for branch selection
        2. Penrose collapse time calculation
        3. Conscious experience parameters

        Args:
            flux_pattern: Flux initialization pattern

        Returns:
            Complete consciousness moment data
        """
        # Initialize pair fluxes
        self.sampler.initialize_pair_fluxes(flux_pattern)

        # Roll all 4 dice
        roll_result = self.sampler.roll_all_dice()

        # Calculate collapse time
        tau_collapse = self.calculate_collapse_time()

        # Experience frequency (Hz)
        frequency = 1 / tau_collapse

        return {
            "roll_result": roll_result,
            "branch_selected": roll_result["branch_selected"],
            "dice_outcomes": roll_result["dice_outcomes"],
            "tau_collapse_s": float(tau_collapse),
            "tau_collapse_ms": float(tau_collapse * 1000),
            "experience_frequency_hz": float(frequency),
            "n_tubulins": self.n_tubulins,
            "quaternionic_signature": roll_result["quaternionic_encoding"],
            "4d_spacetime_coordinates": {
                "t": roll_result["dice_outcomes"][0],
                "x": roll_result["dice_outcomes"][1],
                "y": roll_result["dice_outcomes"][2],
                "z": roll_result["dice_outcomes"][3]
            }
        }


def run_demonstration():
    """
    Run a complete demonstration of the 4-dice consciousness sampling.
    """
    print("=" * 70)
    print("4-DICE CONSCIOUSNESS SAMPLING DEMONSTRATION")
    print("Principia Metaphysica v22.2 - Workstream 1")
    print("=" * 70)

    # Initialize sampler
    sampler = FourDiceSampler(seed=42)

    print("\n1. SSOT CONSTANTS:")
    print(f"   b_3 = {B_3} (third Betti number)")
    print(f"   total_pairs = {TOTAL_PAIRS}")
    print(f"   k_gimel = {K_GIMEL:.6f}")
    print(f"   phi = {PHI:.6f}")
    print(f"   pairs_per_dice = {PAIRS_PER_DICE}")
    print(f"   num_dice = {NUM_DICE}")
    print(f"   dice_modulus = {DICE_MODULUS}")
    print(f"   total_branches = {DICE_MODULUS ** NUM_DICE}")

    print("\n2. DICE GROUP STRUCTURE:")
    for i, group in enumerate(DICE_GROUPS):
        print(f"   Dice {i}: pairs {group}")

    print("\n3. PAIR FLUX INITIALIZATION (golden pattern):")
    fluxes = sampler.initialize_pair_fluxes("golden")
    for i, flux in enumerate(fluxes):
        dice_idx = i // PAIRS_PER_DICE
        print(f"   Pair {i:2d} (Dice {dice_idx}): flux = {flux:.4f}")

    print("\n4. SINGLE ROLL DEMONSTRATION:")
    result = sampler.roll_all_dice()
    print(f"   Dice outcomes: {result['dice_outcomes']}")
    print(f"   Branch selected: {result['branch_selected']} / {result['total_branches']}")
    print(f"   Quaternionic encoding: {result['quaternionic_encoding']}")
    print(f"   Total flux: {result['total_flux']:.4f}")

    print("\n5. BRANCH PROBABILITY ANALYSIS (1000 samples):")
    prob_result = sampler.calculate_branch_probability(target_branch=0, n_samples=1000)
    print(f"   Target branch 0 probability: {prob_result['probability']:.4f}")
    print(f"   Expected (uniform): {prob_result['expected_uniform']:.4f}")
    print(f"   Entropy (bits): {prob_result['entropy']:.2f} / {np.log2(256):.2f} max")

    print("\n6. DICE CORRELATION ANALYSIS:")
    corr_result = sampler.analyze_dice_correlations(n_samples=500)
    print(f"   Mean |correlation|: {corr_result['mean_abs_correlation']:.4f}")
    print(f"   Dice independent: {corr_result['independent']}")
    print(f"   Dice means: {[f'{m:.2f}' for m in corr_result['dice_means']]}")
    print(f"   Expected mean: {corr_result['expected_mean']:.2f}")

    print("\n7. ORCH-OR INTEGRATION:")
    integrator = OrchORIntegrator(n_tubulins=1e16)
    moment = integrator.consciousness_moment("golden")
    print(f"   Collapse time: {moment['tau_collapse_ms']:.3f} ms")
    print(f"   Experience frequency: {moment['experience_frequency_hz']:.1f} Hz")
    print(f"   4D coordinates: {moment['4d_spacetime_coordinates']}")

    print("\n" + "=" * 70)
    print("DEMONSTRATION COMPLETE")
    print("=" * 70)

    return sampler, prob_result, moment


def generate_visualizations(
    output_dir: Optional[str] = None,
    show: bool = True
) -> List[plt.Figure]:
    """
    Generate visualization figures for the 4-dice mechanism.

    Args:
        output_dir: Directory to save figures (None = don't save)
        show: Whether to display figures

    Returns:
        List of generated figures
    """
    sampler = FourDiceSampler(seed=42)
    sampler.initialize_pair_fluxes("golden")
    result = sampler.roll_all_dice()

    visualizer = MandalaVisualizer()
    figures = []

    # Figure 1: Mandala with current state
    fig1 = visualizer.draw_mandala(
        sampler.pair_fluxes,
        dice_outcomes=result["dice_outcomes"],
        branch=result["branch_selected"],
        title="12-Pair Consciousness Mandala with Dice Groups"
    )
    figures.append(fig1)

    # Figure 2: Branch distribution
    prob_result = sampler.calculate_branch_probability(0, n_samples=5000)
    fig2 = visualizer.draw_branch_distribution(
        np.array(prob_result["all_branch_counts"]),
        title="Branch Selection Distribution (5000 samples)"
    )
    figures.append(fig2)

    if output_dir:
        import os
        os.makedirs(output_dir, exist_ok=True)
        fig1.savefig(os.path.join(output_dir, "mandala_dice_groups.png"), dpi=150)
        fig2.savefig(os.path.join(output_dir, "branch_distribution.png"), dpi=150)
        print(f"Figures saved to {output_dir}")

    if show:
        plt.show()

    return figures


# =============================================================================
# GEMINI REVIEW QUESTIONS
# =============================================================================

GEMINI_QUESTIONS = """
GEMINI-STYLE MATHEMATICAL RIGOR REVIEW QUESTIONS
=================================================

These questions are designed for recursive peer review by Gemini or similar
AI systems to validate the mathematical foundations of the 4-dice mechanism.

1. GEOMETRIC SIGNIFICANCE IN G2:
   - Does the 4-dice grouping (12 pairs -> 4 groups of 3) have geometric
     significance in the G2 manifold structure?
   - The grouping 12 = 4 x 3 suggests a factorization. In G2, we have:
     * dim(G2) = 14 = 7 + 7 (vector and adjoint)
     * 12 pairs relate to 12 spatial dimensions from bridge structure
   - Question: Is there a subgroup of G2 with order 4 that acts on the
     3-cycles in a way that produces this grouping?
   - Possible connection: G2 has a Z/3Z triality structure. Combined with
     the Z/4Z from R_perp^4 = I, we get Z/12Z = Z/4Z x Z/3Z.

2. QUATERNIONIC STRUCTURE:
   - The mod-4 arithmetic strongly suggests quaternionic structure.
   - R_perp satisfies R_perp^2 = -I, which is the defining property of
     imaginary quaternionic units (i^2 = j^2 = k^2 = -1).
   - The 4 dice outcomes (0,1,2,3) could represent:
     * Real axis (d0) + three imaginary axes (d1, d2, d3)
     * Or: 4 roots of unity in C (1, i, -1, -i) reduced mod 4
   - Question: Can the branch selection formula
     branch = d0 + 4*d1 + 16*d2 + 64*d3
     be reinterpreted as a quaternionic number q = d0 + d1*i + d2*j + d3*k
     in a specific representation?

3. 4D SPACETIME CONNECTION:
   - The 4 dice naturally map to 4D spacetime coordinates (t, x, y, z).
   - Each dice "selects" one of 4 possible values for its dimension.
   - Question: Is this connection physical or merely analogical?
   - Deeper question: Does the OR (Objective Reduction) collapse mechanism
     in Orch-OR theory naturally produce 4D spacetime from the selection
     of 4 independent quantum outcomes?
   - Connection to signature: 4D Minkowski has (3,1) signature. The 4
     dice could represent 3 spatial + 1 temporal, with the temporal
     dice (d0) being "special" due to the +1 vs +4 coefficient.

4. INFORMATION THEORETIC:
   - 4 dice with 4 outcomes each = 4^4 = 256 branches = 8 bits.
   - 12 pairs with mod-4 aggregation suggests 2 bits per pair, but
     grouped into dice of 3 pairs.
   - Question: Is there information loss in the grouping? What is the
     channel capacity of the 12-pair -> 4-dice -> 8-bit mapping?

5. CONSISTENCY WITH ORCH-OR:
   - Penrose's OR requires gravitational self-energy to trigger collapse.
   - Our mechanism uses R_perp flux sampling.
   - Question: Can the flux sum be related to gravitational self-energy
     via E_G ~ sum_i f_res^i * G * m^2 / r ?
   - This would unify the branch selection with the collapse trigger.

6. PREDICTIVE POWER:
   - The mechanism predicts 256 possible branches per OR event.
   - At ~40 Hz consciousness rate, this gives 256 * 40 = 10,240 bits/s
     of "consciousness bandwidth".
   - Question: Can this be tested against psychophysical measurements
     of information processing rates in conscious experience?
"""


if __name__ == "__main__":
    # Run demonstration
    sampler, prob_result, moment = run_demonstration()

    print("\n" + GEMINI_QUESTIONS)

    # Optionally generate visualizations (uncomment to run)
    # generate_visualizations(show=True)
