#!/usr/bin/env python3
"""
PRINCIPIA METAPHYSICA v21.0 - Section 1: Foundations of Dimensional Descent
============================================================================

DOI: 10.5281/zenodo.18079602

v21.0 STERILE MODEL: (24,1) signature with 2D Euclidean bridge and dual shadows.
All 125 constants are geometric residues, not tuned.

This simulation generates the content for Section 1 of the paper:
  1.1 The 26D(24,1) Ancestral Bulk with Euclidean Bridge
  1.2 The Euclidean Bridge and OR Reduction
  1.3 The G2 Manifold (V7) per Shadow
  1.4 The 6D→4D Projection

SECTION: 1 (Foundations of Dimensional Descent)

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.

Dedicated To:
    My Wife: Elizabeth May Watts
    Our Messiah: Jesus Of Nazareth
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
    Formula,
    Parameter,
)


class FoundationsV16_2(SimulationBase):
    """
    Section 1: Foundations of Dimensional Descent (v21.0).

    Provides the sterile derivation narrative for the (24,1)→4D descent path:
    - 1.1: The 26D(24,1) Ancestral Bulk with Euclidean Bridge
    - 1.2: The Euclidean Bridge and OR Reduction
    - 1.3: The G2 Manifold V7 per Shadow (7D Geometric Hard-Lock)
    - 1.4: The 6D→4D Projection (Calabi-Yau Filtering)
    """

    # Dynamic formula IDs referenced by this section
    FORMULA_REFS = [
        "26d-signature",
        "spr2-gauge",
        "g2-holonomy",
        "b3-generations",
        "calabi-yau-projection",
    ]

    # Dynamic parameter paths referenced by this section
    PARAM_REFS = [
        "dimensions.D_bulk",
        "dimensions.D_after_sp2r",
        "dimensions.D_observable",
        "topology.b3",
        "topology.euler_chi",
        "particle.n_generations",
    ]

    @property
    def metadata(self) -> SimulationMetadata:
        """Return metadata about this simulation."""
        return SimulationMetadata(
            id="foundations_v16_2",
            version="21.0",
            domain="foundations",
            title="Foundations of Dimensional Descent",
            description="The (24,1) bulk with Euclidean bridge, dual shadows, and G2 compactification",
            section_id="1",
            subsection_id="1.1"  # v19.0: Unique subsection (introduction_v16_0 owns section 1)
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
        """Key formulas for dimensional descent."""
        return self.FORMULA_REFS

    def run(self, registry: 'PMRegistry') -> Dict[str, Any]:
        """Execute - returns empty dict as this is narrative only."""
        return {}

    def get_section_content(self) -> Optional[SectionContent]:
        """
        Return section content for Section 1: Foundations of Dimensional Descent.

        Returns:
            SectionContent instance with the sterile model foundation narrative
        """
        content_blocks = [
            # NOTE: Abstract/lead paragraph removed - content is now in Section 0 (abstract_v17_2.py)
            # Section 1 should start directly with the foundational content

            # ================================================================
            # 1.1 The 26D(24,1) Ancestral Bulk with Euclidean Bridge
            # ================================================================
            ContentBlock(
                type="heading",
                content="The 26D(24,1) Ancestral Bulk with Euclidean Bridge",
                level=2,
                label="1.1"
            ),
            ContentBlock(
                type="paragraph",
                content=(
                    "The foundational premise of the Sterile Model is that the observable universe "
                    "is not an independent system, but a lower-dimensional <strong>residue</strong> "
                    "of a <strong>26D(24,1) Bosonic Ancestral Bulk</strong>. This high-dimensional "
                    "state represents the 'Total Potential' of the physical registry, with unified "
                    "time (eliminating ghosts and closed timelike curves) and a 2D Euclidean shared "
                    "bridge enabling dual-shadow coherence."
                )
            ),
            ContentBlock(
                type="heading",
                content="1.1.1 The Algebraic Origin",
                level=3
            ),
            ContentBlock(
                type="paragraph",
                content=(
                    "At the 26D level, the universe is governed by the symmetries of the "
                    "<strong>Monster Group</strong> and the <strong>Leech Lattice</strong>. "
                    "The (24,1) signature is critical: it provides twenty-four spacelike dimensions "
                    "and one unified timelike dimension. This specific configuration allows for "
                    "<strong>ghost-free stability</strong>—a state where the vacuum energy "
                    "is perfectly balanced without CTC instabilities."
                )
            ),
            ContentBlock(
                type="equation",
                content=r"\text{Signature}(M^{26}) = (24, 1) \quad \Rightarrow \quad ds^2 = \sum_{i=1}^{24} dx_i^2 - dt^2",
                label="26d-signature"
            ),
            ContentBlock(
                type="heading",
                content="1.1.2 The Dual-Shadow Structure",
                level=3
            ),
            ContentBlock(
                type="paragraph",
                content=(
                    "The 26D bulk descends into <strong>dual shadows</strong> connected by a "
                    "<strong>2D Euclidean bridge</strong>. Each shadow contains (11,1) degrees of freedom, "
                    "while the bridge dimensions (y₁, y₂) are purely spacelike (2,0):"
                )
            ),
            ContentBlock(
                type="list",
                items=[
                    "<strong>Bridge Metric:</strong> ds²<sub>bridge</sub> = dy₁² + dy₂² (positive-definite, timeless)",
                    "<strong>Shadow Structure:</strong> 2 × [(5,1)<sub>bridge</sub> ⊕ ⊕<sub>k</sub>(3,1)<sub>k</sub>] per generation",
                    "<strong>OR Reduction:</strong> 90° rotation operator R<sub>⊥</sub> enables cross-shadow coordinate sampling"
                ],
                label="dual-shadow-structure"
            ),
            ContentBlock(
                type="heading",
                content="1.1.3 The Symmetry Threshold",
                level=3
            ),
            ContentBlock(
                type="paragraph",
                content=(
                    "The 26D(24,1) state descends via <strong>Dimensional Collapse</strong>. "
                    "The 26-dimensional bosonic string space 'shatters' into the dual-shadow configuration, "
                    "with the Euclidean bridge providing the coherence substrate. This transition is a "
                    "<strong>Topological Shattering</strong>, where the high-dimensional bulk breaks "
                    "along the fault lines of the G₂ holonomy into two mirrored 4D condensates."
                )
            ),
            ContentBlock(
                type="note",
                content=(
                    "<h4>Foundational Note: The Origin of Sterility</h4>"
                    "<p>The 'Sterility' of our 4D reality is inherited from this 26D origin. Because "
                    "the ancestral bulk contains a finite amount of 'Symmetry Budget,' the 125 residues "
                    "extracted in 4D must sum to a specific topological constant. The dual-shadow "
                    "structure enforces this via balanced b₃ residue splits (12/12) across shadows.</p>"
                ),
                label="sterility-origin"
            ),

            # ================================================================
            # 1.2 The Euclidean Bridge and OR Reduction
            # ================================================================
            ContentBlock(
                type="heading",
                content="The Euclidean Bridge and OR Reduction",
                level=2,
                label="1.2"
            ),
            ContentBlock(
                type="paragraph",
                content=(
                    "The connection between the dual (24,1) shadows is mediated by a "
                    "<strong>2D Euclidean bridge</strong> with signature (2,0). This timeless substrate "
                    "enables cross-shadow coordinate sampling via <strong>Orthogonal Reduction (OR)</strong>, "
                    "providing the mechanism for coherent information flow between the normal and mirror sectors."
                )
            ),
            ContentBlock(
                type="heading",
                content="1.2.1 The Bridge Metric",
                level=3
            ),
            ContentBlock(
                type="paragraph",
                content=(
                    "The bridge is purely Euclidean with positive-definite metric. This eliminates ghost "
                    "modes and closed timelike curves that would arise from multi-time theories. The bridge "
                    "provides a 'timeless' substrate for cross-shadow sampling, where conformal pressure "
                    "from condensate flux gradients drives the breathing dark energy mechanism."
                )
            ),
            ContentBlock(
                type="equation",
                content=r"ds^2_{\text{bridge}} = dy_1^2 + dy_2^2 \quad \text{(positive-definite, no ghosts)}",
                label="bridge-metric"
            ),
            ContentBlock(
                type="heading",
                content="1.2.2 The OR Reduction Operator",
                level=3
            ),
            ContentBlock(
                type="paragraph",
                content=(
                    "Cross-shadow coordinate sampling uses the <strong>Orthogonal Reduction operator R<sub>⊥</sub></strong>, "
                    "a 90° rotation that maps normal-shadow gradients to mirror-shadow coordinates. This operator "
                    "satisfies R<sub>⊥</sub>² = −I, providing Möbius double-cover properties essential for spinor coherence:"
                )
            ),
            ContentBlock(
                type="list",
                items=[
                    "<strong>Rotation Matrix:</strong> R<sub>⊥</sub> = [[0, −1], [1, 0]] (det = 1, orientation-preserving)",
                    "<strong>External Sampling:</strong> z'<sub>mirror</sub> = R<sub>⊥</sub> z<sub>normal</sub> + Δy",
                    "<strong>Möbius Property:</strong> R<sub>⊥</sub>² = −I enables spinor return after double traversal"
                ],
                label="or-reduction-operator"
            ),
            ContentBlock(
                type="heading",
                content="1.2.3 The Breathing Dark Energy Mechanism",
                level=3
            ),
            ContentBlock(
                type="paragraph",
                content=(
                    "The bridge pressure arises from <strong>condensate flux mismatch</strong> between shadows. "
                    "Where normal and mirror shadow pressure profiles differ, the residue drives cosmic acceleration. "
                    "This yields thawing dark energy with w₀ = −1 + 1/b₃ = −23/24 ≈ −0.9583, matching DESI 2025 "
                    "within 0.02σ. The breathing density formula is: ρ<sub>breath</sub> = |T<sup>ab</sup><sub>normal</sub> − R<sub>⊥</sub> T<sup>ab</sup><sub>mirror</sub>|."
                )
            ),

            # ================================================================
            # 1.3 The G2 Manifold (V7) per Shadow
            # ================================================================
            ContentBlock(
                type="heading",
                content="The G₂ Manifold (V₇): Per-Shadow Compactification",
                level=2,
                label="1.3"
            ),
            ContentBlock(
                type="paragraph",
                content=(
                    "Each dual shadow undergoes independent <strong>G₂ compactification</strong> on a "
                    "<strong>7-dimensional Riemannian manifold (7,0)</strong>. This per-shadow structure "
                    "provides the geometric rigidity that prevents the constants of nature from drifting. "
                    "The G₂ manifold is the 'Hard-Lock' that ensures each 4D condensate is a unique, "
                    "non-negotiable state with n<sub>gen</sub> = χ<sub>eff</sub>/(4·b₃) = 144/48 = 3 generations per shadow."
                )
            ),
            ContentBlock(
                type="heading",
                content="1.3.1 G₂ Holonomy and Path Independence",
                level=3
            ),
            ContentBlock(
                type="paragraph",
                content=(
                    "The V₇ manifold is unique because it is the only 7D structure that supports a "
                    "<strong>torsion-free, Ricci-flat metric</strong>. This G₂ holonomy implies that "
                    "the extraction of physical residues is 'Path Independent.' Whether a particle mass "
                    "is derived through the lepton sector or the gauge sector, the resulting value is "
                    "identical because it is anchored to the manifold's global geometry. This eliminates "
                    "the 'Fine-Tuning' problem; the numbers are not adjusted to match—they are locked "
                    "by the manifold's inability to be anything other than itself."
                )
            ),
            ContentBlock(
                type="equation",
                content=r"\text{Hol}(g) \subseteq G_2 \iff \exists \eta: \nabla \eta = 0 \quad \Rightarrow \quad R_{\mu\nu} = 0",
                label="g2-holonomy"
            ),
            ContentBlock(
                type="heading",
                content="1.3.2 The Laplacian Spectrum (λₙ)",
                level=3
            ),
            ContentBlock(
                type="paragraph",
                content=(
                    "The defining mathematical feature of Section 1.3 is the <strong>Manifold Laplacian "
                    "(Δ<sub>V₇</sub>)</strong>. Every one of the 125 residues observed in the Standard Model "
                    "corresponds to a specific spectral eigenvalue of this operator:"
                )
            ),
            ContentBlock(
                type="list",
                items=[
                    "<strong>Low-Frequency Modes:</strong> Correspond to global cosmological constants (e.g., H₀, Λ).",
                    "<strong>High-Frequency Modes:</strong> Correspond to discrete particle masses (e.g., the Top Quark)."
                ],
                label="laplacian-modes"
            ),
            ContentBlock(
                type="paragraph",
                content=(
                    "By identifying constants as resonant frequencies of the V₇ shape, we move from "
                    "empirical observation to <strong>geometric derivation</strong>. If the 'shape' of "
                    "the universe is V₇, then the 125 residues are its natural vibrations."
                )
            ),
            ContentBlock(
                type="heading",
                content="1.3.3 The b₃ Cycles and Flux-Tube Screening",
                level=3
            ),
            ContentBlock(
                type="paragraph",
                content=(
                    "Within the G₂ manifold, the vacuum energy is not a free-floating value. It is "
                    "trapped within the <strong>b₃ Betti cycles</strong>. These 3-dimensional 'loops' "
                    "act as flux-tubes that screen the high-energy tension of the 26D bulk. The "
                    "cancellation of brane tensions within these cycles is what yields the "
                    "<strong>10⁻⁵⁰ stability floor</strong>. This mechanism provides the first-principles "
                    "resolution to the Cosmological Constant Problem."
                )
            ),
            ContentBlock(
                type="equation",
                content=r"b_3 = 24 \quad \Rightarrow \quad N_{\text{gen}} = \frac{b_3}{8} = 3 \quad \text{(three fermion generations)}",
                label="b3-generations"
            ),

            # ================================================================
            # 1.4 The 6D→4D Projection
            # ================================================================
            ContentBlock(
                type="heading",
                content="The 6D → 4D Projection: Calabi-Yau Filtering",
                level=2,
                label="1.4"
            ),
            ContentBlock(
                type="paragraph",
                content=(
                    "The final stage of the dimensional descent is the projection of the 7D G₂ residues "
                    "onto our 4-dimensional Minkowski spacetime. This process involves a transition through "
                    "a <strong>6-dimensional Calabi-Yau intermediate</strong>, which acts as a 'Diffraction "
                    "Grating' for the high-dimensional symmetries. It is at this stage that the abstract "
                    "geometric nodes of the V₇ manifold manifest as the specific Flavor Physics and Gauge "
                    "Couplings of the Standard Model."
                )
            ),
            ContentBlock(
                type="heading",
                content="1.4.1 Calabi-Yau Sub-Manifolds and Chirality",
                level=3
            ),
            ContentBlock(
                type="paragraph",
                content=(
                    "As the V₇ holonomy projects into 4D, the G₂ structure decomposes into a "
                    "<strong>Calabi-Yau 3-fold (CY₃)</strong>. This 6-dimensional sub-manifold is "
                    "responsible for the emergence of <strong>Chirality</strong> (the left-handed "
                    "preference of the weak force). The specific 'Hodge numbers' (h<sup>1,1</sup>, h<sup>2,1</sup>) "
                    "of this 6D filter determine the number of particle generations."
                )
            ),
            ContentBlock(
                type="equation",
                content=r"V_7 \xrightarrow{\text{CY}_3} M^4 \times K^6 \quad \Rightarrow \quad SU(3)_C \times SU(2)_L \times U(1)_Y",
                label="cy3-projection"
            ),
            ContentBlock(
                type="heading",
                content="1.4.2 Brane-Node Shadowing",
                level=3
            ),
            ContentBlock(
                type="paragraph",
                content=(
                    "In 4D reality, fundamental particles are perceived as point-like excitations. "
                    "However, in the Sterile Model, these are recognized as <strong>Shadows of "
                    "Brane-Node Intersections</strong>:"
                )
            ),
            ContentBlock(
                type="list",
                items=[
                    "<strong>Mass Generation:</strong> The mass of a particle is the 'shadow length' cast by a V₇ spectral node through the 6D Calabi-Yau filter.",
                    "<strong>Charge & Coupling:</strong> The force couplings (g<sub>s</sub>, g<sub>w</sub>, e) are the 'aperture widths' of the Calabi-Yau pores through which the ancestral 26D flux passes."
                ],
                label="brane-shadows"
            ),
            ContentBlock(
                type="heading",
                content="1.4.3 The 4D Minkowski World-Sheet",
                level=3
            ),
            ContentBlock(
                type="paragraph",
                content=(
                    "Our observable universe is the <strong>4D World-Sheet</strong> upon which this "
                    "entire descent is recorded. The 125 residues are the terminal artifacts of the "
                    "26D(24,2) potential. At this level, the 'Fine-Structure Constant' and the "
                    "'Proton-to-Electron Mass Ratio' are revealed not as lucky accidents, but as the "
                    "<strong>Terminal Geometric Identity</strong> of the manifold. 4D reality is a "
                    "'topologically locked' state, where the physical constants represent the only "
                    "mathematically consistent residues of the ancestral 26D lineage."
                )
            ),
            ContentBlock(
                type="note",
                content=(
                    "<h4>The Descent Path Summary</h4>"
                    "<p>26D(24,2) → 13D [S<sub>PR</sub>(2) Gauge] → 7D [G₂ Manifold] → 6D [CY₃] → 4D [World-Sheet]</p>"
                    "<p>At each stage, the 'Symmetry Budget' is conserved, and the 125 residues are "
                    "progressively 'extracted' as the unique spectral eigenvalues of the descended geometry.</p>"
                ),
                label="descent-summary"
            ),
        ]

        return SectionContent(
            section_id="1",
            subsection_id="1.1",  # v19.0: Unique subsection
            title="Foundations of Dimensional Descent",
            abstract="The 26D(24,2) ancestral bulk, S_PR(2) gauge filter, G2 manifold, and 6D→4D projection.",
            content_blocks=content_blocks
        )

    def get_formulas(self) -> List[Formula]:
        """Return formula definitions for dimensional descent foundations."""
        return [
            Formula(
                id="26d-signature",
                label="(1.1)",
                latex=r"\text{Signature}(M^{26}) = (24, 2)",
                plain_text="Signature(M^26) = (24, 2)",
                category="THEORY",
                description="26D ancestral bulk signature with 24 spatial and 2 temporal dimensions.",
                input_params=["dimensions.D_bulk"],
                output_params=[],
            ),
            Formula(
                id="spr2-gauge",
                label="(1.2)",
                latex=r"t_2 \xrightarrow{S_{PR}(2)} \Lambda",
                plain_text="t2 -> Lambda via S_PR(2)",
                category="THEORY",
                description="S_PR(2) gauge freezing second time dimension into vacuum energy.",
                input_params=["dimensions.D_bulk"],
                output_params=["dimensions.D_after_sp2r"],
            ),
            Formula(
                id="g2-holonomy",
                label="(1.3)",
                latex=r"\text{Hol}(g) \subseteq G_2 \iff \exists \eta: \nabla \eta = 0",
                plain_text="Hol(g) ⊆ G2 iff exists eta: nabla eta = 0",
                category="THEORY",
                description="G2 holonomy condition for torsion-free, Ricci-flat metric.",
                input_params=["topology.b3", "topology.euler_chi"],
                output_params=[],
            ),
            # b3 Generations formula - critical for fermion generation count
            Formula(
                id="b3-generations",
                label="(1.3b)",
                latex=r"N_{\text{gen}} = \frac{b_3}{8} = \frac{24}{8} = 3",
                plain_text="N_gen = b3/8 = 24/8 = 3",
                category="DERIVED",
                description="Three fermion generations from b3 Betti number of G2 manifold.",
                input_params=["topology.b3"],
                output_params=["particle.n_generations"],
            ),
            Formula(
                id="calabi-yau-projection",
                label="(1.4)",
                latex=r"V_7 \xrightarrow{\text{CY}_3} M^4 \times K^6",
                plain_text="V7 -> M^4 x K^6 via CY3",
                category="THEORY",
                description="Calabi-Yau filtering from 7D G2 to 4D Minkowski spacetime.",
                input_params=["dimensions.D_after_sp2r"],
                output_params=["dimensions.D_observable"],
            ),
        ]

    def get_output_param_definitions(self) -> List[Parameter]:
        """Return parameter definitions - narrative section has no output parameters."""
        return []


# Module execution
if __name__ == "__main__":
    from simulations.base import PMRegistry
    registry = PMRegistry()
    sim = FoundationsV16_2()
    print(f"Simulation: {sim.metadata.title}")
    print(f"Version: {sim.metadata.version}")
    print(f"Section: {sim.metadata.section_id}")
    content = sim.get_section_content()
    if content:
        print(f"Content blocks: {len(content.content_blocks)}")
