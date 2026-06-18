# RH approaches & computational tracks (object-level literature notes)

Cited grounding for the experiment tracks. The proposer MUST consult this before
inventing a method. Extend it with the `scout` role; keep sources attached. None
of this proves RH — it maps the falsifiable, computable surface.

## Equivalent reformulations that give a *computable* signal
- **Critical-line verification** (`zero_verification`). Hardy Z(t) is real and
  vanishes exactly at zeros on the line; #sign-changes of Z on (0,T] compared to
  the exact count N(T) (Turing's method) certifies all zeros up to T are simple
  and on the line. Record: >10^13 zeros verified (Platt; Gourdon 2004 to ~10^13).
  Tooling: `mpmath.siegelz`, `mpmath.nzeros`, `mpmath.siegeltheta`.
  Falsifiable: a resolved deficit would indicate an off-line/multiple zero.
- **Li's criterion** (`li_criterion`). RH <=> lambda_n >= 0 for all n>=1, where
  lambda_n = sum_rho [1-(1-1/rho)^n] (Li 1997; Bombieri-Lagarias 1999; Keiper
  1992 computed them). lambda_1 = 1 + gamma/2 - (1/2)ln(4pi) exactly. Caution:
  truncated zero-sums converge slowly (~ln(T)/T); use exact S_1 + power sums
  S_j=sum rho^-j (j>=2) and lambda_n = sum_j C(n,j)(-1)^(j+1) S_j, watching for
  cancellation at large n. Asymptotically lambda_n ~ (n/2)(ln n - 1 + gamma -
  ln 2pi) under RH.
- **de Bruijn-Newman constant** (`de_bruijn_newman`). RH <=> Lambda <= 0. Known:
  **0 <= Lambda <= 0.2** (lower bound Lambda>=0: Rodgers-Tao 2020; upper bound
  via Polymath15 / Tao). Close zero pairs push the lower bound up toward 0.
- **Robin's inequality** (`robin_inequality`). RH <=> sigma(n) < e^gamma n ln ln n
  for all n>5040 (Robin 1984). Extremal candidates: superabundant / colossally
  abundant numbers; primorials are the squarefree sub-family. sigma(n)/n exact
  from factorization. A violation with n>5040 disproves RH.
- **Explicit formula** (`explicit_formula`). Riemann-von Mangoldt / Weil explicit
  formula links sums over zeros to sums over primes (psi(x) = x - sum_rho
  x^rho/rho - ...). Residual checks: truncated zero-sum reconstructs the prime
  counting oscillations. Falsifiable consistency check, not a proof.

## Certified (rigorous) verification — the gold standard
- **Platt & Trudgian (2021): RH true up to height 3*10^12** (> 12.3*10^12 zeros),
  done *rigorously* with interval/ball arithmetic and rigorously derived
  truncation bounds -- not floating point. This is the benchmark for what
  "certified" means here. <https://arxiv.org/abs/2004.09765>
- **Tool: Arb** (via `python-flint`, available in this env) gives rigorous ball
  enclosures of zeta with proven error bars; `acb.zeta()`. A sign change of the
  real Hardy Z whose endpoint enclosures rigorously exclude 0 is a *proof* of a
  zero on the line. -> infinilab track `certified_zero_verification` is a
  faithful miniature of Platt-Trudgian. Cost: Arb zeta is slower than mpmath, so
  certified heights are lower, but the result is theorem-grade.
- Hardy Z certified via Z(t) = Re(exp(i*theta(t)) * zeta(1/2+it)), with
  theta(t) = Im(lgamma(1/4+i t/2)) - (t/2) ln(pi), all as Arb enclosures.

## de Bruijn-Newman, sharpened
- **Rodgers-Tao (2018/2020): Lambda >= 0** (Newman's conjecture), so RH <=>
  Lambda = 0. <https://terrytao.wordpress.com/2018/01/19/the-de-bruijn-newman-constant-is-non-negativ/>
- Historic lower bounds came from **Lehmer pairs** (very close zeros), e.g.
  Lambda > -1.14541*10^-11 (Saouter-Gourdon-Demichel) before Rodgers-Tao.
  -> lehmer_pairs feeds dB-N; report Lehmer-pair "strength", cite an exact
  formula before claiming a specific Lambda bound.

## Explicit formula, made precise (explicit_formula track)
- **von Mangoldt**: psi(x) = x - sum_rho x^rho/rho - ln(2*pi) - (1/2)ln(1-x^-2),
  sum over nontrivial zeros as a symmetric limit |Im rho| <= T. Truncating at the
  first N zeros reconstructs the prime oscillations of psi(x); residual vs the
  exact psi(x) (sum of von Mangoldt Lambda(n)) is a falsifiable consistency
  check. Under RH the zero-sum is O(x^{1/2+eps}). <https://arxiv.org/pdf/2312.00108>

## Statistics of the zeros (support, not equivalence)
- **Montgomery-Odlyzko / GUE** (`zero_statistics`). Pair correlation of zeros
  matches GUE random-matrix statistics (Montgomery 1973 conjecture; Odlyzko's
  computations). Hilbert-Polya: zeros as eigenvalues of a self-adjoint operator
  => all real => on the line. Spacing fits Wigner surmise, not Poisson.
- **Lehmer pairs** (`lehmer_pairs`). Anomalously close zeros (Lehmer 1956); the
  smallest normalized gaps. Feed de Bruijn-Newman lower bounds.

## Practical numerics (CPU, minutes)
- `mpmath`: zeta, zetazero, siegelz, siegeltheta, nzeros (pure-python, trusted).
- `python-flint` / `gmpy2`: faster big-arith if needed (optional).
- LMFDB hosts precomputed zeros to high height for cross-checking.
- Precision rule of thumb: dps must exceed ~ log10 of the height plus margin;
  sampling step must sit well below the local mean gap 2*pi/log(T).

## Where the headroom is (candidate next experiments)
- Push `zero_verification` T much higher (blocked Turing windows).
- Accurate Li coefficients via S_j + Richardson/extrapolation (needs a harness
  primitive; flagged as a meta task — see research/meta_log.md).
- de Bruijn-Newman lower bound from the closest observed Lehmer pair.
- Explicit-formula reconstruction of psi(x) from N zeros.
- Robin on colossally abundant (not just primorial) numbers.
