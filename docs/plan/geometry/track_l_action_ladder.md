# Track L: the action ladder: one master action, a validated sub-action at every step (2026-10-27)

Owner request: keep closing the geometry; validate the master action and its sub-actions at
every step; re-create established physics along the way. Builds on
`master_action_audit.md` (Track M) and Track M2 in `../2026-10-26-generalize-rust-action.md`.

## State
- G2 on the adopted path: `g2_closure.closure_report()` = CLOSED_BY_THEOREM (H1-H8 hold).
- Master action: nine partial statements, none a complete functional, and no reduction is
  performed (audit §1). Owner items 1-11 in audit §7 are still open.

## Design
A theory-agnostic package `src/metaphysica/actions/`. Like testground, it imports nothing
from `simulations`, `generators` or `website`.
- **Action:** dimension D, signature (s, t), fields (kind, components, mass dimension) and
  terms. Each coefficient has a mass dimension and a source (INPUT, DERIVED, CALIBRATED or
  OPEN) naming the simulation that provides it.
- **Step validation:** every term balances to mass dimension D; one sign convention; every
  coefficient's source is named; OPEN is allowed only on a term marked open. The verdict
  names the first failure, the same shape as `g2_closure` (measured, holds, can_fail, source).
- **Reduction:** parent → child over an internal space (dim, Ricci-flat flag, Betti numbers,
  volume). It checks that D_child = D_parent − dim, that child coefficients follow from the
  parent's through the declared map (e.g. M_Pl^2 = M_*^(D−2) Vol), and that zero modes from
  the Betti numbers match the child's field content.
- **Correspondence:** established physics the step must reproduce. Each is computed
  (sympy), never asserted, cites its textbook source and has a failing control.
- **Ladder:** an ordered list of steps; the report gives per-step validation, reduction and
  correspondence results, and the first failure.

The engine is trusted on PM only after it re-creates known physics (controls, lane L1).

## PM ladder (lane L2)
26D (24,2) → [bridge] → 13D (12,1) ×2 shadows → [G2 (7,0)] → 6D (5,1) → [KK] → 4D (3,1),
as in the chain comment in `geometric_anchors_core.py`. `gauge/master_action.py` becomes
the single source, and the other statements render from it (Track M2). The open choices
become forks in the path engine (Track P): spinor Weyl 4096 | Dirac 8192, bulk gauge
E8xE8 | none, dilaton canonical | dimensionless. Terms that exist only under one option use
P3's `applies_when` gates. The ladder report is a signal per configuration, so the path
audit costs every candidate action. Undefined terms (L_C, V_bridge, V_face, V_tor, OR^i,
rho_breath) are reported OPEN at their step, not hidden.

## Geometry next (lane L3, after L2)
- G2 zero modes on the adopted seed (b2 = 12, b3 = 43) versus PM's claimed 4D content: the
  first real geometry → physics test.
- D-028: Betti numbers are valid for only 36 of 340 classes (`d028_rust.md`). Make them
  computed for every class, then pre-register D-029 (the wider Γ class) before running it.

## Lanes
| Lane | Brief | Depends on |
|---|---|---|
| L1 engine + established-physics controls | `briefs/L1-ladder-engine.md` | none |
| L2a single master action: one definition, every published statement rendered from it, dimension checks per step (the duplicate list is in `../paper/track_f_formulas.md`) | (write after L1) | L1 |
| L2b action forks and gated terms | (write after L2a, P3) | L2a, P3 |
| L3 zero modes, D-028 Betti, D-029 | (write after L2) | L2 |

## Status
- 2026-10-27: plan written; L1 started. L2 split into L2a (no forks, starts after L1) and L2b.
