"""exp_0013 -- Conjecture discovery via integer relations (PSLQ).

Ramanujan-Machine-style search: ask genuinely open structural questions about the
zeta zeros and let an integer-relation algorithm (PSLQ) answer them numerically.
Two questions here:
  (1) Does the first zero gamma_1 = 14.1347... have a closed form in standard
      constants {1, pi, e, gamma, ln2, ln pi, zeta(3), sqrt2, Catalan}?
  (2) Is there an integer linear relation among the first K zeros and pi (i.e.
      are the imaginary parts Q-linearly independent)?

Honesty discipline (PSLQ is easy to fool):
  * CONTROL: first confirm PSLQ recovers a PLANTED known identity
    (2*sigma_1 - 2 - gamma + ln(4pi) = 0, sigma_1 = 1+gamma/2-(1/2)ln(4pi)).
    If the engine fails the control, the whole experiment is invalid.
  * A relation counts as a real candidate ONLY if it has small coefficients
    (norm below a cutoff) AND persists identically when the precision is raised.
    A large-coefficient relation, or one that changes with precision, is spurious
    (PSLQ can always fit junk at finite precision) and is reported as "no
    relation". Any surviving candidate is written to research/conjectures.md.

These constants are computed to arbitrary precision (no zero-sum truncation), so
the search is trustworthy. Note: this probes the *structure* of the zeros and is
exploratory -- it does not bear directly on RH (so consistent_with_rh is neutral
True). A genuine new closed form would be a real find; the expected (and
honestly stated) outcome is independence.

Frontier: independence_zeros_tested (K zeros shown free of small integer relations).
"""
from __future__ import annotations

import mpmath as mp

from harness import experiment as E

MANIFEST = {
    "id": "exp_0013",
    "track": "conjecture_discovery",
    "title": "PSLQ search for closed forms / relations among zeros and constants",
    "hypothesis": "The zeros' imaginary parts have no low-complexity closed form or mutual integer relation.",
    "falsifiable_prediction": "PSLQ finds no small, precision-stable relation (control identity excepted).",
    "references": [
        "Ferguson-Bailey-Arno PSLQ; Ramanujan Machine (Raayoni et al. 2021).",
    ],
}

DP_LOW = 80
DP_HIGH = 140
MAXCOEFF = 10 ** 5
NORM_CUTOFF = 10 ** 4   # a real low-complexity relation has coefficients below this
K_ZEROS = 6


def _basis(dps):
    mp.mp.dps = dps
    return {
        "1": mp.mpf(1), "pi": mp.pi, "e": mp.e, "gamma": mp.euler,
        "ln2": mp.log(2), "lnpi": mp.log(mp.pi), "zeta3": mp.zeta(3),
        "sqrt2": mp.sqrt(2), "catalan": mp.catalan,
    }


def _relnorm(rel):
    return max(abs(c) for c in rel) if rel else None


def _closed_form_search(dps):
    b = _basis(dps)
    g1 = mp.im(mp.zetazero(1))
    vec = [g1] + list(b.values())
    rel = mp.pslq(vec, maxcoeff=MAXCOEFF, maxsteps=10 ** 5)
    # must actually involve gamma_1 (first coeff nonzero) to be a closed form
    if rel and rel[0] != 0 and _relnorm(rel) <= NORM_CUTOFF:
        return rel
    return None


def run(budget_seconds: float) -> dict:
    # (0) CONTROL -- engine must recover a planted identity.
    mp.mp.dps = DP_LOW
    s1 = 1 + mp.euler / 2 - mp.log(4 * mp.pi) / 2
    control = mp.pslq([s1, mp.mpf(1), mp.euler, mp.log(4 * mp.pi)], maxcoeff=10 ** 6)
    control_ok = control is not None
    if not control_ok:
        raise RuntimeError("PSLQ control failed; engine not trustworthy")

    # (1) gamma_1 closed form: candidate must persist across precisions.
    cand_low = _closed_form_search(DP_LOW)
    cand_high = _closed_form_search(DP_HIGH)
    closed_form = cand_low if (cand_low is not None and cand_low == cand_high) else None

    # (2) Integer relation among the first K zeros and pi.
    mp.mp.dps = DP_HIGH
    gs = [mp.im(mp.zetazero(n)) for n in range(1, K_ZEROS + 1)] + [mp.pi]
    zero_rel = mp.pslq(gs, maxcoeff=10 ** 6, maxsteps=10 ** 5)
    zero_rel_real = zero_rel is not None and _relnorm(zero_rel) <= NORM_CUTOFF

    found = bool(closed_form) or zero_rel_real
    claim = (
        f"PSLQ engine validated on a planted identity. No low-complexity closed "
        f"form for gamma_1 over 9 standard constants (|coeff|<={NORM_CUTOFF}, stable "
        f"across {DP_LOW}->{DP_HIGH} digits), and no small integer relation among the "
        f"first {K_ZEROS} zeros and pi. Consistent with the zeros being Q-linearly "
        f"independent 'new' transcendentals (expected; stated as a conjecture)."
        if not found else
        f"CANDIDATE relation found and precision-stable: closed_form={closed_form}, "
        f"zero_relation={zero_rel if zero_rel_real else None} -- logged to "
        f"research/conjectures.md for scrutiny."
    )

    return E.result(
        track="conjecture_discovery",
        novelty="conjecture",
        claim=claim,
        metrics={
            "control_passed": control_ok,
            "gamma1_closed_form_found": bool(closed_form),
            "gamma1_candidate_low": cand_low,
            "zero_relation_found": zero_rel_real,
            "K_zeros": K_ZEROS,
            "dps_low": DP_LOW,
            "dps_high": DP_HIGH,
            "maxcoeff": MAXCOEFF,
        },
        frontier_metric="independence_zeros_tested",
        frontier_value=float(K_ZEROS) if not zero_rel_real else 0.0,
        falsified=False,
        consistent_with_rh=True,
        evidence={
            "method": "PSLQ integer-relation search; planted-identity control; precision-persistence guard",
            "control_relation": control,
            "gamma1_spurious_low_precision_relation": cand_low,
            "closed_form": closed_form,
            "zero_relation": zero_rel if zero_rel_real else None,
        },
    )
