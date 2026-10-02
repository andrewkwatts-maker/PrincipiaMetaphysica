# D-019 annex — path assessment configuration (skeleton; final before the first run)

Status: SKELETON (2026-10-02). The fields below are filled at the end of Phase 3, and
this file is committed before any PM assessment run. A run whose assessment-config
sha256 differs from the one recorded here is void (kill condition K5).

| Field | Value |
|---|---|
| assessment configuration | `src/metaphysica/theories/pm/configs/assessment.yaml` (to be created) |
| sha256 | _pending_ |
| active selection digest | _pending_ (D-015 state) |
| constraints (Requires / Excludes) | _pending — each with its rationale quote and source_ |
| target facts | n_gen = 3 |
| standing-failure rule | checks failing in every assessed configuration are excluded and disclosed |
| policy forks held | render_policy, theory_uncertainty_policy |
| measured run budget | _pending — Phase 1 pilot: wall time, peak memory, timeout, jobs_ |
| modes | assess (active + considered), reassess (+ retired-reassessable), archaeology (+ retired-certain) |
