# Sahayak — Live Pitch, Demo Scripts & Judge Runbook

### Team Paytm Power Rangers | Lankipalli Tharun · Radhika Tenali
### Paytm AI Hackathon · Track 3: Autonomous AI Teammates

> **The Hackathon Winning Principle:** *"The live call is everything. Two workflows, zero humans, zero slides during the live call."*

---

## 1. Demo Architecture & Screen Setup

For the live pitch to the judges, the screen should display a **3-Pane Split View**:

```
+-----------------------------------------------------------------------------------+
|                            SAHAYAK MISSION CONTROL                                |
+-------------------------+-------------------------------+-------------------------+
|      PANE 1: PHONE      |      PANE 2: AGENT BRAIN      |   PANE 3: AUDIT & OPS   |
|                         |                               |                         |
| [ Merchant Caller UI ]  | State: [ DIAGNOSE ]           | Live Append-Only Stream |
| Audio Waveform: ~~~~~~  | Confidence: 96%               | [16:20:01] INBOUND CALL |
|                         | FSM: LISTEN -> DIAG -> ACT    | [16:20:02] G1 PASSED    |
| Live Transcript:        |                               | [16:20:03] G2 PASSED    |
| "Bhaiya, kal ka paisa   | Tool Called:                  | [16:20:04] G3 PASSED    |
|  nahi aaya..."          | > retry_settlement(14250)     | [16:20:05] RETRY QUEUED |
|                         | Gateway ACK: CONFIRMED ✅     | [16:20:06] SMS LINK SENT|
| Speaker: Sarvam Bulbul  |                               |                         |
| Latency: 1.48s ⚡       | Proactive Cross-Sell:         | Active Guardrails:      |
|                         | > EMI Due: ₹3,200             | [₹50K Cap: OK]          |
|                         | > Link Dispatched ✅          | [Fraud Check: CLEAN]    |
+-------------------------+-------------------------------+-------------------------+
```

---

## 2. Scenario 1: The Signature Live Call (Slide 1 Compound Demo)

> **Goal:** Demonstrate **CS Resolution + Proactive Sales Cross-Sell** in a single autonomous call in **Hindi** with zero human intervention.

* **Merchant Profile:** `M_1092` (Ramesh Sharma, Indiranagar)
* **Pre-condition:** Settlement of ₹14,250 delayed due to Bank Holiday. EMI of ₹3,200 due tomorrow.

### Turn-by-Turn Dialogue & System Reactions

#### Turn 1: Inbound Problem Statement
* **Merchant Speaks (into mic):**
  > *"Bhaiya, kal ka paisa abhi tak nahi aaya. Dukan kholne ke liye samaan lana hai, kya problem hai?"*
* **System Telemetry on Screen:**
  * **Sarvam STT:** Detects `hi-IN` · Latency: 420ms.
  * **Agent Core:** State changes: `LISTEN` $\rightarrow$ `DIAGNOSE`.
  * **Confidence Gauge:** Jumps to **96%** (Category: `SETTLEMENT_DELAY`).
  * **State:** `FETCH_CONTEXT` $\rightarrow$ Calls `GET /settlement/M_1092/status` $\rightarrow$ Returns `₹14,250, BANK_HOLIDAY`.
* **Guardrail Pipeline Fires:**
  * Caller verified? ✅ (+919876543210 matches M_1092)
  * Fraud flag? ✅ (Clean)
  * Confidence $\ge$ 80%? ✅ (96%)
  * Amount $\le$ ₹50,000? ✅ (₹14,250 is well below cap)
* **State `ACT`:** Calls `POST /settlement/M_1092/retry` $\rightarrow$ Queued for 6:00 AM.
* **State `VERIFY`:** Calls `GET /settlement/M_1092/retry/confirm` $\rightarrow$ Gateway returns `CONFIRMED_PROCESSED`.
* **Cross-Workflow Proactive Check (Sales):**
  * Calls `GET /loan/M_1092/emi` $\rightarrow$ Detects EMI ₹3,200 due tomorrow (`2026-10-30`).
  * Calls `POST /sales/payment-link/send` $\rightarrow$ Returns SMS confirmation.
* **Sarvam TTS Audio (Played on speaker):**
  > *"Namaste Ramesh ji! Kal bank holiday hone ki wajah se ₹14,250 ka settlement ruka hua tha. Humne kal subah 6 baje ke liye retry schedule kar diya hai aur payment gateway se confirmation aa chuka hai. Aapko callback ki bilkul zaroorat nahi hai — kaam ho gaya hai!*
  > 
  > *Aur Ramesh ji, aapki loan EMI ₹3,200 kal due hai, uska payment link maine aapke WhatsApp aur SMS par bhej diya hai taaki aapka credit score badhiya rahe."*
* **Turn Latency:** **1.62 seconds** (Well within the $<2\text{s}$ design target).

---

## 3. Scenario 2: Multilingual Support (Kannada Demo)

> **Goal:** Prove Sarvam AI's purpose-built Indian speech model on regional languages.

