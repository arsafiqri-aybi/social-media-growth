from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Any, Optional

from .core import NeuralReasoner, _clamp01
from .model import ReasoningCase, ReasoningResult
from .evidence import EvidenceRegistry

@dataclass
class HierarchicalResult:
    subnode_result: ReasoningResult
    core_seed_rollup: Dict[str, float]
    core_result: ReasoningResult
    evidence_warnings: List[Dict[str, Any]]
    negative_evidence: Dict[str, float]

class HierarchicalReasoner:
    """
    Two-level reasoner:
      sub-neuron network -> conservative core roll-up -> core network.

    The roll-up is an architecture heuristic, not a psychometric latent-variable model.
    """

    def __init__(
        self,
        core_nodes_path,
        core_edges_path,
        subnodes_path,
        subedges_path,
        evidence_path=None,
        contradictions_path=None,
    ):
        self.core_reasoner = NeuralReasoner(core_nodes_path, core_edges_path)
        self.sub_reasoner = NeuralReasoner(subnodes_path, subedges_path)

        import json
        subnodes_data = json.loads(Path(subnodes_path).read_text())
        self.parent = {n["id"]: n["parent"] for n in subnodes_data["nodes"]}
        self.by_parent: Dict[str, List[str]] = {}
        for nid, parent in self.parent.items():
            self.by_parent.setdefault(parent, []).append(nid)

        self.evidence: Optional[EvidenceRegistry] = None
        if evidence_path and contradictions_path:
            self.evidence = EvidenceRegistry(evidence_path, contradictions_path)

    def _rollup(self, activations, negative_evidence=None):
        negative_evidence = negative_evidence or {}
        out = {}
        for parent, child_ids in self.by_parent.items():
            vals = sorted((activations.get(cid, 0.0) for cid in child_ids), reverse=True)
            if not vals:
                out[parent] = 0.0
                continue
            top = vals[0]
            breadth = sum(vals[1:]) / max(1, len(vals) - 1) if len(vals) > 1 else 0.0
            positive = _clamp01(top + 0.15 * breadth)

            negs = [negative_evidence.get(cid, 0.0) for cid in child_ids]
            negative = max(negs) if negs else 0.0
            out[parent] = _clamp01(positive - 0.50 * negative)
        return out

    def reason(
        self,
        subnode_seeds: Dict[str, float],
        context=None,
        direct_core_seeds=None,
        negative_evidence=None,
    ) -> HierarchicalResult:
        context = context or {}
        direct_core_seeds = direct_core_seeds or {}
        negative_evidence = negative_evidence or {}

        sub_result = self.sub_reasoner.reason(
            ReasoningCase(seeds=subnode_seeds, context=context)
        )
        rollup = self._rollup(sub_result.activations, negative_evidence)

        unknown = set(direct_core_seeds) - set(self.core_reasoner.nodes)
        if unknown:
            raise ValueError(f"Unknown direct core seeds: {sorted(unknown)}")
        for nid, value in direct_core_seeds.items():
            rollup[nid] = max(rollup.get(nid, 0.0), _clamp01(value))

        core_result = self.core_reasoner.reason(
            ReasoningCase(seeds=rollup, context=context)
        )

        warnings = []
        if self.evidence:
            active_targets = (
                [t.edge_id for t in sub_result.trace[:12]] +
                [t.edge_id for t in core_result.trace[:12]] +
                core_result.dominant_nodes
            )
            warnings = self.evidence.warnings_for(active_targets)

        return HierarchicalResult(
            subnode_result=sub_result,
            core_seed_rollup={k: round(v, 6) for k, v in rollup.items()},
            core_result=core_result,
            evidence_warnings=warnings,
            negative_evidence=negative_evidence,
        )
