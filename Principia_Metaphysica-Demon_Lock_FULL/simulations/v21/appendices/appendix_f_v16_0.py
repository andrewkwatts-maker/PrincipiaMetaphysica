#!/usr/bin/env python3
"""
Appendix F: Dimensional Decomposition v21.0 - Dual Shadow Framework
====================================================================

Mathematical framework for reducing 26-dimensional (24,1) unified time signature
spacetime into dual 13D(12,1) shadows connected by a 2D Euclidean bridge. Shows how
the breathing dark energy parameter emerges from bridge pressure mismatch.

The v22 decomposition follows:
1. (24,1) unified time signature from critical string theory (no ghosts)
2. 27D(26,1) = 12×(2,0) bridge pairs + (0,1) shared time
3. Bridge WARPS to create shadows: 12×(2,0) → 2×13D(12,1) via coordinate selection
4. OR reduction operator R_perp with Mobius property R_perp² = -I
5. Per-shadow G₂ compactification: 13D(12,1) → (3,1) + G₂(7) + fiber
6. Each (2,0) pair (x_i, y_i): x_i → Normal shadow, y_i → Mirror shadow

References:
- Acharya & Witten (2001) "Chiral Fermions from G2 Manifolds"
- DESI Collaboration (2025) "DESI DR2 Results"
- Joyce (2000) "Compact Manifolds with Special Holonomy"

NOTE: This is a COMPLETE REWRITE from v16.0 (24,2) to v21.0 (24,1) framework.
The old Sp(2,R) gauge-fixing approach is archived in appendix_d_sp2r_invariance_v16_0.py.

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.

Dedicated To:
    My Wife: Elizabeth May Watts
    Our Messiah: Jesus Of Nazareth
"""

import numpy as np
from typing import Dict, Any, List, Optional
import sys
import os

# Add parent directories to path for imports
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.insert(0, project_root)

from simulations.base import (
    SimulationBase,
    SimulationMetadata,
    Formula,
    Parameter,
    SectionContent,
    ContentBlock,
)


