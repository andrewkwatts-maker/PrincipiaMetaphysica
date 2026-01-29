"""
Simulation Return Schema
=========================

Defines the comprehensive return schema that all v16 simulations must follow.
All fields are mandatory (but can be empty lists/dicts) to ensure schema compliance.

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.

Dedicated To:
    My Wife: Elizabeth May Watts
    Our Messiah: Jesus Of Nazareth
"""

from dataclasses import dataclass, field, asdict
from typing import Dict, Any, List, Optional
from enum import Enum
import json


class ValidationStatus(str, Enum):
    """Validation status for parameters against experimental bounds."""
    PASS = "PASS"           # Within bounds or above lower bounds
    FAIL = "FAIL"           # Outside bounds
    MARGINAL = "MARGINAL"   # Close to bounds (within 1 sigma)
    UNKNOWN = "UNKNOWN"     # No experimental bound to compare
    NA = "N/A"              # Not applicable (e.g., ESTABLISHED params)


class ParameterStatus(str, Enum):
    """Parameter provenance status."""
    ESTABLISHED = "ESTABLISHED"   # From PDG/NuFIT/DESI - cannot override
    GEOMETRIC = "GEOMETRIC"       # From G2 topology - cannot override
    DERIVED = "DERIVED"           # Computed from ESTABLISHED + THEORY
    PREDICTED = "PREDICTED"       # Testable predictions
    CALIBRATED = "CALIBRATED"     # O(1) coefficients
    SYSTEM = "SYSTEM"             # Non-scientific metadata (version, timestamps, etc.)


class FormulaCategory(str, Enum):
    """Formula category based on derivation chain."""
    ESTABLISHED = "ESTABLISHED"   # Standard physics (axioms)
    THEORY = "THEORY"             # PM-specific theoretical formulas
    DERIVED = "DERIVED"           # Computed from THEORY + ESTABLISHED
    PREDICTIONS = "PREDICTIONS"   # Testable predictions


