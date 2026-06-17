# Iteration 0005 -- Robin's inequality on the primorials

- **module**: `experiments.exp_0005_robin_primorials`
- **track**: `robin_inequality`
- **status**: OK  |  **kept**: True  |  **falsified**: False
- **frontier**: n_primorials_checked = 1995.0
- **skeptic**: sound -- Max ratio at k=6 is correct: primorial Robin ratio decreases monotonically toward limit 6/pi^2~0.608, so the first qualifying primorial is the worst case. dps=30 vastly sufficient vs ratios ~0.6-0.78 far below 1. Claim honestly scoped as 'consistent with RH on primorials,' not a proof; falsification condition correct. Frontier count (1995) genuine.
- **elapsed**: 2.3s

## Hypothesis
sigma(n) < e^gamma n ln ln n for every primorial n > 5040.

## Claim (entailed by the numbers)
Robin's inequality holds for all 1995 primorials P_k > 5040 up to k=2000: max ratio f=0.77546 at k=6 (< 1). Consistent with RH on the primorial family.

## Metrics
```json
{
  "n_primorials_checked": 1995,
  "largest_k": 2000,
  "max_robin_ratio": 0.7754605402051012,
  "max_ratio_at_k": 6,
  "ln_largest_primorial": 17228.579093450142,
  "violation": false
}
```

## Evidence
```json
{
  "method": "exact sigma/n = prod(1+1/p) for squarefree primorials; ratio vs e^gamma ln ln n",
  "max_ratio": 0.7754605402051012,
  "worst_violation": null
}
```
