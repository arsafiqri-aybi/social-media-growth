# Core Edge Map v0.1

This file is the initial network map. It is deliberately conservative.

## Edge confidence

| Source | Target | Relation | Mechanism | Confidence |
|---|---|---|---|---|
| Valuation | Attention | biases | learned reward/value changes selection priority | Strongly supported |
| Reinforcement | Attention | biases | reward history creates learned attentional priority | Strongly supported |
| Curiosity | Attention | directs | information seeking prioritizes informative sampling | Strongly supported |
| Curiosity | Valuation | interacts | information has subjective value | Strongly supported |
| Valuation | Curiosity | interacts | expected value/information gain shapes seeking | Strongly supported |
| Emotion | Social Transmission | increases probability | arousal/action activation can increase sharing | Strongly supported, bounded |
| Identity | Social Transmission | moderates/drives | group relevance and norms alter expression/influence | Strongly supported at general level |
| Identity | Connection | supports | homophily/congruence can increase affinity | Moderately supported |
| Identity | Trust | supports | similarity/homophily can influence trust/evaluation | Moderately supported |
| Identity | Valuation | biases | self/group relevance changes subjective importance | Moderately supported |
| Connection | Trust | supports | relational engagement can increase receptivity/trust | Moderately supported |
| Trust | Connection | supports | reliable source evaluation can facilitate attachment | Moderately supported |
| Trust | Valuation / response | biases | credibility changes message evaluation | Strongly supported |
| Connection | Reinforcement / return | may support | relational value motivates repeated engagement | Emerging |
| Curiosity | Reinforcement / return | may support | rewarding information-seeking encourages future exploration | Emerging |
| Trust | Social Transmission | may support | confidence may raise willingness to recommend | Emerging |
| Connection | Social Transmission | may support | affiliation/loyalty may encourage advocacy | Emerging |
| Identity | Attention | may bias | self-relevance may prioritize processing | Emerging in current repo |
| Social Transmission | Attention (new person) | enables | exposure places content into another person's attention environment | System-level fact |

## Key feedback loops

### Loop A — Learned Value / Attention Loop

```
Reward / useful outcome
        ↓
Reinforcement & learned value
        ↓
Attention bias toward associated cue
        ↓
More exposure / interaction opportunities
        ↓
New outcome updates value
        ↺
```

**Status:** underlying links strongly supported; full social-media loop strength is context-dependent.

### Loop B — Identity / Connection / Trust Loop

```
Perceived similarity / shared identity
      ↓                 ↘
Connection  ↔  Trust
      ↓          ↓
Repeated relational engagement
      ↺
```

**Status:** multiple components supported, but the complete bidirectional loop should be treated as a model, not a universal causal law.

### Loop C — Curiosity / Information Value Loop

```
Uncertainty / novelty / knowledge gap
        ↓
Curiosity
        ↓
Attention + information seeking
        ↓
Information obtained
        ↓
Value / learning update
        ↺ future exploration
```

**Status:** mechanism strongly grounded in curiosity/information-seeking research; exact social-media dynamics remain context-dependent.

### Loop D — Emotion / Transmission / Social Feedback Loop

```
Emotion / arousal
       ↓
Social transmission
       ↓
Audience response / social feedback
       ↓
Learned value + identity/norm signals
       ↺
```

**Status:** emotion -> transmission is strongly supported in bounded contexts. The return path through social feedback is a system hypothesis requiring direct testing.

## Important rule

An arrow is not automatically causal.

Each future edge record should eventually include:
- causal status;
- effect size where meaningful;
- population;
- context;
- mediator/moderator;
- evidence quality;
- contradicting evidence;
- last reviewed date.
