"""
Sahayak Layer 2: Explicit Reasoning Trace Logger
Ensures full auditability: "Explicit reasoning trace - not a black box."
"""

from typing import Dict, Any, List
from audit.writer import audit_writer
from audit.schema import AuditEventType


class ReasoningTrace:
    """Records the structured chain-of-thought at every state transition."""

    def __init__(self, session_id: str, merchant_id: str):
        self.session_id = session_id
        self.merchant_id = merchant_id
        self.steps: List[Dict[str, Any]] = []

    def record_step(
        self,
        state: str,
        observation: str,
        thought: str,
        decision: str,
        confidence: float,
        metadata: Dict[str, Any] = None
    ):
        """Append an explicit reasoning node."""
        step = {
            "step_num": len(self.steps) + 1,
            "state": state,
            "observation": observation,
            "thought": thought,
            "decision": decision,
            "confidence": confidence,
            "metadata": metadata or {}
        }
        self.steps.append(step)

    def get_trace_summary(self) -> List[Dict[str, Any]]:
        return list(self.steps)
