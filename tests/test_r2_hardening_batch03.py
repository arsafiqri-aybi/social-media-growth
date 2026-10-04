from pathlib import Path
import json
import unittest

ROOT=Path(__file__).resolve().parents[1]
C=ROOT/"research"/"r2"/"cycle02"
N=ROOT/"research"/"r2"/"cycle01"/"l2-neuron-candidates.json"

class R2HardeningBatch03Tests(unittest.TestCase):
    def setUp(self):
        self.nodes=json.loads(N.read_text())["neurons"]
        self.promotions=json.loads((C/"batch03-promotion-decisions.json").read_text())["decisions"]
        self.sources=json.loads((C/"batch03-source-registry.json").read_text())["sources"]
        self.claims=json.loads((C/"batch03-atomic-claims.json").read_text())["claims"]
        self.holds=json.loads((C/"batch03-holds.json").read_text())["holds"]

    def test_total_l2_records_stay_constant(self):
        self.assertEqual(len(self.nodes),116)

    def test_batch03_promotions_remain_nonaccepted(self):
        by={n["id"]:n for n in self.nodes}
        self.assertTrue(all(by[p["node_id"]]["status"]!="accepted" for p in self.promotions))

    def test_no_node_is_accepted_yet(self):
        self.assertFalse(any(n["status"]=="accepted" for n in self.nodes))

    def test_sources_resolve(self):
        ids={s["id"] for s in self.sources}
        unresolved=[(c["id"],sid) for c in self.claims for sid in c["source_ids"] if sid not in ids]
        self.assertEqual(unresolved,[])

    def test_batch03_holds_were_not_silently_accepted(self):
        by={n["id"]:n for n in self.nodes}
        held=[nid for h in self.holds for nid in h["nodes"]]
        self.assertTrue(all(by[nid]["status"]!="accepted" for nid in held))

    def test_batch03_promoted_nodes_span_all_eight_cores(self):
        by={n["id"]:n for n in self.nodes}
        cores={by[p["node_id"]]["primary_core"] for p in self.promotions}
        self.assertEqual(cores,{"attention","curiosity","valuation_emotion","identity","trust","connection","social_transmission","reinforcement_habit"})

if __name__=="__main__":
    unittest.main()
