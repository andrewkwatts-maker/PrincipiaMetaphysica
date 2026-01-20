# Fermion Simulations v16.0

This module contains fermion-related simulations using the SimulationBase infrastructure.

## Available Simulations

### FermionGenerationsV16 (`fermion_generations_v16_0.py`)

Derives the number of fermion generations and Yukawa hierarchy from G2 manifold topology.

**Key Results:**
- Exactly 3 generations (parameter-free from topology)
- Yukawa hierarchy parameter epsilon ~ 0.223
- Pneuma chiral filter strength = 7/8

## Quick Start

### Basic Usage

```python
from simulations.v16.fermion import FermionGenerationsV16
from simulations.base import PMRegistry

# Create registry and set inputs
registry = PMRegistry.get_instance()
registry.set_param("topology.CHI_EFF", 144, source="TCS_G2_187", status="GEOMETRIC")
registry.set_param("topology.b3", 24, source="TCS_G2_187", status="GEOMETRIC")

# Run simulation
sim = FermionGenerationsV16()
results = sim.execute(registry, verbose=True)

# Access results
n_gen = results["fermion.n_generations"]  # 3
epsilon = results["fermion.yukawa_hierarchy"]  # ~0.223
filter_strength = results["fermion.chiral_filter_strength"]  # 0.875
```

### Standalone Execution

```python
from simulations.v16.fermion.fermion_generations_v16_0 import run_fermion_generations

# Run with built-in defaults
results = run_fermion_generations(verbose=True)
```

### Command Line

```bash
cd h:\Github\PrincipiaMetaphysica
python -m simulations.v16.fermion.fermion_generations_v16_0
```

## Physics Overview

### Generation Number Derivation

The number of fermion generations follows from **spinor saturation** on the G2 manifold:

```
n_gen = N_flux / spinor_DOF
      = (chi_eff / 6) / 8
      = 144 / 48
      = 3
```

