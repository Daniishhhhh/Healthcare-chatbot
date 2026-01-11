# 🚦 Person A - Response formatting
# app/utils/formatters.py
# app/utils/formatters.py

# 🤖 Person B - Response Formatting for Different Interfaces

import re
from typing import Dict, Any

def format_response_for_interface(response_text: str, interface: str, language: str) -> str:
    """
    Format responses appropriately for WhatsApp vs SMS vs Voice interfaces
    """
    if interface.lower() == "whatsapp":
        return format_for_whatsapp(response_text, language)
    elif interface.lower() == "sms":
        return format_for_sms(response_text, language)
    elif interface.lower() == "voice":
        return format_for_voice(response_text, language)
    else:
        return response_text # Default formatting

def format_for_whatsapp(text: str, language: str) -> str:
    """
    Format for WhatsApp - supports emojis, bold text, bullets
    """
    # Add health emoji based on content
    if any(keyword in text.lower() for keyword in ["emergency", "urgent", "जरूरी", "ଜରୁରୀ"]):
        text = "🚨 " + text
    elif any(keyword in text.lower() for keyword in ["fever", "बुखार", "ଜ୍ୱର"]):
        text = "🤒 " + text
    elif any(keyword in text.lower() for keyword in ["cold", "cough", "सर्दी", "खांसी", "ଶୀତ", "କାଶ"]):
        text = "🤧 " + text
    elif any(keyword in text.lower() for keyword in ["welcome", "स्वागत", "ସ୍ୱାଗତ"]):
        text = "🏥 " + text
    
    return text

def format_for_sms(text: str, language: str) -> str:
    """
    Format for SMS - plain text, 160 char limit, no emojis for basic phones
    """
    # Remove emojis and special characters that might not display on basic phones
    text = re.sub(r'[^\w\s\-.,!?():]+', '', text)
    
    # Truncate if too long for SMS
    if len(text) > 155:  # Leave room for "..."
        text = text[:152] + "..."
    
    return text.strip()

def format_for_voice(text: str, language: str) -> str:
    """
    Format for voice - remove emojis, add pauses for natural speech
    """
    # Remove emojis and special formatting
    text = re.sub(r'[^\w\s\-.,!?()]+', '', text)
    
    # Add pauses for voice synthesis (represented as ...)
    text = text.replace('. ', '. ... ')
    text = text.replace('! ', '! ... ')
    text = text.replace('? ', '? ... ')
    
    return text
