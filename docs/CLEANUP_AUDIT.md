# Cleanup Audit — both repositories, 2026-09-23

**Status:** PHASE 1 report. Nothing in this document has been acted on at the
time of writing. It is the list of candidates, the evidence for each, and a
classification. Phase 2 acts on `SAFE_DELETE` and `SAFE_MOVE` only.

**Scope:** `H:/Github/metaphysica` (the Python engine) and
`H:/Github/PrincipiaMetaphysica` (the published static site, and the live
register at `docs/OUTSTANDING_ISSUES.md`).

**The standing rule this audit obeys:** falsified, withdrawn, retired and
superseded work stays on the books, runnable and labelled. Nothing below is
classified for deletion because its claim turned out false. Where a document
is historical, the correct outcome is a label, not a removal — and in every
case checked, the label was already there.

---

## Headline finding

Both repositories are already close to clean. The tracked trees are tidy: the
engine's tracked root is nine files, all of which belong, and the site's is
eleven, all of which belong. There are **no** tracked backup files, no
`*_old` / `*_v1` / `*.bak`, no committed caches, and no orphaned tracked
directories in either repo.

What clutter exists is almost entirely **untracked local build output** in the
engine repo — already covered by `.gitignore`, costing ~58 MB of working copy,
and invisible to git. The one genuine piece of tracked-adjacent litter is a
427 KB scratch transcript at the site root.

