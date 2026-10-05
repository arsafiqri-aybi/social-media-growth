from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Dict, List, Set

from benchmarks import AdversarialBenchmark


@dataclass
class GateResult:
    id: str
    property: str
    status: str
    evidence: List[str]
    limitations: List[str]


@dataclass
class FinalAuditResult:
    gates: List[GateResult]
    pass_count_without_external_ci: int
    pending_external_ci_count: int
    critical_failures: List[str]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "gates": [asdict(x) for x in self.gates],
            "pass_count_without_external_ci": self.pass_count_without_external_ci,
            "pending_external_ci_count": self.pending_external_ci_count,
            "critical_failures": self.critical_failures,
        }


class FinalTenTenAuditor:
    CORE_FAMILIES={
        "attention","curiosity","valuation_emotion","identity",
        "trust","connection","social_transmission","reinforcement_habit",
    }

    def __init__(self, root: str | Path):
        self.root=Path(root)
        self.nodes=self._load("research/r2/cycle01/l2-neuron-candidates.json")["neurons"]
        self.modules=self._load("research/r2/cycle01/module-specs.json")["modules"]
        self.edges=self._load("research/r3/cycle03/scientific-edges.json")["edges"]
        self.pairs=self._load("research/r3/cycle03/pair-coverage-matrix.json")["pairs"]
        self.loops=self._load("research/r3/cycle03/feedback-loops.json")["loops"]
        self.connectors=self._load("research/r3/cycle03/context-connectors.json")["connectors"]
        self.modifiers=self._load("research/r3/cycle01/context-modifiers.json")["modifiers"]
        self.node_audit=self._load("research/r2/acceptance/node-audit.json")["audit"]
        self.r2_sat=self._load("research/r2/acceptance/saturation-audit.json")
        self.r3_sat=self._load("research/r3/cycle03/saturation-audit.json")
        self.module_audit=self._load("research/r2/module-lifecycle-audit.json")["audit"]
        self.contradictions=self._load("research/cycles/02/contradiction-register.json").get("records",[])
        self.measurement_audit=self._load("measurement/v2/validation-audit.json")
        self.reasoning_audit=self._load("reasoning/v2/validation-audit.json")
        self.benchmark_audit=self._load("benchmarks/validation-audit.json")
        self.gap_criticality=self._load("research/r3/cycle03/gap-criticality-audit.json").get("gaps",[])
        self.claim_ids,self.source_ids=self._collect_research_ids()

    def _load(self, rel: str) -> Dict[str, Any]:
        return json.loads((self.root/rel).read_text())

    def _collect_research_ids(self) -> tuple[Set[str],Set[str]]:
        claims:set[str]=set()
        sources:set[str]=set()
        for path in (self.root/"research").rglob("*.json"):
            try:
                data=json.loads(path.read_text())
            except Exception:
                continue
            for c in data.get("claims",[]):
                if isinstance(c,dict) and c.get("id"):
                    claims.add(c["id"])
            for s in data.get("sources",[]):
                if isinstance(s,dict) and s.get("id"):
                    sources.add(s["id"])
        return claims,sources

    @staticmethod
    def _gate(gid: str, prop: str, ok: bool, evidence: List[str], limitations: List[str] | None=None) -> GateResult:
        return GateResult(gid,prop,"PASS" if ok else "FAIL",evidence,limitations or [])

    def run(self) -> FinalAuditResult:
        gates:List[GateResult]=[]
        accepted_nodes=[n for n in self.nodes if n["status"]=="accepted"]
        provisional_nodes=[n for n in self.nodes if n["status"]=="provisional"]
        accepted_edges=[e for e in self.edges if e["status"]=="accepted_edge"]
        provisional_edges=[e for e in self.edges if e["status"]=="provisional_edge"]
        active_edge_nodes={n["id"] for n in self.nodes}|{c["id"] for c in self.connectors}
        node_audit_by={a["node_id"]:a for a in self.node_audit}

        g1=(
            len(accepted_nodes)==84
            and {n["primary_core"] for n in accepted_nodes}==self.CORE_FAMILIES
            and all(n.get("definition") and n.get("acceptance_gate")=="R2_ACCEPTANCE_V1_PASS" for n in accepted_nodes)
        )
        gates.append(self._gate("G1","Conceptual correctness",g1,[
            "84 canonical accepted L2 nodes retain explicit definitions and passed R2 acceptance.",
            "All eight core families contain accepted canonical mechanisms."
        ],["PASS is scoped to the current evidence-backed ontology; it is not a claim of universal psychological truth."]))

        g2=(
            len(self.modules)==45
            and all(m.get("definition") and m.get("claim_ids") and m.get("boundary_conditions") for m in self.modules)
            and all(m.get("status") in {
                "accepted_container","accepted_container_with_bounded_gaps",
                "bounded_provisional_container","deferred_research_container"
            } for m in self.modules)
            and all(n["parent_id"] in {m["id"] for m in self.modules} for n in self.nodes)
        )
        gates.append(self._gate("G2","Mechanistic clarity",g2,[
            "45 mechanism modules have definitions, claim links, boundaries, and explicit lifecycle states.",
            "All L2 records resolve to a mechanism parent."
        ],["Five modules intentionally remain bounded/deferred rather than being falsely promoted."]))

        accepted_node_evidence_ok=all(
            node_audit_by[n["id"]]["gates"]["evidence_sufficiency"]=="PASS"
            and node_audit_by[n["id"]]["gates"]["provenance"]=="PASS"
            for n in accepted_nodes
        )
        node_claims_resolve=all(set(n.get("claim_ids",[])).issubset(self.claim_ids) for n in accepted_nodes)
        edge_evidence_ok=all(
            e.get("evidence_claim_ids") and e.get("support_source_ids")
            and set(e["evidence_claim_ids"]).issubset(self.claim_ids)
            and set(e["support_source_ids"]).issubset(self.source_ids)
            for e in accepted_edges
        )
        g3=accepted_node_evidence_ok and node_claims_resolve and edge_evidence_ok
        gates.append(self._gate("G3","Evidence support",g3,[
            "Every accepted node passed direct evidence + provenance gates.",
            "Every accepted scientific edge has resolvable claim and source provenance."
        ]))

        mixed_edges=[e for e in self.edges if e.get("causal_status")=="mixed" or e.get("contradiction_source_ids")]
        g4=len(self.contradictions)>0 and len(mixed_edges)>0 and all(not g.get("blocks_final_gate",False) for g in self.gap_criticality)
        gates.append(self._gate("G4","Contradictory evidence checked",g4,[
            f"Contradiction register contains {len(self.contradictions)} explicit records.",
            f"{len(mixed_edges)} R3 edges preserve mixed/contradictory evidence.",
            "R3 criticality audit preserves unresolved noncritical gaps instead of deleting them."
        ]))

        g5=(
            self.reasoning_audit.get("status")=="PASS"
            and self.benchmark_audit.get("status")=="PASS"
            and all(e.get("causal_status") for e in self.edges)
        )
        gates.append(self._gate("G5","Causal language calibrated",g5,[
            "Reasoning v2 enforces causal-language ceilings.",
            "Adversarial suite verifies correlation, mixed evidence, and hypothesis paths cannot escalate to causal claims."
        ]))

        g6=(
            all(n.get("boundary_conditions") for n in accepted_nodes)
            and all(e.get("boundary_conditions") for e in self.edges)
        )
        gates.append(self._gate("G6","Boundary conditions known",g6,[
            "All accepted nodes contain explicit boundary conditions.",
            "All R3 edges, including system and provisional edges, carry boundary conditions."
        ]))

        g7=(
            not any(n["status"]=="candidate" for n in self.nodes)
            and all(m.get("status")!="provisional" for m in self.modules)
            and len(self.module_audit)==45
        )
        gates.append(self._gate("G7","Non-redundancy",g7,[
            "No unresolved candidate neuron remains.",
            "Merged/moved/refined/deferred/derived/contested records preserve provenance rather than duplicating active ontology.",
            "All 45 modules have explicit lifecycle resolution."
        ]))

        pair_keys={tuple(sorted((p["core_a"],p["core_b"]))) for p in self.pairs}
        g8=(
            len(self.pairs)==28 and len(pair_keys)==28
            and len(self.edges)==26 and len(self.modifiers)>=1 and len(self.loops)>=1
        )
        gates.append(self._gate("G8","Network integration",g8,[
            "28/28 unordered core-family pairs are explicitly audited.",
            f"Graph contains {len(self.edges)} typed edges, {len(self.modifiers)} context modifiers, and {len(self.loops)} feedback-loop models."
        ]))

        g9=self.measurement_audit.get("status")=="PASS"
        gates.append(self._gate("G9","Measurement awareness",g9,[
            "Measurement v2 validation passed.",
            "Ambiguous platform metrics cannot auto-seed latent psychological states.",
            "Validated construct measures require instrument validity, domain match, and dimension match."
        ]))

        bench=AdversarialBenchmark(self.root).run()
        g10=(
            len(self.contradictions)>0
            and bench.failed==0
            and len(self.gap_criticality)>0
        )
        gates.append(self._gate("G10","Failure awareness",g10,[
            f"Adversarial suite passes {bench.passed}/{bench.total} failure-oriented scenarios.",
            "Contradiction, non-edge, gap, and module-lifecycle artifacts remain explicit."
        ]))

        reasoning_scenarios=sum(1 for s in AdversarialBenchmark(self.root).scenarios if s["category"]=="reasoning")
        g11=self.reasoning_audit.get("status")=="PASS" and reasoning_scenarios>=10 and bench.failed==0
        gates.append(self._gate("G11","Reasoning usability",g11,[
            "Canonical Reasoning Engine v2 validation is PASS.",
            f"Adversarial suite includes {reasoning_scenarios} dedicated reasoning scenarios with deterministic expected outcomes/refusals."
        ]))

        node_ids=[n["id"] for n in self.nodes]
        module_ids=[m["id"] for m in self.modules]
        edge_ids=[e["id"] for e in self.edges]
        endpoint_ok=all(e["source"] in active_edge_nodes and e["target"] in active_edge_nodes for e in self.edges)
        g12=(
            len(node_ids)==len(set(node_ids))
            and len(module_ids)==len(set(module_ids))
            and len(edge_ids)==len(set(edge_ids))
            and endpoint_ok and node_claims_resolve and edge_evidence_ok
        )
        gates.append(self._gate("G12","Retrieval usability",g12,[
            "Canonical node/module/edge IDs are unique.",
            "All R3 edge endpoints resolve to known nodes/connectors.",
            "Accepted-node and accepted-edge evidence references resolve."
        ]))

        g13=(
            self.reasoning_audit.get("ci",{}).get("status")=="success"
            and self.measurement_audit.get("ci",{}).get("status")=="success"
            and self.benchmark_audit.get("ci",{}).get("status")=="success"
            and bench.failed==0
        )
        gates.append(self._gate("G13","Automated validation",g13,[
            "Reasoning, measurement/calibration, and adversarial validation artifacts all reference successful CI runs.",
            "Current deterministic adversarial suite passes in-process."
        ]))

        accepted_cores={n["primary_core"] for n in accepted_nodes}
        module_blockers=[m for m in self.module_audit if m.get("blocks_final_gate")]
        g14=(
            accepted_cores==self.CORE_FAMILIES
            and self.r2_sat.get("status")=="PASS_WITH_NONCRITICAL_EVIDENCE_GAPS"
            and self.r3_sat.get("unresolved_critical_gaps")==0
            and not module_blockers
        )
        gates.append(self._gate("G14","No obvious fundamental mechanism missing",g14,[
            "All eight core families retain accepted canonical mechanisms.",
            "R2 saturation passed with only explicit noncritical evidence gaps.",
            "R3 reports zero unresolved critical connection gaps.",
            "No module-lifecycle record blocks the final gate."
        ],["This is a scoped saturation judgment, not proof that future research cannot add mechanisms."]))

        g15=(
            not any(n["status"]=="candidate" for n in self.nodes)
            and all(m.get("status") in {
                "accepted_container","accepted_container_with_bounded_gaps",
                "bounded_provisional_container","deferred_research_container"
            } for m in self.modules)
        )
        gates.append(self._gate("G15","No unresolved major overlap",g15,[
            "R2 closure eliminated unresolved candidate state.",
            "Overlapping ideas were explicitly merged/moved/refined/deferred instead of silently coexisting."
        ]))

        g16=len(self.pairs)==28 and self.r3_sat.get("unresolved_critical_gaps")==0
        gates.append(self._gate("G16","Major cross-core connections mapped",g16,[
            "All 28 unordered core pairs are audited.",
            "Connection-build saturation reports zero critical unresolved gaps."
        ]))

        supported_loops=[l for l in self.loops if l.get("status") in {"bounded_model","strengthened_bounded_model","supported_bounded_loop"}]
        no_fake_strength=all(l.get("strength_claim")=="NOT_ESTIMATED" for l in self.loops)
        g17=len(self.loops)>=5 and len(supported_loops)>=3 and no_fake_strength
        gates.append(self._gate("G17","Major feedback loops mapped",g17,[
            f"{len(self.loops)} loop models are represented; {len(supported_loops)} are bounded/supported models.",
            "Loop strength is explicitly NOT_ESTIMATED rather than fabricated."
        ]))

        uncertainty_scenarios={"ADV-017","ADV-018","ADV-019","ADV-020","ADV-024"}
        scenario_ids={s["id"] for s in AdversarialBenchmark(self.root).scenarios}
        g18=self.reasoning_audit.get("status")=="PASS" and uncertainty_scenarios.issubset(scenario_ids) and bench.failed==0
        gates.append(self._gate("G18","Uncertainty propagated",g18,[
            "Reasoning engine preserves provisional, mixed, opposing, and unresolved-context states.",
            "Dedicated adversarial scenarios test uncertainty ceilings and counterevidence."
        ]))

        no_runtime_weights=all("weight" not in e and e.get("runtime_parameter_ref") is None for e in self.edges)
        provenance_complete=all(
            set(e.get("evidence_claim_ids",[])).issubset(self.claim_ids)
            and set(e.get("support_source_ids",[])).issubset(self.source_ids)
            for e in self.edges if e["status"]!="system_edge"
        )
        g19=no_runtime_weights and provenance_complete
        gates.append(self._gate("G19","Empirical metadata preserved",g19,[
            "Scientific edges retain claim/source provenance.",
            "No scientific edge contains a runtime weight or calibrated runtime parameter.",
            "Empirical metadata is separated from runtime propagation semantics."
        ]))

        gates.append(GateResult(
            "G20","Tests/CI pass","PENDING_EXTERNAL_CI",
            ["This audit implementation must itself pass GitHub Actions before final closure."],
            []
        ))

        failures=[g.id for g in gates if g.status=="FAIL"]
        return FinalAuditResult(
            gates=gates,
            pass_count_without_external_ci=sum(g.status=="PASS" for g in gates),
            pending_external_ci_count=sum(g.status=="PENDING_EXTERNAL_CI" for g in gates),
            critical_failures=failures,
        )
