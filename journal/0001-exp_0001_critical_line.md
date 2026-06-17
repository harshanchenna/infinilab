# Iteration 0001 -- Critical-line verification via Z sign changes vs N(T)

- **module**: `experiments.exp_0001_critical_line`
- **track**: `zero_verification`
- **status**: OK  |  **kept**: True  |  **falsified**: False
- **frontier**: T_verified = 150.0
- **skeptic**: sound -- Classic Z-sign-change vs Turing N(T) check, correctly applied. At T=150, dps=15 and step=1/16 (mean gap ~1.25) are well within tolerance; no precision/resolution artifact. N(150)=52 matches the asymptotic and known tables. Claim is scoped to verified height, disclaims RH proof, attributes to Odlyzko/LMFDB, and never overclaims falsification. Honestly entailed.
- **elapsed**: 4.0s

## Hypothesis
Every nontrivial zero with 0 < Im < T lies on Re = 1/2.

## Claim (entailed by the numbers)
All 52 nontrivial zeros with 0 < Im < 150.00 lie on the critical line: Hardy Z has exactly N(T)=52 sign changes.

## Metrics
```json
{
  "T": 150.0,
  "step": 0.0625,
  "n_sign_changes": 52,
  "n_exact_NT": 52,
  "n_samples": 2401,
  "matched": true
}
```

## Evidence
```json
{
  "method": "Riemann-Siegel Z sign changes vs Turing N(T)",
  "matched": true
}
```
