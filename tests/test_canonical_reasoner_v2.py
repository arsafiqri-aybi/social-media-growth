from pathlib import Path
import unittest

from engine.canonical import (
    CanonicalReasoner,
    CanonicalReasoningCase,
    OperationalFeedbackStore,
    summarize_canonical,
)

ROOT=Path(__file__).resolve().parents[1]


class CanonicalReasonerV2Tests(unittest.TestCase):
    def setUp(self):
        self.r=CanonicalReasoner.from_repo_root(ROOT)

    def test_accepted_mechanistic_path_is_traversed_without_numeric_weights(self):
        out=self.r.reason(CanonicalReasoningCase(
            seeds={"ID-N02":"structured_observation"},
            targets=["VE-N01"],
        ))
        c=out.conclusions["VE-N01"]
        self.assertEqual(c.status,"bounded_support")
        self.assertEqual(c.selected_path_edge_ids,["R3-E003"])
        self.assertFalse(c.strong_causal_claim_allowed)
        self.assertEqual(c.causal_ceiling,"mechanistic_noncausal")

    def test_provisional_mixed_edge_caps_claim(self):
        out=self.r.reason(CanonicalReasoningCase(
            seeds={"VE-N12":"direct_measurement"},
            targets=["ST-N02"],
        ))
        c=out.conclusions["ST-N02"]
        self.assertIn(c.status,{"provisional_hypothesis","contested_or_mixed"})
        self.assertEqual(c.causal_ceiling,"hypothesis_only")
        self.assertFalse(c.strong_causal_claim_allowed)
        h=next(h for h in out.hypotheses if h.target=="ST-N02")
        self.assertIn("SRC-ST-003",h.contradiction_source_ids)

    def test_system_edge_reports_opportunity_but_does_not_cascade(self):
        out=self.r.reason(CanonicalReasoningCase(
            seeds={"ST-N01":"structured_observation"},
            targets=["RH-N02"],
            max_depth=3,
        ))
        self.assertEqual(out.conclusions["RH-N02"].status,"unsupported_in_current_graph")
        self.assertTrue(any(x.edge_id=="R3-E026" for x in out.opportunities))

    def test_observed_social_feedback_can_enter_reward_learning_path(self):
        out=self.r.reason(CanonicalReasoningCase(
            seeds={"CTX-SOCIAL-FEEDBACK":"external_event"},
            targets=["RH-N02"],
            max_depth=2,
        ))
        c=out.conclusions["RH-N02"]
        self.assertEqual(c.status,"bounded_support")
        self.assertEqual(c.causal_ceiling,"causal_bounded")
        self.assertTrue(c.strong_causal_claim_allowed)
        self.assertEqual(c.selected_path_edge_ids,["R3-E024"])

    def test_correlational_edge_cannot_become_causal_claim(self):
        out=self.r.reason(CanonicalReasoningCase(
            seeds={"TR-N03":"validated_observation"},
            targets=["CON-N04"],
        ))
        c=out.conclusions["CON-N04"]
        self.assertEqual(c.status,"bounded_support")
        self.assertEqual(c.causal_ceiling,"association_only")
        self.assertFalse(c.strong_causal_claim_allowed)

    def test_missing_context_is_qualification_not_numeric_penalty(self):
        noctx=self.r.reason(CanonicalReasoningCase(
            seeds={"ID-N08":"structured_observation"},
            targets=["ST-N07"],
        ))
        ctx=self.r.reason(CanonicalReasoningCase(
            seeds={"ID-N08":"structured_observation"},
            context={"CTX-AUDIENCE-COMPOSITION":{"observed":True}},
            targets=["ST-N07"],
        ))
        h1=next(h for h in noctx.hypotheses if h.target=="ST-N07")
        h2=next(h for h in ctx.hypotheses if h.target=="ST-N07")
        self.assertIn("CTX-AUDIENCE-COMPOSITION",h1.unresolved_modifiers)
        self.assertIn("CTX-AUDIENCE-COMPOSITION",h2.observed_modifiers)
        self.assertEqual(h1.operational_priority,h2.operational_priority)

    def test_raw_numeric_activation_is_rejected(self):
        with self.assertRaises(ValueError):
            self.r.reason(CanonicalReasoningCase(seeds={"ID-N02":0.8}))

    def test_raw_platform_proxy_is_rejected(self):
        with self.assertRaises(ValueError):
            self.r.reason(CanonicalReasoningCase(seeds={"share_rate":"structured_observation"}))

    def test_noncanonical_node_is_rejected(self):
        with self.assertRaises(ValueError):
            self.r.reason(CanonicalReasoningCase(seeds={"RH-N11":"user_hypothesis"}))

    def test_deterministic(self):
        case=CanonicalReasoningCase(
            seeds={"CTX-SOCIAL-FEEDBACK":"external_event","ID-N02":"structured_observation"},
            max_depth=3,
        )
        self.assertEqual(self.r.reason(case).to_dict(),self.r.reason(case).to_dict())

    def test_summary_exposes_causal_ceiling(self):
        out=self.r.reason(CanonicalReasoningCase(
            seeds={"TR-N03":"validated_observation"},
            targets=["CON-N04"],
        ))
        s=summarize_canonical(out)
        self.assertIn("association_only",s)

    def test_feedback_store_does_not_mutate_scientific_graph(self):
        before=self.r.scientific_snapshot()
        store=OperationalFeedbackStore()
        store.record("case-1",{"share_rate":{"value":0.04}})
        after=self.r.scientific_snapshot()
        self.assertEqual(before,after)
        self.assertEqual(store.snapshot()[0]["scope"],"account_local_operational_evidence")


if __name__=="__main__":
    unittest.main()
