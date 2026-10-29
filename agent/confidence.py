"""
Sahayak Layer 2: Confidence Scorer
Computes numerical confidence score (0-100) for issue diagnosis and intent parsing.
"""

from typing import Dict, Any, Tuple


class ConfidenceScorer:
    """Evaluates lexical, acoustic, and context match signals to produce a 0-100 score."""

    @staticmethod
    def calculate_confidence(
        utterance: str,
        matched_category: str,
        detected_entities: Dict[str, Any],
        stt_confidence: float = 0.95
    ) -> float:
        """
        Combines STT confidence, keyword density, and entity completeness into a 0-100 score.
        """
        if not utterance or matched_category == "UNKNOWN":
            return 35.0  # Low confidence -> triggers Gate 3 Guardrail
            
        base_score = stt_confidence * 70.0  # Max 70 from transcription quality
        
        # Keyword alignment bonus
        category_keywords = {
            "SETTLEMENT_DELAY": ["paisa", "paise", "nahi aaya", "aaye", "settlement", "bank", "holiday", "pending", "kal ka"],
            "SOUNDBOX_FAILURE": ["soundbox", "bol", "awaaz", "speaker", "audio", "charge", "battery", "kharab", "mathadtha illa"],
            "FAILED_PAYMENT": ["kat gaye", "customer", "deducted", "kata", "debit", "received"],
            "EMI_KYC_BLOCK": ["emi", "loan", "kyc", "limit", "account", "block", "freeze"]
        }
        
        keywords = category_keywords.get(matched_category, [])
        matches = sum(1 for kw in keywords if kw in utterance.lower())
        keyword_bonus = min(20.0, matches * 7.0)
        
        # Entity completeness bonus
        entity_bonus = 10.0 if detected_entities else 5.0
        
        final_score = min(99.0, max(20.0, base_score + keyword_bonus + entity_bonus))
        return round(final_score, 1)
