"""
Sahayak Layer 2: Multi-turn Conversation Manager
Maintains merchant interaction session state across multiple dialogue turns.
"""

import uuid
from typing import Dict, Any, List


class ConversationSession:
    """Stores turns, transcript history, and active entity contexts."""

    def __init__(self, merchant_id: str, caller_phone: str):
        self.session_id = f"SESS_{uuid.uuid4().hex[:8].upper()}"
        self.merchant_id = merchant_id
        self.caller_phone = caller_phone
        self.turns: List[Dict[str, Any]] = []
        self.context: Dict[str, Any] = {}
        self.transcript: List[Dict[str, str]] = []
        self.status = "ACTIVE"

    def add_turn(self, speaker: str, text: str, latency_ms: int = 0):
        self.transcript.append({"speaker": speaker, "text": text})
        self.turns.append({
            "speaker": speaker,
            "text": text,
            "latency_ms": latency_ms
        })

    def get_full_transcript(self) -> List[Dict[str, str]]:
        return list(self.transcript)
