from twilio.rest import Client
from decouple import config
import logging
from datetime import datetime

client = Client(config("TWILIO_ACCOUNT_SID"), config("TWILIO_AUTH_TOKEN"))

# Mock ASHA worker data
ASHA_WORKERS = [
    {
        "asha_id": "ASHA_KLD_001",
        "name": "Sunita Devi",
        "district": "kalahandi",
        "phone": "+91-8765432109",
        "languages": ["odia", "hindi"]
    },
    {
        "asha_id": "ASHA_KHR_001",
        "name": "Mamta Singh", 
        "district": "khordha",
        "phone": "+91-8765432108",
        "languages": ["odia", "english"]
    }
]

# Emergency keywords
EMERGENCY_KEYWORDS = {
    "high_fever": ["103", "high fever", "ଉଚ୍ଚ ଜ୍ୱର", "तेज बुखार"],
    "chest_pain": ["chest pain", "ଛାତି ଯନ୍ତ୍ରଣା", "सीने में दर्द"],
    "breathing": ["breathing problem", "cannot breathe", "ନିଶ୍ୱାସ", "सांस"],
    "unconscious": ["unconscious", "fainted", "ବେହୋସ", "बेहोश"]
}

async def check_emergency_keywords(user_message: str, user_phone: str) -> tuple[bool, str]:
    """Check if message contains emergency keywords"""
    
    message_lower = user_message.lower()
    
    for emergency_type, keywords in EMERGENCY_KEYWORDS.items():
        for keyword in keywords:
            if keyword.lower() in message_lower:
                # This is an emergency - escalate
                escalation_result = await escalate_to_asha(user_phone, user_message, emergency_type)
                return True, escalation_result
    
    return False, ""

async def escalate_to_asha(user_phone: str, symptoms: str, emergency_type: str) -> str:
    """Escalate emergency to ASHA worker"""
    
    try:
        # For demo, use first ASHA worker
        asha = ASHA_WORKERS[0]  # In production, determine by location
        
        # Create emergency message for ASHA worker
        emergency_msg = f"""🚨 EMERGENCY ALERT 🚨
Patient: {user_phone}
Symptoms: {symptoms}
Emergency Type: {emergency_type}
Time: {datetime.now().strftime('%Y-%m-%d %H:%M')}

Please contact patient immediately.
SWASTHYA SETU"""
        
        # Send SMS to ASHA worker (for demo, we'll log it)
        logging.info(f"DEMO: Sending emergency alert to ASHA {asha['name']} at {asha['phone']}")
        logging.info(f"Emergency message: {emergency_msg}")
        
        # In production, uncomment this:
        # client.messages.create(
        #     body=emergency_msg,
        #     from_=config("TWILIO_PHONE_NUMBER"),
        #     to=asha["phone"]
        # )
        
        return f"""🚨 EMERGENCY DETECTED! 🚨

Your symptoms indicate urgent medical attention needed.

✅ ASHA worker {asha['name']} has been notified
📞 They will contact you shortly at {user_phone}

🚨 IMMEDIATE ACTIONS:
• Call 108 for ambulance if severe
• Stay calm and don't panic  
• Keep phone nearby for ASHA call

Emergency services are being arranged for you."""
        
    except Exception as e:
        logging.error(f"Failed to escalate emergency: {str(e)}")
        return """🚨 EMERGENCY DETECTED! 🚨

Please call immediately:
• Ambulance: 108
• Medical Emergency: 102  
• Police: 100

Your emergency has been logged. Stay safe!"""
