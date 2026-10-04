from pathlib import Path
import json
import unittest

ROOT=Path(__file__).resolve().parents[1]
C=ROOT/"research"/"r2"/"cycle02"
N=ROOT/"research"/"r2"/"cycle01"/"l2-neuron-candidates.json"

class R2HardeningBatch02Tests(unittest.TestCase):
    def setUp(self):
        self.nodes=json.loads(N.read_text())["neurons"]
        self.promotions=json.loads((C/"batch02-promotion-decisions.json").read_text())["decisions"]
        self.sources=json.loads((C/"batch02-source-registry.json").read_text())["sources"]
        self.claims=json.loads((C/"batch02-atomic-claims.json").read_text())["claims"]

    def test_repo_has_116_l2_records(self):
        self.assertEqual(len(self.nodes),116)

    def test_batch02_promoted_all_eight_core_families_at_that_stage(self):
        by={n["id"]:n for n in self.nodes}
        cores={by[p["node_id"]]["primary_core"] for p in self.promotions}
        self.assertEqual(cores,{"attention","curiosity","valuation_emotion","identity","trust","connection","social_transmission","reinforcement_habit"})

    def test_batch02_decisions_were_provisional_promotions(self):
        self.assertTrue(all(p["decision"]=="PROMOTE_CANDIDATE_TO_PROVISIONAL" for p in self.promotions))
        self.assertTrue(all(p["new_status"]=="provisional" for p in self.promotions))

    def test_current_batch02_nodes_follow_valid_later_lifecycle(self):
        by={n["id"]:n for n in self.nodes}
        self.assertTrue(all(by[p["node_id"]]["status"] in {"provisional","accepted"} for p in self.promotions))
        for p in self.promotions:
            n=by[p["node_id"]]
            if n["status"]=="accepted":
                self.assertEqual(n.get("acceptance_gate"),"R2_ACCEPTANCE_V1_PASS")

    def test_claim_sources_resolve(self):
        ids={s["id"] for s in self.sources}
        unresolved=[]
        for c in self.claims:
            for sid in c["source_ids"]:
                if sid not in ids:
                    unresolved.append((c["id"],sid))
        self.assertEqual(unresolved,[])

    def test_arbitration_node_remains_noncanonical(self):
        by={n["id"]:n for n in self.nodes}
        self.assertEqual(by["RH-N11"]["status"],"contested_model")
        self.assertNotIn(by["RH-N11"]["status"],{"provisional","accepted"})

if __name__=="__main__":
    unittest.main()
