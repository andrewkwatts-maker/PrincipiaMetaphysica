# G2 Geometry Simulations v16

## Overview

This module contains v16 geometric simulations implementing the `SimulationBase` interface. These simulations compute fundamental topology parameters for the TCS G2 manifold #187 used throughout Principia Metaphysica.

## Simulations

### G2GeometryV16 (`g2_geometry_v16_0.py`)

**Status:** Root simulation (no dependencies)

**Purpose:** Compute fundamental G2 topology invariants from TCS construction.

**Inputs:** None (uses ESTABLISHED constants from literature)

**Outputs:**
- `topology.b2` - Second Betti number (4 Kahler moduli)
- `topology.b3` - Third Betti number (24 associative 3-cycles)
- `topology.CHI_EFF` - Effective Euler characteristic (144)
- `topology.n_gen` - Number of fermion generations (3)
- `topology.K_MATCHING` - K3 matching fibres (4)
- `topology.d_over_R` - Cycle separation ratio (0.12)

**Formulas:**
- `g2-holonomy` - G2 holonomy condition (parallel spinor)
- `euler-characteristic` - χ_eff from Hodge numbers
- `betti-numbers` - Complete Betti number sequence
- `three-generations` - n_gen = χ_eff / 48
- `cycle-matching` - K_matching from TCS gluing

**Section Content:** Section 2 appendices on G2 geometry

## Architecture

All v16 simulations follow this structure:

```python
class MySimulation(SimulationBase):
    @property
    def metadata(self) -> SimulationMetadata:
        # id, version, domain, title, description, section_id

    @property
    def required_inputs(self) -> List[str]:
        # Parameter paths needed from registry

    @property
    def output_params(self) -> List[str]:
        # Parameter paths this simulation computes

    @property
    def output_formulas(self) -> List[str]:
        # Formula IDs this simulation provides

    def run(self, registry: PMRegistry) -> Dict[str, Any]:
        # Computation logic

    def get_section_content(self) -> SectionContent:
        # Generate paper section content

    def get_formulas(self) -> List[Formula]:
        # Define formulas with derivations

    def get_output_param_definitions(self) -> List[Parameter]:
        # Define output parameters with metadata
```

## Usage

### Basic Execution

```python
from simulations.v16.geometric import G2GeometryV16
from simulations.base import PMRegistry

# Get registry instance
registry = PMRegistry.get_instance()

# Create and run simulation
sim = G2GeometryV16()
results = sim.execute(registry, verbose=True)

# Access computed values
b3 = registry.get_param("topology.b3")
chi_eff = registry.get_param("topology.CHI_EFF")
```

### Integration with Other Simulations

```python
# G2 geometry is a root simulation - other simulations depend on it
from simulations.v16.geometric import G2GeometryV16
from simulations.v16.gauge import GaugeUnificationV16

registry = PMRegistry.get_instance()

# Run G2 geometry first (provides topology.* parameters)
g2_sim = G2GeometryV16()
g2_sim.execute(registry)

# Then run gauge unification (requires topology.CHI_EFF, etc.)
gauge_sim = GaugeUnificationV16()
gauge_sim.execute(registry)
```

## Parameter Categories

### GEOMETRIC (Pure Topology)
Parameters derived purely from TCS manifold topology:
- `topology.b2`, `topology.b3` - Betti numbers
- `topology.CHI_EFF` - Euler characteristic
- `topology.n_gen` - Generation count from index theorem
- `topology.K_MATCHING` - TCS matching parameter

### Formula Categories

All formulas in G2GeometryV16 are **THEORY** category:
- Derive from ESTABLISHED physics (Joyce, Hitchin, Atiyah-Singer)
- Form the theoretical foundation for PM framework
- Not phenomenologically fitted

## Validation

The simulation validates G2 holonomy via four conditions:
1. Exactly one parallel spinor (Killing spinor)
2. Ricci-flatness: R_μν = 0
3. Closed associative 3-form: dΦ = 0
4. Closed coassociative 4-form: d(*Φ) = 0

All conditions are satisfied for TCS #187.

## Holonomy Precision Limit

The warp factor k_gimel = b3/2 + 1/π exhibits a fundamental precision limit:

```
k_gimel = 24/2 + 1/π = 12.318309886183791...
```

**Precision Note:**
- The value 12.318309 (6 decimal places) represents the **Holonomy Precision Limit**
- Using 12.319 (3 decimal places) introduces ~0.008% error in alpha^-1 derivation
- This is NOT a free parameter - it is exactly determined by b3=24 and π
- The transcendental 1/π term encodes the curved geometry of the G2 manifold

In `alpha_rigor_v16_1.py`, we maintain full precision throughout the computation to achieve the CODATA match for the fine structure constant alpha^-1 = 137.035999.

## References

1. **Joyce, D. (2000)** "Compact Manifolds with Special Holonomy"
   *Foundational text on G2 manifolds*

2. **Hitchin, N. (2000)** "The Geometry of G2 Manifolds" [arXiv:math/0010054](https://arxiv.org/abs/math/0010054)
   *G2 holonomy and parallel spinors*

3. **Corti et al. (2015)** "G2-Manifolds and Moduli Spaces" [arXiv:1503.05500](https://arxiv.org/abs/1503.05500)
   *TCS construction and classification*

4. **Kovalev (2003)** "Twisted Connected Sums" [arXiv:math/0012189](https://arxiv.org/abs/math/0012189)
   *TCS gluing construction*

5. **Acharya (2002)** [arXiv:hep-th/0212294](https://arxiv.org/abs/hep-th/0212294)
   *Index theorem for chiral fermions on G2*

## Upgrade from v15

### v15.0 (Legacy)
- Separate files for metric validation and Yukawa overlaps
- Manual parameter passing between simulations
- No standardized interface
- Limited provenance tracking

### v16.0 (Current)
- Unified `SimulationBase` interface
- `PMRegistry` for centralized parameter management
- Complete formula derivation chains
- Section content generation
- Full metadata and provenance tracking

## Future Work

Planned additions to v16 geometric domain:
- Yukawa overlap integrals (from v15.0)
- Moduli stabilization (racetrack)
- CP phase from topology
- Flux quantization constraints

## Testing

Run the test suite:
```bash
python simulations/v21/geometric/g2_geometry_v16_0.py
```

Expected output:
```
======================================================================
 G2 Geometry and Topology (v16.0)
======================================================================

[g2_geometry_v16_0] Starting G2 Geometry and Topology...
[g2_geometry_v16_0] Completed in 0.05ms

======================================================================
 COMPUTED TOPOLOGY PARAMETERS
======================================================================
  b2 (Kahler moduli):       4
  b3 (associative cycles):  24
  chi_eff:                  144
  n_gen:                    3
  K_matching:               4
  d/R:                      0.12

  G2 holonomy valid:        True
======================================================================
```

## License

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.
