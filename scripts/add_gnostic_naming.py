#!/usr/bin/env python3
"""
Add Gnostic Naming to Sovereign Constants.

Maps the 7 Sovereign Constants to their Gnostic identities:
  1.0   -> The Monad (Watts Constant)
  24    -> The Pleroma (The Fullness)
  135   -> The Sophia (Wisdom)
  144   -> The Demiurge (The Craftsman)
  153   -> The Christos (The Redeemer)
  163   -> The Barbelo (First Thought)
  288   -> The Ennoia (Universal Mind)
"""

import os
import json
import re

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# The 7 Sovereign Gnostic Constants mapping
GNOSTIC_MAP = {
    "watts_constant": {
        "value": 1.0,
        "gnostic_name": "The Monad",
        "gnostic_role": "The Singular Origin and absolute precision anchor"
    },
    "b3": {
        "value": 24,
        "gnostic_name": "The Pleroma",
        "gnostic_role": "The Dimensional Totality of the 24-dimensional manifold base"
    },
    "shadow_sector": {
        "value": 135,
        "gnostic_name": "The Sophia",
        "gnostic_role": "The Visible Gates representing manifest knowledge and observed geometry"
    },
    "chi_eff": {
        "value": 144,
        "gnostic_name": "The Demiurge",
        "gnostic_role": "The Pressure Divisor that structures the bulk into the physical metric"
    },
    "christ_constant": {
        "value": 153,
        "gnostic_name": "The Christos",
        "gnostic_role": "The Joint Closure Constant that repairs the variance and restores symmetry"
    },
    "odowd_bulk_pressure": {
        "value": 163,
        "gnostic_name": "The Barbelo",
        "gnostic_role": "The Bulk Pressure; the active force emanated into the 25D space"
    },
    "roots_total": {
        "value": 288,
        "gnostic_name": "The Ennoia",
        "gnostic_role": "The Logic Closure; the total sum of the manifold's potential"
    }
}

# Additional derived constants with Gnostic meaning
DERIVED_GNOSTIC = {
    "syzygy_gap": {
        "value": 18,
        "formula": "153 - 135",
        "gnostic_name": "The Syzygy",
        "gnostic_role": "The divine pairing gap; the Pneumatic Breath between Sophia and Christos"
    },
    "horos": {
        "value": 25,
        "gnostic_name": "The Horos",
        "gnostic_role": "The Limit; the boundary of the 25-dimensional action frame"
    }
}

