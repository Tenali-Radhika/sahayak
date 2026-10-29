"""
Sahayak - Production-Grade FastAPI Mission Control Server
Team Paytm Power Rangers | Track 3: Autonomous AI Teammates
Exposes:
- UI Dashboard at http://localhost:8000/
- 6 Paytm Mock API Surfaces at /api/v1/
- Agent Live Turn Runner at /api/v1/agent/turn
- Live Append-Only Audit Stream at /api/v1/audit/stream
- Benchmark Test Runner at /api/v1/eval/run
"""

import os
from typing import Dict, Any, Optional
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

import mock_backend as backend
from agent.conversation import ConversationSession
from agent.state_machine import AgentStateMachine
from audit.viewer import get_live_audit_feed
from eval.runner import run_benchmark_suite

app = FastAPI(
    title="Sahayak - Autonomous AI Teammate API",
    description="Backend for Track 3: Autonomous AI Teammates (Paytm AI Hackathon)",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request schemas
class AgentTurnRequest(BaseModel):
    merchant_id: str = "M_1092"
    caller_phone: str = "+919876543210"
    utterance: str = "Bhaiya, kal ka paisa abhi tak nahi aaya."
    language_code: str = "hi-IN"


class RetrySettlementRequest(BaseModel):
    settlement_id: str
    requested_amount_inr: float


# Serve UI Root
@app.get("/", response_class=HTMLResponse)
def read_root():
    ui_path = os.path.join(os.path.dirname(__file__), "ui", "index.html")
    if os.path.exists(ui_path):
        with open(ui_path, "r", encoding="utf-8") as f:
            return f.read()
    return "<h1>Sahayak Backend Running. UI file not found.</h1>"


# ------------------------------------------------------------------------------
# AGENT INTERFACE
# ------------------------------------------------------------------------------
@app.post("/api/v1/agent/turn")
def execute_agent_turn(req: AgentTurnRequest):
    """Executes the 6-state autonomous cycle for the merchant utterance."""
    session = ConversationSession(merchant_id=req.merchant_id, caller_phone=req.caller_phone)
    sm = AgentStateMachine(session)
    result = sm.execute_turn(req.utterance, lang_code=req.language_code)
    return result


@app.get("/api/v1/audit/stream")
def get_audit_stream():
    """Returns the latest append-only audit entries for the live UI feed."""
    return get_live_audit_feed(limit=30)


@app.post("/api/v1/eval/run")
def trigger_eval_run():
    """Runs the 20-scenario benchmark suite programmatically."""
    scorecard = run_benchmark_suite()
    return scorecard


# ------------------------------------------------------------------------------
# LAYER 4: 6 PAYTM MOCK API SURFACES
# ------------------------------------------------------------------------------

# 4a: Merchant Profile & KYC
@app.get("/api/v1/merchant/{merchant_id}/profile")
def api_get_profile(merchant_id: str):
    profile = backend.get_merchant_profile(merchant_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Merchant not found")
    return profile


@app.get("/api/v1/merchant/{merchant_id}/kyc")
def api_get_kyc(merchant_id: str):
    kyc = backend.get_kyc_status(merchant_id)
    if not kyc:
        raise HTTPException(status_code=404, detail="Merchant not found")
    return kyc


@app.post("/api/v1/merchant/{merchant_id}/kyc/resend-link")
def api_resend_kyc(merchant_id: str):
    return backend.resend_kyc_link(merchant_id)


# 4b: Settlement & Payment Gateway
@app.get("/api/v1/settlement/{merchant_id}/status")
def api_get_settlement(merchant_id: str):
    settlement = backend.get_settlement_status(merchant_id)
    if not settlement:
        raise HTTPException(status_code=404, detail="No settlement record")
    return settlement


@app.post("/api/v1/settlement/{merchant_id}/retry")
def api_retry_settlement(merchant_id: str, req: RetrySettlementRequest):
    return backend.retry_settlement(merchant_id, req.settlement_id, req.requested_amount_inr)


@app.get("/api/v1/settlement/{merchant_id}/retry/confirm")
def api_confirm_retry(merchant_id: str, job_id: str):
    return backend.confirm_settlement_retry(job_id)


# 4c: Device & Logistics
@app.get("/api/v1/device/{merchant_id}/status")
def api_get_device(merchant_id: str):
    return backend.get_device_status(merchant_id)


@app.post("/api/v1/device/{merchant_id}/replace")
def api_replace_device(merchant_id: str, fault_reason: str = "SPEAKER_FAULT"):
    return backend.replace_device(merchant_id, f"SBX_{merchant_id[-4:]}", fault_reason)


@app.get("/api/v1/device/{merchant_id}/logistics")
def api_device_logistics(merchant_id: str, order_id: Optional[str] = None):
    return backend.get_device_logistics(merchant_id, order_id)


# 4d: Loan & EMI Management
@app.get("/api/v1/loan/{merchant_id}/status")
def api_get_loan(merchant_id: str):
    loan = backend.get_loan_status(merchant_id)
    if not loan:
        raise HTTPException(status_code=404, detail="No active loan")
    return loan


@app.get("/api/v1/loan/{merchant_id}/emi")
def api_get_emi(merchant_id: str):
    return backend.get_emi_details(merchant_id)


@app.post("/api/v1/loan/{merchant_id}/emi/send-link")
def api_send_emi_link(merchant_id: str):
    return backend.send_emi_payment_link(merchant_id)


# 4e: CRM & Ticketing
@app.post("/api/v1/crm/ticket/create")
def api_create_ticket(merchant_id: str, category: str, issue_type: str):
    return backend.create_crm_ticket(merchant_id, category, issue_type, ["AUTONOMOUS_ACTION"])


# 4f: Sales Outreach & Payment Links
@app.post("/api/v1/sales/payment-link/send")
def api_send_payment_link(merchant_id: str, amount_inr: float = 3200.0, purpose: str = "PROACTIVE_EMI"):
    return backend.send_payment_link(merchant_id, amount_inr, purpose)


@app.post("/api/v1/sales/nudge/trigger")
def api_trigger_nudge(merchant_id: str, campaign_type: str = "SOUNDBOX_4G_UPGRADE"):
    return backend.trigger_nudge(merchant_id, campaign_type)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True)
