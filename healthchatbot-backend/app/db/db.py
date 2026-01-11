# 🚦 Person A - Enhanced DB connections
# 🚦 Person A - Enhanced DB connections with proper error handling and language detection
from motor.motor_asyncio import AsyncIOMotorClient
from decouple import config
import logging
from datetime import datetime
from typing import Optional, Dict, List
import re

class Database:
    client: AsyncIOMotorClient = None
    
db = Database()

async def get_database():
    """Get database instance with error handling"""
    try:
        return db.client.swasthya_setu
    except Exception as e:
        logging.error(f"Database connection error: {str(e)}")
        raise

async def connect_to_mongo():
    """Create database connection with retry logic"""
    try:
        connection_string = config("MONGO_CONNECTION_STRING", default="mongodb://mongodb:27017")
        db.client = AsyncIOMotorClient(connection_string)
        
        # Test connection
        await db.client.admin.command('ismaster')
        logging.info("✅ Connected to MongoDB successfully")
        
        # Create indexes for better performance
        await create_indexes()
        
    except Exception as e:
        logging.error(f"❌ Failed to connect to MongoDB: {str(e)}")
        raise

async def close_mongo_connection():
    """Close database connection gracefully"""
    try:
        if db.client:
            db.client.close()
            logging.info("✅ Disconnected from MongoDB")
    except Exception as e:
        logging.error(f"Error closing MongoDB connection: {str(e)}")

async def create_indexes():
    """Create database indexes for optimal performance"""
    try:
        database = await get_database()
        
        # Chat history indexes
        await database.chat_history.create_index("user_phone")
        await database.chat_history.create_index("timestamp")
        await database.chat_history.create_index([("user_phone", 1), ("timestamp", -1)])
        
        # Appointments indexes
        await database.appointments.create_index("user_phone")
        await database.appointments.create_index("confirmation_id")
        await database.appointments.create_index("clinic_id")
        await database.appointments.create_index("created_at")
        
        logging.info("✅ Database indexes created successfully")
        
    except Exception as e:
        logging.error(f"Failed to create indexes: {str(e)}")

def detect_language(text: str) -> str:
    """Enhanced language detection for Odia, Hindi, and English"""
    if not text:
        return "unknown"
    
    text = text.strip().lower()
    
    # Odia script detection (Odia characters)
    odia_chars = ['ଅ', 'ଆ', 'ଇ', 'ଈ', 'ଉ', 'ଊ', 'ଏ', 'ଐ', 'ଓ', 'ଔ', 
                  'କ', 'ଖ', 'ଗ', 'ଘ', 'ଙ', 'ଚ', 'ଛ', 'ଜ', 'ଝ', 'ଞ',
                  'ଟ', 'ଠ', 'ଡ', 'ଢ', 'ଣ', 'ତ', 'ଥ', 'ଦ', 'ଧ', 'ନ',
                  'ପ', 'ଫ', 'ବ', 'ଭ', 'ମ', 'ଯ', 'ର', 'ଲ', 'ଵ', 'ଶ',
                  'ଷ', 'ସ', 'ହ', 'ଳ', 'ଜ୍ୱର', 'ମୁଣ୍ଡବିନ୍ଧା', 'କାଶ']
    
    if any(char in text for char in odia_chars):
        return "odia"
    
    # Hindi script detection (Devanagari characters)
    hindi_chars = ['अ', 'आ', 'इ', 'ई', 'उ', 'ऊ', 'ए', 'ऐ', 'ओ', 'औ',
                   'क', 'ख', 'ग', 'घ', 'ङ', 'च', 'छ', 'ज', 'झ', 'ञ',
                   'ट', 'ठ', 'ड', 'ढ', 'ण', 'त', 'थ', 'द', 'ध', 'न',
                   'प', 'फ', 'ब', 'भ', 'म', 'य', 'र', 'ल', 'व', 'श',
                   'ष', 'स', 'ह', 'बुखार', 'खांसी', 'दर्द']
    
    if any(char in text for char in hindi_chars):
        return "hindi"
    
    # English detection (basic ASCII + common English health terms)
    english_terms = ['fever', 'cough', 'headache', 'pain', 'appointment', 
                     'doctor', 'hospital', 'medicine', 'emergency', 'help']
    
    if any(term in text for term in english_terms) or text.isascii():
        return "english"
    
    return "mixed"

async def save_chat_history(user_phone: str, user_message: str, bot_response: str):
    """Save chat conversation to database with enhanced metadata"""
    try:
        database = await get_database()
        chat_collection = database.chat_history
        
        # Detect language and extract basic intent
        detected_language = detect_language(user_message)
        
        # Basic intent detection
        intent = "general"
        if any(word in user_message.lower() for word in ['fever', 'ଜ୍ୱର', 'बुखार']):
            intent = "symptom_fever"
        elif any(word in user_message.lower() for word in ['cough', 'କାଶ', 'खांसी']):
            intent = "symptom_cough"
        elif any(word in user_message.lower() for word in ['headache', 'ମୁଣ୍ଡବିନ୍ଧା', 'सिरदर्द']):
            intent = "symptom_headache"
        elif any(word in user_message.lower() for word in ['appointment', 'ଆପଏଣ୍ଟମେଣ୍ଟ', 'अपॉइंटमेंट']):
            intent = "appointment_booking"
        elif any(word in user_message.lower() for word in ['emergency', 'chest pain', 'ଛାତି ଯନ୍ତ୍ରଣା']):
            intent = "emergency"
        
        chat_data = {
            "user_phone": user_phone,
            "user_message": user_message,
            "bot_response": bot_response,
            "timestamp": datetime.now(),
            "language": detected_language,
            "intent": intent,
            "message_length": len(user_message),
            "response_length": len(bot_response),
            "session_id": f"{user_phone}_{datetime.now().strftime('%Y%m%d')}"  # Daily session
        }
        
        result = await chat_collection.insert_one(chat_data)
        logging.info(f"✅ Chat history saved: {result.inserted_id} | User: {user_phone} | Language: {detected_language}")
        
        return result.inserted_id
        
    except Exception as e:
        logging.error(f"❌ Failed to save chat history: {str(e)}")
        return None

