from pathlib import Path
import unittest

from measurement import MeasurementMapper

ROOT = Path(__file__).resolve().parents[1]

class MeasurementTests(unittest.TestCase):
    def setUp(self):
        self.mapper = MeasurementMapper(ROOT / "measurement" / "proxies.json")

    def test_share_rate_maps_mostly_to_observed_sharing(self):
        out = self.mapper.map({"share_rate":{"value":0.04,"baseline":0.02}})
        self.assertIn("transmission.sharing", out.subnode_seeds)
        self.assertGreater(
            out.subnode_seeds["transmission.sharing"],
            out.subnode_seeds.get("transmission.identity_signaling", 0)
        )

    def test_returning_viewer_does_not_equal_habit(self):
        out = self.mapper.map({"returning_viewer_rate":{"value":0.30,"baseline":0.20}})
        self.assertIn("habit.context_association", out.subnode_seeds)
        self.assertTrue(any("does not prove habit" in w for w in out.warnings))

    def test_below_baseline_becomes_negative_evidence(self):
        out = self.mapper.map({"completion_rate":{"value":0.20,"baseline":0.40}})
        self.assertTrue(out.negative_evidence)
        self.assertFalse(out.subnode_seeds)

    def test_unknown_proxy_rejected(self):
        with self.assertRaises(ValueError):
            self.mapper.map({"dopamine_score":{"normalized":1.0}})

if __name__ == "__main__":
    unittest.main()