class AppendixFDimensionalDecomposition(SimulationBase):
    """
    Appendix F: v22 Dimensional Decomposition with 12×(2,0) Bridge Architecture

    Derives the dimensional reduction: 27D(26,1) = 12×(2,0) + (0,1)
    where the 12 bridge pairs WARP to create dual 13D(12,1) shadows via
    coordinate selection, then per-shadow G₂ compactification to (3,1) + G₂.

    Key changes from v16.0 (24,2):
    - Unified time (24,1) eliminates ghosts and CTCs
    - Dual shadows replace single 13D shadow
    - Euclidean bridge (2,0) replaces Sp(2,R) gauge-fixing
    - OR reduction operator R_perp provides Mobius double-cover
    - Breathing dark energy from bridge pressure mismatch
    """

    @property
    def metadata(self) -> SimulationMetadata:
        """Return simulation metadata."""
        return SimulationMetadata(
            id="appendix_f_v21_0",
            version="21.0",
            domain="appendices",
            title="Appendix F: v21 Dimensional Decomposition (Dual-Shadow Bridge)",
            description=(
                "Mathematical framework for reducing 26-dimensional (24,1) unified time signature "
                "spacetime into dual 13D(12,1) shadows connected by a 2D Euclidean bridge."
            ),
            section_id="2",
            subsection_id="F",
            appendix=True
        )

    @property
    def required_inputs(self) -> List[str]:
        """Return list of required input parameter paths."""
        return [
            "topology.b3",
        ]

    @property
    def output_params(self) -> List[str]:
        """Return list of output parameter paths."""
        return [
            "dimensions.bulk_signature",
            "dimensions.shadow_signature",
            "dimensions.bridge_signature",
            "dimensions.or_operator_property",
            "dimensions.bridge_period",
            "dimensions.breathing_w0",
        ]

    @property
    def output_formulas(self) -> List[str]:
        """Return list of formula IDs this simulation provides."""
        return [
            "v21-unified-time-metric",
            "v21-dual-shadow-split",
            "v21-euclidean-bridge-metric",
            "v21-or-reduction-operator",
            "v21-mobius-property",
            "v21-breathing-dark-energy",
        ]

    def run(self, registry: 'PMRegistry') -> Dict[str, Any]:
        """
        Execute v21 dimensional decomposition calculation.

        Args:
            registry: PMRegistry instance with input parameters

        Returns:
            Dictionary with dimensional reduction results
        """
        # v22 DIMENSIONAL STRUCTURE
        # 27D(26,1) = 12×(2,0) bridge pairs + (0,1) shared time
        D_bulk = 25  # 25D bulk (not 26D - that's legacy)

        # v22: 12×(2,0) bridge pairs = 24 spatial dimensions
        n_bridge_pairs = 12  # 12 Euclidean bridge pairs
        bridge_dims_per_pair = 2  # Each (2,0) pair has 2 spatial dimensions
        total_bridge_spatial = n_bridge_pairs * bridge_dims_per_pair  # = 24 spatial
        shared_time = 1  # (0,1) shared between shadows

        # Verify: 24 spatial + 1 time = 25D
        assert total_bridge_spatial + shared_time == D_bulk

        # v22: Bridge pairs WARP to create dual shadows via coordinate selection
        # Each (x_i, y_i) pair contributes: x_i → Normal shadow, y_i → Mirror shadow
        # Result: Each shadow gets 12 spatial + 1 shared time = 13D(12,1)
        shadow_spatial = 12  # 12 spatial from 12 bridge pairs (one coord each)
        shadow_time = 1  # 1 shared time
        shadow_total = shadow_spatial + shadow_time  # = 13D per shadow

        # Per-shadow G₂ compactification: 13D(12,1) → (3,1) + G₂(7) + S¹(1) fiber
        phys_spatial = 3
        phys_time = 1
        g2_dimensions = 7
        s1_fiber = 1  # Remaining from 13D

        # Verify: 3 + 7 + 1 (fiber) + 1 (time from 13D total) = 12 + 1 = 13D
        assert phys_spatial + g2_dimensions + s1_fiber + 1 == shadow_total + 1

        # OR Reduction Operator R_perp
        # R_perp = [[0, -1], [1, 0]]
        # R_perp^2 = -I (Mobius double-cover)
        R_perp = np.array([[0, -1], [1, 0]])
        R_perp_squared = R_perp @ R_perp
        mobius_verified = np.allclose(R_perp_squared, -np.eye(2))

        # Bridge period from golden ratio
        phi = (1 + np.sqrt(5)) / 2  # Golden ratio ~ 1.618
        bridge_period = 2 * np.pi * np.sqrt(phi)  # ~ 7.99

        # Breathing dark energy from b3 topology
        b3 = registry.get_param("topology.b3")
        w0_breathing = -1 + 1/b3  # = -23/24 for b3=24

        return {
            "dimensions.bulk_signature": (24, 1),
            "dimensions.shadow_signature": (12, 1),  # v22: 12 spatial + 1 shared time = 13D
            "dimensions.bridge_structure": "12×(2,0)",  # v22: 12 bridge pairs
            "dimensions.n_bridge_pairs": n_bridge_pairs,
            "dimensions.or_operator_property": "R_perp^2 = -I (Mobius)",
            "dimensions.mobius_verified": mobius_verified,
            "dimensions.bridge_period": bridge_period,
            "dimensions.breathing_w0": w0_breathing,
            "dimensions.D_bulk": D_bulk,  # v22: 25D not 26D
            "dimensions.g2_dimensions": g2_dimensions,
            "dimensions.shadow_total": shadow_total,  # v22: 13D per shadow
        }

    def get_section_content(self) -> Optional[SectionContent]:
        """
        Return section content for Appendix F - v21 Dimensional Decomposition.

        Returns:
            SectionContent with dimensional reduction derivation
        """
        return SectionContent(
            section_id="2",
            subsection_id="F",
            appendix=True,
            title="Appendix F: v22 Dimensional Decomposition (12×(2,0) Bridge Architecture)",
            abstract=(
                "v22 mathematical framework: 27D(26,1) = 12×(2,0) bridge pairs + (0,1) shared time. "
                "The 12 Euclidean bridge pairs WARP to create dual 13D(12,1) shadows via coordinate selection. "
                "Each (x_i, y_i) pair contributes x_i → Normal shadow, y_i → Mirror shadow. "
                "Breathing dark energy emerges from bridge pressure mismatch."
            ),
            content_blocks=[
                ContentBlock(
                    type="subsection",
                    content="F.1 Critical Dimension and Unified Time"
                ),
                ContentBlock(
                    type="paragraph",
                    content=(
                        "The bosonic string requires D = 26 spacetime dimensions for conformal "
                        "anomaly cancellation. In the v21 framework, this has unified time signature "
                        "(24,1) with 24 spacelike and 1 timelike direction, eliminating the ghost modes "
                        "and closed timelike curves that would arise from two-time physics."
                    )
                ),
                ContentBlock(
                    type="formula",
                    content=r"ds^2 = \sum_{i=1}^{24} dx_i^2 - dt^2",
                    formula_id="v21-unified-time-metric",
                    label="(F.1)"
                ),
                ContentBlock(
                    type="paragraph",
                    content=(
                        "The metric has signature (24,1) with coordinates (x^i, t) where t is the "
                        "single unified time coordinate. This structure ensures manifest unitarity and "
                        "positive-norm states throughout the quantum theory."
                    )
                ),
                ContentBlock(
                    type="subsection",
                    content="F.2 Dual-Shadow Split"
                ),
                ContentBlock(
                    type="paragraph",
                    content=(
                        "The 26D bulk with (24,1) signature splits into dual 'shadow' spacetimes "
                        "connected by a 2D Euclidean bridge:"
                    )
                ),
                ContentBlock(
                    type="formula",
                    content=r"25D_{(24,1)} = 12 \times (2,0) + (0,1) \xrightarrow{R_\perp} 2 \times 13D_{(12,1)}",
                    formula_id="v22-bridge-to-shadow-warp",
                    label="(F.2)"
                ),
                ContentBlock(
                    type="paragraph",
                    content=(
                        "v22: The 12×(2,0) bridge pairs WARP to create dual shadows via coordinate selection. "
                        "Each (x_i, y_i) pair contributes: x_i → Normal shadow, y_i → Mirror shadow. "
                        "Result: Each shadow gets 12 spatial + 1 shared time = 13D(12,1)."
                    )
                ),
                ContentBlock(
                    type="subsection",
                    content="F.3 The Euclidean Bridge"
                ),
                ContentBlock(
                    type="paragraph",
                    content=(
                        "v22: The 12×(2,0) bridge has 12 Euclidean pairs, each with positive-definite metric:"
                    )
                ),
                ContentBlock(
                    type="formula",
                    content=r"ds^2_{\text{bridge}} = \sum_{i=1}^{12} (dx_i^2 + dy_i^2)",
                    formula_id="v22-euclidean-bridge-metric",
                    label="(F.3)"
                ),
                ContentBlock(
                    type="paragraph",
                    content=(
                        "Key properties of the 12×(2,0) bridge pairs:\n"
                        "- **12 Euclidean pairs**: Each (x_i, y_i) spans 2D with positive-definite metric\n"
                        "- **Coordinate selection**: x_i → Normal shadow, y_i → Mirror shadow\n"
                        "- **Bridge creates shadows**: Bridge pairs WARP to become shadow dimensions\n"
                        "- **Golden scaling**: Period L = 2*pi*sqrt(phi) ~ 7.99"
                    )
                ),
                ContentBlock(
                    type="subsection",
                    content="F.4 OR Reduction Operator"
                ),
                ContentBlock(
                    type="paragraph",
                    content=(
                        "Cross-shadow coordinate sampling uses the Orthogonal Reduction operator R_perp, "
                        "which provides a 90-degree rotation between shadow coordinate systems:"
                    )
                ),
                ContentBlock(
                    type="formula",
                    content=r"R_\perp = \begin{pmatrix} 0 & -1 \\ 1 & 0 \end{pmatrix}",
                    formula_id="v21-or-reduction-operator",
                    label="(F.4)"
                ),
                ContentBlock(
                    type="paragraph",
                    content=(
                        "The OR operator has the critical Mobius property:"
                    )
                ),
                ContentBlock(
                    type="formula",
                    content=r"R_\perp^2 = -I \quad \text{(Mobius double-cover)}",
                    formula_id="v21-mobius-property",
                    label="(F.5)"
                ),
                ContentBlock(
                    type="paragraph",
                    content=(
                        "This Mobius property provides spinor double-cover:\n"
                        "- Single traversal: psi -> -psi (sign flip)\n"
                        "- Double traversal: psi -> psi (identity return)\n\n"
                        "This ensures spinor coherence across the dual-shadow structure, with fermions "
                        "requiring two bridge cycles for identity return."
                    )
                ),
                ContentBlock(
                    type="subsection",
                    content="F.5 Per-Shadow G2 Compactification"
                ),
                ContentBlock(
                    type="paragraph",
                    content=(
                        "Each shadow independently compactifies on a G2 manifold (7,0):"
                    )
                ),
                ContentBlock(
                    type="formula",
                    content=r"\text{Shadow}_{13D(12,1)} \rightarrow M^4_{(3,1)} \times G_2(7) \times \text{fiber}",
                    label="(F.6)"
                ),
                ContentBlock(
                    type="paragraph",
                    content=(
                        "The G2 manifold is Riemannian (all positive eigenvalues) with b3 = 24 "
                        "associative 3-cycles, split symmetrically: 12 cycles per shadow."
                    )
                ),
                ContentBlock(
                    type="subsection",
                    content="F.6 Breathing Dark Energy"
                ),
                ContentBlock(
                    type="paragraph",
                    content=(
                        "The bridge pressure arises from condensate flux mismatch between shadows. "
                        "This drives the breathing dark energy with equation of state:"
                    )
                ),
                ContentBlock(
                    type="formula",
                    content=r"w_0 = -1 + \frac{1}{b_3} = -1 + \frac{1}{24} = -\frac{23}{24} \approx -0.9583",
                    formula_id="v21-breathing-dark-energy",
                    label="(F.7)"
                ),
                ContentBlock(
                    type="paragraph",
                    content=(
                        "This prediction matches the DESI 2025 measurement (w0 = -0.957 +/- 0.067) "
                        "to within 0.02 sigma - essentially an exact match."
                    )
                ),
                ContentBlock(
                    type="subsection",
                    content="F.7 Comparison: v21 vs v16 (Two-Time)"
                ),
                ContentBlock(
                    type="paragraph",
                    content=(
                        "The v21 framework differs fundamentally from the v16 two-time approach:\n\n"
                        "| Feature | v16 (24,2) | v21 (24,1) |\n"
                        "|---------|-----------|------------|\n"
                        "| Time signature | Two times | Unified time |\n"
                        "| Ghost modes | Require Sp(2,R) elimination | None (manifest unitarity) |\n"
                        "| Shadow structure | Single 13D | Dual 13D(12,1) + bridge |\n"
                        "| Bridge mechanism | Sp(2,R) gauge | Euclidean (2,0) |\n"
                        "| Spinor return | Not explicit | Mobius R^2 = -I |\n"
                        "| Dark energy | Vacuum energy | Bridge pressure |\n"
                    )
                ),
                ContentBlock(
                    type="subsection",
                    content="F.8 Simulation Code"
                ),
                ContentBlock(
                    type="code",
                    content="""# v21_dimensional_decomposition.py
import numpy as np

def v21_dimensional_reduction() -> dict:
    \"\"\"Calculate v21 dimensional decomposition from (24,1) to dual shadows + bridge.

    Returns:
        Dictionary with dimensional reduction chain
    \"\"\"
    # Critical dimension
    D_critical = 26

    # v22: 27D(26,1) = 12×(2,0) bridge pairs + (0,1) shared time
    bulk_space = 24
    bulk_time = 1
    bulk_signature = (bulk_space, bulk_time)

    # v22: 12×(2,0) bridge pairs WARP to create dual shadows
    n_bridge_pairs = 12
    shadow_space = 12  # Each shadow gets 12 spatial from coordinate selection
    shadow_time = 1    # Shared time
    shadow_signature = (shadow_space, shadow_time)  # 13D(12,1) per shadow

    # 12×(2,0) Euclidean bridge pairs
    bridge_dims_per_pair = 2  # Each (x_i, y_i) has 2D
    bridge_signature = "12×(2,0)"  # 12 Euclidean pairs

    # OR reduction operator
    R_perp = np.array([[0, -1], [1, 0]])
    R_perp_sq = R_perp @ R_perp
    mobius_verified = np.allclose(R_perp_sq, -np.eye(2))

    # Bridge period from golden ratio
    phi = (1 + np.sqrt(5)) / 2
    bridge_period = 2 * np.pi * np.sqrt(phi)  # ~ 7.99

    # Breathing dark energy
    b3 = 24
    w0_breathing = -1 + 1/b3  # = -23/24

    # Per-shadow G2 compactification
    phys_spatial = 3
    phys_time = 1
    g2_dim = 7

    # Verify: 3 + 7 + 1 + 1 = 12 + 1 = 13D per shadow
    # (3 physical + 7 G2 + 1 fiber + 1 time from shadow = 12 + 1)
    assert phys_spatial + g2_dim + 1 + 1 == shadow_space + shadow_time

    return {
        'bulk_signature': bulk_signature,
        'shadow_signature': shadow_signature,
        'bridge_signature': bridge_signature,
        'R_perp_mobius': mobius_verified,
        'bridge_period': bridge_period,
        'w0_breathing': w0_breathing,
        'g2_dimensions': g2_dim,
    }

# Result: w0 = -23/24 = -0.9583 (matches DESI 2025 at 0.02 sigma)""",
                    language="python",
                    label="Python code for v21 dimensional decomposition"
                ),
            ],
            formula_refs=[
                "v21-unified-time-metric",
                "v21-dual-shadow-split",
                "v21-euclidean-bridge-metric",
                "v21-or-reduction-operator",
                "v21-mobius-property",
                "v21-breathing-dark-energy",
            ],
            param_refs=[
                "dimensions.bulk_signature",
                "dimensions.shadow_signature",
                "dimensions.bridge_signature",
                "topology.b3",
            ]
        )

    def get_formulas(self) -> List[Formula]:
        """
        Return list of formulas for v21 dimensional decomposition.

        Returns:
            List of Formula instances
        """
        return [
            Formula(
                id="v21-unified-time-metric",
                label="(F.1)",
                latex=r"ds^2 = \sum_{i=1}^{24} dx_i^2 - dt^2",
                plain_text="ds^2 = sum(dx_i^2) - dt^2 (signature (24,1))",
                category="FOUNDATIONAL",
                description=(
                    "v21 unified time metric with signature (24,1). Eliminates ghost modes "
                    "and closed timelike curves present in (24,2) two-time physics."
                ),
                input_params=[],
                output_params=["dimensions.bulk_signature"],
            ),
            Formula(
                id="v22-bridge-to-shadow-warp",
                label="(F.2)",
                latex=r"25D_{(24,1)} = 12 \times (2,0) + (0,1) \xrightarrow{R_\perp} 2 \times 13D_{(12,1)}",
                plain_text="27D(26,1) = 12×(2,0) + (0,1) → 2×13D(12,1)",
                category="FOUNDATIONAL",
                description=(
                    "v22: 12×(2,0) bridge pairs + (0,1) shared time WARP to create dual 13D(12,1) shadows. "
                    "Bridge pairs ARE the source of shadows via coordinate selection."
                ),
                input_params=["dimensions.bulk_signature"],
                output_params=["dimensions.shadow_signature", "dimensions.bridge_structure"],
            ),
            Formula(
                id="v22-euclidean-bridge-metric",
                label="(F.3)",
                latex=r"ds^2_{\text{bridge}} = \sum_{i=1}^{12} (dx_i^2 + dy_i^2)",
                plain_text="ds^2_bridge = sum_i(dx_i^2 + dy_i^2) for i=1..12",
                category="FOUNDATIONAL",
                description=(
                    "v22: 12×(2,0) Euclidean bridge metric. Each (x_i, y_i) pair has positive-definite "
                    "metric. Coordinate selection: x_i → Normal shadow, y_i → Mirror shadow."
                ),
                input_params=[],
                output_params=["dimensions.bridge_structure"],
            ),
            Formula(
                id="v21-or-reduction-operator",
                label="(F.4)",
                latex=r"R_\perp = \begin{pmatrix} 0 & -1 \\ 1 & 0 \end{pmatrix}",
                plain_text="R_perp = [[0, -1], [1, 0]]",
                category="FOUNDATIONAL",
                description=(
                    "OR Reduction operator for cross-shadow coordinate mapping. "
                    "Performs 90-degree rotation with determinant 1 (orientation-preserving)."
                ),
                input_params=[],
                output_params=["dimensions.or_operator_property"],
            ),
            Formula(
                id="v21-mobius-property",
                label="(F.5)",
                latex=r"R_\perp^2 = -I \quad \text{(Mobius double-cover)}",
                plain_text="R_perp^2 = -I (Mobius double-cover)",
                category="DERIVED",
                description=(
                    "Mobius property of OR operator: R_perp^2 = -I. Provides spinor double-cover "
                    "ensuring fermion coherence across bridge cycles."
                ),
                input_params=[],
                output_params=[],
                terms={
                    "R_perp": "OR Reduction operator",
                    "-I": "Negative identity matrix",
                    "Mobius": "Double-cover property for spinors",
                },
            ),
            Formula(
                id="v21-breathing-dark-energy",
                label="(F.7)",
                latex=r"w_0 = -1 + \frac{1}{b_3} = -\frac{23}{24} \approx -0.9583",
                plain_text="w0 = -1 + 1/b3 = -23/24 = -0.9583",
                category="DERIVED",
                description=(
                    "Breathing dark energy equation of state from bridge pressure mismatch. "
                    "Matches DESI 2025 measurement at 0.02 sigma."
                ),
                input_params=["topology.b3"],
                output_params=["dimensions.breathing_w0"],
            ),
        ]

    def get_output_param_definitions(self) -> List[Parameter]:
        """
        Return parameter definitions for v21 dimensional decomposition outputs.

        Returns:
            List of Parameter instances
        """
        return [
            Parameter(
                path="dimensions.bulk_signature",
                name="v21 Bulk Spacetime Signature",
                units="dimensionless",
                status="FOUNDATIONAL",
                description="Signature (24,1) of v21 unified time bosonic string spacetime",
                no_experimental_value=True,
            ),
            Parameter(
                path="dimensions.shadow_signature",
                name="Per-Shadow Spacetime Signature",
                units="dimensionless",
                status="DERIVED",
                description="Signature (10,1) per dual shadow in v21 framework",
                no_experimental_value=True,
            ),
            Parameter(
                path="dimensions.bridge_signature",
                name="Euclidean Bridge Signature",
                units="dimensionless",
                status="DERIVED",
                description="Signature (2,0) of positive-definite Euclidean bridge",
                no_experimental_value=True,
            ),
            Parameter(
                path="dimensions.or_operator_property",
                name="OR Operator Mobius Property",
                units="dimensionless",
                status="DERIVED",
                description="R_perp^2 = -I Mobius double-cover property",
                no_experimental_value=True,
            ),
            Parameter(
                path="dimensions.bridge_period",
                name="Bridge Period",
                units="Planck lengths",
                status="DERIVED",
                description="Bridge period L = 2*pi*sqrt(phi) ~ 7.99 from golden ratio",
                no_experimental_value=True,
            ),
            Parameter(
                path="dimensions.breathing_w0",
                name="Breathing Dark Energy w0",
                units="dimensionless",
                status="DERIVED",
                description="w0 = -1 + 1/b3 = -23/24 from bridge pressure mismatch",
                experimental_bound=-0.957,
                bound_type="central",
                bound_source="DESI2025",
                uncertainty=0.067,
            ),
        ]


