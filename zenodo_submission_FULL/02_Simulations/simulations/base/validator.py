"""
Validation Utilities
=====================

JSON schema-based validation for simulations, formulas, parameters,
and registry data.

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.

Dedicated To:
    My Wife: Elizabeth May Watts
    Our Messiah: Jesus Of Nazareth
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, TYPE_CHECKING
import re
import math

if TYPE_CHECKING:
    from .simulation_base import SimulationBase
    from .registry import PMRegistry


@dataclass
class ValidationResult:
    """
    Result of a validation check.

    Attributes:
        passed: Whether validation passed
        errors: List of error messages
        warnings: List of warning messages
    """
    passed: bool
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)

    def add_error(self, message: str) -> None:
        """Add an error message."""
        self.errors.append(message)
        self.passed = False

    def add_warning(self, message: str) -> None:
        """Add a warning message."""
        self.warnings.append(message)

    def __str__(self) -> str:
        """String representation."""
        lines = [f"Validation: {'PASSED' if self.passed else 'FAILED'}"]

        if self.errors:
            lines.append(f"\nErrors ({len(self.errors)}):")
            for err in self.errors:
                lines.append(f"  - {err}")

        if self.warnings:
            lines.append(f"\nWarnings ({len(self.warnings)}):")
            for warn in self.warnings:
                lines.append(f"  - {warn}")

        return "\n".join(lines)


class SimulationValidator:
    """
    Validator for simulation classes and their metadata.

    Provides JSON schema-based validation for:
    - Simulation metadata
    - Formula definitions
    - Parameter definitions
    """

    # JSON Schema for metadata validation
    METADATA_SCHEMA = {
        "type": "object",
        "required": ["id", "version", "domain", "title", "description", "section_id"],
        "properties": {
            "id": {"type": "string", "pattern": r"^[a-z_]+_v\d+_\d+$"},
            "version": {"type": "string", "pattern": r"^\d+\.\d+$"},
            "domain": {
                "type": "string",
                "enum": [
                    "gauge", "cosmology", "fermion", "neutrino", "proton",
                    "higgs", "moduli", "pneuma", "geometric", "quantum_bio"
                ]
            },
            "title": {"type": "string", "minLength": 5},
            "description": {"type": "string", "minLength": 10},
            "section_id": {"type": "string", "pattern": r"^[1-9A-N](\.\d+)?$"},
            "subsection_id": {"type": ["string", "null"]},
        }
    }

    # JSON Schema for formula validation
    FORMULA_SCHEMA = {
        "type": "object",
        "required": ["id", "label", "latex", "category"],
        "properties": {
            "id": {"type": "string", "pattern": r"^[a-z][a-z0-9-]*$"},
            "label": {"type": "string", "pattern": r"^\(\d+\.\d+\)"},
            "latex": {"type": "string", "minLength": 1},
            "plain_text": {"type": "string"},
            "category": {
                "type": "string",
                "enum": ["ESTABLISHED", "THEORY", "DERIVED", "PREDICTIONS"]
            },
            "description": {"type": "string"},
            "input_params": {"type": "array", "items": {"type": "string"}},
            "output_params": {"type": "array", "items": {"type": "string"}},
            "derivation": {"type": ["object", "null"]},
            "terms": {"type": "object"},
        }
    }

    # JSON Schema for parameter validation
    PARAMETER_SCHEMA = {
        "type": "object",
        "required": ["path", "name", "units", "status", "description"],
        "properties": {
            "path": {"type": "string", "pattern": r"^[a-z_]+\.[a-z_0-9]+$"},
            "name": {"type": "string", "minLength": 1},
            "units": {"type": "string", "minLength": 1},
            "status": {
                "type": "string",
                "enum": ["ESTABLISHED", "GEOMETRIC", "DERIVED", "PREDICTED", "CALIBRATED"]
            },
            "description": {"type": "string", "minLength": 1},
            "derivation_formula": {"type": ["string", "null"]},
            "experimental_bound": {"type": ["number", "null"]},
            "bound_type": {
                "type": ["string", "null"],
                "enum": ["upper", "lower", "range", "measured", None]
            },
            "bound_source": {"type": ["string", "null"]},
        }
    }

    @classmethod
    def validate_simulation(cls, simulation: 'SimulationBase') -> ValidationResult:
        """
        Validate a simulation instance.

        Checks:
        1. Metadata is properly formed
        2. Required inputs are specified
        3. Output params and formulas are specified
        4. Formulas are well-formed
        5. Output parameters are well-defined

        Args:
            simulation: SimulationBase instance to validate

        Returns:
            ValidationResult with any errors or warnings
        """
        result = ValidationResult(passed=True)

        # Validate metadata
        try:
            metadata = simulation.metadata
            cls._validate_dict_against_schema(
                metadata.__dict__,
                cls.METADATA_SCHEMA,
                "metadata",
                result
            )
        except Exception as e:
            result.add_error(f"Failed to get metadata: {e}")

        # Validate required inputs
        try:
            required_inputs = simulation.required_inputs
            if not isinstance(required_inputs, list):
                result.add_error("required_inputs must be a list")
            elif not required_inputs:
                result.add_warning("No required inputs specified")
            else:
                for inp in required_inputs:
                    if not isinstance(inp, str) or '.' not in inp:
                        result.add_error(f"Invalid input path: {inp}")
        except Exception as e:
            result.add_error(f"Failed to get required_inputs: {e}")

        # Validate output params
        try:
            output_params = simulation.output_params
            if not isinstance(output_params, list):
                result.add_error("output_params must be a list")
            elif not output_params:
                result.add_warning("No output parameters specified")
            else:
                for out in output_params:
                    if not isinstance(out, str) or '.' not in out:
                        result.add_error(f"Invalid output path: {out}")
        except Exception as e:
            result.add_error(f"Failed to get output_params: {e}")

        # Validate output formulas
        try:
            output_formulas = simulation.output_formulas
            if not isinstance(output_formulas, list):
                result.add_error("output_formulas must be a list")
        except Exception as e:
            result.add_error(f"Failed to get output_formulas: {e}")

        # Validate formulas
        try:
            formulas = simulation.get_formulas()
            for formula in formulas:
                cls._validate_dict_against_schema(
                    formula.__dict__,
                    cls.FORMULA_SCHEMA,
                    f"formula {formula.id}",
                    result
                )
                # Check formula outputs are in simulation outputs
                for param in formula.output_params:
                    if param not in simulation.output_params:
                        result.add_error(
                            f"Formula {formula.id} outputs {param} not in simulation outputs"
                        )
        except Exception as e:
            result.add_error(f"Failed to get formulas: {e}")

        # Validate parameter definitions
        try:
            params = simulation.get_output_param_definitions()
            for param in params:
                cls._validate_dict_against_schema(
                    param.__dict__,
                    cls.PARAMETER_SCHEMA,
                    f"parameter {param.path}",
                    result
                )
        except Exception as e:
            result.add_error(f"Failed to get output parameter definitions: {e}")

        return result

    @classmethod
    def _validate_dict_against_schema(
        cls,
        data: Dict[str, Any],
        schema: Dict[str, Any],
        context: str,
        result: ValidationResult
    ) -> None:
        """
        Validate a dictionary against a JSON schema (simplified implementation).

        Args:
            data: Dictionary to validate
            schema: JSON schema
            context: Context string for error messages
            result: ValidationResult to add errors/warnings to
        """
        # Check required fields
        required = schema.get("required", [])
        for field_name in required:
            if field_name not in data or data[field_name] is None:
                result.add_error(f"{context}: missing required field '{field_name}'")

        # Check field types and constraints
        properties = schema.get("properties", {})
        for field_name, field_schema in properties.items():
            if field_name not in data:
                continue

            value = data[field_name]
            expected_type = field_schema.get("type")

            if expected_type:
                if not cls._check_type(value, expected_type):
                    result.add_error(
                        f"{context}.{field_name}: expected {expected_type}, got {type(value).__name__}"
                    )
                    continue

            # Check enum constraints
            if "enum" in field_schema:
                if value not in field_schema["enum"]:
                    result.add_error(
                        f"{context}.{field_name}: value '{value}' not in allowed values {field_schema['enum']}"
                    )

            # Check string patterns
            if "pattern" in field_schema and isinstance(value, str):
                pattern = field_schema["pattern"]
                if not re.match(pattern, value):
                    result.add_warning(
                        f"{context}.{field_name}: value '{value}' does not match pattern '{pattern}'"
                    )

            # Check minimum length
            if "minLength" in field_schema and isinstance(value, str):
                if len(value) < field_schema["minLength"]:
                    result.add_error(
                        f"{context}.{field_name}: length {len(value)} < minimum {field_schema['minLength']}"
                    )

    @staticmethod
    def _check_type(value: Any, expected_type: Any) -> bool:
        """
        Check if value matches expected type(s).

        Args:
            value: Value to check
            expected_type: Expected type (string or list of strings)

        Returns:
            True if type matches, False otherwise
        """
        if isinstance(expected_type, list):
            return any(SimulationValidator._check_type(value, t) for t in expected_type)

        type_map = {
            "string": str,
            "number": (int, float),
            "integer": int,
            "boolean": bool,
            "array": list,
            "object": dict,
            "null": type(None),
        }

        python_type = type_map.get(expected_type)
        if python_type is None:
            return True  # Unknown type, pass validation

        return isinstance(value, python_type)


class RegistryValidator:
    """
    Validator for registry data and dependencies.

    Provides methods to:
    - Check that all dependencies are satisfied
    - Verify that outputs match expected parameters
    - Validate computed values
    """

    @staticmethod
    def check_dependencies(
        sim: 'SimulationBase',
        registry: 'PMRegistry'
    ) -> ValidationResult:
        """
        Check that all required parameters are present in the registry.

        Args:
            sim: SimulationBase instance
            registry: PMRegistry instance

        Returns:
            ValidationResult indicating missing parameters
        """
        result = ValidationResult(passed=True)

        for param_path in sim.required_inputs:
            if not registry.has_param(param_path):
                entry = registry.get_entry(param_path)
                if entry and entry.status == "ESTABLISHED":
                    result.add_error(f"Missing ESTABLISHED param: {param_path}")
                else:
                    result.add_error(
                        f"Missing computed param: {param_path} - run dependency first"
                    )

        return result

    @staticmethod
    def check_outputs(
        sim: 'SimulationBase',
        results: Dict[str, Any],
        registry: 'PMRegistry'
    ) -> ValidationResult:
        """
        Check that all expected output parameters were computed correctly.

        Args:
            sim: SimulationBase instance
            results: Dictionary of computed results
            registry: PMRegistry instance

        Returns:
            ValidationResult indicating issues with outputs
        """
        result = ValidationResult(passed=True)

        for param_path in sim.output_params:
            if param_path not in results:
                result.add_error(f"Missing output: {param_path}")
            else:
                value = results[param_path]

                # Check for NaN/Inf
                if isinstance(value, float):
                    if math.isnan(value) or math.isinf(value):
                        result.add_error(f"Invalid value for {param_path}: {value}")

                # Check against existing value in registry
                existing = registry.get_entry(param_path)
                if existing is not None:
                    old_val = existing.value
                    if isinstance(old_val, (int, float)) and isinstance(value, (int, float)):
                        if old_val != 0:
                            rel_diff = abs(value - old_val) / abs(old_val)
                            if rel_diff > 0.01:  # 1% tolerance
                                result.add_warning(
                                    f"Value mismatch for {param_path}: "
                                    f"existing={old_val}, new={value}"
                                )

        return result

    @staticmethod
    def validate_against_bounds(
        registry: 'PMRegistry'
    ) -> ValidationResult:
        """
        Validate all predicted parameters against experimental bounds.

        Args:
            registry: PMRegistry instance

        Returns:
            ValidationResult with any bound violations
        """
        result = ValidationResult(passed=True)

        for path, entry in registry._parameters.items():
            if entry.status not in ["DERIVED", "PREDICTED"]:
                continue

            meta = entry.metadata or {}
            bound = meta.get('experimental_bound')
            bound_type = meta.get('bound_type')

            if bound is None or bound_type is None:
                continue

            value = entry.value

            if bound_type == "lower" and value < bound:
                result.add_error(
                    f"{path}: value {value} violates lower bound {bound}"
                )
            elif bound_type == "upper" and value > bound:
                result.add_error(
                    f"{path}: value {value} violates upper bound {bound}"
                )

        return result
