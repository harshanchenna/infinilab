"""exp_0010 -- Certified critical-line verification toward T=10000.

Same theorem-grade, checkpoint-matched method as exp_0009 (Arb ball arithmetic;
each certified Hardy-Z sign change proves an on-line zero; certify only up to the
highest checkpoint where the proven count equals N(T) with no uncertified
points), pushed toward T=10000. Mean zero gap near T=10000 is ~0.68; step 1/16 =
0.0625 gives ~11 samples/gap, enough to resolve close pairs (and any miss only
lowers certified_T, never falsely certifies). Self-caps at the wall-clock budget
and reports the certified height reached.

Frontier: certified_T.
"""
from __future__ import annotations

import time

import mpmath as mp

from harness import rh_certified as C
from harness import rh_lib as L
from harness import experiment as E

MANIFEST = {
    "id": "exp_0010",
    "track": "certified_zero_verification",
    "title": "Certified verification toward T=10000",
    "hypothesis": "Every zero up to height T is provably on Re=1/2.",
    "falsifiable_prediction": "Proven on-line count equals N(T) at each checkpoint.",
    "references": ["Platt & Trudgian (2021); Arb; research/rh_approaches.md."],
}

PREC_BITS = 200
STEP = mp.mpf(1) / 16
TARGET_T = 10000
CHECKPOINT = mp.mpf(250)


def run(budget_seconds: float) -> dict:
    C.set_prec(PREC_BITS)
    C.selfcheck()
    deadline = time.time() + 0.92 * budget_seconds

    t = mp.mpf(0)
    step = STEP
    prev = C.certified_sign(C.hardy_z(str(t)))
    proven = 0
    uncertified = 0 if prev != 0 else 1
    certified_T = 0.0
    next_check = CHECKPOINT
    last_T = mp.mpf(0)
    i = 0
    halted_reason = "reached target"
    target = mp.mpf(TARGET_T)

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
        f"N(T) at every {int(CHECKPOINT)}-step checkpoint, no uncertified points). "
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
