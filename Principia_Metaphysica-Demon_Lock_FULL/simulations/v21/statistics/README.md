# Statistics Module - Covariance Matrix Analysis

## Overview

This module implements rigorous statistical validation of Principia Metaphysica v16.1 predictions using **full covariance matrices** that properly account for correlated parameter uncertainties. This is a significant improvement over independent parameter comparisons, which ignore correlations and can lead to incorrect statistical conclusions.

## Key Features

### 1. Covariance Matrix Handling
- **NuFIT 6.0**: 4×4 covariance matrix for neutrino oscillation parameters (θ₁₂, θ₁₃, θ₂₃, δ_CP)
- **DESI 2025**: 4×4 covariance matrix for cosmological parameters (w₀, wₐ, Ωₘ, H₀)
- Proper treatment of correlations (e.g., ρ(θ₂₃, δ_CP) = 0.32, ρ(w₀, wₐ) = -0.75)

### 2. Chi-Square Computation
```
χ² = (x - μ)ᵀ Σ⁻¹ (x - μ)
```
where:
- `x` = predicted values (from PM theory)
- `μ` = experimental central values
- `Σ` = covariance matrix
- `Σ⁻¹` = inverse covariance (precision matrix)

### 3. Goodness-of-Fit Metrics
- **Chi-square**: Total χ² value
- **Degrees of freedom**: n_params - n_free_params
- **P-value**: Probability of obtaining χ² ≥ observed by chance
- **Reduced chi-square**: χ²/ndof (should be ≈ 1 for good fit)
- **Status classification**: EXCELLENT / GOOD / ACCEPTABLE / MARGINAL / TENSION

## File Structure

```
simulations/v21/statistics/
├── __init__.py                      # Module exports
├── rigor_covariance_v16_1.py        # Main covariance analysis simulation
└── README.md                        # This file

simulations/data/experimental/
├── nufit_6_0_covariance.json        # NuFIT 6.0 covariance matrices
├── nufit_6_0_parameters.json        # NuFIT 6.0 central values
├── desi_2025_constraints.json       # DESI 2025 cosmological constraints
└── pdg_2024_values.json             # PDG particle physics values
```

## Covariance Data Format

The `nufit_6_0_covariance.json` file contains:

1. **Parameters**: Central values and uncertainties
2. **Correlation Matrix**: Dimensionless coefficients ρ ∈ [-1, 1]
   - Diagonal: all 1.0 (perfect self-correlation)
   - Off-diagonal: correlation between pairs
3. **Covariance Matrix**: Computed as Cov[i,j] = ρ[i,j] × σᵢ × σⱼ
4. **Inverse Covariance**: Precision matrix for χ² calculation
5. **Eigensystem**: Principal directions of parameter correlations

### Example: Neutrino Correlation Matrix (Normal Ordering)

```json
{
  "parameters_order": ["theta_12", "theta_13", "theta_23", "delta_CP"],
  "matrix": [
    [1.0000,  0.0200, -0.0100,  0.0050],
    [0.0200,  1.0000,  0.0800, -0.1500],
    [-0.0100, 0.0800,  1.0000,  0.3200],
    [0.0050, -0.1500,  0.3200,  1.0000]
  ]
}
```

**Key correlations**:
- θ₂₃ vs δ_CP: **ρ = 0.32** (strong positive correlation)
- θ₁₃ vs δ_CP: **ρ = -0.15** (moderate negative correlation)
- θ₁₂ vs θ₁₃: **ρ = 0.02** (negligible correlation)

## Usage

### Standalone Execution

```bash
cd /h/Github/PrincipiaMetaphysica
python simulations/v21/statistics/rigor_covariance_v16_1.py
```

### Python API

```python
from simulations.v16.statistics import RigorCovarianceV16_1, run_covariance_analysis
from simulations.base import PMRegistry

# Method 1: Direct execution
results = run_covariance_analysis(verbose=True)

# Method 2: Full control
registry = PMRegistry.get_instance()

# Set predictions
registry.set_param("neutrino.theta_12_pred", 33.59, source="neutrino_mixing_v16_0")
registry.set_param("neutrino.theta_13_pred", 8.33, source="neutrino_mixing_v16_0")
registry.set_param("neutrino.theta_23_pred", 42.75, source="neutrino_mixing_v16_0")
registry.set_param("neutrino.delta_CP_pred", 232.5, source="neutrino_mixing_v16_0")

registry.set_param("cosmology.w0_derived", -0.846, source="dark_energy_v16_0")
registry.set_param("cosmology.wa_derived", 0.288, source="dark_energy_v16_0")
registry.set_param("cosmology.Omega_m", 0.310, source="cosmology_sim")
registry.set_param("cosmology.H0", 68.5, source="cosmology_sim")

# Run analysis
sim = RigorCovarianceV16_1()
results = sim.execute(registry, verbose=True)

# Access results
print(f"Neutrino χ² = {results['statistics.neutrino_chi_square']:.2f}")
print(f"Neutrino p-value = {results['statistics.neutrino_p_value']:.4f}")
print(f"Combined status: {results['statistics.combined_status']}")
```

