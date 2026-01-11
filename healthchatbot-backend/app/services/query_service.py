# 🚦 Person A / 🤖 Person B - Query processing
# app/services/query_service.py
import json
import logging
from typing import Dict, List, Any, Optional
from pathlib import Path
import re

logger = logging.getLogger(__name__)

class HealthQueryProcessor:
    """
    RAG Pipeline with multilingual support for health queries
    """
    
    def __init__(self):
        self.symptoms_db = self._load_health_data()
        self.intent_patterns = self._load_intent_patterns()
    
    def _load_health_data(self) -> Dict[str, Dict]:
        """Load multilingual health response data"""
        health_data = {
            "odia": {},
            "hindi": {},
            "english": {}
        }
        
        try:
            # Try to load Odia symptoms
            odia_path = Path("app/data/health/symptoms_odia.json")
            if odia_path.exists():
                with open(odia_path, 'r', encoding='utf-8') as f:
                    health_data["odia"] = json.load(f)
            
            # Try to load Hindi symptoms  
            hindi_path = Path("app/data/health/symptoms_hindi.json")
            if hindi_path.exists():
                with open(hindi_path, 'r', encoding='utf-8') as f:
                    health_data["hindi"] = json.load(f)
                    
        except Exception as e:
            logger.warning(f"Could not load health data: {e}")
            
        return health_data
    
    def _load_intent_patterns(self) -> Dict:
        """Load intent classification patterns"""
        return {
            "emergency": ["emergency", "urgent", "help", "आपातकाल", "जरूरी", "ଜରୁରୀକାଳୀନ"],
            "symptoms": ["fever", "बुखार", "ଜ୍ୱର", "cold", "cough", "pain", "दर्द"],
            "appointments": ["appointment", "doctor", "clinic", "अपॉइंटमेंट"],
            "general": ["hello", "hi", "नमस्ते", "ନମସ୍କାର"]
        }
    
    async def process_query_async(self, query: str, language: str) -> Dict[str, Any]:
        """Process health query asynchronously"""
        return await self._process_query(query, language)
    
    async def _process_query(self, query: str, language: str) -> Dict[str, Any]:
        """Internal query processing"""
        query_lower = query.lower()
        
        # Emergency detection
        if any(emergency_word in query_lower for emergency_word in self.intent_patterns["emergency"]):
            return {
                "response": self._get_emergency_response(language),
                "intent": "emergency",
                "language": language,
                "emergency": True,
                "severity": "critical"
            }
        
        # Symptom detection
        if any(symptom_word in query_lower for symptom_word in self.intent_patterns["symptoms"]):
            return {
                "response": self._get_symptom_response(query, language),
                "intent": "symptoms", 
                "language": language,
                "emergency": False,
                "severity": "mild"
            }
        
        # Default response
        return {
            "response": self._get_default_response(language),
            "intent": "general",
            "language": language, 
            "emergency": False
        }
    
    def _get_emergency_response(self, language: str) -> str:
        """Get emergency response in specified language"""
        responses = {
            "en": "🚨 EMERGENCY DETECTED! Call 108 immediately for ambulance. ASHA worker has been alerted. Stay calm, help is coming!",
            "hi": "🚨 आपातकाल का पता चला! एम्बुलेंस के लिए तुरंत 108 पर कॉल करें। आशा कार्यकर्ता को सचेत कर दिया गया है।",
            "or": "🚨 ଜରୁରୀକାଳୀନ ପରିସ୍ଥିତି! ଆମ୍ବୁଲାନ୍ସ ପାଇଁ ତୁରନ୍ତ 108 ରେ କଲ କରନ୍ତୁ। ଆଶା କର୍ମୀଙ୍କୁ ସତର୍କ କରାଯାଇଛି।"
        }
        return responses.get(language, responses["en"])
    
    def _get_symptom_response(self, query: str, language: str) -> str:
        """Get symptom-specific response"""
        query_lower = query.lower()
        
        # Fever detection
        if any(word in query_lower for word in ["fever", "बुखार", "ଜ୍ୱର"]):
            responses = {
                "en": "🤒 For fever: Take paracetamol, rest, drink fluids. If fever >101°F or persists >3 days, contact ASHA worker Sunita Devi (Kalahandi).",
                "hi": "🤒 बुखार के लिए: पैरासिटामोल लें, आराम करें, तरल पदार्थ पिएं। अगर बुखार 101°F से ज्यादा हो या 3 दिन से ज्यादा रहे तो आशा कार्यकर्ता से संपर्क करें।",
                "or": "🤒 ଜ୍ୱର ପାଇଁ: ପାରାସିଟାମଲ ନିଅନ୍ତୁ, ବିଶ୍ରାମ ନିଅନ୍ତୁ, ତରଳ ପଦାର୍ଥ ପିଅନ୍ତୁ। ଯଦି ଜ୍ୱର 101°F ରୁ ଅଧିକ ହୁଏ କିମ୍ବା 3 ଦିନରୁ ଅଧିକ ରହେ ତେବେ ଆଶା କର୍ମୀଙ୍କ ସହ ଯୋଗାଯୋଗ କରନ୍ତୁ।"
            }
            return responses.get(language, responses["en"])
        
        # Cold/Cough detection
        if any(word in query_lower for word in ["cold", "cough", "खांसी", "कାଶ"]):
            responses = {
                "en": "🤧 For cold/cough: Steam inhalation, warm water with honey-ginger. Rest well. See doctor if symptoms worsen after 5 days.",
                "hi": "🤧 सर्दी/खांसी के लिए: भाप लें, शहद-अदरक के साथ गर्म पानी पिएं। अच्छा आराम करें।",
                "or": "🤧 ଶୀତ/କାଶ ପାଇଁ: ବାଷ୍ପ ନିଅନ୍ତୁ, ମହୁ-ଅଦା ସହିତ ଗରମ ପାଣି ପିଅନ୍ତୁ। ଭଲ ବିଶ୍ରାମ ନିଅନ୍ତୁ।"
            }
            return responses.get(language, responses["en"])
        
        # Default symptom response
        return self._get_default_response(language)
    
    def _get_default_response(self, language: str) -> str:
        """Get default response in specified language"""
        responses = {
            "en": "🏥 I'm your rural health assistant. I can help with fever, cold, emergencies, and health questions. What symptoms are you experiencing?",
            "hi": "🏥 मैं आपका ग्रामीण स्वास्थ्य सहायक हूं। मैं बुखार, सर्दी, आपातकाल और स्वास्थ्य प्रश्नों में मदद कर सकता हूं।",
            "or": "🏥 ମୁଁ ଆପଣଙ୍କର ଗ୍ରାମୀଣ ସ୍ୱାସ୍ଥ୍ୟ ସହାୟକ। ମୁଁ ଜ୍ୱର, ଶୀତ, ଜରୁରୀକାଳୀନ ଏବଂ ସ୍ୱାସ୍ଥ୍ୟ ପ୍ରଶ୍ନରେ ସାହାଯ୍ୟ କରିପାରିବି।"
        }
        return responses.get(language, responses["en"])
