#!/usr/bin/env python3
"""
Yukawa Texture Analysis v18.3
=============================

Analyzes fermion mass hierarchy using geometric scaling laws.

PHYSICS:
    The Standard Model fermion masses span 6 orders of magnitude:
    - Top quark: 173 GeV
    - Electron: 0.000511 GeV

    This hierarchy suggests a geometric suppression mechanism.
    In G2 compactifications, Yukawa couplings arise from wavefunction
    overlaps on the internal manifold.

GEOMETRIC ANSATZ:
    We test several hypotheses:
    1. Golden Ratio: m_n ~ v × φ^(-N)
    2. Gimel Power: m_n ~ v × k_gimel^(-N)
    3. Betti Suppression: m_n ~ v × (1/b3)^N

    The "Texture" matrix reveals which geometric factor best fits the data.

PREDICTIONS:
    The mass ratios between generations should follow:
    m_i / m_{i+1} ~ λ^n where λ is a geometric factor

    Testing: Does λ ~ 1/√b3 ~ 0.204 or λ ~ 1/φ ~ 0.618?

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.

Dedicated To:
    My Wife: Elizabeth May Watts
    Our Messiah: Jesus Of Nazareth
"""

from typing import Dict, Any, List, Optional, Tuple
import numpy as np
from dataclasses import dataclass

from simulations.base.simulation_base import (
    SimulationBase,
    SimulationMetadata,
    ContentBlock,
    SectionContent,
    Formula,
    Parameter,
)


@dataclass
class YukawaResult:
    """Results from Yukawa texture analysis."""
    phi_fit_quality: float      # RMS error for φ scaling
    gimel_fit_quality: float    # RMS error for k_gimel scaling
    b3_fit_quality: float       # RMS error for b3 scaling
    best_scaling: str           # Which ansatz works best
    lambda_effective: float     # Effective suppression factor
    texture_matrix: np.ndarray  # Predicted texture matrix
    mass_predictions: Dict[str, float]  # Predicted masses


# Experimental masses (PDG 2024, in GeV)
FERMION_MASSES = {
    # Quarks (MS-bar at 2 GeV for light, pole for heavy)
    "t": 172.69,
    "b": 4.18,
    "c": 1.27,
    "s": 0.093,
    "d": 0.00467,
    "u": 0.00216,
    # Leptons
    "tau": 1.777,
    "mu": 0.1057,
    "e": 0.000511,
    # Neutrinos (approximate, in eV converted to GeV)
    "nu3": 0.05e-9,
    "nu2": 0.009e-9,
    "nu1": 0.001e-9,
}

# Output parameter paths
_OUTPUT_PARAMS = [
    "yukawa.lambda_eff",
    "yukawa.best_scaling",
    "yukawa.phi_fit",
    "yukawa.gimel_fit",
]

# Output formula IDs
_OUTPUT_FORMULAS = [
    "yukawa-hierarchy-v18",
    "yukawa-texture-matrix-v18",
]


