from pathlib import Path
import unittest

from audits import FinalTenTenAuditor

ROOT=Path(__file__).resolve().parents[1]


class FinalTenTenAuditTests(unittest.TestCase):
    def test_nineteen_internal_gates_pass_and_ci_gate_is_explicitly_pending(self):
        out=FinalTenTenAuditor(ROOT).run()
        by={g.id:g for g in out.gates}
        self.assertEqual(len(out.gates),20)
        self.assertEqual(out.critical_failures,[])
        self.assertEqual(out.pass_count_without_external_ci,19)
        self.assertEqual(out.pending_external_ci_count,1)
        self.assertEqual(by["G20"].status,"PENDING_EXTERNAL_CI")

    def test_bounded_knowledge_is_not_silently_promoted(self):
        out=FinalTenTenAuditor(ROOT).run()
        by={g.id:g for g in out.gates}
        self.assertEqual(by["G14"].status,"PASS")
        self.assertTrue(by["G14"].limitations)


if __name__=="__main__":
    unittest.main()
