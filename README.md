# Social Media Growth

Research-grounded neural knowledge architecture for building and growing social-media accounts.

## Current stage

**Human Psychological Core + Neural Reasoning Layer v0.1**

This repository is no longer only a knowledge library. It contains an executable, auditable graph reasoner that uses the eight core psychological families as nodes and evidence-weighted relationships as edges.

## Core neurons

1. Attention
2. Curiosity
3. Valuation & Emotion
4. Identity
5. Trust
6. Connection
7. Social Transmission
8. Reinforcement & Habit

These are candidate core families, not immutable truths.

## Runtime concept

```text
observations
   ↓
seed activations + context
   ↓
8-node psychological network
   ↕
typed, weighted, evidence-discounted edges
   ↓
iterative propagation
   ↓
dominant mechanisms + conflicts + audit trace
```

The architecture is **not a linear funnel** and the numeric weights are **not claimed empirical effect sizes**. Weak evidence is explicitly discounted and every propagated conclusion can be traced back to edges and mechanisms.

## Run

```bash
python -m engine.cli examples/case_identity_curiosity.json
python -m unittest discover -s tests -v
```

No third-party Python dependencies are required for v0.1.

## Repository map

- `neurons/` — research-grounded base knowledge for each core family
- `connections/core-edge-map.md` — conceptual edge map
- `data/nodes.json` — machine-readable node registry
- `data/edges.json` — machine-readable weighted edge registry
- `engine/` — executable reasoning runtime
- `tests/` — deterministic behavioral tests
- `examples/` — example reasoning cases
- `docs/reasoning-engine.md` — runtime and scientific guardrails
- `research/` — evidence policy and source registry

## Scientific constraint

The engine is a **decision-support model**, not a biological simulation of the brain. It can reason consistently over the knowledge architecture, expose interactions, and surface uncertainty. It must not turn heuristic weights into fake psychological precision.

## Scope lock

The current layer focuses on the **Human Psychological Core**. Platform algorithms, content formats, branding, production, monetization, and growth tactics should connect later rather than contaminate this base layer.
