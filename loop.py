#!/usr/bin/env python3
"""infinilab AUTOMATED driver (legacy) -- the self-driving forever-loop.

PREFER `lab.py` + AGENTS.md. The recommended way to run infinilab is now
agent-driven: an agent (Claude Code, Codex, a human) reads AGENTS.md and drives
the deterministic `lab.py` CLI itself, with its own tools. That works in any
harness and needs no `claude` subprocess.

This module is the *automated* alternative: it shells out to the `claude` CLI to
play the proposer/scout/meta roles unattended. Keep it for hands-off batch runs;
it depends on the `claude` binary being installed. One iteration:

    propose -> verify (Tier-1, hard) -> skeptic (Tier-2, soft) -> record -> commit

    python loop.py step                   One full propose->...->commit cycle.
    python loop.py loop [--max N]         Run cycles forever (or N times).
    python loop.py record <module> [--no-skeptic]   (delegates to harness.driver)

Models via env: INFINILAB_PROPOSER_MODEL (sonnet), INFINILAB_SKEPTIC_MODEL
(opus). Everything needed to resume lives in git: experiments/, state/, journal/.
"""
from __future__ import annotations

import argparse
import glob
import json
import os
import re
import subprocess
import sys
import time

from harness import verify as V
from harness import ledger as Ledger
from harness import skeptic as Skeptic
from harness import experiment as E
from harness import project as P
from harness import driver as D

ROOT = os.path.dirname(os.path.abspath(__file__))            # repo root (engine)
PROJECT_DIR = P.DIR                                          # active project dir
EXPERIMENTS_DIR = P.path("experiments")
JOURNAL_DIR = P.path("journal")
EXPERIMENTS_PKG = P.EXPERIMENTS_PKG                          # dotted module prefix
PROPOSER_MODEL = os.environ.get("INFINILAB_PROPOSER_MODEL", "sonnet")
BUDGET = 300.0


# --------------------------------------------------------------------------- #
# Recording a verified experiment
# --------------------------------------------------------------------------- #
def record(module: str, run_skeptic: bool = True, budget: float = BUDGET) -> Ledger.Iteration:
    """Verify an experiment module, run the (claude) skeptic if it passed and
    advances, then delegate ledger/journal/KB bookkeeping to harness.driver.

    The deterministic mechanics live in harness.driver (shared with lab.py); the
    only thing this automated path adds is shelling out to the claude skeptic.
    """
    print(f"-> verifying {module} (budget {budget:.0f}s)")
    verdict = V.verify(module, budget)
    print("   " + verdict.summary())

    skeptic_verdict = skeptic_notes = None
    if run_skeptic and D.needs_skeptic(verdict):
        print(f"-> skeptic ({Skeptic.SKEPTIC_MODEL}) reviewing claim ...")
        skeptic_verdict, skeptic_notes = Skeptic.review(module, verdict)
        print(f"   skeptic: {skeptic_verdict} -- {(skeptic_notes or '')[:120]}")

    rec = Ledger.consider(verdict, skeptic_verdict, skeptic_notes)
    print(f"   ledger #{rec.iteration}: kept={rec.kept} advanced={rec.advanced_frontier}")
    if rec.kept:
        path = D.write_journal(rec, verdict)
        D.update_knowledge_base(rec)
        print(f"   journal: {os.path.relpath(path, ROOT)}")
    return rec


