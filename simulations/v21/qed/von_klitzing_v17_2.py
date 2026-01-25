"""
Von Klitzing Constant Derivation v17.2
======================================

The Von Klitzing constant uses DIRECT EXPANSION (1+epsilon)
because R_K = h/e^2, where h expands and e is invariant.

CODATA 2022: R_K = 25812.80745 Ohm

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
CODATA_RK = 25812.80745  # Ohm


class VonKlitzingV17(SimulationBase):
    """Von Klitzing constant derivation using Direct Expansion."""

    def __init__(self):
        self.bulk_rk = None
        self.manifest_rk = None
        self.variance = None

    @property
    def metadata(self) -> SimulationMetadata:
        return SimulationMetadata(
            id="von_klitzing_v17_2", version="17.2", domain="qed",
            title="Von Klitzing from Direct Expansion",
            description="R_K expands with h since e is invariant.",
            section_id="6", subsection_id="6.5"
        )

    @property
    def required_inputs(self) -> List[str]:
        return ["topology.b3"]

    @property
    def output_params(self) -> List[str]:
        return ["qed.bulk_von_klitzing", "qed.manifest_von_klitzing"]

    @property
    def output_formulas(self) -> List[str]:
        return ["rk-direct-expansion"]

    def run(self, registry: PMRegistry) -> Dict[str, Any]:
        self.bulk_rk = _REG.bulk_von_klitzing
        self.manifest_rk = _REG.manifest_von_klitzing
        self.variance = abs(self.manifest_rk - CODATA_RK)
        return {
            "qed.bulk_von_klitzing": self.bulk_rk,
            "qed.manifest_von_klitzing": self.manifest_rk,
        }

    def validate(self) -> bool:
        return self.variance < 1e-5 if self.variance is not None else False

    def get_section_content(self) -> Optional[SectionContent]:
        return SectionContent(
            section_id="6",
            subsection_id="6.5",
            title="Von Klitzing Constant",
            abstract="Derives the Von Klitzing constant using direct expansion (1+epsilon).",
            content_blocks=[
                ContentBlock(type="equation", content=r"R_K = R_{K,bulk} \times (1+\epsilon)")
            ]
        )

    def get_formulas(self) -> List[Formula]:
        return [
            Formula(
                id="rk-direct-expansion",
                label="(6.5)",
                latex=r"R_K = R_{K,bulk}(1+\epsilon)",
                plain_text="R_K = R_K_bulk * (1+epsilon)",
                category="DERIVED",
                description="Von Klitzing constant expands with h",
            ),
        ]

    def get_output_param_definitions(self) -> List[Parameter]:
        return [
            Parameter(
                path="qed.bulk_von_klitzing",
                name="Bulk Von Klitzing Constant",
                units="Ohm",
                status="DERIVED",
                description="Von Klitzing constant in bulk (before expansion)",
                no_experimental_value=True,
            ),
            Parameter(
                path="qed.manifest_von_klitzing",
                name="Manifest Von Klitzing Constant",
                units="Ohm",
                status="DERIVED",
                description="Von Klitzing constant after (1+epsilon) expansion",
                experimental_bound=CODATA_RK,
                bound_type="measured",
                bound_source="CODATA2022",
            ),
        ]


if __name__ == "__main__":
    print("VON KLITZING CONSTANT v17.2 - Direct Expansion")
    sim = VonKlitzingV17()
    registry = PMRegistry()
    registry.set_param("topology.b3", _REG.elders, source="ESTABLISHED:FormulasRegistry")
    sim.run(registry)
    print(f"CODATA:   {CODATA_RK:.10f} Ohm")
    print(f"Bulk:     {sim.bulk_rk:.10f} Ohm")
    print(f"Manifest: {sim.manifest_rk:.10f} Ohm")
    print(f"Valid:    {sim.validate()}")
