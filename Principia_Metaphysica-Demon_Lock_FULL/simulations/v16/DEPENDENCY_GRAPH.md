# v16 Simulation Dependency Graph

This document provides a comprehensive dependency analysis of all v16 simulations, showing what depends on what and the execution order.

---

## Visual Dependency Graph

```
                    ┌─────────────────────────────────────┐
                    │     ESTABLISHED PHYSICS             │
                    │  • PDG 2024                         │
                    │  • NuFIT 6.0                        │
                    │  • TCS Topology #187                │
                    │  • Physical Constants               │
                    │  • Experimental Bounds              │
                    └───────────────┬─────────────────────┘
                                    │
                    ┌───────────────┴───────────────┐
                    │                               │
            ┌───────▼────────┐              ┌──────▼──────┐
            │  Introduction  │              │ Appendix A  │
            │   Section 1    │              │    Math     │
            └────────────────┘              └─────────────┘
                    │
        ┌───────────┴───────────┬─────────────────┐
        │                       │                 │
   ┌────▼─────┐         ┌──────▼──────┐    ┌────▼─────┐
   │ G2 Geom  │         │   Pneuma    │    │  Gauge   │
   │ Sec 2.1  │         │   Sec 2.2   │    │  Sec 3   │
   │          │         │             │    │          │
   │ K_MATCH  │         │ vev, coupling│   │ M_GUT    │
   │ vol_g2   │         │ mass_scale  │    │ ALPHA_GUT│
   └────┬─────┘         └──────┬──────┘    └────┬─────┘
        │                      │                │
        └──────────┬───────────┴────────────────┘
                   │
       ┌───────────┼───────────┬─────────────┬─────────────┐
       │           │           │             │             │
  ┌────▼────┐ ┌───▼────┐ ┌───▼─────┐ ┌─────▼─────┐ ┌────▼─────┐
  │Chirality│ │Fermion │ │   CKM   │ │   Higgs   │ │ Neutrino │
  │ Sec 4.1 │ │ Gen    │ │ Sec 4.3 │ │  Sec 4.4  │ │ Sec 4.5  │
  │         │ │Sec 4.2 │ │         │ │           │ │          │
  └─────────┘ └────────┘ └─────────┘ └───────────┘ └────┬─────┘
       │           │           │             │            │
       └───────────┴───────────┴─────────────┴────────────┘
                                    │
                              ┌─────▼──────┐
                              │   Proton   │
                              │  Sec 4.6   │
                              │  Decay     │
                              └─────┬──────┘
                                    │
       ┌────────────────────────────┼─────────────────────────┐
       │                            │                         │
  ┌────▼────────┐          ┌────────▼────────┐      ┌────────▼────────┐
  │  Cosmo      │          │  Dark Energy    │      │  Multi-Sector   │
  │  Intro      │          │    Sec 5.2      │      │    Sec 5.3      │
  │  Sec 5.1    │          │                 │      │                 │
  └─────────────┘          └─────────────────┘      └─────────────────┘
       │                            │                         │
       └────────────────────────────┼─────────────────────────┘
                                    │
                              ┌─────▼──────┐
                              │  Thermal   │
                              │   Time     │
                              │  Sec 5.4   │
                              └─────┬──────┘
                                    │
                    ┌───────────────┼───────────────┐
                    │               │               │
             ┌──────▼──────┐  ┌────▼────┐   ┌──────▼──────┐
             │ Predictions │  │Discussion│   │ Appendix B  │
             │   Sec 6     │  │  Sec 7  │   │   Methods   │
             └─────────────┘  └─────────┘   └─────────────┘
                    │               │               │
                    └───────────────┼───────────────┘
                                    │
                    ┌───────────────┴───────────────┐
                    │                               │
             ┌──────▼──────┐               ┌────────▼────────┐
             │ Appendix C  │               │   Appendix D    │
             │ Derivations │               │     Tables      │
             └─────────────┘               └─────────────────┘
```

---

## Dependency Tiers

