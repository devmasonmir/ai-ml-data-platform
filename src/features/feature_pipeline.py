"""PySpark Feature Transformation Pipeline."""
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def compute_user_features(transactions: list) -> list:
    """Simulate distributed aggregation for user behavioral features."""
    logger.info("Computing user feature aggregates...")
    user_data = {}
    for tx in transactions:
        uid = tx["user_id"]
        if uid not in user_data:
            user_data[uid] = {"amounts": [], "count": 0}
        user_data[uid]["amounts"].append(tx["amount"])
        user_data[uid]["count"] += 1

    features = []
    for uid, data in user_data.items():
        avg_val = sum(data["amounts"]) / max(len(data["amounts"]), 1)
        features.append({
            "user_id": uid,
            "avg_order_value_30d": round(avg_val, 2),
            "total_transactions_30d": data["count"],
            "high_value_customer": avg_val > 500.0
        })
    logger.info("Generated " + str(len(features)) + " feature records")
    return features

if __name__ == "__main__":
    mock_txs = [
        {"user_id": "u1", "amount": 120.0},
        {"user_id": "u1", "amount": 950.0},
        {"user_id": "u2", "amount": 35.0}
    ]
    feats = compute_user_features(mock_txs)
    print("Features:", feats)