@dataclass
class ReferenceEntry:
    """A bibliographic reference."""
    id: str                       # e.g., "langacker1981"
    authors: str                  # e.g., "Langacker, P."
    title: str                    # e.g., "Grand Unified Theories"
    journal: str = ""             # e.g., "Phys. Rep."
    volume: str = ""              # e.g., "72"
    pages: str = ""               # e.g., "185-385"
    year: int = 0                 # e.g., 1981
    arxiv: str = ""               # e.g., "hep-ph/9801234"
    doi: str = ""                 # e.g., "10.1016/..."
    url: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class FoundationEntry:
    """A foundation physics concept/formula referenced by the simulation."""
    id: str                       # e.g., "einstein-field-equations"
    title: str                    # e.g., "Einstein Field Equations"
    category: str                 # e.g., "general_relativity"
    latex: str = ""               # Main formula LaTeX
    description: str = ""         # Brief description
    prerequisites: List[str] = field(default_factory=list)  # Other foundation IDs
    references: List[str] = field(default_factory=list)     # Reference IDs

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class FormulaEntry:
    """Full formula metadata for schema compliance."""
    id: str
    label: str                    # e.g., "(4.12)"
    section: str                  # e.g., "4"
    sectionId: str                # e.g., "4.6"
    equationNumber: str           # e.g., "4.12"
    latex: str
    plainText: str
    category: str                 # FormulaCategory value
    description: str
    inputParams: List[str] = field(default_factory=list)
    outputParams: List[str] = field(default_factory=list)
    derivedFrom: List[str] = field(default_factory=list)    # Parent formula IDs
    derivation: Dict[str, Any] = field(default_factory=dict)
    terms: Dict[str, Any] = field(default_factory=dict)
    computedValue: Optional[Any] = None
    units: str = ""
    status: str = "active"
    validated: bool = False

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class ParameterEntry:
    """Full parameter metadata for schema compliance."""
    path: str                     # e.g., "proton_decay.tau_p_years"
    name: str                     # e.g., "Proton Lifetime"
    symbol: str = ""              # e.g., "tau_p"
    latex: str = ""               # e.g., r"\tau_p"
    value: Any = None             # Computed value
    uncertainty: Optional[float] = None
    units: str = ""
    status: str = ""              # ParameterStatus value
    source: str = ""              # Source simulation ID or "ESTABLISHED:PDG2024"
    description: str = ""
    derivationFormula: str = ""   # Formula ID that derives this
    experimentalValue: Optional[float] = None
    experimentalUncertainty: Optional[float] = None
    experimentalSource: str = ""
    experimentalBound: Optional[float] = None
    boundType: str = ""           # "upper", "lower", "range", "measured"
    boundSource: str = ""
    validationStatus: str = ""    # ValidationStatus value
    validationRatio: Optional[float] = None  # value / bound
    validationMessage: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class SectionEntry:
    """Section content for the paper."""
    sectionId: str                # e.g., "4.6"
    parentSection: str = ""       # e.g., "4"
    title: str = ""
    abstract: str = ""
    contentBlocks: List[Dict[str, Any]] = field(default_factory=list)
    formulaRefs: List[str] = field(default_factory=list)
    paramRefs: List[str] = field(default_factory=list)
    foundationRefs: List[str] = field(default_factory=list)
    referenceRefs: List[str] = field(default_factory=list)
    subsections: List[Dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class InputValidationEntry:
    """Input parameter validation result."""
    path: str
    required: bool
    present: bool
    value: Any = None
    source: str = ""
    status: str = ""              # "OK", "MISSING", "INVALID"
    message: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class TypeDataEntry:
    """Type information for parameters."""
    path: str
    expectedType: str             # "float", "int", "string", "array"
    actualType: str = ""
    isNumeric: bool = False
    isFinite: bool = True
    range: List[float] = field(default_factory=list)  # [min, max] if applicable

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class CertificateEntry:
    """A certificate assertion for simulation outputs (SSOT Rule 4)."""
    id: str                       # e.g., "CERT_G2_RICCI_FLAT"
    assertion: str                # What is being certified
    condition: str                # Mathematical condition (evaluable expression)
    tolerance: float = 0.0       # Numerical tolerance
    status: str = "OFFLINE"      # "PASS", "FAIL", "OFFLINE"
    wolfram_query: Optional[str] = None  # Wolfram Alpha query string
    wolfram_result: Optional[str] = None  # Returned result or "OFFLINE"
    sector: str = ""             # Domain category
    simulation_source: str = ""  # Source simulation ID

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class ProofEntry:
    """A mathematical proof (SSOT Rule for proofs)."""
    id: str                       # e.g., "P_G2_RICCI_FLAT"
    theorem: str                  # Statement of the theorem
    steps: List[str] = field(default_factory=list)  # Proof steps
    qed: str = ""                # QED conclusion statement
    simulation_source: str = ""  # Source simulation ID

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class DiscoveryEntry:
    """A discovery claim from simulation results."""
    id: str                       # e.g., "D_ALPHA_GEOMETRIC"
    claim: str                    # Discovery claim statement
    evidence: str = ""           # Supporting evidence summary
    significance: str = ""       # Scientific significance
    simulation_source: str = ""  # Source simulation ID
    confidence: str = "medium"   # "high", "medium", "speculative"

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class LearningMaterialEntry:
    """An educational resource for AI validation (SSOT Rule 7)."""
    topic: str                    # Physics concept
    url: str                      # Link to resource
    relevance: str = ""          # How this concept is used
    validation_hint: str = ""    # What an AI reviewer should check

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class GateCheckEntry:
    """A gate check result (SSOT Rule 9)."""
    gate_id: str                  # Gate identifier
    simulation_id: str            # Source simulation ID
    assertion: str                # What the gate checks
    result: str = "PASS"         # "PASS" or "FAIL"
    timestamp: str = ""          # ISO timestamp
    details: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class SelfValidationEntry:
    """Self-validation result (SSOT Rule 5)."""
    name: str                     # Check description
    passed: bool = True          # Pass/fail
    confidence_interval: Dict[str, float] = field(default_factory=dict)  # lower, upper, sigma
    log_level: str = "INFO"      # "DEBUG", "INFO", "WARNING", "ERROR"
    message: str = ""            # Result message

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class SimulationResult:
    """
    Comprehensive simulation result that must be returned by all v16 simulations.

    All fields are mandatory (but can be empty) to ensure schema compliance.
    """
    # Metadata
    simulationId: str             # e.g., "proton_decay_v16_0"
    version: str                  # e.g., "16.0"
    domain: str                   # e.g., "proton"
    title: str
    timestamp: str = ""           # ISO format
    executionTimeMs: float = 0.0

    # Required content sections (even if empty)
    sections: List[SectionEntry] = field(default_factory=list)
    foundations: List[FoundationEntry] = field(default_factory=list)
    references: List[ReferenceEntry] = field(default_factory=list)
    formulas: List[FormulaEntry] = field(default_factory=list)

    # Parameters (both input and output)
    inputParameters: List[ParameterEntry] = field(default_factory=list)
    outputParameters: List[ParameterEntry] = field(default_factory=list)

    # Validation
    inputValidation: List[InputValidationEntry] = field(default_factory=list)
    outputValidation: List[Dict[str, Any]] = field(default_factory=list)

    # Type data
    typeData: List[TypeDataEntry] = field(default_factory=list)

    # Raw computed values (for backwards compatibility)
    computedValues: Dict[str, Any] = field(default_factory=dict)

    # SSOT extensions (Phase 3)
    certificates: List[CertificateEntry] = field(default_factory=list)
    proofs: List[ProofEntry] = field(default_factory=list)
    discoveries: List[DiscoveryEntry] = field(default_factory=list)
    learningMaterials: List[LearningMaterialEntry] = field(default_factory=list)
    gateChecks: List[GateCheckEntry] = field(default_factory=list)
    selfValidation: List[SelfValidationEntry] = field(default_factory=list)

    # Status
    success: bool = True
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        result = {
            "simulationId": self.simulationId,
            "version": self.version,
            "domain": self.domain,
            "title": self.title,
            "timestamp": self.timestamp,
            "executionTimeMs": self.executionTimeMs,
            "sections": [s.to_dict() if hasattr(s, 'to_dict') else s for s in self.sections],
            "foundations": [f.to_dict() if hasattr(f, 'to_dict') else f for f in self.foundations],
            "references": [r.to_dict() if hasattr(r, 'to_dict') else r for r in self.references],
            "formulas": [f.to_dict() if hasattr(f, 'to_dict') else f for f in self.formulas],
            "inputParameters": [p.to_dict() if hasattr(p, 'to_dict') else p for p in self.inputParameters],
            "outputParameters": [p.to_dict() if hasattr(p, 'to_dict') else p for p in self.outputParameters],
            "inputValidation": [v.to_dict() if hasattr(v, 'to_dict') else v for v in self.inputValidation],
            "outputValidation": self.outputValidation,
            "typeData": [t.to_dict() if hasattr(t, 'to_dict') else t for t in self.typeData],
            "computedValues": self.computedValues,
            # SSOT extensions
            "certificates": [c.to_dict() if hasattr(c, 'to_dict') else c for c in self.certificates],
            "proofs": [p.to_dict() if hasattr(p, 'to_dict') else p for p in self.proofs],
            "discoveries": [d.to_dict() if hasattr(d, 'to_dict') else d for d in self.discoveries],
            "learningMaterials": [m.to_dict() if hasattr(m, 'to_dict') else m for m in self.learningMaterials],
            "gateChecks": [g.to_dict() if hasattr(g, 'to_dict') else g for g in self.gateChecks],
            "selfValidation": [v.to_dict() if hasattr(v, 'to_dict') else v for v in self.selfValidation],
            "success": self.success,
            "errors": self.errors,
            "warnings": self.warnings,
        }
        return result

    def to_json(self, indent: int = 2) -> str:
        """Convert to JSON string."""
        return json.dumps(self.to_dict(), indent=indent, default=str)


# JSON Schema for validation
SIMULATION_RESULT_SCHEMA = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "SimulationResult",
    "description": "Comprehensive simulation result schema for v16 simulations",
    "type": "object",
    "required": [
        "simulationId", "version", "domain", "title",
        "sections", "foundations", "references", "formulas",
        "inputParameters", "outputParameters", "inputValidation",
        "typeData", "computedValues", "success"
    ],
    "properties": {
        "simulationId": {"type": "string", "pattern": "^[a-z_]+_v\\d+_\\d+$"},
        "version": {"type": "string", "pattern": "^\\d+\\.\\d+$"},
        "domain": {"type": "string"},
        "title": {"type": "string", "minLength": 1},
        "timestamp": {"type": "string"},
        "executionTimeMs": {"type": "number"},

        "sections": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["sectionId"],
                "properties": {
                    "sectionId": {"type": "string"},
                    "parentSection": {"type": "string"},
                    "title": {"type": "string"},
                    "abstract": {"type": "string"},
                    "contentBlocks": {"type": "array"},
                    "formulaRefs": {"type": "array", "items": {"type": "string"}},
                    "paramRefs": {"type": "array", "items": {"type": "string"}},
                    "foundationRefs": {"type": "array", "items": {"type": "string"}},
                    "referenceRefs": {"type": "array", "items": {"type": "string"}},
                    "subsections": {"type": "array"}
                }
            }
        },

        "foundations": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["id", "title", "category"],
                "properties": {
                    "id": {"type": "string"},
                    "title": {"type": "string"},
                    "category": {"type": "string"},
                    "latex": {"type": "string"},
                    "description": {"type": "string"},
                    "prerequisites": {"type": "array", "items": {"type": "string"}},
                    "references": {"type": "array", "items": {"type": "string"}}
                }
            }
        },

        "references": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["id", "authors", "title"],
                "properties": {
                    "id": {"type": "string"},
                    "authors": {"type": "string"},
                    "title": {"type": "string"},
                    "journal": {"type": "string"},
                    "volume": {"type": "string"},
                    "pages": {"type": "string"},
                    "year": {"type": "integer"},
                    "arxiv": {"type": "string"},
                    "doi": {"type": "string"},
                    "url": {"type": "string"}
                }
            }
        },

        "formulas": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["id", "label", "latex", "category"],
                "properties": {
                    "id": {"type": "string"},
                    "label": {"type": "string"},
                    "section": {"type": "string"},
                    "sectionId": {"type": "string"},
                    "equationNumber": {"type": "string"},
                    "latex": {"type": "string"},
                    "plainText": {"type": "string"},
                    "category": {"type": "string", "enum": ["ESTABLISHED", "THEORY", "DERIVED", "PREDICTIONS"]},
                    "description": {"type": "string"},
                    "inputParams": {"type": "array", "items": {"type": "string"}},
                    "outputParams": {"type": "array", "items": {"type": "string"}},
                    "derivedFrom": {"type": "array", "items": {"type": "string"}},
                    "derivation": {"type": "object"},
                    "terms": {"type": "object"},
                    "computedValue": {},
                    "units": {"type": "string"},
                    "status": {"type": "string"},
                    "validated": {"type": "boolean"}
                }
            }
        },

        "inputParameters": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["path", "name"],
                "properties": {
                    "path": {"type": "string"},
                    "name": {"type": "string"},
                    "symbol": {"type": "string"},
                    "latex": {"type": "string"},
                    "value": {},
                    "uncertainty": {"type": ["number", "null"]},
                    "units": {"type": "string"},
                    "status": {"type": "string"},
                    "source": {"type": "string"},
                    "description": {"type": "string"}
                }
            }
        },

        "outputParameters": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["path", "name", "value"],
                "properties": {
                    "path": {"type": "string"},
                    "name": {"type": "string"},
                    "symbol": {"type": "string"},
                    "latex": {"type": "string"},
                    "value": {},
                    "uncertainty": {"type": ["number", "null"]},
                    "units": {"type": "string"},
                    "status": {"type": "string"},
                    "source": {"type": "string"},
                    "description": {"type": "string"},
                    "derivationFormula": {"type": "string"},
                    "experimentalValue": {"type": ["number", "null"]},
                    "experimentalUncertainty": {"type": ["number", "null"]},
                    "experimentalSource": {"type": "string"},
                    "experimentalBound": {"type": ["number", "null"]},
                    "boundType": {"type": "string"},
                    "boundSource": {"type": "string"},
                    "validationStatus": {"type": "string", "enum": ["PASS", "FAIL", "MARGINAL", "UNKNOWN", "N/A", ""]},
                    "validationRatio": {"type": ["number", "null"]},
                    "validationMessage": {"type": "string"}
                }
            }
        },

        "inputValidation": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["path", "required", "present"],
                "properties": {
                    "path": {"type": "string"},
                    "required": {"type": "boolean"},
                    "present": {"type": "boolean"},
                    "value": {},
                    "source": {"type": "string"},
                    "status": {"type": "string"},
                    "message": {"type": "string"}
                }
            }
        },

        "outputValidation": {"type": "array"},

        "typeData": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["path", "expectedType"],
                "properties": {
                    "path": {"type": "string"},
                    "expectedType": {"type": "string"},
                    "actualType": {"type": "string"},
                    "isNumeric": {"type": "boolean"},
                    "isFinite": {"type": "boolean"},
                    "range": {"type": "array", "items": {"type": "number"}}
                }
            }
        },

        "computedValues": {"type": "object"},
        "success": {"type": "boolean"},
        "errors": {"type": "array", "items": {"type": "string"}},
        "warnings": {"type": "array", "items": {"type": "string"}}
    }
}