* **Merchant Profile:** `M_1092`
* **Merchant Speaks (Kannada):**
  > *"Namaskara, nanna soundbox belaggeyinda mathadtha illa. Yenu madodu?"*
  > *(Hello, my soundbox is not speaking since morning. What should I do?)*
* **System Telemetry:**
  * **Sarvam STT:** Detects `kn-IN` · Latency: 440ms.
  * **Diagnosis:** `DEVICE_FAILURE` (Confidence: 94%).
  * **Action:** Queries `/device/M_1092/status` $\rightarrow$ Detects `SPEAKER_COIL_OPEN`.
  * **Action:** Calls `POST /device/M_1092/replace` $\rightarrow$ Generates replacement order.
  * **Action:** Calls `GET /device/M_1092/logistics` $\rightarrow$ Returns ETA tomorrow 2 PM.
* **Sarvam TTS Audio (Kannada):**
  > *"Namaskara Ramesh avare! Nimma Soundbox speaker alli samasye ide. Naavu hosa Soundbox dispatch madiddive. Nale madhyahna 2 gante olage nimma dukanige talupatte. Tracking link SMS moolaka kalisiddene."*

---

## 4. Scenario 3: Safety & Senior Teammate Escalation (Judge Stress Test)

> **Goal:** Prove **Guardrail Layer Gate 4 (₹50K Cap)** and **Senior Teammate Escalation (USP #3)**.

* **Merchant Profile:** `M_8819` (Vikram Singh)
* **Pre-condition:** Attempting to clear an unauthorized high-value batch of ₹1,20,000.

### Dialogue & System Reactions
* **Merchant Speaks:**
  > *"Mera ₹1,20,000 ka settlement ruka hai! Abhi ke abhi mere account mein transfer karo, nahi toh main Paytm band kar dunga!"*
* **System Telemetry:**
  * **Agent Core:** State: `DIAGNOSE` $\rightarrow$ Proposes `retry_settlement(amount=120000)`.
  * **Guardrail Gate 4 Check:**
    $$\text{Amount requested: ₹1,20,000} > \text{₹50,000 Hard Limit}$$
    **RESULT: ❌ BLOCKED! VIOLATION: `EXCEEDS_HARD_CAP`.**
  * **System Decision:** DO NOT RETRY. TRANSITION TO `ESCALATE`.
* **Screen Visual Cue:**
  * Left pane turns subtle amber/red banner: `GUARDRAIL TRIGGERED: ₹50,000 CAP`.
  * Right pane pops up the **Escalation Packet Modal**:
    * **Issue:** ₹1,20,000 settlement hold.
    * **What Sahayak Checked:** Account active, batch status risk hold.
    * **Why Blocked:** Amount exceeds ₹50K autonomous limit.
    * **Next Recommended Action:** Route to Priority Banking Desk for manual token authorization.
    * **Full Transcript:** Attached.
* **Sarvam TTS Audio:**
  > *"Vikram ji, main dekh sakta hoon ki aapka ₹1,20,000 ka settlement ruka hua hai. Kyunki yeh rashi hamare automated safety limit ₹50,000 se zyada hai, isliye suraksha ke liye main yeh call turant hamare Senior Settlement Specialist ko transfer kar raha hoon. Maine saari jankari unke screen par bhej di hai, aapko dobara batana nahi padega."*
* **Judge Takeaway:** *"The AI never hallucinated or gave away money it wasn't allowed to touch. And the human agent never starts from zero."*

---

## 5. Judge Q&A Defense Sheet

| Potential Judge Question | Sahayak Winning Answer |
|--------------------------|------------------------|
| **"What if the merchant tries to jailbreak the AI to refund money?"** | "The LLM does not execute money actions directly. It only produces a proposed tool call. The proposal must pass our deterministic Guardrail Layer in Python code—verifying caller ID, checking fraud flags, and enforcing the ₹50K hard cap. Prompts can be fooled; hard-coded arithmetic gates cannot." |
| **"Why Sarvam AI instead of OpenAI Whisper/GPT-4o?"** | "Indian merchants don't speak textbook English or formal Hindi. They speak code-mixed language like *'Bhaiya kal ka settlement nahi aaya'*. Sarvam AI is trained natively on Indian merchant accents and dialects, and delivers the sub-2s voice latency required for natural merchant phone calls." |
| **"How do you justify your ₹5–15 pricing model?"** | "Paytm spends ₹339 Cr every quarter on sales and service. A human customer support call costs approximately ₹40–₹60. At ₹10 per resolved ticket, Paytm cuts resolution cost by 75% while Sahayak operates 24/7." |
| **"What happens if Sarvam AI or the internet lags?"** | "We have built local cached audio fallbacks in `demo/assets` and pre-rendered Web Audio buffers. The live demo can run purely on cloud API, but if conference Wi-Fi fails, the demo switches to the offline harness without breaking." |

---

*Keep this runbook open on a second device or printed during the hackathon demo.*

