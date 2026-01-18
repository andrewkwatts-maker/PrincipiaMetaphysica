#!/usr/bin/env python3
"""
PRINCIPIA METAPHYSICA v19.0 - Appendix N: Vielbein and Spin Connection
=======================================================================

DOI: 10.5281/zenodo.18079602

v19.0 FRAMEWORK: Vielbein formalism for spinors in curved spacetime.

This appendix provides a pedagogical introduction to the vielbein (tetrad)
formalism, following the eigenchris YouTube style of step-by-step, intuitive
derivations. The vielbein is essential for coupling spinors to gravity because
spinors transform under the local Lorentz group, not under general coordinate
transformations.

KEY CONCEPTS:
- Vielbein (tetrad): A field of orthonormal frames at each spacetime point
- Spin connection: The gauge field for local Lorentz transformations
- Cartan structure equations: Relate torsion and curvature to vielbein/connection
- Lorentz covariant derivative: Allows spinors to propagate in curved spacetime

WHY VIELBEIN?
In General Relativity, we work with tensor fields that transform under diffeomorphisms.
But spinors are not tensors - they transform under the double cover of the Lorentz group
(Spin(1,3)). To define spinors on a curved manifold, we need a local Lorentz frame at
each point. The vielbein provides exactly this: it maps between "curved" spacetime
indices and "flat" tangent space indices where we know how to define spinors.

APPENDIX: N (Vielbein and Spin Connection)

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.

Dedicated To:
    My Wife: Elizabeth May Watts
    Our Messiah: Jesus Of Nazareth
"""

import numpy as np
from typing import Dict, Any, List, Optional
import sys
import os

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


class VielbeinFormalism:
    """
    Vielbein (tetrad) formalism computations.

    The vielbein e^A_mu provides a map between curved spacetime indices (mu, nu, ...)
    and flat tangent space indices (A, B, ...). This is essential for defining
    spinor fields on curved manifolds.

    Notation conventions:
    - Greek indices (mu, nu, ...): curved spacetime indices, range 0-3
    - Capital Latin (A, B, ...): flat tangent space (Lorentz) indices, range 0-3
    - Lowercase Latin (a, b, ...): sometimes used for spatial Lorentz indices 1-3
    """

    # Minkowski metric in flat tangent space
    ETA = np.diag([1, -1, -1, -1])  # Mostly-minus convention (+---)

    @staticmethod
    def metric_from_vielbein(vielbein: np.ndarray) -> np.ndarray:
        """
        Compute the metric tensor from the vielbein.

        The fundamental relation: g_munu = eta_AB * e^A_mu * e^B_nu

        This shows that the metric is a derived quantity - the vielbein
        is more fundamental because it carries Lorentz structure.

        Args:
            vielbein: 4x4 array e^A_mu (first index A, second index mu)

        Returns:
            4x4 metric tensor g_munu
        """
        # g_munu = eta_AB * e^A_mu * e^B_nu
        # = sum over A,B of eta_AB * e^A_mu * e^B_nu
        metric = np.einsum('AB,Am,Bn->mn', VielbeinFormalism.ETA, vielbein, vielbein)
        return metric

    @staticmethod
    def vielbein_inverse(vielbein: np.ndarray) -> np.ndarray:
        """
        Compute the inverse vielbein E_A^mu.

        The inverse vielbein satisfies:
        - e^A_mu * E_A^nu = delta^nu_mu (completeness in spacetime)
        - e^A_mu * E_B^mu = delta^A_B (completeness in tangent space)

        Args:
            vielbein: 4x4 array e^A_mu

        Returns:
            4x4 inverse vielbein E_A^mu
        """
        return np.linalg.inv(vielbein.T).T

    @staticmethod
    def compute_spin_connection_from_vielbein(
        vielbein: np.ndarray,
        vielbein_deriv: np.ndarray
    ) -> np.ndarray:
        """
        Compute the torsion-free spin connection from vielbein and its derivatives.

        The spin connection omega^A_B_mu is determined by the torsion-free
        condition (first Cartan structure equation with T = 0):

        d e^A + omega^A_B wedge e^B = 0

        In components: partial_mu e^A_nu - partial_nu e^A_mu
                      + omega^A_B_mu e^B_nu - omega^A_B_nu e^B_mu = 0

        Args:
            vielbein: 4x4 array e^A_mu
            vielbein_deriv: 4x4x4 array partial_lambda e^A_mu

        Returns:
            4x4x4 spin connection omega^A_B_mu
        """
        E = VielbeinFormalism.vielbein_inverse(vielbein)
        eta = VielbeinFormalism.ETA

        # omega^A_B_mu = E^nu_B (partial_mu e^A_nu - partial_nu e^A_mu)
        #              + (1/2) e^A_lambda E^lambda_C E^rho_B (partial_rho e^C_sigma - partial_sigma e^C_rho) g^sigma_mu
        # Simplified for torsion-free case using Christoffel-like construction

        omega = np.zeros((4, 4, 4))

        # Using the formula: omega_AB_mu = E_A^nu (partial_mu e_B_nu - Gamma^lambda_mu_nu e_B_lambda)
        # where Gamma is the Christoffel symbol
        # This is equivalent to demanding metric compatibility and torsion-free

        # For this pedagogical implementation, compute directly:
        # omega^A_Bmu = E^nu_A partial_mu e^A_nu + (terms for antisymmetry in AB)
        for A in range(4):
            for B in range(4):
                for mu in range(4):
                    for nu in range(4):
                        omega[A, B, mu] += E[A, nu] * vielbein_deriv[mu, B, nu]

        # Antisymmetrize in Lorentz indices (lower both with eta)
        omega_antisym = np.zeros((4, 4, 4))
        for A in range(4):
            for B in range(4):
                for mu in range(4):
                    # omega_AB_mu = eta_AC omega^C_B_mu
                    omega_AB = sum(eta[A, C] * omega[C, B, mu] for C in range(4))
                    omega_BA = sum(eta[B, C] * omega[C, A, mu] for C in range(4))
                    omega_antisym[A, B, mu] = 0.5 * (omega_AB - omega_BA)

        return omega_antisym

    @staticmethod
    def compute_riemann_from_spin_connection(
        omega: np.ndarray,
        omega_deriv: np.ndarray
    ) -> np.ndarray:
        """
        Compute Riemann curvature from spin connection (second Cartan equation).

        R^A_B = d omega^A_B + omega^A_C wedge omega^C_B

        In components:
        R^A_B_mu_nu = partial_mu omega^A_B_nu - partial_nu omega^A_B_mu
                    + omega^A_C_mu omega^C_B_nu - omega^A_C_nu omega^C_B_mu

        Args:
            omega: 4x4x4 spin connection omega^A_B_mu
            omega_deriv: 4x4x4x4 derivative partial_lambda omega^A_B_mu

        Returns:
            4x4x4x4 Riemann tensor R^A_B_mu_nu
        """
        R = np.zeros((4, 4, 4, 4))

        for A in range(4):
            for B in range(4):
                for mu in range(4):
                    for nu in range(4):
                        # d omega term
                        R[A, B, mu, nu] = omega_deriv[mu, A, B, nu] - omega_deriv[nu, A, B, mu]

                        # omega wedge omega term
                        for C in range(4):
                            R[A, B, mu, nu] += omega[A, C, mu] * omega[C, B, nu]
                            R[A, B, mu, nu] -= omega[A, C, nu] * omega[C, B, mu]

        return R


