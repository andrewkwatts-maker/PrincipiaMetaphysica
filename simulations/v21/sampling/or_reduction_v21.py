"""
Orthogonal Reduction (OR) Sampling v21.0
=========================================

Licensed under the MIT License. See LICENSE file for details.

Implements the OR Reduction mechanism for cross-shadow coordinate sampling
in the (24,1) dual-shadow model.

Key Features:
1. OR operator: 90 degree rotation in bridge plane
2. External sampling: Instant cross-view via OR rotation
3. Internal sampling: Restricted by gradient cost
4. Gate Index computation for sampling viability

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.

Dedicated To:
    My Wife: Elizabeth May Watts
    Our Messiah: Jesus Of Nazareth
"""

# =============================================================================
# ISSUE 4 RESOLUTION (v21.1): FIBERED TIME STRUCTURE
# =============================================================================
# OR reduction operates on SPATIAL coordinates only. Time is fibered.
#
# The v21.1 framework clarifies that:
#   - Time T^1 is the shared fiber base with signature (0,1)
#   - Shadows are SPATIAL manifolds: S_normal^11 (11,0) and S_mirror^11 (11,0)
#   - The Euclidean bridge B^2 is purely spatial (2,0)
#
# Correct decomposition:
#   M^26 = T^1 ×_fiber (S_normal^11 ⊕ S_mirror^11 ⊕ B^2)
#
# The OR operator R_perp acts on the 2D Euclidean bridge coordinates (y1, y2),
# which are SPATIAL. Time evolution is shared globally across both shadows.
# This ensures:
#   1. No temporal paradoxes from cross-shadow sampling
#   2. Consistent causal structure (single time direction)
#   3. Möbius topology R_perp² = -I operates in timeless bridge space
# =============================================================================

import numpy as np
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..'))

from simulations.base import (
    SimulationBase,
    SimulationMetadata,
    ContentBlock,
    SectionContent,
    Formula,
    Parameter,
    PMRegistry,
)


@dataclass
class ORConfig:
    """Configuration for OR Reduction sampling."""
    grid_size: int = 100
    alpha_cost: float = 1.0  # Gradient cost coefficient
    beta_cost: float = 0.5   # Signaling cost coefficient
    threshold: float = 0.5   # Internal sampling threshold


