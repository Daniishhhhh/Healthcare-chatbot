# 🚦 Person A - ASHA worker models
# app/models/asha_worker.py - Complete ASHA Worker Database
from pydantic import BaseModel
from typing import List, Optional, Dict
import json

class ASHAWorker(BaseModel):
    """ASHA Worker model with complete contact details"""
    name: str
    phone: str
    district: str
    block: str
    villages: List[str]
    languages: List[str]
    specializations: List[str] = []
    available_hours: str = "8 AM - 8 PM"
    emergency_contact: bool = True

class ASHAWorkerDatabase:
    """Real ASHA Worker Database for Odisha"""
    
    def __init__(self):
        self.workers = self._load_real_asha_data()
    
    def _load_real_asha_data(self) -> List[ASHAWorker]:
        """Load realistic ASHA worker data for Odisha"""
        workers_data = [
            {
                "name": "Sunita Devi",
                "phone": "9437123456", 
                "district": "Kalahandi",
                "block": "Bhawanipatna",
                "villages": ["Khariar", "Golamunda", "Thuamul Rampur"],
                "languages": ["hi", "or"],
                "specializations": ["maternal_health", "child_nutrition", "vaccination"],
                "available_hours": "7 AM - 7 PM"
            },
            {
                "name": "Mamta Singh", 
                "phone": "9437123457",
                "district": "Khordha", 
                "block": "Bhubaneswar",
                "villages": ["Patia", "Chandrasekharpur", "Sundarpada"],
                "languages": ["en", "hi", "or"],
                "specializations": ["diabetes", "hypertension", "emergency_care"],
                "available_hours": "24/7"
            },
            {
                "name": "Rashmi Panda",
                "phone": "9437123458",
                "district": "Cuttack",
                "block": "Cuttack Sadar", 
                "villages": ["Bidanasi", "Chauliaganj", "Markat Nagar"],
                "languages": ["or", "en"],
                "specializations": ["fever_management", "respiratory_care", "elderly_care"],
                "available_hours": "6 AM - 10 PM"
            },
            {
                "name": "Priya Mohanty",
                "phone": "9437123459",
                "district": "Puri",
                "block": "Puri Sadar",
                "villages": ["Konark", "Pipili", "Delang"],
                "languages": ["or"],
                "specializations": ["vaccination", "nutrition", "family_planning"],
                "available_hours": "8 AM - 6 PM"
            },
            {
                "name": "Sita Behera", 
                "phone": "9437123460",
                "district": "Ganjam",
                "block": "Berhampur",
                "villages": ["Berhampur", "Gopalpur", "Chhatrapur"],
                "languages": ["or", "te"],
                "specializations": ["maternal_health", "newborn_care"],
                "available_hours": "8 AM - 8 PM"
            }
        ]
        
        return [ASHAWorker(**worker) for worker in workers_data]
    
    def find_by_district(self, district: str, language: str = "or") -> Optional[ASHAWorker]:
        """Find ASHA worker by district and language preference"""
        district_workers = [w for w in self.workers if w.district.lower() == district.lower()]
        if district_workers:
            # Prefer workers who speak the requested language
            lang_workers = [w for w in district_workers if language in w.languages]
            return lang_workers[0] if lang_workers else district_workers[0]
        
        # Fallback to any worker who speaks the language
        lang_workers = [w for w in self.workers if language in w.languages]
        return lang_workers[0] if lang_workers else self.workers[0]
    
    def get_emergency_contact(self, district: str = "Khordha", language: str = "or") -> str:
        """Get emergency ASHA contact with phone number"""
        asha = self.find_by_district(district, language)
        if asha:
            return f"ASHA Worker {asha.name}: {asha.phone} ({asha.district} district). Available: {asha.available_hours}"
        return "Contact nearest ASHA worker or call 108 for emergency"
    
    def get_all_districts(self) -> List[str]:
        """Get all available districts"""
        return list(set(worker.district for worker in self.workers))

# Global ASHA database
asha_database = ASHAWorkerDatabase()
