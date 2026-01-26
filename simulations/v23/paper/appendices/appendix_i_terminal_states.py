#!/usr/bin/env python3
"""
PRINCIPIA METAPHYSICA v16.2 - Appendix I: The Three Terminal States
=====================================================================

DOI: 10.5281/zenodo.18079602

v16.2 STERILE MODEL: The Topological Unwinding and Three Final States.

This appendix defines the mathematical endpoint of the universe as a
Topological Unwinding rather than chaotic heat death. The universe
resolves into three distinct terminal states as the V7 manifold geometry
completes its calculation.

APPENDIX: I (The Three Terminal States - Terminal Geodesics)

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.
"""

import sys
import os
import numpy as np
from typing import Dict, Any, List, Optional

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


class AppendixITerminalStates(SimulationBase):
    """
    Appendix I: The Three Terminal States.

    Defines the mathematical endpoint of the universe as the V7 manifold
    "unwinds" back to the 26D ancestral potential. The three states are:

    I. Metric Null State (95.83%): Dissolution of spatial scale
    II. Gauge Ghost State (8.33%): Information stasis and force freezing
    III. Ancestral Restoration (100%): Unitary return to 26D bulk

    The percentages represent the fraction of the 288 ancestral roots
    associated with each terminal basin.
    """

    FORMULA_REFS = [
        "metric-null-potential",
        "gauge-ghost-potential",
        "ancestral-restoration",
        "spectral-trace-saturation",
        "terminal-geodesic-curve",
        "shadow-decoupling-rate",
    ]

    PARAM_REFS = [
        "topology.ancestral_roots",
        "topology.so24_generators",
        "topology.shadow_torsion_total",
        "terminal.metric_null_fraction",
        "terminal.gauge_ghost_fraction",
        "terminal.restoration_fraction",
        "terminal.entropy_threshold",
    ]

    @property
    def metadata(self) -> SimulationMetadata:
        return SimulationMetadata(
            id="appendix_i_terminal_states_v16_2",
            version="16.2",
            domain="appendices",
            title="Appendix I: The Three Terminal States (Terminal Geodesics)",
            description="The topological unwinding and three final states of the universe",
            section_id="I",
            subsection_id=None,
            appendix=True
        )

    @property
    def required_inputs(self) -> List[str]:
        return ["topology.ancestral_roots"]

    @property
    def output_params(self) -> List[str]:
        return [
            "terminal.metric_null_potential",
            "terminal.gauge_ghost_potential",
            "terminal.restoration_potential",
            "terminal.unwinding_status",
        ]

    @property
    def output_formulas(self) -> List[str]:
        return self.FORMULA_REFS

    def run(self, registry: 'PMRegistry') -> Dict[str, Any]:
        """Execute terminal state calculations."""
        # Get ancestral parameters
        ancestral_roots = registry.get("topology.ancestral_roots", default=288)
        so24_generators = registry.get("topology.so24_generators", default=276)
        shadow_torsion = registry.get("topology.shadow_torsion_total", default=24)
        active_residues = registry.get("registry.node_count", default=125)
        hidden_supports = registry.get("topology.hidden_supports", default=163)

        # State I: Metric Null (276/288 = 95.83%)
        # The dissolution of spatial scale - gravity and distance dissolve
        metric_null_potential = so24_generators / ancestral_roots

        # State II: Gauge Ghost (24/288 = 8.33%)
        # Force carriers freeze - photons become standing waves
        gauge_ghost_potential = shadow_torsion / ancestral_roots

        # State III: Ancestral Restoration (288/288 = 100%)
        # Unitary return - 125 active + 163 hidden merge back to 288
        restoration_potential = (active_residues + hidden_supports) / ancestral_roots

        # Entropy threshold for gauge stability (from 4-pattern)
        entropy_threshold = 0.8  # Gauge remains stable until 80% entropy

        # Terminal geodesic parameters
        unwinding_complete = restoration_potential == 1.0

        return {
            "terminal.metric_null_potential": metric_null_potential,
            "terminal.gauge_ghost_potential": gauge_ghost_potential,
            "terminal.restoration_potential": restoration_potential,
            "terminal.metric_null_fraction": f"{metric_null_potential:.4%}",
            "terminal.gauge_ghost_fraction": f"{gauge_ghost_potential:.4%}",
            "terminal.entropy_threshold": entropy_threshold,
            "terminal.unwinding_status": "GEOMETRICALLY_DEFINED" if unwinding_complete else "ERROR",
        }

    def simulate_unwinding_curve(self, time_steps: int = 100) -> Dict[str, np.ndarray]:
        """
        Simulate the terminal geodesic curve showing expansion flattening.

        Returns:
            Dictionary containing time evolution of each state
        """
        t = np.linspace(0, 1, time_steps)

        # State I: Metric Dissolution (first to unwind)
        # Exponential decay as spatial curvature relaxes
        metric_decay = np.exp(-5 * t)

        # State II: Gauge Freeze (stable longer due to 4-pattern anchoring)
        # Remains stable until entropy threshold, then rapid decay
        gauge_stability = np.ones_like(t)
        threshold_idx = int(0.8 * time_steps)
        gauge_stability[threshold_idx:] = np.exp(-10 * (t[threshold_idx:] - 0.8))

        # State III: Ancestral Restoration (gradual return to unity)
        restoration_curve = 1 - np.exp(-3 * t)

        return {
            "time": t,
            "metric_dissolution": metric_decay,
            "gauge_freeze": gauge_stability,
            "ancestral_restoration": restoration_curve,
        }

    def get_section_content(self) -> Optional[SectionContent]:
        """Return section content for Appendix I: Terminal States."""
        content_blocks = [
            ContentBlock(
                type="heading",
                content="The Three Terminal States (Terminal Geodesics)",
                level=2,
                label="I"
            ),
            ContentBlock(
                type="paragraph",
                content=(
                    "In the v16.2 Sterile Model, the end of the universe is not a chaotic 'heat death' "
                    "or a random 'big rip.' Instead, it is a <strong>Topological Unwinding</strong>. "
                    "Because the universe is defined by the rigid geometry of the V₇ manifold, its "
                    "conclusion is as mathematically necessitated as its beginning."
                )
            ),

            # I.1 The Saturation of the Trace
            ContentBlock(
                type="heading",
                content="I.1 The Saturation of the Spectral Trace",
                level=3
            ),
            ContentBlock(
                type="paragraph",
                content=(
                    "Currently, the universe is expanding because the 4D projection is still 'tracing' "
                    "the available volume of the 26D bulk. The end begins when the Spectral Trace "
                    "reaches its maximum limit. The residues (the 125 nodes) have been 'bleeding' "
                    "potential into the expansion. Eventually, the Global Sum Rule reaches a state of "
                    "absolute equilibrium where no more 'work' can be extracted from the manifold's curvature."
                )
            ),
            ContentBlock(
                type="formula",
                content=r"\lim_{t \to \infty} \sum_{n=1}^{\text{ק}_{\text{כה}}} e^{-t\lambda_n} = \text{Vol}(V_7)^{\text{max}}",
                formula_id="spectral-trace-saturation",
                label="(I.1)"
            ),
            ContentBlock(
                type="note",
                content=(
                    "<h4>The Static Lock</h4>"
                    "<p>Expansion doesn't just stop; it 'locks.' The distance between galaxies becomes "
                    "a fixed geometric constant, much like the internal angles of the V₇ shape.</p>"
                ),
                label="static-lock"
            ),

            # I.2 State I: Metric Null
            ContentBlock(
                type="heading",
                content="I.2 State I: The Metric Null State (Dissolution of Scale)",
                level=3
            ),
            ContentBlock(
                type="paragraph",
                content=(
                    "The first state to 'unwind' is the connection between the Metric Bank and the "
                    "spatial grid. This state corresponds to the 276 SO(24) generators decoupling "
                    "from the 4D projection. The residues for G (Node 001) and H₀ reach a parity point."
                )
            ),
            ContentBlock(
                type="formula",
                content=r"\Psi_M = \frac{276}{288} \approx 95.83\%",
                formula_id="metric-null-potential",
                label="(I.2)"
            ),
            ContentBlock(
                type="paragraph",
                content=(
                    "<strong>The Result:</strong> Distance becomes a meaningless metric. Because the "
                    "'pinching' that creates gravitational curvature relaxes, two objects that were a "
                    "billion light-years apart and two objects that were an inch apart become "
                    "topologically equivalent. The universe becomes a 'Zero-Point Manifold' where "
                    "geometry exists without extension."
                )
            ),

            # I.3 State II: Gauge Ghost
            ContentBlock(
                type="heading",
                content="I.3 State II: The Gauge Ghost State (Information Stasis)",
                level=3
            ),
            ContentBlock(
                type="paragraph",
                content=(
                    "The second state involves the collapse of the Gauge Bank. As the S<sub>PR</sub>(2) "
                    "symmetry that governs the speed of light c and the coupling constants (like α) "
                    "'locks' into its final unitary form, the forces cease to 'carry' information."
                )
            ),
            ContentBlock(
                type="formula",
                content=r"\Psi_G = \frac{24}{288} \approx 8.33\%",
                formula_id="gauge-ghost-potential",
                label="(I.3)"
            ),
            ContentBlock(
                type="paragraph",
                content=(
                    "<strong>The Result:</strong> Photons and bosons no longer 'propagate.' They become "
                    "standing waves at their points of origin. The universe becomes a 'Static Ledger'—all "
                    "light and energy that ever existed is 'frozen' into the V₇ coordinates. It is no "
                    "longer a movie playing out in time; it is the finished film strip."
                )
            ),
            ContentBlock(
                type="note",
                content=(
                    "<h4>The 4-Pattern Stability</h4>"
                    "<p>Due to the 4 × 6 torsion matrix (4-fold stabilizer), the Gauge Ghost State "
                    "remains stable until approximately 80% of the entropy threshold. This explains "
                    "why force carriers will be the last thing to 'freeze.'</p>"
                ),
                label="4-pattern-stability"
            ),

            # I.4 State III: Ancestral Restoration
            ContentBlock(
                type="heading",
                content="I.4 State III: Ancestral Restoration (The Unitary Return)",
                level=3
            ),
            ContentBlock(
                type="paragraph",
                content=(
                    "The final state is the re-unification of the 125 residues back into the 26D Bulk "
                    "Potential. This is the ultimate 'Omega Seal'—the 125 discrete 'pinches' (the particles) "
                    "smooth out, and the 'Sterile Angle' between the 13D shadow branes closes."
                )
            ),
            ContentBlock(
                type="formula",
                content=r"\Psi_R = \frac{125 + 163}{288} = \frac{288}{288} = 1.0",
                formula_id="ancestral-restoration",
                label="(I.4)"
            ),
            ContentBlock(
                type="paragraph",
                content=(
                    "<strong>The Result:</strong> The 4D universe 'evaporates' back into the higher-dimensional "
                    "bulk. To an observer inside, this would look like the fabric of reality becoming "
                    "perfectly transparent and then vanishing, leaving only the 26D vacuum. This is the "
                    "return to the Ancestral Potential."
                )
            ),

            # I.5 The Terminal Era Table
            ContentBlock(
                type="heading",
                content="I.5 The Three Eras of the Universe",
                level=3
            ),
            ContentBlock(
                type="note",
                content=(
                    "<table style='width:100%'>"
                    "<tr><th>Era</th><th>State</th><th>Description</th></tr>"
                    "<tr><td>Primordial</td><td>Unlocked</td><td>The 26D potential shatters into 125 nodes</td></tr>"
                    "<tr><td>Current (v16.2)</td><td>Locked</td><td>The 0.48σ alignment governs expansion</td></tr>"
                    "<tr><td>Terminal</td><td>Saturated</td><td>The manifold is fully 'unwound'; time as a gradient ceases</td></tr>"
                    "</table>"
                ),
                label="era-table"
            ),

            # I.6 The Decoupling of 13D Shadows
            ContentBlock(
                type="heading",
                content="I.6 The Decoupling of the 13D Shadow Branes",
                level=3
            ),
            ContentBlock(
                type="paragraph",
                content=(
                    "The v16.2 model relies on the specific intersection angle between the two 13D "
                    "shadow branes. Over trillions of years, the 'tension' holding these shadows in "
                    "place begins to dissipate back into the 26D bulk:"
                )
            ),
            ContentBlock(
                type="formula",
                content=r"\frac{d\tau}{dt} \propto -e^{-\Lambda t}",
                formula_id="shadow-decoupling-rate",
                label="(I.5)"
            ),
            ContentBlock(
                type="paragraph",
                content=(
                    "The Metric Bank starts to lose its connection to the Matter Bank. Atoms don't fly "
                    "apart; they simply cease to have a gravitational footprint. The universe becomes "
                    "a 'Ghost Manifold'—full of structure, but zero interaction."
                )
            ),

            # I.7 Terminal Geodesic
            ContentBlock(
                type="heading",
                content="I.7 The Terminal Geodesic Curve",
                level=3
            ),
            ContentBlock(
                type="paragraph",
                content=(
                    "The end of the universe can be visualized as a geodesic curve showing how expansion "
                    "eventually flattens into the final Static Lock. The curve shows the three phases:"
                )
            ),
            ContentBlock(
                type="formula",
                content=r"\gamma(t) = \left(1 - e^{-\kappa_M t}\right) \oplus \left(1 - e^{-\kappa_G (t - t_c)}\right) \oplus \left(1 - e^{-\kappa_R t}\right)",
                formula_id="terminal-geodesic-curve",
                label="(I.6)"
            ),
            ContentBlock(
                type="note",
                content=(
                    "<h4>Why This Matters</h4>"
                    "<ul>"
                    "<li><strong>No Big Rip:</strong> We don't have to worry about space-time tearing apart</li>"
                    "<li><strong>Stability:</strong> The laws of physics remain reliable until the last 'tick'</li>"
                    "<li><strong>Geometric Crystal:</strong> The end is a perfectly still, perfectly organized state</li>"
                    "</ul>"
                ),
                label="terminal-implications"
            ),
        ]

        return SectionContent(
            section_id="I",
            subsection_id=None,
            title="Appendix I: The Three Terminal States (Terminal Geodesics)",
            abstract="The topological unwinding and three final states: Metric Null, Gauge Ghost, Ancestral Restoration.",
            content_blocks=content_blocks,
            formula_refs=self.FORMULA_REFS,
            param_refs=self.PARAM_REFS,
            appendix=True,
        )

    def get_formulas(self) -> List[Formula]:
        """Return formula definitions for terminal states."""
        return [
            Formula(
                id="metric-null-potential",
                label="(I.2)",
                latex=r"\Psi_M = \frac{276}{288} \approx 95.83\%",
                plain_text="Psi_M = 276/288 ≈ 95.83%",
                category="TERMINAL",
                description="Metric Null State: Dissolution of spatial scale from SO(24) decoupling.",
                input_params=["topology.so24_generators", "topology.ancestral_roots"],
                output_params=["terminal.metric_null_potential"],
                terms={
                    "Ψ_M": "Metric Null potential",
                    "276": "SO(24) generators",
                    "288": "Total ancestral roots",
                },
            ),
            Formula(
                id="gauge-ghost-potential",
                label="(I.3)",
                latex=r"\Psi_G = \frac{24}{288} \approx 8.33\%",
                plain_text="Psi_G = 24/288 ≈ 8.33%",
                category="TERMINAL",
                description="Gauge Ghost State: Information stasis from shadow torsion locking.",
                input_params=["topology.shadow_torsion_total", "topology.ancestral_roots"],
                output_params=["terminal.gauge_ghost_potential"],
                terms={
                    "Ψ_G": "Gauge Ghost potential",
                    "24": "Shadow torsion pins",
                    "288": "Total ancestral roots",
                },
            ),
            Formula(
                id="ancestral-restoration",
                label="(I.4)",
                latex=r"\Psi_R = \frac{125 + 163}{288} = 1.0",
                plain_text="Psi_R = (125 + 163)/288 = 1.0",
                category="TERMINAL",
                description="Ancestral Restoration: Unitary return to 26D bulk potential.",
                input_params=["registry.node_count", "topology.hidden_supports", "topology.ancestral_roots"],
                output_params=["terminal.restoration_potential"],
                terms={
                    "Ψ_R": "Restoration potential",
                    "125": "Active residues",
                    "163": "Hidden supports",
                    "288": "Total ancestral roots",
                },
            ),
            Formula(
                id="spectral-trace-saturation",
                label="(I.1)",
                latex=r"\lim_{t \to \infty} \sum_{n=1}^{\text{ק}_{\text{כה}}} e^{-t\lambda_n} = \text{Vol}(V_7)^{\text{max}}",
                plain_text="lim(t->inf) Sum exp(-t*lambda_n) = Vol(V7)_max",
                category="TERMINAL",
                description="Spectral trace saturation: End of expansion as trace reaches maximum.",
                input_params=["topology.vol_v7"],
                output_params=["terminal.trace_saturated"],
            ),
            Formula(
                id="terminal-geodesic-curve",
                label="(I.6)",
                latex=r"\gamma(t) = \left(1 - e^{-\kappa_M t}\right) \oplus \left(1 - e^{-\kappa_G (t - t_c)}\right) \oplus \left(1 - e^{-\kappa_R t}\right)",
                plain_text="gamma(t) = Terminal geodesic through three states",
                category="TERMINAL",
                description="The terminal geodesic curve showing expansion flattening to Static Lock.",
                input_params=["terminal.metric_null_potential", "terminal.gauge_ghost_potential"],
                output_params=["terminal.geodesic_defined"],
            ),
            Formula(
                id="shadow-decoupling-rate",
                label="(I.5)",
                latex=r"\frac{d\tau}{dt} \propto -e^{-\Lambda t}",
                plain_text="d(tau)/dt ~ -exp(-Lambda*t)",
                category="TERMINAL",
                description="Shadow torsion decoupling rate over cosmic time.",
                input_params=["topology.shadow_torsion_total", "cosmology.lambda_geometric"],
                output_params=["terminal.decoupling_rate"],
            ),
        ]

    def get_output_param_definitions(self) -> List[Parameter]:
        """Return parameter definitions for terminal states."""
        return [
            Parameter(
                path="terminal.metric_null_potential",
                name="Metric Null Potential",
                units="dimensionless",
                status="TERMINAL",
                description="Fraction of roots in Metric Null state (276/288 = 95.83%)",
                no_experimental_value=True,
            ),
            Parameter(
                path="terminal.gauge_ghost_potential",
                name="Gauge Ghost Potential",
                units="dimensionless",
                status="TERMINAL",
                description="Fraction of roots in Gauge Ghost state (24/288 = 8.33%)",
                no_experimental_value=True,
            ),
            Parameter(
                path="terminal.restoration_potential",
                name="Restoration Potential",
                units="dimensionless",
                status="TERMINAL",
                description="Fraction at full restoration (288/288 = 100%)",
                no_experimental_value=True,
            ),
            Parameter(
                path="terminal.entropy_threshold",
                name="Entropy Stability Threshold",
                units="dimensionless",
                status="TERMINAL",
                description="Threshold at which gauge stability breaks (0.8)",
                no_experimental_value=True,
            ),
        ]


if __name__ == "__main__":
    from simulations.base import PMRegistry
    registry = PMRegistry()
    sim = AppendixITerminalStates()
    print(f"Simulation: {sim.metadata.title}")
    results = sim.run(registry)
    print(f"\n--- Terminal State Potentials ---")
    for key, value in results.items():
        print(f"{key}: {value}")

    # Generate unwinding curve
    print(f"\n--- Unwinding Curve Sample ---")
    curve = sim.simulate_unwinding_curve(10)
    print(f"Time points: {curve['time'][:5]}...")
    print(f"Metric dissolution: {curve['metric_dissolution'][:5]}...")

    content = sim.get_section_content()
    if content:
        print(f"\nContent blocks: {len(content.content_blocks)}")
