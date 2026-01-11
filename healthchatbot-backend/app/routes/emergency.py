# 🚦 Person A - ASHA worker escalation
from fastapi import APIRouter, HTTPException
from app.services.emergency_service import escalate_to_asha, ASHA_WORKERS
from pydantic import BaseModel

router = APIRouter()

class EmergencyRequest(BaseModel):
    user_phone: str
    symptoms: str
    location: str

@router.post("/escalate")
async def emergency_escalate(request: EmergencyRequest):
    """Manually escalate emergency to ASHA worker"""
    
    try:
        result = await escalate_to_asha(
            request.user_phone, 
            request.symptoms, 
            "manual_escalation"
        )
        
        return {
            "status": "escalated",
            "message": result,
            "emergency_contacts": {
                "ambulance": "108",
                "medical": "102",
                "police": "100"
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Emergency escalation failed: {str(e)}")

@router.get("/contacts")
async def get_emergency_contacts():
    """Get emergency contact information"""
    
    return {
        "emergency_numbers": {
            "ambulance": "108",
            "medical_emergency": "102", 
            "covid_helpline": "1075",
            "police": "100"
        },
        "asha_workers": ASHA_WORKERS
    }
