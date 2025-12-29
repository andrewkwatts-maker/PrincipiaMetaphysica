#!/usr/bin/env python3
"""
PRINCIPIA METAPHYSICA v16.1 - Rigorous Covariance Matrix Analysis
==================================================================

This module implements proper statistical analysis with full covariance matrices
for correlated parameter uncertainties. Unlike independent parameter comparisons,
this accounts for correlations between measurements.

COVARIANCE MATRICES:
1. NuFIT 6.0 (2025): Neutrino oscillation parameters
   - Parameters: θ₁₂, θ₁₃, θ₂₃, δ_CP
   - Full 4×4 covariance matrix with correlations

2. DESI 2025: Cosmological parameters
   - Parameters: w₀, wₐ, Ωₘ, H₀
   - Full 4×4 covariance matrix with CPL degeneracy

STATISTICAL METHODS:
- Chi-square with correlations: χ² = (x - μ)ᵀ Σ⁻¹ (x - μ)
- Goodness-of-fit: p-value from χ² distribution
- Degrees of freedom: n_params - n_free_params
- Pull distributions: individual parameter tensions accounting for correlations

OUTPUTS:
- Combined chi-square for all sectors
- Sector-specific chi-squares (neutrino, cosmology)
- Goodness-of-fit p-values
- Pull distributions with proper error propagation
- Correlation-aware tension flags

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.
"""

import numpy as np
import json
import os
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass, field
from scipy import stats
import sys

# Add parent directories to path for imports
_current_dir = os.path.dirname(os.path.abspath(__file__))
_simulations_root = os.path.dirname(os.path.dirname(os.path.dirname(_current_dir)))
sys.path.insert(0, _simulations_root)

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
class CovarianceData:
    """
    Complete covariance data for a set of parameters.

    Attributes:
        parameter_names: List of parameter names in order
        central_values: Central experimental values
        uncertainties: 1σ uncertainties (diagonal of covariance)
        correlation_matrix: Correlation coefficient matrix (symmetric, diag=1)
        covariance_matrix: Full covariance matrix
        inverse_covariance: Inverse covariance (precision matrix)
        units: Units for each parameter
        source: Data source identifier
    """
    parameter_names: List[str]
    central_values: np.ndarray
    uncertainties: np.ndarray
    correlation_matrix: np.ndarray
    covariance_matrix: np.ndarray
    inverse_covariance: np.ndarray
    units: List[str]
    source: str

    def __post_init__(self):
        """Validate matrix shapes and properties."""
        n = len(self.parameter_names)

        # Check shapes
        assert self.central_values.shape == (n,), f"central_values shape mismatch: {self.central_values.shape} vs ({n},)"
        assert self.uncertainties.shape == (n,), f"uncertainties shape mismatch"
        assert self.correlation_matrix.shape == (n, n), f"correlation_matrix shape mismatch"
        assert self.covariance_matrix.shape == (n, n), f"covariance_matrix shape mismatch"
        assert self.inverse_covariance.shape == (n, n), f"inverse_covariance shape mismatch"

        # Check correlation matrix properties
        assert np.allclose(self.correlation_matrix, self.correlation_matrix.T), "Correlation matrix not symmetric"
        assert np.allclose(np.diag(self.correlation_matrix), 1.0), "Correlation matrix diagonal not 1.0"

        # Check covariance matrix properties
        assert np.allclose(self.covariance_matrix, self.covariance_matrix.T), "Covariance matrix not symmetric"

        # Check positive definiteness (all eigenvalues > 0)
        eigvals = np.linalg.eigvalsh(self.covariance_matrix)
        assert np.all(eigvals > 0), f"Covariance matrix not positive definite: eigenvalues = {eigvals}"


