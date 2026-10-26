# D-028 orbifold scan on the Rust core (Track R)

Status: computation only. No D-028 ruling is changed and nothing is adopted.
All work is uncommitted in the worktree `metaphysica-orbiscan` (branch `orbiscan`, merged with `core-paper` first, no conflicts).

## Method

Profile (Python reference, order-96 class, cProfile 66.6 s): `meet` 60 s, mostly Fraction arithmetic in `torus_solve`; `point_loci` 49 s of that.
The hot loops were ported to `rust/physica_core/src/orbifold/` (exact integer and rational arithmetic, DEN = 12):

- `num.rs`: Rat (i128), floor division as Python `//`, Smith normal form with the same pivot order, HNF, rank, restriction of M to span(B), elementary symmetric functions (Newton).
- `iso.rs`: affine maps, compose, integer inverse, element order, `close_group` (same BFS order, same error text "group order exceeds N (no closure)").
- `locus.rs`: fixed loci by torus solve, keys (HNF of annihilator plus phase), image, pointwise-fix test, `meet`, insertion-ordered map.
- `strata.rs`: orbits, stabilisers H and S, stratum type (A_{k-1}, circle, other-dimD, codim-7), flat Betti numbers, iterated meets (3 rounds). Meets and point loci are parallel with an order-preserving `std::thread::scope` map; pairs with a dim-0 locus are skipped (provably the same result).
- `mod.rs`: `close_group_rows`, `analyse_rows` (returns JSON). Exposed in `pyfacade.rs` as `py_orbifold_close_group` and `py_orbifold_analyse`.

Float parts of the Python reference are replaced by exact integers: the restriction R of M to the locus, elementary symmetric functions by Newton identities, `free_normal` as rank(M-I) == 7-d, and the no-fixed-vector test as rank of stacked (M_h - I) == 7. The only float field left is `exceptional`, compared after rounding to 6 places.
All Rust functions are 45 lines or fewer.

Python glue (`src/metaphysica/simulations/PM/geometry/orbifold_gauge_scan.py`): `close_group` and `analyse` dispatch through `metaphysica._dispatch.rust_fn`, `backend = "auto" | "rust" | "python"`, Python stays the reference path (`_close_group_py`, `_analyse_py`). Driver: `scripts/d028_full_scan.py` (resumable, multiprocessing, JSONL).

## Parity evidence

- `tests/test_orbifold_gauge_scan_rust.py`: 11 tests, Rust equals Python field for field (group elements and BFS order, full record). Cases: closure and both error paths, hexagonal Z3 control (9 A2 loci, gauge factors {3: 9}, no codim-7), active Z2^3, standalone order-3 and order-4 cyclic groups, order-64 classes with an order-4 delta, order-96 classes (314/0, 314/64, 84/0), threads=4 equals threads=1, bad backend fails early.
- pytest (new file plus existing 16): 27 passed in 126 s.
- `cargo test --release --lib`: 107 passed.
- Class enumeration with the Rust closure reproduced the earlier tally exactly: 19516 candidates, 11664 valid, 740 classes, 7852 rejected.

## Timings (Python vs Rust, `analyse`, one class)

| group order | Python | Rust (1 thread) | speedup |
|---|---|---|---|
| 64 (order-4 ext.) | 4.8 s | 0.18 s | 27x |
| 96 (idx 314/0) | 13.5 s | 0.50 s | 27x |
| 96 (idx 84/0) | 37.2 s | 1.03 s | 36x |
| 192 (idx 76/0) | 299 s | 7.7 s | 39x |
| 384 | 1007 s | 29.8 s (16 s uncontended; 2.7 s with 24 threads) | 34x (up to ~370x threaded) |

`scan_classes` (enumeration, cap 1536): 1007 s Python-closure, 477 s with Rust closure (remainder is Python digests and `from_euclid`).
Full cap-1536 analysis: 740 classes, 16 processes, 184 s wall (2800 core-seconds), 0 errors.

## Full D-028 counts, cap 1536 (the D-028 baseline; records: `H:/claude-scratch/d028_full/records.jsonl`, 740 records)

Classes 740 (order-3: 340, order-4: 400); 11664 valid candidates; 7852 rejected, all order-3, "group order exceeds 1536".
Order-3 class counts by group order: 96:40, 192:3, 288:79, 384:28, 576:3, 768:13, 864:117, 1152:51, 1536:6. All 340 analysed (146 were unanalysed before).

