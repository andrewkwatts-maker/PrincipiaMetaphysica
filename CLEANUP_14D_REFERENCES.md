# Cleanup Plan: Remove 14D×2 References

## Context
The codebase currently contains ~204 references to "14D×2" framework that contradicts the correct MASTERPLAN2 framework.

## Correct Framework (MASTERPLAN2)
```
26D with signature (24,2) - 24 space + 2 time
   ↓ Sp(2,R) gauge fixing (NOT compactification)
13D with signature (12,1) - 12 space + 1 time
   ↓ G₂ compactification (7D compact)
6D bulk with signature (5,1) - 5 space + 1 time
   ↓ Torus compactification (2D compact)
4D observable with signature (3,1) - 3 space + 1 time

Branes: (5,1) observable + 3×(3,1) shadow
```

## Incorrect Framework (to be removed)
```
26D = M¹⁴_A ⊗ M¹⁴_B (two 14D halves)
Each 14D with signature (12,2)
```

## Files Requiring Updates (by priority)

### HIGH PRIORITY - Core HTML Files (11 files)
1. **beginners-guide-printable.html** - 13 matches
   - Remove "26D = 14D×2" explanations
   - Replace with "26D → Sp(2,R) → 13D" framework

2. **beginners-guide.html** - 29 matches
   - Update shadow analogy section
   - Fix apartment building visualization

3. **computational-appendices.html** - 8 matches
   - Update code comments
   - Fix framework descriptions

4. **foundations/calabi-yau.html** - 9 matches
   - Update CY4 → G₂ compactification explanations
   - Fix χ_eff calculations (144 from G₂, not 72+72 from two 14D halves)

5. **diagrams/theory-diagrams.html** - 15 matches
   - Redraw dimensional hierarchy diagram
   - Update 2T structure diagram
   - Fix Lagrangian structure diagram

6. **PAPER_2T_UPDATE_SECTION.html** - 4 matches
   - Remove 14D×2 decomposition section
   - Replace with Sp(2,R) gauge fixing explanation

7. **foundations/einstein-hilbert-action.html** - 13 matches
   - Update action pathway
   - Fix stage descriptions

8. **philosophical-implications.html** - 12 matches
   - Update SVG diagrams
   - Fix fermionic primacy explanations

9. **foundations/g2-manifolds.html** - 17 matches
   - Remove "two 14D halves" references
   - Update to single 13D → 6D compactification
   - Fix χ_eff = 144 derivation (from flux-dressed G₂, not mirror copies)

### REPLACEMENT PATTERNS

#### Pattern 1: Dimensional Decomposition
```html
<!-- INCORRECT -->
26D = 14D×2 (two 14D halves sharing 2 times)
M²⁶ = M¹⁴_A ⊗ M¹⁴_B

<!-- CORRECT -->
26D with signature (24,2)
   ↓ Sp(2,R) gauge fixing
13D with signature (12,1)
```

#### Pattern 2: Signature References
```html
<!-- INCORRECT -->
Each 14D half has signature (12,2)

<!-- CORRECT -->
13D has signature (12,1): 12 spatial + 1 timelike
```

#### Pattern 3: Two-Time Structure
```html
<!-- INCORRECT -->
Two 14D halves share 2 times (t_therm, t_ortho)

<!-- CORRECT -->
26D bulk has 2 timelike dimensions with (24,2) signature.
Sp(2,R) gauge fixing projects to 13D with 1 effective time.
Two-time invariants couple via thermal time τ in f(R,T,τ) gravity.
```

#### Pattern 4: Euler Characteristic
```html
<!-- INCORRECT -->
χ_total = χ_A + χ_B = 72 + 72 = 144 (two 14D halves)

<!-- CORRECT -->
χ_eff = 144 from flux-dressed G₂ topology
Direct derivation from G₂ conical singularities and flux quanta
```

#### Pattern 5: Compactification Pathway
```html
<!-- INCORRECT -->
26D → 14D×2 via Sp(2,R) → 7D×2 via dual G₂

<!-- CORRECT -->
26D (24,2) → 13D (12,1) via Sp(2,R) gauge fixing
          → 6D (5,1) via G₂ compactification (7D compact)
          → 4D (3,1) via torus compactification (2D compact)
```

## Implementation Strategy

### Phase 1: Beginner's Guides (Week 1)
- beginners-guide.html
- beginners-guide-printable.html
- Update analogies to use correct 13D framework

### Phase 2: Technical Foundations (Week 2)
- foundations/g2-manifolds.html
- foundations/calabi-yau.html
- foundations/einstein-hilbert-action.html
- computational-appendices.html

### Phase 3: Diagrams & Visualizations (Week 3)
- diagrams/theory-diagrams.html
- philosophical-implications.html (SVG updates)

### Phase 4: Validation (Week 4)
- Grep for remaining "14D" references
- Verify all signatures are correct
- Run SimulateTheory.py validation
- Check git diff for consistency

## Key Concepts to Preserve

1. **Sp(2,R) is gauge fixing, NOT compactification**
   - Projects 26D coordinates to 13D physical space
   - Removes ghost states (makes theory unitary)

2. **Two-time physics still present**
   - 26D has (24,2) signature with 2 timelike dimensions
   - After Sp(2,R), effective 13D has (12,1) with 1 time
   - Two-time invariants (like τ) appear in 4D effective theory via f(R,T,τ)

3. **Shadow universes from brane structure**
   - (5,1) observable brane + 3×(3,1) shadow branes
   - NOT from "two 14D halves"

4. **Generation count from G₂ topology**
   - χ_eff = 144 from flux-dressed G₂ manifold
   - NOT from summing two 72s from "two halves"

## Validation Checklist

- [ ] No references to "14D×2" remain
- [ ] No references to "M¹⁴_A ⊗ M¹⁴_B" remain
- [ ] All signatures correct: (24,2) → (12,1) → (5,1) → (3,1)
- [ ] All χ_eff derivations reference G₂ flux-dressing
- [ ] All dimensional reduction descriptions mention Sp(2,R) gauge fixing
- [ ] SimulateTheory.py validation passes
- [ ] Git diff reviewed for consistency
