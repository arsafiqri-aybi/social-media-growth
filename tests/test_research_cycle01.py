from pathlib import Path
import json
import unittest

ROOT = Path(__file__).resolve().parents[1]
CYCLE = ROOT / "research" / "cycles" / "01"

class ResearchCycle01Tests(unittest.TestCase):
    def setUp(self):
        self.defs = json.loads((CYCLE/"core-definition-map.json").read_text())
        self.modules = json.loads((CYCLE/"candidate-modules.json").read_text())
        self.claims = json.loads((CYCLE/"atomic-claims.json").read_text())
        self.sources = json.loads((CYCLE/"source-registry.json").read_text())

    def test_all_eight_cores_have_definition_entry(self):
        cores = {x["core"] for x in self.defs["cores"]}
        self.assertEqual(cores, {
            "attention","curiosity","valuation_emotion","identity",
            "trust","connection","social_transmission","reinforcement_habit"
        })

    def test_all_eight_cores_have_candidate_modules(self):
        cores = {x["core"] for x in self.modules["modules"]}
        self.assertEqual(cores, {
            "attention","curiosity","valuation_emotion","identity",
            "trust","connection","social_transmission","reinforcement_habit"
        })

    def test_claim_sources_resolve(self):
        source_ids = {x["id"] for x in self.sources["sources"]}
        unresolved = []
        for claim in self.claims["claims"]:
            for sid in claim["source_ids"]:
                if sid not in source_ids:
                    unresolved.append((claim["id"], sid))
        self.assertEqual(unresolved, [])

    def test_each_core_has_multiple_sources(self):
        counts = {c:0 for c in {
            "attention","curiosity","valuation_emotion","identity",
            "trust","connection","social_transmission","reinforcement_habit"
        }}
        for src in self.sources["sources"]:
            for c in src["core"]:
                if c in counts:
                    counts[c] += 1
        self.assertTrue(all(v >= 2 for v in counts.values()), counts)

    def test_modules_are_candidates_not_accepted(self):
        self.assertEqual(self.modules["status"], "candidate_not_yet_accepted")

if __name__ == "__main__":
    unittest.main()
