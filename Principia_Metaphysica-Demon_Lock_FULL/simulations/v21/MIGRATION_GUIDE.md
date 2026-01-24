# Migration Guide: v13/v14/v15 → v16 Simulations

This guide helps you migrate from legacy fermion simulations to the new v16 infrastructure.

## Overview of Changes

### Old Architecture (v13-v15)
- Standalone scripts with direct config.py imports
- Print-based output for debugging
- No standard interface
- Ad-hoc data structures
- Manual registry management

### New Architecture (v16)
- SimulationBase abstract interface
- PMRegistry for parameter management
- Structured data returns
- Complete formula and section metadata
- Automatic registry injection

## Quick Migration Examples

### Example 1: Basic Generation Count

**OLD (v13.0):**
```python
from simulations.core.fermion.fermion_chirality_generations_v13_0 import (
    verify_fermion_chirality_and_generations
)

# Run with defaults
results = verify_fermion_chirality_and_generations(chi_eff=144, verbose=True)

# Access results
n_gen = results['n_generations']
chiral_filter = results['chiral_filter_strength']
```

**NEW (v16.0):**
```python
from simulations.v16.fermion import FermionGenerationsV16
from simulations.base import PMRegistry

# Setup registry
registry = PMRegistry.get_instance()
registry.set_param("topology.CHI_EFF", 144, source="TCS", status="GEOMETRIC")
registry.set_param("topology.b3", 24, source="TCS", status="GEOMETRIC")

# Run simulation
sim = FermionGenerationsV16()
results = sim.execute(registry, verbose=True)

# Access results (now in registry)
n_gen = registry.get_param("fermion.n_generations")
chiral_filter = registry.get_param("fermion.chiral_filter_strength")
```

### Example 2: Yukawa Textures

**OLD (v14.2):**
```python
from simulations.core.fermion.yukawa_texture_geometric_v14_2 import (
    GeometricYukawaTextures
)

sim = GeometricYukawaTextures()
results = sim.derive_all_textures(verbose=True)

epsilon = results['epsilon_derived']
fermion_data = results['fermions']['top']
```

**NEW (v16.0):**
```python
from simulations.v16.fermion import FermionGenerationsV16
from simulations.base import PMRegistry

registry = PMRegistry.get_instance()
registry.set_param("topology.CHI_EFF", 144, source="TCS", status="GEOMETRIC")
registry.set_param("topology.b3", 24, source="TCS", status="GEOMETRIC")

sim = FermionGenerationsV16()
results = sim.execute(registry, verbose=True)

# Get Yukawa parameter
epsilon = registry.get_param("fermion.epsilon_fn")

# For detailed fermion masses, use the class directly
top_mass_predicted = sim.geometric_coeffs['top'] * epsilon**sim.fn_charges['top'] * 174.0
```

### Example 3: Export to theory_output.json

**OLD (v13.0):**
```python
from simulations.core.fermion.fermion_chirality_generations_v13_0 import (
    export_chirality_data
)

data = export_chirality_data()
# Manual JSON serialization
```

**NEW (v16.0):**
```python
from simulations.v16.fermion import FermionGenerationsV16
from simulations.base import PMRegistry

# Run simulation
registry = PMRegistry.get_instance()
registry.set_param("topology.CHI_EFF", 144, source="TCS", status="GEOMETRIC")
registry.set_param("topology.b3", 24, source="TCS", status="GEOMETRIC")

sim = FermionGenerationsV16()
sim.execute(registry)

# Export entire registry (includes all parameters, formulas, sections)
params = registry.export_parameters()
formulas = registry.export_formulas()
sections = registry.export_sections()

# Specific exports
theory_data = {
    'n_generations': params['fermion.n_generations']['value'],
    'epsilon': params['fermion.epsilon_fn']['value'],
    'chiral_filter': params['fermion.chiral_filter_strength']['value'],
    'formulas': {fid: formulas[fid] for fid in sim.output_formulas}
}
```

## Parameter Mapping

### Input Parameters

| Old Code | v16 Registry Path | Source |
|----------|-------------------|--------|
| `chi_eff` (arg) | `topology.CHI_EFF` | `GEOMETRIC` |
| `spinor_dof` (hardcoded) | Internal constant | N/A |
| `lambda_curvature` (class attr) | Internal constant | N/A |
| `b3` (from config) | `topology.b3` | `GEOMETRIC` |

### Output Parameters

| Old Code | v16 Registry Path | Status |
|----------|-------------------|--------|
| `results['n_generations']` | `fermion.n_generations` | `DERIVED` |
| `results['chiral_filter_strength']` | `fermion.chiral_filter_strength` | `DERIVED` |
| `results['epsilon_derived']` | `fermion.epsilon_fn` | `DERIVED` |
| `results['n_flux']` | `fermion.n_flux` | `DERIVED` |

## Formula Access

### OLD: Direct from CoreFormulas
```python
from config import CoreFormulas

formula = CoreFormulas.GENERATION_NUMBER
latex = formula.latex
value = formula.computed_value
```

### NEW: From Simulation
```python
from simulations.v16.fermion import FermionGenerationsV16

sim = FermionGenerationsV16()
formulas = sim.get_formulas()

# Find specific formula
gen_formula = next(f for f in formulas if f.id == "generation-number")
latex = gen_formula.latex
derivation = gen_formula.derivation
terms = gen_formula.terms
```

## Section Content Generation

### OLD: No section content
```python
# Section content was manually written in separate files
# No programmatic generation available
```

