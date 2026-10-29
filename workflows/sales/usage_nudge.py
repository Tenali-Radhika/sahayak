"""
Sahayak Layer 6: Soundbox Retention & 4G Upgrade Nudge
"""

from typing import Dict, Any
import mock_backend as backend
from audit.writer import audit_writer
from audit.schema import AuditEventType


def trigger_soundbox_upgrade_nudge(merchant_id: str = "M_1092") -> Dict[str, Any]:
    """Detects low device usage or legacy 2G device and dispatches upgrade voucher."""
    nudge = backend.trigger_nudge(merchant_id, "SOUNDBOX_4G_UPGRADE", "UPGRADE_50_OFF")
    
    audit_writer.append(
        f"SALES_SESS_{merchant_id}",
        merchant_id,
        AuditEventType.SALES_OUTREACH,
        "PROACTIVE_OUTREACH",
        {"workflow": "SOUNDBOX_UPGRADE", "nudge": nudge}
    )
    
    return {
        "status": "DELIVERED",
        "merchant_id": merchant_id,
        "campaign": "SOUNDBOX_4G_UPGRADE",
        "offer_text": nudge["offer_text"]
    }

