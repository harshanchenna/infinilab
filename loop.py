#!/usr/bin/env python3
"""infinilab driver -- the forever-loop.

Modeled on Karpathy's autoresearch loop, adapted from "optimize one training
script" to "grow a verified library of RH experiments". One iteration:

    propose -> verify (Tier-1, hard) -> skeptic (Tier-2, soft) -> record -> commit

Subcommands
-----------
    python loop.py status                 Show the frontier and recent ledger.
    python loop.py record <module> [--no-skeptic]
                                          Verify+record an existing experiment
                                          (used to seed, or to re-run one).
    python loop.py step                   One full propose->...->commit cycle.
    python loop.py loop [--max N]         Run cycles forever (or N times).

The proposer is a cheap model (Sonnet) that WRITES a new experiments/exp_*.py.
The skeptic is a stronger model (Opus) that only vets the claim. Models are set
via env: INFINILAB_PROPOSER_MODEL (default sonnet), INFINILAB_SKEPTIC_MODEL
(default opus).

Everything the loop needs to resume lives in git: experiments/, state/, and
journal/. A fresh LLM can read AGENTS.md + state/ and continue.
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

ROOT = os.path.dirname(os.path.abspath(__file__))
EXPERIMENTS_DIR = os.path.join(ROOT, "experiments")
JOURNAL_DIR = os.path.join(ROOT, "journal")
PROPOSER_MODEL = os.environ.get("INFINILAB_PROPOSER_MODEL", "sonnet")
BUDGET = 300.0


# --------------------------------------------------------------------------- #
# Recording a verified experiment
# --------------------------------------------------------------------------- #
def record(module: str, run_skeptic: bool = True, budget: float = BUDGET) -> Ledger.Iteration:
    """Verify an experiment module, run the skeptic if it passed and advances,
    update the ledger/frontier, and write a journal entry if kept."""
    print(f"-> verifying {module} (budget {budget:.0f}s)")
    verdict = V.verify(module, budget)
    print("   " + verdict.summary())

    skeptic_verdict = skeptic_notes = None
    # Only spend skeptic tokens when the result actually matters (passed Tier-1
    # and would change the frontier or is a falsification).
    if run_skeptic and verdict.ok and verdict.result:
        prev = Ledger.frontier_value(verdict.result["track"])
        worth_review = (
            verdict.result["falsified"]
            or prev is None
            or verdict.result["frontier_value"] > prev
        )
        if worth_review:
            print(f"-> skeptic ({Skeptic.SKEPTIC_MODEL}) reviewing claim ...")
            skeptic_verdict, skeptic_notes = Skeptic.review(module, verdict)
            print(f"   skeptic: {skeptic_verdict} -- {(skeptic_notes or '')[:120]}")

    rec = Ledger.consider(verdict, skeptic_verdict, skeptic_notes)
    print(f"   ledger #{rec.iteration}: kept={rec.kept} advanced={rec.advanced_frontier}")

    if rec.kept:
        _write_journal(rec, verdict)
        _update_knowledge_base(rec, verdict)
    return rec


def _write_journal(rec: Ledger.Iteration, verdict: V.Verdict) -> None:
    os.makedirs(JOURNAL_DIR, exist_ok=True)
    path = os.path.join(JOURNAL_DIR, f"{rec.iteration:04d}-{rec.module.split('.')[-1]}.md")
    m = verdict.manifest or {}
    r = verdict.result or {}
    lines = [
        f"# Iteration {rec.iteration:04d} -- {m.get('title', rec.module)}",
        "",
        f"- **module**: `{rec.module}`",
        f"- **track**: `{rec.track}`",
        f"- **status**: {rec.status}  |  **kept**: {rec.kept}  |  **falsified**: {rec.falsified}",
        f"- **frontier**: {rec.frontier_metric} = {rec.frontier_value}",
        f"- **skeptic**: {rec.skeptic_verdict or 'n/a'}"
        + (f" -- {rec.skeptic_notes}" if rec.skeptic_notes else ""),
        f"- **elapsed**: {rec.elapsed_seconds:.1f}s",
        "",
        "## Hypothesis",
        m.get("hypothesis", "(none)"),
        "",
        "## Claim (entailed by the numbers)",
        r.get("claim", "(none)"),
        "",
        "## Metrics",
        "```json",
        json.dumps(r.get("metrics", {}), indent=2),
        "```",
        "",
        "## Evidence",
        "```json",
        json.dumps(r.get("evidence", {}), indent=2),
        "```",
    ]
    with open(path, "w") as f:
        f.write("\n".join(lines) + "\n")
    print(f"   journal: {os.path.relpath(path, ROOT)}")


def _update_knowledge_base(rec: Ledger.Iteration, verdict: V.Verdict) -> None:
    tag = "FALSIFICATION! " if rec.falsified else ""
    entry = (
        f"- **[{rec.track}]** {tag}{rec.claim} "
        f"(iter {rec.iteration}, `{rec.module.split('.')[-1]}`, "
        f"{rec.frontier_metric}={rec.frontier_value:g}, skeptic={rec.skeptic_verdict or 'n/a'})"
    )
    Ledger.append_knowledge(entry)


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
    with open(os.path.join(ROOT, "prompts", "proposer.md")) as f:
        system = f.read()

    task = (
        f"Write the next experiment as a NEW file "
        f"experiments/{expected_prefix}<slug>.py (slug = short snake_case name). "
        f"It MUST satisfy the contract in harness/experiment.py: a MANIFEST dict "
        f"and a run(budget_seconds)->dict built via harness.experiment.result(). "
        f"Compose only trusted primitives from harness/rh_lib.py. Pick a track "
        f"and a frontier to push, given the current state below. Do not edit "
        f"anything under harness/. After writing, stop.\n\n"
        f"=== CURRENT STATE ===\n{context}\n"
    )

    skip_perms = os.environ.get("INFINILAB_SKIP_PERMISSIONS", "1") == "1"
    cmd = ["claude", "-p", task, "--model", PROPOSER_MODEL,
           "--append-system-prompt", system]
    if skip_perms:
        cmd.append("--dangerously-skip-permissions")

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
    module = "experiments." + os.path.splitext(os.path.basename(matches[-1]))[0]
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
    path = Ledger.LEDGER_PATH
    if not os.path.exists(path):
        return []
    with open(path) as f:
        rows = [json.loads(line) for line in f if line.strip()]
    slim = [{kk: r.get(kk) for kk in ("iteration", "module", "status", "track",
            "frontier_value", "kept", "skeptic_verdict")} for r in rows[-k:]]
    return slim


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
    i = 0
    while max_iter is None or i < max_iter:
        i += 1
        print(f"\n===== cycle {i} =====")
        ok = step(budget)
        if not ok:
            print("cycle produced nothing; backing off 30s")
            time.sleep(30)
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
    frontier = Ledger.load_frontier()
    print("FRONTIER (best per track):")
    if not frontier:
        print("  (empty)")
    for track, info in sorted(frontier.items()):
        print(f"  {track:20s} {info['frontier_metric']}={info['frontier_value']:g} "
              f"(iter {info['iteration']}, {'FALSIFIED' if info.get('falsified') else 'ok'})")
    print("\nRECENT LEDGER:")
    for r in _tail_ledger(10):
        print(f"  #{r['iteration']:>3} {r['status']:<13} {r.get('track') or '-':18} "
              f"kept={r['kept']} skeptic={r.get('skeptic_verdict')}")


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
    args = p.parse_args(argv)

    if args.cmd == "status":
        cmd_status()
    elif args.cmd == "record":
        record(args.module, run_skeptic=not args.no_skeptic, budget=args.budget)
    elif args.cmd == "step":
        step(args.budget)
    elif args.cmd == "loop":
        loop(args.max, args.budget)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