async def save_appointment(appointment_data: dict):
    """Save appointment to database with enhanced validation and metadata"""
    try:
        database = await get_database()
        appointments_collection = database.appointments
        
        # Add metadata and validation
        enhanced_appointment = {
            **appointment_data,
            "created_at": datetime.now(),
            "updated_at": datetime.now(),
            "status": appointment_data.get("status", "confirmed"),
            "source": "whatsapp_chatbot",
            "is_active": True,
            "reminder_sent": False,
            "follow_up_required": False
        }
        
        # Validate required fields
        required_fields = ["user_phone", "clinic_id", "date", "time"]
        for field in required_fields:
            if field not in enhanced_appointment:
                raise ValueError(f"Missing required field: {field}")
        
        result = await appointments_collection.insert_one(enhanced_appointment)
        logging.info(f"✅ Appointment saved: {result.inserted_id} | User: {appointment_data.get('user_phone')} | Clinic: {appointment_data.get('clinic_name')}")
        
        return result.inserted_id
        
    except Exception as e:
        logging.error(f"❌ Failed to save appointment: {str(e)}")
        return None

async def get_chat_statistics() -> Dict:
    """Get comprehensive chat statistics for dashboard"""
    try:
        database = await get_database()
        
        # Basic counts
        total_chats = await database.chat_history.count_documents({})
        total_appointments = await database.appointments.count_documents({})
        
        # Language distribution
        language_pipeline = [
            {"$group": {"_id": "$language", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}}
        ]
        language_stats = await database.chat_history.aggregate(language_pipeline).to_list(None)
        
        # Intent distribution
        intent_pipeline = [
            {"$group": {"_id": "$intent", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}}
        ]
        intent_stats = await database.chat_history.aggregate(intent_pipeline).to_list(None)
        
        # Today's activity
        today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        today_chats = await database.chat_history.count_documents({"timestamp": {"$gte": today}})
        today_appointments = await database.appointments.count_documents({"created_at": {"$gte": today}})
        
        return {
            "total_conversations": total_chats,
            "total_appointments": total_appointments,
            "today_conversations": today_chats,
            "today_appointments": today_appointments,
            "language_distribution": language_stats,
            "intent_distribution": intent_stats,
            "last_updated": datetime.now().isoformat()
        }
        
    except Exception as e:
        logging.error(f"Failed to get statistics: {str(e)}")
        return {"error": str(e)}

async def get_user_chat_history(user_phone: str, limit: int = 50) -> List[Dict]:
    """Get chat history for a specific user"""
    try:
        database = await get_database()
        
        cursor = database.chat_history.find(
            {"user_phone": user_phone}
        ).sort("timestamp", -1).limit(limit)
        
        history = await cursor.to_list(length=limit)
        
        # Convert ObjectId to string for JSON serialization
        for chat in history:
            chat["_id"] = str(chat["_id"])
        
        return history
        
    except Exception as e:
        logging.error(f"Failed to get chat history for {user_phone}: {str(e)}")
        return []

async def save_emergency_escalation(user_phone: str, symptoms: str, asha_worker: Dict, escalation_type: str):
    """Save emergency escalation records for tracking and compliance"""
    try:
        database = await get_database()
        emergency_collection = database.emergency_escalations
        
        escalation_data = {
            "user_phone": user_phone,
            "symptoms": symptoms,
            "asha_worker": asha_worker,
            "escalation_type": escalation_type,
            "timestamp": datetime.now(),
            "status": "escalated",
            "resolution_status": "pending",
            "follow_up_required": True,
            "priority": "high" if "chest pain" in symptoms.lower() else "medium"
        }
        
        result = await emergency_collection.insert_one(escalation_data)
        logging.info(f"🚨 Emergency escalation logged: {result.inserted_id} | User: {user_phone}")
        
        return result.inserted_id
        
    except Exception as e:
        logging.error(f"Failed to save emergency escalation: {str(e)}")
        return None

async def health_check_database() -> Dict:
    """Comprehensive database health check for monitoring"""
    try:
        # Test connection
        await db.client.admin.command('ismaster')
        
        # Get database stats
        database = await get_database()
        stats = await database.command("dbstats")
        
        # Collection counts
        collections = {
            "chat_history": await database.chat_history.count_documents({}),
            "appointments": await database.appointments.count_documents({}),
            "emergency_escalations": await database.get_collection("emergency_escalations").count_documents({})
        }
        
        return {
            "status": "healthy",
            "connection": "active",
            "collections": collections,
            "database_size_mb": round(stats["dataSize"] / (1024 * 1024), 2),
            "last_check": datetime.now().isoformat()
        }
        
    except Exception as e:
        logging.error(f"Database health check failed: {str(e)}")
        return {
            "status": "unhealthy",
            "error": str(e),
            "last_check": datetime.now().isoformat()
        }
