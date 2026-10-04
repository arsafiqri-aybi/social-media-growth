# Canonical Reasoning Engine v2 — Build 01

This runtime is the first executable layer over the accepted R2/R3 knowledge graph.

It does **not** pretend that psychology has already been numerically calibrated.

## Flow

Structured evidence input
→ validate canonical node/context
→ retrieve outgoing typed edges
→ traverse accepted/provisional scientific paths
→ preserve mixed/null evidence
→ apply context as qualifiers, not invented multipliers
→ stop system edges at opportunity/enabling semantics
→ synthesize target hypotheses
→ expose trace, boundaries, contradictions, and causal-language ceiling

## What was deliberately removed from the old engine

The legacy engine remains intact for backward compatibility, but v2 does not reuse:
- hand-authored scientific-looking propagation weights;
- confidence labels converted automatically to numbers;
- core roll-ups that resemble latent psychometric scores without calibration.

## Edge semantics

- **accepted_edge**: traversable canonical relationship. This still does not imply causality.
- **provisional_edge**: traversable only as a bounded hypothesis; it caps the path at provisional.
- **system_edge**: opportunity/enabling mechanic only. It does not auto-activate a psychological state.

For example, sharing can create an *opportunity* for social feedback. The engine does not infer that feedback actually occurred. If social feedback is explicitly observed as an external event, the accepted social-feedback → reward-learning path may then be traversed.

## Feedback

`OperationalFeedbackStore` stores account-specific outcomes separately. It cannot edit node status, edge status, provenance, or scientific claims.

That separation is mandatory: one account performing well must never rewrite the scientific base.

## Current limitation

This is a qualitative inference runtime. Numerical effect magnitude, proxy calibration, and account-specific operational parameters belong to the next Measurement/Calibration block.
