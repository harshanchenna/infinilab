"""Project descriptor: Riemann Hypothesis.

A project supplies its research TRACKS and a short NAME; the generic engine
(harness/) supplies everything else (contract, verifier, ledger, skeptic, loop).
The active project is selected by the INFINILAB_PROJECT env var (default
projects.riemann) and resolved by harness/project.py.
"""

NAME = "riemann"

# The main conjecture this project probes (used in prompts / honest framing).
CONJECTURE = "Riemann Hypothesis: all nontrivial zeros of zeta have real part 1/2."

TRACKS = {
    "zero_verification": "All zeros up to height T lie on the critical line (Z sign changes == N(T)).",
    "certified_zero_verification": "Theorem-grade: zeros on the line up to T PROVEN via Arb ball arithmetic.",
    "zero_statistics": "Normalized zero spacings follow GUE (Montgomery-Odlyzko).",
    "lehmer_pairs": "Search for anomalously close zero pairs; smallest normalized gap.",
    "li_criterion": "Li/Keiper coefficients lambda_n are non-negative (lambda_n >= 0 <=> RH).",
    "de_bruijn_newman": "Bounds on the de Bruijn-Newman constant Lambda (RH <=> Lambda <= 0).",
    "explicit_formula": "Riemann's explicit formula linking zeros and primes; residual checks.",
    "robin_inequality": "Robin's inequality sigma(n) < e^gamma n log log n for n > 5040 (<=> RH).",
    "conjecture_discovery": "Search for new closed forms / integer relations among zeros and constants (Ramanujan-Machine style).",
}
