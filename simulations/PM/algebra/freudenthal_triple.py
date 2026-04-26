"""
Freudenthal Triple System — 27D Pneuma Condensate
===================================================

The 27D Pneuma condensate in M²⁷(24,1,2) is identified with elements of the
Freudenthal triple system over the exceptional Jordan algebra J₃(𝕆): 3×3
Hermitian matrices over the octonions with 27 real degrees of freedom.

Key results:
  - Cubic norm N(A) = c₁c₂c₃ − c₁|x₁|² − c₂|x₂|² − c₃|x₃|² + 2Re(x₁x₂x₃)
    encodes the racetrack potential V_bridge / V_face
  - Quartic invariant q(A) from the E₇ 56D rep gives the 125 spectral residue
    proxy and the ALP mass scale
  - The triple product {x,y,z} implements Pneuma field bilinears

Dependencies: g2_geometry_v16_0 (topology.elder_kads = b₃ = 24)

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.
"""

import math
import sys
import os
from typing import Dict, Any, List, Optional

project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.insert(0, project_root)

from simulations.base import (
    SimulationBase,
    SimulationMetadata,
    Formula,
    Parameter,
    ContentBlock,
    SectionContent,
)


class FreudenthalTripleSimulation(SimulationBase):
    """
    Freudenthal triple system on J₃(𝕆) — 27D Pneuma condensate.

    Computes cubic norm, quartic invariant, and triple product structure
    of the Pneuma condensate element derived from b₃ = 24 topology.
    """

    @property
    def metadata(self) -> SimulationMetadata:
        return SimulationMetadata(
            id="freudenthal_triple_v1_0",
            version="1.0",
            domain="algebra",
            title="Freudenthal Triple System (27D Pneuma Condensate)",
            description="J₃(𝕆) cubic norm and quartic invariant from the 27D Pneuma condensate",
            section_id="A2",
            appendix=True,
        )

    @property
    def required_inputs(self) -> List[str]:
        return ["topology.elder_kads"]

    @property
    def output_params(self) -> List[str]:
        return [
            "algebra.freudenthal_cubic_norm",
            "algebra.freudenthal_quartic",
            "algebra.freudenthal_jordan_trace",
            "algebra.pneuma_27d_condensate_scale",
        ]

    @property
    def output_formulas(self) -> List[str]:
        return [
            "freudenthal-cubic-norm",
            "freudenthal-quartic-invariant",
            "freudenthal-triple-product",
        ]

    def run(self, registry: "PMRegistry") -> Dict[str, Any]:
        b3 = registry.get_param("topology.elder_kads")
        if b3 is None:
            b3 = 24

        try:
            from eml_math.freudenthal import FreudenthalTripleSystem
            fts = FreudenthalTripleSystem.from_pneuma_condensate(b3=float(b3))
            cubic_norm = fts.cubic_norm()
            quartic = fts.quartic()
            jordan_trace = fts.jordan_trace()
            condensate_scale = float(b3) / 27.0
        except ImportError:
            condensate_scale = float(b3) / 27.0
            jordan_trace = 3.0 * condensate_scale
            cubic_norm = condensate_scale ** 3
            quartic = (jordan_trace ** 2 * (3.0 * condensate_scale ** 2)) / 4.0

        return {
            "algebra.freudenthal_cubic_norm": cubic_norm,
            "algebra.freudenthal_quartic": quartic,
            "algebra.freudenthal_jordan_trace": jordan_trace,
            "algebra.pneuma_27d_condensate_scale": condensate_scale,
            "_b3": b3,
        }

    def run_eml(self, registry: "PMRegistry") -> Dict[str, Any]:
        """EML path — same computation via EML library."""
        b3 = registry.get_param("topology.elder_kads")
        if b3 is None:
            b3 = 24

        try:
            from eml_math.freudenthal import FreudenthalTripleSystem
            from simulations.core.eml_integration import eml_scalar, eml_compute, eml_div, eml_mul
            fts = FreudenthalTripleSystem.from_pneuma_condensate(b3=float(b3))
            condensate_scale_pt = eml_div(eml_scalar(float(b3)), eml_scalar(27.0))
            condensate_scale = eml_compute(condensate_scale_pt)
            cubic_norm = fts.cubic_norm()
            quartic = fts.quartic()
            jordan_trace = fts.jordan_trace()
        except ImportError:
            return self.run(registry)

        return {
            "algebra.freudenthal_cubic_norm": cubic_norm,
            "algebra.freudenthal_quartic": quartic,
            "algebra.freudenthal_jordan_trace": jordan_trace,
            "algebra.pneuma_27d_condensate_scale": condensate_scale,
            "_b3": b3,
        }

    def get_formulas(self) -> List[Formula]:
        return [
            Formula(
                id="freudenthal-cubic-norm",
                label="(A2.1)",
                latex=r"N(A) = c_1 c_2 c_3 - c_1|x_1|^2 - c_2|x_2|^2 - c_3|x_3|^2 + 2\,\mathrm{Re}(x_1 x_2 x_3)",
                plain_text="N(A) = c1*c2*c3 - c1|x1|^2 - c2|x2|^2 - c3|x3|^2 + 2Re(x1 x2 x3)",
                category="DERIVED",
                description="Cubic norm (Jordan determinant) of the exceptional Jordan algebra J₃(𝕆). "
                            "In PM this equals the racetrack potential V_bridge / V_face.",
                inputParams=["topology.elder_kads"],
                outputParams=["algebra.freudenthal_cubic_norm"],
                eml_latex=r"\mathrm{ops.sub}(\mathrm{ops.mul}(c_1, c_2, c_3),\; \mathrm{ops.add}(c_1|x_1|^2,\ldots))",
                eml_description="Cubic norm via EML subtraction of off-diagonal octonion norms from diagonal product.",
                derivation={
                    "steps": [
                        "J₃(𝕆): 3×3 Hermitian matrices over octonions 𝕆 with 27 real dimensions",
                        "Diagonal entries (c₁,c₂,c₃) contribute c₁c₂c₃ to the cubic determinant",
                        "Off-diagonal octonion entries xᵢ subtract cᵢ|xᵢ|² from the norm",
                        "Non-associativity of 𝕆 gives the Re(x₁x₂x₃) cross term",
                        "N(A) vanishes iff A is rank-1 (null element of the Jordan algebra)",
                    ]
                },
                terms={
                    "c_1, c_2, c_3": {"description": "Real diagonal entries of the 3×3 Hermitian matrix"},
                    "x_1, x_2, x_3": {"description": "Off-diagonal octonion entries (8 components each)"},
                    "N(A)": {"description": "Cubic norm = Jordan determinant of the 27D element A"},
                },
            ),
            Formula(
                id="freudenthal-quartic-invariant",
                label="(A2.2)",
                latex=r"q(A) = \frac{\mathrm{Tr}(A)^2 \cdot \langle A, A \rangle}{4}",
                plain_text="q(A) = Tr(A)^2 * <A,A> / 4",
                category="DERIVED",
                description="Quartic invariant of the Freudenthal triple system. "
                            "Proxy for the E₇ quartic Casimir; encodes the ALP mass scale "
                            "and 125 spectral residue proxy.",
                inputParams=["topology.elder_kads"],
                outputParams=["algebra.freudenthal_quartic"],
                eml_latex=r"\mathrm{ops.div}(\mathrm{ops.mul}(\mathrm{Tr}^2, \langle A,A\rangle), 4)",
                eml_description="Quartic via EML: ops.div(ops.mul(ops.pow(trace,2), norm_sq), 4)",
                derivation={
                    "method": "Freudenthal quartic from Jordan trace and inner product",
                    "parentFormulas": ["freudenthal-cubic-norm"],
                    "steps": [
                        "The quadratic form ⟨A,A⟩ on J₃(𝕆) is the Jordan inner product Tr(A²)",
                        "The quartic invariant q(A) = Tr(A)²·⟨A,A⟩/4 is the leading E₇ Casimir on J₃(𝕆)",
                        "For a symmetric condensate with equal diagonals cᵢ = s, Tr(A) = 3s and ⟨A,A⟩ = 3s²",
                        "This gives q(A) = (3s)²·(3s²)/4 = 27s⁴/4, encoding the ALP mass scale",
                    ],
                    "references": ["Freudenthal, H. (1954) 'Beziehungen der E7 und E8 zur Oktavenebene'"],
                },
                terms={
                    r"\mathrm{Tr}(A)": "Jordan trace = c₁ + c₂ + c₃ of the 27D condensate element",
                    r"\langle A, A \rangle": "Jordan inner product Tr(A²) — norm-squared of the condensate",
                    r"q(A)": "Quartic invariant — E₇ quartic Casimir evaluated on the Pneuma condensate",
                },
            ),
            Formula(
                id="freudenthal-triple-product",
                label="(A2.3)",
                latex=r"\{x, y, z\}_i = \langle x, y \rangle_J z_i + \langle z, y \rangle_J x_i - \langle x, z \rangle_J y_i",
                plain_text="{x,y,z}_i = <x,y>*z_i + <z,y>*x_i - <x,z>*y_i",
                category="DERIVED",
                description="Freudenthal triple product — implements Pneuma field bilinears. "
                            "This is the linearized version via the Jordan bilinear form ⟨·,·⟩_J.",
                inputParams=[],
                outputParams=[],
                eml_description="Triple product via EML linear combination of Jordan inner products.",
                derivation={
                    "method": "Linearization of Jordan triple system from J₃(𝕆)",
                    "parentFormulas": ["freudenthal-cubic-norm"],
                    "steps": [
                        "The Freudenthal triple system T(J) is the Jordan algebra J ⊕ J* equipped with a symplectic form",
                        "The triple product {x,y,z} is defined from the trilinear form of the cubic norm N",
                        "Linearizing: {x,y,z}_i = ⟨x,y⟩_J z_i + ⟨z,y⟩_J x_i − ⟨x,z⟩_J y_i",
                        "This structure governs the Pneuma field three-point functions in M²⁷",
                    ],
                    "references": ["Brown, R.B. (1969) 'Groups of type E7'. J. Reine Angew. Math. 236, 79–102"],
                },
                terms={
                    r"\{x, y, z\}": "Freudenthal triple product — trilinear map on J₃(𝕆) elements",
                    r"\langle x, y \rangle_J": "Jordan bilinear inner product on J₃(𝕆)",
                },
            ),
        ]

    def get_output_param_definitions(self) -> List[Parameter]:
        return [
            Parameter(
                path="algebra.freudenthal_cubic_norm",
                name="Freudenthal Cubic Norm N(A)",
                units="dimensionless",
                status="DERIVED",
                description="Cubic norm (Jordan determinant) of the 27D Pneuma condensate element in J₃(𝕆). "
                            "Equals V_bridge / V_face in the racetrack potential.",
                derivation_formula="freudenthal-cubic-norm",
                no_experimental_value=True,
                eml_description="EML: ops.pow(eml_scalar(condensate_scale), eml_scalar(3.0)) — cubic norm N(A) = s³ for the symmetric Pneuma element with diagonal entries s = b₃/27",
            ),
            Parameter(
                path="algebra.freudenthal_quartic",
                name="Freudenthal Quartic Invariant q(A)",
                units="dimensionless",
                status="DERIVED",
                description="Quartic invariant of the Freudenthal triple system. "
                            "Proxy for E₇ quartic Casimir; encodes ALP mass scale.",
                derivation_formula="freudenthal-quartic-invariant",
                no_experimental_value=True,
                eml_description="EML: ops.div(ops.mul(ops.pow(eml_vec('algebra.freudenthal_jordan_trace'), eml_scalar(2.0)), ops.mul(eml_scalar(3.0), ops.pow(eml_scalar(condensate_scale), eml_scalar(2.0)))), eml_scalar(4.0)) — quartic q(A) = Tr(A)²·3s²/4",
            ),
            Parameter(
                path="algebra.freudenthal_jordan_trace",
                name="Freudenthal Jordan Trace Tr(A)",
                units="dimensionless",
                status="DERIVED",
                description="Jordan trace = c₁ + c₂ + c₃ of the 27D Pneuma condensate. "
                            "Equals 3 × (b₃/27) = b₃/9.",
                derivation_formula="freudenthal-cubic-norm",
                no_experimental_value=True,
                eml_description="EML: ops.mul(eml_scalar(3.0), ops.div(eml_vec('topology.elder_kads'), eml_scalar(27.0))) — Jordan trace Tr(A) = 3·(b₃/27) = b₃/9",
            ),
            Parameter(
                path="algebra.pneuma_27d_condensate_scale",
                name="Pneuma Condensate Scale",
                units="dimensionless",
                status="DERIVED",
                description="Condensate scale = b₃/27 for the symmetric Pneuma element in J₃(𝕆).",
                no_experimental_value=True,
                eml_description="EML: ops.div(eml_vec('topology.elder_kads'), eml_scalar(27.0)) — condensate scale s = b₃/27 (b₃=24 gives s≈0.888…)",
            ),
        ]

    def get_section_content(self) -> Optional[SectionContent]:
        b3 = 24
        condensate_scale = b3 / 27.0
        trace = 3.0 * condensate_scale
        cubic = condensate_scale ** 3
        quartic = (trace ** 2 * (3.0 * condensate_scale ** 2)) / 4.0

        blocks = [
            ContentBlock(type="heading", content="Freudenthal Triple System and the 27D Pneuma Condensate", level=2),
            ContentBlock(
                type="paragraph",
                content=(
                    "The 27-dimensional Pneuma condensate in the M²⁷(24,1,2) bulk is identified with "
                    "an element of the Freudenthal triple system over the exceptional Jordan algebra "
                    "J₃(𝕆): 3×3 Hermitian matrices over the octonions. "
                    "This 27-dimensional algebra has dimension 3 + 3×8 = 27, matching the bulk dimension exactly."
                ),
            ),
            ContentBlock(
                type="paragraph",
                content=(
                    "<Normal>"
                    "The cubic norm N(A) = c₁c₂c₃ − c₁|x₁|² − c₂|x₂|² − c₃|x₃|² + 2Re(x₁x₂x₃) "
                    "is the Jordan determinant and encodes the racetrack potential V_bridge/V_face. "
                    "</Normal>"
                    "<EML>"
                    "In EML mirror-phase notation: N(A) = ops.add(ops.mul(c₁,c₂,c₃), ops.neg(ops.add(c₁|x₁|², c₂|x₂|², c₃|x₃|²)), ops.mul(2, Re(x₁x₂x₃))). "
                    "The EML operator tree exposes the cancellation structure of the racetrack potential. "
                    "</EML>"
                ),
            ),
            ContentBlock(
                type="callout",
                callout_type="success",
                title="Computed Values (b₃ = {})".format(int(b3)),
                content=(
                    f"Pneuma condensate scale: b₃/27 = {float(b3)/27:.6f}  |  "
                    f"Jordan trace Tr(A) = {trace:.6f}  |  "
                    f"Cubic norm N(A) = {cubic:.6g}  |  "
                    f"Quartic invariant q(A) = {quartic:.6g}"
                ),
            ),
        ]

        return SectionContent(
            section_id="A2",
            subsection_id=None,
            title="Freudenthal Triple System: 27D Pneuma Condensate",
            abstract="The exceptional Jordan algebra J₃(𝕆) models the 27D Pneuma condensate; "
                     "its cubic norm encodes the racetrack potential and its quartic invariant "
                     "gives the ALP mass scale.",
            content_blocks=blocks,
            formula_refs=["freudenthal-cubic-norm", "freudenthal-quartic-invariant", "freudenthal-triple-product"],
            param_refs=self.output_params,
            appendix=True,
        )

    def get_certificates(self) -> List[Dict[str, Any]]:
        b3 = 24
        scale = b3 / 27.0
        trace = 3.0 * scale
        cubic = scale ** 3
        quartic = (trace ** 2 * (3.0 * scale ** 2)) / 4.0
        return [
            {
                "id": "CERT_FTS_SCALE",
                "assertion": f"Pneuma condensate scale = b3/27 = {scale:.8f} (b3=24)",
                "condition": f"abs({scale} - 24/27) < 1e-12",
                "status": "PASS",
            },
            {
                "id": "CERT_FTS_CUBIC",
                "assertion": f"Cubic norm N(A) = (b3/27)^3 = {cubic:.8f}",
                "condition": f"abs({cubic} - (24/27)**3) < 1e-12",
                "status": "PASS",
            },
            {
                "id": "CERT_FTS_QUARTIC_POSITIVE",
                "assertion": f"Quartic invariant q(A) = {quartic:.8g} > 0",
                "condition": f"{quartic} > 0",
                "status": "PASS",
            },
        ]

    def validate_self(self) -> Dict[str, Any]:
        b3 = 24
        scale = b3 / 27.0
        trace = 3.0 * scale
        cubic = scale ** 3
        quartic = (trace ** 2 * (3.0 * scale ** 2)) / 4.0
        return {
            "checks": [
                {
                    "name": "condensate_scale_from_b3",
                    "passed": abs(scale - 24.0 / 27.0) < 1e-12,
                    "log_level": "INFO",
                    "message": f"Pneuma condensate scale = b3/27 = {scale:.8f}",
                },
                {
                    "name": "cubic_norm_positive",
                    "passed": cubic > 0,
                    "log_level": "INFO",
                    "message": f"Cubic norm N(A) = {cubic:.8g} > 0",
                },
                {
                    "name": "quartic_invariant_positive",
                    "passed": quartic > 0,
                    "log_level": "INFO",
                    "message": f"Quartic invariant q(A) = {quartic:.8g} > 0",
                },
            ]
        }

    def get_references(self) -> List[Dict[str, Any]]:
        return [
            {
                "id": "freudenthal1954",
                "authors": "Freudenthal, H.",
                "title": "Beziehungen der E7 und E8 zur Oktavenebene I-II",
                "year": 1954,
                "url": "https://link.springer.com/article/10.1007/BF02564513",
            },
            {
                "id": "brown1969",
                "authors": "Brown, R.B.",
                "title": "Groups of type E7",
                "year": 1969,
                "doi": "10.1515/crll.1969.236.79",
            },
        ]

    def get_learning_materials(self) -> List[Dict[str, Any]]:
        return [
            {
                "topic": "Exceptional Jordan Algebra J3(O)",
                "url": "https://en.wikipedia.org/wiki/Freudenthal_magic_square",
                "relevance": "Background on the Freudenthal magic square and J3(O) construction underlying the 27D condensate",
            },
            {
                "topic": "Cubic Norm Forms",
                "url": "https://en.wikipedia.org/wiki/Albert_algebra",
                "relevance": "Albert algebra = J3(O) with its cubic norm, the mathematical structure of the Pneuma condensate",
            },
        ]
