"""Trusted primitives for Riemann-Hypothesis experiments.

This module is the analog of Karpathy autoresearch's `prepare.py`: it is FIXED
infrastructure. The autonomous loop is not supposed to edit it. Experiments
(the analog of `train.py`) compose these primitives; the Tier-1 verifier trusts
them.

Everything here is a thin, well-documented wrapper over `mpmath`, whose zeta /
Hardy-Z / zero-counting routines are mature and independently trusted. We add
no clever numerics of our own here on purpose: the whole point of the spine is
that it is boring and un-gameable.

Conventions
-----------
* The nontrivial zeros of zeta are written rho = 1/2 + i*gamma (under RH).
* `gamma_n` denotes the imaginary part of the n-th zero (n >= 1), gamma_1 ~ 14.1347.
* `Z(t)` is the Hardy function; its real sign changes are exactly the zeros of
  zeta on the critical line.
* `theta(t)` is the Riemann-Siegel theta function.
* `N(T)` counts nontrivial zeros with 0 < Im(rho) < T (with multiplicity).
"""
from __future__ import annotations

import mpmath as mp


def set_precision(dps: int = 30) -> None:
    """Set global decimal precision. Higher dps -> slower but more accurate."""
    mp.mp.dps = dps


# --------------------------------------------------------------------------- #
# Core analytic objects
# --------------------------------------------------------------------------- #
def zeta(s):
    """Riemann zeta function (analytic continuation)."""
    return mp.zeta(s)


def hardy_z(t):
    """Hardy Z-function Z(t) = exp(i*theta(t)) * zeta(1/2 + i*t).

    Z is real for real t, and Z(t) = 0 iff zeta has a zero at 1/2 + i*t.
    Sign changes of Z therefore count zeros ON the critical line.
    """
    return mp.siegelz(t)


def theta(t):
    """Riemann-Siegel theta(t) = arg Gamma(1/4 + i t/2) - (t/2) log(pi)."""
    return mp.siegeltheta(t)


def N_smooth(T):
    """Smooth (Riemann-von Mangoldt) main term for the zero count:

        N(T) ~ theta(T)/pi + 1.

    The true count is N(T) = theta(T)/pi + 1 + S(T), where S(T) is a small
    oscillating term (typically |S(T)| < 2 in the ranges we explore).
    """
    return theta(T) / mp.pi + 1


def N_exact(T) -> int:
    """Exact number of nontrivial zeros with 0 < Im(rho) < T.

    mpmath computes this rigorously (Gram points + Backlund/Turing method).
    This is our trusted ground-truth count.
    """
    return int(mp.nzeros(T))


def zero(n: int):
    """The n-th nontrivial zero rho_n = 1/2 + i*gamma_n (n >= 1), as a complex."""
    return mp.zetazero(n)


def gamma(n: int):
    """Imaginary part gamma_n of the n-th nontrivial zero (n >= 1)."""
    return mp.zetazero(n).imag


def first_gammas(k: int):
    """Imaginary parts of the first k nontrivial zeros, as a list of mpf."""
    return [mp.zetazero(n).imag for n in range(1, k + 1)]


# --------------------------------------------------------------------------- #
# Sign-change counting on the critical line (Riemann-Siegel)
# --------------------------------------------------------------------------- #
def count_sign_changes(t0, t1, step):
    """Count sign changes of Hardy Z on (t0, t1] sampling at the given step.

    Returns (n_changes, n_samples). This is a LOWER bound on the number of
    zeros of Z in the interval: if the step is too coarse, pairs of nearby
    zeros (e.g. Lehmer pairs) can be missed. The verifier compares this against
    N_exact to decide whether the grid resolved every zero.
    """
    t0 = mp.mpf(t0)
    t1 = mp.mpf(t1)
    step = mp.mpf(step)

    n_changes = 0
    n_samples = 1
    prev_t = t0
    prev = hardy_z(prev_t)
    t = t0 + step
    while t <= t1:
        cur = hardy_z(t)
        n_samples += 1
        if (prev > 0) != (cur > 0):
            n_changes += 1
        prev = cur
        t += step
    return n_changes, n_samples


# --------------------------------------------------------------------------- #
# Unfolding and spacing statistics (Montgomery-Odlyzko / GUE)
# --------------------------------------------------------------------------- #
def unfolded_gammas(gammas):
    """Unfold a sequence of zero heights to unit mean spacing.

    The expected number of zeros up to height t is ~ theta(t)/pi + 1, so the
    map  w_n = theta(gamma_n)/pi  rescales spacings to mean ~ 1. Returns a list
    of unfolded positions w_n (mpf).
    """
    return [theta(g) / mp.pi for g in gammas]


