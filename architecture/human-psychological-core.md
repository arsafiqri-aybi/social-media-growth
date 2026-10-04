# Human Psychological Core

## Purpose

Model the human mechanisms that determine why people notice, seek, value, identify with, trust, connect to, transmit, and repeatedly return to social-media information and creators.

The system is **not**:

```
Attention -> Curiosity -> Emotion -> Identity -> Trust -> ...
```

It is a many-to-many network.

## Core node set v0.1

| ID | Core neuron | Core question |
|---|---|---|
| HPC-01 | Attention | What receives limited processing priority? |
| HPC-02 | Curiosity | Why does a person seek additional information? |
| HPC-03 | Valuation & Emotion | Why does information feel important, rewarding, or affectively activating? |
| HPC-04 | Identity | How does self/group representation shape perception and behavior? |
| HPC-05 | Trust | Why is a source or message treated as credible/reliable? |
| HPC-06 | Connection | How does psychological relational attachment to a creator/source form? |
| HPC-07 | Social Transmission | Why is information passed to other people? |
| HPC-08 | Reinforcement & Habit | Why does behavior become more likely to recur in recurring contexts? |

## Important correction

Two earlier labels mixed mechanisms with outcomes:

- **Emotion / Value**: emotion and valuation are related but not identical. They remain one core family for now, with separate subnodes.
- **Return / Reinforcement**: return is an observed behavior; reinforcement/habit are candidate mechanisms that help explain recurrence.

## Node schema

Every neuron must eventually contain:

1. Definition
2. Underlying mechanism
3. Evidence base
4. Boundary conditions
5. Social-media relevance
6. Incoming edges
7. Outgoing edges
8. Failure modes / misuse
9. Confidence
10. Open questions

## Edge schema

Every material connection must record:

- source node
- target node
- direction
- relation type
- mechanism
- evidence type
- causal status
- moderators / boundary conditions
- confidence
- source

Possible relation types include:

- activates
- biases
- increases probability
- moderates
- mediates
- reinforces
- inhibits
- co-varies
- enables
- feedback

## Connector mechanisms

Some psychologically important mechanisms should not automatically become ninth/tenth core neurons. They can act as connectors across several nodes.

Initial connector candidates:

- goals
- context
- novelty
- uncertainty
- familiarity
- reward learning
- social norms
- homophily / similarity
- perceived relevance
- memory / learning

## Evidence labels

- **Established** — converging evidence including strong reviews/meta-analysis and/or replicated experimental work.
- **Strongly supported** — multiple good studies/reviews; causal scope may still be bounded.
- **Moderately supported** — meaningful evidence, but heterogeneity or causal limitations remain.
- **Emerging** — promising evidence but architecture should remain provisional.
- **Hypothesis** — useful connection requiring direct verification.

## Architecture rule

A node can:
- influence multiple other nodes;
- be influenced by multiple nodes;
- participate in multiple feedback loops;
- change strength by audience, context, platform, culture, topic, and prior learning.

Therefore, the architecture stores **typed weighted edges**, not a single sequence.