**Inputs:**
- `chi_eff = 144`: Effective Euler characteristic (TCS G2 manifold #187)
- Flux quantization: N_flux = chi_eff / 6 = 24
- Spinor DOF: 8 real components (Spin(7) representation)

**Result:** Exactly 3 generations (parameter-free)

### Yukawa Hierarchy

Fermion masses follow a **Froggatt-Nielsen texture** from geometric wave-function overlaps:

```
Y_f = A_f * epsilon^Q_f
epsilon = exp(-lambda) ~ 0.223
```

**Mechanism:**
- Fermions localize on associative 3-cycles at different positions
- Yukawa couplings from overlap integrals with Higgs VEV
- Topological charge Q_f = graph distance from Higgs cycle
- Suppression parameter epsilon derived from G2 curvature (lambda = 1.5)

**Agreement:** epsilon ~ 0.223 matches Cabibbo angle V_us = 0.2257

### Pneuma Chiral Filter

Chirality selection via **axial torsion coupling** in the Dirac operator:

```
D_eff = gamma^mu (d_mu + igA_mu + gamma^5 T_mu)
```

**Mechanism:**
- Pneuma condensate gradient: nabla<Psi_P>
- Induces axial torsion: T_mu ~ nabla_mu<Psi_P>
- gamma^5 coupling creates chirality-dependent potentials
- Left-handed modes: trapped on observable brane
- Right-handed modes: expelled to UV bulk

**Filter strength:** 7/8 from Spin(7) active components

## API Reference

### Class: FermionGenerationsV16

Implements `SimulationBase` interface for fermion generation derivation.

#### Metadata

```python
@property
def metadata(self) -> SimulationMetadata
```

Returns simulation metadata:
- **ID:** `fermion_generations_v16_0`
- **Version:** `16.0`
- **Domain:** `fermion`
- **Section:** `4.2` (Fermion Generations and Yukawa Texture)

#### Required Inputs

```python
@property
def required_inputs(self) -> List[str]
```

Returns: `["topology.CHI_EFF", "topology.b3"]`

#### Output Parameters

```python
@property
def output_params(self) -> List[str]
```

Returns:
- `fermion.n_generations`: Number of generations (3)
- `fermion.yukawa_hierarchy`: Yukawa parameter (~0.223)
- `fermion.chiral_filter_strength`: Filter strength (7/8)
- `fermion.n_flux`: Flux quanta (24)
- `fermion.epsilon_fn`: Froggatt-Nielsen parameter

#### Output Formulas

```python
@property
def output_formulas(self) -> List[str]
```

Returns:
- `generation-number`: Three generations from spinor saturation
- `yukawa-texture`: Yukawa hierarchy from geometric FN mechanism
- `pneuma-chiral-filter`: Modified Dirac operator with axial torsion

#### Methods

##### run(registry: PMRegistry) -> Dict[str, Any]

Executes the simulation computation.

**Args:**
- `registry`: PMRegistry instance with topology inputs

**Returns:**
- Dictionary with computed parameter values and metadata

**Example:**
```python
results = sim.run(registry)
print(f"Generations: {results['fermion.n_generations']}")
```

##### get_section_content() -> SectionContent

Returns complete paper content for Section 4.2.

**Returns:**
- SectionContent with 7 content blocks:
  - Introduction to generation count
  - Generation number formula
  - Explanation and validation
  - Yukawa hierarchy introduction
  - Yukawa texture formula
  - Pneuma chiral filter introduction
  - Modified Dirac operator formula

##### get_formulas() -> List[Formula]

Returns all formulas with full metadata.

**Returns:**
- List of 3 Formula objects with:
  - LaTeX and plain text representations
  - Derivation chains (steps, assumptions, references)
  - Term definitions for hover tooltips
  - Input/output parameter linkage

##### get_output_param_definitions() -> List[Parameter]

Returns parameter definitions for all outputs.

**Returns:**
- List of 5 Parameter objects with:
  - Full descriptions
  - Units and status
  - Derivation formula references
  - Experimental bounds

## Integration Examples

### With Gauge Unification

```python
from simulations.v16.fermion import FermionGenerationsV16
from simulations.v16.gauge import GaugeUnificationV16  # (when available)

registry = PMRegistry.get_instance()

# Set topology inputs
registry.set_param("topology.CHI_EFF", 144, source="TCS", status="GEOMETRIC")
registry.set_param("topology.b3", 24, source="TCS", status="GEOMETRIC")

# Run fermion simulation
fermion_sim = FermionGenerationsV16()
fermion_results = fermion_sim.execute(registry)

# Use epsilon in gauge calculations
epsilon = registry.get_param("fermion.epsilon_fn")
# ... (gauge unification can use epsilon for threshold corrections)
```

### With Paper Renderer

```python
from simulations.v16.fermion import FermionGenerationsV16

sim = FermionGenerationsV16()

# Get section content for paper
section = sim.get_section_content()

# Export to paper renderer
paper_data = {
    'section_id': section.section_id,
    'title': section.title,
    'blocks': [
        {
            'type': block.type,
            'content': block.content,
            'formula_id': block.formula_id
        }
        for block in section.content_blocks
    ]
}

# Get formulas for hover functionality
formulas = sim.get_formulas()
formula_data = {
    f.id: {
        'latex': f.latex,
        'terms': f.terms
    }
    for f in formulas
}
```

### Parameter Export

```python
from simulations.v16.fermion import FermionGenerationsV16

sim = FermionGenerationsV16()
params = sim.get_output_param_definitions()

# Export for parameter table
param_table = [
    {
        'path': p.path,
        'name': p.name,
        'units': p.units,
        'status': p.status,
        'experimental_bound': p.experimental_bound
    }
    for p in params
]
```

## Testing

Run the test suite:

```bash
cd h:\Github\PrincipiaMetaphysica
python test_fermion_v16.py
```

Tests cover:
- Metadata validation
- Input/output specification
- Computation accuracy
- Formula generation
- Parameter definitions
- Section content
- Registry integration

## Physics References

1. **Generation Count:**
   - Acharya-Witten (2001): Chiral fermions from G2
   - Joyce (2000): Spinor structures on G2 manifolds

2. **Yukawa Hierarchy:**
   - Froggatt-Nielsen (1979): Hierarchy from horizontal symmetry
   - Acharya et al. (2007): Yukawa couplings from M-theory

3. **Chiral Filter:**
   - Kaplan (1992): Domain wall fermions
   - Contopanagos-Einhorn (1992): Chiral fermions from torsion

## Version History

### v16.0 (2025-12-28)
- Initial release using SimulationBase infrastructure
- Unified v13/v14/v15 fermion derivations
- Complete paper content generation
- Full registry integration

---

**Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.**
