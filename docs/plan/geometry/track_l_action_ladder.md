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
| L2a single master action as a checked ladder; map of published statements | briefs/L2a-master-ladder.md | L1 |
| L2c render every published action statement from the ladder; retire duplicates | (write after L2a, F1) | L2a, F1 |
| L2b action forks and gated terms | (write after L2a, P3) | L2a, P3 |
| L3a zero modes on the seed, nonabelian gauge source | briefs/L3a-zero-modes.md | L2 |
| L3b D-028 invalid reasons, codim-7 local types, gauge-source candidates | briefs/L3b-gauge-source.md | L3a |
| L3c D-029 pre-registration | (write after L3b) | L3b |

## L3a result (merged 48ad890)
- Generic `actions/zero_modes.py`. Controls: Joyce (12, 43) gives 12 vectors and 43 chirals;
  11D on T^7 gives 28 vectors and 70 scalars (failing control: no dualisation, 63).
- **The 13D action has no p-form fields** (only G and Psi). So the G2 step gives no gauge
  fields at all, not even the U(1)^12 that a C3 form would give on b2 = 12. It does give
  43 metric-modulus scalars (b3), which the 6D action doesn't declare: `zero_modes:scalar`
  fails. G and the 8 spinor components match.
- `nonabelian_gauge_source` fails. SU(3)×SU(2) enters only through the OPEN `A4:L_SM` term,
  with no D-028 class named. Keeping the active Z2^3's 12 A1 loci singular gives SU(2)^12
  with b1 = 3 adjoint chirals (non-chiral), no SU(3), and (b2, b3) = (0, 7).
- Failing checks: [owner_item_6] → [nonabelian_gauge_source, owner_item_6, zero_modes:scalar].
- Owner decision: add a 3-form (or other p-form) to the 13D action, as in M-theory, and/or
  name a D-028 singular class with SU(3)×SU(2) as the gauge source (139 such classes at cap
  1536). Then declare the 43 moduli in 6D, or say how they are stabilised.

## Status
- 2026-10-27: plan written; L1 started. L2 split into L2a (no forks, starts after L1) and L2b.
- L1 merged (c9c1f2f): `metaphysica.actions`, 35 tests, every control and failing control computed; LEGAL.txt. L2a started (briefs/L2a-master-ladder.md).
- L2a merged (36bb6a4). L2c merged (e7ae865): 26D/13D/4D action formulas render from the ladder; 5 duplicates retired; de-frt, f-r-t-tau and scalar pneuma-lagrangian marked "Not derived from the master action" (owner: retire?). Open: owner item 6 (second time in 26 -> 13) is the only failing ladder check; reduced-lagrangian-4d still mostly-minus.
- L3a merged (48ad890); see "L3a result". L3b started (briefs/L3b-gauge-source.md).
