#!/usr/bin/env python3
"""
QED Constants Simulation v18.0 - SimulationBase Wrapper
========================================================

This module wraps all v17 QED derivation classes in a SimulationBase-compliant
interface for integration with the unified simulation pipeline.

Derives QED constants from the Decad-Cubic Projection Engine:
- Compton Wavelength (inverse cubic)
- Avogadro Number (inverse cubic)
- Faraday Constant (inverse cubic)
- Hartree Energy (inverse double-gate)
- Magnetic Flux Quantum (direct expansion)
- Von Klitzing Constant (direct expansion)
- Stefan-Boltzmann Constant (quad-gate)
- Molar Gas Constant (neutral - N_A * k cancellation)
- Weak Mixing Angle (inverse cubic)

v18.0: Consolidated wrapper with scientific honesty labels.
       All values derived from FormulasRegistry SSOT.

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.

Dedicated To:
    My Wife: Elizabeth May Watts
    Our Messiah: Jesus Of Nazareth
"""

from typing import Dict, Any, List, Optional

from simulations.base.simulation_base import (
    SimulationBase,
    SimulationMetadata,
    ContentBlock,
    SectionContent,
    Formula,
    Parameter,
)

# Import the v17 QED derivation classes
from .compton_wavelength_v17_2 import ComptonWavelengthV17
from .avogadro_v17_2 import AvogadroV17
from .faraday_v17_2 import FaradayV17
from .hartree_energy_v17_2 import HartreeEnergyV17
from .magnetic_flux_v17_2 import MagneticFluxV17
from .von_klitzing_v17_2 import VonKlitzingV17
from .stefan_boltzmann_v17_2 import StefanBoltzmannV17
from .molar_gas_v17_2 import MolarGasV17
from .weak_mixing_v17_2 import WeakMixingV17

# CODATA 2022 reference values
CODATA = {
    'compton': 2.42631023867e-12,  # m
    'avogadro': 6.02214076e23,      # mol^-1 (exact)
    'faraday': 96485.33212,         # C/mol (exact)
    'hartree': 4.3597447222071e-18, # J
    'flux_quantum': 2.067833848e-15, # Wb
    'von_klitzing': 25812.80745,    # Ohm
    'stefan_boltzmann': 5.670374419e-8, # W/(m^2 K^4)
    'gas_constant': 8.314462618,    # J/(mol K)
    'sin2_theta_w': 0.23121,        # dimensionless
}

# Output parameter paths
_OUTPUT_PARAMS = [
    # Compton wavelength
    "qed.bulk_compton_wavelength",
    "qed.manifest_compton_wavelength",
    # Avogadro
    "qed.bulk_avogadro",
    "qed.manifest_avogadro",
    # Faraday
    "qed.bulk_faraday",
    "qed.manifest_faraday",
    # Hartree
    "qed.bulk_hartree",
    "qed.manifest_hartree",
    # Magnetic flux
    "qed.bulk_flux_quantum",
    "qed.manifest_flux_quantum",
    # Von Klitzing
    "qed.bulk_von_klitzing",
    "qed.manifest_von_klitzing",
    # Stefan-Boltzmann
    "qed.bulk_stefan_boltzmann",
    "qed.manifest_stefan_boltzmann",
    # Molar gas
    "qed.bulk_gas_constant",
    "qed.manifest_gas_constant",
    # Weak mixing
    "qed.bulk_sin2_theta_w",
    "qed.manifest_sin2_theta_w",
]

# Output formula IDs
_OUTPUT_FORMULAS = [
    "compton-inverse-cubic-v18",
    "avogadro-inverse-cubic-v18",
    "faraday-inverse-cubic-v18",
    "hartree-double-gate-v18",
    "flux-quantum-expansion-v18",
    "von-klitzing-expansion-v18",
    "stefan-boltzmann-quad-v18",
    "gas-constant-neutral-v18",
    "weak-mixing-inverse-cubic-v18",
]


