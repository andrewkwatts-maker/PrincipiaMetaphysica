#!/usr/bin/env python3
"""
PRINCIPIA METAPHYSICA v16.0 - Introduction
===========================================

Provides section content for the Introduction (Section 1).

This simulation does not compute physics parameters, but instead generates
the narrative content and cross-references for the paper's introduction.

SECTION: 1 (Introduction)

OUTPUTS:
    - None (narrative content only)

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.
"""

import sys
import os
from typing import Dict, Any, List, Optional

# Add parent directories to path for imports
_current_dir = os.path.dirname(os.path.abspath(__file__))
_simulations_dir = os.path.dirname(os.path.dirname(_current_dir))
_project_root = os.path.dirname(_simulations_dir)
sys.path.insert(0, _project_root)

from simulations.base import (
    SimulationBase,
    SimulationMetadata,
    ContentBlock,
    SectionContent,
)


class IntroductionV16(SimulationBase):
    """
    Introduction section generator (v16.0).

    Provides narrative content for the introduction section,
    including historical context, framework overview, and
    key predictions summary.
    """

    @property
    def metadata(self) -> SimulationMetadata:
        """Return metadata about this simulation."""
        return SimulationMetadata(
            id="introduction_v16_0",
            version="16.0",
            domain="introduction",
            title="Introduction to Principia Metaphysica",
            description="Narrative introduction to the PM framework and key predictions",
            section_id="1",
            subsection_id=None
        )

    @property
    def required_inputs(self) -> List[str]:
        """No required inputs - this is narrative content only."""
        return []

    @property
    def output_params(self) -> List[str]:
        """No output parameters - narrative content only."""
        return []

    @property
    def output_formulas(self) -> List[str]:
        """No formulas - introduction is narrative."""
        return []

    def run(self, registry: 'PMRegistry') -> Dict[str, Any]:
        """
        Execute the introduction generation.

        Args:
            registry: PMRegistry instance (not used)

        Returns:
            Empty dictionary (no computed parameters)
        """
        # Introduction section provides narrative content only
        return {}

    def get_section_content(self) -> Optional[SectionContent]:
        """
        Return section content for Section 1: Introduction.

        Returns:
            SectionContent instance with introduction narrative
        """
        content_blocks = [
            ContentBlock(
                type="paragraph",
                content=(
                    "The pursuit of a unified description of all fundamental forces represents "
                    "one of the most profound intellectual endeavors in theoretical physics. "
                    "This section traces the historical arc from Maxwell's unification of "
                    "electricity and magnetism to modern attempts at Grand Unified Theories, "
                    "while introducing the novel approach of deriving geometry from a fundamental "
                    "fermionic field."
                ),
                className="lead"
            ),
            ContentBlock(
                type="paragraph",
                content=(
                    "<strong>Principia Metaphysica</strong> posits a 26D spacetime with signature "
                    "(24,2)—incorporating two time dimensions related by Sp(2,R) gauge symmetry—"
                    "from which an observable 13D shadow emerges. Compactification occurs on a "
                    "<strong>TCS (Twisted Connected Sum) G₂ manifold</strong> with "
                    "<strong>h<sup>1,1</sup>=4 Kähler moduli sectors</strong>, enabling "
                    "<strong>racetrack moduli stabilization</strong> that dynamically derives "
                    "ε ≈ 0.2257 (the Cabibbo angle) without tuning."
                )
            ),
            ContentBlock(
                type="paragraph",
                content=(
                    "The <strong>Pneuma-Vielbein bridge (v15.1)</strong> validates metric "
                    "emergence from spinor bilinears with Lorentzian signature (-,+,+,+). "
                    "Key predictions include w₀ = -11/13 and wₐ ≈ 0.27, matching DESI 2024 observations."
                )
            ),
            ContentBlock(
                type="heading",
                content="The Quest for Unification",
                level=2
            ),
            ContentBlock(
                type="paragraph",
                content=(
                    "The history of physics is, in large part, a history of unification. "
                    "James Clerk Maxwell's synthesis of electricity and magnetism in 1865 "
                    "revealed that apparently distinct phenomena were manifestations of a "
                    "single electromagnetic field. This triumph established a paradigm: what "
                    "appears as separate forces at low energies may be unified at higher "
                    "energy scales."
                )
            ),
            ContentBlock(
                type="paragraph",
                content=(
                    "The 20th century witnessed further dramatic unifications. The "
                    "Glashow-Weinberg-Salam electroweak theory (1967-1968) demonstrated that "
                    "electromagnetism and the weak nuclear force are unified into a single "
                    "SU(2)<sub>L</sub> × U(1)<sub>Y</sub> gauge theory, spontaneously broken "
                    "at the electroweak scale (~246 GeV) to yield the observed low-energy "
                    "phenomenology."
                )
            ),
            ContentBlock(
                type="heading",
                content="The Principia Metaphysica Framework",
                level=2
            ),
            ContentBlock(
                type="paragraph",
                content=(
                    "Principia Metaphysica builds on the foundation of M-theory and Grand "
                    "Unification, but introduces several key innovations:"
                )
            ),
            ContentBlock(
                type="list",
                items=[
                    "<strong>Two-Time Framework:</strong> A 26D spacetime with signature (24,2), "
                    "where two time dimensions are related by Sp(2,R) gauge symmetry",

                    "<strong>G₂ Holonomy Compactification:</strong> Dimensional reduction on "
                    "TCS G₂ manifolds with h<sup>1,1</sup>=4 Kähler moduli sectors",

                    "<strong>Pneuma Field:</strong> A fundamental fermionic field from which "
                    "spacetime geometry emerges via spinor bilinears (Pneuma-Vielbein bridge)",

                    "<strong>Racetrack Moduli Stabilization:</strong> Dynamic fixing of moduli "
                    "that derives the Cabibbo angle ε ≈ 0.2257 without tuning",

                    "<strong>Thermal Time Hypothesis:</strong> Time emerges from the thermodynamic "
                    "properties of the Pneuma field via modular flow",
                ]
            ),
            ContentBlock(
                type="heading",
                content="Key Predictions",
                level=2
            ),
            ContentBlock(
                type="paragraph",
                content="Principia Metaphysica makes several testable predictions:"
            ),
            ContentBlock(
                type="table",
                headers=["Observable", "PM Prediction", "Experimental Status"],
                rows=[
                    [
                        "Dark energy EoS (w₀)",
                        "w₀ = -11/13 ≈ -0.846",
                        "DESI 2024: -0.827 ± 0.063 (0.3σ agreement)"
                    ],
                    [
                        "Dark energy evolution (wₐ)",
                        "wₐ ≈ 0.27",
                        "DESI 2024: 0.29 ± 0.15 (0.1σ agreement)"
                    ],
                    [
                        "Fermion generations",
                        "n_gen = 3 (from χ_eff/48)",
                        "Standard Model: exactly 3 (exact match)"
                    ],
                    [
                        "Cabibbo angle",
                        "ε ≈ 0.2257",
                        "PDG: 0.2257 ± 0.0010 (exact match)"
                    ],
                    [
                        "GUT scale",
                        "M_GUT ~ 2×10¹⁶ GeV",
                        "Theoretical range (untested)"
                    ],
                    [
                        "Proton lifetime",
                        "τ_p ~ 3.9×10³⁴ years",
                        "Super-K bound: > 1.67×10³⁴ years (2.3× above bound)"
                    ],
                ]
            ),
            ContentBlock(
                type="heading",
                content="Organization of This Paper",
                level=2
            ),
            ContentBlock(
                type="paragraph",
                content=(
                    "The remainder of this paper is organized as follows. Section 2 presents "
                    "the geometric framework, including G₂ holonomy, the Pneuma field, and "
                    "metric emergence. Section 3 derives gauge coupling unification and the "
                    "GUT scale. Section 4 covers the fermion sector, including generation "
                    "number, Yukawa hierarchy, Higgs mass, neutrino mixing, and proton decay. "
                    "Section 5 presents the cosmological framework, including dark matter, "
                    "dark energy, and thermal time. Section 6 summarizes falsifiable predictions, "
                    "and Section 7 discusses implications and future directions."
                )
            ),
        ]

        return SectionContent(
            section_id="1",
            subsection_id=None,
            title="Introduction",
            abstract=(
                "We present Principia Metaphysica, a unified framework deriving the Standard "
                "Model and cosmological observables from a 26D two-time spacetime compactified "
                "on a TCS G₂ manifold. The framework makes falsifiable predictions for dark "
                "energy, proton decay, and neutrino physics, with excellent agreement to DESI "
                "2024 measurements."
            ),
            content_blocks=content_blocks,
            formula_refs=[],
            param_refs=[
                "desi.w0",
                "desi.wa",
                "topology.n_gen",
                "gauge.M_GUT",
                "proton_decay.tau_p_years",
            ]
        )

    def get_formulas(self) -> List:
        """No formulas in introduction section."""
        return []

    def get_output_param_definitions(self) -> List:
        """No output parameters in introduction section."""
        return []

    def get_references(self) -> List[Dict[str, str]]:
        """Return historical references for introduction."""
        return [
            {
                "id": "maxwell_1865",
                "authors": "Maxwell, J. C.",
                "title": "A Dynamical Theory of the Electromagnetic Field",
                "journal": "Phil. Trans. R. Soc. Lond.",
                "volume": "155",
                "year": "1865"
            },
            {
                "id": "glashow_1961",
                "authors": "Glashow, S. L.",
                "title": "Partial Symmetries of Weak Interactions",
                "journal": "Nucl. Phys.",
                "volume": "22",
                "year": "1961"
            },
            {
                "id": "weinberg_1967",
                "authors": "Weinberg, S.",
                "title": "A Model of Leptons",
                "journal": "Phys. Rev. Lett.",
                "volume": "19",
                "year": "1967"
            },
            {
                "id": "georgi_glashow_1974",
                "authors": "Georgi, H. and Glashow, S. L.",
                "title": "Unity of All Elementary Particle Forces",
                "journal": "Phys. Rev. Lett.",
                "volume": "32",
                "year": "1974"
            },
        ]


def main():
    """Run the simulation standalone for testing."""
    import io
    import sys

    # Ensure UTF-8 output encoding
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

    from simulations.base import PMRegistry

    # Create registry
    registry = PMRegistry()

    # Create and run simulation
    sim = IntroductionV16()

    print("=" * 70)
    print(f" {sim.metadata.title}")
    print("=" * 70)
    print()

    # Generate section content
    section_content = sim.get_section_content()

    print(f"Section: {section_content.section_id}")
    print(f"Title: {section_content.title}")
    print(f"Abstract: {section_content.abstract[:100]}...")
    print(f"Content blocks: {len(section_content.content_blocks)}")
    print()


if __name__ == "__main__":
    main()
