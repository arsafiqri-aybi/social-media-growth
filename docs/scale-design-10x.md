# Human Psychological Core — Scale Design 10/10

## Status

**PROMPT LOCK: COMPLETE**  
**SCALE DESIGN: COMPLETE**  
**NEXT: ARCHITECTURE DESIGN**

## Scaling principle

The goal is not to maximize node count. The goal is the **smallest architecture that can pass every scientific, reasoning, measurement, and verification gate**.

Counts below are only capacity envelopes. They are not completion targets.

| Layer | Initial capacity envelope | Expansion rule |
|---|---:|---|
| Core families | 8 candidate anchors | change only after ontology evidence review |
| Mechanism modules | ~4–12/core | add only if a distinct mechanism needs its own evidence/logic |
| Substantive neurons | ~15–50/core | add only if it improves explanation, reasoning, measurement or retrieval |
| Micro-neurons | on demand | split only when a neuron bundles separable mechanisms |
| Material edges | no fixed count | every edge requires mechanism + evidence + integration value |

This gives an initial **capacity** of roughly 32–96 modules and 120–400 substantive neurons, but the system may finish smaller or require a Scale re-plan. The numbers are not a success metric.

## Execution architecture

```text
S0  State + ontology audit
        ↓
S1  Eight bounded core research programs
        ↕
S2  Cross-core connectors / edge program
        ↓
S3  Measurement + construct-validity program
        ↓
S4  Empirical calibration program
        ↓
S5  Executable reasoning integration
        ↓
S6  Benchmark + adversarial evaluation
        ↓
S7  Gap / saturation audit
        ↺ refine only failed descendants
```

### Why this route

A single depth-first stream would over-develop one core while leaving hidden gaps elsewhere. Eight bounded core workstreams give breadth, while a cross-core integrator prevents the result from becoming eight isolated psychology libraries.

The verifier is structurally separate from synthesis: supporting literature alone cannot close a gate. Every core needs contradiction/boundary search and an ontology-overlap audit.

## Per-core minimum research package

Each core must eventually cover:

1. construct definition and competing definitions;
2. major mechanism families;
3. causal evidence where available;
4. correlational/observational evidence;
5. cognitive/neural basis where materially explanatory;
6. individual differences;
7. social and cultural moderators;
8. context/platform transfer limits;
9. contradictory/null evidence;
10. measurement instruments/proxies;
11. cross-core incoming/outgoing mechanisms;
12. failure modes and open questions.

## Completion is evidence-based, not count-based

A core is not complete because it has 30 neurons. It is complete only when:

- major mechanisms are represented;
- no major mechanism remains bundled ambiguously;
- deliberate disconfirmation search has been performed;
- important moderators and boundary conditions are represented;
- measurement ambiguity is explicit;
- material cross-core connections are typed and evidence-backed;
- remaining retrieval yields mostly refinement rather than structural change.

## Reasoning scale

The final runtime must reason at multiple levels:

```text
Observation
→ measurement/proxy evidence
→ micro/neuron mechanisms
→ module state
→ core state
↔ cross-core network
→ competing explanations
→ uncertainty + contradiction
→ auditable synthesis
```

A high activation value may never be interpreted alone. The system must inspect alternative causes, opposing edges, context, evidence quality, and measurement ambiguity.

## Verification architecture

Three independent evidence classes must remain distinct:

- **scientific evidence** — papers/reviews/meta-analyses;
- **software evidence** — schema/unit/integration/CI tests;
- **predictive evidence** — benchmark cases and later real outcome evaluation.

Passing software tests does not prove psychology is correct. A strong paper does not prove implementation is correct. Both are required.

## Re-plan conditions

Return to Scale rather than forcing the current design if:

- a core must split;
- two cores cannot be cleanly distinguished;
- a fundamental mechanism falls outside all eight cores;
- connection/context representation cannot express conflicting evidence;
- measurement cannot distinguish major alternative explanations;
- repeated benchmark failure shows architecture, not implementation, is the bottleneck.

## Governor boundary

Governor may optimize retrieval, context, effort, reuse, and retry strategy.

It may **not** reduce evidence standards, remove contradiction search, hide uncertainty, relax measurement validity, or declare completion while a mandatory gate is open.

## Current decision

The current 8-core architecture is **preserved as an upstream candidate**, not frozen as truth.

No further neuron expansion should occur until **Architecture Design** defines:

- module taxonomy;
- node schema;
- edge ontology;
- moderator/context model;
- evidence object;
- measurement object;
- uncertainty model;
- reasoning layers;
- versioning/invalidation rules.

That is the next stage.
