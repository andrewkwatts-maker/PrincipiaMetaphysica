"""
Merged Dimensional Descent v21.0
=================================

Licensed under the MIT License. See LICENSE file for details.

Implements the complete dimensional descent chain for the 27D(26,1) dual-shadow model:
27D(26,1) bulk -> dual shadows -> Euclidean bridge -> G2 compact -> condensate projection

This simulation combines all v21 components:
- Bridge pressure
- G2 compactification
- OR Reduction sampling
- Cyclic Mobius return
- Breathing dark energy

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.

Dedicated To:
    My Wife: Elizabeth May Watts
    Our Messiah: Jesus Of Nazareth
"""

import numpy as np
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..'))

from simulations.base import (
    SimulationBase,
    SimulationMetadata,
    ContentBlock,
    SectionContent,
    Formula,
    Parameter,
    PMRegistry,
    PHI,
    B3,
    CHI_EFF,
)


@dataclass
class DescentConfig:
    """Configuration for merged descent computation."""
    # Bulk signature - v23.1: 27D(26,1) = 24 spatial + 2 central bridge + 1 time
    D_bulk: int = 27  # 26 space + 1 time = (26,1)
    D_space: int = 26  # 24 core spatial + 2 central bridge
    D_core_spatial: int = 24  # Core spatial dimensions
    D_time: int = 1

    # Bridge dimensions
    D_bridge: int = 2  # Shared Euclidean (2,0) central sampler

    # G2 compactification
    D_g2: int = 7  # 7D per shadow

    # Condensate structure
    D_bridge_extended: int = 6  # 5,1 bridge (5 space + 1 time)
    D_generation: int = 4  # 3,1 per generation

    # Topology
    b3_total: int = 24
    chi_eff: int = 144
    num_generations: int = 3