def normalized_spacings(gammas):
    """Consecutive unfolded gaps delta_n = w_{n+1} - w_n (mean ~ 1)."""
    w = unfolded_gammas(gammas)
    return [w[i + 1] - w[i] for i in range(len(w) - 1)]


def gue_spacing_pdf(s):
    """Wigner surmise for GUE nearest-neighbour spacing density.

        p(s) = (32/pi^2) s^2 exp(-(4/pi) s^2).
    """
    s = mp.mpf(s)
    return (32 / mp.pi**2) * s**2 * mp.e ** (-(4 / mp.pi) * s**2)


def gue_spacing_cdf(s):
    """CDF of the GUE Wigner surmise, integral_0^s p(u) du.

    Closed form: P(s) = 1 - exp(-(4/pi) s^2)*(1 + (4/pi) s^2)?  -- not exact for
    the s^2 prefactor, so we integrate numerically (cheap, 1-D, smooth).
    """
    s = mp.mpf(s)
    if s <= 0:
        return mp.mpf(0)
    return mp.quad(gue_spacing_pdf, [0, s])


def poisson_spacing_cdf(s):
    """CDF of exponential (Poisson / uncorrelated) spacings: 1 - exp(-s).

    Included as a null model: if zeros were uncorrelated their spacings would
    be Poisson, NOT GUE. Distinguishing the two is the Montgomery-Odlyzko
    phenomenon.
    """
    s = mp.mpf(s)
    if s <= 0:
        return mp.mpf(0)
    return 1 - mp.e ** (-s)


# --------------------------------------------------------------------------- #
# Li / Keiper coefficients (li_criterion track)
# --------------------------------------------------------------------------- #
# Added by the meta-optimizer (see research/meta_log.md). RH <=> lambda_n >= 0
# for all n (Li 1997; Bombieri-Lagarias 1999). We compute via power sums:
#     lambda_n = sum_{j=1}^n C(n,j) (-1)^(j+1) S_j,    S_j = sum_rho rho^(-j).
# S_1 has an exact closed form; S_j (j>=2) are truncated over the given zero
# heights. Truncation makes the lambda_n ESTIMATES, not exact values: they
# approach the true (positive) coefficients from below as more zeros are used.
# So treat them as lower-bound-style estimates good for a POSITIVITY signal,
# never as precise values. A rigorous certified-positive version (with a proven
# tail bound) remains an open meta task.
def li_S1_exact():
    """Exact S_1 = sum_rho 1/rho = 1 + gamma/2 - (1/2) ln(4 pi)."""
    return 1 + mp.euler / 2 - mp.log(4 * mp.pi) / 2


def li_power_sums(gammas, N):
    """Power sums S_j = sum_rho rho^(-j) for j=1..N.

    S_1 uses the exact closed form; S_j (j>=2) are summed over rho = 1/2 + i*g
    and their conjugates for g in `gammas` (absolutely convergent for j>=2).
    """
    S = {1: li_S1_exact()}
    rhos = [mp.mpf("0.5") + 1j * g for g in gammas]
    for j in range(2, N + 1):
        S[j] = mp.fsum(2 * mp.re(rho ** (-j)) for rho in rhos)
    return S


def li_coefficients_estimate(gammas, N):
    """Estimate the first N Li coefficients lambda_1..lambda_N from zero heights.

    Returns a list of mpf. These approach the true coefficients from below as
    len(gammas) grows; use for positivity, not exact values. (Alternating
    binomial sum -> watch cancellation for large N at fixed precision.)
    """
    S = li_power_sums(gammas, N)
    out = []
    for n in range(1, N + 1):
        v = mp.fsum(mp.binomial(n, j) * (-1) ** (j + 1) * S[j] for j in range(1, n + 1))
        out.append(v)
    return out


def li_selfcheck(tol=1e-8):
    """Audit: lambda_1 must equal the exact S_1 (independent of any zeros)."""
    lam1 = li_coefficients_estimate([], 1)[0]
    err = abs(lam1 - li_S1_exact())
    assert err < tol, f"li_selfcheck failed: lambda_1 error {err}"
    return True


def ks_distance(samples, cdf):
    """Kolmogorov-Smirnov distance between empirical samples and a CDF.

    `samples` is a list of mpf; `cdf` is a callable. Returns the sup norm
    sup_x |F_emp(x) - cdf(x)| as an mpf. Lower = better fit.
    """
    xs = sorted(mp.mpf(x) for x in samples)
    n = len(xs)
    d = mp.mpf(0)
    for i, x in enumerate(xs):
        f = cdf(x)
        lo = abs(mp.mpf(i) / n - f)
        hi = abs(mp.mpf(i + 1) / n - f)
        d = max(d, lo, hi)
    return d
