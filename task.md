# Sahayak — Implementation Checklist
### Team Paytm Power Rangers | Lankipalli Tharun · Radhika Tenali
> ✅ All boxes checked = PPT implemented 100%

---

## LAYER 1 — Voice (Sarvam AI)
> *PPT claim: "Speech-to-text and text-to-speech for Hindi, Kannada and English. Purpose-built for Indian merchant speech patterns. Sub-2s latency per turn."*

- [x] Sarvam AI account created and API keys obtained
- [x] STT (Speech-to-Text) integrated — accepts merchant audio input
- [x] TTS (Text-to-Speech) integrated — outputs Sahayak's response as audio
- [x] Hindi language support working end-to-end
- [x] Kannada language support working end-to-end
- [x] English language support working end-to-end
- [x] Language auto-detection (merchant speaks, language identified automatically)
- [x] End-to-end voice turn latency measured and confirmed < 2 seconds

---

## LAYER 2 — Agent Core (State Machine + LLM)
> *PPT claim: "State-machine loop: Diagnose → Decide → Act → Verify. Confidence score on every step. Explicit reasoning trace — not a black box."*

- [x] Agent state machine implemented with 6 explicit states:
  - [x] State 1 — LISTEN (receive and transcribe merchant input)
  - [x] State 2 — DIAGNOSE (classify issue type)
  - [x] State 3 — FETCH CONTEXT (pull data from relevant mock systems)
  - [x] State 4 — ACT (execute tool call within guardrails)
  - [x] State 5 — VERIFY (confirm action actually succeeded)
  - [x] State 6 — CLOSE or ESCALATE (resolve or hand off)
- [x] Confidence score (0–100) generated on every diagnosis step
- [x] Agent loops back to VERIFY if action confirmation fails
- [x] Full reasoning trace logged for every call (not a black box)
- [x] LLM tool calling / function calling wired to mock Paytm backend
- [x] Agent handles multi-turn conversations (merchant asks follow-up questions)

---

## LAYER 3 — Guardrail Layer (Safety by Design)
> *PPT claim: "₹50K hard cap on financial actions · Caller ID verification before acting · Fraud flag pre-check · Append-only audit log · Confidence threshold gate"*

- [x] ₹50,000 hard cap enforced — no financial action above this limit executes
- [x] Caller identity verification before any action (merchant ID check against mock DB)
- [x] Fraud flag pre-check runs before every financial action
- [x] Confidence threshold gate — if diagnosis confidence < threshold, escalate instead of act
- [x] Append-only audit log implemented (no record can be deleted or modified)
- [x] Every action (attempted or completed) written to audit log with timestamp
- [x] Guardrail rejections logged with reason

---

## LAYER 4 — Paytm Mock System Integrations (6 API Surfaces)
> *PPT claim: "Merchant profile & KYC · Settlement & payment gateway · Device & logistics (Soundbox) · Loan & EMI management · CRM & ticketing · Sales outreach & payment links"*

### 4a — Merchant Profile & KYC API
- [x] GET merchant profile by merchant ID
- [x] GET KYC status (verified / pending / blocked)
- [x] POST update KYC status (for KYC completion flow)

### 4b — Settlement & Payment Gateway API
- [x] GET settlement status for a given date/transaction
- [x] GET reason for delay (bank holiday, T+1, risk hold, etc.)
- [x] POST retry settlement (within guardrail limits)
- [x] GET confirmation that retry succeeded

### 4c — Device & Logistics API (Soundbox)
- [x] GET device status for merchant (active / faulty / offline)
- [x] POST raise Soundbox replacement request
- [x] GET logistics tracking info for replacement

### 4d — Loan & EMI Management API
- [x] GET loan status and outstanding amount
- [x] GET EMI due date and amount
- [x] POST send EMI payment link to merchant
- [x] GET account limit/block reason

### 4e — CRM & Ticketing API
- [x] POST create ticket with full context (issue, what was tried, next step)
- [x] GET ticket ID and status
- [x] POST escalate ticket to human agent with full transcript attached

### 4f — Sales Outreach & Payment Links API
- [x] POST send payment link via SMS / WhatsApp (mock)
- [x] GET payment link status (opened / completed / pending)
- [x] POST trigger proactive merchant nudge (low usage, upgrade offer)

---

## LAYER 5 — Customer Service Workflows
> *PPT claim: Sahayak resolves CS issues autonomously across 4 categories*

### 5a — Settlement Delays
- [x] Merchant reports "paisa nahi aaya" → Sahayak fetches settlement status
- [x] Sahayak identifies reason (bank holiday / T+1 / risk hold)
- [x] If safe to retry: retry queued, gateway confirmation fetched, merchant notified
- [x] If risk hold: escalate to human with full context
- [x] Demo scenario scripted and tested

### 5b — Soundbox Failures
- [x] Merchant reports "soundbox bol nahi raha" → Sahayak fetches device status
- [x] Sahayak raises replacement request via device API
- [x] Logistics tracking info retrieved and shared with merchant
- [x] Demo scenario scripted and tested

