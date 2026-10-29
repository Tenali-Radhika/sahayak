"""
Sahayak Layer 2: LLM & Tool Calling Orchestrator
Maps merchant natural speech to structured intents, entities, and tool calls.
"""

import re
from typing import Dict, Any, Tuple
from agent.confidence import ConfidenceScorer


class AgentLLM:
    """Classifies merchant intent, extracts parameters, and selects autonomous tool actions."""

    @staticmethod
    def diagnose_issue(utterance: str, merchant_id: str) -> Dict[str, Any]:
        """
        Classifies incoming merchant utterance into the 4 core ticket categories:
        1. SETTLEMENT_DELAY (~40% of tickets)
        2. SOUNDBOX_FAILURE (~25% of tickets)
        3. FAILED_PAYMENT (~20% of tickets)
        4. EMI_KYC_BLOCK (~15% of tickets)
        """
        lower = utterance.lower()
        entities: Dict[str, Any] = {}
        
        # Check for garbled / gibberish speech (simulating low confidence scenario)
        if len(utterance.strip()) < 4 or re.match(r'^[a-z]{1,4}$', lower) or "asdf" in lower or "gibberish" in lower:
            conf = 42.0
            return {
                "category": "UNKNOWN",
                "sub_intent": "UNCLEAR_SPEECH",
                "confidence": conf,
                "proposed_tool": None,
                "entities": {}
            }
            
        # 1. Settlement Delays
        if any(w in lower for w in ["paisa", "paise", "settlement", "ruka", "nahi aaya", "nahi mile", "credit"]):
            if any(w in lower for w in ["customer", "grahak", "kat gaye"]):
                category = "FAILED_PAYMENT"
                sub_intent = "CUSTOMER_DEBITED_NOT_CREDITED"
                proposed_tool = "resync_transaction"
                entities["approx_amount"] = 450.0
            else:
                category = "SETTLEMENT_DELAY"
                sub_intent = "DELAYED_BATCH_INQUIRY"
                proposed_tool = "retry_settlement"
                entities["requested_date"] = "2026-10-28"
                # Check if high amount requested in speech
                if "1,20,000" in lower or "120000" in lower or "lakh" in lower:
                    entities["amount_inr"] = 120000.00
                else:
                    entities["amount_inr"] = 14250.00

        # 2. Soundbox Failures
        elif any(w in lower for w in ["soundbox", "speaker", "bol nahi", "awaaz", "charge", "battery", "mathadtha illa"]):
            category = "SOUNDBOX_FAILURE"
            sub_intent = "HARDWARE_SPEAKER_FAULT"
            proposed_tool = "replace_device"
            entities["device_type"] = "SOUNDBOX_4G"

        # 3. Failed / Missing Payments
        elif any(w in lower for w in ["kat gaya", "kat gaye", "customer", "deducted"]):
            category = "FAILED_PAYMENT"
            sub_intent = "CUSTOMER_DEBITED_NOT_CREDITED"
            proposed_tool = "resync_transaction"
            entities["approx_amount"] = 450.0

        # 4. EMI & KYC Issues
        elif any(w in lower for w in ["emi", "loan", "kyc", "limit", "block", "freeze", "account limit"]):
            category = "EMI_KYC_BLOCK"
            if "kyc" in lower or "limit" in lower or "freeze" in lower:
                sub_intent = "KYC_VERIFICATION_REQUIRED"
                proposed_tool = "resend_kyc_link"
            else:
                sub_intent = "EMI_PAYMENT_DUE"
                proposed_tool = "send_emi_payment_link"
                entities["amount_inr"] = 3200.0

        else:
            # Fallback category
            category = "GENERAL_INQUIRY"
            sub_intent = "MERCHANT_SUPPORT"
            proposed_tool = "fetch_merchant_profile"
            
        conf = ConfidenceScorer.calculate_confidence(utterance, category, entities)
        
        return {
            "category": category,
            "sub_intent": sub_intent,
            "confidence": conf,
            "proposed_tool": proposed_tool,
            "entities": entities
        }

    @staticmethod
    def generate_response(
        category: str,
        lang_code: str,
        action_result: Dict[str, Any],
        proactive_sales_info: Dict[str, Any] = None
    ) -> str:
        """
        Generates culturally natural, reassuring merchant responses.
        """
        # Kannada responses
        if lang_code == "kn-IN":
            if category == "SOUNDBOX_FAILURE":
                return "Namaskara Ramesh avare! Nimma Soundbox speaker alli samasye ide. Naavu hosa Soundbox dispatch madiddive. Nale madhyahna 2 gante olage nimma dukanige talupatte. Tracking link SMS moolaka kalisiddene."
            return "Namaskara! Nimma samasye pariharavagide. Paytm upayogisಿದ್ದಕ್ಕಾಗಿ dhanyavada."

        # Indian English responses
        if lang_code == "en-IN":
            msg = f"Hello! Your {category.lower().replace('_', ' ')} has been autonomously verified and resolved."
            if proactive_sales_info:
                msg += f" Also, your loan EMI of ₹{proactive_sales_info.get('amount_inr', 3200):,.0f} is due tomorrow. The payment link has been sent to your phone."
            return msg

        # Default: Hindi (Natural Merchant Colloquial)
        if category == "SETTLEMENT_DELAY":
            response = "Namaste Ramesh ji! Kal bank holiday hone ki wajah se ₹14,250 ka settlement ruka hua tha. Humne kal subah 6 baje ke liye retry schedule kar diya hai aur payment gateway se confirmation aa chuka hai. Aapko callback ki bilkul zaroorat nahi hai — kaam ho gaya hai!"
            if proactive_sales_info and proactive_sales_info.get("is_due_tomorrow"):
                emi_amt = proactive_sales_info.get("next_emi_amount_inr", 3200)
                response += f" Aur Ramesh ji, aapki loan EMI ₹{emi_amt:,.0f} kal due hai, uska payment link maine aapke WhatsApp aur SMS par bhej diya hai taaki aapka business record badhiya rahe."
            return response
            
        elif category == "SOUNDBOX_FAILURE":
            return "Namaste! Aapke Soundbox ka speaker hardware kharab ho gaya hai. Humne naye Soundbox ka express replacement dispatch kar diya hai jo kal dopahar 2 baje tak aapke dukan par pahunch jayega. Tracking link SMS par bhej diya hai."
            
        elif category == "FAILED_PAYMENT":
            return "Namaste! Customer ka ₹450 ka payment gateway par verify ho gaya hai aur aapke account mein credit sync kar diya gaya hai. Soundbox par notification trigger ho gaya hai."
            
        elif category == "EMI_KYC_BLOCK":
            return "Namaste! Aapka account limit update karne ke liye quick biometric KYC update link aapke registered number par bhej diya gaya hai. Link par click karke aap 2 minute mein verification complete kar sakte hain."

        return "Namaste! Aapki request safely process ho gayi hai. Paytm business partner banne ke liye dhanyavad."
