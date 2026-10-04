import json
import math
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Any

def _clamp01(x):
    return max(0.0, min(1.0, float(x)))

@dataclass
class MeasurementResult:
    subnode_seeds: Dict[str, float]
    negative_evidence: Dict[str, float]
    trace: List[Dict[str, Any]]
    warnings: List[str]

class MeasurementMapper:
    """
    Conservative observation -> subnode mapper.

    It maps measurable platform/account signals to candidate psychological
    subnodes. These are proxies, not validated latent-variable estimates.
    """

    def __init__(self, proxy_path):
        data = json.loads(Path(proxy_path).read_text())
        self.proxies = {p["id"]: p for p in data["proxies"]}

    @staticmethod
    def _strength(obs, sensitivity):
        if "normalized_delta" in obs:
            return _clamp01(obs["normalized_delta"])
        if "normalized" in obs:
            return _clamp01(obs["normalized"])
        if "value" not in obs or "baseline" not in obs:
            raise ValueError("Observation needs normalized_delta, normalized, or value+baseline")
        value = float(obs["value"])
        baseline = float(obs["baseline"])
        if baseline < 0 or value < 0:
            raise ValueError("Rates/metrics must be non-negative")
        if baseline == 0:
            return _clamp01(value)
        relative_change = (value - baseline) / max(abs(baseline), 1e-9)
        if relative_change >= 0:
            return _clamp01(1.0 - math.exp(-float(sensitivity) * relative_change))
        return -_clamp01(1.0 - math.exp(-float(sensitivity) * abs(relative_change)))

    def map(self, observations: Dict[str, Dict[str, float]]) -> MeasurementResult:
        positive: Dict[str, float] = {}
        negative: Dict[str, float] = {}
        trace = []
        warnings = []

        for proxy_id, obs in observations.items():
            if proxy_id not in self.proxies:
                raise ValueError(f"Unknown measurement proxy: {proxy_id}")
            proxy = self.proxies[proxy_id]
            strength = self._strength(obs, proxy.get("sensitivity", 0.5))
            warnings.append(f"{proxy_id}: {proxy['ambiguity']}")
            for target in proxy["targets"]:
                contribution = strength * float(target["weight"])
                node = target["node"]
                if contribution >= 0:
                    positive[node] = max(positive.get(node, 0.0), contribution)
                else:
                    negative[node] = max(negative.get(node, 0.0), abs(contribution))
                trace.append({
                    "proxy": proxy_id,
                    "node": node,
                    "proxy_strength": round(strength, 6),
                    "mapping_weight": target["weight"],
                    "contribution": round(contribution, 6),
                    "confidence": proxy["confidence"],
                    "ambiguity": proxy["ambiguity"],
                })

        return MeasurementResult(
            subnode_seeds={k: round(_clamp01(v), 6) for k, v in positive.items()},
            negative_evidence={k: round(_clamp01(v), 6) for k, v in negative.items()},
            trace=sorted(trace, key=lambda x: abs(x["contribution"]), reverse=True),
            warnings=warnings,
        )
