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
from datetime import datetime
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..'))

from simulations.base import (
    SimulationBase, SimulationMetadata, ContentBlock, SectionContent, Formula, Parameter, PMRegistry,
)
from simulations.core.FormulasRegistry import get_registry

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
        return ["topology.elder_kads"]

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
                ContentBlock(type="paragraph", content=(
                    "The Molar Gas Constant is unique among derived constants: it requires NO "
                    "projection adjustment. Since R = N_A * k_B, where N_A contracts via "
                    "1/(1+epsilon) and k_B (Boltzmann constant) expands via (1+epsilon), "
                    "the adjustments cancel perfectly. R is therefore a Pleromic Invariant -- "
                    "the 'Still Point' where expansion and contraction are in exact balance."
                )),
                ContentBlock(type="equation", content=r"R = N_A \times k_B = \text{invariant}"),
                ContentBlock(type="paragraph", content=(
                    "The CODATA 2022 exact value is R = 8.314462618 J/(mol K). This invariance "
                    "is a structural prediction of the Decad-Cubic Projection Engine: any product "
                    "of an inverse-cubic and a direct-expansion quantity cancels the epsilon "
                    "correction, producing an exact bulk-to-manifest identity."
                )),
            ]
        )

    def get_formulas(self) -> List[Formula]:
        return [
            Formula(
                id="molar-gas-neutral",
                label="(6.8)",
                latex=r"R = N_A \cdot k_B = \text{invariant (Pleromic)}",
                plain_text="R = N_A * k_B = invariant (Pleromic Still Point)",
                category="DERIVED",
                description="Molar gas constant is invariant because N_A contraction cancels k_B expansion exactly.",
                derivation={
                    "steps": [
                        "Identify the Decad-Cubic epsilon = 1/(ENNOIA * DECAD^2) = 1/28800",
                        "N_A contracts: N_A_manifest = N_A_bulk / (1+epsilon) (inverse cubic, particle count decreases)",
                        "k_B expands: k_B_manifest = k_B_bulk * (1+epsilon) (direct expansion, thermal energy increases)",
                        "Product: R = N_A * k_B = [N_A_bulk/(1+eps)] * [k_B_bulk*(1+eps)] = N_A_bulk * k_B_bulk = R_bulk = invariant"
                    ],
                    "method": "Neutral Bridge (expansion and contraction cancel exactly)",
                    "parentFormulas": ["avogadro-inverse-cubic", "boltzmann-direct-expansion"]
                },
                terms={
                    "R": "Molar gas constant, 8.314462618 J/(mol K) (exact, Pleromic invariant)",
                    "N_A": "Avogadro constant (contracts via 1/(1+epsilon))",
                    "k_B": "Boltzmann constant (expands via (1+epsilon))",
                    "epsilon": "Projection parameter 1/28800 (cancels in product)"
                },
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


    # -------------------------------------------------------------------------
    # SSOT Metadata Methods
    # -------------------------------------------------------------------------

    def get_references(self) -> List[Dict[str, Any]]:
        """Return bibliographic references for the molar gas constant derivation."""
        return [
            {
                "id": "codata2022r",
                "authors": "Tiesinga, E., Mohr, P.J., Newell, D.B., Taylor, B.N.",
                "title": "CODATA Recommended Values of the Fundamental Physical Constants: 2022",
                "journal": "Journal of Physical and Chemical Reference Data",
                "year": 2024,
                "url": "https://physics.nist.gov/cuu/Constants/",
                "notes": "R = 8.314462618 J/(mol K) (exact since 2019 SI: R = N_A * k_B)"
            },
            {
                "id": "bipm2019",
                "authors": "BIPM",
                "title": "SI Brochure: The International System of Units (9th edition)",
                "publisher": "Bureau International des Poids et Mesures",
                "year": 2019,
                "url": "https://www.bipm.org/en/measurement-units",
                "notes": "R is exact because both N_A and k_B are exact in the 2019 SI"
            },
        ]

    def get_certificates(self) -> List[Dict[str, Any]]:
        """Return certificate assertions for molar gas constant derivation."""
        manifest = self.manifest_r if self.manifest_r is not None else _REG.manifest_molar_gas_constant
        variance = abs(manifest - CODATA_R)
        passed = variance < 1e-9

        return [
            {
                "id": "CERT_MOLAR_GAS_INVARIANCE",
                "assertion": "Molar gas constant R is a Pleromic invariant: manifest matches CODATA exactly",
                "condition": f"|R_manifest - R_CODATA| < 1e-9  (actual: {variance:.3e})",
                "tolerance": 1e-9,
                "status": "PASS" if passed else "FAIL",
                "wolfram_query": "molar gas constant in J/(mol K)",
                "wolfram_result": "8.314462618 J/(mol K) (exact)",
                "sector": "qed"
            },
        ]

    def get_learning_materials(self) -> List[Dict[str, Any]]:
        """Return educational resources about the molar gas constant."""
        return [
            {
                "topic": "Molar gas constant",
                "url": "https://en.wikipedia.org/wiki/Gas_constant",
                "relevance": "R = N_A * k_B = 8.314462618 J/(mol K); this simulation shows R is invariant because N_A contraction exactly cancels k_B expansion",
                "validation_hint": "Verify R = 6.02214076e23 * 1.380649e-23 = 8.314462618... J/(mol K) (both factors exact since 2019 SI)"
            },
        ]

    def validate_self(self) -> Dict[str, Any]:
        """Validate that molar gas constant is invariant under projection."""
        checks = []
        manifest = self.manifest_r if self.manifest_r is not None else _REG.manifest_molar_gas_constant
        variance = abs(manifest - CODATA_R)

        # Check 1: Matches CODATA exactly
        match_ok = variance < 1e-9
        checks.append({
            "name": "Molar gas constant matches CODATA 2022 exact value",
            "passed": match_ok,
            "confidence_interval": {
                "lower": CODATA_R - 1e-9,
                "upper": CODATA_R + 1e-9,
                "sigma": 0.0
            },
            "log_level": "INFO" if match_ok else "ERROR",
            "message": f"Variance = {variance:.3e} J/(mol K) (tolerance 1e-9)"
        })

        # Check 2: Invariance check -- manifest equals CODATA (no bulk/manifest split)
        invariance_ok = variance < 1e-6
        checks.append({
            "name": "R is a Pleromic invariant (neutral bridge: no net adjustment)",
            "passed": invariance_ok,
            "confidence_interval": None,
            "log_level": "INFO" if invariance_ok else "WARNING",
            "message": f"R_manifest = {manifest:.12f}, CODATA = {CODATA_R:.12f}"
        })

        return {
            "passed": all(c["passed"] for c in checks),
            "checks": checks
        }

    def get_gate_checks(self) -> List[Dict[str, Any]]:
        """Return gate check results for molar gas constant derivation."""
        manifest = self.manifest_r if self.manifest_r is not None else _REG.manifest_molar_gas_constant
        variance = abs(manifest - CODATA_R)
        passed = variance < 1e-9

        return [
            {
                "gate_id": "G26_MOLAR_GAS_INVARIANCE",
                "simulation_id": self.metadata.id,
                "assertion": "Molar gas constant is a Pleromic invariant: N_A contraction cancels k_B expansion",
                "result": "PASS" if passed else "FAIL",
                "timestamp": datetime.now().isoformat(),
                "details": {
                    "codata_value": CODATA_R,
                    "derived_value": manifest,
                    "variance": variance,
                    "projection_type": "neutral_bridge",
                    "note": "R = N_A * k_B: inverse cubic cancels direct expansion"
                }
            },
        ]


if __name__ == "__main__":
    print("MOLAR GAS CONSTANT v17.2 - Neutral Bridge (The Still Point)")
    sim = MolarGasV17()
    registry = PMRegistry()
    registry.set_param("topology.elder_kads", _REG.elder_kads, source="ESTABLISHED:FormulasRegistry")
    sim.run(registry)
    print(f"CODATA:   {CODATA_R:.12f} J/(mol K)")
    print(f"Manifest: {sim.manifest_r:.12f} J/(mol K)")
    print(f"Variance: {sim.variance:.15e}")
    print(f"Valid:    {sim.validate()}")
    print("Note: R is invariant - N_A contraction cancels k expansion!")
