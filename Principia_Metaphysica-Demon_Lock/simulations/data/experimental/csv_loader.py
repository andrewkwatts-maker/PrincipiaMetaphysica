"""
CSV Loader for Experimental Physics Data
==========================================

Loads experimental values from CSV files for PDG 2024, NuFIT 6.0, and DESI 2025.
Provides easy lookup by parameter name.

Usage:
    from simulations.data.experimental.csv_loader import ExperimentalCSV

    # Get PDG value
    m_higgs = ExperimentalCSV.pdg("m_higgs")
    print(f"Higgs mass: {m_higgs['value']} +/- {m_higgs['uncertainty']} {m_higgs['units']}")

    # Get NuFIT value (Normal Ordering)
    theta_12 = ExperimentalCSV.nufit("theta_12")

    # Get DESI value
    w0 = ExperimentalCSV.desi("w0")

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.
"""

import csv
import os
from pathlib import Path
from typing import Dict, Any, Optional
from functools import lru_cache


class ExperimentalCSV:
    """Load and query experimental values from CSV files."""

    DATA_DIR = Path(__file__).parent

    @classmethod
    @lru_cache(maxsize=1)
    def _load_pdg(cls) -> Dict[str, Dict[str, Any]]:
        """Load PDG 2024 CSV data."""
        return cls._load_csv("pdg_2024.csv")

    @classmethod
    @lru_cache(maxsize=1)
    def _load_nufit(cls) -> Dict[str, Dict[str, Any]]:
        """Load NuFIT 6.0 CSV data."""
        return cls._load_csv("nufit_6_0.csv")

    @classmethod
    @lru_cache(maxsize=1)
    def _load_desi(cls) -> Dict[str, Dict[str, Any]]:
        """Load DESI 2025 CSV data."""
        return cls._load_csv("desi_2025.csv")

    @classmethod
    def _load_csv(cls, filename: str) -> Dict[str, Dict[str, Any]]:
        """Load a CSV file into a dictionary keyed by param_id."""
        filepath = cls.DATA_DIR / filename
        data = {}

        with open(filepath, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                param_id = row['param_id']
                # Convert numeric strings to floats
                processed = {}
                for key, value in row.items():
                    if value == '':
                        processed[key] = None
                    elif key in ('value', 'uncertainty', 'uncertainty_plus', 'uncertainty_minus'):
                        try:
                            processed[key] = float(value) if value else None
                        except ValueError:
                            processed[key] = value
                    else:
                        processed[key] = value
                data[param_id] = processed

        return data

    @classmethod
    def pdg(cls, param_id: str) -> Optional[Dict[str, Any]]:
        """
        Get a PDG 2024 experimental value by parameter ID.

        Args:
            param_id: Parameter identifier (e.g., "m_higgs", "alpha_em", "V_us")

        Returns:
            Dictionary with value, uncertainty, units, source, description
            or None if not found
        """
        data = cls._load_pdg()
        return data.get(param_id)

    @classmethod
    def nufit(cls, param_id: str, ordering: str = "NO") -> Optional[Dict[str, Any]]:
        """
        Get a NuFIT 6.0 experimental value by parameter ID.

        Args:
            param_id: Parameter identifier (e.g., "theta_12", "delta_CP")
            ordering: "NO" for Normal Ordering, "IO" for Inverted Ordering

        Returns:
            Dictionary with value, uncertainties, units, source
            or None if not found
        """
        data = cls._load_nufit()

        # For IO, look for _IO suffix version
        if ordering == "IO" and param_id + "_IO" in data:
            return data[param_id + "_IO"]

        result = data.get(param_id)
        if result and (ordering == "NO" or result.get('ordering') in (None, 'NO', 'preference')):
            return result
        return None

    @classmethod
    def desi(cls, param_id: str, dataset: str = None) -> Optional[Dict[str, Any]]:
        """
        Get a DESI 2025 experimental value by parameter ID.

        Args:
            param_id: Parameter identifier (e.g., "w0", "H0", "Omega_m")
            dataset: Optional specific dataset (e.g., "BAO_only", "BAO+CMB")

        Returns:
            Dictionary with value, uncertainties, units, source
            or None if not found
        """
        data = cls._load_desi()

        # For specific dataset, try with suffix
        if dataset:
            suffixed_id = f"{param_id}_{dataset.replace('+', '_')}"
            if suffixed_id in data:
                return data[suffixed_id]

        return data.get(param_id)

    @classmethod
    def get_experimental_value(cls, source: str, param_id: str, **kwargs) -> Optional[Dict[str, Any]]:
        """
        Universal getter for any experimental source.

        Args:
            source: "PDG2024", "NuFIT6.0", "DESI2025"
            param_id: Parameter identifier
            **kwargs: Additional arguments (ordering for NuFIT, dataset for DESI)

        Returns:
            Dictionary with experimental value data or None
        """
        source_upper = source.upper().replace(" ", "").replace(".", "")

        if "PDG" in source_upper:
            return cls.pdg(param_id)
        elif "NUFIT" in source_upper:
            return cls.nufit(param_id, kwargs.get('ordering', 'NO'))
        elif "DESI" in source_upper:
            return cls.desi(param_id, kwargs.get('dataset'))
        else:
            raise ValueError(f"Unknown source: {source}")

    @classmethod
    def all_pdg(cls) -> Dict[str, Dict[str, Any]]:
        """Return all PDG 2024 values."""
        return dict(cls._load_pdg())

    @classmethod
    def all_nufit(cls, ordering: str = "NO") -> Dict[str, Dict[str, Any]]:
        """Return all NuFIT 6.0 values for given ordering."""
        data = cls._load_nufit()
        if ordering == "NO":
            return {k: v for k, v in data.items() if not k.endswith("_IO")}
        else:
            # Return IO versions, stripping _IO suffix from keys
            return {k.replace("_IO", ""): v for k, v in data.items() if k.endswith("_IO") or v.get('ordering') in (None, 'preference')}

    @classmethod
    def all_desi(cls) -> Dict[str, Dict[str, Any]]:
        """Return all DESI 2025 values."""
        return dict(cls._load_desi())


# Convenience functions for direct import
def get_pdg(param_id: str) -> Optional[Dict[str, Any]]:
    """Get PDG 2024 value by parameter ID."""
    return ExperimentalCSV.pdg(param_id)

def get_nufit(param_id: str, ordering: str = "NO") -> Optional[Dict[str, Any]]:
    """Get NuFIT 6.0 value by parameter ID."""
    return ExperimentalCSV.nufit(param_id, ordering)

def get_desi(param_id: str) -> Optional[Dict[str, Any]]:
    """Get DESI 2025 value by parameter ID."""
    return ExperimentalCSV.desi(param_id)


if __name__ == "__main__":
    # Demo usage
    print("PDG 2024 Values:")
    print("-" * 50)
    for param in ["m_higgs", "alpha_em", "m_top", "V_us"]:
        val = ExperimentalCSV.pdg(param)
        if val:
            print(f"  {param}: {val['value']} +/- {val['uncertainty']} {val['units']}")

    print("\nNuFIT 6.0 Values (Normal Ordering):")
    print("-" * 50)
    for param in ["theta_12", "theta_23", "delta_CP"]:
        val = ExperimentalCSV.nufit(param)
        if val:
            print(f"  {param}: {val['value']} +{val.get('uncertainty_plus', '?')}/-{val.get('uncertainty_minus', '?')} {val['units']}")

    print("\nDESI 2025 Values:")
    print("-" * 50)
    for param in ["w0", "H0", "Omega_m"]:
        val = ExperimentalCSV.desi(param)
        if val:
            print(f"  {param}: {val['value']} +/- {val.get('uncertainty', val.get('uncertainty_plus', '?'))} {val['units']}")
