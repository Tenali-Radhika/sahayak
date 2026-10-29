"""
Sahayak Layer 7: Escalation Packet Builder
Guarantees: "The human teammate never starts from zero."
"""

import uuid
from datetime import datetime, timezone
from typing import Dict, Any, List


def build_escalation_packet(
    session_id: str,
    merchant_id: str,
    merchant_name: str,
    phone_number: str,
    trigger_reason: str,
    issue_summary: str,
    what_sahayak_tried: List[Dict[str, Any]],
    next_recommended_action: str,
    full_transcript: List[Dict[str, str]],
    priority: str = "HIGH"
) -> Dict[str, Any]:
    """
    Constructs the 4-part complete escalation context packet promised in USP #3.
    """
    return {
        "escalation_id": f"ESC_{uuid.uuid4().hex[:8].upper()}",
        "session_id": session_id,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "priority": priority,
        "merchant_info": {
            "merchant_id": merchant_id,
            "business_name": merchant_name,
            "phone_number": phone_number
        },
        "trigger_reason": trigger_reason,
        # USP 3 Field 1: Issue Summary
        "issue_summary": issue_summary,
        # USP 3 Field 2: What Sahayak Tried
        "what_sahayak_tried": what_sahayak_tried,
        # USP 3 Field 3: Next Recommended Action
        "next_recommended_action": next_recommended_action,
        # USP 3 Field 4: Full Transcript
        "full_transcript": full_transcript,
        "assigned_desk": "PRIORITY_RISK_SETTLEMENT_DESK" if "SETTLEMENT" in trigger_reason or "CAP" in trigger_reason else "PRIORITY_ESCALATION_QUEUE",
        "sla_minutes": 15
    }
