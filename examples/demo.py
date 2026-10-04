import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from engine import NeuralReasoner, ReasoningCase
from engine.explain import summarize

nodes = json.loads((ROOT / "data" / "nodes.json").read_text())
labels = {n["id"]: n["label"] for n in nodes["nodes"]}

reasoner = NeuralReasoner(
    ROOT / "data" / "nodes.json",
    ROOT / "data" / "edges.json"
)

case = ReasoningCase(
    seeds={
        "identity": 0.82,
        "curiosity": 0.70,
        "trust": 0.35,
        "valuation_emotion": 0.68
    },
    context={"high_arousal": 0.75},
    notes="Identity-relevant, curiosity-rich content with moderate-low trust."
)

result = reasoner.reason(case)
print(summarize(result, labels))