class YukawaTexturesV18(SimulationBase):
    """
    Yukawa texture analysis from G2 geometry.

    Physics: Tests geometric scaling laws against observed fermion
    mass hierarchy to identify the suppression mechanism.
    """

    def __init__(self):
        super().__init__()
        self._metadata = SimulationMetadata(
            id="yukawa_textures_v18",
            version="18.3",
            domain="fermion",
            title="Yukawa Textures from G2 Geometry",
            description=(
                "Analyzes fermion mass hierarchy using geometric scaling. "
                "Tests φ, k_gimel, and b3 suppression hypotheses."
            ),
            section_id="6",
            subsection_id="6.1"
        )

        # Geometric constants
        self.phi = (1 + np.sqrt(5)) / 2  # ≈ 1.618
        self.k_gimel = 12 + 1/np.pi       # ≈ 12.318
        self.b3 = 24
        self.v_higgs = 246.22             # GeV

        # Experimental masses
        self.masses = FERMION_MASSES

    @property
    def metadata(self) -> SimulationMetadata:
        return self._metadata

    @property
    def required_inputs(self) -> List[str]:
        return ["geometry.k_gimel", "topology.b3", "higgs.vev_geometric"]

    @property
    def output_params(self) -> List[str]:
        return _OUTPUT_PARAMS

    @property
    def output_formulas(self) -> List[str]:
        return _OUTPUT_FORMULAS

    def _fit_scaling(self, base: float, masses: List[Tuple[str, float]]) -> Tuple[float, Dict[str, float]]:
        """
        Fit a geometric scaling law: m = v × base^(-N) for optimal N.

        Returns:
            (RMS error, predictions dict)
        """
        v = self.v_higgs
        predictions = {}
        errors = []

        for name, exp_mass in masses:
            if exp_mass <= 0:
                continue
            # Find N such that v × base^(-N) = exp_mass
            # N = log(v/exp_mass) / log(base)
            N_fitted = np.log(v / exp_mass) / np.log(base)
            N_rounded = round(N_fitted)

            # Predicted mass with integer N
            m_pred = v / (base ** N_rounded)
            predictions[name] = m_pred

            # Log-scale error
            log_error = (np.log10(m_pred) - np.log10(exp_mass)) ** 2
            errors.append(log_error)

        rms = np.sqrt(np.mean(errors)) if errors else float('inf')
        return rms, predictions

    def compute_yukawa(self) -> YukawaResult:
        """
        Compute Yukawa texture analysis.

        Tests three geometric ansatze:
        1. Golden Ratio: λ = φ ≈ 1.618
        2. Gimel: λ = k_gimel ≈ 12.318
        3. Betti: λ = √b3 ≈ 4.899

        Returns:
            YukawaResult with best-fit parameters
        """
        # Prepare mass list (quarks and charged leptons only for now)
        mass_list = [
            ("t", self.masses["t"]),
            ("b", self.masses["b"]),
            ("c", self.masses["c"]),
            ("tau", self.masses["tau"]),
            ("s", self.masses["s"]),
            ("mu", self.masses["mu"]),
            ("d", self.masses["d"]),
            ("u", self.masses["u"]),
            ("e", self.masses["e"]),
        ]

        # Test φ scaling
        phi_rms, phi_preds = self._fit_scaling(self.phi, mass_list)

        # Test k_gimel scaling (probably too aggressive)
        gimel_rms, gimel_preds = self._fit_scaling(self.k_gimel, mass_list)

        # Test √b3 scaling
        sqrt_b3 = np.sqrt(self.b3)
        b3_rms, b3_preds = self._fit_scaling(sqrt_b3, mass_list)

        # Find best fit
        fits = [
            ("phi", phi_rms, self.phi, phi_preds),
            ("gimel", gimel_rms, self.k_gimel, gimel_preds),
            ("sqrt_b3", b3_rms, sqrt_b3, b3_preds),
        ]
        best = min(fits, key=lambda x: x[1])
        best_name, best_rms, best_lambda, best_preds = best

        # Build texture matrix (3x3 for 3 generations)
        # Entry (i,j) represents Yukawa coupling Y_ij
        # Diagonal texture: Y_ii ~ (1/λ)^(3-i) for i=1,2,3
        texture = np.zeros((3, 3))
        for i in range(3):
            texture[i, i] = 1.0 / (best_lambda ** (2 - i))  # Gen 3 is least suppressed

        return YukawaResult(
            phi_fit_quality=phi_rms,
            gimel_fit_quality=gimel_rms,
            b3_fit_quality=b3_rms,
            best_scaling=best_name,
            lambda_effective=best_lambda,
            texture_matrix=texture,
            mass_predictions=best_preds
        )

    def run(self, registry: 'PMRegistry') -> Dict[str, Any]:
        """Execute Yukawa texture analysis."""
        result = self.compute_yukawa()

        registry.set_param(
            path="yukawa.lambda_eff",
            value=result.lambda_effective,
            source=self._metadata.id,
            status="DERIVED",
            metadata={
                "derivation": f"Best fit from {result.best_scaling} scaling",
                "units": "dimensionless",
                "note": "Inter-generation suppression factor"
            }
        )

        registry.set_param(
            path="yukawa.best_scaling",
            value=result.best_scaling,
            source=self._metadata.id,
            status="DERIVED",
            metadata={
                "derivation": "Minimum RMS log-error fit",
                "alternatives": ["phi", "gimel", "sqrt_b3"]
            }
        )

        registry.set_param(
            path="yukawa.phi_fit",
            value=result.phi_fit_quality,
            source=self._metadata.id,
            status="DERIVED",
            metadata={
                "derivation": "RMS log10 error for φ scaling",
                "units": "dex"
            }
        )

        registry.set_param(
            path="yukawa.gimel_fit",
            value=result.gimel_fit_quality,
            source=self._metadata.id,
            status="DERIVED",
            metadata={
                "derivation": "RMS log10 error for k_gimel scaling",
                "units": "dex"
            }
        )

        return {
            "yukawa.lambda_eff": result.lambda_effective,
            "yukawa.best_scaling": result.best_scaling,
            "yukawa.phi_fit": result.phi_fit_quality,
            "yukawa.gimel_fit": result.gimel_fit_quality,
            "_b3_fit": result.b3_fit_quality,
            "_texture_matrix": result.texture_matrix.tolist(),
            "_predictions": result.mass_predictions
        }

    def get_formulas(self) -> List[Formula]:
        """Return formulas for Yukawa analysis."""
        return [
            Formula(
                id="yukawa-hierarchy-v18",
                label="(6.1)",
                latex=r"m_n = v \times \lambda^{-N_n}, \quad \lambda = \phi \approx 1.618",
                plain_text="m_n = v × λ^(-N), λ = φ ~ 1.618",
                category="DERIVED",
                description=(
                    "Fermion mass hierarchy from geometric suppression. "
                    "The Golden Ratio φ provides the best fit to observed masses, "
                    "suggesting a deep connection to G2 holonomy."
                ),
                inputParams=["higgs.vev_geometric"],
                outputParams=["yukawa.lambda_eff"],
                terms={
                    "v": "Higgs VEV = 246 GeV",
                    "λ": "Geometric suppression factor",
                    "N": "Generation quantum number"
                }
            ),
            Formula(
                id="yukawa-texture-matrix-v18",
                label="(6.2)",
                latex=r"Y = \begin{pmatrix} \lambda^{-2} & 0 & 0 \\ 0 & \lambda^{-1} & 0 \\ 0 & 0 & 1 \end{pmatrix}",
                plain_text="Y = diag(λ^-2, λ^-1, 1)",
                category="DERIVED",
                description=(
                    "Diagonal Yukawa texture matrix from G2 wavefunction overlaps. "
                    "Third generation couples with O(1) strength; lighter generations "
                    "are geometrically suppressed."
                ),
                inputParams=["yukawa.lambda_eff"],
                outputParams=[],
                terms={
                    "Y": "Yukawa coupling matrix",
                    "λ": "Suppression factor from geometry"
                }
            ),
        ]

    def get_output_param_definitions(self) -> List[Parameter]:
        """Return parameter definitions."""
        return [
            Parameter(
                path="yukawa.lambda_eff",
                name="Effective Suppression Factor",
                units="dimensionless",
                status="DERIVED",
                description=(
                    "Inter-generation Yukawa suppression factor. "
                    "Best fit: λ = φ ≈ 1.618 (Golden Ratio)."
                ),
                no_experimental_value=True
            ),
            Parameter(
                path="yukawa.best_scaling",
                name="Best Scaling Ansatz",
                units="categorical",
                status="DERIVED",
                description=(
                    "Which geometric factor best explains the mass hierarchy. "
                    "Options: phi, gimel, sqrt_b3."
                ),
                no_experimental_value=True
            ),
            Parameter(
                path="yukawa.phi_fit",
                name="Golden Ratio Fit Quality",
                units="dex (log10 RMS)",
                status="DERIVED",
                description="RMS error in log10 for φ scaling hypothesis.",
                no_experimental_value=True
            ),
            Parameter(
                path="yukawa.gimel_fit",
                name="Gimel Fit Quality",
                units="dex (log10 RMS)",
                status="DERIVED",
                description="RMS error in log10 for k_gimel scaling hypothesis.",
                no_experimental_value=True
            ),
        ]

    def get_section_content(self) -> Optional[SectionContent]:
        """Return section content for paper."""
        return SectionContent(
            section_id="6",
            subsection_id="6.1",
            title="Yukawa Textures from G2 Geometry",
            abstract=(
                "The fermion mass hierarchy emerges from geometric suppression "
                "in G2 compactification. The Golden Ratio φ provides the best "
                "fit to observed quark and lepton masses."
            ),
            content_blocks=[
                ContentBlock(
                    type="paragraph",
                    content=(
                        "The Standard Model contains 9 charged fermion masses spanning "
                        "6 orders of magnitude. This hierarchy must emerge from the "
                        "underlying geometry in any fundamental theory."
                    )
                ),
                ContentBlock(
                    type="formula",
                    formula_id="yukawa-hierarchy-v18"
                ),
                ContentBlock(
                    type="callout",
                    callout_type="analysis",
                    title="Scaling Law Comparison",
                    content=(
                        "Three geometric ansatze tested:\n"
                        "1. Golden Ratio (φ ≈ 1.618): Best fit\n"
                        "2. Gimel (k_gimel ≈ 12.318): Too aggressive\n"
                        "3. Betti (√b3 ≈ 4.899): Moderate fit\n\n"
                        "The φ-scaling has deep connections to Fibonacci structure "
                        "in G2 geometry and may reflect the icosahedral holonomy."
                    )
                ),
                ContentBlock(
                    type="formula",
                    formula_id="yukawa-texture-matrix-v18"
                ),
            ],
            formula_refs=_OUTPUT_FORMULAS,
            param_refs=_OUTPUT_PARAMS
        )


