# Human Psychological Core — Architecture Design 10/10

## Decision

**ARCHITECTURE DESIGN: COMPLETE**

The system is a **typed evidence graph with a retrieval hierarchy**, not a tree pretending to be cognition.

Hierarchy answers **"where does this construct belong?"**  
Graph edges answer **"how does it interact?"**

```text
L0 CORE FAMILY
   ↓ composition/retrieval
L1 MECHANISM MODULE
   ↓
L2 NEURON
   ↓ optional only when needed
L3 MICRO-NEURON

L0–L3  ↔  L0–L3 through typed scientific edges
           ↑
   context/moderators
           ↑
 observations → measurement mappings

Every inference
→ atomic claim(s)
→ source/evidence
→ uncertainty
→ audit trace
```

## 1. Ontology layers

### L0 — Core

A broad functional family. The existing eight remain **candidate anchors**:

Attention; Curiosity; Valuation & Emotion; Identity; Trust; Connection; Social Transmission; Reinforcement & Habit.

They are not assumed mutually exclusive or permanently correct. Research may trigger a Scale re-plan.

### L1 — Module

A module is a **mechanism cluster**, not a chapter heading.

A module exists only when grouping several neurons improves at least one of:
- explanatory coherence;
- evidence synthesis;
- measurement;
- reasoning;
- retrieval;
- verification.

Modules receive one or more role tags such as detection/representation, appraisal/valuation, motivation, control, learning, identity, normative, relational, action, recurrence, or monitoring.

### L2 — Neuron

The normal atomic reasoning unit.

A neuron must be sufficiently specific that:
- its definition is distinguishable;
- evidence can support or contradict it;
- it can participate in meaningful edges;
- measurement options can be stated;
- failure/boundary conditions can be attached.

### L3 — Micro-neuron

Optional. Use only when an L2 neuron still hides separable mechanisms, causal pathways, or measurement constructs.

**No mandatory L3 depth.**

## 2. Node schema

Every psychological node stores:

- stable immutable ID;
- label + aliases;
- level and lifecycle status;
- primary core;
- optional secondary memberships;
- parent module where applicable;
- role tags;
- atomic definition;
- inclusion/exclusion boundaries;
- mechanism summary;
- competing constructs;
- evidence claim IDs;
- incoming/outgoing edge IDs;
- moderator/context IDs;
- measurement IDs;
- uncertainty records;
- failure modes;
- open questions;
- content version + review metadata.

A node may belong primarily to one core while maintaining cross-core memberships. This prevents artificial duplication.

## 3. Edge ontology

Edges are first-class scientific objects.

Every material edge stores:

- immutable edge ID;
- source and target;
- relation type;
- polarity;
- directionality;
- mechanism;
- causal status;
- atomic claim IDs;
- supporting + contrasting evidence;
- moderator/context references;
- boundary conditions;
- transport limits;
- evidence quality;
- runtime parameter reference;
- lifecycle/review status.

### Critical separation

```text
SCIENTIFIC EDGE STRENGTH
        ≠
EMPIRICAL EFFECT SIZE
        ≠
RUNTIME PROPAGATION COEFFICIENT
```

They may become related only through an explicit calibration artifact.

## 4. Context / moderator model

Context is not a free-form dictionary anymore.

Ten first-class context families:

1. person
2. goal/task
3. content/message
4. creator/source
5. social/group
6. relationship history
7. temporal/learning history
8. platform/affordance
9. culture
10. situation/environment

A context modifier states:
- which node/edge it modifies;
- expected direction;
- mechanism;
- evidence claims;
- range/domain;
- whether evidence supports moderation or it is only a hypothesis.

## 5. Evidence architecture

Evidence is separated into:

```text
SOURCE
  ↓
ATOMIC CLAIM
  ↓
supports / contrasts / bounds
  ↓
NODE or EDGE
```

An **atomic claim** has one scientific assertion only.

Claim types include:
- descriptive;
- association;
- causal;
- mechanistic;
- moderation;
- mediation;
- measurement;
- null;
- contradiction;
- transport/generalization.

