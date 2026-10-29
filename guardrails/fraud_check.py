"""
Guardrail Gate 2: Fraud & Risk Flag Pre-check
"""

from typing import Tuple
from mock_backend.mock_data import db


def check_fraud_and_risk(merchant_id: str) -> Tuple[bool, str]:
    """
    Checks if merchant has active fraud flags, active disputes, or hardship holds.
    Returns: (is_clean: bool, flag_reason: str)
    """
    merchant = db.merchants.get(merchant_id)
    if not merchant:
        return False, f"Merchant '{merchant_id}' not found."
        
    if merchant.get("is_fraud_flagged", False):
        return False, "FRAUD_FLAG_ACTIVE: Merchant account is flagged by Risk Operations."
        
    if merchant.get("active_disputes", 0) > 0:
        return False, f"ACTIVE_DISPUTE_SUSPENSION: Merchant has {merchant['active_disputes']} unresolved dispute(s)."
        
    if merchant.get("hardship_flag", False):
        return False, "HARDSHIP_HOLD: Merchant is marked for priority empathetic human counseling."
        
    return True, "No fraud, dispute, or hardship flags detected."

