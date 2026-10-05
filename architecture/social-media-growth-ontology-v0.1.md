# Social Media Growth Global Ontology v0.1

Status: **provisional locked ontology**
Depends on: accepted HPC v1 baseline

## 1. Purpose

This ontology wraps the existing Human Psychological Core in a broader account-growth reasoning architecture without destroying the HPC local ontology.

The global system separates:
- what the account is trying to achieve;
- the context in which it operates;
- human psychological mechanisms;
- operational growth systems;
- evidence;
- observations;
- reasoning;
- account-local learning.

## 2. Global object classes

### governance_object
Defines goals, constraints, resources, risk boundaries, ethics, and horizon.

### context_dimension
A state or moderator such as platform, culture, audience segment, account maturity, format, category, creator history, or temporal condition.

### foundation_system
Stable upstream explanatory base. Current instance: Human Psychological Core.

### operational_core
A major irreducible operational problem family required for account growth reasoning.

Accepted candidate set v0.1:
- audience_value
- communication_content
- distribution_discovery
- relationship_retention
- learning_adaptation

### subsystem
A coherent cluster that improves explanation, retrieval, measurement, or decision-making.

### mechanism
A process that changes probability/state or explains a relationship.

### reasoning_unit
Smallest normally reusable unit that can own definition, evidence, edges, boundaries, and measurement mappings.

### scientific_edge
Evidence-qualified relationship between constructs/mechanisms.

### system_edge
Platform/environment opportunity or enabling relation that does not by itself assert a psychological state change.

### evidence_object
Source-backed claim/synthesis with method, population, context, support/contrast, and confidence.

### observation
Directly recorded event or state from an account/platform/user study.

### measurement_proxy
Mapping from an observation to a candidate construct with validity limits and competing explanations.

### intervention
Controlled or deliberate account change intended to test or alter a mechanism.

### prediction
Expected observable consequence conditional on a hypothesis/intervention.

### outcome
Observed result after exposure/intervention.

### uncertainty_record
Epistemic, construct, measurement, transport/context, or runtime uncertainty.

### benchmark_case
Scenario used to test diagnosis, explanation, and recommendation quality.

## 3. Global hierarchy

```text
G0 Governance
G1 Foundation
G2 Operational Core
G3 Subsystem
G4 Mechanism
G5 Reasoning Unit
G6 Connection
G7 Evidence
G8 Observation / Measurement
G9 Reasoning / Decision
G10 Feedback / Learning
```

This hierarchy is compositional, not a causal sequence.

## 4. Namespace compatibility

Existing HPC:
- L0 core family
- L1 mechanism module
- L2 neuron
- L3 optional micro-neuron

remains unchanged.

Global references should use namespace-qualified identities, for example:

- `hpc:L0:attention`
- `hpc:L2:...`
- `smg:G2:audience_value`
- `smg:G3:communication_content:positioning`

Do not migrate existing HPC IDs merely for cosmetic consistency.

## 5. Core boundary tests

A proposed new operational core must pass all tests:

1. **Distinct question** — solves a root problem not already represented.
2. **Irreducible failure mode** — can fail while peer cores function.
3. **Operational consequence** — materially changes diagnosis/intervention.
4. **Evidence footprint** — has a defensible independent literature/mechanism base.
5. **Cross-context relevance** — is not merely one platform feature or one business model.
6. **Non-duplication** — cannot be represented more cleanly as subsystem/context/outcome.
7. **Measurement route** — has observable consequences or testable implications.

If it fails, model it lower in the ontology.

## 6. Current core decisions

### audience_value
Represents audience model + external/account-side value hypothesis.

### communication_content
Represents encoding and creative/message execution.

### distribution_discovery
Represents exposure opportunity, retrieval, ranking, search, and network diffusion.

### relationship_retention
Represents account-level accumulation of relational and return states over time.

### learning_adaptation
Represents measurement, experimentation, diagnosis updating, and account-local calibration.

## 7. Cross-cutting non-core classes

Do not promote by default:
- brand;
- algorithm;
- virality;
- community;
- monetization;
- conversion;
- posting consistency;
- creator operations;
- trends;
- platform features.

These may become subsystems, mechanisms, contexts, interventions, or outcomes depending on function.

## 8. Edge vocabulary

Reuse existing HPC edge semantics where compatible and extend cautiously.

Candidate global relations:
- causes_increase
- causes_decrease
- supports
- inhibits
- biases
- enables
- competes_with
- updates
- reinforces
- mediates
- moderates
- predicts
- associates_with
- feedback_link
- system_exposure
- constrains
- selects
- encodes
- retrieves
- ranks
- exposes
- measures
- tests
- falsifies

A new relation type requires a semantic distinction, not merely different wording.

## 9. Scientific separation

Keep separate:
- scientific evidence strength;
- observed effect magnitude;
- account-local predictive association;
- runtime traversal parameter;
- platform metric.

No automatic transformation between them.

## 10. Lifecycle

Global ontology objects may be:
- candidate
- under_review
- accepted
- provisional
- deprecated
- rejected

The current five operational cores are **accepted_provisional_v0.1**.