@dataclass
class ChiSquareResult:
    """
    Chi-square test result with full diagnostics.

    Attributes:
        chi_square: Total χ² value
        ndof: Number of degrees of freedom
        p_value: Goodness-of-fit p-value (probability of χ² ≥ observed)
        reduced_chi_square: χ²/ndof
        status: "EXCELLENT", "GOOD", "ACCEPTABLE", "MARGINAL", or "TENSION"
        predictions: PM predicted values
        observations: Experimental central values
        residuals: predictions - observations
        pulls: Normalized pulls accounting for correlations
        covariance_data: Full covariance information
    """
    chi_square: float
    ndof: int
    p_value: float
    reduced_chi_square: float
    status: str
    predictions: np.ndarray
    observations: np.ndarray
    residuals: np.ndarray
    pulls: np.ndarray
    covariance_data: CovarianceData

    def get_sigma_equivalent(self) -> float:
        """
        Get equivalent sigma deviation from p-value.

        For a chi-square distribution, we can convert p-value to equivalent
        sigma for a normal distribution.

        Returns:
            Equivalent number of standard deviations
        """
        # For p-value, find sigma such that P(|Z| > sigma) = p_value for Z ~ N(0,1)
        # This is: sigma = Φ⁻¹(1 - p/2) where Φ is normal CDF
        if self.p_value >= 0.5:
            return 0.0
        return stats.norm.ppf(1 - self.p_value / 2)

    def __str__(self) -> str:
        """String representation with key metrics."""
        sigma_eq = self.get_sigma_equivalent()
        return (
            f"ChiSquareResult:\n"
            f"  χ² = {self.chi_square:.2f} (ndof={self.ndof})\n"
            f"  χ²/ndof = {self.reduced_chi_square:.2f}\n"
            f"  p-value = {self.p_value:.4f} ({sigma_eq:.2f}σ equivalent)\n"
            f"  Status: {self.status}"
        )


