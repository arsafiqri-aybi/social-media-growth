from __future__ import annotations

import copy
from dataclasses import asdict, dataclass, field
from typing import Any, Dict, List, Optional


ALLOWED_STATES = {
    "high", "low", "up", "down", "flat", "present", "absent", "unknown"
}


@dataclass(frozen=True)
class PredictionRecord:
    prediction_id: str
    account_id: str
    hypothesis_id: str
    intervention: Dict[str, Any]
    expected_metric_states: Dict[str, str]
    falsification_metric_states: Dict[str, str]
    context: Dict[str, Any] = field(default_factory=dict)
    source_rule_ids: List[str] = field(default_factory=list)
    note: Optional[str] = None
    scope: str = "account_local_operational_prediction"

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class OutcomeRecord:
    prediction_id: str
    account_id: str
    hypothesis_id: str
    observed_metric_states: Dict[str, str]
    evaluation: str
    note: Optional[str] = None
    scope: str = "account_local_operational_outcome"

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class PredictionOutcomeStore:
    """Append-only account-local prediction/outcome store.

    This class has no method or reference capable of mutating the scientific
    graph. It records operational learning only.
    """

    def __init__(self) -> None:
        self._predictions: Dict[str, PredictionRecord] = {}
        self._outcomes: List[OutcomeRecord] = []

    @staticmethod
    def _validate_states(states: Dict[str, str], label: str) -> None:
        if not isinstance(states, dict) or not states:
            raise ValueError(f"{label} must be a non-empty mapping")
        for key, value in states.items():
            if not key:
                raise ValueError(f"{label} contains an empty metric key")
            if value not in ALLOWED_STATES:
                raise ValueError(
                    f"Unsupported metric state '{value}' in {label}; "
                    f"allowed={sorted(ALLOWED_STATES)}"
                )

    @staticmethod
    def _matches(
        observed: Dict[str, str],
        condition: Dict[str, str],
    ) -> bool:
        return all(observed.get(key) == value for key, value in condition.items())

    def register_prediction(
        self,
        *,
        prediction_id: str,
        account_id: str,
        hypothesis_id: str,
        intervention: Dict[str, Any],
        expected_metric_states: Dict[str, str],
        falsification_metric_states: Dict[str, str],
        context: Optional[Dict[str, Any]] = None,
        source_rule_ids: Optional[List[str]] = None,
        note: Optional[str] = None,
    ) -> PredictionRecord:
        if not prediction_id or not account_id or not hypothesis_id:
            raise ValueError(
                "prediction_id, account_id, and hypothesis_id are required"
            )
        if prediction_id in self._predictions:
            raise ValueError(f"Prediction already exists: {prediction_id}")
        if not isinstance(intervention, dict) or not intervention:
            raise ValueError("intervention must be a non-empty mapping")

        self._validate_states(expected_metric_states, "expected_metric_states")
        self._validate_states(
            falsification_metric_states,
            "falsification_metric_states",
        )

        for metric, expected in expected_metric_states.items():
            if falsification_metric_states.get(metric) == expected:
                raise ValueError(
                    f"Metric '{metric}' has identical expected and "
                    "falsification states"
                )

        record = PredictionRecord(
            prediction_id=prediction_id,
            account_id=account_id,
            hypothesis_id=hypothesis_id,
            intervention=copy.deepcopy(intervention),
            expected_metric_states=copy.deepcopy(expected_metric_states),
            falsification_metric_states=copy.deepcopy(
                falsification_metric_states
            ),
            context=copy.deepcopy(context or {}),
            source_rule_ids=sorted(set(source_rule_ids or [])),
            note=note,
        )
        self._predictions[prediction_id] = record
        return record

    def record_outcome(
        self,
        *,
        prediction_id: str,
        observed_metric_states: Dict[str, str],
        note: Optional[str] = None,
    ) -> OutcomeRecord:
        if prediction_id not in self._predictions:
            raise ValueError(
                "Outcome rejected: a prediction must be registered first"
            )
        self._validate_states(observed_metric_states, "observed_metric_states")

        prediction = self._predictions[prediction_id]
        falsifies = self._matches(
            observed_metric_states,
            prediction.falsification_metric_states,
        )
        supports = self._matches(
            observed_metric_states,
            prediction.expected_metric_states,
        )

        if falsifies:
            evaluation = "falsifies_prediction"
        elif supports:
            evaluation = "supports_prediction"
        else:
            evaluation = "inconclusive"

        outcome = OutcomeRecord(
            prediction_id=prediction_id,
            account_id=prediction.account_id,
            hypothesis_id=prediction.hypothesis_id,
            observed_metric_states=copy.deepcopy(observed_metric_states),
            evaluation=evaluation,
            note=note,
        )
        self._outcomes.append(outcome)
        return outcome

    def prediction(self, prediction_id: str) -> Dict[str, Any]:
        if prediction_id not in self._predictions:
            raise KeyError(prediction_id)
        return self._predictions[prediction_id].to_dict()

    def outcomes(self) -> List[Dict[str, Any]]:
        return [x.to_dict() for x in self._outcomes]

    def local_belief_summary(
        self,
        *,
        account_id: str,
        hypothesis_id: str,
    ) -> Dict[str, Any]:
        relevant = [
            x
            for x in self._outcomes
            if x.account_id == account_id and x.hypothesis_id == hypothesis_id
        ]
        counts = {
            "supports_prediction": 0,
            "falsifies_prediction": 0,
            "inconclusive": 0,
        }
        for outcome in relevant:
            counts[outcome.evaluation] += 1

        support = counts["supports_prediction"]
        falsify = counts["falsifies_prediction"]
        inconclusive = counts["inconclusive"]

        if not relevant:
            status = "no_outcomes"
        elif support and falsify:
            status = "mixed_local_evidence"
        elif support:
            status = "local_support_pattern"
        elif falsify:
            status = "local_falsification_pattern"
        else:
            status = "inconclusive_local_evidence"

        return {
            "account_id": account_id,
            "hypothesis_id": hypothesis_id,
            "status": status,
            "counts": counts,
            "outcome_count": len(relevant),
            "scope": "account_local_operational_belief_only",
            "scientific_evidence_mutation_allowed": False,
            "warning": (
                "This summary describes account-local prediction outcomes. "
                "It is not a scientific confidence score or causal effect size."
            ),
        }
