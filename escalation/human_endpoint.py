"""
Sahayak Layer 7: Mock Human Agent Desk Endpoint
Receives escalation packets and logs them to the human queue.
"""

from typing import Dict, Any, List
from audit.writer import audit_writer
from audit.schema import AuditEventType

# Mock human queue
ESCALATION_QUEUE: List[Dict[str, Any]] = []


def dispatch_to_human_agent(escalation_packet: Dict[str, Any]) -> Dict[str, Any]:
    """
    Simulates routing the escalation packet to a senior human agent's terminal.
    Records the event to the audit ledger.
    """
    ESCALATION_QUEUE.append(escalation_packet)
    
    # Audit log entry for senior teammate escalation
    audit_writer.append(
        escalation_packet["session_id"],
        escalation_packet["merchant_info"]["merchant_id"],
        AuditEventType.ESCALATION_TRIGGERED,
        "ESCALATE",
        {
            "escalation_id": escalation_packet["escalation_id"],
            "trigger_reason": escalation_packet["trigger_reason"],
            "assigned_desk": escalation_packet["assigned_desk"],
            "packet_completeness_check": {
                "has_issue_summary": bool(escalation_packet.get("issue_summary")),
                "has_what_tried": bool(escalation_packet.get("what_sahayak_tried")),
                "has_next_action": bool(escalation_packet.get("next_recommended_action")),
                "has_full_transcript": bool(escalation_packet.get("full_transcript"))
            }
        }
    )
    
    return {
        "status": "QUEUED_WITH_FULL_CONTEXT",
        "escalation_id": escalation_packet["escalation_id"],
        "assigned_desk": escalation_packet["assigned_desk"],
        "sla_minutes": escalation_packet["sla_minutes"]
    }
