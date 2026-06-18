# Iteration 0010 -- Certified verification toward T=10000

- **module**: `experiments.exp_0010_certified_10k`
- **track**: `certified_zero_verification`
- **status**: OK  |  **kept**: True  |  **falsified**: False
- **frontier**: certified_T = 5000.0
- **skeptic**: sound -- Claim certifies T=5000 (not the aspirational 10000) and is conservative: the 5250 mismatch shows a missed pair under the 1/16 grid, but that only lowers certified_T—it never falsely certifies, since proven==N(T) at every checkpoint up to 5000 forces all zeros there onto the line. frontier_value=5000 genuinely backed. Honest interpretation.
- **elapsed**: 62.6s

## Hypothesis
Every zero up to height T is provably on Re=1/2.

## Claim (entailed by the numbers)
CERTIFIED: all zeros up to T=5000 proven on the critical line via Arb ball arithmetic (4785 proven on-line zeros, matching N(T) at every 250-step checkpoint, no uncertified points). Halted: count/parity mismatch at T=5250 (proven=4785, N(T)=4787, uncertified=0).

## Metrics
```json
{
  "certified_T": 5000.0,
  "prec_bits": 200,
  "step": 0.0625,
  "proven_on_line_zeros": 4785,
  "reached_T": 5250.0,
  "uncertified_points": 0,
  "halted_reason": "count/parity mismatch at T=5250 (proven=4785, N(T)=4787, uncertified=0)"
}
```

## Evidence
```json
{
  "method": "Arb rigorous Hardy-Z; checkpointed proven-count == N(T)",
  "proven_on_line_zeros": 4785,
  "certified_T": 5000.0
}
```
