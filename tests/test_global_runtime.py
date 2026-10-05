import unittest
from pathlib import Path

from reasoning.global_runtime import GlobalGrowthReasoner


ROOT = Path(__file__).resolve().parents[1]


class GlobalGrowthReasonerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.reasoner = GlobalGrowthReasoner.from_repo_root(ROOT)

    def test_high_exposure_low_selection_does_not_become_algorithm_failure(self):
        out = self.reasoner.reason({
            "goal": {"objective": "qualified_growth"},
            "metric_states": {"exposure": "high", "selection": "low"},
            "observations": [{"type": "impression"}],
            "proxies": ["selection_rate"],
        })
        self.assertIn("GR-001", out.matched_rules)
        self.assertIn("algorithm_failure", out.forbidden_inferences)
        cores = {x["core"] for x in out.bottleneck_candidates}
        self.assertEqual(cores, {"audience_value", "communication_content"})
        self.assertEqual(out.causal_ceiling, "observational_diagnosis_only")
        self.assertIsNone(out.hpc_reasoning)

    def test_high_completion_low_return_never_claims_habit(self):
        out = self.reasoner.reason({
            "goal": {"objective": "retained_audience"},
            "metric_states": {"completion": "high", "return": "low"},
            "proxies": ["completion_rate", "return_rate"],
        })
        self.assertIn("GR-003", out.matched_rules)
        self.assertIn("no_habit", out.forbidden_inferences)
        self.assertNotIn("habit_established", out.forbidden_inferences)

    def test_return_up_preserves_multiple_explanations(self):
        out = self.reasoner.reason({
            "goal": {"objective": "retention"},
            "metric_states": {"return": "up"},
            "proxies": ["return_rate"],
        })
        self.assertIn("GR-005", out.matched_rules)
        self.assertIn("habit_candidate", out.competing_explanations)
        self.assertIn("platform_rediscovery", out.competing_explanations)
        self.assertIn("habit_established", out.forbidden_inferences)

    def test_platform_optimized_experiment_caps_causal_ceiling(self):
        out = self.reasoner.reason({
            "goal": {"objective": "creative_learning"},
            "metric_states": {"selection": "high", "continuation": "low"},
            "experiment": {
                "experiment_id": "exp-platform",
                "hypothesis_id": "h-creative",
                "intervention": "creative-a-vs-b",
                "assignment_unit": "platform_campaign",
                "delivery_control": "platform_optimized",
                "randomization_documented": True,
                "audience_composition_checked": False,
                "platform_targeting_can_vary": True,
            },
        })
        self.assertEqual(out.causal_ceiling, "confounded_or_noncausal_design")
        self.assertFalse(
            out.experiment_assessment["bounded_causal_claim_allowed"]
        )

    def test_optional_hpc_case_uses_canonical_reasoner(self):
        out = self.reasoner.reason({
            "goal": {"objective": "understand_trust_path"},
            "metric_states": {},
            "hpc_case": {
                "seeds": {"TR-N03": "validated_observation"},
                "targets": ["CON-N04"],
                "max_depth": 2,
            },
        })
        self.assertIsNotNone(out.hpc_reasoning)
        self.assertIn("CON-N04", out.hpc_reasoning["conclusions"])

    def test_raw_platform_metric_cannot_enter_hpc_case(self):
        with self.assertRaises(ValueError):
            self.reasoner.reason({
                "goal": {"objective": "test_guardrail"},
                "metric_states": {"shares": "up"},
                "hpc_case": {
                    "seeds": {"share_rate": "structured_observation"}
                },
            })

    def test_deterministic(self):
        case = {
            "goal": {"objective": "growth"},
            "metric_states": {
                "exposure": "up",
                "likes": "up",
                "conversion": "down",
                "nonfollower_reach": "up",
                "continuation": "down",
            },
            "proxies": ["conversion_rate", "continuation_rate"],
        }
        self.assertEqual(
            self.reasoner.reason(case).to_dict(),
            self.reasoner.reason(case).to_dict(),
        )

    def test_unknown_metric_state_key_rejected(self):
        with self.assertRaises(ValueError):
            self.reasoner.reason({
                "goal": {"objective": "growth"},
                "metric_states": {"magic_metric": "high"},
            })


if __name__ == "__main__":
    unittest.main()
