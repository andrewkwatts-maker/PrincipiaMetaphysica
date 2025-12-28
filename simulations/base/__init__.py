"""
Simulations Base Module
========================

This module provides the foundational classes and utilities for the Principia
Metaphysica simulation framework. It includes:

- SimulationBase: Abstract base class for all simulations
- PMRegistry: Central registry for parameters, formulas, and sections
- Validation: Schema-based validation for simulations and data
- Injection: Utilities for injecting computed results into the registry
- Schema: Comprehensive return schema for v16 simulations

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.
"""

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

# Aliases for backward compatibility
Reference = ReferenceEntry
Foundation = FoundationEntry

__all__ = [
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
]

__version__ = "1.0.0"
