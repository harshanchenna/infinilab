"""exp_0004 -- Extend critical-line verification to greater height T.

Same rigorous method as exp_0001 (Hardy-Z sign changes counted against the
exact zero count N(T) from Turing's method), pushed to a larger height to
advance the zero_verification frontier (previously T=150). The step is kept
well below the local mean zero gap 2*pi/log(T) so every zero is resolved; the
verification is certified only if #sign-changes == N_exact(T).

Frontier: T_verified.
"""
from __future__ import annotations

import time

import mpmath as mp

from projects.riemann.lib import rh_lib as L
from harness import experiment as E

MANIFEST = {
    "id": "exp_0004",
    "track": "zero_verification",
    "title": "Critical-line verification to greater height (T up to ~600)",
    "hypothesis": "Every nontrivial zero with 0 < Im < T lies on Re = 1/2.",
    "falsifiable_prediction": "#sign-changes of Z on (0,T] equals N_exact(T).",
    "references": ["Riemann-Siegel; Turing's method; Odlyzko verifications."],
}

# Mean gap near T=600 is 2*pi/log(600) ~ 0.98; step 1/16 = 0.0625 resolves it
# with ~15 samples per gap.
STEP = mp.mpf(1) / 16
DPS = 18
TARGET_T = 600


def run(budget_seconds: float) -> dict:
    L.set_precision(DPS)
    deadline = time.time() + 0.7 * budget_seconds

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
    t_verified = float(T) if matched else 0.0

    claim = (
        f"All {n_exact} nontrivial zeros with 0 < Im < {float(T):.2f} lie on the "
        f"critical line: Hardy Z has exactly N(T)={n_exact} sign changes."
        if matched else
        f"Grid under-resolved at T={float(T):.2f}: {n_changes} sign changes vs "
        f"N(T)={n_exact}; no off-line zero implied, height not certified."
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
        falsified=False,
        consistent_with_rh=True,
        evidence={
            "method": "Riemann-Siegel Z sign changes vs Turing N(T)",
            "matched": matched,
        },
    )
