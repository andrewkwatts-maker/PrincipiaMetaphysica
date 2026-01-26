"""
Avogadro Number Derivation v17.2
================================

The Avogadro Number uses INVERSE CUBIC PROJECTION 1/(1+epsilon)
because counts contract as space expands.

CODATA 2022: N_A = 6.02214076 x 10^23 mol^-1 (exact)

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.
"""

from typing import Dict, Any, List, Optional
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..'))

from simulations.base import (
    SimulationBase, SimulationMetadata, ContentBlock, SectionContent, Formula, Parameter, PMRegistry,
)
from simulations.core.FormulasRegistry import get_registry

_REG = get_registry()
CODATA_NA = 6.02214076e23  # mol^-1 (exact)


class AvogadroV17(SimulationBase):
    """Avogadro Number derivation using Inverse Cubic Projection."""

    def __init__(self):
        self.bulk_na = None
        self.manifest_na = None
        self.variance = None

    @property
    def metadata(self) -> SimulationMetadata:
        return SimulationMetadata(
            id="avogadro_v17_2", version="17.2", domain="qed",
            title="Avogadro from Inverse Cubic",
            description="N_A contracts because counts decrease as space expands.",
            section_id="6", subsection_id="6.6"
        )

    @property
    def required_inputs(self) -> List[str]:
        return ["topology.elder_kads"]

    @property
    def output_params(self) -> List[str]:
        return ["qed.bulk_avogadro", "qed.manifest_avogadro"]

    @property
    def output_formulas(self) -> List[str]:
        return ["avogadro-inverse-cubic"]

    def run(self, registry: PMRegistry) -> Dict[str, Any]:
        self.bulk_na = _REG.bulk_avogadro
        self.manifest_na = _REG.manifest_avogadro
        self.variance = abs(self.manifest_na - CODATA_NA)
        return {
            "qed.bulk_avogadro": self.bulk_na,
            "qed.manifest_avogadro": self.manifest_na,
        }

    def validate(self) -> bool:
        return self.variance < 1e10 if self.variance is not None else False  # Within 1e10 for large number

    def get_section_content(self) -> Optional[SectionContent]:
        return SectionContent(
            section_id="6",
            subsection_id="6.6",
            title="Avogadro Number",
            abstract="Derives Avogadro's number using inverse cubic 1/(1+epsilon) contraction.",
            content_blocks=[
                ContentBlock(type="equation", content=r"N_A = N_{A,bulk} / (1+\epsilon)")
            ]
        )

    def get_formulas(self) -> List[Formula]:
        return [
            Formula(
                id="avogadro-inverse-cubic",
                label="(6.6)",
                latex=r"N_A = N_{A,bulk}/(1+\epsilon)",
                plain_text="N_A = N_A_bulk / (1+epsilon)",
                category="DERIVED",
                description="Avogadro number contracts via inverse cubic",
            ),
        ]

    def get_output_param_definitions(self) -> List[Parameter]:
        return [
            Parameter(
                path="qed.bulk_avogadro",
                name="Bulk Avogadro Number",
                units="mol^-1",
                status="DERIVED",
                description="Avogadro number in bulk (before contraction)",
                no_experimental_value=True,
            ),
            Parameter(
                path="qed.manifest_avogadro",
                name="Manifest Avogadro Number",
                units="mol^-1",
                status="DERIVED",
                description="Avogadro number after 1/(1+epsilon) contraction",
                experimental_bound=CODATA_NA,
                bound_type="measured",
                bound_source="CODATA2022",
            ),
        ]


if __name__ == "__main__":
    print("AVOGADRO NUMBER v17.2 - Inverse Cubic")
    sim = AvogadroV17()
    registry = PMRegistry()
    registry.set_param("topology.elder_kads", _REG.elder_kads, source="ESTABLISHED:FormulasRegistry")
    sim.run(registry)
    print(f"CODATA:   {CODATA_NA:.10e}")
    print(f"Bulk:     {sim.bulk_na:.10e}")
    print(f"Manifest: {sim.manifest_na:.10e}")
    print(f"Valid:    {sim.validate()}")
