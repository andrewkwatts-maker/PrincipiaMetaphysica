"""
Experimental Data Loader for Principia Metaphysica
====================================================

Loads experimental physics values from cached JSON files instead of hardcoding.
This ensures:
1. Values are traceable to specific data releases
2. Updates can be made by updating JSON files
3. No risk of typos in code
4. Full metadata including uncertainties and sources

Data Sources:
- DESI 2025: simulations/data/experimental/desi_2025_constraints.json
- NuFIT 6.0: simulations/data/experimental/nufit_6_0_parameters.json
- PDG 2024: simulations/data/experimental/pdg_2024_values.json

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.

Dedicated To:
    My Wife: Elizabeth May Watts
    Our Messiah: Jesus Of Nazareth
"""

import json
import os
from pathlib import Path
from typing import Dict, Any, Optional
from dataclasses import dataclass
import warnings


@dataclass
class ExperimentalValue:
    """A single experimental measurement with full metadata."""
    value: float
    uncertainty: float
    units: str
    source: str
    description: str = ""


class ExperimentalDataLoader:
    """
    Loads experimental data from cached JSON files.

    Usage:
        loader = ExperimentalDataLoader()

        # Get DESI w0 value
        w0 = loader.get_desi("w0")
        print(f"w0 = {w0.value} ± {w0.uncertainty}")

        # Get all PDG values
        pdg = loader.get_all_pdg()
    """

    # Data directory relative to this file
    DATA_DIR = Path(__file__).parent / "experimental"

    # Cached data
    _desi_data: Optional[Dict] = None
    _nufit_data: Optional[Dict] = None
    _pdg_data: Optional[Dict] = None

    def __init__(self, data_dir: Optional[Path] = None):
        """
        Initialize the data loader.

        Args:
            data_dir: Optional custom data directory path
        """
        if data_dir:
            self.DATA_DIR = Path(data_dir)

        self._validate_data_files()

    def _validate_data_files(self) -> None:
        """Ensure all required data files exist."""
        required_files = [
            "desi_2025_constraints.json",
            "nufit_6_0_parameters.json",
            "pdg_2024_values.json"
        ]

        for filename in required_files:
            filepath = self.DATA_DIR / filename
            if not filepath.exists():
                warnings.warn(f"Missing experimental data file: {filepath}")

    def _load_json(self, filename: str) -> Dict:
        """Load and cache a JSON file."""
        filepath = self.DATA_DIR / filename
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)

    # =========================================================================
    # DESI Data
    # =========================================================================

    def get_desi_data(self) -> Dict:
        """Get full DESI data dictionary."""
        if self._desi_data is None:
            self._desi_data = self._load_json("desi_2025_constraints.json")
        return self._desi_data

    def get_desi(self, param_name: str) -> ExperimentalValue:
        """
        Get a DESI cosmological parameter.

        Args:
            param_name: Parameter name (w0, wa, H0, Omega_m, etc.)

        Returns:
            ExperimentalValue with value, uncertainty, and metadata
        """
        data = self.get_desi_data()
        params = data.get("cosmological_parameters", {})

        if param_name not in params:
            raise KeyError(f"DESI parameter '{param_name}' not found. "
                          f"Available: {list(params.keys())}")

        p = params[param_name]
        return ExperimentalValue(
            value=p["value"],
            uncertainty=p.get("uncertainty_plus", p.get("uncertainty", 0)),
            units=p.get("units", ""),
            source=f"DESI 2025 ({data['metadata'].get('arxiv', '')})",
            description=p.get("description", "")
        )

    def get_desi_w0(self) -> ExperimentalValue:
        """Get DESI w0 (dark energy equation of state)."""
        return self.get_desi("w0")

    def get_desi_wa(self) -> ExperimentalValue:
        """Get DESI wa (dark energy evolution)."""
        return self.get_desi("wa")

    # =========================================================================
    # NuFIT Data
    # =========================================================================

    def get_nufit_data(self) -> Dict:
        """Get full NuFIT data dictionary."""
        if self._nufit_data is None:
            self._nufit_data = self._load_json("nufit_6_0_parameters.json")
        return self._nufit_data

    def get_nufit(self, param_name: str, ordering: str = "normal_ordering") -> ExperimentalValue:
        """
        Get a NuFIT neutrino parameter.

        Args:
            param_name: Parameter name (theta_12, theta_23, theta_13, delta_CP, etc.)
            ordering: "normal_ordering" or "inverted_ordering"

        Returns:
            ExperimentalValue with value, uncertainty, and metadata
        """
        data = self.get_nufit_data()

        if ordering not in data:
            raise KeyError(f"Ordering '{ordering}' not found. "
                          f"Use 'normal_ordering' or 'inverted_ordering'")

        params = data[ordering]

        if param_name not in params:
            raise KeyError(f"NuFIT parameter '{param_name}' not found. "
                          f"Available: {list(params.keys())}")

        p = params[param_name]
        # Use average of asymmetric uncertainties
        unc = (p.get("uncertainty_plus", 0) + p.get("uncertainty_minus", 0)) / 2
        if unc == 0:
            unc = p.get("uncertainty", 0)

        return ExperimentalValue(
            value=p["value"],
            uncertainty=unc,
            units=p.get("units", ""),
            source=f"NuFIT 6.0 ({data['metadata'].get('date', '')})",
            description=p.get("description", "")
        )

    def get_mass_ordering_preference(self) -> Dict:
        """Get NuFIT mass ordering preference statistics."""
        data = self.get_nufit_data()
        return data.get("mass_ordering_preference", {})

    # =========================================================================
    # PDG Data
    # =========================================================================

    def get_pdg_data(self) -> Dict:
        """Get full PDG data dictionary."""
        if self._pdg_data is None:
            self._pdg_data = self._load_json("pdg_2024_values.json")
        return self._pdg_data

    def get_pdg(self, category: str, param_name: str) -> ExperimentalValue:
        """
        Get a PDG particle physics parameter.

        Args:
            category: Category (fundamental_constants, gauge_bosons, leptons, quarks, etc.)
            param_name: Parameter name within category

        Returns:
            ExperimentalValue with value, uncertainty, and metadata
        """
        data = self.get_pdg_data()

        if category not in data:
            raise KeyError(f"PDG category '{category}' not found. "
                          f"Available: {[k for k in data.keys() if k != 'metadata']}")

        params = data[category]

        if param_name not in params:
            raise KeyError(f"PDG parameter '{param_name}' not found in '{category}'. "
                          f"Available: {list(params.keys())}")

        p = params[param_name]
        return ExperimentalValue(
            value=p["value"],
            uncertainty=p.get("uncertainty", 0),
            units=p.get("units", ""),
            source="PDG 2024",
            description=p.get("description", "")
        )

    def get_pdg_mass(self, particle: str) -> ExperimentalValue:
        """
        Get particle mass from PDG.

        Args:
            particle: Particle name (electron, muon, tau, up, down, etc.)

        Returns:
            ExperimentalValue for particle mass
        """
        # Map particle names to categories
        lepton_masses = ["electron", "muon", "tau"]
        quark_masses = ["up", "down", "strange", "charm", "bottom", "top"]
        boson_masses = ["W", "Z", "higgs"]
        baryon_masses = ["proton", "neutron"]

        if particle in lepton_masses:
            return self.get_pdg("leptons", f"m_{particle}")
        elif particle in quark_masses:
            return self.get_pdg("quarks", f"m_{particle}")
        elif particle in boson_masses:
            return self.get_pdg("gauge_bosons", f"m_{particle}")
        elif particle in baryon_masses:
            return self.get_pdg("baryons", f"m_{particle}")
        else:
            raise KeyError(f"Unknown particle '{particle}'")

    # =========================================================================
    # Registry Integration
    # =========================================================================

    def load_all_into_registry(self, registry: 'PMRegistry') -> None:
        """
        Load all experimental values into a PMRegistry instance.

        This replaces hardcoded values with values from cached JSON files.

        Args:
            registry: PMRegistry instance to populate
        """
        self._load_desi_into_registry(registry)
        self._load_nufit_into_registry(registry)
        self._load_pdg_into_registry(registry)

    def _load_desi_into_registry(self, registry: 'PMRegistry') -> None:
        """Load DESI values into registry."""
        desi_params = ["w0", "wa", "H0", "Omega_m", "Omega_DE", "sigma8"]

        for param_name in desi_params:
            try:
                val = self.get_desi(param_name)
                registry.set_param(
                    path=f"desi.{param_name}",
                    value=val.value,
                    source=f"ESTABLISHED:DESI_2025",
                    uncertainty=val.uncertainty,
                    status="ESTABLISHED",
                    metadata={
                        "units": val.units,
                        "description": val.description,
                        "source_file": "desi_2025_constraints.json"
                    }
                )
            except KeyError:
                pass  # Parameter not in data file

    def _load_nufit_into_registry(self, registry: 'PMRegistry') -> None:
        """Load NuFIT values into registry (Normal Ordering by default)."""
        nufit_params = [
            "theta_12", "theta_23", "theta_13", "delta_CP",
            "delta_m21_sq", "delta_m31_sq"
        ]

        for param_name in nufit_params:
            try:
                val = self.get_nufit(param_name, "normal_ordering")
                registry.set_param(
                    path=f"nufit.{param_name}",
                    value=val.value,
                    source=f"ESTABLISHED:NuFIT6.0",
                    uncertainty=val.uncertainty,
                    status="ESTABLISHED",
                    metadata={
                        "units": val.units,
                        "description": val.description,
                        "source_file": "nufit_6_0_parameters.json"
                    }
                )
            except KeyError:
                pass

        # Also store mass ordering preference
        mo = self.get_mass_ordering_preference()
        if mo:
            registry.set_param(
                path="nufit.mass_ordering_chi2_diff",
                value=mo.get("chi2_difference", 0),
                source="ESTABLISHED:NuFIT6.0",
                status="ESTABLISHED",
                metadata={
                    "preferred": mo.get("preferred", "NO"),
                    "sigma": mo.get("sigma_preference", 0),
                    "notes": mo.get("notes", "")
                }
            )

    def _load_pdg_into_registry(self, registry: 'PMRegistry') -> None:
        """Load PDG values into registry."""
        data = self.get_pdg_data()

        # Load all categories
        for category, params in data.items():
            if category in ("metadata", "verification"):
                continue

            for param_name, param_data in params.items():
                if not isinstance(param_data, dict):
                    continue

                registry.set_param(
                    path=f"pdg.{param_name}",
                    value=param_data.get("value"),
                    source="ESTABLISHED:PDG2024",
                    uncertainty=param_data.get("uncertainty", 0),
                    status="ESTABLISHED",
                    metadata={
                        "units": param_data.get("units", ""),
                        "description": param_data.get("description", ""),
                        "source_file": "pdg_2024_values.json"
                    }
                )


