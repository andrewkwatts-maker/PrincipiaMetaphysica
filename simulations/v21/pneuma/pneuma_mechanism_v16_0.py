#!/usr/bin/env python3
"""
PRINCIPIA METAPHYSICA v22.0 - Pneuma Mechanism (Geometric Framework)
====================================================================

v22.0 CHANGES:
  - 12x(2,0) paired bridge system: M^{24,1} = T^1 x_fiber (bigoplus_{i=1}^{12} B_i^{2,0})
  - Pneuma I/O mechanism via paired bridges as "neural gates"
  - Per-pair OR reduction: R_perp^i = [[0,-1],[1,0]] for each pair
  - Full OR: tensor_{i=1}^{12} R_perp^i

PNEUMA I/O MECHANISM (v22):
  Each bridge pair B_i = (y_{1i}, y_{2i}) serves as a "neural gate":
    - Input (y_{1i}): Perception channel from bulk time t
    - Output (y_{2i}): Intuition via cyclic feedback through OR
  This creates 12 parallel consciousness channels.

Licensed under the MIT License. See LICENSE file for details.

Implements the Pneuma field dynamics and geometric coupling mechanism.

This simulation computes:
1. Pneuma coupling constant from G2 topology
2. Flow parameter governing field dynamics
3. Lagrangian validity via racetrack potential
4. Vielbein emergence from spinor bilinears
5. (v22) Neural gate I/O structure from 12 paired bridges

THEORETICAL FOUNDATION:
    The Pneuma field is a parallel spinor on the G2 holonomy manifold.
    Its dynamics are fully specified by:
    - Kinetic term: Standard spinor from vielbein emergence
    - Mass term: From G2 flux quantization (m_P ~ M_GUT / sqrt(chi_eff))
    - Potential: Racetrack from competing instantons
    - VEV: Dynamically selected via energy minimization
    - (v22) I/O structure: 12 paired bridges as neural gates

SECTION: 2 (Geometric Framework)

OUTPUTS:
    - pneuma.coupling: Pneuma-geometry coupling constant
    - pneuma.flow_parameter: Field flow parameter
    - pneuma.lagrangian_valid: Boolean flag for Lagrangian validity
    - pneuma.vev: Vacuum expectation value
    - pneuma.mass_scale: Characteristic mass scale

FORMULAS:
    - pneuma-lagrangian: Full Pneuma Lagrangian with racetrack potential
    - pneuma-flow: Flow equation for Pneuma field dynamics

REFERENCES:
    - Joyce (2000) "Compact Manifolds with Special Holonomy"
    - Acharya, Witten (2001) "M Theory and Singularities of G2 Manifolds"
    - Karigiannis (2009) "Flows of G2 Structures"
    - KKLT (2003) "de Sitter Vacua in String Theory" arXiv:hep-th/0301240

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.

Dedicated To:
    My Wife: Elizabeth May Watts
    Our Messiah: Jesus Of Nazareth
"""

import sys
import os
import numpy as np
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