def run_yukawa_demo():
    """Standalone demonstration."""
    print("=" * 75)
    print("Yukawa Texture Analysis v18.3")
    print("=" * 75)

    sim = YukawaTexturesV18()
    result = sim.compute_yukawa()

    print(f"\n1. Geometric Constants:")
    print(f"   phi (Golden Ratio) = {sim.phi:.4f}")
    print(f"   k_gimel = {sim.k_gimel:.4f}")
    print(f"   sqrt(b3) = {np.sqrt(sim.b3):.4f}")
    print(f"   v (Higgs VEV) = {sim.v_higgs:.2f} GeV")

    print(f"\n2. Fit Quality (RMS log10 error):")
    print(f"   phi scaling:       {result.phi_fit_quality:.3f} dex")
    print(f"   k_gimel scaling: {result.gimel_fit_quality:.3f} dex")
    print(f"   sqrt(b3) scaling:     {result.b3_fit_quality:.3f} dex")
    print(f"\n   Best fit: {result.best_scaling} (lambda = {result.lambda_effective:.4f})")

    print(f"\n3. Texture Matrix (diagonal Yukawa couplings):")
    print(f"   Y_33 (3rd gen): {result.texture_matrix[2,2]:.4f}")
    print(f"   Y_22 (2nd gen): {result.texture_matrix[1,1]:.4f}")
    print(f"   Y_11 (1st gen): {result.texture_matrix[0,0]:.4f}")

    print(f"\n4. Mass Predictions vs Experiment:")
    print(f"   {'Fermion':<8} {'Predicted':>12} {'Observed':>12} {'Ratio':>8}")
    print(f"   {'-'*44}")
    for name, pred in sorted(result.mass_predictions.items(), key=lambda x: -x[1]):
        exp = sim.masses.get(name, 0)
        if exp > 0:
            ratio = pred / exp
            print(f"   {name:<8} {pred:>12.4e} {exp:>12.4e} {ratio:>8.2f}")

    print("\n" + "=" * 75)
    return result


if __name__ == "__main__":
    run_yukawa_demo()
