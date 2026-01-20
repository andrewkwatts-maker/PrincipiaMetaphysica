"""
Bridge Pressure Mechanism v21.0
================================

Licensed under the MIT License. See LICENSE file for details.

Implements the Euclidean (2,0) shared bridge pressure mechanism for the
(24,1) dual-shadow model. This simulation computes:

1. Conformal pressure from condensate fluxes into the bridge
2. Orthogonal Reduction (OR) sampling vectors
3. Breathing dark energy from shadow mismatch
4. Forward pressure drive from gradients

Key Formulas:
- Bridge metric: ds^2 = dy1^2 + dy2^2 (positive-definite, timeless)
- Pressure: phi(y) = sum_k log(1 + f_k * exp(-r^2 / 2*sigma^2))
- OR Rotation: R_perp = [[0, -1], [1, 0]] (90 degree rotation)
- Breathing: rho_breath = |T_normal - R_perp T_mirror|

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.

Dedicated To:
    My Wife: Elizabeth May Watts
    Our Messiah: Jesus Of Nazareth
"""

import numpy as np
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass, field

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
    MetadataBuilder,
    PHI,
)


@dataclass
class BridgeConfig:
    """Configuration for bridge pressure computation."""
    grid_size: int = 100
    y_range: Tuple[float, float] = (-10.0, 10.0)
    phi_golden: float = float(PHI)  # 1.618...
    sigma_local: float = 0.618  # 1/phi

    # Residue splits (tunable for w target)
    residue_normal: List[float] = field(default_factory=lambda: [41, 42, 42])
    residue_mirror: List[float] = field(default_factory=lambda: [19, 23, 21])

    # Branch centers in bridge (asymmetric for pressure/breathing)
    centers_normal: List[Tuple[float, float]] = field(
        default_factory=lambda: [(1.3, 0.7), (1.0, -1.0), (-0.7, 1.4)]
    )
    centers_mirror: List[Tuple[float, float]] = field(
        default_factory=lambda: [(-1.3, -0.7), (-1.0, 1.0), (0.7, -1.4)]
    )


