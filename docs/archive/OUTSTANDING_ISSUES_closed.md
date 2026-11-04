# Outstanding issues - closed/resolved (archived verbatim from OUTSTANDING_ISSUES.md)

## Tier 1 — Open physics problems  (subsection moved from OUTSTANDING_ISSUES.md)

### 1.6c The global fit was a literal, and four other numbers were too — ✅ CLOSED 2026-09-01
`statistical_rigor_validator` read `summary.get("global_chi_squared", 0.23)`
from a report whose summary block has never carried that key, so the 0.23
default — a value carried over from v23.9 — fired on **every** run, together
with a `degrees_of_freedom` default of 25. The p-value, the EDOF comparison
and the headline verdict were all computed from those two literals rather
than from the 136 rows in the same file. Three further faults compounded it:

* with the file **absent** it set the same literals, set the row list to
  empty, and still published a full report including "Full Independence:
  True" — a complete statistical analysis of no data;
* the p-value **tail** was chosen from the data but **interpreted** from the
  `use_lower_tail` flag, so an upper-tail p ≈ 0 was reported as "TOO_GOOD
  (suspiciously perfect fit)" — the conclusion inverted;
* `recalculate_with_theory_uncertainty` summed only `PASS` and `MARGINAL`
  rows, measuring fit quality over exactly the rows that already agreed.

Same code, same file, now: **χ² = 126,677 over 64 scoring rows, p = 0,
POOR_FIT**. `UNBOUNDED` rows are excluded — `gauge.M_GUT_GEOMETRIC` compares
2.1e16 GeV against 1.67e34, a proton *lifetime*, and contributed 3.4e38 by
itself. The three `algebra.gaugino_cabibbo_*` rows are 95.4% of what remains;
they are now labelled FALSIFIED, and the fit is published both with and
without the withdrawn candidates rather than either being chosen silently.
Excluding them does not rescue it: reduced χ² is still 96.9.

**Still open:** the EDOF = 3 ansatz and the `np.random` Jacobian remain
scaffolds, and say so in `scaffold_notes`. Read `chi_squared_from_rows`,
which depends on neither.

## Tier 1 — Open physics problems  (subsection moved from OUTSTANDING_ISSUES.md)

### 1.6d Twenty statuses were being upgraded at export — ✅ CLOSED 2026-09-01
The export whitelist preserved seven status names and rewrote everything
else to `DERIVED`. An AST walk over every `Parameter(status=...)` literal
found **27 declared, 7 surviving** — and the rewrite always ran in the same
direction, because DERIVED is stronger than nearly all of them. `FITTED` (19
parameters), `ANSATZ` (7, including `gauge.su2_sin2_theta_W` and
`gauge.su3_alpha_s_predicted`), `SPECULATIVE` (3), `PLAUSIBLE` (6),
`TOPOLOGY_CANDIDATE` and `RETRODICTED_VARIANT` all shipped as derivations.
`FALSIFIED` and `MEASURED` were each found separately and are the same bug.

This subsumes §1.3's `wa_thawing` concern: the framework had already labelled
it `FITTED` — its own description reads "dim(Psi)=4 multiplier introduced
post-hoc" — and the export was overwriting that label. 21 statuses now ship
where 7 did; DERIVED falls 338 → 275.

## Tier 1 — Open physics problems  (subsection moved from OUTSTANDING_ISSUES.md)

### 1.6e Twenty anchors claimed to be tuning-free consequences of b₃ — ✅ CLOSED 2026-09-01
`geometric_anchors.py` registered every anchor `GEOMETRIC` with
`"fundamental": True` and `"tuning_free": True`, without exception. Twenty
are raw experimental input: the three NuFIT mixing angles, the SH0ES H₀, the
Planck matter density, the DESI w₀/wₐ, the PDG Wolfenstein A and Jarlskog,
and two openly phenomenological fit values.

The correct classification **already existed** — a `measured_params` set with
a docstring explaining exactly this distinction — inside a method named
`register_to_registry` that is not defined on the class and is called from
nowhere. The whole block was dead code; the right answer sat in the
repository and never ran.

`geometry.theta_13` is the sharpest case and settles §1.1's cross-check
question: the producer returns a hardcoded `8.54` whose own comment reads
`8.54 deg (NuFIT)`, and its `eml_description` is the bare literal
`eml_scalar(8.54)`. It is the anchor restated, so it is **deliberately left
unscored** — binding it would publish a ~0σ PASS measuring nothing. The
register's "0.4σ cross-check" claim is withdrawn.

`particle.theta_13_deg` **is** a derivation and is now scored for the first
time: **0.805σ PASS** against NuFIT 6.0 8.58 ± 0.11, confirming the prose
"0.8σ" as a computed row. `geometry.sum_m_nu` clears the 0.12 eV bound with
32% margin. Scored rows 172 → 174.

## Tier 1 — Open physics problems  (subsection moved from OUTSTANDING_ISSUES.md)

### 1.6f Ambiguous bare names let a prediction agree with its own anchor — ✅ CLOSED 2026-09-02
`_build_context` gave EML expressions three ways to name a parameter: full
path, last two components, or the bare last component. The bare form used
`setdefault`, so where several parameters shared a last component the **first
encountered won** — silently, in dictionary insertion order.

Twenty-four names collide, and they are mostly a *prediction against its own
anchor*:

| bare name | one meaning | the other |
|---|---|---|
| `theta_13` | NuFIT 8.58 | geometry 8.54 |
| `theta_23` | NuFIT 42.2 | geometry 49 |
| `sin2_theta_W` | PDG 0.23122 | geometry 0.231905 |
| `wa` | DESI −0.86 | geometry −0.204 |
| `M_PLANCK` | reduced 2.435e18 | full 1.22089e19 |

An `eml_description` written against `theta_13` evaluated against whichever
came first. Bound to the anchor, a prediction was compared with the very
measurement it exists to predict, and agreed trivially — the fake-pass
pattern reached by dict ordering rather than by any decision. The `M_PLANCK`
pair is the √8π confusion behind a 97.65σ error this repo already corrected
once.

A short alias is now bound only when every parameter claiming it agrees.
Otherwise it stays unbound and the expression must qualify it, turning a
silent wrong answer into a visible unbound-name error. The 24 refused names
ship in `eml_crosscheck.json` as `ambiguous_short_names`.

**The cost is real and is the point:** 35 rows moved out of AGREE, DISAGREE
fell 62 → 52 (ten were disagreeing *because* they had bound the wrong
value), and the strict rate went 0.79 → 0.683. Those agreements rested on an
arbitrary choice.

## Tier 1 — Open physics problems  (subsection moved from OUTSTANDING_ISSUES.md)

### 1.6g Two more silent gaps in the artifact layer — ✅ CLOSED 2026-09-02; 12 further phantoms resolved 2026-09-04
**207 declared dependencies do not exist.** 122 formulas declare
`input_params` and 128 declare `output_params` naming no registry parameter.
The walker's `producer_of` simply has no entry, so the edge is invisible and
`b3_rooted_count` (366 of 422) was measured over partly fictional chains.
`topology.euler_chi` appears 20 times, `cosmology.H0_geometric` 11,
`topology.vol_v7` 10. Now published as `declared_paths_that_do_not_exist`; a
scheduled pass has since resolved 90 of them, leaving 117 —
reported, not repaired, since create-the-path vs drop-the-declaration is a
per-formula question.


**2026-09-04:** 12 additional phantom paths resolved by replacing with
real registry counterparts or dropping declarations with no registry match:
`topology.nitzotzin_roots` → `topology.ancestral_roots` (5 formula inputs),
`topology.barbelo_modulus` → `topology.hidden_supports` (1 input + 1 FormulasRegistry pm_path),
`topology.demiurgic_Yetts` → dropped (no registry counterpart; pm_path removed from FormulasRegistry),
`topology.logos_joint` → dropped (no registry counterpart),
`topology.euler_chi` → `topology.mephorash_chi` (18 formula inputs across 7 paper modules),
`cosmology.H0_late` → `cosmology.H0_late_evolved` (1 input),
`certificates.tier1/2/3_status` → dropped (CertificateStack never registers these),
`topology.sophian_modulus` → `registry.node_count` (3 inputs + 1 FormulasRegistry pm_path),
`established.c` → `cosmology.speed_of_light_derived` (1 input),
`constants.D_crit` → `topology.critical_dim` (1 input).
The `dependency_chains.json` artifact still shows 117 because regenerating it requires
`pip install metaphysica[sims]`; the code-level count is now ≈105.

**`derivation_formula` was declared 315× and exported 0×.**
`register_outputs` read every other field off the parameter definition and
passed this one over, so nothing could link a parameter to the formula
producing it. Now carried through metadata like `eml_description`: 195
parameters name 114 formulas, with exactly one dangling id
(`odowd-h0-composite`) pinned by a test.

## Tier 1 — Open physics problems  (subsection moved from OUTSTANDING_ISSUES.md)

### 1.6h Two citations pointed at the wrong document — ✅ CLOSED 2026-09-04
An identifier can be unique, well-formed, resolvable — and wrong. Verified
against Crossref:

| entry | carried | actually resolves to |
|---|---|---|
| `penrose-2004` "The Road to Reality" (2004) | `10.1038/nphys344` | *Direct force measurements on DNA in a solid-state nanopore*, Nature Physics **2** (2006) — a journal that did not exist in 2004 |
| `weinberg-1972` "Gravitation and Cosmology" (1972) | `10.1002/piuz.19740050511` | *Preise für Jahres‑Abonnement 1975*, Physik in unserer Zeit **5** (1974) — a subscription price list |

A reader following the Penrose citation arrived at a DNA nanopore
experiment.

**Every check passed.** `every_reference_is_identifiable` — both *have* an
identifier. `no_conflicting_identifiers` — it looks for one id claimed by
entries of different years, and each of these was claimed once; **an id can
be wrong without being shared**. `no_duplicate_titles` — each book had a
second, correctly-identified entry, but under its full subtitle, so strict
normalisation saw two different works.

Both DOIs are replaced with identifiers their correctly-formed twins already
carried (ISBN + OpenLibrary for Penrose, the Wiley URL for Weinberg) — SSOT
respected, nothing invented.

