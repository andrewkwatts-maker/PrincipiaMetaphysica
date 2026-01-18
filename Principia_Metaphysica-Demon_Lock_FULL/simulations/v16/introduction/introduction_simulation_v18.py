#!/usr/bin/env python3
"""
Introduction Simulation v18.0 - SimulationBase Wrapper
=======================================================

This module wraps the v17 introduction classes in a SimulationBase-compliant
interface for integration with the unified simulation pipeline.

Provides framework overview and introduction content for Principia Metaphysica:
- Division algebra decomposition D = 1 + 4 + 8 = 13
- Dimensional hierarchy 26D -> 13D -> 4D
- Hurwitz theorem constraints
- G2 manifold framework introduction
- Historical context and theoretical background

v18.0: Unified introduction wrapper with formulas and framework parameters.

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.

Dedicated To:
    My Wife: Elizabeth May Watts
    Our Messiah: Jesus Of Nazareth
"""

from typing import TYPE_CHECKING, Dict, Any, List, Optional

from simulations.base.simulation_base import (
    SimulationBase,
    SimulationMetadata,
    ContentBlock,
    SectionContent,
    Formula,
    Parameter,
)

# Import the v17 classes for delegation
from .introduction_v16_0 import IntroductionV16
from .abstract_v17_2 import AbstractV17_2

if TYPE_CHECKING:
    from simulations.base import PMRegistry


# Output parameter paths for this simulation
_OUTPUT_PARAMS = [
    # Dimensional structure
    "dimensions.D_bulk",
    "dimensions.D_after_sp2r",
    "dimensions.D_observable",
    "dimensions.D_G2",
    "dimensions.D_spin8",
    # Division algebra dimensions
    "dimensions.D_real",
    "dimensions.D_quaternion",
    "dimensions.D_octonion",
    # Framework topology
    "topology.b3",
    "topology.chi_eff",
    "topology.n_gen",
    # Signature
    "signature.timelike",
    "signature.spacelike",
]

# Output formula IDs
_OUTPUT_FORMULAS = [
    "division-algebra-decomposition-v18",
    "dimensional-hierarchy-v18",
    "hurwitz-constraint-v18",
    "fermion-generations-topology-v18",
    "spinor-decomposition-v18",
]