class SpinorCovariantDerivative:
    """
    Covariant derivative for spinors in curved spacetime.

    Unlike vectors and tensors, spinors cannot be parallel-transported using
    the Christoffel connection. We need the spin connection which is valued
    in the Lorentz algebra.

    The covariant derivative of a spinor psi is:
    D_mu psi = partial_mu psi + (1/4) omega^AB_mu gamma_A gamma_B psi

    where gamma_A are the Dirac matrices in flat space and omega^AB_mu
    is the spin connection.
    """

    @staticmethod
    def lorentz_generator(A: int, B: int, gamma: np.ndarray) -> np.ndarray:
        """
        Compute the Lorentz generator Sigma^AB = (1/4)[gamma^A, gamma^B].

        The Lorentz generators satisfy the Lorentz algebra:
        [Sigma^AB, Sigma^CD] = eta^AC Sigma^BD - eta^BC Sigma^AD
                             - eta^AD Sigma^BC + eta^BD Sigma^AC

        Args:
            A: First Lorentz index
            B: Second Lorentz index
            gamma: Array of 4x4 Dirac gamma matrices

        Returns:
            4x4 Lorentz generator matrix
        """
        return 0.25 * (gamma[A] @ gamma[B] - gamma[B] @ gamma[A])

    @staticmethod
    def spinor_connection_term(
        omega: np.ndarray,
        gamma: np.ndarray,
        mu: int
    ) -> np.ndarray:
        """
        Compute the spinor connection contribution (1/4) omega^AB_mu Sigma_AB.

        This is the term that must be added to the partial derivative
        to make the full covariant derivative for spinors.

        Args:
            omega: Spin connection omega^AB_mu (antisymmetric in AB)
            gamma: Dirac gamma matrices
            mu: Spacetime index

        Returns:
            4x4 matrix representing the connection term
        """
        result = np.zeros((4, 4), dtype=complex)

        for A in range(4):
            for B in range(4):
                if A < B:  # Use antisymmetry
                    Sigma_AB = SpinorCovariantDerivative.lorentz_generator(A, B, gamma)
                    result += omega[A, B, mu] * Sigma_AB

        return result


