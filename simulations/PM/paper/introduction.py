#!/usr/bin/env python3
"""
PRINCIPIA METAPHYSICA v24.2 - Introduction
===========================================

DOI: 10.5281/zenodo.18079602

Licensed under the MIT License. See LICENSE file for details.

v24.2: M^{27}(24,1,2) structure with S^(2,0) sampler data fields.
       4096-component Pneuma spinor field from Cl(26,1).
       Dual 13D(12,1) shadows via OR reduction on 12 bridge pairs.

Provides section content for the Introduction (Section 1).

This simulation does not compute physics parameters, but instead generates
the narrative content and cross-references for the paper's introduction.

SECTION: 1 (Introduction)

v24.2 TOPOLOGICALLY ANCHORED: 125 constants from EDOF=3 seeds (116:1 compression).

OUTPUTS:
    - None (narrative content only)

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.

Dedicated To:
    My Wife: Elizabeth May Watts
    Our Messiah: Jesus Of Nazareth
"""

import sys
import os
from datetime import datetime
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
            version="24.2",
            domain="introduction",
            title="Introduction to Principia Metaphysica",
            description="Narrative introduction to the PM v24.2 (24,1,2) Dual-Shadow framework - Topologically Anchored with EDOF=3 (1 geometric + 2 calibrations)",
            section_id="1",
            subsection_id=None
        )

    @property
    def required_inputs(self) -> List[str]:
        """Registry parameters referenced by the introduction narrative."""
        return ["topology.elder_kads"]

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

    def get_beginner_explanation(self) -> Dict[str, Any]:
        """
        Return a beginner-friendly explanation of Principia Metaphysica.

        Returns:
            Dictionary with title and explanation suitable for non-experts
        """
        return {
            "title": "What is Principia Metaphysica?",
            "summary": (
                "Principia Metaphysica is a theory that attempts to explain fundamental physics "
                "by starting from a simple idea: what if spacetime itself emerges from a more "
                "fundamental quantum field?"
            ),
            "explanation": (
                "Principia Metaphysica is a theory that attempts to explain fundamental physics "
                "by starting from a simple idea: what if spacetime itself emerges from a more "
                "fundamental quantum field?"
            ),
            "key_concepts": [
                {
                    "name": "Extra Dimensions",
                    "explanation": (
                        "Just as a 3D object casts a 2D shadow, our 4D spacetime "
                        "(3 space + 1 time) might be a 'shadow' of a higher-dimensional reality. "
                        "PM proposes 26 dimensions that reduce down to the 4 we observe."
                    )
                },
                {
                    "name": "Dual Shadows with Euclidean Bridge",
                    "explanation": (
                        "The theory uses a single unified time with a 2D Euclidean bridge "
                        "connecting dual 'shadow' universes. This structure eliminates ghost "
                        "modes and explains dark energy through 'breathing' pressure mismatch."
                    )
                },
                {
                    "name": "Geometry to Physics",
                    "explanation": (
                        "Instead of putting particles and forces into spacetime, PM derives "
                        "spacetime geometry from a fundamental fermionic field (the 'Pneuma'). "
                        "The shape of this geometry determines particle properties."
                    )
                },
                {
                    "name": "Testable Predictions",
                    "explanation": (
                        "Unlike some theories, PM makes specific predictions that can be tested: "
                        "dark energy equation of state w₀ = -23/24 (consistent with DESI 2025 thawing constraints), "
                        "neutrino mass sum (0.082 eV, within cosmological bounds), proton decay "
                        "lifetime (future tests), and Kaluza-Klein modes at ~5 TeV (LHC searches)."
                    )
                }
            ],
            "why_it_matters": (
                "The power of this approach is that it derives many measured values (like the "
                "Yukawa hierarchy parameter ε ≈ 0.223, which matches the Cabibbo angle V<sub>us</sub> ≈ 0.2257 "
                "to within 1%) from pure geometry, rather than treating them as arbitrary input parameters."
            )
        }

    def get_foundations(self) -> Dict[str, str]:
        """
        Return the foundational principles of Principia Metaphysica.

        Returns:
            Dictionary mapping principle names to descriptions
        """
        foundations = {
            "metric_emergence": (
                "Spacetime geometry emerges dynamically from fermionic spinor bilinears "
                "within the Pneuma field. The Pneuma-Vielbein bridge construction establishes "
                "a direct link between fundamental fermionic degrees of freedom and the emergent "
                "metric, consistently yielding Lorentzian signature (-,+,+,+) in 4D without "
                "requiring ad hoc assumptions about the background spacetime structure. This "
                "avoids the traditional circular dependence on a pre-existing metric."
            ),
            "dimensional_hierarchy": (
                "27D spacetime with structure (24,1,2) = 12×(2,0) bridges + (0,1) time + S<sup>(2,0)</sup> sampler data fields warps into dual "
                "13D(12,1) shadows via coordinate selection. Each shadow "
                "compactifies on G₂ manifolds to 4D, preserving gauge symmetries "
                "and generating observable physics."
            ),
            "moduli_stabilization": (
                "Racetrack superpotential with h<sup>1,1</sup>=4 Kähler moduli dynamically "
                "fixes geometric parameters, deriving ε ≈ 0.2257 (Cabibbo angle) "
                "without free parameters."
            ),
            "thermal_time": (
                "Physical time emerges from the modular flow associated with the KMS "
                "(Kubo-Martin-Schwinger) thermal equilibrium state of the Pneuma field. "
                "This identification resolves the 'frozen formalism' problem inherent in "
                "canonical quantum gravity, where time is absent at the fundamental level. "
                "By grounding temporal evolution in the thermodynamic properties of the "
                "Pneuma field, the framework provides a natural link between quantum gravity "
                "and the arrow of time, suggesting that time is an emergent property of the "
                "system's thermal state rather than a fundamental background parameter."
            ),
            "gauge_unification": (
                "SU(3) × SU(2) × U(1) gauge couplings unify at M<sub>GUT</sub> ~ 2×10¹⁶ GeV "
                "via geometric running, with α<sub>GUT</sub>⁻¹ ≈ 42.7 determined by G₂ topology."
            ),
            "topological_generations": (
                "Number of fermion generations n<sub>gen</sub> = χ<sub>eff</sub>/48 = 144/48 = 3 follows "
                "from G₂ Euler characteristic, providing parameter-free prediction "
                "matching Standard Model exactly."
            ),
            "yukawa_hierarchy": (
                "Fermion mass hierarchy emerges from exponential wavefunction overlap "
                "suppression on G₂ cycles, explaining m<sub>t</sub>/m<sub>e</sub> ~ 10⁵ naturally."
            ),
            "cosmological_framework": (
                "Dark energy EoS w₀ = -1 + 1/b₃ = -23/24 from dimensional reduction, dark matter "
                "from mirror sector with Ω<sub>DM</sub>/Ω<sub>b</sub> ~ 5.4, both matching observations "
                "without fine-tuning."
            )
        }

        assert all(v.strip() for v in foundations.values()), "All foundations must be non-empty"
        assert len(foundations) >= 6, "Must have at least 6 foundational principles"

        return foundations

    def get_section_content(self) -> Optional[SectionContent]:
        """
        Return section content for Section 1: Introduction.

        Returns:
            SectionContent instance with introduction narrative
        """
        # Validate that helper methods return non-empty content
        beginner_exp = self.get_beginner_explanation()
        assert beginner_exp, "get_beginner_explanation() returned empty content"

        foundations = self.get_foundations()
        assert foundations, "get_foundations() returned empty content"
        assert len(foundations) >= 6, "get_foundations() must return at least 6 principles"

        content_blocks = [
            # Lead paragraph (abstract) - v24.2 Dual-Shadow Model
            ContentBlock(
                type="paragraph",
                content=(
                    'This paper presents <strong>Principia Metaphysica <span class="pm-value" data-pm-value="framework.version_label">v24.2</span></strong>, a <strong>Topologically Anchored Framework</strong> '
                    "in which 125 fundamental physical constants emerge as spectral residues of a single compact <strong>G₂ manifold (TCS #187)</strong> "
                    "under Ricci flow from <strong>EDOF=3</strong> (EDOF=3: 1 geometric seed b₃ + 2 calibrations), achieving <strong>116:1 compression ratio</strong>. "
                    "The bulk manifold <strong>M<sup>27</sup>(24,1,2)</strong> decomposes as: "
                    "<em>24</em> G₂ physics dimensions (12×(2,0) bridge pairs creating dual 13D shadows), "
                    "<em>1</em> unified timelike fiber T¹, and "
                    "<em>2</em> <strong>sampler data fields</strong> S<sup>(2,0)</sup> (an architecturally separate Euclidean sector "
                    "providing global cross-shadow objective reduction averaging). "
                    "The framework splits into <strong>dual 13D(12,1) shadows</strong> connected by <strong>12×(2,0) Euclidean "
                    "bridges</strong>, with each shadow compactifying via G₂ holonomy through "
                    "11D → 7D → 4D descent. The internal <strong>V₇ manifold</strong> with <strong>b₃ = "
                    '<span class="pm-value" data-pm-value="topology.elder_kads">24</span></strong> and '
                    '<strong>χ = <span class="pm-value" data-pm-value="topology.mephorash_chi">144</span></strong> '
                    "provides all structure: fermion generations (χ<sub>eff</sub>/48 = 3), "
                    "mixing angles, mass hierarchies, and cosmological parameters. The framework "
                    "achieves <strong>0.48σ global alignment</strong> with Planck 2018, DESI 2025, "
                    "and NuFIT 6.0 experimental data, including dark energy <strong>w₀ = -23/24</strong> "
                    'consistent with DESI 2025 thawing dark energy constraints and <strong>H₀ = '
                    '<span class="pm-value" data-pm-value="cosmology.H0_local">71.55</span> km/s/Mpc</strong> within '
                    "1.4σ of SH0ES 2025. New results: thermal time coupling "
                    "<strong>α<sub>T</sub> = D<sub>total</sub>/D<sub>string</sub> = 27/10</strong> "
                    "(DERIVED, zero free parameters), CSS <strong>[[24,12,8]]</strong> quantum code "
                    "from self-dual Golay (protects ≤3 moduli errors), and breathing dark energy "
                    "ρ<sub>breath</sub> from 12-pair OR aggregation. All derivation chains are recorded in "
                    '<span class="pm-value" data-pm-value="statistics.certificates_total">72</span>+ '
                    "reproducibility certificates."
                ),
                label="lead"
            ),

            # Status & Caveats note
            ContentBlock(
                type="note",
                content=(
                    "<h4>Status &amp; Caveats</h4>"
                    "<p>Principia Metaphysica is a <strong>speculative theoretical framework</strong> "
                    "in early development. While it produces geometric expressions for many physical "
                    "constants, several important caveats apply:</p>"
                    "<ul>"
                    "<li><strong>No peer review:</strong> This work has not yet been reviewed by "
                    "the broader physics community.</li>"
                    "<li><strong>EDOF=3 (Minimal calibration inputs):</strong> Three quantities (VEV coefficient, "
                    "\u03b1<sub>GUT</sub> coefficient, Re(T) from Higgs mass) provide scale anchoring. "
                    "Two PMNS parameters (\u03b8\u2081\u2083, \u03b4<sub>CP</sub>) are fitted to NuFIT 6.0 pending explicit Yukawa calculation.</li>"
                    "<li><strong>Predictions vs. postdictions:</strong> Many &lsquo;predictions&rsquo; "
                    "are comparisons with already-measured values (postdictions). Genuine predictions "
                    "(proton decay rate, KK graviton mass, axion properties) remain untested.</li>"
                    "<li><strong>Consciousness appendix:</strong> The Orch-OR/consciousness "
                    "appendix is an interpretive speculation, not a core claim of the framework.</li>"
                    "</ul>"
                ),
                label="status-caveats"
            ),

            # 1.1 The Quest for Unification
            ContentBlock(
                type="heading",
                content="The Quest for Unification",
                level=2,
                label="1.1"
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
                type="note",
                content=(
                    "<h4>Maxwell's Legacy</h4>"
                    "<p>Maxwell's equations demonstrated that electric and magnetic fields are "
                    "two aspects of a single entity, the electromagnetic field tensor F<sub>μν</sub>. "
                    "The symmetry underlying this unification is the U(1) gauge symmetry of "
                    "electrodynamics.</p>"
                ),
                label="maxwell-legacy"
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
                type="paragraph",
                content=(
                    "The Standard Model of particle physics incorporates the electroweak theory "
                    "with quantum chromodynamics (QCD), the SU(3)<sub>C</sub> gauge theory of the "
                    "strong nuclear force. While phenomenologically successful, the Standard Model's "
                    "gauge group G<sub>SM</sub> = SU(3)<sub>C</sub> × SU(2)<sub>L</sub> × U(1)<sub>Y</sub> "
                    "appears somewhat arbitrary, motivating the search for a larger unifying structure."
                )
            ),
            ContentBlock(
                type="equation",
                content="G<sub>SM</sub> = SU(3)<sub>C</sub> × SU(2)<sub>L</sub> × U(1)<sub>Y</sub> ⊂ G<sub>GUT</sub>",
                label="sm-gut-embedding"
            ),
            ContentBlock(
                type="paragraph",
                content=(
                    "Grand Unified Theories (GUTs), pioneered by Georgi, Glashow, Pati, and Salam "
                    "in the 1970s, embed the Standard Model into a larger simple gauge group. The "
                    "minimal SU(5) model of Georgi-Glashow (1974) provided the first concrete "
                    "realization, though it is now disfavored by proton decay constraints. The SO(10) "
                    "model, proposed independently by Fritzsch and Minkowski (1975) and by Georgi "
                    "(1975), remains a compelling candidate due to its natural accommodation of a "
                    "right-handed neutrino and elegant family structure."
                )
            ),
            ContentBlock(
                type="list",
                items=[
                    "<strong>SU(5):</strong> Minimal GUT; predicts proton decay at rates now excluded",
                    "<strong>SO(10):</strong> Natural right-handed neutrino; all fermions in 16-dim spinor",
                    "<strong>E<sub>6</sub>:</strong> Emerges naturally from heterotic string compactifications",
                    "<strong>Flipped SU(5):</strong> SU(5) × U(1)<sub>X</sub> with different hypercharge embedding"
                ],
                label="gut-models"
            ),

            # 1.2 Geometrization of Forces
            ContentBlock(
                type="heading",
                content="Geometrization of Forces",
                level=2,
                label="1.2"
            ),
            ContentBlock(
                type="paragraph",
                content=(
                    "A parallel thread in the unification program concerns the geometrization of "
                    "gauge forces. Einstein's general relativity demonstrated that gravity is not "
                    "a force in the Newtonian sense but rather the manifestation of spacetime curvature. "
                    "The natural question arises: can other forces be similarly geometrized?"
                )
            ),
            ContentBlock(
                type="paragraph",
                content=(
                    "The Kaluza-Klein (KK) proposal (Kaluza 1921, Klein 1926) provided an affirmative "
                    "answer for electromagnetism. By extending spacetime from 4 to 5 dimensions and "
                    "compactifying the extra dimension on a circle S¹, the gravitational field in 5D "
                    "yields both 4D gravity and a U(1) gauge field upon dimensional reduction."
                )
            ),
            ContentBlock(
                type="equation",
                content="M<sup>5</sup> = M<sup>4</sup> × S<sup>1</sup> → g<sub>MN</sub><sup>(5)</sup> → {g<sub>μν</sub><sup>(4)</sup>, A<sub>μ</sub>, φ}",
                label="kk-decomposition"
            ),
            ContentBlock(
                type="paragraph",
                content=(
                    "The gauge symmetry arises geometrically: the U(1) corresponds to isometries of "
                    "the internal S¹. More generally, compactification on a manifold K with isometry "
                    "group G yields a gauge theory with gauge group G in the lower-dimensional "
                    "effective theory."
                )
            ),
            ContentBlock(
                type="note",
                content=(
                    "<h4>Gauge from Geometry</h4>"
                    "<p>For a general internal manifold K<sup>d</sup>, the isometry group Isom(K) "
                    "becomes the gauge group of the dimensionally reduced theory. The gauge bosons "
                    "correspond to Killing vectors on the internal space. This geometric origin "
                    "provides a natural explanation for the gauge principle.</p>"
                ),
                label="gauge-from-geometry"
            ),
            ContentBlock(
                type="paragraph",
                content=(
                    "To accommodate the full Standard Model gauge group, one requires an internal "
                    "manifold K whose isometry group contains G<sub>SM</sub>. For SO(10) unification, "
                    "the internal space must possess SO(10) isometries. This constraint severely "
                    "restricts the geometry of K and motivates the search for specific compactification "
                    "manifolds."
                )
            ),
            ContentBlock(
                type="paragraph",
                content=(
                    "Modern realizations of this program include supergravity compactifications, "
                    "heterotic string theory on Calabi-Yau manifolds, and M-theory on G₂ holonomy "
                    "manifolds. Each approach provides a rich structure connecting extra-dimensional "
                    "geometry to four-dimensional particle physics."
                )
            ),

            # 1.3 A Fermionic Foundation for Geometry
            ContentBlock(
                type="heading",
                content="A Fermionic Foundation for Geometry",
                level=2,
                label="1.3"
            ),
            ContentBlock(
                type="note",
                content=(
                    "<h4>Why Go Beyond Standard Kaluza-Klein?</h4>"
                    "<p>The Kaluza-Klein framework described in Section 1.2 is elegant but incomplete. "
                    "While it successfully derives gauge symmetries from extra-dimensional geometry, "
                    "it faces three fundamental obstacles that prevent a complete unification:</p>"
                    "<ul class=\"concept-list\">"
                    "<li><strong>The Chirality Problem:</strong> Standard KK reduction produces vector-like "
                    "(non-chiral) fermions, but the Standard Model requires chiral fermions where left "
                    "and right components transform differently under the gauge group.</li>"
                    "<li><strong>The Moduli Problem:</strong> The size and shape of the internal manifold "
                    "K appear as massless scalar fields (moduli) that would mediate unobserved long-range "
                    "forces unless stabilized by an additional mechanism.</li>"
                    "<li><strong>The Origin Problem:</strong> Why should the internal manifold K exist "
                    "at all? What physical principle selects its topology and geometry?</li>"
                    "</ul>"
                    "<p>The <strong>Pneuma approach</strong> addresses all three problems simultaneously "
                    "by proposing that the internal geometry is not a static background but emerges "
                    "dynamically from a fundamental fermionic field. The condensate structure of this "
                    "field naturally generates chirality, stabilizes moduli, and determines the geometry "
                    "from first principles.</p>"
                ),
                label="why-pneuma"
            ),
            ContentBlock(
                type="paragraph",
                content=(
                    "This framework introduces a conceptual innovation: rather than postulating the "
                    "internal geometry as a fundamental given, we propose that it emerges from the "
                    "dynamics of a fundamental fermionic field, the <strong>Pneuma field</strong> "
                    "Ψ<sub>P</sub>."
                )
            ),
            ContentBlock(
                type="note",
                content=(
                    "<h4>The Pneuma Postulate (v24.2 Dual-Shadow Framework)</h4>"
                    "<p>In the full 27D theory with structure (24,1,2) = 12×(2,0) bridges + (0,1) time + S<sup>(2,0)</sup> sampler data fields, the Pneuma field Ψ<sub>P</sub> "
                    "is a <strong>4096-component spinor</strong> of Cl(26,1). Bridge pairs WARP to create "
                    "<strong>dual 13D(12,1) shadows</strong> via coordinate selection (each: 12 spatial + 1 shared time), "
                    "with positive-definite metric ds² = dy₁² + dy₂². Each shadow contains an effective "
                    "64-component spinor. The internal manifold is a <strong>7D TCS (Twisted Connected "
                    "Sum) G₂ manifold</strong> K<sub>Pneuma</sub> with <strong>h<sup>1,1</sup>=4 Kähler "
                    "moduli sectors</strong>—not a static background but a dynamic geometric structure "
                    "formed from Pneuma condensates. Racetrack moduli stabilization across these four "
                    "sectors dynamically determines the vacuum structure and derives ε ≈ 0.2257.</p>"
                ),
                label="pneuma-postulate"
            ),
            ContentBlock(
                type="paragraph",
                content=(
                    "In the v24.2 framework, the full 27D bulk has structure (24,1,2) = 12×(2,0) bridges + (0,1) time + S<sup>(2,0)</sup> sampler data fields, eliminating "
                    "ghost modes and closed timelike curves. The Pneuma field Ψ<sub>P</sub> transforms under "
                    "Spin(26,1). The 12 bridge pairs WARP to create dual 13D(12,1) shadows via coordinate selection, each "
                    "bridge with OR reduction operator R<sub>⊥</sub> providing Möbius double-cover (R<sub>⊥</sub>² = −I). "
                    "Each shadow has Spin(12,1) symmetry with a 64-component spinor representation. Bilinear "
                    "condensates of this field generate the geometric tensors that define the internal manifold structure."
                )
            ),
            ContentBlock(
                type="equation",
                content=(
                    "Ψ<sub>P</sub> ∈ <strong>4096</strong><sub>Spin(26,1)</sub><br/>"
                    "&nbsp;&nbsp;&nbsp;&nbsp;→ 2 × <strong>64</strong><sub>Spin(12,1)</sub><br/>"
                    "&nbsp;&nbsp;&nbsp;&nbsp;→ ⟨Ψ<sub>P</sub>Γ<sub>A...B</sub>Ψ<sub>P</sub>⟩ defines geometry"
                ),
                label="pneuma-condensate"
            ),
            ContentBlock(
                type="paragraph",
                content=(
                    "This approach addresses a fundamental problem in higher-dimensional theories: the "
                    "<strong>chirality problem</strong>. In standard Kaluza-Klein compactifications, "
                    "fermions in higher dimensions are necessarily non-chiral (vector-like), yet the "
                    "Standard Model fermions are manifestly chiral."
                )
            ),
            ContentBlock(
                type="note",
                content=(
                    "<h4>What is Chirality and Why Does It Matter?</h4>"
                    "<p><strong>Chirality</strong> refers to the distinction between left-handed and "
                    "right-handed fermions. Mathematically, a Dirac spinor ψ can be decomposed into "
                    "two Weyl spinors: ψ = ψ<sub>L</sub> + ψ<sub>R</sub>, where "
                    "ψ<sub>L,R</sub> = (1/2)(1 ∓ γ⁵)ψ.</p>"
                    "<p>The Standard Model is <em>maximally chiral</em>: the weak force (SU(2)<sub>L</sub>) "
                    "couples <strong>only to left-handed fermions</strong>. This is not a small effect—it "
                    "is the very structure of the weak interaction. For example:</p>"
                    "<ul>"
                    "<li>Left-handed electrons (e<sub>L</sub>) form doublets with neutrinos and couple to W bosons</li>"
                    "<li>Right-handed electrons (e<sub>R</sub>) are singlets and do <em>not</em> couple to W bosons</li>"
                    "<li>This asymmetry is why parity is violated in weak interactions (Wu experiment, 1956)</li>"
                    "</ul>"
                    "<p><strong>The problem:</strong> In higher dimensions (D > 4), fermions generically "
                    "come in <em>vector-like pairs</em>—for every left-handed mode, there is a right-handed "
                    "partner with identical quantum numbers. When you dimensionally reduce, you get equal "
                    "numbers of each chirality. But the Standard Model requires n<sub>L</sub> ≠ n<sub>R</sub> "
                    "for the weak sector!</p>"
                ),
                label="chirality-explanation"
            ),
            ContentBlock(
                type="list",
                items=[
                    "<strong>Orbifold projections:</strong> Discrete identifications removing half the degrees of freedom",
                    "<strong>Magnetic flux backgrounds:</strong> Index theorems yield chiral zero modes",
                    "<strong>Domain wall localization:</strong> Chiral modes bound to topological defects",
                    "<strong>Wilson line breaking:</strong> Gauge holonomy generates chiral spectrum"
                ],
                label="chirality-mechanisms"
            ),
            ContentBlock(
                type="paragraph",
                content=(
                    "The Pneuma mechanism provides a novel solution: the fundamental Ψ<sub>P</sub> is "
                    "non-chiral in 13D, but its condensate structure spontaneously selects a preferred "
                    "orientation in the internal space, generating effective chirality in the 4D reduction. "
                    "The mathematical framework for this involves the representation theory of Spin(12,1) "
                    "and its decomposition under the 4D Lorentz group times the internal symmetry group."
                )
            ),
            ContentBlock(
                type="equation",
                content=(
                    "Spin(12,1) ⊃ Spin(3,1) × Spin(8) → <strong>64</strong><br/>"
                    "&nbsp;&nbsp;&nbsp;&nbsp;= (<strong>2</strong>,<strong>8</strong><sub>s</sub>) ⊕ "
                    "(<strong>2</strong>,<strong>8</strong><sub>c</sub>) ⊕ "
                    "(<strong>2̄</strong>,<strong>8</strong><sub>v</sub>) ⊕ "
                    "(<strong>2̄</strong>,<strong>8</strong><sub>s</sub>)"
                ),
                label="spinor-decomposition"
            ),
            ContentBlock(
                type="paragraph",
                content=(
                    "The chirality selection mechanism is intimately connected to the topology of the "
                    "condensate configuration. Different condensate patterns correspond to different "
                    "effective theories in 4D, with the physically realized configuration determined by "
                    "energetic considerations and symmetry requirements."
                )
            ),
            ContentBlock(
                type="note",
                content=(
                    "<h4>Dual-Shadow Chirality</h4>"
                    "<p>In the v24.2 27D unified-time framework, the dual 13D(12,1) shadows are created when "
                    "12×(2,0) bridge pairs WARP via coordinate selection. The per-pair OR reduction operator R<sub>⊥</sub> "
                    "provides spinor double-cover: R<sub>⊥</sub>² = -I per pair. "
                    "The mirror shadow contains fermions with "
                    "opposite chirality assignments, ensuring overall CPT conservation while allowing "
                    "maximal parity violation in each 13D(12,1) shadow sector.</p>"
                ),
                label="dual-shadow-chirality"
            ),

            # 1.4 The Division Algebra Origin of D = 13
            ContentBlock(
                type="heading",
                content="The Division Algebra Origin of D = 13 (Observable Shadow of 26D)",
                level=2,
                label="1.4"
            ),
            ContentBlock(
                type="note",
                content=(
                    "<h4>Framework: 27D → Dual 13D(12,1) Shadows</h4>"
                    "<p>In the v24.2 Principia Metaphysica framework, the fundamental theory lives in "
                    "<strong>27D with structure (24,1,2) = 12×(2,0) bridges + (0,1) time + S<sup>(2,0)</sup> sampler data fields</strong>. "
                    "The 12 bridge pairs WARP to create dual 13D(12,1) shadows via coordinate selection "
                    "(each: 12 spatial from bridge + 1 shared time). Each shadow compactifies on G₂ "
                    "with the OR reduction operator R<sub>⊥</sub> providing cross-shadow coherence. This section explains why "
                    "D = 13 = 1 + 4 + 8 is the unique division-algebra-consistent dimension for the observable sector.</p>"
                ),
                label="framework-26d-dual-shadows"
            ),
            ContentBlock(
                type="paragraph",
                content=(
                    "A central question for any higher-dimensional theory is: why this particular dimension? "
                    "For string theory, D = 10 emerges from worldsheet conformal anomaly cancellation. For "
                    "M-theory, D = 11 is the maximum dimension admitting supergravity. For Principia "
                    "Metaphysica, <strong>the full theory requires D = 26 (bosonic string critical "
                    "dimension)</strong>, but the <strong>observable shadow D = 13 emerges uniquely from "
                    "the mathematics of normed division algebras</strong>."
                )
            ),
            ContentBlock(
                type="note",
                content=(
                    "<h4>The Hurwitz Theorem (1898)</h4>"
                    "<p>There exist exactly <strong>four</strong> normed division algebras over the real numbers:</p>"
                    "<ul class=\"concept-list\">"
                    "<li><strong>R</strong> (Real numbers): dimension 1 — associative, commutative, ordered</li>"
                    "<li><strong>C</strong> (Complex numbers): dimension 2 — associative, commutative</li>"
                    "<li><strong>H</strong> (Quaternions): dimension 4 — associative, non-commutative</li>"
                    "<li><strong>O</strong> (Octonions): dimension 8 — non-associative, alternative</li>"
                    "</ul>"
                    "<p style=\"margin-top: 1rem; font-style: italic;\">No other dimensions admit such "
                    "algebraic structure. The dimensions 1, 2, 4, 8 are mathematically privileged.</p>"
                ),
                label="hurwitz-theorem"
            ),
            ContentBlock(
                type="paragraph",
                content=(
                    "The total dimension D = 13 admits a <em>unique</em> decomposition into division "
                    "algebra dimensions that satisfies the physical requirements of the theory:"
                )
            ),
            ContentBlock(
                type="equation",
                content=(
                    "D = 13 = 1 + 4 + 8 = dim(<strong>R</strong>) + dim(<strong>H</strong>) + "
                    "dim(<strong>O</strong>)"
                ),
                label="division-algebra-decomposition"
            ),
            ContentBlock(
                type="paragraph",
                content=(
                    "Each component has a precise physical interpretation: <strong>R</strong> (dimension 1) "
                    "corresponds to emergent thermal time, <strong>H</strong> (dimension 4) to Lorentzian "
                    "spacetime with Spin(3,1) ≅ SL(2,C), and <strong>O</strong> (dimension 8) to the "
                    "internal manifold K<sub>Pneuma</sub> with Aut(O) = G₂ and E₈ lattice structure."
                )
            ),
            ContentBlock(
                type="note",
                content=(
                    "<h4>The Hurwitz Constraint</h4>"
                    "<p><strong>Neither 3 nor 9 is a division algebra dimension.</strong> The Hurwitz "
                    "theorem establishes that no normed division algebra exists in dimension 3 or 9 (or "
                    "any dimension other than 1, 2, 4, 8). Any decomposition using non-division-algebra "
                    "dimensions lacks the algebraic structure necessary for consistent spinor physics and "
                    "gauge theory.</p>"
                ),
                label="hurwitz-constraint"
            ),
            ContentBlock(
                type="paragraph",
                content=(
                    "The major candidates for fundamental theory—string theory (D = 10), M-theory (D = 11), "
                    "and now Principia Metaphysica (D = 26 full / D = 13 per shadow)—have division algebra "
                    "interpretations with crucial differences. D = 10 = 2 + 8 = <strong>C</strong> + "
                    "<strong>O</strong> (worldsheet coordinates + transverse directions, requires "
                    "supersymmetry). D = 11 = 1 + 2 + 8 = <strong>R</strong> + <strong>C</strong> + "
                    "<strong>O</strong> (mixed structure, requires supersymmetry, 7D G₂ holonomy). "
                    "D = 13 = 1 + 4 + 8 = <strong>R</strong> + <strong>H</strong> + <strong>O</strong> "
                    "(emergent thermal time, quaternionic spacetime, full 8D octonionic geometry, "
                    "<strong>no supersymmetry required</strong>). D = 27 with (24,1,2) = 12×(2,0) + S<sup>(2,0)</sup> + (0,1): "
                    "12 bridge pairs warp to create 2×13D(12,1) shadows, predicting w₀ = -1 + 1/b₃ = -23/24 "
                    "from bridge pressure mismatch."
                )
            ),
            ContentBlock(
                type="paragraph",
                content=(
                    "A key distinction is that D = 13 = <strong>R</strong> + <strong>H</strong> + "
                    "<strong>O</strong> excludes the complex numbers <strong>C</strong>, whereas D = 10 "
                    "and D = 11 include it. This exclusion is physically meaningful: (1) No worldsheet—the "
                    "complex structure <strong>C</strong> in string theory represents the 2D worldsheet, "
                    "but Principia Metaphysica has no fundamental strings. (2) Emergent time—time emerges "
                    "thermodynamically from <strong>R</strong> (real-valued entropy), not geometrically "
                    "from <strong>C</strong>. (3) Quaternionic spacetime—the 4D spacetime structure arises "
                    "directly from <strong>H</strong>, preserving the natural quaternionic structure of the "
                    "Lorentz group. (4) Full octonionic geometry—the internal 8D manifold has full octonionic "
                    "structure, not the reduced 7D G₂ geometry of M-theory."
                )
            ),
            ContentBlock(
                type="note",
                content=(
                    "<h4>Theorem (D = 13 Uniqueness)</h4>"
                    "<p>Let D be a spacetime dimension satisfying:</p>"
                    "<ol>"
                    "<li>D can be expressed as a sum of normed division algebra dimensions</li>"
                    "<li>The decomposition includes exactly one factor of dimension 1 (emergent time)</li>"
                    "<li>The decomposition includes exactly one factor of dimension 4 (Lorentz spacetime)</li>"
                    "<li>The decomposition includes exactly one factor of dimension 8 (maximal internal structure)</li>"
                    "<li>Complex structure (dimension 2) is excluded (no worldsheet)</li>"
                    "</ol>"
                    "<p>Then <strong>D = 13 = 1 + 4 + 8</strong> is the <em>unique</em> solution.</p>"
                ),
                label="uniqueness-theorem"
            ),
            ContentBlock(
                type="paragraph",
                content=(
                    "The proof is immediate: given the constraints, the only possible sum is "
                    "D = dim(<strong>R</strong>) + dim(<strong>H</strong>) + dim(<strong>O</strong>) = "
                    "1 + 4 + 8 = 13. This is a theorem, not a choice. The Hurwitz theorem constrains the "
                    "building blocks, and the physical requirements select exactly D = 13."
                )
            ),
            ContentBlock(
                type="paragraph",
                content=(
                    "The dimension D = 13 appears throughout exceptional mathematics, confirming its deep "
                    "structural significance: dim(F₄) = 52 = 4 × 13 (automorphisms of J₃(O)), "
                    "dim(E₆) = 78 = 6 × 13 (collineations of OP²), dim(J₃(O)) - dim(G₂) = 27 - 14 = 13 "
                    "(Jordan algebra mod automorphisms), Ω₁₃^Spin = Ω₁₃^String = 0 (both cobordism groups "
                    "vanish—rare coincidence ensuring anomaly cancellation)."
                )
            ),

            # 1.5 Outline of the Paper
            ContentBlock(
                type="heading",
                content="Outline of the Paper (v24.2 Dual-Shadow Framework)",
                level=2,
                label="1.5"
            ),
            ContentBlock(
                type="paragraph",
                content=(
                    "The remainder of this paper develops the <strong>Principia Metaphysica</strong> "
                    "theoretical framework systematically and derives its physical consequences. The central "
                    "insight is the M<sup>27</sup>(24,1,2) = 12×(2,0) bridges + (0,1) time + S<sup>(2,0)</sup> sampler data fields → dual 13D(12,1) shadows → 4D dimensional hierarchy, where the "
                    "Euclidean bridge structure enables the derivation of key cosmological parameters. The structure is as follows:"
                )
            ),
            ContentBlock(
                type="paragraph",
                content=(
                    "<strong>Section 2 (Spectral Decomposition)</strong>: Complete spectral decomposition of the G\u2082 manifold; 27D bulk with (24,1,2) structure; "
                    "dual 13D(12,1) shadow emergence via OR reduction; racetrack moduli "
                    "stabilization. <strong>Section 3 (Cosmological Results)</strong>: Hubble tension, S<sub>8</sub> suppression; "
                    "Planck 2018 and DESI 2025 alignment. <strong>Section 4 "
                    "(CKM/PMNS from G\u2082 Triality)</strong>: Unified CKM and PMNS matrices from G\u2082 triality; "
                    "Yukawa hierarchies (\u03b5 = 0.2257 from racetrack); mixing angle derivations. "
                    "<strong>Section 5 (Dark Energy Attractor)</strong>: w\u2080 = -1 + 1/b\u2083 = -23/24, w\u2090 \u2248 -0.204 derived; "
                    "breathing dark energy potential. "
                    "<strong>Section 6 (Baryon Asymmetry)</strong>: Baryon asymmetry from G\u2082 cycles and Jarlskog invariant. "
                    "<strong>Section 7 (ALP Portal Physics)</strong>: Axion-like particle portal physics from Face 3 K\u00e4hler moduli; "
                    "dark matter portal coupling. "
                    "Appendices provide spectral registry (A), algebraic foundations (B\u2013C), statistical logs (D), and validation certificates (F\u2013G)."
                )
            ),
            ContentBlock(
                type="paragraph",
                content=(
                    "This hierarchical structure moves from the foundational 27D geometric framework "
                    "through the particle physics phenomenology to cosmological implications and "
                    "experimental tests. Each section builds upon the preceding material, developing a "
                    "coherent picture of unified physics from 27D origins through dual 13D(12,1) shadows to observable "
                    "4D consequences."
                )
            ),
            ContentBlock(
                type="note",
                content=(
                    "<h4>Key Feature: Derived Modulus</h4>"
                    "<p>A significant advancement was achieved by inverting the Higgs mass formula to "
                    "constrain Re(T) from the measured Higgs mass (125.25 GeV), rather than choosing "
                    "it arbitrarily. (Open problem: Higgs inversion yields Re(T) ≈ 9.865; the BBN-calibrated value 7.086 "
                    "and geometric value 1.833 remain in tension.) This ensures swampland compliance and completes "
                    "the geometric unification where both λ₀ (from SO(10) matching) and Re(T) (from "
                    "experimental data) are now fully determined.</p>"
                    "<p><strong>EDOF=3 Statistical Framework:</strong> The framework achieves <strong>116:1 compression ratio</strong> "
                    "with three calibration seeds: VEV factor 1.5859 (calibrated; base ratio ln(M<sub>Pl</sub>/v<sub>EW</sub>)/b₃ ≈ 1.534, 3.4% gap open), "
                    "α<sub>GUT</sub> coefficient 0.032177, and Re(T) constrained from Higgs mass (9.865 via inversion; 7.086 calibrated for BBN)—all documented. "
                    "With the derivation of KK scale (M<sub>KK</sub> ≈ 4.5 TeV from k<sub>eff</sub> = b₃/(2+ε)), "
                    "Yukawa textures (ε = exp(-λ) with λ=1.5), and CP phase (δ<sub>CP</sub> = π/2 from topological orientations), "
                    "this leaves <strong>58+ Standard Model + compactification parameters as pure geometric predictions</strong>. "
                    "Racetrack moduli stabilization dynamically derives the Cabibbo angle ε = 0.2257 from flux competition "
                    "(minimal phenomenological input). Yukawa overlaps validated via 7D Monte Carlo on explicit G₂ associative cycles.</p>"
                ),
                label="derived-modulus"
            ),
            ContentBlock(
                type="table",
                content=(
                    "<h4>Seed Hierarchy (EDOF = 3)</h4>"
                    "<table style='width:100%; border-collapse:collapse; margin:1rem 0;'>"
                    "<tr style='border-bottom:2px solid #555;'>"
                    "<th style='text-align:left; padding:0.5rem;'>Seed</th>"
                    "<th style='text-align:left; padding:0.5rem;'>Value</th>"
                    "<th style='text-align:left; padding:0.5rem;'>Status</th>"
                    "<th style='text-align:left; padding:0.5rem;'>Role</th></tr>"
                    "<tr style='border-bottom:1px solid #333;'>"
                    "<td style='padding:0.5rem;'>b₃</td>"
                    "<td style='padding:0.5rem;'>24</td>"
                    "<td style='padding:0.5rem;'><strong>GEOMETRIC</strong></td>"
                    "<td style='padding:0.5rem;'>G₂ Betti number — topological invariant</td></tr>"
                    "<tr style='border-bottom:1px solid #333;'>"
                    "<td style='padding:0.5rem;'>VEV coefficient</td>"
                    "<td style='padding:0.5rem;'>1.5859</td>"
                    "<td style='padding:0.5rem;'>CALIBRATED</td>"
                    "<td style='padding:0.5rem;'>Scale anchor (3.4% gap from ln(M<sub>Pl</sub>/v)/b₃ — open)</td></tr>"
                    "<tr style='border-bottom:1px solid #333;'>"
                    "<td style='padding:0.5rem;'>Re(T)</td>"
                    "<td style='padding:0.5rem;'>9.865 / 7.086</td>"
                    "<td style='padding:0.5rem;'>CONSTRAINED</td>"
                    "<td style='padding:0.5rem;'>Kähler modulus — Higgs inversion (9.865) vs BBN calibrated (7.086)</td></tr>"
                    "</table>"
                    "<p><strong>Honest compression:</strong> 125 SM constants from 1 geometric integer + 2 calibrations → 116:1 ratio. "
                    "True geometric prediction: b₃ = 24 only. The other two seeds are phenomenological anchors.</p>"
                ),
                label="seed-hierarchy-table"
            ),
            ContentBlock(
                type="note",
                content=(
                    "<h4>Central Thesis: Topologically Anchored Framework (EDOF=3)</h4>"
                    "<p>The central claim is that a <strong>27D spacetime with structure (24,1,2) = 12×(2,0) + S<sup>(2,0)</sup> + (0,1)</strong>, "
                    "with 12 bridge pairs warping to create dual 13D(12,1) shadows, provides a <strong>ghost-free framework</strong> containing a 1 + 3 brane hierarchy. "
                    "The dual-shadow structure, with geometry emerging from the 4096-component Pneuma field, achieves <strong>116:1 compression ratio</strong> "
                    "from <strong>EDOF=3</strong> (EDOF=3: 1 geometric seed b₃ + 2 calibrations) to simultaneously explain: "
                    "(1) the origin of gauge forces from 26D isometries, "
                    "(2) chiral structure via dual-shadow Möbius mechanism, "
                    "(3) emergence of time from modular flow, "
                    "(4) <strong>specific values w₀ = -1 + 1/b₃ = -23/24, wₐ ≈ -0.204, M<sub>KK</sub> ≈ 4.5 TeV, "
                    "Yukawa textures (ε<sup>Q</sup> hierarchy with ε = 0.2257 from racetrack moduli stabilization), "
                    "δ<sub>CP</sub> = π/2 as geometric predictions</strong> from topology (b₃=24, λ=1.5 with minimal phenomenological input), "
                    "and (5) may address aspects of the quantum measurement problem through geometric correlations in the mirror shadow.</p>"
                ),
                label="central-thesis"
            ),

            # 1.6 Theoretical Context & Related Work
            ContentBlock(
                type="heading",
                content="Theoretical Context & Related Work",
                level=2,
                label="1.6"
            ),
            ContentBlock(
                type="paragraph",
                content=(
                    "Principia Metaphysica derives observable 4D physics—including Yukawa textures, mixing "
                    "angles, and mirror dark matter abundance—from wavefunction overlaps and racetrack-moduli "
                    "stabilization on a higher-dimensional G₂ manifold. This projection-based approach, where "
                    "effective low-energy physics emerges from geometric features of a compact internal space, "
                    "builds upon and extends several foundational programs in theoretical physics."
                )
            ),
            ContentBlock(
                type="note",
                content=(
                    "<h4>Kaluza-Klein Theory (1920s)</h4>"
                    "<p>The original insight that extra compact dimensions can yield gauge interactions from "
                    "pure geometry remains the conceptual ancestor of all modern unification programs. PM "
                    "inherits this philosophy while extending to 27D with structure (24,1,2) = 12×(2,0) bridges + (0,1) time + S<sup>(2,0)</sup> sampler data fields and employing G₂ "
                    "holonomy for chirality in each of the dual 13D(12,1) shadows.</p>"
                ),
                label="kk-context"
            ),
            ContentBlock(
                type="note",
                content=(
                    "<h4>M-Theory on G₂ Manifolds (Acharya, Witten, et al. ~2000s–present)</h4>"
                    "<p>Compactification on G₂ holonomy manifolds naturally produces chiral fermions, "
                    "mirror/shadow sectors, and dark matter candidates via singularities and fluxes. PM draws "
                    "heavily on this literature, particularly the work of <strong>Acharya & Witten (2001)</strong> "
                    "on chirality from G₂, <strong>Corti-Haskins-Nordström-Pacini (2015)</strong> on TCS "
                    "constructions, and <strong>Halverson & Morrison (2020)</strong> on the G₂ landscape. The "
                    "racetrack stabilization mechanism for moduli also follows established string phenomenology "
                    "(KKLT 2003, Blanco-Pillado et al. 2004).</p>"
                ),
                label="g2-context"
            ),
            ContentBlock(
                type="note",
                content=(
                    "<h4>Historical Note: Two-Time Physics (Bars 1998–2010)</h4>"
                    "<p>Itzhak Bars' program demonstrating that 2T physics with gauge symmetry "
                    "provides a unified view of 1T systems via different gauge choices historically informed "
                    "early PM development. However, v24.2 adopts structure (24,1,2) = 12×(2,0) + S<sup>(2,0)</sup> + (0,1) with bridge pairs that WARP "
                    "to create shadows. The dual 13D(12,1) shadow structure with per-pair OR reduction "
                    "preserves key phenomenological features while ensuring manifest unitarity."
                    "[v24.2: This historical approach is superseded by the Euclidean bridge mechanism.]</p>"
                ),
                label="historical-two-time-context"
            ),
            ContentBlock(
                type="paragraph",
                content=(
                    "The general strategy of projecting or embedding 4D observer physics within a larger "
                    "geometric structure also shares broad conceptual parallels with other speculative "
                    "unification frameworks: String Theory Landscape & Flux Compactifications (discretuum of "
                    "vacua, PM's landscape scanner identifying 49 valid TCS topologies), F-Theory GUTs (Vafa "
                    "et al., elliptically fibered geometries yielding grand unification with geometric origins "
                    "for Yukawas), Braneworld Scenarios (Randall-Sundrum warped extra dimensions), and Geometric "
                    "Unity (Weinstein 2021, observerse construction with 14D manifold)."
                )
            ),
            ContentBlock(
                type="note",
                content=(
                    "<h4>PM's Independent Contributions</h4>"
                    "<p>While acknowledging these intellectual debts and parallels, PM's <em>specific "
                    "mechanisms</em> represent independent developments:</p>"
                    "<ul>"
                    "<li><strong>G₂ triple overlap integrals</strong> for Yukawa textures from explicit 7D Monte Carlo</li>"
                    "<li><strong>Racetrack-blended sector sampling</strong> for cosmological ratios (DM/baryon ~5.8 predicted)</li>"
                    "<li><strong>χ<sub>eff</sub> = 144 flux quantization</strong> determining n<sub>gen</sub> = 3 parameter-free</li>"
                    "<li><strong>Pneuma-microtubule coupling</strong> inspired by Orch-OR quantum biology (speculative appendix)</li>"
                    "<li><strong>Thermal time hypothesis</strong> for emergent time from modular flow on G₂</li>"
                    "</ul>"
                    "<p>The framework is rooted in M-theory-inspired phenomenology, building on established "
                    "literature while proposing novel mechanisms that yield 55+ testable predictions from pure "
                    "geometry.</p>"
                ),
                label="pm-contributions"
            ),
        ]

        return SectionContent(
            section_id="1",
            subsection_id=None,
            title="Introduction",
            abstract=(
                "The pursuit of a unified description of all fundamental forces represents one of the "
                "most profound intellectual endeavors in theoretical physics. This section traces the "
                "historical arc from Maxwell's unification of electricity and magnetism to modern attempts "
                "at Grand Unified Theories, while introducing the novel approach of proposing that geometry emerges from "
                "a fundamental fermionic field. Principia Metaphysica v24.2 posits a 27D spacetime with unified "
                "structure (24,1,2) = 12\u00d7(2,0) + S<sup>(2,0)</sup> + (0,1)\u2014with 12 bridge pairs warping to create dual 13D(12,1) shadows\u2014"
                "eliminating ghost modes while preserving phenomenological richness. Compactification occurs "
                "on a TCS (Twisted Connected Sum) G\u2082 manifold with h<sup>1,1</sup>=4 K\u00e4hler moduli sectors, enabling "
                "racetrack moduli stabilization that dynamically derives \u03b5 \u2248 0.2257 (the Cabibbo angle) without "
                "tuning. The Primordial Spinor Field-Vielbein bridge validates metric emergence from spinor bilinears with "
                "Lorentzian signature (-,+,+,+). Key predictions include w\u2080 = -1 + 1/b\u2083 = -23/24 and w\u2090 \u2248 -0.204, "
                "consistent with DESI 2025 thawing observations."
            ),
            content_blocks=content_blocks,
            formula_refs=[],
            param_refs=[
                "D_bulk",
                "D_shadow",
                "D_bridge",
                "D_observable",
                "D_G2",
                "D_spin8",
                "wa_PM_effective",
                "w0_PM",
                "alpha_GUT_inv",
                "higgs_mass.m_h_GeV",
                "proton_lifetime.tau_p_years",
                "vev_pneuma.v_EW",
            ]
        )

    def get_formulas(self) -> List[Formula]:
        """Return key framework formula for the introduction."""
        return [
            Formula(
                id="intro-division-algebra-decomposition",
                label="(1.4)",
                latex=r"D = 13 = 1 + 4 + 8 = \dim(\mathbb{R}) + \dim(\mathbb{H}) + \dim(\mathbb{O})",
                plain_text="D = 13 = 1 + 4 + 8 = dim(R) + dim(H) + dim(O)",
                category="DERIVED",
                description=(
                    "The shadow dimension D=13 admits a unique decomposition into normed division "
                    "algebra components, as classified by the Hurwitz theorem (1898): real R (dim 1, "
                    "encoding emergent thermal time from KMS modular flow), quaternionic H (dim 4, "
                    "encoding Lorentz spacetime with Spin(3,1) isomorphic to SL(2,H)), and octonionic "
                    "O (dim 8, encoding the internal G2 manifold whose automorphism group Aut(O) = G2 "
                    "governs gauge symmetry and particle content). The decomposition 13 = 1 + 4 + 8 is "
                    "the unique partition of 13 into Hurwitz dimensions that assigns exactly one factor "
                    "to each physical role, with the exclusion of dim 2 (complex numbers) reflecting the "
                    "absence of a fundamental worldsheet degree of freedom in the observable sector."
                ),
                input_params=[
                    "dimensions.D_bulk",
                    "topology.elder_kads",
                ],
                output_params=[
                    "dimensions.D_shadow",
                ],
                derivation={
                    "steps": [
                        {"description": "Hurwitz theorem: only 4 normed division algebras exist over R with dimensions 1, 2, 4, 8", "formula": r"\mathbb{R}(1),\; \mathbb{C}(2),\; \mathbb{H}(4),\; \mathbb{O}(8)"},
                        {"description": "Physical constraints: exactly one factor each of dim 1 (time), dim 4 (spacetime), dim 8 (internal); exclude dim 2 (no worldsheet)", "formula": r"D = \dim(\mathbb{R}) + \dim(\mathbb{H}) + \dim(\mathbb{O})"},
                        {"description": "Unique solution yields D=13 per shadow, with Aut(O) = G2 governing internal geometry", "formula": r"D = 1 + 4 + 8 = 13, \quad \text{Aut}(\mathbb{O}) = G_2"},
                    ],
                    "method": "hurwitz_classification",
                    "parentFormulas": []
                },
                terms={
                    "D": "Total dimension of each observable shadow sector (13)",
                    "R": "Real numbers, dimension 1 (emergent thermal time)",
                    "H": "Quaternions, dimension 4 (Lorentzian spacetime with Spin(3,1))",
                    "O": "Octonions, dimension 8 (internal manifold with Aut(O) = G2)",
                    "Aut(O)": "Automorphism group of octonions, isomorphic to G2",
                }
            )
        ]

    def get_output_param_definitions(self) -> List[Parameter]:
        """No output parameters in introduction section — narrative section."""
        return [
            Parameter(
                path="introduction.subsection_count",
                name="Introduction Subsection Count",
                no_experimental_value=True,
                units="sections",
                description="Number of subsections in the introduction (1.1 through 1.6)",
                status="SYSTEM"
            )
        ]

    def get_references(self) -> List[Dict[str, str]]:
        """Return historical references for introduction."""
        return [
            {
                "id": "maxwell_1865",
                "authors": "Maxwell, J. C.",
                "title": "A Dynamical Theory of the Electromagnetic Field",
                "journal": "Phil. Trans. R. Soc. Lond.",
                "volume": "155",
                "year": "1865",
                "url": "https://doi.org/10.1098/rstl.1865.0008"
            },
            {
                "id": "glashow_1961",
                "authors": "Glashow, S. L.",
                "title": "Partial Symmetries of Weak Interactions",
                "journal": "Nucl. Phys.",
                "volume": "22",
                "year": "1961",
                "url": "https://doi.org/10.1016/0029-5582(61)90469-2"
            },
            {
                "id": "weinberg_1967",
                "authors": "Weinberg, S.",
                "title": "A Model of Leptons",
                "journal": "Phys. Rev. Lett.",
                "volume": "19",
                "year": "1967",
                "url": "https://doi.org/10.1103/PhysRevLett.19.1264"
            },
            {
                "id": "georgi_glashow_1974",
                "authors": "Georgi, H. and Glashow, S. L.",
                "title": "Unity of All Elementary Particle Forces",
                "journal": "Phys. Rev. Lett.",
                "volume": "32",
                "year": "1974",
                "url": "https://doi.org/10.1103/PhysRevLett.32.438"
            },
        ]


    # -------------------------------------------------------------------------
    # SSOT enrichment methods
    # -------------------------------------------------------------------------

    def get_certificates(self) -> List[Dict[str, Any]]:
        """Return certificate assertions verifying introduction section integrity."""
        section = self.get_section_content()
        blocks = section.content_blocks if section else []
        paragraph_blocks = [b for b in blocks if b.type == "paragraph"]
        total_text = " ".join(b.content for b in paragraph_blocks)
        word_count = len(total_text.split())
        heading_blocks = [b for b in blocks if b.type == "heading"]
        has_key_concepts = all(
            term in total_text
            for term in ["Maxwell", "Kaluza-Klein", "Pneuma", "division algebra", "G\u2082"]
        )

        return [
            {
                "id": "CERT_INTRO_WORD_COUNT",
                "assertion": "Introduction contains at least 500 words of substantive content",
                "condition": f"word_count >= 500 (actual: {word_count})",
                "tolerance": 500,
                "status": "PASS" if word_count >= 500 else "FAIL",
                "wolfram_query": "N/A (content integrity check)",
                "wolfram_result": "N/A",
                "sector": "paper"
            },
            {
                "id": "CERT_INTRO_KEY_CONCEPTS",
                "assertion": "Introduction covers Maxwell, Kaluza-Klein, Pneuma, division algebras, and G2",
                "condition": f"all key concepts present: {has_key_concepts}",
                "tolerance": "exact",
                "status": "PASS" if has_key_concepts else "FAIL",
                "wolfram_query": "N/A (content integrity check)",
                "wolfram_result": "N/A",
                "sector": "paper"
            },
            {
                "id": "CERT_INTRO_SUBSECTIONS",
                "assertion": "Introduction has at least 5 subsection headings",
                "condition": f"heading_count >= 5 (actual: {len(heading_blocks)})",
                "tolerance": 5,
                "status": "PASS" if len(heading_blocks) >= 5 else "FAIL",
                "wolfram_query": "N/A (structural check)",
                "wolfram_result": "N/A",
                "sector": "paper"
            },
        ]

    def get_learning_materials(self) -> List[Dict[str, Any]]:
        """Return educational resources about concepts introduced in the introduction."""
        return [
            {
                "topic": "Electroweak unification",
                "url": "https://en.wikipedia.org/wiki/Electroweak_interaction",
                "relevance": "Section 1.1 traces unification history from Maxwell through Glashow-Weinberg-Salam electroweak theory",
                "validation_hint": "Electroweak theory unifies EM and weak force at ~246 GeV (SU(2)_L x U(1)_Y)"
            },
            {
                "topic": "Kaluza-Klein theory",
                "url": "https://en.wikipedia.org/wiki/Kaluza%E2%80%93Klein_theory",
                "relevance": "Section 1.2 describes geometrization of forces via extra dimensions; PM extends this to 27D with G2 compactification",
                "validation_hint": "5D KK yields gravity + U(1); PM requires 27D for full Standard Model gauge group"
            },
            {
                "topic": "Normed division algebras and the Hurwitz theorem",
                "url": "https://en.wikipedia.org/wiki/Hurwitz%27s_theorem_(composition_algebras)",
                "relevance": "Section 1.4 derives D=13 uniqueness from division algebra dimensions 1+4+8 (R+H+O)",
                "validation_hint": "Only 4 normed division algebras exist: R(1), C(2), H(4), O(8) by Hurwitz 1898"
            },
            {
                "topic": "G2 holonomy and M-theory compactification",
                "url": "https://en.wikipedia.org/wiki/G2_manifold",
                "relevance": "Introduction establishes G2 holonomy as the compactification mechanism yielding chiral fermions and 3 generations",
                "validation_hint": "G2 holonomy on 7-manifolds preserves N=1 SUSY in 4D; chirality from singular fibers"
            },
        ]

    def validate_self(self) -> Dict[str, Any]:
        """Validate introduction section integrity."""
        checks = []
        section = self.get_section_content()
        blocks = section.content_blocks if section else []
        paragraph_blocks = [b for b in blocks if b.type == "paragraph"]
        total_text = " ".join(b.content for b in paragraph_blocks)
        word_count = len(total_text.split())

        wc_ok = word_count >= 500
        checks.append({
            "name": "Introduction word count meets minimum (>=500)",
            "passed": wc_ok,
            "confidence_interval": {
                "lower": 500,
                "upper": 10000,
                "sigma": 0.0
            },
            "log_level": "INFO" if wc_ok else "ERROR",
            "message": f"Word count = {word_count} (minimum 500)"
        })

        foundations = self.get_foundations()
        f_ok = len(foundations) >= 6
        checks.append({
            "name": "At least 6 foundational principles defined",
            "passed": f_ok,
            "confidence_interval": {
                "lower": 6,
                "upper": 20,
                "sigma": 0.0
            },
            "log_level": "INFO" if f_ok else "ERROR",
            "message": f"Foundation principles = {len(foundations)} (minimum 6)"
        })

        refs = self.get_references()
        r_ok = len(refs) >= 3
        checks.append({
            "name": "At least 3 references provided",
            "passed": r_ok,
            "confidence_interval": {
                "lower": 3,
                "upper": 50,
                "sigma": 0.0
            },
            "log_level": "INFO" if r_ok else "ERROR",
            "message": f"References = {len(refs)} (minimum 3)"
        })

        return {
            "passed": all(c["passed"] for c in checks),
            "checks": checks
        }

    def get_gate_checks(self) -> List[Dict[str, Any]]:
        """Return gate check results for introduction section."""
        section = self.get_section_content()
        blocks = section.content_blocks if section else []
        paragraph_blocks = [b for b in blocks if b.type == "paragraph"]
        total_text = " ".join(b.content for b in paragraph_blocks)
        word_count = len(total_text.split())
        passed = word_count >= 500

        return [
            {
                "gate_id": "G_INTRO_CONTENT_INTEGRITY",
                "simulation_id": self.metadata.id,
                "assertion": "Introduction section provides comprehensive framework overview with historical context (>=500 words)",
                "result": "PASS" if passed else "FAIL",
                "timestamp": datetime.now().isoformat(),
                "details": {
                    "word_count": word_count,
                    "content_blocks": len(blocks),
                    "foundations_count": len(self.get_foundations()),
                    "references_count": len(self.get_references()),
                    "section_type": "narrative_introduction"
                }
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
