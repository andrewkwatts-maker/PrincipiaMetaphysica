# Foundations Category Standardization Plan

**Date:** 2025-12-26

## Current Issue

The `category` field in foundations uses **inconsistent naming conventions**:
- Some use Title Case: "Established Mathematics", "Established Physics", "Theoretical Physics"
- Others use snake_case: "algebra", "differential_geometry", "quantum_field_theory"

This creates problems for:
- Filtering and searching
- Visual grouping in UI
- Alphabetical sorting
- Code maintainability

## Current Category Distribution

### Title Case (3 categories, 5 foundations)
- **Established Mathematics** (2 foundations)
  - Ricci Tensor & Ricci Scalar
  - Tomita-Takesaki Theory
- **Established Physics** (2 foundations)
  - Unruh Effect
  - Yang-Mills Theory
- **Theoretical Physics** (1 foundation)
  - SO(10) Grand Unified Theory

### snake_case (9 categories, 12 foundations)
- **algebra** (1 foundation)
  - Clifford Algebra
- **differential_geometry** (1 foundation)
  - Metric Tensor
- **dimensional_reduction** (1 foundation)
  - Kaluza-Klein Theory
- **geometry** (2 foundations)
  - Calabi-Yau Manifolds
  - G₂ Manifolds
- **gravity** (2 foundations)
  - Einstein Field Equations
  - Einstein-Hilbert Action
- **quantum** (1 foundation)
  - Dirac Equation
- **quantum_field_theory** (1 foundation)
  - Dirac Spinors
- **thermal_qft** (1 foundation)
  - KMS Condition
- **thermodynamics** (2 foundations)
  - Boltzmann Entropy
  - Hawking Temperature

## Recommended Standardization

### Option A: Pure snake_case (RECOMMENDED)

Convert all categories to lowercase snake_case with specific domains:

```
Established Mathematics → differential_geometry (Ricci Tensor)
Established Mathematics → operator_theory (Tomita-Takesaki)
Established Physics → thermal_physics (Unruh Effect)
Established Physics → gauge_theory (Yang-Mills)
Theoretical Physics → grand_unification (SO(10))
```

**Proposed Final Categories:**
1. `differential_geometry` - Metric Tensor, Ricci Tensor & Ricci Scalar
2. `geometry` - Calabi-Yau Manifolds, G₂ Manifolds
3. `algebra` - Clifford Algebra
4. `operator_theory` - Tomita-Takesaki Theory
5. `dimensional_reduction` - Kaluza-Klein Theory
6. `gravity` - Einstein Field Equations, Einstein-Hilbert Action
7. `quantum_mechanics` - Dirac Equation
8. `quantum_field_theory` - Dirac Spinors
9. `thermal_qft` - KMS Condition
10. `gauge_theory` - Yang-Mills Theory
11. `thermodynamics` - Boltzmann Entropy, Hawking Temperature
12. `thermal_physics` - Unruh Effect (or merge with thermodynamics)
13. `grand_unification` - SO(10) Grand Unified Theory

### Option B: Title Case with Hierarchical Structure

Convert all to Title Case and use hierarchical categories:

```
Mathematics/Differential Geometry
Mathematics/Geometry
Mathematics/Algebra
Mathematics/Operator Theory
Physics/Gravity
Physics/Quantum Mechanics
Physics/Quantum Field Theory
Physics/Thermal Physics
Physics/Gauge Theory
Physics/Grand Unification
Physics/Dimensional Reduction
```

**Pros:** More readable, hierarchical
**Cons:** Harder to filter programmatically, requires delimiter handling

## Implementation Plan

### Step 1: Create Category Mapping

```json
{
  "Established Mathematics": {
    "Ricci Tensor & Ricci Scalar": "differential_geometry",
    "Tomita-Takesaki Theory": "operator_theory"
  },
  "Established Physics": {
    "Unruh Effect": "thermal_physics",
    "Yang-Mills Theory": "gauge_theory"
  },
  "Theoretical Physics": {
    "SO(10) Grand Unified Theory": "grand_unification"
  },
  "quantum": {
    "Dirac Equation": "quantum_mechanics"
  }
}
```

### Step 2: Update theory_output.json

Run migration script to update all category values.

### Step 3: Update Frontend Code

Update any UI components that filter or display by category.

### Step 4: Validate

- Verify all 17 foundations updated correctly
- Test filtering functionality
- Check alphabetical sorting
- Validate JSON structure

## Detailed Mapping

| Foundation | Current Category | Recommended Category | Rationale |
|------------|------------------|---------------------|-----------|
| Ricci Tensor & Ricci Scalar | Established Mathematics | `differential_geometry` | Mathematical structure of curved spacetime |
| Tomita-Takesaki Theory | Established Mathematics | `operator_theory` | Von Neumann algebra theory |
| Unruh Effect | Established Physics | `thermal_physics` | Thermal radiation from acceleration |
| Yang-Mills Theory | Established Physics | `gauge_theory` | Non-abelian gauge theory |
| SO(10) Grand Unified Theory | Theoretical Physics | `grand_unification` | Unified gauge theory |
| Clifford Algebra | algebra | `algebra` | ✓ Already correct |
| Metric Tensor | differential_geometry | `differential_geometry` | ✓ Already correct |
| Kaluza-Klein Theory | dimensional_reduction | `dimensional_reduction` | ✓ Already correct |
| Calabi-Yau Manifolds | geometry | `geometry` | ✓ Already correct |
| G₂ Manifolds | geometry | `geometry` | ✓ Already correct |
| Einstein Field Equations | gravity | `gravity` | ✓ Already correct |
| Einstein-Hilbert Action | gravity | `gravity` | ✓ Already correct |
| Dirac Equation | quantum | `quantum_mechanics` | Relativistic quantum mechanics |
| Dirac Spinors | quantum_field_theory | `quantum_field_theory` | ✓ Already correct |
| KMS Condition | thermal_qft | `thermal_qft` | ✓ Already correct |
| Boltzmann Entropy | thermodynamics | `thermodynamics` | ✓ Already correct |
| Hawking Temperature | thermodynamics | `thermodynamics` | ✓ Already correct |

## Summary

- **Categories to change:** 5
- **Categories already correct:** 12
- **New categories to create:** 3 (`operator_theory`, `thermal_physics`, `grand_unification`, `quantum_mechanics`)
- **Categories to merge:** Consider merging `thermal_physics` with `thermodynamics`
- **Estimated time:** 30 minutes

## Final Category List (12 total)

1. `algebra` (1)
2. `differential_geometry` (2)
3. `dimensional_reduction` (1)
4. `gauge_theory` (1)
5. `geometry` (2)
6. `grand_unification` (1)
7. `gravity` (2)
8. `operator_theory` (1)
9. `quantum_field_theory` (1)
10. `quantum_mechanics` (1)
11. `thermal_qft` (1)
12. `thermodynamics` (3)

**Total Foundations:** 17

---

*See also: `FOUNDATIONS_METADATA_AUDIT.md` for full metadata analysis*
