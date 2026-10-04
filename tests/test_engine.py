import json
from pathlib import Path
import tempfile
import unittest

from engine import NeuralReasoner, ReasoningCase

ROOT = Path(__file__).resolve().parents[1]

class NeuralReasonerTests(unittest.TestCase):
    def setUp(self):
        self.r = NeuralReasoner(
            ROOT / "data" / "nodes.json",
            ROOT / "data" / "edges.json"
        )

    def test_curiosity_propagates_to_attention_and_value(self):
        out = self.r.reason(ReasoningCase(seeds={"curiosity": 0.9}))
        self.assertGreater(out.activations["attention"], 0.20)
        self.assertGreater(out.activations["valuation_emotion"], 0.15)
        self.assertIn("curiosity", out.dominant_nodes)

    def test_identity_activates_social_and_relational_nodes(self):
        out = self.r.reason(ReasoningCase(seeds={"identity": 0.9}))
        self.assertGreater(out.activations["social_transmission"], 0.15)
        self.assertGreater(out.activations["connection"], 0.10)
        self.assertGreater(out.activations["trust"], 0.08)

    def test_high_arousal_context_strengthens_emotion_to_transmission(self):
        low = self.r.reason(ReasoningCase(
            seeds={"valuation_emotion": 0.8},
            context={"high_arousal": 0.0}
        ))
        high = self.r.reason(ReasoningCase(
            seeds={"valuation_emotion": 0.8},
            context={"high_arousal": 1.0}
        ))
        self.assertGreater(
            high.support["social_transmission"],
            low.support["social_transmission"]
        )

    def test_unknown_node_rejected(self):
        with self.assertRaises(ValueError):
            self.r.reason(ReasoningCase(seeds={"virality_magic": 1.0}))

    def test_deterministic(self):
        case = ReasoningCase(seeds={"trust": 0.8, "identity": 0.6})
        a = self.r.reason(case)
        b = self.r.reason(case)
        self.assertEqual(a.activations, b.activations)
        self.assertEqual(a.dominant_nodes, b.dominant_nodes)

    def test_negative_edge_can_create_tension(self):
        edges = json.loads((ROOT / "data" / "edges.json").read_text())
        edges["edges"].append({
            "id":"test_inhibit",
            "source":"identity",
            "target":"social_transmission",
            "relation":"inhibits",
            "weight":-0.55,
            "confidence":"strong",
            "causal_status":"software_test_only",
            "mechanism":"synthetic inhibition used only to verify runtime conflict handling"
        })
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "edges.json"
            path.write_text(json.dumps(edges))
            r = NeuralReasoner(ROOT / "data" / "nodes.json", path)
            out = r.reason(ReasoningCase(seeds={
                "identity": 1.0,
                "valuation_emotion": 0.9
            }))
            self.assertGreater(out.support["social_transmission"], 0.05)
            self.assertGreater(out.inhibition["social_transmission"], 0.05)
            self.assertTrue(any(x["node"] == "social_transmission" for x in out.tensions))

if __name__ == "__main__":
    unittest.main()
