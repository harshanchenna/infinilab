# infinilab

An **autoresearch-style forever-loop** aimed at the Riemann Hypothesis (RH),
inspired by Andrej Karpathy's [`autoresearch`](https://github.com/karpathy/autoresearch).

Karpathy's loop optimizes a single training script against one cheap, honest
metric (`val_bpb`): an agent proposes a change, a time-boxed run measures it,
and the change is kept iff it beat the best. infinilab ports that idea from ML
to mathematics. The hard part of the port is that math has no `val_bpb` and LLMs
happily hallucinate proofs — so the design centers on **what makes a result
real**.

## The three-tier verifier
1. **Tier 1 — hard computational spine (truth).** Every experiment must produce
   a *falsifiable numerical artifact that runs and passes*. `harness/verify.py`
   executes it in a subprocess under a wall-clock budget and derives a verdict
   purely from running code and reading numbers. No language model. This is the
   `val_bpb` analog: cheap, automatic, un-gameable.
2. **Tier 2 — adversarial skeptic (soundness).** A stronger model (Opus) vets
   only the *claim* around real numbers — overclaiming, numerical artifacts,
   metric gaming. It can demote, never promote, which neutralizes LLM-judge
   self-preference and sycophancy.
3. **Tier 3 — formal (deferred).** Lean for small discrete lemmas, later;
   analytic number theory for RH isn't in mathlib yet.

This split came out of a research sweep over FunSearch (hard evaluator gates
truth — the pattern we adopt), AlphaProof/Lean (rigorous but premature for
analytic number theory today), and the AI-Scientist family (LLM-judge failure
modes we design against).

## Honesty about the ceiling
A CPU forever-loop will not *prove* RH. It can push concrete frontiers, build a
clean reproducible knowledge base, and — the only way numerics could settle it —
*disprove* RH by exhibiting an off-line zero or a violated equivalent. Every
experiment is built so a wrong sub-conjecture could be caught.

## Layout
```
program.md            Research directions & rules (the human->agent "skill").
AGENTS.md             How any LLM resumes the project from just the repo.
loop.py               The driver: propose -> verify -> skeptic -> record -> commit.
harness/              Trusted spine (DO NOT EDIT to pass a result):
  rh_lib.py             mpmath-backed RH primitives (Z, theta, N(T), zeros, GUE).
  experiment.py         The experiment contract: tracks, Result schema, validation.
  verify.py             Tier-1 hard verifier (subprocess + wall-clock budget).
  run_experiment.py     Subprocess entrypoint.
  ledger.py             Durable git-tracked memory + frontier ("keep" rules).
  skeptic.py            Tier-2 skeptic invocation (Opus).
prompts/              proposer.md (Sonnet) and skeptic.md (Opus).
experiments/          Every experiment ever proposed (the full search tree).
state/                frontier.json, ledger.jsonl, knowledge_base.md (the state).
journal/              One markdown writeup per kept iteration.
```

## Quickstart
```bash
pip install -e .            # mpmath, numpy, sympy
python loop.py status
python loop.py record experiments.exp_0001_critical_line
python loop.py loop --max 10
```

See **AGENTS.md** to continue the research, and **program.md** to steer it.
