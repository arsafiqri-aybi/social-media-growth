from pathlib import Path
import unittest

from engine.canonical import CanonicalReasoner, CanonicalReasoningCase
from measurement import CanonicalMeasurementMapper, OperationalCalibrationStore

ROOT=Path(__file__).resolve().parents[1]


class CanonicalMeasurementV2Tests(unittest.TestCase):
    def setUp(self):
        self.m=CanonicalMeasurementMapper.from_repo_root(ROOT)

    def test_share_rate_seeds_only_observed_sharing_action(self):
        out=self.m.map({"share_rate":{"value":0.04,"baseline":0.02}})
        self.assertIn("ST-N01",out.reasoning_seeds)
        self.assertNotIn("ST-N07",out.reasoning_seeds)
        self.assertEqual(out.reasoning_seeds["ST-N01"]["basis"],"structured_observation")
        self.assertTrue(any(x["candidate_node_id"]=="ST-N07" for x in out.candidate_explanations))

    def test_returning_viewer_never_auto_diagnoses_habit_or_connection(self):
        out=self.m.map({"returning_viewer_rate":{"value":0.30,"baseline":0.20}})
        self.assertEqual(out.reasoning_seeds,{})
        ids={x["candidate_node_id"] for x in out.candidate_explanations}
        self.assertIn("RH-N06",ids)
        self.assertIn("CON-N04",ids)
        self.assertTrue(any("does not prove habit" in w for w in out.warnings))

    def test_credibility_survey_requires_validated_instrument_and_domain_match(self):
        blocked=self.m.map({
            "source_credibility_survey":{
                "direction":"up",
                "validated_instrument":False,
                "domain_match":True,
                "dimension":"trustworthiness",
            }
        })
        self.assertNotIn("TR-N03",blocked.reasoning_seeds)

        allowed=self.m.map({
            "source_credibility_survey":{
                "direction":"up",
                "validated_instrument":True,
                "domain_match":True,
                "dimension":"trustworthiness",
            }
        })
        self.assertEqual(allowed.reasoning_seeds["TR-N03"]["basis"],"direct_measurement")

    def test_profile_visit_enters_reasoner_as_proxy_hypothesis(self):
        out=self.m.map({"profile_visit_rate":{"value":0.05,"baseline":0.03}})
        self.assertEqual(out.reasoning_seeds["CUR-N10"]["basis"],"proxy_hypothesis")

        r=CanonicalReasoner.from_repo_root(ROOT)
        rr=r.reason(CanonicalReasoningCase(
            seeds=out.reasoning_seeds,
            targets=["VE-N01"],
            max_depth=3,
        ))
        for h in rr.hypotheses:
            if h.source_seed=="CUR-N10":
                self.assertEqual(h.path_status,"provisional_path")
                self.assertEqual(h.causal_ceiling,"hypothesis_only")

    def test_completion_rate_is_retained_without_latent_seed(self):
        out=self.m.map({"completion_rate":{"value":0.70,"baseline":0.50}})
        self.assertEqual(out.reasoning_seeds,{})
        self.assertTrue(any(e.proxy_id=="completion_rate" and not e.can_seed_reasoner for e in out.evidence))

    def test_lower_share_rate_does_not_become_negative_latent_state(self):
        out=self.m.map({"share_rate":{"value":0.01,"baseline":0.03}})
        self.assertEqual(out.reasoning_seeds,{})

    def test_social_feedback_event_maps_to_system_event(self):
        out=self.m.map({"social_feedback_count":{"value":12}})
        self.assertEqual(out.reasoning_seeds["CTX-SOCIAL-FEEDBACK"]["basis"],"external_event")

    def test_unknown_metric_is_rejected(self):
        with self.assertRaises(ValueError):
            self.m.map({"dopamine_score":{"value":1}})


class OperationalCalibrationTests(unittest.TestCase):
    def test_insufficient_data_is_not_overinterpreted(self):
        c=OperationalCalibrationStore()
        c.record("1",{"share_rate":0.02},{"next_share_rate":0.03})
        s=c.summarize("share_rate","next_share_rate",min_records=3)
        self.assertEqual(s.status,"insufficient_data")
        self.assertIsNone(s.pearson_r)

    def test_account_local_association_is_descriptive_only(self):
        c=OperationalCalibrationStore()
        for i in range(1,6):
            c.record(str(i),{"save_rate":float(i)},{"next_completion":float(i*2)})
        s=c.summarize("save_rate","next_completion",min_records=5)
        self.assertEqual(s.status,"descriptive_association_only")
        self.assertEqual(s.association_direction,"positive")
        self.assertFalse(s.scientific_effect_claim_allowed)
        self.assertFalse(s.latent_state_claim_allowed)

    def test_calibration_export_cannot_mutate_scientific_graph(self):
        c=OperationalCalibrationStore()
        c.record("1",{"share_rate":1.0},{"next_share_rate":2.0})
        e=c.export()
        self.assertFalse(e["scientific_graph_mutation_allowed"])
        self.assertFalse(e["latent_state_inference_allowed"])


if __name__=="__main__":
    unittest.main()