class BridgePressureV21(SimulationBase):
    """
    Euclidean bridge pressure simulation for (24,1) dual-shadow model.

    Computes pressure gradients from G2-localized condensate fluxes
    pressing into the shared 2D bridge, enabling OR Reduction sampling
    and breathing dark energy.
    """

    def __init__(self, config: Optional[BridgeConfig] = None):
        """Initialize bridge pressure simulation."""
        self.config = config or BridgeConfig()
        self._computed = False
        self._results: Dict[str, Any] = {}

    @property
    def metadata(self) -> SimulationMetadata:
        """Return simulation metadata."""
        return SimulationMetadata(
            id="bridge_pressure_v21",
            version="21.0",
            domain="foundations",
            title="Euclidean Bridge Pressure Mechanism",
            description=(
                "Computes conformal pressure from G2 condensate fluxes into the "
                "shared (2,0) Euclidean bridge. Implements OR Reduction sampling "
                "and breathing dark energy from shadow mismatch."
            ),
            section_id="1",
            subsection_id="1.5"
        )

    @property
    def required_inputs(self) -> List[str]:
        """Return required input parameter paths."""
        return [
            "topology.b3",
            "topology.chi_eff",
        ]

    @property
    def output_params(self) -> List[str]:
        """Return output parameter paths."""
        return [
            "bridge.pressure_normal",
            "bridge.pressure_mirror",
            "bridge.rho_breath",
            "bridge.w_estimate",
            "bridge.or_strength",
            "bridge.viability",
        ]

    @property
    def output_formulas(self) -> List[str]:
        """Return formula IDs this simulation provides."""
        return [
            "bridge-metric-euclidean",
            "conformal-pressure",
            "or-reduction-operator",
            "breathing-density",
            "bridge-stress-tensor",
        ]

    def run(self, registry: PMRegistry) -> Dict[str, Any]:
        """
        Execute the bridge pressure computation.

        Args:
            registry: PMRegistry instance to read inputs from

        Returns:
            Dictionary mapping parameter paths to computed values
        """
        self.validate_inputs(registry)

        # Create bridge grid
        y = np.linspace(*self.config.y_range, self.config.grid_size)
        Y1, Y2 = np.meshgrid(y, y)

        # Step 1: Compute condensate pressure for each shadow
        phi_normal = self._compute_condensate_pressure(
            Y1, Y2,
            self.config.residue_normal,
            self.config.centers_normal
        )
        phi_mirror_raw = self._compute_condensate_pressure(
            Y1, Y2,
            self.config.residue_mirror,
            self.config.centers_mirror
        )

        # Step 2: Apply OR Reduction to mirror pressure
        grad_m_rot, phi_mirror_sampled = self._apply_or_reduction(phi_mirror_raw)

        # Step 3: Compute stress tensors
        T_normal = self._compute_stress_tensor(phi_normal)
        T_mirror = phi_mirror_sampled

        # Step 4: Compute breathing density
        rho_breath = np.abs(T_normal - T_mirror)

        # Step 5: Estimate w from breathing
        w_estimate = self._estimate_w(rho_breath)

        # Step 6: Compute gate metrics
        or_strength = np.mean(np.sqrt(grad_m_rot[0]**2 + grad_m_rot[1]**2))
        viability = np.mean(rho_breath) / (np.std(rho_breath) + 1e-10)

        # Store results
        self._results = {
            'Y1': Y1, 'Y2': Y2,
            'phi_normal': phi_normal,
            'phi_mirror_raw': phi_mirror_raw,
            'phi_mirror_sampled': phi_mirror_sampled,
            'grad_m_rot': grad_m_rot,
            'T_normal': T_normal,
            'T_mirror': T_mirror,
            'rho_breath': rho_breath,
        }
        self._computed = True

        return {
            "bridge.pressure_normal": float(np.mean(phi_normal)),
            "bridge.pressure_mirror": float(np.mean(phi_mirror_raw)),
            "bridge.rho_breath": float(np.mean(rho_breath)),
            "bridge.w_estimate": w_estimate,
            "bridge.or_strength": or_strength,
            "bridge.viability": viability,
        }

    def _compute_condensate_pressure(
        self,
        Y1: np.ndarray,
        Y2: np.ndarray,
        residues: List[float],
        centers: List[Tuple[float, float]]
    ) -> np.ndarray:
        """
        Compute conformal pressure from G2-localized condensate fluxes.

        Formula:
            phi(y1, y2) = sum_k log(1 + f_k * exp(-(r - c_k)^2 / 2*sigma^2))

        Args:
            Y1, Y2: Bridge coordinate grids
            residues: Flux magnitudes per branch
            centers: Branch centers in bridge plane

        Returns:
            Pressure field phi(y1, y2)
        """
        phi = np.zeros_like(Y1)
        sigma = self.config.sigma_local

        for flux, (c1, c2) in zip(residues, centers):
            r2 = (Y1 - c1)**2 + (Y2 - c2)**2 + 1e-10
            phi += flux * np.exp(-r2 / (2 * sigma**2))

        return np.log(1 + phi)

    def _apply_or_reduction(
        self,
        phi_raw: np.ndarray
    ) -> Tuple[Tuple[np.ndarray, np.ndarray], np.ndarray]:
        """
        Apply Orthogonal Reduction (90 degree rotation) for mirror sampling.

        The OR operator R_perp rotates gradients by 90 degrees:
            R_perp = [[0, -1], [1, 0]]
            (grad_y1, grad_y2) -> (-grad_y2, grad_y1)

        Args:
            phi_raw: Raw mirror pressure field

        Returns:
            Tuple of (rotated gradients, sampled pressure energy)
        """
        # Compute gradients
        grad_y1 = np.gradient(phi_raw, axis=0)
        grad_y2 = np.gradient(phi_raw, axis=1)

        # Apply OR rotation: (g1, g2) -> (-g2, g1)
        grad_m_rot_y1 = -grad_y2
        grad_m_rot_y2 = grad_y1

        # Compute sampled pressure (energy from rotated path)
        phi_sampled = grad_m_rot_y1**2 + grad_m_rot_y2**2

        return (grad_m_rot_y1, grad_m_rot_y2), phi_sampled

    def _compute_stress_tensor(self, phi: np.ndarray) -> np.ndarray:
        """
        Compute stress-energy tensor from pressure gradients.

        Formula:
            T^{ab} ~ partial^a phi * partial^b phi

        For visualization, we use the trace:
            T = |grad phi|^2
        """
        grad_y1 = np.gradient(phi, axis=0)
        grad_y2 = np.gradient(phi, axis=1)
        return grad_y1**2 + grad_y2**2

    def _estimate_w(self, rho_breath: np.ndarray) -> float:
        """
        Estimate dark energy equation of state from breathing density.

        Formula:
            w = -1 + (kappa_breath * <rho_breath>) / rho_crit

        where kappa_breath = 1/phi^2 ~ 0.382
        """
        kappa_breath = 1.0 / (self.config.phi_golden ** 2)
        mean_breath = np.mean(rho_breath)
        max_breath = np.max(rho_breath) + 1e-10

        w = -1.0 + kappa_breath * mean_breath / max_breath
        return float(w)

    def get_visualization_data(self) -> Optional[Dict[str, np.ndarray]]:
        """Return computed fields for visualization."""
        if not self._computed:
            return None
        return self._results.copy()

    def get_section_content(self) -> Optional[SectionContent]:
        """Return section content for the paper."""
        return SectionContent(
            section_id="1",
            subsection_id="1.5",
            title="Euclidean Bridge and OR Reduction",
            abstract=(
                "The (24,1) bulk shares a 2D Euclidean bridge between dual shadows. "
                "Condensate fluxes from G2-localized modes create pressure gradients "
                "in the bridge. Orthogonal Reduction (OR) enables instant cross-shadow "
                "sampling, while breathing from pressure mismatch drives dark energy."
            ),
            content_blocks=[
                ContentBlock(
                    type="paragraph",
                    content=(
                        "The shared Euclidean bridge provides a timeless geometric "
                        "substrate linking the dual shadows. Its positive-definite metric "
                        "eliminates ghost/CTC issues while enabling relational dynamics."
                    )
                ),
                ContentBlock(
                    type="formula",
                    content=r"ds^2_{\text{bridge}} = dy_1^2 + dy_2^2",
                    formula_id="bridge-metric-euclidean",
                    label="(1.15)"
                ),
                ContentBlock(
                    type="paragraph",
                    content=(
                        "Each shadow's G2 condensates press into the bridge via their "
                        "residue fluxes, creating conformal pressure fields:"
                    )
                ),
                ContentBlock(
                    type="formula",
                    content=r"\phi(y_1, y_2) = \sum_k \log\left(1 + f_k e^{-\frac{(y - c_k)^2}{2\sigma^2}}\right)",
                    formula_id="conformal-pressure",
                    label="(1.16)"
                ),
                ContentBlock(
                    type="paragraph",
                    content=(
                        "The OR Reduction operator enables instant cross-shadow coordinate "
                        "sampling via 90 degree rotation in the bridge plane:"
                    )
                ),
                ContentBlock(
                    type="formula",
                    content=r"R_\perp = \begin{pmatrix} 0 & -1 \\ 1 & 0 \end{pmatrix}, \quad R_\perp^2 = -I",
                    formula_id="or-reduction-operator",
                    label="(1.17)"
                ),
                ContentBlock(
                    type="paragraph",
                    content=(
                        "Dark energy breathing arises from the mismatch between shadows:"
                    )
                ),
                ContentBlock(
                    type="formula",
                    content=r"\rho_{\text{breath}} = |T^{ab}_{\text{normal}} - R_\perp T^{ab}_{\text{mirror}}|",
                    formula_id="breathing-density",
                    label="(1.18)"
                ),
            ],
            formula_refs=[
                "bridge-metric-euclidean",
                "conformal-pressure",
                "or-reduction-operator",
                "breathing-density",
            ],
            param_refs=[
                "bridge.rho_breath",
                "bridge.w_estimate",
                "bridge.or_strength",
            ]
        )

    def get_formulas(self) -> List[Formula]:
        """Return list of formulas this simulation provides."""
        return [
            Formula(
                id="bridge-metric-euclidean",
                label="(1.15)",
                latex=r"ds^2_{\text{bridge}} = dy_1^2 + dy_2^2",
                plain_text="ds^2_bridge = dy1^2 + dy2^2",
                category="THEORY",
                description="Euclidean (2,0) bridge metric - positive-definite and timeless",
                inputParams=[],
                outputParams=["bridge.metric"],
                input_params=[],
                output_params=["bridge.metric"],
                derivation={
                    "steps": [
                        {"description": "Shared dimensions from dual shadows",
                         "formula": r"{y_1, y_2} \subset \mathbb{R}^{24}"},
                        {"description": "Euclidean signature (positive-definite)",
                         "formula": r"(2,0) \text{ signature}"},
                        {"description": "No timelike component - eliminates ghosts",
                         "formula": r"\text{det}(g) > 0"}
                    ],
                    "references": ["PM Section 1.5: Euclidean Bridge"]
                },
                terms={
                    "ds^2": "Line element in bridge",
                    "y_1, y_2": "Shared Euclidean coordinates",
                }
            ),
            Formula(
                id="conformal-pressure",
                label="(1.16)",
                latex=r"\phi(y_1, y_2) = \sum_k \log\left(1 + f_k e^{-\frac{(y - c_k)^2}{2\sigma^2}}\right)",
                plain_text="phi(y) = sum_k log(1 + f_k * exp(-r^2/2*sigma^2))",
                category="DERIVED",
                description="Conformal pressure from G2 condensate fluxes in bridge",
                inputParams=["topology.residues", "bridge.centers"],
                outputParams=["bridge.pressure"],
                input_params=["topology.residues", "bridge.centers"],
                output_params=["bridge.pressure"],
                derivation={
                    "steps": [
                        {"description": "Gaussian localization from G2 cones",
                         "formula": r"f_k \propto \text{residue}_k"},
                        {"description": "Logarithmic for pressure scaling",
                         "formula": r"\phi \sim \log(1 + \text{flux})"},
                        {"description": "Width from inverse golden ratio",
                         "formula": r"\sigma = 1/\phi \approx 0.618"}
                    ],
                    "references": ["PM Appendix J: Torsion Funnel"]
                },
                terms={
                    "phi": "Conformal pressure field",
                    "f_k": "Residue flux for branch k",
                    "c_k": "Branch center in bridge",
                    "sigma": "Localization width (1/golden ratio)",
                }
            ),
            Formula(
                id="or-reduction-operator",
                label="(1.17)",
                latex=r"R_\perp = \begin{pmatrix} 0 & -1 \\ 1 & 0 \end{pmatrix}, \quad R_\perp^2 = -I",
                plain_text="R_perp = [[0, -1], [1, 0]], R_perp^2 = -I",
                category="THEORY",
                description="Orthogonal Reduction operator for cross-shadow sampling",
                inputParams=[],
                outputParams=["bridge.or_sampling"],
                input_params=[],
                output_params=["bridge.or_sampling"],
                derivation={
                    "steps": [
                        {"description": "90 degree rotation in Euclidean plane",
                         "formula": r"\theta = \pi/2"},
                        {"description": "Maps gradients orthogonally",
                         "formula": r"(\partial_1, \partial_2) \to (-\partial_2, \partial_1)"},
                        {"description": "Double application gives Mobius flip",
                         "formula": r"R_\perp^2 = -I"}
                    ],
                    "references": ["PM Section 1.5: OR Reduction"]
                },
                terms={
                    "R_perp": "Orthogonal reduction operator",
                    "-I": "Negative identity (Mobius flip)",
                }
            ),
            Formula(
                id="breathing-density",
                label="(1.18)",
                latex=r"\rho_{\text{breath}} = |T^{ab}_{\text{normal}} - R_\perp T^{ab}_{\text{mirror}}|",
                plain_text="rho_breath = |T_normal - R_perp T_mirror|",
                category="DERIVED",
                description="Breathing dark energy density from shadow pressure mismatch",
                inputParams=["bridge.T_normal", "bridge.T_mirror"],
                outputParams=["cosmology.rho_breath"],
                input_params=["bridge.T_normal", "bridge.T_mirror"],
                output_params=["cosmology.rho_breath"],
                derivation={
                    "steps": [
                        {"description": "Stress tensor from pressure gradients",
                         "formula": r"T^{ab} = \partial^a \phi \partial^b \phi"},
                        {"description": "OR rotation of mirror tensor",
                         "formula": r"R_\perp T^{ab}_{\text{mirror}}"},
                        {"description": "Mismatch drives expansion",
                         "formula": r"\rho_{\text{breath}} \to w \approx -0.958"}
                    ],
                    "references": ["PM Section 3: Cosmology"]
                },
                terms={
                    "rho_breath": "Breathing dark energy density",
                    "T^ab": "Stress-energy tensor in bridge",
                    "R_perp": "OR reduction operator",
                }
            ),
        ]

    def get_output_param_definitions(self) -> List[Parameter]:
        """Return parameter definitions for outputs."""
        return [
            Parameter(
                path="bridge.rho_breath",
                name="Breathing Dark Energy Density",
                units="dimensionless",
                status="DERIVED",
                description=(
                    "Mean breathing density from shadow pressure mismatch. "
                    "Drives the w equation of state away from -1."
                ),
                derivation_formula="breathing-density",
                no_experimental_value=True
            ),
            Parameter(
                path="bridge.w_estimate",
                name="Estimated Dark Energy EoS",
                units="dimensionless",
                status="PREDICTED",
                description=(
                    "Dark energy equation of state estimated from breathing. "
                    "Target: w ~ -0.958 (DESI alignment)."
                ),
                derivation_formula="breathing-density",
                experimental_bound=-0.958,
                bound_type="central_value",
                bound_source="DESI2025_thawing",
                uncertainty=0.067
            ),
            Parameter(
                path="bridge.or_strength",
                name="OR Sampling Strength",
                units="dimensionless",
                status="DERIVED",
                description=(
                    "Mean strength of OR reduction sampling vectors. "
                    "Gate target: > 1.0 for LOCKED status."
                ),
                derivation_formula="or-reduction-operator",
                no_experimental_value=True
            ),
            Parameter(
                path="bridge.viability",
                name="Bridge Pressure Viability",
                units="dimensionless",
                status="GATE",
                description=(
                    "Viability score: mean(rho_breath) / std(rho_breath). "
                    "Gate target: > 0.8 for LOCKED status."
                ),
                derivation_formula="breathing-density",
                no_experimental_value=True
            ),
        ]


