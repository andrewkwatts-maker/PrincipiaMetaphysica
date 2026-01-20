"""
Weak Mixing Angle Derivation v17.2
==================================

The Weak Mixing Angle uses INVERSE CUBIC (Torsion Gate) 1/(1+epsilon)
because sin^2(theta_W) is a coupling ratio that contracts.

CODATA/SM Value: sin^2(theta_W) = 0.23121 (at Z-pole)

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.
"""

from typing import Dict, Any, List, Optional
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..'))

from simulations.base import (
    SimulationBase, SimulationMetadata, ContentBlock, SectionContent, Formula, Parameter, PMRegistry,
)
from core.FormulasRegistry import get_registry

_REG = get_registry()
CODATA_WEAK = 0.23121  # sin^2(theta_W) at Z-pole


class WeakMixingV17(SimulationBase):
    """Weak Mixing Angle derivation using Torsion Gate (Inverse Cubic)."""

    def __init__(self):
        self.bulk_weak = None
        self.manifest_weak = None
        self.variance = None

    @property
    def metadata(self) -> SimulationMetadata:
        return SimulationMetadata(
            id="weak_mixing_v17_2", version="17.2", domain="qed",
            title="Weak Mixing Angle from Torsion Gate",
            description="sin^2(theta_W) contracts because it's a coupling ratio.",
            section_id="6", subsection_id="6.9"
        )

    @property
    def required_inputs(self) -> List[str]:
        return ["topology.b3"]

    @property
    def output_params(self) -> List[str]:
        return ["qed.bulk_weak_mixing", "qed.manifest_weak_mixing"]

    @property
    def output_formulas(self) -> List[str]:
        return ["weak-mixing-torsion"]

    def run(self, registry: PMRegistry) -> Dict[str, Any]:
        self.bulk_weak = _REG.bulk_weak_mixing_angle
        self.manifest_weak = _REG.manifest_weak_mixing_angle
        self.variance = abs(self.manifest_weak - CODATA_WEAK)
        return {
            "qed.bulk_weak_mixing": self.bulk_weak,
            "qed.manifest_weak_mixing": self.manifest_weak,
        }

    def validate(self) -> bool:
        return self.variance < 1e-6 if self.variance is not None else False

    def get_section_content(self) -> Optional[SectionContent]:
        return SectionContent(
            section_id="6",
            subsection_id="6.9",
            title="Weak Mixing Angle",
            abstract="Derives the weak mixing angle using inverse cubic (Torsion Gate) contraction.",
            content_blocks=[
                ContentBlock(type="text", content=(
                    "The Weak Mixing Angle determines the ratio between W and Z bosons. "
                    "As a coupling ratio, it contracts via the Torsion Gate as the "
                    "3D grid expands, making the mixing slightly 'thinner'."
                )),
                ContentBlock(type="equation", content=r"\sin^2\theta_W = \sin^2\theta_{W,bulk} / (1+\epsilon)")
            ]
        )

    def get_formulas(self) -> List[Formula]:
        return [
            Formula(
                id="weak-mixing-torsion",
                label="(6.9)",
                latex=r"\sin^2\theta_W = \sin^2\theta_{W,bulk}/(1+\epsilon)",
                plain_text="sin^2(theta_W) = sin^2(theta_W_bulk) / (1+epsilon)",
                category="DERIVED",
                description="Weak mixing angle contracts via Torsion Gate",
            ),
        ]

    def get_output_param_definitions(self) -> List[Parameter]:
        return [
            Parameter(
                path="qed.bulk_weak_mixing",
                name="Bulk Weak Mixing Angle",
                units="dimensionless",
                status="DERIVED",
                description="sin^2(theta_W) in bulk (before Torsion Gate)",
                no_experimental_value=True,
            ),
            Parameter(
                path="qed.manifest_weak_mixing",
                name="Manifest Weak Mixing Angle",
                units="dimensionless",
                status="DERIVED",
                description="sin^2(theta_W) after 1/(1+epsilon) Torsion Gate contraction",
                experimental_bound=CODATA_WEAK,
                bound_type="measured",
                bound_source="PDG2024",
            ),
        ]


if __name__ == "__main__":
    print("WEAK MIXING ANGLE v17.2 - Torsion Gate")
    sim = WeakMixingV17()
    registry = PMRegistry()
    registry.set_param("topology.b3", _REG.b3, source="ESTABLISHED:FormulasRegistry")
    sim.run(registry)
    print(f"Target:   {CODATA_WEAK:.10f}")
    print(f"Bulk:     {sim.bulk_weak:.10f}")
    print(f"Manifest: {sim.manifest_weak:.10f}")
    print(f"Variance: {sim.variance:.10e}")
    print(f"Valid:    {sim.validate()}")
