import argparse
import json
from pathlib import Path

from .core import NeuralReasoner
from .model import ReasoningCase
from .explain import summarize


def main():
    parser = argparse.ArgumentParser(description="Run the Social Media Growth neural reasoner.")
    parser.add_argument("case", help="Path to a JSON case file.")
    parser.add_argument("--nodes", default="data/nodes.json")
    parser.add_argument("--edges", default="data/edges.json")
    parser.add_argument("--json", action="store_true", help="Emit machine-readable JSON.")
    args = parser.parse_args()

    case_data = json.loads(Path(args.case).read_text())
    reasoner = NeuralReasoner(args.nodes, args.edges)
    result = reasoner.reason(
        ReasoningCase(
            seeds=case_data.get("seeds", {}),
            context=case_data.get("context", {}),
            goals=case_data.get("goals", []),
            notes=case_data.get("notes"),
        )
    )

    if args.json:
        payload = {
            "activations": result.activations,
            "confidence": result.confidence,
            "support": result.support,
            "inhibition": result.inhibition,
            "iterations": result.iterations,
            "converged": result.converged,
            "dominant_nodes": result.dominant_nodes,
            "tensions": result.tensions,
            "trace": [t.__dict__ for t in result.trace],
        }
        print(json.dumps(payload, indent=2))
        return

    nodes = json.loads(Path(args.nodes).read_text())
    labels = {n["id"]: n["label"] for n in nodes["nodes"]}
    print(summarize(result, labels))


if __name__ == "__main__":
    main()
