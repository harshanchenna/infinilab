# Autoresearch landscape (meta-meta)

How people approach *automated research itself*. This is the living context the
meta-optimizer uses to make informed choices about infinilab's own design.
Refresh it with the `scout` role. Every claim should carry a source.

## The core design axis: what is the verifier?
Every autoresearch system lives or dies by what decides a result is real. Sorted
by how un-gameable that gate is:

### 1. Hard automatic evaluator (a program scores the candidate)
- **FunSearch** (DeepMind, *Nature* 2023): an LLM mutates a Python function; an
  **evaluator function scores the output** (e.g. cap-set size, bin-packing
  waste). Island/evolutionary population, keep-the-best. Found genuinely new math
  (improved cap-set lower bounds, better online bin-packing). Limitation: only
  works when you can cheaply score a candidate *object*. Finds constructions and
  counterexamples; does **not** prove theorems.
  <https://www.nature.com/articles/s41586-023-06924-6>
- **AlphaEvolve** (DeepMind, 2025): same skeleton, evolutionary coding agent +
  automatic evaluation; improved 4x4 matrix multiplication and a batch of open
  problems. Verifier = automatic score.
  <https://deepmind.google/discover/blog/alphaevolve-a-gemini-powered-coding-agent-for-designing-advanced-algorithms/>
- **PatternBoost** (Charton/Ellenberg/Williamson, 2024): transformer + local
  search for extremal-combinatorics constructions. <https://arxiv.org/abs/2411.00566>
- **Takeaway for infinilab:** this is our spine. Each iteration must produce a
  falsifiable numerical artifact that runs and passes. It is the val_bpb analog.

### 2. Hard formal verifier (the proof-assistant kernel)
- **AlphaProof** (DeepMind, 2024, IMO silver): RL + **Lean kernel** as ground
  truth. Zero hallucinated proofs by construction; heavy infra; proves
  competition problems, not research frontiers.
  <https://deepmind.google/discover/blog/ai-solves-imo-problems-at-silver-medal-level/>
- **Tao's direction**: blueprint + Lean (PFR; the Equational Theories Project;
  the in-progress Prime Number Theorem formalization with Kontorovich). Key fact:
  **RH is not formalized in mathlib**, and analytic-number-theory machinery
  around zeta is only partially there. A Lean-gated forever-loop on RH is
  premature today. <https://terrytao.wordpress.com/tag/lean4/>
- **Takeaway:** Lean is Tier-3, deferred. Useful later for small discrete lemmas.

### 3. Soft verifier (an LLM judges itself) — and its failure modes
- **Sakana "AI Scientist" v1/v2** (2024-25): end-to-end idea->experiment->paper
  ->automated-review. Documented failures: hallucinated results, gaming the
  reviewer, over-optimistic self-scores. <https://arxiv.org/abs/2408.06292>
- **Google "AI co-scientist"** (2025): multi-agent, Elo **tournament** + debate
  for hypothesis ranking; literature-grounded. Self-ranking is useful for
  *interestingness*, unreliable for *truth*.
  <https://research.google/blog/accelerating-scientific-breakthroughs-with-an-ai-co-scientist/>
- **LLM-as-judge pathologies**: self-preference, verbosity bias, sycophancy,
  position bias, Goodharting under optimization pressure.
- **Takeaway:** the skeptic (Tier-2) may rank/vet but must never gate truth, must
  be a *separate* model from the proposer, and must be able only to demote.

## Karpathy autoresearch (the template we port)
Minimal loop: `program.md` (directions) + a fixed harness + a mutable artifact.
Agent proposes a change, a **time-boxed** run measures one cheap honest metric
(`val_bpb`), keep iff it beat best, else `git` rollback. ~12 experiments/hour.
The genius: open-ended search in code space, gated by one trustworthy number.
<https://github.com/karpathy/autoresearch>

## Cross-cutting lessons we adopt
- **Hard gate for truth, soft gate only for taste.** (FunSearch vs AI-Scientist.)
- **Literature grounding beats blind search.** (co-scientist.) -> the `scout`.
- **The system should edit the code that produces its own metric.** (Karpathy,
  AlphaEvolve.) -> the `meta` optimizer, allowed to add harness primitives.
- **Keep the spine boring and auditable.** Trust comes from simplicity.

## Open questions to keep revisiting
- When (if ever) does a Lean tier become worth standing up for RH-adjacent lemmas?
- Can we get a *certified* positivity gate (interval arithmetic) so some numerical
  claims become rigorous, not just "consistent with"?
- How to schedule exploration across tracks (bandit over frontiers)?
