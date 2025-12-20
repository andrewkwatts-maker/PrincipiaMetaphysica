# Enochian Brane Localization Factor Implementation Plan (v12.9)

## Nomenclature Summary

### Brane Localization Factors (Λ)

| Enochian | Greek | Symbol | Formula | Brane | Signature | Element |
|----------|-------|--------|---------|-------|-----------|---------|
| Exarp | Α (Alpha) | **Λ_Α** | e^(-k×0×πR) = 1 | SM Observable | (5,1) | Air |
| Bitom | Π (Pi) | **Λ_Π** | e^(-k×πR/3) | Generation 1 | (3,1) | Fire |
| Hcoma | Υ (Upsilon) | **Λ_Υ** | e^(-k×2πR/3) | Generation 2 | (3,1) | Water |
| Nanta | Γ (Gamma) | **Λ_Γ** | e^(-k×πR) | Generation 3 | (3,1) | Earth |

### Greek Letter Rationale
- **Α (Alpha)** - First letter, primary observable brane
- **Π (Pi)** - From Πῦρ (Pyr = Fire)
- **Υ (Upsilon)** - From Ὕδωρ (Hydor = Water)
- **Γ (Gamma)** - From Γαῖα (Gaia = Earth)

### Sitra Shadow Coupling

| Parameter | Symbol | Value | Pairing | Physics |
|-----------|--------|-------|---------|---------|
| Shadow_ק | **ק_Α_Γ** | 0.576152 | Λ_Α ↔ Λ_Γ | Air↔Earth (Exarp↔Nanta) |
| Shadow_ח | **ח_Π_Υ** | 0.576152 | Λ_Π ↔ Λ_Υ | Fire↔Water (Bitom↔Hcoma) |

---

## Implementation Tasks

### Task 1: config.py - BraneNomenclature Class
**File:** `config.py` (after G2DirectionNomenclature, ~line 2110)

Add new class with:
- ENOCHIAN_NAMES tuple
- GREEK_LETTERS tuple (Α, Π, Υ, Γ)
- GREEK_NAMES tuple (Alpha, Pi, Upsilon, Gamma)
- LAMBDA_SYMBOLS tuple (Λ_Α, Λ_Π, Λ_Υ, Λ_Γ)
- ELEMENTS tuple (Air, Fire, Water, Earth)
- DIRECTIONS tuple (East, South, West, North)
- SIGNATURES tuple ((5,1), (3,1), (3,1), (3,1))
- Y_POSITIONS tuple (0.0, 1/3, 2/3, 1.0)
- SITRA_COUPLINGS dict with ק_Α_Γ and ח_Π_Υ
- Localization factor calculation methods
- get_all_branes() for JSON export

### Task 2: core/constants.py - BraneLocalizationFactors Dataclass
**File:** `core/constants.py` (after G2DirectionNames)

Add frozen dataclass with:
- lambda_alpha, lambda_pi, lambda_upsilon, lambda_gamma
- kuf_alpha_gamma, chet_pi_upsilon
- Variable name mappings

### Task 3: run_all_simulations.py - Export Function
**File:** `run_all_simulations.py` (after g2_direction_nomenclature export)

Add export block for brane_nomenclature section

### Task 4: theory_output.json - Brane Section
**File:** `theory_output.json`

Add new section `brane_nomenclature` with complete structure

### Task 5: ancient-numerology.html - Enochian Branes Section
**File:** `ancient-numerology.html` (after G₂ Sefirot section)

Add correlation box with:
- Enochian Watchtower mapping
- Greek letter table
- Sitra pairing diagram
- Skeptical note

### Task 6: dimensional-reduction-pathway.svg - Brane Labels
**File:** `images/dimensional-reduction-pathway.svg`

Update Branch 1 and Branch 2 boxes with Enochian/Greek labels

### Task 7: Paper HTML Sections
**Files:** `sections/geometric-framework.html`, `sections/fermion-sector.html`

Add Enochian brane terminology where branes are discussed

---

## Variable Naming Convention

### Python Variables
```python
# Localization factors
LAMBDA_ALPHA = 1.0                    # Λ_Α (Exarp)
LAMBDA_PI = exp(-k * pi * R / 3)      # Λ_Π (Bitom)
LAMBDA_UPSILON = exp(-k * 2*pi*R / 3) # Λ_Υ (Hcoma)
LAMBDA_GAMMA = exp(-k * pi * R)       # Λ_Γ (Nanta)

# Sitra couplings (already exist, add aliases)
KUF_ALPHA_GAMMA = shadow_kuf = 0.576152  # ק_Α_Γ
CHET_PI_UPSILON = shadow_chet = 0.576152 # ח_Π_Υ
```

### JavaScript Variables
```javascript
braneLocalization: {
    lambda_alpha: 1.0,           // Λ_Α (Exarp/Air)
    lambda_pi: 2.5e-6,           // Λ_Π (Bitom/Fire)
    lambda_upsilon: 6.3e-12,     // Λ_Υ (Hcoma/Water)
    lambda_gamma: 1.6e-17,       // Λ_Γ (Nanta/Earth)
    kuf_alpha_gamma: 0.576152,   // ק_Α_Γ
    chet_pi_upsilon: 0.576152    // ח_Π_Υ
}
```

### Display Notation
- Λ_Α or Λ<sub>Α</sub> (HTML)
- ק_Α_Γ or ק<sub>Α–Γ</sub> (HTML)

---

## Agent Assignments

| Agent | Task | Files | Priority |
|-------|------|-------|----------|
| 1 | BraneNomenclature class | config.py | High |
| 2 | BraneLocalizationFactors dataclass | core/constants.py | High |
| 3 | Export function + JSON | run_all_simulations.py, theory_output.json | High |
| 4 | Numerology section | ancient-numerology.html | Medium |
| 5 | SVG diagram update | dimensional-reduction-pathway.svg | Medium |
| 6 | Paper sections | sections/*.html | Low |

---

## Validation Checklist

- [ ] `from config import BraneNomenclature` imports
- [ ] Localization factors computed correctly (k=35, R=1)
- [ ] Sitra couplings match existing shadow_kuf/shadow_chet
- [ ] JSON export includes all brane data
- [ ] Website displays Greek letters correctly
- [ ] SVG renders with Enochian labels
- [ ] Paper sections use consistent terminology

---

## Version Bump

**v12.8 → v12.9** includes:
- 24 Shadow Dimension Greek nomenclature (New Jerusalem)
- 7 G₂ Direction Hebrew nomenclature (Sefirot + Enochian Kings)
- 4 Brane Localization Factor nomenclature (Enochian Watchtowers)