## Output Parameters

The simulation produces the following registry parameters:

### Neutrino Sector
- `statistics.neutrino_chi_square`: χ² value for neutrino parameters
- `statistics.neutrino_ndof`: Degrees of freedom (4 for NuFIT)
- `statistics.neutrino_p_value`: Goodness-of-fit p-value
- `statistics.neutrino_status`: Fit quality classification

### Cosmology Sector
- `statistics.cosmology_chi_square`: χ² value for cosmological parameters
- `statistics.cosmology_ndof`: Degrees of freedom (4 for DESI)
- `statistics.cosmology_p_value`: Goodness-of-fit p-value
- `statistics.cosmology_status`: Fit quality classification

### Combined
- `statistics.combined_chi_square`: Sum of neutrino + cosmology χ²
- `statistics.combined_ndof`: Sum of degrees of freedom
- `statistics.combined_p_value`: Overall goodness-of-fit
- `statistics.combined_status`: Overall fit quality

## Interpretation

### Status Classifications

| Status | Reduced χ² | Interpretation |
|--------|-----------|----------------|
| **EXCELLENT** | < 1.5 | Exceptional agreement with data |
| **GOOD** | 1.5 - 2.0 | Good agreement, minor tensions possible |
| **ACCEPTABLE** | 2.0 - 3.0 | Acceptable fit, some parameter tensions |
| **MARGINAL** | 3.0 - 5.0 | Marginal fit, significant tensions |
| **TENSION** | > 5.0 | Poor fit, major discrepancies |

### P-Value Interpretation

- **p > 0.05**: Null hypothesis not rejected (95% confidence)
- **0.01 < p < 0.05**: Marginal evidence against null hypothesis
- **p < 0.01**: Strong evidence against null hypothesis

### Correlations Matter!

**Example**: Suppose θ₂₃ and δ_CP are both 1σ off from experiment:
- **Without correlations**: χ² = 1² + 1² = 2.0
- **With ρ = 0.32**: χ² ≈ 1.6 (correlations reduce tension!)

The covariance approach correctly accounts for this, preventing over-estimation of tensions.

## Mathematical Details

### Chi-Square Formula

For n parameters with covariance matrix Σ:

```
χ² = Σᵢ Σⱼ (xᵢ - μᵢ) (Σ⁻¹)ᵢⱼ (xⱼ - μⱼ)
```

In matrix form:
```
χ² = Δxᵀ Σ⁻¹ Δx
```

where Δx = x - μ is the residual vector.

### Covariance Construction

From correlation matrix ρ and uncertainties σ:

```
Σᵢⱼ = ρᵢⱼ × σᵢ × σⱼ
```

### P-Value from Chi-Square

```
p = P(χ² ≥ χ²_obs | H₀) = 1 - F_χ²(χ²_obs; ν)
```

where F_χ² is the chi-square CDF with ν degrees of freedom.

## Data Sources

1. **NuFIT 6.0 (2024)**
   - Website: http://www.nu-fit.org/
   - Paper: arXiv:2111.03086
   - Global fit of neutrino oscillation data
   - Includes T2K, NOvA, Super-K, Daya Bay, RENO, Double Chooz

2. **DESI 2025**
   - Paper: arXiv:2411.12022
   - Dark Energy Spectroscopic Instrument
   - BAO + CMB + PantheonPlus analysis
   - CPL parameterization: w(a) = w₀ + wₐ(1 - a)

## Validation

The covariance matrices have been validated for:
- ✓ Symmetry: Σ = Σᵀ
- ✓ Positive definiteness: all eigenvalues > 0
- ✓ Correlation diagonal: ρᵢᵢ = 1.0 for all i
- ✓ Correlation bounds: -1 ≤ ρᵢⱼ ≤ 1 for all i,j
- ✓ Consistency: Σ computed from ρ and σ matches published values

## Future Extensions

Potential improvements:
1. **Planck 2025**: Add CMB covariance matrix for Ωₘ, H₀, σ₈
2. **Cross-sector correlations**: Include neutrino-cosmology correlations (e.g., Σ_mν vs Ωₘ)
3. **Profile likelihood**: Marginalize over nuisance parameters
4. **Bayesian analysis**: Compute posterior probabilities, Bayes factors
5. **Monte Carlo**: Generate parameter samples from covariance matrices

## References

1. **NuFIT Collaboration** (2024). "NuFIT 6.0: Global neutrino oscillation fit". http://www.nu-fit.org/
2. **DESI Collaboration** (2024). "DESI 2024 VII: Cosmological Constraints from Full-Shape Analysis". arXiv:2411.12022
3. **Press et al.** (2007). "Numerical Recipes: The Art of Scientific Computing". Cambridge University Press. Chapter 15: Modeling of Data.
4. **PDG** (2024). "Review of Particle Physics". Particle Data Group. Section on Statistics.

## Copyright

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.

Part of the Principia Metaphysica project.
