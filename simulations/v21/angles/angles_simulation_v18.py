#!/usr/bin/env python3
"""
Geometric Angles Simulations v18.0 - SimulationBase Wrapper
============================================================

This module wraps the v17 angles classes in a SimulationBase-compliant
interface for integration with the unified simulation pipeline.

Computes key geometric angles from the theory:
- Bazien angles: Shadow brane intersection angles
- Octonion angles: Division algebra angles (golden, triality, Fano)
- G2 holonomy angles: Calibration and symmetry locking
- SU(3) embedding angles: Regular and irregular embeddings

v18.0: Consolidated angles simulations with proper schema compliance.

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.

Dedicated To:
    My Wife: Elizabeth May Watts
    Our Messiah: Jesus Of Nazareth
"""

from typing import Dict, Any, List, Optional
import numpy as np

from simulations.base.simulation_base import (
    SimulationBase,
    SimulationMetadata,
    ContentBlock,
    SectionContent,
    Formula,
    Parameter,
)

# Import the v17 angles classes
from .bazien_angles_v17 import BazienAngles
from .octonion_angles_v17 import OctonionAngles
from .g2_holonomy_angles_v17 import G2HolonomyAngles
from .su3_embedding_angles_v17 import SU3EmbeddingAngles


# Output parameter paths
_OUTPUT_PARAMS = [
    # Bazien angles
    "angles.sterile_deg",
    "angles.golden_deg",
    "angles.shadow_projection_deg",
    "angles.cabibbo_precursor_deg",
    # Octonion angles
    "angles.large_golden_deg",
    "angles.triality_cycle_deg",
    "angles.fano_base_deg",
    # G2 holonomy
    "angles.associative_cal_deg",
    "angles.theta_23_forced_deg",
    "angles.coassociative_cal_deg",
    # SU(3) embedding
    "angles.simple_root_deg",
    "angles.embedding_cal_deg",
    "angles.su3_delta_deg",
]

# Output formula IDs
_OUTPUT_FORMULAS = [
    "sterile-angle-bazien-v18",
    "golden-angle-octonion-v18",
    "theta-23-holonomy-v18",
    "su3-embedding-cal-v18",
]