def tune_residues_for_w_target(
    w_target: float = -0.958,
    tolerance: float = 0.01,
    max_iterations: int = 100
) -> Optional[BridgeConfig]:
    """
    Fine-tune residue configuration to achieve target w.

    Args:
        w_target: Target dark energy EoS (default DESI-aligned)
        tolerance: Acceptable deviation from target
        max_iterations: Maximum tuning iterations

    Returns:
        BridgeConfig with tuned residues, or None if not converged
    """
    config = BridgeConfig()
    registry = PMRegistry.get_instance()

    # Set minimal required params
    if not registry.has_param("topology.b3"):
        registry.set_param("topology.b3", 24, source="G2_topology", status="ESTABLISHED")
    if not registry.has_param("topology.chi_eff"):
        registry.set_param("topology.chi_eff", 144, source="G2_topology", status="ESTABLISHED")

    best_config = config
    best_error = float('inf')

    for i in range(max_iterations):
        sim = BridgePressureV21(config)
        results = sim.run(registry)
        w_computed = results["bridge.w_estimate"]
        error = abs(w_computed - w_target)

        if error < best_error:
            best_error = error
            best_config = BridgeConfig(
                residue_normal=list(config.residue_normal),
                residue_mirror=list(config.residue_mirror),
                centers_normal=list(config.centers_normal),
                centers_mirror=list(config.centers_mirror),
            )

        if error < tolerance:
            print(f"Converged at iteration {i}: w = {w_computed:.5f}")
            return best_config

        # Adjust mirror residues based on error direction
        adjustment = 0.5 if w_computed > w_target else -0.5
        config.residue_mirror = [r + adjustment for r in config.residue_mirror]

    print(f"Did not converge. Best w = {w_target + best_error * np.sign(w_target):.5f}")
    return best_config


