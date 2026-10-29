"""
Sahayak Layer 5a: Settlement Delay Workflow (~40% of tickets)
Handles: "Kal ka paisa nahi aaya"
"""

from typing import Dict, Any
from agent.conversation import ConversationSession
from agent.state_machine import AgentStateMachine


def run_settlement_workflow(
    merchant_id: str = "M_1092",
    caller_phone: str = "+919876543210",
    utterance: str = "Bhaiya, kal ka paisa abhi tak nahi aaya."
) -> Dict[str, Any]:
    session = ConversationSession(merchant_id=merchant_id, caller_phone=caller_phone)
    sm = AgentStateMachine(session)
    return sm.execute_turn(utterance, lang_code="hi-IN")
