# Phase 7 — High-Centrality Mechanism Depth v0.1

Status: **MINIMUM TARGETED DEPTH COMPLETE**

Phase 7 does not attempt exhaustive decomposition. It deepens only the pathways most likely to cause wrong account-level diagnosis if left ambiguous.

## Selected packages

1. **Audience–Value Fit**
2. **Message / Creative Response**
3. **Exposure vs Human Response**
4. **Trust / Relationship Accumulation**
5. **Measurement / Experimental Learning**

The machine-readable reasoning units live in:
`mechanisms/phase7-mechanism-registry-v0.1.json`

## 1. Audience–Value Fit

Canonical reasoning chain:

```text
audience-state hypothesis
        ↓
segment/heterogeneity representation
        ↓
value hypothesis
        ↓
relevance-fit hypothesis
        ↓
content + distribution choices
        ↓
observed response
        ↓
composition/confound check
        ↓
account-local update
```

Key decision:
**Audience & Value remains one core for now.**

Reason:
Audience representation and value proposition have different objects but are tightly coupled operationally. Current evidence does not justify a root split, while the registry already separates audience-state, segment heterogeneity, value hypothesis and relevance fit as distinct reasoning units.

Segmentation guardrail:
A cluster is useful only when it improves explanation or action. Mathematical separation alone is not enough. Domain interpretation, stability, outcome relevance and transport matter.

## 2. Message / Creative Response

The global system must not use one generic "engagement" state.

Minimum observable decomposition:

```text
EXPOSED
  ↓
APPEAL / SELECT?
  ↓
CONTINUE CONSUMING?
  ↓
SATISFIED / VALUED?
  ↓
ACT / RETURN / SHARE?
```

This is not a universal funnel. People can act without completing, return without sharing, or be satisfied without publicly engaging.

Operational distinction:
- **Appeal**: choice to begin/avoid.
- **Continuation**: persistence after selection.
- **Satisfaction**: post-consumption evaluation, requiring qualified evidence.

Content-characteristic effects stay context-dependent. No universal rule such as "video always wins", "shorter always wins", or "emotion always wins" may become canonical.

## 3. Exposure vs Human Response

Mandatory separation:

```text
eligibility
→ retrieval/ranking
→ exposure opportunity
→ human selection
→ continuation
→ evaluation/satisfaction
→ action
```

Platform systems and human psychology occupy different layers.

Therefore:
- recommendation ≠ attention;
- impression ≠ interest;
- completion ≠ satisfaction;
- share ≠ a unique transmission motive;
- follow ≠ trust;
- return ≠ habit.

Personalized ranking creates an additional problem:
**the audience receiving later content can be partly shaped by earlier responses.**
Metric changes can therefore reflect changing exposure composition rather than a stable underlying audience preference.

## 4. Trust / Relationship Accumulation

Relationship & Retention owns **longitudinal account-level composition**, while latent Trust, Connection, Identity and Reinforcement remain in HPC.

Minimum representation:

```text
repeated encounter
    ↓
familiarity / recognition hypothesis
    ↓
credibility + expectation evidence
    ↕
HPC trust / connection / identity
    ↓
relationship-state hypothesis
    ↓
return / participation / loyalty / advocacy observations
```

Parasocial relationship remains a real construct but must not be inferred from:
- follows alone;
- comments alone;
- returning viewers alone;
- watch time alone.

Use validated constructs or strong triangulation when a PSR claim matters.

## 5. Measurement / Experimental Learning

Canonical diagnostic loop:

```text
OBSERVATION
↓
VALIDITY CLASS
↓
COMPETING EXPLANATIONS
↓
IDENTIFIABILITY CHECK
↓
HYPOTHESIS
↓
PREDICTION
↓
INTERVENTION
↓
OUTCOME
↓
FALSIFICATION CHECK
↓
ACCOUNT-LOCAL UPDATE
```

Critical research-method guardrail:
Platform "A/B tests" do not automatically imply clean random assignment at the user-exposure level. Delivery and targeting systems may differ across conditions, creating confounding between creative and platform selection.

The engine must therefore describe causal confidence based on design, not on the label "A/B test".

## 6. Cross-package causal tension examples

### Case: high reach, weak continuation
Candidate interpretations:
- distribution opportunity succeeded;
- initial appeal may be weak;
- audience composition may be broad/poorly fit;
- content expectation may mismatch delivery.

Do not conclude "algorithm problem" from this pattern.

### Case: strong completion, weak return
Candidate interpretations:
- content satisfies one-off intent;
- weak creator/account relationship;
- low recurring value;
- distribution does not create repeated opportunity;
- series/expectation structure absent.

Do not conclude "content failed".

### Case: rising likes, falling qualified conversions
Candidate interpretations:
- audience composition shifted;
- content became more broadly appealing but less goal-relevant;
- metric proxy is misaligned with Governance objective;
- distribution reached lower-intent viewers.

Do not optimize likes automatically.

### Case: returning viewers rise
Candidate interpretations include:
- increased familiarity;
- series structure;
- platform rediscovery;
- genuine relationship;
- habitual cue-response;
- repeated topical need.

Do not infer habit or loyalty without stronger evidence.

## Phase 7 decision

The five high-centrality packages now have sufficiently distinct reasoning units, boundaries, evidence classes and failure warnings to support global measurement design.

**Phase 7 v0.1 gate: PASS.**

This is not mechanism saturation. Further depth is triggered by benchmark failure, measurement ambiguity, conflicting evidence, or a downstream reasoning dependency.
