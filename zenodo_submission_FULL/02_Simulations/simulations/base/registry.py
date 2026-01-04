"""
PMRegistry - Central Parameter, Formula, and Section Registry
===============================================================

Singleton registry for managing all computed parameters, formulas,
and section content in Principia Metaphysica simulations.

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.

Dedicated To:
    My Wife: Elizabeth May Watts
    Our Messiah: Jesus Of Nazareth
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
        value: The parameter value (theory prediction or established value)
        source: Source of the value (simulation ID or "ESTABLISHED:SOURCE")
        uncertainty: Optional uncertainty/error on the theory prediction
        status: Status ("ESTABLISHED", "GEOMETRIC", "DERIVED", "PREDICTED", "CALIBRATED")
        timestamp: When the value was set
        metadata: Additional metadata

        # Experimental comparison fields (for validation)
        experimental_value: Experimental measurement for comparison (PDG, NuFIT, DESI, etc.)
        experimental_uncertainty: 1-sigma uncertainty on experimental value
        experimental_source: Citation for experimental value (e.g., "PDG2024", "NuFIT6.0")
        bound_type: Type of comparison ("measured", "upper", "lower", "range")

        # Validation results (computed from theory vs experiment)
        sigma_deviation: Number of sigmas between theory and experiment
        validation_status: "PASS", "MARGINAL", "TENSION", "FAIL", or "NO_DATA"
    """
    value: Any
    source: str
    uncertainty: Optional[float] = None
    status: str = "DERIVED"
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    metadata: Dict[str, Any] = field(default_factory=dict)

    # Experimental comparison fields
    experimental_value: Optional[float] = None
    experimental_uncertainty: Optional[float] = None
    experimental_source: Optional[str] = None
    bound_type: Optional[str] = None  # "measured", "upper", "lower", "range"

    # Validation results
    sigma_deviation: Optional[float] = None
    validation_status: Optional[str] = None  # "PASS", "MARGINAL", "TENSION", "FAIL", "NO_DATA"


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

    def get(self, path: str, default: Any = None) -> Any:
        """
        Get a parameter value with optional default.

        Args:
            path: Parameter path
            default: Value to return if parameter doesn't exist

        Returns:
            Parameter value or default if not found
        """
        if path not in self._parameters:
            if default is not None:
                return default
            raise KeyError(f"Parameter '{path}' not found in registry")
        return self._parameters[path].value

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
        metadata: Optional[Dict[str, Any]] = None,
        experimental_value: Optional[float] = None,
        experimental_uncertainty: Optional[float] = None,
        experimental_source: Optional[str] = None,
        bound_type: Optional[str] = None
    ) -> None:
        """
        Set a parameter in the registry.

        Args:
            path: Parameter path (e.g., "gauge.M_GUT")
            value: Parameter value (theory prediction)
            source: Source identifier (simulation ID or "ESTABLISHED:SOURCE")
            uncertainty: Optional uncertainty on theory prediction
            status: Status ("ESTABLISHED", "GEOMETRIC", "DERIVED", "PREDICTED", "CALIBRATED")
            metadata: Optional additional metadata
            experimental_value: Experimental measurement for comparison
            experimental_uncertainty: 1-sigma uncertainty on experimental value
            experimental_source: Citation (e.g., "PDG2024", "NuFIT6.0", "DESI2025")
            bound_type: Type of bound ("measured", "upper", "lower", "range")
        """
        # Check for overwrites and warn if value differs significantly
        if path in self._parameters:
            existing = self._parameters[path]
            # Prevent overwriting ESTABLISHED params
            if existing.status == "ESTABLISHED" and not source.startswith("ESTABLISHED"):
                raise ValueError(f"Cannot override ESTABLISHED param '{path}'")
            self.warn_mismatch(path, value, source)

        # Compute sigma deviation if we have experimental data
        sigma_deviation = None
        validation_status = "NO_DATA"

        if experimental_value is not None and value is not None:
            try:
                theory_val = float(value)
                exp_val = float(experimental_value)

                if bound_type in ("measured", "central_value") and experimental_uncertainty is not None and experimental_uncertainty > 0:
                    # Standard sigma calculation: |theory - exp| / sigma
                    sigma_deviation = abs(theory_val - exp_val) / experimental_uncertainty

                    if sigma_deviation < 1.0:
                        validation_status = "PASS"
                    elif sigma_deviation < 2.0:
                        validation_status = "MARGINAL"
                    elif sigma_deviation < 3.0:
                        validation_status = "TENSION"
                    else:
                        validation_status = "FAIL"

                elif bound_type in ("measured", "central_value") and experimental_uncertainty is None:
                    # No uncertainty provided - compute relative error
                    if exp_val != 0:
                        relative_error = abs(theory_val - exp_val) / abs(exp_val)
                        if relative_error < 0.01:  # Within 1%
                            validation_status = "PASS"
                        elif relative_error < 0.05:  # Within 5%
                            validation_status = "MARGINAL"
                        elif relative_error < 0.10:  # Within 10%
                            validation_status = "TENSION"
                        else:
                            validation_status = "FAIL"

                elif bound_type == "lower":
                    # Theory must exceed lower bound
                    if theory_val > exp_val:
                        validation_status = "PASS"
                        sigma_deviation = (theory_val - exp_val) / exp_val if exp_val != 0 else None
                    else:
                        validation_status = "FAIL"
                        sigma_deviation = (exp_val - theory_val) / exp_val if exp_val != 0 else None

                elif bound_type == "upper":
                    # Theory must be below upper bound
                    if theory_val < exp_val:
                        validation_status = "PASS"
                        sigma_deviation = (exp_val - theory_val) / exp_val if exp_val != 0 else None
                    else:
                        validation_status = "FAIL"
                        sigma_deviation = (theory_val - exp_val) / exp_val if exp_val != 0 else None

            except (TypeError, ValueError):
                # Non-numeric values, can't compute sigma
                pass

        entry = RegistryEntry(
            value=value,
            source=source,
            uncertainty=uncertainty,
            status=status,
            metadata=metadata or {},
            experimental_value=experimental_value,
            experimental_uncertainty=experimental_uncertainty,
            experimental_source=experimental_source,
            bound_type=bound_type,
            sigma_deviation=sigma_deviation,
            validation_status=validation_status
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
            section_id: Section identifier (e.g., "2", "4", "5")
            content: SectionContent instance

        Note:
            For appendices (where appendix=True), the subsection_id is used
            as the storage key to allow multiple appendices. The section_id
            indicates which section the appendix relates to.
        """
        # Use subsection_id as key for appendices (e.g., "A", "B", "C"...)
        key = section_id
        if content.appendix and content.subsection_id:
            key = content.subsection_id

        if key in self._sections:
            warnings.warn(f"Overwriting section {key}")

        self._sections[key] = SectionEntry(content=content)

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
        Export all parameters as a dictionary with full experimental validation data.

        Returns:
            Dictionary mapping parameter paths to their full entries including:
            - value: Theory prediction or established value
            - source: Source simulation or ESTABLISHED:* citation
            - uncertainty: Uncertainty on theory prediction
            - status: Parameter status (ESTABLISHED, GEOMETRIC, DERIVED, etc.)
            - experimental_value: Experimental measurement for comparison
            - experimental_uncertainty: 1-sigma uncertainty on experiment
            - experimental_source: Citation for experimental value
            - bound_type: Type of bound (measured, upper, lower, range)
            - sigma_deviation: Number of sigmas between theory and experiment
            - validation_status: PASS, MARGINAL, TENSION, FAIL, or NO_DATA
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
                # Experimental comparison fields
                'experimental_value': entry.experimental_value,
                'experimental_uncertainty': entry.experimental_uncertainty,
                'experimental_source': entry.experimental_source,
                'bound_type': entry.bound_type,
                # Validation results
                'sigma_deviation': entry.sigma_deviation,
                'validation_status': entry.validation_status,
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
            # Generate title from description if not set
            title = getattr(f, 'title', None)
            if not title and f.description:
                title = f.description.split('.')[0].strip()[:80]
            result[formula_id] = {
                'id': f.id,
                'label': f.label,
                'latex': f.latex,
                'plain_text': f.plain_text,
                'category': f.category,
                'description': f.description,
                'title': title,
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
            # Build content_blocks with all fields
            content_blocks = []
            for block in s.content_blocks:
                block_data = {
                    'type': block.type,
                    'content': block.content,
                }
                if block.formula_id:
                    block_data['formula_id'] = block.formula_id
                if block.label:
                    block_data['label'] = block.label
                    block_data['equationNumber'] = block.label
                if block.level:
                    block_data['level'] = block.level
                if block.items:
                    block_data['items'] = block.items
                if block.headers:
                    block_data['headers'] = block.headers
                if block.rows:
                    block_data['rows'] = block.rows
                content_blocks.append(block_data)

            # Use 'id' as expected by website renderer (not 'section_id')
            # Determine order based on appendix flag
            if s.appendix and s.subsection_id:
                # Appendices come after main sections (100+)
                order = 100 + ord(s.subsection_id.upper()) - ord('A')
            elif s.section_id and s.section_id[0].isdigit():
                order = int(s.section_id.split('.')[0])
            else:
                order = 99

            result[section_id] = {
                'id': s.section_id,
                'appendix': s.appendix,  # Boolean: render at end of paper
                'subsection_id': s.subsection_id,  # Appendix letter (A, B, C...)
                'type': 'appendix' if s.appendix else 'section',  # For renderer compatibility
                'section_type': s.section_type,  # Deprecated, kept for compatibility
                'title': s.title,
                'shortTitle': s.title,
                'order': order,
                'abstract': s.abstract,
                'contentBlocks': content_blocks,  # camelCase for website compatibility
                'content_blocks': content_blocks,  # snake_case for Python compatibility
                'formulaRefs': s.formula_refs,
                'paramRefs': s.param_refs,
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

    # -------------------------------------------------------------------------
    # Accuracy Validation (Sigma Deviation Computation)
    # -------------------------------------------------------------------------

    def compute_sigma_deviation(
        self,
        predicted_value: float,
        experimental_path: str
    ) -> Dict[str, Any]:
        """
        Compute sigma deviation between predicted and experimental values.

        Args:
            predicted_value: The theory prediction
            experimental_path: Path to experimental value (e.g., "desi.w0")

        Returns:
            Dictionary with deviation analysis:
            {
                'predicted': float,
                'experimental': float,
                'uncertainty': float,
                'sigma': float,
                'status': str,  # 'EXCELLENT'/'GOOD'/'ACCEPTABLE'/'TENSION'
                'source': str
            }
        """
        if not self.has_param(experimental_path):
            return {
                'predicted': predicted_value,
                'experimental': None,
                'uncertainty': None,
                'sigma': None,
                'status': 'MISSING_DATA',
                'source': None
            }

        entry = self.get_entry(experimental_path)
        exp_value = entry.value
        uncertainty = entry.uncertainty or 0.0

        if uncertainty == 0:
            # No uncertainty available
            sigma = None
            status = 'NO_UNCERTAINTY'
        else:
            sigma = abs(predicted_value - exp_value) / uncertainty
            if sigma < 1.0:
                status = 'EXCELLENT'
            elif sigma < 2.0:
                status = 'GOOD'
            elif sigma < 3.0:
                status = 'ACCEPTABLE'
            else:
                status = 'TENSION'

        return {
            'predicted': predicted_value,
            'experimental': exp_value,
            'uncertainty': uncertainty,
            'sigma': sigma,
            'status': status,
            'source': entry.source
        }

    def validate_prediction(
        self,
        prediction_path: str,
        experimental_path: str,
        metadata_key: str = 'validation'
    ) -> Dict[str, Any]:
        """
        Validate a prediction against experimental data and store result.

        Args:
            prediction_path: Path to predicted parameter
            experimental_path: Path to experimental parameter
            metadata_key: Key to store validation result in metadata

        Returns:
            Validation result dictionary
        """
        if not self.has_param(prediction_path):
            raise KeyError(f"Prediction '{prediction_path}' not in registry")

        pred_entry = self.get_entry(prediction_path)
        result = self.compute_sigma_deviation(pred_entry.value, experimental_path)

        # Store validation in metadata
        pred_entry.metadata[metadata_key] = result

        return result

    def get_accuracy_report(self) -> Dict[str, Any]:
        """
        Generate accuracy report for all predictions with validation data.

        Returns:
            Dictionary with accuracy statistics and details
        """
        report = {
            'excellent': [],  # < 1σ
            'good': [],       # 1-2σ
            'acceptable': [], # 2-3σ
            'tension': [],    # > 3σ
            'unvalidated': [],
            'summary': {}
        }

        for path, entry in self._parameters.items():
            if entry.status in ('DERIVED', 'PREDICTED'):
                validation = entry.metadata.get('validation')
                if validation:
                    status = validation.get('status', 'UNKNOWN')
                    item = {
                        'path': path,
                        'predicted': validation.get('predicted'),
                        'experimental': validation.get('experimental'),
                        'sigma': validation.get('sigma'),
                        'source': validation.get('source')
                    }
                    if status == 'EXCELLENT':
                        report['excellent'].append(item)
                    elif status == 'GOOD':
                        report['good'].append(item)
                    elif status == 'ACCEPTABLE':
                        report['acceptable'].append(item)
                    elif status == 'TENSION':
                        report['tension'].append(item)
                else:
                    report['unvalidated'].append(path)

        # Compute summary
        total = (len(report['excellent']) + len(report['good']) +
                 len(report['acceptable']) + len(report['tension']))
        report['summary'] = {
            'total_validated': total,
            'excellent_count': len(report['excellent']),
            'good_count': len(report['good']),
            'acceptable_count': len(report['acceptable']),
            'tension_count': len(report['tension']),
            'unvalidated_count': len(report['unvalidated'])
        }

        return report
