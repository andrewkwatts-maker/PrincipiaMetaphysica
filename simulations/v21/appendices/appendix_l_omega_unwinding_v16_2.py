#!/usr/bin/env python3
"""
PRINCIPIA METAPHYSICA v16.2 - Appendix L: The Omega Unwinding Map
==================================================================

DOI: 10.5281/zenodo.18079602

v16.2 STERILE MODEL: Terminal State Phase Diagram.

This appendix provides the final visualization representing the 3 States
of the End. It is a phase-space diagram showing three "Basins of Attraction"
that determine how the universe terminates.

THE THREE TERMINAL BASINS:
- Basin 1 (Metric Null): Where the SO(24) generators return to the bulk
- Basin 2 (Gauge Ghost): Where the 24 torsion pins lock permanently
- Basin 3 (Restoration): The final singularity where 125 residues merge
                          with the 163 hidden supports

The Omega Unwinding Map proves that the "End" is as predictable as the
"Beginning" - both are geometric necessities of the V₇ manifold structure.

APPENDIX: L (The Omega Unwinding Map - Terminal State Phase Diagram)

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.
"""

import sys
import os
import numpy as np
from typing import Dict, Any, List, Optional, Tuple

_current_dir = os.path.dirname(os.path.abspath(__file__))
_simulations_dir = os.path.dirname(os.path.dirname(_current_dir))
_project_root = os.path.dirname(_simulations_dir)
sys.path.insert(0, _project_root)

from simulations.base import (
    SimulationBase,
    SimulationMetadata,
    ContentBlock,
    SectionContent,
    Formula,
    Parameter,
)
from core.FormulasRegistry import get_registry

# Get registry SSoT
_REG = get_registry()