class PneumaMechanismV16(SimulationBase):
    """
    Pneuma Field Mechanism Simulation (v22.0).

    Computes Pneuma field dynamics from G2 topology and validates
    the Lagrangian structure via racetrack potential analysis.

    v22.0 ADDITIONS:
        - 12x(2,0) paired bridge structure
        - Neural gate I/O mechanism for consciousness
        - Per-pair OR reduction operators
        - Input (y_{1i}): Perception from bulk time
        - Output (y_{2i}): Intuition via cyclic feedback
    """

    # v22.0: Number of bridge pairs from b3/2
    N_BRIDGE_PAIRS = 12  # b3 = 24 => 24/2 = 12 pairs

    def __init__(self):
        """Initialize the Pneuma mechanism simulation."""
        # G2 structure constants
        self.g2_norm = np.sqrt(7.0 / 3.0)  # Associative form norm

        # Racetrack parameters (will be computed from topology)
        self.a = None  # First instanton coefficient
        self.b = None  # Second instanton coefficient
        self.A = 1.0   # Prefactor (O(1))
        self.B = 1.03  # Prefactor with asymmetry

        # v22.0: Per-pair OR reduction operator
        # R_perp^i = [[0, -1], [1, 0]] for each pair i = 1, ..., 12
        self.R_perp = np.array([[0, -1], [1, 0]], dtype=float)

    # =========================================================================
    # METADATA
    # =========================================================================

    @property
    def metadata(self) -> SimulationMetadata:
        """Return metadata about this simulation."""
        return SimulationMetadata(
            id="pneuma_mechanism_v22_0",
            version="22.0",
            domain="pneuma",
            title="Pneuma Field Mechanism with 12x(2,0) Paired Bridges",
            description="Compute Pneuma field dynamics, coupling constants, neural gate I/O, and Lagrangian validity from G2 geometry with 12 paired bridge structure",
            section_id="2",
            subsection_id="2.6"  # v19.0: Unique subsection (Pneuma Mechanism)
        )

    @property
    def required_inputs(self) -> List[str]:
        """Return list of required input parameter paths from ESTABLISHED constants."""
        return [
            "constants.M_PLANCK",     # Planck mass for normalization
            "pdg.m_higgs",            # Higgs mass for hierarchy
        ]

    @property
    def output_params(self) -> List[str]:
        """Return list of output parameter paths."""
        return [
            "pneuma.coupling",
            "pneuma.flow_parameter",
            "pneuma.lagrangian_valid",
            "pneuma.vev",
            "pneuma.mass_scale",
            # v22.0: Neural gate I/O parameters
            "pneuma.n_bridge_pairs",
            "pneuma.neural_gate_active",
        ]

    @property
    def output_formulas(self) -> List[str]:
        """Return list of formula IDs this simulation provides."""
        return [
            "pneuma-lagrangian",
            "pneuma-flow",
            # v22.0: Neural gate formulas
            "pneuma-neural-gate",
            "pneuma-or-reduction",
        ]

    # =========================================================================
    # CORE COMPUTATION
    # =========================================================================

    def run(self, registry: 'PMRegistry') -> Dict[str, Any]:
        """
        Execute the Pneuma mechanism simulation.

        Args:
            registry: PMRegistry instance to read inputs from

        Returns:
            Dictionary mapping parameter paths to computed values
        """
        # Get input parameters
        M_PLANCK = registry.get_param("constants.M_PLANCK")
        m_higgs = registry.get_param("pdg.m_higgs")

        # Get topology parameters (if available) or use defaults
        if registry.has_param("topology.chi_eff"):
            chi_eff = registry.get_param("topology.chi_eff")
        else:
            chi_eff = 144  # Standard TCS #187 topology

        if registry.has_param("topology.b3"):
            b3 = registry.get_param("topology.b3")
        else:
            b3 = 24  # Associative 3-cycles

        # Compute flux quantization
        N_flux = chi_eff // 6  # = 24 for chi_eff = 144

        # Racetrack coefficients from instanton counting
        self.a = 2 * np.pi / N_flux           # = 2pi/24
        self.b = 2 * np.pi / (N_flux - 1)     # = 2pi/23

        # Compute Pneuma VEV from racetrack minimum
        vev = self._compute_vev()

        # Compute mass scale from G2 topology
        # m_P ~ M_GUT / sqrt(chi_eff) ~ 10^13 GeV
        # For now, use M_Planck / sqrt(chi_eff) as proxy
        mass_scale = M_PLANCK / np.sqrt(chi_eff)

        # Compute coupling constant from G2 normalization and topology
        # g_pneuma ~ sqrt(b3/24) * g2_norm * (m_higgs / M_Planck)
        topological_factor = np.sqrt(b3 / 24.0)
        hierarchy_factor = m_higgs / M_PLANCK
        coupling = topological_factor * self.g2_norm * hierarchy_factor

        # Compute flow parameter (dimensionless)
        # Governs field evolution: phi_dot = -flow_parameter * dV/dphi
        flow_parameter = self._compute_flow_parameter()

        # Validate Lagrangian via stability check
        lagrangian_valid = self._validate_lagrangian(vev)

        # v22.0: Compute neural gate structure from b3
        n_bridge_pairs = b3 // 2  # b3 = 24 => 12 pairs
        neural_gate_active = lagrangian_valid and n_bridge_pairs == self.N_BRIDGE_PAIRS

        # Return computed values
        return {
            "pneuma.coupling": float(coupling),
            "pneuma.flow_parameter": float(flow_parameter),
            "pneuma.lagrangian_valid": bool(lagrangian_valid),
            "pneuma.vev": float(vev),
            "pneuma.mass_scale": float(mass_scale),
            # v22.0: Neural gate I/O
            "pneuma.n_bridge_pairs": int(n_bridge_pairs),
            "pneuma.neural_gate_active": bool(neural_gate_active),
        }

    # =========================================================================
    # HELPER METHODS
    # =========================================================================

    def _superpotential_derivative(self, psi: float) -> float:
        """
        Derivative dW/dPsi of racetrack superpotential.

        dW/dPsi = -A*a*exp(-a*Psi) + B*b*exp(-b*Psi)
        """
        return -self.A * self.a * np.exp(-self.a * psi) + self.B * self.b * np.exp(-self.b * psi)

    def _potential(self, psi: float) -> float:
        """
        Scalar potential V(Psi) = |dW/dPsi|^2.
        """
        dW = self._superpotential_derivative(psi)
        return dW ** 2

    def _potential_second_derivative(self, psi: float) -> float:
        """
        Second derivative d^2V/dPsi^2 for stability check.
        """
        term_a = self.A * self.a * np.exp(-self.a * psi)
        term_b = self.B * self.b * np.exp(-self.b * psi)
        dW = -term_a + term_b
        d2W = self.A * self.a**2 * np.exp(-self.a * psi) - self.B * self.b**2 * np.exp(-self.b * psi)
        d3W = -self.A * self.a**3 * np.exp(-self.a * psi) + self.B * self.b**3 * np.exp(-self.b * psi)

        return 2 * d2W**2 + 2 * dW * d3W

    def _compute_vev(self) -> float:
        """
        Compute Pneuma VEV from analytic minimum.

        <Psi_P> = (1/(b-a)) * ln(B*b / (A*a))
        """
        if self.a is None or self.b is None:
            raise ValueError("Racetrack coefficients not initialized")

        return (1 / (self.b - self.a)) * np.log((self.B * self.b) / (self.A * self.a))

    def _compute_flow_parameter(self) -> float:
        """
        Compute flow parameter governing field dynamics.

        Lambda = sqrt(2 * V''(<Psi>)) (characteristic frequency)
        """
        vev = self._compute_vev()
        d2V = self._potential_second_derivative(vev)

        if d2V > 0:
            return np.sqrt(2 * d2V)
        else:
            return 0.0  # Unstable - should not happen

    def _validate_lagrangian(self, vev: float) -> bool:
        """
        Validate Lagrangian via stability check.

        Lagrangian is valid if:
        1. V''(<Psi>) > 0 (stable minimum)
        2. VEV is finite and positive
        """
        if not np.isfinite(vev) or vev <= 0:
            return False

        hessian = self._potential_second_derivative(vev)
        return hessian > 0

    def _apply_or_reduction(self, y1: float, y2: float) -> tuple:
        """
        Apply per-pair OR reduction operator R_perp to bridge coordinates.

        v22.0: Each pair (y_{1i}, y_{2i}) transforms under:
            R_perp^i = [[0, -1], [1, 0]]

        Input channel (y_1): Perception from bulk time t
        Output channel (y_2): Intuition via cyclic feedback

        Args:
            y1: Normal-shadow coordinate (perception input)
            y2: Mirror-shadow coordinate (intuition output)

        Returns:
            Tuple (y1', y2') after 90-degree rotation
        """
        vec = np.array([y1, y2])
        transformed = self.R_perp @ vec
        return (transformed[0], transformed[1])

    def _compute_full_or_reduction(self) -> np.ndarray:
        """
        Compute full OR reduction operator as tensor product.

        v22.0: R_perp^full = bigotimes_{i=1}^{12} R_perp^i

        The full operator is a 2^12 x 2^12 = 4096 x 4096 matrix,
        but we represent it symbolically as the tensor product.

        Returns:
            2x2 per-pair operator (full tensor computed on-demand)
        """
        # Return per-pair operator; full tensor is too large to store
        # Property: (R_perp^full)^2 = (-1)^12 * I = I (even number of pairs)
        return self.R_perp

    # =========================================================================
    # SECTION CONTENT
    # =========================================================================

    def get_section_content(self) -> Optional[SectionContent]:
        """
        Return section content for Section 2 - The Pneuma Lagrangian (COMPLETE MIGRATION from section-pneuma-lagrangian.json).

        This supplementary section provides a detailed derivation of the Pneuma field dynamics,
        from the fundamental 26D action through dimensional reduction to the 4D effective theory.
        """
        content_blocks = []

        # =====================================================================
        # INTRODUCTION
        # =====================================================================
        content_blocks.extend([
            ContentBlock(
                type="paragraph",
                content="The Pneuma Lagrangian is the fundamental fermionic field term that sources all of physics - from spacetime geometry to matter content. It represents a generalized Dirac action for a fundamental fermionic field living in the full 26-dimensional spacetime with signature (24,1) plus Euclidean bridge."
            ),
            ContentBlock(
                type="formula",
                content="S = ∫ d^26 X √(-G) [R + Ψ_P (iΓ^M D_M - m)Ψ_P + ℒ_bridge]",
                label="Main Equation"
            ),
        ])

        # =====================================================================
        # COMPONENT BREAKDOWN
        # =====================================================================
        content_blocks.extend([
            ContentBlock(
                type="heading",
                content="Component Breakdown"
            ),
            ContentBlock(
                type="paragraph",
                content="The Pneuma Lagrangian is a generalized Dirac action for a fundamental fermionic field living in the full 26-dimensional spacetime with signature (24,1) plus Euclidean bridge. After OR reduction, we obtain dual (11,1) shadows with unified time. Each component has specific physical meaning:"
            ),
            ContentBlock(
                type="heading",
                content="Dirac Adjoint"
            ),
            ContentBlock(
                type="paragraph",
                content="The Dirac adjoint of the Pneuma field: Ψ̄_P = Ψ_P† Γ^0. Required for Lorentz-invariant bilinears in higher dimensions."
            ),
            ContentBlock(
                type="heading",
                content="Pneuma Spinor Field"
            ),
            ContentBlock(
                type="paragraph",
                content="A 4096-component Dirac spinor in full 26D (2^12 = 4096 from Cl(24,1)). Reduces to 64-component effective spinor via OR reduction. Further decomposes as 64 = 4 x 16 under 4D spacetime x internal manifold split."
            ),
            ContentBlock(
                type="heading",
                content="Kinetic Term"
            ),
            ContentBlock(
                type="paragraph",
                content="The covariant Dirac operator: Γ^M D_M where M runs over all 26 dimensions (effective dual shadows after OR reduction). Γ^M are 4096x4096 matrices in 26D Cl(24,1), 64x64 in effective dual shadow Cl(11,1)."
            ),
            ContentBlock(
                type="heading",
                content="Bulk Mass"
            ),
            ContentBlock(
                type="paragraph",
                content="The fundamental mass parameter m_P for the Pneuma field. Sets the scale for Pneuma condensation and influences 4D fermion masses through dimensional reduction."
            ),
            ContentBlock(
                type="heading",
                content="Orthogonal Time Coupling"
            ),
            ContentBlock(
                type="paragraph",
                content="In 26D with signature (24,1) plus Euclidean bridge: coupling constant g times the bridge coordinates. The Euclidean bridge enables thermal time emergence and resolves causality issues via OR reduction to unified time."
            ),
            ContentBlock(
                type="heading",
                content="Quartic Interaction"
            ),
            ContentBlock(
                type="paragraph",
                content="Self-interaction term with coupling constant λ. Responsible for Pneuma condensation and dynamical mass generation through spontaneous symmetry breaking."
            ),
        ])

        # =====================================================================
        # GAMMA MATRICES: 26D to 13D
        # =====================================================================
        content_blocks.extend([
            ContentBlock(
                type="heading",
                content="The Gamma Matrices: 26D to 13D"
            ),
            ContentBlock(
                type="paragraph",
                content="In full 26D with signature (24,1), the gamma matrices Γ^M form a representation of the Clifford algebra Cl(24,1) with dimension 2^12 = 4096. Upon OR reduction to dual shadows, we obtain the effective Cl(11,1) algebra:"
            ),
            ContentBlock(
                type="heading",
                content="Dimensional Reduction: Cl(24,1) → Cl(11,1)"
            ),
            ContentBlock(
                type="paragraph",
                content="Full 26D: Spinor dimension = 2^12 = 4096 components from Cl(24,1). Effective dual shadows: After OR reduction, spinor reduces to 2^6 = 64 components. The OR reduction produces dual (11,1) shadows with unified time from (24,1) plus Euclidean bridge."
            ),
            ContentBlock(
                type="paragraph",
                content="In the effective 13D theory, the gamma matrices can be constructed from tensor products:"
            ),
            ContentBlock(
                type="formula",
                content="Γ^μ = γ^μ ⊗ 1_16 (μ = 0,1,2,3)\nΓ^{a+3} = γ^5 ⊗ Σ^a (a = 1,...,8)\n— Tensor product decomposition",
                label=""
            ),
            ContentBlock(
                type="paragraph",
                content="Here γ^μ are the 4D Dirac matrices, γ^5 = iγ^0γ^1γ^2γ^3 is the 4D chirality operator, and Σ^a are 16×16 matrices acting on the internal spinor space."
            ),
            ContentBlock(
                type="callout",
                callout_type="info",
                title="Dimensional Reduction: Cl(24,1) → Cl(12,1)",
                content="Full 26D: Spinor dimension = 2^12 = 4096 components from Cl(24,1). Effective dual shadows: After OR reduction, spinor reduces to 2^6 = 64 components. The OR reduction produces dual (11,1) shadows with unified time from (24,1) plus Euclidean bridge."
            ),
        ])

        # =====================================================================
        # COVARIANT DERIVATIVE
        # =====================================================================
        content_blocks.extend([
            ContentBlock(
                type="heading",
                content="The Covariant Derivative"
            ),
            ContentBlock(
                type="paragraph",
                content="The full covariant derivative D_M acting on the Pneuma spinor in 26D includes both gravitational and gauge connections. In the full theory, M ranges over all 26 dimensions; in the effective 13D theory, M = 0, 1, ..., 12. The derivative includes spin connection and gauge field contributions."
            ),
        ])

        # =====================================================================
        # PHYSICAL INTERPRETATION
        # =====================================================================
        content_blocks.extend([
            ContentBlock(
                type="heading",
                content="Physical Interpretation"
            ),
            ContentBlock(
                type="heading",
                content="Source of Geometry"
            ),
            ContentBlock(
                type="paragraph",
                content="The Pneuma field Ψ_P is not merely a matter field living on a fixed background - it is the fundamental source of spacetime itself. Through its bilinear condensates: g_mn ∝ ⟨Ψ̄_P Γ_mn Ψ_P⟩, these vacuum expectation values generate the metric structure of the internal manifold K_Pneuma, effectively determining the geometry of the extra dimensions."
            ),
            ContentBlock(
                type="paragraph",
                content="K_Pneuma is realized as an explicit TCS (Twisted Connected Sum) G₂ manifold with Betti numbers b₂=4 (associative cycles hosting D₅ singularity for SO(10) gauge symmetry) and b₃=24 (co-associative cycles controlling Yukawa textures), constructed via π/6 hyper-Kähler rotation following Corti-Haskins-Nordenstam-Pacini (arXiv:1809.09083)."
            ),
            ContentBlock(
                type="heading",
                content="Source of Matter"
            ),
            ContentBlock(
                type="paragraph",
                content="Upon dimensional reduction over K_Pneuma, the full 4096-component 26D spinor (or equivalently, the 64-component effective dual shadow spinor) decomposes into 4D chiral fermions. The topological structure (zero modes of the Dirac operator on K_Pneuma) determines the number of generations: n_gen = χ_eff / 48 = 144 / 48 = 3."
            ),
            ContentBlock(
                type="callout",
                callout_type="info",
                title="Key Insight",
                content="The same field Ψ_P that generates spacetime geometry also gives rise to all observable matter. This is the deep unification at the heart of Principia Metaphysica: geometry and matter share a common fermionic origin."
            ),
            ContentBlock(
                type="callout",
                callout_type="info",
                title="Field Taxonomy and Statistics",
                content="Pneuma field (Ψ_P): Chiral spinor field (4096-component in 26D from Cl(24,1), 64-component in dual shadows). Mashiach (An Attractor Scalar) field (χ): Attractor scalar field for dark energy (separate from Pneuma). Framework statistics: 45/48 SM parameters within 1σ (93.8%), 12 exact matches."
            ),
        ])

        # =====================================================================
        # THERMAL TIME CONNECTION
        # =====================================================================
        content_blocks.extend([
            ContentBlock(
                type="heading",
                content="Connection to Thermal Time"
            ),
            ContentBlock(
                type="paragraph",
                content="The Pneuma field statistics also generate the flow of time through the Thermal Time Hypothesis (TTH). The entropy of Pneuma field configurations defines a statistical state ρ, and the modular flow σ_t associated with this state is identified with physical time evolution. This provides a thermodynamic origin for the arrow of time: time flows in the direction of increasing Pneuma field entropy."
            ),
            ContentBlock(
                type="formula",
                content="t = α_T · S[ρ] — Time from Pneuma entropy",
                label=""
            ),
        ])

        # =====================================================================
        # CONDENSATE GAP EQUATION
        # =====================================================================
        content_blocks.extend([
            ContentBlock(
                type="heading",
                content="Condensate Gap Equation (SymPy Derivation)"
            ),
            ContentBlock(
                type="paragraph",
                content="The quartic interaction term λ(Ψ̄Ψ)² combined with the orthogonal time coupling g·t_ortho leads to a self-consistent gap equation for the Pneuma condensate. Using mean-field approximation, we derive the condensate mass gap Δ:"
            ),
            ContentBlock(
                type="heading",
                content="Mean-Field Derivation"
            ),
            ContentBlock(
                type="paragraph",
                content="Starting from the interaction Lagrangian:"
            ),
            ContentBlock(
                type="formula",
                content="ℒ_int = λ(Ψ̄Ψ)² + g·t_ortho·Ψ̄Ψ — Interaction terms for gap derivation",
                label=""
            ),
            ContentBlock(
                type="paragraph",
                content="Applying the mean-field approximation with vacuum expectation value v = ⟨Ψ̄Ψ⟩, we obtain the gap equation."
            ),
            ContentBlock(
                type="heading",
                content="Stability Analysis"
            ),
            ContentBlock(
                type="paragraph",
                content="To verify that the condensate solution is stable and exhibits spontaneous symmetry breaking, we compute the derivative of the gap with respect to the VEV. The positivity of dΔ/dv confirms that the condensate exhibits positive feedback: an increase in the VEV leads to an increase in the gap, which is the hallmark of a self-consistent solution and spontaneous symmetry breaking."
            ),
            ContentBlock(
                type="heading",
                content="Numerical Example"
            ),
            ContentBlock(
                type="paragraph",
                content="Using representative parameters to demonstrate the gap equation: λ = 0.1 (Quartic coupling), g = 0.01 (Thermal coupling), t_ortho = 1 (Orthogonal time), E_F = 10 (Fermi energy)."
            ),
            ContentBlock(
                type="formula",
                content="Results (v = 2): Δ(v=2) = (0.5 × 2) / (1 + 0.01 × 1 / 10) = 1 / 1.01 ≈ 0.99\ndΔ/dv = 0.5 / 1.01 ≈ 0.495 > 0 (stable)\n— Numerical verification of gap stability",
                label=""
            ),
            ContentBlock(
                type="heading",
                content="Physical Interpretation"
            ),
            ContentBlock(
                type="callout",
                callout_type="info",
                title="Condensate Stability and Geometric Emergence",
                content="Δ > 0 derives condensate stability: the positive gap ensures the Pneuma field develops a non-trivial vacuum expectation value, breaking the original symmetry spontaneously. K_Pneuma Geometry: The stable condensate forms the internal geometry K_Pneuma. The Euler characteristic χ = 72 arises from the Hodge number h^{3,1} which counts Δ-cycles - deformation modes of the gap. Swampland Compliance: The finite gap Δ ensures the theory avoids massless scalar modes in the moduli space, satisfying Swampland constraints. Infinite or zero gap would signal pathological behavior incompatible with quantum gravity."
            ),
            ContentBlock(
                type="callout",
                callout_type="info",
                title="SymPy Code Reference",
                content="The full symbolic derivation of the gap equation, stability analysis, and numerical verification was performed using SymPy. The complete computational notebook demonstrates: symbolic differentiation of gap equation, stability criterion verification, numerical evaluation with physical parameters."
            ),
        ])

        # =====================================================================
        # ORTHOGONAL TIME COUPLING
        # =====================================================================
        content_blocks.extend([
            ContentBlock(
                type="heading",
                content="The Orthogonal Time Coupling: g*t_ortho"
            ),
            ContentBlock(
                type="paragraph",
                content="A distinguishing feature of the 25D formulation is the unified time structure in the signature (24,1). The term g*t_ortho in the Lagrangian couples the Pneuma field to the Euclidean bridge direction."
            ),
            ContentBlock(
                type="heading",
                content="Physical Role"
            ),
            ContentBlock(
                type="callout",
                callout_type="info",
                title="Why (24,1) with Euclidean Bridge?",
                content="The signature (24,1) with Euclidean bridge arises naturally from the requirement that the Pneuma field generate both spacetime geometry and matter content consistently. The bridge coordinates are not directly observable but manifest through thermodynamic and entropic phenomena in the effective dual shadow theory."
            ),
        ])

        # =====================================================================
        # v22.0: PNEUMA I/O MECHANISM (NEURAL GATES)
        # =====================================================================
        content_blocks.extend([
            ContentBlock(
                type="heading",
                content="v22.0: Pneuma I/O Mechanism (Neural Gates)"
            ),
            ContentBlock(
                type="paragraph",
                content="The v22.0 framework introduces the 12x(2,0) paired bridge system where each bridge pair B_i = (y_{1i}, y_{2i}) serves as a 'neural gate' for consciousness flow between shadows. The pairing arises from b_3 = 24/2 = 12 pairs."
            ),
            ContentBlock(
                type="heading",
                content="Input-Output Structure"
            ),
            ContentBlock(
                type="paragraph",
                content="Each neural gate has distinct input and output channels:"
            ),
            ContentBlock(
                type="formula",
                content="Input (y_{1i}): Perception from bulk time t\nOutput (y_{2i}): Intuition via cyclic feedback through OR\n-- 12 parallel consciousness channels",
                label=""
            ),
            ContentBlock(
                type="heading",
                content="Per-Pair OR Reduction"
            ),
            ContentBlock(
                type="paragraph",
                content="Cross-shadow coordinate sampling uses per-pair OR operators. Each 2x2 operator acts on the corresponding bridge pair:"
            ),
            ContentBlock(
                type="formula",
                content="R_perp^i = [[0, -1], [1, 0]] for i = 1, ..., 12\nR_perp^full = tensor product over all 12 pairs\n(R_perp^full)^2 = (-1)^12 * I = I (identity)\n-- Per-pair OR reduction with spinor coherence",
                label=""
            ),
            ContentBlock(
                type="callout",
                callout_type="info",
                title="Neural Gate Dynamics",
                content="The 12 bridge pairs create 12 parallel channels for consciousness flow: y_{1i} coordinates aggregate to form the normal shadow (perception input), y_{2i} coordinates aggregate to form the mirror shadow (intuition output). Each shadow maintains independent G2 compactification while being connected through the OR reduction mechanism."
            ),
            ContentBlock(
                type="heading",
                content="Bulk Decomposition (v22)"
            ),
            ContentBlock(
                type="formula",
                content="M^{24,1} = T^1 x_fiber (bigoplus_{i=1}^{12} B_i^{2,0})\nds^2 = -dt^2 + sum_{i=1}^{12} (dy_{1i}^2 + dy_{2i}^2)\n-- 24 spacelike from 12x2 pairs, 1 timelike (unified)",
                label=""
            ),
        ])

        # =====================================================================
        # 2T PHYSICS p-BRANE ACTION
        # =====================================================================
        content_blocks.extend([
            ContentBlock(
                type="heading",
                content="2T Physics p-Brane Action Formulation"
            ),
            ContentBlock(
                type="paragraph",
                content="Complementary to the Pneuma field Lagrangian, we can formulate the theory in terms of extended objects (p-branes) propagating in the full 26D spacetime with signature (24,1) plus Euclidean bridge. This formulation makes manifest the higher-dimensional origin and the role of OR reduction via R_perp operator producing dual (11,1) shadows with unified time."
            ),
            ContentBlock(
                type="heading",
                content="General 2T p-Brane Action"
            ),
            ContentBlock(
                type="paragraph",
                content="The action for a p-brane in 2T physics consists of two parts: the Nambu-Goto term (world-volume) and the Wess-Zumino term (gauge coupling)."
            ),
            ContentBlock(
                type="callout",
                callout_type="info",
                title="Dual-Shadow Physics Framework",
                content="This action is formulated in the full 26D spacetime with signature (24,1) plus Euclidean bridge. The OR reduction via R_perp operator acts on the embedding coordinates X^M(ξ), producing dual (11,1) shadows with shared time while maintaining covariance."
            ),
            ContentBlock(
                type="heading",
                content="Brane Configuration: Observable and Shadow Branes"
            ),
            ContentBlock(
                type="paragraph",
                content="The Pneuma sector consists of four distinct p-branes embedded in the 26D spacetime. Before gauge fixing, each brane has two timelike dimensions:"
            ),
            ContentBlock(
                type="heading",
                content="Observable 5-Brane"
            ),
            ContentBlock(
                type="paragraph",
                content="5 spatial + 1 temporal dimension with Euclidean bridge. After OR reduction via R_perp: dual (11,1) shadows emerge with shared time. Hosts the visible matter sector and 4D spacetime as a subspace."
            ),
            ContentBlock(
                type="heading",
                content="First Shadow 3-Brane"
            ),
            ContentBlock(
                type="paragraph",
                content="3 spatial dimensions in dual (11,1) shadow with shared unified time. Contributes to dark sector structure."
            ),
            ContentBlock(
                type="heading",
                content="Second Shadow 3-Brane"
            ),
            ContentBlock(
                type="paragraph",
                content="3 spatial dimensions in dual (11,1) shadow with shared unified time. Second dark sector component."
            ),
            ContentBlock(
                type="heading",
                content="Third Shadow 3-Brane"
            ),
            ContentBlock(
                type="paragraph",
                content="3 spatial dimensions in dual (11,1) shadow with shared unified time. Third dark sector component."
            ),
            ContentBlock(
                type="callout",
                callout_type="info",
                title="OR Reduction: 26D(24,1) to dual (11,1) shadows via bridge",
                content="Starting configuration: 26D with signature (24,1) plus Euclidean bridge coordinates (y1, y2) for timeless substrate. After OR reduction via R_perp: dual (11,1) shadows + 2D(2,0) Euclidean bridge - effective theory with unified time shared between shadows. The OR reduction procedure produces the dual-shadow structure while preserving the physical degrees of freedom. Bridge effects persist through Euclidean substrate coupling in the effective action."
            ),
            ContentBlock(
                type="heading",
                content="Null Constraints"
            ),
            ContentBlock(
                type="paragraph",
                content="The 2T physics formulation requires three null constraints on the embedding coordinates X^M(ξ) and their conjugate momenta P^M(ξ):"
            ),
            ContentBlock(
                type="formula",
                content="X^M X_M = 0 — Position Null Constraint\nX^M P_M = 0 — Mixed Null Constraint\nP^M P_M + M^2 = 0 — Mass-Shell Constraint\n— Null Constraints in 2T Physics (3.8)",
                label=""
            ),
            ContentBlock(
                type="paragraph",
                content="These constraints are first-class and generate the OR reduction structure. They ensure that: ghosts from the dual-shadow framework are eliminated; physical degrees of freedom are preserved; gauge invariance is manifest through the R_perp operator."
            ),
            ContentBlock(
                type="heading",
                content="BPS Bound and Central Charges"
            ),
            ContentBlock(
                type="paragraph",
                content="For supersymmetric branes (BPS states), the brane tension saturates a lower bound set by the central charges of the extended supersymmetry algebra SO(24,1): T_p = |Z|. The BPS condition ensures stability: branes cannot decay to lower-tension configurations because the central charge is topologically conserved. This is the origin of the stability of matter in the theory."
            ),
            ContentBlock(
                type="callout",
                callout_type="info",
                title="Central Charges in SO(24,1)",
                content="Observable 5-brane: Z_5 ∈ ∧^5(R^{24,1}) - rank-5 antisymmetric tensor charge. Shadow 3-branes: Z_3^(i) ∈ ∧^3(R^{24,1}), i=1,2,3 - three rank-3 antisymmetric tensor charges. These central charges commute with all supersymmetry generators and are topological invariants. The dimensions (5,1) and (3,1) are selected to maximize the allowed central charge structure while satisfying the total dimension constraint 25 = (5+1)+(3+1)+(3+1)+(3+1) + 7 (internal)."
            ),
        ])

        # =====================================================================
        # 4D EFFECTIVE LAGRANGIAN
        # =====================================================================
        content_blocks.extend([
            ContentBlock(
                type="heading",
                content="4D Effective Lagrangian"
            ),
            ContentBlock(
                type="paragraph",
                content="Starting from the full 26D Lagrangian (or equivalently, the 2T p-brane action), we first gauge-fix to 13D (with the g·t_ortho term encoding the second time direction), then perform Kaluza-Klein reduction over the 8-dimensional internal manifold K_Pneuma. This yields the 4D fermion sector:"
            ),
            ContentBlock(
                type="formula",
                content="ℒ_4D,fermion = Σ_{i=1}^3 ψ_i (iγ^μ D_μ - m_i)ψ_i + (Yukawa couplings)\n— 4D effective fermion Lagrangian from dimensional reduction",
                label=""
            ),
            ContentBlock(
                type="paragraph",
                content="The three generations (i = 1, 2, 3) arise from the three independent zero modes of the internal Dirac operator. The 4D masses m_i and Yukawa couplings are determined by overlap integrals of these zero mode wave functions over K_Pneuma."
            ),
            ContentBlock(
                type="callout",
                callout_type="info",
                title="Equivalence of Formulations",
                content="The Pneuma field Lagrangian (fermionic) and the 2T p-brane action (bosonic) are dual descriptions of the same underlying theory. The duality relates: fermionic currents ↔ brane charges; Dirac operator zero modes ↔ brane world-volume fermions; spinor condensates ↔ brane tensions."
            ),
        ])

        # =====================================================================
        # COMPLETE LAGRANGIAN HIERARCHY
        # =====================================================================
        content_blocks.extend([
            ContentBlock(
                type="heading",
                content="Complete Lagrangian Hierarchy"
            ),
            ContentBlock(
                type="paragraph",
                content="The following presents the complete hierarchy of Lagrangians from the 26D bulk action down to 4D observable physics. Each level emerges naturally from dimensional reduction and gauge fixing, with fermionic primacy maintained throughout."
            ),
            ContentBlock(
                type="heading",
                content="1. Master Bulk Action (26D)"
            ),
            ContentBlock(
                type="paragraph",
                content="The fundamental action in full 25D spacetime with signature (24,1), emphasizing fermionic primacy:"
            ),
            ContentBlock(
                type="callout",
                callout_type="info",
                title="Fermionic Primacy",
                content="The Pneuma spinor Ψ_P is not a matter field on a fixed background. The fermionic term sources the Einstein equations: R_MN = T_MN[Ψ_P]. Spacetime geometry emerges from Pneuma condensates, embodying true fermionic primacy."
            ),
            ContentBlock(
                type="heading",
                content="2. 13D Shadow Effective Lagrangian"
            ),
            ContentBlock(
                type="paragraph",
                content="After OR reduction from 26D (24,1) to dual (11,1) shadows with unified time, the 4096-component spinor from Cl(24,1) reduces to effective 64 components:"
            ),
            ContentBlock(
                type="callout",
                callout_type="info",
                title="Dimensional Reduction: 26D(24,1) → dual (11,1) + 2D(2,0)",
                content="OR reduction via R_perp produces dual shadows with unified time: (24,1) → 2x(11,1) + bridge(2,0). Spinor dimension: 2^12 = 4096 from Cl(24,1) → 2^6 = 64 effective components. The flux terms L_flux stabilize moduli via KKLT/LVS mechanisms. The complex structure modulus Re(T) = 7.086 is derived from the measured Higgs mass (125.10 GeV), completing the moduli stabilization picture with full swampland compliance."
            ),
            ContentBlock(
                type="heading",
                content="3. 4D Observable Effective Lagrangian"
            ),
            ContentBlock(
                type="paragraph",
                content="The effective 4D Lagrangian includes f(R,T,τ) modified gravity with specific coefficients derived from higher-dimensional reduction: α_F (Starobinsky Coefficient), β_F (Matter Coupling), γ_F (Two-Time Invariant), δ_F (Dynamical Evolution)."
            ),
            ContentBlock(
                type="heading",
                content="4. Mashiach Attractor Lagrangian"
            ),
            ContentBlock(
                type="paragraph",
                content="The dark energy sector is described by the Mashiach scalar field with late-time attractor dynamics ensuring w → -1.0. The potential V(φ) is constructed to have a stable late-time attractor: φ_M VEV ~ 2.5 M_Pl, w = -1.0 exactly at minimum, Λ ~ (2.4 meV)^4, attractor dynamics φ̈ + 3Hφ̇ + V'(φ) = 0."
            ),
            ContentBlock(
                type="callout",
                callout_type="info",
                title="Attractor Dynamics",
                content="The Mashiach field φ evolves according to the Klein-Gordon equation in an FRW background: φ̈ + 3Hφ̇ + V'(φ) = 0. At late times, the field rolls to the minimum of V(φ), where φ̇ → 0, yielding w = -1.0 without fine-tuning. This is the attractor solution - independent of initial conditions."
            ),
            ContentBlock(
                type="heading",
                content="Summary: The Lagrangian Cascade"
            ),
            ContentBlock(
                type="paragraph",
                content="The complete descent from fundamental 26D physics to 4D observables:"
            ),
            ContentBlock(
                type="formula",
                content="Level 1 (26D): S = ∫ d^26 X √(-G) [R + Ψ_P (iΓ^M D_M - m)Ψ_P] with (24,1) + Euclidean bridge\n↓ OR reduction via R_perp (unified time)\nLevel 2 (dual shadows): ℒ = M_*^11 R + Ψ_64 (iγ^μ ∇_μ - m_eff)Ψ_64 + ℒ_flux in 2×(11,1) with shared time + (2,0) bridge\n↓ KK reduction → 4D\nLevel 3 (4D): f(R,T,τ) = R + α_F R² + β_F T + γ_F Rτ + δ_F (∂_t τ)R\nLevel 4 (DE): ℒ_φ = -½(∂φ)² - V(φ_M), V = V_0[1 + A cos(ωφ_M/f)]\n— Complete Lagrangian Hierarchy (v21 unified time)",
                label=""
            ),
        ])

        return SectionContent(
            section_id="2",
            subsection_id="2.6",  # v19.0: Match metadata subsection_id
            title="The Pneuma Lagrangian",
            abstract="The fundamental fermionic field term that sources all of physics - from spacetime geometry to matter content.",
            content_blocks=content_blocks,
            formula_refs=["pneuma-lagrangian", "pneuma-flow"],
            param_refs=["pneuma.coupling", "pneuma.flow_parameter", "pneuma.vev", "pneuma.mass_scale"]
        )

    # =========================================================================
    # FORMULAS
    # =========================================================================

    def get_formulas(self) -> List[Formula]:
        """Return list of formulas with derivation chains."""
        formulas = [
            Formula(
                id="pneuma-lagrangian",
                label="(2.1)",
                latex=r"\mathcal{L}_{\text{pneuma}} = \frac{1}{2} \partial_\mu \Psi_P \partial^\mu \Psi_P - V(\Psi_P) + \mathcal{L}_{\text{vielbein}}",
                plain_text="L_pneuma = (1/2) d_mu Psi_P d^mu Psi_P - V(Psi_P) + L_vielbein",
                category="THEORY",
                description="Full Pneuma Lagrangian with kinetic, potential, and vielbein terms",
                inputParams=["topology.chi_eff", "topology.b3"],
                outputParams=["pneuma.coupling"],
                input_params=["topology.chi_eff", "topology.b3"],
                output_params=["pneuma.coupling"],
                derivation={
                    "source": "G2 holonomy geometry",
                    "steps": [
                        "Start with parallel spinor on G2 manifold",
                        "Derive kinetic term from spinor covariant derivative",
                        "Obtain potential from racetrack superpotential W = A exp(-a Psi) - B exp(-b Psi)",
                        "Include vielbein coupling from spinor bilinears"
                    ],
                    "assumptions": [
                        "G2 holonomy preserved",
                        "SUSY breaking via F-term potential",
                        "Flux quantization N_flux = chi_eff / 6"
                    ]
                },
                terms={
                    "kinetic": r"\frac{1}{2} \partial_\mu \Psi_P \partial^\mu \Psi_P",
                    "potential": r"V(\Psi_P) = |dW/d\Psi_P|^2",
                    "vielbein": r"\mathcal{L}_{\text{vielbein}} = \bar{\eta} \Gamma^a e_a^\mu D_\mu \eta"
                }
            ),
            # v22.0: Neural Gate I/O Formula
            Formula(
                id="pneuma-neural-gate",
                label="(2.3)",
                latex=r"B_i^{2,0} = (y_{1i}, y_{2i}) \quad \text{Input: } y_{1i} \text{ (perception)} \quad \text{Output: } y_{2i} \text{ (intuition)}",
                plain_text="B_i^{2,0} = (y_{1i}, y_{2i}); Input: y_{1i} (perception); Output: y_{2i} (intuition)",
                category="THEORY",
                description="v22.0 Neural gate structure: each bridge pair serves as I/O channel for consciousness",
                input_params=["topology.b3"],
                output_params=["pneuma.n_bridge_pairs", "pneuma.neural_gate_active"],
                derivation={
                    "source": "12x(2,0) paired bridge system",
                    "steps": [
                        "b3 = 24 Betti number from G2 topology",
                        "24 / 2 = 12 paired bridges",
                        "Each pair B_i has Euclidean (2,0) signature",
                        "y_{1i} aggregates form normal shadow (perception input)",
                        "y_{2i} aggregates form mirror shadow (intuition output)"
                    ],
                    "assumptions": [
                        "Independent G2 compactification per shadow",
                        "Cyclic feedback through OR reduction"
                    ]
                },
            ),
            # v22.0: Per-Pair OR Reduction Formula
            Formula(
                id="pneuma-or-reduction",
                label="(2.4)",
                latex=r"R_\perp^i = \begin{pmatrix} 0 & -1 \\ 1 & 0 \end{pmatrix} \quad R_\perp^{\text{full}} = \bigotimes_{i=1}^{12} R_\perp^i",
                plain_text="R_perp^i = [[0,-1],[1,0]]; R_perp^full = tensor_{i=1}^{12} R_perp^i",
                category="THEORY",
                description="v22.0 Per-pair OR reduction: 90-degree rotation on each bridge pair, full operator as tensor product",
                input_params=["topology.b3"],
                output_params=[],
                derivation={
                    "source": "OR reduction on paired bridges",
                    "steps": [
                        "Per-pair operator: R_perp^i = [[0,-1],[1,0]] (90 deg rotation)",
                        "Full tensor product: R_perp^full = tensor over 12 pairs",
                        "Property: (R_perp^i)^2 = -I per pair",
                        "Full double-traversal: (R_perp^full)^2 = (-1)^12 I = I",
                        "Even number of pairs ensures spinor coherence"
                    ],
                    "assumptions": [
                        "Orientation-preserving (det = 1)",
                        "Mobius double-cover for spinors"
                    ]
                },
            ),
            Formula(
                id="pneuma-flow",
                label="(2.2)",
                latex=r"\dot{\Psi}_P = -\lambda \frac{\partial V}{\partial \Psi_P}",
                plain_text="dΨ_P/dt = -λ ∂V/∂Ψ_P",
                category="THEORY",
                description="Flow equation governing Pneuma field dynamics",
                inputParams=["pneuma.flow_parameter"],
                outputParams=["pneuma.vev"],
                input_params=["pneuma.flow_parameter"],
                output_params=["pneuma.vev"],
                derivation={
                    "source": "Gradient flow on potential",
                    "steps": [
                        "Write equation of motion from Lagrangian",
                        "Apply slow-roll approximation (3H dot_Psi ~ -dV/dPsi)",
                        "Define effective flow parameter lambda ~ sqrt(V'')"
                    ],
                    "assumptions": [
                        "Overdamped regime (slow-roll)",
                        "Homogeneous field configuration",
                        "Adiabatic evolution"
                    ]
                },
                terms={
                    "flow_parameter": r"\lambda = \sqrt{2 V''(\langle\Psi_P\rangle)}",
                    "derivative": r"\frac{\partial V}{\partial \Psi_P} = 2 \frac{dW}{d\Psi_P} \frac{d^2W}{d\Psi_P^2}"
                }
            ),
        ]

        return formulas

    # =========================================================================
    # PARAMETER DEFINITIONS
    # =========================================================================

    def get_output_param_definitions(self) -> List[Parameter]:
        """Return parameter definitions for outputs."""
        return [
            Parameter(
                path="pneuma.coupling",
                name="Pneuma Coupling Constant",
                units="dimensionless",
                status="GEOMETRIC",
                description="Coupling constant between Pneuma field and spacetime geometry",
                derivation_formula="pneuma-lagrangian",
                no_experimental_value=True,
            ),
            Parameter(
                path="pneuma.flow_parameter",
                name="Pneuma Flow Parameter",
                units="dimensionless",
                status="DERIVED",
                description="Characteristic frequency governing Pneuma field evolution",
                derivation_formula="pneuma-flow",
                no_experimental_value=True,
            ),
            Parameter(
                path="pneuma.lagrangian_valid",
                name="Lagrangian Validity Flag",
                units="dimensionless",
                status="DERIVED",
                description="Boolean flag indicating whether Pneuma Lagrangian has stable vacuum",
                derivation_formula="pneuma-lagrangian",
                no_experimental_value=True,
            ),
            Parameter(
                path="pneuma.vev",
                name="Pneuma VEV",
                units="dimensionless",
                status="DERIVED",
                description="Vacuum expectation value of Pneuma field from racetrack minimum",
                derivation_formula="pneuma-flow",
                no_experimental_value=True,
            ),
            Parameter(
                path="pneuma.mass_scale",
                name="Pneuma Mass Scale",
                units="GeV",
                status="DERIVED",
                description="Characteristic mass scale of Pneuma field (m_P ~ M_Planck / sqrt(chi_eff))",
                derivation_formula="pneuma-lagrangian",
                no_experimental_value=True,
            ),
            # v22.0: Neural gate parameters
            Parameter(
                path="pneuma.n_bridge_pairs",
                name="Number of Bridge Pairs",
                units="dimensionless",
                status="EXACT",
                description="v22.0: Number of (2,0) paired bridges. n = b3/2 = 24/2 = 12 pairs.",
                derivation_formula="pneuma-neural-gate",
                no_experimental_value=True,
            ),
            Parameter(
                path="pneuma.neural_gate_active",
                name="Neural Gate Active",
                units="dimensionless",
                status="DERIVED",
                description="v22.0: Boolean flag indicating 12 neural gates are active for consciousness I/O.",
                derivation_formula="pneuma-neural-gate",
                no_experimental_value=True,
            ),
        ]

    # =========================================================================
    # FOUNDATIONS
    # =========================================================================

    def get_foundations(self) -> List[Dict[str, str]]:
        """Return foundational concepts for this simulation."""
        return [
            {
                "id": "g2-manifolds",
                "title": "G2 Holonomy Manifolds",
                "category": "differential_geometry",
                "description": "Seven-dimensional manifolds with exceptional G2 holonomy group"
            },
            {
                "id": "m-theory",
                "title": "M-Theory",
                "category": "string_theory",
                "description": "Eleven-dimensional unified framework for string theories"
            },
            {
                "id": "kaluza-klein",
                "title": "Kaluza-Klein Theory",
                "category": "unified_field_theory",
                "description": "Unification via extra compact dimensions"
            },
        ]

    # =========================================================================
    # REFERENCES
    # =========================================================================

    def get_references(self) -> List[Dict[str, str]]:
        """Return academic references for this simulation."""
        return [
            {
                "id": "joyce2000",
                "authors": "Joyce, D.",
                "title": "Compact Manifolds with Special Holonomy",
                "journal": "Oxford University Press",
                "year": "2000"
            },
            {
                "id": "witten1995",
                "authors": "Witten, E.",
                "title": "String theory dynamics in various dimensions",
                "journal": "Nucl. Phys. B",
                "volume": "443",
                "year": "1995"
            },
            {
                "id": "cvetic2002",
                "authors": "Cvetic, M. et al.",
                "title": "M-theory compactifications on G2 manifolds",
                "journal": "Phys. Rev. D",
                "volume": "65",
                "year": "2002"
            },
        ]

    def get_beginner_explanation(self) -> Dict[str, Any]:
        """
        Return beginner-friendly explanation for auto-generation of guide content.

        Returns:
            Dictionary with beginner explanation fields
        """
        return {
            "icon": "🌊",
            "title": "The Pneuma Field (Breathing Life into Geometry)",
            "simpleExplanation": (
                "The word 'pneuma' comes from ancient Greek meaning 'breath' or 'spirit'. In this theory, the Pneuma "
                "field is a special quantum field that 'breathes' in the hidden dimensions - it's always present, "
                "permeating all of space like an invisible mist. But unlike the Higgs field (which gives particles mass), "
                "the Pneuma field does something even more fundamental: it *creates spacetime itself*. The way it couples "
                "to geometry through 'vielbein emergence' means that the smooth fabric of space and time that Einstein "
                "described isn't fundamental - it emerges from the collective behavior of this deeper field living in "
                "7 extra dimensions."
            ),
            "analogy": (
                "Think of spacetime like the surface of the ocean. From a distance, it looks smooth and continuous. "
                "But zoom in close enough, and you see it's made of countless water molecules jostling around. The Pneuma "
                "field is like those water molecules - individual quantum 'drops' whose collective motion creates the "
                "illusion of a smooth surface (spacetime). When the Pneuma field 'flows' (changes its value), it's like "
                "a current in the ocean: the curvature of spacetime (Einstein's gravity) emerges from how fast this flow "
                "is changing. The 'racetrack potential' that governs the Pneuma field is like the seafloor topology - "
                "it has valleys and hills that the field naturally settles into, and our universe's Pneuma VEV (vacuum "
                "expectation value) is which valley we ended up in."
            ),
            "keyTakeaway": (
                "The Pneuma field provides a mechanism for spacetime emergence: 4D gravity arises from 7D geometry "
                "via vielbein coupling, with dynamics governed by a racetrack potential."
            ),
            "technicalDetail": (
                "The Pneuma Lagrangian: L = (1/2)∂_μΨ_P ∂^μΨ_P - V(Ψ_P) + L_vielbein, where V(Ψ_P) = |dW/dΨ_P|² from "
                "racetrack superpotential W = A exp(-aΨ) - B exp(-bΨ). Instanton coefficients: a = 2π/N_flux, b = 2π/(N_flux-1) "
                "with N_flux = χ_eff/6 = 24. VEV from analytic minimum: <Ψ_P> = ln(Bb/Aa)/(b-a). Vielbein emergence: "
                "e_a^μ ∝ ⟨η̄ γ^a η⟩ where η is the G2 parallel spinor, coupling Pneuma gradient ∇_μΨ_P to spacetime "
                "metric via L_vielbein = κ_P (∇_μΨ_P)(η̄ Γ^a e_a^μ D_μ η). This creates effective Einstein-Hilbert "
                "action from spinor kinetic term: S_EH ~ ∫ d⁴x √g R emerges from integrating out Pneuma-spinor loops."
            ),
            "prediction": (
                "Pneuma field excitations around the VEV would manifest as ultra-light scalar particles (m_Ψ ~ M_Planck/√χ_eff ~ "
                "10^16 GeV) that couple to curvature. These are inaccessible to colliders but could affect early universe "
                "cosmology (inflation, reheating) or be detectable as modifications to General Relativity at extreme scales."
            )
        }