A new **`no_near_duplicate_titles` ADVISORY** closes the detection route:
titles agreeing once a subtitle is dropped, in the same year. Deliberately
*not* a gate — a looser key would collapse the seven deliberate PDG
per-section citations, the distinct CODATA 2014/2018/2022 releases, and two
genuinely different Acharya G₂-MSSM papers, and merging those is a worse
error than the duplicate. It surfaces 14 entries in 5 groups for human
decision. The strict gates are untouched and a test asserts they still pass,
so the advisory was not bought by weakening them.

**Bibliography status:** all four gates PASS — 180 references, 0 duplicate
titles, 0 identifier conflicts, 0 orphans — with 5 near-duplicate groups
outstanding as advisories.


## Tier 1 — Open physics problems  (subsection moved from OUTSTANDING_ISSUES.md)

### 1.8 The bridge-to-channel join — ✅ **CLOSED 2026-09-01**, and it derives two things that were inputs
The register listed "nothing maps a bridge index to a G₂ coordinate pair" as
the load-bearing geometric gap. The two structures turn out to have identical
shape: each coupling triangle is indexed by an omitted Fano point and its
three vertices are the three lines through that point, so a maximal placement
is 4 points × 3 lines = 12 slots against 4 faces × 3 bridges = 12.

Adding **one stated assumption** — that the E₈ block a bridge carries is a
property of the *channel* rather than of the face observing it, i.e. one
global labelling of the 7 Fano lines by 3 blocks shared by every face — and
enumerating all 3⁷ = 2187 labellings yields two results that were previously
put in by hand:

| was | now |
|---|---|
| `n_faces = 4` read off h^{1,1} = 4 of the TCS #187 building block, which `four_face_structure` itself classifies FITTED | **4 is the maximum.** No labelling makes 5, 6 or 7 points simultaneously rainbow. |
| `face_genericity` narrowed 35 → 7 by fiat; the fork read OPEN with "NOT derived — nothing in the framework forbids collinear labels" | **The 28 line-containing 4-point sets admit zero labellings**; each of the 7 arcs admits 18. Genericity is a consequence. Fork OPEN → RULED. |

**And the assignment is unique up to symmetry** (added 2026-09-02). The
7 × 18 = 126 remaining possibilities are *all* relabellings, so nothing
physical is left undetermined:

1. **The block partition is canonical given the arc.** Each K₄ edge {p,q}
   spans a Fano line, and that line meets the arc's complement line in
   exactly one point. Grouping the six edges by which complement point they
   hit gives fibres that are precisely the three perfect matchings of K₄.
   The 3! is therefore only *which complement point is called block 0*.
2. **The spare factor of 3 touches nothing** — it is the colour of the
   complement line, which lies on no face and is incident to no bridge.
3. **The seven arcs are one orbit.** Aut(Fano) = PSL(3,2) has order 168, is
   transitive on the 7 arcs, and the arc stabiliser of order 168/7 = 24 acts
   as the *full* S₄ on that arc's four faces. No arc is singled out by the
   incidence geometry, and the face labels are free too.

The structure closes as **K₄ on the four faces**: 4 faces ↔ vertices,
6 channel-lines ↔ edges, **12 bridges ↔ the 12 directed edges** (ordered
pairs of faces — so "bridge" is literal, and 12 is K₄'s directed-edge count
rather than a separate input), 3 E₈ blocks ↔ the 3 perfect matchings, and
one spare line incident to no face. The 18 is then 3! proper 3-edge-colourings
× 3 free colours for the complement line.

**Kill conditions.** Any 5-point rainbow set, or any line-containing 4-set
admitting a labelling, retracts the respective half of the derivation. The
uniqueness is *conditional* on nothing elsewhere in the framework
distinguishing a Fano direction: a preferred imaginary octonion, or a shadow
asymmetry singling out a coordinate, breaks PSL(3,2) and makes the arc
choice physical again. The global-labelling premise remains an input and is
flagged as such wherever the result is quoted.

Two further pieces of arbitrariness dissolved rather than being resolved.
The **576** cross-E₈-valid groupings form a single *regular* orbit under
S₄ × S₄ renaming bridges inside E₈ blocks, so stride-4 is a coordinate
convention, not a fitted choice — one leg of the FITTED classification is
answered (h^{1,1} = 4 from TCS #187 and the imposed cross-E₈ property are
not). And **n_gen = 3** is fixed twice over — Leech 24 = 8+8+8, and q+1 = 3
lines through every point of the order-2 projective plane — rather than
being 12/4 arithmetic on two numbers taken from the manifold.

Two supporting claims were also converted from prose to code. The
"15400 total groupings, 576 cross-E₈-valid" figures behind the FITTED
classification of the face grouping had no implementation; both now come
from an enumeration agreeing with closed forms 12!/((3!)⁴4!) and (4!)².
And the stride-4 vs contiguous conflict is settled: they are **different
objects**, since the contiguous grouping's first face lies entirely inside
one E₈ block. The 576 form a single **regular** orbit under S₄ × S₄ renaming
bridges inside E₈ blocks, so stride-4 {i, i+4, i+8} is a coordinate
convention, not a fitted selection among rivals.

## Tier 1 — Open physics problems  (subsection moved from OUTSTANDING_ISSUES.md)

### 1.9 `compute_leakage_from_lattice` did not do what it said — ✅ CLOSED 2026-09-01
Its docstring claimed the leakage coupling was "derived from the actual
stabilized moduli rather than hardcoding ratio=6.0" and was "NOT hardcoded
but verified from the moduli". It computed the four face volumes from
`bridge_moduli`, **discarded them**, and returned `1/sqrt(n_bridges // 2)` —
a function of the bridge *count* alone, identical for any moduli whatsoever.
The topological derivation (n_aligned = n_pairs/2 = χ_eff/b₃ = 6) is
defensible and is kept; the provenance claim is withdrawn, and the volumes
are now load-bearing as a check that can fail.

## Tier 1 — Open physics problems  (subsection moved from OUTSTANDING_ISSUES.md)

### 1.11 Cross-shadow coupling — RESOLVED affirmatively, at a stated scope
_(new 2026-08-26; `AutoGenerated/topological_flux.json`)_

The bridge sector had **no** cross-shadow interaction: the one metric
channel that could carry one (off-diagonal ∝ L₁L₂cos θ) is identically
zero at the stabilised vacuum, which sits at θ = 90° exactly on all 12
bridge pairs — the reason `reflection_positivity_gate` reports
MARGINAL_VACUOUS rather than PASS. The topological route was proposed to
carry the coupling instead. **It does.** Evaluated at the stabilised
vacuum, ∫ φ ∧ F_A ∧ F_B = **5.6476e+02**, and it is *maximal* there,
where the metric channel reads 2.1e−30. The two channels are exactly
complementary (area L₁L₂sin θ vs metric L₁L₂cos θ).

Three independent checks back it: two routes sharing no code (the ε
contraction and ⟨∗φ, F_A∧F_B⟩) agree to relative 6e−16; the selection
rule is exact by enumeration — **42 of 210** disjoint channels survive,
non-zero iff the complementary triple is associative; and forbidden
channels are *structurally* zero (0.0, not 1e−15).

**Scope, asserted by test:** flat ℝ⁷ with constant coefficients, so this
is coefficient × volume — a number, **not a topological invariant**.
It establishes that the integrand is non-vanishing, which is what the
interaction sector needed to exist at all. Topological content requires
harmonic representatives on a compact G₂ manifold with b₃ = 24 (deferred
DEC work). **Kill condition on record:** if the bridge-to-channel
assignment, once derived, places the physical bridges only on
non-associative complements, every physical channel is forbidden and this
route dies — the rule permits 42 of 210, so it can rule the configuration
out.

**Assignment narrowed (2026-08-30, `docs/BRIDGE_CHANNEL_ASSIGNMENT.md`).**
The 21 unordered allowed couplings on the 21 coordinate pairs form a
**2-regular graph — seven disjoint triangles**, one per coordinate *k*,
whose three vertices are a perfect matching of the other six points and
whose three edges are the three Fano lines through *k*. The selection rule
is the Fano incidence of φ's associative triples, not a filter.

Over **all C(21,12) = 293,930** placements of the twelve bridges the live
coupling count runs **5 to 12 and is never zero**, with the maximum 12
reached by exactly **35 = C(7,4)** placements — those taking four complete
triangles. The framework independently carries **four faces of three
bridges**, and `four_face_structure` records that its 4×3 grouping is
*"one of 576, NOT unique by cross-E₈ alone"*. **Each face is a triangle**,
which supplied the missing independent criterion.

**Superseded 2026-09-01 — see §1.8.** What was a proposal here (with a stated
falsifier, and "four faces from b₂ = 4" as its input) is now closed: adding the
single stated assumption that the E₈ block is a property of the channel makes
n_faces = 4 the *maximum* rather than a reading of h^{1,1}, makes genericity a
consequence rather than a criterion, and closes the whole structure as K₄ on
the four faces — 12 bridges = 12 directed edges, 3 E₈ blocks = 3 perfect
matchings. Read §1.8 and `docs/BRIDGE_CHANNEL_ASSIGNMENT.md` for the current
statement; this paragraph is kept because it records what the claim was before
the join, and the falsifier it stated is the one that was met.

⚠ **Correction to this entry's own earlier kill condition.** It previously
read "if the bridges sit only on non-associative complements every channel
is forbidden and the route is dead". That event **cannot occur** (minimum
5, never 0), so it was an unfalsifiable guard — the defect this register
exists to catch, committed here. Retired in the artifact as
`kill_condition_retired` and replaced. The correction *strengthens* the
result: cross-shadow coupling is not merely non-zero at the vacuum, it is
**structurally unavoidable**.

**Still underived:** which four of the seven points the faces choose — though
§1.8 now shows the seven choices form a single PSL(3,2) orbit, so they are
physically equivalent unless something else in the framework distinguishes a
Fano direction — and, blocking the Path A vs Path B canonical-term ruling, any
3-form on the 13D shadow. Path A
(∫₁₃ C₃ ∧ G₄ ∧ G₄ ∧ F₂, G₄ = dC₃) is degree-valid and computable the
moment C₃ exists, but the framework derives φ only on the 7D cycle; the
13D side carries scalars. Evaluating it would mean inventing an ansatz,
so it is recorded BLOCKED_ON_UNDERIVED_INPUT rather than fabricated.

---

