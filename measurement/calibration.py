from __future__ import annotations

import copy
import math
from dataclasses import dataclass, asdict
from typing import Any, Dict, List, Optional, Tuple


@dataclass(frozen=True)
class CalibrationSummary:
    predictor_id: str
    outcome_id: str
    sample_count: int
    status: str
    pearson_r: Optional[float]
    association_direction: str
    interpretation: str
    scientific_effect_claim_allowed: bool = False
    latent_state_claim_allowed: bool = False


class OperationalCalibrationStore:
    """
    Account-local empirical calibration over observable variables only.

    This class never receives or mutates scientific nodes/edges. Its outputs are
    predictive associations for one operational context, not causal estimates and
    not psychological latent-state estimates.
    """

    def __init__(self) -> None:
        self._records: List[Dict[str, Any]] = []

    def record(
        self,
        case_id: str,
        predictors: Dict[str, float],
        outcomes: Dict[str, float],
        context: Optional[Dict[str, Any]] = None,
    ) -> None:
        if not case_id:
            raise ValueError("case_id is required")
        if not predictors or not outcomes:
            raise ValueError("predictors and outcomes are required")
        self._records.append({
            "case_id": str(case_id),
            "predictors": {k: float(v) for k, v in predictors.items()},
            "outcomes": {k: float(v) for k, v in outcomes.items()},
            "context": copy.deepcopy(context or {}),
        })

    @staticmethod
    def _pearson(xs: List[float], ys: List[float]) -> Optional[float]:
        if len(xs) != len(ys) or len(xs) < 2:
            return None
        mx = sum(xs) / len(xs)
        my = sum(ys) / len(ys)
        dx = [x - mx for x in xs]
        dy = [y - my for y in ys]
        vx = sum(x * x for x in dx)
        vy = sum(y * y for y in dy)
        if vx <= 0 or vy <= 0:
            return None
        return sum(x * y for x, y in zip(dx, dy)) / math.sqrt(vx * vy)

    def summarize(
        self,
        predictor_id: str,
        outcome_id: str,
        min_records: int = 20,
    ) -> CalibrationSummary:
        pairs: List[Tuple[float, float]] = []
        for r in self._records:
            if predictor_id in r["predictors"] and outcome_id in r["outcomes"]:
                pairs.append((r["predictors"][predictor_id], r["outcomes"][outcome_id]))

        n = len(pairs)
        if n < min_records:
            return CalibrationSummary(
                predictor_id=predictor_id,
                outcome_id=outcome_id,
                sample_count=n,
                status="insufficient_data",
                pearson_r=None,
                association_direction="unknown",
                interpretation=(
                    f"Need at least {min_records} paired account-local observations before "
                    "reporting even a descriptive predictive association."
                ),
            )

        r = self._pearson([x for x, _ in pairs], [y for _, y in pairs])
        if r is None:
            status = "non_identifiable"
            direction = "unknown"
            interpretation = "Association is not identifiable because at least one variable has no usable variance."
        else:
            status = "descriptive_association_only"
            direction = "positive" if r > 0 else "negative" if r < 0 else "zero"
            interpretation = (
                "Account-local descriptive association only. It is not causal, is not a "
                "psychological latent-state estimate, and must not rewrite scientific graph edges."
            )

        return CalibrationSummary(
            predictor_id=predictor_id,
            outcome_id=outcome_id,
            sample_count=n,
            status=status,
            pearson_r=None if r is None else round(r, 6),
            association_direction=direction,
            interpretation=interpretation,
        )

    def export(self) -> Dict[str, Any]:
        return {
            "scope": "account_local_operational_calibration",
            "records": copy.deepcopy(self._records),
            "scientific_graph_mutation_allowed": False,
            "latent_state_inference_allowed": False,
        }
