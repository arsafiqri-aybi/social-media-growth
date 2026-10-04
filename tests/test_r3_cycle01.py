from pathlib import Path
import json
import unittest
ROOT=Path(__file__).resolve().parents[1]
R=ROOT/"research"/"r3"/"cycle01"
N=ROOT/"research"/"r2"/"cycle01"/"l2-neuron-candidates.json"

class R3Cycle01Tests(unittest.TestCase):
    def setUp(self):
        self.edges=json.loads((R/"scientific-edges.json").read_text())["edges"]
        self.pairs=json.loads((R/"pair-coverage-matrix.json").read_text())["pairs"]
        self.nodes={n["id"]:n for n in json.loads(N.read_text())["neurons"]}

    def test_no_edge_contains_runtime_weight(self):
        self.assertTrue(all("weight" not in e and e["runtime_parameter_ref"] is None for e in self.edges))

    def test_all_28_core_pairs_audited(self):
        self.assertEqual(len(self.pairs),28)
        self.assertEqual(len({tuple(sorted((p["core_a"],p["core_b"]))) for p in self.pairs}),28)

    def test_accepted_edges_use_accepted_psych_nodes(self):
        for e in self.edges:
            if e["status"]!="accepted_edge": continue
            if e["source"] in self.nodes: self.assertEqual(self.nodes[e["source"]]["status"],"accepted")
            if e["target"] in self.nodes: self.assertEqual(self.nodes[e["target"]]["status"],"accepted")

    def test_non_system_edges_have_evidence(self):
        for e in self.edges:
            if e["status"]!="system_edge":
                self.assertTrue(e["evidence_claim_ids"])
                self.assertTrue(e["support_source_ids"])

    def test_arousal_edge_keeps_null_evidence(self):
        e=next(x for x in self.edges if x["id"]=="R3-E009")
        self.assertEqual(e["causal_status"],"mixed")
        self.assertTrue(e["contradiction_claim_ids"])
        self.assertTrue(e["contradiction_source_ids"])

    def test_system_edges_are_system_mechanical(self):
        for e in self.edges:
            if e["status"]=="system_edge": self.assertEqual(e["causal_status"],"system_mechanical")

if __name__=="__main__":
    unittest.main()