class AnglesSimulationV18(SimulationBase):
    """
    Simulation wrapper for v18 geometric angles computations.

    Computes angles from the theory's geometric structure:
    - Bazien: Shadow brane intersection angles (125/288 sterile projection)
    - Octonion: Division algebra angles (phi-based golden angles)
    - G2 Holonomy: Calibration angles and symmetry locking
    - SU(3): Color and neutrino mixing embedding angles
    """

    def __init__(self):
        super().__init__()
        self._metadata = SimulationMetadata(
            id="angles_simulation_v18_0",
            version="18.0",
            domain="angles",
            title="Geometric Angles from G2/Octonion Structure",
            description=(
                "Computes key geometric angles from shadow brane intersections, "
                "octonionic division algebra, G2 holonomy calibrations, and "
                "SU(3) embeddings. Angles lock physical parameters."
            ),
            section_id="2",  # Geometry section
            subsection_id="2.5"
        )
        # Initialize angle computation classes
        self._bazien = BazienAngles()
        self._octonion = OctonionAngles()
        self._g2_holonomy = G2HolonomyAngles()
        self._su3_embedding = SU3EmbeddingAngles()

    @property
    def metadata(self) -> SimulationMetadata:
        return self._metadata

    @property
    def required_inputs(self) -> List[str]:
        """No required inputs - pure geometric computations."""
        return []

    @property
    def output_params(self) -> List[str]:
        return _OUTPUT_PARAMS

    @property
    def output_formulas(self) -> List[str]:
        return _OUTPUT_FORMULAS

    def run(self, registry: 'PMRegistry') -> Dict[str, Any]:
        """Execute all angle computations and register to PM Registry."""
        results = {}

        # Bazien angles
        bazien = self._bazien.compute_all_angles()
        results["angles.sterile_deg"] = bazien.sterile_angle_deg
        results["angles.golden_deg"] = bazien.golden_angle_deg
        results["angles.shadow_projection_deg"] = bazien.shadow_projection_deg
        results["angles.cabibbo_precursor_deg"] = bazien.cabibbo_precursor_deg

        # Octonion angles
        octonion = self._octonion.compute_all_angles()
        results["angles.large_golden_deg"] = octonion.large_golden_deg
        results["angles.triality_cycle_deg"] = octonion.triality_cycle_deg
        results["angles.fano_base_deg"] = octonion.fano_base_deg

        # G2 holonomy angles
        g2 = self._g2_holonomy.compute_all_angles()
        results["angles.associative_cal_deg"] = g2.associative_cal_deg
        results["angles.theta_23_forced_deg"] = g2.theta_23_forced_deg
        results["angles.coassociative_cal_deg"] = g2.coassociative_cal_deg

        # SU(3) embedding angles
        su3 = self._su3_embedding.compute_all_angles()
        results["angles.simple_root_deg"] = su3.simple_root_deg
        results["angles.embedding_cal_deg"] = su3.embedding_cal_deg
        results["angles.su3_delta_deg"] = su3.su3_delta_deg

        # v18.0 FIX: Register all computed angles to PM Registry
        for path, value in results.items():
            if not registry.has_param(path):
                registry.set_param(
                    path=path,
                    value=value,
                    source=self._metadata.id,
                    status="GEOMETRIC",
                    metadata={
                        "derivation": "Geometric angle from G2/octonion topology",
                        "units": "degrees"
                    }
                )

        return results

    def get_formulas(self) -> List[Formula]:
        """Return formulas for angle computations."""
        return [
            Formula(
                id="sterile-angle-bazien-v18",
                label="(2.15)",
                latex=r"\theta_{\text{sterile}} = \arcsin\left(\frac{125}{288}\right) \approx 25.72°",
                plain_text="theta_sterile = arcsin(125/288) ~ 25.72 deg",
                category="GEOMETRIC",
                description=(
                    "Sterile angle from shadow brane intersection. "
                    "125 observable residues from 288 ancestral roots."
                ),
                inputParams=[],
                outputParams=["angles.sterile_deg"],
                terms={
                    "125": "Observable spectral residues",
                    "288": "Ancestral root basis (Appendix H)"
                }
            ),
            Formula(
                id="golden-angle-octonion-v18",
                label="(2.16)",
                latex=r"\theta_g = \arctan\left(\frac{1}{\phi}\right) \approx 31.72°",
                plain_text="theta_g = arctan(1/phi) ~ 31.72 deg",
                category="GEOMETRIC",
                description=(
                    "Primary octonionic golden angle. Base for many "
                    "residues and mixing angles in the theory."
                ),
                inputParams=[],
                outputParams=["angles.golden_deg"],
                terms={
                    "phi": "Golden ratio (1 + sqrt(5))/2 ~ 1.618",
                    "theta_g": "Base angle for residue projections"
                }
            ),
            Formula(
                id="theta-23-holonomy-v18",
                label="(2.17)",
                latex=r"\theta_{23} = 45° + \delta_{\text{Kahler}} + \delta_{\text{Flux}} = 49.75°",
                plain_text="theta_23 = 45 + 0.75 + 4.0 = 49.75 deg",
                category="EXACT",
                description=(
                    "Atmospheric mixing angle exactly locked by G2 holonomy. "
                    "SU(3) subgroup Shadow=Shadow symmetry forces this value."
                ),
                inputParams=[],
                outputParams=["angles.theta_23_forced_deg"],
                terms={
                    "45": "Maximal mixing base",
                    "delta_Kahler": "0.75 deg Kahler correction",
                    "delta_Flux": "4.0 deg flux correction"
                }
            ),
            Formula(
                id="su3-embedding-cal-v18",
                label="(2.18)",
                latex=r"\theta_{\text{embed}} = \arccos\left(\sqrt{\frac{1}{3}}\right) \approx 54.74°",
                plain_text="theta_embed = arccos(sqrt(1/3)) ~ 54.74 deg",
                category="GEOMETRIC",
                description=(
                    "SU(3) embedding calibration angle in G2. "
                    "From 3-cycle norm projection in associative embedding."
                ),
                inputParams=[],
                outputParams=["angles.embedding_cal_deg"],
                terms={
                    "sqrt(1/3)": "Norm projection factor",
                    "SU(3)": "Color symmetry subgroup of G2"
                }
            ),
        ]

    def get_output_param_definitions(self) -> List[Parameter]:
        """Return parameter definitions for outputs."""
        return [
            Parameter(
                path="angles.sterile_deg",
                name="Sterile Angle",
                units="degrees",
                status="GEOMETRIC",
                description="Shadow brane intersection angle: arcsin(125/288)",
                no_experimental_value=True
            ),
            Parameter(
                path="angles.golden_deg",
                name="Golden Angle",
                units="degrees",
                status="GEOMETRIC",
                description="Primary octonionic golden angle: arctan(1/phi)",
                no_experimental_value=True
            ),
            Parameter(
                path="angles.theta_23_forced_deg",
                name="Atmospheric Mixing Angle",
                units="degrees",
                status="EXACT",
                description="G2 holonomy-forced theta_23 = 49.75 deg (experimental: 49.0 +/- 1.3 deg, < 1 sigma)",
                experimental_bound=49.0,
                bound_type="measured",
                bound_source="NuFIT6.0",
                uncertainty=1.3
            ),
            Parameter(
                path="angles.large_golden_deg",
                name="Large Golden Angle",
                units="degrees",
                status="GEOMETRIC",
                description="360/phi^2 ~ 137.51 deg (phyllotaxis angle)",
                no_experimental_value=True
            ),
            Parameter(
                path="angles.triality_cycle_deg",
                name="Triality Cycle Angle",
                units="degrees",
                status="GEOMETRIC",
                description="G2 outer automorphism triality: 120 deg",
                no_experimental_value=True
            ),
            Parameter(
                path="angles.associative_cal_deg",
                name="Associative Calibration",
                units="degrees",
                status="GEOMETRIC",
                description="G2 associative 3-form: arccos(1/3) ~ 70.53 deg",
                no_experimental_value=True
            ),
            Parameter(
                path="angles.embedding_cal_deg",
                name="SU(3) Embedding Calibration",
                units="degrees",
                status="GEOMETRIC",
                description="Regular SU(3) in G2: arccos(sqrt(1/3)) ~ 54.74 deg",
                no_experimental_value=True
            ),
        ]

    def get_section_content(self) -> Optional[SectionContent]:
        """Return section content for the paper."""
        return SectionContent(
            section_id="2",
            subsection_id="2.5",
            title="Geometric Angles from G2/Octonion Structure",
            abstract=(
                "Key geometric angles from shadow brane intersections, octonionic "
                "division algebra, G2 holonomy calibrations, and SU(3) embeddings. "
                "These angles lock physical parameters without tuning."
            ),
            content_blocks=[
                ContentBlock(
                    type="heading",
                    content="Bazien Angles: Shadow Brane Intersection",
                    level=2
                ),
                ContentBlock(
                    type="paragraph",
                    content=(
                        "The sterile angle theta_sterile = arcsin(125/288) ~ 25.72 deg "
                        "governs the projection bottleneck from 288 ancestral roots to "
                        "125 observable spectral residues during dimensional descent."
                    )
                ),
                ContentBlock(
                    type="formula",
                    formula_id="sterile-angle-bazien-v18"
                ),
                ContentBlock(
                    type="heading",
                    content="G2 Holonomy-Locked theta_23",
                    level=2
                ),
                ContentBlock(
                    type="paragraph",
                    content=(
                        "The atmospheric mixing angle theta_23 = 49.75 deg is EXACTLY "
                        "locked by G2 holonomy's SU(3) subgroup. The Shadow=Shadow "
                        "symmetry forces this value with no freedom for adjustment."
                    )
                ),
                ContentBlock(
                    type="formula",
                    formula_id="theta-23-holonomy-v18"
                ),
                ContentBlock(
                    type="heading",
                    content="Octonionic Golden Angles",
                    level=2
                ),
                ContentBlock(
                    type="paragraph",
                    content=(
                        "The golden ratio phi appears throughout the theory. The large "
                        "golden angle 360/phi^2 ~ 137.51 deg is strikingly close to "
                        "1/alpha ~ 137.036, refined via sterile and torsion residues."
                    )
                ),
            ],
            formula_refs=_OUTPUT_FORMULAS,
            param_refs=_OUTPUT_PARAMS
        )


def run_angles_simulation(verbose: bool = True):
    """Run the angles simulation standalone (for testing)."""
    from simulations.base import PMRegistry

    registry = PMRegistry.get_instance()
    sim = AnglesSimulationV18()

    if verbose:
        print("=" * 70)
        print(f"Running: {sim.metadata.title}")
        print("=" * 70)

    results = sim.run(registry)

    if verbose:
        print("\nResults:")
        for key, value in results.items():
            if isinstance(value, float):
                print(f"  {key}: {value:.6f}")
            else:
                print(f"  {key}: {value}")

    return results


if __name__ == '__main__':
    run_angles_simulation()
