"""
Sahayak Layer 7: Escalation Trigger Evaluator
Identifies situations where Sahayak knows when NOT to act autonomously.
"""

from typing import Dict, Any, Tuple, Optional


def evaluate_escalation_triggers(
    merchant: Dict[str, Any],
    proposed_amount: Optional[float] = None,
    confidence_score: float = 100.0,
    sentiment_distressed: bool = False
) -> Tuple[bool, Optional[str], Optional[str]]:
    """
    Evaluates all criteria that mandate immediate human specialist transfer:
    1. Fraud flag
    2. Active dispute
    3. Hardship case
    4. Amount > ₹50,000
    5. Caller distressed / angry
    6. Confidence < 80%
    
    Returns: (needs_escalation: bool, trigger_code: Optional[str], rationale: Optional[str])
    """
    if merchant.get("is_fraud_flagged", False):
        return True, "FRAUD_FLAG_ACTIVE", "Merchant flagged for suspected fraudulent velocity."
        
    if merchant.get("active_disputes", 0) > 0:
        return True, "ACTIVE_DISPUTE_SUSPENSION", "Account has open chargeback or legal dispute."
        
    if merchant.get("hardship_flag", False):
        return True, "HARDSHIP_CASE", "Merchant flagged for sensitive hardship assistance."
        
    if proposed_amount is not None and proposed_amount > 50000.0:
        return True, "AMOUNT_EXCEEDS_50K_CAP", f"Transaction value ₹{proposed_amount:,.2f} exceeds ₹50K autonomous limit."
        
    if sentiment_distressed:
        return True, "CALLER_DISTRESS_DETECTED", "High caller distress/agitation detected in merchant speech."
        
    if confidence_score < 80.0:
        return True, "CONFIDENCE_BELOW_THRESHOLD", f"Diagnosis confidence {confidence_score:.1f}% below 80% safety gate."
        
    return False, None, None
