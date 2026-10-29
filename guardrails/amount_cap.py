"""
Guardrail Gate 4: ₹50,000 Hard Limit Cap
"""

from typing import Tuple

HARD_CAP_INR = 50000.00


def check_amount_cap(amount_inr: float, hard_cap: float = HARD_CAP_INR) -> Tuple[bool, str]:
    """
    Non-negotiable deterministic hard barrier for financial actions.
    No settlement retry, payment trigger, or refund above ₹50,000 can execute autonomously.
    Returns: (is_within_cap: bool, message: str)
    """
    if amount_inr > hard_cap:
        return False, f"AMOUNT_EXCEEDS_50K_CAP: Requested amount ₹{amount_inr:,.2f} exceeds ₹{hard_cap:,.2f} hard limit."
        
    return True, f"Amount ₹{amount_inr:,.2f} is within safe autonomous cap of ₹{hard_cap:,.2f}."

