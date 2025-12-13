"""
Principia Metaphysica Core Module
=================================

SOLID-compliant architecture for theoretical physics calculations.

This module provides:
- Domain-specific configuration classes (dimensions, topology, phenomenology)
- Abstract base class for simulations (Interface Segregation)
- Dependency injection for configuration (Dependency Inversion)
- Registry pattern for simulation modules (Open/Closed)

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.
"""

from .constants import (
    DimensionalStructure,
    TopologyParameters,
    EnergyScales,
    GaugeParameters,
    NeutrinoConfig,
    DarkEnergyConfig,
    ProtonDecayConfig,
)

from .simulation_base import (
    SimulationBase,
    SimulationResult,
    SimulationRegistry,
)

from .config_provider import (
    ConfigProvider,
    get_config,
)

from .logging_config import (
    setup_logging,
    get_logger,
    log_operation,
    SimulationLogger,
)

from .validation import (
    ValidationResult,
    PhysicsValidator,
    ExperimentalComparator,
    ConsistencyChecker,
    validate_n_gen,
    validate_chi_eff,
    validate_m_gut,
    validate_proton_lifetime,
)

__all__ = [
    # Constants
    'DimensionalStructure',
    'TopologyParameters',
    'EnergyScales',
    'GaugeParameters',
    'NeutrinoConfig',
    'DarkEnergyConfig',
    'ProtonDecayConfig',
    # Simulation framework
    'SimulationBase',
    'SimulationResult',
    'SimulationRegistry',
    # Configuration
    'ConfigProvider',
    'get_config',
    # Logging
    'setup_logging',
    'get_logger',
    'log_operation',
    'SimulationLogger',
    # Validation
    'ValidationResult',
    'PhysicsValidator',
    'ExperimentalComparator',
    'ConsistencyChecker',
    'validate_n_gen',
    'validate_chi_eff',
    'validate_m_gut',
    'validate_proton_lifetime',
]

__version__ = "12.7"
