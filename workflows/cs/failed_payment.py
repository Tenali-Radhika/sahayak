"""
Sahayak Layer 5c: Failed / Missing Payment Workflow (~20% of tickets)
Handles: "Customer ke paise kat gaye, mujhe nahi mile"
"""

from typing import Dict, Any
from agent.conversation import ConversationSession
from agent.state_machine import AgentStateMachine


def run_failed_payment_workflow(
    merchant_id: str = "M_1092",
    caller_phone: str = "+919876543210",
    utterance: str = "Customer ke paise kat gaye, par mujhe account mein nahi mile."
) -> Dict[str, Any]:
    session = ConversationSession(merchant_id=merchant_id, caller_phone=caller_phone)
    sm = AgentStateMachine(session)
    return sm.execute_turn(utterance, lang_code="hi-IN")