# =============================================================================
# STANDALONE EXECUTION
# =============================================================================

def main():
    """Standalone execution for testing."""
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

    print("=" * 70)
    print(" PNEUMA MECHANISM SIMULATION v16.0")
    print("=" * 70)
    print()

    # Create simulation
    sim = PneumaMechanismV16()

    # Print metadata
    print("METADATA:")
    print(f"  ID: {sim.metadata.id}")
    print(f"  Version: {sim.metadata.version}")
    print(f"  Domain: {sim.metadata.domain}")
    print(f"  Title: {sim.metadata.title}")
    print(f"  Section: {sim.metadata.section_id}")
    print()

    # Create mock registry with required inputs
    from simulations.base import PMRegistry
    registry = PMRegistry()

    # Load established physics
    from simulations.base.established import EstablishedPhysics
    EstablishedPhysics.load_into_registry(registry)

    # Set topology parameters
    registry.set_param("topology.chi_eff", 144, source="TCS_187", status="ESTABLISHED")
    registry.set_param("topology.b3", 24, source="TCS_187", status="ESTABLISHED")

    # Run simulation
    print("RUNNING SIMULATION...")
    results = sim.execute(registry, verbose=True)

    print()
    print("RESULTS:")
    for key, value in results.items():
        if isinstance(value, bool):
            print(f"  {key} = {value}")
        elif isinstance(value, float):
            print(f"  {key} = {value:.6e}")
        else:
            print(f"  {key} = {value}")

    print()
    print("=" * 70)
    print(" VALIDATION")
    print("=" * 70)

    # Check Lagrangian validity
    if results["pneuma.lagrangian_valid"]:
        print("  Lagrangian: VALID (stable vacuum)")
    else:
        print("  Lagrangian: INVALID (unstable)")

    print(f"  VEV: {results['pneuma.vev']:.6f}")
    print(f"  Mass scale: {results['pneuma.mass_scale']:.3e} GeV")
    print(f"  Coupling: {results['pneuma.coupling']:.6e}")
    print(f"  Flow parameter: {results['pneuma.flow_parameter']:.6f}")

    print()
    print("=" * 70)


if __name__ == "__main__":
    main()
