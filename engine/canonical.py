from __future__ import annotations

import copy
import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple


ALLOWED_SEED_BASES = {
    "direct_measurement",
    "validated_observation",
    "structured_observation",
    "external_event",
    "user_hypothesis",
}
ALLOWED_DIRECTIONS = {"support", "oppose"}


@dataclass(frozen=True)
class SeedSignal:
    node_id: str
    direction: str
    basis: str
    note: Optional[str] = None
    lifecycle_status: Optional[str] = None


@dataclass
class CanonicalReasoningCase:
    seeds: Dict[str, Any]
    context: Dict[str, Any] = field(default_factory=dict)
    targets: List[str] = field(default_factory=list)
    max_depth: int = 3
    case_id: Optional[str] = None


@dataclass(frozen=True)
class TraceStep:
    edge_id: str
    source: str
    target: str
    edge_status: str
    relation: str
    sign: str
    causal_status: str
    mechanism: str
    inference_kind: str
    boundary_conditions: Tuple[str, ...]
    contradiction_source_ids: Tuple[str, ...]
    observed_modifiers: Tuple[str, ...]
    unresolved_modifiers: Tuple[str, ...]


@dataclass
class PathHypothesis:
    source_seed: str
    target: str
    path_nodes: List[str]
    edge_ids: List[str]
    path_status: str
    causal_ceiling: str
    operational_priority: int
    strong_causal_claim_allowed: bool
    boundary_conditions: List[str]
    contradiction_source_ids: List[str]
    observed_modifiers: List[str]
    unresolved_modifiers: List[str]
    reasons: List[str]


@dataclass
class TargetConclusion:
    target: str
    status: str
    causal_ceiling: str
    selected_path_edge_ids: List[str]
    alternative_path_edge_ids: List[List[str]]
    strong_causal_claim_allowed: bool
    explanation: str
    warnings: List[str]


@dataclass
class CanonicalReasoningResult:
    seeds: List[SeedSignal]
    hypotheses: List[PathHypothesis]
    conclusions: Dict[str, TargetConclusion]
    trace: List[TraceStep]
    tensions: List[Dict[str, Any]]
    opportunities: List[TraceStep]
    warnings: List[str]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "seeds": [asdict(x) for x in self.seeds],
            "hypotheses": [asdict(x) for x in self.hypotheses],
            "conclusions": {k: asdict(v) for k, v in self.conclusions.items()},
            "trace": [asdict(x) for x in self.trace],
            "tensions": copy.deepcopy(self.tensions),
            "opportunities": [asdict(x) for x in self.opportunities],
            "warnings": list(self.warnings),
        }


class OperationalFeedbackStore:
    """
    Account/local observations are deliberately isolated from scientific graph data.

    Records stored here may later be used by a calibration layer. They never mutate
    node lifecycle state, scientific edge status, source provenance, or effect claims.
    """

    def __init__(self) -> None:
        self._records: List[Dict[str, Any]] = []

    def record(
        self,
        case_id: str,
        observations: Dict[str, Any],
        notes: Optional[str] = None,
    ) -> Dict[str, Any]:
        if not case_id:
            raise ValueError("case_id is required")
        record = {
            "case_id": str(case_id),
            "observations": copy.deepcopy(observations),
            "notes": notes,
            "scope": "account_local_operational_evidence",
        }
        self._records.append(record)
        return copy.deepcopy(record)

    def snapshot(self) -> List[Dict[str, Any]]:
        return copy.deepcopy(self._records)


