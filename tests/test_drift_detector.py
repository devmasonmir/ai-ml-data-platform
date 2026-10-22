import math
import unittest

from src.monitoring.drift_detector import FeatureDriftDetector


class FeatureDriftDetectorTests(unittest.TestCase):
    def test_accepts_counts_and_normalizes_them(self):
        count_score = FeatureDriftDetector.calculate_psi([20, 30, 50], [21, 29, 50])
        proportion_score = FeatureDriftDetector.calculate_psi(
            [0.2, 0.3, 0.5], [0.21, 0.29, 0.5]
        )

        self.assertEqual(count_score, proportion_score)

    def test_zero_frequency_bins_produce_a_finite_score(self):
        score = FeatureDriftDetector.calculate_psi([0, 50, 50], [10, 40, 50])

        self.assertTrue(math.isfinite(score))
        self.assertGreater(score, 0)

    def test_rejects_mismatched_bins_instead_of_truncating(self):
        with self.assertRaisesRegex(ValueError, "same bins"):
            FeatureDriftDetector.calculate_psi([0.5, 0.5], [0.2, 0.3, 0.5])

    def test_rejects_empty_distributions(self):
        with self.assertRaisesRegex(ValueError, "at least one bin"):
            FeatureDriftDetector.calculate_psi([], [])

    def test_rejects_zero_total_distribution(self):
        with self.assertRaisesRegex(ValueError, "greater than zero"):
            FeatureDriftDetector.calculate_psi([0, 0], [0.5, 0.5])

    def test_rejects_negative_values(self):
        with self.assertRaisesRegex(ValueError, "non-negative"):
            FeatureDriftDetector.calculate_psi([0.6, -0.1], [0.5, 0.5])

    def test_rejects_non_finite_values(self):
        for invalid_value in (math.nan, math.inf, -math.inf):
            with self.subTest(invalid_value=invalid_value):
                with self.assertRaisesRegex(ValueError, "finite"):
                    FeatureDriftDetector.calculate_psi(
                        [0.5, invalid_value], [0.5, 0.5]
                    )

    def test_rejects_boolean_bins(self):
        with self.assertRaisesRegex(TypeError, "real number"):
            FeatureDriftDetector.calculate_psi([True, 1], [1, 1])

    def test_preserves_significant_drift_classification(self):
        result = FeatureDriftDetector.evaluate_drift(
            "order_amount", [10, 20, 70], [70, 20, 10]
        )

        self.assertEqual(result["status"], "SIGNIFICANT_DRIFT")
        self.assertTrue(result["action_required"])


if __name__ == "__main__":
    unittest.main()
