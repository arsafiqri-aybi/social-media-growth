from pathlib import Path
import json
import unittest

ROOT = Path(__file__).resolve().parents[1]
C = ROOT/"research"/"cycles"/"02"

EXPECTED = {
    "attention","curiosity","valuation_emotion","identity",
    "trust","connection","social_transmission","reinforcement_habit"
}

class ResearchCycle02Tests(unittest.TestCase):
    def setUp(self):
        self.sources = json.loads((C/"source-registry.json").read_text())
        self.claims = json.loads((C/"atomic-claims.json").read_text())
        self.measure = json.loads((C/"measurement-validity-map.json").read_text())
        self.context = json.loads((C/"culture-individual-differences.json").read_text())
        self.modules = json.loads((C/"candidate-modules-v2.json").read_text())
        self.split = json.loads((C/"split-risk-decision.json").read_text())

    def test_claim_sources_resolve(self):
        ids = {x["id"] for x in self.sources["sources"]}
        unresolved = []
        for c in self.claims["claims"]:
            for sid in c["source_ids"]:
                if sid not in ids:
                    unresolved.append((c["id"], sid))
        self.assertEqual(unresolved, [])

    def test_measurement_map_covers_all_cores(self):
        self.assertEqual({x["core"] for x in self.measure["cores"]}, EXPECTED)

    def test_context_map_covers_all_cores(self):
        self.assertEqual({x["core"] for x in self.context["cores"]}, EXPECTED)

    def test_v2_module_count_and_coverage(self):
        mods = self.modules["modules"]
        self.assertEqual(len(mods), 45)
        self.assertEqual({x["core"] for x in mods}, EXPECTED)
        self.assertEqual(len({x["id"] for x in mods}), len(mods))

    def test_eight_core_decision_preserved(self):
        self.assertEqual(self.split["decision"], "PRESERVE_8_L0_CORE_ANCHORS_WITH_COMPOSITE_SEMANTICS")
        self.assertEqual(len(self.split["core_semantics"]), 8)
        self.assertEqual(self.split["core_semantics"]["valuation_emotion"], "composite_family_no_unitary_latent_score")
        self.assertEqual(self.split["core_semantics"]["reinforcement_habit"], "composite_family_no_unitary_latent_score")

    def test_all_cores_have_disconfirmation_or_boundary_claim(self):
        by_core = {k:0 for k in EXPECTED}
        qualifying = {"contradiction","null","transport_generalization","measurement"}
        for c in self.claims["claims"]:
            if c["claim_type"] in qualifying:
                for t in c["target_ids"]:
                    if t in by_core:
                        by_core[t] += 1
        self.assertTrue(all(v >= 1 for v in by_core.values()), by_core)

if __name__ == "__main__":
    unittest.main()
