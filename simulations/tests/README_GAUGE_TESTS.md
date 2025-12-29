# Gauge Invariance Test Suite

## Overview

Comprehensive test suite for verifying gauge invariance, symmetry structure, and anomaly cancellation in the Principia Metaphysica theory. The tests validate the theoretical consistency of the gauge sector from G2 holonomy down to the Standard Model.

## Test Coverage

### 1. Gauge Group Structure (`TestGaugeGroupStructure`)

Tests the fundamental gauge group structure and GUT embeddings.

#### `test_gauge_coupling_unification_at_gut_scale`
- **Physics**: Verifies that gauge couplings unify at M_GUT ≈ 2×10^16 GeV
- **Tests**: α_GUT ≈ 1/24 from G2 topology (b₃ = 24)
- **Tolerance**: <10% deviation from topological prediction

#### `test_gauge_group_dimension_consistency`
- **Physics**: Validates group dimensions for SM → SU(5) → SO(10) chain
- **Tests**:
  - dim[SU(3)×SU(2)×U(1)] = 12
  - dim[SU(5)] = 24
  - dim[SO(10)] = 45
- **Ensures**: Proper subgroup embeddings

#### `test_g2_holonomy_to_su3_embedding`
- **Physics**: G2 holonomy reduces to SU(3) color gauge group
- **Tests**:
  - G2 dimension = 14, rank = 2
  - SU(3) dimension = 8, rank = 2 (maximal embedding)
  - b₃ = 24 from TCS G2 manifold

#### `test_so10_fermion_representation`
- **Physics**: SO(10) 16-spinor contains one generation of SM fermions
- **Tests**: 16 = (3,2,1/6) + (3̄,1,-2/3) + (3̄,1,1/3) + (1,2,-1/2) + (1,1,1) + (1,1,0)
- **Validates**: Complete fermion content including right-handed neutrinos

### 2. Symmetry Breaking Chain (`TestSymmetryBreakingChain`)

Tests the cascade of symmetry breaking from GUT to electroweak scale.

#### `test_gut_symmetry_breaking_scale`
- **Physics**: SO(10) → SU(3)×SU(2)×U(1) at M_GUT
- **Tests**:
  - M_GUT > 10^15 GeV
  - Proton lifetime τ_p > 1.6×10^34 years (Super-K bound)
- **Formula**: τ_p ∝ M_GUT^4 / (α_GUT^2 × m_p^5)

#### `test_electroweak_symmetry_breaking`
- **Physics**: SU(2)×U(1) → U(1)_EM at v_EW = 246 GeV
- **Tests**:
  - W and Z boson masses from Higgs VEV
  - Relation: m_Z = m_W / cos(θ_W)
  - Higgs mass stability: 124.5 < m_H < 126.0 GeV

#### `test_quantum_number_conservation_at_breaking`
- **Physics**: Quantum numbers conserved in SO(10) → SM decomposition
- **Tests**: Each fermion representation has consistent Q = T³ + Y
- **Validates**: 16-dimensional representation completeness

#### `test_weak_mixing_angle_running`
- **Physics**: sin²θ_W runs from 3/8 (GUT) to 0.2312 (M_Z)
- **Tests**:
  - SO(10) prediction: sin²θ_W(M_GUT) = 3/8
  - PDG measurement: sin²θ_W(M_Z) = 0.2312
- **Validates**: RG running direction is correct

### 3. Anomaly Cancellation (`TestAnomalyCancellation`)

Tests that all gauge anomalies vanish for quantum consistency.

#### `test_triangle_anomaly_cancellation_U1`
- **Physics**: U(1)_Y³ triangle anomaly must vanish
- **Formula**: A_Y³ = Σ_f n_f Y_f³ = 0
- **Tests**: Contribution from quarks cancels leptons
- **Precision**: |A_Y³| < 10^-10

#### `test_triangle_anomaly_cancellation_SU2_U1`
- **Physics**: SU(2)²×U(1)_Y mixed anomaly must vanish
- **Formula**: A_SU2²_U1 = Σ_f T(R_f) Y_f = 0
- **Tests**: Only SU(2) doublets contribute
- **Precision**: |A_SU2²_U1| < 10^-10

#### `test_gravitational_anomaly_cancellation`
- **Physics**: Gravitational anomaly (chiral fermions)
- **Formula**: A_grav = n_left - n_right = 0
- **Tests**: Each generation has 8 left + 8 right = 16 total
- **Requires**: Right-handed neutrinos (unique to SO(10))

#### `test_so10_automatic_anomaly_cancellation`
- **Physics**: SO(10) representations automatically cancel all anomalies
- **Tests**:
  - Spinor dimension = 2^(n/2-1) = 16 for SO(10)
  - Three generations = 3 × 16 = 48 fermions
