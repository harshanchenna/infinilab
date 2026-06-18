"""exp_0005 -- Robin's inequality on the primorials.

Robin (1984): RH is TRUE  <=>  sigma(n) < e^gamma * n * ln(ln(n))  for all
n > 5040, where sigma is the sum-of-divisors function. A single violation with
n > 5040 would DISPROVE RH. The extremal candidates cluster among highly
composite numbers; the primorials P_k = product of the first k primes are the
canonical squarefree near-extremal family, so they are a natural place to look
for a violation.

We check the primorials exactly. For a squarefree n = P_k,
    sigma(n)/n = prod_{i<=k} (1 + 1/p_i),     ln(n) = sum_{i<=k} ln(p_i),
so the Robin ratio
    f(P_k) = (sigma(P_k)/P_k) / (e^gamma * ln(ln(P_k)))
is computed with no large-integer arithmetic and no rounding of sigma. We report
the maximum ratio over all primorials with P_k > 5040 and confirm every such
ratio is < 1.

Scope (stated honestly): this checks the PRIMORIAL family, not all integers, so
a clean pass is "consistent with RH on the primorials", not a proof. A ratio
>= 1 here, however, WOULD be a genuine disproof and is flagged as falsified.

Frontier: n_primorials_checked (k of the largest primorial tested).
"""
from __future__ import annotations

import time

import mpmath as mp
import sympy

from harness import experiment as E

MANIFEST = {
    "id": "exp_0005",
    "track": "robin_inequality",
    "title": "Robin's inequality on the primorials",
    "hypothesis": "sigma(n) < e^gamma n ln ln n for every primorial n > 5040.",
    "falsifiable_prediction": "Robin ratio f(P_k) < 1 for all primorials P_k > 5040.",
    "references": [
        "Robin (1984): RH <=> sigma(n) < e^gamma n ln ln n for n > 5040.",
        "Primorials / superabundant numbers as Robin extremal candidates.",
    ],
}

DPS = 30
TARGET_K = 2000  # number of primes in the largest primorial; capped by budget


def run(budget_seconds: float) -> dict:
    mp.mp.dps = DPS
    deadline = time.time() + 0.85 * budget_seconds
    egamma = mp.e ** mp.euler

    sigma_over_n = mp.mpf(1)   # running product of (1 + 1/p)
    ln_n = mp.mpf(0)           # running sum of ln(p)  = ln(primorial)
    max_ratio = None
    max_ratio_k = None
    worst_violation = None     # (k, ratio) if any f >= 1 with P_k > 5040
    k = 0
    checked = 0

    for p in sympy.primerange(2, 10**9):
        k += 1
        p = mp.mpf(int(p))
        sigma_over_n *= (1 + 1 / p)
        ln_n += mp.log(p)
        # Only meaningful once the primorial exceeds Robin's threshold 5040.
        if ln_n > mp.log(5040):
            lnln = mp.log(ln_n)
            ratio = sigma_over_n / (egamma * lnln)
            checked += 1
            if max_ratio is None or ratio > max_ratio:
                max_ratio = ratio
                max_ratio_k = k
            if ratio >= 1 and worst_violation is None:
                worst_violation = (k, float(ratio))
        if k >= TARGET_K or time.time() > deadline:
            break

    falsified = worst_violation is not None
    claim = (
        f"Robin's inequality holds for all {checked} primorials P_k > 5040 up to "
        f"k={k}: max ratio f={float(max_ratio):.5f} at k={max_ratio_k} (< 1). "
        f"Consistent with RH on the primorial family."
        if not falsified else
        f"VIOLATION: Robin ratio f >= 1 at primorial k={worst_violation[0]} "
        f"(f={worst_violation[1]:.6f}) with P_k > 5040 -- would disprove RH."
    )

    return E.result(
        track="robin_inequality",
        claim=claim,
        metrics={
            "n_primorials_checked": checked,
            "largest_k": k,
            "max_robin_ratio": float(max_ratio) if max_ratio is not None else None,
            "max_ratio_at_k": max_ratio_k,
            "ln_largest_primorial": float(ln_n),
            "violation": falsified,
        },
        frontier_metric="n_primorials_checked",
        frontier_value=float(checked),
        falsified=falsified,
        consistent_with_rh=not falsified,
        evidence={
            "method": "exact sigma/n = prod(1+1/p) for squarefree primorials; ratio vs e^gamma ln ln n",
            "max_ratio": float(max_ratio) if max_ratio is not None else None,
            "worst_violation": worst_violation,
        },
    )
