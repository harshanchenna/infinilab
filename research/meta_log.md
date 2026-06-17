# Meta log

Dated record of process self-optimizations: signals observed, changes made,
expected effect. Written by the `meta` role (and by humans seeding it).

## 2026-06-17 — bootstrap: literature + meta layers added
**Signal.** The loop was a blind numerical search with no literature grounding
and no mechanism to improve its own process. Real autoresearch systems
(co-scientist's literature grounding; Karpathy/AlphaEvolve editing the code that
produces the metric) do both.
**Change.** Added (1) a `scout` role (read-only, writes cited notes to
`research/`), seeded `research/landscape.md` (how autoresearch is done) and
`research/rh_approaches.md` (RH methods/records/pitfalls); (2) a `meta` role
(this log) allowed to improve prompts/tracks/program and add harness primitives
under governance; (3) loop interleaving of scout/meta; (4) proposer now must
consult the research notes first.
**Expected effect.** Experiments grounded in known methods; methodological
weaknesses get fixed instead of repeated.

## 2026-06-17 — open meta task: accurate Li coefficients
**Signal.** Empirically (see session work toward `li_criterion`), the direct
truncated zero-sum lambda_n = sum_rho [1-(1-1/rho)^n] converges slowly
(~ln(T)/T): even with the exact closed form S_1 = 1+gamma/2-(1/2)ln(4pi)
(matches lambda_1 to ~3e-11), the higher lambda_n (n>=2) come out ~3% low at
K=400 zeros and approach from below. Good enough for a POSITIVITY claim (Li's
criterion only needs lambda_n>=0), not for accurate values.
**Proposed change (open).** Add a trusted `harness/rh_lib.py` primitive for Li
coefficients with either (a) power sums S_j plus Richardson/tail extrapolation,
or (b) the xi-function Taylor-coefficient method (Keiper 1992), with a built-in
self-check against published values (lambda_1..lambda_6). Until then, the
`li_criterion` track must scope claims to "positive, monotone-increasing-in-K
lower-bound estimates, consistent with Li's criterion", never to precise values.
**Status.** PARTIALLY ADDRESSED (2026-06-17). Added harness primitives
`li_S1_exact`, `li_power_sums`, `li_coefficients_estimate`, `li_selfcheck`
(commit `meta(harness):`). exp_0006 uses them for an honestly-scoped positivity
claim (two truncations K and 2K, require positive + monotone-increasing), kept,
skeptic verdict sound. STILL OPEN: a *rigorous* certified-positive version with a
proven tail bound (interval arithmetic on the S_j tail) so positivity becomes a
theorem-grade signal rather than "consistent with".

## 2026-06-17 — meta pass after 9 iterations: certification changes priorities
**Signals (from ledger/frontier).** 9 iterations, 7 tracks, all kept, all skeptic
`sound`. The decisive development: the `certified_zero_verification` track (Arb,
theorem-grade) reached T=2000, now EXCEEDING the heuristic `zero_verification`
frontier (T=600) at negligible cost (~0.4 ms/Hardy-Z eval). Heuristic sign-change
counting is therefore largely SUPERSEDED for verification — it survives only as
cheap reconnaissance.
**Meta-meta read.** This vindicates the landscape.md thesis "hard gate for truth":
we now have a tier that is not merely un-gameable but *theorem-grade*. The highest
marginal value is converting more tracks from "consistent with RH" to "proven".
**Change.** (1) Re-point program.md focus: push certified_T toward Platt-Trudgian
territory and build CERTIFIED versions of other criteria (Robin via Arb logs;
rigorous Li positivity via a proven power-sum tail bound). (2) Demote heuristic
`zero_verification` to reconnaissance in program.md. (3) Logged here.
**Open meta tasks.** (a) Incremental/resumable certified walk (avoid recomputing
from t=0 each run). (b) Rigorous Li tail bound (needs an explicit N(t) bound,
e.g. Trudgian) to make positivity theorem-grade. (c) Exact Lehmer-pair ->
de Bruijn-Newman lower-bound formula before claiming a Lambda bound.
