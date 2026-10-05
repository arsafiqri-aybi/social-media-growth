from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional


@dataclass(frozen=True)
class MeasurementEvidence:
    proxy_id: str
    target_id: Optional[str]
    validity_class: str
    observed_direction: str
    reasoning_basis: Optional[str]
    reasoning_direction: Optional[str]
    can_seed_reasoner: bool
    rationale: str
    warning: str
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class CanonicalMeasurementResult:
    evidence: List[MeasurementEvidence]
    reasoning_seeds: Dict[str, Dict[str, Any]]
    candidate_explanations: List[Dict[str, Any]]
    warnings: List[str]
    conflicts: List[Dict[str, Any]]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "evidence": [asdict(x) for x in self.evidence],
            "reasoning_seeds": self.reasoning_seeds,
            "candidate_explanations": self.candidate_explanations,
            "warnings": self.warnings,
            "conflicts": self.conflicts,
        }


class CanonicalMeasurementMapper:
    """
    Conservative observable -> evidence mapper.

    It does not estimate latent activation magnitudes. It decides whether an
    observation is direct behavior/event evidence, construct-valid measurement,
    hypothesis-grade proxy evidence, or an ambiguous observable that must not
    auto-seed a latent psychological node.
    """

    BASIS_PRIORITY = {
        "direct_measurement": 5,
        "validated_observation": 4,
        "external_event": 4,
        "structured_observation": 3,
        "proxy_hypothesis": 1,
    }

    def __init__(self, registry_path: str | Path, nodes_path: str | Path, connectors_path: str | Path):
        self.registry = json.loads(Path(registry_path).read_text())
        self.specs = {p["id"]: p for p in self.registry["proxies"]}
        self.nodes = {
            n["id"]: n for n in json.loads(Path(nodes_path).read_text())["neurons"]
        }
        self.connectors = {
            c["id"]: c for c in json.loads(Path(connectors_path).read_text())["connectors"]
        }
        self._validate_registry()

    @classmethod
    def from_repo_root(cls, root: str | Path) -> "CanonicalMeasurementMapper":
        root = Path(root)
        return cls(
            root / "measurement/v2/proxies.json",
            root / "research/r2/cycle01/l2-neuron-candidates.json",
            root / "research/r3/cycle03/context-connectors.json",
        )

    def _validate_registry(self) -> None:
        known = set(self.nodes) | set(self.connectors)
        for spec in self.specs.values():
            for target in spec.get("direct_targets", []):
                tid = target["node_id"]
                if tid not in known:
                    raise ValueError(f"Unknown target {tid} in proxy {spec['id']}")
                if tid in self.nodes and self.nodes[tid]["status"] not in {"accepted", "provisional"}:
                    raise ValueError(f"Proxy {spec['id']} points to noncanonical node {tid}")

    @staticmethod
    def _observed_direction(obs: Dict[str, Any]) -> str:
        explicit = obs.get("direction")
        if explicit is not None:
            mapping = {
                "up": "up",
                "increase": "up",
                "down": "down",
                "decrease": "down",
                "present": "present",
                "absent": "absent",
                "flat": "flat",
                "unchanged": "flat",
            }
            if explicit not in mapping:
                raise ValueError(f"Unsupported observation direction: {explicit}")
            return mapping[explicit]

        if "value" in obs and "baseline" in obs:
            value = float(obs["value"])
            baseline = float(obs["baseline"])
            if value > baseline:
                return "up"
            if value < baseline:
                return "down"
            return "flat"

        if "value" in obs:
            value = float(obs["value"])
            if value > 0:
                return "present"
            if value == 0:
                return "absent"

        raise ValueError(
            "Observation requires explicit direction, value+baseline, or event/count value."
        )

    @staticmethod
    def _requirements_met(spec: Dict[str, Any], obs: Dict[str, Any]) -> bool:
        for req in spec.get("requires", []):
            if not bool(obs.get(req)):
                return False
        return True

    @staticmethod
    def _reasoning_direction(observed_direction: str) -> Optional[str]:
        if observed_direction in {"up", "present"}:
            return "support"
        if observed_direction in {"down", "absent"}:
            return "oppose"
        return None

    def map(self, observations: Dict[str, Dict[str, Any]]) -> CanonicalMeasurementResult:
        evidence: List[MeasurementEvidence] = []
        candidate_explanations: List[Dict[str, Any]] = []
        warnings: List[str] = []
        seed_candidates: Dict[str, List[Dict[str, Any]]] = {}

        for proxy_id in sorted(observations):
            if proxy_id not in self.specs:
                raise ValueError(f"Unknown measurement proxy: {proxy_id}")
            obs = dict(observations[proxy_id])
            spec = self.specs[proxy_id]
            direction = self._observed_direction(obs)
            warning = spec["warning"]
            warnings.append(f"{proxy_id}: {warning}")

            for candidate in spec.get("candidate_explanations", []):
                candidate_explanations.append({
                    "proxy_id": proxy_id,
                    "candidate_node_id": candidate,
                    "observed_direction": direction,
                    "status": "competing_explanation_only",
                    "auto_seeded": False,
                    "reason": "Candidate explanations are not identified by the observable alone.",
                })

            requirements_met = self._requirements_met(spec, obs)
            allowed_positive = direction in set(spec.get("seed_on", []))
            allowed_negative = direction in set(spec.get("negative_seed_on", []))
            allowed = allowed_positive or allowed_negative

            if spec["validity_class"] == "validated_construct_measure" and not requirements_met:
                allowed = False
                warnings.append(
                    f"{proxy_id}: latent seeding blocked because validated_instrument/domain_match requirements were not satisfied."
                )

            if not spec.get("direct_targets"):
                evidence.append(MeasurementEvidence(
                    proxy_id=proxy_id,
                    target_id=None,
                    validity_class=spec["validity_class"],
                    observed_direction=direction,
                    reasoning_basis=None,
                    reasoning_direction=None,
                    can_seed_reasoner=False,
                    rationale="Observable retained without automatic latent-state inference.",
                    warning=warning,
                    metadata={"requirements_met": requirements_met},
                ))
                continue

            for target in spec["direct_targets"]:
                target_id = target["node_id"]
                if target.get("dimension") and obs.get("dimension") not in {None, target["dimension"]}:
                    continue

                reasoning_direction = self._reasoning_direction(direction)
                can_seed = bool(allowed and reasoning_direction)
                basis = target["basis"] if can_seed else None
                rationale = (
                    "Construct/behavior mapping satisfies the registry seeding rule."
                    if can_seed
                    else "Observation is preserved but does not satisfy the automatic seeding rule."
                )
                ev = MeasurementEvidence(
                    proxy_id=proxy_id,
                    target_id=target_id,
                    validity_class=spec["validity_class"],
                    observed_direction=direction,
                    reasoning_basis=basis,
                    reasoning_direction=reasoning_direction if can_seed else None,
                    can_seed_reasoner=can_seed,
                    rationale=rationale,
                    warning=warning,
                    metadata={
                        "requirements_met": requirements_met,
                        "dimension": target.get("dimension"),
                    },
                )
                evidence.append(ev)
                if can_seed:
                    seed_candidates.setdefault(target_id, []).append({
                        "basis": basis,
                        "direction": reasoning_direction,
                        "note": f"Measurement v2 from {proxy_id}; validity_class={spec['validity_class']}",
                        "proxy_id": proxy_id,
                    })

        reasoning_seeds: Dict[str, Dict[str, Any]] = {}
        conflicts: List[Dict[str, Any]] = []
        for target_id, candidates in sorted(seed_candidates.items()):
            directions = {x["direction"] for x in candidates}
            if len(directions) > 1:
                conflicts.append({
                    "target_id": target_id,
                    "type": "measurement_direction_conflict",
                    "candidates": candidates,
                    "resolution": "no automatic seed; preserve competing evidence",
                })
                continue

            selected = sorted(
                candidates,
                key=lambda x: (-self.BASIS_PRIORITY.get(x["basis"], 0), x["proxy_id"]),
            )[0]
            reasoning_seeds[target_id] = {
                "basis": selected["basis"],
                "direction": selected["direction"],
                "note": selected["note"],
            }

        return CanonicalMeasurementResult(
            evidence=evidence,
            reasoning_seeds=reasoning_seeds,
            candidate_explanations=candidate_explanations,
            warnings=warnings,
            conflicts=conflicts,
        )
