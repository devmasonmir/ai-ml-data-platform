import math
import unittest

from src.features.feature_pipeline import compute_user_features
from src.monitoring.drift_detector import FeatureDriftDetector
from src.rag.embedding_preparer import RAGDatasetPreparer


class FeaturePipelineTests(unittest.TestCase):
    def test_aggregates_transactions_by_user(self):
        transactions = [
            {"user_id": "u1", "amount": 100.0},
            {"user_id": "u1", "amount": 200.0},
            {"user_id": "u2", "amount": 600.0},
        ]

        features = compute_user_features(transactions)

        self.assertEqual(
            features,
            [
                {
                    "user_id": "u1",
                    "avg_order_value_30d": 150.0,
                    "total_transactions_30d": 2,
                    "high_value_customer": False,
                },
                {
                    "user_id": "u2",
                    "avg_order_value_30d": 600.0,
                    "total_transactions_30d": 1,
                    "high_value_customer": True,
                },
            ],
        )

    def test_rejects_non_list_input(self):
        with self.assertRaisesRegex(TypeError, "transactions must be a list"):
            compute_user_features(({"user_id": "u1", "amount": 10},))

    def test_rejects_non_mapping_transaction(self):
        with self.assertRaisesRegex(TypeError, "index 0 must be a dictionary"):
            compute_user_features(["not-a-transaction"])

    def test_rejects_missing_or_blank_user_id(self):
        for user_id in (None, "", "   ", 123):
            with self.subTest(user_id=user_id):
                with self.assertRaisesRegex(ValueError, "non-empty string user_id"):
                    compute_user_features([{"user_id": user_id, "amount": 10}])

    def test_rejects_missing_non_numeric_or_boolean_amount(self):
        for amount in (None, "10", True):
            with self.subTest(amount=amount):
                with self.assertRaisesRegex(TypeError, "amount must be a real number"):
                    compute_user_features([{"user_id": "u1", "amount": amount}])

    def test_rejects_non_finite_amount(self):
        for amount in (math.nan, math.inf, -math.inf):
            with self.subTest(amount=amount):
                with self.assertRaisesRegex(ValueError, "amount must be finite"):
                    compute_user_features([{"user_id": "u1", "amount": amount}])


class ExistingCapabilityTests(unittest.TestCase):
    def test_drift_normal(self):
        result = FeatureDriftDetector.evaluate_drift(
            "order_amt", [0.2, 0.3, 0.5], [0.21, 0.29, 0.50]
        )

        self.assertEqual(result["status"], "NORMAL")
        self.assertFalse(result["action_required"])

    def test_drift_detected(self):
        result = FeatureDriftDetector.evaluate_drift(
            "order_amt", [0.1, 0.2, 0.7], [0.7, 0.2, 0.1]
        )

        self.assertTrue(result["action_required"])

    def test_rag_preparation(self):
        records = RAGDatasetPreparer.prepare_dataset(
            [{"id": "doc-1", "text": "A sufficiently detailed synthetic record."}]
        )

        self.assertEqual(records[0]["doc_id"], "doc-1")
        self.assertTrue(records[0]["is_rag_ready"])


if __name__ == "__main__":
    unittest.main()
