from pathlib import Path
import json
import unittest
ROOT=Path(__file__).resolve().parents[1]
R=ROOT/"research"/"r3"/"cycle02"
N=ROOT/"research"/"r2"/"cycle01"/"l2-neuron-candidates.json"

class R3Cycle02Tests(unittest.TestCase):
    def setUp(self):
        self.edges=json.loads((R/"scientific-edges.json").read_text())["edges"]
        self.pairs=json.loads((R/"pair-coverage-matrix.json").read_text())["pairs"]
        self.non_edges=json.loads((R/"non-edge-decisions.json").read_text())["decisions"]
        self.nodes={n["id"]:n for n in json.loads(N.read_text())["neurons"]}

    def test_edge_count_and_no_runtime_weights(self):
        self.assertEqual(len(self.edges),23)
        self.assertTrue(all("weight" not in e and e["runtime_parameter_ref"] is None for e in self.edges))

    def test_all_28_pairs_remain_audited(self):
        self.assertEqual(len(self.pairs),28)
        self.assertEqual(len({tuple(sorted((p["core_a"],p["core_b"]))) for p in self.pairs}),28)

    def test_accepted_edges_use_accepted_nodes(self):
        for e in self.edges:
            if e["status"]!="accepted_edge": continue
            if e["source"] in self.nodes: self.assertEqual(self.nodes[e["source"]]["status"],"accepted")
            if e["target"] in self.nodes: self.assertEqual(self.nodes[e["target"]]["status"],"accepted")

    def test_curiosity_reinforcement_edge_is_accepted_but_not_habit_claim(self):
        e=next(e for e in self.edges if e["id"]=="R3-E022")
        self.assertEqual(e["status"],"accepted_edge")
        self.assertIn("not synonymous with habit", " ".join(e["boundary_conditions"]).lower())

    def test_expertise_psr_edge_preserves_conflict(self):
        e=next(e for e in self.edges if e["id"]=="R3-E023")
        self.assertEqual(e["status"],"provisional_edge")
        self.assertEqual(e["causal_status"],"mixed")
        self.assertTrue(e["contradiction_source_ids"])

    def test_construct_mismatch_edges_are_explicitly_rejected(self):
        ids={d["id"] for d in self.non_edges}
        self.assertIn("R3C2-NE01",ids)
        self.assertIn("R3C2-NE02",ids)

    def test_trust_to_psr_is_association_not_causal_claim(self):
        e=next(e for e in self.edges if e["id"]=="R3-E013")
        self.assertEqual(e["status"],"accepted_edge")
        self.assertEqual(e["causal_status"],"correlational")

if __name__=="__main__":
    unittest.main()
