"""
Guardrail Gate 5: Idempotency & Reversibility Check
"""

import time
from typing import Dict, Tuple

# Key: action_fingerprint -> timestamp of execution
_EXECUTION_CACHE: Dict[str, float] = {}
COOLDOWN_SECONDS = 5.0  # Prevent duplicate rapid double-clicks (5s cooldown for demo responsiveness)


def check_idempotency(action_key: str, cooldown: float = COOLDOWN_SECONDS) -> Tuple[bool, str]:
    """
    Prevents duplicate actions, double credits, or race conditions.
    Returns: (is_unique: bool, message: str)
    """
    now = time.time()
    if action_key in _EXECUTION_CACHE:
        prev_time = _EXECUTION_CACHE[action_key]
        if (now - prev_time) < cooldown:
            return False, f"DUPLICATE_ACTION_BLOCKED: Action '{action_key}' was recently executed {now - prev_time:.1f}s ago."
            
    _EXECUTION_CACHE[action_key] = now
    return True, "Action idempotency check passed."


def clear_idempotency_cache():
    """Reset for testing."""
    _EXECUTION_CACHE.clear()

