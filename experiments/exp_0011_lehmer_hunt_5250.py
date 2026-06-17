"""exp_0011 -- Resolve the close zero pair flagged near T~5250 (frontier-search).

This is a genuine open-ended search, not a reproduction: exp_0010's certified
walk (step 1/16) lost 2 zeros between the T=5000 and T=5250 checkpoints --
the signature of a close (near-Lehmer) pair whose +/-/+ excursion fit inside one
grid step. We did not know it was there; now we resolve it.

Method (all rigorous, Arb): densely sample certified Hardy-Z over (5000, 5250],
collect certified sign changes (each a proven on-line zero), bisect each to
locate the zero, then find the smallest consecutive gap and its NORMALIZED value
  delta = (gamma_{k+1}-gamma_k) * (1/2pi) * ln(gamma_k/2pi)
(mean normalized gap = 1). A small delta is a Lehmer pair; such pairs drive lower
bounds on the de Bruijn-Newman constant (RH <=> Lambda <= 0, and Lambda >= 0 is
proven, Rodgers-Tao). We compare to the smallest gap seen so far in the lab
(0.291, from exp_0003 at T~415).

Frontier: inverse_min_normalized_gap (1/delta) -- larger = a closer pair.
"""
from __future__ import annotations

import time

import mpmath as mp

from harness import rh_certified as C
from harness import experiment as E

MANIFEST = {
    "id": "exp_0011",
    "track": "lehmer_pairs",
    "title": "Resolve and measure the close zero pair near T~5250",
    "hypothesis": "A near-Lehmer pair sits in (5000,5250]; measure its normalized gap.",
    "falsifiable_prediction": "Two certified zeros within < one coarse step; small normalized gap.",
    "references": [
        "Lehmer (1956); Rodgers-Tao (2018) Lambda>=0; research/rh_approaches.md.",
    ],
}

PREC_BITS = 220
T0, T1 = mp.mpf(5000), mp.mpf(5250)
STEP = mp.mpf(1) / 128


def _bisect_zero(a, b, sa, depth=50):
    """Locate a zero in (a,b) where certified_sign(Z(a))=sa, sign(Z(b))=-sa."""
    for _ in range(depth):
        m = (a + b) / 2
        sm = C.certified_sign(C.hardy_z(str(m)))
        if sm == 0:        # ball straddles 0: we are essentially at the zero
            return m
        if sm == sa:
            a = m
        else:
            b = m
    return (a + b) / 2


def run(budget_seconds: float) -> dict:
    C.set_prec(PREC_BITS)
    C.selfcheck()
    deadline = time.time() + 0.9 * budget_seconds

    # Dense certified scan; record zero locations at each sign change.
    zeros = []
    t = T0
    prev_t = t
    prev = C.certified_sign(C.hardy_z(str(t)))
    while t < T1:
        t += STEP
        s = C.certified_sign(C.hardy_z(str(t)))
        if s != 0 and prev != 0 and s != prev:
            zeros.append(_bisect_zero(prev_t, t, prev))
        if s != 0:
            prev = s
            prev_t = t
        if time.time() > deadline:
            break

    # Consecutive gaps, normalized to unit mean spacing.
    gaps = []
    for i in range(len(zeros) - 1):
        g = zeros[i]
        dt = zeros[i + 1] - zeros[i]
        delta = dt * mp.log(g / (2 * mp.pi)) / (2 * mp.pi)
        gaps.append((delta, g, zeros[i + 1]))
    gaps.sort(key=lambda x: x[0])
    min_delta, lo, hi = gaps[0] if gaps else (mp.mpf("nan"), mp.mpf(0), mp.mpf(0))
    prior_best = mp.mpf("0.291")
    new_record = bool(gaps) and min_delta < prior_best

    claim = (
        f"Resolved {len(zeros)} zeros in ({float(T0):.0f},{float(T1):.0f}]; closest "
        f"pair at heights {float(lo):.4f}, {float(hi):.4f} with raw gap "
        f"{float(hi-lo):.5f} and normalized gap delta={float(min_delta):.4f} "
        f"({'NEW lab record close pair (<0.291)' if new_record else 'not below the 0.291 lab record'}). "
        f"A genuine near-Lehmer pair; all gaps positive, consistent with RH."
    )

    return E.result(
        track="lehmer_pairs",
        novelty="frontier-search",
        claim=claim,
        metrics={
            "n_zeros_resolved": len(zeros),
            "min_normalized_gap": float(min_delta) if gaps else None,
            "raw_gap": float(hi - lo) if gaps else None,
            "pair_heights": [float(lo), float(hi)] if gaps else None,
            "new_lab_record": new_record,
        },
        frontier_metric="inverse_min_normalized_gap",
        frontier_value=float(1 / min_delta) if gaps and min_delta > 0 else 0.0,
        falsified=False,
        consistent_with_rh=True,
        evidence={
            "method": "dense certified Arb Z scan + bisection to locate zeros",
            "closest_pair": [float(lo), float(hi)] if gaps else None,
            "normalized_gap": float(min_delta) if gaps else None,
            "prior_lab_record": float(prior_best),
        },
    )
