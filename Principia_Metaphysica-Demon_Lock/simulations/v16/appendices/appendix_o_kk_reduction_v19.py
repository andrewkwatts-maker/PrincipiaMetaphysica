#!/usr/bin/env python3
"""
PRINCIPIA METAPHYSICA v19.0 - Appendix O: Kaluza-Klein Reduction Steps
=======================================================================

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.

Dedicated To:
    My Wife: Elizabeth May Watts
    Our Messiah: Jesus Of Nazareth

This appendix provides a step-by-step pedagogical derivation of how extra dimensions
give rise to gauge fields and scalars. Following the eigenchris YouTube style, we build
intuition from the simplest case (5D circle reduction) and generalize to the full
Principia Metaphysica dimensional chain: 26D -> 13D (Sp(2,R)) -> 7D (G2) -> 4D.

APPENDIX: O (Kaluza-Klein Reduction Steps)

Topics covered:
    1. The Kaluza-Klein metric ansatz
    2. Circle reduction (5D -> 4D) as the simplest example
    3. How gauge fields emerge from off-diagonal metric components
    4. How scalars (dilaton) emerge from internal volume moduli
    5. Mode expansion on compact manifolds
    6. Mass spectrum from internal eigenvalues
    7. Zero modes and massless fields
    8. Generalization to higher dimensions
    9. The Principia chain: 26D -> 13D -> 7D -> 4D
    10. Consistency conditions for truncation
"""

import sys
import os
import numpy as np
from decimal import Decimal, getcontext
from typing import Dict, Any, List, Optional

getcontext().prec = 50

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
    PI,
)


