import unittest
from pathlib import Path

from benchmarks.global_adversarial import GlobalAdversarialBenchmark


ROOT = Path(__file__).resolve().parents[1]


class GlobalAdversarialBenchmarkTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.benchmark = GlobalAdversarialBenchmark.from_repo_root(ROOT)

    def test_all_global_adversarial_scenarios_pass(self):
        results = self.benchmark.run_all()
        failures = {
            r.scenario_id: r.failures
            for r in results
            if not r.passed
        }
        self.assertFalse(failures, failures)

    def test_suite_has_minimum_failure_mode_breadth(self):
        scenarios = self.benchmark.suite["scenarios"]
        self.assertGreaterEqual(len(scenarios), 15)
        ids = {s["id"] for s in scenarios}
        self.assertEqual(len(ids), len(scenarios))

    def test_suite_includes_negative_hpc_boundary_case(self):
        scenario = next(
            s for s in self.benchmark.suite["scenarios"]
            if s["id"] == "GB-015"
        )
        self.assertEqual(scenario["expect_error"], "ValueError")


if __name__ == "__main__":
    unittest.main()