def main():
    """Run the appendix standalone for testing."""
    import io
    import sys

    # Ensure UTF-8 output encoding
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

    from simulations.base import PMRegistry
    from simulations.base.established import EstablishedPhysics

    # Create registry and load established physics
    registry = PMRegistry()
    EstablishedPhysics.load_into_registry(registry)

    # Add topology parameters if needed
    if not registry.has_param("topology.b3"):
        registry.set_param("topology.b3", 24)

    # Create and run appendix
    appendix = AppendixFDimensionalDecomposition()

    print("=" * 70)
    print(f" {appendix.metadata.title}")
    print("=" * 70)
    print(f"Appendix ID: {appendix.metadata.id}")
    print(f"Version: {appendix.metadata.version}")
    print(f"Section: {appendix.metadata.section_id}.{appendix.metadata.subsection_id}")
    print()

    # Execute
    results = appendix.execute(registry, verbose=True)

    # Print results
    print("\n" + "=" * 70)
    print(" v21 DIMENSIONAL DECOMPOSITION")
    print("=" * 70)
    print(f"Bulk Signature: {results.get('dimensions.bulk_signature', (0,0))}")
    print(f"Shadow Signature: {results.get('dimensions.shadow_signature', (0,0))}")
    print(f"Bridge Signature: {results.get('dimensions.bridge_signature', (0,0))}")
    print(f"Mobius Verified: {results.get('dimensions.mobius_verified', False)}")
    print(f"Bridge Period: {results.get('dimensions.bridge_period', 0):.4f}")
    print(f"Breathing w0: {results.get('dimensions.breathing_w0', 0):.6f}")
    print(f"G2 Dimensions: {results.get('dimensions.g2_dimensions', 0)}")
    print()


if __name__ == "__main__":
    main()
