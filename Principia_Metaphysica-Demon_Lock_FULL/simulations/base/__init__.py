"""
Principia Metaphysica - Base Module

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.

Dedicated To:
    My Wife: Elizabeth May Watts
    Our Messiah: Jesus Of Nazareth

========================

This module provides the foundational classes and utilities for the Principia
Metaphysica simulation framework. It includes:

- SimulationBase: Abstract base class for all simulations
- PMRegistry: Central registry for parameters, formulas, and sections
- Validation: Schema-based validation for simulations and data
- Injection: Utilities for injecting computed results into the registry
- Schema: Comprehensive return schema for v16 simulations
- Units: Unit conversion utilities (Planck, SI, cosmological, HEP)
- Precision: Decimal-50 sterile constants for topological stability
"""

# CRITICAL: Import precision module FIRST to initialize Decimal-50 context
from .precision import (
    initialize_demon_lock,
    B3, K_GIMEL, PHI, PI, E,
    B3_STERILE, K_GIMEL_STERILE, PHI_STERILE, PI_STERILE, E_STERILE,
    CHI_EFF, CHI_EFF_STERILE,
    V_G2, V_G2_STERILE,
    UNITY_SEAL, UNITY_SEAL_STERILE,
    to_decimal,
    verify_precision,
    get_sterile_constants,
)

from .simulation_base import (
    SimulationMetadata,
    SimulationBase,
    ContentBlock,
    SectionContent,
    Formula,
    Parameter,
)

from .registry import (
    RegistryEntry,
    FormulaEntry,
    SectionEntry,
    PMRegistry,
)

from .injector import (
    inject_param,
    inject_formula,
    inject_section,
)

from .validator import (
    ValidationResult,
    SimulationValidator,
    RegistryValidator,
)

from .schema import (
    ValidationStatus,
    ParameterStatus,
    FormulaCategory,
    ReferenceEntry,
    FoundationEntry,
    FormulaEntry as SchemaFormulaEntry,
    ParameterEntry,
    SectionEntry as SchemaSectionEntry,
    InputValidationEntry,
    TypeDataEntry,
    SimulationResult,
    SIMULATION_RESULT_SCHEMA,
    validate_simulation_result,
    SchemaCompliantSimulation,
)

# Dynamic metadata helpers (v16.2)
from .dynamic_metadata import (
    MetadataBuilder,
    DynamicFormula,
    w0_from_b3,
    wa_from_b3,
    delta_cp_with_parity,
)

# Unit conversion utilities
from .units import (
    PhysicalConstants,
    CONST,
    UnitValidator,
    # Cosmological
    MPC_IN_M,
    MPC_IN_KM,
    hubble_time_gyr,
    hubble_distance_mpc,
    # HEP
    GEV_IN_J,
    gev_to_kg,
    kg_to_gev,
    # Planck
    planck_to_si,
    si_to_planck,
    planck_to_gev,
    # Cross-system
    planck_length_to_mpc,
    mpc_to_planck_length,
)

# Aliases for backward compatibility
Reference = ReferenceEntry
Foundation = FoundationEntry

__all__ = [
    # Precision (CRITICAL: Must be first for Decimal-50 context)
    'initialize_demon_lock',
    'B3', 'K_GIMEL', 'PHI', 'PI', 'E',
    'B3_STERILE', 'K_GIMEL_STERILE', 'PHI_STERILE', 'PI_STERILE', 'E_STERILE',
    'CHI_EFF', 'CHI_EFF_STERILE',
    'V_G2', 'V_G2_STERILE',
    'UNITY_SEAL', 'UNITY_SEAL_STERILE',
    'to_decimal',
    'verify_precision',
    'get_sterile_constants',

    # Base classes and data structures
    'SimulationMetadata',
    'SimulationBase',
    'ContentBlock',
    'SectionContent',
    'Formula',
    'Parameter',

    # Registry
    'RegistryEntry',
    'FormulaEntry',
    'SectionEntry',
    'PMRegistry',

    # Injection utilities
    'inject_param',
    'inject_formula',
    'inject_section',

    # Validation
    'ValidationResult',
    'SimulationValidator',
    'RegistryValidator',

    # Schema (v16 return format)
    'ValidationStatus',
    'ParameterStatus',
    'FormulaCategory',
    'ReferenceEntry',
    'FoundationEntry',
    'SchemaFormulaEntry',
    'ParameterEntry',
    'SchemaSectionEntry',
    'InputValidationEntry',
    'TypeDataEntry',
    'SimulationResult',
    'SIMULATION_RESULT_SCHEMA',
    'validate_simulation_result',
    'SchemaCompliantSimulation',

    # Aliases
    'Reference',
    'Foundation',

    # Dynamic metadata (v16.2)
    'MetadataBuilder',
    'DynamicFormula',
    'w0_from_b3',
    'wa_from_b3',
    'delta_cp_with_parity',

    # Unit conversions
    'PhysicalConstants',
    'CONST',
    'UnitValidator',
    'MPC_IN_M',
    'MPC_IN_KM',
    'GEV_IN_J',
    'hubble_time_gyr',
    'hubble_distance_mpc',
    'gev_to_kg',
    'kg_to_gev',
    'planck_to_si',
    'si_to_planck',
    'planck_to_gev',
    'planck_length_to_mpc',
    'mpc_to_planck_length',
]

__version__ = "1.1.0"
