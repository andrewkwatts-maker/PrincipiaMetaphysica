"""
Faraday Constant Derivation v17.2
=================================

The Faraday Constant uses INVERSE CUBIC PROJECTION 1/(1+epsilon)
because F = N_A * e, and since e is invariant, F follows N_A's adjustment.

CODATA 2022: F = 96485.33212 C mol^-1

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
CODATA_FARADAY = 96485.33212  # C mol^-1


class FaradayV17(SimulationBase):
    """Faraday Constant derivation using Inverse Cubic Projection."""

    def __init__(self):
        self.bulk_f = None
        self.manifest_f = None
        self.variance = None

    @property
    def metadata(self) -> SimulationMetadata:
        return SimulationMetadata(
            id="faraday_v17_2", version="17.2", domain="qed",
            title="Faraday from Inverse Cubic",
            description="F = N_A * e, follows N_A's adjustment since e is invariant.",
            section_id="6", subsection_id="6.7"
        )

    @property
    def required_inputs(self) -> List[str]:
        return ["topology.b3"]

    @property
    def output_params(self) -> List[str]:
        return ["qed.bulk_faraday", "qed.manifest_faraday"]

    @property
    def output_formulas(self) -> List[str]:
        return ["faraday-inverse-cubic"]

    def run(self, registry: PMRegistry) -> Dict[str, Any]:
        self.bulk_f = _REG.bulk_faraday
        self.manifest_f = _REG.manifest_faraday
        self.variance = abs(self.manifest_f - CODATA_FARADAY)
        return {
            "qed.bulk_faraday": self.bulk_f,
            "qed.manifest_faraday": self.manifest_f,
        }

    def validate(self) -> bool:
        return self.variance < 1e-5 if self.variance is not None else False

    def get_section_content(self) -> Optional[SectionContent]:
        return SectionContent(
            section_id="6",
            subsection_id="6.7",
            title="Faraday Constant",
            abstract="Derives the Faraday constant using inverse cubic 1/(1+epsilon) contraction.",
            content_blocks=[
                ContentBlock(type="equation", content=r"F = F_{bulk} / (1+\epsilon)")
            ]
        )

    def get_formulas(self) -> List[Formula]:
        return [
            Formula(
                id="faraday-inverse-cubic",
                label="(6.7)",
                latex=r"F = F_{bulk}/(1+\epsilon)",
                plain_text="F = F_bulk / (1+epsilon)",
                category="DERIVED",
                description="Faraday constant follows Avogadro contraction",
            ),
        ]

    def get_output_param_definitions(self) -> List[Parameter]:
        return [
            Parameter(
                path="qed.bulk_faraday",
                name="Bulk Faraday Constant",
                units="C/mol",
                status="DERIVED",
                description="Faraday constant in bulk (before contraction)",
                no_experimental_value=True,
            ),
            Parameter(
                path="qed.manifest_faraday",
                name="Manifest Faraday Constant",
                units="C/mol",
                status="DERIVED",
                description="Faraday constant after 1/(1+epsilon) contraction",
                experimental_bound=CODATA_FARADAY,
                bound_type="measured",
                bound_source="CODATA2022",
            ),
        ]


if __name__ == "__main__":
    print("FARADAY CONSTANT v17.2 - Inverse Cubic")
    sim = FaradayV17()
    registry = PMRegistry()
    registry.set_param("topology.b3", _REG.governing_elder_kad, source="ESTABLISHED:FormulasRegistry")
    sim.run(registry)
    print(f"CODATA:   {CODATA_FARADAY:.10f} C/mol")
    print(f"Bulk:     {sim.bulk_f:.10f} C/mol")
    print(f"Manifest: {sim.manifest_f:.10f} C/mol")
    print(f"Valid:    {sim.validate()}")
