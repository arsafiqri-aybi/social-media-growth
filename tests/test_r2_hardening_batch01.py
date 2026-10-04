from pathlib import Path
import json
import unittest

ROOT=Path(__file__).resolve().parents[1]
C=ROOT/"research"/"r2"/"cycle02"
N=ROOT/"research"/"r2"/"cycle01"/"l2-neuron-candidates.json"

class R2HardeningBatch01Tests(unittest.TestCase):
    def setUp(self):
        self.decisions=json.loads((C/"promotion-decisions.json").read_text())["decisions"]
        self.claims=json.loads((C/"atomic-claims.json").read_text())["claims"]
        self.sources=json.loads((C/"source-registry.json").read_text())["sources"]
        self.nodes=json.loads(N.read_text())["neurons"]

    def test_all_eight_cores_are_represented_in_promoted_nodes(self):
        by_id={n["id"]:n for n in self.nodes}
        cores={by_id[d["node_id"]]["primary_core"] for d in self.decisions}
        self.assertEqual(cores,{"attention","curiosity","valuation_emotion","identity","trust","connection","social_transmission","reinforcement_habit"})

    def test_promoted_nodes_are_provisional_not_accepted(self):
        by_id={n["id"]:n for n in self.nodes}
        self.assertTrue(all(by_id[d["node_id"]]["status"]=="provisional" for d in self.decisions))
        self.assertFalse(any(n["status"]=="accepted" for n in self.nodes))

    def test_hardening_claim_sources_resolve(self):
        source_ids={s["id"] for s in self.sources}
        unresolved=[]
        for c in self.claims:
            for sid in c["source_ids"]:
                if sid not in source_ids: unresolved.append((c["id"],sid))
        self.assertEqual(unresolved,[])

    def test_each_promotion_has_measurement_and_boundary(self):
        self.assertTrue(all(d["measurement_route"] and d["boundary"] for d in self.decisions))

if __name__=="__main__":
    unittest.main()
