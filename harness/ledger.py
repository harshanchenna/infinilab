"""The ledger: durable memory of the loop.

State lives in git-tracked files so the forever-loop is fully resumable from a
fresh container (the whole repo is cloned, state and all):

    state/ledger.jsonl    -- append-only, one JSON record per iteration attempt.
    state/frontier.json   -- best frontier_value achieved per track ("the best").
    state/knowledge_base.md -- human-readable, skeptic-vetted accumulated facts.

"Keeping" semantics (the analog of autoresearch's "commit if it beat best"):
a verified result is KEPT iff it is a FALSIFICATION, or it strictly advances
its track's frontier. Everything else is logged but not promoted, so the loop
never churns the knowledge base with noise.
"""
from __future__ import annotations

import json
import os
import time
from dataclasses import dataclass, asdict
from typing import Optional

STATE_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "state")
LEDGER_PATH = os.path.join(STATE_DIR, "ledger.jsonl")
FRONTIER_PATH = os.path.join(STATE_DIR, "frontier.json")
KB_PATH = os.path.join(STATE_DIR, "knowledge_base.md")


@dataclass
class Iteration:
    iteration: int
    module: str
    status: str               # verifier status
    track: Optional[str]
    novelty: Optional[str]    # reproduction | frontier-search | conjecture | falsification-attempt
    frontier_metric: Optional[str]
    frontier_value: Optional[float]
    advanced_frontier: bool
    kept: bool
    falsified: bool
    claim: Optional[str]
    skeptic_verdict: Optional[str]   # sound | overclaimed | flawed | None (not run)
    skeptic_notes: Optional[str]
    elapsed_seconds: float
    timestamp: float


def _ensure_state() -> None:
    os.makedirs(STATE_DIR, exist_ok=True)
    if not os.path.exists(FRONTIER_PATH):
        _write_json(FRONTIER_PATH, {})


def load_frontier() -> dict:
    _ensure_state()
    try:
        with open(FRONTIER_PATH) as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def next_iteration_number() -> int:
    if not os.path.exists(LEDGER_PATH):
        return 1
    n = 0
    with open(LEDGER_PATH) as f:
        for _ in f:
            n += 1
    return n + 1


def frontier_value(track: str) -> Optional[float]:
    return load_frontier().get(track, {}).get("frontier_value")


def consider(verdict, skeptic_verdict: Optional[str] = None,
             skeptic_notes: Optional[str] = None) -> Iteration:
    """Apply keeping rules to a verifier Verdict, update frontier, append ledger.

    Returns the recorded Iteration. Does NOT itself write journal/KB prose --
    the loop driver does that for kept results, optionally gated by the skeptic.
    """
    _ensure_state()
    it_num = next_iteration_number()

    track = None
    novelty = None
    fmetric = None
    fvalue = None
    claim = None
    falsified = False
    advanced = False
    kept = False

    if verdict.result:
        r = verdict.result
        track = r["track"]
        novelty = r.get("novelty", "reproduction")
        fmetric = r["frontier_metric"]
        fvalue = float(r["frontier_value"])
        claim = r["claim"]
        falsified = bool(r["falsified"])

        frontier = load_frontier()
        prev = frontier.get(track, {}).get("frontier_value")
        advanced = prev is None or fvalue > prev

        # A flawed skeptic verdict blocks promotion even if the number advanced:
        # the spine proved the code ran, but a flawed *interpretation* must not
        # enter the frontier/KB. (Falsifications are never auto-kept silently;
        # they still require evidence, already enforced by the contract.)
        promotable = skeptic_verdict in (None, "sound")
        if (falsified or advanced) and verdict.ok and promotable:
            kept = True
            frontier[track] = {
                "frontier_metric": fmetric,
                "frontier_value": fvalue,
                "module": verdict.module,
                "iteration": it_num,
                "claim": claim,
                "falsified": falsified,
                "updated_at": time.time(),
            }
            _write_json(FRONTIER_PATH, frontier)

    rec = Iteration(
        iteration=it_num,
        module=verdict.module,
        status=verdict.status,
        track=track,
        novelty=novelty,
        frontier_metric=fmetric,
        frontier_value=fvalue,
        advanced_frontier=advanced,
        kept=kept,
        falsified=falsified,
        claim=claim,
        skeptic_verdict=skeptic_verdict,
        skeptic_notes=skeptic_notes,
        elapsed_seconds=verdict.elapsed_seconds,
        timestamp=time.time(),
    )
    with open(LEDGER_PATH, "a") as f:
        f.write(json.dumps(asdict(rec)) + "\n")
    return rec


def append_knowledge(entry: str) -> None:
    """Append a vetted fact to the human-readable knowledge base."""
    _ensure_state()
    header_needed = not os.path.exists(KB_PATH)
    with open(KB_PATH, "a") as f:
        if header_needed:
            f.write("# Knowledge base\n\nSkeptic-vetted, reproducible facts kept by the loop.\n\n")
        f.write(entry.rstrip() + "\n\n")


def _write_json(path: str, obj) -> None:
    tmp = path + ".tmp"
    with open(tmp, "w") as f:
        json.dump(obj, f, indent=2, sort_keys=True)
    os.replace(tmp, path)
