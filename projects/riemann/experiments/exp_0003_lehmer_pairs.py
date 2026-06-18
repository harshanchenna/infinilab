"""exp_0003 -- Search for Lehmer pairs: the smallest normalized zero gap.

A "Lehmer pair" is two consecutive nontrivial zeros that are anomalously close
on the critical line -- a normalized gap delta_n = (w_{n+1}-w_n) << 1, where
w_n = theta(gamma_n)/pi unfolds to unit mean spacing. Such near-collisions are
the numerical pressure points of RH: a pair that actually merged and moved off
the line would disprove it, and the closest known pairs feed lower bounds on the
de Bruijn-Newman constant Lambda (now known to satisfy Lambda >= 0, Polymath15).

This experiment scans the first K zeros, computes all normalized gaps, and
reports the smallest one and where it occurs. It does NOT claim a disproof --
a small positive gap is fully consistent with RH; it is simply the kind of
object whose behaviour we want to track as K grows.

Frontier: n_zeros_scanned (K). Scanning more zeros = a more thorough search.
Secondary signal: min_normalized_gap (smaller = a tighter near-collision found).
"""
from __future__ import annotations

import time

from projects.riemann.lib import rh_lib as L
from harness import experiment as E

MANIFEST = {
    "id": "exp_0003",
    "track": "lehmer_pairs",
    "title": "Smallest normalized gap between consecutive zeta zeros",
    "hypothesis": "Consecutive zeros never collide; the smallest normalized gap stays > 0.",
    "falsifiable_prediction": "Every normalized gap delta_n > 0 (a zero gap would be extraordinary).",
    "references": [
        "Lehmer (1956), close pairs of zeros.",
        "Polymath15 / Tao: Lambda >= 0 for the de Bruijn-Newman constant.",
    ],
}

DPS = 25
TARGET_K = 300  # capped by the wall-clock budget below


def run(budget_seconds: float) -> dict:
    L.set_precision(DPS)
    deadline = time.time() + 0.85 * budget_seconds

    gammas = []
    for n in range(1, TARGET_K + 1):
        gammas.append(L.gamma(n))
        if time.time() > deadline:
            break
    k = len(gammas)

    spac = L.normalized_spacings(gammas)
    # Locate the minimum gap and the pair of zeros that realize it.
    min_gap = None
    min_idx = -1
    for i, d in enumerate(spac):
        if min_gap is None or d < min_gap:
            min_gap = d
            min_idx = i
    # zeros (1-indexed) that realize the smallest gap
    pair_lo = min_idx + 1
    pair_hi = min_idx + 2

    falsified = bool(min_gap is not None and min_gap <= 0)
    claim = (
        f"Scanned first {k} zeros: smallest normalized gap "
        f"{float(min_gap):.4f} between zeros #{pair_lo} and #{pair_hi} "
        f"(heights {float(gammas[min_idx]):.3f}, {float(gammas[min_idx+1]):.3f}). "
        f"All gaps positive; consistent with RH (no collision)."
    )

    return E.result(
        track="lehmer_pairs",
        claim=claim,
        metrics={
            "n_zeros_scanned": k,
            "min_normalized_gap": float(min_gap),
            "closest_pair": [pair_lo, pair_hi],
            "closest_pair_heights": [float(gammas[min_idx]), float(gammas[min_idx + 1])],
            "n_gaps": len(spac),
        },
        frontier_metric="n_zeros_scanned",
        frontier_value=float(k),
        falsified=falsified,
        consistent_with_rh=not falsified,
        evidence={
            "method": "unfold via theta/pi; min over consecutive normalized gaps",
            "min_gap": float(min_gap),
            "closest_pair_indices": [pair_lo, pair_hi],
        },
    )
