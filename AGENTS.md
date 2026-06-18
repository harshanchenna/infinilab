# AGENTS.md — you are the research loop

You are an agent (Claude Code, Codex, or a human at a terminal) resuming
**infinilab** from nothing but this repo. Everything needed is in git. **You** are
the loop: you propose, you scrutinise, and you record. The repo gives you the
un-gameable bookkeeping (`lab.py`); you bring the creativity. Nothing here shells
out to an LLM — it works in any harness.

## What this is
A **project-agnostic** autoresearch loop with a hard, un-gameable verifier
(FunSearch / AlphaEvolve / Karpathy-autoresearch lineage). A candidate is kept
only if a cheap, rigorous program scores it better than the best so far. The
generic engine lives in `harness/`; each problem is a **project** under
`projects/<name>/`. See `README.md` for architecture and `docs/opportunities.md`
for which problems suit this loop.

## Pick the active project
Set `INFINILAB_PROJECT=projects.<name>` (default `projects.riemann`). Everything
else — tracks, state, prompts, experiments, lib — resolves from it. Current:
- `projects.riemann` — Riemann Hypothesis (mature: 15 iterations, 8 tracks, a
  certified zero-verification tier, a de Bruijn–Newman bound). Mostly
  reproduction-grade — RH has no cheap scalar to push.
- `projects.cap_set` — cap sets in F_3^n (the canonical FunSearch problem: evolve
  a `priority` function for a greedy constructor; `is_cap` is the rigorous spine).

## Read the state first (in this order)
For the active project `projects/<name>/`:
1. `program.md` — goal, rules, track portfolio, current focus.
2. `state/frontier.json` — best result per `track::metric` (the leaderboard).
3. `state/knowledge_base.md` — vetted facts.
4. `state/ledger.jsonl` — append-only history of every attempt.
5. `journal/NNNN-*.md` — a writeup per kept iteration.
6. `experiments/exp_*.py` — every experiment ever proposed.
7. `research/` — literature grounding + `meta_log.md` (process self-optimization).
8. `prompts/` — your role prompts: `proposer.md`, `skeptic.md`, `scout.md`,
   `meta.md`, and (cap_set) `evolve.md`.

## One iteration (the playbook you run yourself)
```bash
pip install -e .                 # mpmath, numpy, sympy
python lab.py status             # 0. read the frontier + recent ledger
python lab.py next               # filename + module name for the next experiment
```
1. **Propose** (you = proposer; read `prompts/proposer.md`). Pick a track and a
   frontier to push. Write a NEW `projects/<name>/experiments/exp_NNNN_<slug>.py`
   satisfying the contract in `harness/experiment.py`: a `MANIFEST` dict and a
   `run(budget_seconds) -> dict` built via `harness.experiment.result(...)`.
   Compose ONLY trusted primitives from `projects/<name>/lib/`. Set `novelty`
   honestly (reproduction / frontier-search / conjecture / falsification-attempt).
2. **Verify** (Tier-1, hard): `python lab.py verify <module>`. It runs your
   experiment in a subprocess and prints the numbers. If it says the result would
   advance the frontier, go to step 3; otherwise you may record directly.
3. **Scrutinise** (Tier-2, you = skeptic; read `prompts/skeptic.md`). For any
   frontier-advancing result or claimed falsification, adversarially check the
   claim: overclaiming, numerical artifacts, metric gaming, novelty overclaim.
   Reach a verdict: `sound` | `overclaimed` | `flawed`.
4. **Record**: `python lab.py record <module> --skeptic sound` (or
   `overclaimed`/`flawed`, with `--notes "…"`). The keeping rule promotes only
   `sound` results that strictly advance a frontier (or falsifications with
   evidence). Kept results auto-write the journal + knowledge base.
5. **Commit & push** every iteration so the next agent resumes cleanly:
   ```bash
   git add -A && git commit -m "iter NNNN: … [track]" && git push
   ```

## FunSearch evolution (cap_set, and future construction projects)
When a project defines an `EVOLVE` spec (cap_set does), you evolve a small
`priority` function rather than writing a fresh experiment each time:
```bash
python lab.py evolve status                 # islands + best scores
python lab.py evolve sample --k 2           # parent programs to learn from
#   ... write a NEW priority program (read prompts/evolve.md) ...
python lab.py evolve eval path/to/prog.py   # rigorous score; registers if it runs
python lab.py evolve best                   # current champion per dimension
```
The evaluator is the un-gameable spine (`is_cap` audits every construction).
Promote a champion into the frontier by writing a one-line experiment that runs
it and `record`-ing, as usual.

## Invariants
- `harness/` and a project's `lib/` are the trusted spine; never edit them to
  make a result pass.
- Claims must be entailed by the numbers. Prefer honest nulls to overclaims.
- A falsification needs concrete, auditable evidence.
- Commit AND push often, with detailed messages, so the next agent picks up cold.

## Add a new project
Create `projects/<name>/` with: `project.py` (NAME, CONJECTURE, TRACKS; optional
`EVOLVE`), `lib/` (trusted primitives = the rigorous verifier), `prompts/`,
`program.md`, `experiments/__init__.py`. The engine creates `state/` and
`journal/` on first record.

## Automated alternative (optional)
`loop.py` is a legacy self-driving wrapper that shells out to the `claude` CLI to
play these roles unattended. Prefer the agent-driven `lab.py` flow above; use
`loop.py` only for hands-off batch runs where the `claude` binary is available.