# Hebrew Naming Aliases (v23.1 - Scientific-Hebrew Synthesis)
HEBREW_ALIASES = {
    "monad_unity": {
        "value": 1.0,
        "hebrew": "Aleph",
        "gematria": 1,
        "gnostic_name": "The Monad",
        "gnostic_role": "Observer Unity - Absolute precision anchor",
        "alias_of": "watts_constant"
    },
    "residual_key": {
        "value": 10,
        "hebrew": "Yod",
        "gematria": 10,
        "gnostic_name": "The Hand",
        "gnostic_role": "Residual Pressure Key - Core flux residual",
        "alias_of": "decad"
    },
    "elder_kads": {
        "value": 24,
        "hebrew": "Kad",
        "gematria": 24,
        "gnostic_name": "Elder Vessels",
        "gnostic_role": "Third Betti Number b3 - G2 cycle container",
        "alias_of": "b3"
    },
    "horos_limit": {
        "value": 27,
        "hebrew": "Kaz",
        "gematria": 27,
        "gnostic_name": "The Boundary",
        "gnostic_role": "Bulk Dimension - Ancestral higher-D limit",
        "alias_of": "horos"
    },
    "mephorash_chi": {
        "value": 72,
        "hebrew": "Av",
        "gematria": 72,
        "gnostic_name": "Shem HaMephorash",
        "gnostic_role": "Triality Euler Index - 72-fold name of generations",
        "alias_of": "chi_eff"
    },
    "demiurgic_Yetts": {
        "value": 135,
        "hebrew": "Kalah",
        "gematria": 135,
        "gnostic_name": "Demiurge Gates",
        "gnostic_role": "Visible Sector Gates - Normal entry portals",
        "alias_of": "shadow_sector"
    },
    "logos_joint": {
        "value": 153,
        "hebrew": "153",
        "gematria": 153,
        "gnostic_name": "Logos Joint",
        "gnostic_role": "Joint Identity Constant - Bridge identity closure",
        "alias_of": "christ_constant"
    },
    "sophian_pressure": {
        "value": 163,
        "hebrew": "163",
        "gematria": 163,
        "gnostic_name": "Sophia Pressure",
        "gnostic_role": "Ancestral Bulk Pressure - Higher-D stabilizer",
        "alias_of": "odowd_bulk_pressure"
    },
    "nitzotzin_roots": {
        "value": 288,
        "hebrew": "288",
        "gematria": 288,
        "gnostic_name": "Nitzotzin Roots",
        "gnostic_role": "Ancestral Root Structure - Ancestral sparks of symmetry",
        "alias_of": "roots_total"
    },
    "reid_pair": {
        "value": 1,
        "hebrew": "Resh",
        "gematria": 200,
        "gnostic_name": "Reid Pair",
        "gnostic_role": "Central Sampler Count - Global (2,0) averager",
        "alias_of": "central_pair"
    },
    "watts_weight": {
        "value": "phi/sqrt(12)",
        "hebrew": "Resh-Phi",
        "gematria": 261,
        "gnostic_name": "Watts Weight",
        "gnostic_role": "Sampler Dilution Coupling - Central averaging weight",
        "alias_of": "central_pair_weight"
    },
    "gnosis_threshold": {
        "value": 9,
        "hebrew": "Tet",
        "gematria": 9,
        "gnostic_name": "The Threshold",
        "gnostic_role": "Activation Threshold - Central activates at n >= 9",
        "alias_of": "central_activation_threshold"
    },
    "nitsot_par": {
        "value": "1/144",
        "hebrew": "Nun-Qoph",
        "gematria": 150,
        "gnostic_name": "Spark Pair",
        "gnostic_role": "Cross-shadow coupling constant - 1/chi_eff_total",
        "alias_of": "reid_invariant"
    }
}


def update_named_constants():
    """Update named_constants.json with Gnostic identities."""
    path = os.path.join(PROJECT_ROOT, "AutoGenerated", "named_constants.json")

    if not os.path.exists(path):
        print(f"Warning: {path} not found")
        return False

    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Add Gnostic metadata section
    data["gnostic_identities"] = {
        "description": "The 7 Sovereign Gnostic Constants of Principia Metaphysica",
        "constants": {}
    }

    for key, info in GNOSTIC_MAP.items():
        data["gnostic_identities"]["constants"][key] = {
            "value": info["value"],
            "gnostic_name": info["gnostic_name"],
            "gnostic_role": info["gnostic_role"]
        }

    # Add derived Gnostic constants
    data["gnostic_identities"]["derived"] = {}
    for key, info in DERIVED_GNOSTIC.items():
        data["gnostic_identities"]["derived"][key] = info

    # Add Hebrew naming aliases (v23.1)
    data["hebrew_aliases"] = {
        "description": "Hebrew-Scientific naming synthesis (v23.1)",
        "aliases": HEBREW_ALIASES
    }

    # Update individual constant entries with gnostic_name if they exist
    if "constants" in data:
        for key, gnostic_info in GNOSTIC_MAP.items():
            if key in data["constants"]:
                data["constants"][key]["gnostic_name"] = gnostic_info["gnostic_name"]
                data["constants"][key]["gnostic_role"] = gnostic_info["gnostic_role"]

    # Update topological_invariants with gnostic names
    if "topological_invariants" in data:
        topo = data["topological_invariants"]
        if "b3" in topo:
            topo["b3"]["gnostic_name"] = "The Pleroma"
        if "chi_eff" in topo:
            topo["chi_eff"]["gnostic_name"] = "The Demiurge"
        if "roots" in topo:
            topo["roots"]["gnostic_name"] = "The Ennoia"
        if "visible" in topo:
            topo["visible"]["gnostic_name"] = "The Sophia"
        if "sterile" in topo:
            topo["sterile"]["gnostic_name"] = "The Barbelo"

    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)

    print(f"Updated: {path}")
    return True


