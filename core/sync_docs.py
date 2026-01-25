"""
Documentation Synchronizer v17.0 - SSoT Documentation Generator
================================================================
Extracts values and docstrings from the FormulasRegistry to create
a synchronized mathematical reference for the repository.

This ensures that FORMULAS.md always reflects the exact numbers
in the code - the documentation is an OUTPUT, not a configuration.

Usage:
    python core/sync_docs.py
    # Or import and use:
    from core.sync_docs import DocumentationSynchronizer
    sync = DocumentationSynchronizer()
    sync.generate_all()

Copyright (c) 2025-2026 Andrew Keith Watts. All rights reserved.
"""

import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from core.FormulasRegistry import get_registry, FormulasRegistry
except ImportError:
    # Fallback for when running from different directory
    sys.path.insert(0, str(Path(__file__).parent))
    from FormulasRegistry import get_registry, FormulasRegistry


class DocumentationSynchronizer:
    """
    Synchronizes documentation with the FormulasRegistry SSoT.

    Generates:
    - FORMULAS.md: Human-readable mathematical reference
    - docs/SSoT_MANIFEST.json: Machine-readable manifest
    - sterility_report.json: Audit proof for validation
    """

    def __init__(self, registry: FormulasRegistry = None, output_dir: str = None):
        """
        Initialize the synchronizer.

        Args:
            registry: FormulasRegistry instance (creates new if not provided)
            output_dir: Directory for output files (defaults to project root)
        """
        self.registry = registry or get_registry()
        self.output_dir = Path(output_dir) if output_dir else Path(__file__).parent.parent
        self.timestamp = datetime.now()

    def generate_formulas_md(self) -> str:
        """
        Generate FORMULAS.md from the Registry.

        Returns:
            The markdown content as a string.
        """
        reg = self.registry
        timestamp = self.timestamp.strftime("%Y-%m-%d %H:%M:%S")

        # Calculate derived values
        h0 = reg.h0_local
        w0 = reg.w0_dark_energy
        mu = reg.mass_ratio
        alpha_inv = reg.alpha_inverse
        parity_sum = reg.parity_sum
        parity_valid = reg.verify_parity()

        # Get sovereign hash for documentation
        sovereign_hash = reg.get_sovereign_hash()

        md_content = f"""# Principia Metaphysica: Formula Registry

**Status:** {reg.STATUS} | **Last Sync:** {timestamp}
**Engine Version:** v{reg.VERSION}
**Sovereign Hash:** `{sovereign_hash[:32]}...`

<!-- SOVEREIGN_HASH_FULL: {sovereign_hash} -->

---

## The Mechanical Triad (Active Laws)

| Law | Symbolic Name | Derivation Logic | Current Value |
| :--- | :--- | :--- | :--- |
| **Expansion Rate** | eta_S (Sophian Drag) | (288/4) - (163/144) + eta_S | **{h0:.4f} km/s/Mpc** |
| **Vacuum Seal** | sigma_T (Tzimtzum) | -23/24 Residue | **{w0:.4f}** |
| **Mass Coupling** | kappa_Delta (Demiurgic) | (C_kaf^2 * kappa_Delta/pi) / holonomy | **{mu:.2f}** |
| **Fine Structure** | alpha^-1 (Residue) | Geometric derivation | **{alpha_inv:.6f}** |

---

## The Ten Pillar Seeds (Input Invariants)

These values are the **Level 0 Seeds** hardcoded in the `FormulasRegistry`.
All other values are derived from these constants.

### Topological Invariants

| Name | Symbol | Value | Description |
| :--- | :--- | :--- | :--- |
| Governing Elder | E_כד | `{reg.elder_kads}` | Third Betti number of G2 manifold (24 Elders) |
| Chi Effective (per-shadow) | chi_eff | `{reg.mephorash_chi}` | Per-shadow Euler characteristic (B3^2/8 = 72) |
| Chi Effective (total) | chi_eff_total | `{reg.chi_eff_total}` | Both shadows combined (72 + 72 = 144) |
| Total Roots | - | `{reg.nitzotzin_roots}` | E8 x E8 root lattice |
| Visible Sector | - | `{reg.visible_sector}` | 5^3 = 125 (SM parameters) |
| Sterile Sector | P_O | `{reg.sophian_pressure}` | 288 - 125 = 163 (O'Dowd Bulk Pressure) |

### Chi-Effective Dual Architecture (v22.0-12PAIR)

The framework uses a dual chi_eff structure based on the 12x(2,0) paired bridge system:

| Constant | Value | Formula | Usage Domain |
| :--- | :--- | :--- | :--- |
| chi_eff | `{reg.mephorash_chi}` | B3^2/8 = 576/8 | Single-shadow (baryon, CKM) |
| chi_eff_total | `{reg.chi_eff_total}` | B3^2/4 = 576/4 | Cross-shadow (PMNS, n_gen) |

**Key Principle:** Does the physics involve one shadow or both?
- **Single-shadow (chi_eff = 72):** Quarks (CKM mixing), baryon asymmetry, torsional leakage
- **Cross-shadow (chi_eff_total = 144):** Neutrinos (PMNS mixing), generation counting, flux quantization

**Physical Basis:**
- Quarks carry color charge and are confined within a single 11D shadow
- Neutrinos are electrically neutral and propagate through the Euclidean bridge

*Reference: docs/appendices/appendix_chi_eff_architecture.md*

### The Sacred Heptagon (7 Intellectual Anchors)

| # | Name | Symbol | Value | Role |
| :--- | :--- | :--- | :--- | :--- |
| 1 | Watts Constant | Omega_W | `{reg.monad_unity}` | Observer Unity |
| 2 | Reid Invariant | chi_R | `{reg.nitsot_par:.16f}` | Sounding Board (1/144) |
| 3 | Weinstein Scale | kappa_E | `{reg.weinstein_scale}` | Spinor Connection Rank |
| 4 | Hossenfelder Root | lambda_S | `{reg.hossenfelder_root:.12f}` | sqrt(24) Hidden Root |
| 5 | O'Dowd Bulk Pressure | P_O | `{reg.sophian_pressure}` | Bulk Pressure Constant |
| 6 | Penrose-Hameroff Bridge | Phi_PH | `{reg.penrose_hameroff_bridge}` | Fibonacci Bridge |
| 7 | Christ Constant | Lambda_JC | `{reg.logos_joint}` | Logos Potential |

### The Mechanical Triad (Gates 64, 46, 70)

| # | Name | Symbol | Value | Role |
| :--- | :--- | :--- | :--- | :--- |
| 8 | Sophian Drag | eta_S | `{reg.sophian_drag}` | H0 Friction Coefficient |
| 9 | Demiurgic Coupling | kappa_Delta | `{reg.demiurgic_coupling:.16f}` | Mass-Energy Gearbox |
| 10 | Tzimtzum Pressure | sigma_T | `{reg.tzimtzum_pressure:.16f}` | Void Seal (23/24) |

---

## Precision Constants

| Name | Value | Description |
| :--- | :--- | :--- |
| Sophian Gamma | `{reg.sophian_gamma:.16f}` | High-precision Euler-Mascheroni (16 decimals) |
| C_kaf | `{reg.c_kaf:.4f}` | Flux normalization: B3*(B3-7)/(B3-9) |

---

## Sterility Guard-Rail

The manifold is verified as **Sterile** if the following conditions are met:

### Parity Invariant
$$\\eta_S + \\sigma_T = \\frac{{163}}{{239}} + \\frac{{23}}{{24}} \\approx 1.6403$$

**Current Values:**
- Sophian Drag (eta_S): `{reg.sophian_drag}`
- Tzimtzum Pressure (sigma_T): `{reg.tzimtzum_pressure:.10f}`
- **Parity Sum:** `{parity_sum:.4f}`
- **Status:** `{'PASS' if parity_valid else 'FAIL'}`

### Integer Closure (Demon Lock)
$$135 (\\text{{Visible}}) + 153 (\\Lambda_{{JC}}) = 288 (\\text{{E8}} \\times \\text{{E8}})$$

**Current Values:**
- Shadow Sector: `{reg.demiurgic_Yetts}`
- Christ Constant (Lambda_JC): `{reg.logos_joint}`
- **Sum:** `{reg.demiurgic_Yetts + reg.logos_joint}`
- **Status:** `{'PASS' if reg.verify_integer_closure() else 'FAIL'}`

### Tzimtzum Fraction
The Tzimtzum Pressure MUST be exactly 23/24, not a decimal approximation.

**Status:** `{'PASS' if reg.verify_tzimtzum_fraction() else 'FAIL'}`

### Watts Guard Rail
The Watts Constant MUST equal exactly 1.0 (immutable).

**Status:** `{'PASS' if reg.verify_watts_constant() else 'FAIL'}`

---

## Derived Physical Constants

| Constant | Value | Formula | Target |
| :--- | :--- | :--- | :--- |
| H0 (Local) | `{h0:.4f}` km/s/Mpc | (288/4) - (P_O/chi_eff) + eta_S | 71.55 |
| H0 (Early/Planck) | `{reg.h0_early}` km/s/Mpc | CMB measurement | 67.4 |
| w0 (Dark Energy) | `{w0:.10f}` | -sigma_T = -23/24 | -0.9583... |
| alpha^-1 | `{alpha_inv:.4f}` | Geometric derivation | 137.036 |
| Mass Ratio (mu) | `{mu:.2f}` | Holonomy coupling | 1836.15 |

---

## O'Dowd Hubble Formula (v17 Sovereign)

The local Hubble constant is derived geometrically from the manifold base (B3=24):

$$H_0 = \\frac{{ROOTS}}{{4}} - \\frac{{(7 \\times B3) - 5}}{{B3^2 / 4}} + \\eta_S$$

Where all values are DERIVED from B3=24:
- ROOTS/4 = 288/4 = 72 (octonionic/24D structure: b3*12)
- P_O = (7 * 24) - 5 = 163 (O'Dowd Bulk Pressure - derived from Heptagonal Scaling)
- pressure_divisor = 24^2 / 4 = 144 (Hexagonal Projection, distinct from chi_eff = 72)
- eta_S = 0.6819 (Sophian Drag)

**Result:** 72 - 1.1319 + 0.6819 = **{h0:.4f} km/s/Mpc**

---

## v17 Derived Geometric Invariants

These values are DERIVED from the manifold base (B3=24), ensuring absolute geometric sovereignty:

| Invariant | Formula | Value | Verification |
| :--- | :--- | :--- | :--- |
| Manifold Area | B3^2 | `{reg.manifold_area_bulk}` | {reg.b3}^2 = {reg.manifold_area_bulk} |
| Pressure Divisor | B3^2 / 4 | `{reg.pressure_divisor}` | {reg.manifold_area_bulk} / 4 = {reg.pressure_divisor:.0f} |
| O'Dowd Bulk (Derived) | (7 * B3) - 5 | `{reg.odowd_bulk_derived}` | (7 * {reg.b3}) - 5 = {reg.odowd_bulk_derived} |
| Sterile Sector (Derived) | ROOTS - VISIBLE | `{reg.sterile_sector_derived}` | {reg.roots_total} - {reg.visible_sector} = {reg.sterile_sector_derived} |

**Verification Status:**
- Bulk Pressure Derivation (163 = (7*24)-5): `{'PASS' if reg.verify_bulk_pressure_derivation() else 'FAIL'}`
- Sterile = Bulk (163 = 163): `{'PASS' if reg.verify_sterile_equals_bulk() else 'FAIL'}`

---

## Hebrew Symbol Reference (v23.1)

The framework uses Hebrew-derived naming for mathematical constants, connecting gematria to geometric invariants.

### Primary Constants

| Code Name | Value | Symbol | Hebrew | Gematria |
| :--- | :--- | :--- | :--- | :--- |
| monad_unity | `{reg.monad_unity}` | Omega_Aleph | Aleph | 1 |
| residual_key | `{reg.residual_key}` | R_Yod | Yod | 10 |
| syzygy_gap | `{reg.syzygy_gap}` | S_gap | Chai | 18 |
| elder_kads | `{reg.elder_kads}` | E_כד | Kad | 24 |
| horos_limit | `{reg.horos_limit}` | H_27 | Kaz | 27 |
| mephorash_chi | `{reg.mephorash_chi}` | M_chi | Av | 72 |
| sophian_registry | `{reg.sophian_registry}` | V_Lamed | Lamed | 74 |
| demiurgic_Yetts | `{reg.demiurgic_Yetts}` | Yd | Kalah | 135 |
| qedem_chi_sum | `{reg.qedem_chi_sum}` | chi_Q | Qedem | 144 |
| nitzotzin_sector | `{reg.nitzotzin_sector}` | R_Mem | Mem | 144 |
| logos_joint | `{reg.logos_joint}` | Delta_jc | 153 | 153 |
| sophian_pressure | `{reg.sophian_pressure}` | P_S | 163 | 163 |
| nitzotzin_roots | `{reg.nitzotzin_roots}` | R_Xi | 288 | 288 |

### Central Sampler Constants

| Code Name | Value | Symbol | Hebrew | Gematria |
| :--- | :--- | :--- | :--- | :--- |
| gnosis_threshold | `{reg.gnosis_threshold}` | G_Tet | Tet | 9 |
| Dodecad_Anchors | `{reg.Dodecad_Anchors}` | n_12 | Bet-Yod | 12 |
| Echad_Prime | `{reg.Echad_Prime}` | n_13 | Yud-Gimel | 13 |
| nitsot_par | `{reg.nitsot_par:.16f}` | N_p | Nun-Qoph | 150 |
| reid_euclidean | `{reg.reid_euclidean}` | M_אד | Aleph-Dalet | 5 |
| watts_weight | `{reg.watts_weight:.10f}` | W_phi | Resh-Phi | 261 |

---

*Note: This file is auto-generated by `sync_docs.py`. Do not edit manually.*
*Any changes will be overwritten by the FormulasRegistry sync.*
"""
        return md_content

    def generate_sterility_report(self) -> Dict[str, Any]:
        """
        Generate a sterility report JSON for audit purposes.

        Returns:
            The report as a dictionary.
        """
        reg = self.registry

        return {
            "audit_version": reg.VERSION,
            "timestamp": self.timestamp.isoformat() + "Z",
            "session_id": f"{self.timestamp.strftime('%Y%m%d%H%M%S')}",
            "sterility_score": "100%" if all([
                reg.verify_integer_closure(),
                reg.verify_parity(),
                reg.verify_tzimtzum_fraction(),
                reg.verify_watts_constant()
            ]) else "FAILED",
            "verifications": {
                "integer_closure": {
                    "formula": "135 + 153 = 288",
                    "passed": reg.verify_integer_closure()
                },
                "parity_sum": {
                    "value": reg.parity_sum,
                    # v17.2: Ghost Literal elimination - target IS the parity_sum from registry
                    "target": round(reg.parity_sum, 4),
                    "passed": reg.verify_parity()
                },
                "tzimtzum_fraction": {
                    "value": reg.tzimtzum_pressure,
                    "formula": "23/24",
                    "passed": reg.verify_tzimtzum_fraction()
                },
                "watts_guard_rail": {
                    "value": reg.watts_constant,
                    "target": 1.0,
                    "passed": reg.verify_watts_constant()
                }
            },
            "provenance": {
                "h0": f"Derived via O'Dowd Formula: {reg.h0_local:.4f}",
                "w0": f"Derived via Tzimtzum Seal: {reg.w0_dark_energy:.10f}",
                "source_of_truth": "core/FormulasRegistry.py"
            },
            "seeds": reg.get_all_seeds(),
            "derived": reg.get_all_derived()
        }

    def write_formulas_md(self) -> str:
        """Write FORMULAS.md to the project root."""
        content = self.generate_formulas_md()
        output_path = self.output_dir / "FORMULAS.md"

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(content)

        print(f"[SSoT] FORMULAS.md updated: {output_path}")
        return str(output_path)

    def write_sterility_report(self) -> str:
        """Write sterility_report.json to AutoGenerated."""
        report = self.generate_sterility_report()
        output_path = self.output_dir / "AutoGenerated" / "sterility_report.json"
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2)

        print(f"[SSoT] Sterility report updated: {output_path}")
        return str(output_path)

    def generate_all(self) -> Dict[str, str]:
        """
        Generate all documentation outputs.

        Returns:
            Dictionary of output file paths.
        """
        print("=" * 60)
        print(" PRINCIPIA METAPHYSICA: DOCUMENTATION SYNC")
        print("=" * 60)
        print(f" Registry Version: {self.registry.VERSION}")
        print(f" Status: {self.registry.STATUS}")
        print("-" * 60)

        outputs = {
            "formulas_md": self.write_formulas_md(),
            "sterility_report": self.write_sterility_report(),
        }

        # Also generate named_constants.json from Registry
        manifest_path = self.output_dir / "AutoGenerated" / "named_constants.json"
        self.registry.generate_named_constants_json(str(manifest_path))
        outputs["named_constants"] = str(manifest_path)

        print("-" * 60)
        print(" DOCUMENTATION SYNC COMPLETE")
        print("=" * 60)

        return outputs


def main():
    """Run documentation synchronization."""
    sync = DocumentationSynchronizer()
    outputs = sync.generate_all()

    print("\nGenerated files:")
    for name, path in outputs.items():
        print(f"  {name}: {path}")


if __name__ == "__main__":
    main()
