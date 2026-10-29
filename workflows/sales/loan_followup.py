"""
Sahayak Layer 6: Loan Pre-Qualification Follow-up
"""

from typing import Dict, Any
import mock_backend as backend
from audit.writer import audit_writer
from audit.schema import AuditEventType


def trigger_loan_followup(merchant_id: str = "M_1092") -> Dict[str, Any]:
    """Identifies eligible merchants for credit line top-up and surfaces next best action."""
    nudge = backend.trigger_nudge(merchant_id, "DAILY_LOAN_TOPUP")
    
    audit_writer.append(
        f"SALES_SESS_{merchant_id}",
        merchant_id,
        AuditEventType.SALES_OUTREACH,
        "PROACTIVE_OUTREACH",
        {"workflow": "LOAN_TOPUP", "nudge": nudge}
    )
    
    return {
        "status": "OFFER_SURFACED",
        "merchant_id": merchant_id,
        "preapproved_amount_inr": 100000.0,
        "offer_text": nudge["offer_text"]
    }
