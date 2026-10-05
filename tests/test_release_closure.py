from pathlib import Path
import json
import unittest

ROOT=Path(__file__).resolve().parents[1]

class HPCV1ReleaseClosureTests(unittest.TestCase):
    def setUp(self):
        self.contract=json.loads((ROOT/"contracts/hpc-10x-execution-contract.json").read_text())
        self.report=json.loads((ROOT/"audits/final-10-10-report.json").read_text())

    def test_contract_is_closed_with_all_outputs_present(self):
        self.assertEqual(self.contract["status"],"COMPLETE_WITH_BOUNDED_NONCRITICAL_GAPS")
        self.assertTrue(all(o["state"]=="PRESENT" for o in self.contract["required_outputs"]))

    def test_all_twenty_gates_are_pass(self):
        self.assertEqual(len(self.contract["gates"]),20)
        self.assertTrue(all(g["status"]=="PASS" for g in self.contract["gates"]))
        self.assertEqual(self.report["quality_gate_score"],"20/20")

    def test_bounded_knowledge_remains_explicit(self):
        b=self.report["bounded_noncritical_gaps"]
        self.assertEqual(b["provisional_l2_nodes"]["count"],12)
        self.assertEqual(b["bounded_provisional_modules"]["count"],4)
        self.assertEqual(b["deferred_research_modules"]["count"],1)
        self.assertEqual(b["provisional_scientific_edges"]["count"],8)

    def test_release_does_not_claim_universal_predictive_validity(self):
        joined=" ".join(self.report["nonclaims"]).lower()
        self.assertIn("not evidence of real-world predictive validity",joined)
        self.assertIn("not a claim of universal",joined)

if __name__=="__main__":
    unittest.main()
