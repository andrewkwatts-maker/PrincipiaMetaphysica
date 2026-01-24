"""
Magnetic Flux Quantum Derivation v17.2
======================================

The Magnetic Flux Quantum uses DIRECT EXPANSION (1+epsilon)
because Phi_0 = h/(2e), where h expands and e is invariant.

CODATA 2022: Phi_0 = 2.067833848 x 10^-15 Wb

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
CODATA_FLUX = 2.067833848e-15  # Wb


class MagneticFluxV17(SimulationBase):
    """Magnetic Flux Quantum derivation using Direct Expansion."""

    def __init__(self):
        self.bulk_flux = None
        self.manifest_flux = None
        self.variance = None

    @property
    def metadata(self) -> SimulationMetadata:
        return SimulationMetadata(
            id="magnetic_flux_v17_2", version="17.2", domain="qed",
            title="Magnetic Flux from Direct Expansion",
            description="Phi_0 expands with h since e is invariant.",
            section_id="6", subsection_id="6.4"
        )

    @property
    def required_inputs(self) -> List[str]:
        return ["topology.b3"]

    @property
    def output_params(self) -> List[str]:
        return ["qed.bulk_magnetic_flux", "qed.manifest_magnetic_flux"]

    @property
    def output_formulas(self) -> List[str]:
        return ["flux-direct-expansion"]

    def run(self, registry: PMRegistry) -> Dict[str, Any]:
        self.bulk_flux = _REG.bulk_magnetic_flux_quantum
        self.manifest_flux = _REG.manifest_magnetic_flux_quantum
        self.variance = abs(self.manifest_flux - CODATA_FLUX)
        return {
            "qed.bulk_magnetic_flux": self.bulk_flux,
            "qed.manifest_magnetic_flux": self.manifest_flux,
        }

    def validate(self) -> bool:
        return self.variance < 1e-25 if self.variance is not None else False

    def get_section_content(self) -> Optional[SectionContent]:
        return SectionContent(
            section_id="6",
            subsection_id="6.4",
            title="Magnetic Flux Quantum",
            abstract="Derives the magnetic flux quantum using direct expansion (1+epsilon).",
            content_blocks=[
                ContentBlock(type="equation", content=r"\Phi_0 = \Phi_{bulk} \times (1+\epsilon)")
            ]
        )

    def get_formulas(self) -> List[Formula]:
        return [
            Formula(
                id="flux-direct-expansion",
                label="(6.4)",
                latex=r"\Phi_0 = \Phi_{bulk}(1+\epsilon)",
                plain_text="Phi_0 = Phi_bulk * (1+epsilon)",
                category="DERIVED",
                description="Magnetic flux quantum expands with h",
            ),
        ]

    def get_output_param_definitions(self) -> List[Parameter]:
        return [
            Parameter(
                path="qed.bulk_magnetic_flux",
                name="Bulk Magnetic Flux Quantum",
                units="Wb",
                status="DERIVED",
                description="Magnetic flux quantum in bulk (before expansion)",
                no_experimental_value=True,
            ),
            Parameter(
                path="qed.manifest_magnetic_flux",
                name="Manifest Magnetic Flux Quantum",
                units="Wb",
                status="DERIVED",
                description="Magnetic flux quantum after (1+epsilon) expansion",
                experimental_bound=CODATA_FLUX,
                bound_type="measured",
                bound_source="CODATA2022",
            ),
        ]


if __name__ == "__main__":
    print("MAGNETIC FLUX QUANTUM v17.2 - Direct Expansion")
    sim = MagneticFluxV17()
    registry = PMRegistry()
    registry.set_param("topology.b3", _REG.b3, source="ESTABLISHED:FormulasRegistry")
    sim.run(registry)
    print(f"CODATA:   {CODATA_FLUX:.15e} Wb")
    print(f"Bulk:     {sim.bulk_flux:.15e} Wb")
    print(f"Manifest: {sim.manifest_flux:.15e} Wb")
    print(f"Valid:    {sim.validate()}")
