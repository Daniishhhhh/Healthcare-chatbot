# 🚦 Person A - PHC/CHC booking system
from fastapi import APIRouter, HTTPException
from models.appointment import AppointmentRequest, AppointmentResponse
from app.db.db import save_appointment
import json
import time
from datetime import datetime

router = APIRouter()

# Mock PHC/CHC data for demo
MOCK_CLINICS = [
    {
        "clinic_id": "PHC_KLD_001",
        "name": "Kalahandi Primary Health Centre",
        "district": "kalahandi",
        "location": "Bhawanipatna",
        "phone": "+91-9876543210",
        "available_slots": ["09:00", "11:00", "14:00", "16:00"]
    },
    {
        "clinic_id": "CHC_KHR_001", 
        "name": "Khordha Community Health Centre",
        "district": "khordha",
        "location": "Bhubaneswar",
        "phone": "+91-9876543211",
        "available_slots": ["10:00", "12:00", "15:00", "17:00"]
    },
    {
        "clinic_id": "PHC_CTC_001",
        "name": "Cuttack Primary Health Centre", 
        "district": "cuttack",
        "location": "Cuttack",
        "phone": "+91-9876543212",
        "available_slots": ["09:30", "11:30", "14:30", "16:30"]
    }
]

@router.post("/book", response_model=AppointmentResponse)
async def book_appointment(request: AppointmentRequest):
    """Book appointment at PHC/CHC"""
    try:
        # Find clinic by district
        clinic = next((c for c in MOCK_CLINICS if c["district"].lower() == request.district.lower()), None)
        
        if not clinic:
            raise HTTPException(status_code=404, detail="No clinic found in your district")
        
        # Generate confirmation ID
        confirmation_id = f"APPT_{clinic['clinic_id']}_{int(time.time())}"
        
        # Save appointment to database
        appointment_data = {
            "user_phone": request.user_phone,
            "clinic_id": clinic["clinic_id"],
            "clinic_name": clinic["name"],
            "district": request.district,
            "date": request.preferred_date,
            "time": request.preferred_time,
            "symptoms": request.symptoms,
            "confirmation_id": confirmation_id,
            "status": "confirmed",
            "created_at": datetime.now()
        }
        
        await save_appointment(appointment_data)
        
        return AppointmentResponse(
            clinic_name=clinic["name"],
            appointment_time=f"{request.preferred_date} at {request.preferred_time}",
            confirmation_id=confirmation_id,
            clinic_phone=clinic["phone"]
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to book appointment: {str(e)}")

@router.get("/available/{district}")
async def get_available_slots(district: str):
    """Get available appointment slots for district"""
    clinic = next((c for c in MOCK_CLINICS if c["district"].lower() == district.lower()), None)
    
    if not clinic:
        raise HTTPException(status_code=404, detail="No clinic found for this district")
    
    return {
        "district": district,
        "clinic": clinic["name"],
        "location": clinic["location"],
        "phone": clinic["phone"],
        "available_slots": clinic["available_slots"]
    }

@router.get("/clinics")
async def get_all_clinics():
    """Get all available clinics"""
    return {"clinics": MOCK_CLINICS}
