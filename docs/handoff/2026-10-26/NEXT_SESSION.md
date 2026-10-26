# Handoff 2026-10-26 (second half): generalize, master action, cleanup

Owner request: "generalize and explore all possible spaces, optimize with rust backend,
master actions well defined, all issues resolved", then "strip out old redundant wordings/
files", "website polished and internally consistent for each branch path".
Plan for all of it: `docs/plan/2026-10-26-generalize-rust-action.md` (Tracks R, M, M2, S, G, C).
Token rule from the receipts session: no sleep/until polls; every agent brief says
"Never use sleep loops; use run_in_background or Monitor with an until-condition."

## State at handoff
- Sweep at 838bebc finished: site/active χ² 3030.0985/4, site_check 10/10, gate tests 160
  passed, path snapshot unchanged. Committed to the site as a37f0af.
- tcs_scope.py then reported 4 strings in 2 racetrack formulas; fixed in engine 5c938fa
  (3 guard cases in test_c4b_residual_tcs.py, failed first). 752d9a4: path_comparison.json.
- Merged into engine `core-paper` with no conflicts: pathcheck 3c4320c, master-audit
  24363a7, cleanup-c a8dd95a, paths-g 06b85dc/10cf402, orbiscan 9b5c302 -> fe3995d.
  - master-audit: notation fixes, 8 formulas DERIVED->ANSATZ, 12 tests.
  - cleanup-c: 26 dead modules removed; superseded_scan ratchets autogen 310, pages 8,
    website 15 (lower after rebuild). Its bundle index.html fixes the abstract that still
    says "Twisted Connected Sum" on the live site; the next rebuild copies it.
  - paths-g: selection files, declared requires/excludes, `variants.forced()`.
  - orbiscan: D-028 scan in Rust (27-39x). 340 order-3 classes at cap 1536 (139
    SU(3)xSU(2) hits), 579 at cap 3456 (229); KC1 no, KC2 0; 6872 close above 3456.
    Open: codim-7 local type; Betti valid for only 36/340. Report geometry/d028_rust.md.
- Rust extension rebuilt from fe3995d and installed as
  `src/metaphysica/_physica_core.cp313-win_amd64.pyd` (gitignored; Sep copy saved as
  `<scratchpad>/_physica_core.sep.pyd`); exposes py_orbifold_analyse.
- Full suite on fe3995d was running: `<scratchpad>/full_fe3995d.txt`.

## Next, in order
1. Full suite on fe3995d passes (compare 3604 passed / 411 skipped at 838bebc), else fix
   with a failing-first test. Then pull origin/main (755d13f), merge core-paper into main.
2. Rebuild + sweep (`RUNS=H:/claude-scratch/runs_g sh docs/plan/paths/merge_d025.sh <S>`):
   expect tcs_scope.py = 0 and bundle/site to differ only in the overview block. Then
   `python -I docs/plan/paths/interactions.py H:/claude-scratch/runs_g` -> overlapping
   fork pairs; run them with `sweep_paths.py`. Lower the C2 ceilings.
3. Agents: G4 incremental path builds + the 5 inert forks (b3_origin, g2_construction,
   moduli_indexing, bulk_signature, face_genericity): wire, or add `Fork.wired=False` so
   describe()/site/sweep stop presenting them as executable. Then G2 option families,
   D-029 pre-registration, M2 (needs owner rulings on the action).
4. Owner items: DECISION_LOG tail (master action 10 items, 74 formula-vs-row, relabels,
   G56/G59, flux_homogeneity fix-or-retire, 15 website hits in Gemini review records).

## Fixed earlier this session (each with a test)
- e79f41f: the superseded-prose ratchet failed only in full runs because the seed-blindness
  harvest inherited METAPHYSICA_OUT and overwrote the suite's staged sections.json with a
  seed_24 build. Found with a per-test probe; the harvest now writes into its scratch dir and
  decodes its output as UTF-8 (cp1252 killed the reader thread). e50f330 (tests prefer the
  published tree over repo-local scratch) is kept but was not the cause.
