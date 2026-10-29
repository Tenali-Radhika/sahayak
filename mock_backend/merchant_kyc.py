"""
Paytm Mock System 4a: Merchant Profile & KYC API
"""

from typing import Dict, Any, Optional
from mock_backend.mock_data import db


def get_merchant_profile(merchant_id: str) -> Optional[Dict[str, Any]]:
    """Retrieve verified merchant profile."""
    return db.merchants.get(merchant_id)


def get_kyc_status(merchant_id: str) -> Optional[Dict[str, Any]]:
    """Get KYC status, limits and documentation flags."""
    merchant = db.merchants.get(merchant_id)
    if not merchant:
        return None
    return {
        "merchant_id": merchant_id,
        "kyc_status": merchant["kyc_status"],
        "daily_limit_inr": merchant["daily_limit_inr"],
        "monthly_limit_inr": merchant["monthly_limit_inr"],
        "pending_documents": ["AADHAAR_OTP_UPDATE"] if merchant["kyc_status"] != "VERIFIED" else [],
        "rejection_reason": None,
        "last_verified_at": "2026-03-10T14:22:00Z"
    }


def resend_kyc_link(merchant_id: str, delivery_channel: str = "WHATSAPP_AND_SMS") -> Dict[str, Any]:
    """Dispatch rapid Aadhaar/e-KYC biometric update link."""
    merchant = db.merchants.get(merchant_id)
    if not merchant:
        raise ValueError(f"Merchant {merchant_id} not found")
        
    link_url = f"https://paytm.me/kyc/{merchant_id}_reup"
    return {
        "status": "SENT",
        "link_url": link_url,
        "expires_in_hours": 24,
        "delivery_id": f"MSG_{hash(merchant_id) % 1000000}"
    }


def update_kyc_status(merchant_id: str, new_status: str) -> Dict[str, Any]:
    """Update KYC status (for mock testing completion flow)."""
    merchant = db.merchants.get(merchant_id)
    if not merchant:
        raise ValueError(f"Merchant {merchant_id} not found")
    merchant["kyc_status"] = new_status
    return {"merchant_id": merchant_id, "updated_status": new_status, "success": True}

