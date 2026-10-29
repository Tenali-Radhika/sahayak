"""
Paytm Mock System 4d: Loan & EMI Management API
"""

import uuid
from typing import Dict, Any, Optional
from mock_backend.mock_data import db


def get_loan_status(merchant_id: str) -> Optional[Dict[str, Any]]:
    """Retrieve merchant cash advance / credit line health."""
    return db.loans.get(merchant_id)


def get_emi_details(merchant_id: str) -> Optional[Dict[str, Any]]:
    """Get upcoming EMI amount and due date."""
    loan = db.loans.get(merchant_id)
    if not loan:
        return None
    return {
        "merchant_id": merchant_id,
        "loan_account_id": loan["loan_account_id"],
        "outstanding_balance_inr": loan["outstanding_balance_inr"],
        "next_emi_amount_inr": loan["next_emi_amount_inr"],
        "next_emi_due_date": loan["next_emi_due_date"],
        "is_due_tomorrow": loan["next_emi_due_date"] in ["2026-10-30", "2026-10-29"]
    }


def send_emi_payment_link(merchant_id: str, amount_inr: Optional[float] = None) -> Dict[str, Any]:
    """Generate and dispatch one-click UPI payment link for EMI."""
    loan = db.loans.get(merchant_id)
    target_amount = amount_inr if amount_inr is not None else (loan["next_emi_amount_inr"] if loan else 1000.0)
    
    link_id = f"PLNK_EMI_{uuid.uuid4().hex[:6].upper()}"
    link_url = f"https://paytm.me/emi/{merchant_id}_{link_id[-4:]}"
    
    record = {
        "payment_link_id": link_id,
        "merchant_id": merchant_id,
        "amount_inr": target_amount,
        "payment_url": link_url,
        "channel": "SMS_AND_WHATSAPP",
        "status": "SMS_SENT"
    }
    
    db.payment_links[link_id] = record
    return record
