from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Dict, List

from engine.canonical import (
    CanonicalReasoner,
    CanonicalReasoningCase,
    OperationalFeedbackStore,
)
from measurement import CanonicalMeasurementMapper, OperationalCalibrationStore


@dataclass
class ScenarioResult:
    id: str
    category: str
    passed: bool
    message: str


@dataclass
class BenchmarkReport:
    total: int
    passed: int
    failed: int
    results: List[ScenarioResult]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "total": self.total,
            "passed": self.passed,
            "failed": self.failed,
            "results": [asdict(x) for x in self.results],
        }


class AdversarialBenchmark:
    def __init__(self, root: str | Path, scenarios_path: str | Path | None = None):
        self.root=Path(root)
        self.reasoner=CanonicalReasoner.from_repo_root(self.root)
        self.mapper=CanonicalMeasurementMapper.from_repo_root(self.root)
        self.scenarios_path=Path(scenarios_path or self.root/"benchmarks/adversarial_scenarios.json")
        self.scenarios=json.loads(self.scenarios_path.read_text())["scenarios"]

    @staticmethod
    def _assert(condition: bool, message: str) -> None:
        if not condition:
            raise AssertionError(message)

    def _measurement(self, s: Dict[str, Any]) -> None:
        out=self.mapper.map(s["observations"])
        exp=s.get("expect",{})
        seed_ids=set(out.reasoning_seeds)
        self._assert(set(exp.get("seed_ids",[])).issubset(seed_ids),f"missing seeds: {set(exp.get('seed_ids',[]))-seed_ids}")
        self._assert(not (set(exp.get("forbid_seed_ids",[])) & seed_ids),f"forbidden seeds present: {set(exp.get('forbid_seed_ids',[])) & seed_ids}")
        candidate_ids={x["candidate_node_id"] for x in out.candidate_explanations}
        self._assert(set(exp.get("candidate_ids",[])).issubset(candidate_ids),"missing candidate explanations")
        for _, pair in exp.get("basis",{}).items():
            node_id,basis=pair
            self._assert(out.reasoning_seeds[node_id]["basis"]==basis,f"wrong basis for {node_id}")
        if "observed_direction" in exp:
            self._assert(any(e.observed_direction==exp["observed_direction"] for e in out.evidence),"expected observed direction missing")

    def _reasoning(self, s: Dict[str, Any]) -> None:
        c=s["case"]
        out=self.reasoner.reason(CanonicalReasoningCase(
            seeds=c["seeds"],
            context=c.get("context",{}),
            targets=c.get("targets",[]),
            max_depth=c.get("max_depth",3),
        ))
        exp=s.get("expect",{})
        target=exp.get("target")
        if target:
            conclusion=out.conclusions[target]
            for key,attr in [
                ("status","status"),
                ("causal_ceiling","causal_ceiling"),
                ("effect_direction","effect_direction"),
                ("strong_causal","strong_causal_claim_allowed"),
            ]:
                if key in exp:
                    self._assert(getattr(conclusion,attr)==exp[key],f"{key}: got {getattr(conclusion,attr)} expected {exp[key]}")
            if "path" in exp:
                self._assert(conclusion.selected_path_edge_ids==exp["path"],f"wrong path {conclusion.selected_path_edge_ids}")
        if "opportunity_edge" in exp:
            self._assert(any(x.edge_id==exp["opportunity_edge"] for x in out.opportunities),"opportunity edge missing")
        if "contradiction_source" in exp:
            self._assert(any(exp["contradiction_source"] in h.contradiction_source_ids for h in out.hypotheses if h.target==target),"contradiction provenance missing")
        if "unresolved_modifier" in exp:
            self._assert(any(exp["unresolved_modifier"] in h.unresolved_modifiers for h in out.hypotheses if h.target==target),"unresolved modifier missing")
        if "trace_edge" in exp:
            step=next(x for x in out.trace if x.edge_id==exp["trace_edge"])
            self._assert(exp["claim_id"] in step.evidence_claim_ids,"claim provenance missing")
            self._assert(exp["source_id"] in step.support_source_ids,"source provenance missing")

    def _expected_error(self, s: Dict[str, Any], measurement: bool) -> None:
        try:
            if measurement:
                self.mapper.map(s["observations"])
            else:
                c=s["case"]
                self.reasoner.reason(CanonicalReasoningCase(
                    seeds=c["seeds"],
                    context=c.get("context",{}),
                    targets=c.get("targets",[]),
                    max_depth=c.get("max_depth",3),
                ))
        except ValueError:
            return
        raise AssertionError("expected ValueError was not raised")

    def _calibration(self, s: Dict[str, Any]) -> None:
        store=OperationalCalibrationStore()
        for r in s["records"]:
            store.record(r["case_id"],r["predictors"],r["outcomes"],r.get("context"))
        q=s["query"]
        out=store.summarize(q["predictor_id"],q["outcome_id"],q["min_records"])
        exp=s["expect"]
        self._assert(out.status==exp["status"],f"wrong calibration status {out.status}")
        if exp.get("r_is_none"):
            self._assert(out.pearson_r is None,"pearson_r should be None")
        if "direction" in exp:
            self._assert(out.association_direction==exp["direction"],"wrong association direction")
        if "scientific_effect_claim_allowed" in exp:
            self._assert(out.scientific_effect_claim_allowed==exp["scientific_effect_claim_allowed"],"scientific claim flag wrong")
        if "latent_state_claim_allowed" in exp:
            self._assert(out.latent_state_claim_allowed==exp["latent_state_claim_allowed"],"latent claim flag wrong")

    def _structural(self, s: Dict[str, Any]) -> None:
        check=s["check"]
        if check=="no_runtime_weights":
            edges=json.loads((self.root/"research/r3/cycle03/scientific-edges.json").read_text())["edges"]
            self._assert(all("weight" not in e and e.get("runtime_parameter_ref") is None for e in edges),"runtime/scientific weight leakage")
        elif check=="pair_count":
            pairs=json.loads((self.root/"research/r3/cycle03/pair-coverage-matrix.json").read_text())["pairs"]
            self._assert(len(pairs)==s["expect_value"],"pair count mismatch")
        elif check=="node_lifecycle":
            nodes=json.loads((self.root/"research/r2/cycle01/l2-neuron-candidates.json").read_text())["neurons"]
            counts={}
            for n in nodes: counts[n["status"]]=counts.get(n["status"],0)+1
            for k,v in s["expect_value"].items():
                self._assert(counts.get(k,0)==v,f"node lifecycle {k} mismatch")
        elif check=="edge_lifecycle":
            edges=json.loads((self.root/"research/r3/cycle03/scientific-edges.json").read_text())["edges"]
            counts={}
            for e in edges: counts[e["status"]]=counts.get(e["status"],0)+1
            for k,v in s["expect_value"].items():
                self._assert(counts.get(k,0)==v,f"edge lifecycle {k} mismatch")
        else:
            raise AssertionError(f"unknown structural check {check}")

    def _feedback_isolation(self) -> None:
        before=self.reasoner.scientific_snapshot()
        store=OperationalFeedbackStore()
        store.record("adv-feedback",{"share_rate":{"value":0.05}})
        after=self.reasoner.scientific_snapshot()
        self._assert(before==after,"scientific graph mutated by account-local feedback")

    def _determinism(self, s: Dict[str, Any]) -> None:
        c=s["case"]
        case=CanonicalReasoningCase(
            seeds=c["seeds"],
            context=c.get("context",{}),
            targets=c.get("targets",[]),
            max_depth=c.get("max_depth",3),
        )
        self._assert(self.reasoner.reason(case).to_dict()==self.reasoner.reason(case).to_dict(),"reasoner is nondeterministic")

    def run_one(self, s: Dict[str, Any]) -> ScenarioResult:
        try:
            t=s["type"]
            if t=="measurement": self._measurement(s)
            elif t=="measurement_error": self._expected_error(s,True)
            elif t=="reasoning": self._reasoning(s)
            elif t=="reasoning_error": self._expected_error(s,False)
            elif t=="calibration": self._calibration(s)
            elif t=="structural": self._structural(s)
            elif t=="feedback_isolation": self._feedback_isolation()
            elif t=="determinism": self._determinism(s)
            else: raise AssertionError(f"unknown scenario type {t}")
            return ScenarioResult(s["id"],s["category"],True,"PASS")
        except Exception as exc:
            return ScenarioResult(s["id"],s["category"],False,f"{type(exc).__name__}: {exc}")

    def run(self) -> BenchmarkReport:
        results=[self.run_one(s) for s in self.scenarios]
        passed=sum(x.passed for x in results)
        return BenchmarkReport(len(results),passed,len(results)-passed,results)
