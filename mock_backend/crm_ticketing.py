"""
Paytm Mock System 4e: CRM & Ticketing API
"""

import uuid
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional
from mock_backend.mock_data import db


def create_crm_ticket(
    merchant_id: str,
    category: str,
    issue_type: str,
    actions_attempted: List[str],
    resolution_status: str = "AUTONOMOUSLY_RESOLVED"
) -> Dict[str, Any]:
    """Autonomous CRM ticket generation."""
    ticket_id = f"TKT_{uuid.uuid4().hex[:6].upper()}"
    now_iso = datetime.now(timezone.utc).isoformat()
    
    ticket = {
        "ticket_id": ticket_id,
        "merchant_id": merchant_id,
        "category": category,
        "issue_type": issue_type,
        "actions_attempted": actions_attempted,
        "status": "CLOSED" if resolution_status == "AUTONOMOUSLY_RESOLVED" else "OPEN",
        "resolution_status": resolution_status,
        "created_at": now_iso,
        "closed_at": now_iso if resolution_status == "AUTONOMOUSLY_RESOLVED" else None
    }
    
    db.tickets[ticket_id] = ticket
    return ticket


def escalate_ticket_to_human(
    merchant_id: str,
    escalation_reason: str,
    issue_summary: str,
    actions_attempted: List[Any],
    next_recommended_action: str,
    full_transcript: Any
) -> Dict[str, Any]:
    """Escalate case to Human Support Queue with 100% complete context packet."""
    ticket_id = f"TKT_ESC_{uuid.uuid4().hex[:6].upper()}"
    
    packet = {
        "ticket_id": ticket_id,
        "merchant_id": merchant_id,
        "escalation_reason": escalation_reason,
        "issue_summary": issue_summary,
        "actions_attempted": actions_attempted,
        "next_recommended_action": next_recommended_action,
        "full_transcript": full_transcript,
        "status": "ASSIGNED_TO_SPECIALIST",
        "assigned_queue": "PRIORITY_RISK_SETTLEMENT_DESK" if "SETTLEMENT" in escalation_reason or "CAP" in escalation_reason else "PRIORITY_DESK",
        "sla_minutes": 15,
        "created_at": datetime.now(timezone.utc).isoformat()
    }
    
    db.tickets[ticket_id] = packet
    return packet


def get_ticket_status(ticket_id: str) -> Optional[Dict[str, Any]]:
    """Get status of CRM ticket."""
    return db.tickets.get(ticket_id)