- **Feature**: No fine-tuning needed for anomaly cancellation

### 4. Hypercharge Quantization (`TestHyperchargeQuantization`)

Tests proper quantization of U(1)_Y hypercharge.

#### `test_hypercharge_quantization_condition`
- **Physics**: Hypercharge must be rational for GUT embedding
- **Tests**: All Y values are n/d with small denominators
- **Values**: Y ∈ {0, ±1/6, ±1/3, ±1/2, ±2/3, 1}

#### `test_hypercharge_and_charge_consistency`
- **Physics**: Q = T³ + Y (Gell-Mann-Nishijima formula)
- **Tests**:
  - Quarks: Q ∈ {-1/3, 2/3}
  - Leptons: Q ∈ {-1, 0}
- **Precision**: |Q_computed - Q_expected| < 10^-10

#### `test_hypercharge_normalization_in_gut`
- **Physics**: GUT normalization Y_GUT = √(3/5) × Y_SM
- **Tests**: Normalization factor for SU(5) embedding
- **Validates**: α₁ = (5/3) α_em / cos²θ_W

### 5. RG Invariance (`TestGaugeInvarianceUnderRGEvolution`)

Tests gauge invariance under renormalization group evolution.

#### `test_beta_function_coefficients`
- **Physics**: 1-loop beta coefficients from SM particle content
- **Values**:
  - b₁ = 41/10 (U(1)_Y increases with energy)
  - b₂ = -19/6 (SU(2)_L decreases)
  - b₃ = -7 (SU(3)_c decreases - asymptotic freedom)

#### `test_asymptotic_freedom_su3`
- **Physics**: QCD coupling decreases at high energy
- **Formula**: b₃ = 11 - 2n_f/3 = 11 - 4 = 7
- **Tests**: n_f = 6 quark flavors
- **Result**: b₃ > 0 confirms asymptotic freedom

#### `test_gauge_coupling_threshold_corrections`
- **Physics**: KK tower corrections at M_* ≈ 5 TeV
- **Formula**: Δ(1/α_i) = (k_i h^{1,1})/(2π) log(M_GUT/M_*)
- **Tests**:
  - h^{1,1} = 24 (TCS G2 Hodge number)
  - Corrections are O(100) from large log ratio
  - All corrections positive (as expected)

## Running the Tests

### Run all gauge tests:
```bash
cd h:\Github\PrincipiaMetaphysica
python -m pytest simulations/tests/test_gauge_invariance.py -v
```

### Run specific test class:
```bash
pytest simulations/tests/test_gauge_invariance.py::TestAnomalyCancellation -v
```

### Run with coverage:
```bash
pytest simulations/tests/test_gauge_invariance.py --cov=simulations.base --cov-report=html
```

### Run only tests with specific marker:
```bash
pytest -m gauge -v
```

## Test Results Summary

- **Total Tests**: 18
- **Test Classes**: 5
- **Coverage Areas**:
  - Gauge group structure and embeddings
  - Symmetry breaking chain (GUT → SM → EW)
  - Triangle and gravitational anomaly cancellation
  - Hypercharge quantization and consistency
  - RG evolution and threshold corrections

## Physics Validation

All tests validate core predictions of Principia Metaphysica:

1. **G2 → SO(10) → SM**: Gauge group emerges naturally from G2 holonomy
2. **α_GUT ≈ 1/24**: Unified coupling tied to b₃ = 24 (topological)
3. **M_GUT ≈ 2×10^16 GeV**: GUT scale from torsion and moduli stabilization
4. **Anomaly-free**: SO(10) automatically satisfies all anomaly cancellation conditions
5. **Right-handed neutrinos**: Required for gravitational anomaly cancellation
6. **Threshold corrections**: KK tower states modify gauge running at M_* ≈ 5 TeV

## Dependencies

- `pytest` >= 8.4.1
- `numpy` >= 1.24.0
- `simulations.base.PMRegistry`
- `simulations.base.EstablishedPhysics`

## References

1. **Langacker (1981)**: "Grand Unified Theories and Proton Decay", Phys. Rep. 72, 185
2. **PDG 2024**: Particle Data Group experimental values
3. **Joyce (2007)**: "Riemannian Holonomy Groups and Calibrated Geometry"
4. **TCS G2 Manifold**: Third Betti number b₃ = 24 for manifold #187

## Notes

- Tests use ESTABLISHED physics values from PDG 2024, NuFIT 6.0
- Registry fixtures create fresh instances to avoid parameter conflicts
- All numerical precision tests use tolerance < 10^-10 for exact quantities
- Approximate tests (e.g., GUT unification) use ~10% tolerance

## Author

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.
