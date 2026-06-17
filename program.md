# program.md — the research program

This is the human→agent instruction file (the analog of Karpathy autoresearch's
`program.md`). It defines *what* we are trying to do and the rules of the game.
The loop reads it; edit it to steer the research.

## Goal
Make incremental, **verifiable** progress on the Riemann Hypothesis (RH) by
running an indefinite loop of small, falsifiable computational experiments, and
accumulating only what survives a hard verifier and an adversarial skeptic.

RH: all nontrivial zeros of ζ(s) have real part 1/2.

We are honest about the ceiling: a forever-loop of CPU experiments will not
*prove* RH. What it can do is (a) push concrete frontiers (verify zeros to
greater height, sharpen statistics, tighten bounds), (b) accumulate a clean,
reproducible knowledge base, and (c) — the only way numerics could ever settle
it — *disprove* RH by exhibiting an off-line zero or a violated equivalent.
Every experiment is built so that a wrong sub-conjecture could be caught.

## How progress is measured (the val_bpb analog)
Three tiers, spine first:
1. **Tier 1 — hard verifier (truth).** `harness/verify.py` runs each experiment
   in a subprocess under a wall-clock budget and reads back numbers. No LLM.
   This decides whether a result is *real*. It cannot be argued with.
2. **Tier 2 — skeptic (soundness).** A stronger model vets only the *claim*
   around real numbers: overclaiming, numerical artifacts, metric gaming. It can
   demote, never promote.
3. **Tier 3 — formal (deferred).** Lean for small discrete lemmas, later. The
   analytic-number-theory machinery for RH is not yet in mathlib, so we do not
   gate on it today.

A result is **kept** iff it is a falsification, or it strictly advances its
track's frontier AND the skeptic did not flag it.

## Beyond blind search: grounding and self-optimization
The loop is not just numerical experiments. Two further roles keep it honest,
informed, and improving:
- **scout** (read-only, literature grounding). Pulls cited findings from papers /
  records into `research/rh_approaches.md` (RH methods) and
  `research/landscape.md` (how autoresearch itself is done). The proposer must
  consult these before inventing a method.
- **meta** (process self-optimization). Reads the loop's own ledger/journal and
  makes the *single* highest-value process change: fix a method the skeptic keeps
  flagging, add a trusted harness primitive, retire a stalled track, tighten a
  prompt. Logged in `research/meta_log.md`. Governance: meta may edit
  prompts/tracks/program freely and add simple, auditable harness primitives
  (commit prefix `meta(harness):`); it may never weaken a verifier or fabricate.

The forever loop interleaves these (defaults: scout every 8 cycles, meta every
10). This is the object / meta / meta-meta stack: experiments, improving the
process, and tracking how the field approaches autoresearch.

## The portfolio (tracks)
Rotate over these; push whichever frontier looks most tractable. (Canonical list
lives in `harness/experiment.py::TRACKS`.)
- `zero_verification` — all zeros up to height T on the line (Z sign changes vs N(T)).
- `zero_statistics` — GUE pair-correlation / spacing of zeros (Montgomery–Odlyzko).
- `lehmer_pairs` — anomalously close zero pairs; smallest normalized gap.
- `li_criterion` — Li/Keiper coefficients λ_n ≥ 0 ⇔ RH.
- `de_bruijn_newman` — bounds on Λ (RH ⇔ Λ ≤ 0).
- `explicit_formula` — zeros↔primes residual checks.
- `robin_inequality` — σ(n) < e^γ n log log n for n > 5040 ⇔ RH.

## Rules
- Never edit `harness/`. It is the trusted spine.
- Claims must be entailed by the numbers. Never "proves RH". Prefer
  "consistent with RH up to <explicit bound>".
- A `falsified=True` result needs concrete, auditable evidence.
- Stay within the wall-clock budget; return the best result so far.
- Prefer small, sharp, correct experiments over sprawling ones.

## Current focus (updated after the 9-iteration meta pass)
**Certification is the priority.** Arb gives theorem-grade results cheaply, so:
1. Push `certified_zero_verification` (certified_T) toward Platt-Trudgian
   territory; make the certified walk incremental/resumable.
2. Build CERTIFIED versions of other criteria: Robin via rigorous Arb logs,
   rigorous Li positivity via a proven power-sum tail bound (needs an explicit
   N(t) bound, e.g. Trudgian).
3. Heuristic `zero_verification` is now SUPERSEDED by the certified track for
   verification — keep it only for cheap reconnaissance.
Other live tracks (`zero_statistics`, `lehmer_pairs`, `li_criterion`,
`robin_inequality`, `explicit_formula`) remain open. See `state/frontier.json`
for live state, `state/knowledge_base.md` for facts, `research/meta_log.md` for
process history.