- 610f226: five algebra sims replaced an unset b3 with 24; they now raise. PMRegistry already
  raises on a missing parameter, so only stub registries were affected.
- 66478c2, merged as 838bebc: the last eight unqualified TCS containers labelled as the retired reading.
  `tcs_scope.py` now runs under `-I` on Windows and accepts "reading"/"belonged" qualifiers.
- `test_seed_blindness` passes again (137 > 135 is gone).
- 18316dc: four failures already present at aab876d (contradiction scan collapsed
  |v| < 5e-11 to one value; m_higgs_pred left the load-bearing set under D-027 r3;
  supplementary sections exempted from SSOT rules 1/4/6/7; 2b_report fixtures).
- 90b1b93: `cosmology.M_Pl_4D`, `geometry.m_planck_4d`, `gravity.newton_constant_theory`
  declared CIRCULAR (each returns the CODATA value it was scored against).
  `geometric_anchors` registers via `set_param`, so it now applies declared exclusions.
  Anchor `derivation` metadata says "Computed at the fitted anchor ANCHOR_FIT = 24, not
  the live b3; topological provenance OPEN" (status and tuning_free untouched: owner).
- 90b1b93, 043a0a4: observer and unitary reports were unseeded, so every build changed
  them and path diffs counted the noise (the "1 → 0 changed value" paths were this, not
  Planck rows). Seeded with `default_rng(0)`.
- 043a0a4: dead `visit_Num(node: ast.Num)` removed (fails at import on Python 3.14);
  guard `tests/test_no_removed_ast_nodes.py`.
- d30639a, `docs/plan/paths/sweep.py`: reused any run with `DONE.json`, so a resumed
  RUNS dir published path diffs from a stale engine. DONE.json now records
  `HEAD+sha256(git diff HEAD)[:16]`; runs from another engine rerun. Untracked engine
  files are not hashed. Path counts published before this from a resumed RUNS dir are
  suspect: the clean sweep raised e.g. dark_energy_betti--b2_4 from 197 to 252 changed
  values (EML cross-check rows that do follow the option).

## Owner decisions added
- Planck CIRCULAR rows: confirm. `cosmology.M_Pl_4D` shows GEOMETRIC though its
  definition says MEASURED (first registrant wins).
- m_W / m_Z: tree relations from v and on-shell sin²θ_W = 0.22320, which is defined
  from m_W/m_Z; likely circular (decide with EW v = 246.37).
- `portals.dm_cross_section_cm2` 1e-91 cm² PASSes an upper bound of 1e-45: tests nothing.
- ANCHOR_FIT = 24 rows scored on main: `geometry.w_zero` = −23/24 PASS while live
  w0 = −42/43 TENSION (w0 published twice); n_s, sum_m_nu PASS. Score as CALIBRATED or
  exclude; GEOMETRIC/tuning_free labels.
- `cosmology.breathing_mode_vev` (DERIVED) and `cosmology.epsilon_KK` (GEOMETRIC) are
  described as CALIBRATED at b3 = 24.
- Earlier list unchanged: K = 4, h11 = n_faces = 4, h31 = 68, Re(T) = 1.833,
  T_OMEGA = −0.875, mephorash_chi, proton S and tau_p, mirror T'/T, plus the
  2026-10-25 list.

## Known, not yet fixed
- `src/metaphysica/simulations/AutoGenerated` is a real, gitignored, stale directory (71 files,
  2026-10-03); it fails `tests/test_output_dir_binding.py` (2 tests). Deleting it is the owner's call.
- generate_interactive_html overwrites site pages; edit the engine website bundle.
- C4b residue 66478c2 (branch `c4b`): confirm after a rebuild that `tcs_scope.py` reports 0, in
  particular the cycle-separation title and the second T_OMEGA string.