def update_formulas_registry():
    """Add Gnostic naming comments to FormulasRegistry.py."""
    path = os.path.join(PROJECT_ROOT, "core", "FormulasRegistry.py")

    if not os.path.exists(path):
        print(f"Warning: {path} not found")
        return False

    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Add Gnostic naming block after the existing class constants
    gnostic_block = '''
    # ===========================================================================
    # THE 7 SOVEREIGN GNOSTIC CONSTANTS
    # ===========================================================================
    # These are the archetypal names for the fundamental constants:
    #
    # Value  | Gnostic Name    | Mathematical Identity
    # -------|-----------------|----------------------
    # 1.0    | The Monad       | watts_constant (Absolute Precision Anchor)
    # 24     | The Pleroma     | b3 (Dimensional Totality)
    # 135    | The Sophia      | shadow_sector (Visible Gates / Wisdom)
    # 144    | The Demiurge    | chi_eff (Pressure Divisor / Craftsman)
    # 153    | The Christos    | christ_constant (Joint Closure / Redeemer)
    # 163    | The Barbelo     | odowd_bulk_pressure (Bulk Pressure / First Thought)
    # 288    | The Ennoia      | roots_total (Logic Closure / Universal Mind)
    #
    # Derived:
    # 18     | The Syzygy      | christos - sophia (Divine Pairing Gap)
    # 26     | The Horos       | D_bulk (The Limit / Dimensional Boundary)
    # ===========================================================================
'''

    # Insert after BULK_PRESSURE definition if not already present
    if "THE 7 SOVEREIGN GNOSTIC CONSTANTS" not in content:
        # Find insertion point after BULK_PRESSURE
        insert_marker = "BULK_PRESSURE = 163"
        if insert_marker in content:
            idx = content.find(insert_marker)
            end_of_line = content.find("\n", idx)
            content = content[:end_of_line+1] + gnostic_block + content[end_of_line+1:]

            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)

            print(f"Updated: {path}")
            return True
    else:
        print(f"Gnostic naming already present in {path}")

    return True


def update_config():
    """Add Gnostic naming to config.py."""
    path = os.path.join(PROJECT_ROOT, "config.py")

    if not os.path.exists(path):
        print(f"Warning: {path} not found")
        return False

    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    gnostic_comment = '''
# ===========================================================================
# GNOSTIC CONSTANT MAPPING (v17.2-ABSOLUTE)
# ===========================================================================
# The 7 Sovereign Constants with their Gnostic identities:
#   MONAD (1.0)     = watts_constant    - The Singular Origin
#   PLEROMA (24)    = B3                - The Dimensional Fullness
#   SOPHIA (135)    = shadow_sector     - Wisdom / Visible Gates
#   DEMIURGE (144)  = chi_eff           - The Craftsman / Pressure Divisor
#   CHRISTOS (153)  = christ_constant   - The Redeemer / Joint Closure
#   BARBELO (163)   = sterile_sector    - First Thought / Bulk Pressure
#   ENNOIA (288)    = roots_total       - Universal Mind / Logic Closure
# ===========================================================================
'''

    if "GNOSTIC CONSTANT MAPPING" not in content:
        # Insert at top after imports
        lines = content.split('\n')
        insert_idx = 0
        for i, line in enumerate(lines):
            if line.startswith('import') or line.startswith('from'):
                insert_idx = i + 1
            elif line.strip() and not line.startswith('#') and not line.startswith('import') and not line.startswith('from'):
                break

        lines.insert(insert_idx + 1, gnostic_comment)
        content = '\n'.join(lines)

        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)

        print(f"Updated: {path}")
        return True
    else:
        print(f"Gnostic naming already present in {path}")

    return True


