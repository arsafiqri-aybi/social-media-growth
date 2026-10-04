# Neural Reasoning Layer v0.1

## What this layer is

The engine turns the Human Psychological Core from a static library into an executable, auditable inference graph.

It does **not** claim to simulate the brain. It is a computational decision-support model grounded in the repository's evidence map.

## Runtime

```text
observations / seed activations
        ↓
context modifiers
        ↓
activate relevant core neurons
        ↓
propagate across typed weighted edges
        ↓
discount edges by evidence confidence
        ↓
normalize graph pressure
        ↓
iterate until convergence / max iterations
        ↓
surface dominant activations + trace + tensions
```

## Why evidence confidence changes propagation

An edge marked `strong` should influence the result more than an edge marked `emerging`. The engine therefore multiplies edge strength by a confidence coefficient.

This coefficient is **not an effect size** and **not a probability that a theory is true**. It is an architecture-level penalty that prevents weak evidence from dominating the inference graph.

## Input contract

A case supplies:

- seed activations `[0,1]`: observations/hypotheses about the case;
- context values `[0,1]`: known moderators;
- optional goals/notes.

Example:

```json
{
  "seeds": {
    "identity": 0.82,
    "curiosity": 0.70,
    "trust": 0.35,
    "valuation_emotion": 0.68
  },
  "context": {
    "high_arousal": 0.75
  }
}
```

## Output contract

The reasoner returns:

- final node activations;
- evidence-signal per node;
- support and inhibition;
- strongest edge contributions;
- dominant nodes;
- convergence metadata;
- tensions/conflicts.

## Important scientific guardrails

1. Activation is **not** a psychological measurement unless seeded from a validated measure.
2. Weight is **not** automatically an empirical effect size.
3. An edge can be useful for reasoning while remaining `emerging`.
4. Correlational evidence must not be labelled causal.
5. Platform outcomes such as views or virality are external system outcomes, not psychological nodes.
6. Weights should be replaced/refined when effect-size evidence is available.
7. Context can change edge strength; no universal "best content" is assumed.

## Next research upgrades

- empirical effect-size registry;
- negative/inhibitory edges;
- measurement layer that maps observed metrics to latent nodes;
- contradiction registry;
- Bayesian/evidence-calibrated alternative to heuristic propagation;
- sub-neuron reasoning inside each of the eight core families;
- case-level uncertainty decomposition.
