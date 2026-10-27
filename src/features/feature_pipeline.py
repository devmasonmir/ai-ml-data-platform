"""PySpark Feature Transformation Pipeline."""
import logging
import math
from numbers import Real

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def _validate_transaction(transaction: object, index: int) -> tuple[str, float]:
    """Return a normalized transaction or raise a record-specific error."""
    if not isinstance(transaction, dict):
        raise TypeError(f"transaction at index {index} must be a dictionary")

    user_id = transaction.get("user_id")
    if not isinstance(user_id, str) or not user_id.strip():
        raise ValueError(
            f"transaction at index {index} must have a non-empty string user_id"
        )

    amount = transaction.get("amount")
    if isinstance(amount, bool) or not isinstance(amount, Real):
        raise TypeError(
            f"transaction at index {index} amount must be a real number"
        )

    normalized_amount = float(amount)
    if not math.isfinite(normalized_amount):
        raise ValueError(f"transaction at index {index} amount must be finite")

    return user_id.strip(), normalized_amount


def compute_user_features(transactions: list) -> list:
    """Aggregate validated transaction amounts into per-user features."""
    if not isinstance(transactions, list):
        raise TypeError("transactions must be a list")

    logger.info("Computing user feature aggregates...")
    user_data = {}
    for index, transaction in enumerate(transactions):
        uid, amount = _validate_transaction(transaction, index)
        if uid not in user_data:
            user_data[uid] = {"amounts": [], "count": 0}
        user_data[uid]["amounts"].append(amount)
        user_data[uid]["count"] += 1

    features = []
    for uid, data in user_data.items():
        avg_val = math.fsum(data["amounts"]) / len(data["amounts"])
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
