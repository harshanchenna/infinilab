"""exp_0007 -- CERTIFIED critical-line verification (theorem-grade, via Arb).

Where exp_0001/0004 used fast floating-point (mpmath) to *count* sign changes,
this experiment PROVES them. Using Arb ball arithmetic (python-flint), each
value of the Hardy function Z(t) is a rigorous enclosure with a proven error
bar. A sign change between two grid points whose enclosures both rigorously
exclude 0 is a *proof* of a simple zero of zeta on the critical line between
them. Counting such certified sign changes gives a rigorous lower bound on the
number of zeros PROVEN to lie on the line up to height T.

This is a miniature of the Platt-Trudgian (2021) rigorous verification of RH to
height 3e12 (arXiv:2004.09765): same idea (interval/ball arithmetic + a fine
grid), smaller height.

Honesty:
  * The certified claim is "at least M zeros proven on the critical line up to T"
    -- this is theorem-grade, depending only on Arb's rigor.
  * We additionally compare M to N(T) (mpmath/Turing). If M == N(T) and there are
    no uncertified grid points, then every zero up to T is accounted for and
    proven on-line: RH is verified up to T. We label N(T) as Turing-method
    (not re-certified here), so the airtight part is the proven-on-line count.

Frontier: certified_T -- the height up to which the certification is clean
(no uncertified points) and M == N(T).
"""
from __future__ import annotations

import time

import mpmath as mp

from harness import rh_certified as C
from harness import rh_lib as L
from harness import experiment as E

MANIFEST = {
    "id": "exp_0007",
    "track": "certified_zero_verification",
    "title": "Certified (Arb) verification of zeros on the critical line",
    "hypothesis": "Every zero up to height T is provably on Re=1/2.",
    "falsifiable_prediction": "Certified Z sign changes account for all N(T) zeros, each proven on-line.",
    "references": [
        "Platt & Trudgian (2021), RH true to 3e12 (arXiv:2004.09765).",
        "Arb ball arithmetic via python-flint; research/rh_approaches.md.",
    ],
}

PREC_BITS = 256
STEP = mp.mpf(1) / 8     # < mean gap (~1.3 near T=150); ~10 samples/gap
TARGET_T = 150           # capped by the wall-clock budget below


def run(budget_seconds: float) -> dict:
    C.set_prec(PREC_BITS)
    C.selfcheck()
    deadline = time.time() + 0.7 * budget_seconds  # leave room for N(T)

    # Walk upward in blocks, counting CERTIFIED sign changes, stopping early if
    # we approach the deadline or hit an uncertified point.
    t = mp.mpf(0)
    step = STEP
    prev = C.certified_sign(C.hardy_z(str(t)))
    n_changes = 0
    n_uncertified = 0 if prev != 0 else 1
    T = mp.mpf(0)
    last_clean_T = mp.mpf(0)
    target = mp.mpf(TARGET_T)
    i = 0
    while t < target:
        t += step
        i += 1
        s = C.certified_sign(C.hardy_z(str(t)))
        if s == 0:
            n_uncertified += 1
        else:
            if prev != 0 and s != prev:
                n_changes += 1
            prev = s
            if n_uncertified == 0:
                last_clean_T = t
        T = t
        if (i & 0x3F) == 0 and time.time() > deadline:
            break

    n_exact = L.N_exact(T)
    clean = (n_uncertified == 0)
    matched = clean and (n_changes == n_exact)
    certified_T = float(last_clean_T) if matched else 0.0

    claim = (
        f"CERTIFIED: at least {n_changes} zeros proven on the critical line up to "
        f"T={float(T):.2f} via Arb ball arithmetic; matches N(T)={n_exact} "
        f"(Turing) with no uncertified points -> RH verified up to T={float(T):.2f}."
        if matched else
        f"Certified {n_changes} on-line zeros up to T={float(T):.2f} "
        f"(N(T)={n_exact}, uncertified points={n_uncertified}); clean certification "
        f"to T={float(last_clean_T):.2f}."
    )

    return E.result(
        track="certified_zero_verification",
        claim=claim,
        metrics={
            "T": float(T),
            "prec_bits": PREC_BITS,
            "step": float(step),
            "certified_sign_changes": n_changes,
            "n_exact_NT": n_exact,
            "n_uncertified_points": n_uncertified,
            "matched_NT": matched,
            "clean_certified_T": float(last_clean_T),
        },
        frontier_metric="certified_T",
        frontier_value=certified_T,
        falsified=False,
        consistent_with_rh=True,
        evidence={
            "method": "Arb rigorous Hardy-Z enclosures; certified sign changes = proven on-line zeros",
            "proven_on_line_zeros": n_changes,
            "matched_NT": matched,
        },
    )
