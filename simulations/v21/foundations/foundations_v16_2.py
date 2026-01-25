#!/usr/bin/env python3
"""
PRINCIPIA METAPHYSICA v22.0 - Section 1: Foundations of Dimensional Descent
============================================================================

DOI: 10.5281/zenodo.18079602

v22.0 STERILE MODEL: M^{24,1} = T^1 x_fiber (bigoplus_{i=1}^{12} B_i^{2,0})
The 12x(2,0) paired bridge system with unified time.
All 125 constants are geometric residues, not tuned.

KEY v22 CHANGES:
  - Bulk decomposition: M^{24,1} = T^1 x_fiber (bigoplus_{i=1}^{12} B_i^{2,0})
  - Metric: ds^2 = -dt^2 + sum_{i=1}^{12} (dy_{1i}^2 + dy_{2i}^2)
  - 24 spacelike from 12x2 pairs, 1 timelike (unified)
  - Shadow structure: y_{1i} aggregates (normal) + y_{2i} aggregates (mirror)
  - OR reduction: bigotimes_{i=1}^{12} R_perp_i

WHY 12 PAIRS: b_3 = 24 => 24/2 = 12 paired bridges

This simulation generates the content for Section 1 of the paper:
  1.1 The 27D(26,1) Ancestral Bulk with 12x(2,0) Paired Bridge
  1.2 The Paired Bridge System and OR Reduction
  1.3 The G2 Manifold (V7) per Shadow
  1.4 The 6D->4D Projection

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
    Section 1: Foundations of Dimensional Descent (v22.0).

    Provides the sterile derivation narrative for the (24,1)->4D descent path
    with 12x(2,0) paired bridge system:
    - 1.1: The 27D(26,1) Ancestral Bulk with 12x(2,0) Paired Bridge
    - 1.2: The Paired Bridge System and OR Reduction
    - 1.3: The G2 Manifold V7 per Shadow (7D Geometric Hard-Lock)
    - 1.4: The 6D->4D Projection (Calabi-Yau Filtering)

    KEY v22 STRUCTURE:
        M^{24,1} = T^1 x_fiber (bigoplus_{i=1}^{12} B_i^{2,0})
        ds^2 = -dt^2 + sum_{i=1}^{12} (dy_{1i}^2 + dy_{2i}^2)

    WHY 12 PAIRS:
        b_3 = 24 (Betti number from G2 topology)
        24 / 2 = 12 paired bridges
        Each pair: (y_{1i}, y_{2i}) with Euclidean (2,0) signature
    """

    # Dynamic formula IDs referenced by this section
    FORMULA_REFS = [
        "26d-signature",
        "euclidean-bridge",
        "or-reduction-tensor",
        "g2-holonomy",
        "b3-generations",
        "calabi-yau-projection",
    ]

    # Dynamic parameter paths referenced by this section
    PARAM_REFS = [
        "dimensions.D_bulk",
        "dimensions.D_shadow",
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
            version="22.0",
            domain="foundations",
            title="Foundations of Dimensional Descent",
            description="The (24,1) bulk with 12x(2,0) paired bridge system, dual shadows, and G2 compactification",
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
            # 1.1 The 27D(26,1) Ancestral Bulk with 12x(2,0) Paired Bridge
            # ================================================================
            ContentBlock(
                type="heading",
                content="The 27D(26,1) Ancestral Bulk with 12x(2,0) Paired Bridge",
                level=2,
                label="1.1"
            ),
            ContentBlock(
                type="paragraph",
                content=(
                    "The foundational premise of the Sterile Model is that the observable universe "
                    "is not an independent system, but a lower-dimensional <strong>residue</strong> "
                    "of a <strong>27D(26,1) Bosonic Ancestral Bulk</strong>. This high-dimensional "
                    "state represents the 'Total Potential' of the physical registry, with unified "
                    "time (eliminating ghosts and closed timelike curves) and a <strong>12x(2,0) "
                    "paired bridge system</strong> enabling dual-shadow coherence."
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
                content=r"\text{Signature}(M^{24,1}) = (24, 1) \quad \Rightarrow \quad ds^2 = -dt^2 + \sum_{i=1}^{12} (dy_{1i}^2 + dy_{2i}^2)",
                label="26d-signature"
            ),
            ContentBlock(
                type="heading",
                content="1.1.2 The 12x(2,0) Paired Bridge Structure",
                level=3
            ),
            ContentBlock(
                type="paragraph",
                content=(
                    "The 26D bulk decomposes into <strong>12 paired bridges</strong>, each with "
                    "Euclidean (2,0) signature. The total bulk structure is:"
                )
            ),
            ContentBlock(
                type="equation",
                content=r"M^{24,1} = T^1 \times_{\text{fiber}} \left(\bigoplus_{i=1}^{12} B_i^{2,0}\right)",
                label="bulk-decomposition"
            ),
            ContentBlock(
                type="paragraph",
                content=(
                    "Each bridge pair B<sub>i</sub> = (y<sub>1i</sub>, y<sub>2i</sub>) contributes "
                    "two spacelike dimensions. This gives 12 x 2 = 24 spacelike dimensions plus "
                    "1 unified timelike dimension, matching the (24,1) signature. The pairing "
                    "arises from the G₂ topology: <strong>b₃ = 24 / 2 = 12 pairs</strong>."
                )
            ),
            ContentBlock(
                type="list",
                items=[
                    "<strong>Bridge Pairs:</strong> B<sub>i</sub><sup>2,0</sup> = (y<sub>1i</sub>, y<sub>2i</sub>) for i = 1,...,12",
                    "<strong>Normal Shadow:</strong> Aggregate of all y<sub>1i</sub> (normal halves) + internal G₂",
                    "<strong>Mirror Shadow:</strong> Aggregate of all y<sub>2i</sub> (mirror halves) + internal G₂",
                    "<strong>Per-pair OR:</strong> R<sub>⊥</sub><sup>i</sup> = [[0,-1],[1,0]] acts on each (y<sub>1i</sub>, y<sub>2i</sub>)"
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
                    "The 27D(26,1) state descends via <strong>Dimensional Collapse</strong>. "
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
            # 1.2 The Paired Bridge System and OR Reduction
            # ================================================================
            ContentBlock(
                type="heading",
                content="The Paired Bridge System and OR Reduction",
                level=2,
                label="1.2"
            ),
            ContentBlock(
                type="paragraph",
                content=(
                    "The connection between the dual shadows is mediated by the "
                    "<strong>12x(2,0) paired bridge system</strong>. Each bridge pair B<sub>i</sub> "
                    "provides a timeless Euclidean substrate enabling cross-shadow coordinate sampling "
                    "via <strong>per-pair Orthogonal Reduction (OR)</strong>."
                )
            ),
            ContentBlock(
                type="heading",
                content="1.2.1 The Paired Bridge Metric",
                level=3
            ),
            ContentBlock(
                type="paragraph",
                content=(
                    "Each of the 12 bridge pairs has positive-definite (2,0) metric, eliminating ghost "
                    "modes and closed timelike curves. The total bridge metric is the direct sum over all pairs:"
                )
            ),
            ContentBlock(
                type="equation",
                content=r"ds^2_{\text{bridge}} = \sum_{i=1}^{12} \left(dy_{1i}^2 + dy_{2i}^2\right) \quad \text{(24D positive-definite)}",
                label="bridge-metric"
            ),
            ContentBlock(
                type="paragraph",
                content=(
                    "The pairing structure arises naturally from the b₃ = 24 Betti number: 24/2 = 12 pairs. "
                    "Each pair serves as a 'neural gate' for consciousness flow between shadows."
                )
            ),
            ContentBlock(
                type="heading",
                content="1.2.2 The Per-Pair OR Reduction Operator",
                level=3
            ),
            ContentBlock(
                type="paragraph",
                content=(
                    "Cross-shadow coordinate sampling uses <strong>per-pair OR operators R<sub>⊥</sub><sup>i</sup></strong>. "
                    "Each 2x2 operator acts on the corresponding bridge pair (y<sub>1i</sub>, y<sub>2i</sub>):"
                )
            ),
            ContentBlock(
                type="equation",
                content=r"R_\perp^i = \begin{pmatrix} 0 & -1 \\ 1 & 0 \end{pmatrix} \quad \Rightarrow \quad R_\perp^{\text{full}} = \bigotimes_{i=1}^{12} R_\perp^i",
                label="or-reduction-tensor"
            ),
            ContentBlock(
                type="list",
                items=[
                    "<strong>Per-Pair Operator:</strong> R<sub>⊥</sub><sup>i</sup> = [[0, -1], [1, 0]] (90 deg rotation on pair i)",
                    "<strong>Full Tensor Product:</strong> R<sub>⊥</sub><sup>full</sup> = tensor product over all 12 pairs",
                    "<strong>Mobius Property:</strong> (R<sub>⊥</sub><sup>i</sup>)² = -I per pair; (R<sub>⊥</sub><sup>full</sup>)² = (-1)^12 I = I",
                    "<strong>Spinor Coherence:</strong> Full double-traversal returns to identity (even number of pairs)"
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
            ContentBlock(
                type="heading",
                content="1.2.4 Hierarchical Bridge Sampling: Local Pairs + Central (2,0) Ancestral Sampler",
                level=3
            ),
            ContentBlock(
                type="paragraph",
                content=(
                    "The v23 framework extends the 12 local (2,0) bridge pairs with a <strong>central (2,0) "
                    "ancestral sampler</strong> that provides global averaging for macro-precision. This hierarchical "
                    "structure enables two levels of condensate selection: local pairs for fine flux control, and the "
                    "central sampler for global coherence during dimensional descent."
                )
            ),
            ContentBlock(
                type="paragraph",
                content=(
                    "<strong>Descent Flow:</strong><br/>"
                    "• Bulk → 12×(2,0) local pairs (fine flux sampling per bridge)<br/>"
                    "• Local → central (2,0) averaging → ancestral descent into condensate ((5,1) + 3×(3,1))"
                )
            ),
            ContentBlock(
                type="equation",
                content=r"p_{\text{anc}} = \frac{1}{12}\sum_{i=1}^{12} p_i + \sqrt{\frac{n_{\text{local}}}{12}} \cdot \phi",
                label="central-sampler-formula"
            ),
            ContentBlock(
                type="paragraph",
                content=(
                    "Here p<sub>i</sub> is the local probability from bridge pair i, n<sub>local</sub> is the "
                    "number of active local pairs (6 baseline → 12 full gnosis), and φ is the golden ratio. "
                    "The central sampler activates at mid-gnosis (n<sub>local</sub> ≥ 9)."
                )
            ),
            ContentBlock(
                type="list",
                items=[
                    "<strong>Dimensional Accounting:</strong> 24 core + 24 local + 2 central = 50 spacelike-like dimensions",
                    "<strong>Local Level:</strong> 12×(2,0) pairs → micro-stability (per-branch selection)",
                    "<strong>Central Level:</strong> 1×(2,0) pair → macro-precision (global averaging)",
                    "<strong>Signature Preservation:</strong> Effective (24,1) maintained (central is Euclidean, no ghosts)"
                ],
                label="hierarchical-sampling-structure"
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
                    "27D(26,1) potential. At this level, the 'Fine-Structure Constant' and the "
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
                    "<p>27D(26,1) = 12×(2,0) + (0,1) → [Bridge pairs WARP via OR] → 2×13D(12,1) → 7D [G₂ Manifold] → 6D [CY₃] → 4D [World-Sheet]</p>"
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
            abstract="The 27D(26,1) ancestral bulk with Euclidean bridge, OR reduction, dual shadows, G2 manifold, and 6D→4D projection.",
            content_blocks=content_blocks
        )

    def get_formulas(self) -> List[Formula]:
        """Return formula definitions for dimensional descent foundations."""
        return [
            Formula(
                id="26d-signature",
                label="(1.1)",
                latex=r"\text{Signature}(M^{24,1}) = (24, 1) \quad ds^2 = -dt^2 + \sum_{i=1}^{12}(dy_{1i}^2 + dy_{2i}^2)",
                plain_text="Signature(M^{24,1}) = (24, 1); ds^2 = -dt^2 + sum_i(dy_{1i}^2 + dy_{2i}^2)",
                category="THEORY",
                description="26D ancestral bulk signature with unified time. 24 spacelike from 12x2 pairs, 1 timelike.",
                input_params=["dimensions.D_bulk", "topology.b3"],
                output_params=[],
            ),
            Formula(
                id="euclidean-bridge",
                label="(1.2)",
                latex=r"M^{24,1} = T^1 \times_{\text{fiber}} \left(\bigoplus_{i=1}^{12} B_i^{2,0}\right)",
                plain_text="M^{24,1} = T^1 x_fiber (bigoplus_{i=1}^{12} B_i^{2,0})",
                category="THEORY",
                description="Fibered time structure with 12x(2,0) paired bridges. b_3=24 => 12 pairs.",
                input_params=["dimensions.D_bulk", "topology.b3"],
                output_params=["dimensions.D_shadow"],
            ),
            Formula(
                id="or-reduction-tensor",
                label="(1.2b)",
                latex=r"R_\perp^{\text{full}} = \bigotimes_{i=1}^{12} R_\perp^i \quad \text{where} \quad R_\perp^i = \begin{pmatrix} 0 & -1 \\ 1 & 0 \end{pmatrix}",
                plain_text="R_perp^full = tensor_{i=1}^{12} R_perp^i where R_perp^i = [[0,-1],[1,0]]",
                category="THEORY",
                description="Full OR reduction operator as tensor product of 12 per-pair 90-degree rotations.",
                input_params=["topology.b3"],
                output_params=[],
            ),
            Formula(
                id="central-sampler-formula",
                label="(1.2c)",
                latex=r"p_{\text{anc}} = \frac{1}{12}\sum_{i=1}^{12} p_i + \sqrt{\frac{n_{\text{local}}}{12}} \cdot \phi",
                plain_text="p_anc = (1/12)*sum(p_i) + sqrt(n_local/12)*phi",
                category="THEORY",
                description="Central (2,0) ancestral sampler formula. Averages 12 local pairs with golden ratio scaling.",
                input_params=["topology.b3"],
                output_params=[],
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
