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

from .monte_carlo import (
    MonteCarloConfig,
    get_mc_config,
    get_n_samples,
    N_SAMPLES_DEFAULT,
)

from .data_flow_validation import (
    DataFlowValidator,
    ValidationIssue,
    validate_data_flow,
)

from .attributed_constants import (
    AttributedConstant,
    ALL_CONSTANTS,
    get_constant,
    get_value,
    print_attribution,
    generate_attribution_report,
    # Key constants with full attribution
    PLANCK_MASS_FULL,
    PLANCK_MASS_REDUCED,
    HIGGS_MASS,
    ELECTROWEAK_VEV,
    FINE_STRUCTURE_CONSTANT,
    THETA_12,
    THETA_23,
    THETA_13,
    DELTA_CP,
    DM21_SQUARED,
    DM31_SQUARED,
    W0_DARK_ENERGY,
    WA_DARK_ENERGY,
    M_GUT,
    ALPHA_GUT_INV,
    HODGE_H11,
    HODGE_B3,
    CHI_EFFECTIVE,
    N_GENERATIONS,
    TAU_PROTON_EXP,
    TAU_PROTON_PM,
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
    # Monte Carlo
    'MonteCarloConfig',
    'get_mc_config',
    'get_n_samples',
    'N_SAMPLES_DEFAULT',
    # Data Flow Validation
    'DataFlowValidator',
    'ValidationIssue',
    'validate_data_flow',
    # Attributed Constants
    'AttributedConstant',
    'ALL_CONSTANTS',
    'get_constant',
    'get_value',
    'print_attribution',
    'generate_attribution_report',
    'PLANCK_MASS_FULL',
    'PLANCK_MASS_REDUCED',
    'HIGGS_MASS',
    'ELECTROWEAK_VEV',
    'FINE_STRUCTURE_CONSTANT',
    'THETA_12',
    'THETA_23',
    'THETA_13',
    'DELTA_CP',
    'DM21_SQUARED',
    'DM31_SQUARED',
    'W0_DARK_ENERGY',
    'WA_DARK_ENERGY',
    'M_GUT',
    'ALPHA_GUT_INV',
    'HODGE_H11',
    'HODGE_B3',
    'CHI_EFFECTIVE',
    'N_GENERATIONS',
    'TAU_PROTON_EXP',
    'TAU_PROTON_PM',
]

__version__ = "12.7"
