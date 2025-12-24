# v14.2 Paper Update Plan

## Key v14.2 Changes to Propagate

### 1. KK Spectrum Derivation (CRITICAL - removes circularity)
**OLD**: M_KK = 5 TeV (hardcoded input)
**NEW**: M_KK = M_Pl × exp(-k_eff × π) where k_eff = b₃/(2+ε) ≈ 10.80
- ε = exp(-λ) ≈ 0.223 (Cabibbo angle from G₂ curvature λ=1.5)
- Result: M_KK ≈ 4.5 TeV (derived from topology, not input!)
- Unifies UV topology (b₃=24) → IR physics (M_KK) → Flavor (Cabibbo)

### 2. Geometric Yukawa Textures (Froggatt-Nielsen)
**OLD**: Yukawa couplings mentioned but not derived geometrically
**NEW**: Geometric Froggatt-Nielsen mechanism:
- ε = exp(-λ) = exp(-1.5) ≈ 0.223 (same λ as KK derivation!)
- Fermion masses: m_f = A_f × v × ε^Q_f
- FN charges Q encode radial positions in G₂ manifold
- All 9 fermion masses derived from wave-function overlaps

FN Charges:
- Up-type: top=0, charm=2, up=4
- Down-type: bottom=2, strange=3, down=4
- Leptons: tau=2, muon=4, electron=6

### 3. Topological CP Phase
**OLD**: δ_CP calibrated to NuFIT 6.0, "pending derivation"
**NEW**: δ_CP = π × (Σ orientations) / b₃ = π × (12/24) = π/2 = 90°
- Maximal CP violation from G₂ cycle orientations
- Z₂ structure (#187) gives 12/24 net orientation sum
- |sin δ_CP| = 1 (maximal)

## Sections to Update

| Section | Priority | Key Changes |
|---------|----------|-------------|
| geometric-framework.html | HIGH | Add k_eff derivation, connect λ=1.5 to all physics |
| fermion-sector.html | HIGH | Yukawa textures, CP phase derivation, remove "pending" |
| predictions.html | HIGH | KK spectrum derived (not input), update validation |
| gauge-unification.html | MEDIUM | Reference KK scale derivation |
| introduction.html | MEDIUM | Update overview to reflect derived hierarchy |
| cosmology.html | LOW | KK graviton cross-references |
| conclusion.html | MEDIUM | Summary updates |
| theory-analysis.html | LOW | Validation references |

## Changes to REMOVE (obsolete)

1. Any mention of "5 TeV hardcoded" or circular KK input
2. "Pending derivation" for Yukawa or CP phase
3. Old Yukawa formulas without ε^Q structure
4. Any NuFIT calibration notes for δ_CP (now derived)
5. References to M_KK as an "input" rather than "output"

## Formula Updates

### KK Scale
```
OLD: R_c = 1/5 TeV (constraint)
NEW: k_eff = b₃/(2 + ε) = 24/(2 + 0.223) = 10.80
     M_KK = M_Pl × exp(-k_eff × π) = 2.435×10¹⁸ × exp(-33.93) ≈ 4.5 TeV
```

### Yukawa Couplings
```
NEW: Y_f = A_f × ε^Q_f where ε = exp(-1.5) ≈ 0.223
     m_f = Y_f × v/√2
```

### CP Phase
```
NEW: δ_CP = π × (orientation_sum / b₃) = π × (12/24) = π/2 = 90°
```

## Simulation References
- simulations/kk_spectrum_derived_v14_2.py
- simulations/yukawa_texture_geometric_v14_2.py
- simulations/cp_phase_topological_v14_2.py