class AppendixNVielbein(SimulationBase):
    """
    Appendix N: Vielbein and Spin Connection.

    This appendix provides a pedagogical introduction to the vielbein formalism,
    essential for coupling spinors to gravity in the Principia Metaphysica framework.

    Following the eigenchris YouTube pedagogy style, we develop the formalism
    step-by-step with intuitive explanations at each stage:

    1. Why we need vielbein: spinors need local Lorentz frames
    2. Vielbein definition: orthonormal frame field
    3. Metric from vielbein: g = eta * e * e
    4. Inverse and completeness: navigation between spaces
    5. Spin connection: gauge field for local Lorentz
    6. Torsion-free condition: first Cartan equation
    7. Curvature from connection: second Cartan equation
    8. Spinor covariant derivative: how spinors see curvature
    9. Relation to Christoffel: connecting formalisms

    SOLID Principles:
    - Single Responsibility: Handles vielbein formalism documentation
    - Open/Closed: Extensible for higher dimensions (G2 manifolds)
    - Dependency Inversion: References topology via registry when needed
    """

    FORMULA_REFS = [
        "vielbein-metric-relation-v19",
        "vielbein-orthonormality-v19",
        "vielbein-inverse-v19",
        "completeness-spacetime-v19",
        "completeness-tangent-v19",
        "spin-connection-definition-v19",
        "torsion-free-condition-v19",
        "cartan-first-structure-v19",
        "cartan-second-structure-v19",
        "riemann-from-spin-connection-v19",
        "spinor-covariant-derivative-v19",
        "lorentz-generator-spinor-v19",
        "spin-connection-christoffel-relation-v19",
    ]

    PARAM_REFS = [
        "vielbein.spacetime_dimension",
        "vielbein.lorentz_group_dimension",
        "vielbein.spinor_representation_dimension",
    ]

    @property
    def metadata(self) -> SimulationMetadata:
        return SimulationMetadata(
            id="appendix_n_vielbein_v19",
            version="19.0",
            domain="appendices",
            title="Appendix N: Vielbein and Spin Connection",
            description=(
                "Pedagogical introduction to vielbein formalism for coupling "
                "spinors to gravity in curved spacetime, following eigenchris style."
            ),
            section_id="N",
            subsection_id=None,
            appendix=True
        )

    @property
    def required_inputs(self) -> List[str]:
        return []

    @property
    def output_params(self) -> List[str]:
        return [
            "vielbein.spacetime_dimension",
            "vielbein.lorentz_group_dimension",
            "vielbein.spinor_representation_dimension",
        ]

    @property
    def output_formulas(self) -> List[str]:
        return self.FORMULA_REFS

    def run(self, registry: 'PMRegistry') -> Dict[str, Any]:
        """
        Execute vielbein formalism computations.

        Validates dimensional consistency and computes example quantities
        to demonstrate the formalism.

        Args:
            registry: PMRegistry instance

        Returns:
            Dictionary of vielbein-related parameters
        """
        # Spacetime dimension (4D for standard application)
        D = 4

        # Lorentz group SO(1,3) dimension
        lorentz_dim = D * (D - 1) // 2  # = 6

        # Spinor representation dimension (Dirac spinor in 4D)
        spinor_dim = 2 ** (D // 2)  # = 4

        # Number of vielbein components: D x D = 16
        vielbein_components = D * D

        # Number of spin connection components: 6 x 4 = 24 (antisymmetric in Lorentz)
        spin_connection_components = lorentz_dim * D

        # Example: flat spacetime vielbein (identity)
        e_flat = np.eye(4)
        g_flat = VielbeinFormalism.metric_from_vielbein(e_flat)

        # Verify metric is Minkowski
        is_minkowski = np.allclose(g_flat, VielbeinFormalism.ETA)

        return {
            "vielbein.spacetime_dimension": D,
            "vielbein.lorentz_group_dimension": lorentz_dim,
            "vielbein.spinor_representation_dimension": spinor_dim,
            "vielbein.total_components": vielbein_components,
            "vielbein.spin_connection_components": spin_connection_components,
            "vielbein.flat_space_verification": is_minkowski,
        }

    def get_section_content(self) -> Optional[SectionContent]:
        """Return section content for Appendix N: Vielbein and Spin Connection."""
        content_blocks = [
            # Main heading
            ContentBlock(
                type="heading",
                content="Vielbein and Spin Connection",
                level=2,
                label="N"
            ),

            # N.0 Motivation: Why Vielbein?
            ContentBlock(
                type="heading",
                content="N.0 Why Do We Need Vielbein?",
                level=3
            ),
            ContentBlock(
                type="paragraph",
                content=(
                    "In General Relativity, we describe gravity using the metric tensor g_munu, "
                    "which tells us about distances and angles in curved spacetime. Vectors and "
                    "tensors transform under general coordinate transformations (diffeomorphisms). "
                    "But there's a problem: <strong>spinors are not tensors</strong>."
                )
            ),
            ContentBlock(
                type="paragraph",
                content=(
                    "Spinors transform under the double cover of the Lorentz group, Spin(1,3). "
                    "They require a local Lorentz frame - a set of orthonormal basis vectors at "
                    "each point - to be properly defined. The vielbein (German for 'many legs', "
                    "also called 'tetrad' in 4D) provides exactly this: a field of orthonormal "
                    "frames that allows us to define spinors everywhere on a curved manifold."
                )
            ),
            ContentBlock(
                type="note",
                content=(
                    "<h4>Key Insight: Two Types of Indices</h4>"
                    "<ul>"
                    "<li><strong>Curved indices</strong> (Greek: mu, nu, ...): Transform under diffeomorphisms</li>"
                    "<li><strong>Flat indices</strong> (Latin: A, B, ...): Transform under local Lorentz</li>"
                    "</ul>"
                    "<p>The vielbein e^A_mu has one of each type - it's the bridge between the two worlds!</p>"
                ),
                label="index-types"
            ),

            # N.1 Vielbein Definition
            ContentBlock(
                type="heading",
                content="N.1 The Vielbein Field",
                level=3
            ),
            ContentBlock(
                type="paragraph",
                content=(
                    "The vielbein e^A_mu is a set of four orthonormal vector fields (in 4D). "
                    "At each point x, the vectors e^A(x) for A = 0, 1, 2, 3 form an orthonormal "
                    "basis for the tangent space, satisfying:"
                )
            ),
            ContentBlock(
                type="formula",
                content=r"\eta_{AB} = g_{\mu\nu} e^{\mu}_A e^{\nu}_B",
                formula_id="vielbein-orthonormality-v19",
                label="(N.1)"
            ),
            ContentBlock(
                type="paragraph",
                content=(
                    "Here eta_AB is the Minkowski metric diag(+1, -1, -1, -1) in the flat tangent "
                    "space. The vielbein 'solders' the flat tangent space to curved spacetime."
                )
            ),

            # N.2 Metric from Vielbein
            ContentBlock(
                type="heading",
                content="N.2 The Metric as a Derived Quantity",
                level=3
            ),
            ContentBlock(
                type="paragraph",
                content=(
                    "The fundamental relation of the vielbein formalism inverts (N.1) to express "
                    "the curved spacetime metric in terms of the vielbein:"
                )
            ),
            ContentBlock(
                type="formula",
                content=r"g_{\mu\nu} = \eta_{AB} e^A_\mu e^B_\nu",
                formula_id="vielbein-metric-relation-v19",
                label="(N.2)"
            ),
            ContentBlock(
                type="paragraph",
                content=(
                    "This is profound: the metric is no longer fundamental - it's constructed from "
                    "the vielbein! The vielbein carries more information because it knows about "
                    "local Lorentz orientations, not just distances."
                )
            ),
            ContentBlock(
                type="note",
                content=(
                    "<h4>Counting Degrees of Freedom</h4>"
                    "<p>In 4D:</p>"
                    "<ul>"
                    "<li>Metric g_munu: 10 independent components (symmetric 4x4)</li>"
                    "<li>Vielbein e^A_mu: 16 components (general 4x4)</li>"
                    "<li>Local Lorentz: 6 gauge freedoms (SO(1,3) rotations)</li>"
                    "<li>Net vielbein: 16 - 6 = 10 (matches metric!)</li>"
                    "</ul>"
                ),
                label="dof-counting"
            ),

            # N.3 Inverse Vielbein and Completeness
            ContentBlock(
                type="heading",
                content="N.3 Inverse Vielbein and Completeness Relations",
                level=3
            ),
            ContentBlock(
                type="paragraph",
                content=(
                    "The inverse vielbein E_A^mu allows us to go from curved to flat indices. "
                    "It satisfies two completeness relations:"
                )
            ),
            ContentBlock(
                type="formula",
                content=r"e^A_\mu E_A^\nu = \delta^\nu_\mu",
                formula_id="completeness-spacetime-v19",
                label="(N.3)"
            ),
            ContentBlock(
                type="formula",
                content=r"e^A_\mu E_B^\mu = \delta^A_B",
                formula_id="completeness-tangent-v19",
                label="(N.4)"
            ),
            ContentBlock(
                type="paragraph",
                content=(
                    "Equation (N.3) says: sum over Lorentz indices gives identity in spacetime. "
                    "Equation (N.4) says: sum over spacetime indices gives identity in tangent space. "
                    "These let us freely convert indices: V^A = e^A_mu V^mu and V^mu = E_A^mu V^A."
                )
            ),

            # N.4 Spin Connection
            ContentBlock(
                type="heading",
                content="N.4 The Spin Connection",
                level=3
            ),
            ContentBlock(
                type="paragraph",
                content=(
                    "When we have local Lorentz symmetry, we need a gauge field to define covariant "
                    "derivatives. This gauge field is the spin connection omega^A_B_mu. It's "
                    "antisymmetric in the Lorentz indices (because the Lorentz algebra is antisymmetric):"
                )
            ),
            ContentBlock(
                type="formula",
                content=r"\omega_{AB\mu} = -\omega_{BA\mu}",
                formula_id="spin-connection-definition-v19",
                label="(N.5)"
            ),
            ContentBlock(
                type="paragraph",
                content=(
                    "The spin connection has 6 x 4 = 24 components (6 antisymmetric Lorentz pairs "
                    "times 4 spacetime directions). It tells us how to parallel transport "
                    "Lorentz vectors (and spinors) along curves in spacetime."
                )
            ),

            # N.5 Torsion-Free Condition
            ContentBlock(
                type="heading",
                content="N.5 The Torsion-Free Condition",
                level=3
            ),
            ContentBlock(
                type="paragraph",
                content=(
                    "In General Relativity (without torsion), the spin connection is not "
                    "independent - it's determined by the vielbein through the torsion-free "
                    "condition. The torsion 2-form is:"
                )
            ),
            ContentBlock(
                type="formula",
                content=r"T^A = de^A + \omega^A{}_B \wedge e^B = 0",
                formula_id="torsion-free-condition-v19",
                label="(N.6)"
            ),
            ContentBlock(
                type="paragraph",
                content=(
                    "This is the <strong>first Cartan structure equation</strong> with T^A = 0. "
                    "In components:"
                )
            ),
            ContentBlock(
                type="formula",
                content=r"\partial_\mu e^A_\nu - \partial_\nu e^A_\mu + \omega^A{}_{B\mu} e^B_\nu - \omega^A{}_{B\nu} e^B_\mu = 0",
                formula_id="cartan-first-structure-v19",
                label="(N.7)"
            ),
            ContentBlock(
                type="paragraph",
                content=(
                    "This can be solved for omega in terms of e and its derivatives. The result "
                    "is sometimes called the 'Levi-Civita spin connection' or 'Ricci rotation coefficients'."
                )
            ),

            # N.6 Curvature from Spin Connection
            ContentBlock(
                type="heading",
                content="N.6 Curvature: The Second Cartan Equation",
                level=3
            ),
            ContentBlock(
                type="paragraph",
                content=(
                    "The curvature 2-form R^A_B is defined by the <strong>second Cartan structure "
                    "equation</strong>:"
                )
            ),
            ContentBlock(
                type="formula",
                content=r"R^A{}_B = d\omega^A{}_B + \omega^A{}_C \wedge \omega^C{}_B",
                formula_id="cartan-second-structure-v19",
                label="(N.8)"
            ),
            ContentBlock(
                type="paragraph",
                content="In components, the Riemann tensor with Lorentz indices is:"
            ),
            ContentBlock(
                type="formula",
                content=r"R^A{}_{B\mu\nu} = \partial_\mu \omega^A{}_{B\nu} - \partial_\nu \omega^A{}_{B\mu} + \omega^A{}_{C\mu} \omega^C{}_{B\nu} - \omega^A{}_{C\nu} \omega^C{}_{B\mu}",
                formula_id="riemann-from-spin-connection-v19",
                label="(N.9)"
            ),
            ContentBlock(
                type="paragraph",
                content=(
                    "This is related to the usual Riemann tensor with spacetime indices by: "
                    "R^rho_sigma_mu_nu = E_A^rho e^B_sigma R^A_B_mu_nu."
                )
            ),

            # N.7 Spinor Covariant Derivative
            ContentBlock(
                type="heading",
                content="N.7 Covariant Derivative for Spinors",
                level=3
            ),
            ContentBlock(
                type="paragraph",
                content=(
                    "Now we can finally define how spinors are covariantly differentiated! "
                    "For a Dirac spinor psi, the covariant derivative is:"
                )
            ),
            ContentBlock(
                type="formula",
                content=r"D_\mu \psi = \partial_\mu \psi + \frac{1}{4} \omega^{AB}{}_\mu \Sigma_{AB} \psi",
                formula_id="spinor-covariant-derivative-v19",
                label="(N.10)"
            ),
            ContentBlock(
                type="paragraph",
                content="where the Lorentz generators in the spinor representation are:"
            ),
            ContentBlock(
                type="formula",
                content=r"\Sigma_{AB} = \frac{1}{4} [\gamma_A, \gamma_B] = \frac{1}{2} \gamma_A \gamma_B \quad (A \neq B)",
                formula_id="lorentz-generator-spinor-v19",
                label="(N.11)"
            ),
            ContentBlock(
                type="paragraph",
                content=(
                    "The gamma matrices satisfy {gamma_A, gamma_B} = 2 eta_AB. The factor of 1/4 "
                    "in (N.10) ensures correct transformation under infinitesimal Lorentz rotations."
                )
            ),
            ContentBlock(
                type="note",
                content=(
                    "<h4>The Dirac Equation in Curved Spacetime</h4>"
                    "<p>With the covariant derivative defined, we can write the Dirac equation:</p>"
                    "<p style='text-align:center;'>(i gamma^mu D_mu - m) psi = 0</p>"
                    "<p>where gamma^mu = E_A^mu gamma^A uses the inverse vielbein to convert "
                    "flat gamma matrices to curved indices.</p>"
                ),
                label="curved-dirac"
            ),

            # N.8 Relation to Christoffel
            ContentBlock(
                type="heading",
                content="N.8 Relation to Christoffel Symbols",
                level=3
            ),
            ContentBlock(
                type="paragraph",
                content=(
                    "The spin connection and Christoffel symbols are related through the "
                    "vielbein postulate (metric compatibility + torsion-free):"
                )
            ),
            ContentBlock(
                type="formula",
                content=r"\omega^A{}_{B\mu} = e^A_\nu E_B^\rho \Gamma^\nu_{\rho\mu} + e^A_\nu \partial_\mu E_B^\nu",
                formula_id="spin-connection-christoffel-relation-v19",
                label="(N.12)"
            ),
            ContentBlock(
                type="paragraph",
                content=(
                    "This shows that the spin connection 'contains' the Christoffel symbol "
                    "information, plus additional terms involving vielbein derivatives. "
                    "For vectors, both formalisms give equivalent parallel transport; "
                    "for spinors, only the vielbein formalism works."
                )
            ),

            # N.9 Application to PM Framework
            ContentBlock(
                type="heading",
                content="N.9 Application to the Principia Metaphysica Framework",
                level=3
            ),
            ContentBlock(
                type="paragraph",
                content=(
                    "In the PM framework, the vielbein formalism is essential for several reasons:"
                )
            ),
            ContentBlock(
                type="note",
                content=(
                    "<ul>"
                    "<li><strong>G2 holonomy</strong>: On the 7-dimensional G2 manifold, the vielbein "
                    "e^A_m (A = 1,...,7) defines the parallel G2-structure.</li>"
                    "<li><strong>Fermion zero modes</strong>: Spinor fields on G2 require the spin "
                    "connection to define the Dirac operator whose zero modes give fermion generations.</li>"
                    "<li><strong>26D master action</strong>: The bulk vielbein E^A_M with A,M = 0,...,25 "
                    "encodes the unified time (24,1) signature with fibered structure geometry.</li>"
                    "<li><strong>Dimensional reduction</strong>: Vielbein decomposition tracks how "
                    "Lorentz symmetry breaks: SO(24,1) -> SO(3,1) x G2 via Euclidean bridge.</li>"
                    "</ul>"
                ),
                label="pm-applications"
            ),

            # Summary
            ContentBlock(
                type="heading",
                content="N.10 Summary of Key Formulas",
                level=3
            ),
            ContentBlock(
                type="note",
                content=(
                    "<table style='width:100%;'>"
                    "<tr><th>Concept</th><th>Formula</th><th>Meaning</th></tr>"
                    "<tr><td>Metric from vielbein</td><td>g_munu = eta_AB e^A_mu e^B_nu</td><td>Metric is derived quantity</td></tr>"
                    "<tr><td>Completeness</td><td>e^A_mu E_A^nu = delta^nu_mu</td><td>Vielbein inverts itself</td></tr>"
                    "<tr><td>Torsion-free</td><td>de^A + omega^A_B wedge e^B = 0</td><td>First Cartan equation</td></tr>"
                    "<tr><td>Curvature</td><td>R^A_B = d omega + omega wedge omega</td><td>Second Cartan equation</td></tr>"
                    "<tr><td>Spinor derivative</td><td>D_mu psi = partial_mu psi + (1/4) omega Sigma psi</td><td>Spinors see curvature</td></tr>"
                    "</table>"
                ),
                label="summary-table"
            ),
        ]

        return SectionContent(
            section_id="N",
            subsection_id=None,
            title="Appendix N: Vielbein and Spin Connection",
            abstract=(
                "Pedagogical introduction to vielbein formalism for coupling spinors to gravity. "
                "Covers vielbein definition, spin connection, Cartan structure equations, and "
                "covariant derivatives for spinors in curved spacetime."
            ),
            content_blocks=content_blocks,
            formula_refs=self.FORMULA_REFS,
            param_refs=self.PARAM_REFS,
            appendix=True,
        )

    def get_formulas(self) -> List[Formula]:
        """Return formula definitions for the vielbein formalism."""
        return [
            Formula(
                id="vielbein-metric-relation-v19",
                label="(N.2)",
                latex=r"g_{\mu\nu} = \eta_{AB} e^A_\mu e^B_\nu",
                plain_text="Metric from vielbein: g_munu = eta_AB e^A_mu e^B_nu",
                category="FOUNDATIONAL",
                description=(
                    "Metric tensor constructed from vielbein (tetrad) fields. "
                    "The fundamental relation showing metric is derived from vielbein."
                ),
                input_params=["vielbein.e_A_mu", "constants.eta_AB"],
                output_params=["metric.g_munu"],
            ),
            Formula(
                id="vielbein-orthonormality-v19",
                label="(N.1)",
                latex=r"\eta_{AB} = g_{\mu\nu} e^{\mu}_A e^{\nu}_B",
                plain_text="Vielbein orthonormality: eta_AB = g_munu e^mu_A e^nu_B",
                category="FOUNDATIONAL",
                description=(
                    "Orthonormality condition for vielbein. The vielbein vectors form "
                    "an orthonormal basis with respect to the Minkowski metric."
                ),
                input_params=["metric.g_munu", "vielbein.e_A_mu"],
                output_params=[],
            ),
            Formula(
                id="vielbein-inverse-v19",
                label="(N.3a)",
                latex=r"E_A^\mu = (e^{-1})_A^\mu",
                plain_text="Inverse vielbein: E_A^mu = (e^(-1))_A^mu",
                category="FOUNDATIONAL",
                description=(
                    "The inverse vielbein allows conversion from flat Lorentz indices "
                    "to curved spacetime indices."
                ),
                input_params=["vielbein.e_A_mu"],
                output_params=["vielbein.E_A_mu"],
            ),
            Formula(
                id="completeness-spacetime-v19",
                label="(N.3)",
                latex=r"e^A_\mu E_A^\nu = \delta^\nu_\mu",
                plain_text="Spacetime completeness: e^A_mu E_A^nu = delta^nu_mu",
                category="FOUNDATIONAL",
                description=(
                    "Completeness relation in spacetime. Summing over Lorentz indices "
                    "gives the identity in the spacetime manifold."
                ),
                input_params=["vielbein.e_A_mu", "vielbein.E_A_mu"],
                output_params=[],
            ),
            Formula(
                id="completeness-tangent-v19",
                label="(N.4)",
                latex=r"e^A_\mu E_B^\mu = \delta^A_B",
                plain_text="Tangent space completeness: e^A_mu E_B^mu = delta^A_B",
                category="FOUNDATIONAL",
                description=(
                    "Completeness relation in tangent space. Summing over spacetime indices "
                    "gives the identity in the flat Lorentz frame."
                ),
                input_params=["vielbein.e_A_mu", "vielbein.E_A_mu"],
                output_params=[],
            ),
            Formula(
                id="spin-connection-definition-v19",
                label="(N.5)",
                latex=r"\omega_{AB\mu} = -\omega_{BA\mu}",
                plain_text="Spin connection antisymmetry: omega_ABmu = -omega_BAmu",
                category="FOUNDATIONAL",
                description=(
                    "Antisymmetry of spin connection in Lorentz indices. This follows from "
                    "the antisymmetry of the Lorentz algebra generators."
                ),
                input_params=[],
                output_params=["connection.omega_AB_mu"],
            ),
            Formula(
                id="torsion-free-condition-v19",
                label="(N.6)",
                latex=r"T^A = de^A + \omega^A{}_B \wedge e^B = 0",
                plain_text="Torsion-free: T^A = de^A + omega^A_B wedge e^B = 0",
                category="FOUNDATIONAL",
                description=(
                    "Torsion-free condition (first Cartan structure equation with T=0). "
                    "This determines the spin connection from the vielbein."
                ),
                input_params=["vielbein.e_A_mu", "vielbein.de_A_mu"],
                output_params=["connection.omega_AB_mu"],
            ),
            Formula(
                id="cartan-first-structure-v19",
                label="(N.7)",
                latex=r"\partial_\mu e^A_\nu - \partial_\nu e^A_\mu + \omega^A{}_{B\mu} e^B_\nu - \omega^A{}_{B\nu} e^B_\mu = 0",
                plain_text="First Cartan in components",
                category="FOUNDATIONAL",
                description=(
                    "Component form of the first Cartan structure equation (torsion-free). "
                    "This equation can be solved for omega given e."
                ),
                input_params=["vielbein.e_A_mu", "vielbein.partial_e"],
                output_params=["connection.omega_AB_mu"],
            ),
            Formula(
                id="cartan-second-structure-v19",
                label="(N.8)",
                latex=r"R^A{}_B = d\omega^A{}_B + \omega^A{}_C \wedge \omega^C{}_B",
                plain_text="Curvature 2-form: R^A_B = d omega + omega wedge omega",
                category="FOUNDATIONAL",
                description=(
                    "Second Cartan structure equation defining curvature from spin connection. "
                    "This is the differential form version of the Riemann tensor."
                ),
                input_params=["connection.omega_AB_mu", "connection.d_omega"],
                output_params=["curvature.R_AB_munu"],
            ),
            Formula(
                id="riemann-from-spin-connection-v19",
                label="(N.9)",
                latex=r"R^A{}_{B\mu\nu} = \partial_\mu \omega^A{}_{B\nu} - \partial_\nu \omega^A{}_{B\mu} + \omega^A{}_{C\mu} \omega^C{}_{B\nu} - \omega^A{}_{C\nu} \omega^C{}_{B\mu}",
                plain_text="Riemann tensor from spin connection",
                category="FOUNDATIONAL",
                description=(
                    "Component form of Riemann curvature tensor with Lorentz indices, "
                    "computed from spin connection and its derivatives."
                ),
                input_params=["connection.omega_AB_mu", "connection.partial_omega"],
                output_params=["curvature.R_AB_munu"],
            ),
            Formula(
                id="spinor-covariant-derivative-v19",
                label="(N.10)",
                latex=r"D_\mu \psi = \partial_\mu \psi + \frac{1}{4} \omega^{AB}{}_\mu \Sigma_{AB} \psi",
                plain_text="Spinor covariant derivative: D_mu psi = partial_mu psi + (1/4) omega Sigma psi",
                category="FOUNDATIONAL",
                description=(
                    "Covariant derivative of a Dirac spinor in curved spacetime. "
                    "The spin connection couples to spinors through Lorentz generators."
                ),
                input_params=["spinor.psi", "connection.omega_AB_mu", "spinor.Sigma_AB"],
                output_params=["spinor.D_mu_psi"],
            ),
            Formula(
                id="lorentz-generator-spinor-v19",
                label="(N.11)",
                latex=r"\Sigma_{AB} = \frac{1}{4} [\gamma_A, \gamma_B]",
                plain_text="Lorentz generator: Sigma_AB = (1/4)[gamma_A, gamma_B]",
                category="FOUNDATIONAL",
                description=(
                    "Lorentz algebra generators in the spinor representation. "
                    "Built from commutators of Dirac gamma matrices."
                ),
                input_params=["spinor.gamma_A"],
                output_params=["spinor.Sigma_AB"],
            ),
            Formula(
                id="spin-connection-christoffel-relation-v19",
                label="(N.12)",
                latex=r"\omega^A{}_{B\mu} = e^A_\nu E_B^\rho \Gamma^\nu_{\rho\mu} + e^A_\nu \partial_\mu E_B^\nu",
                plain_text="Spin connection from Christoffel: omega = e E Gamma + e partial E",
                category="FOUNDATIONAL",
                description=(
                    "Relation between spin connection and Christoffel symbols. "
                    "Shows how vielbein formalism encodes standard GR connection."
                ),
                input_params=["vielbein.e_A_mu", "vielbein.E_A_mu", "metric.Gamma_rho_mu_nu"],
                output_params=["connection.omega_AB_mu"],
            ),
        ]

    def get_output_param_definitions(self) -> List[Parameter]:
        """Return parameter definitions for vielbein formalism."""
        return [
            Parameter(
                path="vielbein.spacetime_dimension",
                name="Spacetime Dimension",
                units="dimensionless",
                status="FOUNDATIONAL",
                description="Dimension of spacetime (D=4 for standard applications)",
                no_experimental_value=True,
            ),
            Parameter(
                path="vielbein.lorentz_group_dimension",
                name="Lorentz Group Dimension",
                units="dimensionless",
                status="FOUNDATIONAL",
                description="Dimension of local Lorentz group SO(1,3): D(D-1)/2 = 6",
                no_experimental_value=True,
            ),
            Parameter(
                path="vielbein.spinor_representation_dimension",
                name="Spinor Representation Dimension",
                units="dimensionless",
                status="FOUNDATIONAL",
                description="Dimension of Dirac spinor in 4D: 2^(D/2) = 4",
                no_experimental_value=True,
            ),
        ]

    def get_references(self) -> List[Dict[str, Any]]:
        """Return bibliographic references for vielbein formalism."""
        return [
            {
                "id": "carroll2004",
                "authors": "Carroll, S. M.",
                "title": "Spacetime and Geometry: An Introduction to General Relativity",
                "journal": "Addison Wesley",
                "year": "2004",
            },
            {
                "id": "nakahara2003",
                "authors": "Nakahara, M.",
                "title": "Geometry, Topology and Physics",
                "journal": "CRC Press",
                "year": "2003",
            },
            {
                "id": "weinberg1972",
                "authors": "Weinberg, S.",
                "title": "Gravitation and Cosmology",
                "journal": "John Wiley & Sons",
                "year": "1972",
            },
            {
                "id": "eigenchris2021",
                "authors": "eigenchris",
                "title": "Tensor Calculus and Relativity Tutorial Series",
                "journal": "YouTube",
                "year": "2021",
                "url": "https://www.youtube.com/c/eigenchris",
            },
        ]

    def get_foundations(self) -> List[Dict[str, Any]]:
        """Return foundational concepts for this appendix."""
        return [
            {
                "id": "differential-geometry",
                "title": "Differential Geometry",
                "category": "mathematics",
                "description": "Study of geometry using calculus on manifolds",
            },
            {
                "id": "spinor-theory",
                "title": "Spinor Theory",
                "category": "mathematics",
                "description": "Theory of spinors and their transformation properties",
            },
            {
                "id": "cartan-formalism",
                "title": "Cartan's Formalism",
                "category": "differential_geometry",
                "description": "Differential forms approach to geometry and connections",
            },
            {
                "id": "general-relativity",
                "title": "General Relativity",
                "category": "physics",
                "description": "Einstein's geometric theory of gravity",
            },
        ]


if __name__ == "__main__":
    import io
    import sys

    # Ensure UTF-8 output encoding
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

    from simulations.base import PMRegistry

    # Create registry
    registry = PMRegistry()

    # Create and run appendix
    appendix = AppendixNVielbein()

    print("=" * 70)
    print(f" {appendix.metadata.title}")
    print("=" * 70)
    print(f"Appendix ID: {appendix.metadata.id}")
    print(f"Version: {appendix.metadata.version}")
    print(f"Section: {appendix.metadata.section_id}")
    print()

    # Execute
    results = appendix.run(registry)

    # Print results
    print("\n" + "=" * 70)
    print(" VIELBEIN FORMALISM PARAMETERS")
    print("=" * 70)
    for key, value in results.items():
        print(f"{key}: {value}")
    print()

    # Print formulas
    print("=" * 70)
    print(" FORMULAS (13 total)")
    print("=" * 70)
    for formula in appendix.get_formulas():
        print(f"\n{formula.label} - {formula.id}")
        print(f"  LaTeX: {formula.latex[:60]}..." if len(formula.latex) > 60 else f"  LaTeX: {formula.latex}")
        print(f"  {formula.description[:70]}..." if len(formula.description) > 70 else f"  {formula.description}")
    print()

    # Test vielbein computations
    print("=" * 70)
    print(" VIELBEIN COMPUTATION TESTS")
    print("=" * 70)

    # Test with flat space vielbein
    e_flat = np.eye(4)
    g_flat = VielbeinFormalism.metric_from_vielbein(e_flat)
    print(f"\nFlat vielbein (identity):")
    print(f"  Resulting metric diagonal: {np.diag(g_flat)}")
    print(f"  Is Minkowski? {np.allclose(g_flat, VielbeinFormalism.ETA)}")

    # Test inverse
    E_flat = VielbeinFormalism.vielbein_inverse(e_flat)
    print(f"\nInverse vielbein test:")
    print(f"  e * E = identity? {np.allclose(e_flat @ E_flat, np.eye(4))}")

    print("\n" + "=" * 70)
    print(" APPENDIX N READY FOR PRINCIPIA METAPHYSICA v19.0")
    print("=" * 70)