class IntroductionSimulationV18(SimulationBase):
    """
    Simulation wrapper for v18 introduction content.

    Provides framework overview, division algebra foundations, and
    dimensional hierarchy explanations for Principia Metaphysica.
    """

    def __init__(self):
        super().__init__()
        self._metadata = SimulationMetadata(
            id="introduction_v18_0",
            version="18.0",
            domain="introduction",
            title="Introduction to Principia Metaphysica",
            description=(
                "Framework overview and theoretical foundations for PM v17.2. "
                "Introduces the 26D -> 13D -> 4D dimensional hierarchy, "
                "division algebra constraints, and G2 manifold geometry."
            ),
            section_id="1",
            subsection_id=None
        )
        # Initialize v17 classes for delegation
        self._introduction_v16 = IntroductionV16()
        self._abstract_v17 = AbstractV17_2()

    @property
    def metadata(self) -> SimulationMetadata:
        return self._metadata

    @property
    def required_inputs(self) -> List[str]:
        """No required inputs - this is narrative/framework content."""
        return []

    @property
    def output_params(self) -> List[str]:
        return _OUTPUT_PARAMS

    @property
    def output_formulas(self) -> List[str]:
        return _OUTPUT_FORMULAS

    def run(self, registry: 'PMRegistry') -> Dict[str, Any]:
        """
        Execute the introduction simulation.

        Returns framework dimensional parameters from pure geometry.
        These are fixed by the theory structure, not computed dynamically.
        """
        results = {}

        # Dimensional structure (fixed by theory)
        results["dimensions.D_bulk"] = 26  # Full bulk dimension
        results["dimensions.D_after_sp2r"] = 13  # After Sp(2,R) gauge-fixing
        results["dimensions.D_observable"] = 4  # Observable spacetime
        results["dimensions.D_G2"] = 7  # G2 manifold dimension
        results["dimensions.D_spin8"] = 8  # Internal Spin(8) manifold

        # Division algebra dimensions (Hurwitz theorem)
        results["dimensions.D_real"] = 1  # R (emergent thermal time)
        results["dimensions.D_quaternion"] = 4  # H (Lorentzian spacetime)
        results["dimensions.D_octonion"] = 8  # O (internal manifold)

        # Framework topology (TCS #187)
        results["topology.b3"] = 24  # Third Betti number
        results["topology.chi_eff"] = 144  # Effective Euler characteristic
        results["topology.n_gen"] = 3  # Fermion generations = b3/8

        # Signature (24,2) -> observable (3,1)
        results["signature.timelike"] = 2  # Two time dimensions in bulk
        results["signature.spacelike"] = 24  # Spatial dimensions in bulk

        return results

    def get_formulas(self) -> List[Formula]:
        """Return formulas for introduction/framework section."""
        return [
            Formula(
                id="division-algebra-decomposition-v18",
                label="(1.1)",
                latex=r"D = 13 = 1 + 4 + 8 = \dim(\mathbb{R}) + \dim(\mathbb{H}) + \dim(\mathbb{O})",
                plain_text="D = 13 = 1 + 4 + 8 = dim(R) + dim(H) + dim(O)",
                category="GEOMETRIC",
                description=(
                    "Division algebra decomposition of the observable shadow dimension. "
                    "R (time), H (spacetime), O (internal) - unique by Hurwitz theorem."
                ),
                inputParams=[],
                outputParams=["dimensions.D_after_sp2r"],
                derivation={
                    "steps": [
                        "Hurwitz theorem: only R(1), C(2), H(4), O(8) are normed division algebras",
                        "Physical constraints: need 1D time, 4D spacetime, 8D internal",
                        "Exclude C (no worldsheet in PM)",
                        "D = 1 + 4 + 8 = 13 (unique solution)"
                    ],
                    "status": "THEOREM"
                },
                terms={
                    "R": "Real numbers (emergent thermal time)",
                    "H": "Quaternions (Lorentzian spacetime Spin(3,1))",
                    "O": "Octonions (internal G2 manifold, Aut(O)=G2)"
                }
            ),
            Formula(
                id="dimensional-hierarchy-v18",
                label="(1.2)",
                latex=r"26D_{(24,2)} \xrightarrow{\text{Sp}(2,\mathbb{R})} 13D_{(12,1)} \xrightarrow{G_2} 4D_{(3,1)}",
                plain_text="26D_(24,2) --[Sp(2,R)]--> 13D_(12,1) --[G2]--> 4D_(3,1)",
                category="GEOMETRIC",
                description=(
                    "Dimensional hierarchy from 26D bulk through observable 13D shadow "
                    "to 4D spacetime via G2 compactification."
                ),
                inputParams=[],
                outputParams=["dimensions.D_bulk", "dimensions.D_after_sp2r", "dimensions.D_observable"],
                derivation={
                    "steps": [
                        "26D bulk with signature (24,2) - bosonic string critical dimension",
                        "Sp(2,R) gauge-fixes two time dimensions, leaving 13D shadow",
                        "G2 compactification on 7D TCS manifold yields 4D observable",
                        "Signature preserved: (24,2) -> (12,1) -> (3,1)"
                    ]
                },
                terms={
                    "Sp(2,R)": "Symplectic gauge symmetry relating two times",
                    "G2": "Exceptional holonomy group for 7D compactification",
                    "(24,2)": "Bulk signature (24 space, 2 time)"
                }
            ),
            Formula(
                id="hurwitz-constraint-v18",
                label="(1.3)",
                latex=r"\text{Hurwitz: } \dim(\mathbb{A}) \in \{1, 2, 4, 8\} \text{ only}",
                plain_text="Hurwitz: dim(A) in {1, 2, 4, 8} only",
                category="THEOREM",
                description=(
                    "Hurwitz theorem (1898): exactly four normed division algebras exist. "
                    "This constrains all division-algebra-consistent dimensions."
                ),
                inputParams=[],
                outputParams=[],
                derivation={
                    "steps": [
                        "R (dim 1): associative, commutative, ordered",
                        "C (dim 2): associative, commutative",
                        "H (dim 4): associative, non-commutative",
                        "O (dim 8): non-associative, alternative",
                        "No others exist - proven by Hurwitz 1898"
                    ],
                    "status": "THEOREM"
                },
                terms={
                    "normed": "||ab|| = ||a|| ||b|| for all elements",
                    "division": "Every nonzero element has multiplicative inverse"
                }
            ),
            Formula(
                id="fermion-generations-topology-v18",
                label="(1.4)",
                latex=r"n_\text{gen} = \frac{|\chi_\text{eff}|}{48} = \frac{144}{48} = 3",
                plain_text="n_gen = |chi_eff|/48 = 144/48 = 3",
                category="EXACT",
                description=(
                    "Number of chiral fermion generations from G2 Euler characteristic. "
                    "EXACT topological prediction with no free parameters."
                ),
                inputParams=["topology.chi_eff"],
                outputParams=["topology.n_gen"],
                derivation={
                    "steps": [
                        "chi_eff = 144 for TCS #187 manifold",
                        "48 = 24 x 2 (F-theory index x Z2 parity)",
                        "n_gen = 144/48 = 3 (EXACT)"
                    ],
                    "status": "EXACT"
                },
                terms={
                    "chi_eff": "Effective Euler characteristic = 144",
                    "48": "Combined F-theory (24) and Z2 (2) divisor",
                    "n_gen": "Number of chiral fermion generations"
                }
            ),
            Formula(
                id="spinor-decomposition-v18",
                label="(1.5)",
                latex=r"\text{Spin}(12,1) \supset \text{Spin}(3,1) \times \text{Spin}(8): \mathbf{64} = (\mathbf{2},\mathbf{8}_s) \oplus (\mathbf{2},\mathbf{8}_c) \oplus (\mathbf{\bar{2}},\mathbf{8}_v) \oplus (\mathbf{\bar{2}},\mathbf{8}_s)",
                plain_text="Spin(12,1) > Spin(3,1) x Spin(8): 64 = (2,8_s) + (2,8_c) + (2bar,8_v) + (2bar,8_s)",
                category="REPRESENTATION",
                description=(
                    "Spinor decomposition of 64-component 13D spinor under "
                    "4D Lorentz x internal Spin(8) symmetry."
                ),
                inputParams=[],
                outputParams=[],
                derivation={
                    "steps": [
                        "Spin(12,1) is the 13D Lorentz group",
                        "Decompose under Spin(3,1) x Spin(8)",
                        "64 = 2^6 = 2 x 32 (4D spinor x 8D spinor)",
                        "Spin(8) triality: 8_s, 8_c, 8_v representations"
                    ]
                },
                terms={
                    "8_s": "Spinor representation of Spin(8)",
                    "8_c": "Conjugate spinor of Spin(8)",
                    "8_v": "Vector representation of Spin(8)",
                    "2, 2bar": "Weyl spinors of Spin(3,1)"
                }
            ),
        ]

    def get_output_param_definitions(self) -> List[Parameter]:
        """Return parameter definitions for framework outputs."""
        return [
            Parameter(
                path="dimensions.D_bulk",
                name="Bulk Dimension",
                units="dimensionless",
                status="GEOMETRIC",
                description="Full 26D bulk dimension with signature (24,2)",
                no_experimental_value=True
            ),
            Parameter(
                path="dimensions.D_after_sp2r",
                name="Shadow Dimension",
                units="dimensionless",
                status="GEOMETRIC",
                description="Observable 13D shadow after Sp(2,R) gauge-fixing",
                no_experimental_value=True
            ),
            Parameter(
                path="dimensions.D_observable",
                name="Observable Dimension",
                units="dimensionless",
                status="GEOMETRIC",
                description="4D observable spacetime after G2 compactification",
                experimental_bound=4,
                bound_type="observed",
                bound_source="Direct observation",
                uncertainty=0
            ),
            Parameter(
                path="dimensions.D_G2",
                name="G2 Manifold Dimension",
                units="dimensionless",
                status="GEOMETRIC",
                description="7D internal G2 holonomy manifold",
                no_experimental_value=True
            ),
            Parameter(
                path="dimensions.D_spin8",
                name="Internal Spin(8) Dimension",
                units="dimensionless",
                status="GEOMETRIC",
                description="8D octonionic internal structure",
                no_experimental_value=True
            ),
            Parameter(
                path="dimensions.D_real",
                name="Real Division Algebra Dimension",
                units="dimensionless",
                status="THEOREM",
                description="dim(R) = 1 (emergent thermal time)",
                no_experimental_value=True
            ),
            Parameter(
                path="dimensions.D_quaternion",
                name="Quaternion Division Algebra Dimension",
                units="dimensionless",
                status="THEOREM",
                description="dim(H) = 4 (Lorentzian spacetime)",
                no_experimental_value=True
            ),
            Parameter(
                path="dimensions.D_octonion",
                name="Octonion Division Algebra Dimension",
                units="dimensionless",
                status="THEOREM",
                description="dim(O) = 8 (internal manifold, Aut(O)=G2)",
                no_experimental_value=True
            ),
            Parameter(
                path="topology.b3",
                name="Third Betti Number",
                units="dimensionless",
                status="GEOMETRIC",
                description="b3 = 24 for TCS #187 G2 manifold",
                no_experimental_value=True
            ),
            Parameter(
                path="topology.chi_eff",
                name="Effective Euler Characteristic",
                units="dimensionless",
                status="GEOMETRIC",
                description="chi_eff = 144 for TCS #187 manifold",
                no_experimental_value=True
            ),
            Parameter(
                path="topology.n_gen",
                name="Fermion Generations",
                units="count",
                status="EXACT",
                description="n_gen = chi_eff/48 = 3 (EXACT topological prediction)",
                experimental_bound=3,
                bound_type="measured",
                bound_source="LHC (no 4th generation)",
                uncertainty=0
            ),
            Parameter(
                path="signature.timelike",
                name="Timelike Dimensions (Bulk)",
                units="dimensionless",
                status="GEOMETRIC",
                description="Two time dimensions in 26D bulk",
                no_experimental_value=True
            ),
            Parameter(
                path="signature.spacelike",
                name="Spacelike Dimensions (Bulk)",
                units="dimensionless",
                status="GEOMETRIC",
                description="24 spatial dimensions in 26D bulk",
                no_experimental_value=True
            ),
        ]

    def get_section_content(self) -> Optional[SectionContent]:
        """
        Return section content for Section 1: Introduction.

        Delegates to the v16 introduction for full narrative content.
        """
        # Get the full content from v16 introduction
        v16_content = self._introduction_v16.get_section_content()

        if v16_content is None:
            # Fallback if v16 content unavailable
            return SectionContent(
                section_id="1",
                subsection_id=None,
                title="Introduction to Principia Metaphysica",
                abstract=(
                    "Framework overview introducing the 26D -> 13D -> 4D dimensional "
                    "hierarchy, division algebra constraints from Hurwitz theorem, and "
                    "G2 manifold geometry for particle physics derivations."
                ),
                content_blocks=[
                    ContentBlock(
                        type="heading",
                        content="Division Algebra Foundations",
                        level=2
                    ),
                    ContentBlock(
                        type="paragraph",
                        content=(
                            "The observable shadow dimension D = 13 admits a unique "
                            "decomposition into normed division algebra dimensions: "
                            "D = 1 + 4 + 8 = dim(R) + dim(H) + dim(O). This follows "
                            "from the Hurwitz theorem and physical constraints."
                        )
                    ),
                    ContentBlock(
                        type="formula",
                        formula_id="division-algebra-decomposition-v18"
                    ),
                    ContentBlock(
                        type="heading",
                        content="Dimensional Hierarchy",
                        level=2
                    ),
                    ContentBlock(
                        type="paragraph",
                        content=(
                            "The full theory lives in 26D with signature (24,2). "
                            "Sp(2,R) gauge-fixing projects to the 13D observable shadow, "
                            "which then compactifies on a G2 manifold to yield 4D spacetime."
                        )
                    ),
                    ContentBlock(
                        type="formula",
                        formula_id="dimensional-hierarchy-v18"
                    ),
                ],
                formula_refs=_OUTPUT_FORMULAS,
                param_refs=_OUTPUT_PARAMS
            )

        # Enhance the v16 content with v18 formula references
        return SectionContent(
            section_id=v16_content.section_id,
            subsection_id=v16_content.subsection_id,
            title=v16_content.title,
            abstract=v16_content.abstract,
            content_blocks=v16_content.content_blocks,
            formula_refs=_OUTPUT_FORMULAS,
            param_refs=_OUTPUT_PARAMS
        )

    def get_abstract_content(self) -> Optional[SectionContent]:
        """
        Return the paper abstract (Section 0).

        Delegates to AbstractV17_2.
        """
        return self._abstract_v17.get_section_content()

    def get_beginner_explanation(self) -> Dict[str, Any]:
        """
        Return a beginner-friendly explanation of Principia Metaphysica.

        Delegates to v16 introduction.
        """
        return self._introduction_v16.get_beginner_explanation()

    def get_foundations(self) -> Dict[str, str]:
        """
        Return foundational principles of Principia Metaphysica.

        Delegates to v16 introduction.
        """
        return self._introduction_v16.get_foundations()

    def get_references(self) -> List[Dict[str, str]]:
        """
        Return historical references for the introduction section.

        Delegates to v16 introduction.
        """
        return self._introduction_v16.get_references()


def run_introduction_simulation(verbose: bool = True):
    """Run the introduction simulation standalone (for testing)."""
    from simulations.base import PMRegistry

    registry = PMRegistry.get_instance()
    sim = IntroductionSimulationV18()

    if verbose:
        print("=" * 70)
        print(f"Running: {sim.metadata.title}")
        print("=" * 70)

    results = sim.run(registry)

    if verbose:
        print("\nDimensional Structure:")
        for key, value in results.items():
            if key.startswith("dimensions."):
                print(f"  {key}: {value}")

        print("\nTopology:")
        for key, value in results.items():
            if key.startswith("topology."):
                print(f"  {key}: {value}")

        print("\nSignature:")
        for key, value in results.items():
            if key.startswith("signature."):
                print(f"  {key}: {value}")

        print(f"\nFormulas defined: {len(sim.get_formulas())}")
        print(f"Parameters defined: {len(sim.get_output_param_definitions())}")

    return results


if __name__ == '__main__':
    run_introduction_simulation()
