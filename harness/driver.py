"""Deterministic loop mechanics -- the agent-driven core.

This module is the un-gameable bookkeeping of the loop: verify an experiment
(Tier-1), apply the keeping rules (ledger/frontier), and -- only for kept
results -- write the journal entry and knowledge-base line. There is NO language
model and NO `claude` subprocess here.

That is the whole point of the refactor: the *driving agent* (Claude Code,
Codex, or a human at a REPL) is itself the proposer and the skeptic. It uses its
own tools to write an experiment and to scrutinise a claim, then calls these
functions (via `lab.py`) to record the outcome honestly. The mechanics that must
not be talked past live here; the creative parts live in the agent + prompts.
"""
from __future__ import annotations

import json
import os

from harness import verify as V
from harness import ledger as Ledger
from harness import project as P

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))   # repo root
JOURNAL_DIR = P.path("journal")
DEFAULT_BUDGET = 300.0


# --------------------------------------------------------------------------- #
# Record a verified experiment (verify -> consider -> journal/KB)
# --------------------------------------------------------------------------- #
def record(module: str, skeptic_verdict: str | None = None,
           skeptic_notes: str | None = None,
           budget: float = DEFAULT_BUDGET) -> tuple[V.Verdict, Ledger.Iteration]:
    """Verify `module`, apply keeping rules, and (if kept) write journal + KB.

    `skeptic_verdict` is supplied by the driving agent. The agent should run the
    Tier-2 skeptic step (scrutinise the claim per prompts/skeptic.md) for any
    result that advances a frontier or claims a falsification, and pass the
    verdict here: "sound" promotes, "overclaimed"/"flawed" blocks promotion. A
    None verdict is treated as promotable (used for cheap reproductions that do
    not advance anything, or when the agent vouches for the claim inline).
    """
    verdict = V.verify(module, budget)
    rec = Ledger.consider(verdict, skeptic_verdict, skeptic_notes)
    if rec.kept:
        write_journal(rec, verdict)
        update_knowledge_base(rec)
    return verdict, rec


def needs_skeptic(verdict: V.Verdict) -> bool:
    """True iff this result is worth the agent's Tier-2 scrutiny: it passed the
    spine AND would advance a frontier or claims a falsification."""
    if not (verdict.ok and verdict.result):
        return False
    r = verdict.result
    if r["falsified"]:
        return True
    prev = Ledger.frontier_value(r["track"], r["frontier_metric"])
    return prev is None or r["frontier_value"] > prev


def write_journal(rec: Ledger.Iteration, verdict: V.Verdict) -> str:
    os.makedirs(JOURNAL_DIR, exist_ok=True)
    path = os.path.join(JOURNAL_DIR, f"{rec.iteration:04d}-{rec.module.split('.')[-1]}.md")
    m = verdict.manifest or {}
    r = verdict.result or {}
    lines = [
        f"# Iteration {rec.iteration:04d} -- {m.get('title', rec.module)}",
        "",
        f"- **module**: `{rec.module}`",
        f"- **track**: `{rec.track}`  |  **novelty**: {rec.novelty}",
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
    return path


def update_knowledge_base(rec: Ledger.Iteration) -> None:
    tag = "FALSIFICATION! " if rec.falsified else ""
    entry = (
        f"- **[{rec.track}]** {tag}{rec.claim} "
        f"(iter {rec.iteration}, `{rec.module.split('.')[-1]}`, "
        f"{rec.frontier_metric}={rec.frontier_value:g}, skeptic={rec.skeptic_verdict or 'n/a'})"
    )
    Ledger.append_knowledge(entry)


# --------------------------------------------------------------------------- #
# Read-only views (status, ledger tail) -- used by `lab.py status`
# --------------------------------------------------------------------------- #
def tail_ledger(k: int) -> list[dict]:
    path = Ledger.LEDGER_PATH
    if not os.path.exists(path):
        return []
    with open(path) as f:
        rows = [json.loads(line) for line in f if line.strip()]
    keys = ("iteration", "module", "status", "track", "novelty",
            "frontier_value", "kept", "skeptic_verdict")
    return [{kk: r.get(kk) for kk in keys} for r in rows[-k:]]


def status_text(ledger_n: int = 10) -> str:
    frontier = Ledger.load_frontier()
    out = [f"PROJECT: {P.NAME} -- {P.CONJECTURE}", "",
           "FRONTIER (best per track::metric):"]
    if not frontier:
        out.append("  (empty)")
    for key, info in sorted(frontier.items()):
        label = f"{info.get('track','?')}::{info['frontier_metric']}"
        out.append(f"  {label:46s} {info['frontier_value']:g} "
                   f"(iter {info['iteration']}, {'FALSIFIED' if info.get('falsified') else 'ok'})")
    out += ["", "RECENT LEDGER:"]
    for r in tail_ledger(ledger_n):
        out.append(f"  #{r['iteration']:>3} {r['status']:<13} {r.get('track') or '-':18} "
                   f"kept={r['kept']} skeptic={r.get('skeptic_verdict')}")
    return "\n".join(out)
