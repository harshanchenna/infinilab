# AGENTS.md — how to pick up this project cold

You are an LLM (or human) resuming infinilab from nothing but this repo.
Everything needed is in git. Read this, then continue the loop.

## What this is
A **project-agnostic** autoresearch forever-loop with a hard, un-gameable
verifier (FunSearch / AlphaEvolve / Karpathy-autoresearch lineage). The generic
engine lives in `harness/` + `loop.py`; each research problem is a **project**
under `projects/<name>/`. See `README.md` for architecture and
`docs/opportunities.md` for which problems suit this loop best.

## Pick the active project
Set `INFINILAB_PROJECT=projects.<name>` (default `projects.riemann`). Everything
else (tracks, state, prompts, experiments, lib) is resolved from it by
`harness/project.py`. Current projects:
- `projects.riemann` — Riemann Hypothesis (the first, mature project: 15
  iterations across 8 tracks, incl. a certified zero-verification tier and a
  de Bruijn-Newman bound from a self-discovered Lehmer pair).
- `projects.cap_set` — cap sets in F_3^n (FunSearch-style construction).

## Where a project's state lives (read in this order)
For the active project dir `projects/<name>/`:
1. `program.md` — goal, rules, track portfolio, current focus.
2. `state/frontier.json` — best result per `track::metric` (the leaderboard).
3. `state/knowledge_base.md` — skeptic-vetted facts.
4. `state/ledger.jsonl` — append-only history of every iteration attempt.
5. `journal/NNNN-*.md` — a writeup per kept iteration.
6. `experiments/exp_*.py` — every experiment ever proposed.
7. `research/` — literature grounding + `meta_log.md` (process self-optimization).

## How to run
```bash
pip install -e .
python loop.py status
python loop.py record projects.riemann.experiments.exp_0001_critical_line
python loop.py step                 # one propose->verify->skeptic->commit cycle
python loop.py loop --max 20        # many cycles (scout every 8, meta every 10)
INFINILAB_PROJECT=projects.cap_set python loop.py status   # switch project
```
Models (env): `INFINILAB_PROPOSER_MODEL` (sonnet), `INFINILAB_SKEPTIC_MODEL`
(opus). The loop shells out to the `claude` CLI for propose/scout/meta.

## Add a new project
Create `projects/<name>/` with: `project.py` (NAME, CONJECTURE, TRACKS), `lib/`
(trusted primitives = the rigorous verifier), `prompts/` (proposer, skeptic,
scout, meta), `program.md`, and `experiments/__init__.py`. The engine creates
`state/` and `journal/` on first record. Then act as the proposer (write
`experiments/exp_NNNN_*.py` to the contract in `harness/experiment.py`) and
`INFINILAB_PROJECT=projects.<name> python loop.py record <module>`.

## Invariants
- `harness/` and a project's `lib/` are the trusted spine; never edit them to
  make a result pass.
- Claims must be entailed by the numbers. Prefer honest nulls to overclaims; the
  skeptic polices novelty overclaims (`reproduction` vs genuine frontier work).
- A falsification needs concrete, auditable evidence.
- Commit often with detailed messages so the next agent can pick up cleanly.