### Tier 0: Foundation (No dependencies)
- **ESTABLISHED Physics**: PDG, NuFIT, TCS topology, constants
- **Introduction**: Section 1
- **Appendix A**: Mathematical foundations

### Tier 1: Geometric & Gauge Foundation
Depends only on ESTABLISHED physics.

1. **G2GeometrySimulation** (Section 2.1)
   - Inputs: `topology.chi_eff`, `topology.b3`
   - Outputs: `topology.K_MATCHING`, `geometry.vol_g2`, calibration norms

2. **PneumaMechanismSimulation** (Section 2.2)
   - Inputs: `constants.M_PLANCK`, `pdg.m_higgs`, (optional) `topology.chi_eff`, `topology.b3`
   - Outputs: `pneuma.vev`, `pneuma.coupling`, `pneuma.mass_scale`

3. **GaugeUnificationSimulation** (Section 3)
   - Inputs: `pdg.alpha_s_MZ`, `pdg.sin2_theta_W`, `pdg.m_Z`, `constants.M_PLANCK`
   - Outputs: `gauge.M_GUT`, `gauge.ALPHA_GUT`, threshold corrections

### Tier 2: Fermion & Particle Physics
Depends on Tier 1 outputs.

4. **ChiralitySimulation** (Section 4.1)
   - Inputs: `topology.b3`, `topology.chi_eff` (from G2Geometry)
   - Outputs: `fermion.chirality_mechanism`, `fermion.z2_filter`

5. **FermionGenerationsSimulation** (Section 4.2)
   - Inputs: `topology.b3`, `topology.chi_eff` (from G2Geometry)
   - Outputs: `fermion.n_generations`, `fermion.generation_mechanism`

6. **CKMMatrixSimulation** (Section 4.3)
   - Inputs: `topology.b3`, `topology.chi_eff`, `geometry.associative_norm` (from G2Geometry)
   - Outputs: `ckm.theta_12`, `ckm.theta_13`, `ckm.theta_23`, `ckm.delta_cp`

7. **HiggsMassSimulation** (Section 4.4)
   - Inputs: `topology.CHI_EFF`, `topology.B3`, `gauge.g_gut` (from Gauge)
   - Outputs: `higgs.m_higgs_pred`, `higgs.vev`, `higgs.lambda_eff`

8. **NeutrinoMixingSimulation** (Section 4.5)
   - Inputs: `pdg.theta_23_best`, `topology.b3`, `topology.chi_eff` (from G2Geometry)
   - Outputs: `neutrino.theta_23`, `neutrino.delta_m_sq_23`, mixing parameters

9. **ProtonDecaySimulation** (Section 4.6)
   - Inputs: `gauge.M_GUT`, `gauge.ALPHA_GUT` (from Gauge), `topology.K_MATCHING` (from G2Geometry)
   - Outputs: `proton_decay.tau_p_years`, `proton_decay.suppression_factor`

### Tier 3: Cosmology
Depends on Tier 1 and Tier 2 outputs.

10. **CosmologyIntroSimulation** (Section 5.1)
    - Inputs: (narrative only, minimal dependencies)
    - Outputs: Framework overview

11. **DarkEnergySimulation** (Section 5.2)
    - Inputs: `pneuma.vev`, `pneuma.coupling` (from Pneuma), `pdg.omega_lambda`
    - Outputs: `cosmology.w_de`, `cosmology.rho_de`

12. **MultiSectorCosmologySimulation** (Section 5.3)
    - Inputs: `gauge.M_GUT` (from Gauge), `topology.chi_eff` (from G2Geometry), `pdg.omega_m`, `pdg.H0`
    - Outputs: `cosmology.omega_dm`, `cosmology.hubble_tension`, `cosmology.sigma_8_tension`

13. **ThermalTimeSimulation** (Section 5.4)
    - Inputs: `pneuma.vev` (from Pneuma), `topology.vol_g2` (from G2Geometry)
    - Outputs: `thermal.time_parameter`, `thermal.modular_weight`

### Tier 4: Synthesis & Documentation
Depends on all previous tiers.

