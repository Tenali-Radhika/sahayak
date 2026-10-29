"""
Sahayak - Slide 1 Signature Compound Flow
Executes: Settlement Delay Resolution + Gateway Confirmation + Proactive EMI Delivery
in a SINGLE autonomous call turn.
"""

from typing import Dict, Any
from agent.conversation import ConversationSession
from agent.state_machine import AgentStateMachine


def run_compound_call(
    merchant_id: str = "M_1092",
    caller_phone: str = "+919876543210",
    utterance: str = "Bhaiya, kal ka paisa abhi tak nahi aaya."
) -> Dict[str, Any]:
    """
    Executes the exact demo scenario presented on Slide 1:
    Two workflows, zero humans.
    """
    session = ConversationSession(merchant_id=merchant_id, caller_phone=caller_phone)
    sm = AgentStateMachine(session)
    result = sm.execute_turn(utterance, lang_code="hi-IN")
    return {
        "session_id": session.session_id,
        "merchant_id": merchant_id,
        "input_speech": utterance,
        "spoken_response": result["response_text"],
        "cs_outcome": result["status"],
        "retry_job_id": result["action_result"].get("job_id"),
        "gateway_confirmed": result["action_result"].get("gateway_confirmation", {}).get("confirmation_status") == "CONFIRMED_PROCESSED",
        "sales_proactive_link": result["proactive_sales"].get("link", {}).get("web_url"),
        "latency_ms": result["total_latency_ms"],
        "within_2s_budget": result["within_2s_budget"],
        "reasoning_trace": result["reasoning_trace"]
    }