The second finding is not about clutter at all and is recorded in
[Blocker](#blocker-the-suite-does-not-currently-collect) below: **the engine's
test suite does not currently collect**, for reasons that predate this audit.

---

## Blocker: the suite does not currently collect

This was found while measuring the required baseline and is reported here
because it gates Phase 2's verification, not because it is a cleanup item.

```
collected 2161 items / 4 errors / 3 deselected / 2158 selected
!!!!!!!!!!!!!!!!!!! Interrupted: 4 errors during collection !!!!!!!!!!!!!!!!!!!
```

Single root cause, at `src/metaphysica/simulations/PM/particle/neutrino_mixing.py:2370`:

```python
assert abs(_theta_12_test - 33.59) < 0.5, f"NeutrinoMixing: theta_12 unexpected value: {_theta_12_test}"
```

The module computes `_theta_12_test = 34.2855…` and the assertion fires **at
import time**. Because `simulations/__init__.py:275` imports
`NeutrinoMixingSimulation` eagerly, the failure makes `metaphysica.simulations`
unimportable, which cascades into four collection errors
(`test_ansatz_dependency_graph`, `test_import_health`, `test_ssot_full_compliance`,
`test_triple_track`) and aborts the run.

The arithmetic says this is the in-flight (12,43) migration, not a defect
introduced here. The perturbation is `(b_3 - b_2·n_gen) / (2·chi_eff)`; under
the old (12,24) family that is `(24-36)/288` and yields 33.59°, while under the
(12,43) family the engine now runs it is `(43-36)/288` and yields 34.2855° —
exactly the observed value. The hard-coded 33.59 is a leftover of the previous
family. HEAD's own subject line says as much: *"The engine runs (12,43) while
the published prose still describes (4,24)."*

`neutrino_mixing.py` is one of 26 files with uncommitted modifications and is
active work inside the 24-hour window. **It is left untouched.** Fixing it is
the author's call, not this pass's: the correct new constant is a physics
ruling, not a cleanup edit.

Consequence for Phase 2: the before/after comparison is run with
`--continue-on-collection-errors`, identically on both sides, so the number is
comparable even though it is not green.

---

## Classification summary

| Class | Count | Meaning |
|---|---|---|
| `SAFE_DELETE` | 9 | Untracked, regenerable or pure junk; nothing reads it |
| `SAFE_MOVE` | 0 | No module needs relocating; the layouts are coherent |
| `KEEP_LABELLED` | 8 | Historical/superseded/spent, already labelled — stays |
| `NEEDS_RULING` | 4 | Author's call; left alone |

---

## SAFE_DELETE

All nine are untracked. None is referenced by `build.py` `STEPS`, by any test,
or by any generator. Deleting them changes no git object.

### Engine repo — `H:/Github/metaphysica`

| Path | Size | Last commit | Why dead | Evidence |
|---|---|---|---|---|
| `%SystemDrive%/` | 968 K | never tracked | Windows icon-cache junk | A literal directory created when a command containing the `cmd.exe` variable `%SystemDrive%` ran under Git Bash, which does not expand it. Contains only `ProgramData/Microsoft/Windows/Caches/*.db`. The repo's own `.gitignore:110` documents the incident and ignores the path. |
| `dist/` | 52 M | never tracked | Release bundle, regenerable | One file, `metaphysica-v2.3.1-zenodo.zip`. Regenerated deterministically by `scripts/zenodo_pack.py`. `dist/` is gitignored. |
| `.pytest_cache/` | 271 K | never tracked | Test cache | Regenerated on every run; gitignored. |
| `Pages/` | 1.6 M | never tracked | Website output spilled into the library repo | Written by `python -m metaphysica.build` run without `--out`. `.gitignore:99-104` documents this precise spill as "~30 MB of regenerable noise that masks real changes". The *source* templates live at `src/metaphysica/website/Pages/` and are untouched. |
| `components/` | 228 K | never tracked | ditto | ditto |
| `css/` | 328 K | never tracked | ditto | ditto |
| `foundations/` | 580 K | never tracked | ditto | ditto |
| `images/` | 53 K | never tracked | ditto | ditto |
| `js/` | 1.3 M | never tracked | ditto | ditto |
| `index.html` | 96 K | never tracked | ditto | ditto |

Verified for the spill group: no test reads a root-level `Pages/`, `css/` or
`js/`. The single grep hit in the suite is
`tests/test_visual_regression_script.py:97`, which builds its own
`tmp_path / "Pages"` fixture and never looks at the repo root.

> **Deliberately excluded from this group:** `AutoGenerated/` (30 M) and
> `target/`. See [KEEP](#keep-labelled--keep) below. `AutoGenerated/` is
> gitignored *and* load-bearing — deleting it would break the suite.

### Site repo — `H:/Github/PrincipiaMetaphysica`

| Path | Size | Last commit | Why dead | Evidence |
|---|---|---|---|---|
| `AutoGenerated/AutoGenerated/` | empty | never tracked | Nested duplicate from a build path bug | Contains exactly two empty directories (`AutoGenerated/AutoGenerated/` and `.../plots/`) and zero files. An `out_dir` that already ended in `AutoGenerated` had `AutoGenerated` joined onto it again. |
| `scripts/` | empty | never tracked | Emptied leftover | Zero files, zero tracked entries. Not recreated by the build: `_copy_static()` copies `index.html`, `Pages/`, `css/`, `js/` only, and no generator writes a `scripts/` directory into `out_dir`. The one historical occupant, `gemini_peer_review.py`, is gitignored and gone. |

---

## KEEP_LABELLED / KEEP

Everything in this section looked like a candidate under a naive pattern match
and is not one. Each is here with the evidence that kept it.

| Path | Repo | Why it stays |
|---|---|---|
| `AutoGenerated/` (354 tracked files) | site | **The published deliverable.** Tracked, and `git check-ignore` confirms it is not ignored. Stays tracked; not a build artifact in this repo. |
| `AutoGenerated/` (30 M, untracked) | engine | Gitignored local build output, but **99 test files** read it via `generators/_common.autogen_dir()`, which resolves to `Path.cwd()/"AutoGenerated"`. Deleting it or tightening the ignore around it would break the suite. Left exactly as is. |
| `AutoGenerated/GATES_72_v16_2.json` | site | The `_v16_2` suffix reads like a stale version. It is not: it is the canonical output path, written by `generators/generate_72gates_json.py:483` and consumed by `generate_72_certificates.py:31`, `generate_compression_report.py:61` and `generate_improvement_scorecard.py`. `GATES_72.json` beside it is a deliberate alias written at line 490. Both were committed in HEAD. |
| `AutoGenerated/eml_trees_v25.json` | site | Same shape, same verdict. `TREES_FILENAME` at `simulations/core/eml_tree_adapter.py:115`; live read/write path. Committed in HEAD. |
| `scripts/archive/` (18 files) | engine | Spent one-off migration codemods, kept deliberately as provenance. Carries its own `README.md` saying so, and `.gitignore:95` names the directory as intentionally preserved. Several "would be actively harmful to re-run". |
| `docs/history/RULINGS_ASSESSMENT_2026-08-25.md` | engine | The quarantine occupant. `tests/test_superseded_docs_are_not_live.py` asserts this directory exists, is populated, that every file in it declares `SUPERSEDED` in its first three lines, and that no production module reads it. All four hold. Touching it fails tests by design. |
| `docs/RULINGS_ASSESSMENT.md` | site | A *different*, shorter document from the quarantined one (18 K vs 26 K). Already self-labels: "historical record… `docs/OUTSTANDING_ISSUES.md` is the live register and wins on any disagreement." No relabelling needed. |
| `docs/ARXIV_IDEAS_REGISTER.md`, `docs/BRIDGE_CHANNEL_ASSIGNMENT.md`, `docs/SCALE_DISAGREEMENTS.md` | site | All three are dated, status-marked, carry addenda recording what moved since writing, and cross-reference the register by section. `ARXIV_IDEAS_REGISTER.md` still describes `b3 = 24`, but it is explicitly a dated snapshot with a "read this before mining the lists" status update. Correctly labelled already; no edit. |
| `docs/DECLARATIVE_GATE_STRATEGIES.md`, `docs/TWO_TIME_ASSESSMENT.md`, `docs/PEER_REVIEW_MASTER_LIST.md`, `docs/FUTURE.md`, `docs/local-overrides.md` | engine | All dated and status-marked ("historical", "ADOPTED … RULED 2026-08-31", roadmap). None claims to be live guidance it is not. |
| `docs/OUTSTANDING_ISSUES.md` (395 K) | site | The live register. Not trimmed, not summarised, not reorganised, not touched. |
| `target/` | engine | Rust build cache, gitignored. Not clutter in the git sense, and deleting it forces a full `maturin` rebuild — currently impossible anyway, see Trap notes. |
| `src/metaphysica/website/AutoGenerated/**` | engine | **Wheel package data.** Force-included by the `[tool.maturin] include` glob precisely because the root `AutoGenerated/` ignore would otherwise strip it. The `.gitignore` carries `!` un-ignore rules for it. This is the known gitignore/wheel trap; nothing here is touched. |
| `src/metaphysica/_gnostic_aliases.py` | engine | Deliberate local-only overlay, gitignored by design, documented in `docs/local-overrides.md`. |
| `src/metaphysica/simulations/core/variants.py` | engine | Out of scope by instruction. Not read, not edited. |

---

## NEEDS_RULING

Left alone. Each is a judgement call that belongs to the author.

| Path | Repo | The question |
|---|---|---|
| `NewDirection.txt` | site | 427 KB at the repo root, **untracked and never committed** — `git log --all` returns nothing for it. Its content is a raw coding-session transcript ("Update Todos", "Bash … IN", pasted command output). Referenced by nothing in either repo. It is unambiguously scratch, *but* because it has never been committed there is no git copy: deleting it destroys the only one. Phase 2 therefore **gitignores it** — which removes it as repo clutter and makes it uncommittable — and leaves the bytes on disk for the author to delete or file. |
| `neutrino_mixing.py:2370` | engine | The stale 33.59° constant described under [Blocker](#blocker-the-suite-does-not-currently-collect). A physics ruling on the (12,43) family, and active uncommitted work. |
| `CLAUDE.md` | engine | Tracked in git, yet listed under "Local agent / working artefacts (not for publication)" in `.gitignore:79`. The ignore rule has no effect on an already-tracked file, so the stated intent and the actual state disagree. Resolving it means `git rm --cached`, which changes what the repo publishes. Not a cleanup decision. |
| `Cargo.lock` | engine | Present at the root, untracked, and gitignored at `.gitignore:86`. Normal for a library rather than a binary, so probably deliberate — but it sits next to a tracked `Cargo.toml`, so worth one conscious confirmation. |

---

## `.gitignore` changes proposed

### Site repo — two corrections and one addition

```diff
-# Discussion logs
-*_Discussion_Log_*.txt
-*.pytest_cache/
+# Discussion logs
+*_Discussion_Log_*.txt
+
+# Python caches (the previous `*.pytest_cache/` only matched a *suffixed*
+# directory, never the actual `.pytest_cache/` pytest writes)
+.pytest_cache/
+
+# Raw coding-session transcripts dumped at the repo root. Local working
+# notes, never part of the published site.
+NewDirection.txt
+*_session_transcript.txt
```

`__pycache__/`, `*.py[cod]`, `build/`, `dist/`, `*.egg-info/` are already
present and correct in this file and are not restated.

### Engine repo — no change

Its `.gitignore` already covers `__pycache__/`, `*.py[cod]`, `.pytest_cache/`,
`build/`, `dist/`, `*.egg-info/`, `target/` and the local scratch outputs, and
it carries the `!` un-ignore rules that keep `src/metaphysica/website/AutoGenerated/`
in the wheel. It also already documents, in comments, the two traps that bit
this project before: the unanchored-`js/` bug that stripped website templates
from the wheel, and the `%SystemDrive%` path-expansion incident. **Editing it
carries more risk than it removes.** Nothing proposed.

---

## What was checked and found clean

Recorded so the next pass does not repeat the search.

- **Tracked backup/versioned litter, both repos** — `git ls-files` filtered for
  `_old`, `_v[0-9]`, `_backup`, `.bak`, `.orig`, `.tmp`, `~`, `.log`: the only
  hits are `GATES_72_v16_2.json` and `eml_trees_v25.json`, both live (above).
  The `*.bak` codemod backups that were once committed are gone and ignored.
- **Empty directories** — none in the engine repo. Three in the site repo, of
  which `.claude/worktrees` is gitignored tooling and the other two are
  `SAFE_DELETE` above.
- **Caches in the site repo** — no `__pycache__`, no `.pytest_cache`, no
  `*.egg-info`, no `*.pyc` anywhere outside `.git/`.
- **Tracked roots** — engine: `.gitignore`, `CHANGELOG.md`, `CLAUDE.md`,
  `Cargo.toml`, `LICENSE`, `MODULE.md`, `README.md`, `RELEASE.md`,
  `pyproject.toml`. Site: `.gitattributes`, `.gitignore`, `.nojekyll`,
  `.zenodo.json`, `CITATION.cff`, `CNAME`, `LICENSE`, `README.md`, `_redirects`,
  `build.bat`, `index.html`. Every one belongs where it is.
- **Odd-looking tracked paths** — the two git-quoted entries under
  `AutoGenerated/certificates/` are just a Unicode λ in
  `G46_λ_stability.json`. Generated, legitimate.
- **Module layout** — `src/metaphysica/` splits into `data/` (5),
  `datasheets/` (3), `generators/` (39), `simulations/` (348), `website/` (3).
  Coherent. No module is proposed for relocation, so no import rewrites are
  proposed either.

---

## Environment note

`pip install -e .` does not currently complete:

```
Failed to copy H:\Github\metaphysica\target\maturin\physica_core.dll
  to H:\Github\metaphysica\src\metaphysica\_physica_core.cp313-win_amd64.pyd:
  The process cannot access the file because it is being used by another
  process. (os error 32)
```

A stale lock on the built `.pyd`; no Python process is holding it. The existing
editable install is intact and the Rust backend imports fine
(`metaphysica._physica_core` loads, `__version__` 2.3.1), so the suite runs on
the install already in place. Pre-existing, unrelated to cleanup, and not
fixed here — it would mean deleting `target/`, which this pass declines to do.