### NEW: Automatic Section Generation
```python
from simulations.v16.fermion import FermionGenerationsV16

sim = FermionGenerationsV16()
section = sim.get_section_content()

# Access structured content
print(f"Section {section.section_id}.{section.subsection_id}: {section.title}")
for block in section.content_blocks:
    if block.type == "formula":
        print(f"Formula: {block.formula_id}")
    elif block.type == "paragraph":
        print(f"Text: {block.content[:50]}...")
```

## Registry Integration Patterns

### Pattern 1: Single Simulation

```python
from simulations.v16.fermion import FermionGenerationsV16
from simulations.base import PMRegistry

# Initialize
registry = PMRegistry.get_instance()

# Set topology (would come from topology simulation in production)
registry.set_param("topology.CHI_EFF", 144, source="ESTABLISHED:TCS", status="GEOMETRIC")
registry.set_param("topology.b3", 24, source="ESTABLISHED:TCS", status="GEOMETRIC")

# Run fermion simulation
fermion = FermionGenerationsV16()
fermion.execute(registry)

# Results now in registry
n_gen = registry.get_param("fermion.n_generations")
```

### Pattern 2: Multiple Simulations (Pipeline)

```python
from simulations.v16.fermion import FermionGenerationsV16
from simulations.base import PMRegistry

registry = PMRegistry.get_instance()

# Step 1: Topology (when available)
# topology_sim = TopologySimV16()
# topology_sim.execute(registry)

# For now, set manually
registry.set_param("topology.CHI_EFF", 144, source="TCS", status="GEOMETRIC")
registry.set_param("topology.b3", 24, source="TCS", status="GEOMETRIC")

# Step 2: Fermion generations
fermion = FermionGenerationsV16()
fermion.execute(registry)

# Step 3: Use fermion outputs in next simulation
epsilon = registry.get_param("fermion.epsilon_fn")
# ... pass to gauge unification, etc.
```

### Pattern 3: Testing

```python
from simulations.v16.fermion import FermionGenerationsV16
from simulations.base import PMRegistry

# Reset registry for clean test
PMRegistry.reset_instance()
registry = PMRegistry.get_instance()

# Set test inputs
registry.set_param("topology.CHI_EFF", 144, source="TEST", status="GEOMETRIC")
registry.set_param("topology.b3", 24, source="TEST", status="GEOMETRIC")

# Run simulation
sim = FermionGenerationsV16()
results = sim.run(registry)  # Use run() for raw results

# Validate
assert results["fermion.n_generations"] == 3
assert abs(results["fermion.yukawa_hierarchy"] - 0.223) < 0.001
```

## Common Migration Issues

### Issue 1: Missing config.py imports

**Error:**
```python
from config import CoreFormulas  # ModuleNotFoundError
```

**Solution:**
```python
# Don't import from config in v16 simulations
# Use registry.get_param() instead
from simulations.base import PMRegistry

registry = PMRegistry.get_instance()
chi_eff = registry.get_param("topology.CHI_EFF")
```

### Issue 2: Direct attribute access

**Error:**
```python
sim = FermionGenerationsV16()
chi_eff = sim.chi_eff  # AttributeError
```

**Solution:**
```python
# Get from registry, not simulation object
registry = PMRegistry.get_instance()
chi_eff = registry.get_param("topology.CHI_EFF")
```

### Issue 3: Verbose output

**Old behavior:**
```python
# v13 always prints detailed output
verify_fermion_chirality_and_generations()  # Lots of printing
```

**New control:**
```python
# v16 respects verbose flag
sim.execute(registry, verbose=False)  # No printing
sim.execute(registry, verbose=True)   # Detailed output
```

## Benefits of v16 Architecture

1. **Type Safety**: SimulationBase interface enforces consistent structure
2. **Modularity**: Clean separation of inputs, computation, outputs
3. **Testability**: Easy to mock registry for unit tests
4. **Traceability**: Full provenance tracking in registry
5. **Composability**: Simulations can depend on each other via registry
6. **Documentation**: Formulas include derivation chains and references
7. **Paper Generation**: Section content ready for automated rendering

## Backward Compatibility

The old simulations (v13/v14/v15) are still available in `simulations/core/fermion/` and will continue to work for:
- Legacy scripts
- Comparison/validation
- Historical reference

However, **new development should use v16** for:
- Better maintainability
- Standard interface
- Registry integration
- Paper generation

## Next Steps

After migrating to v16, you can:

1. **Use outputs in other simulations:**
   ```python
   epsilon = registry.get_param("fermion.epsilon_fn")
   # Use in gauge unification, Yukawa predictions, etc.
   ```

2. **Generate paper sections:**
   ```python
   section = sim.get_section_content()
   # Export to paper renderer
   ```

3. **Create parameter tables:**
   ```python
   params = sim.get_output_param_definitions()
   # Generate tables for appendix
   ```

4. **Build simulation pipelines:**
   ```python
   # Topology → Fermion → Gauge → Proton Decay
   # All connected via registry
   ```

## Questions?

For detailed API documentation, see:
- `simulations/v21/fermion/README.md` - Fermion simulation guide
- `simulations/base/simulation_base.py` - SimulationBase interface
- `simulations/base/registry.py` - PMRegistry documentation
- `FERMION_V16_UPGRADE_SUMMARY.md` - Complete upgrade summary

---

**Last Updated:** 2025-12-28
**Migration Author:** Andrew Watts
