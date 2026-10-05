# Benchmark & Adversarial Suite — Build 01

This suite is designed to make the system fail safely, not merely demonstrate happy paths.

It currently covers 34 deterministic scenarios across:
- measurement leakage;
- latent-state overreach;
- construct-dimension leakage;
- missingness;
- invalid metric domains;
- correlation→causation errors;
- provisional/hypothesis escalation;
- mixed/contradictory evidence;
- context omission;
- system-edge hallucination;
- provenance loss;
- lifecycle violations;
- raw-metric bypass attempts;
- calibration overclaim;
- feedback contamination;
- determinism;
- scientific/runtime weight separation;
- graph lifecycle integrity.

A benchmark passes only when the system either reaches the bounded expected conclusion **or refuses/qualifies the inference in the expected way**.

Passing these scenarios does not by itself imply real-world predictive validity. It verifies reasoning and safety semantics of the current architecture.