class AppendixOKKReduction(SimulationBase):
    """
    Appendix O: Kaluza-Klein Reduction Steps.

    Provides pedagogical derivations of dimensional reduction following the
    eigenchris YouTube style - step by step, building intuition from simple
    examples before generalizing to the full 26D framework.

    The key insight: Extra dimensions are not exotic - they simply encode
    gauge symmetries geometrically. A particle moving in a circle (compact
    dimension) looks like a charged particle from the 4D perspective.

    Follows SOLID principles:
    - Single Responsibility: Only handles KK reduction pedagogy
    - Open/Closed: Extends SimulationBase without modification
    - Dependency Inversion: Depends on registry abstraction for values
    """

    # Dynamic formula IDs referenced by this appendix
    FORMULA_REFS = [
        "kk-metric-ansatz-v19",
        "kk-circle-reduction-v19",
        "kk-gauge-emergence-v19",
        "kk-dilaton-scalar-v19",
        "kk-mode-expansion-v19",
        "kk-mass-spectrum-v19",
        "kk-zero-modes-v19",
        "kk-higher-dim-v19",
        "kk-principia-chain-v19",
        "kk-g2-volume-v19",
        "kk-consistency-v19",
        "kk-gauge-coupling-v19",
    ]

    # Dynamic parameter paths referenced by this appendix
    PARAM_REFS = [
        "topology.b3",
        "topology.chi_eff",
        "gauge.alpha_em",
        "gauge.alpha_s",
        "gauge.g_weak",
        "geometry.V_G2",
    ]

    @property
    def metadata(self) -> SimulationMetadata:
        return SimulationMetadata(
            id="appendix_o_kk_reduction_v19",
            version="19.0",
            domain="appendices",
            title="Appendix O: Kaluza-Klein Reduction Steps",
            description="Pedagogical derivation of dimensional reduction from 26D to 4D",
            section_id="O",
            subsection_id=None,
            appendix=True
        )

    @property
    def required_inputs(self) -> List[str]:
        # Narrative content - no strict dependencies
        return []

    @property
    def output_params(self) -> List[str]:
        return [
            "kk.compact_radius_ratio",
            "kk.gauge_coupling_geometric",
            "kk.mass_gap_planck",
        ]

    @property
    def output_formulas(self) -> List[str]:
        return self.FORMULA_REFS

    def run(self, registry: 'PMRegistry') -> Dict[str, Any]:
        """Execute KK reduction computations."""
        # Get geometric inputs with defaults
        b3 = registry.get("topology.b3", default=24)
        V_G2 = registry.get("geometry.V_G2", default=Decimal("0.1667"))

        # Compute KK-derived quantities
        # Compact radius in Planck units (from G2 volume)
        R_compact = float(V_G2) ** (1/7)  # 7th root for G2 manifold

        # Gauge coupling from geometric relation: g^2 ~ 1/(R^2 * M_Pl^2)
        # For SM gauge couplings, this is modulated by cycle volumes
        alpha_geometric = 1.0 / (4 * np.pi * R_compact**2 * float(b3))

        # Mass gap: first KK mode mass ~ 1/R in Planck units
        mass_gap = 1.0 / R_compact

        return {
            "kk.compact_radius_ratio": R_compact,
            "kk.gauge_coupling_geometric": alpha_geometric,
            "kk.mass_gap_planck": mass_gap,
        }

    def get_section_content(self) -> Optional[SectionContent]:
        """Return section content for Appendix O: Kaluza-Klein Reduction Steps."""
        content_blocks = [
            # Main heading
            ContentBlock(
                type="heading",
                content="Kaluza-Klein Reduction Steps",
                level=2,
                label="O"
            ),
            ContentBlock(
                type="paragraph",
                content=(
                    "This appendix provides a step-by-step pedagogical guide to understanding "
                    "how extra dimensions give rise to the gauge fields and scalars of the "
                    "Standard Model. We follow the eigenchris approach: start simple, build "
                    "intuition, then generalize."
                )
            ),
            ContentBlock(
                type="callout",
                content=(
                    "The central insight of Kaluza-Klein theory is profound: <strong>gauge "
                    "symmetries are geometric</strong>. What we perceive as a charged particle "
                    "interacting with an electromagnetic field is actually a particle moving "
                    "in an extra circular dimension."
                ),
                callout_type="info",
                title="The Big Picture"
            ),

            # O.1 The Metric Ansatz
            ContentBlock(
                type="heading",
                content="O.1 The Kaluza-Klein Metric Ansatz",
                level=3
            ),
            ContentBlock(
                type="paragraph",
                content=(
                    "In higher dimensions, gravity is described by a metric tensor with more "
                    "components. The key observation is that when some dimensions are compact, "
                    "the higher-dimensional metric naturally splits into several 4D fields."
                )
            ),
            ContentBlock(
                type="formula",
                content=r"ds^2_{D} = e^{2\alpha\phi} g_{\mu\nu} dx^\mu dx^\nu + e^{2\beta\phi} G_{mn} dy^m dy^n",
                formula_id="kk-metric-ansatz-v19",
                label="(O.1)"
            ),
            ContentBlock(
                type="paragraph",
                content=(
                    "Here the D-dimensional line element splits into an external 4D part "
                    "(with coordinates x<sup>mu</sup>) and an internal compact part "
                    "(with coordinates y<sup>m</sup>). The warping factors involving the "
                    "dilaton phi control how the two spaces couple."
                )
            ),
            ContentBlock(
                type="note",
                content=(
                    "<ul>"
                    "<li><strong>g_{mu nu}</strong>: The 4D spacetime metric (gravity)</li>"
                    "<li><strong>G_{mn}</strong>: The internal manifold metric (encodes gauge and scalar)</li>"
                    "<li><strong>phi</strong>: The dilaton field (overall volume modulus)</li>"
                    "<li><strong>alpha, beta</strong>: Weyl rescaling exponents (chosen for Einstein frame)</li>"
                    "</ul>"
                ),
                label="metric-components"
            ),

            # O.2 Circle Reduction
            ContentBlock(
                type="heading",
                content="O.2 Circle Reduction: The Simplest Example (5D to 4D)",
                level=3
            ),
            ContentBlock(
                type="paragraph",
                content=(
                    "Let us start with the simplest case: one extra dimension compactified on "
                    "a circle S^1 of radius R. This was Kaluza's original idea (1921) and "
                    "remains the template for all dimensional reductions."
                )
            ),
            ContentBlock(
                type="formula",
                content=r"ds^2_5 = g_{\mu\nu} dx^\mu dx^\nu + R^2 (dy + A_\mu dx^\mu)^2",
                formula_id="kk-circle-reduction-v19",
                label="(O.2)"
            ),
            ContentBlock(
                type="paragraph",
                content=(
                    "The magic is in the off-diagonal term A_mu. Expanding the square:"
                )
            ),
            ContentBlock(
                type="formula",
                content=r"ds^2_5 = g_{\mu\nu} dx^\mu dx^\nu + R^2 dy^2 + 2R^2 A_\mu dx^\mu dy + R^2 A_\mu A_\nu dx^\mu dx^\nu",
                formula_id="kk-gauge-emergence-v19",
                label="(O.3)"
            ),
            ContentBlock(
                type="callout",
                content=(
                    "The term 2R^2 A_mu dx^mu dy tells us: A_mu transforms as a gauge field! "
                    "Under the reparametrization y -> y + Lambda(x), we get A_mu -> A_mu - partial_mu Lambda. "
                    "This is exactly how an Abelian gauge field transforms."
                ),
                callout_type="success",
                title="Gauge Field Emergence"
            ),

            # O.3 Dilaton/Scalar Emergence
            ContentBlock(
                type="heading",
                content="O.3 Scalar Fields from Internal Volume",
                level=3
            ),
            ContentBlock(
                type="paragraph",
                content=(
                    "If we allow the radius R to vary over spacetime, R = R(x), we obtain a "
                    "scalar field called the dilaton or radion. This field controls the overall "
                    "size of the extra dimension."
                )
            ),
            ContentBlock(
                type="formula",
                content=r"\phi(x) = \ln\left(\frac{R(x)}{R_0}\right) \quad \Rightarrow \quad R(x) = R_0 e^{\phi(x)}",
                formula_id="kk-dilaton-scalar-v19",
                label="(O.4)"
            ),
            ContentBlock(
                type="paragraph",
                content=(
                    "After dimensional reduction, the 5D Einstein-Hilbert action produces a "
                    "4D action containing: (1) 4D gravity with Planck mass M_Pl^2 ~ M_5^3 * 2*pi*R, "
                    "(2) a U(1) gauge kinetic term -1/4 F^2, and (3) a dilaton kinetic term."
                )
            ),

            # O.4 Mode Expansion
            ContentBlock(
                type="heading",
                content="O.4 Mode Expansion on Compact Manifolds",
                level=3
            ),
            ContentBlock(
                type="paragraph",
                content=(
                    "Any field Phi(x,y) living in 5D can be Fourier expanded along the compact "
                    "direction. On a circle, this gives discrete Kaluza-Klein modes:"
                )
            ),
            ContentBlock(
                type="formula",
                content=r"\Phi(x,y) = \sum_{n=-\infty}^{\infty} \phi_n(x) e^{iny/R}",
                formula_id="kk-mode-expansion-v19",
                label="(O.5)"
            ),
            ContentBlock(
                type="paragraph",
                content=(
                    "Each mode phi_n(x) is a 4D field. The mode number n determines the momentum "
                    "in the compact direction: p_y = n/R. From the 4D perspective, this momentum "
                    "contributes to the mass."
                )
            ),

            # O.5 Mass Spectrum
            ContentBlock(
                type="heading",
                content="O.5 Mass Spectrum from Internal Eigenvalues",
                level=3
            ),
            ContentBlock(
                type="paragraph",
                content=(
                    "The 5D Klein-Gordon equation for a massless field becomes, after mode "
                    "expansion, a tower of 4D massive fields:"
                )
            ),
            ContentBlock(
                type="formula",
                content=r"(\Box_4 + m_n^2)\phi_n = 0 \quad \text{where} \quad m_n^2 = \frac{n^2}{R^2}",
                formula_id="kk-mass-spectrum-v19",
                label="(O.6)"
            ),
            ContentBlock(
                type="callout",
                content=(
                    "This is the <strong>Kaluza-Klein tower</strong>: an infinite series of massive "
                    "particles with masses m_n = |n|/R. For R ~ 1/M_Pl, these masses are at the "
                    "Planck scale and unobservable. Only the n=0 zero mode is massless and "
                    "corresponds to our observed fields."
                ),
                callout_type="info",
                title="The KK Tower"
            ),

            # O.6 Zero Modes
            ContentBlock(
                type="heading",
                content="O.6 Zero Modes: The Massless Fields We Observe",
                level=3
            ),
            ContentBlock(
                type="paragraph",
                content=(
                    "The zero modes (n=0) are the fields that survive to low energies. They are "
                    "constant along the compact direction and solve the internal Laplacian equation "
                    "with zero eigenvalue:"
                )
            ),
            ContentBlock(
                type="formula",
                content=r"\Delta_{K} \psi_0 = 0 \quad \Rightarrow \quad \psi_0 = \text{const} \quad \text{(harmonic form)}",
                formula_id="kk-zero-modes-v19",
                label="(O.7)"
            ),
            ContentBlock(
                type="paragraph",
                content=(
                    "On a more general compact manifold K, the number of zero modes equals the "
                    "number of harmonic forms, which is determined by the Betti numbers b_p(K). "
                    "This is how topology determines the particle content!"
                )
            ),

            # O.7 Generalization
            ContentBlock(
                type="heading",
                content="O.7 Generalization to Non-Abelian Gauge Groups",
                level=3
            ),
            ContentBlock(
                type="paragraph",
                content=(
                    "For non-Abelian gauge groups, we need a compact manifold with non-trivial "
                    "isometry group. The gauge group that emerges in 4D is the isometry group "
                    "of the internal manifold:"
                )
            ),
            ContentBlock(
                type="formula",
                content=r"G_{\text{gauge}}^{4D} = \text{Isom}(K) \quad \Rightarrow \quad \text{SU}(3) \times \text{SU}(2) \times \text{U}(1)",
                formula_id="kk-higher-dim-v19",
                label="(O.8)"
            ),
            ContentBlock(
                type="note",
                content=(
                    "<ul>"
                    "<li><strong>S^1</strong>: Isometry U(1) -> Electromagnetism (Kaluza-Klein)</li>"
                    "<li><strong>S^2</strong>: Isometry SO(3) -> SU(2) (weak-like)</li>"
                    "<li><strong>CP^2</strong>: Isometry SU(3) -> Color (QCD-like)</li>"
                    "<li><strong>G_2 manifold</strong>: Holonomy G_2 contains SM structure</li>"
                    "</ul>"
                ),
                label="isometry-gauge-map"
            ),

            # O.8 The Principia Chain
            ContentBlock(
                type="heading",
                content="O.8 The Principia Chain: 26D to 4D",
                level=3
            ),
            ContentBlock(
                type="paragraph",
                content=(
                    "In Principia Metaphysica, the dimensional reduction proceeds through a "
                    "specific chain that preserves key structures at each stage:"
                )
            ),
            ContentBlock(
                type="formula",
                content=r"26D \xrightarrow{\text{Sp}(2,\mathbb{R})} 13D \xrightarrow{\text{G}_2} 7D \xrightarrow{\text{compact}} 4D",
                formula_id="kk-principia-chain-v19",
                label="(O.9)"
            ),
            ContentBlock(
                type="note",
                content=(
                    "<ul>"
                    "<li><strong>26D -> 13D</strong>: Bosonic string critical dimension reduces via Sp(2,R) "
                    "modular structure, yielding the geometric skeleton</li>"
                    "<li><strong>13D -> 7D</strong>: G_2 holonomy emerges, with 7 compact dimensions "
                    "encoding gauge structure</li>"
                    "<li><strong>7D -> 4D</strong>: Final compactification on associative 3-cycles "
                    "yields the Standard Model in 4D Minkowski space</li>"
                    "</ul>"
                ),
                label="principia-stages"
            ),
            ContentBlock(
                type="formula",
                content=r"M_{\text{Pl}}^2 = M_{26}^{24} \cdot V_{22} \propto M_{7}^{5} \cdot V_{G_2}",
                formula_id="kk-g2-volume-v19",
                label="(O.10)"
            ),

            # O.9 Gauge Coupling from Geometry
            ContentBlock(
                type="heading",
                content="O.9 Gauge Couplings from Cycle Volumes",
                level=3
            ),
            ContentBlock(
                type="paragraph",
                content=(
                    "Each gauge coupling in 4D is determined by the volume of the cycle on "
                    "which the corresponding gauge field is supported. This explains the gauge "
                    "hierarchy geometrically:"
                )
            ),
            ContentBlock(
                type="formula",
                content=r"\frac{1}{g_i^2} = \frac{\text{Vol}(\Sigma_i)}{l_s^{n_i}} \quad \Rightarrow \quad \alpha_i = \frac{g_i^2}{4\pi}",
                formula_id="kk-gauge-coupling-v19",
                label="(O.11)"
            ),
            ContentBlock(
                type="paragraph",
                content=(
                    "For the Standard Model groups in Principia Metaphysica: SU(3) lives on a "
                    "3-cycle with volume V_3, SU(2) on a 2-cycle with volume V_2, and U(1) "
                    "on a 1-cycle with volume V_1. The ratios of these volumes determine "
                    "alpha_s/alpha_em and sin^2(theta_W)."
                )
            ),

            # O.10 Consistency Conditions
            ContentBlock(
                type="heading",
                content="O.10 Consistency Conditions for Truncation",
                level=3
            ),
            ContentBlock(
                type="paragraph",
                content=(
                    "Not every dimensional reduction is consistent. The truncation to zero modes "
                    "must respect the equations of motion. Key conditions include:"
                )
            ),
            ContentBlock(
                type="formula",
                content=r"\text{Consistent truncation:} \quad \mathcal{L}_{4D}[\phi_0] = \int_K \mathcal{L}_{D}[\phi_0, y]\, d^ny",
                formula_id="kk-consistency-v19",
                label="(O.12)"
            ),
            ContentBlock(
                type="note",
                content=(
                    "<ul>"
                    "<li><strong>Moduli stabilization</strong>: The volume moduli must be fixed to "
                    "avoid massless scalars (fifth force constraints)</li>"
                    "<li><strong>Flux quantization</strong>: Internal fluxes must be properly quantized "
                    "to ensure well-defined gauge groups</li>"
                    "<li><strong>Anomaly cancellation</strong>: The 4D theory must be anomaly-free; "
                    "this constrains the matter content</li>"
                    "<li><strong>Supersymmetry breaking</strong>: If present, SUSY must break at "
                    "a scale consistent with observations</li>"
                    "</ul>"
                ),
                label="consistency-conditions"
            ),

            # Summary
            ContentBlock(
                type="heading",
                content="O.11 Summary: From Geometry to Gauge",
                level=3
            ),
            ContentBlock(
                type="callout",
                content=(
                    "Kaluza-Klein reduction teaches us that the Standard Model gauge structure "
                    "is not arbitrary - it emerges from the geometry of extra dimensions. "
                    "In Principia Metaphysica, the specific choice of G_2 holonomy manifold "
                    "(with b_3 = 24 and chi_eff = 144) uniquely determines all gauge couplings "
                    "and matter content. There are no free parameters to tune - only geometry."
                ),
                callout_type="success",
                title="The Geometric Origin of Gauge Symmetry"
            ),
        ]

        return SectionContent(
            section_id="O",
            subsection_id=None,
            title="Appendix O: Kaluza-Klein Reduction Steps",
            abstract=(
                "Pedagogical derivation of how extra dimensions give rise to gauge fields "
                "and scalars, from the simplest 5D circle example to the full Principia "
                "Metaphysica 26D -> 4D chain."
            ),
            content_blocks=content_blocks,
            formula_refs=self.FORMULA_REFS,
            param_refs=self.PARAM_REFS,
            appendix=True,
        )

    def get_formulas(self) -> List[Formula]:
        """Return formula definitions for Appendix O."""
        return [
            Formula(
                id="kk-metric-ansatz-v19",
                label="(O.1)",
                latex=r"ds^2_{D} = e^{2\alpha\phi} g_{\mu\nu} dx^\mu dx^\nu + e^{2\beta\phi} G_{mn} dy^m dy^n",
                plain_text="KK metric ansatz with warping",
                category="FOUNDATIONAL",
                description=(
                    "Kaluza-Klein metric ansatz for dimensional reduction. The D-dimensional "
                    "metric splits into external 4D spacetime and internal compact manifold, "
                    "with dilaton-dependent warping factors."
                ),
                terms={
                    "g_{mu nu}": "4D external spacetime metric",
                    "G_{mn}": "Internal compact manifold metric",
                    "phi": "Dilaton field (volume modulus)",
                    "alpha, beta": "Weyl rescaling exponents for Einstein frame",
                }
            ),
            Formula(
                id="kk-circle-reduction-v19",
                label="(O.2)",
                latex=r"ds^2_5 = g_{\mu\nu} dx^\mu dx^\nu + R^2 (dy + A_\mu dx^\mu)^2",
                plain_text="5D circle metric ansatz with gauge field",
                category="FOUNDATIONAL",
                description=(
                    "The simplest Kaluza-Klein ansatz: 5D metric on M_4 x S^1. The off-diagonal "
                    "term A_mu becomes the U(1) gauge field in 4D."
                ),
                terms={
                    "R": "Radius of compact circle S^1",
                    "A_mu": "Emergent U(1) gauge field",
                    "y": "Compact coordinate (periodic: y ~ y + 2*pi*R)",
                }
            ),
            Formula(
                id="kk-gauge-emergence-v19",
                label="(O.3)",
                latex=r"ds^2_5 = g_{\mu\nu} dx^\mu dx^\nu + R^2 dy^2 + 2R^2 A_\mu dx^\mu dy + R^2 A_\mu A_\nu dx^\mu dx^\nu",
                plain_text="Expanded 5D metric showing gauge field terms",
                category="DERIVED",
                description=(
                    "Expansion of the circle reduction ansatz. The cross-term A_mu dx^mu dy "
                    "shows how gauge transformations arise from coordinate reparametrizations "
                    "in the compact direction."
                ),
                terms={
                    "A_mu dx^mu dy": "Off-diagonal term giving gauge transformation",
                    "A_mu A_nu dx^mu dx^nu": "Quadratic term contributing to gauge kinetics",
                }
            ),
            Formula(
                id="kk-dilaton-scalar-v19",
                label="(O.4)",
                latex=r"\phi(x) = \ln\left(\frac{R(x)}{R_0}\right) \quad \Rightarrow \quad R(x) = R_0 e^{\phi(x)}",
                plain_text="Dilaton field from variable radius",
                category="FOUNDATIONAL",
                description=(
                    "When the compact radius varies over spacetime, it defines a scalar field "
                    "(dilaton/radion). This field must be stabilized to avoid long-range fifth forces."
                ),
                terms={
                    "phi(x)": "Dilaton field (4D scalar)",
                    "R_0": "Reference (stabilized) radius",
                    "R(x)": "Position-dependent compact radius",
                }
            ),
            Formula(
                id="kk-mode-expansion-v19",
                label="(O.5)",
                latex=r"\Phi(x,y) = \sum_{n=-\infty}^{\infty} \phi_n(x) e^{iny/R}",
                plain_text="Fourier mode expansion on circle",
                category="FOUNDATIONAL",
                description=(
                    "Any field in 5D decomposes into a tower of 4D fields indexed by "
                    "the mode number n. Each mode carries momentum n/R in the compact direction."
                ),
                terms={
                    "phi_n(x)": "n-th Kaluza-Klein mode (4D field)",
                    "n": "Mode number (quantized compact momentum)",
                    "exp(iny/R)": "Fourier basis on circle",
                }
            ),
            Formula(
                id="kk-mass-spectrum-v19",
                label="(O.6)",
                latex=r"(\Box_4 + m_n^2)\phi_n = 0 \quad \text{where} \quad m_n^2 = \frac{n^2}{R^2}",
                plain_text="KK mass spectrum: m_n = |n|/R",
                category="DERIVED",
                description=(
                    "The Kaluza-Klein mass tower. Higher modes are heavier, with mass determined "
                    "by compact momentum. For R ~ l_Planck, these masses are at the Planck scale."
                ),
                terms={
                    "Box_4": "4D d'Alembertian (wave operator)",
                    "m_n": "Mass of n-th KK mode",
                    "R": "Compact radius",
                }
            ),
            Formula(
                id="kk-zero-modes-v19",
                label="(O.7)",
                latex=r"\Delta_{K} \psi_0 = 0 \quad \Rightarrow \quad \psi_0 = \text{const} \quad \text{(harmonic form)}",
                plain_text="Zero modes are harmonic forms on compact manifold",
                category="FOUNDATIONAL",
                description=(
                    "Zero modes satisfy the internal Laplacian equation with zero eigenvalue. "
                    "Their number equals the Betti numbers of the compact manifold, linking "
                    "topology to particle content."
                ),
                terms={
                    "Delta_K": "Laplacian on compact manifold K",
                    "psi_0": "Zero mode (harmonic form)",
                    "b_p(K)": "p-th Betti number (counts harmonic p-forms)",
                }
            ),
            Formula(
                id="kk-higher-dim-v19",
                label="(O.8)",
                latex=r"G_{\text{gauge}}^{4D} = \text{Isom}(K) \quad \Rightarrow \quad \text{SU}(3) \times \text{SU}(2) \times \text{U}(1)",
                plain_text="4D gauge group = Isometry group of compact manifold",
                category="FOUNDATIONAL",
                description=(
                    "Non-Abelian gauge groups arise from the isometry group of the internal "
                    "manifold. The Standard Model gauge group emerges from appropriate "
                    "compact manifold with matching isometries."
                ),
                terms={
                    "Isom(K)": "Isometry group of compact manifold K",
                    "SU(3)": "Color gauge group (QCD)",
                    "SU(2)": "Weak isospin gauge group",
                    "U(1)": "Hypercharge gauge group",
                }
            ),
            Formula(
                id="kk-principia-chain-v19",
                label="(O.9)",
                latex=r"26D \xrightarrow{\text{Sp}(2,\mathbb{R})} 13D \xrightarrow{\text{G}_2} 7D \xrightarrow{\text{compact}} 4D",
                plain_text="Principia chain: 26D -> 13D -> 7D -> 4D",
                category="FOUNDATIONAL",
                description=(
                    "The Principia Metaphysica dimensional reduction chain. Each stage "
                    "preserves key structures: Sp(2,R) modular symmetry, G_2 holonomy, "
                    "and finally Standard Model gauge symmetry in 4D."
                ),
                terms={
                    "26D": "Bosonic string critical dimension",
                    "Sp(2,R)": "Modular group of genus-2 surface",
                    "13D": "Intermediate dimension from half-reduction",
                    "G_2": "Exceptional holonomy group in 7D",
                    "4D": "Observable Minkowski spacetime",
                }
            ),
            Formula(
                id="kk-g2-volume-v19",
                label="(O.10)",
                latex=r"M_{\text{Pl}}^2 = M_{26}^{24} \cdot V_{22} \propto M_{7}^{5} \cdot V_{G_2}",
                plain_text="Planck mass from higher-dimensional compactification",
                category="DERIVED",
                description=(
                    "The 4D Planck mass is determined by the higher-dimensional fundamental "
                    "scale and the volume of the compact dimensions. This fixes the hierarchy."
                ),
                terms={
                    "M_Pl": "4D Planck mass",
                    "M_26": "26D fundamental scale",
                    "V_22": "Volume of 22 compact dimensions (26 -> 4)",
                    "M_7": "7D fundamental scale",
                    "V_G2": "Volume of G_2 manifold (7 -> 4)",
                }
            ),
            Formula(
                id="kk-gauge-coupling-v19",
                label="(O.11)",
                latex=r"\frac{1}{g_i^2} = \frac{\text{Vol}(\Sigma_i)}{l_s^{n_i}} \quad \Rightarrow \quad \alpha_i = \frac{g_i^2}{4\pi}",
                plain_text="Gauge coupling from cycle volume",
                category="DERIVED",
                description=(
                    "Each gauge coupling is inversely proportional to the volume of the "
                    "cycle supporting that gauge field. This geometric origin explains "
                    "the gauge hierarchy without fine-tuning."
                ),
                terms={
                    "g_i": "Gauge coupling constant",
                    "Vol(Sigma_i)": "Volume of cycle supporting gauge group i",
                    "l_s": "String length scale",
                    "alpha_i": "Fine structure constant for group i",
                }
            ),
            Formula(
                id="kk-consistency-v19",
                label="(O.12)",
                latex=r"\text{Consistent truncation:} \quad \mathcal{L}_{4D}[\phi_0] = \int_K \mathcal{L}_{D}[\phi_0, y]\, d^ny",
                plain_text="Consistent truncation condition",
                category="FOUNDATIONAL",
                description=(
                    "A truncation to zero modes is consistent if the 4D equations of motion "
                    "follow from the higher-dimensional equations restricted to zero modes. "
                    "Not all compactifications satisfy this."
                ),
                terms={
                    "L_4D": "4D effective Lagrangian",
                    "L_D": "D-dimensional Lagrangian",
                    "phi_0": "Zero-mode fields",
                    "K": "Compact manifold",
                }
            ),
        ]

    def get_output_param_definitions(self) -> List[Parameter]:
        """Return parameter definitions for this appendix."""
        return [
            Parameter(
                path="kk.compact_radius_ratio",
                name="Compact Radius Ratio",
                units="dimensionless",
                status="DERIVED",
                description=(
                    "Effective compact radius in Planck units, derived from G_2 volume "
                    "as R = V_G2^(1/7)"
                ),
                no_experimental_value=True,
            ),
            Parameter(
                path="kk.gauge_coupling_geometric",
                name="Geometric Gauge Coupling",
                units="dimensionless",
                status="DERIVED",
                description=(
                    "Order-of-magnitude gauge coupling from KK geometry: "
                    "alpha ~ 1/(4*pi*R^2*b_3)"
                ),
                no_experimental_value=True,
            ),
            Parameter(
                path="kk.mass_gap_planck",
                name="KK Mass Gap",
                units="M_Planck",
                status="DERIVED",
                description=(
                    "Mass of first Kaluza-Klein mode: m_1 = 1/R. "
                    "For Planck-scale compactification, this is ~M_Planck."
                ),
                no_experimental_value=True,
            ),
        ]


if __name__ == "__main__":
    from simulations.base import PMRegistry
    registry = PMRegistry()
    sim = AppendixOKKReduction()
    print(f"Simulation: {sim.metadata.title}")
    print(f"Version: {sim.metadata.version}")
    print(f"Domain: {sim.metadata.domain}")
    print(f"Appendix: {sim.metadata.appendix}")
    print()
    results = sim.run(registry)
    print("Results:")
    for key, value in results.items():
        print(f"  {key}: {value}")
    print()
    content = sim.get_section_content()
    if content:
        print(f"Content blocks: {len(content.content_blocks)}")
        print(f"Formula refs: {len(content.formula_refs)}")
        print(f"Param refs: {len(content.param_refs)}")
    print()
    formulas = sim.get_formulas()
    print(f"Formulas defined: {len(formulas)}")
    for f in formulas:
        print(f"  {f.label} {f.id}: {f.plain_text}")