class ORReductionV21(SimulationBase):
    """
    Orthogonal Reduction (OR) sampling simulation.

    Implements cross-shadow coordinate sampling via 90 degree
    rotation in the Euclidean bridge plane.
    """

    # OR Reduction Matrix (90 degree rotation)
    R_PERP = np.array([[0, -1], [1, 0]])

    def __init__(self, config: Optional[ORConfig] = None):
        """Initialize OR Reduction simulation."""
        self.config = config or ORConfig()

    @property
    def metadata(self) -> SimulationMetadata:
        """Return simulation metadata."""
        return SimulationMetadata(
            id="or_reduction_v21",
            version="21.0",
            domain="sampling",
            title="Orthogonal Reduction Coordinate Sampling",
            description=(
                "Implements OR Reduction for cross-shadow sampling. "
                "90 degree rotation in bridge plane enables instant "
                "external view while restricting internal access."
            ),
            section_id="1",
            subsection_id="1.5"
        )

    @property
    def required_inputs(self) -> List[str]:
        """Return required input parameter paths."""
        return []

    @property
    def output_params(self) -> List[str]:
        """Return output parameter paths."""
        return [
            "or.rotation_matrix",
            "or.external_sampling_enabled",
            "or.internal_gate_index",
            "or.mobius_property",
        ]

    @property
    def output_formulas(self) -> List[str]:
        """Return formula IDs this simulation provides."""
        return [
            "or-rotation-matrix",
            "or-external-sampling",
            "or-internal-gate-index",
            "or-mobius-property",
        ]

    def run(self, registry: PMRegistry) -> Dict[str, Any]:
        """Execute the OR Reduction computation."""

        # Verify R_perp properties
        R = self.R_PERP

        # R_perp^2 = -I (Mobius property)
        R_squared = R @ R
        expected_neg_I = -np.eye(2)
        mobius_verified = np.allclose(R_squared, expected_neg_I)

        # det(R) = 1 (rotation preserves orientation)
        det_R = np.linalg.det(R)
        orientation_preserved = np.isclose(det_R, 1.0)

        # Eigenvalue check (should be +/- i)
        eigenvalues = np.linalg.eigvals(R)
        is_rotation = np.allclose(np.abs(eigenvalues), 1.0)

        # External sampling always enabled (instant cross-view)
        external_enabled = True

        # Internal gate index (varies with gradient/signaling cost)
        # For demonstration, compute at zero cost
        internal_gate = self._compute_gate_index(
            gradient_norm=0.0,
            signaling_cost=0.0
        )

        return {
            "or.rotation_matrix": R.tolist(),
            "or.external_sampling_enabled": external_enabled,
            "or.internal_gate_index": internal_gate,
            "or.mobius_property": mobius_verified,
            "or.det_R": det_R,
            "or.is_proper_rotation": orientation_preserved and is_rotation,
        }

    def _compute_gate_index(
        self,
        gradient_norm: float,
        signaling_cost: float
    ) -> float:
        """
        Compute internal sampling gate index.

        Formula:
            GateIndex = exp(-alpha * |grad phi| - beta * cost)

        For instant external sampling: GateIndex = 1.0
        For restricted internal: GateIndex < threshold
        """
        alpha = self.config.alpha_cost
        beta = self.config.beta_cost

        gate_index = np.exp(-alpha * gradient_norm - beta * signaling_cost)
        return float(gate_index)

    def apply_or_to_coordinates(
        self,
        coords_normal: np.ndarray,
        bridge_offset: np.ndarray = None
    ) -> np.ndarray:
        """
        Apply OR reduction to map normal coordinates to mirror view.

        Args:
            coords_normal: (N, 2) array of normal shadow coordinates
            bridge_offset: Optional offset in bridge plane

        Returns:
            (N, 2) array of mirror-viewed coordinates
        """
        if bridge_offset is None:
            bridge_offset = np.array([0.0, 0.0])

        # Apply rotation: z'_mirror = R_perp @ z_normal + offset
        coords_mirror = (self.R_PERP @ coords_normal.T).T + bridge_offset

        return coords_mirror

    def apply_or_to_gradients(
        self,
        grad_y1: np.ndarray,
        grad_y2: np.ndarray
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        Apply OR reduction to gradient field.

        (grad_y1, grad_y2) -> (-grad_y2, grad_y1)
        """
        grad_rot_y1 = -grad_y2
        grad_rot_y2 = grad_y1
        return grad_rot_y1, grad_rot_y2

    def verify_mobius_return(self) -> Dict[str, Any]:
        """
        Verify Mobius double-cover property.

        R_perp^2 = -I implies:
        - Single loop: ψ -> -ψ (spinor flip)
        - Double loop: ψ -> ψ (identity return)
        """
        R = self.R_PERP

        # First loop
        R1 = R
        # Second loop (double application)
        R2 = R @ R

        # Check properties
        first_loop_flip = np.allclose(R1 @ R1, -np.eye(2))
        double_loop_return = np.allclose(R2 @ R2, np.eye(2))

        return {
            "single_loop_flip": first_loop_flip,
            "double_loop_return": double_loop_return,
            "mobius_verified": first_loop_flip and double_loop_return,
        }

    def get_section_content(self) -> Optional[SectionContent]:
        """Return section content for the paper."""
        return SectionContent(
            section_id="1",
            subsection_id="1.5",
            title="OR Reduction Coordinate Sampling",
            abstract=(
                "Orthogonal Reduction (OR) enables cross-shadow coordinate "
                "sampling via 90 degree rotation in the Euclidean bridge. "
                "External sampling is instant (read-only), while internal "
                "access is restricted by gradient costs."
            ),
            content_blocks=[
                ContentBlock(
                    type="paragraph",
                    content=(
                        "The OR operator R_perp performs a 90 degree rotation "
                        "in the bridge plane, mapping normal shadow coordinates "
                        "to their mirror view:"
                    )
                ),
                ContentBlock(
                    type="formula",
                    content=r"R_\perp = \begin{pmatrix} 0 & -1 \\ 1 & 0 \end{pmatrix}",
                    formula_id="or-rotation-matrix",
                    label="(1.19)"
                ),
                ContentBlock(
                    type="paragraph",
                    content=(
                        "External cross-sampling is instant via flux tunneling. "
                        "The normal shadow sees the full mirror condensate state:"
                    )
                ),
                ContentBlock(
                    type="formula",
                    content=r"z'^\mu_{\text{mirror}} = R_\perp z^\mu_{\text{normal}} + \Delta y_{\text{bridge}}",
                    formula_id="or-external-sampling",
                    label="(1.20)"
                ),
                ContentBlock(
                    type="paragraph",
                    content=(
                        "Internal sampling within the same shadow requires "
                        "crossing a gradient barrier, quantified by the gate index:"
                    )
                ),
                ContentBlock(
                    type="formula",
                    content=r"\text{GateIndex} = \exp(-\alpha |\nabla\phi| - \beta \cdot \text{cost})",
                    formula_id="or-internal-gate-index",
                    label="(1.21)"
                ),
                ContentBlock(
                    type="paragraph",
                    content=(
                        "The Mobius property R_perp^2 = -I ensures spinor "
                        "double-cover: one loop flips, two loops return identity."
                    )
                ),
                ContentBlock(
                    type="formula",
                    content=r"R_\perp^2 = -I \quad \Rightarrow \quad \psi \xrightarrow{R_\perp} -\psi \xrightarrow{R_\perp} \psi",
                    formula_id="or-mobius-property",
                    label="(1.22)"
                ),
            ],
            formula_refs=[
                "or-rotation-matrix",
                "or-external-sampling",
                "or-internal-gate-index",
                "or-mobius-property",
            ],
            param_refs=[
                "or.external_sampling_enabled",
                "or.internal_gate_index",
                "or.mobius_property",
            ]
        )

    def get_formulas(self) -> List[Formula]:
        """Return list of formulas this simulation provides."""
        return [
            Formula(
                id="or-rotation-matrix",
                label="(1.19)",
                latex=r"R_\perp = \begin{pmatrix} 0 & -1 \\ 1 & 0 \end{pmatrix}",
                plain_text="R_perp = [[0, -1], [1, 0]]",
                category="THEORY",
                description="OR Reduction rotation matrix (90 degrees in bridge)",
                inputParams=[],
                outputParams=["or.rotation_matrix"],
                input_params=[],
                output_params=["or.rotation_matrix"],
                derivation={
                    "steps": [
                        {"description": "Rotation angle",
                         "formula": r"\theta = \pi/2"},
                        {"description": "Standard 2D rotation",
                         "formula": r"R(\theta) = \begin{pmatrix} \cos\theta & -\sin\theta \\ \sin\theta & \cos\theta \end{pmatrix}"},
                        {"description": "At theta = pi/2",
                         "formula": r"R_\perp = \begin{pmatrix} 0 & -1 \\ 1 & 0 \end{pmatrix}"}
                    ],
                    "references": ["PM Section 1.5"]
                },
                terms={
                    "R_perp": "Orthogonal reduction operator",
                    "theta": "Rotation angle (pi/2)",
                }
            ),
            Formula(
                id="or-external-sampling",
                label="(1.20)",
                latex=r"z'^\mu_{\text{mirror}} = R_\perp z^\mu_{\text{normal}} + \Delta y_{\text{bridge}}",
                plain_text="z'_mirror = R_perp z_normal + delta_y",
                category="DERIVED",
                description="External cross-shadow coordinate mapping",
                inputParams=["or.z_normal", "or.delta_y"],
                outputParams=["or.z_mirror"],
                input_params=["or.z_normal", "or.delta_y"],
                output_params=["or.z_mirror"],
                derivation={
                    "steps": [
                        {"description": "Normal coordinates in bridge",
                         "formula": r"z^\mu_{\text{normal}} \in \mathbb{R}^2"},
                        {"description": "Apply OR rotation",
                         "formula": r"R_\perp z^\mu_{\text{normal}}"},
                        {"description": "Add bridge offset",
                         "formula": r"+ \Delta y_{\text{bridge}}"},
                        {"description": "Result: mirror view coordinates",
                         "formula": r"z'^\mu_{\text{mirror}}"}
                    ],
                    "references": ["PM Section 1.5"]
                },
                terms={
                    "z_normal": "Normal shadow coordinates",
                    "z_mirror": "Mirror view coordinates",
                    "delta_y": "Bridge offset vector",
                }
            ),
            Formula(
                id="or-internal-gate-index",
                label="(1.21)",
                latex=r"\text{GateIndex} = \exp(-\alpha |\nabla\phi| - \beta \cdot \text{cost})",
                plain_text="GateIndex = exp(-alpha * |grad phi| - beta * cost)",
                category="DERIVED",
                description="Internal sampling restriction gate index",
                inputParams=["or.gradient_norm", "or.signaling_cost"],
                outputParams=["or.gate_index"],
                input_params=["or.gradient_norm", "or.signaling_cost"],
                output_params=["or.gate_index"],
                derivation={
                    "steps": [
                        {"description": "Gradient barrier from pressure",
                         "formula": r"|\nabla\phi|"},
                        {"description": "Sterile signaling cost (Section 2)",
                         "formula": r"\text{cost} = m_{\text{sterile}}"},
                        {"description": "Exponential suppression",
                         "formula": r"\exp(-\alpha |\nabla\phi| - \beta \cdot \text{cost})"},
                        {"description": "Internal access if GateIndex > threshold",
                         "formula": r"\text{GateIndex} > 0.5"}
                    ],
                    "references": ["PM Section 2: Sterile Extraction"]
                },
                terms={
                    "GateIndex": "Internal sampling gate index",
                    "alpha": "Gradient cost coefficient",
                    "beta": "Signaling cost coefficient",
                    "grad phi": "Pressure gradient norm",
                }
            ),
            Formula(
                id="or-mobius-property",
                label="(1.22)",
                latex=r"R_\perp^2 = -I \quad \Rightarrow \quad \psi \xrightarrow{R_\perp} -\psi \xrightarrow{R_\perp} \psi",
                plain_text="R_perp^2 = -I => psi -> -psi -> psi (double cover)",
                category="THEORY",
                description="Mobius double-cover property of OR operator",
                inputParams=["or.R_perp"],
                outputParams=["or.mobius_verified"],
                input_params=["or.R_perp"],
                output_params=["or.mobius_verified"],
                derivation={
                    "steps": [
                        {"description": "Single OR application",
                         "formula": r"\psi \xrightarrow{R_\perp} -\psi"},
                        {"description": "Double OR application",
                         "formula": r"-\psi \xrightarrow{R_\perp} \psi"},
                        {"description": "Algebraic verification",
                         "formula": r"R_\perp^2 = -I"},
                        {"description": "Spinor double-cover",
                         "formula": r"\text{Mobius return after two loops}"}
                    ],
                    "references": ["PM Appendix I: Cyclic Return"]
                },
                terms={
                    "R_perp^2": "Square of OR operator",
                    "-I": "Negative identity matrix",
                    "psi": "Spinor field",
                }
            ),
        ]

    def get_output_param_definitions(self) -> List[Parameter]:
        """Return parameter definitions for outputs."""
        return [
            Parameter(
                path="or.external_sampling_enabled",
                name="External Sampling Status",
                units="boolean",
                status="ESTABLISHED",
                description="Whether instant cross-shadow sampling is enabled (always True).",
                derivation_formula="or-external-sampling",
                no_experimental_value=True
            ),
            Parameter(
                path="or.internal_gate_index",
                name="Internal Gate Index",
                units="dimensionless",
                status="DERIVED",
                description="Gate index for internal sampling (1.0 at zero cost).",
                derivation_formula="or-internal-gate-index",
                no_experimental_value=True
            ),
            Parameter(
                path="or.mobius_property",
                name="Mobius Property Verified",
                units="boolean",
                status="GATE",
                description="Verification that R_perp^2 = -I (Mobius double-cover).",
                derivation_formula="or-mobius-property",
                no_experimental_value=True
            ),
        ]


# Self-validation
_validation_instance = ORReductionV21()
assert _validation_instance.metadata is not None
assert _validation_instance.metadata.id == "or_reduction_v21"

# Verify R_perp properties at import
_R = ORReductionV21.R_PERP
assert np.allclose(_R @ _R, -np.eye(2)), "R_perp^2 must equal -I"
assert np.isclose(np.linalg.det(_R), 1.0), "det(R_perp) must equal 1"


if __name__ == "__main__":
    print("\n" + "=" * 70)
    print(" OR REDUCTION SAMPLING v21.0")
    print("=" * 70)

    # Create registry
    registry = PMRegistry.get_instance()

    # Run simulation
    sim = ORReductionV21()
    results = sim.execute(registry, verbose=True)

    print("\n" + "=" * 70)
    print(" RESULTS")
    print("=" * 70)
    for key, value in results.items():
        print(f"  {key}: {value}")

    print("\n" + "=" * 70)
    print(" MOBIUS VERIFICATION")
    print("=" * 70)
    mobius = sim.verify_mobius_return()
    for key, value in mobius.items():
        print(f"  {key}: {value}")

    print("=" * 70)
    print(" STATUS: COMPLETE")
    print("=" * 70)