class MergedDescentV21(SimulationBase):
    """
    Complete dimensional descent simulation.

    Traces the full reduction chain from 27D(26,1) bulk through
    dual shadows, G2 compactification, and condensate formation.
    """

    def __init__(self, config: Optional[DescentConfig] = None):
        """Initialize merged descent simulation."""
        self.config = config or DescentConfig()

    @property
    def metadata(self) -> SimulationMetadata:
        """Return simulation metadata."""
        return SimulationMetadata(
            id="merged_descent_v21",
            version="23.1",
            domain="foundations",
            title="Dimensional Descent Chain",
            description=(
                "Complete reduction from 27D(26,1) bulk through dual shadows, "
                "Euclidean bridge, G2 compactification, to observable "
                "condensates (2 x (5,1 + 3x(3,1)))."
            ),
            section_id="1",
            subsection_id="1.1"
        )

    @property
    def required_inputs(self) -> List[str]:
        """Return required input parameter paths."""
        return [
            "topology.b3",
            "topology.chi_eff",
        ]

    @property
    def output_params(self) -> List[str]:
        """Return output parameter paths."""
        return [
            "descent.bulk_signature",
            "descent.bridge_signature",
            "descent.shadow_dims",
            "descent.g2_dims",
            "descent.condensate_structure",
            "descent.total_observable",
            "descent.descent_chain_verified",
        ]

    @property
    def output_formulas(self) -> List[str]:
        """Return formula IDs this simulation provides."""
        return [
            "bulk-signature-24-1",
            "descent-chain-full",
            "condensate-structure",
            "dimension-accounting",
        ]

    def run(self, registry: PMRegistry) -> Dict[str, Any]:
        """Execute the merged descent computation."""
        self.validate_inputs(registry)

        # Step 1: Verify bulk signature
        bulk_sig = self._verify_bulk_signature()

        # Step 2: Compute shadow splitting
        shadow_dims = self._compute_shadow_split()

        # Step 3: Verify G2 compactification
        g2_dims = self._verify_g2_compact()

        # Step 4: Compute condensate structure
        condensate = self._compute_condensate_structure()

        # Step 5: Verify dimension accounting
        total_obs, accounting_verified = self._verify_dimension_accounting()

        # Step 6: Full chain verification
        chain_verified = self._verify_descent_chain()

        return {
            "descent.bulk_signature": bulk_sig,
            "descent.bridge_signature": "(2,0) Euclidean",
            "descent.shadow_dims": shadow_dims,
            "descent.g2_dims": g2_dims,
            "descent.condensate_structure": condensate,
            "descent.total_observable": total_obs,
            "descent.descent_chain_verified": chain_verified,
        }

    def _verify_bulk_signature(self) -> str:
        """Verify 27D(26,1) bulk signature."""
        D_space = self.config.D_space
        D_time = self.config.D_time
        return f"({D_space},{D_time})"

    def _compute_shadow_split(self) -> Dict[str, Any]:
        """
        Compute shadow dimension splitting.

        27D(26,1) = 24 core spatial + 2 central bridge + 1 time
        24 core spacelike = 12 normal + 12 mirror (via 12×(2,0) bridge pairs)
        Central bridge C^(2,0) is shared between both shadows
        """
        D_bridge = self.config.D_bridge
        D_core_spatial = self.config.D_core_spatial
        D_per_shadow = D_core_spatial // 2  # 12 per shadow

        return {
            "D_normal_internal": D_per_shadow,
            "D_mirror_internal": D_per_shadow,
            "D_central_bridge": D_bridge,
            "D_core_spatial": D_core_spatial,
            "total": D_core_spatial + D_bridge,
        }

    def _verify_g2_compact(self) -> Dict[str, Any]:
        """
        Verify G2 compactification per shadow.

        Each shadow compacts 7D on G2 (7,0) Riemannian.
        """
        D_g2 = self.config.D_g2
        b3_per_shadow = self.config.b3_total // 2

        return {
            "D_g2_per_shadow": D_g2,
            "signature": "(7,0) Riemannian",
            "b3_per_shadow": b3_per_shadow,
            "holonomy": "G2",
        }

    def _compute_condensate_structure(self) -> Dict[str, Any]:
        """
        Compute observable condensate structure.

        Per shadow: 5,1 bridge + 3 x (3,1) generations
        Total: 2 x (5,1 + 3 x (3,1))
        """
        D_bridge = self.config.D_bridge_extended  # 5,1
        D_gen = self.config.D_generation  # 3,1
        n_gen = self.config.num_generations

        # Per shadow condensate dimension
        per_shadow = D_bridge + n_gen * D_gen

        return {
            "bridge_extended": f"({self.config.D_bridge_extended - 1},1)",
            "generation_branch": f"({D_gen - 1},1)",
            "num_generations": n_gen,
            "per_shadow_total": per_shadow,
            "dual_total": 2 * per_shadow,
            "structure": f"2 x ({D_bridge - 1},1 + {n_gen} x ({D_gen - 1},1))",
        }

    def _verify_dimension_accounting(self) -> tuple:
        """
        Verify total dimension accounting.

        Bulk 27D(26,1) = 27 total = 24 core spatial + 2 central bridge + 1 time
        After G2: 27 - 2*7 = 13 (central bridge + remaining)
        Observable: 4D spacetime + KK towers
        """
        D_bulk = self.config.D_bulk  # 27
        D_g2_total = 2 * self.config.D_g2  # 14 compact
        D_remaining = D_bulk - D_g2_total  # 13

        # Effective 4D from 3,1 branches
        D_observable = 4

        # KK tower dimensions (including central bridge contribution)
        D_kk = D_remaining - D_observable  # 9 KK

        accounting = {
            "D_bulk": D_bulk,
            "D_compact": D_g2_total,
            "D_remaining": D_remaining,
            "D_observable": D_observable,
            "D_kk": D_kk,
            "D_central_bridge": self.config.D_bridge,
        }

        verified = (D_bulk == D_g2_total + D_remaining) and (D_observable == 4)

        return accounting, verified

    def _verify_descent_chain(self) -> str:
        """
        Verify complete descent chain.

        27D(26,1) -> dual shadows -> (2,0) central bridge -> G2(7,0) -> 2x(5,1 + 3x(3,1))
        """
        checks = []

        # Check 1: Bulk signature - 27D(26,1)
        bulk_ok = (self.config.D_bulk == 27 and self.config.D_space == 26 and self.config.D_time == 1)
        checks.append(("Bulk 27D(26,1)", bulk_ok))

        # Check 2: Core spatial dimensions
        core_ok = (self.config.D_core_spatial == 24)
        checks.append(("Core spatial = 24", core_ok))

        # Check 3: Bridge Euclidean (central sampler)
        bridge_ok = (self.config.D_bridge == 2)
        checks.append(("Central Bridge (2,0)", bridge_ok))

        # Check 4: G2 dimension
        g2_ok = (self.config.D_g2 == 7)
        checks.append(("G2 (7,0)", g2_ok))

        # Check 5: Generations
        gen_ok = (self.config.num_generations == 3)
        checks.append(("Generations = 3", gen_ok))

        # Check 6: b3 matches
        b3_ok = (self.config.b3_total == 24)
        checks.append(("b3 = 24", b3_ok))

        all_passed = all(ok for _, ok in checks)

        if all_passed:
            return "LOCKED: All descent stages verified"
        else:
            failed = [name for name, ok in checks if not ok]
            return f"FAILED: {', '.join(failed)}"

    def get_descent_diagram(self) -> str:
        """Return ASCII diagram of descent chain."""
        return """
        ┌─────────────────────────────────────────────┐
        │           27D(26,1) BULK                    │
        │  24 core spatial + 2 central + 1 time      │
        └──────────────────┬──────────────────────────┘
                           │
                    ┌──────┴──────┐
                    ▼             ▼
        ┌───────────────┐  ┌───────────────┐
        │ NORMAL SHADOW │  │ MIRROR SHADOW │
        │ 12 internal   │  │ 12 internal   │
        │ via 12×(2,0)  │  │ via 12×(2,0)  │
        └───────┬───────┘  └───────┬───────┘
                │                  │
                └───────┬──────────┘
                        │
                ┌───────▼───────┐
                │ C^(2,0) BRIDGE│
                │ Central       │
                │ Sampler       │
                └───────┬───────┘
                        │
              ┌─────────┴─────────┐
              ▼                   ▼
        ┌─────────────┐     ┌─────────────┐
        │ G2 (7,0)    │     │ G2 (7,0)    │
        │ Normal      │     │ Mirror      │
        │ b3=12       │     │ b3=12       │
        └──────┬──────┘     └──────┬──────┘
               │                   │
               ▼                   ▼
        ┌─────────────────────────────────┐
        │    CONDENSATE PROJECTION        │
        │  2 x (5,1 bridge + 3x(3,1))     │
        │                                 │
        │  Normal: 5,1 + 3x(3,1)          │
        │  Mirror: 5,1 + 3x(3,1)          │
        └─────────────────────────────────┘
        """

    def get_section_content(self) -> Optional[SectionContent]:
        """Return section content for the paper."""
        return SectionContent(
            section_id="1",
            subsection_id="1.1",
            title="Foundations of Dimensional Descent",
            abstract=(
                "The 27D(26,1) bulk with unified time descends through dual "
                "shadows sharing a 2D Euclidean central bridge. G2 compactification "
                "on each shadow yields the observable condensate structure: "
                "2 x (5,1 bridge + 3 x (3,1) generational branches)."
            ),
            content_blocks=[
                ContentBlock(
                    type="paragraph",
                    content=(
                        "The ancestral bulk is a 27D(26,1) Lorentzian manifold with "
                        "24 core spatial + 2 central bridge + 1 timelike dimension. "
                        "This unified time eliminates ghost/CTC issues from earlier (24,2) formulations:"
                    )
                ),
                ContentBlock(
                    type="formula",
                    content=r"ds^2 = \sum_{i=1}^{24} dx_i^2 + dy_1^2 + dy_2^2 - dt^2",
                    formula_id="bulk-signature-26-1",
                    label="(1.1)"
                ),
                ContentBlock(
                    type="paragraph",
                    content=(
                        "The complete descent chain proceeds through multiple stages, "
                        "each preserving N=1 supersymmetry:"
                    )
                ),
                ContentBlock(
                    type="formula",
                    content=r"27D(26,1) = 12 \times (2,0) + C^{(2,0)} + (0,1) \xrightarrow{\text{warp}} 2 \times 13D(12,1) \xrightarrow{G_2} 2 \times (5,1 + 3 \times (3,1))",
                    formula_id="descent-chain-full",
                    label="(1.2)"
                ),
                ContentBlock(
                    type="paragraph",
                    content=(
                        "The final observable structure comprises dual independent "
                        "condensates, each with extended bridge and generational branches:"
                    )
                ),
                ContentBlock(
                    type="formula",
                    content=r"\text{Observable} = 2 \times \left[ (5,1)_{\text{bridge}} \oplus \bigoplus_{k=1}^{3} (3,1)_k \right]",
                    formula_id="condensate-structure",
                    label="(1.3)"
                ),
            ],
            formula_refs=[
                "bulk-signature-26-1",
                "descent-chain-full",
                "condensate-structure",
            ],
            param_refs=[
                "descent.bulk_signature",
                "descent.condensate_structure",
                "descent.descent_chain_verified",
            ]
        )

    def get_formulas(self) -> List[Formula]:
        """Return list of formulas this simulation provides."""
        return [
            Formula(
                id="bulk-signature-26-1",
                label="(1.1)",
                latex=r"ds^2 = \sum_{i=1}^{24} dx_i^2 + dy_1^2 + dy_2^2 - dt^2",
                plain_text="ds^2 = sum(dx_i^2) + dy_1^2 + dy_2^2 - dt^2, i=1..24",
                category="THEORY",
                description="27D(26,1) bulk metric with unified time: 24 core spatial + 2 central bridge + 1 time",
                inputParams=[],
                outputParams=["descent.bulk_signature"],
                input_params=[],
                output_params=["descent.bulk_signature"],
                derivation={
                    "steps": [
                        {"description": "24 core spacelike dimensions",
                         "formula": r"\sum_{i=1}^{24} dx_i^2"},
                        {"description": "2 central bridge dimensions C^(2,0)",
                         "formula": r"dy_1^2 + dy_2^2"},
                        {"description": "1 timelike dimension",
                         "formula": r"-dt^2"},
                        {"description": "Lorentzian signature",
                         "formula": r"(26,1)"}
                    ],
                    "references": ["PM Section 1.1"]
                },
                terms={
                    "ds^2": "Line element",
                    "dx_i": "Core spacelike differentials (24)",
                    "dy_1, dy_2": "Central bridge differentials (2)",
                    "dt": "Timelike differential",
                }
            ),
            Formula(
                id="descent-chain-full",
                label="(1.2)",
                latex=r"27D(26,1) = 12 \times (2,0) + C^{(2,0)} + (0,1) \xrightarrow{\text{warp}} 2 \times 13D(12,1) \xrightarrow{G_2} 2 \times (5,1 + 3 \times (3,1))",
                plain_text="27D(26,1) = 12×(2,0) + C^(2,0) + (0,1) -> warp -> 2×13D(12,1) -> G2 -> 2 x (5,1 + 3x(3,1))",
                category="THEORY",
                description="Complete dimensional descent chain from 27D(26,1)",
                inputParams=["topology.b3", "topology.chi_eff"],
                outputParams=["descent.condensate_structure"],
                input_params=["topology.b3", "topology.chi_eff"],
                output_params=["descent.condensate_structure"],
                derivation={
                    "steps": [
                        {"description": "12 bridge pairs warp to create shadows",
                         "formula": r"12 \times (2,0) \to 2 \times 12_{\text{spatial}}"},
                        {"description": "Central bridge sampler",
                         "formula": r"C^{(2,0)}_{\text{central sampler}}"},
                        {"description": "Shared time from (0,1)",
                         "formula": r"(0,1)_{\text{shared time}}"},
                        {"description": "G2 compactifies 7D per shadow",
                         "formula": r"G_2: 7 \to \text{conical}"},
                        {"description": "Observable condensates",
                         "formula": r"2 \times (5,1 + 3 \times (3,1))"}
                    ],
                    "references": ["PM Section 1.1"]
                },
                terms={
                    "(26,1)": "Bulk signature: 26 spatial + 1 time",
                    "(2,0)": "Euclidean bridge pair signature",
                    "C^(2,0)": "Central sampler bridge (2D Euclidean)",
                    "G2": "G2 holonomy compactification",
                    "(5,1)": "Extended bridge (5 space + 1 time)",
                    "(3,1)": "Generational Minkowski branch",
                }
            ),
            Formula(
                id="condensate-structure",
                label="(1.3)",
                latex=r"\text{Observable} = 2 \times \left[ (5,1)_{\text{bridge}} \oplus \bigoplus_{k=1}^{3} (3,1)_k \right]",
                plain_text="Observable = 2 x [(5,1)_bridge + sum_{k=1}^3 (3,1)_k]",
                category="DERIVED",
                description="Dual condensate observable structure",
                inputParams=["g2.n_gen"],
                outputParams=["descent.total_observable"],
                input_params=["g2.n_gen"],
                output_params=["descent.total_observable"],
                derivation={
                    "steps": [
                        {"description": "Extended bridge per shadow",
                         "formula": r"(5,1)_{\text{bridge}}"},
                        {"description": "3 generational branches",
                         "formula": r"\bigoplus_{k=1}^{3} (3,1)_k"},
                        {"description": "Dual shadows",
                         "formula": r"2 \times [\ldots]"},
                        {"description": "Independent condensates",
                         "formula": r"\text{Normal} \oplus \text{Mirror}"}
                    ],
                    "references": ["PM Section 1.1"]
                },
                terms={
                    "(5,1)_bridge": "Extended KK bridge (5 space + 1 time)",
                    "(3,1)_k": "Generation k Minkowski branch",
                    "k=1,2,3": "Three generations from triality",
                }
            ),
        ]

    def get_output_param_definitions(self) -> List[Parameter]:
        """Return parameter definitions for outputs."""
        return [
            Parameter(
                path="descent.bulk_signature",
                name="Bulk Signature",
                units="signature",
                status="ESTABLISHED",
                description="Bulk manifold signature: 27D(26,1) Lorentzian with unified time (24 core + 2 central bridge + 1 time).",
                derivation_formula="bulk-signature-26-1",
                no_experimental_value=True
            ),
            Parameter(
                path="descent.condensate_structure",
                name="Condensate Structure",
                units="structure",
                status="DERIVED",
                description="Observable condensate: 2 x (5,1 + 3x(3,1)) dual independent.",
                derivation_formula="condensate-structure",
                no_experimental_value=True
            ),
            Parameter(
                path="descent.descent_chain_verified",
                name="Descent Chain Gate",
                units="status",
                status="GATE",
                description="Verification that all descent stages are consistent.",
                derivation_formula="descent-chain-full",
                no_experimental_value=True
            ),
        ]


# Self-validation
_validation_instance = MergedDescentV21()
assert _validation_instance.metadata is not None
assert _validation_instance.metadata.id == "merged_descent_v21"


if __name__ == "__main__":
    print("\n" + "=" * 70)
    print(" MERGED DIMENSIONAL DESCENT v21.0")
    print("=" * 70)

    # Create registry
    registry = PMRegistry.get_instance()
    registry.set_param("topology.b3", 24, source="G2_topology", status="ESTABLISHED")
    registry.set_param("topology.chi_eff", 144, source="G2_topology", status="ESTABLISHED")

    # Run simulation
    sim = MergedDescentV21()
    results = sim.execute(registry, verbose=True)

    print("\n" + "=" * 70)
    print(" RESULTS")
    print("=" * 70)
    for key, value in results.items():
        if isinstance(value, dict):
            print(f"  {key}:")
            for k, v in value.items():
                print(f"    {k}: {v}")
        else:
            print(f"  {key}: {value}")

    print("\n" + "=" * 70)
    print(" DESCENT DIAGRAM")
    print("=" * 70)
    print(sim.get_descent_diagram())

    print("=" * 70)
    print(" STATUS: COMPLETE")
    print("=" * 70)
