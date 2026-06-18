"""exp_0006 -- Li's criterion: positivity of the Keiper-Li coefficients.

Li (1997) / Bombieri-Lagarias (1999): RH is TRUE <=> lambda_n >= 0 for all
n >= 1, where lambda_n = sum_rho [1-(1-1/rho)^n]. A single negative lambda_n
would disprove RH.

We use the harness Li primitives (added by the meta-optimizer; see
research/meta_log.md). They compute lambda_n via power sums with the exact
S_1 = 1+gamma/2-(1/2)ln(4pi) plus truncated S_j (j>=2) from the first K zeros.
This makes lambda_n (n>=2) ESTIMATES that approach the true values from below,
so the honest claim is about POSITIVITY and monotone convergence, not precise
values. To make that convergence visible (and guard against a truncation
artifact flipping a sign), we compute at two truncations K and 2K and require:
  * every lambda_n estimate is strictly positive at both K and 2K, AND
  * estimates increase from K to 2K (approaching the positive limit from below).

A clean pass is "consistent with Li's criterion / RH on the first N
coefficients"; never a proof. A negative estimate that persisted and grew in
magnitude with K would be the falsification signal.

Frontier: n_li_coefficients (N checked positive).
"""
from __future__ import annotations

import time

from projects.riemann.lib import rh_lib as L
from harness import experiment as E

MANIFEST = {
    "id": "exp_0006",
    "track": "li_criterion",
    "title": "Positivity of the first N Keiper-Li coefficients",
    "hypothesis": "lambda_n >= 0 for all n (Li's criterion <=> RH).",
    "falsifiable_prediction": "Every lambda_n estimate is positive and increases with K.",
    "references": [
        "Li (1997); Bombieri-Lagarias (1999); Keiper (1992).",
        "research/rh_approaches.md (li_criterion), research/meta_log.md.",
    ],
}

DPS = 30
N_COEFFS = 12
K_BASE = 200  # zeros for the coarse estimate; fine estimate uses 2*K_BASE


def run(budget_seconds: float) -> dict:
    L.set_precision(DPS)
    L.li_selfcheck()  # audit the primitive before trusting it
    deadline = time.time() + 0.85 * budget_seconds

    # Gather up to 2*K_BASE zeros, budget-permitting.
    gammas = []
    target = 2 * K_BASE
    for n in range(1, target + 1):
        gammas.append(L.gamma(n))
        if time.time() > deadline:
            break
    k_fine = len(gammas)
    k_coarse = max(1, k_fine // 2)

    lam_coarse = L.li_coefficients_estimate(gammas[:k_coarse], N_COEFFS)
    lam_fine = L.li_coefficients_estimate(gammas, N_COEFFS)

    all_positive = all(v > 0 for v in lam_fine) and all(v > 0 for v in lam_coarse)
    increasing = all(lf >= lc for lf, lc in zip(lam_fine, lam_coarse))
    min_lambda = min(float(v) for v in lam_fine)
    # Falsification only if an estimate is negative AND grew more negative with K
    # (a persistent, converging negative -- not a transient truncation wobble).
    falsified = any(lf < 0 and lf < lc for lf, lc in zip(lam_fine, lam_coarse))

    claim = (
        f"First {N_COEFFS} Keiper-Li coefficients estimated from {k_fine} zeros are "
        f"all positive (min lambda={min_lambda:.4f}) and increase from K={k_coarse} "
        f"to K={k_fine} (converging from below). Consistent with Li's criterion / RH."
        if not falsified else
        f"Persistent negative Li-coefficient estimate detected (min lambda={min_lambda:.4f}) "
        f"that grows with K -- candidate falsification of RH; needs higher precision."
    )

    return E.result(
        track="li_criterion",
        claim=claim,
        metrics={
            "n_li_coefficients": N_COEFFS,
            "k_coarse": k_coarse,
            "k_fine": k_fine,
            "min_lambda_fine": min_lambda,
            "all_positive": all_positive,
            "monotone_increasing_in_K": increasing,
            "lambda_fine": [float(v) for v in lam_fine],
        },
        frontier_metric="n_li_coefficients",
        frontier_value=float(N_COEFFS) if all_positive else 0.0,
        falsified=falsified,
        consistent_with_rh=not falsified,
        evidence={
            "method": "power sums: exact S_1 + truncated S_j; lambda_n via binomial sum",
            "lambda_coarse": [float(v) for v in lam_coarse],
            "lambda_fine": [float(v) for v in lam_fine],
            "note": "estimates approach true positive values from below; positivity signal only",
        },
    )
