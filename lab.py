#!/usr/bin/env python3
"""lab -- the agent-driven infinilab CLI (deterministic mechanics only).

You (the agent: Claude Code, Codex, or a human) ARE the research loop. This CLI
gives you the un-gameable bookkeeping; you supply the creativity. No language
model is invoked here -- nothing shells out to any LLM. Read AGENTS.md for the
one-iteration playbook.

    python lab.py status                       Frontier + recent ledger.
    python lab.py next                          Next iteration number + filename hint.
    python lab.py verify  <module> [--budget S] Tier-1 verify only; print the numbers.
    python lab.py record  <module> [--budget S] [--skeptic V] [--notes T]
                                                Verify + apply keeping rules + journal/KB.
    python lab.py evolve  <sample|eval|best> …  FunSearch program evolution (if the
                                                active project defines an EVOLVE spec).

Select the active project with INFINILAB_PROJECT=projects.<name> (default
projects.riemann). State lives in git under the project, so any agent can resume
from a fresh clone.
"""
from __future__ import annotations

import argparse
import json
import os
import sys

from harness import driver
from harness import ledger as Ledger
from harness import project as P

DEFAULT_BUDGET = driver.DEFAULT_BUDGET


def cmd_status(args) -> int:
    print(driver.status_text())
    return 0


def cmd_next(args) -> int:
    n = Ledger.next_iteration_number()
    rel = os.path.relpath(P.path("experiments"), driver.ROOT)
    print(f"next iteration: {n}")
    print(f"create:        {rel}/exp_{n:04d}_<slug>.py")
    print(f"module:        {P.EXPERIMENTS_PKG}.exp_{n:04d}_<slug>")
    return 0


def cmd_verify(args) -> int:
    from harness import verify as V
    v = V.verify(args.module, args.budget)
    print(v.summary())
    if v.result:
        # Print the numbers so the agent can scrutinise the claim itself.
        print(json.dumps({"metrics": v.result["metrics"],
                          "frontier_metric": v.result["frontier_metric"],
                          "frontier_value": v.result["frontier_value"],
                          "novelty": v.result["novelty"],
                          "falsified": v.result["falsified"]}, indent=2))
        if driver.needs_skeptic(v):
            print("\nThis result would ADVANCE the frontier (or claims a "
                  "falsification): run the Tier-2 skeptic step (prompts/skeptic.md) "
                  "before `record`, and pass --skeptic sound|overclaimed|flawed.")
    elif v.error:
        print(v.error)
    return 0 if v.ok else 1


def cmd_record(args) -> int:
    verdict, rec = driver.record(args.module, skeptic_verdict=args.skeptic,
                                 skeptic_notes=args.notes, budget=args.budget)
    print(verdict.summary())
    print(f"ledger #{rec.iteration}: kept={rec.kept} advanced={rec.advanced_frontier} "
          f"falsified={rec.falsified} skeptic={rec.skeptic_verdict or 'n/a'}")
    if rec.kept:
        print("KEPT -> journal + knowledge_base updated. Commit and push the state.")
    elif driver.needs_skeptic(verdict) and args.skeptic in (None, "sound"):
        print("Note: advanced the frontier but was NOT kept -- check the verdict above.")
    return 0


def cmd_evolve(args) -> int:
    try:
        from harness import evolve
    except Exception as e:  # pragma: no cover
        print(f"evolve unavailable: {e}", file=sys.stderr)
        return 2
    return evolve.cli(args)


def main(argv: list[str]) -> int:
    p = argparse.ArgumentParser(prog="lab.py", description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)

    sub.add_parser("status", help="frontier + recent ledger")
    sub.add_parser("next", help="next iteration number + filename hint")

    pv = sub.add_parser("verify", help="Tier-1 verify only")
    pv.add_argument("module")
    pv.add_argument("--budget", type=float, default=DEFAULT_BUDGET)

    pr = sub.add_parser("record", help="verify + keeping rules + journal/KB")
    pr.add_argument("module")
    pr.add_argument("--budget", type=float, default=DEFAULT_BUDGET)
    pr.add_argument("--skeptic", choices=["sound", "overclaimed", "flawed"], default=None,
                    help="Tier-2 verdict the agent reached (omit for None=promotable)")
    pr.add_argument("--notes", default=None, help="one-line skeptic rationale")

    pe = sub.add_parser("evolve", help="FunSearch program evolution")
    pe.add_argument("action", choices=["sample", "eval", "best", "status"])
    pe.add_argument("program", nargs="?", help="program file (for eval)")
    pe.add_argument("--island", type=int, default=None)
    pe.add_argument("--k", type=int, default=2, help="parents to sample")
    pe.add_argument("--budget", type=float, default=60.0)

    args = p.parse_args(argv)
    return {
        "status": cmd_status,
        "next": cmd_next,
        "verify": cmd_verify,
        "record": cmd_record,
        "evolve": cmd_evolve,
    }[args.cmd](args)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
