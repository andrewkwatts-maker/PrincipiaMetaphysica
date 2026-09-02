# The Five Scale Disagreements — Assessment

**Prepared:** 2026-08-30 · **Status:** evidence + recommendation; the
rulings are the author's. **Outcomes recorded 2026-09-02 — see the addendum
at the foot of this file.** Four of the five are fixed; only
`spectral.lambda_max` still reads `DISAGREE_SCALE` in `eml_crosscheck.json`.

`DISAGREE_SCALE` marks a row whose EML expression and registered value
differ by a near-exact power of ten. The label invites the assumption
that all five are unit slips. They are not: **only one is**. Every
registered value below was reconstructed numerically before judging, so
each verdict rests on arithmetic rather than on reading the prose.

Ranked by how much of the disagreement is presentation versus physics.

---

## 1. `consciousness.tau_gnosis` — pure unit mismatch, formula CONFIRMED

| | |
|---|---|
| EML evaluates | 2453.253020 |
| Registered | 2.453253 (units field: **seconds**) |
| Ratio | **exactly 1000** |

The EML expression `25 · exp(3.2·√1) · 2²` reproduces the registered
value to **zero relative error** once divided by 1000. The formula is
right; the expression works in milliseconds while the registry declares
seconds.

**Most robust of the five.** Nothing about the derivation is in question
— an exact reconstruction is the strongest evidence available that the
structure is correct. The defect is entirely in units.

**Recommended fix:** convert in the expression (`ops.div(…, 1000)`) or
correct the `units` field to milliseconds. Do **not** simply relabel to
make the check pass — pick whichever is physically intended and make the
other follow.

---

## 2. `gravity.scalar_breathing_amplitude` — result pasted into an input slot

| | |
|---|---|
| EML evaluates | 1.73611e-12 |
| Registered | 1.73611e-09 |
| Ratio | **exactly 0.001** |

The expression is `α_F_r2 × 1e-9` with the comment *"A ~ α_F × (NS merger
strain) ~ 10⁻⁹"*. Since α_F_r2 ≈ 1.736e-3, a strain of 1e-9 gives 1.7e-12
— but the comment says the **result** should be ~10⁻⁹. The `~10⁻⁹` from
the prose was placed where the NS-merger strain belongs; the strain that
yields the registered value is ~10⁻⁶.

**Diagnosable with certainty**, because the docstring states the intended
result independently of the expression. A transcription error, not a
physics disagreement.

**Recommended fix:** replace `eml_scalar(1e-9)` with the actual NS-merger
strain (~1e-6) and cite it. The mantissa 1.73611 matching exactly on both
sides confirms nothing else is wrong.

---

## 3. `consciousness.tau_baseline` — incomplete expression (two defects)

| | |
|---|---|
| EML evaluates | 25 (the bare input constant) |
| Registered | 0.240235 (seconds) |
| Ratio | 104.065 — **not** a power of ten |

Reconstructed exactly: `25 · exp(3.2·√(6/12)) = 240.235 ms = 0.240235 s`,
matching the registered value to **0.0000%**. So the registry value is
fully derivable — the EML expression simply does not express it. It
carries the bare 25 ms seed with neither the six-pair enhancement factor
(≈9.61) nor the ms→s conversion.

Note this row was mislabelled: 104.065 is not a power of ten, so it is
only in this bucket by the classifier's 0.02-dex tolerance. It is an
*incomplete expression*, not a scale error.

**Recommended fix:** write the full expression, mirroring `tau_gnosis`
with `n_pairs = 6`. Both consciousness entries are flagged SPECULATIVE
in-module, and the 3.2 and 2² are phenomenological Orch-OR parameters,
not b₃-derived — internally consistent, but with **no geometric
grounding**. Fixing the expression does not change that status.

---

## 4. `portals.sterile_mixing_sin2_2theta` — NOT a scale error. A falsification.

| | |
|---|---|
| EML claims | sin²(2θ) = 1/b₃ = 1/24 = **4.1667e-02** |
| Registered | **4.2767e-05** |
| Ratio | 974.3 — not a power of ten |
| Anchor | 0.01 (IceCube/MINOS+ 2024) |

**This is the one with real physics content, and it is the most
important finding of the five.**

The registered value passes the declared bound comfortably
(4.28e-05 < 0.01). The EML's elegant geometric claim — sin²(2θ) = 1/b₃,
"sterile mixing from torsion geometry" — evaluates to 0.0417, which
**exceeds it by 4.17×**.

*Bound checked against the literature, not just the registry:* published
MINOS/MINOS+ and IceCube 90% CL limits are sin²(2θ₂₄) ≲ 0.02 at
Δm²₄₁ ~ 0.3 eV², so the registry's 0.01 is the tighter figure and the
1/b₃ claim exceeds the published limit by ~2.1× rather than 4.17×.
Falsified on either, but the factor depends on the anchor — and the real
limit is Δm²-dependent, so the registry storing a bare scalar with no
mass splitting is a separate defect worth fixing.

So this is not two spellings of one number. It is a zero-parameter b₃
claim that the data excludes, sitting in the description field of a
parameter whose registered value comes from different physics entirely
and passes. The row reports PASS while carrying a falsified claim in its
own description.

**Geometric elegance is highest here and accuracy is worst** — precisely
the combination the θ₁₃ = asin(1/6) ruling (register 1.1) already
addressed. The same treatment applies.

**Recommended ruling:** label the `sin²(2θ) = 1/b₃` claim **FALSIFIED**
and keep it on the books per standing policy, then give the registered
value an `eml_description` that describes the derivation actually used.
Leaving a falsified claim as the published description of a passing
parameter is the more serious defect of the two.

