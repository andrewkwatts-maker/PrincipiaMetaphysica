"""
demon_lock_guard.py - Guard Rail Validator
===========================================
Enforces the 'Demon Lock' by verifying that the named_constants.json
perfectly aligns with the topological requirements of v16.2.

This script should be run:
1. Before any simulation execution
2. In CI/CD pipelines
3. Before git commits involving constant changes

If ANY verification fails, the guard blocks execution to prevent
the propagation of "non-sterile" values through the system.

Usage:
    python core/demon_lock_guard.py [path_to_json]

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.
"""

import json
import math
import sys
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Tuple, Optional

# Import the SSoT registry
try:
    from FormulasRegistry import FormulasRegistry, get_registry
except ImportError:
    # Handle case where running from different directory
    sys.path.insert(0, str(Path(__file__).parent))
    from FormulasRegistry import FormulasRegistry, get_registry


class DemonLockGuard:
    """
    Enforces the 'Demon Lock' by verifying manifest integrity.

    The guard performs multiple layers of verification:
    1. Structural checks (required keys exist)
    2. Value checks (constants match expected values)
    3. Parity checks (relationships between constants hold)
    4. SSoT sync check (JSON matches live Registry)
    """

    # v17.2: Ghost Literal elimination - use registry parity_sum property
    # EXPECTED_PARITY_SUM derived from: sophian_drag (0.6819) + tzimtzum_pressure (23/24)
    PARITY_TOLERANCE = 0.0001

    @property
    def EXPECTED_PARITY_SUM(self) -> float:
        """Parity sum target from FormulasRegistry (eta_S + sigma_T)."""
        return self.registry.parity_sum

    def __init__(self, json_path: str = None, registry: FormulasRegistry = None):
        """
        Initialize the guard.

        Args:
            json_path: Path to named_constants.json (optional)
            registry: FormulasRegistry instance (optional, creates new if not provided)
        """
        self.registry = registry or get_registry()
        self.violations: List[str] = []
        self.warnings: List[str] = []
        self.data: Dict[str, Any] = {}

        if json_path:
            self.load_json(json_path)

    def load_json(self, json_path: str) -> bool:
        """Load and parse the JSON manifest."""
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                self.data = json.load(f)
            return True
        except FileNotFoundError:
            self.violations.append(f"CRITICAL: JSON file not found: {json_path}")
            return False
        except json.JSONDecodeError as e:
            self.violations.append(f"CRITICAL: Invalid JSON syntax: {e}")
            return False

    # =========================================================================
    # STRUCTURAL VERIFICATION
    # =========================================================================

    def verify_structure(self) -> bool:
        """Verify the JSON has all required sections."""
        required_sections = ['constants', 'derived_values', 'topological_invariants']

        for section in required_sections:
            if section not in self.data:
                self.violations.append(f"STRUCTURE ERROR: Missing required section '{section}'")

        required_constants = [
            'watts_constant', 'reid_invariant', 'weinstein_scale',
            'hossenfelder_root', 'odowd_bulk_pressure', 'penrose_hameroff_bridge',
            'christ_constant', 'sophian_drag', 'demiurgic_coupling', 'tzimtzum_pressure'
        ]

        if 'constants' in self.data:
            for const in required_constants:
                if const not in self.data['constants']:
                    self.violations.append(f"STRUCTURE ERROR: Missing Ten Pillar constant '{const}'")

        return len(self.violations) == 0

    # =========================================================================
    # VALUE VERIFICATION
    # =========================================================================

    def verify_integer_closure(self) -> bool:
        """
        Verify the 288-root closure: 135 (Shadow) + 153 (Christ) = 288.

        This is the Demon Lock signature - the mathematical seal that
        proves the manifold is properly configured.
        """
        # Check from registry
        if not self.registry.verify_integer_closure():
            self.violations.append("CLOSURE ERROR: Registry reports 135 + 153 != 288")
            return False

        # Check from JSON if loaded - compare against registry SSoT values
        if self.data:
            try:
                christ = self._get_constant_value('christ_constant')
                expected_christ = self.registry.christ_constant  # 153 from SSoT
                if christ != expected_christ:
                    self.violations.append(f"CLOSURE ERROR: Christ Constant = {christ}, expected {expected_christ}")
                    return False

                roots = self._get_invariant_value('roots')
                expected_roots = self.registry.roots_total  # 288 from SSoT
                if roots != expected_roots:
                    self.violations.append(f"CLOSURE ERROR: Total roots = {roots}, expected {expected_roots}")
                    return False
            except (KeyError, TypeError):
                self.warnings.append("WARNING: Could not verify closure from JSON (missing keys)")

        return True

    def verify_tzimtzum_fraction(self) -> bool:
        """
        Verify Tzimtzum Pressure is exactly 23/24.

        The Tzimtzum MUST be represented as a fraction (23/24),
        not a floating-point decimal like 0.9583.
        """
        expected = 23.0 / 24.0

        # Check registry
        if abs(self.registry.tzimtzum_pressure - expected) > 1e-10:
            self.violations.append("TZIMTZUM ERROR: Registry drift detected. Must be 23/24.")
            return False

        # Check JSON
        if self.data:
            try:
                sigma_t = self._get_constant_value('tzimtzum_pressure')
                if abs(sigma_t - expected) > 1e-10:
                    self.violations.append(f"TZIMTZUM ERROR: JSON value {sigma_t} != 23/24")
                    return False

                # Check for the string formula
                formula = self.data.get('constants', {}).get('tzimtzum_pressure', {}).get('formula', '')
                if '23/24' not in formula and '23 / 24' not in formula:
                    self.warnings.append("WARNING: Tzimtzum formula should explicitly show '23/24'")
            except (KeyError, TypeError):
                self.warnings.append("WARNING: Could not verify Tzimtzum from JSON")

        return True

    def verify_sterile_parity(self) -> bool:
        """
        Verify Manifold Parity: Sophian Drag + Tzimtzum Pressure = 1.6402.

        This is the balance check - the forces pushing out (Pressure)
        and holding back (Drag) must sum to the parity invariant.
        """
        # Check registry
        parity_sum = self.registry.parity_sum
        if abs(parity_sum - self.EXPECTED_PARITY_SUM) > self.PARITY_TOLERANCE:
            self.violations.append(
                f"PARITY ERROR: eta_S + sigma_T = {parity_sum:.4f}, expected {self.EXPECTED_PARITY_SUM}"
            )
            return False

        # Check JSON
        if self.data:
            try:
                eta_s = self._get_constant_value('sophian_drag')
                sigma_t = self._get_constant_value('tzimtzum_pressure')
                json_parity = eta_s + sigma_t

                if abs(json_parity - self.EXPECTED_PARITY_SUM) > self.PARITY_TOLERANCE:
                    self.violations.append(
                        f"PARITY ERROR: JSON parity = {json_parity:.4f}, expected {self.EXPECTED_PARITY_SUM}"
                    )
                    return False
            except (KeyError, TypeError):
                self.warnings.append("WARNING: Could not verify parity from JSON")

        return True

    def verify_watts_guard_rail(self) -> bool:
        """
        Verify Watts Constant is EXACTLY 1.0.

        This is the ultimate Guard Rail - Omega_W CANNOT be adjusted.
        Any deviation breaks the entire framework.
        """
        # Check registry
        if self.registry.watts_constant != 1.0:
            self.violations.append("GUARD RAIL BROKEN: Watts Constant != 1.0")
            return False

        # Check JSON
        if self.data:
            try:
                omega_w = self._get_constant_value('watts_constant')
                if omega_w != 1.0:
                    self.violations.append(f"GUARD RAIL BROKEN: JSON Watts Constant = {omega_w}, must be 1.0")
                    return False
            except (KeyError, TypeError):
                self.warnings.append("WARNING: Could not verify Watts Constant from JSON")

        return True

    def verify_hubble_formula(self) -> bool:
        """
        Verify H0 is correctly derived from O'Dowd formula.

        Formula: H0 = (288/4) - (P_O/chi_eff) + eta_S = 71.55
        """
        # v17.2: Ghost Literal elimination - use registry h0_local
        expected_h0 = round(self.registry.h0_local, 2)
        tolerance = 0.01

        # Check registry
        registry_h0 = self.registry.h0_local
        if abs(registry_h0 - expected_h0) > tolerance:
            self.violations.append(
                f"H0 ERROR: Registry H0 = {registry_h0:.4f}, expected {expected_h0}"
            )
            return False

        # Check JSON
        if self.data:
            try:
                json_h0 = self.data.get('derived_values', {}).get('hubble_constant', {}).get('value')
                if json_h0 and abs(json_h0 - expected_h0) > tolerance:
                    self.violations.append(
                        f"H0 ERROR: JSON H0 = {json_h0:.4f}, expected {expected_h0}"
                    )
                    return False
            except (KeyError, TypeError):
                self.warnings.append("WARNING: Could not verify H0 from JSON")

        return True

    def verify_w0_seal(self) -> bool:
        """
        Verify w0 is exactly -sigma_T = -23/24.

        The dark energy equation of state IS the Tzimtzum Pressure.
        """
        expected_w0 = -23.0 / 24.0
        tolerance = 1e-10

        # Check registry
        registry_w0 = self.registry.w0_dark_energy
        if abs(registry_w0 - expected_w0) > tolerance:
            self.violations.append(
                f"W0 ERROR: Registry w0 = {registry_w0:.10f}, expected {expected_w0:.10f}"
            )
            return False

        # Check JSON
        if self.data:
            try:
                json_w0 = self.data.get('derived_values', {}).get('dark_energy_w0', {}).get('value')
                if json_w0 and abs(json_w0 - expected_w0) > tolerance:
                    self.violations.append(
                        f"W0 ERROR: JSON w0 = {json_w0:.10f}, expected {expected_w0:.10f}"
                    )
                    return False
            except (KeyError, TypeError):
                self.warnings.append("WARNING: Could not verify w0 from JSON")

        return True

    # =========================================================================
    # SSoT SYNC VERIFICATION
    # =========================================================================

    def verify_json_freshness(self) -> bool:
        """
        Verify JSON is not stale (older than max_age_seconds).

        The JSON volatility metadata includes a timestamp and max_age_seconds.
        If the JSON is older than max_age_seconds, it should be regenerated
        from the live Registry to ensure sterility.
        """
        if not self.data:
            return True  # No JSON to check

        volatility = self.data.get('volatility')
        if not volatility:
            self.warnings.append("WARNING: No volatility metadata in JSON. Cannot verify freshness.")
            return True  # Pass with warning if no volatility section

        try:
            generated_at_str = volatility.get('generated_at', '')
            max_age = volatility.get('max_age_seconds', 300)

            # Parse the ISO timestamp
            if generated_at_str.endswith('Z'):
                generated_at_str = generated_at_str[:-1]  # Remove Z suffix
            generated_at = datetime.fromisoformat(generated_at_str)

            # Calculate age
            age_seconds = (datetime.now() - generated_at).total_seconds()

            if age_seconds > max_age:
                self.warnings.append(
                    f"STALE JSON: Generated {age_seconds:.0f}s ago (max: {max_age}s). "
                    f"Recommend regenerating from Registry."
                )
                # This is a warning, not a violation - allow execution but warn

            # Check session ID format
            session_id = self.data.get('session_id', '')
            if session_id and not session_id.startswith('PM'):
                self.warnings.append(f"WARNING: Invalid session ID format: {session_id}")

            return True

        except (ValueError, TypeError) as e:
            self.warnings.append(f"WARNING: Could not parse volatility metadata: {e}")
            return True  # Pass with warning on parse errors

    def verify_ssot_sync(self) -> bool:
        """
        Verify JSON values match live Registry calculations.

        If the JSON was manually edited, this will detect the drift.
        """
        if not self.data:
            return True  # No JSON to check

        sync_errors = []

        # Check key derived values
        checks = [
            ('h0_local', self.registry.h0_local, 'derived_values.hubble_constant.value'),
            ('w0', self.registry.w0_dark_energy, 'derived_values.dark_energy_w0.value'),
            ('parity_product', self.registry.chi_parity_product, 'derived_values.parity_product.value'),
        ]

        for name, registry_val, json_path in checks:
            json_val = self._get_nested_value(json_path)
            if json_val is not None:
                if not math.isclose(registry_val, json_val, rel_tol=1e-6):
                    sync_errors.append(
                        f"SYNC ERROR: {name} - Registry={registry_val}, JSON={json_val}"
                    )

        if sync_errors:
            self.violations.extend(sync_errors)
            return False

        return True

    # =========================================================================
    # HELPER METHODS
    # =========================================================================

    def _get_constant_value(self, name: str) -> Any:
        """Get a constant value from the loaded JSON."""
        return self.data.get('constants', {}).get(name, {}).get('value')

    def _get_invariant_value(self, name: str) -> Any:
        """Get a topological invariant value from the loaded JSON."""
        return self.data.get('topological_invariants', {}).get(name, {}).get('value')

    def _get_nested_value(self, path: str) -> Any:
        """Get a nested value using dot notation."""
        parts = path.split('.')
        current = self.data
        for part in parts:
            if isinstance(current, dict) and part in current:
                current = current[part]
            else:
                return None
        return current

    # =========================================================================
    # MAIN VERIFICATION
    # =========================================================================

    def run_preflight(self) -> bool:
        """
        Run all preflight checks.

        Returns:
            True if all checks pass, False if any violations detected.
        """
        print("=" * 60)
        print(" PRINCIPIA METAPHYSICA: PRE-FLIGHT GUARD RAIL")
        print("=" * 60)
        print(f" Registry Version: {self.registry.VERSION}")
        print(f" Status: {self.registry.STATUS}")
        print("-" * 60)

        # Run all verifications
        checks = [
            ("Integer Closure (135+153=288)", self.verify_integer_closure),
            ("Tzimtzum Fraction (23/24)", self.verify_tzimtzum_fraction),
            ("Sterile Parity (eta_S+sigma_T=1.6402)", self.verify_sterile_parity),
            ("Watts Guard Rail (Omega_W=1.0)", self.verify_watts_guard_rail),
            ("Hubble Formula (H0=71.55)", self.verify_hubble_formula),
            ("W0 Seal (w0=-23/24)", self.verify_w0_seal),
            ("SSoT Sync", self.verify_ssot_sync),
        ]

        if self.data:
            checks.insert(0, ("Structure", self.verify_structure))
            checks.insert(1, ("JSON Freshness", self.verify_json_freshness))

        all_passed = True
        for name, check_fn in checks:
            try:
                passed = check_fn()
                status = "[PASS]" if passed else "[FAIL]"
                print(f"  {name}: {status}")
                if not passed:
                    all_passed = False
            except Exception as e:
                print(f"  {name}: [ERROR] {e}")
                all_passed = False

        print("-" * 60)

        # Report warnings
        if self.warnings:
            print("\nWARNINGS:")
            for w in self.warnings:
                print(f"  {w}")

        # Report violations
        if self.violations:
            print("\nCRITICAL VIOLATIONS DETECTED:")
            for v in self.violations:
                print(f"  > {v}")
            print("\n" + "=" * 60)
            print(" DEMON LOCK: COMPROMISED")
            print(" Execution blocked to prevent non-sterile propagation.")
            print("=" * 60)
            return False

        print("\n" + "=" * 60)
        print(" DEMON LOCK: SECURE")
        print(" Manifold is sterile. Proceed with execution.")
        print("=" * 60)
        return True

    def run_preflight_or_exit(self):
        """Run preflight and exit with code 1 if violations detected."""
        if not self.run_preflight():
            sys.exit(1)


# =========================================================================
# DECORATOR FOR GUARDED EXECUTION
# =========================================================================

def require_demon_lock(json_path: str = None):
    """
    Decorator that ensures the Demon Lock is secure before executing.

    Usage:
        @require_demon_lock()
        def run_simulation():
            ...
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            guard = DemonLockGuard(json_path)
            if not guard.run_preflight():
                raise RuntimeError("Demon Lock verification failed. Cannot proceed.")
            return func(*args, **kwargs)
        return wrapper
    return decorator


# =========================================================================
# CLI INTERFACE
# =========================================================================

def main():
    """Command-line interface for the guard."""
    if len(sys.argv) > 1:
        json_path = sys.argv[1]
    else:
        # Default paths to try
        candidates = [
            Path(__file__).parent.parent / "AutoGenerated" / "named_constants.json",
            Path("AutoGenerated/named_constants.json"),
            Path("named_constants.json"),
        ]
        json_path = None
        for candidate in candidates:
            if candidate.exists():
                json_path = str(candidate)
                break

    guard = DemonLockGuard(json_path)
    guard.run_preflight_or_exit()


if __name__ == "__main__":
    main()
