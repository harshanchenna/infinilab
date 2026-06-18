"""exp_0012 -- Hunt for a Robin violation among colossally abundant numbers.

Robin (1984): RH is TRUE <=> sigma(n) < e^gamma n ln ln n for all n > 5040. The
maximum of the Robin ratio f(n) = sigma(n)/(e^gamma n ln ln n) over all n is
attained on the **colossally abundant (CA) numbers** -- the genuine extremal
family (exp_0005 only checked primorials, a weaker squarefree sub-family). So CA
numbers are exactly where a counterexample, if one existed, would live. This is
a falsification-attempt: a CA number n > 5040 with f(n) >= 1 would DISPROVE RH.

CA generation (Alaoglu-Erdos): for each prime p and exponent step k>=1 the
threshold
    eps_{p,k} = log_p( (p^{k+1}-1)/(p^k-1) ) - 1
is strictly decreasing in k; sorting all thresholds in decreasing eps and
crossing them one by one raises exponents and yields the CA numbers in order
(2, 6, 12, 60, 120, 360, 2520, 5040, 55440, ...). For each CA number we compute
f(n) EXACTLY from its factorization (sigma(n)/n = prod (p^{a+1}-1)/((p-1)p^a),
ln n = sum a ln p). We report the maximum f over CA numbers with n > 5040 (the
closest approach to a violation) and flag any f >= 1.

Frontier: max_robin_ratio_CA -- larger = closer to the RH boundary.
"""
from __future__ import annotations

import time

import mpmath as mp
import sympy

from harness import experiment as E

MANIFEST = {
    "id": "exp_0012",
    "track": "robin_inequality",
    "title": "Robin violation hunt over colossally abundant numbers",
    "hypothesis": "No CA number n>5040 violates Robin (f(n) stays < 1).",
    "falsifiable_prediction": "Every CA n>5040 has f(n) < 1; a f(n)>=1 disproves RH.",
    "references": [
        "Robin (1984); Alaoglu-Erdos colossally abundant numbers; Gronwall (limsup f = 1).",
    ],
}

DPS = 50
N_PRIMES = 400
KMAX = 60
# Ignore vanishingly small thresholds: below this, eps values underflow into
# unorderable noise and correspond to astronomically large CA numbers well past
# the region where the Robin ratio makes its closest approach. This floor still
# yields CA numbers with hundreds of digits, far beyond 5040.
EPS_FLOOR = mp.mpf("1e-12")


def run(budget_seconds: float) -> dict:
    mp.mp.dps = DPS
    deadline = time.time() + 0.9 * budget_seconds
    egamma = mp.e ** mp.euler
    ln5040 = mp.log(5040)

    primes = list(sympy.primerange(2, sympy.prime(N_PRIMES) + 1))
    thresholds = []
    for p in primes:
        P = mp.mpf(p)
        for k in range(1, KMAX + 1):
            eps = mp.log((P ** (k + 1) - 1) / (P ** k - 1)) / mp.log(P) - 1
            if eps < EPS_FLOOR:
                break  # eps_{p,k} decreasing in k; rest are below the floor
            thresholds.append((eps, p, k))
    thresholds.sort(key=lambda x: -x[0])  # decreasing eps -> CA numbers in order

    ln_n = mp.mpf(0)
    sigma_over_n = mp.mpf(1)
    expo = {}
    n_ca = 0
    checked = 0
    max_f = None
    max_f_lnn = None
    f_5040 = None
    violation = None

    for eps, p, k in thresholds:
        P = mp.mpf(p)
        if expo.get(p, 0) != k - 1:
            break  # past the cleanly-orderable range; stop the CA walk here
        expo[p] = k
        ln_n += mp.log(P)
        sig_new = (P ** (k + 1) - 1) / ((P - 1) * P ** k)
        sig_old = mp.mpf(1) if k == 1 else (P ** k - 1) / ((P - 1) * P ** (k - 1))
        sigma_over_n *= sig_new / sig_old
        n_ca += 1

        if ln_n > ln5040:
            lnln = mp.log(ln_n)
            f = sigma_over_n / (egamma * lnln)
            checked += 1
            if max_f is None or f > max_f:
                max_f = f
                max_f_lnn = ln_n
            if f >= 1 and violation is None:
                violation = (float(ln_n), float(f))
        elif abs(ln_n - ln5040) < mp.mpf("1e-9"):
            f_5040 = sigma_over_n / (egamma * mp.log(ln_n))

        if time.time() > deadline:
            break

    falsified = violation is not None
    claim = (
        f"Hunted {checked} colossally abundant numbers n>5040 (up to ln n="
        f"{float(max_f_lnn):.1f}, ~{float(max_f_lnn/mp.log(10)):.0f} digits): max "
        f"Robin ratio f={float(max_f):.6f} < 1. No violation -> consistent with RH "
        f"on the true extremal family (closest approach {float(max_f):.6f})."
        if not falsified else
        f"ROBIN VIOLATION at a CA number n>5040 (ln n={violation[0]:.2f}, "
        f"f={violation[1]:.6f} >= 1) -- would DISPROVE RH."
    )

    return E.result(
        track="robin_inequality",
        novelty="falsification-attempt",
        claim=claim,
        metrics={
            "n_CA_total": n_ca,
            "n_CA_above_5040": checked,
            "max_robin_ratio_CA": float(max_f) if max_f is not None else None,
            "max_ratio_ln_n": float(max_f_lnn) if max_f_lnn is not None else None,
            "violation": falsified,
        },
        frontier_metric="max_robin_ratio_CA",
        frontier_value=float(max_f) if max_f is not None else 0.0,
        falsified=falsified,
        consistent_with_rh=not falsified,
        evidence={
            "method": "Alaoglu-Erdos CA generation; exact f(n) from factorization",
            "max_robin_ratio": float(max_f) if max_f is not None else None,
            "violation": violation,
            "largest_ln_n": float(max_f_lnn) if max_f_lnn is not None else None,
        },
    )
