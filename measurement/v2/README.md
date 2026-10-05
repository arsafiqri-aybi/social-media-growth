# Measurement & Calibration v2 — Build 01

The legacy mapper is preserved for backward compatibility, but it is no longer the canonical path into Reasoning Engine v2.

## Measurement flow

Raw platform/account observable
→ classify measurement validity
→ preserve direct observation
→ identify competing explanations
→ seed Reasoning Engine only when allowed
→ keep ambiguity and warnings visible

### Important distinction

- **Direct behavior** such as a logged share may seed the canonical share-action node.
- **External event** such as observed social feedback may seed the social-feedback context event.
- **Validated construct measurement** may seed a latent construct only when the instrument and domain match are explicitly documented.
- **Qualified behavioral proxy** may enter only as `proxy_hypothesis`, which Reasoning Engine automatically caps at provisional/hypothesis-only.
- **Ambiguous platform proxy** never auto-seeds a latent state.

Therefore:
- completion rate ≠ attention;
- returning viewers ≠ habit;
- repeated engagement ≠ parasocial relationship;
- engagement ≠ trust;
- saves ≠ subjective utility.

## Calibration flow

Account-local observable history
→ paired predictor/outcome records
→ descriptive predictive association
→ operational profile

Calibration outputs:
- do not change scientific node status;
- do not change scientific edge status;
- do not estimate latent psychology;
- do not establish causality.

A future calibrated runtime coefficient must pass a separate validation gate before the reasoning engine can consume it.
