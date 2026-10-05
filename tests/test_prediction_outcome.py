import unittest
from pathlib import Path

from engine.canonical import CanonicalReasoner
from learning.prediction_outcome import PredictionOutcomeStore


ROOT = Path(__file__).resolve().parents[1]


class PredictionOutcomeLearningTests(unittest.TestCase):
    def setUp(self):
        self.store = PredictionOutcomeStore()

    def _register(self, prediction_id="p1"):
        return self.store.register_prediction(
            prediction_id=prediction_id,
            account_id="account-a",
            hypothesis_id="appeal-fit",
            intervention={"change": "thumbnail-message"},
            expected_metric_states={"selection": "up"},
            falsification_metric_states={"selection": "down"},
            context={"platform": "example"},
            source_rule_ids=["GR-001"],
        )

    def test_prediction_must_precede_outcome(self):
        with self.assertRaises(ValueError):
            self.store.record_outcome(
                prediction_id="missing",
                observed_metric_states={"selection": "up"},
            )

    def test_supported_prediction_is_account_local_only(self):
        self._register()
        outcome = self.store.record_outcome(
            prediction_id="p1",
            observed_metric_states={"selection": "up"},
        )
        self.assertEqual(outcome.evaluation, "supports_prediction")
        summary = self.store.local_belief_summary(
            account_id="account-a",
            hypothesis_id="appeal-fit",
        )
        self.assertEqual(summary["status"], "local_support_pattern")
        self.assertFalse(summary["scientific_evidence_mutation_allowed"])

    def test_falsification_is_retained(self):
        self._register()
        outcome = self.store.record_outcome(
            prediction_id="p1",
            observed_metric_states={"selection": "down"},
        )
        self.assertEqual(outcome.evaluation, "falsifies_prediction")

    def test_inconclusive_is_not_forced(self):
        self._register()
        outcome = self.store.record_outcome(
            prediction_id="p1",
            observed_metric_states={"selection": "flat"},
        )
        self.assertEqual(outcome.evaluation, "inconclusive")

    def test_mixed_local_evidence_stays_mixed(self):
        self._register("p1")
        self.store.register_prediction(
            prediction_id="p2",
            account_id="account-a",
            hypothesis_id="appeal-fit",
            intervention={"change": "opening-message"},
            expected_metric_states={"selection": "up"},
            falsification_metric_states={"selection": "down"},
        )
        self.store.record_outcome(
            prediction_id="p1",
            observed_metric_states={"selection": "up"},
        )
        self.store.record_outcome(
            prediction_id="p2",
            observed_metric_states={"selection": "down"},
        )
        summary = self.store.local_belief_summary(
            account_id="account-a",
            hypothesis_id="appeal-fit",
        )
        self.assertEqual(summary["status"], "mixed_local_evidence")
        self.assertEqual(summary["counts"]["supports_prediction"], 1)
        self.assertEqual(summary["counts"]["falsifies_prediction"], 1)

    def test_identical_expected_and_falsification_state_rejected(self):
        with self.assertRaises(ValueError):
            self.store.register_prediction(
                prediction_id="bad",
                account_id="account-a",
                hypothesis_id="h",
                intervention={"change": "x"},
                expected_metric_states={"return": "up"},
                falsification_metric_states={"return": "up"},
            )

    def test_learning_store_cannot_mutate_hpc_scientific_graph(self):
        reasoner = CanonicalReasoner.from_repo_root(ROOT)
        before = reasoner.scientific_snapshot()

        self._register()
        self.store.record_outcome(
            prediction_id="p1",
            observed_metric_states={"selection": "up"},
        )
        self.store.local_belief_summary(
            account_id="account-a",
            hypothesis_id="appeal-fit",
        )

        after = reasoner.scientific_snapshot()
        self.assertEqual(before, after)


if __name__ == "__main__":
    unittest.main()
