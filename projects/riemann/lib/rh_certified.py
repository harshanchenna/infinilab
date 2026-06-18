"""Certified (rigorous) primitives via Arb ball arithmetic (python-flint).

Added by the meta-optimizer. Unlike `rh_lib` (mpmath, fast floating point), this
module produces THEOREM-GRADE results: every quantity is an Arb ball carrying a
proven error bound, so a certified sign is a *proof*, not a heuristic. This is a
miniature of the method behind Platt & Trudgian's rigorous verification of RH to
height 3e12 (arXiv:2004.09765); see research/rh_approaches.md.

Requires `python-flint` (Arb). Import fails loudly if unavailable so experiments
that need certification cannot silently fall back to non-rigorous arithmetic.

Hardy Z is computed rigorously as
    Z(t) = Re( exp(i*theta(t)) * zeta(1/2 + i t) ),
    theta(t) = Im(lgamma(1/4 + i t/2)) - (t/2) ln(pi),
all as Arb enclosures. A *certified sign change* of Z between two points -- where
both endpoint enclosures rigorously exclude 0 and have opposite sign -- is a
proof of a simple zero of zeta on the critical line between them.
"""
from __future__ import annotations

from flint import acb, arb, ctx  # hard dependency: no silent fallback


def set_prec(bits: int = 256) -> None:
    """Set Arb working precision in bits."""
    ctx.prec = bits


def _logpi() -> arb:
    return arb.pi().log()


def hardy_z(t) -> arb:
    """Rigorous Arb enclosure of the Hardy function Z(t) (real)."""
    tt = arb(t)
    s = acb(arb("0.25"), tt / 2)
    theta = s.lgamma().imag - (tt / 2) * _logpi()
    rot = acb(arb(0), theta).exp()                 # e^{i theta}
    zl = acb(arb("0.5"), tt).zeta()                # zeta(1/2 + i t)
    return (rot * zl).real                          # rigorous real enclosure


def certified_sign(z: arb) -> int:
    """+1 / -1 if the ball rigorously excludes 0 with that sign, else 0."""
    if z > 0:
        return 1
    if z < 0:
        return -1
    return 0


def count_certified_sign_changes(t0, t1, step):
    """Count rigorously certified sign changes of Z on (t0, t1].

    Returns (n_changes, n_uncertified, last_certified_t):
      * n_changes        proven zeros on the critical line found in the range,
      * n_uncertified    grid points whose Z-ball contained 0 (sign not provable
                         at this precision/step),
      * last_certified_t the largest t reached with NO uncertified point so far
                         (the height up to which the certification is clean).
    A clean run has n_uncertified == 0 and last_certified_t == t1.
    """
    import mpmath as mp

    t = mp.mpf(t0)
    t1 = mp.mpf(t1)
    step = mp.mpf(step)
    prev = certified_sign(hardy_z(str(t)))
    n_changes = 0
    n_uncertified = 0 if prev != 0 else 1
    last_certified_t = t if prev != 0 else mp.mpf(t0)
    while t < t1:
        t += step
        s = certified_sign(hardy_z(str(t)))
        if s == 0:
            n_uncertified += 1
        else:
            if prev != 0 and s != prev:
                n_changes += 1
            prev = s
            if n_uncertified == 0:
                last_certified_t = t
    return n_changes, n_uncertified, float(last_certified_t)


def selfcheck() -> bool:
    """Audit: known certified signs around the first zero (gamma_1 ~ 14.1347)."""
    set_prec(256)
    assert certified_sign(hardy_z("14.0")) == -1, "Z(14.0) should be certified negative"
    assert certified_sign(hardy_z("14.5")) == 1, "Z(14.5) should be certified positive"
    # And a proven sign change implies a zero between them.
    n, unc, _ = count_certified_sign_changes("14.0", "14.5", "0.25")
    assert n == 1 and unc == 0, f"expected 1 certified change, got {n} (unc={unc})"
    return True
