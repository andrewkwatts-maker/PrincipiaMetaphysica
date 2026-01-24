# V16 Simulation Framework - Quick Start Guide

Get up and running with the v16 simulation framework in 5 minutes.

---

## What is the V16 Framework?

The v16 framework is a **production-ready simulation infrastructure** for the Principia Metaphysica paper, containing:

- **22 simulations** covering all paper sections (1-7, Appendices A-D)
- **Unified SimulationBase** interface for consistency
- **Parameter registry** with provenance tracking
- **Formula definitions** with LaTeX and derivation chains
- **Section content generation** for paper-ready output

---

## Quick Navigation

| Document | Purpose | When to Use |
|----------|---------|-------------|
| **[README.md](README.md)** | Main documentation | Learn about the framework |
| **[COMPLETE_SIMULATION_LIST.md](COMPLETE_SIMULATION_LIST.md)** | All 22 simulations | Find a specific simulation |
| **[DEPENDENCY_GRAPH.md](DEPENDENCY_GRAPH.md)** | Dependencies & execution order | Understand what depends on what |
| **[MIGRATION_GUIDE.md](MIGRATION_GUIDE.md)** | Upgrade guide | Migrate old code to v16 |
| **[CLEANUP_SUMMARY.md](CLEANUP_SUMMARY.md)** | Cleanup report | See what changed recently |
| **[QUICK_START.md](QUICK_START.md)** | This file | Get started quickly |

---

## Installation

```bash
# Clone repository
git clone <repo-url>
cd PrincipiaMetaphysica

# Install dependencies (if any)
pip install -r requirements.txt

# Verify installation
python -c "from simulations.v16.gauge import GaugeUnificationSimulation; print('OK')"
```

---

## Running a Single Simulation

### Example: Gauge Unification

```python
from simulations.base import PMRegistry
from simulations.base.established import EstablishedPhysics
from simulations.v16.gauge import GaugeUnificationSimulation

# 1. Create registry and load ESTABLISHED physics
registry = PMRegistry.get_instance()
EstablishedPhysics.load_into_registry(registry)

# 2. Create and execute simulation
sim = GaugeUnificationSimulation()
results = sim.execute(registry, verbose=True)

# 3. Access results
print(f"M_GUT = {results['gauge.M_GUT']:.3e} GeV")
print(f"alpha_GUT = {results['gauge.ALPHA_GUT']:.5f}")
```

**Output**:
```
Running: GaugeUnificationSimulation v16.0
M_GUT = 2.100e+16 GeV
alpha_GUT = 0.03510
```

---

## Running All Simulations

### Method 1: Manually (Full Control)

```python
from simulations.base import PMRegistry
from simulations.base.established import EstablishedPhysics

# Import all simulations
from simulations.v16.geometric import G2GeometrySimulation
from simulations.v16.gauge import GaugeUnificationSimulation
from simulations.v16.pneuma import PneumaMechanismSimulation
# ... etc

# Initialize
registry = PMRegistry.get_instance()
EstablishedPhysics.load_into_registry(registry)

# Tier 1: Core simulations
G2GeometrySimulation().execute(registry)
GaugeUnificationSimulation().execute(registry)
PneumaMechanismSimulation().execute(registry)

# Tier 2: Particle physics
# ... etc

# Export results
params = registry.export_parameters()
formulas = registry.export_formulas()
sections = registry.export_sections()
```

### Method 2: Using a Runner Script (Recommended)

Create `run_all_v16.py`:

