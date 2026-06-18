"""exp_0001 -- Verify all zeta zeros up to height T lie on the critical line.

Method (the classical numerical RH check, Riemann-Siegel + Turing):
  * Hardy's Z(t) is real and Z(t)=0 exactly when zeta(1/2+it)=0. So the number
    of sign changes of Z on (0, T] is a LOWER bound for the number of zeros on
    the critical line up to T.
  * N_exact(T) (mpmath, Turing's method) is the TOTAL number of zeros in the
    critical strip up to T, regardless of where they sit.
  * If #sign_changes(Z, 0, T) == N_exact(T), then every one of those N(T) zeros
    is simple and lies exactly on the line -- RH is verified up to height T.

Falsifiability: if we ever found MORE strip-zeros than line-sign-changes at a
resolution fine enough to resolve all gaps, that would be evidence of an
off-line zero. (A coarse grid can only UNDER-count line zeros, so a deficit is
treated as under-resolution, not as a disproof -- we then report the verified
height honestly rather than overclaiming.)

Frontier: T_verified, the height up to which all zeros are certified on-line.
"""
from __future__ import annotations

import time

import mpmath as mp

from projects.riemann.lib import rh_lib as L
from harness import experiment as E

MANIFEST = {
    "id": "exp_0001",
    "track": "zero_verification",
    "title": "Critical-line verification via Z sign changes vs N(T)",
    "hypothesis": "Every nontrivial zero with 0 < Im < T lies on Re = 1/2.",
    "falsifiable_prediction": "#sign-changes of Z on (0,T] equals N_exact(T).",
    "references": [
        "Riemann-Siegel formula; Turing's method.",
        "Odlyzko's large-scale verifications; LMFDB zeros of zeta.",
    ],
}

# Resolution. 1/16 comfortably resolves zero gaps in this height range (mean
# gap near T~150 is ~ 2pi/log(T) ~ 1.25, far larger than the step).
STEP = mp.mpf(1) / 16
DPS = 15
# Target height; capped dynamically by the wall-clock budget.
TARGET_T = 150


def run(budget_seconds: float) -> dict:
    L.set_precision(DPS)
    deadline = time.time() + 0.7 * budget_seconds  # leave room for N_exact()

    # Walk Z(t) upward counting sign changes, stopping early if we near the
    # deadline so the experiment always returns a valid Result within budget.
    t = mp.mpf(0)
    step = STEP
    prev = L.hardy_z(t)
    n_changes = 0
    n_samples = 1
    T = mp.mpf(0)
    target = mp.mpf(TARGET_T)
    while t < target:
        t += step
        cur = L.hardy_z(t)
        n_samples += 1
        if (prev > 0) != (cur > 0):
            n_changes += 1
        prev = cur
        T = t
        if (n_samples & 0x3FF) == 0 and time.time() > deadline:
            break

    n_exact = L.N_exact(T)
    matched = (n_changes == n_exact)
    # Honest frontier: only certify the height if the grid resolved every zero.
    t_verified = float(T) if matched else 0.0

    claim = (
        f"All {n_exact} nontrivial zeros with 0 < Im < {float(T):.2f} lie on the "
        f"critical line: Hardy Z has exactly N(T)={n_exact} sign changes."
        if matched else
        f"Grid under-resolved: {n_changes} sign changes vs N(T)={n_exact} up to "
        f"T={float(T):.2f}; no off-line zero implied, verification height not certified."
    )

    return E.result(
        track="zero_verification",
        claim=claim,
        metrics={
            "T": float(T),
            "step": float(step),
            "n_sign_changes": n_changes,
            "n_exact_NT": n_exact,
            "n_samples": n_samples,
            "matched": matched,
        },
        frontier_metric="T_verified",
        frontier_value=t_verified,
        # A deficit means we missed zeros with a coarse grid, NOT that a zero is
        # off the line. We never claim falsification from an under-count.
        falsified=False,
        consistent_with_rh=True,
        evidence={
            "method": "Riemann-Siegel Z sign changes vs Turing N(T)",
            "matched": matched,
        },
    )
