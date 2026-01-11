# 🚦 Person A - SMS-only interface
from fastapi import APIRouter, Form, Response
from twilio.twiml.messaging_response import MessagingResponse
from decouple import config
from app.db.db import save_chat_history
import logging

router = APIRouter()

# Simple FAQ data (can reuse from WhatsApp)
FAQ_DATA = {
    "fever": "🌡️ Fever: Rest, fluids, paracetamol. See doctor if fever >101°F for 3+ days.",
    "cough": "😷 Cough: Warm water, steam inhalation. See doctor if persistent >2 weeks.",
    "help": "🏥 SWASTHYA SETU - I can help with health queries, appointments, emergencies. Type symptom or 'appointment'."
}

@router.post("/webhook")
async def sms_webhook(From: str = Form(...), Body: str = Form(...)):
    try:
        user_message = Body.strip().lower()
        user_phone = From
        logging.info(f"📞 Received SMS from {user_phone}: {Body}")

        # Match keywords
        response_text = FAQ_DATA.get(user_message, FAQ_DATA["help"])

        # Save chat history
        await save_chat_history(user_phone, Body, response_text)
        logging.info("💾 Chat history saved successfully")

        # Create Twilio SMS response
        resp = MessagingResponse()
        resp.message(response_text)
        return Response(content=str(resp), media_type="application/xml")

    except Exception as e:
        logging.error(f"❌ SMS webhook error: {str(e)}")
        resp = MessagingResponse()
        resp.message("Sorry, technical issue. Try again later or call 108 for emergencies.")
        return Response(content=str(resp), media_type="application/xml")