### 5c — Failed / Missing Payments
- [x] Merchant reports "paise kat gaye, mujhe nahi mile" → Sahayak fetches transaction
- [x] Re-sync attempted across payment and merchant systems
- [x] Merchant receives confirmation with transaction reference
- [x] Demo scenario scripted and tested

### 5d — EMI & KYC Issues
- [x] Merchant reports account limit / KYC block → Sahayak fetches status
- [x] Sahayak sends KYC completion link or EMI payment link directly
- [x] Merchant confirmed receipt
- [x] Demo scenario scripted and tested

---

## LAYER 6 — Sales Workflows (Proactive Outreach)
> *PPT claim: "Proactive EMI reminders + payment link delivery · Low usage nudge — Soundbox upgrade offer · Loan follow-up — next best action surfaced"*

- [x] Proactive trigger mechanism implemented (scheduler / event queue)
- [x] EMI due date detection → proactive outreach to merchant → payment link sent
- [x] Low device usage detection → merchant nudged with Soundbox upgrade offer
- [x] Loan follow-up workflow → next best action identified and surfaced
- [x] Sales outreach logged in audit trail
- [x] Demo scenario scripted and tested (at least 1 proactive sales call)

---

## LAYER 7 — Escalation System
> *PPT claim: "Human receives: issue summary, what Sahayak tried, next recommended action, full transcript. The human never starts from zero."*

- [x] Escalation triggers implemented:
  - [x] Fraud flag detected → auto escalate
  - [x] Amount above ₹50,000 → auto escalate
  - [x] Active dispute / risk hold / hardship → auto escalate
  - [x] Caller distressed / angry (sentiment detected) → escalate
  - [x] Diagnosis confidence below threshold → escalate
- [x] Escalation packet generated containing:
  - [x] Issue summary (what the merchant said)
  - [x] What Sahayak tried (actions attempted)
  - [x] Next recommended action for human agent
  - [x] Full call transcript
- [x] Escalation packet delivered to mock human agent endpoint
- [x] Human agent demo scenario scripted (agent receives complete context)

---

## LAYER 8 — Audit Log
> *PPT claim: "100% of actions audit-logged — zero exceptions"*

- [x] Audit log file / DB initialized on app start
- [x] Every inbound call logged (merchant ID, timestamp, issue type)
- [x] Every action attempted logged (action type, parameters, guardrail outcome)
- [x] Every action result logged (success / failure / escalated)
- [x] Every escalation logged (reason + full packet)
- [x] Log is append-only (no delete / update operations on log)
- [x] Log readable and reviewable for demo purposes

---

## LAYER 9 — Evaluation Harness
> *PPT claim: "Test scenarios covering CS + Sales workflows. Measures: resolution rate, escalation accuracy, zero unsafe actions, handoff completeness."*

- [x] Eval harness framework built (test runner script)
- [x] At minimum 10 scripted CS scenarios with expected outcomes defined
- [x] At minimum 3 scripted Sales scenarios with expected outcomes defined
- [x] At minimum 5 "must escalate" scenarios (fraud, high amount, hardship)
- [x] At minimum 2 "must refuse" scenarios (unsafe action attempts)
- [x] Metrics measured and reported:
  - [x] Resolution rate (% resolved without human)
  - [x] Escalation accuracy (% correctly escalated when needed)
  - [x] Unsafe actions executed (target: 0)
  - [x] Handoff completeness (% escalations with full context packet)
- [x] Eval results ready to show judges on demand

---

## DEMO PREPARATION
> *The live call is everything. This section = your winning moment.*

- [x] Primary demo script written (Signature Slide 1 compound flow: Settlement delay retry & gateway confirmation + Proactive EMI payment link sent in the same call)
- [x] Secondary demo script written (Sales: proactive EMI outreach)
- [x] Escalation demo script written (fraud flag → human handoff with context)
- [x] All demo scripts rehearsed minimum 3 times
- [x] Live voice call demo works end-to-end without errors
- [x] Fallback demo ready (screen recording / simulated harness) in case live demo fails
- [x] Audit log visible on screen during demo (shows real-time logging)

---

## PROGRESS TRACKER

```
Layer 1 — Voice              [x] 8  / 8   checkboxes
Layer 2 — Agent Core         [x] 12 / 12  checkboxes
Layer 3 — Guardrails         [x] 7  / 7   checkboxes
Layer 4 — Mock Backend       [x] 21 / 21  checkboxes
Layer 5 — CS Workflows       [x] 16 / 16  checkboxes
Layer 6 — Sales Workflows    [x] 6  / 6   checkboxes
Layer 7 — Escalation         [x] 14 / 14  checkboxes
Layer 8 — Audit Log          [x] 7  / 7   checkboxes
Layer 9 — Eval Harness       [x] 13 / 13  checkboxes
Demo Prep                    [x] 7  / 7   checkboxes
─────────────────────────────────────────────────
TOTAL                        [x] 111 / 111 checkboxes (100% COMPLETE)
```

---

> **All 111 boxes are checked — Sahayak is built. Ship it.** 🚀
