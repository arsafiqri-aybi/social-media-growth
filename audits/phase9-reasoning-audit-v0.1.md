# Phase 9 — Integrated Global Reasoning v0.1

Status: **IMPLEMENTED — CI VERIFICATION PENDING**

## Runtime design

The global runtime connects:

```text
Governance objective + Context
          ↓
calibrated qualitative metric states
          ↓
Global Measurement System
          ↓
auditable pattern rules
          ↓
bottleneck hypotheses + competing explanations
          ↓
causal ceiling + forbidden inferences
          ↓
next-test candidates
          ↕
optional Canonical HPC Reasoner
```

## Why qualitative states

The runtime accepts labels such as `high`, `low`, `up`, `down`, and `flat` but **does not calculate them from universal thresholds**.

Those labels must be supplied by account/context calibration, benchmark comparison, or another explicit measurement process.

This prevents arbitrary rules such as:
- 5% is always high;
- 50% completion is always good;
- a universal engagement-rate threshold indicates trust/value.

## HPC integration boundary

Raw platform metrics do not enter the HPC graph.

Optional `hpc_case` input is sent to the existing `CanonicalReasoner`, which:
- accepts only canonical nodes/connectors;
- rejects raw platform proxy IDs;
- preserves evidence/causal ceilings;
- does not use scientific runtime weights.

Thus the global runtime can use the mature HPC graph without weakening its measurement boundaries.

## Initial diagnostic rules

Ten auditable operational rules cover:
- high exposure + low selection;
- high selection + low continuation;
- high completion + low return;
- reach/likes up + conversion down;
- rising return;
- low exposure;
- non-follower reach up + continuation down;
- shares up with satisfaction unknown;
- follows up + weak return;
- high conversion + low return.

These rules create **hypotheses**, never direct causal conclusions.

## Required CI gate

The new test suite checks:
- distribution is not automatically blamed when exposure is already high;
- completion/return pattern does not become a Habit claim;
- return growth preserves multiple competing explanations;
- platform-optimized experiments cap causal claims;
- optional HPC reasoning uses the canonical HPC runtime;
- raw platform metrics are rejected from HPC;
- deterministic output;
- unsupported metric states are rejected.

Phase 9 becomes complete only after the repository CI passes.
