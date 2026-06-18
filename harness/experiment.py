"""The experiment contract.

Every experiment is a Python module in `experiments/` that defines:

    MANIFEST : dict        # static description of the falsifiable claim
    def run(budget_seconds: float) -> dict   # does the computation, returns a Result

The contract is deliberately small. The Tier-1 verifier (`harness/verify.py`)
imports the module in a subprocess, calls `run()` under a wall-clock budget,
and validates the returned Result. Because the verifier just *executes code and
reads numbers*, it cannot be talked into accepting a false claim -- that is the
whole point of the spine.

A Result dict must contain:

    track            : str    -- which research track (must match a known track)
    claim            : str    -- one-line factual statement, entailed by metrics
    metrics          : dict    -- scalar measurements (json-serializable numbers)
    frontier_metric  : str    -- name of the frontier this experiment pushes
    frontier_value   : float  -- value achieved (higher = more progress)
    falsified        : bool    -- True iff a counterexample to RH (or the tracked
                                  sub-conjecture) was found. This is the jackpot
                                  signal; it must be backed by `evidence`.
    consistent_with_rh : bool  -- True iff results are consistent with RH holding
    evidence         : dict    -- raw data sufficient to reproduce/audit the claim

Helpers below build and validate Result dicts so experiments stay terse.
"""
from __future__ import annotations

import math
from typing import Any

from harness import project as _P

# The research tracks come from the ACTIVE project (harness/project.py), so this
# contract is problem-independent. Adding a track is a deliberate project-level
# decision -- it keeps the frontier well-defined.
TRACKS = _P.TRACKS

# Novelty classes. The loop must privilege genuine-unknown work over reproducing
# known facts. Be honest: most verification experiments are "reproduction".
NOVELTY = {
    "reproduction": "Re-derives a known result; validates machinery, not research.",
    "frontier-search": "Open-ended search whose outcome is genuinely unknown to us.",
    "conjecture": "Proposes a new empirical relation/pattern, tested to high precision.",
    "falsification-attempt": "Actively hunts for a counterexample that would disprove the project's conjecture.",
}

REQUIRED_FIELDS = (
    "track",
    "novelty",
    "claim",
    "metrics",
    "frontier_metric",
    "frontier_value",
    "falsified",
    "consistent_with_goal",
    "evidence",
)


def result(
    *,
    track: str,
    claim: str,
    metrics: dict,
    frontier_metric: str,
    frontier_value: float,
    falsified: bool,
    evidence: dict,
    consistent_with_goal: bool | None = None,
    consistent_with_rh: bool | None = None,  # back-compat alias (riemann project)
    novelty: str = "reproduction",
) -> dict:
    """Build a Result dict, coercing mpmath numbers to plain floats/strings.

    `consistent_with_goal` means the result is consistent with the project's main
    conjecture holding. `consistent_with_rh` is accepted as a legacy alias.
    `novelty` defaults to "reproduction"; genuine frontier work sets it (NOVELTY).
    """
    if consistent_with_goal is None:
        consistent_with_goal = consistent_with_rh
    if consistent_with_goal is None:
        raise ResultError("result() requires consistent_with_goal (or legacy consistent_with_rh)")
    return {
        "track": track,
        "novelty": novelty,
        "claim": claim,
        "metrics": _jsonify(metrics),
        "frontier_metric": frontier_metric,
        "frontier_value": float(frontier_value),
        "falsified": bool(falsified),
        "consistent_with_goal": bool(consistent_with_goal),
        "evidence": _jsonify(evidence),
    }


class ResultError(ValueError):
    """Raised when a Result violates the contract."""


def validate(res: Any) -> dict:
    """Validate a Result dict. Returns it unchanged or raises ResultError."""
    if not isinstance(res, dict):
        raise ResultError(f"Result must be a dict, got {type(res).__name__}")
    for f in REQUIRED_FIELDS:
        if f not in res:
            raise ResultError(f"Result missing required field: {f!r}")
    if res["track"] not in TRACKS:
        raise ResultError(
            f"Unknown track {res['track']!r}; known tracks: {sorted(TRACKS)}"
        )
    if res["novelty"] not in NOVELTY:
        raise ResultError(f"Unknown novelty {res['novelty']!r}; allowed: {sorted(NOVELTY)}")
    fv = res["frontier_value"]
    if not isinstance(fv, (int, float)) or not math.isfinite(fv):
        raise ResultError(f"frontier_value must be a finite number, got {fv!r}")
    if not isinstance(res["metrics"], dict):
        raise ResultError("metrics must be a dict")
    if not isinstance(res["evidence"], dict):
        raise ResultError("evidence must be a dict")
    if res["falsified"] and not res["evidence"]:
        raise ResultError("falsified=True requires non-empty evidence (jackpot must be auditable)")
    # A falsification of the conjecture cannot also be 'consistent with' it.
    if res["falsified"] and res["consistent_with_goal"]:
        raise ResultError("falsified and consistent_with_goal cannot both be True")
    return res


def validate_manifest(manifest: Any) -> dict:
    """Light validation of a module-level MANIFEST."""
    if not isinstance(manifest, dict):
        raise ResultError("MANIFEST must be a dict")
    for f in ("id", "track", "title", "hypothesis"):
        if f not in manifest:
            raise ResultError(f"MANIFEST missing required field: {f!r}")
    if manifest["track"] not in TRACKS:
        raise ResultError(f"MANIFEST has unknown track {manifest['track']!r}")
    return manifest


def _jsonify(obj):
    """Recursively coerce mpmath / numpy scalars to JSON-friendly Python types."""
    import mpmath as mp

    if isinstance(obj, dict):
        return {str(k): _jsonify(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [_jsonify(v) for v in obj]
    if isinstance(obj, (mp.mpf, mp.mpc)):
        # Keep full precision as a string; also useful for audit.
        return mp.nstr(obj, 25)
    if isinstance(obj, bool):
        return obj
    if isinstance(obj, int):
        return obj
    if isinstance(obj, float):
        return obj
    try:
        import numpy as np

        if isinstance(obj, np.generic):
            return obj.item()
    except ImportError:
        pass
    return obj