```python
#!/usr/bin/env python3
"""Run all v16 simulations in topological order."""

from simulations.base import PMRegistry
from simulations.base.established import EstablishedPhysics

# Import all simulations
from simulations.v16.introduction import IntroductionSimulation
from simulations.v16.geometric import G2GeometrySimulation
from simulations.v16.pneuma import PneumaMechanismSimulation
from simulations.v16.gauge import GaugeUnificationSimulation
from simulations.v16.fermion import (
    ChiralitySimulation,
    FermionGenerationsSimulation,
    CKMMatrixSimulation
)
from simulations.v16.higgs import HiggsMassSimulation
from simulations.v21.neutrino import NeutrinoMixingSimulation
from simulations.v16.proton import ProtonDecaySimulation
from simulations.v16.cosmology import (
    CosmologyIntroSimulation,
    DarkEnergySimulation,
    MultiSectorCosmologySimulation
)
from simulations.v16.thermal import ThermalTimeSimulation
from simulations.v16.predictions import PredictionsAggregatorSimulation
from simulations.v16.discussion import DiscussionSimulation
from simulations.v16.appendices import (
    AppendixAMathSimulation,
    AppendixBMethodsSimulation,
    AppendixCDerivationsSimulation,
    AppendixDTablesSimulation
)

def main():
    print("=" * 70)
    print("RUNNING ALL V16 SIMULATIONS")
    print("=" * 70)

    # Initialize
    registry = PMRegistry.get_instance()
    EstablishedPhysics.load_into_registry(registry)

    # Tier 0
    print("\nTier 0: Foundation")
    IntroductionSimulation().execute(registry)
    AppendixAMathSimulation().execute(registry)

    # Tier 1
    print("\nTier 1: Core Geometry & Gauge")
    G2GeometrySimulation().execute(registry)
    PneumaMechanismSimulation().execute(registry)
    GaugeUnificationSimulation().execute(registry)

    # Tier 2
    print("\nTier 2: Particle Physics")
    ChiralitySimulation().execute(registry)
    FermionGenerationsSimulation().execute(registry)
    CKMMatrixSimulation().execute(registry)
    HiggsMassSimulation().execute(registry)
    NeutrinoMixingSimulation().execute(registry)
    ProtonDecaySimulation().execute(registry)

    # Tier 3
    print("\nTier 3: Cosmology")
    CosmologyIntroSimulation().execute(registry)
    DarkEnergySimulation().execute(registry)
    MultiSectorCosmologySimulation().execute(registry)
    ThermalTimeSimulation().execute(registry)

    # Tier 4
    print("\nTier 4: Synthesis")
    PredictionsAggregatorSimulation().execute(registry)
    DiscussionSimulation().execute(registry)
    AppendixBMethodsSimulation().execute(registry)
    AppendixCDerivationsSimulation().execute(registry)
    AppendixDTablesSimulation().execute(registry)

    # Export
    print("\n" + "=" * 70)
    print("EXPORTING RESULTS")
    print("=" * 70)

    import json

    params = registry.export_parameters()
    with open('v16_parameters.json', 'w') as f:
        json.dump(params, f, indent=2)
    print(f"✓ Parameters: {len(params)} written to v16_parameters.json")

    formulas = registry.export_formulas()
    with open('v16_formulas.json', 'w') as f:
        json.dump(formulas, f, indent=2)
    print(f"✓ Formulas: {len(formulas)} written to v16_formulas.json")

    sections = registry.export_sections()
    with open('v16_sections.json', 'w') as f:
        json.dump(sections, f, indent=2)
    print(f"✓ Sections: {len(sections)} written to v16_sections.json")

    print("\n" + "=" * 70)
    print("ALL SIMULATIONS COMPLETE")
    print("=" * 70)

if __name__ == "__main__":
    main()
```

Run it:
```bash
python run_all_v16.py
```

---

## Common Tasks

### 1. Find a Simulation for a Specific Section

See **[COMPLETE_SIMULATION_LIST.md](COMPLETE_SIMULATION_LIST.md)** for the complete mapping.

Example:
- **Section 4.5** (Neutrino Mixing) → `simulations.v16.neutrino.NeutrinoMixingSimulation`
- **Section 5.3** (Multi-Sector Cosmology) → `simulations.v16.cosmology.MultiSectorCosmologySimulation`

### 2. Check Dependencies for a Simulation

See **[DEPENDENCY_GRAPH.md](DEPENDENCY_GRAPH.md)** for the complete dependency matrix.

Example: `ProtonDecaySimulation` depends on:
- `GaugeUnificationSimulation` (for `gauge.M_GUT`, `gauge.ALPHA_GUT`)
- `G2GeometrySimulation` (for `topology.K_MATCHING`)

### 3. Access Formulas from a Simulation

```python
from simulations.v16.proton import ProtonDecaySimulation

sim = ProtonDecaySimulation()
formulas = sim.get_formulas()

for formula in formulas:
    print(f"{formula.id}: {formula.latex}")
    print(f"  Category: {formula.category}")
    print(f"  Inputs: {formula.input_params}")
    print(f"  Outputs: {formula.output_params}")
```

