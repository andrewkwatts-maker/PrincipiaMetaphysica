# Complete List of Missing Parameters from linkage_issues.json

## User-Specified Parameters (Added) ✓
1. effective-euler ✓
2. generation-count ✓
3. gut-scale ✓
4. planck-mass ✓
5. thermal-exponent ✓
6. dark-energy-w0 ✓
7. suppression-factor ✓
8. gut-coupling ✓
9. proton-lifetime ✓
10. bulk-scale ✓
11. higgs-vev ✓
12. delta-cp ✓
13. betti-b3 ✓
14. dark-energy-wa ✓
15. betti-b2 ✓

## Additional Missing Parameters (Not Yet Added)

### Simple Parameters
16. theta-23 - Neutrino mixing angle θ₂₃
17. strong-coupling - QCD coupling constant
18. instanton-action - Instanton action for Yukawa generation
19. yukawa-coupling - General Yukawa coupling
20. mashiach-modulus - Mashiach stabilization modulus
21. dark-energy-density - Dark energy density ρ_Λ
22. einstein-constant - 8πG/c⁴
23. hubble-parameter - H₀ Hubble constant
24. inverse-temperature - β = 1/kT
25. boltzmann-constant - k_B Boltzmann constant
26. energy-density - Generic energy density ρ
27. higgs-mu - Higgs μ parameter
28. beta-function-i - RG beta functions
29. gauge-coupling-i - Generic gauge coupling

### Compound/Namespaced Parameters (May need different handling)
30. dimensions.D_EFFECTIVE - Already exists as FundamentalConstants.D_EFFECTIVE
31. gauge.M_GUT - Already exists as GaugeUnificationParameters.M_GUT
32. gauge.ALPHA_GUT - Already exists as GaugeUnificationParameters.ALPHA_GUT
33. pneuma.VEV - Already exists as PneumaRacetrackParameters
34. pneuma-field - Pneuma field ψ
35. dark_energy.w0 - Alias for dark-energy-w0
36. dark_energy.wa - Alias for dark-energy-wa
37. kk_spectrum.m1_TeV - Already exists in KKGravitonParameters

### Formula IDs (Not Parameters)
38. superpotential - This is a formula, not a parameter
39. potential - This is a formula, not a parameter
40. bekenstein-hawking - This is a formula, not a parameter

## Analysis

### Category 1: User-Specified (15 params) - DONE ✓
All 15 parameters requested by user have been added to CORE_PARAMETERS.

### Category 2: Simple Missing Parameters (14 params)
These are straightforward parameter additions that follow the same pattern.
Recommendation: Add these to CORE_PARAMETERS in a follow-up.

### Category 3: Namespaced Parameters (8 params)
These reference existing class attributes but need kebab-case IDs for formula linkage.
Recommendation: Create parameter aliases or update formula references.

### Category 4: Formula References (3 items)
These are formulas incorrectly listed as inputParams.
Recommendation: Fix in formula definitions, not here.

## Priority Action Items

### Immediate (User Request) - COMPLETED ✓
✓ Added 15 user-specified parameters to CORE_PARAMETERS

### High Priority (Simple additions)
- Add theta-23 (θ₂₃ = 45.0° from NuFIT 6.0)
- Add strong-coupling (α_s(M_Z) = 0.1180)
- Add hubble-parameter (H₀ = 67.4 km/s/Mpc)

### Medium Priority (Namespaced parameters)
- Create parameter aliases for:
  - dimensions.D_EFFECTIVE → effective-dimensions (= 6)
  - gauge.M_GUT → gut-scale (already added)
  - pneuma.VEV → pneuma-vev

### Low Priority (Formula cleanup)
- Fix formulas that reference:
  - superpotential as inputParam (should be formula reference)
  - potential as inputParam (should be formula reference)
  - bekenstein-hawking as inputParam (should be formula reference)

## Recommendation

The user's immediate request has been fulfilled (15 parameters added).

For complete resolution of all linkage issues:
1. Add the 14 simple missing parameters
2. Create aliases for the 8 namespaced parameters
3. Fix the 3 formula reference issues in formula-database.js
