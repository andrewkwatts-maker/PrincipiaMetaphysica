# Simulations Package - File Index

## Quick Navigation

- **[SIMULATIONS_README.md](SIMULATIONS_README.md)** - Complete usage guide and documentation
- **[simulations_manifest.json](simulations_manifest.json)** - Detailed file manifest with metadata
- **[EXPORT_SUMMARY.txt](EXPORT_SUMMARY.txt)** - Package export summary and verification

## Main Entry Points

- **[run_all_simulations.py](run_all_simulations.py)** - Run all 30 simulations
- **[config.py](config.py)** - Physics constants and configuration

## Core Framework

### Base Classes (`base/`)
- `simulation_base.py` - Abstract base class for all simulations
- `registry.py` - Simulation registration and discovery
- `established.py` - Established physics validations
- `validator.py` - Validation framework
- `schema.py` - Data schemas and structures
- `formulas.py` - Formula management system
- `sections.py` - Section organization
- `injector.py` - Dependency injection

## Simulations by Domain

### Gauge Theory (`v16/gauge/`)
- `gauge_unification_v16_0.py` - SU(3)×SU(2)×U(1) unification at MX

### Higgs Physics (`v16/higgs/`)
- `higgs_mass_v16_0.py` - Higgs mass prediction (125.35 GeV)

### Fermion Physics (`v16/fermion/`)
- `chirality_v16_0.py` - Chiral fermion structure
- `ckm_matrix_v16_0.py` - CKM quark mixing matrix
- `fermion_generations_v16_0.py` - Three generations from G2 topology

### Neutrino Physics (`v16/neutrino/`)
- `neutrino_mixing_v16_0.py` - Neutrino mixing angles and masses

### Proton Decay (`v16/proton/`)
- `proton_decay_v16_0.py` - Proton lifetime prediction

### Cosmology (`v16/cosmology/`)
- `cosmology_intro_v16_0.py` - Cosmological framework introduction
- `multi_sector_v16_0.py` - Multi-sector cosmological dynamics
- `dark_energy_v16_0.py` - Dark energy mechanism
- `s8_suppression_v16_1.py` - S8 tension resolution
- `jacobian_mathematical_validation.py` - Mathematical validation
- `test_jacobian_analysis.py` - Jacobian analysis tests
- `test_complete_validation.py` - Complete validation tests

### Geometric Framework (`v16/geometric/`)
- `g2_geometry_v16_0.py` - G2 manifold geometry
- `g2_ricci_flow_rigorous.py` - Ricci flow analysis

### Pneuma Mechanism (`v16/pneuma/`)
- `pneuma_mechanism_v16_0.py` - Consciousness-matter coupling

### Thermal Physics (`v16/thermal/`)
- `thermal_time_v16_0.py` - Thermal time emergence

### Introduction & Discussion (`v16/introduction/`, `v16/discussion/`)
- `introduction_v16_0.py` - Theory introduction and overview
- `discussion_v16_0.py` - Discussion and implications

### Predictions (`v16/predictions/`)
- `predictions_aggregator_v16_0.py` - Aggregated predictions across domains

### Mathematical Appendices (`v16/appendices/`)
- `appendix_a_math_v16_0.py` - Mathematical foundations
- `appendix_b_methods_v16_0.py` - Computational methods
- `appendix_c_derivations_v16_0.py` - Detailed derivations
- `appendix_d_tables_v16_0.py` - Reference tables
- `appendix_e_proton_v16_0.py` - Proton decay calculations
- `appendix_f_v16_0.py` - Additional mathematical details
- `appendix_g_v16_0.py` - Further derivations
- `appendix_h_v16_0.py` - Supplementary mathematics
- `appendix_i_v16_0.py` - Extended calculations
- `appendix_j_v16_0.py` - Advanced topics
- `appendix_k_v16_0.py` - Special cases
- `appendix_l_v16_0.py` - Numerical methods
- `appendix_m_v16_0.py` - Statistical analysis
- `appendix_n_v16_0.py` - Error analysis

### Validation Framework (`v16/validation/`)
- `rigorous_validator_v16_1.py` - Advanced validation with covariance
- `example_usage.py` - Validation usage examples

### Statistical Tools (`v16/statistics/`)
- `rigor_covariance_v16_1.py` - Covariance matrix analysis
- `test_covariance_data.py` - Covariance testing
- `example_integration.py` - Integration examples

## Experimental Data

### Data Files (`data/experimental/`)
- `pdg_2024_values.json` - Particle Data Group 2024 values
- `nufit_6_0_parameters.json` - NuFIT 6.0 neutrino parameters
- `nufit_6_0_covariance.json` - NuFIT 6.0 covariance matrix
- `desi_2025_constraints.json` - DESI 2025 cosmological constraints

## Test Suite

### Tests (`tests/`)
- `test_registry.py` - Registry system tests
- `test_gauge_invariance.py` - Gauge invariance tests
- `test_data_loader.py` - Data loading tests
- `conftest.py` - Test configuration

## Statistics

- **Total Files:** 79
- **Python Files:** 73
- **JSON Data Files:** 4
- **Total Lines:** 47,003
- **Total Simulations:** 30
- **Domains Covered:** 13
- **Package Size:** 2.2 MB

## Usage Examples

### Run All Simulations
```bash
python run_all_simulations.py
```

### Run Specific Simulation
```python
from simulations.v16.gauge.gauge_unification_v16_0 import GaugeUnificationV16_0
sim = GaugeUnificationV16_0()
result = sim.run()
```

### Run Tests
```bash
pytest tests/
```

## Documentation Hierarchy

1. **INDEX.md** (this file) - Quick navigation
2. **SIMULATIONS_README.md** - Detailed usage guide
3. **simulations_manifest.json** - Complete file metadata
4. **EXPORT_SUMMARY.txt** - Export verification

---

**Last Updated:** 2025-12-29
**Package Version:** 1.0.0
