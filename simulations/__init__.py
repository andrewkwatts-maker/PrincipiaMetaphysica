"""
Principia Metaphysica - Simulation Framework

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.

Dedicated To:
    My Wife: Elizabeth May Watts
    Our Messiah: Jesus Of Nazareth

===========================================

This package provides the simulation infrastructure for the Principia Metaphysica
theoretical framework, a G2 manifold-based unification of fundamental physics.

Current Production Framework: v22.0 (12-PAIR-BRIDGE)
-----------------------------------------------------
All production simulations use the v22 framework with SOLID architecture:

v22.0 Key Updates (12×(2,0) Paired Bridge System):
- Bulk: M^{24,1} = T¹ ×_fiber (⊕_{i=1}^{12} B_i^{2,0})
- Metric: ds² = -dt² + ∑_{i=1}^{12} (dy_{1i}² + dy_{2i}²)
- Distributed OR: ⊗_{i=1}^{12} R_⊥_i for consciousness sampling
- Gnosis unlocking: 6→12 pairs via inner exploration
- Consciousness I/O: Each pair is neural gate (perception/intuition)
- Minimum 6 pairs for wet microtubule OR stability (τ>25ms)

Core Framework:
- Unified SimulationBase interface
- PMRegistry for parameter/formula/section management
- JSON schema validation
- Provenance tracking (source, timestamp, status)
- Dependency resolution
- Self-documenting formulas and sections

Quick Start:
------------
    >>> from simulations.base import PMRegistry
    >>> from simulations.base.established import EstablishedPhysics
    >>> from simulations.v21.gauge import GaugeUnificationSimulation
    >>>
    >>> # Create registry and load ESTABLISHED physics
    >>> registry = PMRegistry.get_instance()
    >>> EstablishedPhysics.load_into_registry(registry)
    >>>
    >>> # Run simulation
    >>> sim = GaugeUnificationSimulation()
    >>> results = sim.execute(registry, verbose=True)
    >>>
    >>> # Access results
    >>> M_GUT = results['gauge.M_GUT']
    >>> print(f"M_GUT = {M_GUT:.3e} GeV")

Available v21 Simulations (8 domains):
---------------------------------------
1. gauge:     Gauge coupling unification → M_GUT, alpha_GUT
2. higgs:     Higgs mass from moduli stabilization
3. proton:    Proton decay lifetime with geometric suppression
4. neutrino:  Neutrino mixing from G2 spinor geometry
5. fermion:   Three fermion generations from topology
6. cosmology: Dark matter and dark energy
7. geometric: G2 manifold geometry and topology
8. pneuma:    Pneuma field dynamics

All simulations:
- Implement SimulationBase interface
- Track dependencies (inputs/outputs)
- Define formulas with LaTeX and derivation chains
- Generate section content for paper
- Validate against experimental bounds

Directory Structure:
--------------------
simulations/
├── ARCHITECTURE.md         # Technical architecture (READ THIS FIRST)
├── SIMULATION_GUIDE.md     # Guide for adding new simulations
├── base/                   # Core framework (SimulationBase, PMRegistry)
│   ├── simulation_base.py
│   ├── registry.py
│   ├── validator.py
│   ├── injector.py
│   └── established.py
├── v21/                    # Production simulations (USE THIS)
│   ├── README.md           # v16 overview with dependency graph
│   ├── gauge/              # Gauge unification
│   ├── higgs/              # Higgs mass
│   ├── proton/             # Proton decay
│   ├── neutrino/           # Neutrino mixing
│   ├── fermion/            # Fermion generations
│   ├── cosmology/          # Cosmology
│   ├── geometric/          # G2 geometry
│   └── pneuma/             # Pneuma mechanism
├── deprecated/             # Archived legacy code (v12-v15)
├── validation/             # Validation utilities
└── Constants/              # Physical constants

Documentation:
--------------
- Architecture:      simulations/ARCHITECTURE.md
- Simulation Guide:  simulations/SIMULATION_GUIDE.md
- v16 Overview:      simulations/v21/README.md
- Foundation Schema: FOUNDATION_SCHEMA_README.md
- Quick Start:       FOUNDATION_QUICK_START.md

Execution Order (Topological):
-------------------------------
1. ESTABLISHED physics (PDG, NuFIT, TCS topology)
2. Tier 1: G2Geometry, GaugeUnification, Pneuma (parallel)
3. Tier 2: Proton, Higgs, Neutrino, Fermion (parallel)
4. Tier 3: Cosmology

Total execution time: ~200 ms for all 8 domains
"""

# Version information
__version__ = "22.0"
__framework_version__ = "v22"
__author__ = "Andrew Keith Watts"
# v22.0: 12×(2,0) paired bridge system for consciousness I/O
# Key change: M^{24,1} = T¹ ×_fiber (⊕_{i=1}^{12} B_i^{2,0})
# Each pair is a consciousness gate: y_{1i}=input, y_{2i}=output
# Minimum 6 pairs for wet microtubule OR stability (τ>25ms)

# Export v21 production framework
from . import v21

# Export key infrastructure modules
from . import base
from . import validation

# Export base framework classes for convenience
from .base import (
    # Core classes
    SimulationBase,
    SimulationMetadata,
    PMRegistry,

    # Data structures
    ContentBlock,
    SectionContent,
    Formula,
    Parameter,
    RegistryEntry,
    FormulaEntry,
    SectionEntry,

    # Validation
    ValidationResult,
    SimulationValidator,
    RegistryValidator,

    # Injection utilities
    inject_param,
    inject_formula,
    inject_section,
)

