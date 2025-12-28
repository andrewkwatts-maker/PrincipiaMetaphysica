"""
Principia Metaphysica Simulation Framework
===========================================

This package provides the simulation infrastructure for the Principia Metaphysica
theoretical framework, a G2 manifold-based unification of fundamental physics.

Current Production Framework: v16.0
------------------------------------
All production simulations use the v16 framework with SOLID architecture:
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
    >>> from simulations.v16.gauge import GaugeUnificationSimulation
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

Available v16 Simulations (8 domains):
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
├── v16/                    # Production simulations (USE THIS)
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
- v16 Overview:      simulations/v16/README.md
- Foundation Schema: FOUNDATION_SCHEMA_README.md
- Quick Start:       FOUNDATION_QUICK_START.md

Execution Order (Topological):
-------------------------------
1. ESTABLISHED physics (PDG, NuFIT, TCS topology)
2. Tier 1: G2Geometry, GaugeUnification, Pneuma (parallel)
3. Tier 2: Proton, Higgs, Neutrino, Fermion (parallel)
4. Tier 3: Cosmology

Total execution time: ~200 ms for all 8 domains

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.
"""

# Version information
__version__ = "16.0.0"
__framework_version__ = "v16"
__author__ = "Andrew Keith Watts"

# Export v16 production framework
from . import v16

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

# Try to import v16 simulations (optional)
try:
    from .v16.gauge import GaugeUnificationSimulation
    from .v16.higgs import HiggsMassSimulation
    from .v16.proton import ProtonDecaySimulation
    from .v16.neutrino import NeutrinoMixingSimulation
    from .v16.fermion import FermionGenerationsV16 as FermionGenerationsSimulation
    from .v16.cosmology import MultiSectorCosmologySimulation
    from .v16.geometric import G2GeometrySimulation
    from .v16.pneuma import PneumaMechanismSimulation
    _V16_SIMULATIONS_AVAILABLE = True
except ImportError as e:
    _V16_SIMULATIONS_AVAILABLE = False
    import warnings
    warnings.warn(f"Some v16 simulations could not be imported: {e}")

# Define public API
__all__ = [
    # Version info
    '__version__',
    '__framework_version__',
    '__author__',

    # Modules
    'v16',
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

# Add v16 simulations to __all__ if available
if _V16_SIMULATIONS_AVAILABLE:
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
    List all available v16 simulations.

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

    if not _V16_SIMULATIONS_AVAILABLE:
        warnings.warn("Some v16 simulations are not available")

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
    print("  - v16 Overview:      simulations/v16/README.md")
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
        "Please update your code to use simulations.v16.* instead. "
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
                f"Use 'simulations.v16' for all production code. "
                f"See simulations/deprecated/README.md for details."
            )
        raise AttributeError(f"module 'simulations' has no attribute '{name}'")


# Install the blocker
import sys
if 'simulations.core' in sys.modules:
    warnings.warn(
        "simulations.core module detected. This has been deprecated. "
        "Update imports to use simulations.v16",
        DeprecationWarning
    )

# Note: We don't install a full blocker on __getattr__ to avoid breaking
# legitimate attribute access, but the warning system above should catch
# most deprecated usage patterns.
