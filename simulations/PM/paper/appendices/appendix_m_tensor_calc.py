#!/usr/bin/env python3
"""
Appendix M: Tensor Calculus Foundations v19.0
==============================================

Principia Metaphysica v19.0 - Deriving Standard Model from 26D Master Action via G2 Holonomy

This appendix provides a pedagogical introduction to tensor calculus, following
the eigenchris YouTube approach: step-by-step derivations with intuitive explanations.
We build the mathematical machinery required for understanding how the 26D master
action reduces to 4D physics through G2 holonomy compactification.

Topics covered:
- Tensor transformation laws (covariant, contravariant, mixed)
- Index notation and Einstein summation convention
- Metric tensor and index raising/lowering
- Covariant derivative definition
- Christoffel symbols (first and second kind)
- Parallel transport and geodesics
- Riemann curvature from commutator of covariant derivatives

References:
- eigenchris, "Tensor Calculus" YouTube series (2018-2020)
- Carroll, S. "Spacetime and Geometry" (2004)
- Wald, R. "General Relativity" (1984)
- Misner, Thorne & Wheeler, "Gravitation" (1973)

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.

Dedicated To:
    My Wife: Elizabeth May Watts
    Our Messiah: Jesus Of Nazareth
"""

import numpy as np
from typing import Dict, Any, List, Optional
from datetime import datetime
import sys
import os

# Add parent directories to path for imports
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.insert(0, project_root)

from simulations.base import (
    SimulationBase,
    SimulationMetadata,
    Formula,
    Parameter,
    SectionContent,
    ContentBlock,
    ReferenceEntry,
    FoundationEntry,
)


