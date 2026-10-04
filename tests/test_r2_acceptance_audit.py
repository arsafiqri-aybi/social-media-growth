from pathlib import Path
import json
import unittest

ROOT=Path(__file__).resolve().parents[1]
A=ROOT/"research"/"r2"/"acceptance"
N=ROOT/"research"/"r2"/"cycle01"/"l2-neuron-candidates.json"

class R2AcceptanceAuditTests(unittest.TestCase):
    def setUp(self):
        self.nodes=json.loads(N.read_text())["neurons"]
        self.audit=json.loads((A/"node-audit.json").read_text())["audit"]
        self.gaps=json.loads((A/"gap-register.json").read_text())["gaps"]
        self.sat=json.loads((A/"saturation-audit.json").read_text())

    def test_expected_counts(self):
        self.assertEqual(sum(n["status"]=="accepted" for n in self.nodes),84)
        self.assertEqual(sum(n["status"]=="provisional" for n in self.nodes),12)
        self.assertEqual(sum(n["status"]=="candidate" for n in self.nodes),0)

    def test_accepted_pass_all_gates(self):
        by={a["node_id"]:a for a in self.audit}
        for n in self.nodes:
            if n["status"]=="accepted":
                g=by[n["id"]]["gates"]
                self.assertEqual(g["evidence_sufficiency"],"PASS")
                self.assertEqual(g["measurement_validity"],"PASS")
                self.assertEqual(g["non_redundancy"],"PASS")
                self.assertEqual(g["contradiction_boundary"],"PASS")
                self.assertEqual(g["transport_context"],"BOUNDED_PASS")
                self.assertEqual(g["provenance"],"PASS")

    def test_provisional_nodes_match_gap_register(self):
        p={n["id"] for n in self.nodes if n["status"]=="provisional"}
        g={x["node_id"] for x in self.gaps}
        self.assertEqual(p,g)
        self.assertEqual(len(g),12)

    def test_accepted_cover_all_cores(self):
        cores={n["primary_core"] for n in self.nodes if n["status"]=="accepted"}
        self.assertEqual(cores,{"attention","curiosity","valuation_emotion","identity","trust","connection","social_transmission","reinforcement_habit"})

    def test_saturation_is_scoped(self):
        self.assertEqual(self.sat["status"],"PASS_WITH_NONCRITICAL_EVIDENCE_GAPS")
        self.assertEqual(self.sat["system_saturation"],"NOT_CLAIMED")

if __name__=="__main__":
    unittest.main()
