from pathlib import Path
import json
import unittest

ROOT=Path(__file__).resolve().parents[1]
C=ROOT/"research"/"r2"/"cycle01"

CORES={"attention","curiosity","valuation_emotion","identity","trust","connection","social_transmission","reinforcement_habit"}

class R2Cycle01Tests(unittest.TestCase):
    def setUp(self):
        self.modules=json.loads((C/"module-specs.json").read_text())["modules"]
        self.neurons=json.loads((C/"l2-neuron-candidates.json").read_text())["neurons"]
        self.migration=json.loads((C/"legacy-neuron-migration.json").read_text())["migrations"]
        self.connectors=json.loads((C/"connector-candidates.json").read_text())["connectors"]

    def test_all_45_modules_specified(self):
        self.assertEqual(len(self.modules),45)
        self.assertEqual(len({m["id"] for m in self.modules}),45)

    def test_all_modules_have_boundaries_and_claims(self):
        for m in self.modules:
            self.assertTrue(m["definition"])
            self.assertTrue(m["claim_ids"])
            self.assertTrue(m["boundary_conditions"])

    def test_l2_ids_unique_and_parents_resolve(self):
        mids={m["id"] for m in self.modules}
        ids=[n["id"] for n in self.neurons]
        self.assertEqual(len(ids),len(set(ids)))
        self.assertTrue(all(n["parent_id"] in mids for n in self.neurons))

    def test_all_cores_have_l2_candidates(self):
        self.assertEqual({n["primary_core"] for n in self.neurons},CORES)

    def test_no_l2_is_prematurely_accepted(self):
        self.assertTrue(all(n["status"]=="candidate" for n in self.neurons))

    def test_all_29_legacy_nodes_have_one_migration(self):
        self.assertEqual(len(self.migration),29)
        self.assertEqual(len({m["legacy_id"] for m in self.migration}),29)

    def test_required_connector_candidates_exist(self):
        ids={c["id"] for c in self.connectors}
        required={"CTX-PERCEIVED-SIMILARITY","CTX-RELATIONSHIP-RECIPROCITY","CTX-COMMUNICATION-MEDIUM","CTX-CULTURAL-MEANING-SYSTEM"}
        self.assertTrue(required.issubset(ids))

if __name__=="__main__":
    unittest.main()