class CanonicalReasoner:
    """
    Evidence-aware qualitative graph reasoner over the canonical R2/R3 artifacts.

    It is intentionally NOT a psychometric scoring model and NOT a biological neural
    network. It performs auditable symbolic/network inference while preserving
    lifecycle state, causal-language limits, contradictions, context uncertainty,
    and scientific/runtime separation.

    No scientific edge weight is computed or consumed here.
    """

    ACTIVE_NODE_STATUSES = {"accepted", "provisional"}
    ACTIVE_EDGE_STATUSES = {"accepted_edge", "provisional_edge", "system_edge"}

    def __init__(
        self,
        nodes_path: str | Path,
        edges_path: str | Path,
        connectors_path: str | Path,
        modifiers_path: Optional[str | Path] = None,
    ):
        node_data = json.loads(Path(nodes_path).read_text())
        edge_data = json.loads(Path(edges_path).read_text())
        connector_data = json.loads(Path(connectors_path).read_text())

        self.nodes = {n["id"]: n for n in node_data["neurons"]}
        self.connectors = {c["id"]: c for c in connector_data["connectors"]}
        self.edges = [e for e in edge_data["edges"] if e["status"] in self.ACTIVE_EDGE_STATUSES]
        self.edges_by_source: Dict[str, List[Dict[str, Any]]] = {}
        for edge in self.edges:
            if "weight" in edge:
                raise ValueError(
                    f"Canonical scientific edge {edge['id']} illegally contains runtime weight"
                )
            if edge.get("runtime_parameter_ref") is not None:
                raise ValueError(
                    f"Canonical scientific edge {edge['id']} has a calibrated runtime parameter; "
                    "v2 Build 01 does not consume calibrated coefficients yet"
                )
            self.edges_by_source.setdefault(edge["source"], []).append(edge)

        for source in self.edges_by_source:
            self.edges_by_source[source].sort(key=lambda e: e["id"])

        self.modifiers: List[Dict[str, Any]] = []
        if modifiers_path is not None and Path(modifiers_path).exists():
            data = json.loads(Path(modifiers_path).read_text())
            self.modifiers = list(data.get("modifiers", []))

        self.modifiers_by_edge: Dict[str, List[Dict[str, Any]]] = {}
        for mod in self.modifiers:
            for edge_id in mod.get("target_edge_ids", []):
                self.modifiers_by_edge.setdefault(edge_id, []).append(mod)

        self._validate_graph()

    @classmethod
    def from_repo_root(cls, root: str | Path) -> "CanonicalReasoner":
        root = Path(root)
        return cls(
            root / "research/r2/cycle01/l2-neuron-candidates.json",
            root / "research/r3/cycle03/scientific-edges.json",
            root / "research/r3/cycle03/context-connectors.json",
            root / "research/r3/cycle01/context-modifiers.json",
        )

    def _validate_graph(self) -> None:
        known = set(self.nodes) | set(self.connectors)
        for edge in self.edges:
            for key in ("source", "target"):
                if edge[key] not in known:
                    raise ValueError(f"Unknown {key} {edge[key]} in edge {edge['id']}")
            if edge["status"] == "accepted_edge":
                for endpoint in (edge["source"], edge["target"]):
                    if endpoint in self.nodes and self.nodes[endpoint]["status"] != "accepted":
                        raise ValueError(
                            f"Accepted edge {edge['id']} uses non-accepted node {endpoint}"
                        )

    def scientific_snapshot(self) -> Dict[str, Any]:
        return {
            "nodes": copy.deepcopy(self.nodes),
            "connectors": copy.deepcopy(self.connectors),
            "edges": copy.deepcopy(self.edges),
        }

    def _normalize_seed(self, node_id: str, raw: Any) -> SeedSignal:
        if node_id in self.nodes:
            lifecycle = self.nodes[node_id]["status"]
            if lifecycle not in self.ACTIVE_NODE_STATUSES:
                raise ValueError(
                    f"Seed {node_id} is non-canonical lifecycle state: {lifecycle}"
                )
        elif node_id in self.connectors:
            lifecycle = self.connectors[node_id].get("status", "context")
        else:
            raise ValueError(
                f"Unknown seed '{node_id}'. Raw platform proxies must be mapped by the "
                "measurement layer before entering the canonical reasoner."
            )

        if isinstance(raw, (int, float, bool)):
            raise ValueError(
                f"Numeric/bool seed for {node_id} is not allowed in qualitative v2. "
                "Use an explicit evidence basis instead of an uncalibrated activation."
            )
        if isinstance(raw, str):
            basis = raw
            direction = "support"
            note = None
        elif isinstance(raw, dict):
            basis = raw.get("basis")
            direction = raw.get("direction", "support")
            note = raw.get("note")
        else:
            raise ValueError(f"Invalid seed specification for {node_id}: {type(raw).__name__}")

        if basis not in ALLOWED_SEED_BASES:
            raise ValueError(
                f"Invalid seed basis '{basis}' for {node_id}; allowed={sorted(ALLOWED_SEED_BASES)}"
            )
        if direction not in ALLOWED_DIRECTIONS:
            raise ValueError(
                f"Invalid seed direction '{direction}' for {node_id}; allowed={sorted(ALLOWED_DIRECTIONS)}"
            )
        return SeedSignal(
            node_id=node_id,
            direction=direction,
            basis=basis,
            note=note,
            lifecycle_status=lifecycle,
        )

    def _modifier_state(
        self, edge: Dict[str, Any], context: Dict[str, Any]
    ) -> Tuple[List[str], List[str]]:
        required: List[str] = []
        for m in edge.get("moderators", []):
            if m.get("kind") == "context" and m.get("id"):
                required.append(m["id"])
        for mod in self.modifiers_by_edge.get(edge["id"], []):
            if mod.get("source"):
                required.append(mod["source"])
        required = sorted(set(required))

        observed, unresolved = [], []
        for context_id in required:
            if context_id in context:
                observed.append(context_id)
            else:
                unresolved.append(context_id)
        return observed, unresolved

    def _step(self, edge: Dict[str, Any], context: Dict[str, Any]) -> TraceStep:
        observed, unresolved = self._modifier_state(edge, context)
        inference_kind = (
            "opportunity_only" if edge["status"] == "system_edge"
            else "scientific_inference"
        )
        return TraceStep(
            edge_id=edge["id"],
            source=edge["source"],
            target=edge["target"],
            edge_status=edge["status"],
            relation=edge["relation"],
            sign=edge["sign"],
            causal_status=edge["causal_status"],
            mechanism=edge["mechanism"],
            inference_kind=inference_kind,
            boundary_conditions=tuple(edge.get("boundary_conditions", [])),
            contradiction_source_ids=tuple(edge.get("contradiction_source_ids", [])),
            observed_modifiers=tuple(observed),
            unresolved_modifiers=tuple(unresolved),
        )

    @staticmethod
    def _path_semantics(path_edges: Iterable[Dict[str, Any]], seed: SeedSignal) -> Tuple[str, str, bool, List[str]]:
        edges = list(path_edges)
        reasons: List[str] = []

        if seed.lifecycle_status == "provisional":
            path_status = "provisional_path"
            reasons.append("source seed is a provisional canonical node")
        elif any(e["status"] == "provisional_edge" for e in edges):
            path_status = "provisional_path"
            reasons.append("path contains at least one provisional scientific edge")
        elif any(e.get("contradiction_source_ids") for e in edges) or any(
            e.get("causal_status") == "mixed" for e in edges
        ):
            path_status = "mixed_evidence_path"
            reasons.append("path contains mixed/contradictory evidence")
        else:
            path_status = "accepted_graph_path"
            reasons.append("path uses accepted canonical scientific edges")

        causal_statuses = {e.get("causal_status", "unspecified") for e in edges}
        if path_status == "provisional_path":
            causal_ceiling = "hypothesis_only"
        elif any(x == "mixed" for x in causal_statuses):
            causal_ceiling = "mixed_evidence_only"
        elif any(x in {"correlational", "unknown"} for x in causal_statuses):
            causal_ceiling = "association_only"
        elif causal_statuses and all(
            x in {"experimental_causal", "causal"} for x in causal_statuses
        ):
            causal_ceiling = "causal_bounded"
        else:
            causal_ceiling = "mechanistic_noncausal"

        strong_causal = causal_ceiling == "causal_bounded"
        priority = {
            "accepted_graph_path": 3,
            "mixed_evidence_path": 2,
            "provisional_path": 1,
        }[path_status]
        return path_status, causal_ceiling, strong_causal, reasons + [
            "operational_priority orders retrieval paths only; it is not an effect-size or scientific-strength coefficient"
        ]

    def _make_hypothesis(
        self,
        seed: SeedSignal,
        path_nodes: List[str],
        path_edges: List[Dict[str, Any]],
        context: Dict[str, Any],
    ) -> PathHypothesis:
        status, ceiling, strong_causal, reasons = self._path_semantics(path_edges, seed)
        boundaries: List[str] = []
        contradictions: List[str] = []
        observed: List[str] = []
        unresolved: List[str] = []
        for edge in path_edges:
            boundaries.extend(edge.get("boundary_conditions", []))
            contradictions.extend(edge.get("contradiction_source_ids", []))
            o, u = self._modifier_state(edge, context)
            observed.extend(o)
            unresolved.extend(u)
            if edge.get("uncertainty", {}).get("transport_context") == "material":
                unresolved.append("transport_context_material")

        return PathHypothesis(
            source_seed=seed.node_id,
            target=path_nodes[-1],
            path_nodes=list(path_nodes),
            edge_ids=[e["id"] for e in path_edges],
            path_status=status,
            causal_ceiling=ceiling,
            operational_priority={
                "accepted_graph_path": 3,
                "mixed_evidence_path": 2,
                "provisional_path": 1,
            }[status],
            strong_causal_claim_allowed=strong_causal,
            boundary_conditions=sorted(set(boundaries)),
            contradiction_source_ids=sorted(set(contradictions)),
            observed_modifiers=sorted(set(observed)),
            unresolved_modifiers=sorted(set(unresolved)),
            reasons=reasons,
        )

    @staticmethod
    def _synthesize_target(
        target: str, hypotheses: List[PathHypothesis]
    ) -> TargetConclusion:
        if not hypotheses:
            return TargetConclusion(
                target=target,
                status="unsupported_in_current_graph",
                causal_ceiling="no_claim",
                selected_path_edge_ids=[],
                alternative_path_edge_ids=[],
                strong_causal_claim_allowed=False,
                explanation="No traversable scientific path from the supplied evidence reaches this target.",
                warnings=["Absence of a path is not evidence that no relationship exists."],
            )

        ranked = sorted(
            hypotheses,
            key=lambda h: (-h.operational_priority, len(h.edge_ids), tuple(h.edge_ids)),
        )
        best = ranked[0]
        signs = set()
        warnings = set(best.boundary_conditions)
        for h in ranked:
            warnings.update(h.boundary_conditions)
            warnings.update(f"contradiction evidence: {x}" for x in h.contradiction_source_ids)
            if h.unresolved_modifiers:
                warnings.add(
                    "unresolved context/moderators: " + ", ".join(h.unresolved_modifiers)
                )

        if any(h.contradiction_source_ids for h in ranked):
            status = "contested_or_mixed"
        elif best.path_status == "provisional_path":
            status = "provisional_hypothesis"
        elif best.path_status == "mixed_evidence_path":
            status = "bounded_mixed_support"
        else:
            status = "bounded_support"

        explanation = (
            f"Best available path is {best.path_status} with causal-language ceiling "
            f"'{best.causal_ceiling}'. Path priority is operational retrieval ordering, "
            "not an empirical effect magnitude."
        )
        return TargetConclusion(
            target=target,
            status=status,
            causal_ceiling=best.causal_ceiling,
            selected_path_edge_ids=list(best.edge_ids),
            alternative_path_edge_ids=[list(h.edge_ids) for h in ranked[1:]],
            strong_causal_claim_allowed=best.strong_causal_claim_allowed,
            explanation=explanation,
            warnings=sorted(warnings),
        )

    def reason(self, case: CanonicalReasoningCase) -> CanonicalReasoningResult:
        if case.max_depth < 1 or case.max_depth > 6:
            raise ValueError("max_depth must be between 1 and 6")

        seeds = [self._normalize_seed(k, v) for k, v in sorted(case.seeds.items())]
        seed_ids = {s.node_id for s in seeds}

        unknown_targets = set(case.targets) - (set(self.nodes) | set(self.connectors))
        if unknown_targets:
            raise ValueError(f"Unknown targets: {sorted(unknown_targets)}")

        hypotheses: List[PathHypothesis] = []
        trace_by_key: Dict[Tuple[str, str], TraceStep] = {}
        opportunities: List[TraceStep] = []

        for seed in seeds:
            # Queue: (current node, path nodes, path edges)
            queue: List[Tuple[str, List[str], List[Dict[str, Any]]]] = [
                (seed.node_id, [seed.node_id], [])
            ]
            while queue:
                current, path_nodes, path_edges = queue.pop(0)
                if len(path_edges) >= case.max_depth:
                    continue

                for edge in self.edges_by_source.get(current, []):
                    step = self._step(edge, case.context)
                    trace_by_key[(seed.node_id, edge["id"])] = step

                    if edge["status"] == "system_edge":
                        opportunities.append(step)
                        # System edges describe an opportunity/enabling condition, not
                        # occurrence of the target state. Do not automatically cascade.
                        continue

                    target = edge["target"]
                    if target in path_nodes:
                        continue
                    new_nodes = path_nodes + [target]
                    new_edges = path_edges + [edge]
                    hypotheses.append(
                        self._make_hypothesis(seed, new_nodes, new_edges, case.context)
                    )
                    queue.append((target, new_nodes, new_edges))

        # Deterministic de-duplication by source/target/edge path.
        unique: Dict[Tuple[str, str, Tuple[str, ...]], PathHypothesis] = {}
        for h in hypotheses:
            unique[(h.source_seed, h.target, tuple(h.edge_ids))] = h
        hypotheses = sorted(
            unique.values(),
            key=lambda h: (h.target, -h.operational_priority, len(h.edge_ids), tuple(h.edge_ids)),
        )

        targets = sorted(set(case.targets)) if case.targets else sorted({h.target for h in hypotheses})
        conclusions = {
            target: self._synthesize_target(
                target, [h for h in hypotheses if h.target == target]
            )
            for target in targets
        }

        tensions: List[Dict[str, Any]] = []
        by_target: Dict[str, List[PathHypothesis]] = {}
        for h in hypotheses:
            by_target.setdefault(h.target, []).append(h)
        for target, hs in sorted(by_target.items()):
            statuses = {h.path_status for h in hs}
            contradictions = sorted(
                {x for h in hs for x in h.contradiction_source_ids}
            )
            if len(statuses) > 1 or contradictions:
                tensions.append({
                    "target": target,
                    "path_statuses": sorted(statuses),
                    "contradiction_source_ids": contradictions,
                    "interpretation": "Competing or differently bounded paths are preserved rather than averaged.",
                })

        warnings: List[str] = []
        if any(s.lifecycle_status == "provisional" for s in seeds):
            warnings.append(
                "At least one seed is a provisional node; conclusions depending on it cannot exceed provisional status."
            )
        if opportunities:
            warnings.append(
                "System edges are reported as opportunities/enabling conditions and do not auto-activate their targets."
            )
        if any(h.unresolved_modifiers for h in hypotheses):
            warnings.append(
                "Some paths have unresolved context/moderator uncertainty; no numerical context multiplier was invented."
            )

        return CanonicalReasoningResult(
            seeds=seeds,
            hypotheses=hypotheses,
            conclusions=conclusions,
            trace=[trace_by_key[k] for k in sorted(trace_by_key)],
            tensions=tensions,
            opportunities=sorted(opportunities, key=lambda x: (x.source, x.edge_id)),
            warnings=warnings,
        )


def summarize_canonical(result: CanonicalReasoningResult) -> str:
    lines: List[str] = []
    lines.append("Canonical reasoning trace")
    for target, conclusion in sorted(result.conclusions.items()):
        lines.append(
            f"- {target}: {conclusion.status}; causal ceiling={conclusion.causal_ceiling}; "
            f"path={conclusion.selected_path_edge_ids or 'none'}"
        )
    if result.tensions:
        lines.append("Tensions:")
        for t in result.tensions:
            lines.append(
                f"- {t['target']}: statuses={t['path_statuses']} "
                f"contradictions={t['contradiction_source_ids']}"
            )
    if result.warnings:
        lines.append("Warnings:")
        lines.extend(f"- {w}" for w in result.warnings)
    return "\n".join(lines)
