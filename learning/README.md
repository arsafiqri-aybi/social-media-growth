# Prediction → Outcome Learning

This package implements the final account-local learning loop:

```text
diagnosis
→ hypothesis
→ precommitted prediction
→ intervention
→ observed outcome
→ support / falsification / inconclusive
→ account-local belief summary
```

## Hard boundary

This layer **cannot mutate scientific evidence**.

A successful local prediction does not:
- promote a scientific edge;
- change HPC node lifecycle;
- establish universal causality;
- become an empirical effect size.

A failed prediction is also retained rather than hidden.

## Why no probability score yet

The current system counts actual local outcomes and records whether they support, falsify, or fail to resolve a prediction.

It deliberately does not turn a small number of observations into a fake Bayesian probability. Formal probabilistic calibration requires a separately validated model and sufficient data.

## Real-world status

The infrastructure is executable and testable.

Real-world predictive validation remains **pending actual prospective account data**.
