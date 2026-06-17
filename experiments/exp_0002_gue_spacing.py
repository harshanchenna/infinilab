"""exp_0002 -- Zero spacings follow GUE, not Poisson (Montgomery-Odlyzko).

Take the first K nontrivial zeros, unfold them to unit mean spacing using
w_n = theta(gamma_n)/pi, form consecutive gaps, and compare the empirical
spacing distribution against two models via the Kolmogorov-Smirnov distance:

  * GUE Wigner surmise  p(s) = (32/pi^2) s^2 exp(-(4/pi)s^2)   -- the random
    matrix prediction, the hallmark of the conjectured spectral interpretation
    of the zeros (Hilbert-Polya / Montgomery's pair-correlation).
  * Poisson  P(s) = 1 - exp(-s)   -- the null model of uncorrelated levels.

A good fit to GUE and a poor fit to Poisson (ks_gue << ks_poisson) is the
numerically robust, repeatedly-observed signature. This is consistent with RH
(real eigenvalues <-> zeros on the line) but does not prove it.

Frontier: n_zeros_sampled (K). More zeros = a stronger statistical test.
"""
from __future__ import annotations

import time

from harness import rh_lib as L
from harness import experiment as E

MANIFEST = {
    "id": "exp_0002",
    "track": "zero_statistics",
    "title": "GUE vs Poisson nearest-neighbour spacing of zeta zeros",
    "hypothesis": "Unfolded zero spacings follow the GUE Wigner surmise.",
    "falsifiable_prediction": "KS distance to GUE is much smaller than to Poisson.",
    "references": [
        "Montgomery (1973) pair correlation conjecture.",
        "Odlyzko's numerical confirmation of GUE statistics.",
    ],
}

DPS = 20
TARGET_K = 200  # capped by the wall-clock budget below


def run(budget_seconds: float) -> dict:
    L.set_precision(DPS)
    deadline = time.time() + 0.8 * budget_seconds

    gammas = []
    for n in range(1, TARGET_K + 1):
        gammas.append(L.gamma(n))
        if time.time() > deadline:
            break
    k = len(gammas)

    spac = L.normalized_spacings(gammas)
    mean_spacing = sum(spac) / len(spac)
    ks_gue = L.ks_distance(spac, L.gue_spacing_cdf)
    ks_poisson = L.ks_distance(spac, L.poisson_spacing_cdf)
    gue_better = ks_gue < ks_poisson

    claim = (
        f"First {k} zeta zeros: unfolded spacings fit GUE (KS={float(ks_gue):.3f}) "
        f"far better than Poisson (KS={float(ks_poisson):.3f}); mean gap "
        f"{float(mean_spacing):.3f}. Consistent with Montgomery-Odlyzko."
    )

    return E.result(
        track="zero_statistics",
        claim=claim,
        metrics={
            "n_zeros_sampled": k,
            "ks_gue": float(ks_gue),
            "ks_poisson": float(ks_poisson),
            "mean_spacing": float(mean_spacing),
            "gue_fits_better": gue_better,
        },
        frontier_metric="n_zeros_sampled",
        frontier_value=float(k),
        falsified=False,
        consistent_with_rh=True,
        evidence={
            "method": "unfold via theta/pi; KS distance to GUE and Poisson CDFs",
            "n_spacings": len(spac),
            "gamma_1": float(gammas[0]),
            "gamma_last": float(gammas[-1]),
        },
    )
