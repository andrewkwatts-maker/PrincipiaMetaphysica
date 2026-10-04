# D-017 computations — PR-1 result, PR-2/PR-3 design (not yet run)

## PR-1 · RESULT (record in the decision log as D-017 RESULT)
Module `src/metaphysica/simulations/PM/geometry/instanton_cycles.py`
(`subgroup_identity()`, `flat_associative_census(point)`, `instanton_cycle_sweep()`),
tests `tests/test_instanton_cycles.py` (7 passed, ~10 s). **Uncommitted at handoff
time — commit with the next engine batch.**

- Subgroup identity dim(ℝ⁷)^S = 8/|S| − 1 holds on all 16 subgroups of Γ (orders
  1, 2, 4, 8 → 7, 3, 1, 0).
- Canonical point (n = 3): 1,792 rows; |S| = 1/2/4: 656/944/192; no |S| = 8 row;
  rigid ∧ b₁ = 0: 0; qualifying: 0.
- Sweep: the canonical point + every n ≥ 1 pairwise-disjoint class of the first
  generating triple — 9,667 classes, 17,323,264 rows. **Qualifying rows: 0** (as
  predicted). Kill condition did NOT fire.
- The hypothesis is not empty: 245 classes have 16 rows each with S = Γ that are
  rigid with b₁ = 0; every one fails only on freeness (the lemma's mechanism).
- Positive control (a free Hantzsche–Wendt (ℤ/2)² action on T₀₁₂ built outside Γ) is
  flagged; zeroing one shift switches it off.
- Unregistered remark (do not log as a result): with half-unit shifts the shift map
  Γ → F₂⁷ is a homomorphism, which would make "S = Γ and free" impossible for every
  class, n = 0 included. A supplementary n = 0 run would test it; label it
  not pre-registered.
- Consequence: C2's M2-instanton direction moves from NEEDS COMPUTATION to KILLED
  for flat associatives (non-flat associatives out of scope; DPW's are S¹×S², b₁ = 1).

## PR-2 / PR-3 · NOT RUN — design for the next session (agent stopped before code)
**Correct the registration wording when recording the result:** "ε ≥ 25/7" in D-017
H3c cannot hold (ε ≤ 3 whenever V ≥ 0). The correct statement is µ_CH²/2 = 25/7 > 3,
so the late-time attractor is kination (ε → 3). The kill condition (µ_CH < √2) is
unaffected.

Convention: ADV's zⁱ = tⁱ + i sⁱ, s the 43-vector (s_A = Re T^A, u = Re U); K_{ij̄} =
K_ij/4, kinetic −(1/4)K_ij(∂s∂s + ∂t∂t), so g = K/2 on both blocks (the module's
normalisation is right).

Derived predictions (hand, not measured):
- PR-2: any K = −Σ ln(2s_A) + F(x) + c with degree-0 x_k = (8/3)u_k²/(s_A s_B)
  satisfies K(λs) = K(s) − 7 ln λ; all identities follow. **Trap:** at u = 0 neither
  modification changes K_ij or K_ijk, and `_random_point` only reaches X ≲ 0.06 — also
  sample X ≈ 0.3–0.6 or the check proves almost nothing.
- H3a: V = 4e^K[Q + W₁²] (W₁² coefficient 7 − 3 = 4 from K^{ij}K_iK_j = 7);
  s·∂_s ln V = −7 + 2Q/(Q + W₁²) ∈ [−7, −5]; radial length √(7/2) → slope ≥ 5√(2/7).
- H3b: at u = 0, bulk flux only, W₁ = 0: slope² = 2Σ(1 − 2p_A)² ≥ 50/7, equality iff
  all |N_A|s_A equal. Twisted flux must be zero (LM_TABLE_1: bulk indices 1–4 in 3
  pairs, 5–7 in 2).
- H3c: truncation u = 0, N_u = 0 consistent; exponents α_A = √2(2e_A − 1) on the
  hyperplane 1·x = −5√2; µ_CH² = 6 + 8/n for n nonzero bulk fluxes, min 5√(2/7) at
  n = 7 (> √2).
- H3d: Γ^w_{wv} = (1/4)K_ijk w^i w^j v_s^k (w normalised by (1/2)K_ij w w = 1);
  bounded analytically at u = 0 (bulk |Γ| ≤ √2; twisted axions |Γ| ≤ 1; radial
  Γ = −√(2/7)); NOT guaranteed with twisted flux or u ≠ 0 (term ~√(3X)) — numerics
  decide. Report the L_eff bound and the window kill separately.
- H3e: single field at the minimum slope from rest gives ≈ 0.30 e-folds of
  acceleration; hyperinflation steady state does not accelerate (2KE/V ≥ 1.89).

Implementation plan:
1. `flux_homogeneity.py`: vectorised K = −kΣ ln(2s_A) + δΣ1/s_A − 3 ln P(X) +
   βΣ w_k h(x_k) + LM_CONSTANT with P = 1 − X − a₂X² − a₃X³; `value`, `gradient`,
   `hessian`, `third_contract(s, a, b)`; per-term derivatives of x = C u² a⁻¹ b⁻¹
   regular at u = 0 (∂_u^i ∂_a^j ∂_b^k x = C·D_i·(−1)^j j! a^{−1−j}·(−1)^k k! b^{−1−k},
   D = (u², 2u, 2, 0)); L(X) = −3 ln P derivatives; cross-check against
   flux_vacuum at a₂ = a₃ = 0 and against finite differences; variants (a₂, a₃) ∈
   {(0.5,0), (0,0.5), (−0.5,0.25), (1,−1)} and h ∈ {x², x²/(1+x), e^{−x} − 1 + x}
   with non-uniform w_k; checks: homogeneity/Euler/second identities, V reduction,
   λ⁻⁵, metric PD, V > 0, c₂ ≠ 0 controls, slope bound; tolerance 1e-12 scaled;
   falsifier δ ≠ 0 or k ≠ 1 must fail.
2. `flux_acceleration.py`: ∂_s ln V = K_s − T(y,y)/(Q + W²) with y = K⁻¹N; ∂_t ln V =
   2WN/(Q + W²); slope² = 2[∂_s·K⁻¹∂_s + ∂_t·K⁻¹∂_t]; precondition with
   D = diag(s_A, √(s_a s_b)), Cholesky (also tests PD); domain X < 1 ∧ K_ij PD;
   closed-form check vs the complex N = 1 formula (K^{ij̄} = 4K^{ij},
   D_iW = N_i − (i/2)K_iW); H3a random + wide sampling over flux types, W²/Q
   log-uniform, plus L-BFGS slope minimisation from ~10 seeded starts; H3b analytic +
   `flux_vacuum.canonical_slope`; H3c truncation residuals, µ_CH by exact KKT
   min-norm over all 127 bulk-flux supports (exponents as ∇_φ ln V of
   single-component fluxes), ~3 long late-time runs; H3d M = (1/4)[H(s + h v_s) −
   H(s − h v_s)]/(2h), generalised eigenproblem vs K/2 on null(Nᵀ),
   L_eff = 1/max|λ|; H3e e-fold EOM φ'' = −(3 − ε)(φ' + G⁻¹∇ln V) − Γ(φ', φ'),
   ε = (1/4)(s'Ks' + t'Kt'), Γ^s = (1/2)K⁻¹[T(s',s') − T(t',t')],
   Γ^t = K⁻¹T(t',s'); DOP853 with an ε = 1 event; stop at X ≥ 0.95 or Cholesky
   failure (report as leaving the domain); 20 e-folds; 200 ICs (seed 20260930)
   cycling rest/random/uphill/flat-axion velocities with KE = rV, r ∈ (0,1];
   measure the longest run with ε < 1. Falsifiers: toy ln V + pΣ ln s_A with p = 4/7
   (radial slope ~0.53) must be flagged by H3a and give ≥ 1 e-fold in H3e; bulk
   weight k = 1/9 (L = 0.236) must open the H3d window.
3. Write sampling ranges, run length and variant list into the docstrings BEFORE
   the first run. The `slow` marker is registered but not deselected by addopts —
   keep the default test fast and slow-mark the 200-trajectory run.
4. Record the D-017 result (with the ε correction) before any wording changes.
