from pathlib import Path
import unittest

from engine.hierarchical import HierarchicalReasoner
from engine.evidence import EvidenceRegistry

ROOT = Path(__file__).resolve().parents[1]

class HierarchicalTests(unittest.TestCase):
    def setUp(self):
        self.r = HierarchicalReasoner(
            ROOT/"data/nodes.json",
            ROOT/"data/edges.json",
            ROOT/"data/subnodes.json",
            ROOT/"data/subedges.json",
            ROOT/"research/evidence_registry.json",
            ROOT/"research/contradictions.json",
        )

    def test_arousal_propagates_to_sharing_and_core_transmission(self):
        out = self.r.reason(
            subnode_seeds={"emotion.arousal":0.9},
            context={"high_arousal":1.0},
        )
        self.assertGreater(out.subnode_result.activations["transmission.sharing"], 0.2)
        self.assertGreater(out.core_seed_rollup["social_transmission"], 0.2)

    def test_identity_norm_path_is_non_linear(self):
        out = self.r.reason(
            subnode_seeds={"identity.group_identity":0.9}
        )
        self.assertGreater(out.subnode_result.activations["identity.norm_salience"], 0.2)
        self.assertGreater(out.subnode_result.activations["transmission.identity_signaling"], 0.05)
        self.assertGreater(out.core_seed_rollup["identity"], 0.5)
        self.assertGreater(out.core_seed_rollup["social_transmission"], 0.05)

    def test_evidence_warnings_surface_for_active_identity_path(self):
        out = self.r.reason(subnode_seeds={"identity.group_identity":0.9})
        ids = {w["id"] for w in out.evidence_warnings}
        self.assertIn("C-ID-001", ids)

    def test_negative_measurement_can_reduce_rollup(self):
        baseline = self.r.reason(subnode_seeds={"curiosity.information_gain":0.7})
        reduced = self.r.reason(
            subnode_seeds={"curiosity.information_gain":0.7},
            negative_evidence={"curiosity.information_gain":0.8},
        )
        self.assertLess(reduced.core_seed_rollup["curiosity"], baseline.core_seed_rollup["curiosity"])

class EvidenceRegistryTests(unittest.TestCase):
    def test_trust_profile_contains_meta_analysis_and_warning(self):
        reg = EvidenceRegistry(
            ROOT/"research/evidence_registry.json",
            ROOT/"research/contradictions.json",
        )
        profile = reg.profile("e13")
        self.assertTrue(any(x["id"] == "EV-TRUST-001" for x in profile["evidence"]))
        self.assertTrue(any(x["id"] == "C-TRUST-001" for x in profile["contradictions"]))

if __name__ == "__main__":
    unittest.main()
