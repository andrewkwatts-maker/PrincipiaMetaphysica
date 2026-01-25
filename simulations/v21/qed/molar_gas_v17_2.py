"""
Molar Gas Constant Derivation v17.2
===================================

The Molar Gas Constant is a NEUTRAL BRIDGE (no adjustment).
R = N_A * k, and since N_A contracts [1/(1+e)] while k expands [(1+e)],
the adjustments cancel perfectly. R is a Pleromic Invariant.

CODATA 2022: R = 8.314462618 J mol^-1 K^-1 (exact)

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
CODATA_R = 8.314462618  # J mol^-1 K^-1 (exact)


class MolarGasV17(SimulationBase):
    """Molar Gas Constant - The Neutral Bridge (no adjustment)."""

    def __init__(self):
        self.manifest_r = None
        self.variance = None

    @property
    def metadata(self) -> SimulationMetadata:
        return SimulationMetadata(
            id="molar_gas_v17_2", version="17.2", domain="qed",
            title="Molar Gas - Neutral Bridge",
            description="R = N_A * k. Expansion and contraction cancel perfectly.",
            section_id="6", subsection_id="6.8"
        )

    @property
    def required_inputs(self) -> List[str]:
        return ["topology.b3"]

    @property
    def output_params(self) -> List[str]:
        return ["qed.manifest_molar_gas_constant"]

    @property
    def output_formulas(self) -> List[str]:
        return ["molar-gas-neutral"]

    def run(self, registry: PMRegistry) -> Dict[str, Any]:
        self.manifest_r = _REG.manifest_molar_gas_constant
        self.variance = abs(self.manifest_r - CODATA_R)
        return {
            "qed.manifest_molar_gas_constant": self.manifest_r,
        }

    def validate(self) -> bool:
        return self.variance < 1e-9 if self.variance is not None else False

    def get_section_content(self) -> Optional[SectionContent]:
        return SectionContent(
            section_id="6",
            subsection_id="6.8",
            title="Molar Gas Constant - The Still Point",
            abstract="The molar gas constant is invariant: N_A contraction cancels k expansion.",
            content_blocks=[
                ContentBlock(type="text", content=(
                    "The Molar Gas Constant is unique: it requires NO adjustment. "
                    "Since R = N_A * k, where N_A contracts and k expands by the same factor, "
                    "the adjustments cancel. R is a Pleromic Invariant - the 'Still Point' of thermodynamics."
                )),
                ContentBlock(type="equation", content=r"R = N_A \times k = \text{invariant}")
            ]
        )

    def get_formulas(self) -> List[Formula]:
        return [
            Formula(
                id="molar-gas-neutral",
                label="(6.8)",
                latex=r"R = N_A \cdot k = \text{invariant}",
                plain_text="R = N_A * k = invariant",
                category="DERIVED",
                description="Molar gas constant is invariant (N_A contraction cancels k expansion)",
            ),
        ]

    def get_output_param_definitions(self) -> List[Parameter]:
        return [
            Parameter(
                path="qed.manifest_molar_gas_constant",
                name="Molar Gas Constant",
                units="J/(mol K)",
                status="DERIVED",
                description="Molar gas constant R = N_A * k (neutral bridge - no adjustment)",
                experimental_bound=CODATA_R,
                bound_type="measured",
                bound_source="CODATA2022",
            ),
        ]


if __name__ == "__main__":
    print("MOLAR GAS CONSTANT v17.2 - Neutral Bridge (The Still Point)")
    sim = MolarGasV17()
    registry = PMRegistry()
    registry.set_param("topology.b3", _REG.governing_elder_kad, source="ESTABLISHED:FormulasRegistry")
    sim.run(registry)
    print(f"CODATA:   {CODATA_R:.12f} J/(mol K)")
    print(f"Manifest: {sim.manifest_r:.12f} J/(mol K)")
    print(f"Variance: {sim.variance:.15e}")
    print(f"Valid:    {sim.validate()}")
    print("Note: R is invariant - N_A contraction cancels k expansion!")