---

## 5. `spectral.lambda_max` — least resolvable, weakest grounding

| | |
|---|---|
| EML evaluates | 991.624 (`k_gimel × 80.5`) |
| Registered | 9.903956e+17 |
| Ratio | 9.9876e14 — **0.124% off** an exact 1e15 |

The units field says *"dimensionless (k_gimel normalized)"*, so the EML
computes a normalised eigenvalue while the registry stores an
unnormalised one. But the ratio is **not** a clean power of ten: it
misses 1e15 by 0.124%, which is far outside anything a unit convention
explains. Either the normalisation constant or the stored value carries
an additional unexplained factor.

The `80.5` traces to nothing in the registry — it is the least grounded
number in this set, with the appearance of a fitted constant rather than
a derived one.

**Lowest confidence of the five.** Recommend deriving the normalisation
explicitly, or relabelling `80.5` as CALIBRATED if it cannot be derived.
Until then this row should not be read as a check of anything.

---

## Summary

| # | Parameter | Nature | Robustness | Geometric grounding |
|---|---|---|---|---|
| 1 | `tau_gnosis` | unit only (×1000, exact) | **highest** — formula reproduced exactly | none (phenomenological) |
| 2 | `scalar_breathing_amplitude` | result pasted into input slot | high — mantissa matches exactly | n/a (observational input) |
| 3 | `tau_baseline` | incomplete expression | high — registry value reconstructed exactly | none (phenomenological) |
| 4 | `sterile_mixing_sin2_2theta` | **falsified geometric claim** | claim excluded by data at 4.17× | **highest claim, worst accuracy** |
| 5 | `spectral.lambda_max` | unexplained 0.124% residual | **lowest** | `80.5` traces to nothing |

**Most robust and accurate:** `tau_gnosis` — an exact reconstruction
leaves nothing in doubt but the unit.

**Most geometrically consistent as *stated*:** `sterile_mixing` — and
that is exactly why it matters that the data excludes it. Elegance
without accuracy is the pattern this register exists to catch.

**Cross-cutting caution:** four of these five are cheap to make "agree"
by editing the `eml_description`. That would be making a check pass by
editing the thing being checked. In every case the correction belongs on
whichever side is actually wrong, decided on the physics.

---

## Methodological note

The pattern in row 4 is not incidental to this framework, and it has a
literature. Hossenfelder, *Screams for Explanation: Finetuning and
Naturalness in the Foundations of Physics*
([arXiv:1801.02176](https://arxiv.org/abs/1801.02176), Synthese 2019)
argues that finetuning and naturalness arguments carry far less
evidential weight than they are given, and explicitly discusses
**numerological coincidences** — small-integer relations that look
explanatory but are not.

That is the exact failure mode this register keeps recording, three times
now and always in the same direction:

| Claim | Form | Outcome |
|---|---|---|
| θ₁₃ = asin(1/6) | small-integer, zero-parameter | ~9σ, FALSIFIED (reg. 1.1) |
| sin²(2θ) = 1/b₃ | small-integer, zero-parameter | exceeds the bound, §4 above |
| S₈ friction 5.1% | closed form matching no declared model | retired (reg. 1.4, R2) |

Each was maximally elegant, and each was wrong. The relevant discipline
is not "distrust b₃ relations" — b₃ = 24 genuinely fixes several things —
but that **an integer ratio landing near a measured value is weak
evidence on its own**, and needs a derivation chain independent of the
coincidence. The framework's falsification-first posture already
implements this; the citation gives it published footing rather than
being merely a house style.


---

## Addendum — outcomes (2026-09-02)

Read from `AutoGenerated/eml_crosscheck.json`, not from memory. The
`DISAGREE_SCALE` bucket has gone **5 → 1**.

| # | Parameter | Recommendation | Outcome |
|---|---|---|---|
| 1 | `consciousness.tau_gnosis` | fix units, don't relabel to pass | **AGREE** — expression now evaluates 2.453253 against registered 2.4532530 |
| 2 | `gravity.scalar_breathing_amplitude` | supply the real NS-merger strain | **AGREE** — evaluates 1.7361e-09, matching the registered value |
| 3 | `consciousness.tau_baseline` | write the full expression with n_pairs = 6 | **AGREE** — evaluates 0.2402350. Still SPECULATIVE in-module: the 3.2 and 2² remain phenomenological Orch-OR parameters with no geometric grounding, exactly as this note said, and fixing the expression did not change that |
| 4 | `portals.sterile_mixing_sin2_2theta` | label the 1/b₃ claim FALSIFIED, describe the derivation actually used | **DONE** — the description now opens `FALSIFIED: sin²(2θ) = 1/b₃ …` and goes on to state the bridge-mediated type-I seesaw the registered 4.28e-05 actually comes from. The falsified claim stays on the books per standing policy. The row now reads `ERROR` in the cross-check because a prose-led description has no evaluable expression — a lesser defect than the one it replaced, and one of the 89 unevaluable descriptions in §2 of the register |
| 5 | `spectral.lambda_max` | derive the normalisation or relabel `80.5` CALIBRATED | **PARTIAL** — `80.5` is now explicitly labelled CALIBRATED (fitted to the residue count in `run()`, not derived from b₃), and the ratio is documented in the description. The 0.124% residual against an exact 1e15 is **still unexplained**, so this row remains the one open `DISAGREE_SCALE` and should still not be read as a check of anything |

The methodological note below is unchanged and, if anything, strengthened:
row 4's fix was to *label* the elegant claim dead, not to make it agree.