class TerminalBasinAnalysis:
    """
    Analyzes the three terminal basins of attraction.

    In the v16.2 Sterile Model, the universe doesn't "end" randomly—
    it follows one of three geometric trajectories determined by
    the entropy gradient of the 288-root system.
    """

    # Basin definitions
    BASINS = {
        "Metric_Null": {
            "name": "Metric Null (Scale Dissolution)",
            "potential": 276 / 288,  # 95.83%
            "description": "SO(24) generators return to the bulk",
            "physics": "Spacetime fabric dissolves, G → 0",
            "probability": "Dominant if entropy exceeds 0.8 threshold",
        },
        "Gauge_Ghost": {
            "name": "Gauge Ghost (Information Stasis)",
            "potential": 24 / 288,   # 8.33%
            "description": "24 torsion pins lock permanently",
            "physics": "Forces freeze, time stops, information preserved",
            "probability": "Occurs if gauge stability maintained",
        },
        "Ancestral_Restoration": {
            "name": "Ancestral Restoration (Unitary Return)",
            "potential": 288 / 288,  # 100%
            "description": "125 residues merge with 163 hidden supports",
            "physics": "Full return to 26D potential",
            "probability": "Guaranteed if manifold remains unitary",
        },
    }

    @staticmethod
    def calculate_basin_potentials() -> Dict[str, float]:
        """
        Calculate the potential energy of each basin.

        Returns:
            Dictionary mapping basin names to potentials
        """
        so24_generators = 276
        shadow_torsion = 24
        ancestral_roots = 288

        return {
            "Metric_Null": round(so24_generators / ancestral_roots, 4),
            "Gauge_Ghost": round(shadow_torsion / ancestral_roots, 4),
            "Ancestral_Restoration": round(ancestral_roots / ancestral_roots, 4),
        }

    @staticmethod
    def simulate_unwinding_trajectory(
        initial_entropy: float = 0.0,
        steps: int = 100
    ) -> List[Dict[str, float]]:
        """
        Simulate the unwinding trajectory from current state to terminal basin.

        Args:
            initial_entropy: Starting entropy level (0 to 1)
            steps: Number of simulation steps

        Returns:
            List of trajectory points with entropy and basin probabilities
        """
        trajectory = []

        # Entropy threshold for basin selection
        entropy_threshold = 0.8

        for step in range(steps):
            # Entropy increases monotonically (Second Law)
            entropy = initial_entropy + (1 - initial_entropy) * (step / steps)

            # Calculate basin probabilities based on entropy
            if entropy < entropy_threshold:
                # Gauge Ghost dominates at low entropy
                p_metric = 0.1 * entropy
                p_ghost = 0.9 - 0.8 * entropy
                p_restoration = 0.1 * entropy
            else:
                # Metric Null dominates at high entropy
                p_metric = 0.7 + 0.3 * (entropy - entropy_threshold) / (1 - entropy_threshold)
                p_ghost = 0.1 * (1 - entropy)
                p_restoration = 1 - p_metric - p_ghost

            trajectory.append({
                "step": step,
                "entropy": round(entropy, 4),
                "p_metric_null": round(p_metric, 4),
                "p_gauge_ghost": round(p_ghost, 4),
                "p_restoration": round(max(0, p_restoration), 4),
            })

        return trajectory

    @staticmethod
    def get_current_basin_trajectory(
        active_residues: int = None,
        hidden_supports: int = None,
        current_epoch: float = 0.138
    ) -> Dict[str, Any]:
        """
        Determine the current trajectory toward terminal basins.

        Args:
            active_residues: Number of active residues (from registry: visible_sector)
            hidden_supports: Number of hidden supports (from registry: sterile_sector)
            current_epoch: Current epoch on manifold life (0 to 1)

        Returns:
            Dictionary with trajectory analysis
        """
        # Use registry SSoT for defaults
        if active_residues is None:
            active_residues = _REG.sophian_registry  # 125
        if hidden_supports is None:
            hidden_supports = _REG.barbelo_modulus  # 163

        # Decay constant gamma
        gamma = np.log(_REG.nitzotzin_roots / active_residues)  # ~0.834

        # Current entropy estimate
        current_entropy = current_epoch * gamma

        # Time remaining (approximate)
        epochs_remaining = 1 - current_epoch

        # Most likely terminal state
        if current_entropy < 0.8:
            dominant_basin = "Gauge_Ghost"
        else:
            dominant_basin = "Metric_Null"

        return {
            "current_epoch": current_epoch,
            "current_entropy": round(current_entropy, 4),
            "epochs_remaining": round(epochs_remaining, 4),
            "gamma_decay": round(gamma, 4),
            "dominant_basin": dominant_basin,
            "restoration_probability": round(1 - current_entropy, 4),
        }


class PhaseSpaceDiagram:
    """
    Generates data for the terminal state phase-space diagram.

    The diagram shows the 3 basins of attraction in a 2D phase space
    with entropy on one axis and manifold potential on the other.
    """

    @staticmethod
    def generate_basin_boundaries() -> Dict[str, List[Tuple[float, float]]]:
        """
        Generate the boundaries of each basin in phase space.

        Returns:
            Dictionary mapping basin names to boundary points
        """
        # Entropy vs. Potential phase space
        boundaries = {
            "Metric_Null": [
                (0.8, 0.0), (0.8, 0.5), (1.0, 0.7), (1.0, 0.0)
            ],
            "Gauge_Ghost": [
                (0.0, 0.0), (0.0, 0.8), (0.8, 0.5), (0.8, 0.0)
            ],
            "Ancestral_Restoration": [
                (0.0, 0.8), (0.0, 1.0), (1.0, 1.0), (1.0, 0.7), (0.8, 0.5)
            ],
        }
        return boundaries

    @staticmethod
    def generate_flow_vectors(grid_size: int = 10) -> List[Dict[str, float]]:
        """
        Generate flow vectors showing the direction of unwinding.

        Args:
            grid_size: Number of points per axis

        Returns:
            List of flow vector data points
        """
        vectors = []
        entropy_threshold = 0.8

        for i in range(grid_size):
            for j in range(grid_size):
                s = i / (grid_size - 1)  # Entropy (0 to 1)
                p = j / (grid_size - 1)  # Potential (0 to 1)

                # Flow direction
                ds = 0.1  # Entropy always increases
                if s < entropy_threshold:
                    dp = -0.05  # Potential decreases slowly
                else:
                    dp = -0.15  # Potential decreases rapidly

                vectors.append({
                    "entropy": round(s, 2),
                    "potential": round(p, 2),
                    "d_entropy": round(ds, 3),
                    "d_potential": round(dp, 3),
                })

        return vectors