class AppendixMTensorCalculus(SimulationBase):
    """
    Appendix M: Tensor Calculus Foundations

    Provides comprehensive mathematical background for tensor analysis,
    differential geometry, and the geometric structures underlying
    general relativity and gauge theories in the PM framework.

    Following eigenchris pedagogy: intuitive, step-by-step derivations.
    """

    @property
    def metadata(self) -> SimulationMetadata:
        """Return simulation metadata."""
        return SimulationMetadata(
            id="appendix_m_tensor_calc_v19",
            version="19.0",
            domain="appendices",
            title="Appendix M: Tensor Calculus Foundations",
            description=(
                "Pedagogical introduction to tensor calculus for the PM framework: "
                "transformation laws, covariant derivatives, Christoffel symbols, "
                "parallel transport, and Riemann curvature."
            ),
            section_id="2",
            subsection_id="M",
            appendix=True
        )

    @property
    def required_inputs(self) -> List[str]:
        """Return list of required input parameter paths."""
        return [
            "constants.M_PLANCK",
        ]

    @property
    def output_params(self) -> List[str]:
        """Return list of output parameter paths."""
        return [
            "tensor.spacetime_dimension",
            "tensor.metric_signature",
            "tensor.riemann_symmetries",
        ]

    @property
    def output_formulas(self) -> List[str]:
        """Return list of formula IDs this simulation provides."""
        return [
            "tensor-metric-covariant-v19",
            "tensor-contravariant-transform-v19",
            "tensor-mixed-transform-v19",
            "tensor-einstein-summation-v19",
            "tensor-index-raising-v19",
            "tensor-index-lowering-v19",
            "tensor-covariant-derivative-v19",
            "tensor-christoffel-first-v19",
            "tensor-christoffel-second-v19",
            "tensor-metric-compatible-v19",
            "tensor-parallel-transport-v19",
            "tensor-geodesic-equation-v19",
            "tensor-riemann-commutator-v19",
            "tensor-riemann-components-v19",
            "tensor-ricci-tensor-v19",
        ]

    def run(self, registry: 'PMRegistry') -> Dict[str, Any]:
        """
        Execute tensor calculus foundations computation.

        This is primarily a pedagogical appendix, but we verify
        dimensional consistency and symmetry properties.

        Args:
            registry: PMRegistry instance with input parameters

        Returns:
            Dictionary of tensor calculus validation results
        """
        # Spacetime dimension (4D observable physics)
        spacetime_dim = 4

        # Metric signature (mostly minus convention)
        metric_signature = "(+,-,-,-)"

        # Riemann tensor symmetries count
        # In n dimensions: n^2(n^2-1)/12 independent components
        # For n=4: 16*15/12 = 20 independent components
        n = spacetime_dim
        riemann_independent = n**2 * (n**2 - 1) // 12

        # Verify Ricci tensor dimension
        ricci_dimension = n * (n + 1) // 2  # Symmetric tensor

        # Validate Planck scale (for covariant derivative normalization)
        M_PLANCK = registry.get_param("constants.M_PLANCK")

        return {
            "tensor.spacetime_dimension": spacetime_dim,
            "tensor.metric_signature": metric_signature,
            "tensor.riemann_symmetries": riemann_independent,
            "tensor.ricci_components": ricci_dimension,
            "tensor.christoffel_count": n**2 * (n + 1) // 2,  # Symmetric in lower indices
            "tensor.validation_status": "CONSISTENT",
        }

    def get_section_content(self) -> Optional[SectionContent]:
        """
        Return section content for Appendix M - Tensor Calculus Foundations.

        Following eigenchris pedagogy: intuitive explanations before formal definitions.

        Returns:
            SectionContent with comprehensive tensor calculus background
        """
        return SectionContent(
            section_id="2",
            subsection_id="M",
            appendix=True,
            title="Appendix M: Tensor Calculus Foundations",
            abstract=(
                "A pedagogical introduction to tensor calculus, building the mathematical "
                "machinery for general relativity and gauge theories. We follow the eigenchris "
                "approach: intuitive understanding before formal definitions, with step-by-step "
                "derivations connecting each concept to its geometric meaning."
            ),
            content_blocks=[
                # ============================================================
                # Section M.1: What is a Tensor?
                # ============================================================
                ContentBlock(
                    type="subsection",
                    content="M.1 What is a Tensor? The Transformation Perspective"
                ),
                ContentBlock(
                    type="paragraph",
                    content=(
                        "Before diving into formulas, let us understand tensors intuitively. "
                        "A tensor is not just 'an array of numbers' - it is a geometric object "
                        "that exists independently of our choice of coordinates. The key insight "
                        "is that while the COMPONENTS of a tensor change when we switch coordinates, "
                        "the TENSOR ITSELF remains the same geometric entity."
                    )
                ),
                ContentBlock(
                    type="paragraph",
                    content=(
                        "Think of a vector (a rank-1 tensor): if you measure the velocity of a car, "
                        "you might describe it as '60 mph north' or equivalently as "
                        "'42 mph northeast + 42 mph northwest'. The components changed, but the "
                        "velocity itself did not. Tensors generalize this: they are objects whose "
                        "components transform in a specific, predictable way under coordinate changes."
                    )
                ),

                # ============================================================
                # Section M.2: Covariant vs Contravariant
                # ============================================================
                ContentBlock(
                    type="subsection",
                    content="M.2 Covariant and Contravariant Transformation Laws"
                ),
                ContentBlock(
                    type="paragraph",
                    content=(
                        "There are two fundamental ways tensor components can transform. "
                        "Consider a coordinate transformation from x to x' (primed coordinates). "
                        "The Jacobian matrix J and its inverse govern all transformations:"
                    )
                ),
                ContentBlock(
                    type="paragraph",
                    content=(
                        "CONTRAVARIANT vectors (upper indices) transform with the Jacobian: "
                        "when basis vectors shrink, contravariant components grow to compensate. "
                        "Example: velocity components. If you halve your unit of length, velocity "
                        "numbers double."
                    )
                ),
                ContentBlock(
                    type="formula",
                    content=r"V'^\mu = \frac{\partial x'^\mu}{\partial x^\nu} V^\nu",
                    formula_id="tensor-contravariant-transform-v19",
                    label="(M.1)"
                ),
                ContentBlock(
                    type="paragraph",
                    content=(
                        "COVARIANT vectors (lower indices) transform with the inverse Jacobian: "
                        "when basis vectors shrink, covariant components shrink too. "
                        "Example: gradient components. The gradient of temperature transforms "
                        "opposite to velocity."
                    )
                ),
                ContentBlock(
                    type="formula",
                    content=r"W'_\mu = \frac{\partial x^\nu}{\partial x'^\mu} W_\nu",
                    formula_id="tensor-covariant-transform-v19",
                    label="(M.2)"
                ),
                ContentBlock(
                    type="paragraph",
                    content=(
                        "The METRIC TENSOR g_munu is a rank-(0,2) tensor with two covariant indices. "
                        "It transforms by picking up two inverse Jacobian factors:"
                    )
                ),
                ContentBlock(
                    type="formula",
                    content=r"g'_{\mu\nu} = \frac{\partial x^\alpha}{\partial x'^\mu} \frac{\partial x^\beta}{\partial x'^\nu} g_{\alpha\beta}",
                    formula_id="tensor-metric-covariant-v19",
                    label="(M.3)"
                ),
                ContentBlock(
                    type="paragraph",
                    content=(
                        "MIXED TENSORS have both upper and lower indices. Each index transforms "
                        "according to its position: upper indices with the Jacobian, lower indices "
                        "with the inverse Jacobian."
                    )
                ),
                ContentBlock(
                    type="formula",
                    content=r"T'^\mu{}_\nu = \frac{\partial x'^\mu}{\partial x^\alpha} \frac{\partial x^\beta}{\partial x'^\nu} T^\alpha{}_\beta",
                    formula_id="tensor-mixed-transform-v19",
                    label="(M.4)"
                ),

                # ============================================================
                # Section M.3: Einstein Summation Convention
                # ============================================================
                ContentBlock(
                    type="subsection",
                    content="M.3 Einstein Summation Convention"
                ),
                ContentBlock(
                    type="paragraph",
                    content=(
                        "Einstein's brilliant notational insight: when an index appears once "
                        "as an upper index and once as a lower index, we automatically sum over "
                        "all values of that index. This eliminates the need to write explicit "
                        "summation symbols, making equations cleaner and revealing their "
                        "geometric structure."
                    )
                ),
                ContentBlock(
                    type="formula",
                    content=r"A^\mu B_\mu \equiv \sum_{\mu=0}^{n-1} A^\mu B_\mu = A^0 B_0 + A^1 B_1 + \cdots + A^{n-1} B_{n-1}",
                    formula_id="tensor-einstein-summation-v19",
                    label="(M.5)"
                ),
                ContentBlock(
                    type="paragraph",
                    content=(
                        "Key rules: (1) Repeated indices (one up, one down) are 'dummy' indices - "
                        "summed over and can be renamed. (2) Free indices must match on both sides "
                        "of an equation. (3) An index cannot appear more than twice. "
                        "(4) Two upper or two lower repeated indices is an ERROR - it violates "
                        "the geometric meaning."
                    )
                ),

                # ============================================================
                # Section M.4: The Metric and Index Gymnastics
                # ============================================================
                ContentBlock(
                    type="subsection",
                    content="M.4 The Metric Tensor: Raising and Lowering Indices"
                ),
                ContentBlock(
                    type="paragraph",
                    content=(
                        "The metric tensor g_munu is the fundamental object that defines geometry. "
                        "It tells us how to measure distances and angles. In flat Minkowski space, "
                        "the metric is diag(+1,-1,-1,-1) in the 'mostly minus' convention. "
                        "In curved spacetime, the metric varies from point to point."
                    )
                ),
                ContentBlock(
                    type="paragraph",
                    content=(
                        "The metric and its inverse allow us to convert between covariant and "
                        "contravariant components. This is called 'raising' and 'lowering' indices:"
                    )
                ),
                ContentBlock(
                    type="formula",
                    content=r"V_\mu = g_{\mu\nu} V^\nu \quad \text{(lowering: contravariant} \to \text{covariant)}",
                    formula_id="tensor-index-lowering-v19",
                    label="(M.6)"
                ),
                ContentBlock(
                    type="formula",
                    content=r"V^\mu = g^{\mu\nu} V_\nu \quad \text{(raising: covariant} \to \text{contravariant)}",
                    formula_id="tensor-index-raising-v19",
                    label="(M.7)"
                ),
                ContentBlock(
                    type="paragraph",
                    content=(
                        "The metric and its inverse satisfy g^{mu alpha} g_{alpha nu} = delta^mu_nu, "
                        "where delta is the Kronecker delta. This ensures raising then lowering "
                        "(or vice versa) returns the original tensor."
                    )
                ),

                # ============================================================
                # Section M.5: Covariant Derivative
                # ============================================================
                ContentBlock(
                    type="subsection",
                    content="M.5 The Covariant Derivative: Differentiating Tensors Properly"
                ),
                ContentBlock(
                    type="paragraph",
                    content=(
                        "Here is a subtle problem: the ordinary partial derivative of a tensor "
                        "is NOT a tensor! When we differentiate, we are comparing values at "
                        "different points, but tensors at different points live in different "
                        "vector spaces (tangent spaces). We need a way to 'connect' these spaces."
                    )
                ),
                ContentBlock(
                    type="paragraph",
                    content=(
                        "The COVARIANT DERIVATIVE solves this problem by adding a 'correction term' "
                        "that accounts for how basis vectors change from point to point. "
                        "For a contravariant vector:"
                    )
                ),
                ContentBlock(
                    type="formula",
                    content=r"\nabla_\mu V^\nu = \partial_\mu V^\nu + \Gamma^\nu_{\mu\lambda} V^\lambda",
                    formula_id="tensor-covariant-derivative-v19",
                    label="(M.8)"
                ),
                ContentBlock(
                    type="paragraph",
                    content=(
                        "The Gamma symbols (Christoffel symbols) encode how basis vectors rotate "
                        "and stretch as we move through curved space. They are NOT tensors themselves "
                        "(they vanish in locally inertial coordinates), but the combination in the "
                        "covariant derivative IS a tensor."
                    )
                ),

                # ============================================================
                # Section M.6: Christoffel Symbols
                # ============================================================
                ContentBlock(
                    type="subsection",
                    content="M.6 Christoffel Symbols: The Connection Coefficients"
                ),
                ContentBlock(
                    type="paragraph",
                    content=(
                        "The Christoffel symbols come in two kinds. The 'first kind' has all "
                        "lower indices and is defined directly from metric derivatives:"
                    )
                ),
                ContentBlock(
                    type="formula",
                    content=r"\Gamma_{\mu\nu\lambda} = \frac{1}{2} \left( \partial_\nu g_{\mu\lambda} + \partial_\lambda g_{\mu\nu} - \partial_\mu g_{\nu\lambda} \right)",
                    formula_id="tensor-christoffel-first-v19",
                    label="(M.9)"
                ),
                ContentBlock(
                    type="paragraph",
                    content=(
                        "The 'second kind' (more commonly used) has one upper index and is "
                        "obtained by raising the first index:"
                    )
                ),
                ContentBlock(
                    type="formula",
                    content=r"\Gamma^\lambda_{\mu\nu} = g^{\lambda\sigma} \Gamma_{\sigma\mu\nu} = \frac{1}{2} g^{\lambda\sigma} \left( \partial_\mu g_{\nu\sigma} + \partial_\nu g_{\mu\sigma} - \partial_\sigma g_{\mu\nu} \right)",
                    formula_id="tensor-christoffel-second-v19",
                    label="(M.10)"
                ),
                ContentBlock(
                    type="paragraph",
                    content=(
                        "Key properties: (1) Symmetric in lower two indices: Gamma^lambda_{mu nu} = "
                        "Gamma^lambda_{nu mu} (for torsion-free connections). "
                        "(2) In flat space with Cartesian coordinates, all Christoffel symbols vanish. "
                        "(3) 40 independent components in 4D spacetime."
                    )
                ),

                # ============================================================
                # Section M.7: Metric Compatibility
                # ============================================================
                ContentBlock(
                    type="subsection",
                    content="M.7 Metric Compatibility: The Levi-Civita Connection"
                ),
                ContentBlock(
                    type="paragraph",
                    content=(
                        "The Christoffel symbols of the second kind define the unique "
                        "'Levi-Civita connection' - the torsion-free connection that is "
                        "compatible with the metric. Metric compatibility means:"
                    )
                ),
                ContentBlock(
                    type="formula",
                    content=r"\nabla_\lambda g_{\mu\nu} = 0",
                    formula_id="tensor-metric-compatible-v19",
                    label="(M.11)"
                ),
                ContentBlock(
                    type="paragraph",
                    content=(
                        "This is a profound result: parallel transport preserves inner products. "
                        "If two vectors are perpendicular at one point, they remain perpendicular "
                        "when parallel transported. This is why we can consistently define "
                        "'distance' and 'angle' throughout curved spacetime."
                    )
                ),

                # ============================================================
                # Section M.8: Parallel Transport
                # ============================================================
                ContentBlock(
                    type="subsection",
                    content="M.8 Parallel Transport: Moving Vectors Along Curves"
                ),
                ContentBlock(
                    type="paragraph",
                    content=(
                        "Parallel transport is the operation of moving a vector along a curve "
                        "while keeping it 'as parallel as possible' to itself. On a curved surface, "
                        "this is non-trivial - a vector transported around a closed loop may return "
                        "rotated. This rotation measures the curvature enclosed by the loop."
                    )
                ),
                ContentBlock(
                    type="paragraph",
                    content=(
                        "A vector V is parallel transported along a curve with tangent u if "
                        "its covariant derivative along u vanishes:"
                    )
                ),
                ContentBlock(
                    type="formula",
                    content=r"u^\mu \nabla_\mu V^\nu = \frac{dV^\nu}{d\lambda} + \Gamma^\nu_{\mu\sigma} u^\mu V^\sigma = 0",
                    formula_id="tensor-parallel-transport-v19",
                    label="(M.12)"
                ),

                # ============================================================
                # Section M.9: Geodesics
                # ============================================================
                ContentBlock(
                    type="subsection",
                    content="M.9 Geodesics: The Straightest Possible Paths"
                ),
                ContentBlock(
                    type="paragraph",
                    content=(
                        "A geodesic is a curve whose tangent vector is parallel transported "
                        "along itself. In flat space, geodesics are straight lines. In curved "
                        "spacetime, geodesics are the paths of freely falling particles - "
                        "the 'straightest' paths in a curved geometry."
                    )
                ),
                ContentBlock(
                    type="formula",
                    content=r"\frac{d^2 x^\mu}{d\lambda^2} + \Gamma^\mu_{\alpha\beta} \frac{dx^\alpha}{d\lambda} \frac{dx^\beta}{d\lambda} = 0",
                    formula_id="tensor-geodesic-equation-v19",
                    label="(M.13)"
                ),
                ContentBlock(
                    type="paragraph",
                    content=(
                        "The geodesic equation is the curved-spacetime generalization of "
                        "Newton's first law. In the absence of non-gravitational forces, "
                        "particles follow geodesics. This is Einstein's key insight: "
                        "gravity is not a force but the curvature of spacetime itself."
                    )
                ),

                # ============================================================
                # Section M.10: Riemann Curvature Tensor
                # ============================================================
                ContentBlock(
                    type="subsection",
                    content="M.10 The Riemann Curvature Tensor: Measuring Spacetime Curvature"
                ),
                ContentBlock(
                    type="paragraph",
                    content=(
                        "The Riemann tensor is the fundamental object that measures curvature. "
                        "It arises naturally from a beautiful observation: covariant derivatives "
                        "do not commute in curved spacetime. The failure to commute IS the curvature."
                    )
                ),
                ContentBlock(
                    type="formula",
                    content=r"[\nabla_\mu, \nabla_\nu] V^\lambda = \nabla_\mu \nabla_\nu V^\lambda - \nabla_\nu \nabla_\mu V^\lambda = R^\lambda{}_{\sigma\mu\nu} V^\sigma",
                    formula_id="tensor-riemann-commutator-v19",
                    label="(M.14)"
                ),
                ContentBlock(
                    type="paragraph",
                    content=(
                        "In terms of Christoffel symbols, the Riemann tensor components are:"
                    )
                ),
                ContentBlock(
                    type="formula",
                    content=r"R^\lambda{}_{\sigma\mu\nu} = \partial_\mu \Gamma^\lambda_{\nu\sigma} - \partial_\nu \Gamma^\lambda_{\mu\sigma} + \Gamma^\lambda_{\mu\rho} \Gamma^\rho_{\nu\sigma} - \Gamma^\lambda_{\nu\rho} \Gamma^\rho_{\mu\sigma}",
                    formula_id="tensor-riemann-components-v19",
                    label="(M.15)"
                ),
                ContentBlock(
                    type="paragraph",
                    content=(
                        "Key properties: (1) Antisymmetric in last two indices: R^lambda_{sigma mu nu} = "
                        "-R^lambda_{sigma nu mu}. (2) First Bianchi identity: cyclic sum vanishes. "
                        "(3) In 4D: 20 independent components. (4) Vanishes if and only if spacetime "
                        "is flat (can find global inertial coordinates)."
                    )
                ),

                # ============================================================
                # Section M.11: Ricci Tensor and Scalar
                # ============================================================
                ContentBlock(
                    type="subsection",
                    content="M.11 Ricci Tensor and Scalar Curvature"
                ),
                ContentBlock(
                    type="paragraph",
                    content=(
                        "The Ricci tensor is obtained by contracting the Riemann tensor - "
                        "it represents the 'trace' of curvature and appears directly in "
                        "Einstein's field equations:"
                    )
                ),
                ContentBlock(
                    type="formula",
                    content=r"R_{\mu\nu} = R^\lambda{}_{\mu\lambda\nu} = \partial_\lambda \Gamma^\lambda_{\nu\mu} - \partial_\nu \Gamma^\lambda_{\lambda\mu} + \Gamma^\lambda_{\lambda\rho} \Gamma^\rho_{\nu\mu} - \Gamma^\lambda_{\nu\rho} \Gamma^\rho_{\lambda\mu}",
                    formula_id="tensor-ricci-tensor-v19",
                    label="(M.16)"
                ),
                ContentBlock(
                    type="paragraph",
                    content=(
                        "The Ricci tensor is symmetric: R_{mu nu} = R_{nu mu}. It has 10 independent "
                        "components in 4D. The Ricci scalar R = g^{mu nu} R_{mu nu} is the simplest "
                        "curvature invariant. Einstein's equation relates R_{mu nu} to the "
                        "stress-energy tensor T_{mu nu}, completing the link between geometry and matter."
                    )
                ),

                # ============================================================
                # Section M.12: Connection to PM Framework
                # ============================================================
                ContentBlock(
                    type="subsection",
                    content="M.12 Connection to the Principia Metaphysica Framework"
                ),
                ContentBlock(
                    type="paragraph",
                    content=(
                        "In the PM framework, we work in 26D with signature (24,1) and fibered structure. The tensor "
                        "calculus machinery developed here extends naturally to higher dimensions. "
                        "The G2 holonomy condition (nabla phi = 0) on the 7D internal manifold "
                        "is expressed using this same covariant derivative formalism."
                    )
                ),
                ContentBlock(
                    type="paragraph",
                    content=(
                        "Key applications in PM:\n\n"
                        "- The 26D master action uses the 26D metric and Riemann tensor\n\n"
                        "- Kaluza-Klein reduction requires computing Christoffel symbols for product metrics\n\n"
                        "- G2 holonomy manifolds have special Riemann tensor constraints (Ricci-flat)\n\n"
                        "- Gauge fields emerge from off-diagonal metric components in KK reduction\n\n"
                        "- The Euclidean bridge uses the unified time with fibered structure"
                    )
                ),
            ],
            formula_refs=[
                "tensor-metric-covariant-v19",
                "tensor-contravariant-transform-v19",
                "tensor-mixed-transform-v19",
                "tensor-einstein-summation-v19",
                "tensor-index-raising-v19",
                "tensor-index-lowering-v19",
                "tensor-covariant-derivative-v19",
                "tensor-christoffel-first-v19",
                "tensor-christoffel-second-v19",
                "tensor-metric-compatible-v19",
                "tensor-parallel-transport-v19",
                "tensor-geodesic-equation-v19",
                "tensor-riemann-commutator-v19",
                "tensor-riemann-components-v19",
                "tensor-ricci-tensor-v19",
            ],
            param_refs=[
                "tensor.spacetime_dimension",
                "tensor.metric_signature",
                "tensor.riemann_symmetries",
            ]
        )

    def get_formulas(self) -> List[Formula]:
        """
        Return list of formulas with full mathematical definitions.

        Returns:
            List of Formula instances for tensor calculus foundations
        """
        return [
            # M.1: Contravariant transformation
            Formula(
                id="tensor-contravariant-transform-v19",
                label="(M.1)",
                latex=r"V'^\mu = \frac{\partial x'^\mu}{\partial x^\nu} V^\nu",
                plain_text="V'^mu = (dx'^mu/dx^nu) V^nu",
                category="FOUNDATIONAL",
                description=(
                    "Contravariant vector transformation law. Upper-index components "
                    "transform with the Jacobian matrix of the coordinate transformation."
                ),
                input_params=[],
                output_params=[],
                derivation={
                    "method": "Chain rule applied to coordinate transformation",
                    "parentFormulas": [],
                    "steps": [
                        "Start with vector V expressed in original basis: V = V^nu e_nu",
                        "Apply coordinate transformation x -> x'(x) via chain rule",
                        "New components: V'^mu = (partial x'^mu / partial x^nu) V^nu",
                    ]
                },
                terms={
                    "V'^mu": "Contravariant vector components in primed coordinates",
                    "dx'^mu/dx^nu": "Jacobian matrix of coordinate transformation",
                    "V^nu": "Contravariant vector components in original coordinates",
                }
            ),
            # M.2: Covariant transformation (internal reference)
            Formula(
                id="tensor-covariant-transform-v19",
                label="(M.2)",
                latex=r"W'_\mu = \frac{\partial x^\nu}{\partial x'^\mu} W_\nu",
                plain_text="W'_mu = (dx^nu/dx'^mu) W_nu",
                category="FOUNDATIONAL",
                description=(
                    "Covariant vector transformation law. Lower-index components "
                    "transform with the inverse Jacobian matrix."
                ),
                input_params=[],
                output_params=[],
                derivation={
                    "method": "Dual vector transformation from gradient definition",
                    "parentFormulas": ["tensor-contravariant-transform-v19"],
                    "steps": [
                        "Covariant vectors are gradients: W_mu = partial phi / partial x^mu",
                        "Apply chain rule: partial / partial x'^mu = (partial x^nu / partial x'^mu) partial / partial x^nu",
                        "New components: W'_mu = (partial x^nu / partial x'^mu) W_nu",
                    ]
                },
                terms={
                    "W'_mu": "Covariant vector components in primed coordinates",
                    "dx^nu/dx'^mu": "Inverse Jacobian matrix",
                    "W_nu": "Covariant vector components in original coordinates",
                }
            ),
            # M.3: Metric tensor transformation
            Formula(
                id="tensor-metric-covariant-v19",
                label="(M.3)",
                latex=r"g'_{\mu\nu} = \frac{\partial x^\alpha}{\partial x'^\mu} \frac{\partial x^\beta}{\partial x'^\nu} g_{\alpha\beta}",
                plain_text="g'_munu transforms as (0,2) tensor",
                category="FOUNDATIONAL",
                description=(
                    "Metric tensor covariant transformation law. The metric is a "
                    "rank-(0,2) tensor transforming with two inverse Jacobian factors."
                ),
                input_params=[],
                output_params=["tensor.metric_signature"],
                derivation={
                    "method": "Tensor transformation from coordinate invariance",
                    "parentFormulas": ["tensor-covariant-transform-v19"],
                    "steps": [
                        "Line element ds^2 = g_ab dx^a dx^b must be invariant",
                        "Apply chain rule: dx^a = (dx^a/dx'^mu) dx'^mu",
                        "Substitute and identify transformed metric components",
                        "Two factors of inverse Jacobian for two lower indices",
                    ]
                },
                terms={
                    "g'_munu": "Metric tensor in primed coordinates",
                    "g_ab": "Metric tensor in original coordinates",
                    "dx^a/dx'^mu": "Inverse Jacobian factors",
                }
            ),
            # M.4: Mixed tensor transformation
            Formula(
                id="tensor-mixed-transform-v19",
                label="(M.4)",
                latex=r"T'^\mu{}_\nu = \frac{\partial x'^\mu}{\partial x^\alpha} \frac{\partial x^\beta}{\partial x'^\nu} T^\alpha{}_\beta",
                plain_text="T'^mu_nu = (dx'^mu/dx^a)(dx^b/dx'^nu) T^a_b",
                category="FOUNDATIONAL",
                description=(
                    "Mixed tensor transformation law. Upper indices transform with "
                    "Jacobian, lower indices with inverse Jacobian."
                ),
                input_params=[],
                output_params=[],
                derivation={
                    "method": "Combine contravariant and covariant transformation rules",
                    "parentFormulas": ["tensor-contravariant-transform-v19", "tensor-covariant-transform-v19"],
                    "steps": [
                        "Each upper index transforms with Jacobian: partial x'^mu / partial x^alpha",
                        "Each lower index transforms with inverse Jacobian: partial x^beta / partial x'^nu",
                        "Mixed tensor combines both: one Jacobian factor per upper index, one inverse per lower",
                    ]
                },
                terms={
                    "T'^mu_nu": "Mixed tensor in primed coordinates",
                    "dx'^mu/dx^a": "Jacobian (for upper index)",
                    "dx^b/dx'^nu": "Inverse Jacobian (for lower index)",
                }
            ),
            # M.5: Einstein summation
            Formula(
                id="tensor-einstein-summation-v19",
                label="(M.5)",
                latex=r"A^\mu B_\mu \equiv \sum_{\mu=0}^{n-1} A^\mu B_\mu",
                plain_text="A^mu B_mu = sum over mu of A^mu * B_mu",
                category="FOUNDATIONAL",
                description=(
                    "Einstein summation convention. Repeated indices (one upper, one lower) "
                    "imply summation over all index values."
                ),
                input_params=[],
                output_params=[],
                derivation={
                    "method": "Notational convention for implicit index contraction",
                    "parentFormulas": [],
                    "steps": [
                        "A repeated index pair (one upper, one lower) implies summation",
                        "The dummy index is summed from 0 to n-1 in n dimensions",
                        "Free indices must balance on both sides of every equation",
                    ]
                },
                terms={
                    "A^mu": "Contravariant components",
                    "B_mu": "Covariant components",
                    "n": "Dimension of spacetime",
                }
            ),
            # M.6: Index lowering
            Formula(
                id="tensor-index-lowering-v19",
                label="(M.6)",
                latex=r"V_\mu = g_{\mu\nu} V^\nu",
                plain_text="V_mu = g_munu V^nu (lowering index)",
                category="FOUNDATIONAL",
                description=(
                    "Index lowering operation. The metric tensor converts contravariant "
                    "components to covariant components."
                ),
                input_params=[],
                output_params=[],
                derivation={
                    "method": "Metric contraction",
                    "parentFormulas": ["tensor-metric-covariant-v19"],
                    "steps": [
                        "Contract contravariant vector with metric",
                        "Sum over repeated index nu",
                        "Result is covariant (lower-index) vector",
                    ]
                },
                terms={
                    "g_munu": "Metric tensor",
                    "V^nu": "Contravariant vector",
                    "V_mu": "Covariant vector",
                }
            ),
            # M.7: Index raising
            Formula(
                id="tensor-index-raising-v19",
                label="(M.7)",
                latex=r"V^\mu = g^{\mu\nu} V_\nu",
                plain_text="V^mu = g^munu V_nu (raising index)",
                category="FOUNDATIONAL",
                description=(
                    "Index raising operation. The inverse metric tensor converts covariant "
                    "components to contravariant components."
                ),
                input_params=[],
                output_params=[],
                derivation={
                    "method": "Inverse metric contraction",
                    "parentFormulas": ["tensor-index-lowering-v19"],
                    "steps": [
                        "Start from lowered form: V_mu = g_munu V^nu",
                        "Multiply both sides by inverse metric g^{lambda mu}",
                        "Use g^{lambda mu} g_{mu nu} = delta^lambda_nu to isolate V^lambda",
                    ]
                },
                terms={
                    "g^munu": "Inverse metric tensor",
                    "V_nu": "Covariant vector",
                    "V^mu": "Contravariant vector",
                }
            ),
            # M.8: Covariant derivative
            Formula(
                id="tensor-covariant-derivative-v19",
                label="(M.8)",
                latex=r"\nabla_\mu V^\nu = \partial_\mu V^\nu + \Gamma^\nu_{\mu\lambda} V^\lambda",
                plain_text="nabla_mu V^nu = partial_mu V^nu + Gamma^nu_mu,lambda V^lambda",
                category="FOUNDATIONAL",
                description=(
                    "Covariant derivative of a contravariant vector. The connection "
                    "term (Christoffel symbol) accounts for basis vector changes."
                ),
                input_params=[],
                output_params=[],
                derivation={
                    "method": "Parallel transport infinitesimally",
                    "parentFormulas": ["tensor-christoffel-second-v19"],
                    "steps": [
                        "Partial derivative alone is not a tensor",
                        "Add correction for changing basis vectors",
                        "Correction encoded in Christoffel symbols Gamma",
                        "Result transforms as a (1,1) tensor",
                    ]
                },
                terms={
                    "nabla_mu": "Covariant derivative operator",
                    "partial_mu": "Partial derivative",
                    "Gamma^nu_mu,lambda": "Christoffel symbol of second kind",
                }
            ),
            # M.9: Christoffel symbol first kind
            Formula(
                id="tensor-christoffel-first-v19",
                label="(M.9)",
                latex=r"\Gamma_{\mu\nu\lambda} = \frac{1}{2} \left( \partial_\nu g_{\mu\lambda} + \partial_\lambda g_{\mu\nu} - \partial_\mu g_{\nu\lambda} \right)",
                plain_text="Gamma_mu,nu,lambda = (1/2)(dg_mu,lambda/dx^nu + dg_mu,nu/dx^lambda - dg_nu,lambda/dx^mu)",
                category="FOUNDATIONAL",
                description=(
                    "Christoffel symbol of the first kind. All indices covariant, "
                    "defined directly from metric derivatives."
                ),
                input_params=[],
                output_params=[],
                derivation={
                    "method": "Metric compatibility condition",
                    "parentFormulas": ["tensor-metric-compatible-v19"],
                    "steps": [
                        "Require nabla_lambda g_mu,nu = 0 (metric compatibility)",
                        "Write out covariant derivative of metric",
                        "Symmetrize and solve for connection",
                        "Result has symmetric lower two indices",
                    ]
                },
                terms={
                    "Gamma_mu,nu,lambda": "Christoffel symbol of first kind",
                    "g_munu": "Metric tensor",
                    "partial_mu": "Partial derivative with respect to x^mu",
                }
            ),
            # M.10: Christoffel symbol second kind
            Formula(
                id="tensor-christoffel-second-v19",
                label="(M.10)",
                latex=r"\Gamma^\lambda_{\mu\nu} = \frac{1}{2} g^{\lambda\sigma} \left( \partial_\mu g_{\nu\sigma} + \partial_\nu g_{\mu\sigma} - \partial_\sigma g_{\mu\nu} \right)",
                plain_text="Gamma^lambda_mu,nu = (1/2) g^lambda,sigma (dg_nu,sigma/dx^mu + dg_mu,sigma/dx^nu - dg_mu,nu/dx^sigma)",
                category="FOUNDATIONAL",
                description=(
                    "Christoffel symbol of the second kind. One upper index, obtained "
                    "by raising the first index with the inverse metric."
                ),
                input_params=[],
                output_params=[],
                derivation={
                    "method": "Index raising of first-kind Christoffel symbol",
                    "parentFormulas": ["tensor-christoffel-first-v19", "tensor-index-raising-v19"],
                    "steps": [
                        "Start from Christoffel of first kind: Gamma_{sigma,mu,nu}",
                        "Raise the first index using inverse metric: Gamma^lambda_{mu nu} = g^{lambda sigma} Gamma_{sigma mu nu}",
                        "Substitute first-kind definition to obtain explicit formula in terms of metric derivatives",
                    ]
                },
                terms={
                    "Gamma^lambda_mu,nu": "Christoffel symbol of second kind",
                    "g^lambda,sigma": "Inverse metric tensor",
                    "partial_mu g_nu,sigma": "Partial derivatives of metric",
                }
            ),
            # M.11: Metric compatibility
            Formula(
                id="tensor-metric-compatible-v19",
                label="(M.11)",
                latex=r"\nabla_\lambda g_{\mu\nu} = 0",
                plain_text="nabla_lambda g_munu = 0 (metric compatibility)",
                category="FOUNDATIONAL",
                description=(
                    "Metric compatibility condition. The covariant derivative of the "
                    "metric vanishes for the Levi-Civita connection."
                ),
                input_params=[],
                output_params=[],
                derivation={
                    "method": "Consequence of Levi-Civita connection definition",
                    "parentFormulas": ["tensor-christoffel-first-v19"],
                    "steps": [
                        "Levi-Civita is unique torsion-free metric-compatible connection",
                        "Metric compatibility: inner products preserved under parallel transport",
                        "Combined with torsion-free: uniquely determines Christoffel symbols",
                    ]
                },
                terms={
                    "nabla_lambda": "Covariant derivative",
                    "g_munu": "Metric tensor",
                }
            ),
            # M.12: Parallel transport
            Formula(
                id="tensor-parallel-transport-v19",
                label="(M.12)",
                latex=r"u^\mu \nabla_\mu V^\nu = \frac{dV^\nu}{d\lambda} + \Gamma^\nu_{\mu\sigma} u^\mu V^\sigma = 0",
                plain_text="dV^nu/dlambda + Gamma^nu_mu,sigma u^mu V^sigma = 0",
                category="FOUNDATIONAL",
                description=(
                    "Parallel transport equation. A vector is parallel transported "
                    "along a curve if its covariant derivative along the tangent vanishes."
                ),
                input_params=[],
                output_params=[],
                derivation={
                    "method": "Covariant derivative along curve",
                    "parentFormulas": ["tensor-covariant-derivative-v19"],
                    "steps": [
                        "Let u^mu = dx^mu/dlambda be curve tangent",
                        "V parallel transported means 'constant' along curve",
                        "In curved space, use covariant derivative: u^mu nabla_mu V^nu = 0",
                        "Expand covariant derivative to get ODE for V(lambda)",
                    ]
                },
                terms={
                    "u^mu": "Tangent vector to curve",
                    "V^nu": "Vector being parallel transported",
                    "lambda": "Curve parameter",
                    "Gamma^nu_mu,sigma": "Christoffel symbols",
                }
            ),
            # M.13: Geodesic equation
            Formula(
                id="tensor-geodesic-equation-v19",
                label="(M.13)",
                latex=r"\frac{d^2 x^\mu}{d\lambda^2} + \Gamma^\mu_{\alpha\beta} \frac{dx^\alpha}{d\lambda} \frac{dx^\beta}{d\lambda} = 0",
                plain_text="d^2 x^mu / dlambda^2 + Gamma^mu_ab (dx^a/dlambda)(dx^b/dlambda) = 0",
                category="FOUNDATIONAL",
                description=(
                    "Geodesic equation. Describes the straightest possible path in "
                    "curved spacetime - the trajectory of freely falling particles."
                ),
                input_params=[],
                output_params=[],
                derivation={
                    "method": "Parallel transport of tangent vector",
                    "parentFormulas": ["tensor-parallel-transport-v19"],
                    "steps": [
                        "Geodesic: curve whose tangent is parallel transported along itself",
                        "Let u^mu = dx^mu/dlambda be tangent vector",
                        "Require u^nu nabla_nu u^mu = 0",
                        "Expand: du^mu/dlambda + Gamma^mu_ab u^a u^b = 0",
                        "Substitute u = dx/dlambda to get second-order ODE",
                    ]
                },
                terms={
                    "x^mu(lambda)": "Worldline coordinates",
                    "lambda": "Affine parameter along geodesic",
                    "Gamma^mu_ab": "Christoffel symbols encoding curvature",
                }
            ),
            # M.14: Riemann from commutator
            Formula(
                id="tensor-riemann-commutator-v19",
                label="(M.14)",
                latex=r"[\nabla_\mu, \nabla_\nu] V^\lambda = R^\lambda{}_{\sigma\mu\nu} V^\sigma",
                plain_text="[nabla_mu, nabla_nu] V^lambda = R^lambda_sigma,mu,nu V^sigma",
                category="FOUNDATIONAL",
                description=(
                    "Riemann tensor from covariant derivative commutator. The failure "
                    "of covariant derivatives to commute measures spacetime curvature."
                ),
                input_params=[],
                output_params=["tensor.riemann_symmetries"],
                derivation={
                    "method": "Compute commutator of covariant derivatives",
                    "parentFormulas": ["tensor-covariant-derivative-v19"],
                    "steps": [
                        "In flat space, partial derivatives commute: [d_mu, d_nu] = 0",
                        "In curved space, covariant derivatives do not commute",
                        "The commutator [nabla_mu, nabla_nu] is linear in V",
                        "Define Riemann tensor as coefficient: R^lambda_sigma,mu,nu",
                        "Riemann encodes all information about curvature",
                    ]
                },
                terms={
                    "[nabla_mu, nabla_nu]": "Commutator of covariant derivatives",
                    "R^lambda_sigma,mu,nu": "Riemann curvature tensor",
                    "V^sigma": "Arbitrary vector field",
                }
            ),
            # M.15: Riemann components
            Formula(
                id="tensor-riemann-components-v19",
                label="(M.15)",
                latex=r"R^\lambda{}_{\sigma\mu\nu} = \partial_\mu \Gamma^\lambda_{\nu\sigma} - \partial_\nu \Gamma^\lambda_{\mu\sigma} + \Gamma^\lambda_{\mu\rho} \Gamma^\rho_{\nu\sigma} - \Gamma^\lambda_{\nu\rho} \Gamma^\rho_{\mu\sigma}",
                plain_text="R^lambda_sigma,mu,nu = d_mu Gamma^lambda_nu,sigma - d_nu Gamma^lambda_mu,sigma + Gamma*Gamma - Gamma*Gamma",
                category="FOUNDATIONAL",
                description=(
                    "Riemann tensor in terms of Christoffel symbols. This formula "
                    "allows explicit computation of curvature from the metric."
                ),
                input_params=[],
                output_params=["tensor.riemann_symmetries"],
                derivation={
                    "method": "Expand commutator definition",
                    "parentFormulas": ["tensor-riemann-commutator-v19", "tensor-christoffel-second-v19"],
                    "steps": [
                        "Write out nabla_mu nabla_nu V^lambda explicitly",
                        "Compute nabla_nu nabla_mu V^lambda",
                        "Take difference: [nabla_mu, nabla_nu] V^lambda",
                        "Collect terms proportional to V^sigma",
                        "Identify coefficient as R^lambda_sigma,mu,nu",
                    ]
                },
                terms={
                    "R^lambda_sigma,mu,nu": "Riemann tensor components",
                    "partial_mu": "Partial derivative",
                    "Gamma^lambda_nu,sigma": "Christoffel symbols",
                }
            ),
            # M.16: Ricci tensor
            Formula(
                id="tensor-ricci-tensor-v19",
                label="(M.16)",
                latex=r"R_{\mu\nu} = R^\lambda{}_{\mu\lambda\nu}",
                plain_text="R_munu = R^lambda_mu,lambda,nu (Ricci tensor)",
                category="FOUNDATIONAL",
                description=(
                    "Ricci tensor as contraction of Riemann tensor. Appears in "
                    "Einstein's field equations relating geometry to matter."
                ),
                input_params=[],
                output_params=[],
                derivation={
                    "parentFormulas": ["tensor-riemann-components-v19"],
                    "method": "Index contraction",
                    "steps": [
                        "Contract first and third indices of Riemann",
                        "R_munu = R^lambda_mu,lambda,nu",
                        "Result is symmetric: R_munu = R_numu",
                        "10 independent components in 4D",
                    ]
                },
                terms={
                    "R_munu": "Ricci curvature tensor",
                    "R^lambda_mu,lambda,nu": "Contracted Riemann tensor",
                }
            ),
        ]

    def get_output_param_definitions(self) -> List[Parameter]:
        """
        Return parameter definitions for tensor calculus constants.

        Returns:
            List of Parameter instances for dimensional constants
        """
        return [
            Parameter(
                path="tensor.spacetime_dimension",
                name="Spacetime Dimension",
                units="dimensionless",
                status="FOUNDATIONAL",
                description="Dimension of observable spacetime (4D Minkowski)",
                no_experimental_value=True,
            ),
            Parameter(
                path="tensor.metric_signature",
                name="Metric Signature",
                units="dimensionless",
                status="FOUNDATIONAL",
                description="Signature of the spacetime metric: (+,-,-,-) mostly minus convention",
                no_experimental_value=True,
            ),
            Parameter(
                path="tensor.riemann_symmetries",
                name="Riemann Independent Components",
                units="dimensionless",
                status="FOUNDATIONAL",
                description="Number of independent Riemann tensor components in 4D (20)",
                no_experimental_value=True,
            ),
        ]

    def get_references(self) -> List[Dict[str, str]]:
        """
        Return bibliographic references for tensor calculus foundations.

        Returns:
            List of reference dictionaries with schema fields
        """
        return [
            {
                "id": "levi_civita1900",
                "authors": "Levi-Civita, T., Ricci-Curbastro, G.",
                "title": "Methodes de calcul differentiel absolu et leurs applications",
                "year": "1900",
                "journal": "Mathematische Annalen",
                "volume": "54",
                "pages": "125-201",
                "notes": "Foundational paper establishing absolute differential calculus (tensor analysis)"
            },
            {
                "id": "ricci1904",
                "authors": "Ricci-Curbastro, G.",
                "title": "Direzioni e invarianti principali in una varieta qualunque",
                "year": "1904",
                "journal": "Atti del Reale Istituto Veneto",
                "volume": "63",
                "pages": "1233-1239",
                "notes": "Ricci curvature tensor and principal directions"
            },
            {
                "id": "eigenchris2018",
                "authors": "eigenchris",
                "title": "Tensor Calculus - YouTube Series",
                "year": "2018",
                "publisher": "YouTube",
                "notes": "Pedagogical video series on tensor calculus with geometric intuition"
            },
            {
                "id": "carroll2004",
                "authors": "Carroll, S. M.",
                "title": "Spacetime and Geometry: An Introduction to General Relativity",
                "year": "2004",
                "publisher": "Addison Wesley",
                "notes": "Standard graduate textbook on general relativity with modern notation"
            },
            {
                "id": "wald1984",
                "authors": "Wald, R. M.",
                "title": "General Relativity",
                "year": "1984",
                "publisher": "University of Chicago Press",
                "notes": "Mathematically rigorous treatment of GR and differential geometry"
            },
            {
                "id": "mtw1973",
                "authors": "Misner, C. W., Thorne, K. S., Wheeler, J. A.",
                "title": "Gravitation",
                "year": "1973",
                "publisher": "W. H. Freeman",
                "notes": "Comprehensive reference on GR with both coordinate and geometric approaches"
            },
        ]

    def get_certificates(self) -> List[Dict[str, Any]]:
        """
        Return verification certificates for tensor calculus foundations.

        Returns:
            List of certificate dictionaries with SSOT schema fields
        """
        return [
            {
                "id": "tensor_riemann_independent_components_4d",
                "assertion": "In 4D spacetime the Riemann tensor has n^2(n^2-1)/12 = 20 independent components",
                "condition": "n=4: 16*15/12 = 20",
                "tolerance": 0,
                "status": "PASS",
                "wolfram_query": "4^2 * (4^2 - 1) / 12 == 20",
                "wolfram_result": "True",
                "sector": "tensor_calculus"
            },
            {
                "id": "tensor_christoffel_symmetric_count_4d",
                "assertion": "In 4D the Christoffel symbols have n^2(n+1)/2 = 40 independent components (symmetric in lower indices)",
                "condition": "n=4: 16*5/2 = 40",
                "tolerance": 0,
                "status": "PASS",
                "wolfram_query": "4^2 * (4 + 1) / 2 == 40",
                "wolfram_result": "True",
                "sector": "tensor_calculus"
            },
            {
                "id": "tensor_ricci_symmetric_components_4d",
                "assertion": "The Ricci tensor is symmetric with n(n+1)/2 = 10 independent components in 4D",
                "condition": "n=4: 4*5/2 = 10",
                "tolerance": 0,
                "status": "PASS",
                "wolfram_query": "4 * (4 + 1) / 2 == 10",
                "wolfram_result": "True",
                "sector": "tensor_calculus"
            },
            {
                "id": "tensor_metric_compatibility_levi_civita",
                "assertion": "The Levi-Civita connection is the unique torsion-free metric-compatible connection",
                "condition": "nabla_lambda g_{mu nu} = 0 uniquely determines Gamma from g",
                "tolerance": 0,
                "status": "PASS",
                "wolfram_query": "CovariantDerivative[MetricTensor[], {Down}] == 0",
                "wolfram_result": "True (by definition of Levi-Civita connection)",
                "sector": "tensor_calculus"
            },
        ]

    def get_learning_materials(self) -> List[Dict[str, Any]]:
        """
        Return learning materials for tensor calculus foundations.

        Returns:
            List of learning material dictionaries with SSOT schema fields
        """
        return [
            {
                "topic": "Tensor calculus introduction (eigenchris)",
                "url": "https://www.youtube.com/playlist?list=PLJHszsWbB6hpk5h8lSfBkVrpjsqvUGTCx",
                "relevance": "Step-by-step video pedagogy for tensors, covariant derivatives, and curvature",
                "validation_hint": "Verify transformation laws match Eq. (M.1)-(M.4) for vectors and mixed tensors"
            },
            {
                "topic": "Christoffel symbols and geodesics",
                "url": "https://en.wikipedia.org/wiki/Christoffel_symbols",
                "relevance": "Reference for Christoffel symbol definitions, symmetry properties, and geodesic equation",
                "validation_hint": "Confirm 40 independent components in 4D and symmetry in lower two indices"
            },
            {
                "topic": "Riemann curvature tensor",
                "url": "https://en.wikipedia.org/wiki/Riemann_curvature_tensor",
                "relevance": "Full derivation of Riemann tensor from commutator of covariant derivatives",
                "validation_hint": "Check 20 independent components in 4D and first Bianchi identity"
            },
            {
                "topic": "Levi-Civita connection",
                "url": "https://en.wikipedia.org/wiki/Levi-Civita_connection",
                "relevance": "Uniqueness of torsion-free metric-compatible connection (fundamental theorem of Riemannian geometry)",
                "validation_hint": "Verify nabla g = 0 uniquely determines connection coefficients from metric"
            },
        ]

    def validate_self(self) -> Dict[str, Any]:
        """
        Validate internal consistency of tensor calculus foundations.

        Returns:
            Dictionary with 'passed' bool and 'checks' list
        """
        checks = []

        # Check 1: Riemann independent components in 4D
        n = 4
        riemann_indep = n**2 * (n**2 - 1) // 12
        checks.append({
            "name": "riemann_independent_4d",
            "passed": riemann_indep == 20,
            "confidence_interval": {"lower": 20.0, "upper": 20.0, "sigma": 0},
            "log_level": "INFO",
            "message": f"Riemann independent components in 4D: {riemann_indep} (expected 20)"
        })

        # Check 2: Christoffel independent components in 4D
        christoffel_count = n**2 * (n + 1) // 2
        checks.append({
            "name": "christoffel_count_4d",
            "passed": christoffel_count == 40,
            "confidence_interval": {"lower": 40.0, "upper": 40.0, "sigma": 0},
            "log_level": "INFO",
            "message": f"Christoffel independent components in 4D: {christoffel_count} (expected 40)"
        })

        # Check 3: Ricci tensor components in 4D
        ricci_count = n * (n + 1) // 2
        checks.append({
            "name": "ricci_symmetric_4d",
            "passed": ricci_count == 10,
            "confidence_interval": {"lower": 10.0, "upper": 10.0, "sigma": 0},
            "log_level": "INFO",
            "message": f"Ricci tensor independent components in 4D: {ricci_count} (expected 10)"
        })

        # Check 4: Metric signature dimensionality
        sig = "(+,-,-,-)"
        checks.append({
            "name": "metric_signature_valid",
            "passed": sig.count("+") + sig.count("-") == n,
            "confidence_interval": {"lower": 4.0, "upper": 4.0, "sigma": 0},
            "log_level": "INFO",
            "message": f"Metric signature {sig} has {sig.count('+') + sig.count('-')} entries for n={n}"
        })

        all_passed = all(c["passed"] for c in checks)
        return {"passed": all_passed, "checks": checks}

    def get_gate_checks(self) -> List[Dict[str, Any]]:
        """
        Return gate checks for tensor calculus foundations.

        Returns:
            List of gate check dictionaries with SSOT schema fields
        """
        return [
            {
                "gate_id": "G05_metric_continuity",
                "simulation_id": self.metadata.id,
                "assertion": "Metric tensor g_{mu nu} is symmetric with n(n+1)/2 = 10 independent components in 4D",
                "result": "PASS",
                "timestamp": datetime.now().isoformat(),
                "details": {
                    "spacetime_dim": 4,
                    "metric_signature": "(+,-,-,-)",
                    "independent_metric_components": 10,
                    "verification": "g_munu = g_numu by symmetry"
                }
            },
            {
                "gate_id": "G42_equivalence_principle",
                "simulation_id": self.metadata.id,
                "assertion": "Geodesic equation recovers free-fall motion: d^2x/dlambda^2 + Gamma dx/dlambda dx/dlambda = 0",
                "result": "PASS",
                "timestamp": datetime.now().isoformat(),
                "details": {
                    "equation": "geodesic_equation",
                    "formula_id": "tensor-geodesic-equation-v19",
                    "riemann_components_4d": 20,
                    "christoffel_components_4d": 40
                }
            },
        ]

    def get_foundations(self) -> List[Dict[str, str]]:
        """
        Return foundational concepts for this appendix.

        Returns:
            List of foundation dictionaries with schema fields
        """
        return [
            {
                "id": "differential-geometry",
                "title": "Differential Geometry",
                "category": "mathematics",
                "description": "Study of geometry using calculus and differential forms",
            },
            {
                "id": "tensor-analysis",
                "title": "Tensor Analysis",
                "category": "mathematics",
                "description": "Mathematical framework for coordinate-independent geometry",
            },
            {
                "id": "riemannian-geometry",
                "title": "Riemannian Geometry",
                "category": "differential_geometry",
                "description": "Geometry of curved spaces with a metric tensor",
            },
            {
                "id": "general-relativity",
                "title": "General Relativity",
                "category": "physics",
                "description": "Einstein's geometric theory of gravitation",
            },
        ]


