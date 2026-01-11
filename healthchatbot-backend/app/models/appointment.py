# 🚦 Person A - Appointment booking models
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class AppointmentRequest(BaseModel):
    user_phone: str
    district: str
    preferred_date: str
    preferred_time: str
    symptoms: Optional[str] = None

class Clinic(BaseModel):
    clinic_id: str
    name: str
    district: str
    location: str
    phone: str
    available_slots: List[str]

class AppointmentResponse(BaseModel):
    clinic_name: str
    appointment_time: str
    confirmation_id: str
    clinic_phone: str
    status: str = "confirmed"
