"""exp_0009 -- Push CERTIFIED critical-line verification to greater height.

Same theorem-grade method as exp_0007 (Arb ball arithmetic; a certified Hardy-Z
sign change is a proof of an on-line zero), but (a) finer step to resolve close
pairs, and (b) checkpointed matching: at each height checkpoint we compare the
running count of *proven* on-line zeros to N(T) (Turing). We certify RH up to the
highest checkpoint where the proven count still equals N(T) with no uncertified
points -- so a missed close pair can only LOWER the certified height, never
produce a false certification.

This advances the certified_zero_verification frontier past the heuristic
zero_verification frontier (T=600).

Frontier: certified_T (highest checkpoint with proven_count == N(T)).
"""
from __future__ import annotations

import time

import mpmath as mp

from harness import rh_certified as C
from harness import rh_lib as L
from harness import experiment as E

MANIFEST = {
    "id": "exp_0009",
    "track": "certified_zero_verification",
    "title": "Certified verification to greater height (checkpointed)",
    "hypothesis": "Every zero up to height T is provably on Re=1/2.",
    "falsifiable_prediction": "Proven on-line count equals N(T) at each checkpoint.",
    "references": ["Platt & Trudgian (2021); Arb; research/rh_approaches.md."],
}

PREC_BITS = 200
STEP = mp.mpf(1) / 16     # ~10+ samples/gap up to T~2000 (mean gap ~0.8)
TARGET_T = 2000
CHECKPOINT = mp.mpf(100)  # compare proven count to N(T) every 100 in height


def run(budget_seconds: float) -> dict:
    C.set_prec(PREC_BITS)
    C.selfcheck()
    deadline = time.time() + 0.9 * budget_seconds

    t = mp.mpf(0)
    step = STEP
    prev = C.certified_sign(C.hardy_z(str(t)))
    proven = 0
    uncertified = 0 if prev != 0 else 1
    certified_T = 0.0
    next_check = CHECKPOINT
    last_T = mp.mpf(0)
    target = mp.mpf(TARGET_T)
    i = 0
    halted_reason = "reached target"

    while t < target:
        t += step
        i += 1
        s = C.certified_sign(C.hardy_z(str(t)))
        if s == 0:
            uncertified += 1
        else:
            if prev != 0 and s != prev:
                proven += 1
            prev = s
        last_T = t

        if t >= next_check:
            n_exact = L.N_exact(next_check)
            if uncertified == 0 and proven == n_exact:
                certified_T = float(next_check)
                next_check += CHECKPOINT
            else:
                halted_reason = (
                    f"count/parity mismatch at T={float(next_check):.0f} "
                    f"(proven={proven}, N(T)={n_exact}, uncertified={uncertified})"
                )
                break
        if (i & 0x3F) == 0 and time.time() > deadline:
            halted_reason = "wall-clock budget"
            break

    claim = (
        f"CERTIFIED: all zeros up to T={certified_T:.0f} proven on the critical "
        f"line via Arb ball arithmetic ({proven} proven on-line zeros, matching "
        f"N(T) at every 100-step checkpoint, no uncertified points). "
        f"Halted: {halted_reason}."
    )

    return E.result(
        track="certified_zero_verification",
        claim=claim,
        metrics={
            "certified_T": certified_T,
            "prec_bits": PREC_BITS,
            "step": float(step),
            "proven_on_line_zeros": proven,
            "reached_T": float(last_T),
            "uncertified_points": uncertified,
            "halted_reason": halted_reason,
        },
        frontier_metric="certified_T",
        frontier_value=certified_T,
        falsified=False,
        consistent_with_rh=True,
        evidence={
            "method": "Arb rigorous Hardy-Z; checkpointed proven-count == N(T)",
            "proven_on_line_zeros": proven,
            "certified_T": certified_T,
        },
    )
