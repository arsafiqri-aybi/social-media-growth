from __future__ import annotations

import copy
import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional

from engine.canonical import CanonicalReasoner, CanonicalReasoningCase
from measurement.global_measurement import GlobalMeasurementSystem


@dataclass
class GlobalReasoningResult:
    matched_rules: List[str]
    bottleneck_candidates: List[Dict[str, Any]]
    competing_explanations: List[str]
    warnings: List[str]
    forbidden_inferences: List[str]
    next_tests: List[str]
    measurement_trace: Dict[str, Any]
    experiment_assessment: Optional[Dict[str, Any]]
    hpc_reasoning: Optional[Dict[str, Any]]
    causal_ceiling: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class GlobalGrowthReasoner:
    """Conservative account-level diagnostic runtime.

    The runtime matches calibrated qualitative metric states to auditable
    hypothesis rules. It never converts raw platform metrics directly into
    latent psychology. Optional HPC reasoning is delegated to the accepted
    canonical HPC reasoner.
    """

    def __init__(
        self,
        measurement_system: GlobalMeasurementSystem,
        rules: Dict[str, Any],
        runtime_schema: Dict[str, Any],
        hpc_reasoner: CanonicalReasoner,
    ):
        self.measurement_system = measurement_system
        self.rules = sorted(rules["rules"], key=lambda x: x["id"])
        self.runtime_schema = runtime_schema
        self.hpc_reasoner = hpc_reasoner
        self.allowed_metric_keys = set(
            runtime_schema["input"]["metric_states"]["allowed_keys"]
        )
        self.allowed_states = set(
            runtime_schema["input"]["metric_states"]["allowed_states"]
        )

    @classmethod
    def from_repo_root(cls, root: str | Path) -> "GlobalGrowthReasoner":
        root = Path(root)
        measurement_system = GlobalMeasurementSystem.from_repo_root(root)
        rules = json.loads(
            (root / "reasoning/global_rules_v0.1.json").read_text()
        )
        runtime_schema = json.loads(
            (root / "reasoning/global_runtime_schema.json").read_text()
        )
        hpc_reasoner = CanonicalReasoner.from_repo_root(root)
        return cls(measurement_system, rules, runtime_schema, hpc_reasoner)

    def _validate_case(self, case: Dict[str, Any]) -> None:
        if not isinstance(case.get("goal"), dict) or not case["goal"].get("objective"):
            raise ValueError("case.goal.objective is required")
        metric_states = case.get("metric_states")
        if not isinstance(metric_states, dict):
            raise ValueError("case.metric_states must be an object")
        for key, value in metric_states.items():
            if key not in self.allowed_metric_keys:
                raise ValueError(f"Unsupported metric-state key: {key}")
            if value not in self.allowed_states:
                raise ValueError(
                    f"Unsupported state '{value}' for {key}; "
                    f"allowed={sorted(self.allowed_states)}"
                )

    @staticmethod
    def _condition_matches(
        metric_states: Dict[str, str],
        conditions: Dict[str, Any],
    ) -> bool:
        for key, expected in conditions.items():
            actual = metric_states.get(key, "unknown")
            if isinstance(expected, list):
                if actual not in expected:
                    return False
            elif actual != expected:
                return False
        return True

    @staticmethod
    def _dedupe_dicts(items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        seen = set()
        output = []
        for item in items:
            key = json.dumps(item, sort_keys=True)
            if key not in seen:
                seen.add(key)
                output.append(copy.deepcopy(item))
        return output

    @staticmethod
    def _dedupe_strings(items: List[str]) -> List[str]:
        return sorted(set(items))

    def _measurement_trace(self, case: Dict[str, Any]) -> Dict[str, Any]:
        observations = []
        for item in case.get("observations", []):
            observations.append(
                self.measurement_system.assess_observation(item).to_dict()
            )

        proxies = []
        for proxy_id in case.get("proxies", []):
            proxies.append(
                self.measurement_system.assess_proxy(proxy_id).to_dict()
            )

        return {
            "observations": observations,
            "proxies": proxies,
            "rule": (
                "Raw observations/proxies remain measurement evidence and "
                "do not automatically identify latent psychological states."
            ),
        }

    def _reason_hpc(self, case: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        hpc_case = case.get("hpc_case")
        if hpc_case is None:
            return None
        if not isinstance(hpc_case, dict):
            raise ValueError("hpc_case must be an object when supplied")

        reasoning_case = CanonicalReasoningCase(
            seeds=copy.deepcopy(hpc_case.get("seeds", {})),
            context=copy.deepcopy(hpc_case.get("context", {})),
            targets=list(hpc_case.get("targets", [])),
            max_depth=int(hpc_case.get("max_depth", 3)),
            case_id=hpc_case.get("case_id"),
        )
        return self.hpc_reasoner.reason(reasoning_case).to_dict()

    def reason(self, case: Dict[str, Any]) -> GlobalReasoningResult:
        self._validate_case(case)
        metric_states = dict(case["metric_states"])

        matched_rules: List[str] = []
        bottlenecks: List[Dict[str, Any]] = []
        competing: List[str] = []
        warnings: List[str] = []
        forbidden: List[str] = []
        next_tests: List[str] = []

        for rule in self.rules:
            if self._condition_matches(metric_states, rule["when"]):
                matched_rules.append(rule["id"])
                bottlenecks.extend(rule.get("bottlenecks", []))
                competing.extend(rule.get("competing_explanations", []))
                warnings.extend(rule.get("warnings", []))
                forbidden.extend(rule.get("forbidden_inferences", []))
                next_tests.extend(rule.get("next_tests", []))

        measurement_trace = self._measurement_trace(case)
        for obs in measurement_trace["observations"]:
            warnings.extend(obs.get("warnings", []))
        for proxy in measurement_trace["proxies"]:
            if proxy.get("warning"):
                warnings.append(proxy["warning"])

        experiment_assessment = None
        if case.get("experiment") is not None:
            experiment_assessment = self.measurement_system.assess_experiment(
                case["experiment"]
            ).to_dict()
            warnings.extend(experiment_assessment.get("warnings", []))

        hpc_reasoning = self._reason_hpc(case)

        if experiment_assessment is None:
            causal_ceiling = "observational_diagnosis_only"
        elif experiment_assessment["bounded_causal_claim_allowed"]:
            causal_ceiling = "bounded_design_support_possible"
        else:
            causal_ceiling = "confounded_or_noncausal_design"

        if hpc_reasoning is None:
            warnings.append(
                "No canonical HPC case was supplied; psychological mechanisms "
                "remain hypotheses rather than graph-derived HPC conclusions."
            )

        return GlobalReasoningResult(
            matched_rules=sorted(matched_rules),
            bottleneck_candidates=self._dedupe_dicts(bottlenecks),
            competing_explanations=self._dedupe_strings(competing),
            warnings=self._dedupe_strings(warnings),
            forbidden_inferences=self._dedupe_strings(forbidden),
            next_tests=self._dedupe_strings(next_tests),
            measurement_trace=measurement_trace,
            experiment_assessment=experiment_assessment,
            hpc_reasoning=hpc_reasoning,
            causal_ceiling=causal_ceiling,
        )
