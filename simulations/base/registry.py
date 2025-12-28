"""
PMRegistry - Central Parameter, Formula, and Section Registry
===============================================================

Singleton registry for managing all computed parameters, formulas,
and section content in Principia Metaphysica simulations.

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.
"""

from dataclasses import dataclass, field
from typing import Dict, Any, Optional, List
from datetime import datetime
import warnings


@dataclass
class RegistryEntry:
    """
    Entry in the parameter registry.

    Attributes:
        value: The parameter value
        source: Source of the value (simulation ID or "ESTABLISHED:SOURCE")
        uncertainty: Optional uncertainty/error
        status: Status ("ESTABLISHED", "GEOMETRIC", "DERIVED", "PREDICTED", "CALIBRATED")
        timestamp: When the value was set
        metadata: Additional metadata
    """
    value: Any
    source: str
    uncertainty: Optional[float] = None
    status: str = "DERIVED"
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class FormulaEntry:
    """
    Entry in the formula registry.

    Attributes:
        formula: The Formula object
        timestamp: When the formula was added
    """
    formula: 'Formula'
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())


@dataclass
class SectionEntry:
    """
    Entry in the section registry.

    Attributes:
        content: The SectionContent object
        timestamp: When the section was added
    """
    content: 'SectionContent'
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())


