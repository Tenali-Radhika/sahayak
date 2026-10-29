"""
Guardrail Gate 3: Confidence Threshold Gate
"""

from typing import Tuple

DEFAULT_CONFIDENCE_THRESHOLD = 80.0


def check_confidence_threshold(confidence_score: float, threshold: float = DEFAULT_CONFIDENCE_THRESHOLD) -> Tuple[bool, str]:
    """
    Prevents the agent from taking autonomous financial or device action if diagnosis confidence is low.
    Returns: (is_above_threshold: bool, message: str)
    """
    if confidence_score < threshold:
        return False, f"CONFIDENCE_BELOW_THRESHOLD: Confidence {confidence_score:.1f}% is below required {threshold:.1f}% safety barrier."
        
    return True, f"Confidence {confidence_score:.1f}% meets safety threshold ({threshold:.1f}%)."