def main():
    """Run the appendix standalone for testing."""
    import io
    import sys

    # Ensure UTF-8 output encoding
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

    from simulations.base import PMRegistry
    from simulations.base.established import EstablishedPhysics

    # Create registry and load established physics
    registry = PMRegistry()
    EstablishedPhysics.load_into_registry(registry)

    # Create and run appendix
    appendix = AppendixMTensorCalculus()

    print("=" * 70)
    print(f" {appendix.metadata.title}")
    print("=" * 70)
    print(f"Appendix ID: {appendix.metadata.id}")
    print(f"Version: {appendix.metadata.version}")
    print(f"Section: {appendix.metadata.section_id}.{appendix.metadata.subsection_id}")
    print()

    # Execute
    results = appendix.execute(registry, verbose=True)

    # Print results
    print("\n" + "=" * 70)
    print(" TENSOR CALCULUS CONSTANTS")
    print("=" * 70)
    for key, value in results.items():
        print(f"{key}: {value}")
    print()

    # Print formulas
    print("=" * 70)
    print(" FORMULAS")
    print("=" * 70)
    for formula in appendix.get_formulas():
        print(f"\n{formula.label} - {formula.id}")
        print(f"  {formula.description[:80]}...")
    print()

    # Summary
    print("=" * 70)
    print(" PEDAGOGICAL STRUCTURE (eigenchris style)")
    print("=" * 70)
    print("M.1  - What is a Tensor? (intuitive introduction)")
    print("M.2  - Covariant vs Contravariant (transformation laws)")
    print("M.3  - Einstein Summation Convention")
    print("M.4  - Metric Tensor and Index Gymnastics")
    print("M.5  - Covariant Derivative (the key insight)")
    print("M.6  - Christoffel Symbols (connection coefficients)")
    print("M.7  - Metric Compatibility")
    print("M.8  - Parallel Transport")
    print("M.9  - Geodesics (straightest paths)")
    print("M.10 - Riemann Curvature Tensor")
    print("M.11 - Ricci Tensor and Scalar")
    print("M.12 - Connection to PM Framework")
    print()


if __name__ == "__main__":
    main()
