# Social Media Growth

Research-grounded neural knowledge architecture and executable reasoning system for building and growing social-media accounts.

## Current stage

**Human Psychological Core — Reasoning System v0.2**

The repository models social-media psychology as a **dynamic network**, not a linear funnel.

```text
observations
   ↓
measurement proxies + ambiguity
   ↓
29 sub-neurons
   ↕
mechanism-level propagation
   ↓
8 core neurons
   ↕
evidence-weighted network reasoning
   ↓
dominant mechanisms + tensions + evidence warnings
```

## Eight core neurons

1. Attention
2. Curiosity
3. Valuation & Emotion
4. Identity
5. Trust
6. Connection
7. Social Transmission
8. Reinforcement & Habit

## What v0.2 adds

- 29 mechanism-level sub-neurons
- hierarchical sub-neuron → core reasoning
- measurement/proxy layer for real account analytics
- negative evidence handling
- empirical evidence registry
- published effect-size metadata where available
- contradiction / boundary-condition registry
- evidence warnings attached to active reasoning paths
- 15 automated tests

## Run

Core-only reasoning:

```bash
python -m engine.cli examples/case_identity_curiosity.json
```

Observation → sub-neuron → core reasoning:

```bash
python -m engine.hierarchical_cli examples/observed_case.json
```

Tests:

```bash
python -m unittest discover -s tests -v
```

## Scientific constraint

This is a transparent decision-support reasoner, **not a biological brain simulation**.

Important:

- architecture weights are not automatically empirical effect sizes;
- analytics are not direct mind-state measurements;
- correlation is not treated as causation;
- uncertainty, heterogeneity, and contradictory evidence are retained;
- weak/emerging edges are discounted rather than presented as fact.

See:

- `research/evidence_registry.json`
- `research/contradictions.json`
- `research/effect-size-policy.md`
- `docs/measurement-layer.md`
- `docs/sub-neuron-layer.md`

## CI

GitHub Actions runs the full unit-test suite and a reasoning example on pushes to `main` and on pull requests.
