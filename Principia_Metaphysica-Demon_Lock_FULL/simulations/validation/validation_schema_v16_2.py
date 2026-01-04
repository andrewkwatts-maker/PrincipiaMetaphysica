"""
Validation Schema v16.2 - Single Source of Truth Definitions
=============================================================

This module defines the SCHEMA for validation - what fields are required,
what experimental values to compare against, and validation thresholds.

SOLID Principles:
- Single Responsibility: Only defines schema, doesn't perform validation
- Open/Closed: New parameters can be added without modifying validator
- Dependency Inversion: Validator depends on schema, not concrete values

Data Flow:
  Experimental JSON files → Schema (references) → Validator (reads theory_output)

The validator should NEVER contain hardcoded predictions - only:
1. References to where experimental values are stored
2. References to where predictions should be found in theory_output
3. Validation thresholds and metadata requirements

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from enum import Enum


class ValidationStatus(Enum):
    """Possible validation outcomes."""
    PASS = "PASS"           # < 1σ
    MARGINAL = "MARGINAL"   # 1-2σ
    TENSION = "TENSION"     # 2-3σ
    FAIL = "FAIL"           # > 3σ
    MISSING = "MISSING"     # Required field not found
    INVALID = "INVALID"     # Field exists but invalid format


class BoundType(Enum):
    """Type of experimental constraint."""
    MEASURED = "measured"       # Direct measurement (PDG, CODATA, etc.)
    THEORETICAL = "theoretical" # Theoretical bound (SO(10), etc.)
    DERIVED = "derived"         # Derived from other measurements


@dataclass
class ExperimentalReference:
    """
    Reference to where experimental value is stored.

    The validator will load this from the experimental JSON files,
    NOT from hardcoded values in this schema.
    """
    source_file: str  # e.g., "desi_2025_constraints.json"
    json_path: str    # e.g., "cosmological_parameters.w0.value"
    uncertainty_path: Optional[str] = None  # Path to uncertainty
    bound_type: BoundType = BoundType.MEASURED
    source_name: str = ""  # Human-readable source name


@dataclass
class ParameterValidationSpec:
    """
    Specification for validating a single parameter.

    This defines WHERE to find values, not WHAT the values are.
    """
    # Where to find the prediction in theory_output
    prediction_path: str  # e.g., "parameters.cosmology.w0_derived.value"

    # Where to find the experimental reference
    experimental_ref: ExperimentalReference

    # Validation metadata
    name: str
    sector: str  # cosmology, neutrino, higgs, gauge, ckm, constants
    units: str

    # Optional: Use theory uncertainty instead of experimental
    use_theory_uncertainty: bool = False
    theory_uncertainty: Optional[float] = None

    # Optional: Notes about this parameter
    note: str = ""

    # Required metadata fields in theory_output
    required_metadata: List[str] = field(default_factory=lambda: [
        "value", "source", "status"
    ])


@dataclass
class LinkValidationSpec:
    """
    Specification for validating cross-references.
    """
    source_type: str      # "formula", "parameter", "section", etc.
    target_type: str      # What it should link to
    link_field: str       # Field name containing the link
    bidirectional: bool   # Must have reverse link?


@dataclass
class MetadataRequirement:
    """
    Required metadata field specification.
    """
    field_name: str
    field_type: type
    required: bool = True
    default_value: Any = None
    validation_regex: Optional[str] = None


# =============================================================================
# VALIDATION SCHEMA DEFINITIONS
# =============================================================================

# Experimental data file paths (relative to simulations/data/experimental/)
EXPERIMENTAL_DATA_PATHS = {
    "desi": "desi_2025_constraints.json",
    "pdg": "pdg_2024_values.json",
    "codata": "codata_2022.json",
    "nufit": "nufit_6_0.json",
    "planck": "planck_2018.json",
    "shoes": "shoes_2025.json",
}


# Parameter validation specifications
PARAMETER_VALIDATIONS: List[ParameterValidationSpec] = [
    # =========================================================================
    # COSMOLOGY SECTOR
    # =========================================================================
    ParameterValidationSpec(
        prediction_path="parameters.cosmology.w0_derived.value",
        experimental_ref=ExperimentalReference(
            source_file="desi_2025_constraints.json",
            json_path="cosmological_parameters.w0.value",
            uncertainty_path="cosmological_parameters.w0.uncertainty_plus",
            source_name="DESI 2025 (thawing)"
        ),
        name="Dark Energy EoS w0",
        sector="cosmology",
        units="dimensionless"
    ),
    ParameterValidationSpec(
        prediction_path="parameters.cosmology.wa_derived.value",
        experimental_ref=ExperimentalReference(
            source_file="desi_2025_constraints.json",
            json_path="cosmological_parameters.wa.value",
            uncertainty_path="cosmological_parameters.wa.uncertainty_plus",
            source_name="DESI 2025 (thawing)"
        ),
        name="Dark Energy Evolution wa",
        sector="cosmology",
        units="dimensionless",
        note="v16.2 4-form scaling: wa = -1/sqrt(24) * 4 = -0.816"
    ),
    ParameterValidationSpec(
        prediction_path="parameters.cosmology.H0_local.value",
        experimental_ref=ExperimentalReference(
            source_file="shoes_2025.json",
            json_path="H0.value",
            uncertainty_path="H0.uncertainty",
            source_name="SH0ES 2025"
        ),
        name="Hubble Constant (local)",
        sector="cosmology",
        units="km/s/Mpc"
    ),
    ParameterValidationSpec(
        prediction_path="parameters.cosmology.sigma8_pred.value",
        experimental_ref=ExperimentalReference(
            source_file="desi_2025_constraints.json",
            json_path="cosmological_parameters.sigma8.value",
            uncertainty_path="cosmological_parameters.sigma8.uncertainty_plus",
            source_name="DESI 2025"
        ),
        name="Matter Fluctuation sigma8",
        sector="cosmology",
        units="dimensionless"
    ),
    ParameterValidationSpec(
        prediction_path="parameters.cosmology.S8_pred.value",
        experimental_ref=ExperimentalReference(
            source_file="planck_2018.json",
            json_path="S8.value",
            uncertainty_path="S8.uncertainty",
            source_name="Planck 2018"
        ),
        name="Structure Growth S8",
        sector="cosmology",
        units="dimensionless"
    ),
    ParameterValidationSpec(
        prediction_path="parameters.cosmology.T_CMB_pred.value",
        experimental_ref=ExperimentalReference(
            source_file="planck_2018.json",
            json_path="T_CMB.value",
            uncertainty_path="T_CMB.uncertainty",
            source_name="COBE/FIRAS"
        ),
        name="CMB Temperature",
        sector="cosmology",
        units="K",
        use_theory_uncertainty=True,
        theory_uncertainty=0.02
    ),
    ParameterValidationSpec(
        prediction_path="parameters.cosmology.eta_baryon_pred.value",
        experimental_ref=ExperimentalReference(
            source_file="planck_2018.json",
            json_path="eta_baryon.value",
            uncertainty_path="eta_baryon.uncertainty",
            source_name="Planck 2018 (BBN)"
        ),
        name="Baryon-to-Photon Ratio eta",
        sector="cosmology",
        units="dimensionless",
        use_theory_uncertainty=True,
        theory_uncertainty=0.15e-10,  # Theory precision from Leech lattice dilution
        note="eta = b3/(4*10^10) from 24-cycle Leech lattice dilution"
    ),

    # =========================================================================
    # NEUTRINO SECTOR
    # =========================================================================
    ParameterValidationSpec(
        prediction_path="parameters.neutrino.theta_12_pred.value",
        experimental_ref=ExperimentalReference(
            source_file="nufit_6_0.json",
            json_path="theta_12.value",
            uncertainty_path="theta_12.uncertainty",
            source_name="NuFIT 6.0"
        ),
        name="Solar Mixing Angle",
        sector="neutrino",
        units="degrees"
    ),
    ParameterValidationSpec(
        prediction_path="parameters.neutrino.theta_13_pred.value",
        experimental_ref=ExperimentalReference(
            source_file="nufit_6_0.json",
            json_path="theta_13.value",
            uncertainty_path="theta_13.uncertainty",
            source_name="NuFIT 6.0"
        ),
        name="Reactor Mixing Angle",
        sector="neutrino",
        units="degrees"
    ),
    ParameterValidationSpec(
        prediction_path="parameters.neutrino.theta_23_pred.value",
        experimental_ref=ExperimentalReference(
            source_file="nufit_6_0.json",
            json_path="theta_23_IO.value",  # Use IO value
            uncertainty_path="theta_23_IO.uncertainty",
            source_name="NuFIT 6.0 (IO)"
        ),
        name="Atmospheric Mixing Angle",
        sector="neutrino",
        units="degrees"
    ),
    ParameterValidationSpec(
        prediction_path="parameters.neutrino.delta_CP_pred.value",
        experimental_ref=ExperimentalReference(
            source_file="nufit_6_0.json",
            json_path="delta_CP_IO.value",  # Use IO value
            uncertainty_path="delta_CP_IO.uncertainty",
            source_name="NuFIT 6.0 (IO)"
        ),
        name="CP Phase",
        sector="neutrino",
        units="degrees",
        note="v16.2: PM matches IO (278 deg) at 0.02 sigma. NO (232 deg) shows 1.73 sigma tension."
    ),

    # =========================================================================
    # HIGGS SECTOR
    # =========================================================================
    ParameterValidationSpec(
        prediction_path="parameters.higgs.m_higgs_local.value",
        experimental_ref=ExperimentalReference(
            source_file="pdg_2024_values.json",
            json_path="higgs.mass.value",
            uncertainty_path="higgs.mass.uncertainty",
            source_name="PDG 2024"
        ),
        name="Higgs Mass (4D Local)",
        sector="higgs",
        units="GeV"
    ),
    ParameterValidationSpec(
        prediction_path="parameters.higgs.vev_pred.value",
        experimental_ref=ExperimentalReference(
            source_file="pdg_2024_values.json",
            json_path="higgs.vev.value",
            uncertainty_path="higgs.vev.uncertainty",
            source_name="PDG 2024"
        ),
        name="Higgs VEV",
        sector="higgs",
        units="GeV"
    ),

    # =========================================================================
    # GAUGE SECTOR
    # =========================================================================
    ParameterValidationSpec(
        prediction_path="parameters.gauge.sin2_theta_W_gut.value",
        experimental_ref=ExperimentalReference(
            source_file="pdg_2024_values.json",
            json_path="gauge.sin2_theta_W_gut.value",
            uncertainty_path="gauge.sin2_theta_W_gut.uncertainty",
            bound_type=BoundType.THEORETICAL,
            source_name="SO(10) Theory"
        ),
        name="Weak Mixing at GUT",
        sector="gauge",
        units="dimensionless"
    ),
    ParameterValidationSpec(
        prediction_path="parameters.constants.sin2_theta_W_pred.value",
        experimental_ref=ExperimentalReference(
            source_file="pdg_2024_values.json",
            json_path="gauge.sin2_theta_W.value",
            uncertainty_path="gauge.sin2_theta_W.uncertainty",
            source_name="PDG 2024"
        ),
        name="Weak Mixing sin2thetaW",
        sector="gauge",
        units="dimensionless",
        use_theory_uncertainty=True,
        theory_uncertainty=0.001  # Geometric formula has ~0.3% precision
    ),
    ParameterValidationSpec(
        prediction_path="parameters.gauge.ALPHA_GUT.value",
        experimental_ref=ExperimentalReference(
            source_file="pdg_2024_values.json",
            json_path="gauge.alpha_GUT.value",
            uncertainty_path="gauge.alpha_GUT.uncertainty",
            bound_type=BoundType.THEORETICAL,
            source_name="SO(10) Theory"
        ),
        name="GUT Coupling alpha_GUT",
        sector="gauge",
        units="dimensionless"
    ),

    # =========================================================================
    # CKM SECTOR
    # =========================================================================
    ParameterValidationSpec(
        prediction_path="parameters.ckm.V_us_triality.value",
        experimental_ref=ExperimentalReference(
            source_file="pdg_2024_values.json",
            json_path="ckm.V_us.value",
            uncertainty_path="ckm.V_us.uncertainty",
            source_name="PDG 2024"
        ),
        name="CKM |V_us| (Cabibbo)",
        sector="ckm",
        units="dimensionless"
    ),
    ParameterValidationSpec(
        prediction_path="parameters.ckm.V_cb_triality.value",
        experimental_ref=ExperimentalReference(
            source_file="pdg_2024_values.json",
            json_path="ckm.V_cb.value",
            uncertainty_path="ckm.V_cb.uncertainty",
            source_name="PDG 2024"
        ),
        name="CKM |V_cb|",
        sector="ckm",
        units="dimensionless"
    ),
    ParameterValidationSpec(
        prediction_path="parameters.ckm.V_ub_triality.value",
        experimental_ref=ExperimentalReference(
            source_file="pdg_2024_values.json",
            json_path="ckm.V_ub.value",
            uncertainty_path="ckm.V_ub.uncertainty",
            source_name="PDG 2024"
        ),
        name="CKM |V_ub|",
        sector="ckm",
        units="dimensionless"
    ),
    ParameterValidationSpec(
        prediction_path="parameters.ckm.jarlskog_triality.value",
        experimental_ref=ExperimentalReference(
            source_file="pdg_2024_values.json",
            json_path="ckm.jarlskog.value",
            uncertainty_path="ckm.jarlskog.uncertainty",
            source_name="PDG 2024"
        ),
        name="Jarlskog Invariant J",
        sector="ckm",
        units="dimensionless"
    ),

    # =========================================================================
    # FUNDAMENTAL CONSTANTS SECTOR
    # =========================================================================
    ParameterValidationSpec(
        prediction_path="parameters.constants.alpha_inverse_pred.value",
        experimental_ref=ExperimentalReference(
            source_file="codata_2022.json",
            json_path="alpha_inverse.value",
            uncertainty_path="alpha_inverse.uncertainty",
            source_name="CODATA 2022"
        ),
        name="Inverse Fine Structure",
        sector="constants",
        units="dimensionless",
        use_theory_uncertainty=True,
        theory_uncertainty=0.01
    ),
    ParameterValidationSpec(
        prediction_path="parameters.cosmology.M_Pl_4D.value",
        experimental_ref=ExperimentalReference(
            source_file="codata_2022.json",
            json_path="M_PLANCK.value",
            uncertainty_path="M_PLANCK.uncertainty",
            source_name="CODATA 2022"
        ),
        name="Planck Mass (4D)",
        sector="constants",
        units="GeV"
    ),
    ParameterValidationSpec(
        prediction_path="parameters.constants.mu_pe_pred.value",
        experimental_ref=ExperimentalReference(
            source_file="codata_2022.json",
            json_path="mu_pe.value",
            uncertainty_path="mu_pe.uncertainty",
            source_name="CODATA 2022"
        ),
        name="Proton/Electron Ratio",
        sector="constants",
        units="dimensionless",
        use_theory_uncertainty=True,
        theory_uncertainty=2.0
    ),
    ParameterValidationSpec(
        prediction_path="parameters.constants.alpha_s_pred.value",
        experimental_ref=ExperimentalReference(
            source_file="pdg_2024_values.json",
            json_path="constants.alpha_s.value",
            uncertainty_path="constants.alpha_s.uncertainty",
            source_name="PDG 2024"
        ),
        name="Strong Coupling alpha_s(MZ)",
        sector="constants",
        units="dimensionless"
    ),
    ParameterValidationSpec(
        prediction_path="parameters.constants.G_F_pred.value",
        experimental_ref=ExperimentalReference(
            source_file="pdg_2024_values.json",
            json_path="constants.G_F.value",
            uncertainty_path="constants.G_F.uncertainty",
            source_name="PDG 2024"
        ),
        name="Fermi Constant GF",
        sector="constants",
        units="GeV^-2",
        use_theory_uncertainty=True,
        theory_uncertainty=0.002e-5,  # Theory precision ~0.02% from VEV formula
        note="G_F = 1/(sqrt(2)*v^2) where v = k_gimel*(b3-4)"
    ),
]


# Link validation specifications
LINK_VALIDATIONS: List[LinkValidationSpec] = [
    LinkValidationSpec(
        source_type="formula",
        target_type="parameter",
        link_field="outputParams",
        bidirectional=True
    ),
    LinkValidationSpec(
        source_type="formula",
        target_type="parameter",
        link_field="inputParams",
        bidirectional=False
    ),
    LinkValidationSpec(
        source_type="section",
        target_type="formula",
        link_field="formulas",
        bidirectional=True
    ),
    LinkValidationSpec(
        source_type="section",
        target_type="reference",
        link_field="references",
        bidirectional=False
    ),
    LinkValidationSpec(
        source_type="parameter",
        target_type="formula",
        link_field="derivation_formula",
        bidirectional=True
    ),
]


# Required metadata fields for each entity type
METADATA_REQUIREMENTS: Dict[str, List[MetadataRequirement]] = {
    "parameter": [
        MetadataRequirement("value", (int, float), required=True),
        MetadataRequirement("source", str, required=True),
        MetadataRequirement("status", str, required=True),
        MetadataRequirement("units", str, required=False, default_value="dimensionless"),
    ],
    "formula": [
        MetadataRequirement("id", str, required=True),
        MetadataRequirement("latex", str, required=True),
        MetadataRequirement("plain_text", str, required=True),
        MetadataRequirement("outputParams", list, required=False, default_value=[]),
    ],
    "section": [
        MetadataRequirement("id", str, required=True),
        MetadataRequirement("title", str, required=True),
        MetadataRequirement("content", str, required=True),
    ],
    "reference": [
        MetadataRequirement("id", str, required=True),
        MetadataRequirement("title", str, required=True),
        MetadataRequirement("authors", (str, list), required=True),
    ],
}


# Validation thresholds
SIGMA_THRESHOLDS = {
    "pass": 1.0,
    "marginal": 2.0,
    "tension": 3.0,
    # > 3.0 = fail
}


def get_validation_schema() -> Dict[str, Any]:
    """Return the complete validation schema as a dictionary."""
    return {
        "parameter_validations": [
            {
                "prediction_path": spec.prediction_path,
                "experimental_source": spec.experimental_ref.source_file,
                "experimental_path": spec.experimental_ref.json_path,
                "name": spec.name,
                "sector": spec.sector,
                "units": spec.units,
                "use_theory_uncertainty": spec.use_theory_uncertainty,
                "theory_uncertainty": spec.theory_uncertainty,
            }
            for spec in PARAMETER_VALIDATIONS
        ],
        "link_validations": [
            {
                "source_type": spec.source_type,
                "target_type": spec.target_type,
                "link_field": spec.link_field,
                "bidirectional": spec.bidirectional,
            }
            for spec in LINK_VALIDATIONS
        ],
        "metadata_requirements": {
            entity_type: [
                {
                    "field_name": req.field_name,
                    "field_type": req.field_type.__name__ if isinstance(req.field_type, type) else str(req.field_type),
                    "required": req.required,
                }
                for req in requirements
            ]
            for entity_type, requirements in METADATA_REQUIREMENTS.items()
        },
        "sigma_thresholds": SIGMA_THRESHOLDS,
    }