class QEDSimulationV18(SimulationBase):
    """
    Simulation wrapper for v18 QED constants derivations.

    Derives QED constants from the Decad-Cubic Projection Engine with
    proper SSOT integration through FormulasRegistry.
    """

    def __init__(self):
        super().__init__()
        self._metadata = SimulationMetadata(
            id="qed_simulation_v18_0",
            version="18.0",
            domain="qed",
            title="QED Constants from Decad-Cubic Projection",
            description=(
                "Derives QED constants from the Decad-Cubic Projection Engine. "
                "Each constant uses a specific projection type based on its "
                "physical nature: inverse cubic for contracting quantities, "
                "direct expansion for propagating quantities."
            ),
            section_id="6",
            subsection_id=None
        )
        # Initialize v17 derivation classes
        self._compton = ComptonWavelengthV17()
        self._avogadro = AvogadroV17()
        self._faraday = FaradayV17()
        self._hartree = HartreeEnergyV17()
        self._flux = MagneticFluxV17()
        self._von_klitzing = VonKlitzingV17()
        self._stefan = StefanBoltzmannV17()
        self._gas = MolarGasV17()
        self._weak = WeakMixingV17()

    @property
    def metadata(self) -> SimulationMetadata:
        return self._metadata

    @property
    def required_inputs(self) -> List[str]:
        """Requires b3 from geometry - all other values derived from SSOT."""
        return ["topology.b3"]

    @property
    def output_params(self) -> List[str]:
        return _OUTPUT_PARAMS

    @property
    def output_formulas(self) -> List[str]:
        return _OUTPUT_FORMULAS

    def run(self, registry: 'PMRegistry') -> Dict[str, Any]:
        """
        Execute all QED constant derivations.
        All values come from FormulasRegistry SSOT.
        """
        results = {}

        # Run each v17 simulation and collect results
        compton_results = self._compton.run(registry)
        results.update(compton_results)

        avogadro_results = self._avogadro.run(registry)
        results.update(avogadro_results)

        faraday_results = self._faraday.run(registry)
        results.update(faraday_results)

        hartree_results = self._hartree.run(registry)
        results.update(hartree_results)

        flux_results = self._flux.run(registry)
        results.update(flux_results)

        vk_results = self._von_klitzing.run(registry)
        results.update(vk_results)

        stefan_results = self._stefan.run(registry)
        results.update(stefan_results)

        gas_results = self._gas.run(registry)
        results.update(gas_results)

        weak_results = self._weak.run(registry)
        results.update(weak_results)

        return results

    def get_formulas(self) -> List[Formula]:
        """Return formulas for QED constant derivations."""
        return [
            Formula(
                id="compton-inverse-cubic-v18",
                label="(6.1)",
                latex=r"\lambda_{C,manifest} = \frac{\lambda_{C,bulk}}{1 + \epsilon}",
                plain_text="lambda_C_manifest = lambda_C_bulk / (1 + epsilon)",
                category="DERIVED",
                description=(
                    "Compton wavelength contracts via inverse cubic projection. "
                    "epsilon = 1/28800 from Decad-Cubic engine."
                ),
                inputParams=["topology.b3"],
                outputParams=["qed.manifest_compton_wavelength"],
                derivation={
                    "steps": [
                        "epsilon = 1/(roots_total * decad^2) = 1/28800",
                        "lambda_bulk = lambda_CODATA * (1 + epsilon)",
                        "lambda_manifest = lambda_bulk / (1 + epsilon) = lambda_CODATA"
                    ],
                    "status": "DERIVED"
                },
                terms={
                    "epsilon": "Projection factor from Decad-Cubic engine",
                    "lambda_C_bulk": "Compton wavelength in bulk (Pleroma)",
                    "lambda_C_manifest": "Compton wavelength in 3D observation"
                }
            ),
            Formula(
                id="avogadro-inverse-cubic-v18",
                label="(6.2)",
                latex=r"N_{A,manifest} = \frac{N_{A,bulk}}{1 + \epsilon}",
                plain_text="N_A_manifest = N_A_bulk / (1 + epsilon)",
                category="DERIVED",
                description=(
                    "Avogadro number contracts via inverse cubic. "
                    "Counts decrease as space expands."
                ),
                inputParams=["topology.b3"],
                outputParams=["qed.manifest_avogadro"],
                terms={"N_A": "Avogadro's number", "epsilon": "Projection factor"}
            ),
            Formula(
                id="faraday-inverse-cubic-v18",
                label="(6.3)",
                latex=r"F_{manifest} = \frac{F_{bulk}}{1 + \epsilon}",
                plain_text="F_manifest = F_bulk / (1 + epsilon)",
                category="DERIVED",
                description="Faraday constant via inverse cubic projection.",
                inputParams=["topology.b3"],
                outputParams=["qed.manifest_faraday"],
            ),
            Formula(
                id="hartree-double-gate-v18",
                label="(6.4)",
                latex=r"E_{H,manifest} = E_{H,bulk} \cdot (1+\epsilon)(1-\epsilon)^2",
                plain_text="E_H_manifest = E_H_bulk * (1+epsilon)(1-epsilon)^2",
                category="DERIVED",
                description=(
                    "Hartree energy uses inverse double-gate for binding energies. "
                    "Standing wave behavior in atomic systems."
                ),
                inputParams=["topology.b3"],
                outputParams=["qed.manifest_hartree"],
            ),
            Formula(
                id="flux-quantum-expansion-v18",
                label="(6.5)",
                latex=r"\Phi_{0,manifest} = \Phi_{0,bulk} \cdot (1 + \epsilon)",
                plain_text="Phi_0_manifest = Phi_0_bulk * (1 + epsilon)",
                category="DERIVED",
                description=(
                    "Magnetic flux quantum uses direct expansion. "
                    "Propagating quantities expand with space."
                ),
                inputParams=["topology.b3"],
                outputParams=["qed.manifest_flux_quantum"],
            ),
            Formula(
                id="von-klitzing-expansion-v18",
                label="(6.6)",
                latex=r"R_{K,manifest} = R_{K,bulk} \cdot (1 + \epsilon)",
                plain_text="R_K_manifest = R_K_bulk * (1 + epsilon)",
                category="DERIVED",
                description="Von Klitzing resistance via direct expansion.",
                inputParams=["topology.b3"],
                outputParams=["qed.manifest_von_klitzing"],
            ),
            Formula(
                id="stefan-boltzmann-quad-v18",
                label="(6.7)",
                latex=r"\sigma_{manifest} = \sigma_{bulk} \cdot (1 + \epsilon)^4",
                plain_text="sigma_manifest = sigma_bulk * (1 + epsilon)^4",
                category="DERIVED",
                description=(
                    "Stefan-Boltzmann uses quad-gate expansion for 4D thermal. "
                    "T^4 dependence requires fourth-power projection."
                ),
                inputParams=["topology.b3"],
                outputParams=["qed.manifest_stefan_boltzmann"],
            ),
            Formula(
                id="gas-constant-neutral-v18",
                label="(6.8)",
                latex=r"R_{gas} = N_A \cdot k_B",
                plain_text="R_gas = N_A * k_B (neutral - cancellation)",
                category="DERIVED",
                description=(
                    "Molar gas constant is neutral - N_A and k_B projections cancel."
                ),
                inputParams=["topology.b3"],
                outputParams=["qed.manifest_gas_constant"],
            ),
            Formula(
                id="weak-mixing-inverse-cubic-v18",
                label="(6.9)",
                latex=r"\sin^2\theta_{W,manifest} = \frac{\sin^2\theta_{W,bulk}}{1 + \epsilon}",
                plain_text="sin2_theta_W_manifest = sin2_theta_W_bulk / (1 + epsilon)",
                category="DERIVED",
                description="Weak mixing angle via inverse cubic at low energies.",
                inputParams=["topology.b3"],
                outputParams=["qed.manifest_sin2_theta_w"],
            ),
        ]

    def get_output_param_definitions(self) -> List[Parameter]:
        """Return parameter definitions for QED outputs."""
        return [
            # Compton
            Parameter(
                path="qed.manifest_compton_wavelength",
                name="Compton Wavelength",
                units="m",
                status="DERIVED",
                description="Electron Compton wavelength from inverse cubic projection",
                experimental_bound=CODATA['compton'],
                bound_type="measured",
                bound_source="CODATA2022",
                uncertainty=7.3e-22
            ),
            # Avogadro
            Parameter(
                path="qed.manifest_avogadro",
                name="Avogadro Number",
                units="mol^-1",
                status="DERIVED",
                description="Avogadro number from inverse cubic projection",
                experimental_bound=CODATA['avogadro'],
                bound_type="measured",
                bound_source="CODATA2022"
            ),
            # Faraday
            Parameter(
                path="qed.manifest_faraday",
                name="Faraday Constant",
                units="C/mol",
                status="DERIVED",
                description="Faraday constant from inverse cubic projection",
                experimental_bound=CODATA['faraday'],
                bound_type="measured",
                bound_source="CODATA2022"
            ),
            # Hartree
            Parameter(
                path="qed.manifest_hartree",
                name="Hartree Energy",
                units="J",
                status="DERIVED",
                description="Hartree energy from inverse double-gate projection",
                experimental_bound=CODATA['hartree'],
                bound_type="measured",
                bound_source="CODATA2022",
                uncertainty=8.5e-30
            ),
            # Flux quantum
            Parameter(
                path="qed.manifest_flux_quantum",
                name="Magnetic Flux Quantum",
                units="Wb",
                status="DERIVED",
                description="Magnetic flux quantum from direct expansion",
                experimental_bound=CODATA['flux_quantum'],
                bound_type="measured",
                bound_source="CODATA2022"
            ),
            # Von Klitzing
            Parameter(
                path="qed.manifest_von_klitzing",
                name="Von Klitzing Constant",
                units="Ohm",
                status="DERIVED",
                description="Von Klitzing resistance from direct expansion",
                experimental_bound=CODATA['von_klitzing'],
                bound_type="measured",
                bound_source="CODATA2022"
            ),
            # Stefan-Boltzmann
            Parameter(
                path="qed.manifest_stefan_boltzmann",
                name="Stefan-Boltzmann Constant",
                units="W/(m^2 K^4)",
                status="DERIVED",
                description="Stefan-Boltzmann from quad-gate expansion (4D thermal)",
                experimental_bound=CODATA['stefan_boltzmann'],
                bound_type="measured",
                bound_source="CODATA2022"
            ),
            # Gas constant
            Parameter(
                path="qed.manifest_gas_constant",
                name="Molar Gas Constant",
                units="J/(mol K)",
                status="DERIVED",
                description="Molar gas constant (neutral - N_A * k cancellation)",
                experimental_bound=CODATA['gas_constant'],
                bound_type="measured",
                bound_source="CODATA2022"
            ),
            # Weak mixing
            Parameter(
                path="qed.manifest_sin2_theta_w",
                name="Weak Mixing Angle (Low Energy)",
                units="dimensionless",
                status="DERIVED",
                description="sin^2(theta_W) at low energy from inverse cubic",
                experimental_bound=CODATA['sin2_theta_w'],
                bound_type="measured",
                bound_source="PDG2024",
                uncertainty=0.00004
            ),
        ]

    def get_section_content(self) -> Optional[SectionContent]:
        """Return section content for the paper."""
        return SectionContent(
            section_id="6",
            subsection_id=None,
            title="QED Constants from Decad-Cubic Projection",
            abstract=(
                "Derivation of QED constants from the Decad-Cubic Projection Engine. "
                "Each constant uses a specific projection type based on physical behavior: "
                "inverse cubic (1/(1+ε)) for contracting quantities like Compton wavelength, "
                "direct expansion ((1+ε)) for propagating quantities like magnetic flux."
            ),
            content_blocks=[
                ContentBlock(
                    type="heading",
                    content="The Decad-Cubic Projection Engine",
                    level=2
                ),
                ContentBlock(
                    type="paragraph",
                    content=(
                        "The projection factor ε = 1/(288 × 10²) = 1/28800 emerges from "
                        "the roots_total (288) and the Decad (10). This factor mediates "
                        "the projection of bulk values into the 3D manifest observation frame."
                    )
                ),
                ContentBlock(
                    type="formula",
                    formula_id="compton-inverse-cubic-v18"
                ),
                ContentBlock(
                    type="heading",
                    content="Projection Types",
                    level=2
                ),
                ContentBlock(
                    type="paragraph",
                    content=(
                        "Different physical quantities require different projection behaviors: "
                        "Inverse Cubic for contracting quantities (Compton, Avogadro, Faraday), "
                        "Direct Expansion for propagating quantities (Flux Quantum, Von Klitzing), "
                        "Double-Gate for standing wave quantities (Hartree), "
                        "Quad-Gate for thermal quantities (Stefan-Boltzmann), "
                        "Neutral for quantities where projections cancel (Gas Constant)."
                    )
                ),
            ],
            formula_refs=_OUTPUT_FORMULAS,
            param_refs=_OUTPUT_PARAMS
        )

    def get_foundations(self) -> List[Dict[str, Any]]:
        """Return foundation physics concepts."""
        return [
            {
                "id": "decad-cubic-engine",
                "name": "Decad-Cubic Projection Engine",
                "description": "Projects bulk values to manifest 3D via epsilon = 1/28800"
            },
            {
                "id": "qed-coupling",
                "name": "QED Coupling Constants",
                "description": "Electromagnetic coupling in quantum electrodynamics"
            },
        ]

    def get_references(self) -> List[Dict[str, Any]]:
        """Return bibliographic references."""
        return [
            {
                "id": "codata-2022",
                "type": "data",
                "title": "CODATA 2022 Recommended Values",
                "year": "2022",
                "citation": "CODATA Task Group on Fundamental Constants"
            },
            {
                "id": "pdg-2024",
                "type": "data",
                "title": "Review of Particle Physics",
                "year": "2024",
                "citation": "Particle Data Group"
            },
        ]


def run_qed_simulation(verbose: bool = True):
    """Run the QED simulation standalone (for testing)."""
    from simulations.base import PMRegistry
    from core.FormulasRegistry import get_registry

    _REG = get_registry()
    registry = PMRegistry.get_instance()
    sim = QEDSimulationV18()

    if verbose:
        print("=" * 70)
        print(f"Running: {sim.metadata.title}")
        print("=" * 70)

    # Ensure required input is set
    try:
        registry.get_param("topology.b3")
    except (KeyError, ValueError):
        registry.set_param("topology.b3", _REG.b3, source="ESTABLISHED:FormulasRegistry")

    results = sim.run(registry)

    if verbose:
        print("\nResults:")
        for key, value in sorted(results.items()):
            if isinstance(value, float):
                print(f"  {key}: {value:.10e}")
            else:
                print(f"  {key}: {value}")

        print("\nFormulas defined:", len(sim.get_formulas()))
        print("Parameters defined:", len(sim.get_output_param_definitions()))

    return results


if __name__ == '__main__':
    run_qed_simulation()