Order-3 (340 classes):
- SU(3) classes 139; all 139 are SU(3)xSU(2) hits. SU(6) classes 36 (all also SU(3)). SU(4): 0.
- Non-A strata: 122 classes, all hits. Labels: C3/Z6 (642 strata), nonabelian |H|=12 (72).
- Codim-7: 107 classes (92 hits), 2288 orbits. Top (orbit size, stabiliser order): (144,8) x592, (48,8) x360, (72,12) x168.
- Resolved Betti valid for only 36 classes. Classes with crossings: 304.
- b1 of A2 loci: 0 (270), 1 (139), never 3. b1 of A1 loci in hits: 0 (1456), 1 (746), 3 (72).
- Top hit groups: SU(2)^9 x SU(3)^4 (24), SU(2)^16 x SU(3)^3 x SU(6) (18), SU(2)^6 x SU(3)^4 (12), SU(2)^16 x SU(3)^4 (12).

Order-4 (400 classes; 32:44, 64:212, 128:144): SU(4) 74, SU(3) 0, non-A strata 248 classes (C3/Z4 980, nonabelian 168), codim-7 113 classes (1712 orbits). Identical to the earlier results.

KC1: does not fire. KC2 (all A loci with b1 = 3 in a hit): fires for 0 hits.

## MAX_ORDER past 1536: feasibility

The 7852 rejected candidates are finite groups (bounded linear part times a translation subgroup) but their order is large. Sampling about 4% of them, closure orders run 2304, 2592, 3456, 4608, 5184, 7776, 10368, 15552, 20736, 23328, 31104, 41472, 62208, 69984, 93312, 124416, up to 279936. About 13% of sampled signed-permutation candidates exceed 300000. Roughly 12% of rejected candidates close at order <= 3456, about 32% at <= 10368, about 58% at <= 31104.
Analysis cost grows steeply (16 threads, one class): 2304: 5.7 s (1984 loci); 2592: 13.8 s (4212 loci); 3456: 95 s (7552 loci); 10368 extrapolates to 30+ min per class, so a cap of 10368 is hours of work and the tail beyond about 31104 is not realistic with this design.

Tried: `--max-order 3456`, order-3 only, 20 processes (`records_cap3456.jsonl`, 579 records, 0 errors, 556 s analysis wall, 10896 core-seconds, slowest class 512 s). Enumeration: 12644 valid candidates, 979 classes, 6872 candidates still rejected (order > 3456).
Order-3 classes by order: 96:40, 192:3, 288:79, 384:28, 576:3, 768:13, 864:117, 1152:51, 1536:6, 2304:13, 2592:158, 3456:68.
Raised-cap order-3 counts (579 classes):
- SU(3) classes 229, all SU(3)xSU(2) hits. SU(6): 65 (all with SU(3)). SU(4): 0.
- Non-A strata: 199 classes, all hits. Labels C3/Z6 (1076), nonabelian |H|=12 (132).
- Codim-7: 177 classes (147 hits), 3744 orbits. Top (orbit, stab): (432,8) x672, (144,8) x592, (48,8) x360, (288,12) x224, (216,12) x224, (72,12) x168.
- betti_valid 60. Classes with crossings 519.
- b1 of A2 loci: 0 (466), 1 (229), never 3. b1 of A1 loci in hits: 0 (2223), 1 (1287), 3 (120).
- KC2 fires for 0 hits. KC1 does not fire.
- Top hit groups: SU(2)^9 x SU(3)^4 (40), SU(2)^16 x SU(3)^3 x SU(6) (32), SU(2)^16 x SU(3)^4 (22), SU(2)^6 x SU(3)^4 (20).
The 239 new classes (orders 2304, 2592, 3456) add 90 SU(3)xSU(2) hits and 29 SU(6) classes; no new kill criterion fires.

## Unfinished or not feasible

- Candidates with closure order above 3456 (6872 of them; the tail exceeds 300000) are still unanalysed. Orders up to about 10368 are possible but cost hours; beyond about 31104 needs a different algorithm (for example quotienting out the translation subgroup first).
- The local type of codim-7 points is unclassified.
- Resolved Betti numbers are open for most hits (betti_valid is true for 36 of 340 classes at cap 1536, 60 of 579 at cap 3456).
- `exceptional` floats are compared after rounding, not bit-exact.
- The built extension `src/metaphysica/_physica_core.pyd` is gitignored; rebuild with `cargo build --release --features python`.