## Tier 2 — Framework and SSOT hygiene  (subsection moved from OUTSTANDING_ISSUES.md)

### 2.1 7 of 72 gates remain declarative — G19/G25/G26/G39/G56/G59/G67 ✅ CLOSED 2026-09-03
32 COMPUTED_PASS, **2 COMPUTED_FAIL (G12 + the G72 seal reporting it)**,
7 DECLARATIVE, 31 with no evaluation record. The seven Strategy-A gates
(G01, G13, G17, G22, G23, G29, G40) were promoted via a semantic tier;
the R6/R7 rulings added G32 (semantic: sin²θ_W = 3/8 exact at GUT) and
G36 (registry: framework first-row sum vs PDG 0.9985 ± 0.0007, two-sided,
Cabibbo-anomaly-live), and converted G12 with the PDG uncertainty and no
theory buffer — it reads **COMPUTED_FAIL at ~17σ** until a cited theory
uncertainty exists, and the G72 seal honestly aggregates that failure
(`failed_gates: [12]`). An honest FAIL outranks a declarative shrug.
G19/G25/G26/G39/G56/G59/G67 were converted from DECLARATIVE to COMPUTED
this session using live registry evaluation — computed_pass now 32 (was 25).

## Tier 2 — Framework and SSOT hygiene  (subsection moved from OUTSTANDING_ISSUES.md)

### 2.6a The dashboard contradicted the gates — ✅ CLOSED 2026-09-01
`improvement_scorecard.json` published "42/42 testable gates LOCKED (100.0%
complete), open_gate_ids: []" with G12 among the locked ids, while
`evaluation_summary` in the same directory reported G12 COMPUTED_FAIL at
17.1σ and the G72 seal failing on it. The generator read
`verification_status` — what a certificate *asserts* about itself — and never
looked at `evaluation_status`, which records what happened when the gate was
executed. A gate could be VERIFIED and COMPUTED_FAIL at once, and the
dashboard showed the first.

Now **32 COMPUTED_PASS, 2 COMPUTED_FAIL, open ['12', '72']**, with 7 DECLARATIVE
(no executable form) and 31 with no evaluation record counted separately so a
computed-pass rate is not mistaken for gate completion. The `summary` block is a
legitimate declarative tally and now says so. G19/G25/G26/G39/G56/G59/G67 were
subsequently converted (✅ CLOSED 2026-09-03), reducing DECLARATIVE 14 → 7.

## Tier 2 — Framework and SSOT hygiene  (subsection moved from OUTSTANDING_ISSUES.md)

### 2.6 Terminology audit — ✅ CLOSED this session (0 flags)
The auditor was under-powered *and* its own guidance was stale: it
advised "26D = 24 + 1 + 2" (the pre-two-time accounting) and had no rule
for `27D` or "unified time". After adding those rules it surfaced **173
genuine stale references** that every previous sweep had missed —
142 "unified time", 17 `25D`, 14 `27D` — because earlier passes searched
for signatures like `(24,1)` rather than the prose phrasing. All cleared;
a Jordan/exceptional-algebra exemption was added so `dim J₃(𝕆) = 27` is
never flagged, plus history-marker exemptions. Audit now reads
**0 flags / CONSISTENT**.

## 2026-08-20 update — literature review + evidential audit  (subsection moved from OUTSTANDING_ISSUES.md)

### θ₁₃ ruled NOT_PREDICTED (§1.1 resolved, negatively)
A 6243-form enumeration over the framework's own seeds put **143 candidates inside
the 1σ window with ~53 expected by chance** — no excess. An independent literature
sweep found **18 framework-native expressions** within 1σ (π/(144−3), φ/(72+1),
1/(72−27), …) plus 13 simple rationals. θ₁₃ is one O(0.15) number known to 1.3%;
this integer inventory hits it by construction, so *any* relation adopted would
have ~18 equally good siblings and carries no predictive content. No published
mechanism yields 8.57° without fitting, and modular flavour symmetry is obstructed
anyway: it needs SL(2,ℤ) on a **complex** modulus, while G₂ moduli are **real**.
Quark-lepton complementarity is falsified (9.155°, +5.3σ).

## 2026-09-05 (second pass) — three open problems closed from the literature

Counters held at zero throughout (phantom 0, silent defaults 0, EML strict 1.0,
580 AGREE). 1710 tests pass. Three Tier 1 items move, and one silent artifact
bug was found while doing it.

### C1. Vol(X₇) is derivable — the placeholder is retired (closes part of 1.6g / the G₂-volume gap)

