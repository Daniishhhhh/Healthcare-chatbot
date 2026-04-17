from __future__ import annotations

import logging
from datetime import datetime
from typing import Dict, List, Tuple

from decouple import config
from twilio.rest import Client

logger = logging.getLogger(__name__)

try:
    client = Client(config("TWILIO_ACCOUNT_SID"), config("TWILIO_AUTH_TOKEN"))
except Exception:
    client = None
    logger.warning("Twilio client not configured; emergency SMS disabled.")

# Mock ASHA worker data
ASHA_WORKERS = [
    {
        "asha_id": "ASHA_KLD_001",
        "name": "Sunita Devi",
        "district": "kalahandi",
        "phone": "+91-8765432109",
        "languages": ["odia", "hindi"],
    },
    {
        "asha_id": "ASHA_KHR_001",
        "name": "Mamta Singh",
        "district": "khordha",
        "phone": "+91-8765432108",
        "languages": ["odia", "english"],
    },
]

# Emergency scoring weights
SYMPTOM_WEIGHTS: Dict[str, int] = {
    "chest pain": 5,
    "सीने": 5,
    "ଛାତି": 5,
    "bleeding": 5,
    "heavy bleeding": 5,
    "severe": 3,
    "severe pain": 3,
    "breath": 4,
    "सांस": 4,
    "ଶ୍ୱାସ": 4,
    "can't breathe": 4,
    "unconscious": 4,
    "बेहोश": 4,
}

EMERGENCY_KEYWORDS = {
    "high_fever": ["103", "high fever", "ଉଚ୍ଚ ଜ୍ୱର", "तेज बुखार"],
    "chest_pain": ["chest pain", "ଛାତି ଯନ୍ତ୍ରଣା", "सीने में दर्द"],
    "breathing": ["breathing problem", "cannot breathe", "ନିଶ୍ୱାସ", "सांस"],
    "unconscious": ["unconscious", "fainted", "ବେହୋସ", "बेहोश"],
}


class EmergencyEngine:
    """Score messages to reduce false positives while keeping urgent cases fast."""

    def __init__(self, threshold: int = 6):
        self.threshold = threshold

    def score(self, message: str) -> Tuple[int, List[str]]:
        text = message.lower()
        triggers = []
        score = 0
        for phrase, weight in SYMPTOM_WEIGHTS.items():
            if phrase in text:
                score += weight
                triggers.append(phrase)
        return score, triggers

    def assess(self, message: str) -> Dict[str, object]:
        score, triggers = self.score(message)
        triggered = score >= self.threshold
        return {"score": score, "triggered": triggered, "triggers": triggers}

    def build_emergency_message(self, user_phone: str, symptoms: str) -> str:
        return (
            "🚨 Immediate medical attention recommended.\n"
            "• Call 108 for an ambulance right away.\n"
            "• Stay with the patient and keep them responsive.\n"
            f"• We are notifying the nearest ASHA worker for {user_phone}.\n"
            f"Symptoms noted: {symptoms}"
        )


emergency_engine = EmergencyEngine()


async def check_emergency_keywords(user_message: str, user_phone: str) -> tuple[bool, str]:
    """Check emergency keywords and scoring."""
    score_result = emergency_engine.assess(user_message)
    message_lower = user_message.lower()

    if score_result["triggered"]:
        escalation_result = await escalate_to_asha(
            user_phone, user_message, "scored_emergency"
        )
        return True, escalation_result

    for emergency_type, keywords in EMERGENCY_KEYWORDS.items():
        for keyword in keywords:
            if keyword.lower() in message_lower:
                escalation_result = await escalate_to_asha(
                    user_phone, user_message, emergency_type
                )
                return True, escalation_result

    return False, ""


async def escalate_to_asha(user_phone: str, symptoms: str, emergency_type: str) -> str:
    """Escalate emergency to ASHA worker with graceful fallback."""
    try:
        asha = ASHA_WORKERS[0]  # In production, determine by location

        emergency_msg = f"""🚨 EMERGENCY ALERT 🚨
Patient: {user_phone}
Symptoms: {symptoms}
Emergency Type: {emergency_type}
Time: {datetime.now().strftime('%Y-%m-%d %H:%M')}

Please contact patient immediately.
SWASTHYA SETU"""

        if client:
            try:
                client.messages.create(
                    body=emergency_msg,
                    from_=config("TWILIO_PHONE_NUMBER", default=""),
                    to=asha["phone"],
                )
            except Exception as sms_error:
                logger.warning(f"SMS escalation failed: {sms_error}")
        else:
            logger.info("Twilio not configured; skipping SMS send.")

        return (
            "🚨 Emergency detected!\n"
            f"✅ ASHA worker {asha['name']} has been notified.\n"
            "📞 They will reach out shortly. If symptoms worsen, call 108 immediately."
        )

    except Exception as e:
        logger.error(f"Failed to escalate emergency: {str(e)}")
        return (
            "🚨 Emergency detected! Please call immediately:\n"
            "• Ambulance: 108\n"
            "• Medical Emergency: 102\n"
            "If you cannot place the call, ask someone nearby to assist."
        )
