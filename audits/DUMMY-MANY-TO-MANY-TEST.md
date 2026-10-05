# Dummy Many-to-Many Test — DUMMY-M2M-001

Status: **COMMITTED FOR CI EXECUTION**

## Dummy observation pattern

- exposure: high
- selection: low
- non-follower reach: up
- continuation: down
- shares: up
- satisfaction: unknown
- follows: up
- return: down

## Why this case is adversarial

A simplistic system might say:
- "algorithm problem";
- "content is bad";
- "shares mean satisfaction";
- "more follows means loyalty".

The global reasoning system must reject those shortcuts.

## Expected many-to-many behavior

The same observation bundle should activate hypotheses across:

- Audience & Value;
- Communication & Content;
- Learning & Adaptation;
- Relationship & Retention;

while Distribution remains part of the observed exposure context rather than automatically being blamed.

Expected matched operational rules:
- GR-001
- GR-007
- GR-008
- GR-009

Expected causal ceiling:
`observational_diagnosis_only`

The test also requires:
- plural competing explanations;
- plural next-test candidates;
- no automatic HPC latent conclusion from raw metrics/proxies;
- deterministic repeated output.

## Verification

See:
- `examples/dummy_many_to_many_case.json`
- `tests/test_dummy_many_to_many.py`

CI result must be checked before marking this dummy test PASS.
