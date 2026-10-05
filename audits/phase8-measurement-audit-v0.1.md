# Phase 8 — Global Measurement Integration v0.1

Status: **IMPLEMENTED — CI VERIFICATION PENDING AT COMMIT TIME**

## Added

- machine-readable observation schema;
- machine-readable proxy schema;
- experiment metadata/identifiability schema;
- executable global measurement classifier;
- unit tests for anti-inference and experiment-identifiability rules.

## Architectural separation

The existing HPC measurement v2 remains canonical for HPC construct-specific mappings.

The new global layer handles:
- account/platform observations;
- operational performance stages;
- cross-core proxy ambiguity;
- experiment design identifiability.

It does not estimate latent psychological magnitudes.

## Core invariants encoded

- impression cannot seed Attention;
- completion cannot identify Satisfaction;
- follow cannot identify Loyalty/Trust;
- return cannot identify Habit;
- proxy mappings always preserve alternative explanations;
- validated construct measurement requires instrument + target + domain + population metadata;
- platform-optimized delivery blocks a clean causal claim by default;
- a controlled, documented randomized design may pass a **design gate**, but that still does not guarantee substantive validity.

## Phase 8 gate

The implementation is sufficient for Phase 9 only after CI passes.

Required verification:
`python -m unittest discover -s tests -v`

The push workflow already executes the full suite automatically.
