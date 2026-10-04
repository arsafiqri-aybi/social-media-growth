import json
from pathlib import Path
from typing import List

from .model import Edge, ReasoningCase, EdgeContribution, ReasoningResult


def _clamp01(x: float) -> float:
    return max(0.0, min(1.0, float(x)))


class NeuralReasoner:
    """
    Transparent graph-based reasoning engine.

    This is not a biological neural network and does not claim to reproduce
    human cognition. It operationalizes the repository's psychological
    architecture as auditable weighted inference.
    """

    def __init__(self, nodes_path: str, edges_path: str, damping: float = 0.62,
                 max_iterations: int = 12, convergence_epsilon: float = 1e-4):
        self.damping = damping
        self.max_iterations = max_iterations
        self.convergence_epsilon = convergence_epsilon

        nodes_data = json.loads(Path(nodes_path).read_text())
        edges_data = json.loads(Path(edges_path).read_text())
        self.nodes = {n["id"]: n for n in nodes_data["nodes"]}
        confidence_weights = edges_data["confidence_weights"]

        self.edges: List[Edge] = []
        for e in edges_data["edges"]:
            if e["source"] not in self.nodes or e["target"] not in self.nodes:
                raise ValueError(f"Unknown node in edge {e['id']}")
            self.edges.append(
                Edge(
                    id=e["id"],
                    source=e["source"],
                    target=e["target"],
                    relation=e["relation"],
                    weight=float(e["weight"]),
                    confidence=e["confidence"],
                    confidence_weight=float(confidence_weights[e["confidence"]]),
                    causal_status=e.get("causal_status", "unspecified"),
                    mechanism=e["mechanism"],
                    contexts=e.get("contexts", {}),
                )
            )

    def _context_multiplier(self, edge: Edge, context):
        m = 1.0
        for key, multiplier in edge.contexts.items():
            if key in context:
                v = _clamp01(context[key])
                m *= 1.0 + (float(multiplier) - 1.0) * v
        return max(0.0, m)

    def reason(self, case: ReasoningCase) -> ReasoningResult:
        unknown = set(case.seeds) - set(self.nodes)
        if unknown:
            raise ValueError(f"Unknown seed nodes: {sorted(unknown)}")

        seeds = {nid: _clamp01(case.seeds.get(nid, 0.0)) for nid in self.nodes}
        a = dict(seeds)
        trace = []
        converged = False
        support = {nid: 0.0 for nid in self.nodes}
        inhibition = {nid: 0.0 for nid in self.nodes}
        incoming_conf = {nid: [] for nid in self.nodes}

        for iteration in range(1, self.max_iterations + 1):
            net = {nid: 0.0 for nid in self.nodes}
            abs_net = {nid: 0.0 for nid in self.nodes}
            support = {nid: 0.0 for nid in self.nodes}
            inhibition = {nid: 0.0 for nid in self.nodes}
            incoming_conf = {nid: [] for nid in self.nodes}
            iter_trace = []

            for edge in self.edges:
                cm = self._context_multiplier(edge, case.context)
                signed_weight = edge.weight
                contrib = (
                    a[edge.source] *
                    signed_weight *
                    edge.confidence_weight *
                    cm
                )
                net[edge.target] += contrib
                abs_net[edge.target] += abs(contrib)
                incoming_conf[edge.target].append(edge.confidence_weight)
                if contrib >= 0:
                    support[edge.target] += contrib
                else:
                    inhibition[edge.target] += abs(contrib)

                if abs(contrib) > 1e-8:
                    iter_trace.append(
                        EdgeContribution(
                            edge_id=edge.id,
                            source=edge.source,
                            target=edge.target,
                            relation=edge.relation,
                            raw_source_activation=a[edge.source],
                            signed_weight=signed_weight,
                            confidence_weight=edge.confidence_weight,
                            context_multiplier=cm,
                            contribution=contrib,
                            mechanism=edge.mechanism,
                            causal_status=edge.causal_status,
                        )
                    )

            nxt = {}
            for nid in self.nodes:
                propagated = 0.0 if abs_net[nid] == 0 else net[nid] / max(1.0, abs_net[nid])
                nxt[nid] = _clamp01(seeds[nid] + self.damping * propagated)

            delta = max(abs(nxt[nid] - a[nid]) for nid in self.nodes)
            a = nxt
            trace = iter_trace
            if delta < self.convergence_epsilon:
                converged = True
                break

        node_conf = {}
        for nid in self.nodes:
            cs = incoming_conf[nid]
            evidence_coverage = sum(cs) / len(cs) if cs else (1.0 if seeds[nid] > 0 else 0.0)
            seed_basis = 1.0 if seeds[nid] > 0 else 0.0
            node_conf[nid] = _clamp01(0.55 * evidence_coverage + 0.45 * seed_basis)

        dominant = [nid for nid, _ in sorted(a.items(), key=lambda kv: kv[1], reverse=True)[:4]]

        tensions = []
        for nid in self.nodes:
            s, i = support[nid], inhibition[nid]
            if s > 0.05 and i > 0.05:
                tensions.append({
                    "node": nid,
                    "support": round(s, 4),
                    "inhibition": round(i, 4),
                    "balance": round(s - i, 4),
                })

        return ReasoningResult(
            activations={k: round(v, 6) for k, v in a.items()},
            confidence={k: round(v, 6) for k, v in node_conf.items()},
            support={k: round(v, 6) for k, v in support.items()},
            inhibition={k: round(v, 6) for k, v in inhibition.items()},
            trace=sorted(trace, key=lambda t: abs(t.contribution), reverse=True),
            iterations=iteration,
            converged=converged,
            dominant_nodes=dominant,
            tensions=tensions,
        )
