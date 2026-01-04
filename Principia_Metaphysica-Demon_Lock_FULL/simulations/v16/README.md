# Simulations v16 - Unified SimulationBase Framework

**Version**: 16.0
**Date**: 2025-12-28
**Status**: Production

This directory contains version 16 simulations using the unified `SimulationBase` infrastructure from `simulations.base`.

---

## Table of Contents

1. [Overview](#overview)
2. [Directory Structure](#directory-structure)
3. [All v16 Simulations](#all-v16-simulations)
4. [Dependency Graph](#dependency-graph)
5. [Execution Order](#execution-order)
6. [Usage Examples](#usage-examples)
7. [SimulationBase Interface](#simulationbase-interface)
8. [Output Format](#output-format)
9. [Running All Simulations](#running-all-simulations)
10. [Adding New Simulations](#adding-new-simulations)

---

## Overview

All v16 simulations implement a consistent interface for:

- **Metadata and versioning**: Unique IDs, versions, domains
- **Input/output parameter tracking**: Clear dependencies
- **Formula definitions**: LaTeX, plain text, derivation chains
- **Section content generation**: Paper-ready text and formulas
- **Registry integration**: Provenance tracking for all computed values

### Key Features

✅ **SOLID design principles**: Single responsibility, open/closed, dependency inversion
✅ **JSON schema validation**: Automated checking of metadata, formulas, parameters
✅ **Provenance tracking**: Every value knows its source and timestamp
✅ **Mismatch detection**: Warns if computed values change unexpectedly
✅ **Self-documenting**: Metadata and formulas are machine-readable

---

## Directory Structure

```
v16/
├── README.md                           # This file
├── MIGRATION_GUIDE.md                  # Guide for upgrading to v16
├── HIGGS_V16_UPGRADE_SUMMARY.md        # Higgs upgrade notes
├── PNEUMA_V16_UPGRADE_SUMMARY.md       # Pneuma upgrade notes
├── __init__.py                          # Module initialization
│
├── gauge/                               # Gauge sector (unification, couplings)
│   ├── __init__.py
│   ├── gauge_unification_v16_0.py
│   └── README.md
│
├── higgs/                               # Higgs sector (mass, VEV, quartic)
│   ├── __init__.py
│   ├── higgs_mass_v16_0.py
│   └── README.md (planned)
│
├── proton/                              # Proton decay
│   ├── __init__.py
│   ├── proton_decay_v16_0.py
│   └── README.md (planned)
│
├── neutrino/                            # Neutrino mixing and masses
│   ├── __init__.py
│   ├── neutrino_mixing_v16_0.py
│   ├── README.md
│   └── UPGRADE_SUMMARY.md
│
├── fermion/                             # Fermion generations, Yukawa
│   ├── __init__.py
│   ├── fermion_generations_v16_0.py
│   └── README.md
│
├── cosmology/                           # Dark matter, dark energy
│   ├── __init__.py
│   ├── multi_sector_v16_0.py
│   └── README.md
│
├── geometric/                           # G2 geometry, topology
│   ├── __init__.py
│   ├── g2_geometry_v16_0.py
│   ├── README.md
│   └── UPGRADE_SUMMARY.md
│
└── pneuma/                              # Pneuma field dynamics
    ├── __init__.py
    ├── pneuma_mechanism_v16_0.py
    └── README.md
```

---

## All v16 Simulations

### 1. Gauge Sector

#### `GaugeUnificationSimulation` (v16.0)
- **File**: `gauge/gauge_unification_v16_0.py`
- **Section**: 3
- **Status**: ✅ Complete

**Computes**:
- `gauge.M_GUT`: GUT scale (2.1e16 GeV)
- `gauge.ALPHA_GUT`: Unified coupling (0.0351)
- `gauge.sin2_theta_W_GUT`: Weak mixing angle at GUT scale
- `gauge.delta_alpha_kk`: KK tower threshold correction
- `gauge.delta_alpha_as`: Asymptotic safety correction

**Inputs**:
- `pdg.alpha_s_MZ`, `pdg.sin2_theta_W`, `pdg.m_Z` (ESTABLISHED)
- `constants.M_PLANCK`, `constants.alpha_em` (ESTABLISHED)

**Key Physics**:
- 3-loop RG evolution with Pneuma contributions
- KK tower thresholds from CY4 (h^{1,1} = 24)
- Asymptotic safety UV fixed point (SO(10))

---

### 2. Higgs Sector

#### `HiggsMassSimulation` (v16.0)
- **File**: `higgs/higgs_mass_v16_0.py`
- **Section**: 4.4
- **Status**: ✅ Complete

**Computes**:
- `higgs.m_higgs_pred`: Higgs mass (phenomenological, 125.10 GeV)
- `higgs.m_higgs_geometric`: Higgs mass (geometric, ~414 GeV)
- `higgs.lambda_eff_pheno`: Effective quartic (phenomenological)
- `higgs.lambda_eff_geometric`: Effective quartic (geometric)
- `higgs.vev`: Electroweak VEV (246 GeV)
- `moduli.stabilization_status`: Moduli stabilization status

**Inputs**:
- `topology.CHI_EFF`, `topology.B3`, `topology.T_OMEGA` (GEOMETRIC)
- `higgs.vev_yukawa`, `yukawa.y_top`, `gauge.g_gut` (PHENOMENOLOGICAL)
- `moduli.re_t_attractor`, `moduli.re_t_phenomenological` (DERIVED)

**Key Physics**:
- Racetrack moduli stabilization
- Higgs quartic from SO(10) matching
- Loop corrections from moduli-Higgs interactions
- Demonstrates geometric approach fails → phenomenological constraint needed

---

### 3. Proton Decay

#### `ProtonDecaySimulation` (v16.0)
- **File**: `proton/proton_decay_v16_0.py`
- **Section**: 4.6
- **Status**: ✅ Complete

**Computes**:
- `proton_decay.tau_p_years`: Proton lifetime (3.9e34 years)
- `proton_decay.suppression_factor`: Geometric suppression S (101.5)
- `proton_decay.super_k_ratio`: Ratio to Super-K bound (2.3)
- `proton_decay.d_over_R`: Cycle separation (0.12)
- `proton_decay.branching_ratio`: BR(p → e+ π0) = 0.25

**Inputs**:
- `gauge.M_GUT`, `gauge.ALPHA_GUT` (DERIVED from gauge_unification)
- `topology.K_MATCHING` (GEOMETRIC from g2_geometry)
- `constants.m_proton`, `bounds.tau_proton_lower` (ESTABLISHED)

**Key Physics**:
- Geometric suppression from TCS cycle separation
- d/R from K3 fibre matching (K=4)
- Wavefunction overlap selection rule
- 2.3× above Super-K bound (1.67e34 years)

---

### 4. Neutrino Sector

#### `NeutrinoMixingSimulation` (v16.0)
- **File**: `neutrino/neutrino_mixing_v16_0.py`
- **Section**: 4.5
- **Status**: ✅ Complete

**Computes**:
- `neutrino.theta_23`: Atmospheric mixing angle
- `neutrino.delta_m_sq_23`: Mass-squared difference
- `neutrino.ordering`: Mass ordering (normal/inverted)
- `neutrino.theta_12`, `neutrino.theta_13`: Other mixing angles
- `neutrino.delta_cp`: CP phase

**Inputs**:
- `pdg.theta_23_best`, `pdg.delta_m_sq_23` (ESTABLISHED, NuFIT 6.0)
- `topology.b3`, `topology.chi_eff` (GEOMETRIC)

**Key Physics**:
- G2 spinor geometry determines mixing angles
- Topology constrains mass hierarchy
- CP violation from associative calibrations

---

### 5. Fermion Sector

#### `FermionGenerationsSimulation` (v16.0)
- **File**: `fermion/fermion_generations_v16_0.py`
- **Section**: 4.3
- **Status**: ✅ Complete

**Computes**:
- `fermion.n_generations`: Number of generations (3)
- `fermion.chirality_mechanism`: Chirality generation mechanism
- `fermion.topology_constraint`: Topological constraint on generations

**Inputs**:
- `topology.b3`, `topology.chi_eff` (GEOMETRIC)

**Key Physics**:
- 3 generations from G2 homology (b3 = 24 = 8 × 3)
- Chirality from Z2 × Z2 filter on TCS
- Yukawa couplings from associative overlaps

---

### 6. Cosmology

#### `MultiSectorCosmologySimulation` (v16.0)
- **File**: `cosmology/multi_sector_v16_0.py`
- **Section**: 5
- **Status**: ✅ Complete

**Computes**:
- `cosmology.omega_dm`: Dark matter density (mirror sector)
- `cosmology.w_de`: Dark energy equation of state
- `cosmology.hubble_tension`: Hubble tension resolution
- `cosmology.sigma_8_tension`: σ8 tension resolution

**Inputs**:
- `gauge.M_GUT`, `topology.chi_eff` (DERIVED/GEOMETRIC)
- `pdg.omega_m`, `pdg.H0` (ESTABLISHED, Planck 2018)

**Key Physics**:
- Mirror dark matter from shadow sector
- Pneuma-driven dark energy
- Multi-sector framework resolves cosmological tensions

---

### 7. G2 Geometry

#### `G2GeometrySimulation` (v16.0)
- **File**: `geometric/g2_geometry_v16_0.py`
- **Section**: 2
- **Status**: ✅ Complete

**Computes**:
- `topology.K_MATCHING`: K3 fibre matching number (4)
- `geometry.vol_g2`: G2 manifold volume
- `geometry.associative_norm`: Associative calibration norm
- `geometry.coassociative_norm`: Coassociative calibration norm

**Inputs**:
- `topology.chi_eff`, `topology.b3` (ESTABLISHED, TCS #187)

**Key Physics**:
- TCS G2 construction (Corti-Haskins-Nordstrom-Pacini 2013)
- Associative and coassociative 3-cycles
- K3 fibration matching conditions

---

### 8. Pneuma Mechanism

#### `PneumaMechanismSimulation` (v16.0)
- **File**: `pneuma/pneuma_mechanism_v16_0.py`
- **Section**: 2
- **Status**: ✅ Complete

**Computes**:
- `pneuma.coupling`: Pneuma-geometry coupling constant
- `pneuma.flow_parameter`: Field flow parameter
- `pneuma.lagrangian_valid`: Lagrangian validity flag
- `pneuma.vev`: Vacuum expectation value
- `pneuma.mass_scale`: Characteristic mass scale (~10^13 GeV)

**Inputs**:
- `constants.M_PLANCK`, `pdg.m_higgs` (ESTABLISHED)
- `topology.chi_eff`, `topology.b3` (GEOMETRIC, optional)

**Key Physics**:
- Parallel spinor on G2 manifold
- Racetrack superpotential from competing instantons
- Vielbein emergence from spinor bilinears
- Dynamical VEV from energy minimization

---

## Dependency Graph

```
                    ┌─────────────────────────┐
                    │  ESTABLISHED PHYSICS    │
                    │  • PDG 2024             │
                    │  • NuFIT 6.0            │
                    │  • TCS Topology #187    │
                    └──────────┬──────────────┘
                               │
              ┌────────────────┼────────────────┐
              │                │                │
              ▼                ▼                ▼
      ┌──────────────┐  ┌──────────────┐  ┌──────────────┐
      │ G2 Geometry  │  │    Gauge     │  │   Pneuma     │
      │              │  │ Unification  │  │  Mechanism   │
      │ Section 2    │  │   Section 3  │  │  Section 2   │
      │ K_MATCHING   │  │   M_GUT      │  │  coupling    │
      │ vol_g2       │  │  ALPHA_GUT   │  │    vev       │
      └───────┬──────┘  └───────┬──────┘  └──────────────┘
              │                 │
              └────────┬────────┘
                       │
              ┌────────┼────────┬────────┐
              │        │        │        │
              ▼        ▼        ▼        ▼
       ┌──────────┐ ┌─────────┐ ┌──────────┐ ┌──────────┐
       │  Proton  │ │  Higgs  │ │ Neutrino │ │ Fermion  │
       │  Decay   │ │  Mass   │ │  Mixing  │ │   Gen.   │
       │ Sec 4.6  │ │ Sec 4.4 │ │ Sec 4.5  │ │ Sec 4.3  │
       │  tau_p   │ │  m_h    │ │ theta_23 │ │  n_gen   │
       └──────────┘ └─────────┘ └──────────┘ └──────────┘
              │        │        │        │
              └────────┼────────┴────────┘
                       │
                       ▼
              ┌─────────────────┐
              │   Cosmology     │
              │   Section 5     │
              │   omega_dm      │
              │   w_de          │
              └─────────────────┘
```

### Dependency Details

| Simulation | Depends On | Provides To |
|------------|------------|-------------|
| **G2Geometry** | TCS topology | Proton, Higgs, Neutrino, Fermion |
| **GaugeUnification** | PDG values | Proton, Higgs, Cosmology |
| **Pneuma** | Constants | (infrastructure) |
| **Proton** | Gauge, G2Geometry | Cosmology |
| **Higgs** | Gauge, Topology, Moduli | Cosmology |
| **Neutrino** | NuFIT, Topology | Cosmology |
| **Fermion** | Topology | Cosmology |
| **Cosmology** | All above | (final outputs) |

---

## Execution Order

To run all v16 simulations, use this topological order:

```python
from simulations.base import PMRegistry
from simulations.base.established import EstablishedPhysics

# Initialize registry
registry = PMRegistry.get_instance()

# 1. Load ESTABLISHED physics
EstablishedPhysics.load_into_registry(registry)

# 2. Tier 1: No dependencies (can run in parallel)
from simulations.v16.geometric import G2GeometrySimulation
from simulations.v16.gauge import GaugeUnificationSimulation
from simulations.v16.pneuma import PneumaMechanismSimulation

g2_sim = G2GeometrySimulation()
gauge_sim = GaugeUnificationSimulation()
pneuma_sim = PneumaMechanismSimulation()

g2_sim.execute(registry)
gauge_sim.execute(registry)
pneuma_sim.execute(registry)

# 3. Tier 2: Depend on Tier 1 (can run in parallel)
from simulations.v16.proton import ProtonDecaySimulation
from simulations.v16.higgs import HiggsMassSimulation
from simulations.v16.neutrino import NeutrinoMixingSimulation
from simulations.v16.fermion import FermionGenerationsSimulation

proton_sim = ProtonDecaySimulation()
higgs_sim = HiggsMassSimulation()
neutrino_sim = NeutrinoMixingSimulation()
fermion_sim = FermionGenerationsSimulation()

proton_sim.execute(registry)
higgs_sim.execute(registry)
neutrino_sim.execute(registry)
fermion_sim.execute(registry)

# 4. Tier 3: Depend on Tier 2
from simulations.v16.cosmology import MultiSectorCosmologySimulation

cosmo_sim = MultiSectorCosmologySimulation()
cosmo_sim.execute(registry)

# 5. Export results
params = registry.export_parameters()
formulas = registry.export_formulas()
sections = registry.export_sections()
```

### Execution Time

| Tier | Simulations | Est. Time |
|------|-------------|-----------|
| 0 | ESTABLISHED loading | ~10 ms |
| 1 | G2, Gauge, Pneuma | ~50 ms |
| 2 | Proton, Higgs, Neutrino, Fermion | ~100 ms |
| 3 | Cosmology | ~50 ms |
| **Total** | **All 8 domains** | **~200 ms** |

---

## Usage Examples

### Basic Usage

```python
from simulations.v16.gauge import GaugeUnificationSimulation
from simulations.base import PMRegistry
from simulations.base.established import EstablishedPhysics

# Create registry and load ESTABLISHED physics
registry = PMRegistry.get_instance()
EstablishedPhysics.load_into_registry(registry)

# Create and run simulation
sim = GaugeUnificationSimulation()
results = sim.execute(registry, verbose=True)

# Access results
M_GUT = results['gauge.M_GUT']
alpha_GUT = results['gauge.ALPHA_GUT']

print(f"M_GUT = {M_GUT:.3e} GeV")
print(f"alpha_GUT = {alpha_GUT:.5f}")
```

### Accessing Formulas

```python
# Get formula definitions
formulas = sim.get_formulas()

for formula in formulas:
    print(f"\n{formula.id}:")
    print(f"  LaTeX: {formula.latex}")
    print(f"  Category: {formula.category}")
    print(f"  Inputs: {formula.input_params}")
    print(f"  Outputs: {formula.output_params}")

    # Print derivation steps
    if formula.derivation:
        print(f"  Derivation:")
        for step in formula.derivation.get('steps', []):
            print(f"    - {step}")
```

### Accessing Section Content

```python
# Get section content
section = sim.get_section_content()

print(f"Section {section.section_id}")
print(f"Title: {section.title}")
print(f"Abstract: {section.abstract}")
print()

for block in section.content_blocks:
    if block.type == "paragraph":
        print(block.content)
        print()
    elif block.type == "formula":
        print(f"{block.label}: {block.content}")
        print()
```

### Checking Dependencies

```python
from simulations.base import RegistryValidator

# Check if dependencies are satisfied
result = RegistryValidator.check_dependencies(sim, registry)

if result.passed:
    print("All dependencies satisfied!")
else:
    print("Missing dependencies:")
    for error in result.errors:
        print(f"  - {error}")
```

### Validating a Simulation

```python
from simulations.base import SimulationValidator

# Validate simulation structure
result = SimulationValidator.validate_simulation(sim)

print(result)  # Shows errors and warnings

if not result.passed:
    print("\nValidation FAILED!")
    for error in result.errors:
        print(f"  ERROR: {error}")
```

---

## SimulationBase Interface

All v16 simulations implement the `SimulationBase` abstract class.

### Required Properties

```python
@property
def metadata(self) -> SimulationMetadata:
    """Simulation metadata (id, version, domain, etc.)"""

@property
def required_inputs(self) -> List[str]:
    """List of required input parameter paths"""

@property
def output_params(self) -> List[str]:
    """List of output parameter paths"""

@property
def output_formulas(self) -> List[str]:
    """List of formula IDs provided"""
```

### Required Methods

```python
def run(self, registry: PMRegistry) -> Dict[str, Any]:
    """Execute the simulation, return computed values"""

def get_section_content(self) -> Optional[SectionContent]:
    """Return section content for the paper"""

def get_formulas(self) -> List[Formula]:
    """Return formula definitions with derivation chains"""

def get_output_param_definitions(self) -> List[Parameter]:
    """Return parameter definitions for outputs"""
```

### Convenience Methods (Provided by Base Class)

```python
def validate_inputs(self, registry: PMRegistry) -> bool:
    """Validate all required inputs are present"""

def inject_outputs(self, registry: PMRegistry, results: Dict) -> None:
    """Inject computed outputs into registry"""

def inject_section(self, registry: PMRegistry) -> None:
    """Inject section content and formulas into registry"""

def execute(self, registry: PMRegistry, verbose: bool = True) -> Dict:
    """Template method: validate → run → inject (all-in-one)"""
```

---

## Output Format

### Parameter Registry Export

```json
{
  "gauge.M_GUT": {
    "value": 2.1e16,
    "source": "gauge_unification_v16_0",
    "status": "DERIVED",
    "uncertainty": 5e14,
    "timestamp": "2025-12-28T10:30:15.123456",
    "metadata": {}
  }
}
```

### Formula Registry Export

```json
{
  "proton-lifetime": {
    "id": "proton-lifetime",
    "label": "(4.12)",
    "latex": "\\tau_p = \\frac{M_{GUT}^4}{\\alpha_{GUT}^2 m_p^5} \\times S^2",
    "plain_text": "tau_p = (M_GUT^4 / (alpha_GUT^2 * m_p^5)) * S^2",
    "category": "DERIVED",
    "description": "Proton decay lifetime with geometric suppression",
    "input_params": ["gauge.M_GUT", "gauge.ALPHA_GUT", ...],
    "output_params": ["proton_decay.tau_p_years"],
    "derivation": {...},
    "terms": {...},
    "timestamp": "2025-12-28T10:30:15.123456"
  }
}
```

### Section Registry Export

```json
{
  "4.6": {
    "section_id": "4",
    "subsection_id": "4.6",
    "title": "Proton Decay",
    "abstract": "We compute the proton lifetime...",
    "content_blocks": [...],
    "formula_refs": ["proton-lifetime", "geometric-suppression"],
    "param_refs": ["proton_decay.tau_p_years"],
    "timestamp": "2025-12-28T10:30:15.123456"
  }
}
```

---

## Running All Simulations

See `simulations/v16/run_all_v16.py` (create if needed):

```python
#!/usr/bin/env python3
"""Run all v16 simulations in topological order."""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from simulations.base import PMRegistry
from simulations.base.established import EstablishedPhysics

# Import all simulations
from simulations.v16.geometric import G2GeometrySimulation
from simulations.v16.gauge import GaugeUnificationSimulation
from simulations.v16.pneuma import PneumaMechanismSimulation
from simulations.v16.proton import ProtonDecaySimulation
from simulations.v16.higgs import HiggsMassSimulation
from simulations.v16.neutrino import NeutrinoMixingSimulation
from simulations.v16.fermion import FermionGenerationsSimulation
from simulations.v16.cosmology import MultiSectorCosmologySimulation


def main():
    print("=" * 70)
    print("RUNNING ALL V16 SIMULATIONS")
    print("=" * 70)
    print()

    # Initialize registry
    registry = PMRegistry.get_instance()

    # Load ESTABLISHED physics
    print("Loading ESTABLISHED physics...")
    EstablishedPhysics.load_into_registry(registry)
    print()

    # Tier 1
    print("TIER 1: G2 Geometry, Gauge Unification, Pneuma")
    print("-" * 70)
    G2GeometrySimulation().execute(registry, verbose=True)
    GaugeUnificationSimulation().execute(registry, verbose=True)
    PneumaMechanismSimulation().execute(registry, verbose=True)
    print()

    # Tier 2
    print("TIER 2: Proton, Higgs, Neutrino, Fermion")
    print("-" * 70)
    ProtonDecaySimulation().execute(registry, verbose=True)
    HiggsMassSimulation().execute(registry, verbose=True)
    NeutrinoMixingSimulation().execute(registry, verbose=True)
    FermionGenerationsSimulation().execute(registry, verbose=True)
    print()

    # Tier 3
    print("TIER 3: Cosmology")
    print("-" * 70)
    MultiSectorCosmologySimulation().execute(registry, verbose=True)
    print()

    # Export
    print("=" * 70)
    print("EXPORTING RESULTS")
    print("=" * 70)

    import json

    params = registry.export_parameters()
    formulas = registry.export_formulas()
    sections = registry.export_sections()

    with open('v16_parameters.json', 'w') as f:
        json.dump(params, f, indent=2)
    print(f"Parameters: {len(params)} written to v16_parameters.json")

    with open('v16_formulas.json', 'w') as f:
        json.dump(formulas, f, indent=2)
    print(f"Formulas: {len(formulas)} written to v16_formulas.json")

    with open('v16_sections.json', 'w') as f:
        json.dump(sections, f, indent=2)
    print(f"Sections: {len(sections)} written to v16_sections.json")

    print()
    print("=" * 70)
    print("ALL SIMULATIONS COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    main()
```

---

## Adding New Simulations

See the comprehensive guide: [SIMULATION_GUIDE.md](../SIMULATION_GUIDE.md)

**Quick steps**:

1. Create file: `<domain>/<description>_v16_0.py`
2. Implement `SimulationBase` interface
3. Define metadata, inputs, outputs, formulas
4. Implement `run()` method with physics
5. Add `main()` for testing
6. Validate with `SimulationValidator`
7. Update `<domain>/__init__.py`
8. Add entry to this README

**Estimated time**: 2-4 hours for a simple simulation

---

## Status Summary

| Domain | Simulation | Version | Section | Status |
|--------|------------|---------|---------|--------|
| Gauge | GaugeUnificationSimulation | 16.0 | 3 | ✅ Complete |
| Higgs | HiggsMassSimulation | 16.0 | 4.4 | ✅ Complete |
| Proton | ProtonDecaySimulation | 16.0 | 4.6 | ✅ Complete |
| Neutrino | NeutrinoMixingSimulation | 16.0 | 4.5 | ✅ Complete |
| Fermion | FermionGenerationsSimulation | 16.0 | 4.3 | ✅ Complete |
| Cosmology | MultiSectorCosmologySimulation | 16.0 | 5 | ✅ Complete |
| Geometric | G2GeometrySimulation | 16.0 | 2 | ✅ Complete |
| Pneuma | PneumaMechanismSimulation | 16.0 | 2 | ✅ Complete |

**Total**: 8 domains, 8 simulations, all v16.0

---

## References

- **Architecture**: `simulations/ARCHITECTURE.md`
- **Simulation Guide**: `simulations/SIMULATION_GUIDE.md`
- **SimulationBase**: `simulations/base/simulation_base.py`
- **PMRegistry**: `simulations/base/registry.py`
- **Validators**: `simulations/base/validator.py`

---

**Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.**
