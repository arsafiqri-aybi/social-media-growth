# Dummy Many-to-Many Test — DUMMY-M2M-001

Status: **PASS**

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

A simplistic system might collapse the pattern into:
- "algorithm problem";
- "content is bad";
- "shares mean satisfaction";
- "more follows means loyalty".

The global reasoning system is required to reject those shortcuts.

## Expected and verified many-to-many behavior

The same observation bundle activates hypotheses across:

- Audience & Value;
- Communication & Content;
- Learning & Adaptation;
- Relationship & Retention;

while Distribution remains part of the exposure context rather than being automatically blamed.

Matched rule requirements:
- GR-001
- GR-007
- GR-008
- GR-009

Required forbidden overclaims include:
- algorithm_failure
- low_attention
- low_curiosity
- content_quality_declined
- audience_satisfied
- social_transmission_motive_identified
- loyalty_growth
- trust_growth

Required causal ceiling:
`observational_diagnosis_only`

Additional assertions:
- at least 8 competing explanations preserved;
- at least 4 next-test candidates preserved;
- no automatic HPC latent conclusion from raw metrics/proxies;
- deterministic repeated output.

## Verification

Commit under test:
`ea04ff9c4397327d5790fe0092f1096d325e3ab0`

GitHub Actions:
- workflow: **Test Reasoning Engine**
- run: **37334793718**
- test job: **SUCCESS**
- full test step: **SUCCESS**
- example reasoning case: **SUCCESS**

## Decision

`DUMMY_MANY_TO_MANY_TEST_PASS`

This demonstrates that the v0.1 runtime can preserve multiple simultaneous operational hypotheses and guardrails in one synthetic case.

It does not establish real-world predictive validity.