# --------------------------------------------------------------------------- #
# Proposing a new experiment (the cheap coding agent)
# --------------------------------------------------------------------------- #
def propose(budget: float = BUDGET) -> str | None:
    """Invoke the proposer model to write the next experiment file.

    Returns the dotted module path of the new experiment, or None on failure.
    """
    n = Ledger.next_iteration_number()
    expected_prefix = f"exp_{n:04d}_"
    context = _proposer_context()
    rel_exp = os.path.relpath(EXPERIMENTS_DIR, ROOT)   # e.g. projects/riemann/experiments
    rel_proj = os.path.relpath(PROJECT_DIR, ROOT)      # e.g. projects/riemann
    with open(P.path("prompts", "proposer.md")) as f:
        system = f.read()

    task = (
        f"Active project: {P.NAME} ({P.CONJECTURE}). Write the next experiment as a "
        f"NEW file {rel_exp}/{expected_prefix}<slug>.py (slug = short snake_case name). "
        f"It MUST satisfy the contract in harness/experiment.py: a MANIFEST dict and a "
        f"run(budget_seconds)->dict built via harness.experiment.result(). Compose only "
        f"trusted primitives from {rel_proj}/lib/ and read this project's notes under "
        f"{rel_proj}/research/ and {rel_proj}/program.md. Pick a track and a frontier to "
        f"push, given the current state below. Do not edit anything under harness/ or "
        f"{rel_proj}/lib/. After writing, stop.\n\n"
        f"=== CURRENT STATE ===\n{context}\n"
    )

    # Headless file writing needs a non-interactive permission mode. We default
    # to acceptEdits (auto-approve file writes), which -- unlike
    # --dangerously-skip-permissions -- is allowed when running as root. Override
    # with INFINILAB_PERMISSION_MODE if desired.
    perm_mode = os.environ.get("INFINILAB_PERMISSION_MODE", "acceptEdits")
    cmd = ["claude", "-p", task, "--model", PROPOSER_MODEL,
           "--permission-mode", perm_mode,
           "--append-system-prompt", system]

    print(f"-> proposer ({PROPOSER_MODEL}) writing {expected_prefix}*.py ...")
    try:
        subprocess.run(cmd, cwd=ROOT, timeout=900, text=True, stdin=subprocess.DEVNULL)
    except (FileNotFoundError, subprocess.TimeoutExpired) as e:
        print(f"   proposer failed: {e}")
        return None

    matches = sorted(glob.glob(os.path.join(EXPERIMENTS_DIR, expected_prefix + "*.py")))
    if not matches:
        print(f"   proposer produced no {expected_prefix}*.py file")
        return None
    module = EXPERIMENTS_PKG + "." + os.path.splitext(os.path.basename(matches[-1]))[0]
    print(f"   proposer wrote {module}")
    return module


def _proposer_context() -> str:
    frontier = Ledger.load_frontier()
    recent = _tail_ledger(8)
    existing = sorted(os.path.basename(p) for p in glob.glob(os.path.join(EXPERIMENTS_DIR, "exp_*.py")))
    return json.dumps({
        "tracks": E.TRACKS,
        "frontier": frontier,
        "recent_iterations": recent,
        "existing_experiments": existing,
    }, indent=2)


def _tail_ledger(k: int) -> list:
    return D.tail_ledger(k)


# --------------------------------------------------------------------------- #
# Literature grounding (scout) and process self-optimization (meta)
# --------------------------------------------------------------------------- #
def _invoke_agent(prompt_file: str, task: str, model: str, timeout: int = 1200) -> bool:
    """Run a claude agent in the repo with a role prompt + task. Returns success."""
    with open(P.path("prompts", prompt_file)) as f:
        system = f.read()
    perm_mode = os.environ.get("INFINILAB_PERMISSION_MODE", "acceptEdits")
    cmd = ["claude", "-p", task, "--model", model,
           "--permission-mode", perm_mode, "--append-system-prompt", system]
    try:
        subprocess.run(cmd, cwd=ROOT, timeout=timeout, text=True, stdin=subprocess.DEVNULL)
        return True
    except (FileNotFoundError, subprocess.TimeoutExpired) as e:
        print(f"   agent failed: {e}")
        return False


def scout(focus: str) -> None:
    """Literature grounding pass: ingest cited findings into the project's research/."""
    model = os.environ.get("INFINILAB_SCOUT_MODEL", "sonnet")
    rel = os.path.relpath(PROJECT_DIR, ROOT)
    print(f"-> scout ({model}) on focus: {focus!r}")
    task = (
        f"Active project: {P.NAME}. Scout focus: {focus}. Use web search/fetch to find "
        f"credible, cited findings and integrate them into this project's research notes "
        f"under {rel}/research/. Every claim needs a source. End with candidate next "
        f"experiments tied to our tracks. Edit only files under {rel}/research/."
    )
    if _invoke_agent("scout.md", task, model):
        _git_commit_paths([os.path.join(rel, "research")], f"scout: ground research on {focus}")


def meta() -> None:
    """Process self-optimization pass: improve prompts/harness/tracks from history."""
    model = os.environ.get("INFINILAB_META_MODEL", "opus")
    rel = os.path.relpath(PROJECT_DIR, ROOT)
    print(f"-> meta ({model}) reviewing loop history")
    task = (
        f"Active project: {P.NAME}. Run a meta-optimization pass. Read {rel}/state/ledger.jsonl, "
        f"{rel}/state/frontier.json, {rel}/journal/, and {rel}/research/. Identify the single "
        f"highest-value process improvement (a stalled track, a method the skeptic keeps "
        f"flagging, a missing project lib primitive, prompt drift), make that change per your "
        f"governance rules, and append a dated entry to {rel}/research/meta_log.md. Prefer one "
        f"sharp, reversible change."
    )
    if _invoke_agent("meta.md", task, model):
        _git_commit_paths(["."], "meta: self-optimization pass")