14. **PredictionsAggregatorSimulation** (Section 6)
    - Inputs: All computed predictions from Tiers 1-3
    - Outputs: Aggregated predictions, experimental signatures

15. **DiscussionSimulation** (Section 7)
    - Inputs: All results from Tiers 1-3
    - Outputs: Interpretation, comparison, future directions

16. **AppendixBMethodsSimulation** (Appendix B)
    - Inputs: Computational methods from all simulations
    - Outputs: Methods documentation

17. **AppendixCDerivationsSimulation** (Appendix C)
    - Inputs: All formulas and derivations
    - Outputs: Detailed derivation documentation

18. **AppendixDTablesSimulation** (Appendix D)
    - Inputs: All computed parameters
    - Outputs: Comprehensive tables

---

## Detailed Dependency Matrix

| Simulation | Depends On (Simulations) | Depends On (Parameters) | Provides |
|------------|-------------------------|------------------------|----------|
| **Introduction** | None | None | Framework overview |
| **G2Geometry** | None | `topology.chi_eff`, `topology.b3` (ESTABLISHED) | `topology.K_MATCHING`, `geometry.vol_g2`, calibrations |
| **Pneuma** | None | `constants.M_PLANCK`, `pdg.m_higgs` | `pneuma.vev`, `pneuma.coupling`, `pneuma.mass_scale` |
| **GaugeUnification** | None | `pdg.alpha_s_MZ`, `pdg.sin2_theta_W`, `pdg.m_Z` | `gauge.M_GUT`, `gauge.ALPHA_GUT` |
| **Chirality** | G2Geometry | `topology.b3`, `topology.chi_eff` | `fermion.chirality_mechanism` |
| **FermionGenerations** | G2Geometry | `topology.b3`, `topology.chi_eff` | `fermion.n_generations` |
| **CKMMatrix** | G2Geometry | `topology.b3`, `geometry.associative_norm` | `ckm.*` mixing angles |
| **HiggsMass** | G2Geometry, GaugeUnification | `topology.CHI_EFF`, `gauge.g_gut` | `higgs.m_higgs_pred`, `higgs.vev` |
| **NeutrinoMixing** | G2Geometry | `topology.b3`, `topology.chi_eff`, `pdg.theta_23_best` | `neutrino.*` mixing parameters |
| **ProtonDecay** | G2Geometry, GaugeUnification | `gauge.M_GUT`, `topology.K_MATCHING` | `proton_decay.tau_p_years` |
| **CosmologyIntro** | None | None | Framework narrative |
| **DarkEnergy** | Pneuma | `pneuma.vev`, `pneuma.coupling` | `cosmology.w_de`, `cosmology.rho_de` |
| **MultiSector** | G2Geometry, GaugeUnification | `gauge.M_GUT`, `topology.chi_eff` | `cosmology.omega_dm`, tension resolutions |
| **ThermalTime** | Pneuma, G2Geometry | `pneuma.vev`, `topology.vol_g2` | `thermal.*` parameters |
| **Predictions** | All Tier 1-3 | All computed values | Aggregated predictions |
| **Discussion** | All Tier 1-3 | All computed values | Interpretation |
| **Appendix A** | None | None | Mathematical foundations |
| **Appendix B** | All | All methods | Methods documentation |
| **Appendix C** | All | All formulas | Detailed derivations |
| **Appendix D** | All | All parameters | Comprehensive tables |

---

## Execution Order

### Recommended Execution Order

To ensure all dependencies are satisfied, execute simulations in this order:

```python
# Tier 0: Foundation
1. Load ESTABLISHED physics
2. Run Introduction (optional, no computational dependencies)
3. Run Appendix A (optional, mathematical background)

# Tier 1: Core Geometry & Gauge (can run in parallel)
4. Run G2GeometrySimulation
5. Run PneumaMechanismSimulation
6. Run GaugeUnificationSimulation

# Tier 2: Particle Physics (can run in parallel after Tier 1)
7. Run ChiralitySimulation
8. Run FermionGenerationsSimulation
9. Run CKMMatrixSimulation
10. Run HiggsMassSimulation
11. Run NeutrinoMixingSimulation
12. Run ProtonDecaySimulation

# Tier 3: Cosmology (can run in parallel after Tier 1-2)
13. Run CosmologyIntroSimulation
14. Run DarkEnergySimulation
15. Run MultiSectorCosmologySimulation
16. Run ThermalTimeSimulation

# Tier 4: Synthesis (run after all computations)
17. Run PredictionsAggregatorSimulation
18. Run DiscussionSimulation
19. Run AppendixBMethodsSimulation
20. Run AppendixCDerivationsSimulation
21. Run AppendixDTablesSimulation
```

