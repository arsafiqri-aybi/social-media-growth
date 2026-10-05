from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Dict, List


@dataclass(frozen=True)
class ObservationAssessment:
    observation_type: str
    validity_class: str
    stage: str
    can_seed_latent: bool
    warnings: List[str]
    requirements_met: bool

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class ProxyAssessment:
    proxy_id: str
    validity_class: str
    stage: str
    candidate_explanations: List[str]
    latent_targets: List[str]
    can_auto_identify_latent: bool
    warning: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class ExperimentAssessment:
    experiment_id: str
    causal_claim_status: str
    bounded_causal_claim_allowed: bool
    warnings: List[str]

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class GlobalMeasurementSystem:
    """Global social-media-growth measurement guardrail.

    Classifies observations/proxies and experiment identifiability.
    It deliberately does not estimate latent psychology or scientific effect sizes.
    """

    def __init__(
        self,
        observation_schema_path: str | Path,
        proxy_schema_path: str | Path,
        experiment_schema_path: str | Path,
    ):
        self.observation_schema = json.loads(Path(observation_schema_path).read_text())
        self.proxy_schema = json.loads(Path(proxy_schema_path).read_text())
        self.experiment_schema = json.loads(Path(experiment_schema_path).read_text())
        self.observation_types = {
            item["id"]: item for item in self.observation_schema["observation_types"]
        }
        self.proxies = {item["id"]: item for item in self.proxy_schema["proxies"]}

    @classmethod
    def from_repo_root(cls, root: str | Path) -> "GlobalMeasurementSystem":
        root = Path(root)
        return cls(
            root / "measurement/global_observation_schema.json",
            root / "measurement/global_proxy_schema.json",
            root / "measurement/global_experiment_schema.json",
        )

    def assess_observation(self, observation: Dict[str, Any]) -> ObservationAssessment:
        observation_type = observation.get("type")
        if observation_type not in self.observation_types:
            raise ValueError(f"Unknown global observation type: {observation_type}")

        spec = self.observation_types[observation_type]
        requirements = spec.get("requirements", [])
        requirements_met = all(bool(observation.get(key)) for key in requirements)
        can_seed = bool(spec.get("can_seed_latent", False))
        warnings = list(spec.get("warnings", []))

        if can_seed and not requirements_met:
            can_seed = False
            warnings.append(
                "Latent seeding blocked because construct-measurement requirements are incomplete."
            )

        return ObservationAssessment(
            observation_type=observation_type,
            validity_class=spec["validity_class"],
            stage=spec["stage"],
            can_seed_latent=can_seed,
            warnings=warnings,
            requirements_met=requirements_met if requirements else True,
        )

    def assess_proxy(self, proxy_id: str) -> ProxyAssessment:
        if proxy_id not in self.proxies:
            raise ValueError(f"Unknown global proxy: {proxy_id}")
        spec = self.proxies[proxy_id]
        return ProxyAssessment(
            proxy_id=proxy_id,
            validity_class=spec["validity_class"],
            stage=spec["stage"],
            candidate_explanations=list(spec.get("candidate_explanations", [])),
            latent_targets=list(spec.get("latent_targets", [])),
            can_auto_identify_latent=False,
            warning=spec["warning"],
        )

    def assess_experiment(self, record: Dict[str, Any]) -> ExperimentAssessment:
        missing = [
            key
            for key in self.experiment_schema["required_fields"]
            if not record.get(key)
        ]
        if missing:
            raise ValueError(
                "Experiment record missing required fields: " + ", ".join(sorted(missing))
            )

        warnings: List[str] = []
        randomization = bool(record.get("randomization_documented"))
        composition_checked = bool(record.get("audience_composition_checked"))
        delivery_control = record.get("delivery_control")
        targeting_can_vary = bool(record.get("platform_targeting_can_vary", False))

        if delivery_control not in self.experiment_schema["delivery_control_values"]:
            raise ValueError(f"Unsupported delivery_control: {delivery_control}")

        allowed = (
            randomization
            and composition_checked
            and delivery_control == "controlled"
            and not targeting_can_vary
        )

        if not randomization:
            warnings.append("Random assignment is not documented.")
        if not composition_checked:
            warnings.append("Audience composition equivalence is not documented.")
        if delivery_control != "controlled":
            warnings.append(
                "Delivery is not fully controlled; platform allocation may affect outcomes."
            )
        if targeting_can_vary:
            warnings.append(
                "Platform targeting/ranking may vary by condition, confounding intervention effects."
            )

        status = (
            "design_supports_bounded_causal_inference"
            if allowed
            else "causal_claim_blocked_or_confounded"
        )

        return ExperimentAssessment(
            experiment_id=str(record["experiment_id"]),
            causal_claim_status=status,
            bounded_causal_claim_allowed=allowed,
            warnings=warnings,
        )
