"""
Sahayak Layer 5d: EMI & KYC Issues Workflow (~15% of tickets)
Handles: "Mera account limit ho gaya" / KYC block
"""

from typing import Dict, Any
from agent.conversation import ConversationSession
from agent.state_machine import AgentStateMachine


def run_emi_kyc_workflow(
    merchant_id: str = "M_5510",
    caller_phone: str = "+919844556677",
    utterance: str = "Mera account limit ho gaya hai, KYC update link chahiye."
) -> Dict[str, Any]:
    session = ConversationSession(merchant_id=merchant_id, caller_phone=caller_phone)
    sm = AgentStateMachine(session)
    return sm.execute_turn(utterance, lang_code="hi-IN")

