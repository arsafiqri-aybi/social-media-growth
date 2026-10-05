# Global Measurement Bridge v0.1

Status: **PHASE 8 INPUT — NOT YET FULL MEASUREMENT SYSTEM**

Purpose:
Connect global operational-core observations to the existing HPC measurement discipline without inferring latent states directly.

## Measurement classes

### M0 — Direct system observation
Examples:
- content published;
- recommendation eligibility flag;
- impression;
- follow;
- logged share;
- click;
- watch duration;
- return event.

These are events, not latent psychology.

### M1 — Derived behavioral metric
Examples:
- selection/start rate;
- continuation curve;
- completion rate;
- share rate;
- return rate;
- cohort retention.

Derived behavior still does not uniquely identify a mechanism.

### M2 — Qualified behavioral proxy
A behavioral pattern with explicit competing explanations and a documented construct mapping.

Example:
repeated voluntary return may support a **relationship/recurrence hypothesis**, but not automatically Habit, Trust, Loyalty or PSR.

### M3 — Validated construct measurement
A validated survey/instrument used in an appropriate population/context with documented transport limits.

Only this class may more directly seed a latent construct, subject to existing HPC measurement rules.

## Mandatory decomposition for content performance

When data allow:

```text
eligible?
→ exposed?
→ selected?
→ continued?
→ completed?
→ satisfaction evidence?
→ acted?
→ returned?
```

Never collapse these into one engagement score.

## Core-specific mappings

### Audience & Value
Observations:
audience composition, search language, topic response, questions/comments, surveys, segment outcomes.

Competing explanations:
distribution selection, topic familiarity, creator familiarity, incentive effects, platform context.

### Communication & Content
Observations:
selection, continuation, completion, drop-off, CTA action, direct feedback.

Competing explanations:
audience mismatch, distribution surface, prior source relationship, duration/format, intent.

### Distribution & Discovery
Observations:
eligibility, impressions, reach, source/surface, follower/non-follower mix, search/referral, recommendation.

Competing explanations:
platform exploration, policy state, audience history, content pool competition.

### Relationship & Retention
Observations:
return cohorts, repeat interactions, follow retention, recurring-series participation, advocacy/referral, validated relational survey.

Competing explanations:
platform rediscovery, repeated topical need, incentive, controversy, habit, convenience.

### Learning & Adaptation
Inputs:
all observations + intervention metadata + content metadata + audience composition + platform state.

Outputs:
bounded diagnosis, competing explanations, prediction, intervention, falsification result, account-local belief update.

## Anti-inference rules

- impression ≠ attention
- start/click ≠ curiosity
- completion ≠ satisfaction
- save ≠ subjective utility
- like ≠ trust
- comment ≠ connection
- share ≠ unique transmission motive
- follow ≠ loyalty
- return ≠ habit
- repeated engagement ≠ PSR
- conversion ≠ long-term value

These inequalities do not mean the metric is useless. They mean it is **non-identifying without additional evidence**.

## Identifiability warning

If an intervention changes both:
- creative/message; and
- who receives the content / how the platform delivers it,

then observed outcome differences do not cleanly identify a creative causal effect.

The experiment record must state:
- what was assigned;
- at which unit;
- how delivery was controlled;
- whether targeting/ranking could differ;
- whether audience composition differed;
- what causal claim is therefore allowed.

## Next Phase 8 work

Convert this bridge into:
- machine-readable global proxy schema;
- account observation schema;
- metric validity classifier;
- competing-explanation generator;
- experimental metadata schema.
