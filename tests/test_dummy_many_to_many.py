import json
import unittest
from pathlib import Path

from reasoning.global_runtime import GlobalGrowthReasoner


ROOT = Path(__file__).resolve().parents[1]


class DummyManyToManyReasoningTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.reasoner = GlobalGrowthReasoner.from_repo_root(ROOT)
        cls.payload = json.loads(
            (ROOT / "examples/dummy_many_to_many_case.json").read_text()
        )

    def test_dummy_case_activates_multiple_operational_cores(self):
        payload = self.payload
        out = self.reasoner.reason(payload["case"])
        expected = payload["expected_reasoning"]

        self.assertTrue(
            set(expected["matched_rules"]).issubset(set(out.matched_rules)),
            (expected["matched_rules"], out.matched_rules),
        )

        actual_cores = {x["core"] for x in out.bottleneck_candidates}
        self.assertTrue(
            set(expected["expected_bottleneck_cores"]).issubset(actual_cores),
            (expected["expected_bottleneck_cores"], sorted(actual_cores)),
        )

        self.assertTrue(
            set(expected["forbidden_overclaims"]).issubset(
                set(out.forbidden_inferences)
            ),
            (
                expected["forbidden_overclaims"],
                out.forbidden_inferences,
            ),
        )

        self.assertEqual(
            out.causal_ceiling,
            expected["causal_ceiling"],
        )

        # The same case must preserve plural competing explanations rather
        # than collapsing to a single-cause story.
        self.assertGreaterEqual(len(out.competing_explanations), 8)
        self.assertGreaterEqual(len(out.next_tests), 4)

        # Raw metrics/proxies must remain measurement evidence; they must not
        # create a canonical HPC conclusion when no explicit hpc_case exists.
        self.assertIsNone(out.hpc_reasoning)

    def test_dummy_case_is_deterministic(self):
        case = self.payload["case"]
        first = self.reasoner.reason(case).to_dict()
        second = self.reasoner.reason(case).to_dict()
        self.assertEqual(first, second)


if __name__ == "__main__":
    unittest.main()