class PMRegistry:
    """
    Singleton registry for parameters, formulas, and sections.

    This registry serves as the central data store for all simulation
    results, allowing simulations to:
    1. Read input parameters
    2. Write computed parameters
    3. Register formulas and section content
    4. Track provenance and dependencies

    Example Usage:
        registry = PMRegistry.get_instance()

        # Set a parameter
        registry.set_param("gauge.M_GUT", 2.1e16, source="gauge_unification_v16_0")

        # Get a parameter
        M_GUT = registry.get_param("gauge.M_GUT")

        # Check if parameter exists
        if registry.has_param("gauge.ALPHA_GUT"):
            alpha_GUT = registry.get_param("gauge.ALPHA_GUT")

        # Export all data
        params = registry.export_parameters()
        formulas = registry.export_formulas()
        sections = registry.export_sections()
    """

    _instance: Optional['PMRegistry'] = None

    def __new__(cls):
        """Singleton pattern - return existing instance or create new one."""
        if cls._instance is None:
            instance = super().__new__(cls)
            instance._init_registry()
            cls._instance = instance
        return cls._instance

    def _init_registry(self) -> None:
        """Initialize all internal data structures."""
        # Parameter registry: path -> RegistryEntry
        self._parameters: Dict[str, RegistryEntry] = {}

        # Formula registry: formula_id -> FormulaEntry
        self._formulas: Dict[str, FormulaEntry] = {}

        # Section registry: section_id -> SectionEntry
        self._sections: Dict[str, SectionEntry] = {}

        # Provenance tracking: output_path -> [source_simulation_ids]
        self._provenance: Dict[str, List[str]] = {}

        # Mismatch log for debugging
        self._mismatches: List[Dict[str, Any]] = []

    @classmethod
    def get_instance(cls) -> 'PMRegistry':
        """
        Get the singleton instance of PMRegistry.

        Returns:
            The singleton PMRegistry instance
        """
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    @classmethod
    def reset_instance(cls) -> None:
        """Reset the singleton instance (for testing)."""
        if cls._instance is not None:
            cls._instance._init_registry()

    # -------------------------------------------------------------------------
    # Parameter Management
    # -------------------------------------------------------------------------

    def has_param(self, path: str) -> bool:
        """
        Check if a parameter exists in the registry.

        Args:
            path: Parameter path (e.g., "gauge.M_GUT")

        Returns:
            True if parameter exists, False otherwise
        """
        return path in self._parameters

    def get_param(self, path: str) -> Any:
        """
        Get a parameter value from the registry.

        Args:
            path: Parameter path

        Returns:
            Parameter value

        Raises:
            KeyError: If parameter doesn't exist
        """
        if path not in self._parameters:
            raise KeyError(f"Parameter '{path}' not found in registry")
        return self._parameters[path].value

    def get(self, path: str) -> Any:
        """Alias for get_param for convenience."""
        return self.get_param(path)

    def get_entry(self, path: str) -> Optional[RegistryEntry]:
        """
        Get the full registry entry for a parameter.

        Args:
            path: Parameter path

        Returns:
            RegistryEntry or None if not found
        """
        return self._parameters.get(path)

    def set_param(
        self,
        path: str,
        value: Any,
        source: str,
        uncertainty: Optional[float] = None,
        status: str = "DERIVED",
        metadata: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        Set a parameter in the registry.

        Args:
            path: Parameter path (e.g., "gauge.M_GUT")
            value: Parameter value
            source: Source identifier (simulation ID or "ESTABLISHED:SOURCE")
            uncertainty: Optional uncertainty
            status: Status ("ESTABLISHED", "GEOMETRIC", "DERIVED", "PREDICTED", "CALIBRATED")
            metadata: Optional additional metadata
        """
        # Check for overwrites and warn if value differs significantly
        if path in self._parameters:
            existing = self._parameters[path]
            # Prevent overwriting ESTABLISHED params
            if existing.status == "ESTABLISHED" and not source.startswith("ESTABLISHED"):
                raise ValueError(f"Cannot override ESTABLISHED param '{path}'")
            self.warn_mismatch(path, value, source)

        entry = RegistryEntry(
            value=value,
            source=source,
            uncertainty=uncertainty,
            status=status,
            metadata=metadata or {}
        )

        self._parameters[path] = entry

        # Track provenance
        if path not in self._provenance:
            self._provenance[path] = []
        self._provenance[path].append(source)

    # -------------------------------------------------------------------------
    # Formula Management
    # -------------------------------------------------------------------------

    def add_formula(self, formula: 'Formula') -> None:
        """
        Add a formula to the registry.

        Args:
            formula: Formula instance to add
        """
        if formula.id in self._formulas:
            warnings.warn(f"Overwriting formula {formula.id}")

        self._formulas[formula.id] = FormulaEntry(formula=formula)

    def get_formula(self, formula_id: str) -> Optional['Formula']:
        """
        Get a formula by ID.

        Args:
            formula_id: Formula ID (e.g., "proton-lifetime")

        Returns:
            Formula instance or None if not found
        """
        entry = self._formulas.get(formula_id)
        return entry.formula if entry else None

    def has_formula(self, formula_id: str) -> bool:
        """
        Check if a formula exists.

        Args:
            formula_id: Formula ID

        Returns:
            True if formula exists, False otherwise
        """
        return formula_id in self._formulas

    # -------------------------------------------------------------------------
    # Section Management
    # -------------------------------------------------------------------------

    def add_section_content(
        self,
        section_id: str,
        content: 'SectionContent'
    ) -> None:
        """
        Add section content to the registry.

        Args:
            section_id: Section identifier (e.g., "4", "4.6")
            content: SectionContent instance
        """
        if section_id in self._sections:
            warnings.warn(f"Overwriting section {section_id}")

        self._sections[section_id] = SectionEntry(content=content)

    def get_section(self, section_id: str) -> Optional['SectionContent']:
        """
        Get section content by ID.

        Args:
            section_id: Section identifier

        Returns:
            SectionContent instance or None if not found
        """
        entry = self._sections.get(section_id)
        return entry.content if entry else None

    def has_section(self, section_id: str) -> bool:
        """
        Check if a section exists.

        Args:
            section_id: Section identifier

        Returns:
            True if section exists, False otherwise
        """
        return section_id in self._sections

    # -------------------------------------------------------------------------
    # Export Methods
    # -------------------------------------------------------------------------

    def export_parameters(self) -> Dict[str, Dict[str, Any]]:
        """
        Export all parameters as a dictionary.

        Returns:
            Dictionary mapping parameter paths to their full entries
        """
        result = {}
        for path, entry in self._parameters.items():
            result[path] = {
                'value': entry.value,
                'source': entry.source,
                'uncertainty': entry.uncertainty,
                'status': entry.status,
                'timestamp': entry.timestamp,
                'metadata': entry.metadata,
            }
        return result

    def export_formulas(self) -> Dict[str, Dict[str, Any]]:
        """
        Export all formulas as a dictionary.

        Returns:
            Dictionary mapping formula IDs to formula data
        """
        result = {}
        for formula_id, entry in self._formulas.items():
            f = entry.formula
            result[formula_id] = {
                'id': f.id,
                'label': f.label,
                'latex': f.latex,
                'plain_text': f.plain_text,
                'category': f.category,
                'description': f.description,
                'input_params': f.input_params,
                'output_params': f.output_params,
                'derivation': f.derivation,
                'terms': f.terms,
                'timestamp': entry.timestamp,
            }
        return result

    def export_sections(self) -> Dict[str, Dict[str, Any]]:
        """
        Export all sections as a dictionary.

        Returns:
            Dictionary mapping section IDs to section data
        """
        result = {}
        for section_id, entry in self._sections.items():
            s = entry.content
            result[section_id] = {
                'section_id': s.section_id,
                'subsection_id': s.subsection_id,
                'title': s.title,
                'abstract': s.abstract,
                'content_blocks': [
                    {
                        'type': block.type,
                        'content': block.content,
                        'formula_id': block.formula_id,
                        'label': block.label,
                    }
                    for block in s.content_blocks
                ],
                'formula_refs': s.formula_refs,
                'param_refs': s.param_refs,
                'timestamp': entry.timestamp,
            }
        return result

    def export_provenance(self) -> Dict[str, List[str]]:
        """
        Export provenance tracking.

        Returns:
            Dictionary mapping output paths to source simulation IDs
        """
        return dict(self._provenance)

    # -------------------------------------------------------------------------
    # Mismatch Tracking
    # -------------------------------------------------------------------------

    def warn_mismatch(self, path: str, new_value: Any, new_source: str) -> None:
        """
        Warn if setting a parameter that already exists with a different value.

        Args:
            path: Parameter path
            new_value: New value being set
            new_source: Source of new value
        """
        if path not in self._parameters:
            return

        old_entry = self._parameters[path]
        old_value = old_entry.value

        # Check for significant differences (handle floats with tolerance)
        try:
            if isinstance(old_value, (int, float)) and isinstance(new_value, (int, float)):
                if old_value != 0:
                    rel_diff = abs(new_value - old_value) / abs(old_value)
                    if rel_diff > 0.01:  # 1% tolerance
                        self._log_mismatch(path, old_value, old_entry.source, new_value, new_source)
            elif old_value != new_value:
                self._log_mismatch(path, old_value, old_entry.source, new_value, new_source)
        except Exception:
            # If comparison fails, log it
            if old_value != new_value:
                self._log_mismatch(path, old_value, old_entry.source, new_value, new_source)

    def _log_mismatch(
        self,
        path: str,
        old_value: Any,
        old_source: str,
        new_value: Any,
        new_source: str
    ) -> None:
        """
        Log a parameter mismatch.

        Args:
            path: Parameter path
            old_value: Previous value
            old_source: Source of previous value
            new_value: New value
            new_source: Source of new value
        """
        mismatch = {
            'path': path,
            'old_value': old_value,
            'old_source': old_source,
            'new_value': new_value,
            'new_source': new_source,
            'timestamp': datetime.now().isoformat(),
        }

        self._mismatches.append(mismatch)

        warnings.warn(
            f"Parameter mismatch for '{path}':\n"
            f"  Old: {old_value} (from {old_source})\n"
            f"  New: {new_value} (from {new_source})"
        )

    def get_mismatches(self) -> List[Dict[str, Any]]:
        """
        Get all logged mismatches.

        Returns:
            List of mismatch records
        """
        return list(self._mismatches)

    def validate_all(self) -> List[str]:
        """
        Return list of validation issues.

        Returns:
            List of issue descriptions
        """
        issues = []
        for path, entry in self._parameters.items():
            if entry.status == "DERIVED" and not self._provenance.get(path):
                issues.append(f"{path}: DERIVED but no source simulation")
        return issues
