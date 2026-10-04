# Measurement Layer v0.2

## Purpose

Convert observable account/platform signals into **candidate sub-neuron evidence** without pretending that analytics are direct psychological measurements.

## Core rule

A metric is not a mind-state.

Examples:

- watch/completion behavior is not pure attention;
- returning-viewer rate is not proof of habit;
- engagement is not proof of trust;
- share count directly observes transmission behavior, but not the motive for sharing.

## Proxy mapping

`measurement/proxies.json` stores the observable proxy, target subnodes, conservative mapping weights, confidence label, ambiguity warning, and sensitivity for baseline-relative normalization.

The mapper accepts:

- `normalized_delta` in `[0,1]`;
- `normalized` in `[0,1]`;
- or `value + baseline`, converted to a bounded baseline-relative signal.

Below-baseline signals are kept as **negative evidence** rather than silently discarded.

## Scientific status

These mappings are operational priors, not validated psychometric scales.

Future versions should validate mappings against survey/experimental measures, estimate platform-specific measurement error, model missingness/selection bias, and separate creator-level, content-level, and audience-level observations.
