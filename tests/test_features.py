import pytest
from src.features.feature_pipeline import compute_user_features
from src.monitoring.drift_detector import FeatureDriftDetector
from src.rag.embedding_preparer import RAGDatasetPreparer

def test_feature_pipeline():
    txs = [{"user_id": "u1", "amount": 100.0}, {"user_id": "u1", "amount": 200.0}]
    feats = compute_user_features(txs)
    assert len(feats) == 1
    assert feats[0]["user_id"] == "u1"
    assert feats[0]["avg_order_value_30d"] == 150.0

def test_drift_normal():
    base = [0.2, 0.3, 0.5]
    curr = [0.21, 0.29, 0.50]
    res = FeatureDriftDetector.evaluate_drift("order_amt", base, curr)
    assert res["status"] == "NORMAL"
    assert res["action_required"] is False

def test_drift_detected():
    base = [0.1, 0.2, 0.7]
    curr = [0.7, 0.2, 0.1]
    res = FeatureDriftDetector.evaluate_drift("order_amt", base, curr)
    assert res["action_required"] is True
