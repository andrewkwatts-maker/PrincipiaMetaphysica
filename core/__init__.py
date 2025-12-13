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
]

__version__ = "12.7"
