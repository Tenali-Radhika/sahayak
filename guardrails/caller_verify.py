"""
Guardrail Gate 1: Caller ID & Identity Verification
"""

from typing import Dict, Any, Tuple
from mock_backend.mock_data import db


def verify_caller_identity(caller_phone: str, claimed_merchant_id: str) -> Tuple[bool, str]:
    """
    Validates that the incoming caller phone number strictly matches the registered merchant record.
    Returns: (is_valid: bool, reason_message: str)
    """
    merchant = db.merchants.get(claimed_merchant_id)
    if not merchant:
        return False, f"Merchant ID '{claimed_merchant_id}' does not exist in registry."
        
    registered_phone = merchant.get("phone_number", "")
    # Normalize phone strings
    norm_caller = caller_phone.replace(" ", "").replace("-", "")
    norm_registered = registered_phone.replace(" ", "").replace("-", "")
    
    if norm_caller != norm_registered:
        return False, f"Caller phone '{caller_phone}' does not match registered phone for {claimed_merchant_id}."
        
    return True, "Caller ID verified successfully against merchant record."