def validate_simulation_result(result: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate a simulation result against the schema.

    Args:
        result: Dictionary to validate

    Returns:
        Dictionary with 'valid' boolean and 'errors' list
    """
    errors = []

    # Check required fields
    required = SIMULATION_RESULT_SCHEMA["required"]
    for field_name in required:
        if field_name not in result:
            errors.append(f"Missing required field: {field_name}")
        elif result[field_name] is None:
            errors.append(f"Required field is null: {field_name}")

    # Check types
    properties = SIMULATION_RESULT_SCHEMA["properties"]
    for field_name, field_schema in properties.items():
        if field_name not in result:
            continue

        value = result[field_name]
        expected_type = field_schema.get("type")

        if expected_type == "string" and not isinstance(value, str):
            errors.append(f"{field_name}: expected string, got {type(value).__name__}")
        elif expected_type == "number" and not isinstance(value, (int, float)):
            errors.append(f"{field_name}: expected number, got {type(value).__name__}")
        elif expected_type == "boolean" and not isinstance(value, bool):
            errors.append(f"{field_name}: expected boolean, got {type(value).__name__}")
        elif expected_type == "array" and not isinstance(value, list):
            errors.append(f"{field_name}: expected array, got {type(value).__name__}")
        elif expected_type == "object" and not isinstance(value, dict):
            errors.append(f"{field_name}: expected object, got {type(value).__name__}")

    # Check simulationId pattern
    if "simulationId" in result:
        import re
        pattern = r"^[a-z_]+_v\d+_\d+$"
        if not re.match(pattern, result["simulationId"]):
            errors.append(f"simulationId doesn't match pattern: {result['simulationId']}")

    return {
        "valid": len(errors) == 0,
        "errors": errors
    }


class SchemaCompliantSimulation:
    """
    Mixin class to add schema-compliant result generation to simulations.

    Usage:
        class MySimulation(SimulationBase, SchemaCompliantSimulation):
            ...

            def execute_with_schema(self, registry):
                return self.build_result(registry, self.run(registry))
    """

    def build_result(
        self,
        registry: 'PMRegistry',
        computed_values: Dict[str, Any],
        execution_time_ms: float = 0.0
    ) -> SimulationResult:
        """
        Build a schema-compliant SimulationResult from computed values.

        Args:
            registry: PMRegistry with input parameters
            computed_values: Dictionary of computed values from run()
            execution_time_ms: Execution time in milliseconds

        Returns:
            SimulationResult instance
        """
        from datetime import datetime
        import math

        metadata = self.metadata

        # Build input validation entries
        input_validation = []
        input_parameters = []
        for param_path in self.required_inputs:
            present = registry.has_param(param_path)
            value = registry.get_param(param_path) if present else None
            entry = registry.get_entry(param_path) if present else None

            input_validation.append(InputValidationEntry(
                path=param_path,
                required=True,
                present=present,
                value=value,
                source=entry.source if entry else "",
                status="OK" if present else "MISSING",
                message="" if present else f"Required parameter {param_path} not found"
            ))

            if present and entry:
                input_parameters.append(ParameterEntry(
                    path=param_path,
                    name=entry.metadata.get("description", param_path) if entry.metadata else param_path,
                    value=value,
                    uncertainty=entry.uncertainty,
                    units=entry.metadata.get("units", "") if entry.metadata else "",
                    status=entry.status,
                    source=entry.source,
                    description=entry.metadata.get("description", "") if entry.metadata else ""
                ))

        # Build output parameter entries with validation
        output_parameters = []
        type_data = []
        for param_def in self.get_output_param_definitions():
            value = computed_values.get(param_def.path)

            # Determine validation status
            validation_status = ValidationStatus.UNKNOWN.value
            validation_ratio = None
            validation_message = ""

            if param_def.experimental_bound is not None and value is not None:
                if param_def.bound_type == "lower":
                    validation_ratio = value / param_def.experimental_bound
                    if validation_ratio > 1.5:
                        validation_status = ValidationStatus.PASS.value
                        validation_message = f"Value {value:.2e} is {validation_ratio:.2f}x above lower bound"
                    elif validation_ratio > 1.0:
                        validation_status = ValidationStatus.MARGINAL.value
                        validation_message = f"Value {value:.2e} is only {validation_ratio:.2f}x above lower bound"
                    else:
                        validation_status = ValidationStatus.FAIL.value
                        validation_message = f"Value {value:.2e} violates lower bound {param_def.experimental_bound:.2e}"
                elif param_def.bound_type == "upper":
                    validation_ratio = value / param_def.experimental_bound
                    if validation_ratio < 0.5:
                        validation_status = ValidationStatus.PASS.value
                        validation_message = f"Value {value:.2e} is well below upper bound"
                    elif validation_ratio < 1.0:
                        validation_status = ValidationStatus.MARGINAL.value
                        validation_message = f"Value {value:.2e} is close to upper bound"
                    else:
                        validation_status = ValidationStatus.FAIL.value
                        validation_message = f"Value {value:.2e} violates upper bound {param_def.experimental_bound:.2e}"

            output_parameters.append(ParameterEntry(
                path=param_def.path,
                name=param_def.name,
                value=value,
                units=param_def.units,
                status=param_def.status,
                source=metadata.id,
                description=param_def.description,
                derivationFormula=param_def.derivation_formula or "",
                experimentalBound=param_def.experimental_bound,
                boundType=param_def.bound_type or "",
                boundSource=param_def.bound_source or "",
                validationStatus=validation_status,
                validationRatio=validation_ratio,
                validationMessage=validation_message
            ))

            # Type data
            actual_type = type(value).__name__ if value is not None else "null"
            is_numeric = isinstance(value, (int, float))
            is_finite = is_numeric and not (math.isnan(value) or math.isinf(value)) if is_numeric else True

            type_data.append(TypeDataEntry(
                path=param_def.path,
                expectedType="number" if param_def.units != "string" else "string",
                actualType=actual_type,
                isNumeric=is_numeric,
                isFinite=is_finite
            ))

        # Build formula entries
        formula_entries = []
        for formula in self.get_formulas():
            section_parts = metadata.section_id.split('.')
            formula_entries.append(FormulaEntry(
                id=formula.id,
                label=formula.label,
                section=section_parts[0] if section_parts else "",
                sectionId=metadata.section_id,
                equationNumber=formula.label.strip("()") if formula.label else "",
                latex=formula.latex,
                plainText=formula.plain_text,
                category=formula.category,
                description=formula.description,
                inputParams=formula.input_params,
                outputParams=formula.output_params,
                derivedFrom=formula.derivation.get("parentFormulas", []) if formula.derivation else [],
                derivation=formula.derivation or {},
                terms=formula.terms,
                computedValue=computed_values.get(formula.output_params[0]) if formula.output_params else None,
                units="",
                status="active",
                validated=True
            ))

        # Build section entries
        section_entries = []
        section_content = self.get_section_content()
        if section_content:
            content_blocks = []
            for block in section_content.content_blocks:
                content_blocks.append({
                    "type": block.type,
                    "content": block.content,
                    "formulaId": block.formula_id or "",
                    "label": block.label or ""
                })

            section_entries.append(SectionEntry(
                sectionId=section_content.subsection_id or section_content.section_id,
                parentSection=section_content.section_id if section_content.subsection_id else "",
                title=section_content.title,
                abstract=section_content.abstract,
                contentBlocks=content_blocks,
                formulaRefs=section_content.formula_refs,
                paramRefs=section_content.param_refs,
                foundationRefs=[],
                referenceRefs=[]
            ))

        # Build result
        return SimulationResult(
            simulationId=metadata.id,
            version=metadata.version,
            domain=metadata.domain,
            title=metadata.title,
            timestamp=datetime.now().isoformat(),
            executionTimeMs=execution_time_ms,
            sections=section_entries,
            foundations=[],  # To be populated by subclasses
            references=[],   # To be populated by subclasses
            formulas=formula_entries,
            inputParameters=input_parameters,
            outputParameters=output_parameters,
            inputValidation=input_validation,
            outputValidation=[],
            typeData=type_data,
            computedValues=computed_values,
            success=True,
            errors=[],
            warnings=[]
        )
