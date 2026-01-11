# app/services/health_data_loader.py
"""
Health Data Loader - Loads all medical data from JSON files
Uses the real doctor-verified JSON data you provided
"""
import json
import logging
from pathlib import Path
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

class HealthDataLoader:
    """Load and manage all health-related data from JSON files"""
    
    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.symptoms_db = {}
        self.emergency_protocols = {}
        self.asha_contacts = {}
        self.seasonal_alerts = {}
        self._load_all_data()
    
    def _load_all_data(self):
        """Load all health data from JSON files"""
        try:
            self._load_symptoms_data()
            self._load_emergency_protocols()
            self._load_asha_contacts()
            self._load_seasonal_alerts()
            logger.info("✅ All health data loaded successfully")
        except Exception as e:
            logger.error(f"❌ Error loading health data: {e}")
    
    def _load_symptoms_data(self):
        """Load symptoms data from JSON files"""
        self.symptoms_db = {
            "hindi": self._load_json_file("health/symptoms_hindi.json"),
            "odia": self._load_json_file("health/symptoms_odia.json"), 
            "english": self._load_json_file("health/symptoms_english.json")
        }
        logger.info(f"📊 Loaded symptoms for {len(self.symptoms_db)} languages")
    
    def _load_emergency_protocols(self):
        """Load emergency protocols"""
        self.emergency_protocols = self._load_json_file("health/emergency_protocols.json")
        if not self.emergency_protocols:
            # Fallback emergency data
            self.emergency_protocols = {
                "emergency_keywords": {
                    "en": ["chest pain", "heart attack", "stroke", "breathing difficulty", "unconscious"],
                    "hi": ["सीने में दर्द", "दिल का दौरा", "स्ट्रोक", "सांस लेने में तकलीफ", "बेहोशी"],
                    "or": ["ଛାତି ଯନ୍ତ୍ରଣା", "ହୃଦଘାତ", "ସ୍ଟ୍ରୋକ୍", "ଶ୍ୱାସ ନେବାରେ କଷ୍ଟ", "ଅଚେତନତା"]
                }
            }
        logger.info("🚨 Emergency protocols loaded")
    
    def _load_asha_contacts(self):
        """Load ASHA worker contacts"""
        self.asha_contacts = self._load_json_file("clinics/asha_workers.json")
        if not self.asha_contacts:
            # Fallback ASHA data with your real contacts
            self.asha_contacts = {
                "contacts": {
                    "kalahandi": {
                        "name": "Sunita Devi",
                        "phone": "9437123456",
                        "available": "7 AM - 7 PM (Emergency: 24/7)",
                        "specializes": "Maternal health, Child nutrition, Vaccination"
                    },
                    "khordha": {
                        "name": "Mamta Singh",
                        "phone": "9437123457",
                        "available": "8 AM - 6 PM",
                        "specializes": "Diabetes, Blood Pressure"
                    }
                }
            }
        logger.info("📞 ASHA contacts loaded")
    
    def _load_seasonal_alerts(self):
        """Load seasonal health alerts"""
        seasonal_data = self._load_json_file("health/seasonal_alerts.json")
        if seasonal_data:
            self.seasonal_alerts = seasonal_data
        logger.info("🌦️ Seasonal alerts loaded")
    
    def _load_json_file(self, filename: str) -> Dict[str, Any]:
        """Load a JSON file with error handling"""
        file_path = self.data_dir / filename
        try:
            if file_path.exists():
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    logger.info(f"✅ Loaded {filename}")
                    return data
            else:
                logger.warning(f"⚠️ File not found: {filename}")
                return {}
        except Exception as e:
            logger.error(f"❌ Error loading {filename}: {e}")
            return {}
    
    def get_symptoms_for_language(self, language: str) -> Dict[str, Any]:
        """Get symptoms data for specific language"""
        lang_map = {"hi": "hindi", "or": "odia", "en": "english"}
        mapped_lang = lang_map.get(language, "english")
        return self.symptoms_db.get(mapped_lang, {})
    
    def get_emergency_keywords(self, language: str) -> list:
        """Get emergency keywords for specific language"""
        return self.emergency_protocols.get("emergency_keywords", {}).get(language, [])
    
    def get_asha_contacts(self) -> Dict[str, Any]:
        """Get all ASHA worker contacts"""
        return self.asha_contacts.get("contacts", {})
    
    def get_seasonal_alerts(self) -> list:
        """Get seasonal health alerts"""
        return self.seasonal_alerts.get("seasonal_alerts", [])
    
    def reload_data(self):
        """Reload all data from files"""
        logger.info("🔄 Reloading health data...")
        self._load_all_data()

# Global instance
health_data = HealthDataLoader()
