from pathlib import Path
import json
import unittest

ROOT=Path(__file__).resolve().parents[1]
C=ROOT/"research"/"r2"/"cycle02"
N=ROOT/"research"/"r2"/"cycle01"/"l2-neuron-candidates.json"

class R2ClosureBatch04Tests(unittest.TestCase):
    def setUp(self):
        self.nodes=json.loads(N.read_text())["neurons"]
        self.decisions=json.loads((C/"batch04-closure-decisions.json").read_text())["decisions"]
        self.sources=json.loads((C/"batch04-source-registry.json").read_text())["sources"]
        self.claims=json.loads((C/"batch04-atomic-claims.json").read_text())["claims"]

    def test_exactly_34_candidate_records_received_closure_decisions(self):
        self.assertEqual(len(self.decisions),34)
        self.assertEqual(len({d["id"] for d in self.decisions}),34)

    def test_no_unresolved_candidates_remain(self):
        self.assertEqual([n["id"] for n in self.nodes if n["status"]=="candidate"],[])

    def test_batch04_itself_did_not_directly_accept_nodes(self):
        self.assertFalse(any(d["to_status"]=="accepted" for d in self.decisions))

    def test_every_nonactive_closure_has_target(self):
        for d in self.decisions:
            if d["to_status"]!="provisional":
                self.assertTrue(d["target"])

    def test_sources_resolve(self):
        ids={s["id"] for s in self.sources}
        unresolved=[(c["id"],sid) for c in self.claims for sid in c["source_ids"] if sid not in ids]
        self.assertEqual(unresolved,[])

    def test_active_nodes_cover_all_cores(self):
        cores={n["primary_core"] for n in self.nodes if n["status"] in {"provisional","accepted"}}
        self.assertEqual(cores,{"attention","curiosity","valuation_emotion","identity","trust","connection","social_transmission","reinforcement_habit"})

if __name__=="__main__":
    unittest.main()
