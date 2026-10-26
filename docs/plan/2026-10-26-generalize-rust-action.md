# Generalize the spaces, Rust hot paths, master action (2026-10-26)

Owner request: "generalize and explore all possible spaces, optimize with rust backend and
ensure we have master actions well defined, all issues resolved".
Rules unchanged: values move only by owner ruling; a scan adopts nothing (D-028 ruling 4);
a test per fix; agents never commit; engine `core-paper` is not edited while a build runs.

## Track R: D-028 scan complete, in Rust (worktree `metaphysica-orbiscan`)
- Port the scan's hot loops (group closure, conjugate digests, fixed-locus analysis) to
  `rust/physica_core`, exposed through `_dispatch` with the Python path kept as reference.
  Parity tests: Rust and Python agree on every record for a fixed sample.
- Then finish D-028's own class: all 340 order-3 classes (146 unanalysed), and the 7852
  candidates rejected above order 1536 if the cap can be raised.
- Report counts in `docs/plan/geometry/d028_scan.md`; no adoption.

## Track M: master action well defined (worktree `metaphysica-master`)
- Three definitions: `config/parameters/master_action.py`, `simulations/PM/gauge/master_action.py`,
  `simulations/PM/derivations/lagrangian_master.py` (+ `gauge_sector_complete.py`).
- For each term: fields, dimension and signature, mass dimension of every term, where each
  coefficient comes from (input, derived, calibrated), which simulation computes it, and whether
  the three definitions agree. Report `docs/plan/geometry/master_action_audit.md`.
- Fix label, prose and internal-consistency bugs with tests; value changes go to the owner list.

## Track S: path space beyond single deviations (after the rebuild)
- 22 forks, product 2.79e9; single deviations 42. Exhaustive is impossible.
- From the single-deviation sweep, two forks interact only if their changed-row sets overlap.
  Disjoint pairs are additive and need no run. Count overlapping pairs, run only those,
  and report non-additive pairs (the real joint space).

## Generalization of the geometry scan (proposal, D-029 to pre-register after Track R)
- Wider Γ class (Z2^3 plus two extra generators), other lattices compatible with φ₀.
- Pre-register rulings and kill conditions in DECISION_LOG before any run.

## Track G: general paths and switches (owner request 2026-10-26, after Track S data)
Today: 22 forks of hand-listed discrete options (`variants.FORKS`), one env var per fork,
`sweep.py` runs single deviations only, `switch_search` checks combinations after the fact,
every path is a full build. Steps, each with tests, none moving an adopted value:
- G1 Selections as data. A path is a full `{fork: option}` map with a canonical id (sorted
  digest). `METAPHYSICA_SELECTION=<json file>` sets many forks at once; `resolve` reads it
  after the explicit override and before the per-fork env var. `sweep.py` takes a list of
  selections (single deviations, the overlapping pairs from `interactions.py`, or any list).
- G2 Option families. A fork may declare a family (generator over a stated domain) instead of
  a hand list: Joyce/orbifold Betti pairs from the D-028 records (`b3_seed`, `b3_origin`),
  the 24 Niemeier lattices (`lattice_24d`), signatures (p,q) with fixed p+q (`bulk_signature`).
  Family members are CONSIDERED; the domain comes from data or a cited list, never invented.
  Consumers must read the option's parameters, not its id string.
- G3 Declared compatibility. Options carry `requires`/`excludes` on other forks' options, so
  the product space is pruned before enumeration; `switch_search.consistency_checks` keeps
  the checks that need computation. Report the pruned size beside 2.79e9.
- G4 Incremental paths. Map each `resolve` call site (29) to its simulation, and each fork to
  the rows it changes (from Track S). A path build reruns only simulations downstream of
  the forks it changes, reusing `active` for the rest; parity test against a full build.
- G5 Rust where measured. Profile a path build and the switch search; port only hot loops to
  `physica_core` behind `_dispatch` with parity tests (as Track R).
Order: G1 then G3 (cheap, unlock joint runs), G4 (makes the space affordable), G2, G5.

## Track C: strip stale wording and dead files (owner request 2026-10-26)
Standing rule kept: a refuted pathway stays runnable and labelled (DISABLED option) because a
refutation that cannot be rerun is folklore. What goes: anything not simulatable, not
referenced, or saying something the current path no longer says.
- C1 Dead code: modules no import, test, build list or script names (inventory script
  output); delete with git rm after a test sweep proves nothing loads them.
- C2 Stale prose everywhere it is published: extend `superseded_scan` beyond sections.json to
  pages, FAQ, beginner guide, datasheets, formulas, certificates and website source. Its
  vocabulary comes from data: every DISABLED option's summary/claim plus the retired list
  (b3 = 24 as live, TCS #187, seed_24 as adopted). Ratchet each surface to 0 by rewriting to
  the adopted path or wrapping in a "Superseded path" callout.
- C3 Duplicate statements of one quantity (e.g. w0 published twice, the 74 formula-vs-row
  differences): one source, others read it; value choice is the owner's.
- C4 Every remaining DERIVED/GEOMETRIC claim names the simulation that computes it on every
  path (from path_consistency.py); claims with no simulation are relabelled, not deleted.
- C5 Docs: P/docs/plan and handoff folders older than the last two sessions move to
  docs/archive with an index line each.
Runs after the sweep; engine work in its own worktree.

## Track M2: one master action, its open choices as forks (after Track M, owner rulings)
Track M found nine partial statements and no complete functional (`geometry/master_action_audit.md`).
"Well defined" needs one action; "proved" then means each term's dimension, coefficient source
and reduction is computed by a simulation and tested. The open choices become forks (Track G
families), so each candidate action is runnable, not argued:
- spinor: Weyl 4096 (m, lambda vanish, dropped) | Dirac 8192 (m, lambda kept)
- bulk gauge sector: E8xE8 Yang-Mills | none (gauge fields from geometry only)
- L_C, V_bridge, V_face, V_tor, OR^i, rho_breath: define from the simulation that computes
  them, or drop; each kept term gets a simulation and a mass-dimension test
- dilaton: canonical [phi] = 12 with xi R phi^2 | dimensionless with g_s = e^phi (no xi term)
- sign convention: one, mostly plus, enforced by a test over every action formula
Deliverable: `simulations/PM/gauge/master_action.py` becomes the single source; the other eight
statements render from it; a test checks every term balances to mass dimension 26.
