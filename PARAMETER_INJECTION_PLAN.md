# Parameter Injection Architecture Plan

**Version:** 1.0
**Date:** 2025-12-28

## Overview

This document outlines the architecture for moving hardcoded parameter values to simulation-derived outputs, ensuring all physics quantities are either:
1. **ESTABLISHED** - Experimental measurements (PDG, NuFIT, DESI)
2. **DERIVED** - Computed from G2 geometry
3. **PREDICTED** - Output from simulations

---

## Current State (Problems)

### 1. Hardcoded Parameters in Simulations

Many simulations have values hardcoded that should be:
- Imported from config.py
- Outputs from other simulations
- Derived from geometry

**Examples:**
```python
# In higgs_mass_v12_4_moduli_stabilization.py
v = 174.0       # Should import HiggsVEVs.V_YUKAWA
y_t = 0.99      # Should come from Yukawa simulation
λ₀ = 0.129      # Should come from gauge simulation

# In yukawa_texture_geometric_v14_2.py
geometric_coeffs = {'top': 1.0, ...}  # Should be computed from G2 overlaps
```

### 2. Circular Dependencies

```
Higgs mass (PDG) → Constrains Re(T) → "Predicts" Higgs mass
```

### 3. No Provenance Tracking

Parameters don't track:
- Which simulation computed them
- What inputs were used
- Whether value is established/derived/predicted

---

## Target Architecture

### 1. Parameter Registry

Create a centralized registry that tracks all parameters:

```python
# In new file: simulations/parameter_registry.py

@dataclass
class TrackedParameter:
    id: str
    value: float
    uncertainty: float
    source: Literal["ESTABLISHED", "DERIVED", "PREDICTED"]
    computed_by: Optional[str]  # Simulation file that computed it
    depends_on: List[str]       # Input parameter IDs
    timestamp: datetime
    version: str

class ParameterRegistry:
    _parameters: Dict[str, TrackedParameter] = {}

    @classmethod
    def register(cls, param: TrackedParameter):
        """Register a computed parameter with full provenance."""
        if param.id in cls._parameters:
            old = cls._parameters[param.id]
            if old.source == "ESTABLISHED" and param.source != "ESTABLISHED":
                raise ValueError(f"Cannot override ESTABLISHED parameter {param.id}")
        cls._parameters[param.id] = param

    @classmethod
    def get(cls, param_id: str) -> TrackedParameter:
        """Get parameter with validation."""
        if param_id not in cls._parameters:
            warnings.warn(f"Parameter {param_id} not in registry - using fallback")
        return cls._parameters.get(param_id)

    @classmethod
    def validate_provenance(cls) -> List[str]:
        """Check all parameters have proper derivation chain."""
        issues = []
        for pid, param in cls._parameters.items():
            if param.source == "PREDICTED" and not param.computed_by:
                issues.append(f"{pid}: PREDICTED but no computed_by")
            if param.source == "DERIVED" and not param.depends_on:
                issues.append(f"{pid}: DERIVED but no depends_on")
        return issues
```

### 2. Simulation Output Protocol

Each simulation must export its outputs to the registry:

```python
# In each simulation file

def export_to_registry():
    """Export computed values to parameter registry."""
    from parameter_registry import ParameterRegistry, TrackedParameter

    ParameterRegistry.register(TrackedParameter(
        id="higgs.m_h_GeV",
        value=125.10,
        uncertainty=0.24,
        source="PREDICTED",
        computed_by="higgs_mass_v12_4_moduli_stabilization.py",
        depends_on=["moduli.Re_T", "gauge.lambda_0", "fermion.y_t"],
        timestamp=datetime.now(),
        version="v12.4"
    ))
```

### 3. Dependency-Ordered Execution

Modify `run_all_simulations.py` to:
1. Build dependency graph from parameter registry
2. Execute simulations in topological order
3. Pass outputs to dependent simulations

```python
# In run_all_simulations.py

SIMULATION_DEPENDENCIES = {
    # Simulation: [depends on simulations]
    "g2_metric_ricci_validator": [],                    # Foundation
    "racetrack_moduli_stabilization": ["g2_metric"],    # Uses topology
    "g2_torsion_m_gut": ["g2_metric"],                  # Uses torsion
    "gauge_unification": ["g2_torsion_m_gut"],          # Uses M_GUT
    "g2_yukawa_overlap": ["racetrack"],                 # Uses epsilon
    "higgs_mass": ["gauge_unification", "g2_yukawa"],   # Uses λ₀, y_t
    "fermion_masses": ["higgs_mass", "g2_yukawa"],      # Uses v, Y_f
    "proton_decay": ["gauge_unification"],              # Uses M_GUT
    "neutrino_pmns": ["g2_metric"],                     # Uses topology
}

def run_in_dependency_order():
    """Execute simulations respecting dependencies."""
    executed = set()
    results = {}

    while len(executed) < len(SIMULATION_DEPENDENCIES):
        for sim, deps in SIMULATION_DEPENDENCIES.items():
            if sim in executed:
                continue
            if all(d in executed for d in deps):
                # Get inputs from previously executed simulations
                inputs = {d: results[d] for d in deps}
                results[sim] = run_simulation(sim, inputs)
                executed.add(sim)

    return results
```

### 4. Runtime Warnings for Underived Parameters

Add warnings when parameters are used without being derived:

