# infinilab

A **project-agnostic, autoresearch-style forever-loop** with a hard, un-gameable
verifier at its core. An agent proposes a candidate (code/construction), a
program scores it cheaply and rigorously, and the result is kept only if it beats
the best — the FunSearch / AlphaEvolve / Karpathy-autoresearch pattern, wrapped
in a ledger, an adversarial skeptic, literature grounding, and self-optimization.

**The agent IS the loop.** Rather than a driver that shells out to an LLM, an
agent (Claude Code, Codex, or a human) drives a deterministic CLI (`lab.py`)
with its own tools: it proposes an experiment, verifies it (Tier-1), scrutinises
the claim (Tier-2), and records the outcome. Nothing here invokes an LLM, so it
runs in any harness. Read **AGENTS.md** for the one-iteration playbook.

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
  skeptic.py          Tier-2 reviewer helper (used by the legacy automated driver).
  driver.py           Deterministic mechanics: verify -> keeping rules -> journal/KB.
                      No LLM. Shared by lab.py and loop.py.
  evolve.py           FunSearch program evolution: island DB + rigorous evaluator
                      (used when a project defines an EVOLVE spec).
lab.py              The agent-driven CLI (PRIMARY): status / next / verify /
                    record / evolve. You drive it; it invokes no LLM.
loop.py             Legacy automated driver: shells out to the `claude` CLI to
                    self-play propose/scout/meta unattended.
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

## Quickstart (agent-driven)
```bash
pip install -e .                                  # mpmath, numpy, sympy
python lab.py status                              # frontier + recent ledger
python lab.py next                                # next experiment filename/module
# ... write projects/<name>/experiments/exp_NNNN_<slug>.py ...
python lab.py verify <module>                     # Tier-1: run it, read the numbers
python lab.py record <module> --skeptic sound     # keeping rules + journal/KB
# FunSearch evolution (cap_set):
INFINILAB_PROJECT=projects.cap_set python lab.py evolve status
# pick a different project for any command:
INFINILAB_PROJECT=projects.cap_set python lab.py status
```

See **AGENTS.md** for the full one-iteration playbook (the agent is the loop),
and each project's `program.md` to steer it. `loop.py` remains as a legacy
automated driver for hands-off runs.
