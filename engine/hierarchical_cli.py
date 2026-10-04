import argparse
import json
from pathlib import Path

from measurement import MeasurementMapper
from .hierarchical import HierarchicalReasoner

def main():
    parser = argparse.ArgumentParser(description="Run hierarchical Social Media Growth reasoning.")
    parser.add_argument("case", help="JSON case with observations and/or subnode seeds.")
    args = parser.parse_args()

    payload = json.loads(Path(args.case).read_text())
    observations = payload.get("observations", {})
    manual_subnode_seeds = payload.get("subnode_seeds", {})

    mapper = MeasurementMapper("measurement/proxies.json")
    mapped = mapper.map(observations) if observations else None

    subnode_seeds = dict(manual_subnode_seeds)
    negative = {}
    measurement_trace = []
    measurement_warnings = []
    if mapped:
        for node, value in mapped.subnode_seeds.items():
            subnode_seeds[node] = max(subnode_seeds.get(node, 0.0), value)
        negative = mapped.negative_evidence
        measurement_trace = mapped.trace
        measurement_warnings = mapped.warnings

    reasoner = HierarchicalReasoner(
        "data/nodes.json",
        "data/edges.json",
        "data/subnodes.json",
        "data/subedges.json",
        "research/evidence_registry.json",
        "research/contradictions.json",
    )
    result = reasoner.reason(
        subnode_seeds=subnode_seeds,
        context=payload.get("context", {}),
        direct_core_seeds=payload.get("core_seeds", {}),
        negative_evidence=negative,
    )

    out = {
        "measurement": {
            "subnode_seeds": subnode_seeds,
            "negative_evidence": negative,
            "warnings": measurement_warnings,
            "trace": measurement_trace[:12],
        },
        "subnodes": {
            "dominant_nodes": result.subnode_result.dominant_nodes,
            "activations": result.subnode_result.activations,
        },
        "core_seed_rollup": result.core_seed_rollup,
        "core": {
            "dominant_nodes": result.core_result.dominant_nodes,
            "activations": result.core_result.activations,
            "tensions": result.core_result.tensions,
        },
        "evidence_warnings": result.evidence_warnings,
    }
    print(json.dumps(out, indent=2))

if __name__ == "__main__":
    main()
