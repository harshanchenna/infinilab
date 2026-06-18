# infinilab

A **project-agnostic, autoresearch-style forever-loop** with a hard, un-gameable
verifier at its core. An LLM proposes a candidate (code/construction), a program
scores it cheaply and rigorously, and the result is kept only if it beats the
best — the FunSearch / AlphaEvolve / Karpathy-autoresearch pattern, wrapped in a
ledger, an adversarial skeptic, literature grounding, and self-optimization.

## Architecture: generic engine + swappable projects
```
harness/            The generic engine (problem-INDEPENDENT):
  project.py          Resolves the ACTIVE project (env INFINILAB_PROJECT).
  experiment.py       The Result contract: novelty, validation; TRACKS injected
                      from the active project.
  verify.py           Tier-1 verifier: runs an experiment in a subprocess under a
                      wall-clock budget; verdict from executing code + reading
                      numbers. No LLM. The un-gameable spine.
  run_experiment.py   Subprocess entrypoint.
  ledger.py           Durable, git-tracked memory: ledger.jsonl, frontier.json
                      (keyed by track::metric), knowledge_base.md.
  skeptic.py          Tier-2 adversarial reviewer (Opus): vets claims only.
loop.py             The driver: propose -> verify -> skeptic -> record -> commit,
                    plus scout (literature) and meta (self-optimization) passes.
projects/
  riemann/            The first project (Riemann Hypothesis).
    project.py          NAME, CONJECTURE, TRACKS.
    lib/                Trusted primitives (rh_lib, rh_certified).
    experiments/        Every experiment ever proposed.
    prompts/            proposer / skeptic / scout / meta.
    program.md          Research directions for this project.
    state/  journal/  research/   Per-project memory and notes.
  <next>/             A new project drops in here with the same shape.
```

Select a project with `INFINILAB_PROJECT=projects.<name>` (default
`projects.riemann`). Nothing in `harness/` hardcodes a problem.

## The three-tier verifier
1. **Hard computational spine (truth).** Each experiment must produce a
   falsifiable artifact that runs and passes. Cheap, automatic, un-gameable.
2. **Adversarial skeptic (soundness).** A stronger model vets only the *claim*
   (overclaiming, numerical artifacts, novelty overclaim, metric gaming). It can
   demote, never promote.
3. **Formal (deferred).** Lean for small discrete lemmas, later.

This split came out of a research sweep over FunSearch (hard evaluator gates
truth — the pattern we adopt), AlphaProof/Lean (rigorous but heavy), and the
AI-Scientist family (LLM-judge failure modes we design against). See
`docs/opportunities.md` for where this loop can have the most impact.

## Quickstart
```bash
pip install -e .                                  # mpmath, numpy, sympy
python loop.py status                             # frontier + recent ledger
python loop.py record projects.riemann.experiments.exp_0001_critical_line
python loop.py loop --max 10                      # propose/verify/skeptic/commit
# pick a different project:
INFINILAB_PROJECT=projects.cap_set python loop.py status
```

See **AGENTS.md** to continue the research from a fresh clone, and each project's
`program.md` to steer it.