# Singleton instance for convenience
_loader: Optional[ExperimentalDataLoader] = None


def get_loader() -> ExperimentalDataLoader:
    """Get the singleton ExperimentalDataLoader instance."""
    global _loader
    if _loader is None:
        _loader = ExperimentalDataLoader()
    return _loader


# ============================================================================
# Convenience Functions
# ============================================================================

def get_desi_w0() -> ExperimentalValue:
    """Get DESI w0 value."""
    return get_loader().get_desi_w0()


def get_desi_wa() -> ExperimentalValue:
    """Get DESI wa value."""
    return get_loader().get_desi_wa()


def get_nufit_theta12() -> ExperimentalValue:
    """Get NuFIT theta_12 value."""
    return get_loader().get_nufit("theta_12")


def get_pdg_higgs_mass() -> ExperimentalValue:
    """Get PDG Higgs mass."""
    return get_loader().get_pdg_mass("higgs")


# ============================================================================
# Self-Test
# ============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("EXPERIMENTAL DATA LOADER - SELF TEST")
    print("=" * 60)

    loader = ExperimentalDataLoader()

    print("\n--- DESI 2025 ---")
    w0 = loader.get_desi_w0()
    wa = loader.get_desi_wa()
    print(f"w0 = {w0.value} ± {w0.uncertainty} ({w0.source})")
    print(f"wa = {wa.value} ± {wa.uncertainty} ({wa.source})")

    print("\n--- NuFIT 6.0 (Normal Ordering) ---")
    for param in ["theta_12", "theta_23", "theta_13", "delta_CP"]:
        val = loader.get_nufit(param)
        print(f"{param} = {val.value} ± {val.uncertainty} {val.units}")

    mo = loader.get_mass_ordering_preference()
    print(f"\nMass ordering: {mo['preferred']} preferred at {mo['sigma_preference']} sigma")

    print("\n--- PDG 2024 ---")
    for particle in ["higgs", "top", "W", "Z"]:
        try:
            mass = loader.get_pdg_mass(particle)
            print(f"m_{particle} = {mass.value} ± {mass.uncertainty} {mass.units}")
        except KeyError as e:
            print(f"  {particle}: {e}")

    print("\n" + "=" * 60)
    print("SELF TEST COMPLETE")
    print("=" * 60)