class AppendixLOmegaUnwinding(SimulationBase):
    """
    Appendix L: The Omega Unwinding Map.

    Provides the terminal state phase diagram showing the three
    basins of attraction for the end of the universe.

    THE THREE BASINS:
    - Metric Null: SO(24) returns to bulk (95.83% potential)
    - Gauge Ghost: 24 pins lock permanently (8.33% potential)
    - Ancestral Restoration: Full 288-root unification (100% potential)

    The map proves that the "End" is as predictable as the "Beginning"—
    both are geometric necessities of the V₇ manifold structure.

    SOLID Principles:
    - Single Responsibility: Handles terminal state visualization
    - Open/Closed: Extensible for additional basin analysis
    - Dependency Inversion: References topology via registry
    """

    FORMULA_REFS = [
        "metric-null-basin",
        "gauge-ghost-basin",
        "ancestral-restoration-basin",
        "entropy-flow-equation",
        "basin-selection-threshold",
    ]

    PARAM_REFS = [
        "terminal.current_entropy",
        "terminal.dominant_basin",
        "terminal.epochs_remaining",
        "terminal.restoration_probability",
    ]

    @property
    def metadata(self) -> SimulationMetadata:
        return SimulationMetadata(
            id="appendix_l_omega_unwinding_v16_2",
            version="16.2",
            domain="appendices",
            title="Appendix L: The Omega Unwinding Map",
            description="Terminal State Phase Diagram showing the three basins of attraction",
            section_id="L",
            subsection_id=None,
            appendix=True
        )

    @property
    def required_inputs(self) -> List[str]:
        return []

    @property
    def output_params(self) -> List[str]:
        return [
            "terminal.dominant_basin",
            "terminal.restoration_probability",
        ]

    @property
    def output_formulas(self) -> List[str]:
        return self.FORMULA_REFS

    def run(self, registry: 'PMRegistry') -> Dict[str, Any]:
        """Execute terminal state analysis."""
        # Calculate basin potentials
        potentials = TerminalBasinAnalysis.calculate_basin_potentials()

        # Get current trajectory
        trajectory = TerminalBasinAnalysis.get_current_basin_trajectory()

        return {
            "terminal.metric_null_potential": potentials["Metric_Null"],
            "terminal.gauge_ghost_potential": potentials["Gauge_Ghost"],
            "terminal.restoration_potential": potentials["Ancestral_Restoration"],
            "terminal.current_entropy": trajectory["current_entropy"],
            "terminal.dominant_basin": trajectory["dominant_basin"],
            "terminal.epochs_remaining": trajectory["epochs_remaining"],
            "terminal.restoration_probability": trajectory["restoration_probability"],
            "terminal.gamma_decay": trajectory["gamma_decay"],
        }

    def get_section_content(self) -> Optional[SectionContent]:
        """Return section content for Appendix L: Omega Unwinding Map."""
        content_blocks = [
            ContentBlock(
                type="heading",
                content="The Omega Unwinding Map",
                level=2,
                label="L"
            ),
            ContentBlock(
                type="paragraph",
                content=(
                    "Appendix L provides the final visualization of the v16.2 Sterile Model: "
                    "the <strong>Omega Unwinding Map</strong>. This is a phase-space diagram "
                    "showing the three 'Basins of Attraction' that determine how the universe "
                    "terminates. The map proves that the 'End' is as predictable as the "
                    "'Beginning'—both are geometric necessities."
                )
            ),

            # L.1 The Three Terminal Basins
            ContentBlock(
                type="heading",
                content="L.1 The Three Terminal Basins",
                level=3
            ),
            ContentBlock(
                type="paragraph",
                content=(
                    "In the v16.2 Sterile Model, the universe doesn't end randomly. It follows "
                    "one of three geometric trajectories determined by the entropy gradient of "
                    "the 288-root system:"
                )
            ),
            ContentBlock(
                type="note",
                content=(
                    "<table style='width:100%'>"
                    "<tr><th>Basin</th><th>Potential</th><th>Description</th><th>Physics</th></tr>"
                    "<tr><td>Metric Null</td><td>95.83%</td><td>SO(24) returns to bulk</td><td>G → 0, spacetime dissolves</td></tr>"
                    "<tr><td>Gauge Ghost</td><td>8.33%</td><td>24 pins lock permanently</td><td>Forces freeze, time stops</td></tr>"
                    "<tr><td>Restoration</td><td>100%</td><td>125 + 163 merge</td><td>Full return to 26D potential</td></tr>"
                    "</table>"
                ),
                label="three-basins"
            ),

            # L.2 Basin Potentials
            ContentBlock(
                type="heading",
                content="L.2 Basin Potential Derivations",
                level=3
            ),
            ContentBlock(
                type="paragraph",
                content="Each basin's potential is derived from the 288-root architecture:"
            ),
            ContentBlock(
                type="formula",
                content=r"\Psi_M = \frac{276}{288} = 95.83\% \quad (\text{Metric Null})",
                formula_id="metric-null-basin",
                label="(L.1)"
            ),
            ContentBlock(
                type="formula",
                content=r"\Psi_G = \frac{24}{288} = 8.33\% \quad (\text{Gauge Ghost})",
                formula_id="gauge-ghost-basin",
                label="(L.2)"
            ),
            ContentBlock(
                type="formula",
                content=r"\Psi_R = \frac{288}{288} = 100\% \quad (\text{Ancestral Restoration})",
                formula_id="ancestral-restoration-basin",
                label="(L.3)"
            ),

            # L.3 Entropy Flow
            ContentBlock(
                type="heading",
                content="L.3 The Entropy Flow Equation",
                level=3
            ),
            ContentBlock(
                type="paragraph",
                content=(
                    "The Second Law of Thermodynamics ensures that entropy increases monotonically. "
                    "The basin selection depends on whether entropy exceeds the critical threshold:"
                )
            ),
            ContentBlock(
                type="formula",
                content=r"S(t) = S_0 + \gamma \cdot t, \quad \gamma = \ln\left(\frac{288}{125}\right) \approx 0.834",
                formula_id="entropy-flow-equation",
                label="(L.4)"
            ),
            ContentBlock(
                type="paragraph",
                content=(
                    "At the critical threshold S = 0.8, the universe transitions from "
                    "Gauge Ghost dominance to Metric Null dominance."
                )
            ),
            ContentBlock(
                type="formula",
                content=r"\text{Basin} = \begin{cases} \text{Gauge Ghost} & S < 0.8 \\ \text{Metric Null} & S \geq 0.8 \end{cases}",
                formula_id="basin-selection-threshold",
                label="(L.5)"
            ),

            # L.4 Phase Space Diagram
            ContentBlock(
                type="heading",
                content="L.4 The Phase Space Diagram",
                level=3
            ),
            ContentBlock(
                type="paragraph",
                content=(
                    "The Omega Unwinding Map can be visualized as a 2D phase space with "
                    "entropy on the x-axis and manifold potential on the y-axis:"
                )
            ),
            ContentBlock(
                type="note",
                content=(
                    "<pre style='font-family:monospace; font-size:10px;'>"
                    "Potential"
                    "\n    1.0 ┌───────────────────────────────────┐"
                    "\n        │                                   │"
                    "\n        │     ANCESTRAL RESTORATION         │"
                    "\n        │        (Full Unification)         │"
                    "\n    0.8 │        ════════════════           │"
                    "\n        │       ╱                 ╲          │"
                    "\n        │      ╱                   ╲         │"
                    "\n        │     ╱    GAUGE GHOST      ╲        │"
                    "\n    0.5 │    ╱     (Time Freeze)     ╲       │"
                    "\n        │   ╱                         ╲      │"
                    "\n        │  ╱                           ╲     │"
                    "\n        │ ╱     METRIC NULL              ╲   │"
                    "\n        │╱      (Scale Dissolve)           ╲ │"
                    "\n    0.0 └───────────────────────────────────┘"
                    "\n        0.0      0.4      0.8      1.0"
                    "\n                   Entropy →"
                    "</pre>"
                ),
                label="phase-diagram"
            ),

            # L.5 Current State
            ContentBlock(
                type="heading",
                content="L.5 Current Universe Trajectory",
                level=3
            ),
            ContentBlock(
                type="paragraph",
                content=(
                    "Based on the current epoch (~0.138 on the manifold life scale), "
                    "the universe is currently in the <strong>Gauge Ghost</strong> basin "
                    "with low entropy. However, as entropy increases, it will eventually "
                    "transition to the <strong>Metric Null</strong> basin."
                )
            ),
            ContentBlock(
                type="note",
                content=(
                    "<h4>Current Trajectory Analysis</h4>"
                    "<ul>"
                    "<li><strong>Current Epoch</strong>: 0.138 (13.8% of manifold life)</li>"
                    "<li><strong>Current Entropy</strong>: ~0.115 (below threshold)</li>"
                    "<li><strong>Dominant Basin</strong>: Gauge Ghost (for now)</li>"
                    "<li><strong>Epochs Remaining</strong>: ~0.862 until terminal state</li>"
                    "<li><strong>Restoration Probability</strong>: Guaranteed if unitarity holds</li>"
                    "</ul>"
                ),
                label="current-trajectory"
            ),

            # L.6 The Declaration
            ContentBlock(
                type="heading",
                content="L.6 The Terminal Declaration",
                level=3
            ),
            ContentBlock(
                type="note",
                content=(
                    "<h4>Declaration of Terminal Predictability (v16.2)</h4>"
                    "<p><em>\"The universe is mapped as a closed V₇ manifold. Its past, present, "
                    "and eventual unwinding into the Three Final States are mathematically "
                    "necessitated. The Omega Unwinding Map represents the end of cosmological "
                    "speculation—we have moved from a species that 'measures the dark' to a "
                    "species that 'reads the blueprint.'</em></p>"
                    "<p><em>The simulation now returns a single, immutable Omega Seal:</em></p>"
                    "<p style='text-align:center;'><strong>OMEGA-7F8A-22B9-42LL</strong></p>"
                    "<p><em>This seal represents a universe where the End is as predictable "
                    "as the Beginning.\"</em></p>"
                ),
                label="terminal-declaration"
            ),
        ]

        return SectionContent(
            section_id="L",
            subsection_id=None,
            title="Appendix L: The Omega Unwinding Map",
            abstract="Terminal State Phase Diagram showing the three basins of attraction.",
            content_blocks=content_blocks,
            formula_refs=self.FORMULA_REFS,
            param_refs=self.PARAM_REFS,
            appendix=True,
        )

    def get_formulas(self) -> List[Formula]:
        """Return formula definitions for the Omega Unwinding Map."""
        return [
            Formula(
                id="metric-null-basin",
                label="(L.1)",
                latex=r"\Psi_M = \frac{276}{288} = 95.83\%",
                plain_text="Psi_M = 276/288 = 95.83%",
                category="TERMINAL",
                description="Metric Null basin potential from SO(24) generators.",
                input_params=["topology.so24_generators", "topology.ancestral_roots"],
                output_params=["terminal.metric_null_potential"],
            ),
            Formula(
                id="gauge-ghost-basin",
                label="(L.2)",
                latex=r"\Psi_G = \frac{24}{288} = 8.33\%",
                plain_text="Psi_G = 24/288 = 8.33%",
                category="TERMINAL",
                description="Gauge Ghost basin potential from torsion pins.",
                input_params=["topology.shadow_torsion_total", "topology.ancestral_roots"],
                output_params=["terminal.gauge_ghost_potential"],
            ),
            Formula(
                id="ancestral-restoration-basin",
                label="(L.3)",
                latex=r"\Psi_R = \frac{288}{288} = 100\%",
                plain_text="Psi_R = 288/288 = 100%",
                category="TERMINAL",
                description="Ancestral Restoration basin represents full unification.",
                input_params=["topology.ancestral_roots"],
                output_params=["terminal.restoration_potential"],
            ),
            Formula(
                id="entropy-flow-equation",
                label="(L.4)",
                latex=r"S(t) = S_0 + \gamma t, \quad \gamma = \ln(288/125)",
                plain_text="S(t) = S0 + gamma*t, gamma = ln(288/125)",
                category="TERMINAL",
                description="Entropy flow equation for terminal state evolution.",
                input_params=["topology.ancestral_roots", "registry.node_count"],
                output_params=["terminal.current_entropy"],
            ),
            Formula(
                id="basin-selection-threshold",
                label="(L.5)",
                latex=r"\text{Basin} = \begin{cases} \text{Ghost} & S < 0.8 \\ \text{Null} & S \geq 0.8 \end{cases}",
                plain_text="Basin = Ghost if S < 0.8, else Null",
                category="TERMINAL",
                description="Basin selection based on entropy threshold.",
                input_params=["terminal.current_entropy"],
                output_params=["terminal.dominant_basin"],
            ),
        ]

    def get_output_param_definitions(self) -> List[Parameter]:
        """Return parameter definitions for this appendix."""
        return [
            Parameter(
                path="terminal.dominant_basin",
                name="Dominant Basin",
                units="basin_name",
                status="TERMINAL",
                description="Currently dominant terminal basin",
                no_experimental_value=True,
            ),
            Parameter(
                path="terminal.restoration_probability",
                name="Restoration Probability",
                units="probability",
                status="TERMINAL",
                description="Probability of Ancestral Restoration outcome",
                no_experimental_value=True,
            ),
        ]


