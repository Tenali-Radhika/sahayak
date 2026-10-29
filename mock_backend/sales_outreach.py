"""
Paytm Mock System 4f: Sales Outreach & Payment Links API
"""

import uuid
from typing import Dict, Any, Optional
from mock_backend.mock_data import db


def send_payment_link(
    merchant_id: str,
    amount_inr: float,
    purpose: str = "PROACTIVE_EMI_COLLECTION",
    short_code: Optional[str] = None
) -> Dict[str, Any]:
    """Generate dynamic UPI payment link and send via SMS/WhatsApp."""
    link_id = f"LNK_{uuid.uuid4().hex[:6].upper()}"
    link_record = {
        "link_id": link_id,
        "merchant_id": merchant_id,
        "amount_inr": amount_inr,
        "purpose": purpose,
        "upi_intent_uri": f"upi://pay?pa=paytm.collection@icici&pn=PaytmLending&am={amount_inr:.2f}&tr={link_id}",
        "web_url": f"https://paytm.me/pay/{link_id}",
        "sent_via": "SMS_AND_WHATSAPP",
        "status": "DISPATCHED"
    }
    db.payment_links[link_id] = link_record
    return link_record


def get_payment_link_status(link_id: str) -> Optional[Dict[str, Any]]:
    """Get status of payment link."""
    return db.payment_links.get(link_id)


def trigger_nudge(merchant_id: str, campaign_type: str, discount_offer_code: Optional[str] = None) -> Dict[str, Any]:
    """Trigger proactive merchant retention or upsell nudge."""
    campaign_id = f"CMP_{uuid.uuid4().hex[:6].upper()}"
    
    offers = {
        "SOUNDBOX_4G_UPGRADE": "Upgrade your Soundbox 2G to 4G Voice with zero installation fee and 50% rental discount.",
        "DAILY_LOAN_TOPUP": "Special festive business loan top-up of ₹1,00,000 pre-approved for your store.",
        "FAST_SETTLEMENT_SUBSCRIPTION": "Get instant settlements 3 times a day with Paytm SuperSettlement."
    }
    
    nudge = {
        "campaign_id": campaign_id,
        "merchant_id": merchant_id,
        "campaign_type": campaign_type,
        "offer_text": offers.get(campaign_type, "Special merchant offer activated."),
        "dispatched": True,
        "channel": "VOICE_AND_APP_NOTIFICATION"
    }
    
    db.nudges.append(nudge)
    return nudge