### Parallelization Opportunities

Within each tier, simulations can be run in parallel:

- **Tier 1**: 3 simulations can run in parallel
- **Tier 2**: 6 simulations can run in parallel
- **Tier 3**: 4 simulations can run in parallel
- **Tier 4**: 5 simulations can run sequentially (or in groups)

### Estimated Execution Time

| Tier | Simulations | Sequential Time | Parallel Time |
|------|-------------|-----------------|---------------|
| 0 | Load ESTABLISHED + Intro + App A | ~20 ms | ~20 ms |
| 1 | G2, Pneuma, Gauge | ~150 ms | ~50 ms |
| 2 | 6 particle physics sims | ~600 ms | ~100 ms |
| 3 | 4 cosmology sims | ~400 ms | ~100 ms |
| 4 | 5 synthesis sims | ~250 ms | ~100 ms |
| **Total** | **22 simulations** | **~1420 ms** | **~370 ms** |

With parallelization, all simulations can complete in under 400 ms.

---

## Critical Path Analysis

The **critical path** (longest dependency chain) is:

```
ESTABLISHED → G2Geometry → ProtonDecay → MultiSector → Predictions → Appendix D
```

This path has **6 steps** and determines the minimum execution time even with unlimited parallelization.

### Critical Path Details

1. **ESTABLISHED** → Load PDG, NuFIT, TCS topology (~10 ms)
2. **G2Geometry** → Compute K_MATCHING, vol_g2 (~50 ms)
3. **GaugeUnification** (parallel) → Compute M_GUT (~50 ms)
4. **ProtonDecay** → Compute tau_p using M_GUT and K_MATCHING (~100 ms)
5. **MultiSector** → Use M_GUT and topology (~100 ms)
6. **Predictions** → Aggregate all results (~50 ms)
7. **Appendix D** → Generate tables (~50 ms)

**Critical Path Time**: ~410 ms

---

## Dependency Cycles

**Analysis**: No circular dependencies detected.

All dependencies form a **directed acyclic graph (DAG)**, which ensures:
- ✅ Well-defined execution order
- ✅ No deadlocks
- ✅ Parallelization is possible
- ✅ Incremental execution is supported

---

## Registry Parameter Flow

### Key Parameter Chains

1. **Topology Chain**:
   ```
   ESTABLISHED → topology.chi_eff, topology.b3
              → G2Geometry → topology.K_MATCHING, geometry.vol_g2
              → All fermion sims, cosmology sims
   ```

2. **Gauge Chain**:
   ```
   ESTABLISHED → pdg.alpha_s_MZ, pdg.sin2_theta_W
              → GaugeUnification → gauge.M_GUT, gauge.ALPHA_GUT
              → ProtonDecay, HiggsMass, MultiSector
   ```

3. **Pneuma Chain**:
   ```
   ESTABLISHED → constants.M_PLANCK, pdg.m_higgs
              → Pneuma → pneuma.vev, pneuma.coupling
              → DarkEnergy, ThermalTime
   ```

---

## Conclusion

The v16 simulation framework has a well-structured dependency graph with:
- **22 simulations** covering all paper sections
- **4 execution tiers** enabling parallelization
- **No circular dependencies** (clean DAG)
- **~370 ms total execution time** (with parallelization)
- **6-step critical path** determining minimum time

All simulations can be executed reliably in the order specified, with significant performance gains from parallel execution within each tier.

---

**Last Updated**: 2025-12-28
**Framework Version**: v16.0
