# Effect-Size and Evidence Calibration Policy

## Why effect sizes are not direct graph weights

A meta-analytic correlation such as `r = 0.60` is not automatically a causal coefficient and cannot safely be copied into a propagation edge.

Reasons include:

- correlation versus causation;
- different constructs and operationalizations;
- different outcomes;
- heterogeneity across populations/platforms/products;
- publication bias and small-study effects;
- overlapping predictors;
- moderators and mediators;
- measurement error.

The engine therefore stores empirical effect sizes as **evidence metadata**, while propagation weights remain explicit architecture coefficients.

## When empirical values may influence runtime

An empirical statistic may affect runtime only when:

1. construct definitions match the graph nodes;
2. direction and causal status are appropriate;
3. outcome matches the target node;
4. context is sufficiently comparable;
5. heterogeneity and bias are documented;
6. conversion/calibration rule is specified and tested.

Until then, empirical effect sizes inform confidence, warnings, boundary conditions, and future research prioritization. They do not masquerade as causal probabilities.

## Current example

The influencer meta-analysis in `EV-TRUST-001` reports substantial positive correlations between trustworthiness and several outcomes, but also very high heterogeneity for some attitude relationships and publication-bias signals for some engagement relationships.

Therefore the evidence supports trust as an important mechanism, but the engine does **not** set a universal `trust -> engagement` weight equal to the pooled correlation.