```python
# In config.py parameter access

class ParameterAccess:
    """Wrapper that warns on access to underived parameters."""

    @staticmethod
    def get(param_id: str, default=None):
        from parameter_registry import ParameterRegistry

        param = ParameterRegistry.get(param_id)
        if param is None:
            warnings.warn(
                f"⚠️ Parameter {param_id} accessed but not in registry. "
                f"Using hardcoded default: {default}",
                UserWarning
            )
            return default

        if param.source == "PREDICTED" and param.computed_by is None:
            warnings.warn(
                f"⚠️ Parameter {param_id} marked PREDICTED but has no computed_by. "
                f"This may be a hardcoded value masquerading as a prediction.",
                UserWarning
            )

        return param.value
```

---

## Implementation Phases

### Phase 1: Registry Infrastructure (Week 1)

1. Create `simulations/parameter_registry.py`
2. Define TrackedParameter dataclass
3. Add basic register/get/validate methods
4. Create ESTABLISHED parameters from PDG/NuFIT/DESI

### Phase 2: Simulation Export (Week 2)

1. Add `export_to_registry()` to each simulation
2. Start with foundational simulations:
   - g2_metric_ricci_validator_v15_0.py
   - racetrack_moduli_stabilization_v15_0.py
   - g2_torsion_m_gut_v12_4.py
3. Progress to dependent simulations

### Phase 3: Dependency Ordering (Week 3)

1. Build SIMULATION_DEPENDENCIES graph
2. Implement topological sort execution
3. Pass outputs between simulations
4. Remove hardcoded values from simulations

### Phase 4: Warnings & Validation (Week 4)

1. Add runtime warnings for underived parameters
2. Implement provenance validation
3. Generate dependency visualization
4. Create parameter flow documentation

---

## Parameter Categories

### ESTABLISHED (Experimental - Cannot Override)

```python
ESTABLISHED_PARAMETERS = {
    # PDG 2024
    "higgs.m_h_PDG": 125.20,        # GeV
    "fermion.m_t_PDG": 172.69,      # GeV
    "fermion.m_b_PDG": 4.18,        # GeV
    "gauge.alpha_em": 1/137.036,
    "gauge.alpha_s_MZ": 0.1180,
    "gauge.sin2_theta_W": 0.23121,

    # NuFIT 6.0
    "neutrino.theta_12": 33.41,     # degrees
    "neutrino.theta_23": 42.2,      # degrees
    "neutrino.theta_13": 8.54,      # degrees
    "neutrino.delta_m21_sq": 7.42e-5,  # eV²

    # DESI DR2
    "cosmology.w0": -0.997,
    "cosmology.wa": -0.70,

    # Super-Kamiokande
    "proton.tau_lower_bound": 1.67e34,  # years
}
```

### DERIVED (From G2 Geometry)

```python
DERIVED_PARAMETERS = {
    # From TCS #187 topology
    "topology.b3": 24,
    "topology.b2": 4,
    "topology.chi_eff": 144,
    "topology.T_omega": -0.884,

    # From racetrack stabilization
    "moduli.T_min": None,           # Computed
    "moduli.epsilon": None,         # Computed
    "moduli.vol_ratio": None,       # Computed

    # From torsion formula
    "gauge.M_GUT": None,            # Computed
    "gauge.alpha_GUT_inv": None,    # Computed
}
```

### PREDICTED (Simulation Outputs)

```python
PREDICTED_PARAMETERS = {
    # From Higgs simulation
    "higgs.m_h_predicted": None,    # Should match PDG

    # From fermion simulation
    "fermion.m_e": None,
    "fermion.m_mu": None,
    "fermion.m_tau": None,
    # ... all 9 fermion masses

    # From proton decay
    "proton.tau_predicted": None,   # Should exceed Super-K bound

    # From neutrino simulation
    "neutrino.theta_13_predicted": None,  # Should match NuFIT
    "neutrino.delta_CP_predicted": None,
}
```

---

## Validation Rules

### 1. No Circular Dependencies

```python
def check_no_cycles():
    """Ensure dependency graph is acyclic."""
    # Topological sort will fail if cycles exist
    try:
        topological_sort(SIMULATION_DEPENDENCIES)
        return True
    except CycleDetected as e:
        raise ValueError(f"Circular dependency: {e.cycle}")
```

### 2. All PREDICTED Must Have Source

```python
def validate_predictions():
    """Every PREDICTED parameter must have computed_by."""
    for pid, param in registry.items():
        if param.source == "PREDICTED":
            assert param.computed_by is not None, f"{pid} has no source"
            assert param.depends_on, f"{pid} has no dependencies"
```

### 3. Cannot Override ESTABLISHED

```python
def validate_established():
    """ESTABLISHED parameters cannot be modified by simulations."""
    for pid, param in registry.items():
        if param.source == "ESTABLISHED":
            assert param.computed_by is None, f"{pid} should not be computed"
```

---

## Files to Create

1. `simulations/parameter_registry.py` - Core registry
2. `simulations/dependency_graph.py` - Topological ordering
3. `simulations/parameter_validation.py` - Validation rules
4. `simulations/export_helpers.py` - Common export utilities

## Files to Modify

1. `run_all_simulations.py` - Use dependency ordering
2. `config.py` - Add parameter access warnings
3. All simulation files in `simulations/core/` - Add export_to_registry()

---

## Expected Outcomes

1. **Full Provenance:** Every parameter traceable to source
2. **No Hidden Hardcoding:** All values either established or derived
3. **Dependency Clarity:** Clear simulation execution order
4. **Runtime Safety:** Warnings for missing derivations
5. **Validation:** Automated checks for circular dependencies

---

## Priority Order

1. **CRITICAL:** Fix fermion mass calculation bug FIRST
2. **HIGH:** Create parameter registry infrastructure
3. **MEDIUM:** Add export_to_registry to simulations
4. **LOW:** Implement full dependency ordering

