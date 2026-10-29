"""
Sahayak - Guardrail Pipeline Orchestrator
Executes all 5 gates in deterministic order before any backend action.
Logs every check to the append-only audit trail.
"""

from typing import Dict, Any, Optional
from guardrails.caller_verify import verify_caller_identity
from guardrails.fraud_check import check_fraud_and_risk
from guardrails.confidence_gate import check_confidence_threshold
from guardrails.amount_cap import check_amount_cap
from guardrails.idempotency import check_idempotency
from audit.writer import audit_writer
from audit.schema import AuditEventType


class GuardrailViolation(Exception):
    """Raised when an action violates safety gates."""
    def __init__(self, code: str, message: str, gate_number: int):
        self.code = code
        self.message = message
        self.gate_number = gate_number
        super().__init__(message)


class GuardrailPipeline:
    """Deterministic orchestrator for all 5 safety barriers."""

    @staticmethod
    def evaluate_action(
        session_id: str,
        caller_phone: str,
        merchant_id: str,
        action_name: str,
        amount_inr: Optional[float] = None,
        confidence_score: float = 100.0,
        action_key: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Executes Gate 1 -> Gate 2 -> Gate 3 -> Gate 4 -> Gate 5.
        Returns evaluation record if all pass; raises GuardrailViolation if any fails.
        """
        eval_record = {
            "action_name": action_name,
            "merchant_id": merchant_id,
            "caller_phone": caller_phone,
            "amount_inr": amount_inr,
            "confidence_score": confidence_score,
            "gates_passed": []
        }

        # Gate 1: Caller ID Verification
        g1_passed, g1_msg = verify_caller_identity(caller_phone, merchant_id)
        if not g1_passed:
            audit_writer.append(
                session_id, merchant_id, AuditEventType.GUARDRAIL_VIOLATION, "GUARDRAIL",
                {"gate": 1, "code": "CALLER_ID_MISMATCH", "reason": g1_msg, "action": action_name}
            )
            raise GuardrailViolation("CALLER_ID_MISMATCH", g1_msg, 1)
        eval_record["gates_passed"].append("GATE_1_CALLER_VERIFIED")

        # Gate 2: Fraud & Risk Flag Pre-check
        g2_passed, g2_msg = check_fraud_and_risk(merchant_id)
        if not g2_passed:
            code = g2_msg.split(":")[0]
            audit_writer.append(
                session_id, merchant_id, AuditEventType.GUARDRAIL_VIOLATION, "GUARDRAIL",
                {"gate": 2, "code": code, "reason": g2_msg, "action": action_name}
            )
            raise GuardrailViolation(code, g2_msg, 2)
        eval_record["gates_passed"].append("GATE_2_FRAUD_CLEAN")

        # Gate 3: Confidence Threshold Gate
        g3_passed, g3_msg = check_confidence_threshold(confidence_score)
        if not g3_passed:
            audit_writer.append(
                session_id, merchant_id, AuditEventType.GUARDRAIL_VIOLATION, "GUARDRAIL",
                {"gate": 3, "code": "CONFIDENCE_BELOW_THRESHOLD", "reason": g3_msg, "action": action_name}
            )
            raise GuardrailViolation("CONFIDENCE_BELOW_THRESHOLD", g3_msg, 3)
        eval_record["gates_passed"].append("GATE_3_CONFIDENCE_ADEQUATE")

        # Gate 4: ₹50,000 Hard Limit Cap (if monetary action)
        if amount_inr is not None and amount_inr > 0:
            g4_passed, g4_msg = check_amount_cap(amount_inr)
            if not g4_passed:
                audit_writer.append(
                    session_id, merchant_id, AuditEventType.GUARDRAIL_VIOLATION, "GUARDRAIL",
                    {"gate": 4, "code": "AMOUNT_EXCEEDS_50K_CAP", "reason": g4_msg, "amount": amount_inr, "action": action_name}
                )
                raise GuardrailViolation("AMOUNT_EXCEEDS_50K_CAP", g4_msg, 4)
            eval_record["gates_passed"].append("GATE_4_AMOUNT_WITHIN_CAP")

        # Gate 5: Idempotency & Reversibility
        key = action_key or f"{merchant_id}:{action_name}:{amount_inr}"
        g5_passed, g5_msg = check_idempotency(key)
        if not g5_passed:
            audit_writer.append(
                session_id, merchant_id, AuditEventType.GUARDRAIL_VIOLATION, "GUARDRAIL",
                {"gate": 5, "code": "DUPLICATE_ACTION_BLOCKED", "reason": g5_msg, "action": action_name}
            )
            raise GuardrailViolation("DUPLICATE_ACTION_BLOCKED", g5_msg, 5)
        eval_record["gates_passed"].append("GATE_5_IDEMPOTENT")

        # Log clean pass to audit log
        audit_writer.append(
            session_id, merchant_id, AuditEventType.GUARDRAIL_EVALUATION, "GUARDRAIL",
            {"status": "PASSED", "eval_record": eval_record}
        )
        return eval_record
