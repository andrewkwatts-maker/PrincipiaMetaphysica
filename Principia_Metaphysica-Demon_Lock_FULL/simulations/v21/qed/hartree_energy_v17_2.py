"""
Hartree Energy Derivation v17.2
===============================

Licensed under the MIT License. See LICENSE file for details.

Derives the Hartree energy from the Decad-Cubic Projection Engine.

The Hartree energy uses INVERSE DOUBLE-GATE: 1/[(1+epsilon)(1-epsilon)^2]
because binding energy is inversely related to length-squared (Bohr radius).

CODATA 2022: E_h = 4.3597447222071(85) x 10^-18 J

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
CODATA_HARTREE = 4.3597447222071e-18  # J


class HartreeEnergyV17(SimulationBase):
    """Hartree Energy derivation using Inverse Double-Gate."""

    def __init__(self):
        self.bulk_hartree = None
        self.manifest_hartree = None
        self.variance = None

    @property
    def metadata(self) -> SimulationMetadata:
        return SimulationMetadata(
            id="hartree_energy_v17_2", version="17.2", domain="qed",
            title="Hartree Energy from Inverse Double-Gate",
            description="Binding energy uses inverse of Bohr radius adjustment.",
            section_id="6", subsection_id="6.3"
        )

    @property
    def required_inputs(self) -> List[str]:
        return ["topology.b3"]

    @property
    def output_params(self) -> List[str]:
        return ["qed.bulk_hartree_energy", "qed.manifest_hartree_energy"]

    @property
    def output_formulas(self) -> List[str]:
        return ["hartree-inverse-double-gate"]

    def run(self, registry: PMRegistry) -> Dict[str, Any]:
        self.bulk_hartree = _REG.bulk_hartree_energy
        self.manifest_hartree = _REG.manifest_hartree_energy
        self.variance = abs(self.manifest_hartree - CODATA_HARTREE)
        return {
            "qed.bulk_hartree_energy": self.bulk_hartree,
            "qed.manifest_hartree_energy": self.manifest_hartree,
        }

    def validate(self) -> bool:
        return self.variance < 1e-30 if self.variance is not None else False

    def get_section_content(self) -> Optional[SectionContent]:
        return SectionContent(
            section_id="6",
            subsection_id="6.3",
            title="Hartree Energy",
            abstract="Derives the Hartree energy using inverse double-gate adjustment.",
            content_blocks=[
                ContentBlock(type="equation", content=r"E_h = E_{bulk} \times \frac{1}{(1+\epsilon)(1-\epsilon)^2}")
            ]
        )

    def get_formulas(self) -> List[Formula]:
        return [
            Formula(
                id="hartree-inverse-double-gate",
                label="(6.3)",
                latex=r"E_h = E_{h,bulk} / [(1+\epsilon)(1-\epsilon)^2]",
                plain_text="E_h = E_h_bulk / [(1+epsilon)(1-epsilon)^2]",
                category="DERIVED",
                description="Hartree energy derived via inverse double-gate adjustment",
            ),
        ]

    def get_output_param_definitions(self) -> List[Parameter]:
        return [
            Parameter(
                path="qed.bulk_hartree_energy",
                name="Bulk Hartree Energy",
                units="J",
                status="DERIVED",
                description="Hartree energy in bulk (before Inverse Double-Gate)",
                no_experimental_value=True,
            ),
            Parameter(
                path="qed.manifest_hartree_energy",
                name="Manifest Hartree Energy",
                units="J",
                status="DERIVED",
                description="Hartree energy after Inverse Double-Gate adjustment",
                experimental_bound=CODATA_HARTREE,
                bound_type="measured",
                bound_source="CODATA2022",
            ),
        ]


if __name__ == "__main__":
    print("HARTREE ENERGY v17.2 - Inverse Double-Gate")
    sim = HartreeEnergyV17()
    registry = PMRegistry()
    registry.set_param("topology.b3", _REG.b3, source="ESTABLISHED:FormulasRegistry")
    sim.run(registry)
    print(f"CODATA:   {CODATA_HARTREE:.15e} J")
    print(f"Bulk:     {sim.bulk_hartree:.15e} J")
    print(f"Manifest: {sim.manifest_hartree:.15e} J")
    print(f"Valid:    {sim.validate()}")
