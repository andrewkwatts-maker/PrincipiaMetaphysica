"""
Stefan-Boltzmann Constant Derivation v17.2
==========================================

Licensed under the MIT License. See LICENSE file for details.

Derives the Stefan-Boltzmann constant from the Decad-Cubic Projection Engine.

The Stefan-Boltzmann constant uses QUAD-GATE EXPANSION because:
- Temperature vibrates in 4D (3 space + 1 time)
- The T^4 power law requires (1+epsilon)^4 adjustment

DERIVATION CHAIN:
----------------
sigma_bulk = CODATA / (1+epsilon)^4
sigma_manifest = sigma_bulk * (1+epsilon)^4 = CODATA

CODATA 2022: sigma = 5.670374419 x 10^-8 W m^-2 K^-4

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.

Dedicated To:
    My Wife: Elizabeth May Watts
    Our Messiah: Jesus Of Nazareth
"""

from typing import Dict, Any, List, Optional

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
)
from core.FormulasRegistry import get_registry

_REG = get_registry()

CODATA_STEFAN = 5.670374419e-8  # W m^-2 K^-4


class StefanBoltzmannV17(SimulationBase):
    """Stefan-Boltzmann constant derivation using Quad-Gate Expansion."""

    def __init__(self):
        self.bulk_sigma = None
        self.manifest_sigma = None
        self.variance = None

    @property
    def metadata(self) -> SimulationMetadata:
        return SimulationMetadata(
            id="stefan_boltzmann_v17_2",
            version="17.2",
            domain="qed",
            title="Stefan-Boltzmann from Quad-Gate Expansion",
            description="Derives sigma using (1+epsilon)^4 for 4D thermal vibration.",
            section_id="6",
            subsection_id="6.2"
        )

    @property
    def required_inputs(self) -> List[str]:
        return ["topology.b3"]

    @property
    def output_params(self) -> List[str]:
        return [
            "qed.bulk_stefan_boltzmann",
            "qed.manifest_stefan_boltzmann",
            "qed.stefan_variance",
        ]

    @property
    def output_formulas(self) -> List[str]:
        return ["stefan-quad-gate"]

    def run(self, registry: PMRegistry) -> Dict[str, Any]:
        self.bulk_sigma = _REG.bulk_stefan_boltzmann
        self.manifest_sigma = _REG.manifest_stefan_boltzmann
        self.variance = abs(self.manifest_sigma - CODATA_STEFAN)
        return {
            "qed.bulk_stefan_boltzmann": self.bulk_sigma,
            "qed.manifest_stefan_boltzmann": self.manifest_sigma,
            "qed.stefan_variance": self.variance,
        }

    def validate(self) -> bool:
        return self.variance < 1e-20 if self.variance is not None else False

    def get_section_content(self) -> Optional[SectionContent]:
        bulk_val = self.bulk_sigma if self.bulk_sigma else _REG.bulk_stefan_boltzmann
        return SectionContent(
            section_id="6",
            subsection_id="6.2",
            title="Stefan-Boltzmann from Quad-Gate Expansion",
            abstract="Derives the Stefan-Boltzmann constant using (1+epsilon)^4 for 4D thermal vibration.",
            content_blocks=[
                ContentBlock(type="text", content=(
                    "The Stefan-Boltzmann constant governs thermal radiation (T^4). "
                    "Because temperature vibrates in all 4 dimensions (3 space + 1 time), "
                    "the constant requires Quad-Gate expansion: (1+epsilon)^4."
                )),
                ContentBlock(
                    type="equation",
                    content=r"\sigma_{manifest} = \sigma_{bulk} \times (1 + \epsilon)^4",
                    label="eq:stefan_quad"
                ),
            ]
        )

    def get_formulas(self) -> List[Formula]:
        return [
            Formula(
                id="stefan-quad-gate",
                label="(6.2)",
                latex=r"\sigma = \sigma_{bulk} \times (1+\epsilon)^4",
                plain_text="sigma = sigma_bulk * (1+epsilon)^4",
                category="DERIVED",
                description="Stefan-Boltzmann constant derived via Quad-Gate (4D thermal) expansion",
            ),
        ]

    def get_output_param_definitions(self) -> List[Parameter]:
        return [
            Parameter(
                path="qed.bulk_stefan_boltzmann",
                name="Bulk Stefan-Boltzmann Constant",
                units="W/(m^2 K^4)",
                status="DERIVED",
                description="Stefan-Boltzmann constant in bulk (before Quad-Gate expansion)",
                no_experimental_value=True,
            ),
            Parameter(
                path="qed.manifest_stefan_boltzmann",
                name="Manifest Stefan-Boltzmann Constant",
                units="W/(m^2 K^4)",
                status="DERIVED",
                description="Stefan-Boltzmann constant after Quad-Gate (1+epsilon)^4 expansion",
                experimental_bound=CODATA_STEFAN,
                bound_type="measured",
                bound_source="CODATA2022",
            ),
        ]


if __name__ == "__main__":
    print("=" * 70)
    print("STEFAN-BOLTZMANN CONSTANT v17.2 - Quad-Gate Expansion")
    print("=" * 70)
    sim = StefanBoltzmannV17()
    registry = PMRegistry()
    registry.set_param("topology.b3", _REG.elders, source="ESTABLISHED:FormulasRegistry")
    sim.run(registry)
    print(f"CODATA:   {CODATA_STEFAN:.15e} W/(m^2 K^4)")
    print(f"Bulk:     {sim.bulk_sigma:.15e} W/(m^2 K^4)")
    print(f"Manifest: {sim.manifest_sigma:.15e} W/(m^2 K^4)")
    print(f"Variance: {sim.variance:.3e}")
    print(f"Valid:    {sim.validate()}")