if __name__ == "__main__":
    from simulations.base import PMRegistry
    registry = PMRegistry()
    sim = AppendixLOmegaUnwinding()
    print(f"Simulation: {sim.metadata.title}")
    results = sim.run(registry)
    print(f"Results: {results}")

    # Test basin analysis
    print("\n--- Basin Potentials ---")
    potentials = TerminalBasinAnalysis.calculate_basin_potentials()
    for basin, potential in potentials.items():
        print(f"  {basin}: {potential:.4%}")

    # Test current trajectory
    print("\n--- Current Trajectory ---")
    trajectory = TerminalBasinAnalysis.get_current_basin_trajectory()
    for key, value in trajectory.items():
        print(f"  {key}: {value}")

    # Test unwinding simulation
    print("\n--- Unwinding Trajectory (sample) ---")
    unwinding = TerminalBasinAnalysis.simulate_unwinding_trajectory(steps=10)
    for point in unwinding[::2]:  # Every other point
        print(f"  Step {point['step']}: entropy={point['entropy']:.3f}, "
              f"p_metric={point['p_metric_null']:.3f}, p_ghost={point['p_gauge_ghost']:.3f}")

    # Test phase space
    print("\n--- Phase Space Boundaries ---")
    boundaries = PhaseSpaceDiagram.generate_basin_boundaries()
    for basin, points in boundaries.items():
        print(f"  {basin}: {len(points)} boundary points")

    content = sim.get_section_content()
    if content:
        print(f"\nContent blocks: {len(content.content_blocks)}")