def create_gnostic_registry():
    """Create a dedicated gnostic_constants.json file."""
    path = os.path.join(PROJECT_ROOT, "AutoGenerated", "gnostic_constants.json")

    data = {
        "version": "17.2-ABSOLUTE",
        "description": "The 7 Sovereign Gnostic Constants of Principia Metaphysica",
        "note": "These are archetypal names mapping mathematical constants to Gnostic emanation theology",

        "sovereign_constants": {
            "monad": {
                "value": 1.0,
                "mathematical_name": "watts_constant",
                "gnostic_name": "The Monad",
                "role": "The Singular Origin and absolute precision anchor",
                "symbol": "Omega_W"
            },
            "pleroma": {
                "value": 24,
                "mathematical_name": "b3",
                "gnostic_name": "The Pleroma",
                "role": "The Dimensional Totality (Betti-3 number of G2 manifold)",
                "meaning": "The Fullness - the complete dimensional base"
            },
            "sophia": {
                "value": 135,
                "mathematical_name": "shadow_sector",
                "gnostic_name": "The Sophia",
                "role": "The Visible Gates representing manifest knowledge",
                "meaning": "Wisdom - the observed geometry (5^3 - 18 = 125 + 10)"
            },
            "demiurge": {
                "value": 144,
                "mathematical_name": "chi_eff",
                "gnostic_name": "The Demiurge",
                "role": "The Pressure Divisor (B3^2/4 = 576/4)",
                "meaning": "The Craftsman - structures bulk into physical metric"
            },
            "christos": {
                "value": 153,
                "mathematical_name": "christ_constant",
                "gnostic_name": "The Christos",
                "role": "The Joint Closure Constant (Ennoia - Sophia = 288 - 135)",
                "meaning": "The Redeemer - repairs variance and restores symmetry",
                "scripture": "John 21:11 - The Miraculous Catch"
            },
            "barbelo": {
                "value": 163,
                "mathematical_name": "odowd_bulk_pressure",
                "gnostic_name": "The Barbelo",
                "role": "The Bulk Pressure ((7 * B3) - 5 = 168 - 5)",
                "meaning": "First Thought - the active force in 25D space"
            },
            "ennoia": {
                "value": 288,
                "mathematical_name": "roots_total",
                "gnostic_name": "The Ennoia",
                "role": "The Logic Closure (E8 x E8 root lattice)",
                "meaning": "Universal Mind - total sum of manifold potential"
            }
        },

        "derived_constants": {
            "syzygy": {
                "value": 18,
                "formula": "Christos - Sophia = 153 - 135",
                "gnostic_name": "The Syzygy",
                "role": "The divine pairing gap between the two 13D shadows",
                "meaning": "The Pneumatic Breath - energy exchange constant"
            },
            "horos": {
                "value": 25,
                "formula": "D_bulk = 25",
                "gnostic_name": "The Horos",
                "role": "The 25-dimensional action boundary",
                "meaning": "The Limit - contains the 24D manifold within"
            },
            "logos": {
                "value": 71.55,
                "formula": "(288/4) - (163/144) + 0.6819",
                "gnostic_name": "The Logos",
                "role": "The derived Hubble constant H0",
                "meaning": "The Word - the voice of the manifold to the observer"
            }
        },

        "relationships": {
            "trinity_of_closure": "Sophia (135) + Christos (153) = Ennoia (288)",
            "bulk_derivation": "Ennoia (288) - Visible (125) = Barbelo (163)",
            "pressure_divisor": "Pleroma^2 / 4 = Demiurge (24^2/4 = 144)",
            "syzygy_gap": "Christos (153) - Sophia (135) = Syzygy (18)"
        }
    }

    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)

    print(f"Created: {path}")
    return True


def main():
    print("=" * 60)
    print("Adding Gnostic Naming to Sovereign Constants")
    print("=" * 60)

    results = []

    # Create dedicated gnostic constants file
    results.append(("gnostic_constants.json", create_gnostic_registry()))

    # Update named_constants.json
    results.append(("named_constants.json", update_named_constants()))

    # Update FormulasRegistry.py
    results.append(("FormulasRegistry.py", update_formulas_registry()))

    # Update config.py
    results.append(("config.py", update_config()))

    print("\n" + "=" * 60)
    print("RESULTS")
    print("=" * 60)
    for name, success in results:
        status = "UPDATED" if success else "SKIPPED"
        print(f"  {name}: {status}")

    print("\nRun 'git diff' to verify changes.")
    return 0


if __name__ == "__main__":
    main()