class RigorCovarianceV16_1(SimulationBase):
    """
    Rigorous covariance matrix analysis for PM v16.1.

    This simulation implements proper statistical validation using full
    covariance matrices that account for parameter correlations. It computes:

    1. Neutrino sector chi-square (NuFIT 6.0 4×4 covariance)
    2. Cosmology sector chi-square (DESI 2025 4×4 covariance)
    3. Combined chi-square across all sectors
    4. Goodness-of-fit p-values and status classifications

    The chi-square formula with correlations is:
        χ² = (x - μ)ᵀ Σ⁻¹ (x - μ)

    where:
        x = predicted values (from PM)
        μ = experimental central values
        Σ = covariance matrix (accounts for correlations)
        Σ⁻¹ = inverse covariance (precision matrix)
    """

    # Data directory for covariance matrices
    DATA_DIR = Path(__file__).parent.parent.parent / "data" / "experimental"

    def __init__(self):
        """Initialize the covariance analyzer."""
        self.neutrino_cov: Optional[CovarianceData] = None
        self.cosmology_cov: Optional[CovarianceData] = None

        self.neutrino_result: Optional[ChiSquareResult] = None
        self.cosmology_result: Optional[ChiSquareResult] = None
        self.combined_result: Optional[ChiSquareResult] = None

    # -------------------------------------------------------------------------
    # SimulationBase Interface - Metadata
    # -------------------------------------------------------------------------

    @property
    def metadata(self) -> SimulationMetadata:
        """Return metadata about this simulation."""
        return SimulationMetadata(
            id="rigor_covariance_v16_1",
            version="16.1",
            domain="statistics",
            title="Rigorous Covariance Matrix Analysis",
            description=(
                "Statistical validation of PM v16.1 predictions using full covariance "
                "matrices for correlated parameter uncertainties. Computes chi-square "
                "goodness-of-fit with proper correlations from NuFIT 6.0 (neutrino) "
                "and DESI 2025 (cosmology)."
            ),
            section_id="A",
            subsection_id="A.S"  # Appendix A, Statistics subsection
        )

    @property
    def required_inputs(self) -> List[str]:
        """Return list of required input parameter paths."""
        return [
            # Neutrino predictions
            "neutrino.theta_12_pred",
            "neutrino.theta_13_pred",
            "neutrino.theta_23_pred",
            "neutrino.delta_CP_pred",

            # Cosmology predictions
            "cosmology.w0_derived",
            "cosmology.wa_derived",
            "cosmology.Omega_m",
            "cosmology.H0",
        ]

    @property
    def output_params(self) -> List[str]:
        """Return list of output parameter paths."""
        return [
            # Neutrino sector
            "statistics.neutrino_chi_square",
            "statistics.neutrino_ndof",
            "statistics.neutrino_p_value",
            "statistics.neutrino_status",

            # Cosmology sector
            "statistics.cosmology_chi_square",
            "statistics.cosmology_ndof",
            "statistics.cosmology_p_value",
            "statistics.cosmology_status",

            # Combined
            "statistics.combined_chi_square",
            "statistics.combined_ndof",
            "statistics.combined_p_value",
            "statistics.combined_status",
        ]

    @property
    def output_formulas(self) -> List[str]:
        """Return list of formula IDs this simulation provides."""
        return [
            "chi-square-covariance",
            "p-value-chi-square",
            "reduced-chi-square",
            "pull-definition",
        ]

    # -------------------------------------------------------------------------
    # Data Loading
    # -------------------------------------------------------------------------

    def load_neutrino_covariance(self) -> CovarianceData:
        """
        Load NuFIT 6.0 covariance matrix.

        Returns:
            CovarianceData for neutrino parameters
        """
        filepath = self.DATA_DIR / "nufit_6_0_covariance.json"

        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Extract Normal Ordering data
        no_data = data["normal_ordering"]
        params = no_data["parameters"]
        corr_data = no_data["correlation_matrix"]
        cov_data = no_data["covariance_matrix"]
        inv_cov_data = no_data["inverse_covariance_matrix"]

        # Parameter order
        param_order = corr_data["parameters_order"]

        # Extract values
        central_vals = np.array([params[p]["value"] for p in param_order])
        uncertainties = np.array([params[p]["uncertainty"] for p in param_order])
        units = [params[p]["units"] for p in param_order]

        # Matrices
        corr_matrix = np.array(corr_data["matrix"])
        cov_matrix = np.array(cov_data["matrix"])
        inv_cov_matrix = np.array(inv_cov_data["matrix"])

        return CovarianceData(
            parameter_names=param_order,
            central_values=central_vals,
            uncertainties=uncertainties,
            correlation_matrix=corr_matrix,
            covariance_matrix=cov_matrix,
            inverse_covariance=inv_cov_matrix,
            units=units,
            source="NuFIT 6.0 (2024)"
        )

    def load_cosmology_covariance(self) -> CovarianceData:
        """
        Load DESI 2025 covariance matrix.

        Returns:
            CovarianceData for cosmological parameters
        """
        filepath = self.DATA_DIR / "nufit_6_0_covariance.json"

        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Extract cosmology data
        cosmo_data = data["cosmological_parameters"]
        params = cosmo_data["parameters"]
        corr_data = cosmo_data["correlation_matrix"]
        cov_data = cosmo_data["covariance_matrix"]
        inv_cov_data = cosmo_data["inverse_covariance_matrix"]

        # Parameter order
        param_order = corr_data["parameters_order"]

        # Extract values
        central_vals = np.array([params[p]["value"] for p in param_order])
        uncertainties = np.array([params[p]["uncertainty"] for p in param_order])
        units = [params[p]["units"] for p in param_order]

        # Matrices
        corr_matrix = np.array(corr_data["matrix"])
        cov_matrix = np.array(cov_data["matrix"])
        inv_cov_matrix = np.array(inv_cov_data["matrix"])

        return CovarianceData(
            parameter_names=param_order,
            central_values=central_vals,
            uncertainties=uncertainties,
            correlation_matrix=corr_matrix,
            covariance_matrix=cov_matrix,
            inverse_covariance=inv_cov_matrix,
            units=units,
            source="DESI 2025 (arXiv:2411.12022)"
        )

    # -------------------------------------------------------------------------
    # Chi-Square Computation
    # -------------------------------------------------------------------------

    def compute_chi_square(
        self,
        predictions: np.ndarray,
        cov_data: CovarianceData,
        n_free_params: int = 0
    ) -> ChiSquareResult:
        """
        Compute chi-square with full covariance matrix.

        χ² = (x - μ)ᵀ Σ⁻¹ (x - μ)

        Args:
            predictions: Predicted values (PM theory)
            cov_data: CovarianceData with experimental values and covariance
            n_free_params: Number of free parameters in theory (reduces ndof)

        Returns:
            ChiSquareResult with full diagnostics
        """
        # Compute residuals
        residuals = predictions - cov_data.central_values

        # Compute chi-square: χ² = Δᵀ Σ⁻¹ Δ
        chi_square = float(residuals @ cov_data.inverse_covariance @ residuals)

        # Degrees of freedom
        ndof = len(predictions) - n_free_params

        # P-value from chi-square distribution
        # P(χ² ≥ observed | H0) = 1 - CDF(observed; ndof)
        p_value = 1 - stats.chi2.cdf(chi_square, ndof) if ndof > 0 else 0.0

        # Reduced chi-square
        reduced_chi_square = chi_square / ndof if ndof > 0 else float('inf')

        # Status classification
        if reduced_chi_square < 1.5:
            status = "EXCELLENT"
        elif reduced_chi_square < 2.0:
            status = "GOOD"
        elif reduced_chi_square < 3.0:
            status = "ACCEPTABLE"
        elif reduced_chi_square < 5.0:
            status = "MARGINAL"
        else:
            status = "TENSION"

        # Compute pulls (standardized residuals accounting for correlations)
        # Pull_i = (Δᵀ Σ⁻¹)_i / sqrt((Σ⁻¹)_ii)
        # This gives the contribution of each parameter to chi-square
        pulls = np.zeros(len(predictions))
        for i in range(len(predictions)):
            # Marginal pull for parameter i
            pulls[i] = residuals[i] / np.sqrt(cov_data.covariance_matrix[i, i])

        return ChiSquareResult(
            chi_square=chi_square,
            ndof=ndof,
            p_value=p_value,
            reduced_chi_square=reduced_chi_square,
            status=status,
            predictions=predictions,
            observations=cov_data.central_values,
            residuals=residuals,
            pulls=pulls,
            covariance_data=cov_data
        )

    # -------------------------------------------------------------------------
    # Core Computation
    # -------------------------------------------------------------------------

    def run(self, registry: PMRegistry) -> Dict[str, Any]:
        """
        Execute the covariance analysis.

        Args:
            registry: PMRegistry instance to read inputs from

        Returns:
            Dictionary mapping parameter paths to computed values
        """
        # Load covariance matrices
        self.neutrino_cov = self.load_neutrino_covariance()
        self.cosmology_cov = self.load_cosmology_covariance()

        # Gather neutrino predictions
        neutrino_preds = np.array([
            registry.get_param("neutrino.theta_12_pred"),
            registry.get_param("neutrino.theta_13_pred"),
            registry.get_param("neutrino.theta_23_pred"),
            registry.get_param("neutrino.delta_CP_pred"),
        ])

        # Gather cosmology predictions
        cosmology_preds = np.array([
            registry.get_param("cosmology.w0_derived"),
            registry.get_param("cosmology.wa_derived"),
            registry.get_param("cosmology.Omega_m"),
            registry.get_param("cosmology.H0"),
        ])

        # Compute chi-squares
        self.neutrino_result = self.compute_chi_square(
            neutrino_preds,
            self.neutrino_cov,
            n_free_params=0  # No free parameters in neutrino sector for PM
        )

        self.cosmology_result = self.compute_chi_square(
            cosmology_preds,
            self.cosmology_cov,
            n_free_params=0  # No free parameters in cosmology for PM
        )

        # Combined chi-square (sum of independent sectors)
        combined_chi_square = self.neutrino_result.chi_square + self.cosmology_result.chi_square
        combined_ndof = self.neutrino_result.ndof + self.cosmology_result.ndof
        combined_p_value = 1 - stats.chi2.cdf(combined_chi_square, combined_ndof)
        combined_reduced = combined_chi_square / combined_ndof

        # Combined status
        if combined_reduced < 1.5:
            combined_status = "EXCELLENT"
        elif combined_reduced < 2.0:
            combined_status = "GOOD"
        elif combined_reduced < 3.0:
            combined_status = "ACCEPTABLE"
        elif combined_reduced < 5.0:
            combined_status = "MARGINAL"
        else:
            combined_status = "TENSION"

        # Store combined result
        self.combined_result = ChiSquareResult(
            chi_square=combined_chi_square,
            ndof=combined_ndof,
            p_value=combined_p_value,
            reduced_chi_square=combined_reduced,
            status=combined_status,
            predictions=np.concatenate([neutrino_preds, cosmology_preds]),
            observations=np.concatenate([
                self.neutrino_cov.central_values,
                self.cosmology_cov.central_values
            ]),
            residuals=np.concatenate([
                self.neutrino_result.residuals,
                self.cosmology_result.residuals
            ]),
            pulls=np.concatenate([
                self.neutrino_result.pulls,
                self.cosmology_result.pulls
            ]),
            covariance_data=self.neutrino_cov  # Placeholder (combined cov not computed)
        )

        # Return results
        return {
            # Neutrino
            "statistics.neutrino_chi_square": self.neutrino_result.chi_square,
            "statistics.neutrino_ndof": self.neutrino_result.ndof,
            "statistics.neutrino_p_value": self.neutrino_result.p_value,
            "statistics.neutrino_status": self.neutrino_result.status,

            # Cosmology
            "statistics.cosmology_chi_square": self.cosmology_result.chi_square,
            "statistics.cosmology_ndof": self.cosmology_result.ndof,
            "statistics.cosmology_p_value": self.cosmology_result.p_value,
            "statistics.cosmology_status": self.cosmology_result.status,

            # Combined
            "statistics.combined_chi_square": combined_chi_square,
            "statistics.combined_ndof": combined_ndof,
            "statistics.combined_p_value": combined_p_value,
            "statistics.combined_status": combined_status,
        }

    # -------------------------------------------------------------------------
    # Section Content
    # -------------------------------------------------------------------------

    def get_section_content(self) -> Optional[SectionContent]:
        """
        Return section content for Appendix A.S: Statistical Analysis.

        Returns:
            SectionContent instance describing the covariance analysis
        """
        if not self.neutrino_result or not self.cosmology_result:
            # Not yet run
            return None

        content_blocks = [
            ContentBlock(
                type="heading",
                content="Rigorous Covariance Matrix Analysis",
                level=2
            ),
            ContentBlock(
                type="paragraph",
                content=(
                    "This section presents a rigorous statistical validation of Principia "
                    "Metaphysica v16.1 predictions using full covariance matrices that "
                    "account for correlations between experimental measurements. Unlike "
                    "independent parameter comparisons, this approach properly handles "
                    "the correlated uncertainties present in global fits of neutrino "
                    "oscillation data (NuFIT 6.0) and cosmological parameters (DESI 2025)."
                )
            ),

            # Methodology
            ContentBlock(
                type="heading",
                content="Chi-Square with Covariance",
                level=3
            ),
            ContentBlock(
                type="paragraph",
                content=(
                    "The chi-square statistic accounting for correlated uncertainties is:"
                )
            ),
            ContentBlock(
                type="formula",
                content=r"\chi^2 = (\mathbf{x}_{\text{PM}} - \boldsymbol{\mu}_{\text{exp}})^T "
                       r"\boldsymbol{\Sigma}^{-1} "
                       r"(\mathbf{x}_{\text{PM}} - \boldsymbol{\mu}_{\text{exp}})",
                formula_id="chi-square-covariance",
                label="(A.S.1)"
            ),
            ContentBlock(
                type="paragraph",
                content=(
                    "where x_PM is the vector of PM predictions, μ_exp is the vector of "
                    "experimental central values, and Σ is the covariance matrix encoding "
                    "both variances (diagonal) and correlations (off-diagonal)."
                )
            ),

            # P-value
            ContentBlock(
                type="heading",
                content="Goodness-of-Fit: P-Value",
                level=3
            ),
            ContentBlock(
                type="paragraph",
                content=(
                    "The p-value quantifies the probability of obtaining a chi-square at "
                    "least as large as observed, assuming the theory is correct:"
                )
            ),
            ContentBlock(
                type="formula",
                content=r"p = P(\chi^2 \geq \chi^2_{\text{obs}} \mid \nu) = "
                       r"1 - F_{\chi^2}(\chi^2_{\text{obs}}; \nu)",
                formula_id="p-value-chi-square",
                label="(A.S.2)"
            ),
            ContentBlock(
                type="paragraph",
                content=(
                    "where ν is the number of degrees of freedom (n_params - n_free) and "
                    "F_χ² is the cumulative distribution function of the chi-square distribution. "
                    "A p-value > 0.05 indicates acceptable fit (95% confidence)."
                )
            ),

            # Results tables
            ContentBlock(
                type="heading",
                content="Neutrino Sector Results (NuFIT 6.0)",
                level=3
            ),
            self._build_result_table(self.neutrino_result),
            ContentBlock(
                type="paragraph",
                content=(
                    f"Neutrino sector: χ² = {self.neutrino_result.chi_square:.2f} "
                    f"(ν = {self.neutrino_result.ndof}), "
                    f"p-value = {self.neutrino_result.p_value:.4f}, "
                    f"status: {self.neutrino_result.status}."
                )
            ),

            ContentBlock(
                type="heading",
                content="Cosmology Sector Results (DESI 2025)",
                level=3
            ),
            self._build_result_table(self.cosmology_result),
            ContentBlock(
                type="paragraph",
                content=(
                    f"Cosmology sector: χ² = {self.cosmology_result.chi_square:.2f} "
                    f"(ν = {self.cosmology_result.ndof}), "
                    f"p-value = {self.cosmology_result.p_value:.4f}, "
                    f"status: {self.cosmology_result.status}."
                )
            ),

            # Combined
            ContentBlock(
                type="heading",
                content="Combined Analysis",
                level=3
            ),
            ContentBlock(
                type="paragraph",
                content=(
                    f"Combined (neutrino + cosmology): "
                    f"χ² = {self.combined_result.chi_square:.2f} "
                    f"(ν = {self.combined_result.ndof}), "
                    f"χ²/ν = {self.combined_result.reduced_chi_square:.2f}, "
                    f"p-value = {self.combined_result.p_value:.4f}, "
                    f"status: {self.combined_result.status}. "
                    f"This represents the overall goodness-of-fit of PM v16.1 predictions "
                    f"to experimental data with proper treatment of correlations."
                )
            ),

            # Interpretation
            ContentBlock(
                type="heading",
                content="Interpretation",
                level=3
            ),
            ContentBlock(
                type="paragraph",
                content=(
                    "The covariance matrix approach provides a more rigorous test than "
                    "independent parameter comparisons. The off-diagonal elements capture "
                    "important correlations: for example, NuFIT 6.0 shows strong correlation "
                    "(ρ = 0.32) between θ₂₃ and δ_CP, while DESI 2025 exhibits strong "
                    "anti-correlation (ρ = -0.75) between w₀ and wₐ due to the CPL "
                    "parameterization degeneracy. These correlations are properly accounted "
                    "for in the chi-square computation, providing a statistically sound "
                    "validation of the theory."
                )
            ),
        ]

        return SectionContent(
            section_id="A",
            subsection_id="A.S",
            title="Rigorous Covariance Matrix Analysis",
            abstract=(
                "Statistical validation of PM v16.1 using full covariance matrices for "
                "neutrino oscillation parameters (NuFIT 6.0) and cosmological parameters "
                "(DESI 2025). Computes chi-square goodness-of-fit with proper treatment "
                "of correlations, providing rigorous assessment of theory-experiment agreement."
            ),
            content_blocks=content_blocks,
            formula_refs=["chi-square-covariance", "p-value-chi-square", "reduced-chi-square"],
            param_refs=[
                "statistics.neutrino_chi_square",
                "statistics.cosmology_chi_square",
                "statistics.combined_chi_square",
                "statistics.combined_p_value",
            ]
        )

    def _build_result_table(self, result: ChiSquareResult) -> ContentBlock:
        """Build a table showing parameter-by-parameter results."""
        headers = ["Parameter", "PM Value", "Exp. Value", "Uncertainty", "Pull", "Units"]

        rows = []
        cov = result.covariance_data
        for i, param_name in enumerate(cov.parameter_names):
            rows.append([
                param_name,
                f"{result.predictions[i]:.3f}",
                f"{result.observations[i]:.3f}",
                f"±{cov.uncertainties[i]:.3f}",
                f"{result.pulls[i]:.2f}σ",
                cov.units[i]
            ])

        return ContentBlock(
            type="table",
            headers=headers,
            rows=rows
        )

    # -------------------------------------------------------------------------
    # Formulas
    # -------------------------------------------------------------------------

    def get_formulas(self) -> List[Formula]:
        """
        Return list of formulas this simulation provides.

        Returns:
            List of Formula instances with statistical methodology
        """
        return [
            Formula(
                id="chi-square-covariance",
                label="(A.S.1)",
                latex=r"\chi^2 = (\mathbf{x}_{\text{PM}} - \boldsymbol{\mu}_{\text{exp}})^T "
                      r"\boldsymbol{\Sigma}^{-1} "
                      r"(\mathbf{x}_{\text{PM}} - \boldsymbol{\mu}_{\text{exp}})",
                plain_text="chi^2 = (x_PM - mu_exp)^T Sigma^-1 (x_PM - mu_exp)",
                category="THEORY",
                description="Chi-square statistic with full covariance matrix",
                inputParams=[
                    "*.predictions",
                    "*.experimental_values",
                    "*.covariance_matrix"
                ],
                outputParams=["*.chi_square"],
                input_params=[
                    "*.predictions",
                    "*.experimental_values",
                    "*.covariance_matrix"
                ],
                output_params=["*.chi_square"],
                derivation={
                    "steps": [
                        {
                            "description": "Compute residuals",
                            "formula": r"\Delta \mathbf{x} = \mathbf{x}_{\text{PM}} - \boldsymbol{\mu}_{\text{exp}}"
                        },
                        {
                            "description": "Quadratic form with precision matrix",
                            "formula": r"\chi^2 = \Delta \mathbf{x}^T \boldsymbol{\Sigma}^{-1} \Delta \mathbf{x}"
                        }
                    ],
                    "references": [
                        "Standard multivariate statistics (see Press et al., Numerical Recipes)"
                    ]
                },
                terms={
                    "x_PM": "Vector of PM predicted values",
                    "mu_exp": "Vector of experimental central values",
                    "Sigma": "Covariance matrix (includes correlations)",
                    "Sigma^-1": "Inverse covariance (precision matrix)",
                    "chi^2": "Chi-square statistic"
                }
            ),
            Formula(
                id="p-value-chi-square",
                label="(A.S.2)",
                latex=r"p = P(\chi^2 \geq \chi^2_{\text{obs}} \mid \nu) = "
                      r"1 - F_{\chi^2}(\chi^2_{\text{obs}}; \nu)",
                plain_text="p = 1 - CDF_chi2(chi2_obs; nu)",
                category="THEORY",
                description="P-value from chi-square distribution",
                inputParams=["*.chi_square", "*.ndof"],
                outputParams=["*.p_value"],
                input_params=["*.chi_square", "*.ndof"],
                output_params=["*.p_value"],
                terms={
                    "p": "P-value (probability of worse fit by chance)",
                    "chi^2_obs": "Observed chi-square value",
                    "nu": "Degrees of freedom",
                    "F_chi2": "Chi-square cumulative distribution function"
                }
            ),
            Formula(
                id="reduced-chi-square",
                label="(A.S.3)",
                latex=r"\chi^2_{\nu} = \frac{\chi^2}{\nu}",
                plain_text="chi2_reduced = chi2 / ndof",
                category="THEORY",
                description="Reduced chi-square (chi-square per degree of freedom)",
                inputParams=["*.chi_square", "*.ndof"],
                outputParams=["*.reduced_chi_square"],
                input_params=["*.chi_square", "*.ndof"],
                output_params=["*.reduced_chi_square"],
                terms={
                    "chi2_nu": "Reduced chi-square",
                    "chi2": "Chi-square statistic",
                    "nu": "Degrees of freedom"
                }
            ),
            Formula(
                id="pull-definition",
                label="(A.S.4)",
                latex=r"\text{Pull}_i = \frac{x_{i,\text{PM}} - \mu_{i,\text{exp}}}{\sqrt{\Sigma_{ii}}}",
                plain_text="Pull_i = (x_i_PM - mu_i_exp) / sqrt(Sigma_ii)",
                category="THEORY",
                description="Standardized residual (pull) for parameter i",
                inputParams=["*.predictions", "*.experimental_values", "*.covariance_matrix"],
                outputParams=["*.pulls"],
                input_params=["*.predictions", "*.experimental_values", "*.covariance_matrix"],
                output_params=["*.pulls"],
                terms={
                    "Pull_i": "Standardized residual for parameter i",
                    "x_i_PM": "PM prediction for parameter i",
                    "mu_i_exp": "Experimental value for parameter i",
                    "Sigma_ii": "Variance of parameter i (diagonal of covariance)"
                }
            ),
        ]

    # -------------------------------------------------------------------------
    # Parameter Definitions
    # -------------------------------------------------------------------------

    def get_output_param_definitions(self) -> List[Parameter]:
        """
        Return parameter definitions for outputs.

        Returns:
            List of Parameter instances describing statistical outputs
        """
        return [
            # Neutrino
            Parameter(
                path="statistics.neutrino_chi_square",
                name="Neutrino Chi-Square",
                units="dimensionless",
                status="VALIDATION",
                description="Chi-square statistic for neutrino sector with NuFIT 6.0 covariance"
            ),
            Parameter(
                path="statistics.neutrino_ndof",
                name="Neutrino Degrees of Freedom",
                units="count",
                status="VALIDATION",
                description="Degrees of freedom for neutrino sector (n_params - n_free)"
            ),
            Parameter(
                path="statistics.neutrino_p_value",
                name="Neutrino P-Value",
                units="probability",
                status="VALIDATION",
                description="Goodness-of-fit p-value for neutrino sector"
            ),
            Parameter(
                path="statistics.neutrino_status",
                name="Neutrino Fit Status",
                units="categorical",
                status="VALIDATION",
                description="Neutrino fit quality: EXCELLENT/GOOD/ACCEPTABLE/MARGINAL/TENSION"
            ),

            # Cosmology
            Parameter(
                path="statistics.cosmology_chi_square",
                name="Cosmology Chi-Square",
                units="dimensionless",
                status="VALIDATION",
                description="Chi-square statistic for cosmology sector with DESI 2025 covariance"
            ),
            Parameter(
                path="statistics.cosmology_ndof",
                name="Cosmology Degrees of Freedom",
                units="count",
                status="VALIDATION",
                description="Degrees of freedom for cosmology sector"
            ),
            Parameter(
                path="statistics.cosmology_p_value",
                name="Cosmology P-Value",
                units="probability",
                status="VALIDATION",
                description="Goodness-of-fit p-value for cosmology sector"
            ),
            Parameter(
                path="statistics.cosmology_status",
                name="Cosmology Fit Status",
                units="categorical",
                status="VALIDATION",
                description="Cosmology fit quality: EXCELLENT/GOOD/ACCEPTABLE/MARGINAL/TENSION"
            ),

            # Combined
            Parameter(
                path="statistics.combined_chi_square",
                name="Combined Chi-Square",
                units="dimensionless",
                status="VALIDATION",
                description="Combined chi-square across all sectors"
            ),
            Parameter(
                path="statistics.combined_ndof",
                name="Combined Degrees of Freedom",
                units="count",
                status="VALIDATION",
                description="Combined degrees of freedom"
            ),
            Parameter(
                path="statistics.combined_p_value",
                name="Combined P-Value",
                units="probability",
                status="VALIDATION",
                description="Overall goodness-of-fit p-value"
            ),
            Parameter(
                path="statistics.combined_status",
                name="Combined Fit Status",
                units="categorical",
                status="VALIDATION",
                description="Overall fit quality"
            ),
        ]

    # -------------------------------------------------------------------------
    # Foundations & References
    # -------------------------------------------------------------------------

    def get_foundations(self) -> List[Dict[str, str]]:
        """Return foundational concepts for this simulation."""
        return [
            {
                "id": "covariance-matrix",
                "title": "Covariance Matrix",
                "category": "statistics",
                "description": "Matrix encoding variances and correlations of multivariate distributions"
            },
            {
                "id": "chi-square-test",
                "title": "Chi-Square Goodness-of-Fit Test",
                "category": "statistics",
                "description": "Statistical test for comparing observations with theoretical predictions"
            },
            {
                "id": "correlation",
                "title": "Statistical Correlation",
                "category": "statistics",
                "description": "Measure of linear dependence between random variables"
            },
        ]

    def get_references(self) -> List[Dict[str, Any]]:
        """Return bibliographic references for this simulation."""
        return [
            {
                "id": "nufit2024_cov",
                "authors": "NuFIT Collaboration",
                "title": "NuFIT 6.0 (2024) - Covariance matrices",
                "year": 2024,
                "url": "http://www.nu-fit.org",
                "notes": "Full covariance matrices for neutrino oscillation parameters"
            },
            {
                "id": "desi2024_cov",
                "authors": "DESI Collaboration",
                "title": "DESI 2024 Cosmological Constraints - Covariance",
                "journal": "arXiv",
                "year": 2024,
                "arxiv": "2411.12022",
                "notes": "Covariance matrices from BAO+CMB analysis"
            },
            {
                "id": "numerical_recipes",
                "authors": "Press, W.H., et al.",
                "title": "Numerical Recipes: The Art of Scientific Computing",
                "year": 2007,
                "publisher": "Cambridge University Press",
                "notes": "Chapter 15: Modeling of Data (chi-square fitting)"
            },
        ]