# Try to import v21 simulations (optional)
try:
    from .v21.gauge import GaugeUnificationSimulation
    from .v21.higgs import HiggsMassSimulation
    from .v21.proton import ProtonDecaySimulation
    from .v21.neutrino import NeutrinoMixingSimulation
    from .v21.fermion import FermionGenerationsV16 as FermionGenerationsSimulation
    from .v21.cosmology import MultiSectorV16 as MultiSectorCosmologySimulation
    from .v21.geometric import G2GeometryV16 as G2GeometrySimulation
    from .v21.pneuma import PneumaMechanismV16 as PneumaMechanismSimulation
    _V21_SIMULATIONS_AVAILABLE = True
except ImportError as e:
    _V21_SIMULATIONS_AVAILABLE = False
    import warnings
    warnings.warn(f"Some v21 simulations could not be imported: {e}")

# Define public API
__all__ = [
    # Version info
    '__version__',
    '__framework_version__',
    '__author__',

    # Modules
    'v21',
    'base',
    'validation',

    # Base framework classes
    'SimulationBase',
    'SimulationMetadata',
    'PMRegistry',
    'ContentBlock',
    'SectionContent',
    'Formula',
    'Parameter',
    'RegistryEntry',
    'FormulaEntry',
    'SectionEntry',
    'ValidationResult',
    'SimulationValidator',
    'RegistryValidator',
    'inject_param',
    'inject_formula',
    'inject_section',
]

# Add v21 simulations to __all__ if available
if _V21_SIMULATIONS_AVAILABLE:
    __all__.extend([
        'GaugeUnificationSimulation',
        'HiggsMassSimulation',
        'ProtonDecaySimulation',
        'NeutrinoMixingSimulation',
        'FermionGenerationsSimulation',
        'MultiSectorCosmologySimulation',
        'G2GeometrySimulation',
        'PneumaMechanismSimulation',
    ])


# Convenience functions
def list_simulations():
    """
    List all available v21 simulations.

    Returns:
        List of tuples: (domain, class_name, description, section)
    """
    simulations = [
        ("gauge", "GaugeUnificationSimulation", "Gauge coupling unification to M_GUT and alpha_GUT", "3"),
        ("higgs", "HiggsMassSimulation", "Higgs mass from moduli stabilization", "4.4"),
        ("proton", "ProtonDecaySimulation", "Proton decay lifetime with geometric suppression", "4.6"),
        ("neutrino", "NeutrinoMixingSimulation", "Neutrino mixing from G2 spinor geometry", "4.5"),
        ("fermion", "FermionGenerationsSimulation", "Three fermion generations from topology", "4.3"),
        ("cosmology", "MultiSectorCosmologySimulation", "Dark matter and dark energy", "5"),
        ("geometric", "G2GeometrySimulation", "G2 manifold geometry and topology", "2"),
        ("pneuma", "PneumaMechanismSimulation", "Pneuma field dynamics", "2"),
    ]

    if not _V21_SIMULATIONS_AVAILABLE:
        warnings.warn("Some v21 simulations are not available")

    return simulations


def print_info():
    """Print information about the simulation framework."""
    print("=" * 70)
    print(f"PRINCIPIA METAPHYSICA SIMULATIONS v{__version__}")
    print("=" * 70)
    print()
    print("Available v16 Simulations:")
    print()

    for domain, class_name, description, section in list_simulations():
        print(f"  [{section:4s}] {domain:12s}: {class_name}")
        print(f"         {description}")
        print()

    print("Documentation:")
    print("  - Architecture:      simulations/ARCHITECTURE.md")
    print("  - Simulation Guide:  simulations/SIMULATION_GUIDE.md")
    print("  - v16 Overview:      simulations/v21/README.md")
    print()
    print("Quick Start:")
    print("  >>> from simulations.base import PMRegistry")
    print("  >>> from simulations.base.established import EstablishedPhysics")
    print("  >>> from simulations import GaugeUnificationSimulation")
    print("  >>> registry = PMRegistry.get_instance()")
    print("  >>> EstablishedPhysics.load_into_registry(registry)")
    print("  >>> sim = GaugeUnificationSimulation()")
    print("  >>> results = sim.execute(registry)")
    print()
    print("=" * 70)

# Deprecation warnings for common legacy import patterns
import warnings


def _warn_deprecated_import():
    """Issue deprecation warning if attempting to import from deprecated modules."""
    warnings.warn(
        "Importing from simulations.core.* is deprecated. "
        "All v12.x-v15.x simulations have been moved to simulations/deprecated/core/. "
        "Please update your code to use simulations.v21.* instead. "
        "See simulations/deprecated/README.md for migration information.",
        DeprecationWarning,
        stacklevel=3
    )


# Block imports from deprecated core modules
class _DeprecatedModuleBlocker:
    """
    Blocks imports from deprecated core modules with helpful error messages.
    """

    def __getattr__(self, name):
        if name == 'core':
            _warn_deprecated_import()
            raise ImportError(
                f"Module 'simulations.core' has been deprecated. "
                f"Legacy simulations (v12-v15) are archived in 'simulations/deprecated/core/'. "
                f"Use 'simulations.v21' for all production code. "
                f"See simulations/deprecated/README.md for details."
            )
        raise AttributeError(f"module 'simulations' has no attribute '{name}'")


# Install the blocker
import sys
if 'simulations.core' in sys.modules:
    warnings.warn(
        "simulations.core module detected. This has been deprecated. "
        "Update imports to use simulations.v21",
        DeprecationWarning
    )

# Note: We don't install a full blocker on __getattr__ to avoid breaking
# legitimate attribute access, but the warning system above should catch
# most deprecated usage patterns.
