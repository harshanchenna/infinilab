# Iteration 0009 -- Certified verification to greater height (checkpointed)

- **module**: `experiments.exp_0009_certified_high`
- **track**: `certified_zero_verification`
- **status**: OK  |  **kept**: True  |  **falsified**: False
- **frontier**: certified_T = 2000.0
- **skeptic**: sound -- Standard rigorous method (Arb certified sign changes + count-match to N(T)), correctly bounded to T=2000 with no RH-proof overclaim. N(2000)≈1517 matches; 200 bits and step 1/16 (~13 samples/gap) are adequate; missed pairs only lower certified height. Rests on harness's N_exact/certified_sign being rigorous, which Tier-1 confirmed.
- **elapsed**: 15.8s

## Hypothesis
Every zero up to height T is provably on Re=1/2.

## Claim (entailed by the numbers)
CERTIFIED: all zeros up to T=2000 proven on the critical line via Arb ball arithmetic (1517 proven on-line zeros, matching N(T) at every 100-step checkpoint, no uncertified points). Halted: reached target.

## Metrics
```json
{
  "certified_T": 2000.0,
  "prec_bits": 200,
  "step": 0.0625,
  "proven_on_line_zeros": 1517,
  "reached_T": 2000.0,
  "uncertified_points": 0,
  "halted_reason": "reached target"
}
```

## Evidence
```json
{
  "method": "Arb rigorous Hardy-Z; checkpointed proven-count == N(T)",
  "proven_on_line_zeros": 1517,
  "certified_T": 2000.0
}
```
