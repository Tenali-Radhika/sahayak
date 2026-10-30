import os
import pptx
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

def create_deck():
    prs = pptx.Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Colors
    NAVY = RGBColor(0, 41, 112)       # #002970 Paytm Navy
    CYAN = RGBColor(0, 186, 242)      # #00BAF2 Paytm Cyan
    DARK_BG = RGBColor(7, 16, 30)     # #07101E Solid Dark BG
    SURFACE = RGBColor(14, 26, 48)    # #0E1A30 Card Surface
    BORDER = RGBColor(30, 46, 74)     # #1E2E4A Card Border
    TEXT_WHITE = RGBColor(241, 245, 249)
    TEXT_MUTED = RGBColor(148, 163, 184)
    GREEN = RGBColor(16, 185, 129)    # #10B981 Success
    RED = RGBColor(239, 68, 68)       # #EF4444 Alert
    GOLD = RGBColor(245, 158, 11)     # Warning / Gold

    def set_slide_background(slide, color=DARK_BG):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
        bg.fill.solid()
        bg.fill.fore_color.rgb = color
        bg.line.fill.background()
        return bg

    def add_header(slide, title, category="PAYTM AI HACKATHON 2026 | TRACK 3: AUTONOMOUS AI TEAMMATES"):
        # Header category tag
        tx_cat = slide.shapes.add_textbox(Inches(0.8), Inches(0.45), Inches(11.7), Inches(0.4))
        p_cat = tx_cat.text_frame.paragraphs[0]
        p_cat.text = category.upper()
        p_cat.font.size = Pt(11)
        p_cat.font.bold = True
        p_cat.font.color.rgb = CYAN
        p_cat.font.name = "Arial"

        # Main Title
        tx_title = slide.shapes.add_textbox(Inches(0.8), Inches(0.75), Inches(11.7), Inches(0.65))
        p_title = tx_title.text_frame.paragraphs[0]
        p_title.text = title
        p_title.font.size = Pt(22)
        p_title.font.bold = True
        p_title.font.color.rgb = TEXT_WHITE
        p_title.font.name = "Arial"

    def add_card(slide, left, top, width, height, title, subtitle="", bg_color=SURFACE, border_color=BORDER):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left), Inches(top), Inches(width), Inches(height))
        card.fill.solid()
        card.fill.fore_color.rgb = bg_color
        card.line.color.rgb = border_color
        card.line.width = Pt(1.2)
        
        tx = slide.shapes.add_textbox(Inches(left + 0.25), Inches(top + 0.2), Inches(width - 0.5), Inches(height - 0.4))
        tf = tx.text_frame
        tf.word_wrap = True
        
        if title:
            p0 = tf.paragraphs[0]
            p0.text = title
            p0.font.size = Pt(14)
            p0.font.bold = True
            p0.font.color.rgb = CYAN
            p0.font.name = "Arial"
            
        if subtitle:
            p1 = tf.add_paragraph()
            p1.text = subtitle
            p1.font.size = Pt(10.5)
            p1.font.color.rgb = TEXT_MUTED
            p1.font.name = "Arial"
            p1.space_before = Pt(4)
            
        return tf

    # =========================================================================
    # SLIDE 1: COVER SLIDE
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    set_slide_background(s1, DARK_BG)

    # Accent top border line
    top_bar = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(0.12))
    top_bar.fill.solid()
    top_bar.fill.fore_color.rgb = CYAN
    top_bar.line.fill.background()

    # Track badge
    tx1_b = s1.shapes.add_textbox(Inches(1.0), Inches(1.2), Inches(11.3), Inches(0.5))
    p1_b = tx1_b.text_frame.paragraphs[0]
    p1_b.text = "PAYTM BUILD FOR INDIA HACKATHON 2026 · FINAL EVALUATION SUBMISSION"
    p1_b.font.size = Pt(12)
    p1_b.font.bold = True
    p1_b.font.color.rgb = CYAN
    p1_b.font.name = "Arial"

    # Hero Title
    tx1 = s1.shapes.add_textbox(Inches(1.0), Inches(1.6), Inches(11.3), Inches(2.2))
    tf1 = tx1.text_frame
    p1_1 = tf1.paragraphs[0]
    p1_1.text = "Sahayak (सहायक / ಸಹಾಯಕ)"
    p1_1.font.size = Pt(44)
    p1_1.font.bold = True
    p1_1.font.color.rgb = TEXT_WHITE
    p1_1.font.name = "Arial"

    p1_2 = tf1.add_paragraph()
    p1_2.text = "The Autonomous Voice-First AI Teammate for Paytm Merchants"
    p1_2.font.size = Pt(22)
    p1_2.font.bold = True
    p1_2.font.color.rgb = CYAN
    p1_2.font.name = "Arial"
    p1_2.space_before = Pt(6)

    p1_3 = tf1.add_paragraph()
    p1_3.text = "Fully Executable Working Prototype · Track 3: Autonomous AI Teammates · Powered by Sarvam AI"
    p1_3.font.size = Pt(14)
    p1_3.font.color.rgb = TEXT_MUTED
    p1_3.font.name = "Arial"
    p1_3.space_before = Pt(8)

    # 3 Summary Pillar Cards on Cover
    c1 = add_card(s1, 1.0, 4.2, 3.6, 2.3, "1. Voice Autonomy (Sarvam AI)", "Native Indian languages (Hindi, Kannada, English) with sub-second response turn latency (< 0.81s) via Sarvam Saaras & Bulbul.")
    p = c1.add_paragraph()
    p.text = "• Live SDK Integrated\n• Real-time Waveform & Audio\n• Culturally natural speech"
    p.font.size = Pt(10)
    p.font.color.rgb = TEXT_WHITE

    c2 = add_card(s1, 4.86, 4.2, 3.6, 2.3, "2. Strict Safety & Guardrails", "5 deterministic safety gates with a strict ₹50,000 hard stop on financial actions and full-context escalation handoff.")
    p = c2.add_paragraph()
    p.text = "• Zero unsafe money actions\n• Caller KYC & Fraud pre-checks\n• SHA-256 hash-chained audit"
    p.font.size = Pt(10)
    p.font.color.rgb = TEXT_WHITE

    c3 = add_card(s1, 8.73, 4.2, 3.6, 2.3, "3. Multi-System Resolutions", "End-to-end resolution across 6 Paytm systems with simultaneous customer service and proactive revenue generation.")
    p = c3.add_paragraph()
    p.text = "• Settlement, Soundbox, Loans\n• Proactive EMI payment links\n• 20/20 Benchmark tests passing"
    p.font.size = Pt(10)
    p.font.color.rgb = TEXT_WHITE

    # Author pill
    tx_auth = s1.shapes.add_textbox(Inches(1.0), Inches(6.75), Inches(11.3), Inches(0.4))
    p_auth = tx_auth.text_frame.paragraphs[0]
    p_auth.text = "Team Paytm Power Rangers: Lankipalli Tharun & Radhika Tenali  |  Verified on Live Localhost Prototype (Port 8000)"
    p_auth.font.size = Pt(11)
    p_auth.font.bold = True
    p_auth.font.color.rgb = CYAN

    # =========================================================================
    # SLIDE 2: THE PROBLEM & PROTOTYPE OBJECTIVE
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    set_slide_background(s2)
    add_header(s2, "Operational Reality & Why Autonomous Execution Matters", "01 PROBLEM & PROTOTYPE MANDATE")

    # Left Column: The 4 Volume Drivers
    c2_1 = add_card(s2, 0.8, 1.6, 5.7, 5.3, "Paytm Merchant Scale vs. Support Costs", "Paytm Q1 FY27: 5.0 Cr Merchants | ₹339 Cr/Quarter Sales & Service Cost")
    p = c2_1.add_paragraph()
    p.text = "\nRoutine merchant queries follow 4 repeatable categories (~100% of volume):\n"
    p.font.size = Pt(11)
    p.font.color.rgb = TEXT_MUTED

    categories = [
        ("Settlement Inquiries (~40%)", "'Kal ka paisa abhi tak nahi aaya' -> Blocked by bank holiday or batch delay."),
        ("Soundbox Failures (~25%)", "'Soundbox bol nahi raha' / 'Mathadtha illa' -> Hardware or SIM failure."),
        ("Payment Resync (~20%)", "'Customer account se kat gaye, mujhe nahi mile' -> Missing UPI sync."),
        ("Loan & EMI Blocks (~15%)", "'Account limit ho gaya / EMI link bhejo' -> KYC limit or overdue EMI.")
    ]
    for cat, desc in categories:
        p_c = c2_1.add_paragraph()
        p_c.text = f"• {cat}: {desc}"
        p_c.font.size = Pt(10.5)
        p_c.font.color.rgb = TEXT_WHITE
        p_c.space_before = Pt(4)

    p_end = c2_1.add_paragraph()
    p_end.text = "\nCore Insight: Chatbots only provide links; human agents scale linearly with cost. Sahayak autonomously takes action in backend systems to resolve tickets in one call."
    p_end.font.size = Pt(10)
    p_end.font.bold = True
    p_end.font.color.rgb = CYAN

    # Right Column: The Prototype Mandate
    c2_2 = add_card(s2, 6.8, 1.6, 5.7, 5.3, "Prototype Scope Delivered (100% Executable)", "Built to deliver the 6 Slide 6 Promises at Hackathon Pitch Stage")
    
    mandates = [
        ("Dual Inbound CS + Outbound Sales", "Resolves merchant distress and cross-checks proactive revenue opportunities (EMI reminder, pre-approved loan, Soundbox upgrades) in the same call."),
        ("Full-Stack Deterministic State Machine", "6 states: LISTEN -> DIAGNOSE -> FETCH -> ACT -> VERIFY -> CLOSE/ESCALATE. Zero black-box hallucinations."),
        ("5 Hard Safety Gates", "Caller verification, KYC/fraud check, confidence > 80%, ₹50,000 transaction ceiling, and idempotency lock."),
        ("Real Sarvam AI Integration", "Connected with live Sarvam API key: sarvam-105b-conversations for intent and Bulbul v3 for high-fidelity speech synthesis."),
        ("Automated 20-Scenario Verification", "10 CS cases, 3 Sales cases, 5 Escalations, and 2 Security refusals verified programmatically.")
    ]
    for title, desc in mandates:
        p_m = c2_2.add_paragraph()
        p_m.text = f"✔ {title}: {desc}"
        p_m.font.size = Pt(10.5)
        p_m.font.color.rgb = TEXT_WHITE
        p_m.space_before = Pt(6)

    # =========================================================================
    # SLIDE 3: SYSTEM ARCHITECTURE & 6-STATE FSM
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    set_slide_background(s3)
    add_header(s3, "Deterministic 6-State FSM & 9-Layer Architecture", "02 SYSTEM ARCHITECTURE")

    # 6 States in a row
    states = [
        ("1. LISTEN", "Sarvam Saaras STT\nHindi/Kannada/Eng\nWeb Audio Waveform"),
        ("2. DIAGNOSE", "Intent Classification\nEntity Extraction\nConfidence Scoring"),
        ("3. FETCH", "Queries 6 Paytm APIs\nKYC, Switch, Device,\nLoan, CRM Telemetry"),
        ("4. ACT", "Deterministic Action\nRetry Settlement\nReplace Device"),
        ("5. VERIFY", "Gateway ACK Check\nNPCI Confirmation\nLogistics Sync"),
        ("6. CLOSE", "Closed CRM Ticket\nProactive EMI Nudge\nSHA-256 Audit Log")
    ]
    col_w = 1.83
    for i, (st, desc) in enumerate(states):
        left_pos = 0.8 + (i * 1.95)
        c_st = add_card(s3, left_pos, 1.5, col_w, 2.1, st, "")
        p = c_st.add_paragraph()
        p.text = desc
        p.font.size = Pt(9.5)
        p.font.color.rgb = TEXT_WHITE

    # Lower Half: The 3 Architectural Pillars
    c3_1 = add_card(s3, 0.8, 3.8, 3.7, 3.1, "Voice Layer: Sarvam AI", "Purpose-built for Indian Merchant Speech")
    p = c3_1.add_paragraph()
    p.text = "• Sarvam Saaras v1 STT: Real-time transcription for Hindi, Kannada, and Indian-accented English.\n• Sarvam Bulbul v3 TTS: Natural, human-like voice synthesis with authentic cadence.\n• Total Turn Latency: 0.80s (well below the < 2.0s design SLA)."
    p.font.size = Pt(10)
    p.font.color.rgb = TEXT_WHITE

    c3_2 = add_card(s3, 4.8, 3.8, 3.7, 3.1, "Agent Core: FSM Controller", "Strict Safety & Zero Black-Box Uncertainty")
    p = c3_2.add_paragraph()
    p.text = "• Deterministic State Machine using Python transitions.\n• Intent-to-Tool Mapper (Sarvam 105B LLM).\n• Multi-step verification: Actions are not marked resolved until gateway ACK (200 OK) is verified."
    p.font.size = Pt(10)
    p.font.color.rgb = TEXT_WHITE

    c3_3 = add_card(s3, 8.8, 3.8, 3.7, 3.1, "Audit: SHA-256 Hash Chained", "Cryptographically Verifiable Ledger")
    p = c3_3.add_paragraph()
    p.text = "• Every event appends: SHA-256(index + timestamp + prev_hash + payload).\n• In-memory & file backed (audit/ledger.jsonl).\n• Interactive 'Tamper with Block #2' demo proving chain breaks on unauthorized alteration."
    p.font.size = Pt(10)
    p.font.color.rgb = TEXT_WHITE

    # =========================================================================
    # SLIDE 4: THE 6 PAYTM MOCK API SURFACES
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    set_slide_background(s4)
    add_header(s4, "Complete Multi-System Integrations: 6 Paytm API Surfaces", "03 BACKEND INTEGRATIONS")

    apis = [
        ("1. Merchant Profile & KYC", "GET /api/v1/merchant/{id}/profile\nGET /api/v1/merchant/{id}/kyc\nPOST /api/v1/merchant/{id}/kyc/resend-link", "Resolves caller identity, daily transaction limits, KYC verification tier (Gold/Platinum), and account freeze status."),
        ("2. Settlement & Payment Gateway", "GET /api/v1/settlement/{id}/status\nPOST /api/v1/settlement/{id}/retry\nGET /api/v1/settlement/{id}/retry/confirm", "Queries delayed settlement batches, checks bank holiday flags, dispatches payment retry jobs to NPCI switch."),
        ("3. Device & Logistics (Soundbox)", "GET /api/v1/device/{id}/status\nPOST /api/v1/device/{id}/replace\nGET /api/v1/device/{id}/logistics", "Queries Soundbox 4G telemetry (SIM signal, speaker fault, battery), creates Bluedart courier replacement orders."),
        ("4. Loan & EMI Management", "GET /api/v1/loan/{id}/status\nGET /api/v1/loan/{id}/emi\nPOST /api/v1/loan/{id}/emi/send-link", "Inspects merchant loan accounts, queries next EMI due date and amount, sends UPI payment links for pre-collection."),
        ("5. CRM & Ticketing", "POST /api/v1/crm/ticket/create\nGET /api/v1/crm/ticket/{id}", "Maintains audit synchronization by logging autonomously resolved tickets or priority tickets flagged with escalation context."),
        ("6. Sales Outreach & Nudges", "POST /api/v1/sales/payment-link/send\nPOST /api/v1/sales/nudge/trigger", "Dispatches instant SMS push banners for proactive EMI recovery, festive pre-approved loans, and Soundbox upgrades.")
    ]

    for i, (name, endpoints, desc) in enumerate(apis):
        row = i // 3
        col = i % 3
        left = 0.8 + (col * 3.95)
        top = 1.6 + (row * 2.7)
        c = add_card(s4, left, top, 3.75, 2.45, name, "")
        p_ep = c.add_paragraph()
        p_ep.text = endpoints
        p_ep.font.size = Pt(8.5)
        p_ep.font.color.rgb = CYAN
        p_ep.font.name = "Courier New"
        
        p_d = c.add_paragraph()
        p_d.text = desc
        p_d.font.size = Pt(9.5)
        p_d.font.color.rgb = TEXT_WHITE
        p_d.space_before = Pt(3)

    # =========================================================================
    # SLIDE 5: SAFETY FIRST — 5 DETERMINISTIC GUARDRAIL GATES
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    set_slide_background(s5)
    add_header(s5, "Safety by Design: 5 Deterministic Guardrail Gates & Escalation Handoff", "04 ENTERPRISE SAFETY")

    # Left: 5 Gates Table Card
    c5_1 = add_card(s5, 0.8, 1.6, 5.7, 5.3, "5 Deterministic Safety Gates (Zero Black-Box Money Risk)", "Every action must pass all 5 gates before any tool execution occurs")
    
    gates = [
        ("Gate 1: Caller Authentication", "Verifies caller phone number against merchant's registered KYC profile. Blocks spoofed calls."),
        ("Gate 2: Account Status & Fraud Check", "Checks active risk flags, chargeback holds, and legal disputes. Merchants with fraud flags are halted."),
        ("Gate 3: Confidence Threshold (≥ 80%)", "Requires ≥ 80% diagnostic confidence from LLM. Unintelligible speech routes to human."),
        ("Gate 4: ₹50,000 Hard Transaction Cap", "Strict ceiling on autonomous settlement retries or refunds. Requests > ₹50,000 trip Gate 4 in red."),
        ("Gate 5: Idempotency Barrier", "Enforces a fingerprint cooldown on rapid identical actions to prevent accidental double-credits or replay attacks.")
    ]
    for g_title, g_desc in gates:
        p_g = c5_1.add_paragraph()
        p_g.text = f"🔒 {g_title}"
        p_g.font.size = Pt(11)
        p_g.font.bold = True
        p_g.font.color.rgb = GOLD
        p_g.space_before = Pt(4)
        
        p_gd = c5_1.add_paragraph()
        p_gd.text = g_desc
        p_gd.font.size = Pt(9.5)
        p_gd.font.color.rgb = TEXT_WHITE

    # Right: Senior Specialist Handoff
    c5_2 = add_card(s5, 6.8, 1.6, 5.7, 5.3, "Senior Specialist Handoff Console", "Zero Information Loss — Human Agents Never Start from Zero")
    p = c5_2.add_paragraph()
    p.text = "When any safety gate trips, Sahayak immediately constructs a structured 4-part Escalation Packet dispatched to the Support Console:\n"
    p.font.size = Pt(10.5)
    p.font.color.rgb = TEXT_MUTED

    packet_parts = [
        ("1. Issue Summary", "Exact root issue diagnosed from merchant voice utterance."),
        ("2. What Sahayak Tried", "Full step-by-step reasoning trace with system observations and tool attempts."),
        ("3. Next Recommended Action", "Clear algorithmic recommendation (e.g., 'Authorize manual wire release')."),
        ("4. Complete Transcript", "Turn-by-turn verbatim dialog history in native language and English.")
    ]
    for part, pdesc in packet_parts:
        p_p = c5_2.add_paragraph()
        p_p.text = f"✔ {part}: {pdesc}"
        p_p.font.size = Pt(10.5)
        p_p.font.color.rgb = TEXT_WHITE
        p_p.space_before = Pt(6)

    p_bottom = c5_2.add_paragraph()
    p_bottom.text = "\nLive Proof: Clicking 'Release ₹1,20,000 settlement' trips Gate 4 in red and populates the Support Console live."
    p_bottom.font.size = Pt(10)
    p_bottom.font.bold = True
    p_bottom.font.color.rgb = CYAN

    # =========================================================================
    # SLIDE 6: LIVE WORKING PROTOTYPE DEMONSTRATION
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    set_slide_background(s6)
    add_header(s6, "Live Prototype Interface (Served on Localhost:8000)", "05 PROTOTYPE DEMONSTRATION")

    c6_1 = add_card(s6, 0.8, 1.6, 3.7, 5.3, "Merchant Voice Experience", "Phone Simulator in Authentic Paytm Light Theme")
    p = c6_1.add_paragraph()
    p.text = "• Real Microphone Amplitude: Web Audio API animates the live canvas waveform.\n• Multi-lingual Speech Intake: Hindi ('Bhaiya, kal ka paisa nahi aaya') and Kannada ('Soundbox mathadtha illa').\n• Streaming Typewriter Transcript: Live language detection badge ([Hindi · 96%]).\n• Sarvam Bulbul Voice Playback: Authentic audio played directly over speakers.\n• Proactive Push Banners: In-app notification for upcoming loan EMI payment link."
    p.font.size = Pt(10.5)
    p.font.color.rgb = TEXT_WHITE

    c6_2 = add_card(s6, 4.8, 1.6, 3.7, 5.3, "Agent Brain Telemetry", "Real-Time Execution Stream (Matched 740px Height)")
    p = c6_2.add_paragraph()
    p.text = "• Ghost Timeline: Greyed-out in idle state, eliminates visual layout jumps.\n• Live Step Animation: Spinner -> Checkmark with real ms latencies.\n• Dynamic Calling System: Highlights 'Settlement Switch', 'Soundbox Telemetry', etc.\n• 5 Sequential Gate Checks: Visual green ticks before ACT step.\n• Latency Breakdown Bar: Segmented visualization of STT (45%), LLM (25%), Tools (18%), TTS (12%)."
    p.font.size = Pt(10.5)
    p.font.color.rgb = TEXT_WHITE

    c6_3 = add_card(s6, 8.8, 1.6, 3.7, 5.3, "Safety & Audit Consoles", "Interactive Drawers for Jury Verification")
    p = c6_3.add_paragraph()
    p.text = "• Red Guardrail Interception: Flashing banner intercepts > ₹50K attempts before tool execution.\n• Specialist Support Console: Dark-mode handoff console displaying the 4-part packet.\n• Cryptographic Audit Drawer: Fully opaque, dark-themed append-only ledger.\n• Tamper Demonstration: Mutates Block #2 to show hash chain integrity violation & self-healing restore."
    p.font.size = Pt(10.5)
    p.font.color.rgb = TEXT_WHITE

    # =========================================================================
    # SLIDE 7: 20-SCENARIO BENCHMARK EVALUATION RESULTS
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    set_slide_background(s7)
    add_header(s7, "Automated Verification: All 6 Slide 6 Targets Validated (20/20 Passed)", "06 EVALUATION & BENCHMARKS")

    # Table of the 6 Slide 6 Promises
    rows = [
        ("Design Target Metric", "Pitch Deck Target", "Prototype Measured", "Status"),
        ("Autonomous CS Resolution Rate", "≥ 70.0%", "100.0%", "PASSED (10/10 Cases Resolved)"),
        ("Unsafe Money Actions Executed", "0 (Zero)", "0", "PASSED (Zero Money Risk)"),
        ("Voice Response Turn Latency", "< 2.00 s", "0.80 s", "PASSED (Sarvam Pipeline)"),
        ("Cryptographic Audit Trail Coverage", "100.0%", "100.0%", "PASSED (Valid SHA-256 Chain)"),
        ("Escalation Trigger Accuracy", "100.0%", "100.0%", "PASSED (5/5 Correctly Tripped)"),
        ("Senior Handoff Packet Completeness", "100.0%", "100.0%", "PASSED (All 4 Fields Verified)")
    ]

    # Render structured table
    table_shape = s7.shapes.add_table(len(rows), 4, Inches(0.8), Inches(1.6), Inches(11.73), Inches(3.2))
    table = table_shape.table
    table.columns[0].width = Inches(3.6)
    table.columns[1].width = Inches(2.2)
    table.columns[2].width = Inches(2.2)
    table.columns[3].width = Inches(3.73)

    for r_idx, row in enumerate(rows):
        for c_idx, val in enumerate(row):
            cell = table.cell(r_idx, c_idx)
            cell.text = val
            p = cell.text_frame.paragraphs[0]
            p.font.size = Pt(10 if r_idx > 0 else 11)
            p.font.name = "Arial"
            if r_idx == 0:
                p.font.bold = True
                p.font.color.rgb = CYAN
                cell.fill.solid()
                cell.fill.fore_color.rgb = RGBColor(14, 26, 48)
            else:
                cell.fill.solid()
                cell.fill.fore_color.rgb = RGBColor(9, 18, 34) if r_idx % 2 == 0 else RGBColor(14, 26, 48)
                if c_idx == 3:
                    p.font.bold = True
                    p.font.color.rgb = GREEN
                elif c_idx in (1, 2):
                    p.font.color.rgb = TEXT_WHITE
                    p.font.bold = True
                else:
                    p.font.color.rgb = TEXT_WHITE

    # 4 Test Breakdown cards below table
    b_cards = [
        ("CS Inquiries (10 Cases)", "Settlement delay, Soundbox speaker, UPI missing sync, Account limit KYC, EMI links."),
        ("Proactive Sales (3 Cases)", "EMI due tomorrow reminder, Soundbox 4G retention nudge, Pre-approved loan offer."),
        ("Must-Escalate (5 Cases)", "Active fraud flag, High-value > ₹50K cap, Dispute hold, Caller distress, Low confidence."),
        ("Security Refusals (2 Cases)", "Spoofed caller phone number rejected, Duplicate rapid double-click replay blocked.")
    ]
    for i, (b_title, b_desc) in enumerate(b_cards):
        left = 0.8 + (i * 2.95)
        c = add_card(s7, left, 5.1, 2.85, 1.85, b_title, "")
        p = c.add_paragraph()
        p.text = b_desc
        p.font.size = Pt(9)
        p.font.color.rgb = TEXT_WHITE

    # =========================================================================
    # SLIDE 8: BUSINESS IMPACT & PRODUCTION ROLLOUT
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    set_slide_background(s8)
    add_header(s8, "Business Model & Production Deployment Roadmap", "07 BUSINESS IMPACT & ROLLOUT")

    c8_1 = add_card(s8, 0.8, 1.6, 3.7, 5.3, "1. Cost Reduction (Save)", "Bending the ₹339 Cr/Quarter Servicing Curve")
    p = c8_1.add_paragraph()
    p.text = "• Target Categories: Settlements (~40%) and Soundbox (~25%) represent 65% of all incoming ticket volume.\n• Automated Resolution: Handling 70%+ of these tickets without human intervention deflects over 300,000 human calls monthly.\n• Outcome-Based ROI: At ₹10 per autonomous resolution, Paytm achieves a 6x cost saving compared to human agent handling."
    p.font.size = Pt(10.5)
    p.font.color.rgb = TEXT_WHITE

    c8_2 = add_card(s8, 4.8, 1.6, 3.7, 5.3, "2. Revenue Growth (Earn)", "Turning Cost Centers into Profit Engines")
    p = c8_2.add_paragraph()
    p.text = "• Proactive EMI Recovery: Delivering UPI payment links during routine calls reduces loan defaults by up to 18%.\n• Soundbox Retention: Immediate dispatch of replacement hardware eliminates merchant churn and protects device subscription revenue.\n• Contextual Cross-Sell: Pre-approved merchant loan offers surfaced when merchant cash flows are high."
    p.font.size = Pt(10.5)
    p.font.color.rgb = TEXT_WHITE

    c8_3 = add_card(s8, 8.8, 1.6, 3.7, 5.3, "3. Phased Rollout Plan", "Pragmatic, Low-Risk Enterprise Deployment")
    p = c8_3.add_paragraph()
    p.text = "• Phase 1 (Weeks 1-4): Shadow pilot on 10,000 Bengaluru merchants for Settlement + Soundbox queries.\n• Phase 2 (Weeks 5-8): Expand to Kannada & Hindi voice intake with human approval required on retries > ₹25,000.\n• Phase 3 (Weeks 9-12): Full nationwide deployment with ₹50,000 autonomous ceiling and proactive EMI collection."
    p.font.size = Pt(10.5)
    p.font.color.rgb = TEXT_WHITE

    output_path = "Sahayak_Final_Evaluation_Prototype.pptx"
    prs.save(output_path)
    print(f"[SUCCESS] Created presentation at {output_path}")

if __name__ == "__main__":
    create_deck()
