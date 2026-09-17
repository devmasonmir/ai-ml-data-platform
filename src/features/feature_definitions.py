"""Feature View Schema Definitions."""
from pydantic import BaseModel
from typing import List, Optional

class UserFeatureRecord(BaseModel):
    user_id: str
    avg_order_value_30d: float
    total_transactions_30d: int
    account_age_days: int
    high_value_customer: bool