### 4. Generate Section Content

```python
from simulations.v16.proton import ProtonDecaySimulation

sim = ProtonDecaySimulation()
section = sim.get_section_content()

print(f"Section {section.section_id}: {section.title}")
print(f"\n{section.abstract}")

for block in section.content_blocks:
    if block.type == "paragraph":
        print(f"\n{block.content}")
    elif block.type == "formula":
        print(f"\n{block.label}: {block.content}")
```

### 5. Export All Results to JSON

```python
from simulations.base import PMRegistry

registry = PMRegistry.get_instance()
# ... run simulations ...

import json

# Export parameters
params = registry.export_parameters()
with open('parameters.json', 'w') as f:
    json.dump(params, f, indent=2)

# Export formulas
formulas = registry.export_formulas()
with open('formulas.json', 'w') as f:
    json.dump(formulas, f, indent=2)

# Export sections
sections = registry.export_sections()
with open('sections.json', 'w') as f:
    json.dump(sections, f, indent=2)
```

---

## Understanding the Architecture

### SimulationBase Interface

Every v16 simulation inherits from `SimulationBase` and implements:

```python
class MySimulation(SimulationBase):
    @property
    def metadata(self) -> SimulationMetadata:
        """Simulation metadata (id, version, domain)"""

    @property
    def required_inputs(self) -> List[str]:
        """List of required parameter paths"""

    @property
    def output_params(self) -> List[str]:
        """List of output parameter paths"""

    def run(self, registry: PMRegistry) -> Dict[str, Any]:
        """Execute simulation, return computed values"""

    def get_formulas(self) -> List[Formula]:
        """Return formula definitions"""

    def get_section_content(self) -> SectionContent:
        """Return section content for paper"""
```

### Parameter Registry

The `PMRegistry` tracks all parameters with:
- **Value**: Numerical or string value
- **Source**: Which simulation computed it
- **Status**: ESTABLISHED, DERIVED, PREDICTED
- **Timestamp**: When it was computed
- **Uncertainty**: Error bars (if applicable)

### Execution Flow

```
1. Load ESTABLISHED physics → Registry
2. Run Tier 1 simulations → Compute core parameters → Registry
3. Run Tier 2 simulations → Use Tier 1 outputs → Registry
4. Run Tier 3 simulations → Use Tier 1-2 outputs → Registry
5. Run Tier 4 simulations → Aggregate all results → Registry
6. Export registry → JSON files
```

---

## Troubleshooting

### Error: "Missing required input: gauge.M_GUT"

**Cause**: You're trying to run a simulation before its dependencies.

**Solution**: Run `GaugeUnificationSimulation` first to compute `gauge.M_GUT`.

See **[DEPENDENCY_GRAPH.md](DEPENDENCY_GRAPH.md)** for the correct execution order.

### Error: "File has been unexpectedly modified"

**Cause**: Using the Edit tool on a file that was modified externally.

**Solution**: Read the file again with the Read tool before editing.

### Simulation runs but produces wrong values

**Cause**: Stale registry or incorrect input values.

**Solution**:
1. Create a fresh registry: `registry = PMRegistry.get_instance()`
2. Reload ESTABLISHED physics: `EstablishedPhysics.load_into_registry(registry)`
3. Run simulations in dependency order

---

## Next Steps

- **Learn more**: Read [README.md](README.md) for comprehensive documentation
- **Explore simulations**: Browse [COMPLETE_SIMULATION_LIST.md](COMPLETE_SIMULATION_LIST.md)
- **Understand dependencies**: Study [DEPENDENCY_GRAPH.md](DEPENDENCY_GRAPH.md)
- **Migrate old code**: Follow [MIGRATION_GUIDE.md](MIGRATION_GUIDE.md)
- **Add new simulations**: See README.md → "Adding New Simulations"

---

## Support

For questions or issues:
1. Check documentation in this directory
2. Review simulation source code (all files have detailed docstrings)
3. Consult `simulations/ARCHITECTURE.md` for framework design
4. See `simulations/SIMULATION_GUIDE.md` for development guide

---

**Last Updated**: 2025-12-28
**Framework Version**: v16.0
**Status**: Production
