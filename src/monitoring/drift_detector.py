"""Population Stability Index (PSI) Drift Detector."""
import math
from typing import List, Dict, Any

class FeatureDriftDetector:
    @staticmethod
    def calculate_psi(expected_dist: List[float], actual_dist: List[float]) -> float:
        """Calculate PSI between baseline training distribution and production inference distribution."""
        psi = 0.0
        for e, a in zip(expected_dist, actual_dist):
            e_safe = max(e, 0.0001)
            a_safe = max(a, 0.0001)
            psi += (a_safe - e_safe) * math.log(a_safe / e_safe)
        return round(psi, 4)

    @classmethod
    def evaluate_drift(cls, feature_name: str, expected: List[float], actual: List[float]) -> Dict[str, Any]:
        psi_score = cls.calculate_psi(expected, actual)
        # Industry standard: PSI < 0.1 No change, 0.1 <= PSI <= 0.2 Moderate drift, PSI > 0.2 Significant drift
        status = "NORMAL"
        if psi_score > 0.2:
            status = "SIGNIFICANT_DRIFT"
        elif psi_score >= 0.1:
            status = "MODERATE_DRIFT"

        return {
            "feature": feature_name,
            "psi_score": psi_score,
            "status": status,
            "action_required": psi_score > 0.2
        }