The G₂ volume was a 1.0 placeholder declared by ten formulas across five
modules. It is not unknown: **standard M-theory on a G₂ manifold determines
it from α_GUT**, and the relations are textbook (Friedmann & Witten
[hep-th/0211269](https://arxiv.org/abs/hep-th/0211269); Acharya–Kane–Kumar,
[arXiv:1204.2795](https://arxiv.org/abs/1204.2795)):

- Non-abelian gauge fields localise on three-cycles, and the coupling **is**
  the cycle volume: `4π/g² = 1/α = Vol(Q)`. So
  **`geometry.associative_3cycle_volume` = 1/α_GUT = 24.3** — the path the
  SU(3) reduction declared and no registry held.
- Vol(X₇) is homogeneous of degree 7/3 in the moduli, so
  **`topology.vol_v7` = α_GUT^(−7/3) = 1710.3** in eleven-dimensional Planck
  units.

**The check that could have failed.** Eliminating M₁₁ between
`M_GUT ~ M₁₁ α^(1/3)` and `M_Pl² ~ V₇ M₁₁²` predicts the reduced Planck mass
from α_GUT and M_GUT alone — both registered independently of it:

    M_Pl ~ M_GUT · α_GUT^(−1/3) · √V₇  =  2.516e18 GeV
    registered geometry.M_star          =  2.435e18 GeV
    validation.mpl_from_gut_ratio       =  1.0330   (3.3%)

on a relation carrying dropped order-one factors. This is the framework's
first Planck-mass statement with content: `geometry.m_planck_4d` is the
reduced mass times √(8π), a unit conversion whose 0.26σ PASS is an identity.

Consequence: `validation.phi_g2` = Vol(X₇)·χ/b₃ moves **6 → 10262**. The old
6 was χ/b₃ with an invisible factor of one.

This does **not** rescue `holonomy-volume-constraint`, whose own two steps
disagree (its H₀ bridge inverts to exponent 2, the next step asserts 7) and
which gives ~10¹⁸³. That formula is superseded, not repaired.

### C2. wₐ is not free — thawing forces a band (closes 1.3)

Register 1.3 recorded wₐ = −1/√b₃ as "admitted leading-order" with no
derivation. There is one, and it is a published criterion, not new physics.
**Caldwell & Linder (2005), "The Limits of Quintessence"**
([astro-ph/0505494](https://arxiv.org/abs/astro-ph/0505494)) show thawing
models occupy a narrow wedge of the w–w′ plane, `(1+w) ≤ w′ ≤ 3(1+w)`
(confirmed independently in
[MNRAS 420, 1309](https://academic.oup.com/mnras/article/420/2/1309/984332),
which attributes it to Caldwell & Linder and calls it the LC bound). In CPL,
w′ at a = 1 is exactly −wₐ, so

    (1 + w₀) ≤ −wₐ ≤ 3(1 + w₀)

This framework's w₀ = −(b₃−1)/b₃ gives **1 + w₀ = 1/b₃ exactly**, so the wedge
collapses to a pure statement about b₃:

    wₐ ∈ [ −3/b₃, −1/b₃ ] = [−0.125, −0.0417]

That is zero-parameter and derived. **The registered wₐ is outside it.**
−1/√b₃ = −0.2041 exceeds the upper limit by 1.63×; the retired −4/√b₃ =
−0.8165 misses by 6.5×; wₐ = 0 fails the other end. The module named
*thawing*, which registers `cosmology.wa_thawing`, does not satisfy the
published definition of thawing.

**Recorded, not repaired, and deliberately so:** every point in the band is
*further* from DESI DR2 (−0.86 ± 0.22) than the present value — 3.34σ at the
band edge −3/b₃ against 2.98σ now. Deriving wₐ correctly makes the tension
worse, which is exactly why the choice must not be made to improve a number.
Now registered as `cosmology.wa_thawing_band_min` / `_max` /
`cosmology.wa_in_thawing_band` (= 0).

### C3. The S₈ friction onset cannot be a modulus (closes the open problem in 1.4)

Register 1.4 asked for the friction onset to be derived, noting only
z ≈ 3–4 recovers a weak-lensing-friendly S₈. The onset condition is standard:
a field frozen by Hubble friction rolls when `3H(z) = m_φ`. Run it backwards:

| field mass | z at which it starts oscillating |
|---|---|
| 1 TeV (light SUSY modulus) | ~3 × 10²² |
| 30 TeV (BBN-safe floor) | ~2 × 10²³ |
| needed for S₈ (z ≈ 3–4) | m ≈ 2–3 × 10⁻³² eV ≈ 15 H₀ |

A string modulus starts oscillating **twenty-two orders of magnitude** before
the window S₈ needs. The field that switches on at z ≈ 3–5 has a
quintessence mass, not a modulus mass. This is consistent with
`moduli_dm_coupling.py`'s own numerical verdict that multiplying the moduli
coupling by 8 moves S₈ by 0.2% — **the moduli coupling was never the relevant
knob**, which is why no amount of tuning it worked.

**And the framework already has the right field.** Applying the same onset
condition at the registered `cosmology.z_thaw` = √b₃ = 4.899 gives

    m_φ / H₀ = 3 E(√b₃) = 24.25   =   b₃ to 1.05%

So `z_thaw = √b₃` and `m_φ = b₃·H₀` are the same statement, and the second is
the physical one — falsifiable, in natural units, comparable across sectors.
Registered as `cosmology.m_phi_over_H0`. If the S₈ suppression is real, the
field responsible is the dark energy scalar and the two sectors are one
sector. Wiring S₈ to it is a physics ruling and is not taken here.

### C4. b₃ = 24 is incompatible with a twisted connected sum, and that is fine

The register's stated obstruction — "Crowley–Nordström forces b₂ + b₃ odd for
any TCS" — is not what the literature says, and the actual constraint is
different and sharper. Crowley–Nordström's ν is a **Z/48 invariant** defined
from the signature and Euler characteristic of a Spin(7) coboundary, and for
**every** TCS G₂-manifold ν = 24
([1211.0269](https://arxiv.org/abs/1211.0269),
[Nordström's survey](https://sites.duke.edu/scshgap/files/2016/09/nordstrom_v3.pdf)).
It says nothing about b₂ + b₃ parity.

What *does* bite: TCS manifolds built from pairs of Fano 3-folds satisfy
**71 ≤ b₃ ≤ 155**. b₃ = 24 is far below that floor, so the framework's b₃
cannot come from that construction at all — a cleaner exclusion than the
parity claim.

The escape is already in the literature and already half-recorded here.
Joyce's orbifold resolutions of T⁷/Γ span **b₂ ∈ [0, 28] and b₃ ∈ [4, 215]**,
with 252 distinct (b₂, b₃) pairs among simply-connected examples
([1810.12659](https://arxiv.org/abs/1810.12659)), and Joyce examples can have
odd ν where TCS cannot. **(b₂, b₃) = (4, 24) lies inside the Joyce ranges.**

→ **Action for the author:** the framework should drop the TCS framing and
state Joyce orbifold resolution as the construction. The parity claim in
Tier 1/Phase 6 should be corrected to the b₃ ≥ 71 exclusion, which is the
real one. This does not by itself exhibit a manifold with (4, 24) — the
ranges being compatible is necessary, not sufficient — so the item stays open,
but it is open for a different and much narrower reason than recorded.

### C5. A progress message was deleting fourteen parameters

Found while checking C1. `registry.py`'s v25/v26 module loaders print
`[OK] <module>: <keys>` after each load. On a cp1252 console a parameter key
containing a non-ASCII character raised `UnicodeEncodeError` **inside that
print**; the exception escaped `_try`, escaped `load_v26_modules`, and hit the
caller's `except Exception`, which reported it as *"v26.0 module loading
failed"* — silently dropping the four modules after it and fourteen registry
parameters, the whole `cosmological_tensions` block among them
(`S8_baseline`, `S8_resolved`, `H0_baseline_km_s_Mpc`,
`S8_tension_remaining_sigma`, `H0_tension_remaining_sigma`).

The build happened to run under a UTF-8 stream and carried them; a bare
`run_all_simulations` did not. **The two artifact copies silently disagreed by
fourteen parameters** — 731 against 745 — and nothing compared them. Progress
output now degrades to a readable approximation instead of propagating.

---

## 2026-09-06 (third pass) — nine simulations had never run, and Route 1 is settled

### D1. Route 1 closed: the quintessence field cannot be a Kähler modulus

The `dark_energy_betti` fork moves **OPEN → RULED**, and it is ruled in favour
of the option that fits *worse*.

The framework's own racetrack fixes the answer with no new input. It sets
`a_i = iπ/b₃` and `T_i = b₃·k_gimel/(iπ)`, so

    a_i · T_i = k_gimel        for EVERY face

— the 1/i hierarchy cancels exactly, which is the real content of the
construction: all four condensates are equally suppressed. That combination is
precisely what sets the modulus mass in KKLT-type stabilisation
([Choi et al, hep-th/0503216](https://arxiv.org/abs/hep-th/0503216)):

    m_T = 2 (a T) m_{3/2} = 2 k_gimel m_{3/2}

With this framework's own gravitino mass, `susy.m_3_2_GeV` = 1 TeV, that is
**24.6 TeV**. A rolling dark-energy field needs `m_φ = b₃H₀` = 3.5e-32 eV. The
gap is **7.1e44 — forty-five orders of magnitude**, now published as
`geometry.kahler_over_quintessence_mass`.

So b₂ = 4 is ruled out as the origin of w₀ **despite fitting thirteen times
better** (0.25σ against 3.2σ in the 2D plane). A field stabilised at 24.6 TeV
cannot be rolling today. The quintessence direction must be shift-symmetry
protected — a C₃ axion, counted by b₃ — which is the adopted option.

The same argument independently settles the S₈ friction onset, and both are
*computed* rather than asserted: if the gravitino mass or the racetrack
changes, the ruling moves with them.

**What it costs.** The surviving option is the one at 3.2–3.5σ from DESI DR2.
Ruling on physics rather than on fit means accepting the worse number, and the
tension is now structural rather than a matter of choosing differently. And
the caution survives the ruling: the DR2 central wₐ = −0.86 lies outside the
Caldwell–Linder thawing wedge for **every** n ≥ 4, so the remaining question
is not which integer but whether the sector is thawing at all.

Incidentally, `k_gimel = 12 + 1/π` **exactly** (12.318309886183791), which is
what makes `a·T` come out as a clean constant.

### D2. Nine simulation modules had never run

Each is imported as `try: from X import Y / except ImportError: FLAG = False`,
which cannot distinguish "module absent" from "class name misspelled". Nine
asked for a class with a `V19` suffix the module never defined:

    lagrangian_master, gauge_sector_complete, matter_sector_complete,
    cosmology_sector_complete, and appendices M, N, O, P, Q

The run summary reported **"85 simulations, all passed"** the entire time. The
absence surfaced only indirectly: `g2_holonomy.b2` was missing from the
registry while `topology.b2 = 4` sat beside it.

Reviving them: **422 → 569 formulas, 746 → 807 parameters, 180 → 204 scored
rows** (PASS 47→56, FAIL 14→16, MARGINAL 13→15, TENSION 6→7). b₃-rooted
350 → 381.

Three then failed on `required_inputs` naming paths that exist nowhere —
`constants.M_STAR`, `gauge.alpha_gut`, `geometry.sophian_modulus`,
`geometry.barbelo_modulus`. That is the same phantom class the formula audit
tracks, but `required_inputs` is not walked by it, so they could rot
indefinitely while the module was disabled. `tests/test_no_simulation_is_
silently_disabled.py` now checks both.

They also brought 21 phantom paths and 19 malformed EML expressions with them,
all now cleared: phantom **0**, silent defaults **0**, EML strict **1.0** over
603 rows.

### D3. `b₂ = 0` was a false theorem

`appendix_p_g2_holonomy` hardcoded `b2 = 0` with the comment *"For G2 holonomy
manifolds: b2 = 0 (no harmonic 2-forms)"*, and a `__main__` assertion pinned
it. That is wrong, and is very likely a confusion with b₁: holonomy exactly G₂
forces a finite fundamental group and hence **b₁ = 0**, but places no
constraint on b₂. H² decomposes under G₂ as 14 ⊕ 7, and Joyce's resolutions
realise b₂ anywhere in [0, 28]. It now reads `topology.b2`, and the assertion
checks agreement with the rest of the framework instead of restating a
non-theorem. This closes the "b₂ = 0 vs b₂ = 4" item — it was never a
contradiction between two claims, just one false one, latent because the
module never ran.

### D4. One parameter, two computations, 79% apart

`cosmology_sector_complete` computes `cosmology.omega_dm_geometric` twice.
`DarkMatterDerivation` registers `sterile_ratio × 0.48 = 0.2717`;
`CosmologicalParametersDerivation` computes `sterile_ratio × Ω_m × 0.85 =
0.152` for the same name, carries the comment *"needs adjustment"*, and is
dead. Nothing compared them. The dead line is kept and labelled rather than
deleted, and the live 0.48 is commented *"From Ω_m/(1 − Ω_DE/2)"* and is not
derived anywhere.

---

## 2026-09-06 (fourth pass) — the SSOT debt the revived modules brought  (subsection moved from OUTSTANDING_ISSUES.md)

### Recorded, not closed: ~50 formulas with no derivation dict

`test_rule_1_formulas` is marked `xfail(strict=True)` with the count and the
cause. This is a marker on a real gap, not a weakened check.

The gap could be closed in minutes by assembling a derivation dict
mechanically from each formula's own `latex` and `description` — and that
would be exactly the **pass-by-construction** pattern this suite exists to
catch: a dict that satisfies the step count while saying nothing. Each needs
writing from what the code actually computes, which is per-formula work
across `gauge_sector_complete`, `matter_sector_complete`,
`cosmology_sector_complete` and `lagrangian_master`.

`strict=True` is deliberate: the moment the deficit is cleared the marker
fails as XPASS and must be removed, so it cannot go stale the way the nine
`V19` entries in `_KNOWN_DEAD` did — those were *recorded* as dead by an
earlier session and sat there while the modules stayed absent. Recording a
defect is not the same as fixing it, and the record should make that
uncomfortable.

---

## 2026-09-06 (sixth pass) — the recorded deficits are now closed

### The xfail is gone, because the gap it recorded is closed

All **57** formulas that lacked a derivation dict, or stopped short of three
steps, now have one: 14 in `gauge_sector_complete`, 16 in
`matter_sector_complete`, 12 in `cosmology_sector_complete`, 15 in
`lagrangian_master`. `test_rule_1_formulas` runs unmarked and passes, and
**all 11 SSOT rules are green with no xfail**.

Every step is drawn from the formula's own declared latex, plain_text,
description and terms. Nothing was auto-generated — which was the point of
recording the deficit rather than filling it mechanically last pass.

**Where a formula does not derive what it claims, the derivation says so.**
That is the part worth reading:

| formula | what the note records |
|---|---|
| `higgs-quartic-from-geometry-v19` | despite the id, **not** derived from geometry — it inverts the measured m_H and v |
| `higgs-mass-from-potential-v19` | circular with the above; one of the two is an input |
| `higgs-vev-minimization-v19` | v = 246 GeV is reproduced, not predicted, because mu is fixed from it |
| `christ-constant-153-v19` | fitted; the 9 is **not** the SU(3) Cartan dimension — rank(SU(3)) = 2 |
| `yukawa-froggatt-nielsen-v19` | the A_f prefactors are fitted O(1) coefficients; only epsilon^Q is geometric |
| `yukawa-epsilon-cabibbo-v19` | a 1% numerical coincidence, not a derivation of either quantity |
| `pmns-from-geometry-v19` | theta_13 has no surviving zero-parameter derivation (R1 ruling) |
| `dm-omega-sterile-ratio-v19` | the 0.48 is undocumented, and a **dead second computation** in the same file gives 0.152 for the same parameter |
| `de-h0-odowd-v19` | theta_mix = 31.0 degrees is fitted |
| `de-hubble-tension-v19` | "Tension Resolved" overstates it — 71.55 is 1.43 sigma from SH0ES |
| `cosmo-baryon-asymmetry-v19` | Re(T) is calibrated to the answer, so eta_b is not zero-parameter |
| `neutrino-mass-hierarchy-v19` | an observational input restated, not a prediction |
| `v22-consciousness-io-gate` | stated hypothesis; no observable is computed from it |
| `su3-confinement-v19` | the sigma ~ 1/Vol proportionality is asserted; no string tension is evaluated |
| `u1-anomaly-cancellation-v19` | follows from the hypercharge assignments; the claim that it "emerges from G2 geometry" is not demonstrated |

### Symbolic trees: four supplied, forty-five principled

Of the 49 formulas carrying no tree in either dialect, **four were genuine
omissions** and now have one — `harmonic-cycle-fraction` (18/24),
`bulk-metric-ratio`, `metric-conversion` and `root-lattice-288` (2·chi_eff),
each verified against its own stated value.

The remaining **45 have no scalar form to supply**, and the floor now records
the classification rather than a bare number:

    15  action / Lagrangian          an integral over a field configuration
     7  reduction over an indexed    products and direct sums over a family
        family
     6  tensor / spinor equation     carries free indices; not a scalar
     3  metric decomposition         ds^2 = ... has no value
    14  other structural             Jordan-27 / E7 / E8 pairings, manifold
                                     structure statements, counting chains

Writing trees for those would mean inventing content. That is a principled
floor, not a backlog.

### And the pattern showed up a third time

Giving `root-lattice-288` a real tree revealed it is **2·chi_eff**, which
never reaches b₃ — it had been counted rooted by the degraded latex scan.
`non_b3` goes 180 → 181 with `b3_rooted` unchanged at 381. Supplying the tree
is what exposes the missing edge, exactly as clearing a phantom path did on
2026-09-04 and as fixing the arithma backend did earlier today.

---

## 4. What is not closed, and why

1. **The factor of 2.** If bridges are (face, block) pairs, 24 = 12×2 needs an
   independent account. The two shadows are the obvious candidate; nothing
   derives it.
2. **The TCS obstruction on (b₂, b₃) = (4, 24).** Crowley–Nordström forces
   b₂ + b₃ **odd** for any twisted connected sum; 4 + 24 = 28 is even, so no
   TCS realises it. b₃ = 24 survives — Joyce 1996 has (7, 24). What fails is
   the pairing with b₂ = 4.

   A reconciliation worth testing, **not** adopted here: **b₂ = 7**, which is
   TCS-admissible (7 + 24 = 31, odd), is realised in Joyce 1996, matches the
   seven Fano points, and decomposes as **7 = 4 + 3 = arc + complement line** —
   exactly the split that produces the 4 faces and the 3 blocks. That would
   make b₂ = 7 the total 2-cycle count and the "four faces" a *sub*-structure
   of it rather than the whole. It also breaks n_gen = 12/4 = 3 as currently
   derived, which would need re-deriving. Recorded as a candidate with its
   cost stated; deciding it requires the author.
3. **Whether any physical claim depends on Leech-specific numbers**
   (196560, packing density). Needs an audit before Approach 4 can be adopted.
4. **A preferred Fano direction.** Nothing supplies one. Approach 6 stays
   open, and must not be closed by assertion.

## 2026-09-08 (eleventh pass) — the racetrack does not stabilise anything  (subsection moved from OUTSTANDING_ISSUES.md)

### 2. The closed form is not a stationary point

Embedding the four face values into the twelve bridges (θ = π/2 so area = T
exactly) and differentiating numerically:

    V at the closed-form point = 1.674e-06
    ||grad V||                 = 4.415e-06        (stationary would be ~0)

So "racetrack-stabilized" describes something the code does not do. The four
face moduli are an **ansatz**, not a stabilisation — the same defect class this
campaign has been removing, sitting in the load-bearing part of the geometry.

## 2026-09-13 (fifteenth pass) — THE GEOMETRY CLOSES: b_3 = 24 is an input  (subsection moved from OUTSTANDING_ISSUES.md)

### What is NOT closed

- **Other constructions.** The refutation is specific to Joyce (Z/2)^3 with the
  forced Gamma. A different G2 construction could in principle give b_3 = 24;
  neither option the framework declares does.
- **Why 24.** If b_3 = 24 is an input, the question becomes what sets it. Both
  candidates from the previous pass remain **NUMERICAL** and unadopted: the arc
  flag identity 24 = 12 x 2, and D4's forced 24 roots.
- **The parity prediction.** Every (Z/2)^3 Joyce orbifold of this type must have
  odd b_3. That is how the calibration gate is discharged here — as a
  **falsifiable prediction** rather than a quoted table. Joyce's published
  Betti numbers can confirm or destroy it, and none is asserted here.

**Status: b_3 = 24 REFUTED as a derivation for both declared constructions.
Recorded as an INPUT. The architectural consequence — presenting b_3 = 24 as a
stated input and retiring the apparatus that no longer earns its place — is a
ruling for the author, and the evidence for it is now positive rather than
circumstantial.**

## 2026-09-13 (fifteenth pass) — THE GEOMETRY CLOSES: b_3 = 24 is an input  (subsection moved from OUTSTANDING_ISSUES.md)

### CLOSED: the eml-math install blocker

`eml-math 2.4.0` is published. Verified from the index -- 2.4.0 is the newest
available -- and `pip install "eml-math>=2.4.0"` resolves on a dry run, so the
pin in metaphysica's pyproject is satisfiable from a clean environment.

The pin was always correct; the package simply had not been released. The
version and `src/eml_math/operators.py`, which metaphysica imports as
`eml_math.operators`, were present in the repository at 2.4.0 throughout. What
was missing was the GitHub Release that triggers the wheel build and the
Trusted-Publishing upload. Tag `v2.4.0` and that release now exist.

Worth keeping on the record, because it is the kind of thing that looks like a
code fault and is not: relaxing the pin to the then-latest 2.3.0 would have made
installation succeed and then fail at import, since that version has no
`operators` module at all. A loud failure at install was the better state to be
in, and the fix was to publish rather than to loosen.

Status: CLOSED. Not a framework defect -- a release that had not been cut.

## 2026-09-15 (nineteenth pass) — SETTLED: b_3 ≡ 7 (mod 12), so b_3 = 24 is unreachable

### The retraction led somewhere better than the claim

The (15, 24) verdict was withdrawn when the stabiliser census showed the A₁
model applied outside its domain. Following that to its cause produced a clean
answer with **no assumption left over** — the opposite of what a retraction
usually yields.

**The classification.** Transverse groups, by how many of σ's 4 moved
coordinates each element flips:

    order 2   flips (4,)                    43,664 components
    order 4   flips (2,2,4)                  4,688 components
    order 8   flips (2,2,2,2,2,2,4)             16 components

Pair the transverse R⁴ into C². Flipping **all 4** acts as −1 ∈ SU(2): that is
A₁, hyperkähler, resolved by Eguchi–Hanson. Flipping exactly **2** is either not
complex-linear, or complex-linear with **det = −1** — outside SU(2) either way,
so no complex orbifold and no hyperkähler ALE resolution. Joyce uses C²/±1
precisely because that is the case that works.

**So admissibility was incomplete.** Pairwise-disjointness is necessary but not
sufficient; every component must also be A₁:

    pairwise-disjoint only      446,964 assignments
    plus every component A₁     411,488 assignments

and the surviving profiles collapse to **(n_T3, n_reflected) ∈ {(0,0), (4,0),
(8,0), (12,0)}**.

**Every reflected family vanishes — because the reflected ones WERE the non-A₁
ones.** That removes the ε-dichotomy assumption entirely: with no reflected
families there is no resolution choice left to assume. The table reduces to its
one unambiguous entry, plain T³ → (1, 3), and

| n_T3 | b₂ | b₃ |
|---|---|---|
| 0 | 0 | 7 |
| 4 | 4 | 19 |
| 8 | 8 | 31 |
| 12 | 12 | **43** |

    b_3 = 7 + 3·n_T3,  n_T3 ∈ {0,4,8,12}  ⇒  b_3 ≡ 7 (mod 12)

**24 ≡ 0 (mod 12), so b₃ = 24 is UNREACHABLE.** (4,24) and (7,24) fall with it:
b₂ = 4 forces b₃ = 19, and b₂ = 7 is unattainable since family counts are
multiples of 4.

### Calibration, unprompted — the A6 gate discharged by computation

**(12, 43) is in the reachable set, and 43 is the b₃ of Joyce's canonical
T⁷/(Z/2)³ example.** The machinery reproduced a published value it was never
given. That is the calibration gate satisfied by derivation rather than by
transcribing a table — and it is why the Joyce ch. 12 citation is no longer the
blocker it was two passes ago.

And the family counts are **multiples of 4 capped at 12** — the 4 faces of an
involution, and 4 × 3 = 12 faces × blocks. The same structure the arc/flag work
derived independently, arriving here from a completely different direction.

### What this closes, and what it costs

b₃ = 24 was already an INPUT (2026-09-14 ruling). This removes its **last
possible geometric home among the declared options**: `fano_tcs` places it far
below its exhibited 71–155 range, and Joyce (Z/2)³ now cannot produce it at all.

So one of these must give:

1. **The seed is not 24.** The nearest reachable value is b₃ = 43 at b₂ = 12 —
   also the canonical Joyce example. Then w₀ = −(b₃−1)/b₃ moves from −0.9583 to
   −0.9767, a ~0.9σ shift against the registry's DESI anchor: real but not
   decisive. What IS decisive is **n_gen = b₃/8**: 43/8 is not an integer, and a
   generation count is a number of things. That is the substance of the ruling.
2. **The manifold is neither declared construction.** Then a third construction
   must be named and its Betti range exhibited, and both existing fork branches
   are wrong.

**Scope, stated not overclaimed.** This refutes b₃ = 24 for Joyce's construction
with hyperkähler ALE resolutions. A different resolution of the non-A₁ components
is not excluded — but it is not Joyce's, carries no G₂ metric guarantee, and
would have to be exhibited rather than assumed.

### Method note

Three passes ago this question needed a library book. It is now settled by
computation, and the route was: mechanism-first (Eguchi–Hanson + Künneth), then
a wrong answer, then following the author's lop-sidedness observation to the
flaw, then the flaw's cause turning out to be a missing admissibility condition
that closes the question outright. Every step that mattered came from asking
what the objects *are*, not what the numbers *match*.

### The 43 path is open as a switch, and the generations relocate rather than break

Following the settled result, both live paths now run. Two new OPEN forks, with
adopted options unchanged so no published number moves:

| fork | adopted | alternative |
|---|---|---|
| `b3_seed` | `seed_24` | `seed_43_joyce` |
| `n_gen_source` | `b3_over_dim_O` | `b2_over_faces` |

| | seed_24 | seed_43_joyce |
|---|---|---|
| b₃ | 24, **INPUT**, origin open | 43, **DERIVED** = 7 flat + 3×12 families |
| b₂ | 4, from a previously FITTED h^{1,1} | 12, **DERIVED**, one 2-class per family |
| Joyce-reachable | **no** | **yes**, and it is the canonical published pair |
| w₀ | −23/24, **0.017σ** | −42/43, **0.94σ** |
| n_gen | b₃/8 = 3 | **b₂/4 = 3** |
| D_bulk − b₃ = 2 | holds | **BROKEN**, gives −17 |

#### The crux was the generation count, and the 43 path answers it

At b₃ = 43 the existing derivation fails: 43/8 = 5.375, and a generation count
is a number of things. That looked fatal. But b₂ = 12 arrives **derived from the
same A1 family count**, and

    n_gen = b₂ / n_faces = 12 / 4 = 3

with n_faces = 4 derived as the moved coordinates of an involution (R2). So the
three generations are not lost — they **relocate**, from b₃ and dim 𝕆 to b₂ and
the faces, with both sides derived. The register notes from earlier passes that
an `n_gen = 12/4` derivation existed and that b₂ = 7 would have cost it; at
b₂ = 12 it is exactly right.

The two forks are therefore **coupled**, and the notes say so rather than
implying independence: b₃/8 fails at 43, and b₂/4 gives 1 at the current b₂ = 4.
Exactly one generation source works per seed.

#### What the 43 path costs, recorded and tested

- **w₀ worsens** from 0.017σ to 0.94σ. A test asserts the 43 path is reported as
  the worse fit — concealing that would be the anchor-shopping this project
  already retired once. It is the same trade the `dark_energy_betti` ruling took
  deliberately, in favour of derivedness over agreement.
- **The '+2' identity breaks**: D_bulk − b₃ = 26 − 43 = −17. Either D_bulk is not
  26 on this path, or the identity was never structural. A test asserts the break
  and that the note reads "not dropped".
- **Every b₃ consumer shifts** — racetrack exponent 2π/43, k_bary = 29, χ/b₃,
  wa_thawing — and a test fails if any of them does not respond to the seed.

#### What the author is ruling on

`seed_24` keeps the better w₀ and an **input** b₃ that now has **no geometric
home** among the declared constructions. `seed_43_joyce` derives both Betti
numbers from the resolution count, reproduces Joyce's canonical published pair,
keeps exactly three generations, and pays with w₀ at ~0.94σ and a broken
identity.

`compare_paths()` reports both and selects neither. A test asserts **both pass
the structural discriminator**, so integrality does not force the answer — the
ruling is genuinely the author's.

### The four suggested directions, assessed against the simulation

Four high-leverage tests were proposed. The simulation has already settled two of
them, one is superseded by its own diagnosis, and one is newly possible and paid
off immediately.

#### Test 1 — internal K_IJ from the associative 3-cycles: ADOPTED, and it works

Proposed: compute K_IJ = ∫ ω_I ∧ *ω_J from the actual 3-cycles rather than
importing an external Leech matrix, and test whether the S₄ structure induces
block structure — i.e. whether internal G₂ geometry produces axion hierarchies
without external lattice packings.

This is the right test, and it is now **possible for the first time**, because
the resolution derivation supplies an explicit harmonic 3-form basis. One
correction to the premise: there are **not 24** cycles. b₃ = 24 is unreachable;
at the canonical point b₃ = 43, decomposing as

    7   flat     Γ-invariant Λ³, exactly φ's triples (R3, derived)
    36  twisted  3 per A1 family × 12 families (derived)

At the canonical (12, 43) point the structure is **3 singular involutions with 4
families each**, the other **4 involutions acting freely**. Symmetry therefore
forces K_IJ into **four blocks**:

    K_IJ  =  7  ⊕  12  ⊕  12  ⊕  12

**This answers the question the test was asking: the internal geometry produces a
non-isotropic K_IJ with four distinct blocks and no external lattice anywhere.**
The hierarchy source is the singular-locus decomposition, not a packing.

Two structural bonuses fall out. **3 singular + 4 free = the 7 involutions** —
that is the lop-sidedness, derived rather than posited. And **3 × 4 = 12
families** is the faces × blocks structure arriving for the third time from an
independent direction.

(The block *structure* is forced by symmetry and is computed. The block *values*
still need a metric, which the framework does not have — so hierarchies are shown
to be structurally available, not yet numerically evaluated.)

#### Test 2 — lower-symmetry Niemeier lattices: DECLINED, but the diagnosis is kept

The insight is **correct and valuable**: Leech and E8³ gave Q_shell ∝ I₁₂ because
Co₀ and W(E8)³ are large enough that Schur's lemma forces isotropy. That
explains the earlier null result properly, and it is now on the record.

The proposed fix is declined. Testing D₂₄⁺ or A₁²⁴ would break isotropy, but it
continues down a path already measured as decorative: swapping the lattice moved
**no published number**, the only thing any module read from it was
`dimension → return 24`, and b₃ = 24 is now unreachable anyway. Test 1 reaches
the same goal — genuine off-diagonal structure — through geometry that is
load-bearing. Same target, better route.

#### Test 3 — solve D_I W = 0 on the full N=1 potential: ALREADY DONE, one modulus

Implemented in `racetrack_vacuum.py`: the full V = e^K(K^{IJ̄} D_I W D̄_J̄ W̄ −
3|W|²), every stationary point on (0.5, 300), Hessian-classified in both the
Re(T) and axion directions, under two Kähler slopes. Result: a unique
supersymmetric AdS minimum at Re(T) = 37.85 where D_T W = 0 coincides with full
stationarity, with the dS saddle barrier at 41.7.

The genuine extension in the proposal is **four moduli** with
K = −Σ ln(T_i + T̄_i) and gradient descent in log coordinates. That is not done
and is the natural next step — it is also where the four K_IJ blocks from Test 1
would enter, which makes Tests 1 and 3 the same programme rather than two.

#### Test 4 — asymmetric (8,6,6,6) clustering: ALREADY REFUTED, three ways

Tested in the thirteenth pass and refuted on arithmetic: 8+6+6+6 = **26**, so it
partitions 26 while the Golay code lives on 24; the 8 is **not an octad**, being
built from 6 Golay coordinates plus 2 breathing coordinates that are by
construction outside the 24; and **no** weighting gives δ_T = 0.75 (size → 0.250,
1/size → 0.333, size^(7/3) → 0.489, log → 0.138).

It is now refuted a fourth way: b₃ = 24 is unreachable, so there are no 24 cycles
to partition. Stays FALSIFIED.

#### Terminology

The reading-level toggle ships as **Layperson / Full**. Of the suggested
alternatives, *Conceptual* is the best-argued — it signals the physics stays
rigorous while index notation is translated — but "Layperson" was the author's
own term and is unambiguous to a non-specialist, which is the audience the toggle
exists for. Recorded as a deliberate choice rather than an oversight.

### The (6+2,6,6,6) structure merges with the 43 derivation — because its 24 is not b₃

The author corrected the earlier hint from (5,3,3,3) to **(6+2, 6, 6, 6)**, and
that correction forced me to withdraw the aim of my own refutation.

#### First, the correction I owe

The thirteenth pass refuted (8,6,6,6) partly on the grounds that
8+6+6+6 = **26 ≠ 24**, so Golay and M₂₄ cannot apply. That is true about Golay
and **irrelevant** if the 26 was never meant to be a Golay support. On the
corrected reading the 26 is **D_bulk**, and then the arithmetic is coherent:

    4 faces × 6  = 24,   + 2 on ONE face,   total 26

So that objection was aimed at the wrong claim and is withdrawn. **Two of the
three original objections survive and still matter**: the 8 is not an octad (it
is 6 Golay coordinates plus 2 breathing coordinates that are by construction
outside the 24), and no weighting gives δ_T = 0.75 (tested at 0.250, 0.333,
0.489, 0.138), so it does not rescue the racetrack stationarity it was proposed
for.

#### The apparent conflict

Read as a partition of b₃, the structure is coherent **only at seed_24**:

| | seed_24 | seed_43_joyce |
|---|---|---|
| 4 × 6 = b₃ | ✓ 24 | ✗ 43 |
| D_bulk − b₃ = 2 | ✓ | ✗ −17 |

which put the framework's two most attractive structures in opposition: the
(6+2,6,6,6) face structure needs b₃ = 24, and b₃ = 24 is exactly what the
resolution derivation showed is unreachable.

#### THE MERGE: the 24 is |S₄|, not b₃

It dissolves, because 4 × 6 = 24 is **derived — from the arc structure, not from
the cohomology**. Computed this pass:

    4     arc points = the faces                    derived (R2)
    × 6   each point-stabiliser is S₃, order 6      computed: 6, 6, 6, 6
    = 24  = |S₄|, the arc stabiliser                computed, and 4 cosets × 6
    + 2   = the flag stabiliser order               derived earlier this session
    = 26

Every number in (6+2, 6, 6, 6) is a derived group-theoretic quantity of the Fano
arc, and **none of them is b₃**. So the structure is fully compatible with
b₃ = 43: it describes the symmetry group, the 43 describes the cohomology, and
they are different objects.

That also gives the "breathing +2" a concrete identity for the first time: it is
the **flag stabiliser**, the involution fixing one (arc point, line) incidence.

#### The limitation, stated before it is misread

This merge does **not** derive D_bulk = 26. Partitioning 24 group elements is not
partitioning 24 dimensions, and claiming otherwise is exactly the A4 error this
register exists to catch — index structure mistaken for geometric structure. So:

- **What is established:** the *pattern* (four faces, six each, one lopsided by
  two) is derived, from |S₄| = 4 × 6 and the order-2 flag stabiliser.
- **What is not:** that this pattern is a decomposition of spacetime dimensions.
  D_bulk = 26 remains unexplained by it.

#### Two further merge candidates, recorded not claimed

**The twisted sector is 6².** b₃ = 7 + 36 and 36 = 6 × 6, with 6 = |S₃| the same
point-stabiliser order. It is also 12 families × 3 forms. Two readings of the
same 36; whether the 6² factorisation is structural or coincidental is untested.

**Two lopsided splits, not obviously the same one.** Finding B gives 3 singular +
4 free involutions (a 3+4 split of 7); the face structure gives 1 lopsided + 3
normal (a 1+3 split of 4). Both are lopsided and neither is derived from the
other. Worth testing whether the lopsided face is the one belonging to a
non-singular involution.

---

## 2026-09-21 (twenty-first pass) — the real form is SPLIT, and the metric-free cubic exists  (subsection moved from OUTSTANDING_ISSUES.md)

### b₂ flat = 0 had a false citation, and deriving it settled every degree

`derived_contribution_table` carried `FLAT_B2 = 0` commented **"DERIVED in
joyce_orbifold"**. joyce_orbifold had no Λ² computation at all. The value was
right and its provenance was false — the worse of the two failures, because a
wrong number gets caught and a wrong citation gets trusted.

Deriving it (R5) produced more than the one number. Measured: the **7
coordinates of T⁷ realise the 7 NON-TRIVIAL characters of (Z/2)³ bijectively**.
(Z/2)³ has 8 characters; the trivial one is not among the coordinates. Then:

- **b₁ flat = 0** — no coordinate carries the trivial character.
- **b₂ flat = 0** — χ_iχ_j is trivial iff χ_i = χ_j iff i = j, and a 2-form needs
  i ≠ j. So no invariant 2-form **can** exist. Stronger than none being found.
- **b₃ flat = 7** — zero-sum character triples are exactly the **7 lines of
  PG(2,2)**. Hence the invariant 3-forms *are* the Fano lines, which is why they
  coincide with phi's own support, and why **R3 and R4 were always one fact seen
  twice**.

The coordinate index set is itself a Fano plane, and that single fact — not phi,
not the real form — fixes the whole flat sector. Flat Betti:
**{1, 0, 0, 7, 7, 0, 0, 1}**, with Poincaré duality exact and χ = 0 as any odd
dimension requires; both are self-checks that can fail. A falsifiability test
drops to a proper subgroup of order 4 and confirms invariant 2-forms then **do**
appear, so the derivation depends on Γ rather than being vacuous.

## 2026-09-21 (twenty-second pass) — the A1 resolution becomes an object, and the seed's third source  (subsection moved from OUTSTANDING_ISSUES.md)

### ADDENDUM — the seed's third source, resolved; and the fork propagated HALF way

Written after the twenty-second pass and in answer to its recorded blocker. That
pass named `FormulasRegistry.py:653` as the seed's third frozen source and
declined to change it, correctly. There was also a source it did not reach, and
the way that one failed is the more instructive half.

#### A literal in the runner beat the fork-aware root

`run_all_simulations` **pre-loads** `topology.elder_kads` before the root
simulation runs, and `has_param` makes it first-writer-wins. So a literal 24
there silently beat `g2_geometry`'s fork-aware value. `k_gimel` was hardcoded a
third time in the same block, as `24 / 2 + 1 / np.pi`.

Nothing pre-loaded `b_2`. So on the 43 branch **b₂ moved to 12 while b₃ stayed
24**, and the pipeline ran on a state no declared path produces.

#### What the chimera claimed, and what is actually true

The mixed state produced confident numbers that read as a decisive result:

| | mixed (b₃=24, b₂=12) | **coherent (b₃=43, b₂=12)** | anchor |
|---|---|---|---|
| θ₁₂ | 36.97° — 4.75σ | **34.29° — 1.17σ** | 33.41° |
| θ₁₃ | 15.09° — **58.8σ** | **8.36° — 2.48σ** | 8.63° |
| θ₂₃ | 59.25° — 9.95σ | **50.99° — 1.69σ** | 49.3° |

That first column was in hand and about to be recorded as "the 43 path destroys
the neutrino sector". It does not. θ₁₃ moves from 58.8σ to 2.5σ once both Betti
numbers come from one seed.

**A partially-propagated fork is more dangerous than an inert one.** An inert
fork is visibly inert; a half-live one produces confident arithmetic about a
manifold that is not there. Same family as the A4 bar — the computation was
fine, the object was not.

Both literals now read `seed_values()`, and b₂ is pre-loaded from the same seed
so it cannot move alone. A guard asserts the published (b₃, b₂) pair is one a
declared path produces, **and** asserts that the chimera which shipped — (24,12)
— is rejected by that same rule, so the guard is tested against the state that
actually occurred rather than only against states that work.

#### The cost table, with its scope stated exactly

| | seed_24 (adopted) | seed_43_joyce |
|---|---|---|
| b₃, b₂ | 24, 4 | 43, 12 |
| k_gimel | 12.318 | 21.818 |
| θ₁₂ | 33.59° (0.24σ) | 34.29° (1.17σ) |
| θ₁₃ | ≈8.6° | 8.36° (2.48σ) |
| θ₂₃ | ≈49° | 50.99° (1.69σ) |
| w₀ | −0.9583 (3.62σ) | −0.9767 (3.94σ) |
| **free set** | **37** | **39 measured / 40 honest** |

**SCOPE, and it matters.** This is the **normal track only**. The 43 build still
exits 72, for exactly the reason the twenty-second pass gave: `b3_leaf()` sources
b₃ from `FormulasRegistry`, so the EML/Arithma track stays pinned to 24 and the
triple-track guard fires correctly. The parameters above are written before that
seal check and are coherent among themselves; the EML track is not coherent with
them. So this is **not** a clean end-to-end 43 run, and it is not offered as one.
The previous pass declined to publish a second free-set count on these grounds;
this is offered as a normal-track reading with the caveat attached, not as a
correction to that caution.

**No selection is made.** This is the cost table the `b3_seed` ruling needs.

#### The free set at 43 is 39 measured and 40 honest, and the gap is a defect

Two reductions withdraw themselves on the 43 path exactly as `free_set` is built
to: `algebra.freudenthal_quartic` (16(b₃/27)²) and `cosmology.wa_thawing`
(−4/√b₃) stop reproducing, so both rows return. 37 → 39.

`fermion.n_generations` stays removed, justified as "b₃/8 from the registered
`particle.b3`" — and **`particle.b3` still reads 24 when the seed reads 43**. The
reduction validates 24/8 = 3 and passes for the wrong reason. With a
seed-tracking `particle.b3` it would compute 43/8 = 5.375, fail, and return the
row: **the honest count is 40.**

This sharpens §1's staged inconsistency. `particle.b3` and `cosmology.b3` were
recorded as *mislabelled*, shipping DERIVED while the seed ships INPUT. They are
also **numerically stale** — they do not track the seed at all — and one of them
is now load-bearing for a free-set reduction. That is the SILENTLY_INSENSITIVE
class with a measured consequence, not a labelling complaint. Not fixed: those
rows are an author ruling, and the standing note that "a test fails the day they
change" still holds. What is new is that the cost of leaving them stale is now
one spurious reduction.

#### A correction I owe the twenty-second pass, and one it owes back

**Mine to it.** The task specification it was given asserted that the K_IJ
cross-blocks vanish by character orthogonality. That was wrong, and it said so:
the flat 3-forms and η are both Γ-invariant, so characters cannot separate them,
and leg counting fails too. The O(t²) it derived from the shrinking neck is the
real mechanism. The instruction was mine and the correction is its.

**Its to mine.** `intersection_tensor` read its −2 off "the intersection form on
an A_n resolution is minus the A_n Cartan matrix". The citation was right and the
number was right, and **nothing in the tree could produce either** — a literal
wearing a reference. Building the Eguchi–Hanson object makes −2 arrive a second
way, independently. That is a better outcome than the citation, and the earlier
module was weaker than its docstring implied.

#### Method note

Every branch comparison was made with a **full rebuild between branches**,
because the two runs share gitignored artifacts and a skipped rebuild makes the
second reading meaningless. The adopted build was restored afterwards and
verified at b₃ = 24, b₂ = 4, k_gimel = 12.318, free set 37 — so the published
artifacts are the adopted path and not the experiment.

## 2026-09-21 (twenty-second pass) — the A1 resolution becomes an object, and the seed's third source  (subsection moved from OUTSTANDING_ISSUES.md)

### ADDENDUM — the geometric layer closed out: seed provenance, the exponent pinned, the ledger self-contained

**2026-09-22, after the routine's pass.** Three hardening items land on top of
the routine's work, and with them the geometric layer is closed out in the
sense this campaign uses the word: every reachable claim measured, every
unreachable claim named with its missing object, every null recorded where a
reader would look for it.

#### The free set now says which SEED built its artifact (2dfd477)

Discovered independently of, and complementary to, the routine's resolver fix.
With `METAPHYSICA_VARIANT_B3_SEED=seed_43_joyce` set and no rebuild, the
registered `particle.b3` still reads 24 -- `parameters.json` is a shared
gitignored build artifact, so the three b₃-arithmetic removals verify against
whichever seed last BUILT, with nothing in the output saying which. The guard
LABELS rather than un-removes: the removals are internally consistent with the
artifact as built, so the fork-side count exists only after a rebuild, and
changing the count from the env var alone would fake a measurement never made.
`build_free_set()` now carries `artifact_seed_provenance` (artifact b₃ vs the
live fork's, with a consistency verdict) and, on a mismatch, names the
removals resting on the stale value. The routine's `parameter_artifact`
answers *which file was read*; this answers *which seed built it*. Both
provenance layers are needed and both are tested together.

#### The sqrt(t) wall claim becomes an EXPONENT (ae944d9)

Adversarial review of the routine's orbit scan found one gap: the order-one
test (t·a²/r*² ∈ (0.5, 1.5) over t ∈ [1, 100]) tolerates any wall exponent in
roughly [0.38, 0.62] -- r* ~ t^0.47 would have passed while the register says
sqrt(t). Measured: local log-log slopes 0.49667 → 0.49867 → 0.49948 across
t = 100..3000, approaching ½ monotonically FROM BELOW as the a⁴/r⁴ correction
dies. Pinned as three assertions -- below ½ always, monotone increasing, final
within 5e-3 of ½ (measured deviation 5.2e-4, margin 10×, stated in the file).
The rest of the review found the discipline held: no unfalsifiable
assertions in the nine new modules, the Leech enumeration genuinely exhaustive
(512 = 8³ block characters, 168 faithful), kill conditions tested where they
could fire.

#### The ledger's layer notes carry the measured nulls

`closure_ledger.LAYERS` now records, in the layer notes themselves: integer
flux cannot freeze a METRIC_DEPENDENT row at leading order because the
pairing is t-free (43 integers collapse to 2); and no discrete ansatz reaches
one either (zero traced edges). A reader of the ledger alone now sees not
just that the 7 metric rows are open, but that the two known freezing
mechanisms were tried and measured null. The continuous count stands at 22.

#### The closed-out state of the geometric layer

| layer | state |
|---|---|
| topology | CLOSED -- (12, 43) selected by n_gen = rank(Γ) = 3; b₃ = 7 + 3b₂ makes one input |
| metric | valued at leading order; its degenerate wall located at r* ∝ √t (exponent pinned), off-manifold below t_crit |
| flux | 43 integers → 2 effective at leading order; freezes the scale only (null recorded) |
| flavour | blocked on a NAMED missing object: codimension-7 conical points, of which the enumeration has none; intersection routes closed by admissibility = disjointness |
| wording | generated from live forks; published-artifact ratchet in place; the one literal PASS gate now refuses on both branches |

**The author rulings now waiting, consolidated:** ruling chi_eff also rules
n_gen_source (6b₃/48 ≡ b₃/8 identically -- route C is the b₃-route in
disguise); b3_seed; re_t_adoption. Each has both branches executable with
measured costs. The EML track unblocks on the first of these.

## 2026-09-30 (twenty-fourth pass) — closing the geometry: a certificate, a red-team, and a SETTLED result that fell

The author delegated working decisions under a published decision rule
(validity > closure > consistency > elegance > data as a test). This pass is its
first use. Every step was pre-registered in `docs/DECISION_LOG.md` (D-001 …
D-006) and committed before it was computed; the log carries the evidence, and
this entry carries the narrative.

### THE CERTIFICATE (G0, seeding G4)

The geometry now has one source of truth for prose: the certificate in
`PM/geometry/closed_geometry/`. Each theorem carries:

- a statement rendered from the live computation;
- what it counts, its proof, its falsifier and its scope;
- a test id that fails if it is false;
- references checked against the source.

It follows the seed fork. Flipping to (8, 31) re-derives every statement for that
member, and seed_24 publishes nothing. It is wired into the run as subsection
2.4, with parameter `topology.chi_y7 = 0`.

- **CG.1** The resolved Betti sequence (1, 0, 12, 43, 43, 12, 0, 1), derived from
  Joyce's resolution formula.
- **CG.2** χ(Y₇) = 0. It is the Euler characteristic. The formula still published
  as `euler-characteristic` is the effective index χ_eff: an open ruling, computed
  from off-path TCS Hodge data. Its labels were corrected, and its id and value are
  untouched.
- **CG.3** Twelve singular components, each a flat T³ with b₁ = 3.
- **CG.4** π₁ is finite exactly when all three generating involutions are
  singular, with an explicit infinite-order witness otherwise.
- **CG.5** Gauge content. The 12 loci are C²/ℤ₂ × T³, so each is N = 4 SU(2)
  (Acharya, hep-th/9812205, quoted): no confinement, no gaugino condensate.
- **CG.7** The reachable set: what Joyce's construction reaches from φ's
  (ℤ/2)³. It is family-level, so it publishes on every branch, including
  seed_24, which it excludes: b₃ = 24 is not among the 28 literature-checked
  pairs.
- **CG.6** The flux potential runs away. With the Lukas–Morris Kähler potential
  for exactly this manifold (hep-th/0305078) and the ADV superpotential
  (hep-th/0502060), V = 4e^K K^{ij}N_iN_j > 0, which scales as λ⁻⁵. The control
  with a non-real Chern–Simons invariant finds the supersymmetric AdS vacuum, so
  the method is able to find one.

### THE RED-TEAM, AND WHAT FELL

A blind verifier re-derived G0 without seeing the lead's work. It confirmed every
Betti sequence, χ = 0, π₁ (as a crystallographic group of rank 2^(3−n) − 1), the
independence of the singular involutions, and n ≤ 3.

It also found a defect in a result the codebase had labelled SETTLED.
`all_components_are_a1` tests a component's setwise stabiliser, not the isotropy
at its points, and so rejects Joyce's own JDG II Example 4. The lead read Example
4 in the source: b₂ = 8 + l, b₃ = 47 − l, l = 0 … 8, simply connected, holonomy G₂.

The corrected reachable set was recomputed independently in the codebase
(`joyce_reachability`), with contributions computed from lift characters. It
reproduces Joyce's eq. (27) exactly. The set is (0, 7) plus the lines
b₂ + b₃ = 23, 39 and 55: 28 literature-checked pairs, identical to the
verifier's.

**What survives:**
- b₃ = 24 is unreachable in every variant.
- (12, 43) is reachable, twice over: as Example 3 (all plain) and as Example 4 at
  l = 4.

**What falls:** "b₃ ∈ {7, 19, 31, 43}", "b₃ ≡ 7 mod 12", "b₃ = 7 + 3b₂" as the
family law, "exactly four members", and "(12, 43) is the unique holonomy-G₂
member". The last is true inside the all-plain subfamily; in the full family,
holonomy selects the whole n = 3 line. All of these are relabelled "all-plain
subfamily". Nothing is deleted, and no computed number changed.

`generation_selection` and the ruled `n_gen_source = b2_over_faces` are
labelled the same way: b₂/4 counts the singular involutions only when every
family is plain. On Joyce's full family the invariant count is n, the rank of
the singular span.

The seed's selection argument therefore goes back to the author. Within the
n = 3 line, (12, 43) is picked out in two ways: as the all-plain member (Joyce's
Example 3, symmetric in the three generators), and as the only member on which
b₂/4 agrees with n.

### THE REAL FORM (G3): EVIDENCE READY, RULING REQUESTED

- Flipping φ to the compact form moves 0 of 788 parameters and 0 of 226 numeric
  formula values, measured in two fresh pipeline runs.
- The adopted split form is one transcription sign away from the form the
  framework's own octonion product implies.
- The det B = 0 "wall" appears identically on both forms, and only at t ≥ 0.5.
- On the split form, 6 of the 7 involutions have a neutral (2, 2) transverse ℝ⁴,
  so Eguchi–Hanson is not the local model. The seed's own derivation therefore
  needs the compact form.

The lead recommends `octonion_derived`.

### RE(T) (G2): ABSENCE AT LEADING ORDER

The adopted geometry carries no leading-order pair that fixes Re(T): no
condensate, a runaway flux potential, and a real Chern–Simons invariant. This
covers classical supergravity with the leading-order K and G₄ flux. Membrane
instantons and corrections to K are open. The options for the author: an open
modulus (recommended), a labelled calibration, or research beyond leading order.

### WHAT EACH 24 COUNTS (G5): CLASSIFIED, VERIFICATION RUNNING

A neutral inventory found 121 places where b₃, or a 24 once called b₃, enters a
computation. Each has its verbatim derivation text and its value measured under
both seeds. They were classified by the object each text names (D-004 rules,
D-007 table), and the classification was committed before any re-wiring:

- **B3: 20.** The w₀ family, whose text names "the b3 associative 3-cycles". Its
  cost is confirmed: −42/43.
- **BULK: 7, plus parts of MIXED roots.** Bridge pairs, the 13D shadow, SO(24),
  and G22's torsion pins, all misfiled as b₃. These heal internal numbers.
- **NAMED: 3.** The PMNS distortion, built on the 24-cell. θ₁₃ heals, with a
  trials factor of 2.
- **NONE: 66.** These include k_gimel = b₃/2 + 1/π, whose texts name four objects
  and derive none. Everything built on it — α⁻¹, the Higgs VEV, sin²θ_W, T_CMB,
  μ — is a fit that agrees only at the retired 24.

The contested outcomes run both ways. A blind verifier is classifying a
fixed-seed third of the roots, plus the seven contested ones, from the rules
alone. Nothing is re-wired until it reports.

### DEFECTS FOUND IN PASSING

- `SimulationRunner.run_all()` always exports to the repo-local `AutoGenerated/`.
  A harvest subprocess — including the seed-blindness harvest under seed_24 —
  therefore overwrites the root the tests read first. This is a Stage 3 item.
- The enumeration's assignment counts are 28-fold redundant: each generating
  triple parametrises all 16,384 classes. The class counts are
  6,296 / 5,936 / 2,184 / 280 for n = 0 … 3.
- `pi1_finiteness`'s two "sides" were logically equivalent, so they could not
  confirm each other. This is now stated, together with the proof of E = ker p
  that the rank identification needs.

### MEASURED

- Engine `ee85cfb`. Non-slow suite: 2,743 passed and 1 failed. The one failure
  was the EML b₃-coverage ratchet, which counted the seven new upstream
  certificate formulas as non-rooted. Its baseline was corrected by name in the
  same change: b₃-rooted unchanged at 113, and no existing formula changed its
  rooting. The file then passes 7/7. The session baseline was 2,682 / 0.
- Both artifact roots were rebuilt, each carrying 576 formulas (569 before), all
  seven certificate theorems among them.
- The stale-claims ratchets are at or below their ceilings. CG.7's own falsifier
  sentence first pushed `b3_is_24` to 568. It was reworded to name the seed as
  off-path, not by widening the ratchet's marker list.
- The fork implication matrix was regenerated for both roots.

### AUTHOR RULINGS NOW WAITING (Stage 2 digest)

| ruling | lead's recommendation | evidence |
|---|---|---|
| φ's real form (G3) | compact (`octonion_derived`) | D-003 |
| Re(T) (G2) | open modulus at leading order | D-005 |
| what selects (12, 43) on the n = 3 line | to be argued in the digest | D-006 |
| χ_eff (G1) | pending the consumer inventory | inventory running |
| the demotion of the k_gimel layer to calibrations | labels only; the published values stay | D-007 |