def _git_commit_paths(paths: list[str], subject: str) -> None:
    try:
        subprocess.run(["git", "add"] + paths, cwd=ROOT, check=True)
        # Only commit if something actually changed.
        diff = subprocess.run(["git", "diff", "--cached", "--quiet"], cwd=ROOT)
        if diff.returncode == 0:
            print("   (no changes to commit)")
            return
        subprocess.run(["git", "commit", "-q", "-m", subject], cwd=ROOT, check=True)
        print(f"   committed: {subject}")
    except subprocess.CalledProcessError as e:
        print(f"   git commit skipped: {e}")


# --------------------------------------------------------------------------- #
# One full cycle and the forever loop
# --------------------------------------------------------------------------- #
def step(budget: float = BUDGET) -> bool:
    module = propose(budget)
    if not module:
        return False
    rec = record(module, run_skeptic=True, budget=budget)
    _git_commit(module, rec)
    return True


def loop(max_iter: int | None = None, budget: float = BUDGET) -> None:
    # Periodically ground in the literature (scout) and self-optimize (meta), so
    # the loop stays literature-aware and improves its own process -- not just a
    # blind numerical search. Cadence is configurable.
    scout_every = int(os.environ.get("INFINILAB_SCOUT_EVERY", "8"))
    meta_every = int(os.environ.get("INFINILAB_META_EVERY", "10"))
    scout_foci = ["zero_verification", "li_criterion", "de_bruijn_newman",
                  "robin_inequality", "explicit_formula", "the autoresearch landscape itself"]
    i = 0
    while max_iter is None or i < max_iter:
        i += 1
        print(f"\n===== cycle {i} =====")
        if scout_every and i % scout_every == 1 and i > 1:
            scout(scout_foci[(i // scout_every) % len(scout_foci)])
        ok = step(budget)
        if not ok:
            print("cycle produced nothing; backing off 30s")
            time.sleep(30)
        if meta_every and i % meta_every == 0:
            meta()
    print("loop done")


def _git_commit(module: str, rec: Ledger.Iteration) -> None:
    short = module.split(".")[-1]
    verb = "KEEP" if rec.kept else "log"
    subject = f"iter {rec.iteration:04d}: {verb} {short} [{rec.track or '?'}]"
    body = (
        f"status={rec.status} kept={rec.kept} advanced={rec.advanced_frontier} "
        f"falsified={rec.falsified}\n"
        f"frontier: {rec.frontier_metric}={rec.frontier_value}\n"
        f"skeptic: {rec.skeptic_verdict or 'n/a'}"
        + (f" -- {rec.skeptic_notes}" if rec.skeptic_notes else "")
        + f"\nclaim: {rec.claim or ''}\n"
    )
    try:
        subprocess.run(["git", "add", "-A"], cwd=ROOT, check=True)
        subprocess.run(["git", "commit", "-q", "-m", subject, "-m", body], cwd=ROOT, check=True)
        print(f"   committed: {subject}")
    except subprocess.CalledProcessError as e:
        print(f"   git commit skipped: {e}")


def cmd_status() -> None:
    print(D.status_text())


def main(argv: list[str]) -> int:
    p = argparse.ArgumentParser(prog="loop.py")
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("status")
    pr = sub.add_parser("record")
    pr.add_argument("module")
    pr.add_argument("--no-skeptic", action="store_true")
    pr.add_argument("--budget", type=float, default=BUDGET)
    ps = sub.add_parser("step")
    ps.add_argument("--budget", type=float, default=BUDGET)
    pl = sub.add_parser("loop")
    pl.add_argument("--max", type=int, default=None)
    pl.add_argument("--budget", type=float, default=BUDGET)
    psc = sub.add_parser("scout")
    psc.add_argument("focus", nargs="?", default="the autoresearch landscape itself")
    sub.add_parser("meta")
    args = p.parse_args(argv)

    if args.cmd == "status":
        cmd_status()
    elif args.cmd == "record":
        record(args.module, run_skeptic=not args.no_skeptic, budget=args.budget)
    elif args.cmd == "step":
        step(args.budget)
    elif args.cmd == "loop":
        loop(args.max, args.budget)
    elif args.cmd == "scout":
        scout(args.focus)
    elif args.cmd == "meta":
        meta()
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
