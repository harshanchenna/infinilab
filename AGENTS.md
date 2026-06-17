# AGENTS.md — how to pick up this project cold

You are an LLM (or a human) resuming infinilab from nothing but this repo.
Everything you need is in git. Read this, then continue the loop.

## What this is
An autoresearch-style **forever-loop** on the Riemann Hypothesis, inspired by
Andrej Karpathy's `autoresearch`. The loop repeatedly: proposes a small
falsifiable experiment, runs it under a hard verifier, has a skeptic vet the
claim, keeps it only if it advances a frontier, and commits. See `program.md`
for the research program and `README.md` for the architecture.

## Where the state lives (read these first, in order)
1. `program.md` — the goal, the rules, the track portfolio, current focus.
2. `state/frontier.json` — the best result per track ("the best"). This is the
   live leaderboard the loop is trying to beat.
3. `state/knowledge_base.md` — skeptic-vetted, reproducible facts kept so far.
4. `state/ledger.jsonl` — append-only history of every iteration attempt
   (kept or not), one JSON object per line.
5. `journal/NNNN-*.md` — a human-readable writeup per *kept* iteration.
6. `experiments/exp_*.py` — every experiment ever proposed (the full search
   tree, in git).

If `state/` and `journal/` agree with the latest `experiments/`, you are in a
consistent state and can continue. If they disagree (e.g. an experiment file
exists with no ledger row), re-run it with `python loop.py record <module>`.

## How to run
```bash
pip install mpmath numpy sympy            # or: pip install -e .
python loop.py status                     # show frontier + recent ledger
python loop.py record experiments.exp_0001_critical_line   # verify+record one
python loop.py step                       # one propose->verify->skeptic->commit
python loop.py loop --max 20              # run 20 cycles (omit --max for forever)
```
Models (env): `INFINILAB_PROPOSER_MODEL` (default `sonnet`),
`INFINILAB_SKEPTIC_MODEL` (default `opus`). The proposer/skeptic shell out to the
`claude` CLI; set `INFINILAB_SKIP_PERMISSIONS=0` to require approval for edits.

## How to extend the research yourself (without the driver)
You can act as the proposer directly:
1. Read `state/frontier.json` and pick a track + frontier to beat.
2. Write `experiments/exp_NNNN_<slug>.py` to the contract in
   `harness/experiment.py` (a `MANIFEST` and `run(budget_seconds)->dict` built
   with `harness.experiment.result(...)`). Compose `harness/rh_lib.py`; never
   edit `harness/`.
3. `python loop.py record experiments.exp_NNNN_<slug>` to verify, vet, record.
4. Commit with a detailed message (see git log for the house style).

## Invariants you must preserve
- `harness/` is the trusted spine; do not edit it to make a result pass.
- Claims are entailed by numbers; never claim to prove RH.
- A falsification needs concrete evidence and will be heavily scrutinized.
- Commit often, with detailed messages, so the next agent can pick up cleanly.
