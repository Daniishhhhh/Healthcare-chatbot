# 🚦 Person A - Basic health check endpoint
from fastapi import APIRouter, HTTPException
from app.db.db import get_database
from datetime import datetime
import asyncio

router = APIRouter()

@router.get("/")
async def health_check():
    """Basic health check endpoint"""
    try:
        # Test database connection
        db = await get_database()
        await db.list_collection_names()
        
        return {
            "status": "OK",
            "timestamp": datetime.now().isoformat(),
            "service": "SWASTHYA SETU API",
            "version": "1.0.0",
            "database": "connected"
        }
    except Exception as e:
        raise HTTPException(
            status_code=503, 
            detail=f"Service unavailable: {str(e)}"
        )

@router.get("/stats")
async def get_health_stats():
    """Get basic usage statistics"""
    try:
        db = await get_database()
        
        # Get chat history count
        chat_count = await db.chat_history.count_documents({})
        
        # Get appointment count
        appointment_count = await db.appointments.count_documents({})
        
        return {
            "total_conversations": chat_count,
            "total_appointments": appointment_count,
            "service_status": "operational",
            "last_updated": datetime.now().isoformat()
        }
        
    except Exception as e:
        return {
            "error": str(e),
            "service_status": "degraded"
        }
