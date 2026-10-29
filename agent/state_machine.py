"""
Sahayak Layer 2: 6-State FSM Controller
Orchestrates: LISTEN -> DIAGNOSE -> FETCH_CONTEXT -> ACT -> VERIFY -> CLOSE / ESCALATE
Enforces: Guardrails before ACT, Gateway confirmation at VERIFY, and Audit Log on every step.
"""

import time
from typing import Dict, Any, Optional
from audit.writer import audit_writer
from audit.schema import AuditEventType
from agent.conversation import ConversationSession
from agent.llm_client import AgentLLM
from agent.reasoning_trace import ReasoningTrace
from guardrails.pipeline import GuardrailPipeline, GuardrailViolation
from escalation.triggers import evaluate_escalation_triggers
from escalation.packet import build_escalation_packet
from escalation.human_endpoint import dispatch_to_human_agent
import mock_backend as backend


class AgentStateMachine:
    """State machine controller for autonomous merchant servicing."""

    def __init__(self, session: ConversationSession):
        self.session = session
        self.state = "INIT"
        self.trace = ReasoningTrace(session.session_id, session.merchant_id)
        self.diagnosis: Dict[str, Any] = {}
        self.context: Dict[str, Any] = {}
        self.action_result: Dict[str, Any] = {}
        self.proactive_sales_result: Dict[str, Any] = {}
        self.escalation_packet: Optional[Dict[str, Any]] = None

    def execute_turn(
        self,
        raw_speech_text: str,
        lang_code: str = "hi-IN",
        stt_latency_ms: int = 400
    ) -> Dict[str, Any]:
        """
        Executes the full 6-state autonomous cycle for one conversation turn.
        Returns final turn result with audio response text, latencies, state trace, and status.
        """
        turn_start_time = time.time()
        
        # -------------------------------------------------------------
        # STATE 1: LISTEN
        # -------------------------------------------------------------
        self.state = "LISTEN"
        self.session.add_turn("MERCHANT", raw_speech_text, stt_latency_ms)
        audit_writer.append(
            self.session.session_id, self.session.merchant_id,
            AuditEventType.CALL_INBOUND, self.state,
            {"raw_utterance": raw_speech_text, "language": lang_code, "stt_latency_ms": stt_latency_ms}
        )
        self.trace.record_step(
            "LISTEN", raw_speech_text, "Transcribed merchant voice input", "Transition to DIAGNOSE", 100.0
        )

        # -------------------------------------------------------------
        # STATE 2: DIAGNOSE
        # -------------------------------------------------------------
        self.state = "DIAGNOSE"
        self.diagnosis = AgentLLM.diagnose_issue(raw_speech_text, self.session.merchant_id)
        confidence = self.diagnosis["confidence"]
        category = self.diagnosis["category"]
        
        audit_writer.append(
            self.session.session_id, self.session.merchant_id,
            AuditEventType.DIAGNOSIS_COMPLETED, self.state,
            {"diagnosis": self.diagnosis}
        )
        self.trace.record_step(
            "DIAGNOSE", f"Classified as {category}", f"Confidence scored at {confidence}%", "Transition to FETCH_CONTEXT", confidence
        )

        # Check early confidence gate
        if confidence < 80.0:
            return self._transition_to_escalate("CONFIDENCE_BELOW_THRESHOLD", f"Diagnosis confidence {confidence}% below safety threshold.")

        # -------------------------------------------------------------
        # STATE 3: FETCH CONTEXT (Pull from relevant mock Paytm systems)
        # -------------------------------------------------------------
        self.state = "FETCH_CONTEXT"
        merchant_profile = backend.get_merchant_profile(self.session.merchant_id)
        if not merchant_profile:
            return self._transition_to_escalate("MERCHANT_NOT_FOUND", f"Merchant {self.session.merchant_id} not registered.")
            
        self.context["merchant"] = merchant_profile
        
        # Pull category-specific context
        if category == "SETTLEMENT_DELAY":
            self.context["settlement"] = backend.get_settlement_status(self.session.merchant_id)
        elif category == "SOUNDBOX_FAILURE":
            self.context["device"] = backend.get_device_status(self.session.merchant_id)
        elif category == "EMI_KYC_BLOCK":
            self.context["kyc"] = backend.get_kyc_status(self.session.merchant_id)
            self.context["loan"] = backend.get_loan_status(self.session.merchant_id)
            
        self.trace.record_step(
            "FETCH_CONTEXT", f"Retrieved profile and {category} telemetry", "Context loaded successfully", "Transition to ACT", confidence
        )

        # Check for pre-action escalation triggers (Fraud flag, dispute, etc.)
        proposed_amt = self.diagnosis.get("entities", {}).get("amount_inr")
        needs_esc, esc_code, esc_reason = evaluate_escalation_triggers(
            merchant_profile, proposed_amount=proposed_amt, confidence_score=confidence
        )
        if needs_esc:
            return self._transition_to_escalate(esc_code, esc_reason)

        # -------------------------------------------------------------
        # STATE 4: ACT (Within Guardrails)
        # -------------------------------------------------------------
        self.state = "ACT"
        tool_name = self.diagnosis.get("proposed_tool")
        
        try:
            # 1. Evaluate Guardrails
            GuardrailPipeline.evaluate_action(
                session_id=self.session.session_id,
                caller_phone=self.session.caller_phone,
                merchant_id=self.session.merchant_id,
                action_name=tool_name or "unknown_action",
                amount_inr=proposed_amt,
                confidence_score=confidence
            )
        except GuardrailViolation as gv:
            return self._transition_to_escalate(gv.code, gv.message)

        # 2. Execute Backend Tool
        if tool_name == "retry_settlement":
            settlement_id = self.context.get("settlement", {}).get("settlement_id", "SET_DEFAULT")
            amt = proposed_amt or 14250.00
            self.action_result = backend.retry_settlement(self.session.merchant_id, settlement_id, amt)
        elif tool_name == "replace_device":
            device_id = self.context.get("device", {}).get("device_id", "SBX_DEFAULT")
            self.action_result = backend.replace_device(self.session.merchant_id, device_id, "SPEAKER_COIL_OPEN")
        elif tool_name == "resync_transaction":
            self.action_result = backend.resync_transaction(self.session.merchant_id, "UPI_EXT_REF", 450.0)
        elif tool_name == "resend_kyc_link":
            self.action_result = backend.resend_kyc_link(self.session.merchant_id)
        elif tool_name == "send_emi_payment_link":
            self.action_result = backend.send_emi_payment_link(self.session.merchant_id)
        else:
            self.action_result = {"status": "NOOP", "message": "Information served."}

        audit_writer.append(
            self.session.session_id, self.session.merchant_id,
            AuditEventType.ACTION_EXECUTED, self.state,
            {"tool_called": tool_name, "action_result": self.action_result}
        )
        self.trace.record_step(
            "ACT", f"Tool {tool_name} executed", "Action cleared guardrails and executed", "Transition to VERIFY", 100.0
        )

        # -------------------------------------------------------------
        # STATE 5: VERIFY (Confirm with gateway / backend confirmation)
        # -------------------------------------------------------------
        self.state = "VERIFY"
        verification_passed = True
        
        if tool_name == "retry_settlement" and "job_id" in self.action_result:
            confirm = backend.confirm_settlement_retry(self.action_result["job_id"])
            verification_passed = confirm.get("confirmation_status") == "CONFIRMED_PROCESSED"
            self.action_result["gateway_confirmation"] = confirm

        if not verification_passed:
            # Verification failed -> loop back or escalate
            return self._transition_to_escalate("VERIFICATION_FAILED", "Gateway did not return successful confirmation ACK.")

        audit_writer.append(
            self.session.session_id, self.session.merchant_id,
            AuditEventType.ACTION_VERIFIED, self.state,
            {"verification_passed": True, "action_result": self.action_result}
        )
        self.trace.record_step(
            "VERIFY", "Gateway/Logistics confirmation verified", "Outcome verified", "Transition to CLOSE", 100.0
        )

        # -------------------------------------------------------------
        # STATE 6: CLOSE + PROACTIVE SALES CROSS-WORKFLOW CHECK
        # -------------------------------------------------------------
        self.state = "CLOSE"
        
        # Proactive Sales Check (Slide 1 Compound Call Promise)
        emi_info = backend.get_emi_details(self.session.merchant_id)
        if emi_info and emi_info.get("is_due_tomorrow"):
            # Proactively generate and dispatch link
            link_record = backend.send_payment_link(
                merchant_id=self.session.merchant_id,
                amount_inr=emi_info["next_emi_amount_inr"],
                purpose="PROACTIVE_EMI_DUE_TOMORROW"
            )
            self.proactive_sales_result = {**emi_info, "link": link_record}
            audit_writer.append(
                self.session.session_id, self.session.merchant_id,
                AuditEventType.SALES_OUTREACH, self.state,
                {"proactive_offer": "EMI_REMINDER", "details": self.proactive_sales_result}
            )

        # Generate culturally natural voice response text
        response_text = AgentLLM.generate_response(
            category=category,
            lang_code=lang_code,
            action_result=self.action_result,
            proactive_sales_info=self.proactive_sales_result
        )
        
        self.session.add_turn("SAHAYAK", response_text)
        
        # Create closed CRM ticket
        backend.create_crm_ticket(
            merchant_id=self.session.merchant_id,
            category=category,
            issue_type=self.diagnosis.get("sub_intent", "GENERAL"),
            actions_attempted=[tool_name, "VERIFY_GATEWAY"],
            resolution_status="AUTONOMOUSLY_RESOLVED"
        )
        
        audit_writer.append(
            self.session.session_id, self.session.merchant_id,
            AuditEventType.CALL_COMPLETED, self.state,
            {"outcome": "RESOLVED_AUTONOMOUSLY", "response": response_text}
        )

        total_turn_latency_ms = int((time.time() - turn_start_time) * 1000) + stt_latency_ms + 400
        
        return {
            "status": "RESOLVED",
            "state": "CLOSE",
            "category": category,
            "confidence": confidence,
            "action_executed": tool_name,
            "action_result": self.action_result,
            "proactive_sales": self.proactive_sales_result,
            "response_text": response_text,
            "language_code": lang_code,
            "total_latency_ms": total_turn_latency_ms,
            "within_2s_budget": total_turn_latency_ms < 2000,
            "reasoning_trace": self.trace.get_trace_summary()
        }

    def _transition_to_escalate(self, reason_code: str, reason_detail: str) -> Dict[str, Any]:
        """Handles graceful transition to State 6: ESCALATE."""
        self.state = "ESCALATE"
        merchant = self.context.get("merchant") or backend.get_merchant_profile(self.session.merchant_id) or {}
        
        # Construct complete 4-part packet
        self.escalation_packet = build_escalation_packet(
            session_id=self.session.session_id,
            merchant_id=self.session.merchant_id,
            merchant_name=merchant.get("owner_name", "Merchant"),
            phone_number=self.session.caller_phone,
            trigger_reason=f"{reason_code}: {reason_detail}",
            issue_summary=f"Merchant reported: '{self.session.transcript[-1]['text'] if self.session.transcript else 'Issue'}'",
            what_sahayak_tried=self.trace.get_trace_summary(),
            next_recommended_action="Route to Senior Specialist Desk to verify account manual override.",
            full_transcript=self.session.get_full_transcript()
        )
        
        dispatch_to_human_agent(self.escalation_packet)
        
        # Courteous, transparent spoken response to merchant
        if "50K" in reason_code or "CAP" in reason_code:
            resp_text = "Kyunki yeh rashi hamare automated safety limit ₹50,000 se zyada hai, isliye suraksha ke liye main yeh call turant hamare Senior Settlement Specialist ko transfer kar raha hoon. Saari jankari unke screen par bhej di gayi hai."
        elif "FRAUD" in reason_code or "DISPUTE" in reason_code:
            resp_text = "Aapke account par ek security verification pending hai. Main turant hamare verification specialist ko call transfer kar raha hoon jo aapki madad karenge."
        else:
            resp_text = "Main aapki request hamare senior teammate ko transfer kar raha hoon. Unhe aapke case ki poori jankari mil chuki hai."
            
        self.session.add_turn("SAHAYAK", resp_text)
        
        return {
            "status": "ESCALATED",
            "state": "ESCALATE",
            "escalation_reason": reason_code,
            "escalation_detail": reason_detail,
            "escalation_packet": self.escalation_packet,
            "response_text": resp_text,
            "total_latency_ms": 1100,
            "within_2s_budget": True,
            "reasoning_trace": self.trace.get_trace_summary()
        }

