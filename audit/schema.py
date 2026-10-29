"""
Sahayak - Audit Log Schema
Immutable, hash-chained ledger models.
"""

from enum import Enum
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field


class AuditEventType(str, Enum):
    CALL_INBOUND = "CALL_INBOUND"
    DIAGNOSIS_COMPLETED = "DIAGNOSIS_COMPLETED"
    GUARDRAIL_EVALUATION = "GUARDRAIL_EVALUATION"
    GUARDRAIL_VIOLATION = "GUARDRAIL_VIOLATION"
    ACTION_EXECUTED = "ACTION_EXECUTED"
    ACTION_VERIFIED = "ACTION_VERIFIED"
    SALES_OUTREACH = "SALES_OUTREACH"
    ESCALATION_TRIGGERED = "ESCALATION_TRIGGERED"
    CALL_COMPLETED = "CALL_COMPLETED"


class AuditEntry(BaseModel):
    index: int
    timestamp: str
    prev_hash: str
    session_id: str
    merchant_id: str
    event_type: AuditEventType
    state: str
    details: Dict[str, Any]
    hash: str
