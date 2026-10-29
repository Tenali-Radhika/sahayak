"""
Paytm Mock System 4b: Settlement & Payment Gateway API
"""

import uuid
from datetime import datetime, timezone
from typing import Dict, Any, Optional
from mock_backend.mock_data import db


def get_settlement_status(merchant_id: str, date: Optional[str] = None) -> Optional[Dict[str, Any]]:
    """Retrieve settlement status for a merchant."""
    settlement = db.settlements.get(merchant_id)
    if not settlement:
        return None
    return settlement


def retry_settlement(merchant_id: str, settlement_id: str, requested_amount_inr: float) -> Dict[str, Any]:
    """
    Queue an autonomous re-clearing run.
    Note: Guardrail Layer must have verified Caller ID, Fraud, and ₹50,000 cap before calling this!
    """
    settlement = db.settlements.get(merchant_id)
    if not settlement:
        raise ValueError(f"No settlement record found for merchant {merchant_id}")

    job_id = f"RETRY_JOB_{uuid.uuid4().hex[:8].upper()}"
    job_record = {
        "job_id": job_id,
        "merchant_id": merchant_id,
        "settlement_id": settlement_id,
        "amount_inr": requested_amount_inr,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "scheduled_execution": "2026-10-30T06:00:00+05:30",
        "gateway_status": "ACK_RECEIVED",
        "confirmed": True
    }
    
    db.retry_jobs[job_id] = job_record
    
    # Update settlement status in mock DB
    settlement["status"] = "RETRY_QUEUED"
    settlement["retry_job_id"] = job_id

    return {
        "status": "QUEUED",
        "job_id": job_id,
        "scheduled_execution": "2026-10-30T06:00:00+05:30",
        "estimated_credit_time": "2026-10-30T06:15:00+05:30",
        "gateway_status": "ACK_RECEIVED"
    }


def confirm_settlement_retry(job_id: str) -> Dict[str, Any]:
    """Verify backend clearance with national clearing switch (NPCI / Banking partner)."""
    job = db.retry_jobs.get(job_id)
    if not job:
        # Default mock confirmation for demo jobs
        return {
            "job_id": job_id,
            "confirmation_status": "CONFIRMED_PROCESSED",
            "gateway_ack_code": "NPCI_ACK_SUCCESS_200",
            "settlement_reference": f"UTR_PAYTM_{uuid.uuid4().hex[:9].upper()}",
            "merchant_notified": True
        }
        
    return {
        "job_id": job_id,
        "confirmation_status": "CONFIRMED_PROCESSED",
        "gateway_ack_code": "NPCI_ACK_SUCCESS_200",
        "settlement_reference": f"UTR_PAYTM_{uuid.uuid4().hex[:9].upper()}",
        "merchant_notified": True
    }


def resync_transaction(merchant_id: str, customer_ref: str, approx_amount_inr: float) -> Dict[str, Any]:
    """Cross-checks gateway logs when a customer's money was deducted but didn't sound on Soundbox."""
    txn_id = f"TXN_{uuid.uuid4().hex[:8].upper()}"
    return {
        "sync_status": "RESOLVED_SYNCED",
        "merchant_id": merchant_id,
        "transaction_id": txn_id,
        "amount_inr": approx_amount_inr,
        "credited_to_merchant": True,
        "soundbox_broadcast_trigger": "SUCCESS",
        "reference_id": f"REF_{uuid.uuid4().hex[:6].upper()}"
    }

