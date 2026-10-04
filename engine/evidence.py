import json
from pathlib import Path
from typing import Dict, List, Any

class EvidenceRegistry:
    def __init__(self, evidence_path, contradictions_path):
        self.evidence_data = json.loads(Path(evidence_path).read_text())
        self.contradiction_data = json.loads(Path(contradictions_path).read_text())
        self.evidence = {r["id"]: r for r in self.evidence_data.get("records", [])}
        self.contradictions = {r["id"]: r for r in self.contradiction_data.get("records", [])}

        self._evidence_by_target: Dict[str, List[Dict[str, Any]]] = {}
        for record in self.evidence.values():
            for target in record.get("applies_to", []):
                self._evidence_by_target.setdefault(target, []).append(record)

        self._contradictions_by_target: Dict[str, List[Dict[str, Any]]] = {}
        for record in self.contradictions.values():
            for target in record.get("targets", []):
                self._contradictions_by_target.setdefault(target, []).append(record)

    def profile(self, target_id: str) -> Dict[str, Any]:
        return {
            "target": target_id,
            "evidence": self._evidence_by_target.get(target_id, []),
            "contradictions": self._contradictions_by_target.get(target_id, []),
        }

    def warnings_for(self, target_ids):
        seen = set()
        out = []
        for target in target_ids:
            for warning in self._contradictions_by_target.get(target, []):
                if warning["id"] in seen:
                    continue
                seen.add(warning["id"])
                out.append({
                    "id": warning["id"],
                    "severity": warning["severity"],
                    "type": warning["type"],
                    "statement": warning["statement"],
                    "reasoning_rule": warning["reasoning_rule"],
                    "target": target,
                })
        severity_rank = {"high": 3, "medium": 2, "low": 1}
        out.sort(key=lambda x: severity_rank.get(x["severity"], 0), reverse=True)
        return out
