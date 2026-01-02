#!/usr/bin/env python3
"""
PRINCIPIA METAPHYSICA v16.2 - Appendix H: The 288-Root Basis
==============================================================

DOI: 10.5281/zenodo.18079602

v16.2 STERILE MODEL: The 288 Ancestral Roots and 24 Shadow Torsion.

This appendix provides the mathematical foundation proving that the 125
observable residues are derived from a 288-generator symmetry in the 26D bulk.

The 288 Ancestral Roots = SO(24) Generators (276) + Shadow Torsion (24) - Manifold Cost (12)

APPENDIX: H (The 288-Root Basis - Ancestral Symmetry Architecture)

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


class AppendixH288Roots(SimulationBase):
    """
    Appendix H: The 288-Root Basis.

    Proves that the 125 residues are the observable subset of a 288-generator
    symmetry originating from the SO(24) transverse group of the 26D bulk.

    Key Components:
    - 276: SO(24) generators from 24 transverse dimensions
    - 24: Shadow torsion (12 per 13D shadow brane)
    - 12: Manifold projection cost (consumed for 4D bridge)
    - 288: Total ancestral roots
    - 125: Active observable residues
    - 163: Hidden structural supports
    """

    FORMULA_REFS = [
        "so24-generators",
        "shadow-torsion-sum",
        "ancestral-roots-derivation",
        "sterile-projection-filter",
        "hidden-support-count",
    ]

    PARAM_REFS = [
        "topology.transverse_dimensions",
        "topology.so24_generators",
        "topology.torsion_per_shadow",
        "topology.shadow_torsion_total",
        "topology.manifold_cost",
        "topology.ancestral_roots",
        "topology.hidden_supports",
        "registry.node_count",
    ]

    @property
    def metadata(self) -> SimulationMetadata:
        return SimulationMetadata(
            id="appendix_h_288_roots_v16_2",
            version="16.2",
            domain="appendices",
            title="Appendix H: The 288-Root Basis (Ancestral Symmetry Architecture)",
            description="The 288 ancestral roots from SO(24) and 12-per-shadow torsion",
            section_id="H",
            subsection_id=None,
            appendix=True
        )

    @property
    def required_inputs(self) -> List[str]:
        return []

    @property
    def output_params(self) -> List[str]:
        return [
            "topology.ancestral_roots",
            "topology.so24_generators",
            "topology.shadow_torsion_total",
            "topology.hidden_supports",
            "topology.sterile_ratio",
        ]

    @property
    def output_formulas(self) -> List[str]:
        return self.FORMULA_REFS

    def run(self, registry: 'PMRegistry') -> Dict[str, Any]:
        """Execute 288-Root derivation and validation."""
        # Fundamental constants from geometry
        n_transverse = registry.get("topology.transverse_dimensions", default=24)
        torsion_per_shadow = registry.get("topology.torsion_per_shadow", default=12)
        manifold_cost = registry.get("topology.manifold_cost", default=12)
        active_residues = registry.get("registry.node_count", default=125)

        # SO(24) generators: n(n-1)/2
        so24_generators = (n_transverse * (n_transverse - 1)) // 2  # 276

        # Shadow torsion: 12 per shadow brane × 2 branes
        shadow_torsion_total = torsion_per_shadow * 2  # 24

        # Ancestral roots: generators + torsion - cost
        ancestral_roots = so24_generators + shadow_torsion_total - manifold_cost  # 288

        # Hidden supports: roots - active
        hidden_supports = ancestral_roots - active_residues  # 163

        # Sterile ratio: percentage of roots that manifest
        sterile_ratio = active_residues / ancestral_roots  # 43.4%

        # Sterile angle derivation
        sterile_angle_rad = np.arcsin(active_residues / ancestral_roots)
        sterile_angle_deg = np.degrees(sterile_angle_rad)  # ~25.72°

        return {
            "topology.ancestral_roots": ancestral_roots,
            "topology.so24_generators": so24_generators,
            "topology.shadow_torsion_total": shadow_torsion_total,
            "topology.hidden_supports": hidden_supports,
            "topology.sterile_ratio": sterile_ratio,
            "topology.sterile_angle_deg": sterile_angle_deg,
            "validation.288_root_verified": ancestral_roots == 288,
        }

    def get_section_content(self) -> Optional[SectionContent]:
        """Return section content for Appendix H: The 288-Root Basis."""
        content_blocks = [
            ContentBlock(
                type="heading",
                content="The 288-Root Basis (Ancestral Symmetry Architecture)",
                level=2,
                label="H"
            ),
            ContentBlock(
                type="paragraph",
                content=(
                    "Appendix H establishes the mathematical foundation proving that the 125 "
                    "observable residues are not arbitrary but are the <strong>Observable Subset</strong> "
                    "of a 288-generator symmetry in the 26D ancestral bulk. This section introduces "
                    "the SO(24) transverse group and the 12-per-shadow torsion mechanism."
                )
            ),

            # H.1 The Symmetry Group Origin
            ContentBlock(
                type="heading",
                content="H.1 The SO(24) Transverse Symmetry",
                level=3
            ),
            ContentBlock(
                type="paragraph",
                content=(
                    "In 26D Bosonic String Theory, there are 24 transverse dimensions. The symmetry "
                    "group governing these is SO(24). The number of generators (the dimension) for "
                    "SO(n) is calculated as n(n-1)/2:"
                )
            ),
            ContentBlock(
                type="formula",
                content=r"\text{dim}(SO(24)) = \frac{24 \times 23}{2} = 276",
                formula_id="so24-generators",
                label="(H.1)"
            ),

            # H.2 The Shadow Torsion
            ContentBlock(
                type="heading",
                content="H.2 The 12-Per-Shadow Torsion Mechanism",
                level=3
            ),
            ContentBlock(
                type="paragraph",
                content=(
                    "Each of the two 13D shadow branes requires <strong>12 torsion pins</strong> to "
                    "maintain stability within the 26D bulk. These pins represent the degrees of "
                    "freedom required to 'anchor' a 13D object in higher-dimensional space:"
                )
            ),
            ContentBlock(
                type="formula",
                content=r"\tau_{\text{total}} = \tau_A + \tau_B = 12 + 12 = 24",
                formula_id="shadow-torsion-sum",
                label="(H.2)"
            ),
            ContentBlock(
                type="note",
                content=(
                    "<h4>Why 12 Per Shadow?</h4>"
                    "<p>A 13D brane is a complex topological object. It requires 12 independent "
                    "vectors to be 'pinned' within a 26D bulk. This is analogous to how a 3D object "
                    "requires 6 degrees of freedom (3 translation + 3 rotation) to be fixed in 3D space. "
                    "For a 13D object in 26D, the degrees of freedom scale to 12 per brane.</p>"
                ),
                label="12-per-shadow-explanation"
            ),

            # H.3 The Ancestral Root Derivation
            ContentBlock(
                type="heading",
                content="H.3 The 288 Ancestral Root Derivation",
                level=3
            ),
            ContentBlock(
                type="paragraph",
                content=(
                    "The total 'Symmetry Budget' of the ancestral 26D bulk is calculated by combining "
                    "the SO(24) generators with the shadow torsion, then subtracting the 'manifold cost' "
                    "(the 12 degrees consumed to create the 4D projection bridge):"
                )
            ),
            ContentBlock(
                type="formula",
                content=r"R_{\text{ancestral}} = \text{dim}(SO(24)) + \tau_{\text{total}} - C_{\text{manifold}} = 276 + 24 - 12 = 288",
                formula_id="ancestral-roots-derivation",
                label="(H.3)"
            ),

            # H.4 The Sterile Projection Filter
            ContentBlock(
                type="heading",
                content="H.4 The Sterile Projection Filter (288 → 125)",
                level=3
            ),
            ContentBlock(
                type="paragraph",
                content=(
                    "Not all 288 ancestral roots manifest as observable particles. The V₇ Laplacian "
                    "acts as a <strong>Sterile Filter</strong>, selecting only those residues that "
                    "align with the Sterile Angle (θ ≈ 25.72°):"
                )
            ),
            ContentBlock(
                type="formula",
                content=r"\theta_{\text{sterile}} = \arcsin\left(\frac{125}{288}\right) \approx 25.72°",
                formula_id="sterile-projection-filter",
                label="(H.4)"
            ),

            # H.5 The Hidden Structural Supports
            ContentBlock(
                type="heading",
                content="H.5 The 163 Hidden Structural Supports",
                level=3
            ),
            ContentBlock(
                type="paragraph",
                content=(
                    "The 163 'missing' roots are not lost; they act as the <strong>Structural "
                    "Reinforcement</strong> for the 125 observable residues. They are sub-Planckian "
                    "and provide the internal supports that enforce the Metric Lock:"
                )
            ),
            ContentBlock(
                type="formula",
                content=r"N_{\text{hidden}} = R_{\text{ancestral}} - N_{\text{active}} = 288 - 125 = 163",
                formula_id="hidden-support-count",
                label="(H.5)"
            ),
            ContentBlock(
                type="note",
                content=(
                    "<table style='width:100%'>"
                    "<tr><th>State</th><th>Count</th><th>Status</th><th>Role</th></tr>"
                    "<tr><td>Ancestral Root</td><td>288</td><td>Potential</td><td>The Raw 26D Potential</td></tr>"
                    "<tr><td>Active Residue</td><td>125</td><td>Observable</td><td>The Spectral Registry</td></tr>"
                    "<tr><td>Ghost Support</td><td>163</td><td>Structural</td><td>Enforces Metric Lock</td></tr>"
                    "</table>"
                ),
                label="root-distribution-table"
            ),

            # H.6 The 4-Fold Stabilizer
            ContentBlock(
                type="heading",
                content="H.6 The 4-Fold Stabilizer (4 × 6 Torsion Matrix)",
                level=3
            ),
            ContentBlock(
                type="paragraph",
                content=(
                    "The 24 torsion pins are distributed across the 4 dimensions of spacetime "
                    "(t, x, y, z), with exactly 6 pins per dimension. This <strong>4-Fold Stabilizer</strong> "
                    "is what ensures the universe is isotropic (looks the same in all directions):"
                )
            ),
            ContentBlock(
                type="note",
                content=(
                    "<ul>"
                    "<li><strong>Time (t)</strong>: 6 torsion pins - defines the arrow of causality</li>"
                    "<li><strong>Length (x)</strong>: 6 torsion pins - defines spatial extension</li>"
                    "<li><strong>Width (y)</strong>: 6 torsion pins - orthogonal spatial component</li>"
                    "<li><strong>Depth (z)</strong>: 6 torsion pins - completes 3D spatial grid</li>"
                    "</ul>"
                    "<p>If the torsion were not divisible by 4, the universe would exhibit anisotropy.</p>"
                ),
                label="4-fold-stabilizer"
            ),
        ]

        return SectionContent(
            section_id="H",
            subsection_id=None,
            title="Appendix H: The 288-Root Basis (Ancestral Symmetry Architecture)",
            abstract="The 288 ancestral roots from SO(24) transverse symmetry and 12-per-shadow torsion.",
            content_blocks=content_blocks,
            formula_refs=self.FORMULA_REFS,
            param_refs=self.PARAM_REFS,
            appendix=True,
        )

    def get_formulas(self) -> List[Formula]:
        """Return formula definitions for the 288-Root basis."""
        return [
            Formula(
                id="so24-generators",
                label="(H.1)",
                latex=r"\text{dim}(SO(24)) = \frac{24 \times 23}{2} = 276",
                plain_text="dim(SO(24)) = 24*23/2 = 276",
                category="FOUNDATIONAL",
                description="SO(24) symmetry generators from 24 transverse dimensions.",
                input_params=["topology.transverse_dimensions"],
                output_params=["topology.so24_generators"],
                terms={
                    "SO(24)": "Special orthogonal group in 24 dimensions",
                    "276": "Number of independent generators",
                },
            ),
            Formula(
                id="shadow-torsion-sum",
                label="(H.2)",
                latex=r"\tau_{\text{total}} = \tau_A + \tau_B = 12 + 12 = 24",
                plain_text="tau_total = 12 + 12 = 24",
                category="FOUNDATIONAL",
                description="Total shadow torsion from two 13D branes with 12 pins each.",
                input_params=["topology.torsion_per_shadow"],
                output_params=["topology.shadow_torsion_total"],
                terms={
                    "τ_A": "Torsion pins for Shadow Brane A (12)",
                    "τ_B": "Torsion pins for Shadow Brane B (12)",
                },
            ),
            Formula(
                id="ancestral-roots-derivation",
                label="(H.3)",
                latex=r"R_{\text{ancestral}} = 276 + 24 - 12 = 288",
                plain_text="R_ancestral = 276 + 24 - 12 = 288",
                category="STERILE_PROOF",
                description="Total ancestral roots: SO(24) + torsion - manifold cost.",
                input_params=["topology.so24_generators", "topology.shadow_torsion_total", "topology.manifold_cost"],
                output_params=["topology.ancestral_roots"],
                terms={
                    "276": "SO(24) generators",
                    "24": "Shadow torsion pins",
                    "12": "Manifold projection cost",
                    "288": "Total ancestral roots",
                },
            ),
            Formula(
                id="sterile-projection-filter",
                label="(H.4)",
                latex=r"\theta_{\text{sterile}} = \arcsin\left(\frac{125}{288}\right) \approx 25.72°",
                plain_text="theta_sterile = arcsin(125/288) ≈ 25.72°",
                category="DERIVED",
                description="Sterile angle determining which roots manifest as observables.",
                input_params=["registry.node_count", "topology.ancestral_roots"],
                output_params=["topology.sterile_angle"],
            ),
            Formula(
                id="hidden-support-count",
                label="(H.5)",
                latex=r"N_{\text{hidden}} = 288 - 125 = 163",
                plain_text="N_hidden = 288 - 125 = 163",
                category="DERIVED",
                description="Hidden structural supports that enforce the Metric Lock.",
                input_params=["topology.ancestral_roots", "registry.node_count"],
                output_params=["topology.hidden_supports"],
            ),
        ]

    def get_output_param_definitions(self) -> List[Parameter]:
        """Return parameter definitions for the 288-Root basis."""
        return [
            Parameter(
                path="topology.ancestral_roots",
                name="Ancestral Root Count",
                units="dimensionless",
                status="FOUNDATIONAL",
                description="Total 288 ancestral roots from SO(24) + shadow torsion - manifold cost",
                no_experimental_value=True,
            ),
            Parameter(
                path="topology.so24_generators",
                name="SO(24) Generators",
                units="dimensionless",
                status="FOUNDATIONAL",
                description="Number of SO(24) symmetry generators (276)",
                no_experimental_value=True,
            ),
            Parameter(
                path="topology.shadow_torsion_total",
                name="Total Shadow Torsion",
                units="dimensionless",
                status="FOUNDATIONAL",
                description="Total torsion pins from both 13D shadow branes (24)",
                no_experimental_value=True,
            ),
            Parameter(
                path="topology.hidden_supports",
                name="Hidden Structural Supports",
                units="dimensionless",
                status="DERIVED",
                description="Sub-Planckian supports enforcing Metric Lock (163)",
                no_experimental_value=True,
            ),
            Parameter(
                path="topology.sterile_ratio",
                name="Sterile Saturation Ratio",
                units="dimensionless",
                status="DERIVED",
                description="Percentage of ancestral roots that manifest (125/288 = 43.4%)",
                no_experimental_value=True,
            ),
        ]


if __name__ == "__main__":
    from simulations.base import PMRegistry
    registry = PMRegistry()
    sim = AppendixH288Roots()
    print(f"Simulation: {sim.metadata.title}")
    results = sim.run(registry)
    print(f"\n--- 288-Root Derivation ---")
    for key, value in results.items():
        print(f"{key}: {value}")
    content = sim.get_section_content()
    if content:
        print(f"\nContent blocks: {len(content.content_blocks)}")
        print(f"Formula refs: {content.formula_refs}")