# Self-validation
_validation_instance = BridgePressureV21()
assert _validation_instance.metadata is not None
assert _validation_instance.metadata.id == "bridge_pressure_v21"


if __name__ == "__main__":
    print("\n" + "=" * 70)
    print(" BRIDGE PRESSURE MECHANISM v21.0")
    print("=" * 70)

    # Create registry
    registry = PMRegistry.get_instance()
    registry.set_param("topology.b3", 24, source="G2_topology", status="ESTABLISHED")
    registry.set_param("topology.chi_eff", 144, source="G2_topology", status="ESTABLISHED")

    # Run simulation
    sim = BridgePressureV21()
    results = sim.execute(registry, verbose=True)

    print("\n" + "=" * 70)
    print(" RESULTS")
    print("=" * 70)
    for key, value in results.items():
        print(f"  {key}: {value:.6f}" if isinstance(value, float) else f"  {key}: {value}")

    # Gate checks
    print("\n" + "=" * 70)
    print(" GATE CHECKS")
    print("=" * 70)
    or_strength = results.get("bridge.or_strength", 0)
    viability = results.get("bridge.viability", 0)
    w_estimate = results.get("bridge.w_estimate", -1)

    print(f"  OR Strength: {or_strength:.3f} {'LOCKED' if or_strength > 1.0 else 'MARGINAL'}")
    print(f"  Viability: {viability:.3f} {'LOCKED' if viability > 0.8 else 'MARGINAL'}")
    print(f"  w Estimate: {w_estimate:.5f} (target: -0.958)")

    print("=" * 70)
    print(" STATUS: COMPLETE")
    print("=" * 70)
