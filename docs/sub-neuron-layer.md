# Sub-Neuron Layer v0.2

The eight core neurons are broad functional families. v0.2 adds **29 sub-neurons** so the engine can reason about mechanisms rather than only broad labels.

Examples:

- `attention.learned_value`
- `curiosity.information_gain`
- `emotion.arousal`
- `identity.norm_salience`
- `trust.trustworthiness`
- `connection.parasocial_closeness`
- `transmission.identity_signaling`
- `habit.context_association`

## Runtime

1. Observations map to candidate sub-neuron seeds.
2. Sub-neuron edges propagate local mechanism interactions.
3. Sub-neuron activation is conservatively rolled up into the eight core families.
4. Core network propagation captures broader cross-family feedback.
5. Evidence/contradiction warnings are attached to active paths.

## Roll-up warning

Core roll-up is currently a transparent architecture heuristic: the strongest child signal dominates, broader activation adds a small breadth bonus, and negative evidence can reduce the roll-up.

This is not a fitted latent-variable model and should not be interpreted as psychometric scoring.
