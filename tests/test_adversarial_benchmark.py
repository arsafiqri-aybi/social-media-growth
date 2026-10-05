from pathlib import Path
import unittest

from benchmarks import AdversarialBenchmark

ROOT=Path(__file__).resolve().parents[1]


class AdversarialBenchmarkTests(unittest.TestCase):
    def test_all_adversarial_scenarios_pass(self):
        report=AdversarialBenchmark(ROOT).run()
        failures=[r for r in report.results if not r.passed]
        self.assertEqual(failures,[],msg="\n".join(f"{x.id}: {x.message}" for x in failures))
        self.assertEqual(report.passed,report.total)
        self.assertGreaterEqual(report.total,30)

    def test_suite_spans_multiple_failure_classes(self):
        bench=AdversarialBenchmark(ROOT)
        cats={s["category"] for s in bench.scenarios}
        self.assertTrue({"measurement","reasoning","calibration","structural"}.issubset(cats))


if __name__=="__main__":
    unittest.main()
