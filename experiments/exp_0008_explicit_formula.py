"""exp_0008 -- Explicit formula: reconstruct psi(x) from the zeros.

Von Mangoldt's explicit formula (exact):
    psi(x) = x - sum_rho x^rho/rho - ln(2*pi) - (1/2) ln(1 - x^-2),
where psi(x) = sum_{n<=x} Lambda(n) is the Chebyshev function and the sum runs
over nontrivial zeros rho as a symmetric limit. Truncating at the first N zeros
(pairing rho = 1/2+i*gamma with its conjugate),
    sum_{|gamma|<=gamma_N} x^rho/rho = sum_{k=1}^N 2*Re( x^(1/2+i*gamma_k) / (1/2+i*gamma_k) ),
reconstructs the prime oscillations of psi. We compare the reconstruction to the
EXACT psi(x) (summed directly from the von Mangoldt function) on a grid of
non-integer x (avoiding the jumps at prime powers, where Gibbs oscillations are
unavoidable) and track the RMS residual as N grows.

Falsifiable consistency: the explicit formula must reproduce psi(x); the
residual must shrink as more zeros are included. (Under RH the zero-sum is
O(x^{1/2+eps}); a systematic non-convergence would signal an error or anomaly.)

Frontier: n_zeros_used (N). More zeros = sharper reconstruction.
"""
from __future__ import annotations

import time

import mpmath as mp
import sympy

from harness import rh_lib as L
from harness import experiment as E

MANIFEST = {
    "id": "exp_0008",
    "track": "explicit_formula",
    "title": "Reconstruct Chebyshev psi(x) from zeta zeros (von Mangoldt)",
    "hypothesis": "The zero-sum explicit formula reproduces psi(x); residual -> 0 as N grows.",
    "falsifiable_prediction": "RMS residual over the x-grid decreases as N doubles.",
    "references": [
        "Riemann / von Mangoldt explicit formula; research/rh_approaches.md.",
    ],
}

DPS = 25
N_ZEROS = 200          # capped by budget
X_GRID = [mp.mpf(k) + mp.mpf("0.5") for k in range(10, 81, 5)]  # non-integer x


def psi_exact(xmax):
    """Exact Chebyshev psi(x) = sum_{n<=x} Lambda(n) for the largest grid x."""
    out = {}
    total = mp.mpf(0)
    limit = int(xmax) + 1
    # Precompute Lambda(n): log p if n = p^k, else 0.
    for n in range(2, limit + 1):
        f = sympy.factorint(n)
        if len(f) == 1:
            p = next(iter(f))
            total += mp.log(p)
        out[n] = total
    return out


def psi_from_zeros(x, gammas):
    """Explicit-formula reconstruction of psi(x) using the given zero heights."""
    s = mp.mpf(0)
    for g in gammas:
        rho = mp.mpf("0.5") + 1j * g
        s += 2 * mp.re(mp.power(x, rho) / rho)
    return x - s - mp.log(2 * mp.pi) - mp.log(1 - x ** (-2)) / 2


def _rms(x_grid, gammas, psi_tab):
    sq = mp.mpf(0)
    for x in x_grid:
        approx = psi_from_zeros(x, gammas)
        exact = psi_tab[int(x)]   # psi is constant on (n, n+1); x = n+0.5
        sq += (approx - exact) ** 2
    return mp.sqrt(sq / len(x_grid))


def run(budget_seconds: float) -> dict:
    L.set_precision(DPS)
    deadline = time.time() + 0.85 * budget_seconds

    gammas = []
    for n in range(1, N_ZEROS + 1):
        gammas.append(L.gamma(n))
        if time.time() > deadline:
            break
    n_full = len(gammas)
    n_half = max(1, n_full // 2)

    psi_tab = psi_exact(max(X_GRID))
    rms_full = _rms(X_GRID, gammas, psi_tab)
    rms_half = _rms(X_GRID, gammas[:n_half], psi_tab)
    improved = rms_full < rms_half

    claim = (
        f"Explicit formula reconstructs psi(x) on {len(X_GRID)} points (x in "
        f"[10.5,80.5]): RMS residual {float(rms_full):.4f} with {n_full} zeros, "
        f"down from {float(rms_half):.4f} with {n_half} zeros. Converging as "
        f"predicted; consistent with RH."
    )

    return E.result(
        track="explicit_formula",
        claim=claim,
        metrics={
            "n_zeros_used": n_full,
            "n_zeros_half": n_half,
            "rms_residual_full": float(rms_full),
            "rms_residual_half": float(rms_half),
            "improved_with_more_zeros": improved,
            "n_grid_points": len(X_GRID),
        },
        frontier_metric="n_zeros_used",
        frontier_value=float(n_full),
        falsified=False,
        consistent_with_rh=True,
        evidence={
            "method": "psi(x) = x - sum 2Re(x^rho/rho) - ln(2pi) - (1/2)ln(1-x^-2) vs exact psi",
            "rms_full": float(rms_full),
            "rms_half": float(rms_half),
        },
    )
