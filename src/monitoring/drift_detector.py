"""Population Stability Index (PSI) drift detector."""

import math
from numbers import Real
from typing import Any, Dict, List, Sequence


class FeatureDriftDetector:
    """Validate and compare two binned feature distributions."""

    _EPSILON = 0.0001

    @staticmethod
    def _normalize_distribution(
        distribution: Sequence[float], label: str
    ) -> List[float]:
        if not distribution:
            raise ValueError(f"{label} distribution must contain at least one bin")

        values = []
        for index, value in enumerate(distribution):
            if isinstance(value, bool) or not isinstance(value, Real):
                raise TypeError(
                    f"{label} distribution bin {index} must be a real number"
                )

            numeric_value = float(value)
            if not math.isfinite(numeric_value):
                raise ValueError(
                    f"{label} distribution bin {index} must be finite"
                )
            if numeric_value < 0:
                raise ValueError(
                    f"{label} distribution bin {index} must be non-negative"
                )
            values.append(numeric_value)

        total = math.fsum(values)
        if total <= 0:
            raise ValueError(f"{label} distribution total must be greater than zero")

        return [value / total for value in values]

    @classmethod
    def calculate_psi(
        cls, expected_dist: Sequence[float], actual_dist: Sequence[float]
    ) -> float:
        """Calculate PSI for matching histograms supplied as counts or proportions.

        Both distributions must describe the same non-empty set of bins. Values are
        normalized before comparison, and a small floor keeps zero-frequency bins
        finite without hiding malformed inputs.
        """
        if len(expected_dist) != len(actual_dist):
            raise ValueError("expected and actual distributions must use the same bins")

        expected = cls._normalize_distribution(expected_dist, "expected")
        actual = cls._normalize_distribution(actual_dist, "actual")

        psi = math.fsum(
            (actual_value - expected_value)
            * math.log(actual_value / expected_value)
            for expected_value, actual_value in (
                (max(e, cls._EPSILON), max(a, cls._EPSILON))
                for e, a in zip(expected, actual)
            )
        )
        return round(psi, 6)

    @classmethod
    def evaluate_drift(
        cls,
        feature_name: str,
        expected: Sequence[float],
        actual: Sequence[float],
    ) -> Dict[str, Any]:
        """Return the PSI score and the configured drift severity."""
        psi_score = cls.calculate_psi(expected, actual)
        status = "NORMAL"
        if psi_score > 0.2:
            status = "SIGNIFICANT_DRIFT"
        elif psi_score >= 0.1:
            status = "MODERATE_DRIFT"

        return {
            "feature": feature_name,
            "psi_score": psi_score,
            "status": status,
            "action_required": psi_score > 0.2,
        }