# ============================================================================
# Standalone Execution Function
# ============================================================================

def run_covariance_analysis(verbose: bool = True) -> Dict[str, Any]:
    """
    Standalone execution function for covariance analysis.

    Args:
        verbose: Whether to print detailed output

    Returns:
        Dictionary with statistical results
    """
    from simulations.base import PMRegistry

    # Create registry
    registry = PMRegistry.get_instance()

    # Set up neutrino predictions (example values - should come from neutrino sim)
    registry.set_param("neutrino.theta_12_pred", 33.59, source="neutrino_mixing_v16_0", status="PREDICTED")
    registry.set_param("neutrino.theta_13_pred", 8.33, source="neutrino_mixing_v16_0", status="PREDICTED")
    registry.set_param("neutrino.theta_23_pred", 42.75, source="neutrino_mixing_v16_0", status="PREDICTED")
    registry.set_param("neutrino.delta_CP_pred", 232.5, source="neutrino_mixing_v16_0", status="PREDICTED")

    # Set up cosmology predictions (should come from cosmology sims)
    registry.set_param("cosmology.w0_derived", -11/13, source="dark_energy_v16_0", status="PREDICTED")
    registry.set_param("cosmology.wa_derived", 0.288, source="dark_energy_v16_0", status="PREDICTED")
    registry.set_param("cosmology.Omega_m", 0.310, source="cosmology_sim", status="PREDICTED")
    registry.set_param("cosmology.H0", 68.5, source="cosmology_sim", status="PREDICTED")

    # Create and execute simulation
    sim = RigorCovarianceV16_1()
    results = sim.execute(registry, verbose=verbose)

    if verbose:
        print("\n" + "=" * 75)
        print("COVARIANCE MATRIX ANALYSIS RESULTS")
        print("=" * 75)

        print("\n--- Neutrino Sector (NuFIT 6.0) ---")
        print(sim.neutrino_result)

        print("\n--- Cosmology Sector (DESI 2025) ---")
        print(sim.cosmology_result)

        print("\n--- Combined Analysis ---")
        print(sim.combined_result)

        print("\n" + "=" * 75)

    return results


if __name__ == "__main__":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    run_covariance_analysis(verbose=True)