Each claim records study design, population, sample, construct definitions, outcome, effect estimates if comparable, uncertainty interval, heterogeneity/bias, context, and provenance.

Meta-analysis does not overwrite individual evidence; it becomes a synthesis object linked to its claims.

## 6. Measurement architecture

```text
OBSERVATION
→ PROXY / INSTRUMENT
→ possible latent targets
→ alternative explanations
→ measurement uncertainty
→ reasoning input
```

Each measurement mapping records:
- whether it is direct behavior, validated instrument, classifier, or weak proxy;
- reliability/validity evidence;
- target construct(s);
- alternative explanations;
- population/platform scope;
- missingness/selection risks;
- directionality;
- calibration state.

Therefore:
- shares can directly measure sharing behavior;
- they do not directly measure why someone shared;
- return rate cannot by itself establish habit;
- engagement cannot by itself establish trust.

## 7. Uncertainty model

The system keeps five independent uncertainty channels:

**Epistemic** — how strong/consistent is the scientific evidence?  
**Construct** — how clear/non-overlapping is the construct?  
**Measurement** — how well do observations identify the latent construct?  
**Transport/context** — will evidence generalize to this population/platform/context?  
**Runtime/model** — how much does the computational inference depend on heuristic architecture?

No single "confidence = 0.82" is allowed to erase these differences.

## 8. Reasoning architecture

Seven reasoning stages:

```text
R0 Intake + provenance
R1 Observation / measurement inference
R2 Local neuron & micro-neuron propagation
R3 Module synthesis
R4 Cross-core integration
R5 Competing explanations + conflict + counterfactual checks
R6 Calibrated conclusion
R7 Audit trace + uncertainty report
```

### Mandatory reasoning behavior

Before concluding from a high node activation, the runtime must ask:

- what observations created it?
- what alternative latent constructs explain those observations?
- what evidence supports the active edges?
- what contradictory evidence applies?
- which contexts/moderators are known or missing?
- is the path causal, correlational, or heuristic?
- what would change the conclusion?

## 9. Runtime parameter architecture

Runtime coefficients are stored separately from scientific edges.

Every runtime parameter declares an origin:

- `heuristic`
- `calibrated_empirical`
- `learned_from_benchmark`
- `fixed_system`

A heuristic parameter must never be described as an effect size or probability.

## 10. Versioning + invalidation

Stable IDs never silently change meaning.

Lifecycle:
`candidate → under_review → accepted/provisional → deprecated/rejected`

Material definition change:
- increment node content version;
- invalidate dependent evidence mappings, edges, measurements, and benchmark expectations that rely on changed semantics.

Evidence update:
- invalidate only linked claim syntheses/confidence and downstream inference artifacts;
- do not rebuild unrelated cores.

Rename:
- preserve ID;
- add old label as alias.

Merge/split:
- create explicit migration record;
- deprecate previous node;
- preserve provenance.

## 11. Existing v0.2 migration

The 29 current sub-neurons remain usable as **legacy candidate L2 nodes**.

They are **not automatically accepted into the 10/10 ontology**.

During the Research Program each will be:
- retained;
- refined;
- moved under an L1 module;
- split;
- merged;
- or deprecated,

based on evidence and non-redundancy review.

This preserves valid work without freezing early assumptions.

## 12. Architecture acceptance gates

Architecture Design passes when:

- layer meanings are non-overlapping;
- node/edge/evidence/measurement/context objects are separable;
- scientific strength is separated from runtime weight;
- uncertainty has multiple channels;
- version changes have explicit invalidation rules;
- current v0.2 can migrate without destructive reset;
- machine-readable validation can detect broken IDs and references.

These gates are implemented in the architecture validator/tests.

## Next stage

**RESEARCH PROGRAM**

The next task is not to add hundreds of neurons immediately.

First define the systematic research program for all eight cores:
- research questions;
- search vocabularies;
- inclusion/exclusion criteria;
- evidence extraction schema;
- contradiction search;
- saturation criteria;
- per-core research order;
- cross-core integration checkpoints.
