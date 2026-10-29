"""
Sahayak Layer 5b: Soundbox Failure Workflow (~25% of tickets)
Handles: "Soundbox bol nahi raha"
"""

from typing import Dict, Any
from agent.conversation import ConversationSession
from agent.state_machine import AgentStateMachine


def run_soundbox_workflow(
    merchant_id: str = "M_4401",
    caller_phone: str = "+919822334455",
    utterance: str = "Soundbox bol nahi raha, subah se awaz band hai.",
    lang_code: str = "hi-IN"
) -> Dict[str, Any]:
    session = ConversationSession(merchant_id=merchant_id, caller_phone=caller_phone)
    sm = AgentStateMachine(session)
    return sm.execute_turn(utterance, lang_code=lang_code)

