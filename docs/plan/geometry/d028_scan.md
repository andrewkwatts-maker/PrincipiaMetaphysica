# D-028 scan: gauge groups from flat G2 orbifold loci (rerun, cap 1536)

RETRACTION: the earlier report said "Kill 1 FIRES: no Gamma gives an A2 locus". That was wrong. The module's own control (Z3 on the hexagonal lattice) gives 9 A2 loci, SU(3)^9. The 13372 rejected order-3 extensions failed only because closure exceeded MAX_ORDER = 64 (orders 96 to 1536 occur). A cap artifact, not a result.

Worktree `metaphysica-orbiscan`, not committed. Code `src/metaphysica/simulations/PM/geometry/orbifold_gauge_scan.py`, tests `tests/test_orbifold_gauge_scan.py` (16 pass). Records: scratchpad `records.jsonl` (594 records). Rulings as in D-028.

## Method changes
- MAX_ORDER 64 -> 1536. DEN = 12 already holds thirds (c = 4) and sixths (c = 2); a test checks it.
- Class dedup now uses vectorised conjugate digests (same classes as before, tested), because the key version was too slow above order 100.

## Counts (class: active Z2^3 plus one delta of order 3 or 4; Z^7 and hexagonal lattices)
- 19516 candidate pairs; 11664 close at order <= 1536; 7852 rejected, all order-3 (still above 1536). 740 symmetry classes.
- Order-4 (signed-perm): 400 classes, all analysed. Order 32: 44, order 64: 212, order 128: 144 (the 144 are new; the old cap hid them).
- Order-3 hexagonal, classes by order: 96: 39, 288: 78, 384: 23, 864: 117, 1152: 46. Order-3 signed-perm: 96: 1, 192: 3, 288: 1, 384: 5, 576: 3, 768: 13, 1152: 5, 1536: 6.
- Order-3 analysis is a SAMPLE: 194 of 340 classes (analysis is slow at high order; 45 min budget). Seed 28, shuffled within each order and taken round-robin across orders. Analysed/total: hex 39/39, 39/78, 23/23, 38/117, 23/46; signed-perm 1/1, 3/3, 0/1, 4/5, 3/3, 13/13, 2/5, 6/6.

## SU(3) and SU(4)
- SU(3) (A2 loci): 87 of 194 sampled order-3 classes. None among order-4.
- SU(4) (A3 loci): 74 of 400 order-4 classes, none among order-3. SU(6) (A5): 23 order-3 classes.
- Typical groups: SU(2)^9 x SU(3)^4 (15 classes), SU(2)^16 x SU(3)^3 x SU(6) (12), SU(2)^22 x SU(3) (9). SU(4) classes: SU(2)^10..24 x SU(4)^1..2.
- 76 of the 87 SU(3) classes also have non-A strata (circles, |H| > k) that get no gauge group here, so their groups are incomplete.

## Hits containing SU(3) x SU(2), Kill 2 applied
- All 87 SU(3) classes contain SU(3) x SU(2) DIRECTLY (A2 plus A1 loci). None needs the Pati-Salam route.
- The 74 SU(4) x SU(2)^n classes contain SU(3) x SU(2) only via SU(4) > SU(3) x U(1) (partial resolution of C^2/Z4). That is a mechanism to test, not shown here.
- b1 of A2 loci: 0 (142) or 1 (87); never 3. b1 of A1 loci in hits: 0 (967), 1 (465), 3 (31).
- Kill 2 (all relevant loci b1 = 3, N=4, non-chiral): fires for 0 of 87 hits. No hit is T^3-only.
- Resolved Betti numbers: OPEN for all 87 hits (loci cross; 176 of 194 order-3 classes have crossings). Defined only for 18 order-3 classes without SU(3), e.g. (b2, b3) = (4, 13), (6, 15).

## Codimension-7 points (chirality lead)
- Present in 69 of 194 sampled order-3 classes (60 of the 87 SU(3) hits) and 113 of 400 order-4 classes (30 of the 74 SU(4) classes).
- Orbit sizes and stabiliser orders recorded per class (stabiliser orders 8 to 24 among the most frequent). Local type (C^3/Z_N or not) is NOT classified.

## Verdicts
- KC1 (no Gamma gives an A2 locus): does NOT fire. A2 loci occur in 87 of 194 sampled order-3 classes and in the Z3 control.
- KC2 (hit with all b1 = 3): does NOT fire. Every hit has loci with b1 = 0 or 1.
- Open: U(1)_Y; resolved Betti numbers; the 146 unanalysed order-3 classes; non-A strata. Nothing is adopted (ruling 4); the hits are fork options for the sweep and D-026.
