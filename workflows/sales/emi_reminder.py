"""
Sahayak Layer 6: Proactive EMI Reminder Workflow
Handles proactive outbound outreach for upcoming installments.
"""

from typing import Dict, Any
import mock_backend as backend
from audit.writer import audit_writer
from audit.schema import AuditEventType


def trigger_proactive_emi_reminder(merchant_id: str = "M_1092") -> Dict[str, Any]:
    """Scans loan database, detects upcoming EMI, and delivers payment link."""
    emi_info = backend.get_emi_details(merchant_id)
    if not emi_info:
        return {"status": "NO_ACTIVE_LOAN"}
        
    link_record = backend.send_payment_link(
        merchant_id=merchant_id,
        amount_inr=emi_info["next_emi_amount_inr"],
        purpose="PROACTIVE_EMI_COLLECTION"
    )
    
    audit_writer.append(
        f"SALES_SESS_{merchant_id}",
        merchant_id,
        AuditEventType.SALES_OUTREACH,
        "PROACTIVE_OUTREACH",
        {"workflow": "EMI_REMINDER", "amount": emi_info["next_emi_amount_inr"], "link": link_record}
    )
    
    return {
        "status": "DISPATCHED",
        "merchant_id": merchant_id,
        "amount_inr": emi_info["next_emi_amount_inr"],
        "due_date": emi_info["next_emi_due_date"],
        "payment_link": link_record["web_url"]
    }

