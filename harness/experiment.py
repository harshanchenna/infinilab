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

# The canonical research tracks. The portfolio the loop rotates over.
# Adding a track is a deliberate human/PR-level decision, not something the
# loop does silently -- it keeps the frontier well-defined.
TRACKS = {
    "zero_verification": "All zeros up to height T lie on the critical line (Z sign changes == N(T)).",
    "certified_zero_verification": "Theorem-grade: zeros on the line up to T PROVEN via Arb ball arithmetic.",
    "zero_statistics": "Normalized zero spacings follow GUE (Montgomery-Odlyzko).",
    "lehmer_pairs": "Search for anomalously close zero pairs; smallest normalized gap.",
    "li_criterion": "Li/Keiper coefficients lambda_n are non-negative (lambda_n >= 0 <=> RH).",
    "de_bruijn_newman": "Bounds on the de Bruijn-Newman constant Lambda (RH <=> Lambda <= 0).",
    "explicit_formula": "Riemann's explicit formula linking zeros and primes; residual checks.",
    "robin_inequality": "Robin's inequality sigma(n) < e^gamma n log log n for n > 5040 (<=> RH).",
    "conjecture_discovery": "Search for new closed forms / integer relations among zeros and constants (Ramanujan-Machine style).",
}

# Novelty classes. The loop must privilege genuine-unknown work over reproducing
# known facts. Be honest: most verification experiments are "reproduction".
NOVELTY = {
    "reproduction": "Re-derives a known result; validates machinery, not research.",
    "frontier-search": "Open-ended search whose outcome is genuinely unknown to us.",
    "conjecture": "Proposes a new empirical relation/pattern, tested to high precision.",
    "falsification-attempt": "Actively hunts for a counterexample that would disprove RH (or a sub-conjecture).",
}

REQUIRED_FIELDS = (
    "track",
    "novelty",
    "claim",
    "metrics",
    "frontier_metric",
    "frontier_value",
    "falsified",
    "consistent_with_rh",
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
    consistent_with_rh: bool,
    evidence: dict,
    novelty: str = "reproduction",
) -> dict:
    """Build a Result dict, coercing mpmath numbers to plain floats/strings.

    `novelty` defaults to "reproduction" so older experiments stay valid; genuine
    frontier work must set it explicitly (see NOVELTY).
    """
    return {
        "track": track,
        "novelty": novelty,
        "claim": claim,
        "metrics": _jsonify(metrics),
        "frontier_metric": frontier_metric,
        "frontier_value": float(frontier_value),
        "falsified": bool(falsified),
        "consistent_with_rh": bool(consistent_with_rh),
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
    # A falsification of RH cannot also be 'consistent with RH'.
    if res["falsified"] and res["consistent_with_rh"]:
        raise ResultError("falsified and consistent_with_rh cannot both be True")
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
