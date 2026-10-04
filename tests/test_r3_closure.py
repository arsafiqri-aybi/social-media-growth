from pathlib import Path
import json
import unittest

ROOT=Path(__file__).resolve().parents[1]
R=ROOT/"research"/"r3"/"cycle03"

class R3ClosureTests(unittest.TestCase):
    def setUp(self):
        self.edges=json.loads((R/"scientific-edges.json").read_text())["edges"]
        self.pairs=json.loads((R/"pair-coverage-matrix.json").read_text())["pairs"]
        self.audit=json.loads((R/"edge-audit.json").read_text())["audit"]
        self.sat=json.loads((R/"saturation-audit.json").read_text())
        self.loops=json.loads((R/"feedback-loops.json").read_text())["loops"]

    def test_expected_edge_status_counts(self):
        self.assertEqual(len(self.edges),26)
        self.assertEqual(sum(e["status"]=="accepted_edge" for e in self.edges),14)
        self.assertEqual(sum(e["status"]=="provisional_edge" for e in self.edges),8)
        self.assertEqual(sum(e["status"]=="system_edge" for e in self.edges),4)

    def test_no_runtime_weights(self):
        self.assertTrue(all("weight" not in e and e["runtime_parameter_ref"] is None for e in self.edges))

    def test_all_pairs_audited(self):
        self.assertEqual(len(self.pairs),28)

    def test_social_feedback_loop_is_complete_and_unweighted(self):
        loop=next(l for l in self.loops if l["id"]=="R3-L05")
        self.assertEqual(loop["status"],"supported_bounded_loop")
        self.assertIsNone(loop["missing_return_link"])
        self.assertEqual(loop["strength_claim"],"NOT_ESTIMATED")

    def test_no_critical_connection_gap(self):
        self.assertEqual(self.sat["unresolved_critical_gaps"],0)
        self.assertEqual(self.sat["status"],"PASS_WITH_NONCRITICAL_BOUNDED_GAPS")
        self.assertEqual(self.sat["system_saturation"],"NOT_CLAIMED")

    def test_provisional_edges_have_explicit_audit_gap(self):
        by={a["edge_id"]:a for a in self.audit}
        for e in self.edges:
            if e["status"]=="provisional_edge":
                self.assertEqual(by[e["id"]]["decision"],"RETAIN_PROVISIONAL")
                self.assertTrue(by[e["id"]]["gap"])

if __name__=="__main__":
    unittest.main()
