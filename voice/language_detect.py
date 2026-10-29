"""
Sahayak Layer 1: Multilingual Language Detector
Detects Hindi, Kannada, and Indian English for merchant voice interactions.
"""

import re
from typing import Tuple


def detect_language(text: str) -> Tuple[str, str]:
    """
    Identifies language code and friendly name.
    Supported: 'hi-IN' (Hindi), 'kn-IN' (Kannada), 'en-IN' (English).
    """
    if not text:
        return "hi-IN", "Hindi"
        
    # Check for Kannada Unicode range (\u0C80-\u0CFF) or transliterated Kannada keywords
    kannada_chars = re.findall(r'[\u0C80-\u0CFF]', text)
    kannada_keywords = ["namaskara", "mathadtha", "illa", "nanna", "dukanige", "talupatte", "madiddive", "yenu", "beku", "hosa"]
    lower_words = text.lower().split()
    
    if len(kannada_chars) > 0 or any(kw in lower_words for kw in kannada_keywords):
        return "kn-IN", "Kannada"

    # Check for Devanagari Unicode range (\u0900-\u097F) or Romanized Hindi/Hinglish keywords
    devanagari_chars = re.findall(r'[\u0900-\u097F]', text)
    hindi_keywords = ["bhaiya", "paisa", "nahi", "aaya", "aaye", "mera", "meri", "humne", "bol", "kharab", "kat", "gaye", "karo", "kripya", "namaste"]
    
    if len(devanagari_chars) > 0 or any(kw in lower_words for kw in hindi_keywords):
        return "hi-IN", "Hindi"

    # Default to Indian English
    return "en-IN", "Indian English"

