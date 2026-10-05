import unittest
from pathlib import Path

from measurement.global_measurement import GlobalMeasurementSystem


ROOT = Path(__file__).resolve().parents[1]


class GlobalMeasurementSystemTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.system = GlobalMeasurementSystem.from_repo_root(ROOT)

    def test_impression_never_seeds_latent(self):
        result = self.system.assess_observation({"type": "impression"})
        self.assertEqual(result.validity_class, "M0")
        self.assertFalse(result.can_seed_latent)
        self.assertEqual(result.stage, "exposure")

    def test_validated_measurement_requires_metadata(self):
        blocked = self.system.assess_observation(
            {"type": "validated_construct_measurement"}
        )
        self.assertFalse(blocked.can_seed_latent)
        self.assertFalse(blocked.requirements_met)

        allowed = self.system.assess_observation(
            {
                "type": "validated_construct_measurement",
                "instrument_id": "instrument-x",
                "target_construct": "trust",
                "domain_match": "documented",
                "population_match": "documented",
            }
        )
        self.assertTrue(allowed.can_seed_latent)
        self.assertTrue(allowed.requirements_met)

    def test_completion_proxy_does_not_identify_satisfaction(self):
        result = self.system.assess_proxy("completion_rate")
        self.assertFalse(result.can_auto_identify_latent)
        self.assertIn("not satisfaction", result.warning.lower())

    def test_platform_optimized_experiment_blocks_causal_claim(self):
        result = self.system.assess_experiment(
            {
                "experiment_id": "exp-1",
                "hypothesis_id": "h-1",
                "intervention": "creative-a-vs-b",
                "assignment_unit": "platform_campaign",
                "delivery_control": "platform_optimized",
                "randomization_documented": True,
                "audience_composition_checked": False,
                "platform_targeting_can_vary": True,
            }
        )
        self.assertFalse(result.bounded_causal_claim_allowed)
        self.assertEqual(result.causal_claim_status, "causal_claim_blocked_or_confounded")

    def test_controlled_randomized_design_can_pass_design_gate(self):
        result = self.system.assess_experiment(
            {
                "experiment_id": "exp-2",
                "hypothesis_id": "h-2",
                "intervention": "message-framing",
                "assignment_unit": "user",
                "delivery_control": "controlled",
                "randomization_documented": True,
                "audience_composition_checked": True,
                "platform_targeting_can_vary": False,
            }
        )
        self.assertTrue(result.bounded_causal_claim_allowed)
        self.assertEqual(
            result.causal_claim_status,
            "design_supports_bounded_causal_inference",
        )


if __name__ == "__main__":
    unittest.main()
