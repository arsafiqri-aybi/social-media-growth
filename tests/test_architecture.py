from pathlib import Path
import json
import unittest

from scripts.validate_architecture import validate_architecture

ROOT = Path(__file__).resolve().parents[1]

class ArchitectureContractTests(unittest.TestCase):
    def setUp(self):
        self.arch = json.loads((ROOT/"architecture/ontology.json").read_text())

    def test_architecture_validator_passes(self):
        self.assertEqual(validate_architecture(), [])

    def test_exact_current_core_anchor_count(self):
        self.assertEqual(len(self.arch["core_anchors"]), 8)

    def test_hierarchy_and_graph_are_separated(self):
        self.assertEqual(
            {x["kind"] for x in self.arch["layers"]},
            {"core","module","neuron","micro_neuron"}
        )
        self.assertIn("moderates", self.arch["edge_relation_vocabulary"])
        self.assertIn("competes_with", self.arch["edge_relation_vocabulary"])

    def test_uncertainty_is_multichannel(self):
        required = {"epistemic","construct","measurement","transport_context","runtime_model"}
        self.assertTrue(required.issubset(set(self.arch["uncertainty_channels"])))

    def test_runtime_weight_is_not_effect_size(self):
        self.assertIn("No empirical effect size", self.arch["runtime_rule"])

if __name__ == "__main__":
    unittest.main()
