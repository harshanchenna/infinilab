# Iteration 0004 -- Critical-line verification to greater height (T up to ~600)

- **module**: `experiments.exp_0004_critical_line_high`
- **track**: `zero_verification`
- **status**: OK  |  **kept**: True  |  **falsified**: False
- **frontier**: T_verified = 600.0
- **skeptic**: sound -- Step 0.0625 vs mean gap ~0.98 (~15 samples/gap), dps=18 adequate for T=600. Match of sign-changes to Turing N(T)=341 is self-certifying (under-resolution fails the equality, not passes it), so the claim is correctly scoped to height 600 with no RH overreach or misattribution.
- **elapsed**: 60.9s

## Hypothesis
Every nontrivial zero with 0 < Im < T lies on Re = 1/2.

## Claim (entailed by the numbers)
All 341 nontrivial zeros with 0 < Im < 600.00 lie on the critical line: Hardy Z has exactly N(T)=341 sign changes.

## Metrics
```json
{
  "T": 600.0,
  "step": 0.0625,
  "n_sign_changes": 341,
  "n_exact_NT": 341,
  "n_samples": 9601,
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
