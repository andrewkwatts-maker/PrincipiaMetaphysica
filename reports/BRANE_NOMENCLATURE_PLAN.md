# Enochian Brane Nomenclature Implementation Plan (v12.9)

## Overview

Implement Enochian Watchtower naming for the 4 branes in the PM framework:

| Brane | Signature | Enochian | Direction | Element | Physics Role |
|-------|-----------|----------|-----------|---------|--------------|
| SM Observable | (5,1) | **Exarp** | East | Air | Light, EM, observation |
| Generation 1 | (3,1) | **Bitom** | South | Fire | e, u, d (stable, foundational) |
| Generation 2 | (3,1) | **Hcoma** | West | Water | μ, c, s (transitional) |
| Generation 3 | (3,1) | **Nanta** | North | Earth | τ, t, b (heavy, hidden) |

---

## Existing Parameters to Map

### From `SharedDimensionsParameters` (config.py:1467-1475):

```python
# Current naming:
Y_OBSERVABLE = 0.0           # UV brane (at y=0)
Y_SHADOW_1 = 1.0 / 3.0       # First shadow (at y=πR/3)
Y_SHADOW_2 = 2.0 / 3.0       # Second shadow (at y=2πR/3)
Y_SHADOW_3 = 1.0             # Third shadow (at y=πR, IR brane)

TENSION_OBSERVABLE = 1e19**6  # T_obs ~ M_*^6 (6D Planck scale)
TENSION_SHADOW = 1e19**4      # T_shadow ~ M_*^4 (4D Planck scale)
```

### Proposed Enochian Mapping:

```python
# New naming (aliases):
Y_EXARP = Y_OBSERVABLE = 0.0           # East/Air - Observable
Y_BITOM = Y_SHADOW_1 = 1.0 / 3.0       # South/Fire - Gen 1
Y_HCOMA = Y_SHADOW_2 = 2.0 / 3.0       # West/Water - Gen 2
Y_NANTA = Y_SHADOW_3 = 1.0             # North/Earth - Gen 3

TENSION_EXARP = 1e19**6  # 6D tension
TENSION_BITOM = 1e19**4  # 4D tension (Gen 1)
TENSION_HCOMA = 1e19**4  # 4D tension (Gen 2)
TENSION_NANTA = 1e19**4  # 4D tension (Gen 3)
```

---

## New Parameters to Derive

### 1. Warp Factors at Each Brane

```python
WARP_EXARP = exp(-k × 0 × πR) = 1.0              # No warping at UV
WARP_BITOM = exp(-k × 1/3 × πR) ≈ 2.5e-6        # Mild warping
WARP_HCOMA = exp(-k × 2/3 × πR) ≈ 6.3e-12       # Moderate warping
WARP_NANTA = exp(-k × 1 × πR) ≈ 1.6e-17         # Strong warping (IR)
```

**Physics:** Warp factors explain mass hierarchy: Gen 3 (τ, t, b) is heaviest because Nanta is at IR brane with strongest warping.

### 2. Elemental Coupling Constants

From Enochian magic, each element has associated qualities:

```python
# Elemental affinities (normalized to 1)
ELEMENT_EXARP = {"name": "Air", "quality": "intellect", "coupling": 1.0}
ELEMENT_BITOM = {"name": "Fire", "quality": "will", "coupling": 0.333}
ELEMENT_HCOMA = {"name": "Water", "quality": "emotion", "coupling": 0.667}
ELEMENT_NANTA = {"name": "Earth", "quality": "matter", "coupling": 1.0}
```

### 3. Sitra Pairing Structure

```python
# Elemental opposition pairs (Enochian duality):
SITRA_PAIR_1 = ("Exarp", "Nanta")  # Air ↔ Earth (Light ↔ Hidden)
SITRA_PAIR_2 = ("Bitom", "Hcoma")  # Fire ↔ Water (Stable ↔ Transitional)

# Cross-brane coupling (from Shadow_ק, Shadow_ח):
SITRA_COUPLING_AIR_EARTH = shadow_kuf = 0.576152
SITRA_COUPLING_FIRE_WATER = shadow_chet = 0.576152
```

### 4. Generation-Specific Mass Scales

Using warp factors to derive fermion mass hierarchies:

```python
# Mass scale ratios (from warp factors):
MASS_SCALE_GEN1 = WARP_BITOM / WARP_EXARP  # ≈ 2.5e-6 (light)
MASS_SCALE_GEN2 = WARP_HCOMA / WARP_EXARP  # ≈ 6.3e-12 (medium)
MASS_SCALE_GEN3 = WARP_NANTA / WARP_EXARP  # ≈ 1.6e-17 (heavy before running)
```

---

## Implementation Structure

### New Class: `BraneNomenclature`

```python
class BraneNomenclature:
    """
    Enochian Watchtower Naming for PM Branes (v12.9).

    Maps the 4 branes to the 4 Elemental Tablets from John Dee's
    Enochian system, with physics parameters for each brane.

    Reference: 1 Enoch 33-36 (Gates of Heaven in four directions)
    """

    # Brane names
    BRANES = ("Exarp", "Bitom", "Hcoma", "Nanta")

    # Cardinal directions
    DIRECTIONS = ("East", "South", "West", "North")

    # Elements
    ELEMENTS = ("Air", "Fire", "Water", "Earth")

    # Signatures
    SIGNATURES = ((5, 1), (3, 1), (3, 1), (3, 1))

    # Y-positions (fractions of πR)
    Y_POSITIONS = (0.0, 1/3, 2/3, 1.0)

    # Physics roles
    ROLES = (
        "Observable (SM, EM, light)",
        "Generation 1 (e, u, d - stable)",
        "Generation 2 (μ, c, s - transitional)",
        "Generation 3 (τ, t, b - heavy)"
    )

    # Enoch's descriptions (1 Enoch 33-36)
    ENOCH_QUOTES = (
        "Three gates of heaven open, wherein the stars go forth",
        "From the first gate proceed dew, rain, prosperity",
        "I saw three great gates where the sun sets",
        "I went to the north and saw cold winds, darkness"
    )

    # Sitra pairings
    SITRA_PAIRS = {
        "air_earth": ("Exarp", "Nanta"),
        "fire_water": ("Bitom", "Hcoma")
    }
```

---

## Files to Modify

| File | Change | Priority |
|------|--------|----------|
| `config.py` | Add `BraneNomenclature` class (~100 lines) | High |
| `config.py` | Add aliases in `SharedDimensionsParameters` | High |
| `run_all_simulations.py` | Export brane nomenclature to JSON | Medium |
| `theory_output.json` | Add `brane_nomenclature` section | Medium |
| `ancient-numerology.html` | Add Enochian branes correlation | Medium |
| `dimensional-reduction-pathway.svg` | Label branes with Enochian names | Low |

---

## Validation Checklist

- [ ] `from config import BraneNomenclature` imports successfully
- [ ] All 4 branes have consistent parameters
- [ ] Warp factors match mass hierarchy expectations
- [ ] Sitra pairings are symmetric
- [ ] JSON export includes all brane data
- [ ] Website displays Enochian names correctly

---

## Physics Justification

### Why This Mapping Works

1. **Exarp (Air/East)** → Observable brane
   - Air = thought, observation, communication
   - We OBSERVE through this brane (EM, light)
   - Position y=0 (UV brane, closest to Planck scale)

2. **Bitom (Fire/South)** → Generation 1
   - Fire = fundamental, primary, life-giving
   - First generation is foundational (stable atoms)
   - Lightest masses (least warped)

3. **Hcoma (Water/West)** → Generation 2
   - Water = transition, flow, passage
   - Second generation bridges light and heavy
   - Intermediate warping

4. **Nanta (Earth/North)** → Generation 3
   - Earth = heavy, material, hidden
   - Third generation is heaviest (top, bottom, tau)
   - Strongest warping (IR brane, y=πR)

### Mass Hierarchy from Warping

The Randall-Sundrum warp factor naturally explains why Gen 3 is heaviest:
- Position at IR brane (y=πR) gives maximum warping
- Yukawa couplings are enhanced by warp factor
- Results in top quark being ~100,000× heavier than up quark

---

## Version Impact

This integration warrants: **v12.8 → v12.9**
- Adds Enochian brane nomenclature
- Provides physics-motivated naming for all 4 branes
- Completes the mystical-geometric correspondence system
